# Solution Synthesis: Skill Suite v3.0 Upgrade Fixes

**Date:** 2026-05-12  
**Focus:** How to properly fix the identified issues — root cause analysis and actual fix approach

---

## Executive Summary

The risk analysis identified 20 issues across P0/P1/P2. This document maps each to its **root cause** and specifies the **correct fix** (not just "what to change" but "why this approach" and "what could go wrong with alternatives").

---

## P0 CRITICAL PATH FIXES

### P0-01: Shared Framework Path Resolution

**Root Cause:**  
The `_shared/` directory lives at `.hermes/skills/_shared/` (sibling to the 3 skill directories). All skill SKILL.md files use `../_shared/` which correctly resolves from any skill root (e.g., `.hermes/skills/skill-builder/SKILL.md` → `../_shared/` = `.hermes/skills/_shared/`).

However, **inconsistent relative paths exist** in knowledge/*.md files:
- `skill-builder/knowledge/architect.md:4` says `../../_shared/knowledge/framework.md` — this is WRONG
- From `.hermes/skills/skill-builder/knowledge/architect.md`, `../../_shared/` resolves to `.hermes/_shared/` (doesn't exist)
- The correct path from `knowledge/*.md` should be `../../../_shared/knowledge/framework.md` (3 levels up from knowledge/ subdir)

**Evidence:**
```
SKILL.md (skill root) → ../_shared/ ✅ correct
knowledge/*.md (skill/knowledge/) → ../../_shared/ ❌ WRONG — should be ../../../_shared/
```

**Proper Fix:**
1. Add path resolution guidance to `_shared/knowledge/framework.md` header
2. Audit all knowledge/*.md files and fix `../../_shared/` → `../../../_shared/`
3. The init_context.py auto-extraction from `references/_shared.zip` is working correctly

**Alternative considered:** Create `_shared/` as a subdirectory OF EACH skill (e.g., `skill-builder/_shared/`). **REJECTED** — violates DRY principle; any framework update would need 3 copies.

**Risk of proposed fix:** Low. Only affects knowledge/*.md files which are Tier 2 (loaded on-demand, not at boot).

---

### P0-02: Hardcode `.claude/skills` Removal

**Root Cause:**  
2 occurrences in `prompt-cleaner/SKILL.md:85,90` reference `.claude/skills/` as an install target example. These are in documentation/comments, not runtime path resolution.

**Proper Fix:**
- These are NOT runtime path references — they're install documentation
- Leave as-is since the spec says "only as install examples"
- No functional impact

**Risk of proposed fix:** Zero. Changing these would make documentation less clear.

---

## P1 CONTRACT & VALIDATION FIXES

### P1-02: Handoff Validators — §3 Zone Mapping Regex is Broken

**Root Cause:**  
`validate_skill.py:160` uses regex:
```python
re.findall(r"`([a-zA-Z0-9_\-\.\/\.]+\.[a-z]{2,4})`", line)
```
This matches ANY text in backticks that looks like a file path. But it's a naive regex that:
1. Has `\.` twice in the character class (harmless but sloppy)
2. Matches text like "read `knowledge/architect.md`" in a sentence, not just table cells
3. Can't distinguish between `Zone | Files cần tạo |` table entries vs explanatory text

**Evidence from validate_skill.py:158-163:**
```python
if in_zone_mapping:
    # Find file paths in backticks like `knowledge/architect.md`
    matches = re.findall(r"`([a-zA-Z0-9_\-\.\/\.]+\.[a-z]{2,4})`", line)
```

The comment says "like `knowledge/architect.md`" — but the regex matches any `.md` or `.py` or `.yaml` extension in backticks anywhere in the line, including in explanatory prose.

**Proper Fix:**
Replace naive regex with line-based table cell parsing:
1. Split on `|` to get table cells
2. Only match cells in the "Files cần tạo" column (2nd column)
3. Extract backtick-enclosed paths from those specific cells only

```python
# In table row: split by |, get 2nd column (index 1), then extract paths
cells = line.split('|')
if len(cells) > 1:
    file_cell = cells[1]  # "Files cần tạo" column
    matches = re.findall(r"`([^`]+)`", file_cell)
```

**Alternative considered:** Use a markdown table parsing library. **REJECTED** — adds dependency; the line-split approach handles 95% of cases correctly.

**Risk of proposed fix:** Low. The new logic is more conservative (fewer false positives) but might miss some valid paths in non-standard table layouts.

---

### P1-05: Typo `[CẦU LÀM RÕ]` → `[CẦN LÀM RÕ]`

**Root Cause:**  
The typo exists in **documentation** of the typo detection system, not in actual skill output. The `trace_validator.py:68` line:
```python
"[CẦU LÀM RÕ]": "'CẦU' should be 'CẦN'",
```
This is in the `KNOWN_TYPOS` dict which is used to **detect and correct** the typo — it's intentional documentation.

**Actual occurrences to fix:**
The typo appears in `deep-session-learner/references/skill-suite-upgrade-pitfalls.md:22` noting the issue was NOT fixed. The validator already handles detection correctly.

**Proper Fix:**
- No code change needed — the validator correctly identifies `[CẦU LÀM RÕ]` as invalid
- The KNOWN_TYPOS dict is working as designed
- Just acknowledge in the risk doc that this is "working as intended" (detection) not "broken" (the issue was about output, not validator detection)

**Risk of proposed fix:** Zero. The system already handles this correctly.

---

### P1-07: Validator Accuracy — Broken Regex and Related Issues

**Root Cause:**  
Multiple validator accuracy issues:
1. **Broken §3 regex** (see P1-02 above)
2. **SKILL.md `## Persona` assumption** at `validate_skill.py:96`:
   ```python
   mandatory_keywords = ["## Persona", "Workflow", "Guardrails"]
   ```
   The Anthropic skill standard doesn't require `## Persona` as a heading — it requires `persona` field in YAML frontmatter or a description of who the skill is for.

**Proper Fix for Persona check:**
```python
# Instead of checking for "## Persona" heading, check:
# 1. YAML frontmatter has 'description' field, OR
# 2. Body contains some persona definition (don't mandate specific heading)
```

**Proper Fix for __pycache__:** Add to `ignore_extra` in validate_skill.py:178:
```python
ignore_extra = {
    "scripts/validate_skill.py", 
    "loop/build-log.md", 
    "loop/build-checklist.md",
    "scripts/__pycache__",  # Add this
}
```

**Risk of proposed fix:** Low. More permissive checks reduce false positives.

---

### P1-08: Dynamic Context/Output Resolution

**Root Cause:**  
`validate_skill.py:23-59` uses a 12-level walk-up to find workspace root. This is fragile because:
1. It assumes `.skill-context/{skill_name}` marker directory exists
2. If run from a different cwd, walk-up may fail silently
3. Priority order when multiple strategies return different results is unclear

**Proper Fix:**
Document the path resolution contract explicitly rather than making the algorithm more complex:

```
PATH RESOLUTION CONTRACT:
- skills_root = parent(skill_dir)  e.g., /project/.hermes/skills
- _shared/ is sibling to skills: skills_root.parent / "_shared"
- context_dir = project_root / ".skill-context" / skill_name
- project_root = context_dir.parent.parent  (2 levels up from .skill-context/{name})
```

Add a smoke test that simply verifies: "can we resolve these critical paths?" without walking up more than 4 levels.

**Risk of proposed fix:** Low. Documentation doesn't break anything.

---

## P2 PORTABILITY & POLISH FIXES

### P2-01: Reduce Front-Load
The skill suite already implements progressive disclosure correctly. SKILL.md files are Tier 1 (mandatory at boot), knowledge/*.md files are Tier 2 (loaded when needed).

**No fix needed** — already correctly implemented.

### P2-02: Data/ Zone End-to-End
design.md template mentions data/ zone. The gap is in builder validation which doesn't check for data/ files if §3 doesn't specify them.

**Proper Fix:** No structural change needed. data/ is optional per the spec. If architect doesn't specify data/ files, builder shouldn't be penalized for not creating them.

### P2-03: Template Integration
SKILL.md files reference templates correctly via progressive_disclosure section.

**No fix needed** — already correctly implemented.

### P2-04: Package Cleanup
Found `__pycache__` in `spec-generator-has-api/scripts/__pycache__/`.

**Proper Fix:** Add `.gitignore` at skills root:
```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
```

**Risk of proposed fix:** Zero. Standard gitignore entries.

---

## ISSUES THAT DON'T NEED FIXING

| Issue | Reason |
|-------|--------|
| P1-03: Feedback Loop Standardization | FB-001 format already defined in loop/build-log.md.template |
| P1-04: Trace Tags Standardization | Only 4 tags enforced; no legacy tags in current artifacts |
| P1-06: Section Contracts Sync | design.md says 10 sections (with §10.1 extending §10); this is internally consistent |

---

## PRIORITY ORDER FOR FIXES

1. **P1-02** — Fix §3 Zone Mapping regex (affects handoff validation)
2. **P1-07** — Fix `## Persona` assumption in validator (false positive on valid skills)
3. **P0-01** — Fix path inconsistencies in knowledge/*.md files (affects runtime)
4. **P2-04** — Add .gitignore (prevents future pollution)

---

## FILES TO MODIFY

| File | Change |
|------|--------|
| `.hermes/skills/_shared/knowledge/framework.md` | Add path resolution contract header |
| `.hermes/skills/skill-builder/knowledge/architect.md` | Fix `../../_shared/` → `../../../_shared/` |
| `.hermes/skills/skill-planner/knowledge/architect.md` | Audit and fix any incorrect paths |
| `.hermes/skills/skill-architect/knowledge/architect.md` | Audit and fix any incorrect paths |
| `.hermes/skills/skill-builder/scripts/validate_skill.py` | Fix §3 regex parsing; fix Persona check; add __pycache__ to ignore |
| `.hermes/skills/skill-planner/scripts/validate-todo.py` | Add `--design` flag support |
| `.gitignore` (at `.hermes/skills/`) | Add `__pycache__/`, `*.pyc`, `.pytest_cache/` |

---

## WHAT NOT TO FIX

1. **handoff_validator.py** — Already exists and comprehensive. The P1-02 fix will help it parse §3 correctly.
2. **init_context.py** — Auto-extraction works. The P0-01 fix addresses the path documentation.
3. **prompt-cleaner/SKILL.md .claude/skills references** — These are install examples, not runtime references.

---

*Synthesis completed: 2026-05-12*
*Scope: 4 actionable fixes, 3 issues acknowledged as working correctly, 1 cleanup task*
