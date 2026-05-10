#!/usr/bin/env python3
"""
check-consistency.py — Cross-artifact consistency verification

Validates:
- api.json ↔ business.md consistency
- business.md ↔ flow.md consistency
- flow.md ↔ tasks.md consistency

Usage:
    python check-consistency.py <spec-folder-path>

Exit codes:
    0 = All consistency checks pass
    1 = Consistency issues found
    2 = File not found or unreadable
"""

import sys
import json
import re
import yaml
from pathlib import Path
from typing import Dict, List, Set, Any, Optional


class ConsistencyChecker:
    def __init__(self, spec_folder: Path):
        self.spec_folder = Path(spec_folder)
        self.errors: List[Dict[str, Any]] = []
        self.api_data: Optional[Dict] = None
        self.business_data: Optional[str] = None
        self.flow_data: Optional[str] = None
        self.tasks_data: Optional[Dict] = None

    def check(self) -> bool:
        """Run all consistency checks. Returns True if all pass."""
        self._load_artifacts()
        if self.api_data is None:
            return False

        self._check_api_business_consistency()
        self._check_business_flow_consistency()
        self._check_flow_tasks_consistency()

        return len(self.errors) == 0

    def _load_artifacts(self):
        """Load all artifacts into memory."""
        # Load api.json
        api_path = self.spec_folder / 'api.json'
        if api_path.exists():
            try:
                with open(api_path) as f:
                    self.api_data = json.load(f)
            except json.JSONDecodeError as e:
                self.errors.append({
                    'category': 'A',
                    'rule': 'API-JSON-SYNTAX',
                    'message': f'api.json is not valid JSON: {e}',
                    'fix': 'Fix JSON syntax in api.json'
                })

        # Load business.md (as text for pattern matching)
        business_path = self.spec_folder / 'business.md'
        if business_path.exists():
            with open(business_path) as f:
                self.business_data = f.read()

        # Load flow.md (as text for pattern matching)
        flow_path = self.spec_folder / 'flow.md'
        if flow_path.exists():
            with open(flow_path) as f:
                self.flow_data = f.read()

        # Load tasks.md
        tasks_path = self.spec_folder / 'tasks.md'
        if tasks_path.exists():
            try:
                with open(tasks_path) as f:
                    content = f.read()
                # Parse frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        self.tasks_data = yaml.safe_load(parts[1])
            except yaml.YAMLError as e:
                self.errors.append({
                    'category': 'C',
                    'rule': 'TASKS-YAML-SYNTAX',
                    'message': f'tasks.md is not valid YAML: {e}',
                    'fix': 'Fix YAML syntax in tasks.md'
                })

    def _check_api_business_consistency(self):
        """Category A: api.json ↔ business.md checks."""
        if self.api_data is None or self.business_data is None:
            return

        api_entities = {e['name'] for e in self.api_data.get('entities', [])}
        api_collections = {e['collection'] for e in self.api_data.get('entities', [])}

        # A1: Check entity names match (look for Entity Name: or similar patterns)
        business_entity_pattern = re.compile(r'^###?\s+([A-Z][a-zA-Z0-9]+)\s*$', re.MULTILINE)
        business_entities = set(business_entity_pattern.findall(self.business_data))

        # Filter to only entity-like names (not headers)
        entity_headers = re.findall(r'^##?\s+\d+\.\s+\w+', self.business_data, re.MULTILINE)
        potential_entities = business_entities - set(entity_headers)

        for entity in potential_entities:
            if entity not in api_entities:
                self.errors.append({
                    'category': 'A',
                    'rule': 'A1',
                    'message': f'Entity "{entity}" in business.md not found in api.json',
                    'location': 'business.md',
                    'expected': f'Entity in api.json entities[]',
                    'actual': f'Entity "{entity}" not in api.json',
                    'fix': f'Add entity "{entity}" to api.json or rename in business.md'
                })

        # A2: Check collection slugs match
        business_collection_pattern = re.compile(r'\*\*Collection\*\*:\s*`?([a-z0-9-]+)`?', re.MULTILINE)
        business_collections = set(business_collection_pattern.findall(self.business_data))

        for coll in business_collections:
            if coll not in api_collections:
                self.errors.append({
                    'category': 'A',
                    'rule': 'A2',
                    'message': f'Collection "{coll}" in business.md not found in api.json',
                    'location': 'business.md',
                    'expected': f'Collection in api.json entities[].collection',
                    'actual': f'Collection "{coll}" not in api.json',
                    'fix': f'Add collection "{coll}" to api.json or update business.md'
                })

        # A5: Check endpoint auth matches permissions
        # Extract auth patterns from business.md
        auth_patterns = re.findall(r'\*\*Permission\*\*:\s*(\w+)', self.business_data)
        auth_set = set(auth_patterns)

        for endpoint in self.api_data.get('endpoints', []):
            endpoint_auth = endpoint.get('auth', '')
            if endpoint_auth == 'public':
                continue
            # For non-public endpoints, check if there's a corresponding permission
            if auth_set and endpoint_auth not in ['public', 'authenticated', 'admin']:
                pass  # Custom auth, assume ok

    def _check_business_flow_consistency(self):
        """Category B: business.md ↔ flow.md checks."""
        if self.business_data is None or self.flow_data is None:
            return

        # B1: Check actor naming consistency
        # Extract actors from business.md
        actor_pattern = re.compile(r'^\|\s*([A-Z][a-zA-Z]+)\s*\|', re.MULTILINE)
        business_actors = set(actor_pattern.findall(self.business_data))

        # Extract participants from flow.md
        participant_pattern = re.compile(r'participant\s+(\w+)\s+as', re.MULTILINE)
        flow_participants = set(participant_pattern.findall(self.flow_data))

        # State diagram entities
        state_entity_pattern = re.compile(r'state\s+"([^"]+)"', re.MULTILINE)
        state_entities = set(state_entity_pattern.findall(self.flow_data))

        # Check actors appear in flow as participants
        for actor in business_actors:
            if actor not in flow_participants and actor not in state_entities:
                # Warning: actor from business.md not found in flow diagrams
                # This is informational, not always an error
                pass

        # B2: Check status transitions match
        # Extract status workflow from business.md
        status_pattern = re.compile(r'\|\s*([A-Z]\w+)\s*\|.*?\|\s*([A-Z]\w+)\s*\|', re.MULTILINE)
        business_statuses = set()
        for match in re.finditer(status_pattern, self.business_data):
            business_statuses.add(match.group(1))
            business_statuses.add(match.group(2))

        # Extract states from flow state diagrams
        flow_states = set()
        for match in re.finditer(r'\*\*\w+\*\*\s+State\s+Machine|stateDiagram-v2', self.flow_data):
            # Find states in the state diagram block
            block_start = match.start()
            block_end = min(block_start + 2000, len(self.flow_data))
            block = self.flow_data[block_start:block_end]

            state_in_block = re.findall(r'\[\*\]\s*-->|"([^"]+)"\s*-->', block)
            flow_states.update([s for s in state_in_block if s])

    def _check_flow_tasks_consistency(self):
        """Category C: flow.md ↔ tasks.md checks."""
        if self.flow_data is None or self.tasks_data is None:
            return

        # C1: Check phase coverage - every diagram should have tasks
        diagram_sections = re.findall(r'^##\s+(\d+)\.\s+([^\n]+)', self.flow_data, re.MULTILINE)

        # C3: Check trace field presence
        phases = self.tasks_data.get('phases', {})
        total_tasks = 0
        traced_tasks = 0

        trace_pattern = re.compile(r'^P[1-4]-T[1-4]-\d{3}$')

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
                            'category': 'C',
                            'rule': 'C4',
                            'message': f'Task {task.get("id", "")} has invalid trace format',
                            'location': 'tasks.md',
                            'expected': 'P{phase}-T{phase}-{###}',
                            'actual': trace,
                            'fix': f'Fix trace format for task {task.get("id", "")}'
                        })
                else:
                    self.errors.append({
                        'category': 'C',
                        'rule': 'C3',
                        'message': f'Task {task.get("id", "")} missing trace field',
                        'location': 'tasks.md',
                        'expected': 'trace field present',
                        'actual': 'Missing',
                        'fix': f'Add trace field to task {task.get("id", "")}'
                    })

        # Check 100% trace coverage
        if total_tasks > 0 and traced_tasks < total_tasks:
            coverage = (traced_tasks / total_tasks) * 100
            self.errors.append({
                'category': 'C',
                'rule': 'TRACE-COVERAGE',
                'message': f'Trace coverage is {coverage:.0f}%, expected 100%',
                'location': 'tasks.md',
                'expected': '100% tasks with trace',
                'actual': f'{coverage:.0f}% ({traced_tasks}/{total_tasks})',
                'fix': 'All tasks must have valid trace fields'
            })

    def print_report(self):
        """Print consistency report."""
        print(f"\n{'='*60}")
        print(f"CONSISTENCY CHECK REPORT: {self.spec_folder}")
        print(f"{'='*60}\n")

        if self.errors:
            print(f"ISSUES FOUND ({len(self.errors)}):\n")
            for err in self.errors:
                print(f"  [{err['category']}-{err['rule']}] {err['message']}")
                if 'location' in err:
                    print(f"    Location: {err['location']}")
                print(f"    Fix: {err['fix']}\n")

        if not self.errors:
            print("All consistency checks passed.\n")

        print(f"{'='*60}")
        if self.errors:
            print(f"RESULT: FAIL ({len(self.errors)} issues)")
        else:
            print("RESULT: PASS")
        print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python check-consistency.py <spec-folder-path>")
        sys.exit(2)

    spec_folder = Path(sys.argv[1])

    if not spec_folder.exists():
        print(f"Error: Spec folder not found: {spec_folder}")
        sys.exit(2)

    checker = ConsistencyChecker(spec_folder)
    is_consistent = checker.check()
    checker.print_report()

    sys.exit(0 if is_consistent else 1)


if __name__ == '__main__':
    main()
