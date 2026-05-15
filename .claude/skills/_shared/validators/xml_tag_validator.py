#!/usr/bin/env python3
"""
xml_tag_validator.py — Validate XML semantic tag presence in SKILL.md files.

Checks for presence of <instructions>, <context>, <examples> tags
as defined in CLAUDE.md §3.3 for semantic boundaries.

CLI:
    python xml_tag_validator.py <file.md>

Output: YAML with stage, artifact, timestamp, passed, checks list.
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone

import yaml


REQUIRED_TAGS = ["instructions", "context", "examples"]
OPTIONAL_TAGS = ["input", "output_contract"]


def build_check(name, status, error=None, severity=None, fix_hint=None):
    """Create a single check dict with the standard shape."""
    return {
        "name": name,
        "status": status,
        "error": error,
        "severity": severity,
        "fix_hint": fix_hint,
    }


def check_xml_tags(filepath):
    """Check for XML semantic tag presence in file.

    Returns list of check dicts.
    """
    checks = []

    # Read file
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        checks.append(build_check(
            "File Read", "fail",
            f"File not found: {filepath}", "error",
            "Verify file path is correct"
        ))
        return checks
    except OSError as e:
        checks.append(build_check(
            "File Read", "fail",
            str(e), "error",
            "Check file permissions"
        ))
        return checks

    checks.append(build_check("File Read", "pass"))

    # Check for each required tag
    for tag in REQUIRED_TAGS:
        pattern = rf"<{tag}[^>]*>.*?</{tag}>"
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            checks.append(build_check(
                f"XML Tag: <{tag}>", "pass",
                f"Found <{tag}> tag"
            ))
        else:
            checks.append(build_check(
                f"XML Tag: <{tag}>", "fail",
                f"Missing <{tag}> tag", "warning",
                f"Add <{tag}> semantic boundary tag per CLAUDE.md §3.3"
            ))

    # Check for optional tags
    for tag in OPTIONAL_TAGS:
        pattern = rf"<{tag}[^>]*>.*?</{tag}>"
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            checks.append(build_check(
                f"XML Tag: <{tag}>", "pass",
                f"Found <{tag}> tag (optional)"
            ))

    return checks


def make_result(artifact, checks):
    """Wrap checks into the final YAML-serializable result dict."""
    passed = all(c["status"] == "pass" for c in checks)
    return {
        "stage": "xml_tag_validation",
        "artifact": artifact,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "passed": passed,
        "checks": checks,
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate XML semantic tags in SKILL.md files.")
    parser.add_argument("file", help="Markdown file to validate")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    artifact = os.path.basename(args.file)
    checks = check_xml_tags(args.file)

    result = make_result(artifact, checks)
    print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                    sort_keys=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
