# Resume Checklist — skill-suite-upgrade

> **Purpose**: Procedure for resuming from a checkpoint after interruption
> **Trigger**: When `check_status.py` returns `phase > 0`

---

## Resume Decision Flow

```
check_status.py output
        │
        ▼
┌───────────────────┐
│ phase = 0?        │
└───────────────────┘
        │
        ▼ Yes → Fresh Start
        │
        No
        │
        ▼
┌───────────────────┐
│ staleness level?   │
└───────────────────┘
        │
    ┌───┼───┐
    │   │   │
  <7d  7-30d  >30d
    │   │       │
    ▼   ▼       ▼
  Normal Warning Force Fresh
```

---

## Resume Procedure

### Step 1: Check Status
```bash
python scripts/check_status.py .skill-context/{skill-name}/design.md
```

Parse output:
- `phase`: Current phase (0-4)
- `gates_passed`: List of passed gates
- `last_actor`: Who last edited
- `updated`: Timestamp
- `staleness`: Age check result

### Step 2: Display Checkpoint Info

Present to user:
```
## Checkpoint Found

**Phase**: {phase}
**Gates Passed**: {gates_passed}
**Last Actor**: {last_actor}
**Last Updated**: {updated}
**Confidence**: {confidence}%

**Resume from**: Gate {phase + 1}
```

### Step 3: Ask User

```
Resume options:
1. Resume từ Phase {phase} — tiếp tục từ checkpoint
2. Bắt đầu mới — reset về Phase 0

Chọn option? [1/2]
```

### Step 4: Conditional Actions

#### If Resume (Option 1):
- [ ] Read design.md §{phase} content
- [ ] Verify content is not corrupted
- [ ] Load Tier 2 files for next phase
- [ ] Proceed from Gate {phase + 1}

#### If Fresh Start (Option 2):
- [ ] Ask for confirmation: "This will discard checkpoint"
- [ ] Reset status block:
  ```yaml
  status:
    phase: 0
    gates_passed: []
    last_actor: architect
    confidence: 0
  ```
- [ ] Proceed from Phase 1

---

## Staleness Handling

### Age < 7 days: Normal
- Resume normally
- No warning needed

### Age 7-30 days: Warning
```
⚠️ Checkpoint is {age} days old

Options:
1. Resume anyway
2. Fresh start
```

### Age > 30 days: Force Fresh
```
🚨 Checkpoint is {age} days old (> 30 days)

Forcing fresh start. All previous work will be archived.

[Confirm] to proceed
```

---

## Rollback Procedure

### Trigger: User rejects gate output or error detected

```
1. Identify target phase (previous gate)
2. Archive current design.md to design.md.backup.{timestamp}
3. Restore from checkpoint if exists
4. Update status block:
   status:
     phase: {target_phase - 1}
     gates_passed: [1, 2, ... up to target-1]
5. Notify user of rollback
```

---

## Resume Complete

After resuming:
- [ ] Tier 2 files loaded for current phase
- [ ] Last checkpoint content visible
- [ ] User confirmed resume position
- [ ] Ready to continue

---

## Exit Criteria

| Criterion | Pass | Fail |
|-----------|------|------|
| Status block readable | ✅ | ❌ |
| User choice recorded | ✅ | ❌ |
| Content integrity verified | ✅ | ❌ |
