---
# Verification Rules for skill-builder
# Usage: Load before declaring completion (Phase 4 VERIFY)
---

# Verification Rules — Self-Check Before Completion

> **Usage**: Bắt buộc chạy qua trước khi declare skill hoàn thành. Load ở Phase 4 VERIFY.

---

## Rule 1: Zone Contract Integrity

**Check**: Mọi file trong built skill có tên trong design.md §3?

```bash
# For each file in .claude/skills/{skill-name}/:
#   → Verify filename exists in design.md §3 Zone Mapping table
#   → If not found: BLOCK (unless documented rationale in build-log)
```

**Pass**: All files trace to §3
**Fail**: Any file not in §3 without rationale

---

## Rule 2: Fidelity Parity

**Check**: Target file item count ≥ 80% of source file item count?

```
For each Critical resource → knowledge mapping:
  source_count = count items in resource file
  target_count = count items in built knowledge file
  ratio = target_count / source_count
  IF ratio < 0.80: FAIL fidelity check
```

**Pass**: All mappings maintain ≥ 80% parity
**Fail**: Any mapping below 80%

---

## Rule 3: Progressive Disclosure Compliance

**Check**: All Tier 2 files linked from SKILL.md at correct phase?

```
For each Tier 2 file in progressive_disclosure:
  → Verify markdown link exists in SKILL.md
  → Verify link is at correct phase/section (not Boot)
  → If orphan: FAIL PD compliance
```

**Pass**: All Tier 2 files linked at correct phase
**Fail**: Any orphan or misplaced link

---

## Rule 4: Anthropic Standards Compliance

**Check**: SKILL.md meets all Anthropic requirements?

| Criterion | Pass | Fail |
|-----------|------|------|
| YAML frontmatter at line 1 | `---` on line 1 | No frontmatter |
| `name` kebab-case ≤ 64 chars | Valid kebab-case | Invalid format |
| `description` third-person | Starts with verb (Extracts, Builds) | "I can...", "You can..." |
| `description` ≤ 1024 chars | Within limit | Exceeds |
| Body ≤ 500 lines | Within limit | Exceeds |
| Complex workflow has Tracker | Checklist present | Missing |

---

## Rule 5: Source Trace Coverage

**Check**: ≥ 3 random content blocks have source trace tags?

```
Sample 3 content blocks from built files:
  → Check for [TỪ DESIGN §N] or [TỪ RESOURCE: path]
  → If any block has no trace tag: WARN (not FAIL)
```

**Pass**: ≥ 2/3 blocks traced
**Warn**: 1/3 blocks traced
**Fail**: 0/3 blocks traced

---

## Rule 6: Build-Log Completeness

**Check**: build-log.md has all mandatory sections?

- [ ] `## Resource Inventory` — lists all critical files used
- [ ] `## Resource Usage Matrix` — source → output mapping
- [ ] `## Validation Result` — from validate_skill.py
- [ ] `## Confidence Score` — final weighted score

**Pass**: All 4 sections present with content
**Fail**: Any section missing

---

## Rule 7: Confidence Score Threshold

**Check**: Final confidence score ≥ 70?

| Metric | Weight | Calculation |
|--------|--------|-------------|
| Fidelity parity | 30% | avg(ratio) across all mappings |
| Zone Contract | 25% | files_in_§3 / total_files_created |
| PD Compliance | 20% | tier2_linked / total_tier2 |
| Anthropic Standards | 15% | criteria_passed / total_criteria |
| Build-log | 10% | sections_present / 4 |

**Pass**: Score ≥ 70
**Fail**: Score < 70 → fix and re-verify

---

## Execution Order

Run rules in this order (fail-fast):
1. Zone Contract (structural integrity)
2. Anthropic Standards (compliance)
3. PD Compliance (linking)
4. Fidelity Parity (content quality)
5. Source Trace (hallucination check)
6. Build-log Completeness (evidence)
7. Confidence Score (final assessment)

If Rule 1-2 FAIL → fix before continuing to Rule 3-7.
If Rule 3-7 FAIL → fix and re-run from Rule 3.
