#!/usr/bin/env python3
"""Unit tests for handoff_validator."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from handoff_validator import (
    validate_design_to_planner,
    validate_planner_to_builder,
    validate_builder_complete,
    parse_frontmatter,
    make_check,
)


def test_validate_design_to_planner_imports():
    """Test that validate_design_to_planner is callable."""
    assert callable(validate_design_to_planner)


def test_validate_planner_to_builder_imports():
    """Test that validate_planner_to_builder is callable."""
    assert callable(validate_planner_to_builder)


def test_validate_builder_complete_imports():
    """Test that validate_builder_complete is callable."""
    assert callable(validate_builder_complete)


def test_parse_frontmatter_imports():
    """Test that parse_frontmatter is callable."""
    assert callable(parse_frontmatter)


def test_make_check_creates_valid_dict():
    """Test that make_check creates a properly structured dict."""
    check = make_check("test_check", True, error=None, fix_hint=None)
    assert check["name"] == "test_check"
    assert check["status"] == "pass"
    assert check["error"] is None
    assert check["fix_hint"] is None


def test_make_check_failed_status():
    """Test that make_check with passed=False sets status to fail."""
    check = make_check("test_check", False, error="something wrong", fix_hint="do this")
    assert check["status"] == "fail"
    assert check["error"] == "something wrong"
    assert check["fix_hint"] == "do this"


def test_validate_design_to_planner_with_minimal_valid_data(tmp_path):
    """Test validate_design_to_planner with minimal valid design frontmatter."""
    design_md = tmp_path / "design.md"
    design_md.write_text("""---
skill_schema_version: "3.0.0"
artifact_type: design
stage: architect
status: ready_for_planner
zone_mapping:
  core:
    files:
      - path: core/skill.md
  knowledge:
    files: []
  scripts:
    files: []
  templates:
    files: []
  data:
    files: []
  loop:
    files: []
  assets:
    files: []
progressive_disclosure:
  tier1:
    - path: core/skill.md
      base: skills_root
handoff:
  next_stage: planner
---

## 1. Overview
""")
    data, err = parse_frontmatter(str(design_md))
    assert err is None
    result = validate_design_to_planner(str(design_md), data)
    assert result["stage"] == "design-to-planner"
    assert "passed" in result
    assert "checks" in result


def test_validate_planner_to_builder_with_minimal_valid_data(tmp_path):
    """Test validate_planner_to_builder with minimal valid todo frontmatter."""
    todo_md = tmp_path / "todo.md"
    todo_md.write_text("""---
skill_schema_version: "3.0.0"
artifact_type: todo
stage: planner
status: ready_for_builder
phases:
  - id: PH0
    tasks:
      - id: PH0-T1
        status: done
prerequisites:
  - item: design.md
    status: ready
blockers: []
handoff:
  next_stage: builder
---

## 1. Overview
""")
    data, err = parse_frontmatter(str(todo_md))
    assert err is None
    result = validate_planner_to_builder(str(todo_md), data)
    assert result["stage"] == "planner-to-builder"
    assert "passed" in result
    assert "checks" in result
