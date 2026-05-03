#!/usr/bin/env python3
"""
validate_design.py — Validate design.md completeness and correctness.

Usage:
    python validate_design.py <path-to-design.md>

Returns:
    0 if PASS, 1 if FAIL (with error details printed to stderr)
"""

import sys
import re
import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_SECTIONS = [
    "1. Problem Statement",
    "2. Capability Map",
    "3. Zone Mapping",
    "4. Folder Structure",
    "5. Execution Flow",
    "6. Interaction Points",
    "7. Progressive Disclosure",
    "8. Risks",
    "9. Open Questions",
    "10. Metadata",
]

V21_SECTIONS = [
    "11. Context Management",
    "12. Verification Loop",
    "13. Error Recovery",
    "14. Agent Strength",
]

ALL_SECTIONS = REQUIRED_SECTIONS + V21_SECTIONS

ZONE_MAPPING_HEADERS = ["Zone", "Files cần tạo", "Nội dung", "Bắt buộc?"]

# ---------------------------------------------------------------------------
# Validation Functions
# ---------------------------------------------------------------------------

def read_file(filepath: Path) -> str:
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    return filepath.read_text(encoding="utf-8")


def validate_frontmatter(content: str) -> list[str]:
    errors = []
    # Extract YAML frontmatter
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        errors.append("Missing YAML frontmatter")
        return errors

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML frontmatter: {e}")
        return errors

    required_keys = ["skill_schema_version", "skill_name", "zone_mapping", "progressive_disclosure"]
    for key in required_keys:
        if key not in frontmatter:
            errors.append(f"Missing frontmatter key: {key}")

    if "zone_mapping" in frontmatter:
        zm = frontmatter["zone_mapping"]
        for zone in ["core", "knowledge", "scripts", "templates", "data", "loop", "assets"]:
            if zone not in zm:
                errors.append(f"Missing zone in frontmatter: {zone}")

    return errors


def validate_sections(content: str) -> list[str]:
    errors = []
    for section in REQUIRED_SECTIONS:
        # Match "## 1. Problem Statement" or "## 1 Problem Statement"
        pattern = rf"##\s+{re.escape(section)}"
        if not re.search(pattern, content):
            errors.append(f"Missing required section: {section}")

    # v2.1 sections are recommended but not strictly required
    for section in V21_SECTIONS:
        pattern = rf"##\s+{re.escape(section)}"
        if not re.search(pattern, content):
            errors.append(f"WARNING: Missing v2.1 section: {section}")

    return errors


def validate_zone_mapping(content: str) -> list[str]:
    errors = []
    # Find Zone Mapping section
    zm_match = re.search(r"##\s+3\.\s*Zone Mapping.*?(?=##\s+4\.)", content, re.DOTALL)
    if not zm_match:
        errors.append("Could not extract Zone Mapping section")
        return errors

    zm_content = zm_match.group(0)

    # Check for empty "Files cần tạo" column
    rows = re.findall(r"\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", zm_content)
    for row in rows:
        zone, files, desc, required = row
        zone = zone.strip()
        files = files.strip()
        if zone in ["Zone", "---", "-"]:
            continue
        if not files or files.lower() in ["", "...", "files...", "tbd"]:
            errors.append(f"Zone '{zone}' has empty or placeholder 'Files cần tạo'")

    return errors


def validate_diagrams(content: str) -> list[str]:
    errors = []
    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", content, re.DOTALL)

    if len(mermaid_blocks) < 3:
        errors.append(f"Expected >= 3 Mermaid diagrams, found {len(mermaid_blocks)}")

    # Basic syntax checks
    has_mindmap = any("mindmap" in block.lower() for block in mermaid_blocks)
    has_sequence = any("sequenceDiagram" in block for block in mermaid_blocks)
    has_flowchart = any("flowchart" in block.lower() for block in mermaid_blocks)

    if not has_mindmap:
        errors.append("Missing mindmap diagram (Folder Structure)")
    if not has_sequence:
        errors.append("Missing sequenceDiagram (Execution Flow)")
    if not has_flowchart:
        errors.append("Missing flowchart (Workflow Phases)")

    return errors


def validate_no_placeholders(content: str) -> list[str]:
    errors = []
    # Find HTML comments that look like placeholders
    placeholders = re.findall(r"<!--\s*(.*?)\s*-->", content, re.DOTALL)
    for ph in placeholders:
        ph_clean = ph.strip()
        if ph_clean and not ph_clean.startswith("Trả lời"):
            # Allow Vietnamese instruction comments but flag empty/template ones
            if len(ph_clean) < 50:
                errors.append(f"Potential placeholder comment: <!-- {ph_clean[:50]}... -->")

    # Check for common placeholder patterns (not Markdown ellipses)
    placeholder_patterns = [
        (r"\[TBD\]", "[TBD]"),
        (r"\[TODO\]", "[TODO]"),
        (r"\[FILL IN\]", "[FILL IN]"),
        (r"\{skill_name\}", "{skill_name}"),
        (r"\{date\}", "{date}"),
    ]
    for pattern, label in placeholder_patterns:
        matches = re.findall(pattern, content)
        if matches:
            errors.append(f"Found placeholder pattern '{label}' ({len(matches)} occurrences)")

    return errors


def validate_risks(content: str) -> list[str]:
    errors = []
    risks_section = re.search(r"##\s+8\.\s*Risks.*?(?=##\s+9\.)", content, re.DOTALL)
    if not risks_section:
        errors.append("Could not extract Risks section")
        return errors

    risks_content = risks_section.group(0)
    # Count risk rows (rows with | number |)
    risk_rows = re.findall(r"\|\s*\d+\s*\|", risks_content)
    if len(risk_rows) < 3:
        errors.append(f"Expected >= 3 risks, found {len(risk_rows)}")

    return errors


def validate_metadata(content: str) -> list[str]:
    errors = []
    metadata_section = re.search(r"##\s+10\.\s*Metadata.*?(?=##\s+11\.|$)", content, re.DOTALL)
    if not metadata_section:
        errors.append("Could not extract Metadata section")
        return errors

    meta_content = metadata_section.group(0)
    required_meta = ["Skill Name", "Created", "Author", "Status"]
    for key in required_meta:
        if key not in meta_content:
            errors.append(f"Missing metadata field: {key}")

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_design.py <path-to-design.md>", file=sys.stderr)
        return 1

    filepath = Path(sys.argv[1])
    content = read_file(filepath)

    all_errors = []

    print(f"Validating: {filepath}")
    print("=" * 50)

    # Run validators
    validators = [
        ("Frontmatter", validate_frontmatter),
        ("Sections", validate_sections),
        ("Zone Mapping", validate_zone_mapping),
        ("Diagrams", validate_diagrams),
        ("Placeholders", validate_no_placeholders),
        ("Risks", validate_risks),
        ("Metadata", validate_metadata),
    ]

    for name, validator in validators:
        errors = validator(content)
        if errors:
            print(f"\n❌ {name}:")
            for err in errors:
                print(f"  - {err}")
            all_errors.extend(errors)
        else:
            print(f"✅ {name}")

    print("\n" + "=" * 50)
    if all_errors:
        print(f"RESULT: FAIL ({len(all_errors)} issues found)")
        return 1
    else:
        print("RESULT: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
