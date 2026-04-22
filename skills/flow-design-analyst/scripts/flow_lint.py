#!/usr/bin/env python3
"""
flow_lint.py — Mermaid Flowchart Linter for flow-design-analyst skill

Usage:
  python scripts/flow_lint.py <mermaid_file_or_string> [--verbose]

Trigger: Khi diagram có trên 15 nodes (per design.md §7 Tầng 2)

Detects:
  1. Orphan nodes (khai báo nhưng không có edge nào)
  2. Decision nodes ({}) chỉ có 1 nhánh output (incomplete diamond)
  3. Ký tự \\n trong label string (phải dùng <br/> thay thế)
  4. Label có ký tự đặc biệt nhưng thiếu quotes ""

Exit codes:
  0 = PASS (no issues found)
  1 = FAIL (issues found — list printed to stdout)
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LintIssue:
    line: int
    code: str
    message: str
    severity: str = "ERROR"  # "ERROR" | "WARNING"


def extract_mermaid_content(text: str) -> str:
    """Extract content from ```mermaid ``` blocks or return as-is."""
    pattern = r"```mermaid\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def get_node_ids(lines: list[str]) -> dict[str, int]:
    """Extract all node IDs and their line numbers from flowchart."""
    node_ids: dict[str, int] = {}
    # Match node declarations: id[...], id(...), id{...}, id[(...)], etc.
    node_pattern = re.compile(
        r"^\s*([a-zA-Z][a-zA-Z0-9_]*)"  # node ID
        r"\s*[\[\(\{]"  # opening bracket
    )
    for i, line in enumerate(lines, 1):
        line_clean = line.strip()
        # Skip comments and keywords
        if line_clean.startswith("%%") or line_clean.startswith("subgraph") or line_clean.startswith("end") or line_clean.startswith("direction") or line_clean.startswith("flowchart"):
            continue
        m = node_pattern.match(line)
        if m:
            nid = m.group(1)
            if nid not in ("subgraph", "end", "direction", "flowchart", "TD", "LR", "TB"):
                node_ids[nid] = i
    return node_ids


def get_edges(lines: list[str]) -> dict[str, list[str]]:
    """Build adjacency: source_id -> [target_ids]"""
    adjacency: dict[str, list[str]] = {}
    # Match edges: A --> B, A -- "label" --> B, A -.-> B, etc.
    edge_pattern = re.compile(
        r"([a-zA-Z][a-zA-Z0-9_]*)"  # source
        r"\s*(?:-->|--[^>]*-->|-\.->|==+>|---[ox]?)"  # connectors
        r"\s*([a-zA-Z][a-zA-Z0-9_]*)"  # target
    )
    out_degree: dict[str, set[str]] = {}
    connected_as_target: set[str] = set()

    for line in lines:
        line_clean = line.strip()
        if line_clean.startswith("%%"):
            continue
        for m in edge_pattern.finditer(line_clean):
            src, tgt = m.group(1), m.group(2)
            if src not in out_degree:
                out_degree[src] = set()
            out_degree[src].add(tgt)
            connected_as_target.add(tgt)

    # Build final adjacency
    for src, targets in out_degree.items():
        adjacency[src] = list(targets)

    return adjacency, connected_as_target


def check_orphan_nodes(
    node_ids: dict[str, int],
    adjacency: dict[str, list[str]],
    connected_as_target: set[str],
) -> list[LintIssue]:
    """Check 1: Node declared but has no edges (orphan)."""
    issues = []
    for nid, lineno in node_ids.items():
        has_out = nid in adjacency and len(adjacency[nid]) > 0
        has_in = nid in connected_as_target
        if not has_out and not has_in:
            issues.append(LintIssue(
                line=lineno,
                code="ORPHAN_NODE",
                message=f"Node '{nid}' khai báo nhưng không có edge nào (orphan node)",
                severity="ERROR"
            ))
    return issues


def check_decision_completeness(lines: list[str]) -> list[LintIssue]:
    """Check 2: Decision node {} has only 1 output branch."""
    issues = []
    # Find decision node IDs: id{...} or id{"..."}
    decision_pattern = re.compile(r"([a-zA-Z][a-zA-Z0-9_]*)\s*\{")
    edge_from_pattern = re.compile(r"([a-zA-Z][a-zA-Z0-9_]*)\s*(?:-->|--[^>]*->|-\.->|==+>)")

    decision_nodes: set[str] = set()
    out_edges: dict[str, int] = {}

    for i, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith("%%"):
            continue
        # Find declaration of decision node
        for m in decision_pattern.finditer(line_clean):
            nid = m.group(1)
            if nid not in ("subgraph",):
                decision_nodes.add(nid)

    for line in lines:
        line_clean = line.strip()
        if line_clean.startswith("%%"):
            continue
        for m in edge_from_pattern.finditer(line_clean):
            src = m.group(1)
            if src in decision_nodes:
                out_edges[src] = out_edges.get(src, 0) + 1

    for nid in decision_nodes:
        count = out_edges.get(nid, 0)
        if count < 2:
            issues.append(LintIssue(
                line=0,  # Line unknown without more parsing
                code="INCOMPLETE_DECISION",
                message=f"Decision node '{nid}' chỉ có {count} nhánh output — cần ≥ 2 nhánh",
                severity="ERROR"
            ))
    return issues


def check_newline_in_labels(lines: list[str]) -> list[LintIssue]:
    """Check 3: \\n inside label strings (should use <br/> instead)."""
    issues = []
    label_pattern = re.compile(r'"[^"]*\\n[^"]*"')
    for i, line in enumerate(lines, 1):
        if label_pattern.search(line):
            issues.append(LintIssue(
                line=i,
                code="NEWLINE_IN_LABEL",
                message=r"Tìm thấy '\n' trong label — hãy dùng '<br/>' thay thế",
                severity="ERROR"
            ))
    return issues


def check_unquoted_special_chars(lines: list[str]) -> list[LintIssue]:
    """Check 4: Label with special chars but missing quotes."""
    issues = []
    # Pattern: node declaration with label NOT in quotes but containing special chars
    # Match: id[some text without quotes]
    unquoted_pattern = re.compile(
        r"[a-zA-Z][a-zA-Z0-9_]*"  # node ID
        r"\s*[\[\(]"               # opening bracket
        r"(?!\")"                  # NOT followed by quote
        r"([^\]\)\"]+)"            # content without quote
        r"[\]\)]"                  # closing bracket
    )
    special_chars = set("(){}:/?,&")

    for i, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith("%%") or line_clean.startswith("subgraph"):
            continue
        for m in unquoted_pattern.finditer(line_clean):
            content = m.group(1)
            if any(c in content for c in special_chars):
                issues.append(LintIssue(
                    line=i,
                    code="UNQUOTED_SPECIAL_CHARS",
                    message=f'Label chứa ký tự đặc biệt nhưng thiếu quotes: [{content}]',
                    severity="WARNING"
                ))
    return issues


def lint_mermaid(content: str, verbose: bool = False) -> tuple[list[LintIssue], int]:
    """Run all lint checks and return issues + node count."""
    lines = content.split("\n")

    # Count nodes for logging
    node_ids = get_node_ids(lines)
    node_count = len(node_ids)

    try:
        adjacency, connected_as_target = get_edges(lines)
    except Exception:
        adjacency, connected_as_target = {}, set()

    all_issues: list[LintIssue] = []
    all_issues.extend(check_orphan_nodes(node_ids, adjacency, connected_as_target))
    all_issues.extend(check_decision_completeness(lines))
    all_issues.extend(check_newline_in_labels(lines))
    all_issues.extend(check_unquoted_special_chars(lines))

    return all_issues, node_count


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="flow_lint.py — Mermaid flowchart linter for flow-design-analyst"
    )
    parser.add_argument("input", help="Path to .md or .mmd file, or Mermaid code string")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    # Read input
    path = Path(args.input)
    if path.exists():
        content = path.read_text(encoding="utf-8")
    else:
        content = args.input

    mermaid_content = extract_mermaid_content(content)
    issues, node_count = lint_mermaid(mermaid_content, args.verbose)

    print(f"\n🔍 flow_lint.py — Mermaid Flowchart Linter")
    print(f"📊 Nodes detected: {node_count}")

    if node_count < 15:
        print(f"ℹ️  Note: Diagram có {node_count} nodes (< 15 threshold). Lint vẫn chạy.")

    if not issues:
        print(f"✅ PASS — Không có issues nào được phát hiện.\n")
        sys.exit(0)
    else:
        errors = [i for i in issues if i.severity == "ERROR"]
        warnings = [i for i in issues if i.severity == "WARNING"]

        print(f"\n❌ FAIL — Tìm thấy {len(errors)} ERROR(s) và {len(warnings)} WARNING(s):\n")
        for issue in sorted(issues, key=lambda x: x.line):
            prefix = "❌ ERROR" if issue.severity == "ERROR" else "⚠️  WARN"
            line_info = f"[L{issue.line}]" if issue.line > 0 else "[?]"
            print(f"  {prefix} {line_info} [{issue.code}] {issue.message}")

        print(f"\n📖 Tham khảo: knowledge/mermaid-flowchart-guide.md §4 và loop/flow-checklist.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
