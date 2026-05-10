#!/usr/bin/env python3
"""E2E smoke tests for verifying skill structure exists."""
from pathlib import Path

# Root of the skills rebuild workspace
REBUILD_ROOT = Path(__file__).parent.parent.parent.parent


def test_skill_architect_exists():
    """Test that skill-architect directory exists and has required structure."""
    architect_dir = REBUILD_ROOT / "skill-architect"
    assert architect_dir.exists(), "skill-architect directory must exist"
    assert (architect_dir / "SKILL.md").exists(), "skill-architect must have SKILL.md"


def test_skill_planner_exists():
    """Test that skill-planner directory exists and has required structure."""
    planner_dir = REBUILD_ROOT / "skill-planner"
    assert planner_dir.exists(), "skill-planner directory must exist"
    assert (planner_dir / "SKILL.md").exists(), "skill-planner must have SKILL.md"


def test_skill_builder_exists():
    """Test that skill-builder directory exists and has required structure."""
    builder_dir = REBUILD_ROOT / "skill-builder"
    assert builder_dir.exists(), "skill-builder directory must exist"
    assert (builder_dir / "SKILL.md").exists(), "skill-builder must have SKILL.md"


def test_shared_validators_exist():
    """Test that _shared/validators directory exists with validator modules."""
    validators_dir = REBUILD_ROOT / "_shared" / "validators"
    assert validators_dir.exists(), "_shared/validators directory must exist"
    assert (validators_dir / "handoff_validator.py").exists(), "handoff_validator.py must exist"
    assert (validators_dir / "trace_validator.py").exists(), "trace_validator.py must exist"
    assert (validators_dir / "schema_validator.py").exists(), "schema_validator.py must exist"


def test_all_skills_have_knowledge_loop_scripts(tmp_path):
    """Test that each skill has knowledge/, loop/, and scripts/ directories."""
    for skill_name in ["skill-architect", "skill-planner", "skill-builder"]:
        skill_dir = REBUILD_ROOT / skill_name
        assert (skill_dir / "knowledge").exists(), f"{skill_name} must have knowledge/"
        assert (skill_dir / "loop").exists(), f"{skill_name} must have loop/"
        assert (skill_dir / "scripts").exists(), f"{skill_name} must have scripts/"
