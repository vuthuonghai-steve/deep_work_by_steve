#!/usr/bin/env python3
"""
validate_zone_mapping.py — Validate §3 Zone Mapping against schema

Usage:
    python validate_zone_mapping.py <design_path>

Exit Codes:
    0 = PASS
    1 = FAIL (validation errors)
    2 = EMERGENCY (parse error)
"""

import sys
import json
import yaml
import re
from pathlib import Path

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown file"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))

def extract_zone_mapping_section(content):
    """Extract Zone Mapping section from markdown"""
    pattern = r'##\s+3\.\s+Zone\s+Mapping.*?\n(.*?)(?=\n##\s+|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def parse_zone_table(section_content):
    """Parse markdown table into zone data"""
    lines = section_content.split('\n')
    zones = {}
    
    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        # Skip header row
        if 'Zone' in line and 'Files' in line:
            continue
        # Skip separator rows (all dashes)
        if set(line.replace('|', '').replace('-', '').replace(' ', '')) == set():
            continue
        if line.count('|') < 3:
            continue
        
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) >= 3:
            zone_name = parts[0].lower().strip()
            # Skip if zone name is just dashes or empty
            if not zone_name or zone_name.startswith('-'):
                continue
            files = parts[1].strip()
            content = parts[2].strip()
            mandatory = parts[3].strip() if len(parts) > 3 else ''
            
            zones[zone_name] = {
                'files': files,
                'content': content,
                'mandatory': mandatory
            }
    
    return zones

def validate_zone_mapping(design_path):
    """Main validation function"""
    
    path = Path(design_path)
    if not path.exists():
        return {
            "status": "ERROR",
            "error": f"File not found: {design_path}",
            "exit_code": 2
        }
    
    try:
        content = path.read_text()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": f"Cannot read file: {e}",
            "exit_code": 2
        }
    
    frontmatter = extract_frontmatter(content)
    if not frontmatter:
        return {
            "status": "ERROR",
            "error": "No YAML frontmatter found",
            "exit_code": 2
        }
    
    # Extract §3 Zone Mapping
    section3 = extract_zone_mapping_section(content)
    if not section3:
        return {
            "status": "FAIL",
            "errors": ["§3 Zone Mapping section not found or empty"],
            "exit_code": 1
        }
    
    # Parse table
    zones = parse_zone_table(section3)
    if not zones:
        return {
            "status": "FAIL",
            "errors": ["Could not parse Zone Mapping table"],
            "exit_code": 1
        }
    
    errors = []
    warnings = []
    
    # Validate required zones
    required_zones = ['core']
    for zone in required_zones:
        # Check both exact match and partial match
        zone_found = any(zone in z or z.startswith(zone) for z in zones.keys())
        if not zone_found:
            errors.append(f"Required zone '{zone}' not found in mapping")
    
    # Validate each zone
    for zone_name, zone_data in zones.items():
        files = zone_data.get('files', '')
        content = zone_data.get('content', '')
        mandatory = zone_data.get('mandatory', '')
        
        # Check for empty cells
        if not files or files == '—' or files == '-':
            errors.append(f"Zone '{zone_name}': Files column is empty")
        
        # Check for placeholder text
        placeholder_patterns = ['...', 'xxx', 'example', 'tùy chọn']
        for pattern in placeholder_patterns:
            if pattern.lower() in files.lower():
                warnings.append(f"Zone '{zone_name}': Files may contain placeholder '{pattern}'")
        
        # Core must be mandatory
        if zone_name == 'core' and '✅' not in mandatory and 'yes' not in mandatory.lower():
            warnings.append("Zone 'core': Should be marked as mandatory (✅)")
    
    # Validate coherence with frontmatter zone_mapping
    frontmatter_zones = frontmatter.get('zone_mapping', {})
    if frontmatter_zones:
        fm_zone_names = [z for z in frontmatter_zones.get('zones', {}).keys()]
        table_zone_names = list(zones.keys())
        
        for z in fm_zone_names:
            if z not in table_zone_names:
                warnings.append(f"Zone '{z}' in frontmatter not found in §3 table")
    
    result = {
        "status": "PASS" if not errors else "FAIL",
        "zones_found": len(zones),
        "zones": zones,
        "errors": errors,
        "warnings": warnings,
        "exit_code": 0 if not errors else 1
    }
    
    return result

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: validate_zone_mapping.py <design_path>",
            "exit_code": 1
        }, indent=2))
        sys.exit(1)
    
    design_path = sys.argv[1]
    result = validate_zone_mapping(design_path)
    
    print(json.dumps(result, indent=2))
    sys.exit(result.get('exit_code', 1))

if __name__ == "__main__":
    main()
