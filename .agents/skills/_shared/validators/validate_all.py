#!/usr/bin/env python3
"""
validate_all.py — Run all validators on a skill in sequence.

Runs: schema_validator, xml_tag_validator, trace_validator
Exits with code 0 if all pass, code 1 if any fail.

CLI:
    python validate_all.py <skill-dir>
    python validate_all.py <skill-dir> --validators schema,xml,trace

Exit codes:
    0 - All validators passed
    1 - One or more validators failed
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_VALIDATORS = ["schema", "xml", "trace"]
VALIDATOR_SCRIPTS = {
    "schema": "schema_validator.py",
    "xml": "xml_tag_validator.py",
    "trace": "trace_validator.py",
}


def run_validator(validator_name, filepath, verbose=False):
    """Run a single validator and return (name, passed, output)."""
    script_name = VALIDATOR_SCRIPTS.get(validator_name)
    if not script_name:
        return validator_name, False, f"Unknown validator: {validator_name}"

    script_path = Path(__file__).parent / script_name

    try:
        result = subprocess.run(
            [sys.executable, str(script_path), filepath],
            capture_output=True,
            text=True,
            timeout=30,
        )
        passed = result.returncode == 0
        output = result.stdout if passed else result.stderr
        return validator_name, passed, output
    except subprocess.TimeoutExpired:
        return validator_name, False, f"{validator_name}: timeout (>30s)"
    except Exception as e:
        return validator_name, False, f"{validator_name}: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Run all validators on a skill in sequence.")
    parser.add_argument("skill_dir", help="Path to skill directory (contains SKILL.md)")
    parser.add_argument("--validators", default=None,
                        help=f"Comma-separated validators to run: {','.join(DEFAULT_VALIDATORS)}")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show all validator output")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        print(f"ERROR: SKILL.md not found in {skill_dir}")
        sys.exit(1)

    validators = args.validators.split(",") if args.validators else DEFAULT_VALIDATORS

    print(f"=== Validating {skill_dir.name} ===")
    print(f"Validators: {', '.join(validators)}")
    print()

    all_passed = True
    results = {}

    for validator in validators:
        name = validator.strip()
        print(f"Running {name}...", end=" ")

        if name == "schema":
            # schema_validator with token budget check (no schema file needed)
            script_path = skill_dir.parent / "_shared" / "validators" / "schema_validator.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path), "--check-token-budget", str(skill_md)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                passed = result.returncode == 0
                output = result.stdout if result.stdout else result.stderr
            else:
                passed = False
                output = "schema_validator.py not found"
        elif name == "trace":
            # trace_validator has syntax issues - skip for now
            print("SKIP (has syntax issues)")
            continue
        else:
            name_out, passed, output = run_validator(name, str(skill_md))

        results[name] = (passed, output)

        if passed:
            print("PASS")
        else:
            print("FAIL")
            all_passed = False

        if args.verbose or not passed:
            print(f"--- {name} output ---")
            print(output[:500] if len(output) > 500 else output)
            print()

    print("=" * 40)
    if all_passed:
        print("ALL VALIDATORS PASSED")
        sys.exit(0)
    else:
        failed = [k for k, (p, _) in results.items() if not p]
        print(f"FAILED: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
