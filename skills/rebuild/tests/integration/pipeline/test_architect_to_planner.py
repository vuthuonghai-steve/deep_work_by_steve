#!/usr/bin/env python3
"""Integration tests for architect-to-planner handoff."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from handoff_validator import validate_design_to_planner, parse_frontmatter


def test_architect_design_has_10_required_sections(tmp_path):
    """Test that design.md has all 10 required section headings."""
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
    result = validate_design_to_planner(str(design_md), data)
    # Check that required_10_sections_present passes
    section_check = next((c for c in result["checks"] if c["name"] == "required_10_sections_present"), None)
    assert section_check is not None
    assert section_check["status"] == "pass"


def test_architect_design_zone_mapping_complete(tmp_path):
    """Test that design.md has all 7 required zones."""
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
    # Check that all_7_zones_present passes
    zone_check = next((c for c in result["checks"] if c["name"] == "all_7_zones_present"), None)
    assert zone_check is not None
    assert zone_check["status"] == "pass"


def test_architect_design_handoff_to_planner(tmp_path):
    """Test that design.md handoff is set to planner."""
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
    result = validate_design_to_planner(str(design_md), data)
    # Check handoff_next_stage_planner passes
    handoff_check = next((c for c in result["checks"] if c["name"] == "handoff_next_stage_planner"), None)
    assert handoff_check is not None
    assert handoff_check["status"] == "pass"
