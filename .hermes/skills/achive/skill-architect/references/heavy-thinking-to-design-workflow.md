# Heavy Thinking → Skill Architect Workflow

## Pattern

When user wants to deeply analyze a codebase/problem BEFORE creating a skill design, use this meta-workflow:

```
┌─────────────────────────────────────────────────┐
│ STAGE 1: PARALLEL REASONING (K=4-5 chains)       │
│  Each chain = different analytical lens          │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ STAGE 2: DELIBERATION                            │
│  Synthesize → Core Problems → CASE System       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ STAGE 3: DESIGN (via skill-architect)           │
│  Translate CASE into design.md                  │
└─────────────────────────────────────────────────┘
```

## K-Chain Lenses for Codebase Analysis

| Chain | Lens | Questions |
|-------|------|-----------|
| 1 | Context & State | How does it manage state across sessions? |
| 2 | Handoff & Contract | How does info flow between components? |
| 3 | Implicit vs Explicit | What assumptions are made? |
| 4 | Error Handling | What breaks silently? |
| 5 | Quality Metrics | How is quality measured? |

## CASE System (from Heavy Thinking synthesis)

```
PREVENT  → Status-aware boot + explicit PD triggers
DETECT   → Gate validators + reverse trace
RECOVER  → Rollback procedures + checkpoint resume
```

### YAML Frontmatter Pattern for State

```yaml
---
status:
  phase: 1  # 0=Draft, 1=Booted, 2=Gate1, 3=Gate2, 4=Gate3, 5=Complete
  gates_passed: [1]
  confidence: 85
  updated: "2026-05-10T12:00:00Z"
  last_actor: architect
pds:
  tier1:
    files:
      - path: "SKILL.md"
        required_for: [boot]
  tier2:
    files:
      - path: "knowledge/xxx.md"
        triggers: [entering_phase_1]
        required_for: [phase1]
gates:
  gate_1:
    checklist: loop/gate1_checklist.md
    requires: [status.phase >= 0]
```

## When to Use This Pattern

✅ **Use when:**
- User says "analyze X using heavy thinking"
- Problem is complex with multiple failure modes
- Need to understand before designing solution

❌ **Don't use when:**
- Problem is simple/fast (single-shot sufficient)
- User just wants quick implementation
- Requirements already clear

## Anti-Patterns

- K chains all using same lens → no diversity
- Deliberation just voting instead of synthesis
- Jumping to solution without full chain analysis
