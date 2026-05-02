#!/usr/bin/env python3
"""
Validate Input Normalization Output

Usage:
    python validate_normalization.py <module> <output_dir>

Example:
    python validate_normalization.py M1 Docs/life-2/normalization/
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any


def load_schema(schema_path: str) -> Dict:
    """Load input schema from YAML file."""
    with open(schema_path, 'r') as f:
        content = f.read()

    # Check if it's a markdown file with embedded YAML
    if '```yaml' in content:
        # Extract first YAML block
        import re
        yaml_match = re.search(r'```yaml\s*(.*?)\s*```', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            return yaml.safe_load(yaml_content)

    if '---' in content:
        # Handle markdown with YAML frontmatter
        import re
        # Try to extract all YAML blocks and combine them
        yaml_blocks = re.findall(r'```yaml\s*(.*?)\s*```', content, re.DOTALL)
        if yaml_blocks:
            # Just return first block for now
            return yaml.safe_load(yaml_blocks[0])

    return yaml.safe_load(content)


def load_field_mappings(field_mappings_path: str) -> Dict:
    """Load field mappings from YAML file."""
    with open(field_mappings_path, 'r') as f:
        content = f.read()

    # Check if it's a markdown file with embedded YAML
    if '```yaml' in content:
        import re
        yaml_match = re.search(r'```yaml\s*(.*?)\s*```', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            return yaml.safe_load(yaml_content)

    return yaml.safe_load(content)


def validate_document(doc: Dict, schema: Dict, doc_type: str) -> List[str]:
    """Validate a single document against schema."""
    errors = []

    # Check required fields
    required = schema.get(doc_type, {}).get('required', [])
    for field in required:
        if field not in doc:
            errors.append(f"Missing required field: {field}")

    # Check field types and patterns
    properties = schema.get(doc_type, {}).get('properties', {})
    for field, value in doc.items():
        if field in properties:
            prop_schema = properties[field]
            field_type = prop_schema.get('type')

            # Type validation
            if field_type == 'string' and not isinstance(value, str):
                errors.append(f"Field '{field}' should be string, got {type(value).__name__}")
            elif field_type == 'array' and not isinstance(value, list):
                errors.append(f"Field '{field}' should be array, got {type(value).__name__}")
            elif field_type == 'object' and not isinstance(value, dict):
                errors.append(f"Field '{field}' should be object, got {type(value).__name__}")

            # Pattern validation
            if 'pattern' in prop_schema and isinstance(value, str):
                import re
                pattern = prop_schema['pattern']
                if not re.match(pattern, value):
                    errors.append(f"Field '{field}' does not match pattern: {pattern}")

    return errors


def validate_module_output(module: str, output_dir: Path) -> Dict:
    """Validate all normalization output files for a module."""
    results = {
        'status': 'PASS',
        'module': module,
        'errors': [],
        'warnings': [],
        'files_checked': []
    }

    # Load schema
    skill_dir = Path(__file__).parent.parent
    schema_path = skill_dir / 'data' / 'input-schema.yaml'

    if not schema_path.exists():
        results['status'] = 'FAIL'
        results['errors'].append(f"Schema not found: {schema_path}")
        return results

    schema = load_schema(str(schema_path))

    # Files to check
    files_to_check = [
        (f"{module}-fr-normalized.json", 'Functional Requirement'),
        (f"{module}-us-normalized.json", 'User Story'),
        (f"{module}-uc-normalized.json", 'Use Case'),
    ]

    for filename, doc_type in files_to_check:
        filepath = output_dir / filename
        results['files_checked'].append(filename)

        if not filepath.exists():
            results['status'] = 'FAIL'
            results['errors'].append(f"Missing file: {filename}")
            continue

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Handle both single document and array of documents
            documents = data if isinstance(data, list) else [data]

            for idx, doc in enumerate(documents):
                doc_errors = validate_document(doc, schema, doc_type.lower().replace(' ', ''))
                if doc_errors:
                    results['status'] = 'FAIL'
                    results['errors'].extend([f"{filename}[{idx}]: {e}" for e in doc_errors])

                # Check for traceability
                if 'source' not in doc:
                    results['warnings'].append(f"{filename}[{idx}]: Missing source traceability")

                if 'createdAt' not in doc:
                    results['warnings'].append(f"{filename}[{idx}]: Missing createdAt timestamp")

        except json.JSONDecodeError as e:
            results['status'] = 'FAIL'
            results['errors'].append(f"Invalid JSON in {filename}: {e}")
        except Exception as e:
            results['status'] = 'FAIL'
            results['errors'].append(f"Error processing {filename}: {e}")

    # Check validation report exists
    report_file = output_dir / f"{module}-validation-report.md"
    if not report_file.exists():
        results['warnings'].append(f"Validation report not found: {module}-validation-report.md")

    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_normalization.py <module> <output_dir>")
        print("Example: python validate_normalization.py M1 Docs/life-2/normalization/")
        sys.exit(1)

    module = sys.argv[1]
    output_dir = Path(sys.argv[2])

    if not output_dir.exists():
        print(f"❌ FAIL: Output directory not found: {output_dir}")
        sys.exit(1)

    results = validate_module_output(module, output_dir)

    # Print results
    print(f"\n{'='*60}")
    print(f"Validation Results for {results['module']}")
    print(f"{'='*60}")

    if results['status'] == 'PASS':
        print(f"✅ Status: PASS")
    else:
        print(f"❌ Status: FAIL")

    print(f"\nFiles checked: {', '.join(results['files_checked'])}")

    if results['errors']:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"  - {error}")

    if results['warnings']:
        print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
        for warning in results['warnings']:
            print(f"  - {warning}")

    # Exit with appropriate code
    if results['status'] == 'PASS':
        print(f"\n✅ Validation PASSED")
        sys.exit(0)
    else:
        print(f"\n❌ Validation FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
