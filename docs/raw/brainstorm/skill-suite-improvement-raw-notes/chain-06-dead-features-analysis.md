# Chain 6: Dead Features & Unused Complexity Analysis

**Analysis Date:** 2026-05-12  
**Scope:** Full workspace audit for bloat and unused artifacts

---

## 1. DUPLICATED / OBSOLETE SKILL COPIES

### 1.1 `achive/` Directory — Full Skill Copies (DEAD)

**Path:** `.hermes/skills/achive/`

```
achive/
├── skill-architect/   (~19KB SKILL.md + knowledge/ + loop/ + scripts/ + templates/)
├── skill-builder/    (~7KB SKILL.md + knowledge/ + loop/ + scripts/)
└── skill-planner/    (~11KB SKILL.md + 30KB source_dump.txt + knowledge/ + loop/ + scripts/ + templates/)
```

**Issue:** This is a full copy of the 3 core skills with `source_dump.txt` (76KB of raw training data). These are completely orphaned — never referenced by any active pipeline, documentation, or handoff. The `achive` name (typo of "archive") and the existence of `source_dump.txt` (raw prompt outputs) suggests this was a migration attempt that was never integrated.

**Verdict:** DEAD — no references found in `hermes.md`, `workspce_tree.md`, any doc, or any skill's `progressive_disclosure` config.

---

### 1.2 `skills/rebuild/_shared/knowledge/framework.md` vs `.hermes/skills/_shared/knowledge/framework.md` — Version Drift

**Path A:** `skills/rebuild/_shared/knowledge/framework.md`  
**Path B:** `.hermes/skills/_shared/knowledge/framework.md`

**Issue:** Two copies of the same framework file at different locations. Path A is in the old `skills/rebuild/` factory area. Path B is in the active `.hermes/skills/` area. Both are `../_shared/` from their respective skill directories, but they can diverge on edits.

**Reference from `docs/skill-suite-llm-execution-analysis.md` line P2-01:** "`../_shared/` path breaks when skill relocated" — the relative path only works at `skills/rebuild/`, not at `.hermes/skills/`.

**Verdict:** BLOAT + FRAGILITY — two copies, version drift risk, path resolution inconsistency.

---

### 1.3 `skills/raw/` — 41 Obsolete Skill Packages

**Path:** `skills/raw/`

41 subdirectories containing raw/legacy skill packages:
- `flutter-*` (4 packages): flutter-architecting-apps, flutter-building-layouts, flutter-managing-state, flutter-ui-converter
- `coding-agent/`, `admin-list-view-builder/`, `api-from-ui/`, `api-integration/`
- `mermaid-diagrams/`, `hook-analyzer/`, `pipeline-runner/`
- `react-best-practices/`, `component-hierarchy-analyzer/`
- ... and 28 more

**Total:** 41 raw skill packages, all with `SKILL.md` files.

**Issue:** These are explicitly documented as "Raw skill imports" / "Nguồn tham khảo/legacy/raw import" per `workspce_tree.md` line 119 and line 203. They are NOT referenced by the active skill suite (Architect→Planner→Builder pipeline) and the `skills.yaml` registry points to `.claude/skills/...` paths, not `skills/raw/...`.

**Additional:** `skills/raw/CLAUDE.md` (140 lines, 6KB) is a documentation file about skill loading mechanisms — it explains Claude Code's progressive disclosure but is NOT itself a skill. It adds no functional value to the workspace.

**Also:** `skills/raw/skills.yaml` (656 lines, 21KB) — old registry with hardcoded `.claude/skills/...` paths. This is a reference/legacy file, not actively used.

**Verdict:** DEAD (41 raw skill packages) + CLUTTER (`CLAUDE.md`, `skills.yaml`).

---

## 2. UNUSED / UNREFERENCED SKILL PACKAGES

### 2.1 `deep-session-learner/` — Unused in Active Pipeline

**Path:** `.hermes/skills/deep-session-learner/`

**Reference in `hermes.md` line 52:** "`deep-session-learner` — extract durable knowledge from the current session into a project knowledge base."

**Issue:** Referenced in documentation as a recommended tool, but:
- No skill in the active `skill-architect → skill-planner → skill-builder` pipeline references it
- No `progressive_disclosure` config in any active skill loads it
- Not listed in `skills.yaml` (which uses `.claude/skills/...` paths)
- Not in the `workspce_tree.md` inventory of active vs archived skills

**Also:** `docs/solution-synthesis-v3-upgrade.md` line 110 references a pitfall note inside `deep-session-learner/references/skill-suite-upgrade-pitfalls.md` — but this is internal documentation of known issues, not a skill feature.

**Verdict:** ORPHANED — documented but not integrated into any active workflow.

---

### 2.2 `spec-generator-has-api/` — Unused in Active Pipeline

**Path:** `.hermes/skills/spec-generator-has-api/`

**Reference in `hermes.md` line 56:** "`spec-generator-has-api` — generate validated feature specs: `api.json`, `business.md`, `flow.md`, `tasks.md`."

**Issue:** Same as `deep-session-learner`:
- Listed in `hermes.md` as a primary skill
- But NOT referenced by any active pipeline stage
- NOT in `skills.yaml`
- NOT referenced in `progressive_disclosure` of `skill-architect`, `skill-planner`, or `skill-builder`

**Also:** `docs/solution-synthesis-v3-upgrade.md` line 196 notes `__pycache__` found in `spec-generator-has-api/scripts/__pycache__/` — Python cache artifacts in a skill directory.

**Verdict:** ORPHANED — documented as primary but never wired into active pipeline.

---

### 2.3 `skills/rebuild/spec-generator/` vs `skills/rebuild/skill-suite-upgrade/` — Duplicate Generators

**Path A:** `skills/rebuild/spec-generator/`  
**Path B:** `skills/rebuild/skill-suite-upgrade/`

**`spec-generator`** (per `skills/rebuild/README.md`): "generate feature specs... `api.json`, `business.md`, `flow.md`, `tasks.md`"

**`skill-suite-upgrade`** (per `skills/rebuild/README.md`): mentioned as part of the rebuild suite but its purpose overlaps with migration/upgrading.

**Issue:** `hermes.md` lists `spec-generator-has-api` (in `.hermes/skills/`) as primary, while `skills/rebuild/spec-generator/` is in the rebuild factory. These serve similar purposes (spec generation) and may be redundant.

**Verdict:** UNCLEAR — overlapping functionality, unclear which is canonical.

---

## 3. PYTHON ARTIFACTS — Cache & Test Bloat

### 3.1 `skills/rebuild/__pycache__/`

**Path:** `skills/rebuild/__pycache__/`  
**Contents:** `.pyc` bytecode files — `conftest.cpython-314.pyc`, `conftest.cpython-314-pytest-9.0.3.pyc`

**Issue:** Python bytecode cache from test runs. Should not be committed. No functional value in the repo.

### 3.2 `skills/rebuild/tests/__pycache__/`

**Path:** `skills/rebuild/tests/__pycache__/`  
**Contents:** More `.pyc` files from pytest runs.

### 3.3 `skills/rebuild/.pytest_cache/`

**Path:** `skills/rebuild/.pytest_cache/`  
**Contents:** pytest's cache directory. Test artifact.

### 3.4 `skills/rebuild/tests/e2e/`, `tests/integration/`, `tests/unit/`

**Path:** `skills/rebuild/tests/` with subdirs  
**Note:** The existence of tests is valid — but `conftest.py` at `skills/rebuild/conftest.py` is 2.7KB and may be test infrastructure for a test suite that runs against skill packages.

**Issue (minor):** `__pycache__` and `.pytest_cache` are git-ignored but still present in the working tree.

**Verdict:** BLOAT (cache artifacts).

---

## 4. VERSION DRIFT IN PATHS — Broken References

### 4.1 `../../_shared/` Path in `.hermes/skills/skill-builder/knowledge/architect.md`

**Reference:** `docs/solution-synthesis-v3-upgrade.md` line 22-23:
```
skill-builder/knowledge/architect.md:4 says ../../_shared/knowledge/framework.md — this is WRONG
From .hermes/skills/skill-builder/knowledge/architect.md, ../../_shared/ resolves to .hermes/_shared/ (doesn't exist)
```

**Issue:** The active `.hermes/skills/skill-builder/knowledge/architect.md` has a broken relative path. The correct path should be `../../_shared/` from `knowledge/` → `skill-builder/` → `.hermes/skills/` → `.hermes/skills/_shared/`. But since `_shared` is a sibling to `skill-*` directories at `.hermes/skills/_shared/`, the path from `knowledge/` would be `../../../_shared/` (4 levels up) or the reference should be absolute.

**Verdict:** BROKEN REFERENCE — the path `../../_shared/` doesn't resolve correctly from inside `.hermes/skills/skill-builder/knowledge/`.

---

## 5. `omc-reference/` — Duplicate Reference Skills

### 5.1 `skills/rebuild/omc-reference/`

**Reference:** Listed in `skills/rebuild/README.md` as part of the suite.

### 5.2 `skills/raw/omc-reference/`

### 5.3 `skills/raw/omc-reference-legacy/`

**Issue:** Three versions or copies of `omc-reference` skill:
- `skills/rebuild/omc-reference/`
- `skills/raw/omc-reference/`
- `skills/raw/omc-reference-legacy/`

**Verdict:** DUPLICATION — at least 2 are redundant.

---

## 6. NAMING CLUTTER

### 6.1 `info_temp/` Directory

**Path:** `info_temp/`  
**Contents:** `temp.md` — likely temporary notes.

**Verdict:** CLUTTER — if not actively used, should be removed or documented.

---

## 7. GIT ARTIFACTS IN WORKDIR

### 7.1 `.omx/` Directory

**Path:** `.omx/`  
**Contents:** State files like `notify-fallback-authority-owner.json`, `team-leader-nudge.json`, and log files.

**Note:** These appear to be system/agent state files. If `.omx` is a known system directory (similar to `.omc`), it may be legitimate. But `notify-fallback-*.json` and `team-leader-nudge.json` look like internal orchestration state that should be in `.gitignore`.

### 7.2 `.claude/` Directory

**Path:** `.claude/`  
**Note:** This is a standard Claude Code directory. Legitimate.

---

## SUMMARY TABLE

| ID | Item | Type | Severity | Action |
|----|------|------|----------|--------|
| D1 | `achive/` directory | DEAD | HIGH | Delete entire directory |
| D2 | `skills/raw/` (41 packages) | DEAD/LEGACY | MEDIUM | Archive or delete; they are raw imports |
| D3 | `skills/raw/CLAUDE.md` | CLUTTER | LOW | Delete (documentation, not a skill) |
| D4 | `skills/raw/skills.yaml` | LEGACY | LOW | Archive separately or delete |
| B1 | Two copies of `framework.md` | BLOAT/DRIFT | HIGH | Consolidate to single source |
| B2 | `__pycache__` / `.pytest_cache` | BLOAT | LOW | Already gitignored; verify cleanup |
| O1 | `deep-session-learner/` | ORPHANED | MEDIUM | Wire into pipeline or remove from docs |
| O2 | `spec-generator-has-api/` | ORPHANED | MEDIUM | Wire into pipeline or remove from docs |
| O3 | `skills/rebuild/spec-generator/` vs `skill-suite-upgrade/` | UNCLEAR | LOW | Clarify canonical spec generator |
| R1 | `../../_shared/` broken path | BROKEN | HIGH | Fix path in skill-builder/knowledge/architect.md |
| R2 | `omc-reference/` ×3 copies | DUPLICATION | MEDIUM | Deduplicate |
| C1 | `info_temp/` | CLUTTER | LOW | Clean or document purpose |

---

## RECOMMENDATIONS

1. **Delete `achive/`** — no references, full of dead skill copies
2. **Consolidate `_shared/knowledge/framework.md`** — single source at `.hermes/skills/_shared/`
3. **Fix broken path** in `.hermes/skills/skill-builder/knowledge/architect.md`
4. **Decide on `deep-session-learner` and `spec-generator-has-api`** — either integrate or remove from `hermes.md`
5. **Archive or delete `skills/raw/`** — 41 raw imports serve as no function in active pipeline
6. **Deduplicate `omc-reference`** — keep one canonical copy
7. **Clean `info_temp/`** — temporary directory that adds noise
