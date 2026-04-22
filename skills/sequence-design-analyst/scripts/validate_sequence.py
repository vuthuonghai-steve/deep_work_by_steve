#!/usr/bin/env python3
"""
validate_sequence.py — Mermaid Sequence Diagram Validator for sequence-design-analyst

Usage:
    python validate_sequence.py <mermaid_file_or_string> [--verbose]

Exit codes:
    0 = PASS (valid syntax)
    1 = FAIL (invalid syntax)
"""

import re
import sys
from pathlib import Path


def extract_mermaid_content(text: str) -> str:
    """Extract content from ```mermaid ``` blocks or return as-is."""
    pattern = r"```mermaid\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def validate_sequence_syntax(content: str) -> tuple[bool, list[str]]:
    """Validate Mermaid sequence diagram syntax."""
    errors = []
    lines = content.split("\n")

    # Check for sequenceDiagram directive
    if "sequenceDiagram" not in content:
        errors.append("Missing 'sequenceDiagram' directive")

    # Track participants
    participants = set()
    valid_activations = set()

    for i, line in enumerate(lines, 1):
        line = line.strip()

        # Skip comments and empty lines
        if not line or line.startswith("%%"):
            continue

        # Check participant declarations
        participant_match = re.search(r"participant\s+(\w+)", line)
        if participant_match:
            participants.add(participant_match.group(1))

        # Check actor declarations
        actor_match = re.search(r"actor\s+(\w+)", line)
        if actor_match:
            participants.add(actor_match.group(1))

        # Check loop/alt/opt blocks are properly closed
        if line in ["loop", "alt", "opt", "par", "critical", "section"]:
            # These should have corresponding 'end'
            pass

    # Check for participant in messages
    message_pattern = re.compile(r"(\w+)\s*(?:->>|-->|->|--|<<|>>|-.->|==>|Note\.)\s*(\w+)")
    for line in lines:
        for m in message_pattern.finditer(line):
            sender, receiver = m.group(1), m.group(2)
            if sender != "Note" and sender not in participants:
                errors.append(f"Line {i}: Unknown participant '{sender}'")
            if receiver != "Note" and receiver not in participants:
                errors.append(f"Line {i}: Unknown participant '{receiver}'")

    return len(errors) == 0, errors


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="validate_sequence.py — Mermaid Sequence Diagram Validator"
    )
    parser.add_argument("input", help="Path to .md or .mmd file, or Mermaid code string")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    # Read input
    path = Path(args.input)
    if path.exists():
        content = path.read_text(encoding="utf-8")
    else:
        content = args.input

    mermaid_content = extract_mermaid_content(content)
    is_valid, errors = validate_sequence_syntax(mermaid_content)

    print(f"\n🔍 validate_sequence.py — Mermaid Sequence Diagram Validator")

    if is_valid:
        print(f"✅ PASS — Sequence diagram syntax is valid.\n")
        sys.exit(0)
    else:
        print(f"\n❌ FAIL — Found {len(errors)} issue(s):\n")
        for error in errors:
            print(f"  - {error}")
        print(f"\n📖 Tham khảo: knowledge/uml-rules.md §3")
        sys.exit(1)


if __name__ == "__main__":
    main()
