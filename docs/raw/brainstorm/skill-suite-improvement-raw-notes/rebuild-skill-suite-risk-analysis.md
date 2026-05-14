# Risk Analysis: Proposed Fixes for Skill Suite v3.0 Upgrade

**Date:** 2026-05-12
**Focus:** Risks of proposed fixes — what could go wrong if we try to fix these issues?
**Context:** Skill Suite v3.0 upgrade from v2.x (skill-architect, skill-planner, skill-builder in `skills/rebuild/`)

---

## P0 FIXES — CRITICAL PATH

### P0-01: Shared Framework Path Resolution

**Proposed Fix:** Add `_shared/knowledge/framework.md` and update relative paths (`../_shared/` from SKILL.md, `../../_shared/` from knowledge/*.md)

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R1 | **Path resolution chain breaks in edge case** | HIGH | MEDIUM | If any skill's SKILL.md is invoked from a different cwd than expected, `../_shared/` may resolve to wrong location. The 12-level walk-up in `find_workspace_root()` (validate_skill.py:34) suggests path resolution is already fragile. |
| R2 | **Mis-adjusted knowledge/*.md paths** | HIGH | MEDIUM | Knowledge files reference framework.md but if ANY knowledge file is moved or the directory structure changes, `../../_shared/` breaks. This is a one-time fix that becomes stale if files are reorganized. |
| R3 | **init_context.py extraction fails silently** | MEDIUM | LOW | If `references/_shared.zip` is missing or corrupted, init_context.py falls back but may not signal clearly that shared framework is missing. Agent continues with incomplete context. |
| R4 | **No runtime smoke test** | MEDIUM | HIGH | After fixing paths, there's no automated check that confirms "copy to /tmp/ still resolves". The spec says this but no script enforces it. |

**MITIGATIONS:**
- Add a `--dry-run` flag to validators that simply check "can all referenced files be resolved?"
- Document the path resolution contract explicitly: `skills_root = parent(skill-dir)` is the only guaranteed anchor.

---

### P0-02: Hardcode `.claude/skills` Removal

**Proposed Fix:** Replace `@.claude/skills/...` references with relative paths from skill root.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R5 | **Install target examples become stale** | LOW | HIGH | The spec says "only as install examples" but if install target conventions change (e.g., Hermes changes its default path), SKILL.md documentation becomes misleading without a deprecation mechanism. |
| R6 | **Search/replace catches false positives** | MEDIUM | LOW | If someone writes `@.claude/skills` in a comment or as a literal example (not a path reference), a naive replace could corrupt the file. |
| R7 | **Links become ambiguous in multi-skill context** | MEDIUM | LOW | Relative paths from SKILL.md work for single-skill introspection but may break if the skill suite is loaded as a collective unit rather than individual skills. |

**MITIGATIONS:**
- Manual audit with clear scope: only replace in runtime boot instructions and artifact contracts, not in comments or examples.

---

## P1 FIXES — CONTRACT & VALIDATION

### P1-01: Shared Contract vs Skill-Specific Knowledge Separation

**Proposed Fix:** Move shared framework content to `_shared/knowledge/framework.md`, keep only skill-specific in `knowledge/architect.md`.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R8 | **Version drift between copies** | HIGH | MEDIUM | If someone copies `framework.md` to `_shared/` but continues editing the old location (`skills/raw/_shared/`), the two copies diverge. No mechanism enforces single source of truth. |
| R9 | **Architect.md becomes too thin** | LOW | MEDIUM | If architects strip too much content trying to "only keep skill-specific", they may remove content that IS skill-specific but looks "shared". Loss of important workflow details. |
| R10 | **Validation relies on framework being present** | HIGH | LOW | If `framework.md` is missing (failed P0-01), validators that reference it will fail with cryptic errors rather than clear "shared framework missing" messages. |

---

### P1-02: Handoff Validators

**Proposed Fix:** Create `handoff_validator.py`, extend `validate-todo.py` and `validate_skill.py` with `--design` and `--todo` flags.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R11 | **Circular dependency in validators** | HIGH | MEDIUM | If validate_todo.py calls handoff_validator.py, and handoff_validator.py checks todo.md format, and validate_skill.py calls validate_todo.py... cascading failures could cause all three to fail simultaneously with no clear root cause. |
| R12 | **§3 Zone Mapping parser is brittle** | HIGH | HIGH | The regex `r"`([^`]+)`"` in validate_skill.py:161 matches ANY content in backticks. If Architect writes "copy `knowledge/architect.md` to the skill directory" (valid sentence), it gets counted as an expected file. This is ALREADY broken. The proposed fix doesn't address this. |
| R13 | **New validator creates new false positives** | MEDIUM | HIGH | handoff_validator.py will parse §3 with regex. Any deviation in Architect's formatting (extra spaces, different table format) causes spurious failures, blocking the entire pipeline. |
| R14 | **Fixtures may not represent real-world complexity** | MEDIUM | HIGH | The spec says create good/bad fixtures for validators. But real design.md files will have variations (nested tables, multi-line descriptions, escaped backticks) that fixtures won't catch. Validator passes test but fails on real files. |

---

### P1-03: Feedback Loop Standardization

**Proposed Fix:** Standardize FB-001 format in build-log.md, define status enum.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R15 | **Feedback table gets out of sync with status** | LOW | HIGH | If Builder writes a feedback entry but Planner resolves it without updating the Status column (or vice versa), the validator might pass with stale data. No transaction or locking mechanism. |
| R16 | **Status enum proliferation** | LOW | MEDIUM | Six statuses (READY_FOR_BUILD, BLOCKED_BY_DESIGN, etc.) are manageable but if more are added later, validator logic becomes a state machine that's hard to verify. |
| R17 | **Builder stops too eagerly** | MEDIUM | LOW | If "Blocks Build? = yes" triggers immediate stop, but the feedback is actually resolvable by Builder with a workaround, the workflow becomes inefficient. The rule is too strict. |

---

### P1-04: Trace Tags Standardization

**Proposed Fix:** Enforce only 4 tags, fail on legacy tags.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R18 | **Existing legacy tags in archived logs cause validation failures** | LOW | HIGH | If `build-log.md` or `todo.md` files already contain `[GỢI Ý]` or `[TỪ AUDIT]`, the validator will fail them retroactively. Historical artifacts that were valid when created become "invalid". This is a breaking change for any in-progress builds. |
| R19 | **Tag validator regex is too narrow** | MEDIUM | LOW | The check `if tag in trace_tag for tag in self.TRACE_TAGS` (validate-todo.py:108) is substring matching. A tag like `[TỪ DESIGN §1 EXTENDED]` would pass because it contains `[TỪ DESIGN §`. This might be intentional (extensions allowed) or might be a bug. |
| R20 | **No tag deprecation migration path** | MEDIUM | MEDIUM | If an agent encounters a legacy tag in a live todo.md, the spec says "fail/warn" but doesn't say how to migrate. The agent can't proceed and can't fix the tag itself (it's in the Planner's artifact). |

---

### P1-05: Typo Fix `[CẦU LÀM RÕ]` → `[CẦN LÀM RÕ]`

**Proposed Fix:** Find/replace typo in skill-builder/SKILL.md and add validator check.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R21 | **Typo fix is only in skill-builder** | LOW | MEDIUM | The typo appears in BOTH skill-builder/SKILL.md AND skill-builder/knowledge/architect.md (and potentially in raw/). If only skill-builder/SKILL.md is fixed but knowledge/architect.md is not, Builder still scans the wrong file and misses the blocker. |
| R22 | **Validator check is case-sensitive** | LOW | LOW | The typo check might be implemented as exact string match. If someone writes `[CẦN LÀM RÕ]` with different spacing or unicode normalization, it passes validation but doesn't trigger the Builder's scan correctly. |

**Note:** Confirmed typo exists at `skills/rebuild/skill-builder/SKILL.md:102`.

---

### P1-06: Section Contracts Sync

**Proposed Fix:** Confirm design.md = 12 sections, todo.md = 6 sections, sync all references.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R23 | **"12 sections" is itself wrong** | MEDIUM | LOW | The SKILL.md progressive writing contract shows §1, §2, §3, §4, §5, §6, §7, §8, §9, §10 (with §10.1), §11, §12 — that's actually 11 top-level sections (or 12 counting §10.1 separately). If the Architect team can't agree on the count, the spec itself is inconsistent. |
| R24 | **Template and SKILL.md get out of sync again** | HIGH | HIGH | After fixing, new changes to one but not the other will re-introduce the inconsistency. No enforcement mechanism — only the spec documents the correct count. |
| R25 | **Section numbering changes break external references** | MEDIUM | LOW | If §11 and §12 are added or renumbered, any external documentation or scripts referencing these sections will break. |

---

### P1-07: Validator Accuracy

**Proposed Fix:** Fix false positives/negatives — real markdown table parsing, better regex, skip pycache.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R26 | **Changing table parsing introduces new bugs** | HIGH | MEDIUM | The current implementation uses regex on the entire file. Switching to "real markdown table parsing" requires adding a markdown parser library (or implementing one). Any bugs in the new parser affect all validation runs. |
| R27 | **The `## Persona` assumption is never fully documented** | MEDIUM | LOW | The fix says "don't assume ## Persona — check field content". But what IS the correct way to specify persona? If not documented clearly, agents will continue to use ## Persona and validators will be updated to accept it, making the schema more ambiguous. |
| R28 | **`__pycache__` exclusion list grows unbounded** | LOW | MEDIUM | Each new generated directory (`.pytest_cache`, `node_modules`, `.venv`) that should be excluded requires updating the validator. There's no pattern-based exclusion, just a hardcoded list. |

---

### P1-08: Dynamic Context/Output Resolution

**Proposed Fix:** Add `--project-root`, `--context-dir`, `--skills-root` flags to scripts.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R29 | **Three-way path resolution conflict** | HIGH | MEDIUM | If `--project-root`, `--context-dir`, and `--skills-root` are all provided but contradict each other (e.g., context-dir is not under project-root), the script may produce confusing errors or silently use the wrong directory. Priority order is not specified. |
| R30 | **Scripts with new flags break existing automation** | MEDIUM | HIGH | Any existing CI/CD scripts or wrapper tools that call `validate_skill.py` or `validate-todo.py` without the new flags may break if the new flags are required (not optional). |
| R31 | **Skills_root detection is heuristics-based** | MEDIUM | MEDIUM | `parent(current_skill_dir)` works for `skills/rebuild/skill-builder/` but fails for symlinks, network mounts, or unconventional layouts. The "smoke test copy to /tmp/" will pass but real installs with unusual layouts will fail. |

---

## P2 FIXES — PORTABILITY & POLISH

### P2-01: Reduce Front-Load

**Proposed Fix:** Boot only Tier 1 files, progressive load Tier 2/3.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R32 | **Tier classification is subjective** | LOW | MEDIUM | Who decides what's Tier 1 vs Tier 2? If a file needed "at boot" is classified as Tier 2, the agent boots with incomplete context and makes assumptions. The line between "boot critical" and "phase specific" is blurry. |
| R33 | **SKILL.md grows again after being trimmed** | LOW | HIGH | After reducing Tier 1 to under 5 files, contributors may add more files "just in case", bloating boot again. No enforcement mechanism keeps Tier 1 small. |

---

### P2-02: Data/ Zone End-to-End

**Proposed Fix:** Add data/ to init_context.py, design.md.template, Planner tasks, Builder validation.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R34 | **Data/ zone is optional but validator assumes it exists** | MEDIUM | LOW | If design §3 doesn't specify data files but Builder's validator checks for `data/*` expecting files, it may fail valid skills that genuinely don't need data/. The validator needs to handle "no data/ expected" gracefully. |
| R35 | **Schema format for data/ files is unspecified** | MEDIUM | MEDIUM | What format? YAML? JSON? The spec says "data/*.yaml/json" but there's no schema validator for these files. A malformed data/schema.json won't be caught until runtime. |

---

### P2-03: Template Integration

**Proposed Fix:** Every template must have a runtime reference from SKILL.md.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R36 | **Orphan templates get deleted but are referenced** | LOW | LOW | If a template is truly orphaned (no reference) but is actually needed by a future operation type, deleting it loses information. The audit only catches current references, not potential future uses. |
| R37 | **Template content drifts from SKILL.md description** | LOW | MEDIUM | SKILL.md says "read templates/design.md.template when writing design output" but if someone updates the template without updating the description in SKILL.md, the agent follows outdated instructions. |

---

### P2-04: Package Cleanup

**Proposed Fix:** Remove __pycache__, convert stale build-log.md to template, add .gitignore.

**RISKS:**

| # | Risk | Severity | Likelihood | Impact |
|---|------|----------|------------|--------|
| R38 | **`__pycache__` is generated at runtime** | LOW | HIGH | Even if removed from source, running the skills will regenerate `__pycache__`. The fix needs to be "never commit __pycache__" (via .gitignore) rather than just "delete from source". |
| R39 | **Stale build-log.md has historical value** | LOW | LOW | If the build-log.md in loop/ is a real historical log (not a template), converting it to a template loses the record of what was built. Need to distinguish "historical artifact" vs "template for future use". |

---

## CROSS-CUTTING RISKS

These risks span multiple fixes:

| # | Risk | Affects | Severity | Likelihood |
|---|------|---------|----------|------------|
| CR1 | **Fixes are applied inconsistently across the 3 skills** | All P0, P1 | HIGH | HIGH | skill-architect may get fixed but skill-planner doesn't, breaking the pipeline. |
| CR2 | **Validators pass but real execution fails** | P1-02, P1-07 | HIGH | HIGH | All validation passes but when an agent actually runs the skill, path resolution or context loading fails in ways validators don't check. |
| CR3 | **No rollback plan for a failed fix** | All | HIGH | MEDIUM | If a fix breaks an existing working flow (e.g., validator now fails valid files), there's no documented rollback procedure. |
| CR4 | **Fixtures don't represent production complexity** | P1-02, P1-07 | MEDIUM | HIGH | Validator tests with simple fixtures pass but real-world files with complex tables, unicode, nested structures fail silently or with cryptic errors. |
| CR5 | **Dependency chain creates long failure cascades** | P1-02, P1-08 | MEDIUM | MEDIUM | A failure in P1-08 (path resolution) causes P1-02 validators to fail not because design is bad but because paths don't resolve. The error message says "design.md missing §3" when the real issue is "can't find design.md path". |

---

## RISKS THAT COULD CAUSE CATASTROPHIC FAILURE

**Priority 1 — Most Likely to Block the Entire Upgrade:**

1. **R12 — §3 Zone Mapping regex is fundamentally broken**: The current parser adds ANY backtick-enclosed text as an expected file. This means valid Architect output gets flagged as "missing files" or "extra files" depending on how the Architect wrote the sentence. FIXING this (P1-07) requires replacing the regex with a proper markdown table parser, which is non-trivial.

2. **CR2 — Validators pass but execution fails**: The validators check structure but don't check "can this skill actually run when invoked by Hermes/Claude Code?" Path fixes (P0-01) are verified by "copy to /tmp/" but not by actually invoking the skill.

3. **R28 — No enforcement mechanism for synced documents**: After fixing P1-06 (section contracts), nothing prevents them from going out of sync again on the next change. The next iteration of this problem is guaranteed unless a schema enforcement tool is built.

---

## RECOMMENDED RISK MITIGATIONS (PRIORITY ORDER)

1. **Before any fix:** Write a smoke test that actually invokes the skill (not just validates files) — even a simple "does SKILL.md parse without error" would catch P0-01 failures.
2. **P1-02:** Replace regex-based §3 parsing with a real markdown table parser before claiming "handoff validators work". Test with real Architect outputs, not just fixtures.
3. **P1-06:** Pick ONE authoritative source for section counts (templates or SKILL.md, not both) and make the other a generated derivative.
4. **P1-07:** Add a test that runs the validator against the skill-builder's own files (self-validation). If validate_skill.py fails on skill-builder itself, the validator is broken.
5. **All P0/P1:** Add a "known working state" fixture — a complete design.md + todo.md + built skill that passes all validators — to catch regression.

---

*Analysis completed: 2026-05-12*
*Scope: 20 issues across P0 (2), P1 (8), P2 (4), and Cross-cutting (5) risk categories*
