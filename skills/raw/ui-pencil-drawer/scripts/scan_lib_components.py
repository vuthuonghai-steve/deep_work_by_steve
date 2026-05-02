"""
scan_lib_components.py — Lib-Component Scanner Reference

PURPOSE:
  This script documents the LOGIC for scanning Lib-Component in STi.pen.
  It does NOT directly call Pencil MCP — the AI agent executes this logic
  via batch_get() in Phase 0 Context Boot.

  Use this file to understand the data structure and processing steps
  that AI should replicate using Pencil MCP tools.

DESIGN NOTE (from design.md §9 Q4):
  Python scripts cannot call MCP tools directly. The AI agent performs
  batch_get() calls and processes the JSON response in-context.
  This script serves as: (1) a logic reference, (2) a post-processing
  helper if the AI exports batch_get results to a JSON file.

USAGE BY AI AGENT (Phase 0):
  1. Call batch_get with {patterns: [{reusable: true}], readDepth: 3}
  2. OR call batch_get with {patterns: [{name: "Lib-Component"}], readDepth: 3}
     to find the library frame first, then batch_get its children
  3. Process the response using the logic below (mentally, in-context)
  4. Store result as component_map in project_context

OUTPUT FORMAT:
  {
    "Button-Primary": "FEkTl",
    "Input-Text": "Njux9",
    "Input-Password": "Pq3mR",
    "Card-Post": "Ks7vX",
    ...
  }
"""

import json
import sys
from typing import Optional


def extract_component_name(node: dict) -> Optional[str]:
    """
    Extract human-readable component name from a Pencil node.
    Priority: node['name'] > node['context'] > node['id']
    """
    if node.get('name'):
        return node['name']
    if node.get('context'):
        # Context often contains descriptive names like "Primary button for CTA actions"
        # Extract first meaningful words
        context = node['context']
        return context[:50].strip()
    return None


def scan_reusable_nodes(batch_get_response: dict) -> dict:
    """
    Process the response from:
      batch_get({patterns: [{reusable: true}], readDepth: 3})

    Returns component_map: {name -> nodeId}

    Args:
        batch_get_response: The JSON response dict from batch_get tool

    Returns:
        dict: component_map mapping component names to their node IDs
    """
    component_map = {}
    nodes = batch_get_response.get('nodes', [])

    for node in nodes:
        # Only process nodes explicitly marked as reusable
        if not node.get('reusable', False):
            continue

        node_id = node.get('id')
        if not node_id:
            continue

        name = extract_component_name(node)
        if name:
            component_map[name] = node_id

            # Also register by id as fallback key
            # (useful when AI does fuzzy matching)
            component_map[f'__id_{node_id}'] = node_id

    return component_map


def fuzzy_match_component(query: str, component_map: dict) -> Optional[str]:
    """
    Find best-matching component nodeId for a given query name.
    Used when exact name doesn't exist in component_map.

    Strategy:
      1. Exact match (case-insensitive)
      2. Prefix match
      3. Substring match
      4. Return None if no match

    Args:
        query: Component name to search for (e.g., "input-email", "InputText")
        component_map: Dict from scan_reusable_nodes()

    Returns:
        str: node ID of best match, or None
    """
    query_normalized = query.lower().replace('-', '').replace('_', '').replace(' ', '')

    # Pass 1: Exact match (case-insensitive)
    for name, node_id in component_map.items():
        if name.startswith('__id_'):
            continue
        if name.lower() == query.lower():
            return node_id

    # Pass 2: Normalized exact match
    for name, node_id in component_map.items():
        if name.startswith('__id_'):
            continue
        name_normalized = name.lower().replace('-', '').replace('_', '').replace(' ', '')
        if name_normalized == query_normalized:
            return node_id

    # Pass 3: Substring match (query is contained in name OR name in query)
    matches = []
    for name, node_id in component_map.items():
        if name.startswith('__id_'):
            continue
        name_normalized = name.lower().replace('-', '').replace('_', '').replace(' ', '')
        if query_normalized in name_normalized or name_normalized in query_normalized:
            matches.append((name, node_id))

    if matches:
        # Return shortest match (most specific)
        matches.sort(key=lambda x: len(x[0]))
        return matches[0][1]

    return None


def resolve_blueprint_refs(blueprint_text: str, component_map: dict) -> tuple[str, list]:
    """
    Resolve all CAPS_UNDERSCORE placeholder IDs in a wireframe blueprint
    to real Pencil node IDs from component_map.

    Args:
        blueprint_text: Raw wireframe blueprint markdown text
        component_map: From scan_reusable_nodes()

    Returns:
        tuple: (resolved_blueprint_text, list_of_unresolved_refs)
    """
    import re

    unresolved = []
    # Pattern: ref: CAPS_UNDERSCORE_ID (uppercase letters and underscores)
    placeholder_pattern = re.compile(r'ref:\s+([A-Z][A-Z0-9_]+(?:_ID)?)')

    def resolve_match(match):
        placeholder = match.group(1)
        # Strip _ID suffix for component name lookup
        query = placeholder.replace('_ID', '').replace('_', '-').lower()

        node_id = fuzzy_match_component(query, component_map)
        if node_id:
            return f'ref: {node_id}  # resolved from: {placeholder}'
        else:
            unresolved.append(placeholder)
            return f'ref: MISSING_{placeholder}  # ⚠️ not found in Lib-Component'

    resolved = placeholder_pattern.sub(resolve_match, blueprint_text)
    return resolved, unresolved


def save_component_map(component_map: dict, output_path: str = 'component-map.json'):
    """
    Save component_map to JSON file for reference/debugging.
    Optional — AI agent holds this in-context, no file I/O required.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # Exclude internal __id_ keys from export
        clean_map = {k: v for k, v in component_map.items() if not k.startswith('__id_')}
        json.dump(clean_map, f, ensure_ascii=False, indent=2)
    print(f"✅ Component map saved: {output_path} ({len(clean_map)} components)")


def main():
    """
    CLI entry point — for when batch_get output is piped as JSON.

    Usage:
      # If AI exported batch_get response to a file:
      python scan_lib_components.py batch_get_response.json

      # Output: component-map.json + printed summary
    """
    if len(sys.argv) < 2:
        print("Usage: python scan_lib_components.py <batch_get_response.json>")
        print("       Input: JSON file from Pencil batch_get response")
        print("       Output: component-map.json")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            response = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {input_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    component_map = scan_reusable_nodes(response)

    if not component_map:
        print("⚠️ No reusable components found in response.")
        print("   Check: Does response contain nodes with reusable: true?")
        sys.exit(1)

    # Print summary
    clean_map = {k: v for k, v in component_map.items() if not k.startswith('__id_')}
    print(f"\n📦 Found {len(clean_map)} reusable components:\n")
    for name, node_id in sorted(clean_map.items()):
        print(f"  {name:<40} → {node_id}")

    # Save to file
    save_component_map(component_map)


if __name__ == '__main__':
    main()
