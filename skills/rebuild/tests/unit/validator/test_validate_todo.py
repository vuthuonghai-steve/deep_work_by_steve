#!/usr/bin/env python3
"""Unit tests for todo validation (uses handoff_validator)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from handoff_validator import (
    validate_planner_to_builder,
    parse_frontmatter,
)


def test_validate_planner_to_builder_is_callable():
    """Test that validate_planner_to_builder is callable."""
    assert callable(validate_planner_to_builder)


def test_todo_schema_checks_require_artifact_type(tmp_path):
    """Test that todo validation checks artifact_type field."""
    todo_md = tmp_path / "todo.md"
    todo_md.write_text("""---
skill_schema_version: "3.0.0"
artifact_type: todo
stage: planner
status: ready_for_builder
phases: []
prerequisites: []
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


def test_todo_validation_checks_unique_task_ids(tmp_path):
    """Test that duplicate task IDs are detected."""
    todo_md = tmp_path / "todo.md"
    todo_md.write_text("""---
skill_schema_version: "3.0.0"
artifact_type: todo
stage: planner
status: ready_for_builder
phases:
  - id: PH1
    tasks:
      - id: T1
        status: pending
      - id: T1
        status: pending
prerequisites: []
blockers: []
handoff:
  next_stage: builder
---

## 1. Overview
""")
    data, err = parse_frontmatter(str(todo_md))
    assert err is None
    result = validate_planner_to_builder(str(todo_md), data)
    assert result["passed"] is False
    check_names = [c["name"] for c in result["checks"] if c["status"] == "fail"]
    assert "unique_task_ids" in check_names


def test_todo_validation_checks_depends_on_targets_exist(tmp_path):
    """Test that invalid depends_on references are detected."""
    todo_md = tmp_path / "todo.md"
    todo_md.write_text("""---
skill_schema_version: "3.0.0"
artifact_type: todo
stage: planner
status: ready_for_builder
phases:
  - id: PH1
    tasks:
      - id: T1
        status: pending
        depends_on:
          - NONEXISTENT
prerequisites: []
blockers: []
handoff:
  next_stage: builder
---

## 1. Overview
""")
    data, err = parse_frontmatter(str(todo_md))
    assert err is None
    result = validate_planner_to_builder(str(todo_md), data)
    assert result["passed"] is False
    check_names = [c["name"] for c in result["checks"] if c["status"] == "fail"]
    assert "depends_on_targets_exist" in check_names


def test_todo_validation_checks_unresolved_blockers(tmp_path):
    """Test that unresolved blockers are detected."""
    todo_md = tmp_path / "todo.md"
    todo_md.write_text("""---
skill_schema_version: "3.0.0"
artifact_type: todo
stage: planner
status: ready_for_builder
phases:
  - id: PH0
    tasks:
      - id: T1
        status: done
prerequisites: []
blockers:
  - id: B1
    description: Some blocker
    resolved: false
handoff:
  next_stage: builder
---

## 1. Overview
""")
    data, err = parse_frontmatter(str(todo_md))
    assert err is None
    result = validate_planner_to_builder(str(todo_md), data)
    assert result["passed"] is False
    check_names = [c["name"] for c in result["checks"] if c["status"] == "fail"]
    assert "no_unresolved_blockers" in check_names
