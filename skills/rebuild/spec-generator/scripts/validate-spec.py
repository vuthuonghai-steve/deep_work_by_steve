#!/usr/bin/env python3
"""
validate-spec.py — Validate spec completeness and schema compliance

Usage:
    python validate-spec.py <spec-folder-path>

Exit codes:
    0 = All validations pass
    1 = Validation errors found
    2 = File not found or unreadable
"""

import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any


class SpecValidator:
    def __init__(self, spec_folder: Path):
        self.spec_folder = Path(spec_folder)
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

    def validate(self) -> bool:
        """Run all validations. Returns True if all pass."""
        self._check_artifact_presence()
        if self.errors:
            return False

        self._validate_api_json()
        self._validate_tasks_md()
        self._check_schema_versions()
        self._check_trace_coverage()

        return len(self.errors) == 0

    def _check_artifact_presence(self):
        """Check all 4 required artifacts exist."""
        required = ['api.json', 'business.md', 'flow.md', 'tasks.md']
        for artifact in required:
            path = self.spec_folder / artifact
            if not path.exists():
                self.errors.append({
                    'id': f'PRESENCE-{artifact}',
                    'check': f'{artifact} exists',
                    'expected': 'File present',
                    'actual': 'File missing',
                    'fix': f'Create {artifact}'
                })

    def _validate_api_json(self):
        """Validate api.json against schema."""
        path = self.spec_folder / 'api.json'
        if not path.exists():
            return

        try:
            with open(path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append({
                'id': 'API-JSON-SYNTAX',
                'check': 'api.json is valid JSON',
                'expected': 'Valid JSON',
                'actual': f'JSON error: {e}',
                'fix': 'Fix JSON syntax in api.json'
            })
            return

        # Check required fields
        required_fields = ['spec_version', 'feature', 'engine', 'entities', 'endpoints']
        for field in required_fields:
            if field not in data:
                self.errors.append({
                    'id': 'API-JSON-REQUIRED',
                    'check': f'api.json has {field}',
                    'expected': field,
                    'actual': 'Missing',
                    'fix': f'Add {field} to api.json'
                })

        # Check spec_version value
        if 'spec_version' in data and data['spec_version'] != '2.0.0':
            self.errors.append({
                'id': 'API-JSON-VERSION',
                'check': 'spec_version is 2.0.0',
                'expected': '2.0.0',
                'actual': data['spec_version'],
                'fix': 'Update spec_version to 2.0.0'
            })

        # Check entities array
        if 'entities' in data:
            if not isinstance(data['entities'], list):
                self.errors.append({
                    'id': 'API-JSON-ENTITIES',
                    'check': 'entities is array',
                    'expected': 'array',
                    'actual': type(data['entities']).__name__,
                    'fix': 'entities must be an array'
                })
            elif len(data['entities']) == 0:
                self.errors.append({
                    'id': 'API-JSON-ENTITIES-EMPTY',
                    'check': 'entities has items',
                    'expected': 'min 1 entity',
                    'actual': '0 entities',
                    'fix': 'Add at least 1 entity'
                })

        # Check endpoints array
        if 'endpoints' in data:
            if not isinstance(data['endpoints'], list):
                self.errors.append({
                    'id': 'API-JSON-ENDPOINTS',
                    'check': 'endpoints is array',
                    'expected': 'array',
                    'actual': type(data['endpoints']).__name__,
                    'fix': 'endpoints must be an array'
                })
            elif len(data['endpoints']) == 0:
                self.errors.append({
                    'id': 'API-JSON-ENDPOINTS-EMPTY',
                    'check': 'endpoints has items',
                    'expected': 'min 1 endpoint',
                    'actual': '0 endpoints',
                    'fix': 'Add at least 1 endpoint'
                })
            else:
                # Check each endpoint has trace field
                for i, endpoint in enumerate(data['endpoints']):
                    if 'trace' not in endpoint:
                        self.errors.append({
                            'id': f'API-JSON-ENDPOINT-{i}-TRACE',
                            'check': f'endpoint[{i}] has trace',
                            'expected': 'trace field present',
                            'actual': 'Missing trace',
                            'fix': f'Add trace field to endpoint {i}'
                        })
                    elif not endpoint['trace'].startswith('P1-'):
                        self.errors.append({
                            'id': f'API-JSON-ENDPOINT-{i}-TRACE-FORMAT',
                            'check': f'endpoint[{i}] trace format',
                            'expected': 'P1-{name}',
                            'actual': endpoint['trace'],
                            'fix': 'Trace must start with P1-'
                        })

    def _validate_tasks_md(self):
        """Validate tasks.md structure and trace coverage."""
        path = self.spec_folder / 'tasks.md'
        if not path.exists():
            return

        try:
            with open(path) as f:
                content = f.read()

            # Try to parse frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    meta = yaml.safe_load(parts[1])
                    data = meta if isinstance(meta, dict) else {}
                else:
                    data = {}
            else:
                data = {}

        except yaml.YAMLError as e:
            self.errors.append({
                'id': 'TASKS-YAML-SYNTAX',
                'check': 'tasks.md is valid YAML',
                'expected': 'Valid YAML',
                'actual': f'YAML error: {e}',
                'fix': 'Fix YAML syntax in tasks.md'
            })
            return

        # Check spec_version
        if 'spec_version' in data and data['spec_version'] != '2.0.0':
            self.errors.append({
                'id': 'TASKS-VERSION',
                'check': 'spec_version is 2.0.0',
                'expected': '2.0.0',
                'actual': data['spec_version'],
                'fix': 'Update spec_version to 2.0.0'
            })

        # Check phases exist
        if 'phases' not in data:
            self.errors.append({
                'id': 'TASKS-PHASES',
                'check': 'phases section exists',
                'expected': 'phases present',
                'actual': 'Missing',
                'fix': 'Add phases section to tasks.md'
            })
            return

        phases = data.get('phases', {})

        # Check required phases
        required_phases = ['phase_1', 'phase_2', 'phase_4']
        for phase in required_phases:
            if phase not in phases:
                self.errors.append({
                    'id': f'TASKS-{phase.upper()}',
                    'check': f'{phase} exists',
                    'expected': 'Phase present',
                    'actual': 'Missing',
                    'fix': f'Add {phase} section'
                })

    def _check_schema_versions(self):
        """Check schema versions across artifacts."""
        # api.json
        api_path = self.spec_folder / 'api.json'
        if api_path.exists():
            try:
                with open(api_path) as f:
                    data = json.load(f)
                if data.get('spec_version') != '2.0.0':
                    self.errors.append({
                        'id': 'VERSION-API',
                        'check': 'api.json version is 2.0.0',
                        'expected': '2.0.0',
                        'actual': data.get('spec_version', 'missing'),
                        'fix': 'Update api.json spec_version to 2.0.0'
                    })
            except:
                pass

    def _check_trace_coverage(self):
        """Check that all tasks have trace fields."""
        path = self.spec_folder / 'tasks.md'
        if not path.exists():
            return

        try:
            with open(path) as f:
                content = f.read()

            # Parse frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    meta = yaml.safe_load(parts[1])
                    if isinstance(meta, dict) and 'phases' in meta:
                        self._validate_trace_fields(meta['phases'])
        except:
            pass

    def _validate_trace_fields(self, phases: Dict):
        """Validate trace field presence and format."""
        task_pattern = re.compile(r'^T[1-4]-\d{3}$')
        trace_pattern = re.compile(r'^P[1-4]-T[1-4]-\d{3}$')

        total_tasks = 0
        traced_tasks = 0

        for phase_name, phase_data in phases.items():
            tasks = phase_data.get('tasks', [])
            for task in tasks:
                total_tasks += 1
                if 'trace' in task:
                    trace = task['trace']
                    if trace_pattern.match(trace):
                        traced_tasks += 1
                    else:
                        self.errors.append({
                            'id': f'TRACE-FORMAT-{task.get("id", "unknown")}',
                            'check': 'trace format valid',
                            'expected': 'P{phase}-T{phase}-{###}',
                            'actual': trace,
                            'fix': f'Fix trace format for task {task.get("id", "")}'
                        })
                else:
                    self.errors.append({
                        'id': f'TRACE-MISSING-{task.get("id", "unknown")}',
                        'check': 'task has trace field',
                        'expected': 'trace present',
                        'actual': 'Missing',
                        'fix': f'Add trace field to task {task.get("id", "")}'
                    })

        if total_tasks > 0 and traced_tasks < total_tasks:
            coverage = (traced_tasks / total_tasks) * 100
            self.warnings.append({
                'id': 'TRACE-COVERAGE',
                'check': 'trace coverage is 100%',
                'expected': '100%',
                'actual': f'{coverage:.0f}%',
                'fix': 'All tasks must have trace fields'
            })

    def print_report(self):
        """Print validation report."""
        print(f"\n{'='*60}")
        print(f"SPEC VALIDATION REPORT: {self.spec_folder}")
        print(f"{'='*60}\n")

        if self.errors:
            print(f"ERRORS ({len(self.errors)}):\n")
            for err in self.errors:
                print(f"  [{err['id']}] {err['check']}")
                print(f"    Expected: {err['expected']}")
                print(f"    Actual: {err['actual']}")
                print(f"    Fix: {err['fix']}\n")

        if self.warnings:
            print(f"WARNINGS ({len(self.warnings)}):\n")
            for warn in self.warnings:
                print(f"  [{warn['id']}] {warn['check']}")
                print(f"    Expected: {warn['expected']}")
                print(f"    Actual: {warn['actual']}\n")

        if not self.errors and not self.warnings:
            print("All validations passed.\n")

        print(f"{'='*60}")
        if self.errors:
            print(f"RESULT: FAIL ({len(self.errors)} errors)")
        elif self.warnings:
            print(f"RESULT: PASS with warnings ({len(self.warnings)})")
        else:
            print("RESULT: PASS")
        print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-spec.py <spec-folder-path>")
        sys.exit(2)

    spec_folder = Path(sys.argv[1])

    if not spec_folder.exists():
        print(f"Error: Spec folder not found: {spec_folder}")
        sys.exit(2)

    validator = SpecValidator(spec_folder)
    is_valid = validator.validate()
    validator.print_report()

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
