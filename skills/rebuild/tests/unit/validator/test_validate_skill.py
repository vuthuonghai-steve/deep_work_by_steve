#!/usr/bin/env python3
"""Unit tests for schema_validator (validate_skill)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from schema_validator import (
    parse_frontmatter,
    load_schema,
    validate_against_schema,
    build_check,
    make_result,
)


def test_parse_frontmatter_imports():
    """Test that parse_frontmatter is callable."""
    assert callable(parse_frontmatter)


def test_load_schema_imports():
    """Test that load_schema is callable."""
    assert callable(load_schema)


def test_validate_against_schema_imports():
    """Test that validate_against_schema is callable."""
    assert callable(validate_against_schema)


def test_build_check_imports():
    """Test that build_check is callable."""
    assert callable(build_check)


def test_make_result_imports():
    """Test that make_result is callable."""
    assert callable(make_result)


def test_parse_frontmatter_success(tmp_path):
    """Test parse_frontmatter successfully parses valid frontmatter."""
    f = tmp_path / "test.md"
    f.write_text("""---
key: value
list:
  - item1
  - item2
---

## Content
""")
    data, err = parse_frontmatter(str(f))
    assert err is None
    assert data["key"] == "value"
    assert data["list"] == ["item1", "item2"]


def test_parse_frontmatter_file_not_found():
    """Test parse_frontmatter returns error for missing file."""
    data, err = parse_frontmatter("/nonexistent/file.md")
    assert data is None
    assert err is not None
    assert "not found" in err.lower()


def test_parse_frontmatter_no_frontmatter(tmp_path):
    """Test parse_frontmatter returns error when no frontmatter."""
    f = tmp_path / "test.md"
    f.write_text("## Just content\nNo frontmatter here.")
    data, err = parse_frontmatter(str(f))
    assert data is None
    assert "frontmatter" in err.lower()


def test_build_check_creates_valid_structure():
    """Test build_check creates properly structured dict."""
    check = build_check("test", "pass", error=None, severity="warning", fix_hint="hint")
    assert check["name"] == "test"
    assert check["status"] == "pass"
    assert check["severity"] == "warning"
    assert check["fix_hint"] == "hint"


def test_make_result_with_pass_checks():
    """Test make_result returns passed=True when all checks pass."""
    checks = [build_check("test1", "pass"), build_check("test2", "pass")]
    result = make_result("test.md", checks)
    assert result["passed"] is True
    assert result["artifact"] == "test.md"
    assert len(result["checks"]) == 2


def test_make_result_with_fail_checks():
    """Test make_result returns passed=False when any check fails."""
    checks = [build_check("test1", "pass"), build_check("test2", "fail")]
    result = make_result("test.md", checks)
    assert result["passed"] is False
