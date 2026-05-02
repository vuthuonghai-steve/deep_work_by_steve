#!/usr/bin/env python3
"""
Script validate error-codes.json

Su dung:
    python validate-error-codes.py [path/to/error-codes.json]

    Mac dinh: src/lib/errors/error-codes.json

Kiem tra:
    - JSON format hop le
    - Required fields: code, status, message
    - Error code format: PREFIX_NNN (vd: AUTH_001)
    - HTTP status codes hop le
    - Khong trung lap error codes
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


# =============================================================================
# CONSTANTS
# =============================================================================

REQUIRED_FIELDS = ["code", "status", "message"]
OPTIONAL_FIELDS = ["details", "suggestion", "field"]

VALID_HTTP_STATUS = [400, 401, 403, 404, 409, 422, 429, 500, 502, 503, 504]

ERROR_CODE_PATTERN = re.compile(r"^[A-Z]{2,5}_\d{3}$")
HTTP_ERROR_PATTERN = re.compile(r"^HTTP_\d{3}$")


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_error_code_format(code: str, is_http: bool = False) -> list[str]:
    """Validate error code format"""
    errors = []

    if is_http:
        if not HTTP_ERROR_PATTERN.match(code):
            errors.append(f"HTTP error code '{code}' khong dung format HTTP_NNN")
    else:
        if not ERROR_CODE_PATTERN.match(code):
            errors.append(f"Error code '{code}' khong dung format PREFIX_NNN")

    return errors


def validate_status_code(status: Any, code: str) -> list[str]:
    """Validate HTTP status code"""
    errors = []

    if not isinstance(status, int):
        errors.append(f"Error '{code}': status phai la so nguyen, nhan duoc {type(status).__name__}")
        return errors

    if status not in VALID_HTTP_STATUS:
        errors.append(f"Error '{code}': status {status} khong hop le. Cac gia tri hop le: {VALID_HTTP_STATUS}")

    return errors


def validate_error_entry(code: str, entry: dict, is_http: bool = False) -> list[str]:
    """Validate mot error entry"""
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Error '{code}': thieu truong bat buoc '{field}'")

    # Validate code format
    if "code" in entry:
        errors.extend(validate_error_code_format(entry["code"], is_http))

        # Check code matches key
        if entry["code"] != code and not code.startswith("HTTP_"):
            if not (is_http and entry["code"] == f"HTTP_{entry.get('status', '')}"):
                pass  # Allow HTTP_400 as code for BAD_REQUEST key

    # Validate status code
    if "status" in entry:
        errors.extend(validate_status_code(entry["status"], code))

    # Validate message not empty
    if "message" in entry and not entry["message"].strip():
        errors.append(f"Error '{code}': message khong duoc rong")

    return errors


def validate_http_errors(http_errors: dict) -> list[str]:
    """Validate HTTP_ERRORS section"""
    errors = []

    if not isinstance(http_errors, dict):
        errors.append("HTTP_ERRORS phai la object")
        return errors

    for key, entry in http_errors.items():
        if isinstance(entry, dict) and not key.startswith("_"):
            errors.extend(validate_error_entry(key, entry, is_http=True))

    return errors


def validate_business_errors(business_errors: dict) -> list[str]:
    """Validate BUSINESS_ERRORS section"""
    errors = []
    all_codes = set()

    if not isinstance(business_errors, dict):
        errors.append("BUSINESS_ERRORS phai la object")
        return errors

    for category, category_errors in business_errors.items():
        if not isinstance(category_errors, dict):
            errors.append(f"Category '{category}' phai la object")
            continue

        for code, entry in category_errors.items():
            # Skip description fields
            if code.startswith("_"):
                continue

            if not isinstance(entry, dict):
                errors.append(f"Entry '{code}' phai la object")
                continue

            # Check duplicate codes
            if code in all_codes:
                errors.append(f"Error code '{code}' bi trung lap")
            all_codes.add(code)

            # Check category prefix
            expected_prefix = f"{category}_"
            if not code.startswith(expected_prefix):
                errors.append(f"Error code '{code}' khong bat dau bang prefix '{expected_prefix}'")

            errors.extend(validate_error_entry(code, entry))

    return errors


def validate_json_structure(data: dict) -> list[str]:
    """Validate cau truc JSON tong the"""
    errors = []

    # Check required sections
    if "HTTP_ERRORS" not in data:
        errors.append("Thieu section 'HTTP_ERRORS'")

    if "BUSINESS_ERRORS" not in data:
        errors.append("Thieu section 'BUSINESS_ERRORS'")

    return errors


def validate_error_codes_file(filepath: Path) -> tuple[bool, list[str]]:
    """Validate toan bo file error-codes.json"""
    errors = []

    # Check file exists
    if not filepath.exists():
        return False, [f"File khong ton tai: {filepath}"]

    # Load JSON
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON khong hop le: {e}"]

    # Validate structure
    errors.extend(validate_json_structure(data))

    # Validate sections
    if "HTTP_ERRORS" in data:
        errors.extend(validate_http_errors(data["HTTP_ERRORS"]))

    if "BUSINESS_ERRORS" in data:
        errors.extend(validate_business_errors(data["BUSINESS_ERRORS"]))

    return len(errors) == 0, errors


# =============================================================================
# MAIN
# =============================================================================

def main():
    # Get file path from args or use default
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
    else:
        # Default path relative to project root
        filepath = Path("src/lib/errors/error-codes.json")

    print(f"Dang validate: {filepath}")
    print("-" * 50)

    is_valid, errors = validate_error_codes_file(filepath)

    if is_valid:
        print("THANH CONG: File error-codes.json hop le!")
        print("-" * 50)

        # Print summary
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        http_count = len([k for k in data.get("HTTP_ERRORS", {}).keys() if not k.startswith("_")])

        business_count = 0
        categories = []
        for cat, errors_dict in data.get("BUSINESS_ERRORS", {}).items():
            if isinstance(errors_dict, dict):
                count = len([k for k in errors_dict.keys() if not k.startswith("_")])
                business_count += count
                categories.append(f"{cat}: {count}")

        print(f"HTTP Errors: {http_count}")
        print(f"Business Errors: {business_count}")
        print(f"  Categories: {', '.join(categories)}")

        return 0
    else:
        print("LOI: File error-codes.json khong hop le!")
        print("-" * 50)
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print("-" * 50)
        print(f"Tong: {len(errors)} loi")
        return 1


if __name__ == "__main__":
    sys.exit(main())
