#!/usr/bin/env python3
"""
validate_suite_integrity.py — Programmatic verification script to check path references and
format specifications for the ver-3 Master Skill Suite.

Usage:
    python3 validate_suite_integrity.py
"""

import sys
import os
import re
from pathlib import Path

# Base directories
SUITE_ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = SUITE_ROOT / "_shared"

SKILLS = [
    "skill-explorer",
    "skill-knowledge-miner",
    "skill-architect",
    "production-quality-gatekeeper",
    "skill-planner",
    "skill-builder",
    "production-code-reviewer"
]

def check_file_path(base_dir, relative_str):
    # Try resolving relative path based on file directory
    clean_str = relative_str.strip().strip("'").strip('"')
    
    # Ignore absolute system environment variables
    if clean_str.startswith("${CLAUDE_SKILL_DIR}"):
        clean_str = clean_str.replace("${CLAUDE_SKILL_DIR}", "")
        
    if not clean_str:
        return True, ""
        
    target_path = Path(base_dir) / clean_str
    if target_path.exists():
        return True, str(target_path.resolve())
    return False, str(target_path)

def analyze_skill_markdown(skill_name):
    skill_dir = SUITE_ROOT / skill_name
    skill_file = skill_dir / "SKILL.md"
    
    if not skill_file.exists():
        return {
            "name": skill_name,
            "status": "MISSING",
            "errors": [f"Tệp SKILL.md không tồn tại tại {skill_file}"]
        }
        
    content = skill_file.read_text(encoding="utf-8")
    errors = []
    warnings = []
    
    # 1. XML Boundaries
    for tag in ["instructions", "context", "output_contract"]:
        if f"<{tag}>" not in content or f"</{tag}>" not in content:
            errors.append(f"Thiếu thẻ XML ranh giới ngữ nghĩa: <{tag}> hoặc </{tag}>.")
            
    # 2. must/must_not YAML block in instructions
    if "<instructions>" in content:
        instr_match = re.search(r"<instructions>(.*?)</instructions>", content, re.DOTALL)
        if instr_match:
            instr_text = instr_match.group(1).lower()
            if "must:" not in instr_text and "must_not:" not in instr_text:
                errors.append("Khối <instructions> thiếu phân cấp YAML 'must:' hoặc 'must_not:'.")
                
    # 3. Path references inside boot sequence or progressive disclosure
    # Find all path-like strings (e.g. ../_shared/..., knowledge/..., templates/...)
    paths = re.findall(r"[`'\"]?(\.\.?/[a-zA-Z_0-9\-\.\/_]+|knowledge/[a-zA-Z_0-9\-\.\/_]+|templates/[a-zA-Z_0-9\-\.\/_]+|scripts/[a-zA-Z_0-9\-\.\/_]+|data/[a-zA-Z_0-9\-\.\/_]+|loop/[a-zA-Z_0-9\-\.\/_]+)[`'\"]?", content)
    for p in paths:
        # Ignore extensionless references or template values like {skill-name}
        if "{skill-name}" in p:
            continue
        # Ignore prose examples in planners or dynamic runtime outputs
        if p in ["data/config.yaml", "data/schema.json", "knowledge/domain-handbook.md", "data/quality-matrix.yaml"]:
            continue
        exists, resolved = check_file_path(skill_dir, p)
        if not exists:
            # Check if it refers to context directories which will be created dynamically
            if ".skill-context" in p or "resources/" in p:
                continue
            errors.append(f"Liên kết tham chiếu hỏng (Broken link): '{p}' không tồn tại.")

    return {
        "name": skill_name,
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings
    }

def main():
    print("=====================================================================")
    print("🔄 PROGRAMMATIC INTEGRITY CHECKER FOR MASTER SKILL SUITE ver-3")
    print("=====================================================================")
    
    suite_errors = 0
    
    # Check 6 Skills
    for skill in SKILLS:
        result = analyze_skill_markdown(skill)
        print(f"Skill: {result['name']} -> Verdict: {'✅ PASS' if result['status'] == 'PASS' else '❌ FAIL'}")
        if result["errors"]:
            for err in result["errors"]:
                print(f"  - Error: {err}")
            suite_errors += len(result["errors"])
        if result["warnings"]:
            for warn in result["warnings"]:
                print(f"  - Warning: {warn}")
        print("-" * 69)
        
    # Check _shared directory existence
    if not SHARED_DIR.exists():
        print("❌ FAIL: Thư mục _shared không tồn tại!")
        suite_errors += 1
    else:
        print("✅ PASS: Thư mục _shared tồn tại.")
        # Check standard files in shared
        for f in ["knowledge/framework.md", "knowledge/case-system.md"]:
            p = SHARED_DIR / f
            if p.exists():
                print(f"  - Found: _shared/{f}")
            else:
                print(f"  - Error: Thiếu tệp _shared/{f} quan trọng!")
                suite_errors += 1

    print("=====================================================================")
    print(f"📊 SUMMARY OF SUITE INTEGRITY: {suite_errors} Errors Found")
    print("=====================================================================")
    sys.exit(1 if suite_errors > 0 else 0)

if __name__ == "__main__":
    main()
