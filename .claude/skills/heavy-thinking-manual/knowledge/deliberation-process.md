# Deliberation Process — Synthesis Methodology

## Overview

Deliberation is Stage 2 of Heavy Thinking. After K=8 chains complete their independent analysis, the Deliberator synthesizes findings into a coherent picture. This document defines the deliberation process.

---

## Deliberation Workflow

```
K=8 CHAINS OUTPUT
       ↓
┌─────────────────────────────────────┐
│ STAGE 1: FINDINGS AGGREGATION       │
│ - List all unique findings           │
│ - Categorize by theme                │
│ - Flag contradictions                │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│ STAGE 2: CONSENSUS IDENTIFICATION    │
│ - Find agreements across chains      │
│ - Weight by chain relevance          │
│ - Identify majority positions        │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│ STAGE 3: CONFLICT RESOLUTION        │
│ - Analyze contradictions            │
│ - Apply logic, not voting           │
│ - Document minority positions        │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│ STAGE 4: SYNTHESIS                  │
│ - Combine partial truths            │
│ - Identify CORE problems            │
│ - Generate CASE recommendations      │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│ STAGE 5: OUTPUT                     │
│ - deliberation.md                   │
│ - prepared-context.json             │
│ - checklist.yaml                   │
└─────────────────────────────────────┘
```

---

## Stage 1: Findings Aggregation

### Input
Each chain outputs findings in this format:

```
⚡ Chain N: [LENS NAME]
[CATEGORY]: [Finding 1]
[CATEGORY]: [Finding 2]
...
[ROOT ISSUE if detected]: ...
```

### Process
1. Collect all findings from K chains
2. Deduplicate by content similarity (>80% = duplicate)
3. Group by category (Context, Handoff, Error, etc.)
4. Flag findings that contradict each other

### Output
```json
{
  "total_findings": 47,
  "unique_findings": 38,
  "deduplicated": 9,
  "by_category": {
    "Context": 8,
    "Handoff": 5,
    "Error": 7,
    "Propagation": 6,
    "Quality": 4,
    "Risk": 5,
    "Alternative": 3,
    "Dependency": 4
  },
  "contradictions": [
    {
      "finding_a": "...",
      "finding_b": "...",
      "chains": [3, 7]
    }
  ]
}
```

---

## Stage 2: Consensus Identification

### Consensus Types

| Type | Definition | Action |
|------|------------|--------|
| **Strong Consensus** | ≥7/8 chains agree | Accept as fact |
| **Moderate Consensus** | 5-6/8 chains agree | Accept with note |
| **Weak Consensus** | 3-4/8 chains agree | Investigate further |
| **No Consensus** | <3 chains | Flag as unresolved |

### Process
1. For each finding category, count chains that raised it
2. Weight by chain relevance (Chain 1 findings weighted higher for Context issues)
3. Identify strong consensus items
4. Note minority positions

### Output
```json
{
  "consensus": {
    "strong": [
      {"finding": "Context is insufficient", "chains": [1,2,3,4,5,6,7,8]}
    ],
    "moderate": [...],
    "weak": [...],
    "none": [...]
  }
}
```

---

## Stage 3: Conflict Resolution

### Resolution Principles

1. **Logic over Voting**: Majority is not always right
2. **Evidence over Authority**: Newer chains don't override older
3. **Specificity over Generality**: More specific finding wins
4. **Mechanism over Symptoms**: Root cause analysis beats symptom description

### Conflict Resolution Algorithm

```
For each contradiction:
1. Identify the specific claim in A vs B
2. Check for hidden assumptions in either
3. Evaluate evidence quality (chain cited sources?)
4. Apply resolution principle
5. Document resolution rationale
```

### If Unresolvable

Document as "Unresolved Conflict" and:
- Present both positions fairly
- Let user decide
- Flag in prepared-context as requiring human judgment

---

## Stage 4: Synthesis

### CORE Problems Identification

From aggregated findings, identify 3-5 CORE problems that explain most of the evidence:

```
CORE Problem = 
  Repeated across multiple chains
  + Root cause of many symptoms
  + Actionable (can be addressed)
```

### CASE System Mapping

```
PREVENT:
  - What context/preparation prevents this problem?
  - What gates stop us from proceeding unsafely?

DETECT:
  - What signals indicate the problem is occurring?
  - What metrics tell us we're at risk?
  
RECOVER:
  - What do we do when problem is detected?
  - What's the rollback/escape plan?
```

### Synthesis Output Format

```markdown
## CORE Problems

### Problem 1: [Name]
**Evidence**: Chains 1, 3, 5 all identified this
**Root Cause**: ...
**PREVENT**: ...
**DETECT**: ...
**RECOVER**: ...

### Problem 2: ...
```

---

## Stage 5: Output

### deliberation.md Structure

```markdown
# Deliberation Results — [Task ID]

## Summary
[2-3 sentence overview]

## Chains Analyzed
- K=8
- Total findings: N
- Unique findings: M

## Consensus Map
[Visual representation of consensus]

## CORE Problems
[3-5 problems with CASE analysis]

## Unresolved Conflicts
[Any contradictions that couldn't be resolved]

## Recommendations
[For implementation]
```

### prepared-context.json Structure

```json
{
  "task_id": "...",
  "problem_statement": "...",
  "core_problems": [...],
  "prevention_gates": [...],
  "detection_signals": [...],
  "recovery_procedures": [...],
  "enriched_context": {...},
  "confidence_level": "high|medium|low",
  "ready_for_implementation": true|false
}
```

### checklist.yaml Structure

```yaml
verification_checklist:
  - id: 1
    item: "Context sufficiency verified"
    status: pass|fail|pending
    evidence: "Memory loaded, Session loaded, Project loaded"
  - id: 2
    item: "Core problems identified"
    status: pass|fail|pending
    evidence: "3 problems identified with chain support"
```

---

## Deliberation Quality Gates

| Gate | Criteria | If Fail |
|------|----------|---------|
| G1 | ≥80% of chains provided findings | Request chain regeneration |
| G2 | No strong contradictions unresolved | Flag for human review |
| G3 | CORE problems identified | Re-run synthesis |
| G4 | All CASE cells filled | Complete before proceeding |

---

## Anti-Patterns

1. **Voting Fallacy**: Just counting chains, not evaluating logic
2. **Confirmation Bias**: Favoring findings that match pre-existing belief
3. **Rush to Synthesis**: Skipping detailed analysis for speed
4. **Over-Synthesis**: Forcing consensus where none exists
