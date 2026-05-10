#!/usr/bin/env python3
"""Integration tests for full pipeline handoff."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from handoff_validator import (
    validate_design_to_planner,
    validate_planner_to_builder,
    parse_frontmatter,
)


def test_design_to_planner_handoff_contract(tmp_path):
    """Test design-to-planner handoff contract: design must be ready_for_planner."""
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
## 2. Goals
## 3. Requirements
## 4. Architecture
## 5. Components
## 6. Data Model
## 7. APIs
## 8. Security
## 9. Testing
## 10. Deployment
""")
    data, err = parse_frontmatter(str(design_md))
    assert err is None
    assert data["status"] == "ready_for_planner"
    assert data["handoff"]["next_stage"] == "planner"
    result = validate_design_to_planner(str(design_md), data)
    assert result["stage"] == "design-to-planner"


def test_planner_to_builder_handoff_contract(tmp_path):
    """Test planner-to-builder handoff contract: todo must be ready_for_builder."""
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
    assert data["status"] == "ready_for_builder"
    assert data["handoff"]["next_stage"] == "builder"
    result = validate_planner_to_builder(str(todo_md), data)
    assert result["stage"] == "planner-to-builder"


def test_handoff_chain_design_to_planner_to_builder(tmp_path):
    """Test the full handoff chain: design -> planner -> builder."""
    # Step 1: Valid design
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
## 2. Goals
## 3. Requirements
## 4. Architecture
## 5. Components
## 6. Data Model
## 7. APIs
## 8. Security
## 9. Testing
## 10. Deployment
""")

    # Step 2: Valid todo
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
prerequisites:
  - item: design.md
    status: ready
blockers: []
handoff:
  next_stage: builder
---

## 1. Overview
""")

    # Validate design handoff
    design_data, design_err = parse_frontmatter(str(design_md))
    assert design_err is None
    design_result = validate_design_to_planner(str(design_md), design_data)
    assert design_result["stage"] == "design-to-planner"

    # Validate todo handoff
    todo_data, todo_err = parse_frontmatter(str(todo_md))
    assert todo_err is None
    todo_result = validate_planner_to_builder(str(todo_md), todo_data)
    assert todo_result["stage"] == "planner-to-builder"

    # Both should have proper handoff next_stage
    assert design_data["handoff"]["next_stage"] == "planner"
    assert todo_data["handoff"]["next_stage"] == "builder"
