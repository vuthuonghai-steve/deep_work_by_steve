#!/usr/bin/env python3
"""
scripts/validate.py — Sandbox and Schema Validator Engine.

This script loads distilled tri-format knowledge artifacts, verifies their YAML schemas,
counts tokens against layer budgets, scans content for dangerous shell injection patterns,
and executes code test suites inside a networkless Docker sandbox with gVisor.

If Docker is not running or available, it gracefully falls back to local static validation
with a clear warning.
"""

import os
import sys
import re
import yaml
import subprocess
import shutil
import tempfile
from datetime import datetime, timezone

# --- CONFIGURATION & LIMITS ---
LAYER_LIMITS = {
    "L0": 400,
    "L1": 1200,
    "L2": 2500,
    "L3": 5000
}

FORBIDDEN_PATTERNS = [
    r"(^|[\s;&|])rm\s+-rf([\s;&|]|$)",
    r"(^|[\s;&|])curl([\s;&|]|$)",
    r"(^|[\s;&|])wget([\s;&|]|$)",
    r"(^|[\s;&|])chmod([\s;&|]|$)",
    r"(^|[\s;&|])chown([\s;&|]|$)",
    r"(^|[\s;&|])printenv([\s;&|]|$)",
    r"(^|[\s;&|])env([\s;&|]|$)",
    r"(^|[\s;&|])ssh([\s;&|]|$)",
    r"(^|[\s;&|])aws([\s;&|]|$)",
    r"/etc/passwd",
    r"/etc/shadow",
    r"~/\.ssh",
    r"~/\.aws",
    r"~/\.bashrc"
]

def print_log(level, msg):
    """Print formatted logs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

def count_tokens(text):
    """Estimate token count (fallback to simple character-based ratio if tiktoken missing)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        # Fallback: approximation (Vietnamese/English average 4 chars per token)
        return len(text) // 4

def check_docker_available():
    """Check if Docker daemon is running and responsive."""
    if not shutil.which("docker"):
        return False
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_gvisor_available():
    """Check if gVisor (runsc) runtime is configured in Docker."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5
        )
        return "runsc" in result.stdout
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def scan_shell_injection(content, item_id):
    """Perform static analysis on content to check for shell injection signatures."""
    violations = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(pattern)
    return violations

def validate_schema_and_budget(item):
    """Validate schema structure and token budgets of a single distilled item."""
    item_id = item.get("knowledge_id")
    if not item_id:
        return False, "Thiếu trường 'knowledge_id' bắt buộc."

    required_fields = ["knowledge_id", "layer", "format", "content", "confidence_score"]
    for field in required_fields:
        if field not in item:
            return False, f"[{item_id}] Thiếu trường bắt buộc '{field}'."

    layer = item["layer"]
    fmt = item["format"]
    content = item["content"]
    confidence = item["confidence_score"]

    if layer not in LAYER_LIMITS:
        return False, f"[{item_id}] Trường 'layer' phải là một trong {list(LAYER_LIMITS.keys())}."

    if fmt not in ["markdown", "yaml", "xml"]:
        return False, f"[{item_id}] Trường 'format' phải là 'markdown', 'yaml' hoặc 'xml'."

    if not isinstance(confidence, (int, float)) or not (0.0 <= confidence <= 1.0):
        return False, f"[{item_id}] Trường 'confidence_score' phải là số thực từ 0.0 đến 1.0."

    # Validate Token Budget
    tokens = count_tokens(content)
    limit = LAYER_LIMITS[layer]
    if tokens > limit:
        return False, f"[{item_id}] Vượt quá Token Budget lớp {layer}: {tokens} > {limit} tokens."

    # Anti-Injection Static Check
    injection_violations = scan_shell_injection(content, item_id)
    if injection_violations:
        return False, f"[{item_id}] Phát hiện mẫu câu lệnh nguy hiểm (Shell Injection): {injection_violations}."

    return True, {
        "knowledge_id": item_id,
        "layer": layer,
        "format": fmt,
        "tokens": tokens,
        "confidence_score": confidence,
        "status": "static_checked"
    }

def run_in_docker_sandbox(code_snippet):
    """Execute python code snippet inside a secure networkless Docker container."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write test code to a temp file
        test_file = os.path.join(tmpdir, "test_script.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(code_snippet)

        # Docker CLI command assembly
        cmd = ["docker", "run", "--rm", "--network", "none", "-m", "512m", "--cpus=0.5"]
        
        # Check and use gVisor runtime if available
        if check_gvisor_available():
            cmd.extend(["--runtime", "runsc"])
            print_log("INFO", "Sử dụng gVisor runtime (runsc) để cô lập bảo mật tuyệt đối.")
        else:
            print_log("WARNING", "gVisor (runsc) chưa được cài đặt trên Docker host. Fallback sang default runtime.")

        # Mount temp dir as Read-Only and run python script
        cmd.extend([
            "-v", f"{tmpdir}:/sandbox:ro",
            "python:3.9-slim",
            "python3", "/sandbox/test_script.py"
        ])

        try:
            print_log("INFO", "Khởi chạy Docker Sandbox biệt lập...")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            passed = result.returncode == 0
            logs = result.stdout + result.stderr
            return passed, logs
        except subprocess.TimeoutExpired:
            return False, "Lỗi: Thời gian chạy container vượt quá giới hạn 60 giây (Timeout)."
        except subprocess.SubprocessError as e:
            return False, f"Docker Execution Error: {str(e)}"

def main():
    workspace_dir = os.environ.get("WORKSPACE_DIR", "/home/steve/Work-space/deep_work_by_steve")
    draft_file = os.path.join(workspace_dir, "data/distilled_draft.yaml")
    output_file = os.path.join(workspace_dir, "data/validated_artifacts.yaml")

    # Fallback to local paths if directories do not exist
    os.makedirs(os.path.dirname(draft_file), exist_ok=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print_log("INFO", f"=== Khởi động Sandbox Validator Engine ===")
    print_log("INFO", f"Đọc tệp nháp: {draft_file}")

    if not os.path.exists(draft_file):
        print_log("WARNING", "Không tìm thấy data/distilled_draft.yaml. Tiến hành tạo tệp mock draft để kiểm thử.")
        # Create mock draft if not exists for self-verification
        mock_data = {
            "artifacts": [
                {
                    "knowledge_id": "secure-docker-standards",
                    "layer": "L0",
                    "format": "markdown",
                    "content": "# Cấu hình Docker an toàn\nLuôn sử dụng runtime gVisor.",
                    "confidence_score": 0.95
                },
                {
                    "knowledge_id": "mock-python-snippet",
                    "layer": "L3",
                    "format": "xml",
                    "content": "<example_code>\nprint('Hello from Sandbox!')\n</example_code>",
                    "confidence_score": 0.90,
                    "test_code": "print('Unit test execution verified inside Sandbox!')"
                }
            ]
        }
        with open(draft_file, "w", encoding="utf-8") as f:
            yaml.dump(mock_data, f, default_flow_style=False, allow_unicode=True)

    try:
        with open(draft_file, "r", encoding="utf-8") as f:
            draft_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print_log("ERROR", f"Lỗi cú pháp YAML trong tệp draft: {e}")
        sys.exit(1)

    if not draft_data or "artifacts" not in draft_data:
        print_log("ERROR", "Không tìm thấy danh sách 'artifacts' trong tệp nháp.")
        sys.exit(1)

    docker_ok = check_docker_available()
    if not docker_ok:
        print_log("WARNING", "Docker daemon không chạy hoặc không có quyền truy cập. Chuyển sang LOCAL FALLBACK MODE.")
        print_log("WARNING", "Trong Local Fallback Mode, chỉ tiến hành Static Linting, KHÔNG thực thi mã nguồn.")

    validated_results = []
    has_errors = False

    for item in draft_data["artifacts"]:
        item_id = item.get("knowledge_id", "Unknown")
        print_log("INFO", f"Kiểm định thực thể tri thức: {item_id}...")

        # 1. Static and Schema checks
        success, details = validate_schema_and_budget(item)
        if not success:
            print_log("ERROR", f"Kiểm định tĩnh THẤT BẠI cho {item_id}: {details}")
            has_errors = True
            continue
        
        # 2. Dynamic validation inside Docker sandbox
        if item.get("layer") == "L3" and "test_code" in item:
            if docker_ok:
                print_log("INFO", f"[{item_id}] Phát hiện mã unit test. Bắt đầu đưa vào Docker sandbox...")
                passed, logs = run_in_docker_sandbox(item["test_code"])
                if passed:
                    print_log("INFO", f"[{item_id}] Sandbox validation PASS.")
                    details["status"] = "sandbox_verified"
                    details["logs"] = logs.strip()
                else:
                    print_log("ERROR", f"[{item_id}] Sandbox validation FAIL. Logs:\n{logs}")
                    has_errors = True
                    continue
            else:
                print_log("WARNING", f"[{item_id}] Docker không khả dụng. Bỏ qua chạy unit test, chỉ đánh dấu static checked.")
                details["status"] = "static_checked_only"

        validated_results.append(details)

    # Output generation
    if has_errors:
        print_log("ERROR", "Quá trình kiểm định phát sinh lỗi nghiêm trọng. Dừng pipeline và KHÔNG xuất bản kết quả.")
        sys.exit(1)

    output_data = {
        "stage": "sandbox_validation",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "passed": True,
        "local_fallback_active": not docker_ok,
        "validated_artifacts": validated_results
    }

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(output_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print_log("INFO", f"Kết xuất thành công tệp kiểm định tại: {output_file}")
    except OSError as e:
        print_log("ERROR", f"Không thể ghi kết quả ra tệp validated_artifacts.yaml: {e}")
        sys.exit(1)

    print_log("INFO", "=== KIỂM ĐỊNH HOÀN TẤT THÀNH CÔNG ===")
    sys.exit(0)

if __name__ == "__main__":
    main()
