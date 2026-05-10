# Skill Suite Upgrade — Session Lessons

**Extracted from:** 2026-05-09 skill suite v3.0 upgrade session
**Category:** experience
**Date:** 2026-05-09

---

## Overview

Session corrected prior session's incomplete work on skill suite v3.0 upgrade. Prior session claimed all 9 tasks complete, but P1-05 typo was not fixed and Phase 1 verification was incomplete.

---

## Key Pitfalls Discovered

### P1: Trusting Prior Session Summary Without Verification

**Situation:** Previous session produced a summary claiming all tasks complete. The summary stated "P1-05 already correct — not found" and "Phase 1 verified".

**Problem:** 
- P1-05 typo `[CẦU LÀM RÕ]` was NOT fixed — it existed in `trace_validator.py:12,68`
- Phase 1 verification only checked skill-builder, not all 3 skills

**Lesson learned:**
> ALWAYS verify prior session claims independently. Read the actual files, run the actual commands. Never trust a summary that says "already correct" without checking.

**Action for future sessions:**
- When inheriting work from a prior session, re-verify key claims
- If a task is marked "already correct", still search for the issue to confirm
- Phase 1 requires checking ALL 3 skills (skill-architect, skill-planner, skill-builder)

---

### P2: docs/raw/ Not Read Before Starting

**Situation:** 16 files in `docs/raw/skill-suite-improvement-raw-notes/` were not read or used.

**Problem:**
- Cross-reference analysis revealed conflicts with temp.md
- Missing items in temp.md: testing strategy, migration strategy, state machine design, rollback procedures

**Lesson learned:**
> When upgrading a skill suite, read the raw research/design docs first. They contain the full context that the spec (temp.md) may have summarized or omitted.

---

### P3: Self-Doing Instead of Delegating

**Situation:** Previous session used terminal tool extensively for file edits.

**Problem:** User explicitly wanted "call agent thay vì tự làm tất cả nhé" — delegate to Claude Code/Codex instead of self-doing.

**Lesson learned:**
> For skill suite upgrades, delegate implementation to agents. Use Claude Code for complex file changes, Codex for parallel task execution. Self (terminal/read_file) only for verification and coordination.

---

## Correct Workflow for Skill Suite Upgrades

```
Phase 1: CLARIFY
  - Read temp.md (full spec)
  - Read docs/raw/* (research, design docs)
  - Verify ALL skills, not just one
  - Identify conflicts and missing items

Phase 2: IMPLEMENT (via delegation)
  - Clean prompt for agent
  - delegate_task to Claude Code/Codex
  - Wait for completion before next task

Phase 3: VERIFY
  - Run verification commands
  - Compare git diff (before/after)
  - Report results

Phase 4: COMMIT (only after verify passes)
```

---

## Git Commit Pattern

```bash
git add <file> && git commit -m "fix: P1-05 - fix typo in trace_validator.py"
```

---

## Related

- docs/raw/skill-suite-improvement-raw-notes/
- info_temp/temp.md
- skills/rebuild/_shared/validators/trace_validator.py
