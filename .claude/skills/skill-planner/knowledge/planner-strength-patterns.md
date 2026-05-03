# Planner Strength Patterns — AI Optimization Guide

> Usage: Load during Step ANALYZE for confidence scoring and CoT enforcement
> Purpose: Patterns to maximize AI agent effectiveness in planning

---

## Pattern 1: Chain-of-Thought Enforcement

**What**: Every planning decision must have explicit reasoning.

**Why**: Reduces hallucination, increases consistency, helps review.

**Template**:
```
**Decision**: [What was decided]
**Reasoning**: [Why] — based on which design.md section? Which risk?
**Alternative Considered**: [What else] — why rejected?
**Confidence**: [0-100] — how sure?
```

**Required at**:
- Step ANALYZE: Tier analysis decisions (Domain audit judgment)
- Step ANALYZE: Priority assignment (Critical/High/Medium/Low)
- Step ANALYZE: Dependency detection (which tasks block which)
- Step VERIFY: Confidence scoring decisions

---

## Pattern 2: Confidence-Driven Execution

**What**: Measure confidence score before proceeding.

**Why**: Prevents low-quality output when context unclear.

**Scoring Matrix**:

| Metric | Weight | Score Range | What It Measures |
|--------|--------|-------------|-----------------|
| Task completeness | 30% | 0-100 | All §3 zones mapped to tasks |
| Trace coverage | 25% | 0-100 | All tasks have valid trace tags |
| Resource readiness | 20% | 0-100 | Critical resources are Rich |
| Dependency accuracy | 15% | 0-100 | DAG valid, logical phase order |
| Handoff readiness | 10% | 0-100 | Builder can start immediately |

**Actions**:
- >= 70: Proceed normally
- 50-69: Ask clarifying questions
- < 50: Redesign or reduce scope

---

## Pattern 3: Source-First Planning

**What**: Every claim must trace to source.

**Why**: Prevents hallucination, ensures plans grounded in design.

**Rules**:
- Tasks must reference design.md section via [TỪ DESIGN §N]
- Resource audit must verify actual file content, not assume
- Priority decisions must reference design.md priorities or risks

**Enforcement**: validate-todo.py treats missing trace tags as ERRORS.

---

## Pattern 4: Progressive Verification

**What**: Verify quality at checkpoints, not just at end.

**Why**: Detects errors early, reduces rework cost.

**Checkpoints**:
1. After Step READ: Resource audit complete?
2. After Step ANALYZE: All zones analyzed? CoT documented?
3. After Step WRITE: Schema valid? Trace tags present?
4. Before delivery: Full verification loop passes?

---

## Pattern 5: Graceful Degradation

**What**: When errors occur, reduce scope rather than fail completely.

**Why**: Ensures always have useful output.

**Degradation Levels**:
1. Full plan (6 sections, all zones, all tiers)
2. Essential plan (4 sections, critical zones only)
3. Minimal plan (Phase breakdown + prerequisites only)
4. Blocked plan (Identify blockers, mark as blocked)

---

## Pattern 6: Multi-Agent Coordination

**What**: Design plans with awareness of downstream agents.

**Why**: Reduces friction in handoff.

**Practices**:
- Zone Mapping tasks are the contract for Builder
- Resource readiness ensures Builder can start immediately
- Dependency graph guides Builder execution order
- Verification rules set shared quality standard

---

## Pattern 7: Persistent Learning

**What**: Record learnings to improve future sessions.

**Why**: Skill improves over time.

**Mechanism**:
- `progress.txt` records planning details and learnings
- Builder feedback via `build-log.md` improves future planning
- Anti-patterns discovered → update knowledge files
