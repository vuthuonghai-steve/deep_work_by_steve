# Chain Isolation Enforcer — Anti-Contamination Rules

## Purpose

This document enforces strict chain isolation for Heavy Thinking K=8 parallel reasoning. Violations = invalid analysis.

---

## Isolation Rules (CRITICAL)

### Rule 1: No Cross-Chain Visibility

**RULE**: Each chain MUST NOT know about other chains.

```
❌ INVALID:
- "Based on Chain 3's finding..."
- "As we saw in Chain 7..."
- "Chain 2 correctly identified..."

✅ VALID:
- "Based on provided context..."
- "From the analysis..."
- "The data suggests..."
```

### Rule 2: No Shared Context

**RULE**: Each chain loads its own copy of context. No shared memory.

```
Chain 1: context_copy_1 = load_context()
Chain 2: context_copy_2 = load_context()
...
Chain 8: context_copy_8 = load_context()
```

### Rule 3: Independent Output Streams

**RULE**: Chain output stored separately until Deliberation.

```
Chain 1 → findings_1.md (not visible to others)
Chain 2 → findings_2.md (not visible to others)
...
Chain 8 → findings_8.md (not visible to others)
         ↓
    DELIBERATION (only place chains merge)
```

### Rule 4: Parallel Execution

**RULE**: Chains MUST execute in parallel, not sequential.

```
❌ INVALID (Sequential):
Chain 1 → Chain 2 → Chain 3 → ...

✅ VALID (Parallel):
[Chain 1] ─┐
[Chain 2] ──┼─→ DELIBERATION
...       ──┤
[Chain 8] ─┘
```

---

## Contamination Detection

### Automatic Detection Patterns

| Pattern | Detection Method | Severity |
|---------|-----------------|----------|
| "Chain [N]" reference | Text scan | CRITICAL |
| "As [Chain N] found" | Text scan | CRITICAL |
| "Chain N correctly" | Text scan | CRITICAL |
| Shared variable mutation | Memory check | CRITICAL |
| Sequential timestamps | Log analysis | HIGH |
| Missing parallel markers | Log analysis | HIGH |

### Manual Review Checklist

For each chain output:

- [ ] No mention of "Chain N" by number
- [ ] No reference to other chain findings
- [ ] No "we", "us", "our" referring to other chains
- [ ] Findings are independently derived
- [ ] Timestamp shows parallel execution window

---

## Isolation Enforcement Mechanisms

### For opencode-go

```bash
# Each chain gets isolated prompt
opencode --model opencode-go/deepseek-v4-flash run "
You are an independent analysis chain.
You CANNOT see other chains.
You CANNOT reference other chains.
Focus on: [lens_name]

[Context provided separately]

Analyze independently.
"
```

### For delegate_task

```python
# Each subagent gets isolated constraints
delegate_task(
    goal=f"Analyze task from {lens} perspective",
    context=base_context,  # Only base context, no chain outputs
    constraints={
        "no_cross_reference": True,
        "no_other_chains": True,
        "independent_analysis": True
    }
)
```

### For Inline Reasoning

```python
# Isolation prompt template
prompt = f"""
You are Chain {N} of {K} independent analysis chains.
You are COMPLETELY ISOLATED from other chains.
You do NOT know what other chains exist.
You do NOT know their findings.

Your lens: {lens_name}
Your focus: {lens_focus}

RULES:
- NO references to other chains
- NO "we" or "us" referring to other chains
- ONLY use the provided base context
- Think and analyze INDEPENDENTLY

Context:
{base_context}

Provide your independent analysis.
"""
```

---

## Contamination Response Protocol

### If Contamination Detected

1. **FLAG**: Mark chain as contaminated
   ```
   chain.status = "contaminated"
   chain.contamination_type = "cross_chain_reference"
   ```

2. **QUARANTINE**: Exclude from deliberation
   ```
   deliberation.exclude(chain.id)
   ```

3. **REGENERATE**: Re-run with stricter isolation
   ```
   new_chain = run_chain(chain.lens, isolation_level=2)
   ```

4. **DOCUMENT**: Log event
   ```yaml
   contamination_log:
     - timestamp: "2026-05-11T12:00:00Z"
       chain_id: 3
       type: "cross_chain_reference"
       evidence: "Found 'As Chain 5 identified' in findings"
       action: "Regenerated with strict isolation"
   ```

5. **NOTIFY**: Inform user
   ```
   ⚠️ Contamination detected in Chain 3
   - Type: Cross-chain reference
   - Action: Regenerated with strict isolation
   - Status: Ready for deliberation
   ```

---

## Isolation Verification

### Pre-Deliberation Check

Before starting deliberation, verify:

- [ ] All chains have valid status (complete, not contaminated)
- [ ] No chain mentions other chains
- [ ] Timestamps confirm parallel execution
- [ ] Each chain has independent findings

### Isolation Score Calculation

```
Isolation Score = (Valid Chains / Total Chains) × 100

100% = Perfect isolation
90-99% = Acceptable (note minor issues)
80-89% = Review required
<80% = Regenerate chains
```

---

## Summary

**CHAIN ISOLATION IS NON-NEGOTIABLE**

| Violation | Consequence |
|-----------|-------------|
| Cross-chain reference | Chain quarantined |
| Shared context | Chain regenerated |
| Sequential execution | Analysis invalid |
| Contamination undetected | Quality gate fails |

---

**Remember**: The value of K=8 parallel chains is DIRECTLY PROPORTIONAL to their independence. Contamination destroys analysis validity.
