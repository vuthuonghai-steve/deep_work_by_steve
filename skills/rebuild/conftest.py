"""Pytest configuration and shared fixtures for skill suite tests."""

import tempfile
import pytest
from pathlib import Path

# ===== Sample Fixtures =====

SAMPLE_VALID_DESIGN = """---
name: test-skill
version: 1.0.0
---

# §1. Pain Points
...

# §2. User Profile
...

# §3. Zone Mapping
| Zone | Path | Description |
|------|------|-------------|
| core | SKILL.md | Core skill file |
| knowledge | knowledge/ | Knowledge files |

# §4. Mermaid Diagram
...

# §5. Functionality
...

# §6. Quality Gates
...

# §7. Progressive Disclosure
...

# §8. Dependencies
...

# §9. Open Questions
...

# §10. Version & Dependencies
...

# §10.1 Shared Framework
...

# §11. Naming Conventions
...

# §12. Rollback Procedures
...
"""

SAMPLE_VALID_TODO = """---
name: test-skill
version: 1.0.0
---

## 1. Pre-requisites
...

## 2. Phase 1: Foundation
- [TỪ DESIGN #T1] Task 1
- [TỪ DESIGN #T2] Task 2

## 3. Phase 2: Implementation
- [TỪ DESIGN #T3] Task 3

## 4. Phase 3: Testing
- [TỪ DESIGN #T4] Task 4

## 5. Phase 4: Validation
...

## 6. Phase 5: Delivery
...
"""

SAMPLE_INVALID_DESIGN_MISSING_SECTION = """---
name: test-skill
version: 1.0.0
---

# Only Section 1
"""

SAMPLE_INVALID_TODO_BAD_DEPENDENCY = """---
name: test-skill
version: 1.0.0
---

## 1. Pre-requisites
...

## 2. Phase 1
- [TỪ DESIGN #T999] This task references non-existent T999
"""

# ===== Fixtures =====

@pytest.fixture
def skills_root():
    """Return the skills rebuild root directory."""
    return Path(__file__).parent.resolve()

@pytest.fixture
def sample_valid_design():
    """Return sample valid design.md content."""
    return SAMPLE_VALID_DESIGN

@pytest.fixture
def sample_valid_todo():
    """Return sample valid todo.md content."""
    return SAMPLE_VALID_TODO

@pytest.fixture
def sample_invalid_design():
    """Return sample invalid design.md content."""
    return SAMPLE_INVALID_DESIGN_MISSING_SECTION

@pytest.fixture
def sample_invalid_todo():
    """Return sample invalid todo.md content."""
    return SAMPLE_INVALID_TODO_BAD_DEPENDENCY

@pytest.fixture
def tmp_design_file(sample_valid_design):
    """Create a temp design.md file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(sample_valid_design)
        path = f.name
    yield Path(path)
    Path(path).unlink(missing_ok=True)

@pytest.fixture
def tmp_todo_file(sample_valid_todo):
    """Create a temp todo.md file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(sample_valid_todo)
        path = f.name
    yield Path(path)
    Path(path).unlink(missing_ok=True)
