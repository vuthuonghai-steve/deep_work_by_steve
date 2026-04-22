# Error Codes — Error Handling & Recovery

> Source: arc-1.md §4.2

---

## Overview

Pipeline runner defines error codes for each failure scenario with recovery strategies.

## Error Codes

| Code | Name | Severity | Recovery |
|------|------|----------|----------|
| E001 | SKILL_NOT_FOUND | HIGH | Select alternative skill or stop |
| E002 | VALIDATION_FAILED | HIGH | Retry, skip, or stop |
| E003 | DEPENDENCY_UNSATISFIED | MEDIUM | Wait or stop |
| E004 | STATE_CORRUPTION | HIGH | Restore from backup or stop |
| E005 | CHECKPOINT_SKIP_ATTEMPT | LOW | Require --force flag |
| E006 | MAX_RETRIES_EXCEEDED | HIGH | Stop pipeline |
| E007 | INVALID_PIPELINE_CONFIG | HIGH | Fix pipeline.yaml |
| E008 | SUBAGENT_TIMEOUT | MEDIUM | Retry or stop |

## Error Handling Flow

```
Stage Execution
    │
    ├── Success → Update queue (COMPLETED)
    │
    └── Failure
        ├── E001: SKILL_NOT_FOUND
        │   └── Ask: Select alternative / Stop
        │
        ├── E002: VALIDATION_FAILED
        │   └── Ask: Retry / Skip / Stop
        │
        ├── E003: DEPENDENCY_UNSATISFIED
        │   └── Wait for dependency / Stop
        │
        └── E006: MAX_RETRIES_EXCEEDED
            └── Stop pipeline, report error
```

## Recovery Strategies

### Retry Logic

```python
MAX_RETRIES = 3

def execute_stage(stage):
    for attempt in range(MAX_RETRIES):
        try:
            result = spawn_subagent(stage)
            if validate(result):
                return SUCCESS
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise MaxRetriesExceededError(e)
    return FAILURE
```

### State Recovery

```python
def recover_state(queue_path):
    # Check for backup
    if exists(queue_path + '.backup'):
        restore(queue_path + '.backup', queue_path)
    else:
        # Start fresh
        create_new_queue(queue_path)
```

### Atomic Write Pattern

```python
def update_queue(queue_path, updates):
    temp_path = queue_path + '.tmp'
    # Write to temp
    write_json(temp_path, updates)
    # Atomic rename
    rename(temp_path, queue_path)
```

## User Interaction Prompts

| Error | Prompt |
|-------|--------|
| E001 | `⚠️ Skill '{skill}' not found. Select alternative or [Stop]` |
| E002 | `❌ Validation failed: {error}. [Retry] / [Skip] / [Stop]` |
| E003 | `⏳ Waiting for dependency: {dep}. Wait or [Stop]` |
| E006 | `🛑 Max retries exceeded. [Stop]` |
