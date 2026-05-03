# Agent Strength Patterns — AI Optimization Guide

> Usage: Load when designing complex skills or multi-agent coordination
> Purpose: Provide patterns to maximize AI agent effectiveness

---

## Pattern 1: Chain-of-Thought Enforcement

**What**: Mọi design decision phải có reasoning rõ ràng.

**Why**: Giảm hallucination, tăng consistency, giúp review dễ dàng.

**Template**:
```markdown
**Decision**: [What was decided]
**Reasoning**: [Why] — based on which Pillar? Which Risk?
**Alternative Considered**: [What else] — why rejected?
**Confidence**: [0-100] — how sure?
```

---

## Pattern 2: Progressive Verification

**What**: Verify quality ở mỗi checkpoint, không chỉ cuối.

**Why**: Phát hiện lỗi sớm, giảm cost rework.

**Checkpoints**:
1. After Phase 1: Problem statement clear?
2. After Phase 2: Zone mapping complete?
3. After Phase 3: All diagrams present?
4. Pre-delivery: Full verification loop

---

## Pattern 3: Confidence-Driven Execution

**What**: Đo confidence score trước khi proceed.

**Why**: Ngăn chặn low-quality output khi context unclear.

**Scoring Matrix**:
```markdown
| Metric | Weight | Score |
|--------|--------|-------|
| Output clarity | 30% | 0-100 |
| Zone mapping completeness | 25% | 0-100 |
| Risk coverage | 20% | 0-100 |
| Diagram quality | 15% | 0-100 |
| Handoff readiness | 10% | 0-100 |
```

**Actions**:
- >= 70: Proceed normally
- 50-69: Ask clarifying questions
- < 50: Redesign or reduce scope

---

## Pattern 4: Source-First Documentation

**What**: Mọi claim phải trace về source.

**Why**: Ngăn hallucination, tăng credibility.

**Rules**:
- Knowledge file references must cite source file
- Design decisions must reference user requirements
- Risk mitigations must reference best practices

---

## Pattern 5: Graceful Degradation

**What**: Khi gặp lỗi, giảm scope thay vì fail hoàn toàn.

**Why**: Đảm bảo luôn có output hữu ích.

**Degradation Levels**:
1. Full design (14 sections)
2. Essential design (10 core sections)
3. Minimal design (§1, §3, §10 only)
4. Problem statement only (§1)

---

## Pattern 6: Multi-Agent Coordination

**What**: Design skills với awareness về downstream agents.

**Why**: Giảm friction trong handoff.

**Practices**:
- Zone Mapping là contract chính cho Planner
- PD Plan giúp Builder biết files cần đọc
- Risk list giúp Builder setup guardrails
- Verification rules giúp cả 3 agents cùng quality standard

---

## Pattern 7: Persistent Learning

**What**: Ghi lại learnings để cải thiện future sessions.

**Why**: Skill improves over time.

**Mechanism**:
- `progress.txt` records implementation details
- `build-log.md` records Builder feedback
- Architect reads feedback ở session tiếp theo
- Anti-patterns discovered → add to knowledge files
