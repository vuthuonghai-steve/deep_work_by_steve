#!/usr/bin/env python3
"""
init_context.py — Khoi tao cau truc thu muc .skill-context/{skill-name}/

Tao thu muc context va cac file template cho skill moi.
Safe-create policy: KHONG ghi de file da ton tai.

Usage:
    python init_context.py <skill-name>

Example:
    python init_context.py my-api-analyzer
"""

import sys
import os
import re
from pathlib import Path
from datetime import date


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MAX_WALK_UP_LEVELS = 10

TEMPLATE_FILES = {
    "design.md": "design.md.template",
    "todo.md": "todo.md.template",
    "build-log.md": "build-log.md.template",
}

PLACEHOLDERS = {
    "{skill_name}": "",   # filled at runtime
    "{date}": "",         # filled at runtime
    "{author}": "Skill Architect",
}

FALLBACK_TEMPLATES = {
    "design.md": "# {skill_name} — Architecture Design\n\n> Generated: {date}\n\n## 1. Problem Statement\n\n## 2. Capability Map\n\n## 3. Zone Mapping\n\n## 4. Folder Structure\n\n## 5. Execution Flow\n\n## 6. Interaction Points\n\n## 7. Progressive Disclosure Plan\n\n## 8. Risks & Blind Spots\n\n## 9. Open Questions\n\n## 10. Metadata\n",
    "todo.md": "# {skill_name} — Implementation Plan\n\n> Generated: {date}\n\n## 1. Pre-requisites\n\n## 2. Phase Breakdown\n\n## 3. Knowledge & Resources Needed\n\n## 4. Definition of Done\n\n## 5. Notes\n",
    "build-log.md": "# {skill_name} — Build Log\n\n> Generated: {date}\n\n## 1. Build Session Log\n\n## 2. Files Created\n\n## 3. Decisions Made During Build\n\n## 4. Issues Encountered\n\n## 5. Final Status\n",
}


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def find_project_root(start_dir: Path) -> Path | None:
    """Walk up from start_dir to find the directory containing .claude/."""
    current = start_dir.resolve()
    for _ in range(MAX_WALK_UP_LEVELS):
        if (current / ".claude").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def validate_skill_name(name: str) -> bool:
    """Check that skill name is valid kebab-case."""
    return bool(KEBAB_CASE_PATTERN.match(name))


def resolve_template_content(
    template_name: str, output_name: str, templates_dir: Path
) -> str:
    """Read template file or return fallback content."""
    template_path = templates_dir / template_name
    if template_path.is_file():
        return template_path.read_text(encoding="utf-8")

    print(f"  WARNING: Template '{template_name}' not found, using fallback")
    return FALLBACK_TEMPLATES.get(output_name, f"# {output_name}\n")


def replace_placeholders(content: str, replacements: dict[str, str]) -> str:
    """Replace all placeholders in content."""
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def safe_create_file(filepath: Path, content: str) -> str:
    """Create file only if it does not exist. Return status string."""
    if filepath.exists():
        return "SKIPPED (already exists)"
    filepath.write_text(content, encoding="utf-8")
    return "CREATED"


def main() -> int:
    # --- Argument parsing ---
    if len(sys.argv) != 2:
        print("Usage: python init_context.py <skill-name>")
        print("  skill-name must be kebab-case (e.g., my-api-analyzer)")
        return 1

    skill_name = sys.argv[1]

    if not validate_skill_name(skill_name):
        print(f"Error: '{skill_name}' is not valid kebab-case.")
        print("  Use lowercase letters, numbers, and hyphens only.")
        print("  Example: my-api-analyzer, error-handler, sequence-diagram")
        return 1

    # --- Detect project root ---
    project_root = find_project_root(Path.cwd())
    if project_root is None:
        print("Error: Could not find .claude/ directory.")
        print("  Run this script from within the project directory.")
        return 1

    print(f"Project root: {project_root}")

    # --- Resolve paths ---
    context_root = project_root / ".skill-context"
    skill_context_dir = context_root / skill_name
    resources_dir = skill_context_dir / "resources"
    script_dir = Path(__file__).resolve().parent
    templates_dir = script_dir.parent / "templates"

    # --- Prepare placeholders ---
    replacements = {
        "{skill_name}": skill_name,
        "{date}": date.today().isoformat(),
        "{author}": "Skill Architect",
    }

    # --- Create directories ---
    context_root.mkdir(exist_ok=True)
    skill_context_dir.mkdir(exist_ok=True)
    resources_dir.mkdir(exist_ok=True)

    print(f"\nContext directory: {skill_context_dir}")
    print("-" * 50)

    # --- Create files from templates ---
    results = []
    for output_name, template_name in TEMPLATE_FILES.items():
        raw_content = resolve_template_content(
            template_name, output_name, templates_dir
        )
        content = replace_placeholders(raw_content, replacements)
        filepath = skill_context_dir / output_name
        status = safe_create_file(filepath, content)
        results.append((output_name, status))
        print(f"  {output_name:20s} → {status}")

    # --- Summary ---
    created_count = sum(1 for _, s in results if s == "CREATED")
    skipped_count = sum(1 for _, s in results if "SKIPPED" in s)
    print(f"\nDone: {created_count} created, {skipped_count} skipped")
    print(f"Resources dir: {resources_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
