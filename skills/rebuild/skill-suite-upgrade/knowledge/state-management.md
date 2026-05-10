# State Management — design.md Status Block Protocol

> **Purpose**: Define how status block is written/read from design.md frontmatter

---

## Status Block Schema

```yaml
status:
  phase: 0                    # 0=Draft, 1=Gate1, 2=Gate2, 3=Gate3, 4=Complete
  gates_passed: []            # [1, 2] = gates passed
  last_actor: architect       # architect | planner | builder
  confidence: 85              # 0-100, self-declared
  created: "2026-05-10T00:00:00Z"
  updated: "2026-05-10T12:00:00Z"
```

---

## Phase Definitions

| Phase | Name | Description |
|-------|------|-------------|
| 0 | Draft | Skill just initialized, no gates passed |
| 1 | Gate 1 Passed | Problem Statement confirmed |
| 2 | Gate 2 Passed | Capability Map + Zone Mapping confirmed |
| 3 | Gate 3 Passed | Full design confirmed, ready for Planner |
| 4 | Complete | Skill built and delivered |

---

## Status Transitions

```
Phase 0 ──[Gate 1 OK]──→ Phase 1
Phase 1 ──[Gate 2 OK]──→ Phase 2
Phase 2 ──[Gate 3 OK]──→ Phase 3
Phase 3 ──[Planner done]──→ Phase 4
Phase 4 ──[Builder done]──→ Complete

Any Phase ──[Rollback]──→ Previous phase
```

---

## Status Update Rules

### When to Update

| Event | Action |
|-------|--------|
| After Gate 1 confirmed | phase=1, gates_passed=[1], updated=TIME |
| After Gate 2 confirmed | phase=2, gates_passed=[1,2], updated=TIME |
| After Gate 3 confirmed | phase=3, gates_passed=[1,2,3], updated=TIME |
| Rollback triggered | phase=target_phase, gates_passed=updated |
| Resume from checkpoint | Verify timestamp vs file mtime |

---

## Resume Logic

```python
def determine_start_position(design_path):
    """Called at boot to determine where to resume"""
    
    status = check_status(design_path)
    phase = status['phase']
    
    if phase == 0:
        return "fresh_start"
    
    # Check if checkpoint is stale (> 7 days)
    updated = parse_iso(status['updated'])
    if is_stale(updated, max_days=7):
        return "stale_checkpoint_warning"
    
    return f"resume_phase_{phase}"
```

---

## Staleness Rules

| Condition | Action |
|-----------|--------|
| Checkpoint < 7 days | Resume normally |
| Checkpoint 7-30 days | Show warning, ask user |
| Checkpoint > 30 days | Force fresh start |
| design.md mtime > status.updated | Design was edited externally, refresh status |

---

## Boot Prompt Generation

When resuming, AI should generate:

```
---
## Resume Context

**Last checkpoint**: Phase {phase} - Gate {gates_passed}
**Last actor**: {last_actor}
**Last updated**: {updated}
**Confidence**: {confidence}%

**Resume from**: [Gate {phase} + 1]

[Show §{phase} content for review]
---
```

---

## Status Block in Frontmatter

Full frontmatter template:

```yaml
---
skill_schema_version: "3.0.0"
artifact_type: "design"
skill_name: "{skill_name}"
generated_by: "{generated_by}"
generated_at: "{generated_at}"
stage: "{stage}"
status:
  phase: {phase}
  gates_passed: [{gates}]
  last_actor: "{actor}"
  confidence: {confidence}
  created: "{created}"
  updated: "{updated}"
zone_mapping:
  # ... zone content
---
```
