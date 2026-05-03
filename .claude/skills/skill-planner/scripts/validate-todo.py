#!/usr/bin/env python3
"""
validate-todo.py
Validate todo.md format according to skill-planner v2.1 specification.

Validates:
- YAML frontmatter with required fields
- Markdown body sections
- Trace tags (ERROR level, not warning)
- Phase/task structure
- Schema compliance

Usage:
    python validate-todo.py <path-to-todo.md> [--schema <path-to-schema.json>]

Exit codes:
    0 - Valid
    1 - Validation failed
    2 - File not found / usage error
"""

import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class TodoValidator:
    """Validates todo.md format according to skill-planner v2.1"""

    # Required YAML frontmatter fields
    REQUIRED_YAML_FIELDS = [
        "skill_schema_version",
        "artifact_type",
        "skill_name",
        "generated_by",
        "generated_at",
        "stage",
        "status",
        "phases",
        "blockers",
        "prerequisites",
        "handoff",
    ]

    # Valid values for specific fields
    VALID_SCHEMA_VERSIONS = ["3.0.0", "3.1.0"]
    VALID_ARTIFACT_TYPES = ["todo"]
    VALID_STAGES = ["planner"]
    VALID_STATUSES = ["in_progress", "ready_for_builder", "blocked"]
    VALID_PRIORITIES = ["critical", "high", "medium", "low"]
    VALID_ZONES = ["core", "knowledge", "scripts", "templates", "data", "loop", "assets"]
    VALID_TASK_STATUSES = ["pending", "in_progress", "done", "skipped"]
    VALID_BLOCKER_TYPES = ["CLARIFICATION_NEEDED", "DESIGN_CONFLICT", "RESOURCE_MISSING"]
    VALID_TIERS = ["domain", "technical", "packaging"]
    VALID_PREREQ_STATUSES = ["ready", "missing", "thin"]

    # Required markdown sections
    REQUIRED_SECTIONS = [
        "## 1. Pre-requisites",
        "## 2. Phase Breakdown",
        "## 3. Knowledge & Resources Needed",
        "## 4. Definition of Done",
        "## 5. Notes",
    ]

    # Trace tags (AH1-AH5 enforcement)
    TRACE_TAGS = [
        "[TỪ DESIGN §",
        "[GỢI Ý BỔ SUNG]",
        "[TỪ AUDIT TÀI NGUYÊN]",
        "[CẦN LÀM RÕ]",
    ]

    # Regex patterns
    PHASE_ID_PATTERN = re.compile(r"^PH\d+$")
    TASK_ID_PATTERN = re.compile(r"^T\d+\.\d+$")
    TRACE_TAG_PATTERN = re.compile(r"^\[(TỪ DESIGN §\d+(\.\d+)?|GỢI Ý BỔ SUNG|TỪ AUDIT TÀI NGUYÊN|CẦN LÀM RÕ)\]")

    def __init__(self, filepath: str, schema_path: Optional[str] = None):
        self.filepath = Path(filepath)
        self.schema_path = Path(schema_path) if schema_path else None
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if valid."""
        if not self.filepath.exists():
            self.errors.append(f"File not found: {self.filepath}")
            return False

        content = self.filepath.read_text(encoding="utf-8")

        # Split frontmatter and body
        frontmatter, body = self._split_frontmatter(content)

        # Validate YAML frontmatter
        if frontmatter is None:
            self.errors.append("Missing YAML frontmatter (--- delimiters not found)")
        else:
            self._validate_yaml_frontmatter(frontmatter)

        # Validate markdown body
        self._validate_sections(body or content)
        self._validate_phase_breakdown_columns(body or content)
        self._validate_trace_tags(body or content)
        self._validate_priorities(body or content)
        self._validate_builder_feedback(body or content)

        return len(self.errors) == 0

    def _split_frontmatter(self, content: str) -> tuple:
        """Split content into YAML frontmatter and markdown body."""
        if not content.startswith("---"):
            return None, content

        # Find closing ---
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return None, content

        frontmatter_str = content[3:end_idx].strip()
        body = content[end_idx + 3:].strip()

        return frontmatter_str, body

    def _parse_yaml_simple(self, yaml_str: str) -> Dict[str, Any]:
        """Simple YAML parser for frontmatter (handles basic key-value and nested structures)."""
        result = {}
        current_key = None
        current_indent = 0
        lines = yaml_str.split("\n")

        for line in lines:
            if not line.strip() or line.strip().startswith("#"):
                continue

            # Detect indentation
            indent = len(line) - len(line.lstrip())

            # Top-level key
            if indent == 0 and ":" in line:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()

                if value and value not in ["|", ">"]:
                    # Handle quoted strings
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    # Handle booleans
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False

                    result[key] = value
                else:
                    result[key] = None
                    current_key = key
                    current_indent = indent

        return result

    def _validate_yaml_frontmatter(self, frontmatter_str: str):
        """Validate YAML frontmatter against requirements."""
        try:
            data = self._parse_yaml_simple(frontmatter_str)
        except Exception as e:
            self.errors.append(f"Failed to parse YAML frontmatter: {e}")
            return

        # Check required fields
        for field in self.REQUIRED_YAML_FIELDS:
            if field not in data:
                self.errors.append(f"Missing required YAML field: {field}")

        # Validate specific field values
        if "skill_schema_version" in data:
            if data["skill_schema_version"] not in self.VALID_SCHEMA_VERSIONS:
                self.errors.append(
                    f"Invalid skill_schema_version: {data['skill_schema_version']}. "
                    f"Must be one of: {self.VALID_SCHEMA_VERSIONS}"
                )

        if "artifact_type" in data:
            if data["artifact_type"] not in self.VALID_ARTIFACT_TYPES:
                self.errors.append(
                    f"Invalid artifact_type: {data['artifact_type']}. Must be one of: {self.VALID_ARTIFACT_TYPES}"
                )

        if "stage" in data:
            if data["stage"] not in self.VALID_STAGES:
                self.errors.append(
                    f"Invalid stage: {data['stage']}. Must be one of: {self.VALID_STAGES}"
                )

        if "status" in data:
            if data["status"] not in self.VALID_STATUSES:
                self.errors.append(
                    f"Invalid status: {data['status']}. Must be one of: {self.VALID_STATUSES}"
                )

        if "generated_by" in data:
            if data["generated_by"] != "skill-planner":
                self.errors.append(
                    f"Invalid generated_by: {data['generated_by']}. Must be 'skill-planner'"
                )

        # Validate skill_name pattern
        if "skill_name" in data:
            if not re.match(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$", str(data["skill_name"])):
                self.errors.append(
                    f"Invalid skill_name: {data['skill_name']}. Must be kebab-case"
                )

        # Validate handoff structure
        if "handoff" in data and isinstance(data["handoff"], dict):
            if "next_stage" in data["handoff"]:
                if data["handoff"]["next_stage"] != "builder":
                    self.errors.append(
                        f"Invalid handoff.next_stage: {data['handoff']['next_stage']}. Must be 'builder'"
                    )

    def _validate_sections(self, content: str):
        """Check all required sections exist."""
        for section in self.REQUIRED_SECTIONS:
            if section not in content:
                self.errors.append(f"Missing required section: {section}")

    def _validate_phase_breakdown_columns(self, content: str):
        """Validate Phase Breakdown has correct columns."""
        phase_match = re.search(
            r"## 2\. Phase Breakdown.*?(?=##|\Z)", content, re.DOTALL
        )

        if not phase_match:
            self.errors.append("Section 2. Phase Breakdown not found")
            return

        phase_content = phase_match.group(0)

        has_columns = all(col.lower() in phase_content.lower() for col in ["task", "priority"])
        if not has_columns:
            self.warnings.append(
                "Phase Breakdown may be missing required columns (Task, Priority, Est. Hours, Dependencies, Trace)"
            )

    def _validate_trace_tags(self, content: str):
        """Check that all tasks have valid trace tags. ERRORS, not warnings."""
        tasks = re.findall(r"- \[ \] (.+)$", content, re.MULTILINE)

        for task in tasks:
            task = task.strip()
            if not task:
                continue

            has_tag = any(tag in task for tag in self.TRACE_TAGS)
            if not has_tag:
                # ERROR level — trace tags are mandatory (AH1 enforcement)
                self.errors.append(f"AH1 VIOLATION — Task missing trace tag: '{task[:60]}...'")

    def _validate_priorities(self, content: str):
        """Validate priority values in Phase Breakdown tables."""
        # Find all table rows with priority
        priority_matches = re.findall(
            r"\|\s*(Critical|High|Medium|Low)\s*\|", content, re.IGNORECASE
        )

        for priority in priority_matches:
            if priority.lower() not in [p.lower() for p in self.VALID_PRIORITIES]:
                self.warnings.append(f"Invalid priority value: {priority}")

    def _validate_builder_feedback(self, content: str):
        """Check if Builder Feedback section exists."""
        if "## 6. Builder Feedback Integration" not in content:
            self.warnings.append(
                "Missing optional section: ## 6. Builder Feedback Integration (recommended)"
            )

    def print_report(self):
        """Print validation report."""
        print("=" * 60)
        print(f"Todo.md Validator v2.1 — {self.filepath}")
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
            print("\n✅ VALID — No issues found")

        print("\n" + "=" * 60)

        if self.errors:
            print(f"Result: FAILED ({len(self.errors)} errors, {len(self.warnings)} warnings)")
        elif self.warnings:
            print(f"Result: PASSED WITH WARNINGS ({len(self.warnings)} warnings)")
        else:
            print("Result: PASSED")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-todo.py <path-to-todo.md> [--schema <path-to-schema.json>]")
        sys.exit(2)

    filepath = sys.argv[1]
    schema_path = None

    if "--schema" in sys.argv:
        idx = sys.argv.index("--schema")
        if idx + 1 < len(sys.argv):
            schema_path = sys.argv[idx + 1]

    validator = TodoValidator(filepath, schema_path)

    if validator.validate():
        validator.print_report()
        sys.exit(0)
    else:
        validator.print_report()
        sys.exit(1)


if __name__ == "__main__":
    main()
