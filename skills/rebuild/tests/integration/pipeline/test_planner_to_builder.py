#!/usr/bin/env python3
"""Integration tests for planner-to-builder handoff."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from handoff_validator import validate_planner_to_builder, parse_frontmatter


def test_planner_todo_has_unique_task_ids(tmp_path):
    """Test that todo.md has unique task IDs across all phases."""
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
  - id: PH1
    tasks:
      - id: PH1-T1
        status: pending
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
    # Check that unique_task_ids passes
    unique_check = next((c for c in result["checks"] if c["name"] == "unique_task_ids"), None)
    assert unique_check is not None
    assert unique_check["status"] == "pass"


def test_planner_todo_phase0_all_done(tmp_path):
    """Test that PH0 tasks are all done or skipped."""
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
      - id: PH0-T2
        status: skipped
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
    # Check that phase0_all_done_or_skipped passes
    phase0_check = next((c for c in result["checks"] if c["name"] == "phase0_all_done_or_skipped"), None)
    assert phase0_check is not None
    assert phase0_check["status"] == "pass"


def test_planner_todo_handoff_to_builder(tmp_path):
    """Test that todo.md handoff is set to builder."""
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
    # Check handoff_next_stage_builder passes
    handoff_check = next((c for c in result["checks"] if c["name"] == "handoff_next_stage_builder"), None)
    assert handoff_check is not None
    assert handoff_check["status"] == "pass"


def test_planner_todo_prerequisites_all_ready(tmp_path):
    """Test that all prerequisites have status ready."""
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
  - item: references.md
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
    # Check that prerequisites_all_ready passes
    prereq_check = next((c for c in result["checks"] if c["name"] == "prerequisites_all_ready"), None)
    assert prereq_check is not None
    assert prereq_check["status"] == "pass"
