# Chain Isolation Rules — Anti-Contamination Enforcement

## Overview

Chain isolation is CRITICAL for Heavy Thinking validity. If chains contaminate each other, the analysis is invalid. These rules enforce strict separation.

---

## Fundamental Principle

**Each chain is a BLACK BOX:**
- Chains do NOT see each other
- Chains do NOT know what other chains exist
- Chains do NOT receive output from other chains
- Only the Deliberator has visibility into all chains

---

## Isolation Levels

### Level 1: Strict Isolation (Default)

```
Chain 1 ──→ findings ──→ Deliberator
Chain 2 ──→ findings ──→ Deliberator
Chain 3 ──→ findings ──→ Deliberator
...
Chain 8 ──→ findings ──→ Deliberator
```

**Rules:**
- Each chain runs in complete isolation
- No cross-chain communication
- No shared context between chains
- All chains receive same base context only

### Level 2: Moderate Isolation

Used for simpler tasks where some shared state is acceptable.

**Relaxations:**
- All chains can see base context (user prompt, loaded sources)
- Chains still cannot see each other's findings
- Deliberator still sole synthesizer

### Level 3: Hybrid (For Heavy Thinking Manual)

For this skill, we use **Level 1** for K=8 core chains, then **Level 2** for deliberation.

---

## Enforced Rules

### Rule 1: No Cross-Chain Visibility

```
❌ INVALID:
Chain 1: "Based on Chain 3's finding about..."

✅ VALID:
Chain 1: "Based on provided context..."
```

**Enforcement:**
- Prompt templates must NOT include chain-to-chain references
- Chains must ONLY reference base context
- If chain mentions another chain → contamination flagged

### Rule 2: Independent Context Loading

Each chain loads its own copy of context:

```
Chain 1: loads_context() → [context_copy_1]
Chain 2: loads_context() → [context_copy_2]
...
Chain 8: loads_context() → [context_copy_8]
```

**Rules:**
- No shared memory between chains
- No sequential processing
- Each chain starts fresh

### Rule 3: Separate Output Streams

```
Chain 1 output → findings_1.md
Chain 2 output → findings_2.md
...
Chain 8 output → findings_8.md
```

**Rules:**
- No merging until Deliberation stage
- Files stored separately
- Deliberator reads all at once

### Rule 4: Prompt Sanitization

Prompts MUST NOT contain:
- References to other chains
- Hints about expected findings
- "Good" or "bad" chain behaviors
- Consensus or disagreement indicators

---

## Contamination Detection

### Automatic Detection Triggers

| Pattern | Detection | Action |
|---------|-----------|--------|
| "Chain N" reference | Text scan | Flag as contamination |
| "As [other chain] found" | Text scan | Flag as contamination |
| Shared variable state | Memory check | Restart chain |
| Sequential execution | Timestamp check | Flag as violation |

### Manual Review Checklist

- [ ] No chain mentioned by number in another chain's output
- [ ] No findings appear copied between chains
- [ ] Each chain's findings are independently derived
- [ ] Timestamps show parallel execution

---

## Contamination Response

### If Contamination Detected

1. **Flag**: Mark the contaminated chain
2. **Quarantine**: Do not include in deliberation
3. **Regenerate**: Re-run the chain with stricter isolation
4. **Document**: Log the contamination event
5. **Notify**: Inform user of contamination and resolution

### Contamination Log Entry

```yaml
contamination_event:
  timestamp: "2026-05-11T12:00:00Z"
  chain_affected: 3
  type: "cross_chain_reference"
  evidence: "Chain 3 mentioned Chain 1 findings"
  resolution: "Chain 3 regenerated with strict isolation"
  deliberator_notified: true
```

---

## Isolation Enforcement Mechanisms

### For delegate_task Subagents

```python
# Each subagent receives:
{
  "goal": "Analyze [task] from [lens] perspective",
  "context": "[base_context_only]",
  "constraints": {
    "no_cross_reference": true,
    "no_other_chains": true,
    "independent_analysis": true
  }
}
```

### For opencode-go/deepseek-v4-flash

```bash
opencode --model opencode-go/deepseek-v4-flash run "Analyze [task] from [lens] perspective. Context: [base_context_only]. DO NOT reference other analysis chains."
```

### For Inline Reasoning

```python
# Isolation prompt template
prompt = f"""
You are Chain {N} of {K} independent analysis chains.
Your lens: {lens_name}
Task: {task_description}

RULES:
- You CANNOT see other chains
- You CANNOT reference other chains
- You CAN ONLY use the provided context
- Think independently

Context:
{context}

Analyze and provide findings.
"""
```

---

## Chain Execution Order

```
[CONTEXT LOADING]
       ↓
[SPAWN CHAIN 1] ──→ [CHAIN 2] ──→ ... ──→ [CHAIN 8]
       ↓              ↓                       ↓
  [FINDINGS 1]   [FINDINGS 2]          [FINDINGS 8]
       ↓              ↓                       ↓
       └──────────────┼──────────────────────┘
                      ↓
              [DELIBERATION]
```

**Key Points:**
- Chains spawn in parallel (not sequential)
- All chains receive context at same time
- Findings collected before deliberation begins

---

## Quality Metrics

### Isolation Score

```
Isolation Score = (Valid Chains) / (Total Chains) × 100

100% = Perfect isolation
<100% = Contamination detected
```

### Threshold

- ≥90%: Accept with note
- 80-89%: Review required
- <80%: Regenerate contaminated chains

---

## Summary: Chain Isolation Checklist

For each chain execution:

- [ ] Chain receives only base context
- [ ] Chain does not know other chains exist
- [ ] Chain cannot reference other chains
- [ ] Chain output is independent
- [ ] Chain executes in isolation
- [ ] No contamination detected
