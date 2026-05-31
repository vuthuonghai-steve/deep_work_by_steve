#!/usr/bin/env python3
"""
validate_gate.py — Validate gate checklists for design.md

Usage:
    python validate_gate.py <design_path> [--gate 1|2|3]
    python validate_gate.py <design_path> --all

Exit Codes:
    0 = PASS
    1 = FAIL
    2 = EMERGENCY (critical error)
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

def count_words(text):
    """Count words in text"""
    if not text:
        return 0
    return len(text.split())

def has_content(text, min_words=0):
    """Check if text has meaningful content"""
    if not text or not text.strip():
        return False
    if min_words > 0 and count_words(text) < min_words:
        return False
    return True

def extract_section(content, section_name):
    """Extract a section from markdown content"""
    pattern = rf'##\s+{re.escape(section_name)}.*?\n(.*?)(?=\n##\s+|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

# Gate 1 Checklist
def validate_gate1(frontmatter, content):
    """Gate 1: Problem Statement validation"""
    failures = []
    warnings = []
    
    # Check §1 exists and has content
    section1 = extract_section(content, "1. Problem Statement")
    if not has_content(section1, min_words=50):
        failures.append("§1 Problem Statement: less than 50 words or empty")
    
    # Check Problem, User, Reason are mentioned
    if section1:
        lower = section1.lower()
        if 'problem' not in lower and 'vấn đề' not in lower:
            warnings.append("§1: 'Problem' keyword not found")
        if 'user' not in lower and 'người' not in lower:
            warnings.append("§1: User context not clearly specified")
        if 'reason' not in lower and 'lý do' not in lower:
            warnings.append("§1: Reason/lý do not clearly specified")
    
    # Check status block
    status = frontmatter.get('status', {})
    if not status:
        failures.append("status block missing in frontmatter")
    else:
        if status.get('phase', 0) < 0:
            failures.append("status.phase invalid")
        if 'confidence' not in status:
            warnings.append("status.confidence not declared")
        elif status['confidence'] < 70:
            warnings.append(f"status.confidence is {status['confidence']} (< 70)")
    
    return failures, warnings

# Gate 2 Checklist
def validate_gate2(frontmatter, content):
    """Gate 2: Capability Map + Zone Mapping validation"""
    failures = []
    warnings = []
    
    # Check §2 Capability Map
    section2 = extract_section(content, "2. Capability Map")
    if not has_content(section2):
        failures.append("§2 Capability Map is empty")
    
    # Check 3 Pillars exist
    if section2:
        lower = section2.lower()
        if 'pillar' not in lower and 'tri thức' not in lower and 'knowledge' not in lower:
            failures.append("§2: Pillar 1 (Knowledge) not found")
        if 'process' not in lower and 'quy trình' not in lower:
            failures.append("§2: Pillar 2 (Process) not found")
        if 'guardrail' not in lower and 'kiểm soát' not in lower:
            failures.append("§2: Pillar 3 (Guardrails) not found")
    
    # Check §3 Zone Mapping
    section3 = extract_section(content, "3. Zone Mapping")
    if not has_content(section3):
        failures.append("§3 Zone Mapping is empty")
    else:
        # Check for table format
        if '|' not in section3:
            failures.append("§3: Zone Mapping should be a table with '|'")
        
        # Check core zone is marked
        if 'core' not in section3.lower():
            failures.append("§3: Core zone not found in mapping")
    
    # Check §8 Risks
    section8 = extract_section(content, "8. Risks")
    if not has_content(section8):
        failures.append("§8 Risks & Blind Spots is empty")
    else:
        if section8.count('\n-') < 2:  # At least 3 risks
            warnings.append("§8: Less than 3 risks listed")
    
    return failures, warnings

# Gate 3 Checklist
def validate_gate3(frontmatter, content):
    """Gate 3: Design + Diagrams validation"""
    failures = []
    warnings = []
    
    # Check §4 Folder Structure has Mermaid
    section4 = extract_section(content, "4. Folder Structure")
    if not has_content(section4):
        failures.append("§4 Folder Structure is empty")
    elif 'mermaid' not in section4.lower():
        failures.append("§4: No Mermaid diagram found")
    elif 'mindmap' not in section4.lower():
        warnings.append("§4: Missing mindmap diagram")
    
    # Check §5 Execution Flow has Mermaid
    section5 = extract_section(content, "5. Execution Flow")
    if not has_content(section5):
        failures.append("§5 Execution Flow is empty")
    elif 'mermaid' not in section5.lower():
        failures.append("§5: No Mermaid diagram found")
    elif 'sequencediagram' not in section5.lower():
        warnings.append("§5: Missing sequenceDiagram")
    
    # Check §6 Interaction Points
    section6 = extract_section(content, "6. Interaction Points")
    if not has_content(section6):
        failures.append("§6 Interaction Points is empty")
    
    # Check §7 Progressive Disclosure
    section7 = extract_section(content, "7. Progressive Disclosure Plan")
    if not has_content(section7):
        failures.append("§7 Progressive Disclosure Plan is empty")
    else:
        if 'tier' not in section7.lower():
            warnings.append("§7: Tier structure not clearly defined")
    
    return failures, warnings

def validate_gate(gate_number, design_path):
    """Main validation function"""
    
    path = Path(design_path)
    if not path.exists():
        return {
            "gate": gate_number,
            "status": "ERROR",
            "error": f"File not found: {design_path}",
            "exit_code": 2
        }
    
    try:
        content = path.read_text()
    except Exception as e:
        return {
            "gate": gate_number,
            "status": "ERROR",
            "error": f"Cannot read file: {e}",
            "exit_code": 2
        }
    
    frontmatter = extract_frontmatter(content)
    if not frontmatter:
        return {
            "gate": gate_number,
            "status": "ERROR",
            "error": "No YAML frontmatter found",
            "exit_code": 2
        }
    
    # Run appropriate gate validation
    if gate_number == 1:
        failures, warnings = validate_gate1(frontmatter, content)
    elif gate_number == 2:
        failures, warnings = validate_gate2(frontmatter, content)
    elif gate_number == 3:
        failures, warnings = validate_gate3(frontmatter, content)
    else:
        return {
            "gate": gate_number,
            "status": "ERROR",
            "error": f"Invalid gate number: {gate_number}",
            "exit_code": 2
        }
    
    result = {
        "gate": gate_number,
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": warnings,
        "exit_code": 0 if not failures else 1
    }
    
    return result

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: validate_gate.py <design_path> --gate 1|2|3",
            "exit_code": 1
        }, indent=2))
        sys.exit(1)
    
    design_path = sys.argv[1]
    gate_number = None
    
    # Parse arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--gate' and i < len(sys.argv) - 1:
            gate_number = int(sys.argv[i])
        elif arg == '--all':
            gate_number = 'all'
        elif arg == '--gate' and i >= len(sys.argv) - 1:
            print(json.dumps({"error": "--gate requires a number"}, indent=2))
            sys.exit(1)
    
    if gate_number is None:
        print(json.dumps({"error": "Missing --gate argument"}, indent=2))
        sys.exit(1)
    
    if gate_number == 'all':
        results = []
        for g in [1, 2, 3]:
            result = validate_gate(g, design_path)
            results.append(result)
        
        all_passed = all(r['status'] == 'PASS' for r in results)
        print(json.dumps({
            "all_gates": results,
            "overall_status": "PASS" if all_passed else "FAIL",
            "exit_code": 0 if all_passed else 1
        }, indent=2))
        sys.exit(0 if all_passed else 1)
    
    result = validate_gate(gate_number, design_path)
    print(json.dumps(result, indent=2))
    sys.exit(result['exit_code'])

if __name__ == "__main__":
    main()
