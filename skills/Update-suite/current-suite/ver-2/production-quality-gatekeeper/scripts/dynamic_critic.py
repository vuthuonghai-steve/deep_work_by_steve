#!/usr/bin/env python3
"""
dynamic_critic.py — Dynamic Quality Gates Critic Engine.
Evaluates python scripts against customized, synthesized gates from dynamic-gates.yaml.

Usage:
    python3 dynamic_critic.py --gates <dynamic-gates.yaml> --input <draft_file.py> --turn <turn_num>
"""

import sys
import re
import ast
import yaml
import argparse
from pathlib import Path
from datetime import datetime, timezone

class DynamicCritic:
    def __init__(self, content, file_path, gates):
        self.content = content
        self.file_path = Path(file_path)
        self.gates = gates
        self.results = {}
        self.failures = []

    def log_result(self, gate_id, passed, error_msg="", fix_hint=""):
        self.results[gate_id] = {
            "passed": passed,
            "name": self.gates[gate_id]["name"],
            "description": self.gates[gate_id]["description"],
            "severity": self.gates[gate_id]["severity"]
        }
        if not passed:
            self.results[gate_id]["error"] = error_msg
            self.results[gate_id]["fix_hint"] = fix_hint
            self.failures.append(gate_id)

    def run_evaluations(self):
        # 1. Parse AST
        try:
            tree = ast.parse(self.content)
            # Safe parent assignment
            for n in ast.walk(tree):
                for c in ast.iter_child_nodes(n):
                    if hasattr(c, "_fields") and len(c._fields) == 0:
                        continue
                    c.parent = n
        except SyntaxError as se:
            # Fatal syntax error flags compile check fail
            self.log_result("DEV-SEC-01", False, f"Lỗi biên dịch: {se.msg}", "Sửa lỗi cú pháp.")
            return

        # Collect basic structures
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]

        # Check synthesized gates in loop
        for gid, gate in self.gates.items():
            gtype = gate["type"]
            passed = True
            err = ""
            hint = gate["fix_hint"]

            if gtype == "ast_secret_check":
                secret_pass = True
                for assign in assigns:
                    for target in assign.targets:
                        if isinstance(target, ast.Name):
                            name = target.id.lower()
                            if any(s in name for s in ["api_key", "secret", "token", "password"]):
                                if isinstance(assign.value, ast.Constant) and isinstance(assign.value.value, str):
                                    val = assign.value.value
                                    if len(val) > 4 and not (val.startswith("${") or val.startswith("os.environ")):
                                        secret_pass = False
                                        err = f"Phát hiện gán cứng khóa bảo mật '{target.id}' trong code."
                                        break
                passed = secret_pass

            elif gtype == "ast_naming_snake":
                bad_names = [f.name for f in functions if not re.match(r"^[a-z_][a-z0-9_]*$", f.name)]
                passed = len(bad_names) == 0
                err = f"Tên hàm không snake_case: {', '.join(bad_names)}" if bad_names else ""

            elif gtype == "ast_naming_pascal":
                bad_names = [c.name for c in classes if not re.match(r"^[A-Z][a-zA-Z0-9]*$", c.name)]
                passed = len(bad_names) == 0
                err = f"Tên Class không PascalCase: {', '.join(bad_names)}" if bad_names else ""

            elif gtype == "ast_docstring_check":
                missing = []
                for f in functions:
                    if not f.name.startswith("_") and f.name not in ["__init__", "__str__", "__repr__"]:
                        if not ast.get_docstring(f):
                            missing.append(f.name)
                passed = len(missing) == 0
                err = f"Hàm public thiếu docstring: {', '.join(missing)}" if missing else ""

            elif gtype == "regex_check":
                pattern = gate["pattern"]
                match = re.search(pattern, self.content)
                passed = bool(match)
                err = f"Không tìm thấy ranh giới/logic bắt buộc khớp mẫu: '{pattern}'" if not passed else ""

            elif gtype == "regex_neg_check":
                pattern = gate["pattern"]
                # Exclude comment lines
                code_lines = [line.split("#")[0] for line in self.content.splitlines()]
                code_without_comments = "\n".join(code_lines)
                match = re.search(pattern, code_without_comments, re.IGNORECASE)
                passed = not bool(match)
                err = f"Phát hiện rò rỉ hoặc vi phạm an toàn khớp mẫu cấm: '{pattern}'" if not passed else ""

            self.log_result(gid, passed, err, hint)

def main():
    parser = argparse.ArgumentParser(description="Dynamic Critic Engine.")
    parser.add_argument("--gates", required=True, help="Synthesized gates path")
    parser.add_argument("--input", required=True, help="Input python draft file")
    parser.add_argument("--turn", type=int, default=1)
    
    args = parser.parse_args()
    
    gates_path = Path(args.gates)
    input_path = Path(args.input)
    
    if not gates_path.exists() or not input_path.exists():
        print("❌ Essential validation files not found.")
        sys.exit(2)
        
    gates = yaml.safe_load(gates_path.read_text(encoding="utf-8"))
    content = input_path.read_text(encoding="utf-8")
    
    critic = DynamicCritic(content, args.input, gates)
    critic.run_evaluations()
    
    total = len(critic.results)
    passed = total - len(critic.failures)
    percentage = int((passed / total) * 100) if total > 0 else 0
    
    report = {
        "status": "PASS" if not critic.failures else "FAIL",
        "file": args.input,
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "turn": args.turn,
        "stats": {
            "total": total,
            "passed": passed,
            "failed": len(critic.failures),
            "percentage": percentage
        },
        "results": critic.results,
        "failures": critic.failures
    }
    
    feedback_dir = Path(".skill-context/production-quality-gatekeeper")
    feedback_dir.mkdir(parents=True, exist_ok=True)
    feedback_file = feedback_dir / "feedback.yaml"
    feedback_file.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    
    print(f"\n--- ⚡ DYNAMIC QUALITY MASTER GATES EVALUATION ---")
    print(f"File: {args.input}")
    print(f"Turn: {args.turn} / 10")
    print(f"Gates Synthesized: {total} | Passed: {passed} | Failed: {len(critic.failures)} ({percentage}%)")
    print(f"Verdict: {'✅ PASS' if not critic.failures else '❌ FAIL'}")
    
    if critic.failures:
        print("\nFailed Business & Security Invariants (Must Fix):")
        for fid in critic.failures:
            print(f"- [{fid}] {critic.results[fid]['name']}: {critic.results[fid]['error']}")
            print(f"  Fix Hint: {critic.results[fid]['fix_hint']}")
        sys.exit(1)
    else:
        print("\n🏆 ALL DYNAMIC PRODUCTION GATES PASSED FLAWLESSLY!")
        sys.exit(0)

if __name__ == "__main__":
    main()
