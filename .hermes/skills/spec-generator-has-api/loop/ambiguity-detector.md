# Ambiguity Detector — Phase 0 Check

> Run this check BEFORE any generation. If ambiguity found, STOP and ask questions.

---

## Detection Checklist

### 1. Actor Detection

| Check | Question | Ambiguity If |
|-------|----------|--------------|
| A1 | Is there a primary actor performing actions? | No subject mentioned for main action |
| A2 | Are all roles defined (Admin, User, Guest)? | Generic "user" without clarification |
| A3 | Are permission boundaries specified? | "accessible by users" without definition |

**Undefined Actor Patterns**:
- "the system should..." (no actor)
- "users can..." (which users?)
- "it should..." (what is "it"?)
- "someone needs to..." (who?)

### 2. Field Detection

| Check | Question | Ambiguity If |
|-------|----------|--------------|
| F1 | Are all data entities named? | "relevant data" without specification |
| F2 | Are field types specified? | "some fields" without listing |
| F3 | Are required vs optional fields defined? | "data including..." without classification |

**Undefined Field Patterns**:
- "necessary information" (what info?)
- "user data" (which fields?)
- "related entities" (which ones?)

### 3. Auth Detection

| Check | Question | Ambiguity If |
|-------|----------|--------------|
| G1 | Is authentication method specified? | "secure" without method (JWT? Firebase?) |
| G2 | Are access levels defined? | "authorized users" without specifying who |
| G3 | Is there admin-only functionality? | "admin access" without defining admin role |

**Undefined Auth Patterns**:
- "secure access" (how?)
- "proper permissions" (defined how?)
- "logged in users" (which ones?)

### 4. Edge Case Detection

| Check | Question | Ambiguity If |
|-------|----------|--------------|
| E1 | Are error scenarios covered? | "handle errors" without specifying which |
| E2 | Is concurrent access addressed? | "multiple users" without conflict resolution |
| E3 | Are validation failures specified? | "validate input" without rules |

**Undefined Edge Case Patterns**:
- "edge cases" (what cases?)
- "error handling" (which errors?)
- "fail gracefully" (how?)
- "invalid data" (what is valid?)

### 5. Relationship Detection

| Check | Question | Ambiguity If |
|-------|----------|--------------|
| R1 | Are entity relationships defined? | "related to" without specifying how |
| R2 | Is cardinality specified? | "has many" without count |
| R3 | Are foreign key constraints defined? | "linked to" without constraint details |

**Undefined Relationship Patterns**:
- "connected entities" (which?)
- "parent-child relationship" (which is which?)
- "references" (how enforced?)

### 6. Workflow Detection

| Check | Question | Ambiguity If |
|-------|----------|--------------|
| W1 | Is there a clear sequence of actions? | "process" without steps |
| W2 | Are triggers defined for state changes? | "changes state" (to what? when?) |
| W3 | Is the happy path documented? | "works correctly" (what does that mean?) |

**Undefined Workflow Patterns**:
- "workflow" (what steps?)
- "process should..." (what is the process?)
- "before/after" (before/after what?)

---

## Ambiguity Score

Calculate after running all checks:

| Score | Result | Action |
|-------|--------|--------|
| 0-2 | LOW | Proceed to Phase 1 |
| 3-5 | MEDIUM | Ask clarifying questions |
| 6+ | HIGH | STOP, generate Q template |

---

## Output Format

```
## Phase 0 Ambiguity Detection Result

**Score**: X/6 categories flagged

### Detected Ambiguities
| Category | Issue | Question to Ask |
|----------|-------|-----------------|
| Actor | "..." | "..." |

### Decision
[ ] PROCEED — context sufficient
[ ] QUESTIONS — generated N clarifying questions below
[ ] STOP — too ambiguous, cannot proceed
```

---

## When to Ask Questions

Ask immediately when:
- Score is MEDIUM (3-5)
- Any HIGH severity check fails (A1, F1, G1, E1, R1, W1)
- User says "should handle..." without specification

Use `templates/clarity-questions.yaml` to generate the specific questions.
