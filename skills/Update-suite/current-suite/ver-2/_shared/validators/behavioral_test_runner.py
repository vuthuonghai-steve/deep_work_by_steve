#!/usr/bin/env python3
"""
behavioral_test_runner.py — High-fidelity Behavioral Test and Evaluation Runner.
Challenges ver-2 suite validators with flawed and corrected fixtures.
Proves that the QA system actually fails on errors and successfully passes on clean code.

Usage:
    python3 behavioral_test_runner.py
"""

import sys
import re
import subprocess
from pathlib import Path

# Relative resolving from _shared/validators/
SHARED_VALIDATORS = Path(__file__).resolve().parent
SUITE_ROOT = SHARED_VALIDATORS.parent.parent

# Sibling path resolving for running rebuilt code validators
GATEKEEPER_SCRIPTS = SUITE_ROOT / "production-quality-gatekeeper/scripts"
REVIEWER_SCRIPTS = SUITE_ROOT / "production-code-reviewer/scripts"

# Fixtures moved inside _shared/fixtures
FIXTURES_BAD = SUITE_ROOT / "_shared/fixtures/bad"
FIXTURES_GOOD = SUITE_ROOT / "_shared/fixtures/good"

def run_validator(command_args):
    try:
        res = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            check=False
        )
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)

def test_gatekeeper_behavior():
    print("\n--- TEST SCENARIO 1: production-quality-gatekeeper Behaviour ---")
    
    # 1. Challenge with FLAWED draft code (must fail!)
    bad_code = FIXTURES_BAD / "flawed_code.py"
    print(f"👉 Feeding FLAWED code: {bad_code.name}...")
    
    # Run the Gatekeeper loop_refiner in the ver-2 scripts (sibling path calls)
    code, out, err = run_validator([
        "python3",
        str(GATEKEEPER_SCRIPTS / "loop_refiner.py"),
        "--domain", "dev",
        "--input", str(bad_code),
        "--turn", "1"
    ])
    
    print(f"   Exit Code returned: {code} (Expect: 1 / FAIL)")
    if code == 1:
        print("   ✅ SUCCESS: Gatekeeper correctly rejected the flawed code!")
        # Print first few lines of failures
        failures = re.findall(r"- \[(.*?)\] (.*?)\.", out)
        for fid, msg in failures[:4]:
            print(f"      * Caught violation: [{fid}] {msg}")
    else:
        print("   ❌ FAIL: Gatekeeper failed to reject flawed code or crashed.")
        print(f"   Error: {err}\nStdout: {out}")
        return False

    # 2. Challenge with CORRECTED draft code (must pass!)
    good_code = FIXTURES_GOOD / "flawed_code.py"
    print(f"\n👉 Feeding CORRECTED code: {good_code.name}...")
    code, out, err = run_validator([
        "python3",
        str(GATEKEEPER_SCRIPTS / "loop_refiner.py"),
        "--domain", "dev",
        "--input", str(good_code),
        "--turn", "1"
    ])
    
    print(f"   Exit Code returned: {code} (Expect: 0 / PASS)")
    if code == 0:
        print("   ✅ SUCCESS: Gatekeeper correctly approved the clean code!")
    else:
        print("   ❌ FAIL: Gatekeeper rejected clean code.")
        print(f"   Error: {err}\nStdout: {out}")
        return False
        
    return True

def test_reviewer_behavior():
    print("\n--- TEST SCENARIO 2: production-code-reviewer Behaviour ---")
    
    # 1. Challenge static auditor with flawed code (must catch multiple issues!)
    bad_code = FIXTURES_BAD / "flawed_code.py"
    print(f"👉 Auditing FLAWED code: {bad_code.name}...")
    code, out, err = run_validator([
        "python3",
        str(REVIEWER_SCRIPTS / "code_auditor.py"),
        str(bad_code)
    ])
    
    print(f"   Exit Code returned: {code} (Expect: 1 / FAIL)")
    if code == 1:
        print("   ✅ SUCCESS: Code Reviewer static linter caught blocking issues!")
        # Extract issues
        issues = re.findall(r"- \[(.*?)\] (.*?) \(BLOCKING\)", out)
        for iid, name in issues:
            print(f"      * Blocking Issue: [{iid}] {name}")
    else:
        print("   ❌ FAIL: Reviewer linter did not catch blocking issues.")
        print(f"   Error: {err}\nStdout: {out}")
        return False

    # 2. Challenge static auditor with corrected code (must pass!)
    good_code = FIXTURES_GOOD / "flawed_code.py"
    print(f"\n👉 Auditing CORRECTED code: {good_code.name}...")
    code, out, err = run_validator([
        "python3",
        str(REVIEWER_SCRIPTS / "code_auditor.py"),
        str(good_code)
    ])
    
    print(f"   Exit Code returned: {code} (Expect: 0 / PASS)")
    if code == 0:
        print("   ✅ SUCCESS: Code Reviewer static linter approved corrected PEP8 code!")
    else:
        print("   ❌ FAIL: Reviewer linter rejected clean code.")
        print(f"   Error: {err}\nStdout: {out}")
        return False
        
    return True

def main():
    print("=====================================================================")
    print("🚀 BEHAVIORAL TEST RUNNER — CHALLENGING METRIC INTEGRITY GATES")
    print("=====================================================================")
    
    # Pre-run compilation audit
    res_code, res_out, res_err = run_validator([
        "python3",
        str(SHARED_VALIDATORS / "validate_suite_integrity.py")
    ])
    if res_code != 0:
        print("❌ FAIL: Cấu trúc hệ thống ver-2 bị lỗi liên kết hỏng trước khi chạy test.")
        sys.exit(1)
    
    print("✅ System Structural Sanity check passed.")
    
    # Run behavioral tests
    gatekeeper_ok = test_gatekeeper_behavior()
    reviewer_ok = test_reviewer_behavior()
    
    print("=====================================================================")
    if gatekeeper_ok and reviewer_ok:
        print("🏆 ALL BEHAVIORAL TESTS PASSED SUCCESSFULLY!")
        print("   - Validators proved to aggressively FAIL on bad code.")
        print("   - Validators proved to successfully PASS on clean PEP8 code.")
        print("   - No color fluff. Fully verified programmatic behavior.")
        sys.exit(0)
    else:
        print("❌ BEHAVIORAL TEST SUITE FAILED!")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    main()
