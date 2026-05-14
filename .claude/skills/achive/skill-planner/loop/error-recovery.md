# Error Recovery Procedures

> Usage: Load when errors or hallucinations detected
> Purpose: Guide planner to recover gracefully from failures

---

## Error Detection Triggers

Planner detects errors when:
- Verification loop FAIL
- User rejects todo.md
- Context corruption (file not found, parse error)
- Hallucination detected (claim without source trace)
- Token overflow (context > 80%)
- Confidence score < 50 after asking clarifying questions

---

## Recovery Procedures

### Type 1: Verification FAIL

**Detection**: Self-check in Step VERIFY fails (V1-V6).

**Recovery**:
1. Identify specific failing check from verification output
2. Fix each issue individually
3. Re-run verification loop
4. If unfixable → trigger Type 2 (User Reject rollback)

---

### Type 2: User Reject

**Detection**: User rejects todo.md (partially or fully).

**Recovery**:
1. Identify which section/phase was rejected
2. Rollback to that phase:
   - Phase 0 rejected → Reset prerequisites, re-audit resources
   - Phase 1+ rejected → Reset that phase's tasks, re-analyze
3. If rejection is about scope → offer graceful degradation

---

### Type 3: Context Corruption

**Detection**: File not found, parse error, or missing references.

**Recovery**:
1. Reload Tier 1 files (SKILL.md, architect.md, plan-checklist.md)
2. Skip cache, re-initiate from current phase start
3. If still failing → report to user about corrupted file

---

### Type 4: Hallucination Detected

**Detection**: Claim in todo.md that cannot be traced to design.md or resources.

**Recovery**:
1. Trace claim back to source
2. If source found → update trace tag
3. If source NOT found → remove claim or mark as [CẦN LÀM RÕ]
4. If multiple claims hallucinated → trigger Type 2 (rollback phase)

---

### Type 5: Token Overflow

**Detection**: Context window > 80% or > 95%.

**Recovery**:
1. Drop non-essential Tier 2 files
2. Switch to summary mode for remaining Tier 2
3. Compress: reference instead of inline content
4. If still > 95% → suggest splitting task into smaller skills

---

### Type 6: Low Confidence

**Detection**: Confidence score < 50 after clarifying questions.

**Recovery**:
1. Notify user of low confidence score
2. Present specific weak areas from confidence breakdown
3. Offer alternatives:
   - Collect more information from user
   - Reduce scope (degradation)
   - Split into multiple simpler skills
4. Never deliver todo.md with confidence < 50

---

## Graceful Degradation Levels

When planner cannot produce full plan:

| Level | Output | When to Use |
|-------|--------|-------------|
| 1. Full plan | 6 sections, all zones, all tiers | Normal operation |
| 2. Essential plan | 4 sections (§1, §2, §4, §5), critical zones | Some resources missing |
| 3. Minimal plan | Phase breakdown + prerequisites only | Severe resource gaps |
| 4. Blocked plan | Identify blockers, mark as blocked | Cannot proceed without user input |

---

## Emergency Rollback

**Trigger**: Critical error discovered in delivered todo.md.

**Procedure**:
1. Stop immediately
2. Notify user of error with specific details
3. Identify which phase caused the error
4. Rollback to that phase
5. Re-analyze from that phase start
6. Re-run verification before re-delivering

---

## Error Reporting Format

When reporting errors to user:

```
🚨 [Error Type]
→ Cause: [What triggered this]
→ Impact: [What part of todo.md is affected]
→ Recovery: [What planner will do]
→ Action needed: [What user should provide, if anything]
```
