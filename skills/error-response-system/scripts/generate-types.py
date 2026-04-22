#!/usr/bin/env python3
"""
Script generate TypeScript types tu error-codes.json

Su dung:
    python generate-types.py [path/to/error-codes.json] [output-dir]

    Mac dinh:
        input:  src/lib/errors/error-codes.json
        output: src/lib/errors/

Output files:
    - types.ts: TypeScript interfaces va type definitions
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# =============================================================================
# TEMPLATE STRINGS
# =============================================================================

FILE_HEADER = '''/**
 * Auto-generated TypeScript types tu error-codes.json
 *
 * KHONG CHINH SUA FILE NAY TRUC TIEP!
 * Sua doi error-codes.json va chay `python scripts/generate-types.py`
 *
 * Generated: {timestamp}
 */

'''

TYPES_CONTENT = '''// =============================================================================
// ERROR DETAIL INTERFACE
// =============================================================================

/**
 * Chi tiet loi tra ve cho client
 */
export interface ErrorDetail {{
  /** Ma loi (vd: AUTH_001, HTTP_404) */
  code: string
  /** Thong bao cho user */
  message: string
  /** Chi tiet ky thuat (cho developer) */
  details?: string
  /** Field gay ra loi (cho validation errors) */
  field?: string
  /** Goi y cach khac phuc */
  suggestion?: string
  /** Thoi diem xay ra loi */
  timestamp: string
  /** Request ID de tracing */
  requestId?: string
}}

/**
 * Response format cho errors
 */
export interface ErrorResponse {{
  success: false
  error: ErrorDetail
}}

// =============================================================================
// ERROR CONFIG INTERFACE
// =============================================================================

/**
 * Cau hinh cho mot error code
 */
export interface ErrorConfig {{
  code: string
  status: number
  message: string
  details?: string
  suggestion?: string
}}

// =============================================================================
// HTTP ERROR TYPES
// =============================================================================

/**
 * Cac loai HTTP errors ho tro
 */
export type HttpErrorType = {http_error_types}

/**
 * Mapping HTTP error type -> config
 */
export const HTTP_ERRORS: Record<HttpErrorType, ErrorConfig> = {http_errors_object}

// =============================================================================
// BUSINESS ERROR TYPES
// =============================================================================

/**
 * Cac category cua business errors
 */
export type BusinessErrorCategory = {business_categories}

{business_error_code_types}

/**
 * Union type cua tat ca business error codes
 */
export type BusinessErrorCode = {business_error_union}

/**
 * Mapping business error codes -> config
 */
export const BUSINESS_ERRORS: Record<string, Record<string, ErrorConfig>> = {business_errors_object}

// =============================================================================
// HELPER TYPES
// =============================================================================

/**
 * Tat ca error codes (HTTP + Business)
 */
export type ErrorCode = HttpErrorType | BusinessErrorCode

/**
 * Type guard kiem tra HTTP error
 */
export function isHttpError(code: string): code is HttpErrorType {{
  return code in HTTP_ERRORS
}}

/**
 * Type guard kiem tra Business error
 */
export function isBusinessError(code: string): code is BusinessErrorCode {{
  const category = code.split('_')[0]
  return category in BUSINESS_ERRORS && code in (BUSINESS_ERRORS[category] || {{}})
}}

/**
 * Lay error config tu code
 */
export function getErrorConfig(code: ErrorCode): ErrorConfig | undefined {{
  if (isHttpError(code)) {{
    return HTTP_ERRORS[code]
  }}

  const category = code.split('_')[0]
  return BUSINESS_ERRORS[category]?.[code]
}}
'''


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def format_object_literal(obj: dict, indent: int = 0) -> str:
    """Format dict thanh TypeScript object literal"""
    lines = ["{"]
    indent_str = "  " * (indent + 1)

    for key, value in obj.items():
        if key.startswith("_"):
            continue

        if isinstance(value, dict):
            # Check if this is an error entry or a category
            if "code" in value and "status" in value:
                # Error entry
                lines.append(f'{indent_str}"{key}": {{')
                for k, v in value.items():
                    if isinstance(v, str):
                        lines.append(f'{indent_str}  {k}: "{v}",')
                    else:
                        lines.append(f'{indent_str}  {k}: {v},')
                lines.append(f'{indent_str}}},')
            else:
                # Category
                lines.append(f'{indent_str}"{key}": {{')
                for error_key, error_value in value.items():
                    if error_key.startswith("_"):
                        continue
                    if isinstance(error_value, dict):
                        lines.append(f'{indent_str}  "{error_key}": {{')
                        for k, v in error_value.items():
                            if isinstance(v, str):
                                lines.append(f'{indent_str}    {k}: "{v}",')
                            else:
                                lines.append(f'{indent_str}    {k}: {v},')
                        lines.append(f'{indent_str}  }},')
                lines.append(f'{indent_str}}},')
        elif isinstance(value, str):
            lines.append(f'{indent_str}"{key}": "{value}",')
        else:
            lines.append(f'{indent_str}"{key}": {value},')

    lines.append("  " * indent + "}")
    return "\n".join(lines)


def generate_types_file(data: dict) -> str:
    """Generate noi dung file types.ts"""

    # HTTP error types
    http_errors = data.get("HTTP_ERRORS", {})
    http_error_types = " | ".join([f'"{key}"' for key in http_errors.keys() if not key.startswith("_")])

    # Business error categories va codes
    business_errors = data.get("BUSINESS_ERRORS", {})
    business_categories = " | ".join([f'"{cat}"' for cat in business_errors.keys()])

    # Generate type cho moi category
    business_error_code_types = []
    all_error_codes = []

    for category, errors in business_errors.items():
        if not isinstance(errors, dict):
            continue

        codes = [key for key in errors.keys() if not key.startswith("_")]
        all_error_codes.extend(codes)

        if codes:
            type_name = f"{category}ErrorCode"
            codes_union = " | ".join([f'"{code}"' for code in codes])
            business_error_code_types.append(f"export type {type_name} = {codes_union}")

    business_error_code_types_str = "\n\n".join(business_error_code_types)
    business_error_union = " | ".join([f'"{code}"' for code in all_error_codes])

    # Format objects
    http_errors_filtered = {k: v for k, v in http_errors.items() if not k.startswith("_")}
    http_errors_object = format_object_literal(http_errors_filtered)

    business_errors_object = format_object_literal(business_errors)

    # Generate content
    content = FILE_HEADER.format(timestamp=datetime.now().isoformat())
    content += TYPES_CONTENT.format(
        http_error_types=http_error_types or '""',
        http_errors_object=http_errors_object,
        business_categories=business_categories or '""',
        business_error_code_types=business_error_code_types_str,
        business_error_union=business_error_union or '""',
        business_errors_object=business_errors_object,
    )

    return content


# =============================================================================
# MAIN
# =============================================================================

def main():
    # Get paths from args or use defaults
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = Path("src/lib/errors/error-codes.json")

    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    else:
        output_dir = input_path.parent

    print(f"Input:  {input_path}")
    print(f"Output: {output_dir}")
    print("-" * 50)

    # Check input exists
    if not input_path.exists():
        print(f"LOI: File khong ton tai: {input_path}")
        return 1

    # Load JSON
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"LOI: JSON khong hop le: {e}")
        return 1

    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate types.ts
    types_content = generate_types_file(data)
    types_path = output_dir / "types.ts"

    with open(types_path, "w", encoding="utf-8") as f:
        f.write(types_content)

    print(f"Da tao: {types_path}")

    # Summary
    http_count = len([k for k in data.get("HTTP_ERRORS", {}).keys() if not k.startswith("_")])
    business_count = sum(
        len([k for k in errors.keys() if not k.startswith("_")])
        for errors in data.get("BUSINESS_ERRORS", {}).values()
        if isinstance(errors, dict)
    )

    print("-" * 50)
    print(f"THANH CONG!")
    print(f"  HTTP Errors: {http_count}")
    print(f"  Business Errors: {business_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
