#!/usr/bin/env python3
"""
type_resolver.py — Type Resolver với 3-layer fallback
Usage: from type_resolver import resolve_types; types = resolve_types(project_root='.')

Layer 1 (Project-override): {project_root}/data/project-types.json   ← do từng dự án tự định nghĩa
Layer 2 (Shared-KLTN):      .skill-context/shared/shared-types.json  ← KLTN-specific
Layer 3 (Built-in default): data/default-types.json                  ← luôn có trong skill

Logic: Resolver kiểm tra từng layer theo thứ tự. Nếu layer nào tồn tại → dùng và dừng.
       Layer 3 luôn tồn tại → KHÔNG BAO GIỜ bị lỗi.

Source: design.md §4 Task 1.4, todo.md Task 1.4 [PORTABLE]
"""

import json
import os
from pathlib import Path


def _find_skill_root() -> Path:
    """Tìm thư mục gốc của skill (thư mục chứa data/default-types.json)."""
    current = Path(__file__).parent
    # scripts/ nằm trong skill root, nên parent của scripts/ là skill root
    skill_root = current.parent
    return skill_root


def _find_shared_types() -> Path | None:
    """Tìm .skill-context/shared/shared-types.json từ project root."""
    # Đi ngược từ skill root để tìm .skill-context/shared/
    skill_root = _find_skill_root()
    # .agent/skills/class-diagram-analyst → ngược lên 3 cấp → project root
    project_root = skill_root.parent.parent.parent
    shared_path = project_root / ".skill-context" / "shared" / "shared-types.json"
    return shared_path if shared_path.exists() else None


def resolve_types(project_root: str | None = None) -> dict:
    """
    Resolve field type whitelist với 3-layer fallback.

    Args:
        project_root: Path đến project root để tìm project-types.json. None = chỉ dùng layer 2+3.

    Returns:
        dict với keys: allowed_field_types, mermaid_type_map, aggregate_root_patterns,
                       access_control_actors, lifecycle_hooks
    """
    skill_root = _find_skill_root()

    # Layer 1: Project-override
    if project_root:
        layer1_path = Path(project_root) / "data" / "project-types.json"
        if layer1_path.exists():
            with open(layer1_path, encoding="utf-8") as f:
                return json.load(f)

    # Layer 2: Shared KLTN
    shared_path = _find_shared_types()
    if shared_path:
        with open(shared_path, encoding="utf-8") as f:
            return json.load(f)

    # Layer 3: Built-in default (luôn tồn tại)
    default_path = skill_root / "data" / "default-types.json"
    with open(default_path, encoding="utf-8") as f:
        return json.load(f)


def get_allowed_types(project_root: str | None = None) -> list[str]:
    """Shortcut: chỉ lấy danh sách allowed_field_types."""
    types = resolve_types(project_root)
    return types.get("allowed_field_types", [])


def get_mermaid_type(payload_type: str, project_root: str | None = None) -> str:
    """Chuyển đổi PayloadCMS type sang Mermaid representation."""
    types = resolve_types(project_root)
    type_map = types.get("mermaid_type_map", {})
    return type_map.get(payload_type, "String")  # default fallback là String


if __name__ == "__main__":
    # Quick test
    result = resolve_types()
    print("✅ Type resolver hoạt động bình thường")
    print(f"Allowed types: {result.get('allowed_field_types', [])}")
    print(f"Mermaid map có {len(result.get('mermaid_type_map', {}))} entries")
