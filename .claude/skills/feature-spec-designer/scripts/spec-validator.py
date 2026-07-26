#!/usr/bin/env python3
"""
spec-validator.py — Automated Validator for feature-spec-designer Artifacts
Validates:
1. Path Storage Isolation (Docs/Specs/{feature-name}/ & Docs/Specs/{feature-name}/diagrams/)
2. Mermaid Double Quote Labels Regex
3. Forbidden Words Scanner (TODO, TBD, ..., nhanh, tốt)
4. Calculates Quality Score & Emits JSON Verdict
"""

import sys
import os
import re
import json
from pathlib import Path

FORBIDDEN_WORDS = [r'\bTODO\b', r'\bTBD\b', r'\.\.\.', r'\bnhanh\b', r'\btốt\b', r'\bnhiều\b']
ALLOWED_PATH_PATTERN = r'^Docs/Specs/[a-z0-9-]+/(spec\.md|normalizations\.md|clarification-log\.md|diagrams/[a-z0-9-]+\.mmd)$'

def validate_path(file_path: str) -> bool:
    rel_path = os.path.relpath(file_path)
    return bool(re.match(ALLOWED_PATH_PATTERN, rel_path))

def check_mermaid_quotes(content: str) -> tuple[bool, int]:
    mermaid_blocks = re.findall(r'```mermaid(.*?)```', content, re.DOTALL)
    unquoted_count = 0
    for block in mermaid_blocks:
        # Check node definitions without double quotes like A[Text] or B(Text)
        unquoted_nodes = re.findall(r'\b[A-Za-z0-9_]+[\[\(\{\>][^"\n]+[\]\)\}\>]', block)
        unquoted_count += len(unquoted_nodes)
    return unquoted_count == 0, unquoted_count

def check_forbidden_words(content: str) -> list[str]:
    found = []
    for pattern in FORBIDDEN_WORDS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found.append(pattern)
    return found

def evaluate_spec_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {
            "status": "FAIL",
            "score": 0.0,
            "error": f"File {file_path} does not exist"
        }
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    path_valid = validate_path(file_path)
    mermaid_valid, unquoted_count = check_mermaid_quotes(content)
    forbidden_found = check_forbidden_words(content)

    score = 1.0
    deductions = []

    if not path_valid:
        score -= 0.3
        deductions.append(f"Storage path violation: {file_path} is outside Docs/Specs/{{feature-name}}/")
    if not mermaid_valid:
        score -= 0.3
        deductions.append(f"Found {unquoted_count} unquoted Mermaid labels")
    if forbidden_found:
        score -= 0.2
        deductions.append(f"Found forbidden words: {forbidden_found}")

    score = max(0.0, score)
    status = "PASS" if score >= 0.80 else "FAIL"

    return {
        "file": file_path,
        "status": status,
        "quality_score": round(score, 2),
        "path_valid": path_valid,
        "mermaid_valid": mermaid_valid,
        "forbidden_words": forbidden_found,
        "deductions": deductions
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 spec-validator.py <spec_file_path>")
        sys.exit(1)

    target_file = sys.argv[1]
    result = evaluate_spec_file(target_file)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "PASS":
        sys.exit(1)

if __name__ == "__main__":
    main()
