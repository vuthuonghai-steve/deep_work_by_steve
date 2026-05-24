#!/usr/bin/env python3
"""
schema_validator.py — Validate YAML frontmatter from a Markdown file
against a JSON Schema (Draft-07) defined in a YAML file.

CLI:
    python schema_validator.py --schema <schema.yaml> <file.md>
    python schema_validator.py --check-token-budget <file.md>

Output: YAML with stage, artifact, timestamp, passed, checks list.
Each check: name, status (pass/fail), error, severity, fix_hint.

Gracefully attempts pip install if pyyaml or jsonschema are missing.
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Dependency management — attempt pip install if missing
# ---------------------------------------------------------------------------

def _ensure_deps():
    """Try to import pyyaml and jsonschema. Offer pip install if missing."""
    missing = []

    try:
        import yaml  # noqa: F401
    except ImportError:
        missing.append("pyyaml")

    try:
        from jsonschema import Draft7Validator, FormatChecker  # noqa: F401
    except ImportError:
        missing.append("jsonschema")

    # tiktoken is optional - we have fallback
    try:
        import tiktoken  # noqa: F401
        _HAS_TIKTOKEN = True
    except ImportError:
        _HAS_TIKTOKEN = False

    if not missing:
        return

    print(f"Missing dependencies: {', '.join(missing)}. Attempting pip install...",
          file=sys.stderr)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing, "-q"],
            timeout=60,
        )
        print("Installation successful.\n", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Could not install dependencies: {e}", file=sys.stderr)
        print(f"Please run: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)


_ensure_deps()

import yaml
from jsonschema import Draft7Validator, FormatChecker, ValidationError

_HAS_TIKTOKEN = False
try:
    import tiktoken
    _HAS_TIKTOKEN = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Token Budget Validation
# ---------------------------------------------------------------------------

def count_tokens(text, tokenizer="cl100k_base"):
    """Count tokens in text using tiktoken."""
    if not _HAS_TIKTOKEN:
        # Fallback: naive approximation (Vietnamese ~4 chars/token)
        return len(text) // 4
    try:
        enc = tiktoken.get_encoding(tokenizer)
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4


def validate_token_budget(filepath, layer=None):
    """Validate token budget from frontmatter against actual content.

    Args:
        filepath: Path to the Markdown file
        layer: Optional layer to check (L0, L1, L2). If None, checks all.

    Returns:
        List of check dicts
    """
    checks = []

    # Parse frontmatter
    data, parse_err = parse_frontmatter(filepath)
    if parse_err:
        return [build_check("Token Budget Parsing", "fail", parse_err, "error",
                           "Ensure valid YAML frontmatter with token_budget")]

    # Get token_budget config
    token_budget = data.get("token_budget", {})
    if not token_budget:
        checks.append(build_check(
            "Token Budget Frontmatter", "fail",
            "No token_budget in frontmatter", "warning",
            "Add token_budget section to frontmatter per CLAUDE.md L1_working_policy"
        ))
        return checks

    checks.append(build_check("Token Budget Frontmatter", "pass"))

    # Get limits
    limits = {
        "L0": token_budget.get("L0_limit", 400),
        "L1": token_budget.get("L1_limit", 1200),
        "L2": token_budget.get("L2_limit", 2500),
    }
    enforcement = token_budget.get("enforcement", "soft")
    warning_threshold = token_budget.get("warning_threshold", 0.8)

    # Read file content
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        checks.append(build_check("File Read", "fail", str(e), "error",
                                "Check file permissions"))
        return checks

    # Count tokens (approximate - frontmatter excluded)
    lines = content.split("\n")
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() in ("---", "...",):
            if body_start == 0:
                body_start = i + 1
            else:
                # End of frontmatter
                body_lines = lines[body_start:i]
                break
    else:
        body_lines = lines[body_start:]

    body_text = "\n".join(body_lines)
    token_count = count_tokens(body_text)
    tokenizer_used = token_budget.get("tokenizer", "cl100k_base")

    # Determine which layer to check
    layers_to_check = [layer] if layer else ["L0", "L1", "L2"]

    for layer_name in layers_to_check:
        limit = limits.get(layer_name, 400)
        warning_at = int(limit * warning_threshold)

        checks.append(build_check(
            f"Token Budget {layer_name}",
            "pass",
            f"{token_count} tokens (limit: {limit}, tokenizer: {tokenizer_used})"
        ))

        if token_count > limit:
            if enforcement == "hard":
                checks.append(build_check(
                    f"Token Budget {layer_name} Exceeded", "fail",
                    f"{token_count} > {limit} tokens", "error",
                    f"Content exceeds {layer_name} limit. Reduce content or increase limit."
                ))
            else:
                checks.append(build_check(
                    f"Token Budget {layer_name} Exceeded", "fail",
                    f"{token_count} > {limit} tokens", "warning",
                    f"Content exceeds {layer_name} limit ({enforcement} enforcement)"
                ))
        elif token_count > warning_at:
            checks.append(build_check(
                f"Token Budget {layer_name} Warning", "warn",
                f"{token_count} > {warning_at} tokens (80% threshold)", "warning",
                f"Approaching {layer_name} limit. Consider reducing content."
            ))

    return checks


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(filepath):
    """Extract and parse YAML frontmatter from a Markdown file.

    Returns (data, error_string). On success error_string is None.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return None, f"File not found: {filepath}"
    except OSError as e:
        return None, str(e)

    # Match frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n(?:---|\.\.\.)", content, re.DOTALL)
    if not match:
        return None, "No YAML frontmatter found (must be between --- delimiters)"

    yaml_text = match.group(1)
    if not yaml_text.strip():
        return None, "Frontmatter is empty"

    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        return None, f"YAML parsing error: {e}"

    if data is None:
        return None, "Frontmatter is empty (null)"
    if not isinstance(data, dict):
        return None, f"Frontmatter is not a mapping (got {type(data).__name__})"

    return data, None


def load_schema(schema_path):
    """Load a JSON Schema from a YAML file."""
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = yaml.safe_load(f)
    except FileNotFoundError:
        return None, f"Schema file not found: {schema_path}"
    except yaml.YAMLError as e:
        return None, f"Schema YAML parse error: {e}"
    except OSError as e:
        return None, str(e)

    if not isinstance(schema, dict):
        return None, "Schema is not a valid YAML mapping"
    return schema, None


def _path_string(path):
    """Format a JSON Schema error path for human reading."""
    parts = []
    for elem in path:
        if isinstance(elem, int):
            parts.append(f"[{elem}]")
        else:
            parts.append(str(elem))
    return " -> ".join(parts) if parts else "root"


def _make_hint(err, path_str):
    """Generate a human-readable fix hint from a ValidationError."""
    schema = err.schema
    if "const" in schema:
        return f"Set this field to the required value '{schema['const']}'"
    if "enum" in schema:
        allowed = "', '".join(schema["enum"])
        return f"Set this field to one of: '{allowed}'"
    if "pattern" in schema:
        return f"Ensure this field matches regex: {schema['pattern']}"
    if "format" in schema:
        return f"Ensure this field is a valid {schema['format']} format"
    if "type" in schema:
        return f"Ensure this field is of type {schema['type']}"
    if "required" in schema:
        missing = ", ".join(schema["required"])
        return f"Add required properties: {missing}"
    if "not" in schema:
        return "This field must NOT match the forbidden pattern"
    if "additionalProperties" in schema:
        return "Remove unexpected properties"
    if "minItems" in schema:
        return f"Array must have at least {schema['minItems']} items"
    if "minimum" in schema or "maximum" in schema:
        lo = schema.get("minimum", "-inf")
        hi = schema.get("maximum", "+inf")
        return f"Value must be between {lo} and {hi}"
    return f"Review schema requirements at '{path_str}'"


def build_check(name, status, error=None, severity=None, fix_hint=None):
    """Create a single check dict with the standard shape."""
    return {
        "name": name,
        "status": status,
        "error": error,
        "severity": severity,
        "fix_hint": fix_hint,
    }


def validate_against_schema(data, schema):
    """Validate *data* against *schema*. Return list of check dicts."""
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(data))

    if not errors:
        return [build_check("JSON Schema Compliance", "pass")]

    checks = []
    for err in errors:
        path = _path_string(err.absolute_path)
        hint = _make_hint(err, path)
        severity = "error"
        checks.append(build_check(
            f"Schema: {path}" if path else "Schema: root",
            "fail",
            err.message,
            severity,
            hint,
        ))
    return checks


def make_result(artifact, checks):
    """Wrap checks into the final YAML-serializable result dict."""
    passed = all(c["status"] == "pass" for c in checks)
    return {
        "stage": "schema_validation",
        "artifact": artifact,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "passed": passed,
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter against a JSON Schema.")
    parser.add_argument("--schema", "-s",
                        help="Path to schema YAML file (required unless --check-token-budget)")
    parser.add_argument("--check-token-budget", action="store_true",
                        help="Run token budget validation only (no schema required)")
    parser.add_argument("file", help="Markdown file to validate")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    artifact = os.path.basename(args.file)
    checks = []

    # Token budget only mode
    if args.check_token_budget:
        tb_checks = validate_token_budget(args.file)
        result = make_result(artifact, tb_checks)
        result["stage"] = "token_budget_validation"
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                        sort_keys=False))
        # Soft enforcement: only fail on hard enforcement
        hard_fails = [c for c in tb_checks if c["status"] == "fail" and
                      c.get("severity") == "error"]
        return 0 if len(hard_fails) == 0 else 1

    # 1. Parse frontmatter
    data, parse_err = parse_frontmatter(args.file)
    if parse_err:
        checks.append(build_check(
            "YAML Frontmatter Parsing", "fail",
            parse_err, "error",
            "Ensure the file has valid YAML frontmatter between --- delimiters",
        ))
        result = make_result(artifact, checks)
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                        sort_keys=False))
        return 1

    checks.append(build_check("YAML Frontmatter Parsing", "pass"))

    # 2. Load schema
    if not args.schema:
        checks.append(build_check(
            "Schema Loading", "fail",
            "No schema file provided (use --schema or --check-token-budget)", "error",
            "Provide --schema <file.yaml> or use --check-token-budget",
        ))
        result = make_result(artifact, checks)
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                        sort_keys=False))
        return 1

    schema, schema_err = load_schema(args.schema)
    if schema_err:
        checks.append(build_check(
            "Schema Loading", "fail",
            schema_err, "error",
            "Verify the schema file is valid YAML and exists",
        ))
        result = make_result(artifact, checks)
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                        sort_keys=False))
        return 1

    checks.append(build_check("Schema Loading", "pass"))

    # 3. Validate
    schema_checks = validate_against_schema(data, schema)
    checks.extend(schema_checks)

    # 4. Token budget check (if declared in frontmatter)
    if data.get("token_budget"):
        tb_checks = validate_token_budget(args.file)
        checks.extend(tb_checks)

    result = make_result(artifact, checks)
    print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                    sort_keys=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
