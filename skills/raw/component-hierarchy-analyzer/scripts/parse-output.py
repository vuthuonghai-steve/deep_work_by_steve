#!/usr/bin/env python3
"""
parse-output.py - Parse ASCII tree output and convert to JSON

Usage:
    python scripts/parse-output.py --ascii <ascii_output> --query <query_json>

This script:
- Parses ASCII tree output from generate-component-hierarchy.ts
- Converts to structured JSON matching the schema
- Handles special markers (recursive, ancestor chain)
- Returns JSON with query, root, metadata, warnings, errors
"""

import re
import json
import sys
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    """Represents a node in the component hierarchy tree."""
    name: str
    type: str
    file_path: Optional[str]
    depth: int
    relationship: str
    layout: Optional[str] = None
    module: Optional[str] = None
    recursive: bool = False
    duplicate: bool = False
    children: List['TreeNode'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "filePath": self.file_path,
            "depth": self.depth,
            "relationship": self.relationship,
            "layout": self.layout,
            "module": self.module,
            "recursive": self.recursive,
            "duplicate": self.duplicate,
            "children": [child.to_dict() for child in self.children]
        }


def parse_ascii_line(line: str) -> Optional[Dict[str, Any]]:
    """
    Parse a single ASCII tree line.

    Expected format:
    [ComponentName] - filePath (layout) ↺
    ★ [ComponentName] - filePath (layout) [N children]

    Returns:
        Dictionary with parsed components or None if line doesn't match
    """
    # Remove leading/trailing whitespace
    line = line.strip()
    if not line:
        return None

    # Check for ancestor chain marker
    is_ancestor = line.startswith("★")
    if is_ancestor:
        line = line[1:].strip()

    # Extract component name in brackets
    name_match = re.match(r'\[([^\]]+)\]', line)
    if not name_match:
        return None

    name = name_match.group(1)

    # Extract file path after " - "
    file_match = re.search(r'-\s*([^\(]+)', line)
    file_path = file_match.group(1).strip() if file_match else None

    # Extract layout in parentheses
    layout_match = re.search(r'\(([^)]+)\)', line)
    layout = layout_match.group(1).strip() if layout_match else None

    # Extract module name (if file path is just a module name like "expo-router")
    module = None
    if file_path and not (file_path.endswith('.tsx') or file_path.endswith('.ts') or 
                          file_path.endswith('.jsx') or file_path.endswith('.js') or
                          '/' in file_path):
        module = file_path
        file_path = None

    # Check for recursive marker
    recursive = "↺" in line

    # Check for children count (in ancestor mode)
    children_count = None
    count_match = re.search(r'\[(\d+) children?\]', line)
    if count_match:
        children_count = int(count_match.group(1))

    # Infer component type
    if file_path:
        if "screen" in file_path.lower() or "page" in file_path.lower():
            comp_type = "screen"
        elif "layout" in file_path.lower():
            comp_type = "layout"
        elif "provider" in file_path.lower():
            comp_type = "provider"
        else:
            comp_type = "component"
    elif module:
        comp_type = "framework"
    else:
        comp_type = "unknown"

    return {
        "name": name,
        "type": comp_type,
        "filePath": file_path,
        "layout": layout,
        "module": module,
        "recursive": recursive,
        "is_ancestor": is_ancestor,
        "children_count": children_count
    }


def calculate_depth(line: str) -> int:
    """
    Calculate depth based on tree characters and indentation.

    Tree characters:
    ├──  (mid)
    └──  (last)
    │    (vertical continuation)

    Returns:
        Depth level (0 for root)
    """
    # Count tree prefixes
    depth = 0
    for char in line:
        if char in ['│', '├', '└']:
            depth += 1
        elif char == ' ':
            continue
        else:
            break
    return depth


def build_tree_from_ascii(lines: List[str]) -> tuple[Optional[TreeNode], List[str]]:
    """
    Build tree structure from ASCII lines.

    Args:
        lines: List of ASCII tree output lines

    Returns:
        Tuple of (root_node, warnings)
    """
    if not lines:
        return None, ["Empty output from script"]

    warnings = []
    nodes: List[Dict[str, Any]] = []
    depths: List[int] = []

    # Parse all lines
    for line in lines:
        parsed = parse_ascii_line(line)
        if parsed:
            depth = calculate_depth(line)
            parsed["depth"] = depth
            nodes.append(parsed)
            depths.append(depth)

    if not nodes:
        return None, ["No valid component lines found in output"]

    # Build tree structure
    root_data = nodes[0]
    root = TreeNode(
        name=root_data["name"],
        type=root_data["type"],
        file_path=root_data["filePath"],
        depth=0,
        relationship="root",
        layout=root_data["layout"],
        module=root_data["module"],
        recursive=root_data["recursive"]
    )

    if root_data["recursive"]:
        warnings.append(f"Recursive component detected: {root.name}")

    # Stack to track current path
    stack: List[TreeNode] = [root]
    last_depth = 0

    for i in range(1, len(nodes)):
        node_data = nodes[i]
        current_depth = node_data["depth"]

        # Pop stack to correct parent level
        while len(stack) > current_depth + 1:
            stack.pop()

        parent = stack[-1]

        # Create child node
        child = TreeNode(
            name=node_data["name"],
            type=node_data["type"],
            file_path=node_data["filePath"],
            depth=current_depth,
            relationship="child",
            layout=node_data["layout"],
            module=node_data["module"],
            recursive=node_data["recursive"]
        )

        if node_data["recursive"]:
            warnings.append(f"Recursive component detected: {child.name}")

        # Check for duplicates
        child_key = f"{child.name}@{child.file_path}"
        # Simple duplicate check - in production, would track all seen keys
        # For now, just mark as duplicate if same name appears at same depth
        if any(c.name == child.name and c.depth == child.depth for c in parent.children):
            child.duplicate = True

        parent.children.append(child)
        stack.append(child)

    return root, warnings


def parse_output(
    ascii_output: str,
    query: Dict[str, Any],
    command: str,
    exit_code: int
) -> Dict[str, Any]:
    """
    Parse ASCII output and convert to JSON.

    Args:
        ascii_output: Raw ASCII tree output
        query: Query parameters used
        command: Command that was executed
        exit_code: Exit code from script execution

    Returns:
        JSON structure with query, root, metadata, warnings, errors
    """
    lines = ascii_output.strip().split('\n')
    errors = []
    warnings = []

    try:
        root, parse_warnings = build_tree_from_ascii(lines)
        warnings.extend(parse_warnings)

        if root is None:
            # Fallback: return raw output
            return {
                "query": query,
                "rawOutput": ascii_output,
                "metadata": {
                    "command": command,
                    "exitCode": exit_code,
                    "parserVersion": "0.1.0",
                    "sourceFormat": "ascii-tree"
                },
                "warnings": warnings,
                "errors": parse_warnings if parse_warnings else ["Failed to parse tree structure"]
            }

        return {
            "query": query,
            "root": root.to_dict(),
            "metadata": {
                "command": command,
                "exitCode": exit_code,
                "parserVersion": "0.1.0",
                "sourceFormat": "ascii-tree"
            },
            "warnings": warnings,
            "errors": errors
        }

    except Exception as e:
        errors.append(f"Parse error: {str(e)}")
        return {
            "query": query,
            "rawOutput": ascii_output,
            "metadata": {
                "command": command,
                "exitCode": exit_code,
                "parserVersion": "0.1.0",
                "sourceFormat": "ascii-tree"
            },
            "warnings": warnings,
            "errors": errors
        }


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Parse ASCII tree output to JSON")
    parser.add_argument("--ascii", required=True, help="ASCII tree output string")
    parser.add_argument("--query", required=True, help="Query parameters as JSON string")
    parser.add_argument("--command", required=True, help="Command that was executed")
    parser.add_argument("--exit-code", type=int, default=0, help="Exit code from script")

    args = parser.parse_args()

    query = json.loads(args.query)
    result = parse_output(
        ascii_output=args.ascii,
        query=query,
        command=args.command,
        exit_code=args.exit_code
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if not result["errors"] else 1)


if __name__ == "__main__":
    main()
