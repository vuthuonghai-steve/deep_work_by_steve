---
# Error Recovery Patterns for skill-builder
# Usage: Load when errors detected or Phase 5 deliver
---

# Error Recovery — Graceful Degradation Patterns

> **Usage**: Hướng dẫn xử lý lỗi cho Builder. Load khi detect error hoặc Phase 5 DELIVER.

---

## Error Classification

| Error Type | Severity | Detection | Recovery |
|-----------|----------|-----------|----------|
| Missing input (design.md, todo.md) | CRITICAL | File not found at expected path | STOP. Notify user. Cannot proceed. |
| Missing resource file | CRITICAL | File referenced in design.md §3 not in resources/ | Log → Notify → STOP. Don't fabricate. |
| Contradictory clarification | HIGH | User answers conflict with design.md | Present contradiction, wait for resolution. |
| File creation failure | HIGH | Permission error, invalid path | Log error, flag as blocker in build-log. |
| validate_skill.py FAIL | MEDIUM | Exit code 1, errors in output | Parse errors, fix files, re-run (max 3). |
| Confidence < 50% | MEDIUM | Weighted score calculation | Report weak areas, ask user guidance. |
| Token overflow (Red) | MEDIUM | Context > 80% | Compress, skip non-essential, continue. |
| Placeholder > 10 | HIGH | Count check | STOP build, fill placeholders before continue. |
| Fidelity parity fail | MEDIUM | Target < 80% source item count | Second Pass to fill missing items. |

---

## Per-Phase Recovery Procedures

### Phase 1: PREPARE

```
IF design.md missing:
  LOG: "CRITICAL: design.md not found at .skill-context/{skill-name}/"
  NOTIFY: AskUserQuestion("design.md is missing. Please run skill-architect first.")
  STOP

IF todo.md missing:
  LOG: "CRITICAL: todo.md not found at .skill-context/{skill-name}/"
  NOTIFY: AskUserQuestion("todo.md is missing. Please run skill-planner first.")
  STOP

IF resources/ empty:
  LOG: "WARNING: No resources found. Builder will work from design.md only."
  CONTINUE with reduced fidelity expectations
```

### Phase 2: CLARIFY

```
IF user provides contradictory answers:
  LOG: "CONTRADICTION detected in user clarification"
  NOTIFY: Present contradiction with options
  WAIT for user resolution

IF user doesn't respond:
  LOG: "No user response after clarification request"
  PROCEED with reasonable assumptions
  LOG assumptions in build-log.md
```

### Phase 3: BUILD

```
IF file creation fails:
  LOG: "ERROR: Cannot create {file_path}: {error_message}"
  MARK as blocker in build-log.md
  CONTINUE with other files
  FLAG blocker in DELIVER

IF resource missing during build:
  LOG: "CRITICAL: Resource {path} referenced in design.md §3 not found"
  NOTIFY: AskUserQuestion("Resource file missing. Cannot proceed.")
  STOP

IF token pressure hits Red:
  COMPRESS completed phase summaries
  SKIP non-essential Tier 2/3
  CONTINUE with reduced context
```

### Phase 4: VERIFY

```
IF validate_skill.py fails:
  PARSE errors from output
  FIX each error in corresponding file
  RE-RUN validate_skill.py
  IF fails 3 times:
    LOG: "Validation failed after 3 attempts"
    NOTIFY: Report remaining errors to user
    STOP

IF confidence < 50%:
  REPORT weak areas with specific metrics
  ASK user: "Fix issues or accept with documented risks?"
  IF user says fix → iterate Phase 3/4
  IF user says accept → document risks in build-log, proceed

IF confidence 50-69%:
  FIX identified issues
  RE-CALCULATE confidence
  ITERATE until ≥ 70% or user intervention
```

### Phase 5: DELIVER

```
IF build-log.md write fails:
  TRY alternate path (stdout or temp file)
  LOG: "WARNING: build-log.md write failed, output to stdout"
  CONTINUE with delivery

IF Resource Usage Matrix incomplete:
  LOG: "WARNING: Some critical resources not traced in matrix"
  FLAG as known limitation in build-log
```

---

## Log-Notify-Stop Protocol

For SYSTEM errors (not content errors):

1. **LOG**: Append full error to build-log.md with timestamp
   ```
   ## Error Log
   - **Time**: {timestamp}
   - **Phase**: {current_phase}
   - **Error**: {error_description}
   - **Action**: STOP
   ```

2. **NOTIFY**: Use AskUserQuestion with context
   ```
   "System error in Phase {N}: {error}. Build halted. {suggestion}"
   ```

3. **STOP**: Halt all tasks. Do NOT continue building on broken foundation.

---

## Rollback Decision Tree

```
Error Detected
├── Is it a SYSTEM error (permission, missing critical file)?
│   └── YES → Log → Notify → STOP
├── Is it a CONTENT error (fidelity, placeholder)?
│   └── YES → Fix → Re-verify (max 3 loops)
├── Is it a QUALITY concern (confidence 50-69%)?
│   └── YES → Fix issues → Re-calculate → Iterate
└── Is it a USER issue (contradiction, no response)?
    └── YES → Record assumptions → Proceed with caution
```
