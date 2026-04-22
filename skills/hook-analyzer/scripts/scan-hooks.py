#!/usr/bin/env python3
"""
Hook Analyzer Scanner

Scans Claude Code hook scripts and performs static analysis
to detect security vulnerabilities, bugs, and best practice violations.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Rule definitions
SECURITY_RULES = {
    # Command Injection
    "SEC-CMD-001": {
        "pattern": r'\$\([^)]*\$[^)]+\)',  # Nested command substitution
        "severity": "Critical",
        "description": "Potential command injection: nested command substitution"
    },
    "SEC-CMD-002": {
        "pattern": r'\beval\s+["\$\(]',  # eval with variable
        "severity": "Critical",
        "description": "Use of eval with dynamic input"
    },
    "SEC-CMD-003": {
        "pattern": r'\|\s*(bash|sh|zsh)\s*($|\s)',
        "severity": "Critical",
        "description": "Pipe to shell interpreter detected"
    },
    "SEC-CMD-004": {
        "pattern": r'[^"]\$\w+[^"]',  # Unquoted variable
        "severity": "High",
        "description": "Unquoted variable expansion in string context"
    },

    # Path Traversal
    "SEC-PATH-001": {
        "pattern": r'(cat|cp|rm|ls|cd)\s+["\$][^"\']*\.\./',
        "severity": "High",
        "description": "Potential path traversal in file operation"
    },

    # Privilege Escalation
    "SEC-PRIV-001": {
        "pattern": r'mktemp\s+(?!")',
        "severity": "High",
        "description": "Insecure temp file pattern (should use mktemp with template)"
    },

    # Input Validation
    "SEC-INPUT-001": {
        "pattern": r'\$\{?\w+\}?\s*(>|>>|<)',
        "severity": "High",
        "description": "Unvalidated user input in I/O redirection"
    },

    # Environment
    "SEC-ENV-001": {
        "pattern": r'^ls\s|^cat\s|^grep\s',
        "severity": "High",
        "description": "Relative command path (should use absolute)"
    },
}

BASH_RULES = {
    # Exit Codes
    "BASH-EXIT-001": {
        "pattern": r'^#!/.*bash.*$',
        "expected": "set -euo pipefail",
        "severity": "Critical",
        "description": "Missing error handling: set -euo pipefail"
    },
    "BASH-EXIT-002": {
        "pattern": r'exit\s+0\s*\(.*[fF]ail|exit\s+[^0]',
        "severity": "High",
        "description": "Suspicious exit code (success on failure)"
    },

    # Variables
    "BASH-VAR-001": {
        "pattern": r'^\s+\w+=',
        "expected": "local",
        "severity": "High",
        "description": "Non-local variable assignment in function"
    },
    "BASH-VAR-002": {
        "pattern": r'\$\{?\w+\}?\s*\$\{?\w+\}?',
        "severity": "Medium",
        "description": "Concatenated variables without quotes"
    },

    # Strings
    "BASH-STR-001": {
        "pattern": r'echo\s+\$[\w{]',
        "severity": "Critical",
        "description": "Unquoted variable in echo"
    },

    # Arrays
    "BASH-ARR-001": {
        "pattern": r'\$\w+(\s|$)',
        "severity": "Medium",
        "description": "Unquoted array expansion"
    },

    # Anti-patterns
    "BASH-ANTI-001": {
        "pattern": r'\$\(ls\s+',
        "severity": "Critical",
        "description": "Parsing ls output (fragile)"
    },
    "BASH-ANTI-002": {
        "pattern": r'\|sed\s+.*\$\w',
        "severity": "Medium",
        "description": "Using sed with variable (prefer bash built-in)"
    },

    # Signal handling
    "BASH-SIGNAL-001": {
        "pattern": r'trap\s+.*EXIT',
        "expected": "cleanup",
        "severity": "Medium",
        "description": "Missing cleanup trap"
    },
}

PERFORMANCE_RULES = {
    "PERF-001": {
        "pattern": r'for\s+\w+\s+in\s+\$\([^)]+\)',
        "severity": "Medium",
        "description": "Command substitution in for loop (creates subshell per iteration)"
    },
    "PERF-002": {
        "pattern": r'\$\([^)]+\)\s*\|\s*while',
        "severity": "Low",
        "description": "Pipeline in command substitution (subshell overhead)"
    },
}

@dataclass
class Finding:
    rule_id: str
    severity: str
    description: str
    line: int
    line_content: str
    confidence: int  # 0-100

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AnalysisResult:
    file_path: str
    findings: List[Finding]
    lines_of_code: int
    analysis_time: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "findings": [f.to_dict() for f in self.findings],
            "lines_of_code": self.lines_of_code,
            "analysis_time": self.analysis_time
        }

def load_analysis_rules(yaml_path: str) -> Dict[str, Any]:
    """Load custom analysis rules from YAML config and merge with defaults."""
    import yaml

    # Default rule sets (can be overridden by YAML)
    default_security_rules = {
        "SEC-CMD-001": {
            "pattern": r'\$\([^)]*\$[^)]+\)',
            "severity": "Critical",
            "description": "Potential command injection: nested command substitution"
        },
        "SEC-CMD-002": {
            "pattern": r'\beval\s+["\$\(]',
            "severity": "Critical",
            "description": "Use of eval with dynamic input"
        },
        "SEC-CMD-003": {
            "pattern": r'\|\s*(bash|sh|zsh)\s*($|\s)',
            "severity": "Critical",
            "description": "Pipe to shell interpreter detected"
        },
        "SEC-CMD-004": {
            "pattern": r'[^"]\$\w+[^"]',
            "severity": "High",
            "description": "Unquoted variable expansion in string context"
        },
        "SEC-PATH-001": {
            "pattern": r'(cat|cp|rm|ls|cd)\s+["\$][^"\']*\.\./',
            "severity": "High",
            "description": "Potential path traversal in file operation"
        },
        "SEC-PRIV-001": {
            "pattern": r'mktemp\s+(?!")',
            "severity": "High",
            "description": "Insecure temp file pattern"
        },
        "SEC-INPUT-001": {
            "pattern": r'\$\{?\w+\}?\s*(>|>>|<)',
            "severity": "High",
            "description": "Unvalidated user input in I/O redirection"
        },
        "SEC-ENV-001": {
            "pattern": r'^ls\s|^cat\s|^grep\s',
            "severity": "High",
            "description": "Relative command path (should use absolute)"
        },
    }

    default_bash_rules = {
        "BASH-EXIT-001": {
            "pattern": r'^#!/.*bash.*$',
            "expected": "set -euo pipefail",
            "severity": "Critical",
            "description": "Missing error handling: set -euo pipefail"
        },
        "BASH-EXIT-002": {
            "pattern": r'exit\s+0\s*\(.*[fF]ail|exit\s+[^0]',
            "severity": "High",
            "description": "Suspicious exit code"
        },
        "BASH-VAR-001": {
            "pattern": r'^\s+\w+=',
            "expected": "local",
            "severity": "High",
            "description": "Non-local variable assignment in function"
        },
        "BASH-VAR-002": {
            "pattern": r'\$\{?\w+\}?\s*\$\{?\w+\}?',
            "severity": "Medium",
            "description": "Concatenated variables without quotes"
        },
        "BASH-STR-001": {
            "pattern": r'echo\s+\$[\w{]',
            "severity": "Critical",
            "description": "Unquoted variable in echo"
        },
        "BASH-ARR-001": {
            "pattern": r'\$\w+(\s|$)',
            "severity": "Medium",
            "description": "Unquoted array expansion"
        },
        "BASH-ANTI-001": {
            "pattern": r'\$\(ls\s+',
            "severity": "Critical",
            "description": "Parsing ls output (fragile)"
        },
        "BASH-ANTI-002": {
            "pattern": r'\|sed\s+.*\$\w',
            "severity": "Medium",
            "description": "Using sed with variable"
        },
        "BASH-SIGNAL-001": {
            "pattern": r'trap\s+.*EXIT',
            "expected": "cleanup",
            "severity": "Medium",
            "description": "Missing cleanup trap"
        },
    }

    default_performance_rules = {
        "PERF-001": {
            "pattern": r'for\s+\w+\s+in\s+\$\([^)]+\)',
            "severity": "Medium",
            "description": "Command substitution in for loop"
        },
        "PERF-002": {
            "pattern": r'\$\([^)]+\)\s*\|\s*while',
            "severity": "Low",
            "description": "Pipeline in command substitution"
        },
    }

    # Update global rule dictionaries with defaults
    SECURITY_RULES.update(default_security_rules)
    BASH_RULES.update(default_bash_rules)
    PERFORMANCE_RULES.update(default_performance_rules)

    # Load and merge custom rules from YAML
    if not yaml_path:
        return {"security_rules": {}, "bash_rules": {}, "performance_rules": {}}

    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        if not config:
            return {"security_rules": {}, "bash_rules": {}, "performance_rules": {}}

        # Merge custom security rules
        if 'security_rules' in config:
            for category, rules in config['security_rules'].items():
                if isinstance(rules, list):
                    for rule in rules:
                        rule_id = rule.get('id')
                        if rule_id:
                            SECURITY_RULES[rule_id] = {
                                "pattern": rule.get('pattern', ''),
                                "severity": rule.get('severity', 'Medium'),
                                "description": rule.get('name', rule.get('description', ''))
                            }

        # Merge custom bash rules
        if 'bash_rules' in config:
            for category, rules in config['bash_rules'].items():
                if isinstance(rules, list):
                    for rule in rules:
                        rule_id = rule.get('id')
                        if rule_id:
                            BASH_RULES[rule_id] = {
                                "pattern": rule.get('pattern', ''),
                                "expected": rule.get('expected', ''),
                                "severity": rule.get('severity', 'Medium'),
                                "description": rule.get('name', rule.get('description', ''))
                            }

        # Merge custom performance rules
        if 'performance_rules' in config:
            for rule in config['performance_rules']:
                rule_id = rule.get('id')
                if rule_id:
                    PERFORMANCE_RULES[rule_id] = {
                        "pattern": rule.get('pattern', ''),
                        "severity": rule.get('severity', 'Medium'),
                        "description": rule.get('name', rule.get('description', ''))
                    }

        return config

    except FileNotFoundError:
        print(f"Warning: Config file not found: {yaml_path}", file=sys.stderr)
        return {}
    except yaml.YAMLError as e:
        print(f"Warning: Error parsing YAML: {e}", file=sys.stderr)
        return {}
    except ImportError:
        print("Warning: PyYAML not installed, using default rules only", file=sys.stderr)
        return {}

def analyze_file(file_path: str, config: Dict[str, Any] = None) -> AnalysisResult:
    """Analyze a single hook file."""
    findings = []
    config = config or {}

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except (IOError, PermissionError) as e:
        return AnalysisResult(
            file_path=file_path,
            findings=[],
            lines_of_code=0,
            analysis_time=datetime.now().isoformat()
        )

    # Check for shebang and set -euo pipefail
    has_shebang = lines and lines[0].startswith('#!')
    has_error_handling = any('set -euo pipefail' in line for line in lines)

    # Check line by line
    for i, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith('#'):
            continue

        # Check security rules
        for rule_id, rule in SECURITY_RULES.items():
            if re.search(rule['pattern'], line):
                confidence = calculate_confidence(rule['severity'], has_error_handling, has_shebang)
                findings.append(Finding(
                    rule_id=rule_id,
                    severity=rule['severity'],
                    description=rule['description'],
                    line=i,
                    line_content=line.strip()[:100],
                    confidence=confidence
                ))

        # Check bash rules
        for rule_id, rule in BASH_RULES.items():
            if re.search(rule['pattern'], line):
                confidence = calculate_confidence(rule['severity'], has_error_handling, has_shebang)
                findings.append(Finding(
                    rule_id=rule_id,
                    severity=rule['severity'],
                    description=rule['description'],
                    line=i,
                    line_content=line.strip()[:100],
                    confidence=confidence
                ))

        # Check performance rules
        for rule_id, rule in PERFORMANCE_RULES.items():
            if re.search(rule['pattern'], line):
                findings.append(Finding(
                    rule_id=rule_id,
                    severity=rule['severity'],
                    description=rule['description'],
                    line=i,
                    line_content=line.strip()[:100],
                    confidence=60  # Lower confidence for performance
                ))

    return AnalysisResult(
        file_path=file_path,
        findings=findings,
        lines_of_code=len(lines),
        analysis_time=datetime.now().isoformat()
    )

def calculate_confidence(severity: str, has_error_handling: bool, has_shebang: bool) -> int:
    """Calculate confidence score based on context."""
    base_confidence = {
        "Critical": 90,
        "High": 80,
        "Medium": 70,
        "Low": 60
    }.get(severity, 50)

    # Reduce confidence if error handling is present (might be intentional)
    if has_error_handling:
        base_confidence -= 5

    # Increase confidence if proper shebang is present
    if has_shebang:
        base_confidence += 5

    return max(50, min(100, base_confidence))

def analyze_hooks_directory(hooks_dir: str, config: Dict[str, Any] = None) -> List[AnalysisResult]:
    """Analyze all shell scripts in hooks directory."""
    results = []

    hooks_path = Path(hooks_dir)
    if not hooks_path.exists():
        print(f"Error: Directory {hooks_dir} not found")
        return results

    # Find all .sh files
    sh_files = sorted(hooks_path.glob("**/*.sh"))

    print(f"Found {len(sh_files)} shell scripts in {hooks_dir}")

    for sh_file in sh_files:
        print(f"Analyzing: {sh_file}")
        result = analyze_file(str(sh_file), config)
        results.append(result)

    return results

def generate_summary(results: List[AnalysisResult]) -> Dict[str, Any]:
    """Generate summary statistics from analysis results."""
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
    total_findings = 0

    for result in results:
        for finding in result.findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
            total_findings += 1

    # Calculate health score
    critical_penalty = severity_counts["Critical"] * 20
    high_penalty = severity_counts["High"] * 10
    medium_penalty = severity_counts["Medium"] * 5

    health_score = max(0, 100 - critical_penalty - high_penalty - medium_penalty)

    return {
        "total_files": len(results),
        "total_findings": total_findings,
        "severity_counts": severity_counts,
        "health_score": health_score
    }

def main():
    # Auto-detect config file in same directory as script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = os.path.join(script_dir, "..", "data", "analysis-rules.yaml")

    parser = argparse.ArgumentParser(description="Hook Analyzer - Scan Claude Code hooks")
    parser.add_argument("hooks_dir", nargs="?", default=".claude/hooks",
                        help="Directory containing hook scripts")
    parser.add_argument("--output", "-o", default="analysis-results.json",
                        help="Output JSON file")
    parser.add_argument("--config", "-c", default=default_config,
                        help="Analysis rules YAML file (default: auto-detect from script location)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    parser.add_argument("--no-config", action="store_true",
                        help="Skip loading config file, use only default rules")

    args = parser.parse_args()

    # Load config
    config = {}
    if not args.no_config and os.path.exists(args.config):
        config = load_analysis_rules(args.config)
        print(f"Loaded custom rules from: {args.config}")
    elif not args.no_config:
        print(f"Config file not found: {args.config}, using default rules")

    # Analyze hooks
    results = analyze_hooks_directory(args.hooks_dir, config)

    # Generate summary
    summary = generate_summary(results)

    if args.verbose:
        print(f"\nAnalysis Summary:")
        print(f"  Files analyzed: {summary['total_files']}")
        print(f"  Total findings: {summary['total_findings']}")
        print(f"  Health score: {summary['health_score']}%")
        print(f"\nSeverity breakdown:")
        for severity, count in summary['severity_counts'].items():
            if count > 0:
                print(f"    {severity}: {count}")

    # Write results
    output = {
        "summary": summary,
        "results": [r.to_dict() for r in results],
        "analyzed_at": datetime.now().isoformat()
    }

    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults written to {args.output}")

    # Return exit code based on health score
    if summary['health_score'] < 50:
        return 2  # Critical issues found
    elif summary['health_score'] < 70:
        return 1  # Issues found
    return 0

if __name__ == "__main__":
    sys.exit(main())
