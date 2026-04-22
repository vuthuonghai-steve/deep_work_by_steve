#!/usr/bin/env python3
"""
Pytest configuration for input-normalizer tests.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture
def skill_dir():
    """Return the skill directory path."""
    return Path(__file__).parent.parent


@pytest.fixture
def schema_path(skill_dir):
    """Return path to input-schema.yaml."""
    return skill_dir / "data" / "input-schema.yaml"


@pytest.fixture
def field_mappings_path(skill_dir):
    """Return path to field-mappings.yaml."""
    return skill_dir / "data" / "field-mappings.yaml"


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"
