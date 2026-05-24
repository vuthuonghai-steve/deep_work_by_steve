# K-Chains Lens — 8 Analytical Lenses

## Overview

Heavy Thinking uses K=8 parallel reasoning chains, each exploring the problem from a distinct analytical lens. This document defines each lens in detail.

---

## Chain 1: Context & State

**Lens Focus**: Input context sufficiency, cached vs fresh knowledge

### Questions to Explore
- What context was provided vs what is assumed?
- Is the context current or stale?
- What's the gap between available context and required context?
- What context would improve understanding?

### Chain Output Format
```
⚡ Chain 1: CONTEXT & STATE
[SOURCE]: {memory|session|project|user-prompt}
[FRESHNESS]: {current|stale|unknown}
[GAP]: What context is missing?
[ENRICHMENT]: What additional context needed?
[ROOT ISSUE]: Core context deficiency (if any)
```

### Specific Analysis Triggers
- `fix bug` → Check: Is the bug reproducible with given context?
- `build feature` → Check: Is the feature scope clear with given context?
- `ideation` → Check: Is the problem domain fully defined?
- `spec` → Check: Are all entities and relationships specified?

---

## Chain 2: Handoff & Contract

**Lens Focus**: Session/agent/skill boundaries, information flow

### Questions to Explore
- How does information transfer between boundaries?
- What's the implicit contract between sender and receiver?
- Where does information degrade or get lost?
- Are expectations aligned on both sides of the handoff?

### Chain Output Format
```
⚡ Chain 2: HANDOFF & CONTRACT
[BOUNDARY]: {user→agent|agent→skill|skill→skill|session→session}
[CONTRACT]: What is expected from each side?
[DEGRADATION]: Where does info lose fidelity?
[RISK]: Potential handoff failure modes
[IMPROVEMENT]: How to strengthen handoff
```

### Specific Analysis Triggers
- `fix bug` → Check: Did previous handoff miss critical info?
- `build feature` → Check: Are API contracts clearly defined?
- `ideation` → Check: Is the user's intent correctly understood?

---

## Chain 3: Error Handling

**Lens Focus**: Hallucination, silent failure, confidence/competence gap

### Questions to Explore
- Where might the LLM hallucinate or assume?
- What failures could happen silently?
- Is the confidence level appropriate for the competence level?
- What verification is needed to catch errors?

### Chain Output Format
```
⚡ Chain 3: ERROR HANDLING
[HALLUCINATION RISK]: Areas prone to fabrication
[SILENT FAILURES]: Errors that won't surface immediately
[CONFIDENCE GAP]: Where confidence > competence
[VERIFICATION NEEDED]: What to check before proceeding
[MITIGATION]: How to prevent error propagation
```

### Specific Analysis Triggers
- `fix bug` → Check: Could the "fix" introduce new bugs?
- `build feature` → Check: Are edge cases handled or assumed away?
- `ideation` → Check: Are ideas grounded in reality or speculation?

---

## Chain 4: Propagation

**Lens Focus**: Codebase impact, side effects, dependency chains

### Questions to Explore
- What other parts of the system will this change affect?
- Are there shared dependencies or state mutations?
- What's the blast radius of this change?
- Are there implicit contracts being violated?

### Chain Output Format
```
⚡ Chain 4: PROPAGATION
[AFFECTED COMPONENTS]: List of impacted areas
[SHARED DEPENDENCIES]: Common dependencies at risk
[BLAST RADIUS]: How far will changes propagate?
[CONTRACT VIOLATIONS]: Implicit contracts being broken
[ISOLATION]: How to contain changes
```

### Specific Analysis Triggers
- `fix bug` → Check: Is the bug a symptom of a systemic issue?
- `build feature` → Check: Does this feature depend on unstable components?
- `spec` → Check: Are all side effects documented?

---

## Chain 5: Quality Assurance

**Lens Focus**: Verification, diff analysis, objective metrics

### Questions to Explore
- How do we verify the output is correct?
- What are the acceptance criteria?
- What's the diff between current state and desired state?
- How do we measure quality objectively?

### Chain Output Format
```
⚡ Chain 5: QUALITY ASSURANCE
[ACCEPTANCE CRITERIA]: What defines success?
[VERIFICATION METHOD]: How to verify each criterion
[DIFF ANALYSIS]: Current state vs desired state
[TESTABILITY]: Can this be automatically tested?
[QUALITY METRICS]: Objective measures of success
```

### Specific Analysis Triggers
- `fix bug` → Check: What tests would catch regression?
- `build feature` → Check: What are the success metrics?
- `ideation` → Check: How do we evaluate idea quality?

---

## Chain 6: Risk Assessment

**Lens Focus**: What could go wrong, failure modes

### Questions to Explore
- What's the worst case scenario?
- What assumptions are we making that could be wrong?
- What's the cost of being wrong?
- How do we mitigate identified risks?

### Chain Output Format
```
⚡ Chain 6: RISK ASSESSMENT
[WORST CASE]: Maximum damage scenario
[WRONG ASSUMPTIONS]: List of potential false assumptions
[COST OF FAILURE]: Impact if wrong
[PROBABILITY]: Likelihood of each risk
[MITIGATION STRATEGY]: How to reduce risk
```

### Specific Analysis Triggers
- `fix bug` → Check: Could the fix make things worse?
- `build feature` → Check: Is the feature worth the implementation cost?
- `ideation` → Check: Is this idea worth pursuing?

---

## Chain 7: Alternative Paths

**Lens Focus**: Other valid approaches, trade-offs

### Questions to Explore
- What are the alternative solutions?
- What are the trade-offs of each approach?
- Why is this approach better/worse than alternatives?
- What can we learn from rejected alternatives?

### Chain Output Format
```
⚡ Chain 7: ALTERNATIVE PATHS
[ALTERNATIVE A]: Description + trade-offs
[ALTERNATIVE B]: Description + trade-offs
[ALTERNATIVE C]: Description + trade-offs
[CHOSEN PATH]: Why this approach wins
[LESSONS FROM REJECTED]: What alternatives taught us
```

### Specific Analysis Triggers
- `build feature` → Check: Are there simpler implementations?
- `ideation` → Check: Are we optimizing the right problem?
- `spec` → Check: Is this spec solving the root problem?

---

## Chain 8: Dependency Analysis

**Lens Focus**: External dependencies, third-party risks, upstream changes

### Questions to Explore
- What external services or libraries do we depend on?
- Are there upstream changes that could break us?
- What's the reliability track record of dependencies?
- Do we have fallback plans if dependencies fail?

### Chain Output Format
```
⚡ Chain 8: DEPENDENCY ANALYSIS
[EXTERNAL DEPS]: List of external dependencies
[RELIABILITY]: Track record of each dependency
[UPSTREAM RISK]: How upstream changes could impact us
[FALLBACK PLAN]: What if dependency unavailable
[VERSION PINNING]: Which versions are safe
```

### Specific Analysis Triggers
- `fix bug` → Check: Is this bug caused by dependency issue?
- `build feature` → Check: Does feature depend on unstable APIs?
- `spec` → Check: Are all dependencies specified?

---

## Lens Usage Guidelines

### Trigger-Based Lens Augmentation

| Task Type | Extra Lens | Focus |
|-----------|------------|-------|
| `fix bug` | Chain 1 + Root Cause | Bug reproduction context |
| `build feature` | Chain 4 + Impact | Feature scope analysis |
| `ideation` | Chain 7 + Alternatives | Idea validation |
| `spec` | Chain 8 + Dependencies | Complete specification |

### Chain Execution Priority

1. **Always run**: Chains 1-6 (core analysis)
2. **Context-dependent**: Chains 7-8 (added based on task type)
3. **Complexity-based**: More complex = more chains

### Isolation Rules

- Each chain is INDEPENDENT
- Chains do NOT see each other's output
- Only the Deliberator sees all chains
- Contamination = invalid analysis
