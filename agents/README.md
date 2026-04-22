# pipeline-steve — Multi-Layer Orchestrator Agent

## Overview

`pipeline-steve` là orchestrator agent điều phối 4-layer pipeline. Mỗi layer spawns worker subagents để làm việc song song. **Orchestrator spawns tất cả subagents trực tiếp** — subagents không thể spawn subagents khác.

## ⚠️ Critical Platform Constraint

> **Subagents cannot spawn other subagents.**
> Do đó, **orchestrator phải spawn tất cả worker subagents trực tiếp**.

## Agent Files

| Agent | Role | Color | Tools |
|-------|------|-------|-------|
| `pipeline-steve.md` | Orchestrator — spawns workers for all layers | cyan | Agent, Glob, Read, Bash |
| `explore-layer.md` | Layer 1: Phân tích input + codebase | blue | Agent, Read, Grep, Glob, Bash |
| `implement-layer.md` | Layer 2: Triển khai code | green | Agent, Read, Write, Edit, Glob, Bash |
| `verify-rule-layer.md` | Layer 3: Kiểm tra rules | yellow | Agent, Read, Grep, Glob, Bash |
| `simplify-layer.md` | Layer 4: Tối ưu + /simplify | magenta | Agent, Skill, Read, Write, Edit, Bash, Glob |

## Layer Architecture

```
User Input
    │
    ▼
┌──────────────────────────────────────┐
│         PIPELINE-STEVE                │
│  Orchestrator (spawns all workers)   │
└──────────────┬───────────────────────┘
               │ spawns Layer 1 workers (1-N parallel)
         ┌─────▼─────┐
         │  EXPLORE   │  ← Spawn explore-worker(s) — 1-N agents
         └─────┬─────┘
               │ explore_output
               │ spawns Layer 2 workers (max 4 parallel)
         ┌─────▼─────┐
         │ IMPLEMENT  │  ← Spawn impl-worker(s) — 1-N agents
         └─────┬─────┘
               │ implement_output
               │ spawns Layer 3 workers (per rule, parallel)
         ┌─────▼─────┐
         │VERIFY-RULE│  ← Spawn verify-worker(s) — per rule file
         └─────┬─────┘
               │ verify_output
               │ spawns Layer 4 workers (per group, parallel)
         ┌─────▼─────┐
         │ SIMPLIFY  │  ← Spawn simplify-worker(s) — per file group
         └─────┬─────┘
               │
               ▼
         Final Report
```

## Spawning Pattern (Claude Code Format)

### ✅ Claude Code Spawning Syntax

```markdown
Agent(
  description: "[worker-name] — mô tả ngắn tác vụ",
  prompt: "
Task: [mô tả tác vụ chi tiết]
Input Context: [files, patterns, constraints]
Output Format: [expected output structure]
",
  subagent_type: "general-purpose"
)
```

### ❌ KHÔNG DÙNG (sai syntax)

```javascript
// ❌ KHÔNG dùng JS format
const results = await Promise.all([
  spawnAgent({ task: "..." }),
]);

// ❌ KHÔNG dùng SDK format
await Agent.spawn({
  name: "impl-header",
  type: "general-purpose",
  prompt: "..."
});
```

### Ví dụ: 3 parallel workers cho IMPLEMENT

```markdown
1. Agent(description: "impl-header — build navigation header", prompt: "Implement Header component...", subagent_type: "general-purpose")

2. Agent(description: "impl-sidebar — build sidebar", prompt: "Implement Sidebar component...", subagent_type: "general-purpose")

3. Agent(description: "impl-footer — build footer", prompt: "Implement Footer component...", subagent_type: "general-purpose")
```

## Parallelization Strategy

### Within Layers

| Layer | Max Parallel Workers | Grouping |
|-------|--------------------:|----------|
| Explore | 1-3 | By independent analysis areas |
| Implement | 4 | By independent tasks |
| Verify-Rule | N (per rule file) | 1 worker per rule |
| Simplify | 4 | By file groups (max 5 files/worker) |

### Execution Flow

```
Layer 1: Explore (sequential — must complete first)
  └→ 1-3 parallel workers if independent

Layer 2: Implement (sequential after explore)
  └→ Up to 4 parallel workers per batch
  └→ Next batch if dependencies exist

Layer 3: Verify-Rule (sequential after implement)
  └→ N parallel workers (1 per rule file)

Layer 4: Simplify (sequential after verify)
  └→ Up to 4 parallel workers (grouped by module)
```

## Tool Access per Layer

| Tool | Explore | Implement | Verify | Simplify |
|------|:-------:|:---------:|:------:|:--------:|
| Agent | ✅ | ✅ | ✅ | ✅ |
| Read | ✅ | ✅ | ✅ | ✅ |
| Write | - | ✅ | - | ✅ |
| Edit | - | ✅ | - | ✅ |
| Grep | ✅ | - | ✅ | - |
| Glob | ✅ | ✅ | ✅ | ✅ |
| Bash | ✅ | ✅ | ✅ | ✅ |
| Skill | - | - | - | ✅ |

## Dynamic Rule Resolution

```markdown
1. Glob("{root}/.claude/rules/*.md")
2. If rules exist → proceed with verify-rule layer
3. If no rules → skip layer, note in report
```

## Inter-Layer Data Contract

```markdown
explore_output:
  findings: [list]
  context: { files, dependencies, constraints }
  identified_tasks: [{ desc, target_files, dependencies }]
  parallel_opportunities: [task groups]

implement_output:
  created_files: [list]
  modified_files: [list]
  changed_files: [list]  # for next layer
  summary: "..."
  failed_tasks: [list]

verify_output:
  rule_files: [list]
  passed: [list]
  violations: [{ file, line, rule, violation, fix }]
  warnings: [list]
  status: "pass" | "fail" | "skipped"

simplify_output:
  optimized_files: [list]
  refactors: [list]
  total_lines_removed: N
  status: "completed" | "skipped"
```

## Error Handling

| Layer | On Failure | Retry | Continue Pipeline? |
|-------|-----------|:-----:|-------------------|
| Explore | Abort | 2 | ❌ No |
| Implement | Abort | 2 | ❌ No (if all fail) |
| Implement (partial) | Continue | 1 | ✅ Yes |
| Verify-Rule | Warning | 1 | ✅ Yes |
| Simplify | Warning | 1 | ✅ Yes |

## Output Format

```markdown
═══════════════════════════════════════
       PIPELINE-STEVE EXECUTION REPORT
═══════════════════════════════════════

[EXPLORE] ✅/❌/⏭️ (workers: N)
  Findings: [list]
  Identified Tasks: N tasks
  Parallel Groups: [list]

[IMPLEMENT] ✅/❌/⏭️ (workers: N)
  Created Files: [list]
  Modified Files: [list]
  Failed Tasks: [list or "none"]

[VERIFY-RULE] ✅/⚠️/⏭️ (workers: N)
  Rules Checked: N
  Passed: [list]
  Violations: [list]
  Warnings: [list]

[SIMPLIFY] ✅/⚠️/⏭️ (workers: N)
  Files Optimized: N
  Total Lines Removed: N
  Refactors: [list]

───────────────────────────────────────
Workers Spawned: N | Layers: N/N
Status: ✅ Complete | ⚠️ Partial | ❌ Failed
═══════════════════════════════════════
```

## Usage

```markdown
# User triggers orchestrator
"Triển khai tính năng X cho project Y"

# Orchestrator:
1. Spawn explore-worker(s) → get context
2. Spawn impl-worker(s) → implement in parallel
3. Spawn verify-worker(s) → check rules
4. Spawn simplify-worker(s) → optimize code
5. Aggregate results → final report
```

## Key Design Decisions

1. **Orchestrator spawns all workers** — subagents cannot spawn subagents
2. **Layers are sequential** — explore→implement→verify→simplify
3. **Within layers are parallel** — independent tasks run simultaneously
4. **Dynamic rule detection** — verify-rule layer is conditional
5. **Graceful degradation** — advisory layers (verify/simplify) don't block pipeline
6. **Structured handoffs** — each layer receives previous output as structured data
