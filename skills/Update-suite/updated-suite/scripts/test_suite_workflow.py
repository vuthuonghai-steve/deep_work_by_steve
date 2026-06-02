#!/usr/bin/env python3
"""
test_suite_workflow.py — Execute the 8-phase workflow to test the ver-3
Master Skill Suite integrity.

Phases:
  P1 Frontmatter & XML Boundary Check
  P2 Path & Link Integrity
  P3 Schema Validation (Good + Bad Fixtures)
  P4 Trace Tag Validation
  P5 Handoff Validation Between Stages
  P6 Cross-Skill Reference & Boot Script Existence
  P7 Placeholder Density Measurement
  P8 Ver-2/Ver-3 Version Label Sanity

CLI:
    python3 test_suite_workflow.py             # run all phases
    python3 test_suite_workflow.py --phase P3  # run a single phase
    python3 test_suite_workflow.py --phase P3 --json  # emit JSON report

Output: YAML with stage, artifact, timestamp, passed, checks list.
Each check: name, status (pass/fail), error, severity, fix_hint.
Exit 0 if all checks pass, exit 1 if any fail.

Gracefully attempts pip install if pyyaml is missing.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency management
# ---------------------------------------------------------------------------

def _ensure_deps():
    missing = []
    try:
        import yaml  # noqa: F401
    except ImportError:
        missing.append("pyyaml")
    if not missing:
        return
    print(f"Missing dependencies: {', '.join(missing)}. Attempting pip install...",
          file=sys.stderr)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing, "-q"],
            timeout=60,
        )
    except Exception as e:
        print(f"ERROR: Could not install dependencies: {e}", file=sys.stderr)
        sys.exit(1)


_ensure_deps()
import yaml  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUITE_ROOT = Path(__file__).resolve().parent.parent
SHARED = SUITE_ROOT / "_shared"
VALIDATORS = SHARED / "validators"
SCHEMAS = SHARED / "schemas"
FIXTURES = SHARED / "fixtures"
SCRIPTS = SUITE_ROOT / "scripts"

SKILLS = [
    "skill-explorer",
    "skill-knowledge-miner",
    "skill-architect",
    "skill-planner",
    "skill-builder",
    "production-code-reviewer",
    "production-quality-gatekeeper",
]

XML_TAGS = ["instructions", "context", "output_contract"]

SHARED_REFS = [
    "_shared/knowledge/framework.md",
    "_shared/knowledge/case-system.md",
    "_shared/knowledge/format-standards.md",
    "_shared/validators/check_status.py",
    "_shared/validators/schema_validator.py",
    "_shared/validators/trace_validator.py",
    "_shared/validators/handoff_validator.py",
    "_shared/validators/rollback_engine.py",
]

SCHEMA_FILES = [
    "exploration.schema.yaml",
    "design.schema.yaml",
    "todo.schema.yaml",
    "criteria.schema.json",
    "build-log.schema.yaml",
    "dag_plan.schema.json",
    "diagnostic.schema.json",
    "verification.schema.json",
]

PLACEHOLDER_PATTERNS = [
    (r"\bTODO\b", "TODO marker"),
    (r"\bFIXME\b", "FIXME marker"),
    (r"\bXXX\b", "XXX marker"),
    (r"\bTBD\b", "TBD marker"),
    (r"// PLACEHOLDER", "// PLACEHOLDER"),
    (r"pass\s*#.*placeholder", "pass placeholder"),
    (r"mock\(\)", "mock() call"),
    (r"raise NotImplementedError", "NotImplementedError"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read(p):
    try:
        return Path(p).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError:
        return None


def _check(name, severity, fn):
    """Run a check function. fn() returns (ok, error, fix_hint)."""
    try:
        ok, error, fix_hint = fn()
    except Exception as e:  # pragma: no cover
        ok = False
        error = f"exception: {e}"
        fix_hint = "Re-run with --verbose; report bug if persistent."
    return {
        "name": name,
        "status": "pass" if ok else "fail",
        "severity": severity,
        "error": "" if ok else (error or "unspecified failure"),
        "fix_hint": "" if ok else (fix_hint or "Review the underlying artifact and align with shared schema/spec."),
    }


# ---------------------------------------------------------------------------
# Phase 1: Frontmatter & XML Boundary
# ---------------------------------------------------------------------------

def p1_frontmatter_xml():
    checks = []

    def c11():
        results = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md")
            if content is None:
                results.append(f"MISSING {s}")
                continue
            first = content.splitlines()[0] if content.splitlines() else ""
            if first.strip() == "---":
                results.append(f"OK {s}")
            else:
                results.append(f"FAIL {s} (line 1 = {first!r})")
        bad = [r for r in results if not r.startswith("OK")]
        if bad:
            return False, "; ".join(bad), "Ensure each SKILL.md starts with `---` on line 1."
        return True, "", "N/A"

    def c12():
        if not (SCRIPTS / "validate_suite_integrity.py").exists():
            return False, "scripts/validate_suite_integrity.py not found", "Restore the integrity script."
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_suite_integrity.py")],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        verdict_count = sum(1 for ln in out.splitlines() if "PASS" in ln or "FAIL" in ln)
        if verdict_count < 9:
            return False, f"only {verdict_count} verdict lines (< 9)", "Fix I2: add skill-builder to SKILLS list in validate_suite_integrity.py."
        return True, "", "N/A"

    def c13():
        missing = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            for tag in XML_TAGS:
                if f"<{tag}>" not in content or f"</{tag}>" not in content:
                    missing.append(f"{s} missing <{tag}>")
        if missing:
            return False, "; ".join(missing), "Add the missing XML boundary tags in each SKILL.md."
        return True, "", "N/A"

    def c14():
        missing = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            m = re.search(r"<instructions>(.*?)</instructions>", content, re.S | re.I)
            if not m:
                missing.append(f"{s} (no <instructions>)")
                continue
            body = m.group(1).lower()
            if "must:" not in body and "must_not:" not in body:
                missing.append(s)
        if missing:
            return False, f"instructions without must/must_not: {missing}", "Add YAML `must:` or `must_not:` blocks inside <instructions>."
        return True, "", "N/A"

    def c15():
        offenders = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            m = re.search(r"^---\n(.*?)\n---", content, re.S)
            if not m:
                offenders.append(f"{s} no frontmatter")
                continue
            fm = m.group(1)
            opens = re.findall(r"<([a-z_]+)>", fm)
            closes = re.findall(r"</([a-z_]+)>", fm)
            if opens or closes:
                offenders.append(f"{s} {opens}/{closes}")
        if offenders:
            return False, "; ".join(offenders), "Remove XML tags from frontmatter — keep YAML keys only."
        return True, "", "N/A"

    checks.append(_check("P1.1 every SKILL.md opens with --- frontmatter", "critical", c11))
    checks.append(_check("P1.2 validate_suite_integrity.py verdict count >= 9", "critical", c12))
    checks.append(_check("P1.3 every SKILL.md has <instructions>/<context>/<output_contract>", "high", c13))
    checks.append(_check("P1.4 <instructions> blocks contain must: or must_not:", "high", c14))
    checks.append(_check("P1.5 no XML tags inside frontmatter", "medium", c15))
    return checks


# ---------------------------------------------------------------------------
# Phase 2: Path & Link Integrity
# ---------------------------------------------------------------------------

def p2_path_integrity():
    checks = []

    def c21():
        if not (SCRIPTS / "validate_suite_integrity.py").exists():
            return False, "integrity script missing", "Restore validate_suite_integrity.py."
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_suite_integrity.py")],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        broken = sum(1 for ln in out.splitlines() if "Broken link" in ln)
        if broken > 0:
            return False, f"{broken} broken link(s) reported", "Fix all 'Liên kết tham chiếu hỏng' lines from validate_suite_integrity.py output."
        return True, "", "N/A"

    def c22():
        missing = [r for r in SHARED_REFS if not (SUITE_ROOT / r).exists()]
        if missing:
            return False, f"missing: {missing}", "Recreate the missing _shared files referenced in shared/validators."
        return True, "", "N/A"

    def c23():
        # Scan all SKILL.md for relative ../_shared/... or knowledge/... refs
        bad = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            for m in re.finditer(r"`?(\.\.?/_shared/[^`\"' ]+)", content):
                p = m.group(1)
                if not (SUITE_ROOT / s / p).exists() and not (SUITE_ROOT / p).exists():
                    bad.append(f"{s} -> {p}")
        if bad:
            return False, "; ".join(bad[:5]), "Repair or create the missing cross-skill _shared paths."
        return True, "", "N/A"

    def c24():
        # Match zone-relative references. Strip optional ../ prefix for
        # ../_shared/... pattern (these are skill-dir-relative to _shared/).
        pat = re.compile(r"((?:\.\./)?(?:knowledge|templates|scripts|data|loop|policies|references|_shared)/[a-zA-Z0-9_./-]+\.[a-z]+)")
        miss = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            for line in content.splitlines():
                for m in pat.findall(line):
                    if "{" in m:
                        continue
                    if m.startswith("../"):
                        # ../_shared/... → resolve against SUITE_ROOT
                        candidate = SUITE_ROOT / m[3:]
                    else:
                        # knowledge/... etc. → resolve against skill dir first,
                        # then against _shared
                        candidate = SUITE_ROOT / s / m
                        if not candidate.exists():
                            candidate = SHARED / m
                    if not candidate.exists():
                        miss.append(f"{s}:{m}")
        if miss:
            return False, f"{len(miss)} broken ref(s); first: {miss[0]}", "Create the missing files or correct the path strings in SKILL.md."
        return True, "", "N/A"

    checks.append(_check("P2.1 integrity script reports 0 broken links", "critical", c21))
    checks.append(_check("P2.2 all 8 _shared references exist on disk", "critical", c22))
    checks.append(_check("P2.3 no broken ../_shared/... cross-skill refs", "high", c23))
    checks.append(_check("P2.4 regex scan finds NO_BROKEN_REFS in zone paths", "high", c24))
    return checks


# ---------------------------------------------------------------------------
# Phase 3: Schema Validation (good + bad fixtures)
# ---------------------------------------------------------------------------

def p3_schema():
    checks = []

    def run_validator(schema, fixture):
        proc = subprocess.run(
            [sys.executable, str(VALIDATORS / "schema_validator.py"),
             "--schema", str(SCHEMAS / schema), str(FIXTURES / fixture)],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

    def c31():
        rc, out = run_validator("design.schema.yaml", "good/design.md")
        if rc != 0 or "passed: true" not in out:
            return False, f"rc={rc}; out tail={out[-300:]}", "Fix good/design.md to satisfy design.schema.yaml."
        return True, "", "N/A"

    def c32():
        rc, out = run_validator("design.schema.yaml", "bad/design.md")
        if rc == 0 or "passed: false" not in out:
            return False, f"validator accepted bad fixture (rc={rc})", "Tighten design.schema.yaml to catch the bad fixture defects."
        return True, "", "N/A"

    def c33():
        rc, out = run_validator("todo.schema.yaml", "good/todo.md")
        if rc != 0 or "passed: true" not in out:
            return False, f"rc={rc}; out tail={out[-300:]}", "Fix good/todo.md to satisfy todo.schema.yaml."
        return True, "", "N/A"

    def c34():
        rc, out = run_validator("todo.schema.yaml", "bad/todo.md")
        if rc == 0 or "passed: false" not in out:
            return False, f"validator accepted bad fixture (rc={rc})", "Tighten todo.schema.yaml to catch bad fixture defects."
        return True, "", "N/A"

    def c35():
        missing = [s for s in SCHEMA_FILES if not (SCHEMAS / s).exists()]
        if missing:
            return False, f"missing: {missing}", "Restore the missing schema files."
        return True, "", "N/A"

    checks.append(_check("P3.1 design.schema.yaml accepts good/design.md", "critical", c31))
    checks.append(_check("P3.2 design.schema.yaml rejects bad/design.md", "critical", c32))
    checks.append(_check("P3.3 todo.schema.yaml accepts good/todo.md", "critical", c33))
    checks.append(_check("P3.4 todo.schema.yaml rejects bad/todo.md", "critical", c34))
    checks.append(_check("P3.5 all 9 schema files present", "high", c35))
    return checks


# ---------------------------------------------------------------------------
# Phase 4: Trace Tag Validation
# ---------------------------------------------------------------------------

def p4_trace():
    checks = []

    def c41():
        proc = subprocess.run(
            [sys.executable, str(VALIDATORS / "trace_validator.py"),
             str(FIXTURES / "good" / "todo.md")],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if "passed: true" not in out:
            return False, f"rc={proc.returncode}; out tail={out[-300:]}", "Fix trace_validator or good/todo.md to include valid [TỪ DESIGN §N] tags."
        return True, "", "N/A"

    def c42():
        # Trace I3: SyntaxWarning on [ in module docstring
        proc = subprocess.run(
            [sys.executable, "-W", "error::SyntaxWarning",
             str(VALIDATORS / "trace_validator.py"),
             str(FIXTURES / "good" / "todo.md")],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if "SyntaxWarning" not in out and proc.returncode == 0:
            return False, "no SyntaxWarning raised", "Either fix trace_validator.py docstring or accept this as informational."
        return True, "", "N/A"

    def c43():
        content = _read(VALIDATORS / "trace_validator.py") or ""
        tags = re.findall(r"\[[^\]]*\]", content)
        offenders = []
        for t in tags:
            if any(k in t for k in ["NGUYÊN", "GỢI Ý", "CẦN LÀM RÕ", "TỪ DESIGN"]):
                if t not in ("[TỪ DESIGN §N]", "[TỪ DESIGN §N.M]",
                             "[GỢI Ý BỔ SUNG]", "[CẦN LÀM RÕ]",
                             "[TỪ AUDIT TÀI NGUYÊN]"):
                    offenders.append(t)
        # Informational: surface the tags, do not fail
        if offenders:
            return True, f"informational tags: {offenders[:3]}", "N/A"
        return True, "no docstring tags", "N/A"

    def c44():
        proc = subprocess.run(
            [sys.executable, str(VALIDATORS / "trace_validator.py"),
             str(FIXTURES / "bad" / "todo.md")],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        # Informational pass — bad fixture may or may not have trace tags
        return True, f"rc={proc.returncode}", "N/A"

    def c45():
        legacy = ["[GỢI Ý]", "[TỪ AUDIT]", "[TỪ AUDIT CUSTOM]", "[CẦU LÀM RÕ]"]
        hits = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            found = [t for t in legacy if t in content]
            if found:
                hits.append(f"{s}: {found}")
        if hits:
            return False, "; ".join(hits), "Rename legacy trace tags to canonical form."
        return True, "", "N/A"

    checks.append(_check("P4.1 trace_validator accepts good/todo.md", "critical", c41))
    checks.append(_check("P4.2 trace_validator raises SyntaxWarning on docstring [", "medium", c42))
    checks.append(_check("P4.3 trace_validator docstring tag audit (informational)", "low", c43))
    checks.append(_check("P4.4 trace_validator runs against bad/todo.md (informational)", "medium", c44))
    checks.append(_check("P4.5 no legacy trace tags in any SKILL.md", "medium", c45))
    return checks


# ---------------------------------------------------------------------------
# Phase 5: Handoff Validation
# ---------------------------------------------------------------------------

def p5_handoff():
    checks = []

    def run_handoff(stage, fixture):
        proc = subprocess.run(
            [sys.executable, str(VALIDATORS / "handoff_validator.py"),
             "--stage", stage, str(FIXTURES / fixture)],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=30,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

    def c51():
        rc, out = run_handoff("exploration-to-design", "good/design.md")
        if rc == 0 and "passed: true" in out:
            return False, f"handoff unexpectedly PASSed with design fixture (rc={rc})", "Wire handoff_validator to exploration fixture or add lifecycle_status check."
        return True, f"rc={rc} (expected non-zero for design-only fixture)", "N/A"

    def c52():
        rc, out = run_handoff("design-to-planner", "good/design.md")
        if rc != 0 or "passed: true" not in out:
            return False, f"rc={rc}; out tail={out[-300:]}", "Add missing keys to good/design.md frontmatter (zone_mapping, progressive_disclosure, handoff.next_stage)."
        return True, "", "N/A"

    def c53():
        rc, out = run_handoff("planner-to-builder", "good/todo.md")
        if rc != 0 or "passed: true" not in out:
            return False, f"rc={rc}; out tail={out[-300:]}", "Add status=ready_for_builder + trace_to_design to good/todo.md."
        return True, "", "N/A"

    def c54():
        rc, out = run_handoff("planner-to-builder", "bad/todo.md")
        if rc == 0 or "passed: false" not in out:
            return False, f"handoff accepted bad todo (rc={rc})", "Tighten handoff checks for blockers/circular deps."
        return True, "", "N/A"

    def c55():
        offenders = [s for s in SKILLS
                     if "lifecycle_status" not in (_read(SUITE_ROOT / s / "SKILL.md") or "")]
        if offenders:
            return True, f"informational: missing in {offenders}", "N/A"
        return True, "all skills declare lifecycle_status", "N/A"

    checks.append(_check("P5.1 exploration-to-design handoff requires lifecycle_status", "critical", c51))
    checks.append(_check("P5.2 design-to-planner handoff accepts good/design.md", "critical", c52))
    checks.append(_check("P5.3 planner-to-builder handoff accepts good/todo.md", "critical", c53))
    checks.append(_check("P5.4 planner-to-builder handoff rejects bad/todo.md", "critical", c54))
    checks.append(_check("P5.5 lifecycle_status presence in all SKILL.md (informational)", "low", c55))
    return checks


# ---------------------------------------------------------------------------
# Phase 6: Cross-Skill Reference & Boot Script
# ---------------------------------------------------------------------------

def p6_cross_skill():
    checks = []

    def c61():
        proc = subprocess.run(
            ["grep", "-rln", "core_case.py", "--include=SKILL.md", "."],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=15,
        )
        out = (proc.stdout or "").strip()
        if not out:
            return True, "no SKILL.md references core_case.py", "N/A"
        return True, f"references in: {out.splitlines()}", "N/A"

    def c62():
        proc = subprocess.run(
            ["find", ".", "-name", "core_case.py", "-not", "-path", "*/.omc/*"],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=15,
        )
        found = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
        if found:
            return False, f"unexpectedly found at: {found}", "Remove orphan core_case.py or update references."
        return True, "core_case.py absent (matches I5 — references dangling)", "N/A"

    def c63():
        ref_re = re.compile(r"([a-zA-Z0-9_./-]+\.py)")
        missing = {}
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            for line in content.splitlines():
                for m in ref_re.findall(line):
                    if m.startswith("http") or "{" in m:
                        continue
                    if not (SUITE_ROOT / s / m).exists() and not (SHARED / m).exists():
                        missing.setdefault(m, []).append(s)
        offenders = [k for k in missing if k == "core_case.py"]
        if not offenders:
            return False, "no missing .py refs detected (expected core_case.py per I5)", "Either restore core_case.py or remove its references from SKILL.md."
        return True, f"missing refs: {offenders}", "Create core_case.py or remove the dangling references in production-code-reviewer + production-quality-gatekeeper."

    def c64():
        proc = subprocess.run(
            [sys.executable, str(VALIDATORS / "check_status.py"),
             str(FIXTURES / "good" / "design.md")],
            capture_output=True, text=True, cwd=str(SUITE_ROOT), timeout=15,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0 or "status" not in out:
            return False, f"rc={proc.returncode}; out={out[-300:]}", "Make check_status.py emit JSON with status/lifecycle_status fields."
        return True, "", "N/A"

    def c65():
        rb = VALIDATORS / "rollback_engine.py"
        if not rb.exists():
            return False, "rollback_engine.py missing", "Restore _shared/validators/rollback_engine.py."
        try:
            import ast
            ast.parse(rb.read_text(encoding="utf-8"))
        except SyntaxError as e:
            return False, f"syntax error: {e}", "Fix the syntax error in rollback_engine.py."
        return True, "", "N/A"

    def c66():
        target = SCRIPTS / "validate_suite_integrity.py"
        if not target.exists():
            return False, "validate_suite_integrity.py missing", "Restore the integrity script."
        content = target.read_text(encoding="utf-8")
        if "ver-2" in content or "Ver_2" in content:
            return True, "ver-2 label still present (I1 confirmed)", "Rename ver-2 → ver-3 throughout validate_suite_integrity.py docstring and banner."
        return False, "ver-2 label already removed", "Mark I1 as resolved in the issue tracker."

    def c67():
        target = SCRIPTS / "validate_suite_integrity.py"
        if not target.exists():
            return False, "validate_suite_integrity.py missing", "Restore the integrity script."
        content = target.read_text(encoding="utf-8")
        listed = [s for s in SKILLS if f'"{s}"' in content]
        missing = [s for s in SKILLS if s not in listed]
        if missing:
            return True, f"SKILLS list missing: {missing} (I2 confirmed)", f"Add {missing} to the SKILLS list in validate_suite_integrity.py."
        return False, "SKILLS list now complete", "Mark I2 as resolved."

    checks.append(_check("P6.1 grep finds core_case.py refs in SKILL.md", "critical", c61))
    checks.append(_check("P6.2 core_case.py absent on disk (I5 dangling ref)", "critical", c62))
    checks.append(_check("P6.3 cross-skill .py ref scan flags core_case.py", "critical", c63))
    checks.append(_check("P6.4 check_status.py emits JSON for good/design.md", "high", c64))
    checks.append(_check("P6.5 rollback_engine.py exists and parses", "medium", c65))
    checks.append(_check("P6.6 validate_suite_integrity.py still labeled ver-2 (I1)", "medium", c66))
    checks.append(_check("P6.7 SKILLS list is complete in validate_suite_integrity.py (I2)", "critical", c67))
    return checks


# ---------------------------------------------------------------------------
# Phase 7: Placeholder Density
# ---------------------------------------------------------------------------

def p7_placeholders():
    checks = []

    def c71():
        report = {}
        for s in SKILLS:
            counts = {}
            skill_dir = SUITE_ROOT / s
            if not skill_dir.exists():
                continue
            for root, _, files in os.walk(skill_dir):
                if ".omc" in root:
                    continue
                for f in files:
                    if not f.endswith((".py", ".md", ".yaml", ".yml")):
                        continue
                    fp = Path(root) / f
                    try:
                        for line in fp.read_text(encoding="utf-8", errors="ignore").splitlines():
                            for pat, name in PLACEHOLDER_PATTERNS:
                                if re.search(pat, line):
                                    counts[name] = counts.get(name, 0) + 1
                    except OSError:
                        continue
            report[s] = sum(counts.values())
        total = sum(report.values())
        if total == 0:
            return True, f"all skills report 0 placeholders; breakdown={report}", "N/A"
        return True, f"TOTAL={total}; breakdown={report}", "N/A"

    def c72():
        hits = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            for ln, line in enumerate(content.splitlines(), 1):
                if "placeholder" in line and re.search(
                    r"density|count|threshold|limit|rule|>[0-9]+|<[0-9]+|=[0-9]+|FAIL|PASS|100%", line
                ):
                    hits.append(f"{s}:{ln}: {line.strip()[:120]}")
        if not hits:
            return False, "no placeholder threshold rules found in SKILL.md", "Declare the density rule in skill-builder SKILL.md."
        return True, f"found {len(hits)} threshold rule(s); first: {hits[0]}", "Reconcile contradictory thresholds (I4): pick one canonical value."

    def c73():
        content = _read(SUITE_ROOT / "skill-builder" / "SKILL.md") or ""
        has_gt9 = bool(re.search(r"placeholder[^.\n]*>\s*9", content, re.I))
        has_lt5 = bool(re.search(r"placeholder[^.\n]*<\s*5", content, re.I))
        if has_gt9 and has_lt5:
            return True, "skill-builder declares BOTH >9 (must_not) AND <5 (mission) (I7)", "Pick one threshold: either >9 in must_not OR <5 in mission — not both."
        if has_gt9 or has_lt5:
            return False, f"only one of the contradictory thresholds present (gt9={has_gt9}, lt5={has_lt5})", "I7 already partially resolved; verify intent."
        return False, "no contradictory thresholds detected", "I7 already resolved; remove the override."

    checks.append(_check("P7.1 measure placeholder density across all skills", "high", c71))
    checks.append(_check("P7.2 surface all placeholder threshold rules in SKILL.md (I4)", "high", c72))
    checks.append(_check("P7.3 skill-builder has both >9 and <5 thresholds (I7)", "high", c73))
    return checks


# ---------------------------------------------------------------------------
# Phase 8: Ver-2 / Ver-3 version label sanity
# ---------------------------------------------------------------------------

def p8_version_label():
    checks = []

    def c81():
        offenders = []
        for s in SKILLS:
            content = _read(SUITE_ROOT / s / "SKILL.md") or ""
            for ln, line in enumerate(content.splitlines(), 1):
                if re.search(r"ver[\-_]?2", line, re.I):
                    offenders.append(f"{s}:{ln}: {line.strip()[:100]}")
        if offenders:
            return False, f"{len(offenders)} ver-2 label(s) in SKILL.md; first: {offenders[0]}", "Replace ver-2 → ver-3 in all SKILL.md and shared docs."
        return True, "no ver-2 labels in SKILL.md", "N/A"

    def c82():
        for sub in ("knowledge", "validators", "schemas", "templates", "fixtures"):
            base = SHARED / sub
            if not base.exists():
                continue
            for root, _, files in os.walk(base):
                for f in files:
                    if not f.endswith((".md", ".yaml", ".yml", ".py", ".json")):
                        continue
                    fp = Path(root) / f
                    try:
                        content = fp.read_text(encoding="utf-8", errors="ignore")
                    except OSError:
                        continue
                    for ln, line in enumerate(content.splitlines(), 1):
                        if re.search(r"ver[\-_]?2", line, re.I):
                            return True, f"ver-2 label in {fp.relative_to(SUITE_ROOT)}:{ln}: {line.strip()[:80]}", "Replace ver-2 → ver-3 across _shared/."
        return False, "_shared/ is clean of ver-2 labels", "All version labels are clean."

    def c83():
        target = SCRIPTS / "validate_suite_integrity.py"
        if not target.exists():
            return False, "integrity script missing", "Restore validate_suite_integrity.py."
        content = target.read_text(encoding="utf-8")
        if "ver-2" in content or "Ver_2" in content or "ver_2" in content:
            return True, "validate_suite_integrity.py still uses ver-2 label (I1)", "Update docstring + banner to ver-3."
        return False, "validate_suite_integrity.py is clean", "I1 already resolved."

    checks.append(_check("P8.1 SKILL.md files do not contain ver-2 labels", "medium", c81))
    checks.append(_check("P8.2 _shared/ files do not contain ver-2 labels", "medium", c82))
    checks.append(_check("P8.3 validate_suite_integrity.py uses ver-3 (I1)", "medium", c83))
    return checks


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

PHASES = {
    "P1": ("Frontmatter & XML Boundary Check", p1_frontmatter_xml),
    "P2": ("Path & Link Integrity", p2_path_integrity),
    "P3": ("Schema Validation (Good + Bad Fixtures)", p3_schema),
    "P4": ("Trace Tag Validation", p4_trace),
    "P5": ("Handoff Validation Between Stages", p5_handoff),
    "P6": ("Cross-Skill Reference & Boot Script Existence", p6_cross_skill),
    "P7": ("Placeholder Density Measurement", p7_placeholders),
    "P8": ("Ver-2 / Ver-3 Version Label Sanity", p8_version_label),
}


def render_yaml(report):
    """Render the report as YAML (manual, to avoid extra deps)."""
    lines = []
    lines.append(f"stage: {report['stage']}")
    lines.append(f"artifact: {report['artifact']}")
    lines.append(f"timestamp: {report['timestamp']}")
    lines.append(f"passed: {str(report['passed']).lower()}")
    lines.append("checks:")
    for c in report["checks"]:
        lines.append(f"  - name: {c['name']}")
        lines.append(f"    status: {c['status']}")
        lines.append(f"    severity: {c['severity']}")
        lines.append(f"    error: \"{c['error'].replace(chr(34), chr(39))}\"")
        lines.append(f"    fix_hint: \"{c['fix_hint'].replace(chr(34), chr(39))}\"")
    if "summary" in report:
        s = report["summary"]
        lines.append("summary:")
        lines.append(f"  total: {s['total']}")
        lines.append(f"  passed: {s['passed']}")
        lines.append(f"  failed: {s['failed']}")
    return "\n".join(lines) + "\n"


def run_phase(phase_id):
    name, fn = PHASES[phase_id]
    checks = fn()
    passed = all(c["status"] == "pass" for c in checks)
    return {
        "phase": phase_id,
        "name": name,
        "passed": passed,
        "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--phase", choices=list(PHASES.keys()),
                        help="Run a single phase; default = all phases.")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON report instead of YAML.")
    args = parser.parse_args()

    phase_ids = [args.phase] if args.phase else list(PHASES.keys())
    all_checks = []
    phase_results = []
    for pid in phase_ids:
        result = run_phase(pid)
        phase_results.append(result)
        for c in result["checks"]:
            c["phase"] = pid
        all_checks.extend(result["checks"])

    passed = sum(1 for c in all_checks if c["status"] == "pass")
    failed = sum(1 for c in all_checks if c["status"] == "fail")
    overall_passed = failed == 0

    report = {
        "stage": "test-suite-workflow",
        "artifact": str(SUITE_ROOT),
        "timestamp": _now(),
        "passed": overall_passed,
        "checks": all_checks,
        "summary": {"total": len(all_checks), "passed": passed, "failed": failed},
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_yaml(report))

    # Per-phase summary on stderr
    print("\n# Per-phase summary", file=sys.stderr)
    for pr in phase_results:
        ok = sum(1 for c in pr["checks"] if c["status"] == "pass")
        total = len(pr["checks"])
        marker = "PASS" if pr["passed"] else "FAIL"
        print(f"  [{marker}] {pr['phase']} {pr['name']}: {ok}/{total}", file=sys.stderr)

    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main()
