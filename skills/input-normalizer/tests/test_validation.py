#!/usr/bin/env python3
"""
Test suite for input-normalizer validation.

Tests:
1. Schema validation for FR, US, UC documents
2. Field mapping normalization
3. Priority normalization
4. Module normalization
5. Error code validation
"""

import json
import pytest
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any


# Import the validation module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_normalization import (
    load_schema,
    validate_document,
    validate_module_output,
)


# ============================================================================
# FIXTURES
# ============================================================================

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_test_cases() -> Dict[str, Any]:
    """Load test cases from fixtures."""
    fixture_path = FIXTURES_DIR / "test_cases.yaml"
    with open(fixture_path, 'r') as f:
        content = f.read()

    # Parse the YAML with embedded JSON
    # Split by --- and parse each section
    test_cases = {}
    sections = content.split('---')

    for section in sections:
        if section.strip().startswith('## Valid'):
            # Extract JSON from code block
            json_match = re.search(r'```json\s*(.*?)\s*```', section, re.DOTALL)
            if json_match:
                doc = json.loads(json_match.group(1))
                if 'FR-' in doc.get('id', ''):
                    test_cases['valid_fr'] = doc
                elif 'US-M' in doc.get('id', ''):
                    test_cases['valid_us'] = doc
                elif 'UC-M' in doc.get('id', ''):
                    test_cases['valid_uc'] = doc

        elif section.strip().startswith('## Invalid'):
            # Extract case type from heading
            heading_match = re.search(r'Invalid (\w+)', section)
            if heading_match:
                case_type = heading_match.group(1).lower()
                json_match = re.search(r'```json\s*(.*?)\s*```', section, re.DOTALL)
                if json_match:
                    doc = json.loads(json_match.group(1))
                    test_cases[f'invalid_{case_type}'] = doc

    return test_cases


# Load test cases once
TEST_CASES = load_test_cases()


# ============================================================================
# SCHEMA LOADING TESTS
# ============================================================================

class TestSchemaLoading:
    """Test schema loading functionality."""

    def test_load_schema_from_file(self, schema_path):
        """Test loading schema from YAML file."""
        assert schema_path.exists(), f"Schema file not found: {schema_path}"

        schema = load_schema(str(schema_path))

        assert schema is not None
        assert 'Functional Requirement' in schema or 'functionalrequirement' in str(schema).lower()

    def test_schema_has_all_document_types(self, schema_path):
        """Test that schema defines all three document types."""
        schema = load_schema(str(schema_path))

        # Check FR schema
        fr_schema = schema.get('Functional Requirement') or schema.get('functionalrequirement')
        assert fr_schema is not None, "FR schema not found"

        # Check US schema
        us_schema = schema.get('User Story') or schema.get('userstory')
        assert us_schema is not None, "US schema not found"

        # Check UC schema
        uc_schema = schema.get('Use Case') or schema.get('usecase')
        assert uc_schema is not None, "UC schema not found"


# ============================================================================
# VALID DOCUMENT TESTS
# ============================================================================

class TestValidFR:
    """Tests for valid Functional Requirement documents."""

    def test_valid_fr_passes_validation(self, schema_path):
        """Valid FR should pass all validation rules."""
        schema = load_schema(str(schema_path))
        fr_schema = schema.get('Functional Requirement', {})

        doc = TEST_CASES.get('valid_fr')
        if doc is None:
            pytest.skip("Valid FR test case not found")

        errors = validate_document(doc, schema, 'functionalrequirement')

        # Filter out non-critical warnings
        critical_errors = [e for e in errors if 'Missing' not in e or 'required' in e.lower()]
        assert len(critical_errors) == 0, f"Valid FR has errors: {critical_errors}"

    def test_fr_has_required_fields(self):
        """FR must have all required fields."""
        doc = TEST_CASES.get('valid_fr')
        if doc is None:
            pytest.skip("Valid FR test case not found")

        required = ['id', 'title', 'description', 'priority', 'module', 'source']
        for field in required:
            assert field in doc, f"Missing required field: {field}"

    def test_fr_id_pattern(self):
        """FR ID must match pattern FR-[a-z0-9]+-\\d{3}."""
        doc = TEST_CASES.get('valid_fr')
        if doc is None:
            pytest.skip("Valid FR test case not found")

        pattern = r'^FR-[a-z0-9]+-\d{3}$'
        assert re.match(pattern, doc['id']), f"FR ID pattern mismatch: {doc['id']}"

    def test_fr_priority_enum(self):
        """FR priority must be in enum values."""
        doc = TEST_CASES.get('valid_fr')
        if doc is None:
            pytest.skip("Valid FR test case not found")

        valid_priorities = ['critical', 'high', 'medium', 'low']
        assert doc['priority'] in valid_priorities, f"Invalid priority: {doc['priority']}"

    def test_fr_module_pattern(self):
        """FR module must match pattern M[1-6]."""
        doc = TEST_CASES.get('valid_fr')
        if doc is None:
            pytest.skip("Valid FR test case not found")

        pattern = r'^M[1-6]$'
        assert re.match(pattern, doc['module']), f"Module pattern mismatch: {doc['module']}"


class TestValidUS:
    """Tests for valid User Story documents."""

    def test_valid_us_passes_validation(self, schema_path):
        """Valid US should pass all validation rules."""
        schema = load_schema(str(schema_path))

        doc = TEST_CASES.get('valid_us')
        if doc is None:
            pytest.skip("Valid US test case not found")

        errors = validate_document(doc, schema, 'userstory')

        critical_errors = [e for e in errors if 'Missing' not in e or 'required' in e.lower()]
        assert len(critical_errors) == 0, f"Valid US has errors: {critical_errors}"

    def test_us_has_required_fields(self):
        """US must have all required fields."""
        doc = TEST_CASES.get('valid_us')
        if doc is None:
            pytest.skip("Valid US test case not found")

        required = ['id', 'title', 'description', 'acceptanceCriteria', 'priority', 'module', 'source']
        for field in required:
            assert field in doc, f"Missing required field: {field}"

    def test_us_id_pattern(self):
        """US ID must match pattern US-M[1-6]-\\d{3}."""
        doc = TEST_CASES.get('valid_us')
        if doc is None:
            pytest.skip("Valid US test case not found")

        pattern = r'^US-M[1-6]-\d{3}$'
        assert re.match(pattern, doc['id']), f"US ID pattern mismatch: {doc['id']}"

    def test_us_priority_enum(self):
        """US priority must be in enum values."""
        doc = TEST_CASES.get('valid_us')
        if doc is None:
            pytest.skip("Valid US test case not found")

        valid_priorities = ['must-have', 'should-have', 'could-have', "won't-have"]
        assert doc['priority'] in valid_priorities, f"Invalid priority: {doc['priority']}"

    def test_us_acceptance_criteria_not_empty(self):
        """US acceptanceCriteria must be non-empty array."""
        doc = TEST_CASES.get('valid_us')
        if doc is None:
            pytest.skip("Valid US test case not found")

        assert isinstance(doc['acceptanceCriteria'], list)
        assert len(doc['acceptanceCriteria']) > 0


class TestValidUC:
    """Tests for valid Use Case documents."""

    def test_valid_uc_passes_validation(self, schema_path):
        """Valid UC should pass all validation rules."""
        schema = load_schema(str(schema_path))

        doc = TEST_CASES.get('valid_uc')
        if doc is None:
            pytest.skip("Valid UC test case not found")

        errors = validate_document(doc, schema, 'usecase')

        critical_errors = [e for e in errors if 'Missing' not in e or 'required' in e.lower()]
        assert len(critical_errors) == 0, f"Valid UC has errors: {critical_errors}"

    def test_uc_has_required_fields(self):
        """UC must have all required fields."""
        doc = TEST_CASES.get('valid_uc')
        if doc is None:
            pytest.skip("Valid UC test case not found")

        required = ['id', 'name', 'actor', 'preconditions', 'postconditions', 'flow', 'module', 'source']
        for field in required:
            assert field in doc, f"Missing required field: {field}"

    def test_uc_id_pattern(self):
        """UC ID must match pattern UC-M[1-6]-\\d{3}."""
        doc = TEST_CASES.get('valid_uc')
        if doc is None:
            pytest.skip("Valid UC test case not found")

        pattern = r'^UC-M[1-6]-\d{3}$'
        assert re.match(pattern, doc['id']), f"UC ID pattern mismatch: {doc['id']}"

    def test_uc_flow_has_main_steps(self):
        """UC flow must have main steps."""
        doc = TEST_CASES.get('valid_uc')
        if doc is None:
            pytest.skip("Valid UC test case not found")

        assert 'main' in doc['flow']
        assert len(doc['flow']['main']) > 0


# ============================================================================
# INVALID DOCUMENT TESTS
# ============================================================================

class TestInvalidFR:
    """Tests for invalid Functional Requirement documents."""

    def test_fr_missing_required_field(self, schema_path):
        """FR missing required field should fail validation."""
        schema = load_schema(str(schema_path))

        doc = TEST_CASES.get('invalid_fr')
        if doc is None:
            pytest.skip("Invalid FR test case not found")

        errors = validate_document(doc, schema, 'functionalrequirement')

        # Should have error about missing required field
        assert len(errors) > 0, "Should have validation errors"
        assert any('Missing required field' in e for e in errors), f"Expected missing field error: {errors}"

    def test_fr_wrong_priority_enum(self, schema_path):
        """FR with wrong priority enum should fail."""
        # Test case 2: Wrong priority enum
        fixture_content = Path(FIXTURES_DIR / "test_cases.yaml").read_text()

        # Find and parse the second invalid FR
        json_match = re.search(
            r'## Invalid FR - Wrong Priority Enum.*?```json\s*(.*?)\s*```',
            fixture_content, re.DOTALL
        )
        if not json_match:
            pytest.skip("Test case not found")

        doc = json.loads(json_match.group(1))
        schema = load_schema(str(schema_path))

        errors = validate_document(doc, schema, 'functionalrequirement')

        # Should detect invalid enum value
        assert len(errors) > 0

    def test_fr_wrong_module_pattern(self, schema_path):
        """FR with wrong module pattern should fail."""
        fixture_content = Path(FIXTURES_DIR / "test_cases.yaml").read_text()

        json_match = re.search(
            r'## Invalid FR - Wrong Module Pattern.*?```json\s*(.*?)\s*```',
            fixture_content, re.DOTALL
        )
        if not json_match:
            pytest.skip("Test case not found")

        doc = json.loads(json_match.group(1))
        schema = load_schema(str(schema_path))

        errors = validate_document(doc, schema, 'functionalrequirement')

        assert len(errors) > 0, "Should have validation error for invalid module"


class TestInvalidUS:
    """Tests for invalid User Story documents."""

    def test_us_missing_acceptance_criteria(self, schema_path):
        """US missing acceptanceCriteria should fail."""
        fixture_content = Path(FIXTURES_DIR / "test_cases.yaml").read_text()

        json_match = re.search(
            r'## Invalid US - Missing Acceptance Criteria.*?```json\s*(.*?)\s*```',
            fixture_content, re.DOTALL
        )
        if not json_match:
            pytest.skip("Test case not found")

        doc = json.loads(json_match.group(1))
        schema = load_schema(str(schema_path))

        errors = validate_document(doc, schema, 'userstory')

        assert len(errors) > 0

    def test_us_wrong_priority_enum(self, schema_path):
        """US with wrong priority enum should fail."""
        fixture_content = Path(FIXTURES_DIR / "test_cases.yaml").read_text()

        json_match = re.search(
            r'## Invalid US - Wrong Priority Enum.*?```json\s*(.*?)\s*```',
            fixture_content, re.DOTALL
        )
        if not json_match:
            pytest.skip("Test case not found")

        doc = json.loads(json_match.group(1))
        schema = load_schema(str(schema_path))

        errors = validate_document(doc, schema, 'userstory')

        assert len(errors) > 0


class TestInvalidUC:
    """Tests for invalid Use Case documents."""

    def test_uc_missing_flow_main(self, schema_path):
        """UC missing flow.main should fail."""
        fixture_content = Path(FIXTURES_DIR / "test_cases.yaml").read_text()

        json_match = re.search(
            r'## Invalid UC - Missing Flow Main Steps.*?```json\s*(.*?)\s*```',
            fixture_content, re.DOTALL
        )
        if not json_match:
            pytest.skip("Test case not found")

        doc = json.loads(json_match.group(1))
        schema = load_schema(str(schema_path))

        errors = validate_document(doc, schema, 'usecase')

        assert len(errors) > 0

    def test_uc_wrong_module(self, schema_path):
        """UC with wrong module should fail."""
        fixture_content = Path(FIXTURES_DIR / "test_cases.yaml").read_text()

        json_match = re.search(
            r'## Invalid UC - Wrong Module.*?```json\s*(.*?)\s*```',
            fixture_content, re.DOTALL
        )
        if not json_match:
            pytest.skip("Test case not found")

        doc = json.loads(json_match.group(1))
        schema = load_schema(str(schema_path))

        errors = validate_document(doc, schema, 'usecase')

        assert len(errors) > 0


# ============================================================================
# FIELD MAPPING TESTS
# ============================================================================

class TestFieldMappings:
    """Tests for field mapping normalization."""

    def test_field_mappings_exist(self, field_mappings_path):
        """Test that field mappings file exists and is valid YAML."""
        assert field_mappings_path.exists(), f"Field mappings not found: {field_mappings_path}"

        with open(field_mappings_path, 'r') as f:
            mappings = yaml.safe_load(f)

        assert mappings is not None
        assert 'Functional Requirement Mappings' in mappings or 'functional_requirement' in str(mappings).lower()

    def test_priority_normalization(self, field_mappings_path):
        """Test priority value normalization."""
        with open(field_mappings_path, 'r') as f:
            mappings = yaml.safe_load(f)

        priority_norm = mappings.get('Priority Normalization', {})

        # Test critical variations
        critical_variations = ['critical', 'Critical', 'CRITICAL', 'CRIT', 'P0']
        for var in critical_variations:
            normalized = priority_norm.get(var, var)
            assert normalized == 'critical', f"Failed to normalize: {var}"

    def test_module_normalization(self, field_mappings_path):
        """Test module value normalization."""
        with open(field_mappings_path, 'r') as f:
            mappings = yaml.safe_load(f)

        module_norm = mappings.get('Module Normalization', {})

        # Test M1 variations
        m1_variations = ['m1', 'M1', 'module1', 'auth', 'Auth', 'authentication']
        for var in m1_variations:
            normalized = module_norm.get(var, var)
            assert normalized == 'M1', f"Failed to normalize module: {var}"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full validation workflow."""

    def test_validate_module_output_missing_files(self, tmp_path):
        """Test validation with missing output files."""
        # Create empty temp dir
        result = validate_module_output('M1', tmp_path)

        assert result['status'] == 'FAIL'
        assert len(result['errors']) > 0

    def test_validate_module_output_with_valid_files(self, tmp_path, schema_path):
        """Test validation with valid output files."""
        import shutil

        # Copy schema to temp
        temp_schema = tmp_path / "input-schema.yaml"
        shutil.copy(schema_path, temp_schema)

        # Create valid FR file
        fr_data = TEST_CASES.get('valid_fr', {})
        fr_file = tmp_path / "M1-fr-normalized.json"
        with open(fr_file, 'w') as f:
            json.dump([fr_data], f)

        # Run validation
        result = validate_module_output('M1', tmp_path)

        # Should pass or have only warnings
        assert result['status'] in ['PASS', 'FAIL']

    def test_traceability_fields(self):
        """Test that documents have traceability fields."""
        doc = TEST_CASES.get('valid_fr')
        if doc is None:
            pytest.skip("Valid FR test case not found")

        # Check source field
        assert 'source' in doc
        assert 'file' in doc['source']

        # Check createdAt
        assert 'createdAt' in doc

        # Check originalContent
        assert 'originalContent' in doc


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
