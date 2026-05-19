# Clean Checklist — Validation for Cleaned Prompts

> **Usage**: Load at Phase 3.3 (Validate) to verify cleaned prompt quality before output.
> **Source**: Derived from design.md §3 Zone Mapping + §8 Risks

---

## Validation Checklist

Run this checklist before delivering any cleaned prompt.

### Item 1: Goal-First Check

```
Does <goal> appear as the FIRST component in the output?
```

- [ ] **PASS**: `<goal>` is first
- [ ] **FAIL**: Something else appears before `<goal>`

### Item 2: Already Structured Check

```
Is the original prompt already well-structured?
```

- [ ] **PASS**: Original prompt was unstructured, cleaning added value
- [ ] **FAIL**: Original was already structured — should return as-is per G2

### Item 3: No Hallucination Check

```
Were any context additions made without source:line citation?
```

- [ ] **PASS**: All context additions have citations
- [ ] **FAIL**: Some additions lack source citation

### Item 4: Format Whitelist Check

```
Is the output format one of: Markdown, YAML, or JSON?
```

- [ ] **PASS**: Format is MD, YAML, or JSON
- [ ] **FAIL**: Format is XML or other prohibited format

### Item 5: Length Budget Check

```
Is cleaned prompt ≤ 3x the original length?
```

- [ ] **PASS**: Cleaned ≤ 3x original
- [ ] **FAIL**: Cleaned > 3x original (over-cleaned)

### Item 6: Complete Components Check

```
Does the output contain all 4 required components?
```

- [ ] **PASS**: All 4 present (Goal, Context, Constraints, OutputFormat)
- [ ] **FAIL**: Missing one or more components

---

## Threshold Rules

| Score | Action |
|-------|--------|
| ≥ 5/6 | **PASS** — Deliver cleaned prompt |
| 3-4/6 | **PARTIAL** — Deliver with improvement notes |
| < 3/6 | **FAIL** — Retry restructure with feedback |

---

## Retry Logic

If validation FAILS (<3/6):

1. Review which checklist items failed
2. Apply specific fixes based on failed items
3. Re-run validation
4. If still failing after 2 retries, escalate to PARTIAL delivery with notes

---

## Examples

### Example: PASS Result

```
Item 1: PASS (goal first)
Item 2: PASS (was unstructured)
Item 3: PASS (all citations present)
Item 4: PASS (Markdown format)
Item 5: PASS (2x original length)
Item 6: PASS (all 4 components)
---
Score: 6/6 — DELIVER
```

### Example: FAIL Result

```
Item 1: FAIL (context before goal)
Item 2: FAIL (already structured)
Item 3: PASS (no additions)
Item 4: PASS (YAML format)
Item 5: PASS (1.5x original)
Item 6: PASS (all components)
---
Score: 4/6 — PARTIAL (deliver with note: goal ordering issue)
```

### Example: RETRY Trigger

```
Item 1: FAIL
Item 2: FAIL
Item 3: FAIL
Item 4: PASS
Item 5: FAIL
Item 6: PASS
---
Score: 2/6 — RETRY required
```
