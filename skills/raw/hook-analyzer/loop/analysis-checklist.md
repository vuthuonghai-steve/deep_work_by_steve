# Analysis Checklist — Verification Phase

> **Usage**: Quality verification checklist for hook analysis. Use in Phase 4: Verification.

---

## Pre-Flight Checks

- [ ] All hook files in `.claude/hooks/` have been scanned
- [ ] Each file has at least been read and inspected
- [ ] No files were skipped without justification

---

## Confidence Score Verification

| Check | Threshold | Status |
|-------|-----------|--------|
| Critical issues have confidence ≥ 70% | 70% | [ ] |
| High issues have confidence ≥ 70% | 70% | [ ] |
| Medium issues have confidence ≥ 60% | 60% | [ ] |
| Low issues have confidence ≥ 50% | 50% | [ ] |

### Confidence Score Rules

- **Critical**: Base 90% - 5% if error handling present + 5% if proper shebang
- **High**: Base 80% - 5% if error handling present + 5% if proper shebang
- **Medium**: Base 70% - 10% for uncertain patterns
- **Low**: Base 60% - 10% for heuristics

---

## False Positive Review

### Common False Positives to Watch For

| Pattern | Why It's False Positive | How to Verify |
|---------|------------------------|---------------|
| Unquoted in variable assignment | `var=$value` is safe when not in command context | Check if followed by command |
| `eval` in test conditions | `eval "[[ $a -eq $b ]]"` is safe | Check context |
| Command in subshell in function | Intentional isolation | Verify if cleanup handled |

### False Positive Mitigation

- [ ] Each Critical/High finding has been manually reviewed
- [ ] Findings that are intentional patterns are noted in report
- [ ] Confidence scores adjusted for context-specific cases

---

## Edge Case Coverage

| Edge Case | Covered? | Notes |
|-----------|----------|-------|
| Empty input handling | [ ] | |
| Special characters in paths | [ ] | |
| Signal interruption (Ctrl+C) | [ ] | |
| Permission errors | [ ] | |
| Missing dependencies | [ ] | |
| Timeout handling | [ ] | |

---

## Report Completeness

### Required Sections

- [ ] Executive Summary with health score
- [ ] Severity breakdown table
- [ ] Critical issues detailed
- [ ] High issues detailed
- [ ] Medium issues detailed
- [ ] Low issues detailed
- [ ] Recommendations section
- [ ] File-by-file breakdown

### Content Quality

- [ ] Each finding has line number
- [ ] Each finding has rule ID
- [ ] Each finding has confidence score
- [ ] Code snippets are included (truncated to 100 chars)
- [ ] Recommendations are actionable

---

## Health Score Calculation

```
Health Score = 100 - (Critical × 20) - (High × 10) - (Medium × 5)
```

| Score Range | Status | Action |
|-------------|--------|--------|
| 90-100% | ✅ Healthy | No immediate action |
| 70-89% | ⚠️ Warning | Address High in current sprint |
| 50-69% | 🔶 Attention | Address Critical + High |
| < 50% | 🚨 Critical | Block deployment |

---

## Sign-Off

- [ ] Confidence threshold verified (>70%)
- [ ] Edge cases reviewed
- [ ] False positives filtered
- [ ] Report completeness checked
- [ ] Health score calculated correctly

**Verification Complete**: _______________

**Date**: _______________
