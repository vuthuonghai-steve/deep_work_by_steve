#!/usr/bin/env python3
"""
validate-todo.py
Validate todo.md format according to skill-planner v2.0 specification.

Usage:
    python validate-todo.py <path-to-todo.md>

Exit codes:
    0 - Valid
    1 - Validation failed
    2 - File not found
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


class TodoValidator:
    """Validates todo.md format according to skill-planner v2.0"""

    REQUIRED_SECTIONS = [
        "## 1. Pre-requisites",
        "## 2. Phase Breakdown",
        "## 3. Knowledge & Resources Needed",
        "## 4. Definition of Done",
        "## 5. Notes",
    ]

    OPTIONAL_SECTIONS = [
        "## 6. Builder Feedback Integration",
    ]

    REQUIRED_COLUMNS = ["#", "Task", "Priority", "Est. Hours", "Dependencies", "Trace"]

    TRACE_TAGS = [
        "[TỪ DESIGN §",
        "[GỢI Ý BỔ SUNG]",
        "[TỪ AUDIT TÀI NGUYÊN]",
        "[CẦN LÀM RÕ]",
    ]

    PRIORITIES = ["Critical", "High", "Medium", "Low"]

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if valid."""
        if not self.filepath.exists():
            self.errors.append(f"File not found: {self.filepath}")
            return False

        content = self.filepath.read_text(encoding="utf-8")

        self._validate_sections(content)
        self._validate_phase_breakdown_columns(content)
        self._validate_trace_tags(content)
        self._validate_priorities(content)
        self._validate_builder_feedback(content)

        return len(self.errors) == 0

    def _validate_sections(self, content: str):
        """Check all required sections exist."""
        for section in self.REQUIRED_SECTIONS:
            if section not in content:
                self.errors.append(f"Missing required section: {section}")

    def _validate_phase_breakdown_columns(self, content: str):
        """Validate Phase Breakdown has correct columns."""
        # Look for the table header in Phase Breakdown
        phase_match = re.search(
            r"## 2\. Phase Breakdown.*?(?=##|\Z)", content, re.DOTALL
        )

        if not phase_match:
            self.errors.append("Section 2. Phase Breakdown not found")
            return

        phase_content = phase_match.group(0)

        # Check for column headers
        has_columns = all(col.lower() in phase_content.lower() for col in ["task", "priority"])
        if not has_columns:
            self.warnings.append(
                "Phase Breakdown may be missing required columns (Task, Priority, Est. Hours, Dependencies, Trace)"
            )

    def _validate_trace_tags(self, content: str):
        """Check that all tasks have trace tags."""
        # Find all task items
        tasks = re.findall(r"- \[ \] (.+)$", content, re.MULTILINE)

        for task in tasks:
            task = task.strip()
            if not task:
                continue

            # Check if task has a trace tag
            has_tag = any(tag in task for tag in self.TRACE_TAGS)
            if not has_tag:
                self.warnings.append(f"Task may be missing trace tag: '{task[:50]}...'")

    def _validate_priorities(self, content: str):
        """Validate priority values."""
        priorities = re.findall(r"(?i)(priority[:\s]+)(\w+)", content)

        for _, priority in priorities:
            if priority.capitalize() not in self.PRIORITIES:
                self.warnings.append(f"Invalid priority value: {priority}")

    def _validate_builder_feedback(self, content: str):
        """Check if Builder Feedback section exists (v2.0+)."""
        if "## 6. Builder Feedback Integration" not in content:
            self.warnings.append(
                "Missing optional section: ## 6. Builder Feedback Integration (recommended for v2.0)"
            )

    def print_report(self):
        """Print validation report."""
        print("=" * 60)
        print(f"Todo.md Validator - {self.filepath}")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ VALID - No issues found")

        print("\n" + "=" * 60)

        if self.errors:
            print(f"Result: FAILED ({len(self.errors)} errors)")
        elif self.warnings:
            print(f"Result: PASSED WITH WARNINGS ({len(self.warnings)} warnings)")
        else:
            print("Result: PASSED")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-todo.py <path-to-todo.md>")
        sys.exit(2)

    filepath = sys.argv[1]
    validator = TodoValidator(filepath)

    if validator.validate():
        validator.print_report()
        sys.exit(0)
    else:
        validator.print_report()
        sys.exit(1)


if __name__ == "__main__":
    main()
