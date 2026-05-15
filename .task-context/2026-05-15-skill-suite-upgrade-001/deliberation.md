# Deliberation: Skill Suite Upgrade — REFINED

## REFINED CORE Problems (Validated)

| # | CORE Problem | Severity | Evidence |
|---|--------------|----------|----------|
| **C3** | SKILL.md Token Budget 21x Over | **P0** | architect=14810B, planner=12549B, builder=7587B (budget: 700B) |
| **C4a** | `check_status.py` MISSING | **P0** | Directory `.claude/skills/skill-planner/scripts/` doesn't exist |
| **C4b** | `case-system.md` MISSING | **P0** | EXISTS in `skills/rebuild/` but NOT in active path |
| **C1b** | `validate_skill.py` NO trace tag validation | **P1** | Script exists, Zone Mapping works, but NO trace tag check |
| **C5** | `.claude/.hermes` IDENTICAL | **P2** | Same files (hash matches), safe to consolidate |
| **C7** | `architect.md` too thin | **P2** | skill-architect/knowledge=1789B vs peer avg 4466B |

## Root Causes

| # | Root Cause | Prevention |
|---|-----------|------------|
| RC1 | SKILL.md bloat (no token budget enforcement) | Pre-commit hook + split trigger at 700B |
| RC2 | Missing tier1 files (case-system.md, check_status.py) | Promote from rebuild/ or create |
| RC3 | No trace validation in validate_skill.py | Add trace tag check as ERROR level |

## Priority Breakdown

| Priority | Items |
|----------|-------|
| **P0** | SKILL.md split (~700B), case-system.md restore, check_status.py create |
| **P1** | Add trace validation to validate_skill.py |
| **P2** | Consolidate .hermes/ (safe, identical), enrich architect.md |

## Options

| Option | Scope | Effort | Risk |
|--------|-------|--------|------|
| **A: Aggressive Fix** | P0 + P1 | ~2-3h | Low |
| **B: Full Upgrade** | P0 + P1 + P2 | ~4-6h | Medium |
| **C: Minimal** | P0 only | ~1h | Very Low |

## Recommended: Option A

**Rationale**: Addresses all critical blockers. P2 items are nice-to-have but don't break execution.

## CASE Recommendations

| Category | Action |
|----------|--------|
| PREVENT | SKILL.md split: >700B → stub + on-demand |
| PREVENT | case-system.md: promote from rebuild/ |
| PREVENT | check_status.py: create stub or promote from rebuild/ |
| DETECT | Add trace tag check to validate_skill.py (ERROR level) |
| DETECT | Pre-commit: SKILL.md token count check |
| RECOVER | .hermes/ consolidate: safe (identical files) |
