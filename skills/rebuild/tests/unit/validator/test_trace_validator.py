#!/usr/bin/env python3
"""Unit tests for trace_validator."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "_shared" / "validators"))

from trace_validator import (
    validate_file,
    is_valid,
    is_trace_like,
    find_typo_hint,
    VALID_PATTERNS,
)


def test_validate_file_imports():
    """Test that validate_file is callable."""
    assert callable(validate_file)


def test_is_valid_imports():
    """Test that is_valid is callable."""
    assert callable(is_valid)


def test_is_trace_like_imports():
    """Test that is_trace_like is callable."""
    assert callable(is_trace_like)


def test_find_typo_hint_imports():
    """Test that find_typo_hint is callable."""
    assert callable(find_typo_hint)


def test_valid_patterns_exist():
    """Test that VALID_PATTERNS is a non-empty list."""
    assert isinstance(VALID_PATTERNS, list)
    assert len(VALID_PATTERNS) > 0


def test_is_trace_like_with_valid_tag():
    """Test is_trace_like detects valid trace tag text."""
    assert is_trace_like("TỪ DESIGN §1")
    assert is_trace_like("GỢI Ý BỔ SUNG")
    assert is_trace_like("CẦN LÀM RÕ")
    assert is_trace_like("TỪ AUDIT TÀI NGUYÊN")


def test_is_trace_like_with_invalid_tag():
    """Test is_trace_like returns False for non-trace text."""
    assert not is_trace_like("hello world")
    assert not is_trace_like("regular text")


def test_is_valid_with_valid_tags():
    """Test is_valid returns True for valid trace tags."""
    assert is_valid("[TỪ DESIGN §1]")
    assert is_valid("[TỪ DESIGN §1.2]")
    assert is_valid("[GỢI Ý BỔ SUNG]")
    assert is_valid("[CẦN LÀM RÕ]")
    assert is_valid("[TỪ AUDIT TÀI NGUYÊN]")


def test_is_valid_with_invalid_tags():
    """Test is_valid returns False for invalid trace tags."""
    assert not is_valid("[TỪ DESION §1]")
    assert not is_valid("[CẦU LÀM RÕ]")
    assert not is_valid("[GỢI BỔ SUNG]")


def test_find_typo_hint_detects_known_typos():
    """Test find_typo_hint returns hints for known typos."""
    hint = find_typo_hint("[CẦU LÀM RÕ]")
    assert hint is not None
    assert "CẦU" in hint


def test_validate_file_with_valid_tags(tmp_path):
    """Test validate_file passes with valid trace tags."""
    f = tmp_path / "valid.md"
    f.write_text("""---
---

Content with [TỪ DESIGN §1] valid tag.
Another [GỢI Ý BỔ SUNG] tag.
""")
    result = validate_file(str(f))
    assert result["passed"] is True
    assert result["stage"] == "trace_validation"


def test_validate_file_with_invalid_tags(tmp_path):
    """Test validate_file fails with invalid trace tags."""
    f = tmp_path / "invalid.md"
    f.write_text("""---
---

Content with [TỪ DESION §1] invalid tag.
""")
    result = validate_file(str(f))
    assert result["passed"] is False
    assert len(result["checks"][0]["invalid_tags"]) > 0
