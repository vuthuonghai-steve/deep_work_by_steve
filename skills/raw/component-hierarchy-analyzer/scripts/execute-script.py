#!/usr/bin/env python3
"""
execute-script.py - Execute generate-component-hierarchy.ts and capture output

Usage:
    python scripts/execute-script.py --src <path> --entry <path> [options]

This script:
- Checks executable availability (bun and .ts file)
- Builds CLI arguments from mapped input
- Runs read-only command with subprocess
- Captures stdout, stderr, and exit code
- Returns structured result for parsing
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional


def check_bun_available() -> bool:
    """Check if bun runtime is available in PATH."""
    try:
        result = subprocess.run(
            ["bun", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_script_exists(script_path: Path) -> bool:
    """Check if the TypeScript script exists at the given path."""
    return script_path.exists() and script_path.is_file()


def build_command(
    src: str,
    entry: str,
    focus: Optional[str] = None,
    scope: str = "down",
    layout_only: bool = False,
    alias: Optional[Dict[str, str]] = None,
    root_component: Optional[str] = None,
    script_path: str = "generate-component-hierarchy.ts"
) -> list[str]:
    """
    Build the bun command with all arguments.

    Args:
        src: Source directory path
        entry: Entry file path
        focus: Component name to focus on (optional)
        scope: Focus scope mode (up/full/down)
        layout_only: Whether to enable layout-only mode
        alias: Path alias mappings (optional)
        root_component: Root component name override (optional)
        script_path: Path to the TypeScript script

    Returns:
        List of command arguments
    """
    cmd = ["bun", script_path]
    cmd.extend(["--src", src])
    cmd.extend(["--entry", entry])

    if focus:
        cmd.extend(["--focus", focus])

    if scope:
        cmd.extend(["--scope", scope])

    if layout_only:
        cmd.append("--layoutOnly")

    if alias:
        for key, value in alias.items():
            cmd.extend(["--alias", f"{key}={value}"])

    if root_component:
        cmd.extend(["--rootComponent", root_component])

    return cmd


def execute_command(
    cmd: list[str],
    cwd: Optional[str] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Execute the command and capture output.

    Args:
        cmd: Command list to execute
        cwd: Working directory (defaults to current directory)
        timeout: Timeout in seconds

    Returns:
        Dictionary with stdout, stderr, exit_code, success, error
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "success": result.returncode == 0,
            "error": None
        }
    except subprocess.TimeoutExpired as e:
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout}s",
            "exit_code": -1,
            "success": False,
            "error": "timeout"
        }
    except FileNotFoundError as e:
        return {
            "stdout": "",
            "stderr": f"Command not found: {e.filename}",
            "exit_code": -1,
            "success": False,
            "error": "not_found"
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "success": False,
            "error": "unknown"
        }


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Execute generate-component-hierarchy.ts")
    parser.add_argument("--src", required=True, help="Source directory")
    parser.add_argument("--entry", required=True, help="Entry file path")
    parser.add_argument("--focus", help="Focus on specific component")
    parser.add_argument("--scope", default="down", choices=["up", "full", "down"], help="Focus scope")
    parser.add_argument("--layoutOnly", action="store_true", help="Layout-only mode")
    parser.add_argument("--alias", action="append", help="Path alias (key=value), repeatable")
    parser.add_argument("--rootComponent", help="Root component name override")
    parser.add_argument("--script", default="generate-component-hierarchy.ts", help="Script path")
    parser.add_argument("--cwd", help="Working directory")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")

    args = parser.parse_args()

    # Parse alias pairs
    alias_dict = {}
    if args.alias:
        for pair in args.alias:
            if "=" in pair:
                key, value = pair.split("=", 1)
                alias_dict[key] = value

    # Check bun availability
    if not check_bun_available():
        result = {
            "stdout": "",
            "stderr": "Error: bun runtime not found in PATH. Install bun from https://bun.sh",
            "exit_code": -1,
            "success": False,
            "error": "bun_not_found"
        }
        print(json.dumps(result))
        sys.exit(1)

    # Check script exists
    script_path = Path(args.script)
    if not check_script_exists(script_path):
        result = {
            "stdout": "",
            "stderr": f"Error: Script not found at {args.script}",
            "exit_code": -1,
            "success": False,
            "error": "script_not_found"
        }
        print(json.dumps(result))
        sys.exit(1)

    # Build command
    cmd = build_command(
        src=args.src,
        entry=args.entry,
        focus=args.focus,
        scope=args.scope,
        layout_only=args.layoutOnly,
        alias=alias_dict if alias_dict else None,
        root_component=args.rootComponent,
        script_path=args.script
    )

    # Execute
    result = execute_command(cmd, cwd=args.cwd, timeout=args.timeout)
    result["command"] = " ".join(cmd)

    print(json.dumps(result))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
