# Analysis Example — Heavy Thinking Manual Output

## Example Task

**User Input**: "fix bug in user authentication login"

**Trigger**: `fix bug`
**Task Type**: bugfix
**Task ID**: `2026-05-11-fix-bug-a1b2c3`

---

## Output: task-meta.yaml

```yaml
task_id: 2026-05-11-fix-bug-a1b2c3
created_at: "2026-05-11T12:00:00Z"
updated_at: "2026-05-11T12:30:00Z"
trigger_keyword: "fix bug"
task_type: bugfix
status: complete
chain_count: 9
chains_executed:
  - chain_id: 1
    lens: Context & State
    status: complete
    findings_count: 4
  - chain_id: 2
    lens: Handoff & Contract
    status: complete
    findings_count: 3
  - chain_id: 3
    lens: Error Handling
    status: complete
    findings_count: 5
  - chain_id: 4
    lens: Propagation
    status: complete
    findings_count: 4
  - chain_id: 5
    lens: Quality Assurance
    status: complete
    findings_count: 3
  - chain_id: 6
    lens: Risk Assessment
    status: complete
    findings_count: 4
  - chain_id: 7
    lens: Alternative Paths
    status: complete
    findings_count: 3
  - chain_id: 8
    lens: Dependency Analysis
    status: complete
    findings_count: 3
  - chain_id: 9
    lens: Root Cause
    status: complete
    findings_count: 5
```

---

## Output: context-sources.json (summary)

```json
{
  "audit_timestamp": "2026-05-11T12:00:00Z",
  "sources": {
    "hermes_memory": {
      "status": "loaded",
      "entries": 12,
      "size_bytes": 2048
    },
    "session_history": {
      "status": "loaded",
      "recent_messages": 15,
      "size_bytes": 4096
    },
    "project_files": {
      "status": "partial",
      "files_loaded": 8,
      "size_bytes": 27648
    }
  },
  "audit_summary": {
    "total_sources": 3,
    "loaded": 2,
    "partial": 1,
    "unavailable": 0
  }
}
```

---

## Output: analysis-chains.md (excerpt)

```
⚡ Chain 1: CONTEXT & STATE
[SOURCE]: project_files, session_history
[FRESHNESS]: current
[GAP]: Login flow spans 3 files but only 1 was loaded
[ENRICHMENT]: Need to load auth/middleware.ts and user/service.ts

⚡ Chain 2: HANDOFF & CONTRACT
[BOUNDARY]: user→agent
[CONTRACT]: User expects fix to work without breaking other auth flows
[DEGRADATION]: Original bug report lacks reproduction steps
[RISK]: Assumptions about JWT token handling may be wrong

⚡ Chain 3: ERROR HANDLING
[HALLUCINATION RISK]: JWT expiry calculation
[SILENT FAILURES]: Token refresh race condition
[CONFIDENCE GAP]: Medium - limited context on token service

... (chains 4-9 omitted for brevity)
```

---

## Output: deliberation.md (excerpt)

```markdown
# Deliberation Results — 2026-05-11-fix-bug-a1b2c3

## Summary
The bug in user authentication login stems from a JWT token expiry 
calculation issue combined with a race condition in token refresh.

## CORE Problems

### Problem 1: JWT Expiry Calculation
**Evidence**: Chains 3, 5, 9
**Root Cause**: Token expiry timestamp calculated incorrectly
**PREVENT**: Add validation for token expiry calculation
**DETECT**: Monitor auth failure rates
**RECOVER**: Force logout and re-authenticate

### Problem 2: Token Refresh Race Condition
**Evidence**: Chains 3, 4
**Root Cause]: Concurrent refresh requests not handled
**PREVENT**: Add request queuing
**DETECT**: Log duplicate refresh attempts
**RECOVER**: Discard stale refresh token

### Problem 3: Incomplete Error Context
**Evidence**: Chains 1, 2
**Root Cause]: Error messages lack specificity
**PREVENT**: Add structured error logging
**DETECT**: Monitor error patterns
**RECOVER**: Add debug mode for troubleshooting
```

---

## Output: prepared-context.json (excerpt)

```json
{
  "task_id": "2026-05-11-fix-bug-a1b2c3",
  "problem_statement": "User authentication login fails intermittently",
  "task_type": "bugfix",
  "core_problems": [
    {
      "id": "CP1",
      "name": "JWT Expiry Calculation",
      "description": "Token expiry timestamp calculated incorrectly causing premature logout",
      "root_cause": "Off-by-one error in expiry calculation",
      "evidence": ["Chains 3, 5, 9"],
      "mitigation": "Add unit test for expiry calculation"
    }
  ],
  "confidence_level": "high",
  "ready_for_implementation": true
}
```

---

## Output: checklist.yaml

```yaml
verification_checklist:
  - id: CONTEXT-1
    category: CONTEXT
    item: Hermes Memory loaded
    status: pass
    evidence: Status = loaded

  - id: CHAINS-1
    category: CHAINS
    item: K=9 chains executed
    status: pass
    evidence: 9 chains with findings

  - id: DELIB-4
    category: DELIBERATION
    item: CORE problems identified
    status: pass
    evidence: 3 problems identified

summary:
  total_items: 30
  passed: 28
  failed: 0
  pending: 2
  pass_rate: 93%
```

---

## Summary for User

```
Task ID: 2026-05-11-fix-bug-a1b2c3
Trigger: fix bug

Context Loaded: 3/3 sources
Chains Executed: K=9 (8 core + 1 bug-specific)
Analysis Time: 15 minutes

CORE Problems Identified: 3
1. JWT Expiry Calculation (chains 3,5,9)
2. Token Refresh Race Condition (chains 3,4)
3. Incomplete Error Context (chains 1,2)

Confidence: HIGH

Analysis ready for implementation. Proceed?
```
