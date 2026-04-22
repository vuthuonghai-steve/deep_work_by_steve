#!/usr/bin/env python3
"""
extract_entities.py — Extract entity definitions từ er-diagram.md

Usage:
    python scripts/extract_entities.py --module M1 --er path/to/er-diagram.md
    python scripts/extract_entities.py --module M2 --er Docs/life-2/diagrams/er-diagram.md

Output: JSON hoặc YAML stdout với entity list + fields, relationships

Source: design.md §4 Task 4.1, todo.md Task 4.1 [PORTABLE]
Dependencies: re (built-in Python) — không cần install thư viện ngoài
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Thêm scripts/ vào sys.path để import type_resolver
sys.path.insert(0, str(Path(__file__).parent))
from type_resolver import resolve_types


def load_module_map(module_map_path: str) -> dict:
    """Load module-map.yaml để biết entity list cho từng module."""
    try:
        import yaml
        with open(module_map_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback: parse YAML thủ công với regex cho cấu trúc đơn giản
        return _parse_simple_yaml(module_map_path)
    except FileNotFoundError:
        print(f"ERROR: module-map.yaml không tìm thấy tại {module_map_path}", file=sys.stderr)
        sys.exit(1)


def _parse_simple_yaml(path: str) -> dict:
    """Fallback YAML parser đơn giản dùng re — parse module-map.yaml format."""
    result = {}
    current_module = None
    current_entities = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            # Module key: M1:, M2:, ...
            m = re.match(r'^(M\d+):\s*$', line)
            if m:
                if current_module:
                    result[current_module]['entities'] = current_entities
                current_module = m.group(1)
                result[current_module] = {'entities': []}
                current_entities = []
                continue
            # Entity slug: "    - slug: users"
            m = re.match(r'\s+- slug:\s+(\S+)', line)
            if m and current_module:
                current_entities.append({'slug': m.group(1)})
                continue
            # aggregate_root
            m = re.match(r'\s+aggregate_root:\s+(true|false)', line)
            if m and current_entities:
                current_entities[-1]['aggregate_root'] = m.group(1) == 'true'
                continue
            # embed_in
            m = re.match(r'\s+embed_in:\s+(\S+)', line)
            if m and current_entities:
                current_entities[-1]['embed_in'] = m.group(1)
                continue

    if current_module:
        result[current_module]['entities'] = current_entities

    return result


def get_entities_for_module(module_map: dict, module_id: str) -> list[dict]:
    """Lấy entity list cho module, bỏ qua embedded entities."""
    module_data = module_map.get(module_id.upper(), {})
    entities = module_data.get('entities', [])
    # Chỉ lấy aggregate root — skip embedded
    return [e for e in entities if e.get('aggregate_root', True) and not e.get('embed_in')]


def parse_er_diagram(er_path: str, entity_slugs: list[str]) -> dict:
    """
    Parse er-diagram.md để extract field definitions cho các entity cần thiết.

    ER Diagram format thường có:
    - Entity sections: ### ENTITY_NAME hay ## ENTITY_NAME
    - Field definitions: | fieldName | type | constraints |
    - Hoặc dạng code block với SQL-like syntax
    """
    if not os.path.exists(er_path):
        print(f"ERROR: er-diagram.md không tìm thấy tại {er_path}", file=sys.stderr)
        sys.exit(1)

    with open(er_path, encoding="utf-8") as f:
        content = f.read()

    entities = {}
    for slug in entity_slugs:
        entities[slug] = _extract_entity_fields(content, slug)

    return entities


def _extract_entity_fields(content: str, slug: str) -> dict:
    """
    Extract fields cho một entity cụ thể từ ER content.
    Hỗ trợ nhiều format phổ biến trong er-diagram.md.
    """
    entity_info = {
        'slug': slug,
        'fields': [],
        'relationships': [],
        'source': 'er-diagram.md'
    }

    # Pattern 1: Markdown table format
    # Tìm section của entity (heading)
    slug_upper = slug.upper()
    # Tìm đoạn content của entity
    section_pattern = rf'#+\s+{re.escape(slug_upper)}[^\n]*\n(.*?)(?=\n#+\s+[A-Z_]+|\Z)'
    section_match = re.search(section_pattern, content, re.DOTALL | re.IGNORECASE)

    if section_match:
        section_content = section_match.group(1)
        # Parse markdown table rows: | field | type | ... |
        table_row_pattern = r'\|\s*(`?)(\w+)\1\s*\|\s*(\w+(?:\[\])?)\s*\|([^|]*)\|'
        for m in re.finditer(table_row_pattern, section_content):
            field_name = m.group(2)
            field_type = m.group(3).strip()
            constraints_str = m.group(4).strip()

            # Skip header rows
            if field_name.lower() in ('field', 'column', 'name', 'attribute', 'property'):
                continue

            field_info = {
                'name': field_name,
                'raw_type': field_type,
                'constraints': _parse_constraints(constraints_str),
                'source': f'er-diagram.md#{slug_upper}.{field_name}'
            }
            entity_info['fields'].append(field_info)

    # Pattern 2: SQL CREATE TABLE trong code block
    sql_pattern = rf'(?i)CREATE\s+TABLE\s+`?{re.escape(slug)}`?\s*\((.*?)\)'
    sql_match = re.search(sql_pattern, content, re.DOTALL)
    if sql_match and not entity_info['fields']:
        sql_body = sql_match.group(1)
        col_pattern = r'`(\w+)`\s+(\w+(?:\(\d+(?:,\d+)?\))?)'
        for m in re.finditer(col_pattern, sql_body):
            col_name = m.group(1)
            col_type = m.group(2)
            if col_name.upper() in ('PRIMARY', 'UNIQUE', 'INDEX', 'KEY', 'FOREIGN', 'CONSTRAINT'):
                continue
            entity_info['fields'].append({
                'name': col_name,
                'raw_type': col_type,
                'constraints': {},
                'source': f'er-diagram.md#{slug_upper}.{col_name}'
            })

    return entity_info


def _parse_constraints(constraints_str: str) -> dict:
    """Parse constraint string thành dict."""
    constraints = {}
    if 'NOT NULL' in constraints_str.upper() or 'required' in constraints_str.lower():
        constraints['required'] = True
    if 'UNIQUE' in constraints_str.upper() or 'unique' in constraints_str.lower():
        constraints['unique'] = True
    if 'INDEX' in constraints_str.upper() or 'indexed' in constraints_str.lower():
        constraints['indexed'] = True
    return constraints


def map_to_payload_type(raw_type: str, allowed_types: list[str]) -> str:
    """Map raw ER type sang PayloadCMS type."""
    type_mapping = {
        'varchar': 'text', 'string': 'text', 'char': 'text',
        'text': 'text', 'longtext': 'richText', 'mediumtext': 'richText',
        'int': 'number', 'integer': 'number', 'bigint': 'number',
        'float': 'number', 'double': 'number', 'decimal': 'number',
        'bool': 'boolean', 'boolean': 'boolean', 'tinyint': 'boolean',
        'datetime': 'date', 'timestamp': 'date', 'date': 'date',
        'email': 'email',
        'json': 'json', 'jsonb': 'json',
        'objectid': 'relationship', 'uuid': 'text',
    }

    raw_lower = raw_type.lower().split('(')[0]  # strip (255) etc
    payload_type = type_mapping.get(raw_lower, 'text')

    # Verify nằm trong whitelist
    if payload_type not in allowed_types:
        payload_type = 'text'  # safe fallback

    return payload_type


def main():
    parser = argparse.ArgumentParser(
        description='Extract entities từ er-diagram.md cho một module cụ thể'
    )
    parser.add_argument('--module', required=True, help='Module ID: M1, M2, M3, M4, M5, M6')
    parser.add_argument('--er', required=True, help='Path đến er-diagram.md')
    parser.add_argument('--module-map', default=None, help='Path đến module-map.yaml (optional)')
    parser.add_argument('--project-root', default=None, help='Project root để resolve types')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json', help='Output format')

    args = parser.parse_args()

    # Tìm module-map.yaml nếu không được chỉ định
    if not args.module_map:
        skill_root = Path(__file__).parent.parent
        args.module_map = str(skill_root / 'data' / 'module-map.yaml')

    # Load types whitelist
    allowed_types = resolve_types(args.project_root).get('allowed_field_types', [])

    # Load module map
    module_map = load_module_map(args.module_map)

    # Get entity slugs cho module
    entities_info = get_entities_for_module(module_map, args.module)
    entity_slugs = [e['slug'] for e in entities_info]

    if not entity_slugs:
        print(f"WARNING: Không tìm thấy entity nào cho module {args.module}", file=sys.stderr)
        print(json.dumps({'module': args.module, 'entities': []}))
        return

    # Parse ER diagram
    extracted = parse_er_diagram(args.er, entity_slugs)

    # Map types và format output
    output_entities = []
    for entity_slug, entity_data in extracted.items():
        module_entity_meta = next(
            (e for e in entities_info if e.get('slug') == entity_slug), {}
        )

        # Map field types
        for field in entity_data['fields']:
            field['type'] = map_to_payload_type(field['raw_type'], allowed_types)

        output_entities.append({
            'slug': entity_slug,
            'aggregate_root': module_entity_meta.get('aggregate_root', True),
            'fields': entity_data['fields'],
            'relationships': entity_data['relationships'],
            'source': entity_data['source']
        })

    result = {
        'module': args.module.upper(),
        'entities': output_entities,
        'total': len(output_entities)
    }

    # Output
    if args.format == 'yaml':
        try:
            import yaml
            print(yaml.dump(result, default_flow_style=False, allow_unicode=True))
        except ImportError:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
