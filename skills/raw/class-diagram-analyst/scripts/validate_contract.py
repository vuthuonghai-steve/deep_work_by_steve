#!/usr/bin/env python3
"""
validate_contract.py — Validate YAML Contract cho class-diagram-analyst

Usage:
    python scripts/validate_contract.py path/to/class-mX.yaml
    python scripts/validate_contract.py class-mX.yaml --project-root /path/to/project

Output: PASS/FAIL + violations list (stdout)

Source: design.md §4 Task 4.2, todo.md Task 4.2 [PORTABLE]
Dependencies: pyyaml>=6.0 (pip install pyyaml)
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML chưa được cài. Chạy: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Thêm scripts/ vào sys.path để import type_resolver
sys.path.insert(0, str(Path(__file__).parent))
from type_resolver import get_allowed_types


class ContractValidator:
    """Validate YAML Contract theo 5 điều kiện từ design.md §2.3 Guardrails."""

    def __init__(self, yaml_path: str, project_root: str | None = None):
        self.yaml_path = yaml_path
        self.project_root = project_root
        self.violations = []
        self.warnings = []
        self.allowed_types = get_allowed_types(project_root)

    def load_contract(self) -> dict:
        """Load và parse YAML Contract."""
        try:
            with open(self.yaml_path, encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"ERROR: File không tìm thấy: {self.yaml_path}", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"ERROR: YAML parse error: {e}", file=sys.stderr)
            sys.exit(1)

    def check_source_citations(self, contract: dict):
        """
        Check 1: Mọi field PHẢI có `source:` không rỗng.
        Vi phạm → BLOCK (Guardrail G1)
        """
        entities = contract.get('entities', [])
        for entity in entities:
            slug = entity.get('slug', 'unknown')
            fields = entity.get('fields', [])
            for field in fields:
                field_name = field.get('name', 'unknown')
                source = field.get('source', '')
                if not source or str(source).strip() == '':
                    self.violations.append(
                        f"[G1-CITATION] Entity '{slug}', field '{field_name}': "
                        f"thiếu source citation"
                    )

    def check_type_whitelist(self, contract: dict):
        """
        Check 2: Field type phải nằm trong allowed_field_types.
        Vi phạm → BLOCK (Guardrail G2)
        """
        entities = contract.get('entities', [])
        for entity in entities:
            slug = entity.get('slug', 'unknown')
            fields = entity.get('fields', [])
            for field in fields:
                field_name = field.get('name', 'unknown')
                field_type = field.get('type', '')
                if field_type and field_type not in self.allowed_types:
                    self.violations.append(
                        f"[G2-TYPE] Entity '{slug}', field '{field_name}': "
                        f"type '{field_type}' không hợp lệ. "
                        f"Allowed: {self.allowed_types}"
                    )

    def check_slug_unique(self, contract: dict):
        """
        Check 3: Không có duplicate entity slug.
        Vi phạm → BLOCK (Guardrail G3)
        """
        entities = contract.get('entities', [])
        slugs = [e.get('slug', '') for e in entities]
        seen = set()
        for slug in slugs:
            if slug in seen:
                self.violations.append(
                    f"[G3-SLUG] Duplicate entity slug: '{slug}'"
                )
            seen.add(slug)

    def check_aggregate_root_classification(self, contract: dict):
        """
        Check 4: Aggregate Root phân loại đúng (warning, không BLOCK).
        Guardrail G4 — Alert user.
        """
        entities = contract.get('entities', [])
        for entity in entities:
            slug = entity.get('slug', 'unknown')
            is_root = entity.get('aggregate_root', None)
            if is_root is None:
                self.warnings.append(
                    f"[G4-ROOT] Entity '{slug}': thiếu field 'aggregate_root'. "
                    f"Cần khai báo rõ true/false."
                )

    def check_locked_header(self, contract: dict):
        """
        Check 5: YAML Contract phải có LOCKED header (warning).
        """
        # Đọc raw file để check comment header
        with open(self.yaml_path, encoding='utf-8') as f:
            first_lines = f.read(500)

        if 'LOCKED CONTRACT' not in first_lines and 'DO NOT EDIT' not in first_lines:
            self.warnings.append(
                "[G5-LOCK] YAML Contract thiếu LOCKED header comment. "
                "Thêm: '# ⚠️ LOCKED CONTRACT — DO NOT EDIT MANUALLY.'"
            )

    def validate(self) -> tuple[bool, list[str], list[str]]:
        """
        Chạy tất cả 5 checks.
        Returns: (passed: bool, violations: list, warnings: list)
        """
        contract = self.load_contract()

        self.check_source_citations(contract)
        self.check_type_whitelist(contract)
        self.check_slug_unique(contract)
        self.check_aggregate_root_classification(contract)
        self.check_locked_header(contract)

        passed = len(self.violations) == 0
        return passed, self.violations, self.warnings

    def count_stats(self, contract: dict) -> dict:
        """Thống kê số lượng fields và assumptions."""
        total_fields = 0
        fields_with_source = 0
        fields_as_assumption = 0

        entities = contract.get('entities', [])
        for entity in entities:
            fields = entity.get('fields', [])
            total_fields += len(fields)
            for field in fields:
                source = field.get('source', '')
                if source and str(source).strip():
                    fields_with_source += 1
                assumption = field.get('assumption', False)
                if assumption:
                    fields_as_assumption += 1

        return {
            'total_entities': len(entities),
            'total_fields': total_fields,
            'fields_with_source': fields_with_source,
            'fields_as_assumption': fields_as_assumption,
        }


def main():
    parser = argparse.ArgumentParser(
        description='Validate YAML Contract cho class-diagram-analyst'
    )
    parser.add_argument('yaml_path', help='Path đến class-mX.yaml')
    parser.add_argument('--project-root', default=None, help='Project root để resolve types')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as violations')
    args = parser.parse_args()

    validator = ContractValidator(args.yaml_path, args.project_root)
    passed, violations, warnings = validator.validate()

    # Load lại để lấy stats
    contract = validator.load_contract()
    stats = validator.count_stats(contract)

    print(f"\n{'='*60}")
    print(f"YAML Contract Validation Report")
    print(f"File: {args.yaml_path}")
    print(f"{'='*60}")
    print(f"Stats:")
    print(f"  Total entities : {stats['total_entities']}")
    print(f"  Total fields   : {stats['total_fields']}")
    print(f"  With source    : {stats['fields_with_source']}")
    print(f"  Assumptions    : {stats['fields_as_assumption']}")
    print(f"{'='*60}")

    if violations:
        print(f"\n🔴 VIOLATIONS ({len(violations)}):")
        for v in violations:
            print(f"  ✗ {v}")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")

    # Nếu strict mode, warnings cũng là violations
    if args.strict and warnings:
        passed = False

    print(f"\n{'='*60}")
    if passed:
        print("✅ PASS — Contract hợp lệ")
        sys.exit(0)
    else:
        print("❌ FAIL — Contract có violations cần fix trước khi lock")
        sys.exit(1)


if __name__ == '__main__':
    main()
