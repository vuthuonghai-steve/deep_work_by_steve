#!/usr/bin/env python3
"""
resource_scanner.py — UI Architecture Analyst Resource Discovery

Nhận --module M[X] argument → resolve paths của schema và diagram files
cho module đó → kiểm tra stub/empty → trả về JSON kết quả stdout.

Source: design.md §3 (Scripts), §8 R1 (Context Overflow guard), §9 Q3 (Placeholder detection)

Usage:
    python3 scripts/resource_scanner.py --module M1
    python3 scripts/resource_scanner.py --module M3 --project-root /path/to/project

Output (stdout, JSON):
    {
        "module": "M1",
        "schema": ["path/to/schema.yaml"],
        "diagrams": ["path/to/diagram.md", ...],
        "stubs": ["path/to/stub.md"],
        "missing": ["path/that/does/not/exist.md"],
        "warnings": ["warning message"]
    }

Exit codes:
    0 — Success (may still have stubs/missing, check JSON)
    1 — Invalid module argument
    2 — project root not found or module-paths data unavailable
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

VALID_MODULES = {"M1", "M2", "M3", "M4", "M5", "M6"}

# Placeholder/stub detection thresholds (resolved Q3: 2026-02-21)
STUB_SIZE_THRESHOLD = 200  # bytes — file smaller than this = stub

STUB_KEYWORDS = [
    "TODO",
    "placeholder",
    "...",
]

# Mermaid block types that might be empty stubs
MERMAID_BLOCK_MARKERS = [
    "graph ",
    "graph\n",
    "sequenceDiagram",
    "flowchart ",
    "flowchart\n",
    "classDiagram",
    "stateDiagram",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
]

# Module path mapping — embedded from resources/module-paths.md (JSON format)
# This avoids a file read dependency and keeps the script self-contained
MODULE_PATHS: dict[str, dict[str, list[str]]] = {
    "M1": {
        "schema": [
            "Docs/life-2/database/schema-design/m1-auth-schema.yaml"
        ],
        "sequence": [
            "Docs/life-2/diagrams/sequence-diagrams/detailed-m1-auth.md"
        ],
        "flow": [
            "Docs/life-2/diagrams/flow/flow-login-oauth.md"
        ],
        "class": [
            "Docs/life-2/diagrams/class-diagrams/m1-auth-profile"
        ],
        "activity": [
            "Docs/life-2/diagrams/activity-diagrams/m1-a2-login.md",
            "Docs/life-2/diagrams/activity-diagrams/m1-auth-profile-summary.md",
            "Docs/life-2/diagrams/activity-diagrams/m1-a1-registration.md",
            "Docs/life-2/diagrams/activity-diagrams/m1-a3-verification.md",
            "Docs/life-2/diagrams/activity-diagrams/m1-a5-onboarding.md",
            "Docs/life-2/diagrams/activity-diagrams/m1-a4-recovery.md",
        ],
    },
    "M2": {
        "schema": [
            "Docs/life-2/database/schema-design/m2-content-schema.yaml"
        ],
        "sequence": [
            "Docs/life-2/diagrams/sequence-diagrams/detailed-m2-content.md"
        ],
        "flow": [
            "Docs/life-2/diagrams/flow/flow-content-report.md"
        ],
        "class": [
            "Docs/life-2/diagrams/class-diagrams/m2-content-engine"
        ],
        "activity": [
            "Docs/life-2/diagrams/activity-diagrams/m2-a4-visibility.md",
            "Docs/life-2/diagrams/activity-diagrams/m2-content-engine-summary.md",
            "Docs/life-2/diagrams/activity-diagrams/m2-a2-media-handler.md",
            "Docs/life-2/diagrams/activity-diagrams/m2-a3-post-integrity.md",
            "Docs/life-2/diagrams/activity-diagrams/m2-a1-editor-pipeline.md",
        ],
    },
    "M3": {
        "schema": [
            "Docs/life-2/database/schema-design/m3-discovery-schema.yaml"
        ],
        "sequence": [
            "Docs/life-2/diagrams/sequence-diagrams/detailed-m3-discovery.md"
        ],
        "flow": [],
        "class": [
            "Docs/life-2/diagrams/class-diagrams/m3-discovery-feed"
        ],
        "activity": [
            "Docs/life-2/diagrams/activity-diagrams/m3-a2-search-engine.md",
            "Docs/life-2/diagrams/activity-diagrams/m3-a1-feed-assembler.md",
            "Docs/life-2/diagrams/activity-diagrams/m3-discovery-feed-summary.md",
            "Docs/life-2/diagrams/activity-diagrams/m3-a3-discovery-recommendation.md",
        ],
    },
    "M4": {
        "schema": [
            "Docs/life-2/database/schema-design/m4-engagement-schema.yaml"
        ],
        "sequence": [
            "Docs/life-2/diagrams/sequence-diagrams/detailed-m4-engagement.md"
        ],
        "flow": [],
        "class": [
            "Docs/life-2/diagrams/class-diagrams/m4-engagement"
        ],
        "activity": [
            "Docs/life-2/diagrams/activity-diagrams/m4-a3-connection-privacy.md",
            "Docs/life-2/diagrams/activity-diagrams/m4-a2-engagement-logic.md",
            "Docs/life-2/diagrams/activity-diagrams/m4-a1-friendship-handshake.md",
            "Docs/life-2/diagrams/activity-diagrams/m4-engagement-connections-summary.md",
        ],
    },
    "M5": {
        "schema": [
            "Docs/life-2/database/schema-design/m5-bookmarking-schema.yaml"
        ],
        "sequence": [
            "Docs/life-2/diagrams/sequence-diagrams/detailed-m5-bookmarking.md"
        ],
        "flow": [],
        "class": [
            "Docs/life-2/diagrams/class-diagrams/m5-bookmarking"
        ],
        "activity": [
            "Docs/life-2/diagrams/activity-diagrams/m5-bookmarking-summary.md",
            "Docs/life-2/diagrams/activity-diagrams/m5-a2-collection-orchestrator.md",
            "Docs/life-2/diagrams/activity-diagrams/m5-a1-bookmark-persistence.md",
        ],
    },
    "M6": {
        "schema": [
            "Docs/life-2/database/schema-design/m6-notifications-schema.yaml"
        ],
        "sequence": [
            "Docs/life-2/diagrams/sequence-diagrams/detailed-m6-safety.md"
        ],
        "flow": [],
        "class": [
            "Docs/life-2/diagrams/class-diagrams/m6-notifications-moderation"
        ],
        "activity": [
            "Docs/life-2/diagrams/activity-diagrams/m6-a2-report-pipeline.md",
            "Docs/life-2/diagrams/activity-diagrams/m6-notifications-moderation-summary.md",
            "Docs/life-2/diagrams/activity-diagrams/m6-a3-enforcement-action.md",
            "Docs/life-2/diagrams/activity-diagrams/m6-a1-sse-dispatcher.md",
        ],
    },
}

# ─── Stub Detection (Q3 resolution) ──────────────────────────────────────────


def _is_empty_mermaid_block(content: str) -> bool:
    """Check if a Mermaid diagram block exists but has no content nodes.

    Detects blocks like:
        ```mermaid
        graph LR
        ```
    Where the graph/sequence declaration exists but no nodes/edges follow.
    """
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]

    in_mermaid = False
    mermaid_content_lines = 0

    for line in lines:
        if line.startswith("```mermaid") or line == "```mermaid":
            in_mermaid = True
            mermaid_content_lines = 0
            continue

        if in_mermaid and line == "```":
            # End of mermaid block — check if it had content
            if mermaid_content_lines <= 1:
                # Only the declaration line (e.g., "graph LR") = empty stub
                return True
            in_mermaid = False
            continue

        if in_mermaid:
            # Check if this is just a block marker line (declaration) or actual content
            is_marker = any(line.startswith(m) for m in MERMAID_BLOCK_MARKERS)
            if not is_marker:
                mermaid_content_lines += 1

    return False


def is_stub(file_path: Path) -> tuple[bool, str]:
    """Determine if a file is a stub/placeholder.

    Returns (is_stub, reason).

    Detection criteria (Q3 resolved 2026-02-21):
    1. File size < STUB_SIZE_THRESHOLD bytes
    2. Content contains STUB_KEYWORDS
    3. Mermaid block exists but has no content nodes/edges
    """
    try:
        file_size = file_path.stat().st_size
    except OSError:
        return False, ""

    # Criterion 1: File too small
    if file_size < STUB_SIZE_THRESHOLD:
        return True, f"file size {file_size} bytes < {STUB_SIZE_THRESHOLD} bytes threshold"

    # Read content for keyword and Mermaid checks
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False, ""

    # Criterion 2: Contains stub keywords
    for keyword in STUB_KEYWORDS:
        if keyword in content:
            return True, f"contains stub keyword '{keyword}'"

    # Criterion 3: Empty Mermaid block
    if _is_empty_mermaid_block(content):
        return True, "contains Mermaid block with no content nodes/edges"

    return False, ""


# ─── Path Resolution ──────────────────────────────────────────────────────────


def resolve_project_root(start: Path) -> Path:
    """Walk up directory tree to find project root (contains Docs/ and CLAUDE.md)."""
    current = start.resolve()
    for _ in range(10):  # Max 10 levels up
        if (current / "CLAUDE.md").exists() or (current / "Docs").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return start.resolve()


def scan_module(module: str, project_root: Path) -> dict:
    """Scan all files for a given module, classify as OK / stub / missing."""
    if module not in MODULE_PATHS:
        raise ValueError(f"Unknown module: {module}. Valid: {sorted(VALID_MODULES)}")

    paths_config = MODULE_PATHS[module]

    schema_paths: list[str] = []
    diagram_paths: list[str] = []
    stubs: list[str] = []
    missing: list[str] = []
    warnings: list[str] = []

    # Collect all paths: schema is high-priority; diagrams = sequence + flow + class + activity
    all_schema = paths_config.get("schema", [])
    all_diagrams = (
        paths_config.get("sequence", [])
        + paths_config.get("flow", [])
        + paths_config.get("class", [])
        + paths_config.get("activity", [])
    )

    def classify_path(relative_path: str, category_list: list[str]) -> None:
        """Check a path, classify into schema/diagram/stubs/missing."""
        abs_path = project_root / relative_path

        # Handle directory paths (class diagrams may be dirs)
        if abs_path.is_dir():
            # Collect all .md files in the directory
            md_files = list(abs_path.glob("*.md")) + list(abs_path.glob("*.yaml"))
            if not md_files:
                missing.append(relative_path)
                return
            for f in md_files:
                rel = str(f.relative_to(project_root))
                stub_flag, reason = is_stub(f)
                if stub_flag:
                    stubs.append(rel)
                    warnings.append(f"STUB: {rel} ({reason})")
                else:
                    category_list.append(rel)
            return

        if not abs_path.exists():
            missing.append(relative_path)
            return

        stub_flag, reason = is_stub(abs_path)
        if stub_flag:
            stubs.append(relative_path)
            warnings.append(f"STUB: {relative_path} ({reason})")
        else:
            category_list.append(relative_path)

    for p in all_schema:
        classify_path(p, schema_paths)

    for p in all_diagrams:
        classify_path(p, diagram_paths)

    # Warn about modules with no flow diagrams (M3–M6 have no flow)
    if not paths_config.get("flow"):
        warnings.append(
            f"INFO: {module} has no flow diagrams in mapping. "
            "Activity and sequence diagrams will be used for interaction flow."
        )

    return {
        "module": module,
        "schema": schema_paths,
        "diagrams": diagram_paths,
        "stubs": stubs,
        "missing": missing,
        "warnings": warnings,
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resource_scanner",
        description=(
            "UI Architecture Analyst — Resource Discovery Tool\n"
            "Resolves schema and diagram file paths for a given module,\n"
            "detects stubs/placeholders, returns JSON to stdout."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Valid modules: {', '.join(sorted(VALID_MODULES))}

Examples:
  python3 scripts/resource_scanner.py --module M1
  python3 scripts/resource_scanner.py --module M3 --project-root /home/user/project

Output JSON fields:
  schema    — usable schema file paths
  diagrams  — usable diagram file paths
  stubs     — files detected as stubs/placeholders (trigger IP-3)
  missing   — files not found on disk (trigger IP-3)
  warnings  — informational messages
""",
    )
    parser.add_argument(
        "--module",
        required=True,
        metavar="M[X]",
        help=f"Module to scan. Must be one of: {', '.join(sorted(VALID_MODULES))}",
    )
    parser.add_argument(
        "--project-root",
        metavar="PATH",
        default=None,
        help="Project root directory (auto-detected if not specified)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=False,
        help="Pretty-print JSON output (default: compact)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # ── Validate module (Context Overflow Guard — R1) ───────────────────────
    module = args.module.strip().upper()
    if module not in VALID_MODULES:
        print(
            json.dumps({
                "error": (
                    f"Invalid module: '{args.module}'. "
                    f"Must be one of: {', '.join(sorted(VALID_MODULES))}. "
                    "This guard prevents context overflow from loading all modules at once."
                ),
                "valid_modules": sorted(VALID_MODULES),
            }),
            file=sys.stderr,
        )
        return 1

    # ── Resolve project root ─────────────────────────────────────────────────
    if args.project_root:
        project_root = Path(args.project_root)
        if not project_root.exists():
            print(
                json.dumps({"error": f"Project root not found: {args.project_root}"}),
                file=sys.stderr,
            )
            return 2
    else:
        # Auto-detect: walk up from script location
        script_dir = Path(__file__).parent
        project_root = resolve_project_root(script_dir)

    # ── Scan ─────────────────────────────────────────────────────────────────
    try:
        result = scan_module(module, project_root)
    except Exception as exc:
        print(
            json.dumps({"error": str(exc), "module": module}),
            file=sys.stderr,
        )
        return 2

    # ── Output ───────────────────────────────────────────────────────────────
    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
