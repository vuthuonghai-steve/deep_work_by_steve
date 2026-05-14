---
name: heavy-thinking-manual
description: Heavy Thinking Manual — K=8 parallel reasoning chains for pre-implementation analysis. Triggered by: fix bug, build feature, ideation, create spec. Auto-loads context from Hermes Memory, Session History, and Project Files. Outputs structured analysis to .task-context/{task-id}/.
version: "1.0.0"
author: Steve
category: reasoning
tags: [heavy-thinking, multi-chain, analysis, deliberation, pre-implementation]
pipeline:
  stage_order: 1
  input_contract:
    - type: keyword
      triggers: ["fix bug", "sửa lỗi", "bug", "xây dựng tính năng", "build feature", "new feature", "lên ý tưởng", "brainstorm", "ideation", "tạo spec", "create spec", "viết spec"]
  output_contract:
    - type: directory
      path: ".task-context/{task-id}/"
      files: ["task-meta.yaml", "context-sources.json", "analysis-chains.md", "deliberation.md", "prepared-context.json", "diagrams.mmd", "checklist.yaml"]
  dependencies: []
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "knowledge/k-chains-lens.md"
      base: "skill_dir"
    - path: "data/trigger-keywords.yaml"
      base: "skill_dir"
  tier2:
    - path: "knowledge/context-sources.md"
      base: "skill_dir"
      triggers: ["context_loading"]
    - path: "knowledge/deliberation-process.md"
      base: "skill_dir"
      triggers: ["deliberation"]
    - path: "knowledge/chain-isolation-rules.md"
      base: "skill_dir"
      triggers: ["chain_execution"]
    - path: "scripts/load-context.py"
      base: "skill_dir"
      triggers: ["execution"]
    - path: "scripts/spawn-chains.py"
      base: "skill_dir"
      triggers: ["execution"]
    - path: "templates/task-meta.schema.yaml"
      base: "skill_dir"
      triggers: ["output_generation"]
    - path: "templates/checklist.schema.yaml"
      base: "skill_dir"
      triggers: ["output_generation"]
    - path: "loop/chain-isolation-enforcer.md"
      base: "skill_dir"
      triggers: ["chain_execution"]
  tier3:
    - path: "references/examples/analysis-example.md"
      base: "skill_dir"
      triggers: ["reference"]
    - path: "templates/prepared-context.schema.json"
      base: "skill_dir"
      triggers: ["output_verification"]
license: private
metadata:
  hermes:
    tags: [heavy-thinking, multi-chain, analysis, deliberation, pre-implementation]
    related_skills: []
---


---

# Heavy Thinking Manual

## Mission

Apply Heavy Thinking (K=8 parallel reasoning chains) to analyze tasks BEFORE implementation. Ensure context sufficiency, identify core problems, and prepare enriched input for execution.

**Trigger**: Khi user mention keywords như `fix bug`, `build feature`, `lên ý tưởng`, `tạo spec`.

**Goal**: Không nhảy vào implement cho đến khi analysis hoàn thành.

---

## Boot Sequence

1. Đọc `knowledge/k-chains-lens.md` — 8 lens taxonomy
2. Đọc `data/trigger-keywords.yaml` — trigger keywords config
3. Xác định task type từ trigger keyword
4. Proceed to Phase 1

---

## Workflow Phases

### Phase 1: Context Loading

**Mục tiêu**: Load tất cả context sources và audit gaps.

**Thực hiện**:

1. **Load Hermes Memory**
   ```python
   memory(action='list')
   ```
   - User preferences
   - Past session summaries
   - Tool configurations

2. **Load Session History**
   ```python
   session_search(query="", limit=20)
   ```
   - Current conversation
   - Recent commands
   - Pending tasks

3. **Load Project Files**
   - AGENTS.md / CLAUDE.md
   - Relevant source files
   - Configurations

4. **Context Audit**
   - Report loaded sources
   - Flag missing sources
   - Ask user confirmation if critical sources missing

**Output**: `context-sources.json`

---

### Phase 2: Chain Execution (K=8)

**Mục tiêu**: Spawn 8 parallel reasoning chains, each analyzing from different lens.

**Thực hiện**:

1. **Determine Chain Configuration**
   - Default: K=8 chains (1-8)
   - Based on task type, may add extra chains

2. **Spawn Chains** (Primary: opencode-go/deepseek-v4-flash, Fallback: delegate_task)
   
   **Using opencode-go:**
   ```bash
   opencode --model opencode-go/deepseek-v4-flash run "Analyze task from [lens] perspective. Context: [enriched_context]. Output format: [chain_format]"
   ```

   **Using delegate_task (fallback):**
   ```python
   delegate_task(
     goal="Analyze task from [lens] perspective",
     context="[enriched_context]",
     toolsets=["terminal", "file"]
   )
   ```

3. **Chain Isolation** (CRITICAL)
   - Each chain is INDEPENDENT
   - No cross-chain visibility
   - Only Deliberator sees all chains
   - See `knowledge/chain-isolation-rules.md`

**8 Chain Lenses**:

| Chain | Lens | Focus |
|-------|------|-------|
| 1 | Context & State | Input sufficiency, cached vs fresh |
| 2 | Handoff & Contract | Session/agent/skill boundaries |
| 3 | Error Handling | Hallucination, silent failures |
| 4 | Propagation | Codebase impact, side effects |
| 5 | Quality Assurance | Verification, diff, metrics |
| 6 | Risk Assessment | Failure modes, risk mitigation |
| 7 | Alternative Paths | Other valid approaches |
| 8 | Dependency Analysis | External dependencies |

**Task-Type Augmentation**:

| Task Type | Extra Chain | Focus |
|-----------|-------------|-------|
| `fix bug` | Root Cause | Bug reproduction |
| `build feature` | Impact | Scope analysis |
| `ideation` | Alternatives | Idea validation |
| `spec` | Dependencies | Complete spec |

**Output**: `analysis-chains.md` (combined findings)

---

### Phase 3: Deliberation

**Mục tiêu**: Synthesize chain findings into CORE problems and CASE recommendations.

**Thực hiện**:

1. **Findings Aggregation**
   - Collect all findings
   - Deduplicate
   - Categorize by theme

2. **Consensus Identification**
   - Strong (≥7/8 agree)
   - Moderate (5-6/8 agree)
   - Weak (3-4/8 agree)
   - None (<3 agree)

3. **Conflict Resolution**
   - Apply logic, not voting
   - Document minority positions
   - Flag unresolved for human review

4. **Synthesis**
   - Identify 3-5 CORE problems
   - Apply CASE System:
     - **PREVENT**: Context enrichment, acceptance criteria
     - **DETECT**: Verification gates, quality metrics
     - **RECOVER**: Rollback, escalation

**Output**: `deliberation.md` + `prepared-context.json`

---

### Phase 4: Output Generation

**Mục tiêu**: Write all output files to `.task-context/{task-id}/`.

**Thực hiện**:

1. **Create Task Directory**
   ```python
   task_id = "{date}-{trigger-keyword}-{uuid-short}"
   # e.g., 2026-05-11-fix-bug-a1b2c3
   ```

2. **Write Output Files**
   - `task-meta.yaml` — Task metadata
   - `context-sources.json` — Context audit
   - `analysis-chains.md` — Chain findings
   - `deliberation.md` — Synthesis
   - `prepared-context.json` — Enriched input
   - `diagrams.mmd` — Mermaid diagrams
   - `checklist.yaml` — Verification checklist

3. **Quality Gate Review**
   - Run through `loop/quality-gate.md`
   - Verify all schemas validate
   - Flag any issues

---

### Phase 5: Delivery

**Mục tiêu**: Present results to user and wait for directive.

**Thực hiện**:

1. **Present Summary**
   - Task ID and trigger
   - Context sources loaded
   - CORE problems identified
   - Prepared context ready

2. **Interaction Points**:
   - IP1: Context loaded → "Found X sources. Missing: Y. Continue?"
   - IP2: Chains complete → Show deliberation summary
   - IP3: Quality gate fail → Report failed items
   - IP4: Task too broad → Request scope clarification
   - IP5: Output complete → "Proceed to implementation?"

3. **Wait for User Directive**
   - Proceed to implementation
   - Request changes
   - Cancel task

---

## Task ID Pattern

```
{date}-{trigger-keyword}-{uuid-short}
```

**Examples**:
- `2026-05-11-fix-bug-a1b2c3`
- `2026-05-11-build-feature-d4e5f6`
- `2026-05-11-ideation-g7h8i9`

---

## Output Directory Structure

```
.task-context/{task-id}/
├── task-meta.yaml          # Task metadata
├── context-sources.json    # Context audit (loaded + missing)
├── analysis-chains.md      # K=8 chain findings
├── deliberation.md         # Synthesis + CORE problems
├── prepared-context.json   # Enriched input for implementation
├── diagrams.mmd            # Mermaid diagrams
└── checklist.yaml          # Verification checklist
```

---

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | **No Premature Implementation** | Must complete all 5 phases before any code/write |
| G2 | **Context Audit Required** | Must report loaded + missing sources |
| G3 | **Chain Isolation** | Chains must not see each other |
| G4 | **Schema Validation** | Output must validate against schemas |
| G5 | **User Confirmation** | Must wait for user at each interaction point |

---

## Anti-Pitfalls

1. **Jumping to Solution**: Analyze first, implement second
2. **Context Assumption**: Don't assume context is sufficient
3. **Chain Contamination**: Keep chains independent
4. **Incomplete Synthesis**: Deliberate over ALL chains
5. **Format Drift**: Follow schemas exactly

---

## Related Knowledge

- `knowledge/k-chains-lens.md` — 8 lens definitions
- `knowledge/context-sources.md` — Context loading guide
- `knowledge/deliberation-process.md` — Synthesis methodology
- `knowledge/chain-isolation-rules.md` — Anti-contamination rules
- `loop/quality-gate.md` — Verification checklist
- `loop/chain-isolation-enforcer.md` — Isolation enforcement

---

## Execution Example

```python
# Trigger detected: user says "fix bug in auth"
task_id = "2026-05-11-fix-bug-a1b2c3"

# Phase 1: Load Context
context = load_all_context()
# → memory + session + project files

# Phase 2: Spawn K=8 Chains
chains = spawn_k_chains(task_id, context)
# → 8 parallel analyses

# Phase 3: Deliberation
deliberation = deliberate(chains)
# → CORE problems + CASE recommendations

# Phase 4: Write Output
write_output_files(task_id, context, chains, deliberation)
# → .task-context/{task-id}/

# Phase 5: Present & Wait
present_to_user(task_id)
# → User approves or requests changes
```
