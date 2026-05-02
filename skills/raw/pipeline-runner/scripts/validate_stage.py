#!/usr/bin/env python3
"""
Validate stage output

Usage:
    python validate_stage.py <task-input.json>
"""

import sys
import json
import subprocess
from pathlib import Path


def validate_stage(task_input: dict) -> dict:
    """Run validation script and check exit code"""

    validation = task_input.get('validation', {})
    script = validation.get('script')
    expected_exit = validation.get('expected_exit_code', 0)
    required_outputs = validation.get('required_outputs', [])

    # Check required outputs exist
    missing = []
    for output_path in required_outputs:
        if not Path(output_path).exists():
            missing.append(output_path)

    if missing:
        return {
            'status': 'FAIL',
            'error': 'Missing outputs',
            'details': missing
        }

    # Run validation script if provided
    if script:
        try:
            result = subprocess.run(
                ['python', script],
                capture_output=True,
                timeout=60
            )
            exit_code = result.returncode

            if exit_code != expected_exit:
                return {
                    'status': 'FAIL',
                    'error': f'Validation script failed with exit code {exit_code}',
                    'stdout': result.stdout.decode(),
                    'stderr': result.stderr.decode()
                }

        except subprocess.TimeoutExpired:
            return {
                'status': 'FAIL',
                'error': 'Validation script timeout'
            }
        except Exception as e:
            return {
                'status': 'FAIL',
                'error': str(e)
            }

    return {
        'status': 'PASS',
        'validated_outputs': required_outputs
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_stage.py <task-input.json>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, 'r') as f:
        task_input = json.load(f)

    result = validate_stage(task_input)

    if result['status'] == 'PASS':
        print("✅ Validation passed")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
