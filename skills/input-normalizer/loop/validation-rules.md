# Validation Rules

> **Usage**: Validation rules and error codes. Load when implementing validation logic.

---

## Error Codes Reference

### Critical Errors (E00x)

| Code | Message | Action |
|------|---------|--------|
| E001 | Missing required field: `{field}` | STOP processing this document |
| E002 | Invalid format for field `{field}`. Expected: `{expected}` | STOP processing this document |
| E003 | Invalid enum value for `{field}`. Allowed: `{allowed}` | STOP processing this document |
| E004 | Duplicate ID detected: `{id}` | STOP processing this document |
| E005 | Invalid ID pattern. Expected format: `{format}` | STOP processing this document |

### Warnings (W00x)

| Code | Message | Action |
|------|---------|--------|
| W001 | Optional field missing: `{field}` | Continue with default value |
| W002 | Non-standard format detected for `{field}` | Continue with best-effort parsing |
| W003 | Empty array for field: `{field}` | Continue with empty array |
| W004 | Ambiguous module detected: `{module}` | Continue with inferred value |
| W005 | Missing source file reference | Continue, mark as auto-generated |

### Info Messages (I00x)

| Code | Message | Action |
|------|---------|--------|
| I001 | Field auto-generated: `{field}` | Log only |
| I002 | ID generated from sequence: `{id}` | Log only |
| I003 | Timestamp auto-added: `{timestamp}` | Log only |

---

## Validation Levels

| Level | Exit Code | Description |
|-------|-----------|-------------|
| ERROR | 1 (fatal) | Critical failure - stop processing |
| WARNING | 0 (success) | Non-critical issue - continue but report |
| INFO | 0 (success) | Informational - log only |

---

## Required Field Validation

### Functional Requirement

```python
REQUIRED_FR_FIELDS = [
    "id",
    "title",
    "description",
    "priority",
    "module",
    "source"
]
```

### User Story

```python
REQUIRED_US_FIELDS = [
    "id",
    "title",
    "description",
    "acceptanceCriteria",
    "priority",
    "module",
    "source"
]
```

### Use Case

```python
REQUIRED_UC_FIELDS = [
    "id",
    "name",
    "actor",
    "preconditions",
    "postconditions",
    "flow",
    "module",
    "source"
]
```

---

## Format Validation Rules

### ID Patterns

| Document Type | Pattern | Example |
|--------------|---------|---------|
| FR | `^FR-[a-z0-9]+-\d{3}$` | FR-m1-001 |
| US | `^US-M[1-6]-\d{3}$` | US-M1-001 |
| UC | `^UC-M[1-6]-\d{3}$` | UC-M1-001 |

### Priority Enums

| Document Type | Allowed Values |
|--------------|----------------|
| FR | `critical`, `high`, `medium`, `low` |
| US | `must-have`, `should-have`, `could-have`, `won't-have` |
| UC | N/A (no priority field) |

### Module Values

| Valid Values |
|--------------|
| M1, M2, M3, M4, M5, M6 |

---

## Validation Flow

```
START
  │
  ▼
Check Required Fields
  │
  ├── Missing → E001 → STOP
  │
  ▼
Validate ID Format
  │
  ├── Invalid → E005 → STOP
  │
  ▼
Validate Enums
  │
  ├── Invalid → E003 → STOP
  │
  ▼
Validate Source
  │
  ├── Missing file → W005 → Continue
  │
  ▼
Add Warnings for Optional Fields
  │
  ▼
Generate Report
  │
  ▼
END (Exit 0)
```

---

## Best Practices

1. **Fail Fast**: Stop on critical errors (E00x)
2. **Warn and Continue**: On warnings, add to report and continue
3. **Always Report**: Generate validation report even if all pass
4. **Preserve Original**: Keep source content in `originalContent`
5. **Idempotent**: Same input → same output (deterministic IDs)
