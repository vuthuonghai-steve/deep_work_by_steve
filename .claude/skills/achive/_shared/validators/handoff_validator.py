#!/usr/bin/env python3
"""
handoff_validator.py — Validate handoff readiness per stage.

Validates that an artifact meets the handoff contract for a given stage.

Stages:
  design-to-planner   Validate design.md is ready for the Planner
  planner-to-builder  Validate todo.md is ready for the Builder
  builder-complete    Validate build-log.md is complete and consistent

CLI:
    python handoff_validator.py --stage <stage> <file.md>

Output: YAML with stage, artifact, passed, checks list.
Each check: name, status (pass/fail), error, fix_hint.
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Dependency management
# ---------------------------------------------------------------------------

def _ensure_deps():
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("Missing pyyaml. Attempting pip install...", file=sys.stderr)
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyyaml", "-q"],
                timeout=60,
            )
            print("Installation successful.\n", file=sys.stderr)
        except Exception as e:
            print(f"ERROR: Could not install pyyaml: {e}", file=sys.stderr)
            print("Please run: pip install pyyaml", file=sys.stderr)
            sys.exit(1)


_ensure_deps()
import yaml


# ---------------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(file_path):
    """Extract and parse YAML frontmatter from a Markdown file.

    Returns (data, error_string).
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, f"File not found: {file_path}"
    except OSError as e:
        return None, str(e)

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

    if not isinstance(data, dict):
        return None, "Frontmatter must be a YAML mapping"

    return data, None


def get_markdown_headings(file_path):
    """Return the list of ##-level section heading text lines from the
    Markdown body (after frontmatter)."""
    content = Path(file_path).read_text(encoding="utf-8")
    parts = content.split("---", 2)
    body = parts[2] if len(parts) >= 3 else content
    return re.findall(r"^##\s+(.+)", body, re.MULTILINE)


def make_check(name, passed, error=None, fix_hint=None):
    """Create a single check dict."""
    return {
        "name": name,
        "status": "pass" if passed else "fail",
        "error": error,
        "fix_hint": fix_hint,
    }


# ---------------------------------------------------------------------------
# Trace tag validation helper
# ---------------------------------------------------------------------------

VALID_TRACE_PATTERNS = [
    re.compile(r"^\[TỪ DESIGN §[0-9]+(\.[0-9]+)?\]$"),
    re.compile(r"^\[GỢI Ý BỔ SUNG\]$"),
    re.compile(r"^\[CẦN LÀM RÕ\]$"),
    re.compile(r"^\[TỪ AUDIT TÀI NGUYÊN\]$"),
]

TRACE_KEYWORDS = ["TỪ ", "GỢI", "CẦN", "CẦU", "DESIGN", "AUDIT", "TÀI NGUYÊN", "DESION"]
ANY_BRACKET = re.compile(r"\[([^\]]*)\]")


def _is_trace_like(text):
    upper = text.upper()
    return any(kw.upper() in upper for kw in TRACE_KEYWORDS)


def find_invalid_trace_tags(file_path):
    """Return list of invalid trace tags found in a file."""
    content = Path(file_path).read_text(encoding="utf-8")
    bad = []
    for match in ANY_BRACKET.finditer(content):
        tag = match.group(0)
        if _is_trace_like(match.group(1)):
            if not any(p.match(tag) for p in VALID_TRACE_PATTERNS):
                bad.append(tag)
    return bad


# ---------------------------------------------------------------------------
# Stage: design-to-planner
# ---------------------------------------------------------------------------

# The 10 required sections (by their numbered prefix)
REQUIRED_SECTION_PREFIXES = [
    "1.", "2.", "3.", "4.", "5.",
    "6.", "7.", "8.", "9.", "10.",
]

REQUIRED_ZONES = ["core", "knowledge", "scripts", "templates", "data", "loop", "assets"]


def _check_schema(data, expected_artifact_type, expected_stage):
    """Run basic schema checks and return a list of check dicts."""
    checks = []

    version = data.get("skill_schema_version")
    checks.append(make_check(
        "schema_version",
        version == "3.0.0",
        error=f"skill_schema_version must be '3.0.0', got '{version}'" if version != "3.0.0" else None,
        fix_hint='Set skill_schema_version: "3.0.0"',
    ))

    artifact = data.get("artifact_type")
    checks.append(make_check(
        "artifact_type",
        artifact == expected_artifact_type,
        error=f"artifact_type must be '{expected_artifact_type}', got '{artifact}'" if artifact != expected_artifact_type else None,
        fix_hint=f"Set artifact_type: \"{expected_artifact_type}\"",
    ))

    stage = data.get("stage")
    checks.append(make_check(
        "stage",
        stage == expected_stage,
        error=f"stage must be '{expected_stage}', got '{stage}'" if stage != expected_stage else None,
        fix_hint=f"Set stage: \"{expected_stage}\"",
    ))

    return checks


def validate_design_to_planner(file_path, data):
    """Validate design.md for handoff from Architect to Planner."""
    checks = []

    # Schema checks
    checks.extend(_check_schema(data, "design", "architect"))

    # Status must be ready_for_planner
    status = data.get("status")
    checks.append(make_check(
        "status_ready_for_planner",
        status == "ready_for_planner",
        error=f"status must be 'ready_for_planner', got '{status}'" if status != "ready_for_planner" else None,
        fix_hint="Set status: \"ready_for_planner\"",
    ))

    # All 7 zones present
    zone_mapping = data.get("zone_mapping", {})
    present = [z for z in REQUIRED_ZONES if z in zone_mapping]
    missing_zones = set(REQUIRED_ZONES) - set(present)
    checks.append(make_check(
        "all_7_zones_present",
        len(missing_zones) == 0,
        error=f"Missing zones: {sorted(missing_zones)}" if missing_zones else None,
        fix_hint="Add zone_mapping entries for all 7 zones: core, knowledge, scripts, templates, data, loop, assets",
    ))

    # Valid paths: no absolute, no ".."
    bad_paths = []
    for zname, zdata in zone_mapping.items():
        for f_entry in zdata.get("files", []):
            p = f_entry.get("path", "")
            if p.startswith("/"):
                bad_paths.append(f"{zname}: '{p}' (absolute path)")
            elif ".." in p.split("/"):
                bad_paths.append(f"{zname}: '{p}' (contains '..')")
    checks.append(make_check(
        "valid_paths_no_absolute_or_dotdot",
        len(bad_paths) == 0,
        error=f"Invalid paths: {bad_paths}" if bad_paths else None,
        fix_hint="Paths must be relative, must not start with '/', and must not contain '..' segments",
    ))

    # Progressive disclosure tier1 has base field
    pd = data.get("progressive_disclosure", {})
    tier1 = pd.get("tier1", [])
    tier1_missing_base = [item.get("path", "?") for item in tier1 if "base" not in item]
    checks.append(make_check(
        "tier1_base_field",
        len(tier1_missing_base) == 0,
        error=f"tier1 items missing 'base' field: {tier1_missing_base}" if tier1_missing_base else None,
        fix_hint="Every tier1 item must have a 'base' field set to 'skills_root' or 'skill_dir'",
    ))

    # All 10 required section headings present in body
    headings = get_markdown_headings(file_path)
    missing_sections = []
    for prefix in REQUIRED_SECTION_PREFIXES:
        if not any(h.strip().startswith(prefix) for h in headings):
            missing_sections.append(prefix)
    checks.append(make_check(
        "required_10_sections_present",
        len(missing_sections) == 0,
        error=f"Missing section headings starting with: {missing_sections}" if missing_sections else None,
        fix_hint="Add ## 1. through ## 10. section headings in the Markdown body",
    ))

    # Handoff next_stage == planner
    handoff = data.get("handoff", {})
    next_stage = handoff.get("next_stage")
    checks.append(make_check(
        "handoff_next_stage_planner",
        next_stage == "planner",
        error=f"handoff.next_stage must be 'planner', got '{next_stage}'" if next_stage != "planner" else None,
        fix_hint="Set handoff.next_stage: \"planner\"",
    ))

    # Trace tags: no unparseable tags
    invalid_tags = find_invalid_trace_tags(file_path)
    checks.append(make_check(
        "trace_tags_valid",
        len(invalid_tags) == 0,
        error=f"Invalid trace tags found: {invalid_tags}" if invalid_tags else None,
        fix_hint="Use only valid tag patterns: [TỪ DESIGN §N], [GỢI Ý BỔ SUNG], [CẦN LÀM RÕ], [TỪ AUDIT TÀI NGUYÊN]",
    ))

    passed = all(c["status"] == "pass" for c in checks)
    return {
        "stage": "design-to-planner",
        "artifact": Path(file_path).name,
        "passed": passed,
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# Stage: planner-to-builder
# ---------------------------------------------------------------------------

def validate_planner_to_builder(file_path, data):
    """Validate todo.md for handoff from Planner to Builder."""
    checks = []

    # Schema checks
    checks.extend(_check_schema(data, "todo", "planner"))

    # Status must be ready_for_builder
    status = data.get("status")
    checks.append(make_check(
        "status_ready_for_builder",
        status == "ready_for_builder",
        error=f"status must be 'ready_for_builder', got '{status}'" if status != "ready_for_builder" else None,
        fix_hint="Set status: \"ready_for_builder\"",
    ))

    # Collect all task IDs across phases
    all_tasks = []
    for phase in data.get("phases", []):
        for task in phase.get("tasks", []):
            all_tasks.append(task)

    task_ids = [t.get("id") for t in all_tasks]

    # All task IDs unique
    seen = {}
    dups = []
    for tid in task_ids:
        if tid in seen:
            dups.append(tid)
        seen[tid] = True
    checks.append(make_check(
        "unique_task_ids",
        len(dups) == 0,
        error=f"Duplicate task IDs: {sorted(set(dups))}" if dups else None,
        fix_hint="Each task must have a unique 'id' field",
    ))

    # All depends_on IDs exist
    id_set = set(task_ids)
    bad_deps = []
    dep_summary = {}
    for task in all_tasks:
        for dep in task.get("depends_on", []):
            if dep not in id_set:
                bad_deps.append(dep)
                dep_summary.setdefault(task["id"], []).append(dep)
    checks.append(make_check(
        "depends_on_targets_exist",
        len(bad_deps) == 0,
        error=f"Missing dependency targets in tasks: {dep_summary}" if bad_deps else None,
        fix_hint="Every depends_on value must reference a valid task ID within this todo.md",
    ))

    # No blockers with resolved: false
    blockers = data.get("blockers", [])
    unresolved = [b["id"] for b in blockers if b.get("resolved") is False]
    checks.append(make_check(
        "no_unresolved_blockers",
        len(unresolved) == 0,
        error=f"Unresolved blockers: {unresolved}" if unresolved else None,
        fix_hint="Set resolved: true on all blockers, or resolve them before handoff",
    ))

    # All PH0 tasks: done or skipped
    ph0_tasks = []
    for phase in data.get("phases", []):
        if phase.get("id") == "PH0":
            ph0_tasks = phase.get("tasks", [])
    ph0_not_finished = [
        t["id"] for t in ph0_tasks
        if t.get("status") not in ("done", "skipped")
    ]
    checks.append(make_check(
        "phase0_all_done_or_skipped",
        len(ph0_not_finished) == 0,
        error=f"PH0 tasks not finished: {ph0_not_finished}" if ph0_not_finished else None,
        fix_hint="All Phase 0 (PH0) tasks must have status 'done' or 'skipped' before handoff",
    ))

    # All prerequisites status: ready
    preqs = data.get("prerequisites", [])
    not_ready = [(p["item"], p.get("status")) for p in preqs if p.get("status") != "ready"]
    checks.append(make_check(
        "prerequisites_all_ready",
        len(not_ready) == 0,
        error=f"Prerequisites not ready: {not_ready}" if not_ready else None,
        fix_hint="All prerequisites must have status: \"ready\"",
    ))

    # Handoff next_stage == builder
    handoff = data.get("handoff", {})
    next_stage = handoff.get("next_stage")
    checks.append(make_check(
        "handoff_next_stage_builder",
        next_stage == "builder",
        error=f"handoff.next_stage must be 'builder', got '{next_stage}'" if next_stage != "builder" else None,
        fix_hint="Set handoff.next_stage: \"builder\"",
    ))

    passed = all(c["status"] == "pass" for c in checks)
    return {
        "stage": "planner-to-builder",
        "artifact": Path(file_path).name,
        "passed": passed,
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# Stage: builder-complete
# ---------------------------------------------------------------------------

def validate_builder_complete(file_path, data):
    """Validate build-log.md for completion."""
    checks = []

    # Schema checks
    checks.extend(_check_schema(data, "build-log", "builder"))

    # No STOP_AND_REPORT in execution_trace
    trace = data.get("execution_trace", [])
    stop_entries = [e for e in trace if e.get("decision") == "STOP_AND_REPORT"]
    checks.append(make_check(
        "no_stop_and_report",
        len(stop_entries) == 0,
        error=f"STOP_AND_REPORT found in execution_trace: {[e.get('task_id') for e in stop_entries]}" if stop_entries else None,
        fix_hint="Resolve all STOP_AND_REPORT decisions before marking build as complete",
    ))

    # Contradiction check: no failed action alongside validator_pass == true
    failed_actions = [e for e in trace if e.get("status") == "failed"]
    qm = data.get("quality_metrics", {})
    vp = qm.get("validator_pass")

    # Check A: if failed action exists AND no STOP_AND_REPORT, that's a problem
    failed_without_stop = [
        e for e in failed_actions
        if e.get("decision") != "STOP_AND_REPORT"
    ]
    checks.append(make_check(
        "failed_actions_have_stop_and_report",
        len(failed_without_stop) == 0,
        error=f"Failed actions without STOP_AND_REPORT: {[e.get('task_id') for e in failed_without_stop]}" if failed_without_stop else None,
        fix_hint="Every failed action should have decision: STOP_AND_REPORT",
    ))

    # Check B: validator_pass contradiction — failed execution but validator_pass=true
    has_failed = len(failed_actions) > 0
    vp_contradiction = has_failed and vp is True
    checks.append(make_check(
        "no_validator_pass_contradiction",
        not vp_contradiction,
        error="execution_trace has failed actions but quality_metrics.validator_pass=true (contradiction)" if vp_contradiction else None,
        fix_hint="If any execution_trace action failed, validator_pass must be false",
    ))

    # Placeholder ratio < 0.10
    pr = qm.get("placeholder_ratio", 1.0)
    checks.append(make_check(
        "placeholder_ratio_below_0.10",
        pr < 0.10,
        error=f"placeholder_ratio is {pr}, must be < 0.10" if pr >= 0.10 else None,
        fix_hint="Reduce placeholder content to achieve placeholder_ratio < 0.10",
    ))

    # validator_pass == true
    checks.append(make_check(
        "validator_pass_true",
        vp is True,
        error="validator_pass must be true for build completion" if vp is not True else None,
        fix_hint="Set quality_metrics.validator_pass: true",
    ))

    passed = all(c["status"] == "pass" for c in checks)
    return {
        "stage": "builder-complete",
        "artifact": Path(file_path).name,
        "passed": passed,
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# CLI and routing
# ---------------------------------------------------------------------------

STAGE_VALIDATORS = {
    "design-to-planner": validate_design_to_planner,
    "planner-to-builder": validate_planner_to_builder,
    "builder-complete": validate_builder_complete,
}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate handoff readiness for a given stage.")
    parser.add_argument("--stage", "-s", required=True,
                        choices=list(STAGE_VALIDATORS.keys()),
                        help="Validation stage")
    parser.add_argument("file", help="Artifact file to validate")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    file_path = args.file

    # Parse frontmatter
    data, parse_err = parse_frontmatter(file_path)
    if parse_err:
        result = {
            "stage": args.stage,
            "artifact": Path(file_path).name,
            "passed": False,
            "checks": [make_check(
                "yaml_frontmatter_parse",
                False,
                parse_err,
                "Ensure the file has valid YAML frontmatter between --- delimiters",
            )],
        }
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                        sort_keys=False))
        return 1

    # Route to the right validator
    validator_fn = STAGE_VALIDATORS[args.stage]
    result = validator_fn(file_path, data)

    print(yaml.dump(result, default_flow_style=False, allow_unicode=True,
                    sort_keys=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
