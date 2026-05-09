# AGENTS — Agent System & Architecture Documentation

> **Consolidated from project README files** - Central documentation for agent roles, skills, and architecture

---

## 🏗️ Agent Architecture Overview

### Multi-Layer Orchestrator System

`pipeline-steve` là orchestrator agent điều phối 4-layer pipeline. Mỗi layer spawns worker subagents để làm việc song song. **Orchestrator spawns tất cả subagents trực tiếp** — subagents không thể spawn subagents khác.

#### ⚠️ Critical Platform Constraint

> **Subagents cannot spawn other subagents.**
> Do đó, **orchestrator phải spawn tất cả worker subagents trực tiếp**.

#### Agent Files & Roles

| Agent | Role | Color | Tools |
|-------|------|-------|-------|
| `pipeline-steve.md` | Orchestrator — spawns workers for all layers | cyan | Agent, Glob, Read, Bash |
| `explore-layer.md` | Layer 1: Phân tích input + codebase | blue | Agent, Read, Grep, Glob, Bash |
| `implement-layer.md` | Layer 2: Triển khai code | green | Agent, Read, Write, Edit, Glob, Bash |
| `verify-rule-layer.md` | Layer 3: Kiểm tra rules | yellow | Agent, Read, Grep, Glob, Bash |
| `simplify-layer.md` | Layer 4: Tối ưu + /simplify | magenta | Agent, Skill, Read, Write, Edit, Bash, Glob |

#### Layer Architecture Flow

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

---

## 🛠️ Skill Development Pipeline

### Master Skill Suite — Rebuild

Bộ công cụ xây dựng Agent Skill bài bản, chạy theo pipeline 3 giai đoạn.

```
Yêu cầu  →  skill-architect  →  design.md
                                ↓
           skill-planner  →  todo.md
                                ↓
           skill-builder  →  <skill-package>
```

#### Pipeline Stages

| Stage | Skill | Input | Output |
|-------|-------|-------|--------|
| 1 | `skill-architect` | Yêu cầu người dùng | `design.md` |
| 2 | `skill-planner` | `design.md` | `todo.md` |
| 3 | `skill-builder` | `design.md` + `todo.md` | Skill hoàn chỉnh |

### skill-architect (Stage 1)

**Vai trò:** Senior Design Architect — phân tích yêu cầu, thiết kế kiến trúc skill.

**3 Phase có Gate:**

1. **Collect** — Thu thập Pain Point, User, Expected Output
2. **Analyze** — Map vào 3 Pillars & 7 Zones
3. **Design** — Xuất sơ đồ Mermaid + design.md hoàn chỉnh

**Output:** `design.md` với 10+ sections (§1-§12)

### skill-planner (Stage 2)

**Vai trò:** Senior Skill Planner — đọc design.md, phân tích kiến thức cần thiết, tạo kế hoạch triển khai.

**Core tasks:**

- Audit tài nguyên (Rich vs Thin)
- Phân tích 3-tier knowledge: Domain → Technical → Packaging
- Sinh task list với trace tags

**Output:** `todo.md` với Phase Breakdown + Pre-requisites table

### skill-builder (Stage 3)

**Vai trò:** Senior Implementation Engineer — transform design thành skill hoàn chỉnh.

**5 Phase:**

1. **PREPARE** — Đọc inputs, assess feasibility
2. **CLARIFY** — Hỏi user về ambiguities
3. **BUILD** — Implement theo todo.md phase-by-phase
4. **VERIFY** — Quality gate với Placeholder Scale
5. **DELIVER** — Hoàn thiện build-log.md

**Placeholder Scale:** <5 ✅ → 5-9 ⚠️ → 10+ ❌

---

## 📦 Skill Structure (7 Zones)

### Complete Skill Package Structure

```
{skill-name}/
├── SKILL.md           # Core: persona, workflow, guardrails
├── knowledge/         # Domain knowledge, standards
├── scripts/           # Automation tools
├── templates/         # Output format templates
├── data/              # Config, schemas
└── loop/              # Checklists, verify rules
```

### Shared Framework

`_shared/knowledge/framework.md` chứa single source of truth cho cả bộ:

- 7 Zones Structure
- Pipeline Flow & Handoff Contracts
- Naming Conventions (kebab-case)
- Anti-Hallucination Rules
- Quality Gates

---

## 🔧 Agent Tool Access Matrix

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

---

## 📊 Knowledge Base Integration

### Knowledge Categories

- **`programming/`** - Programming languages, frameworks, best practices
- **`experience/`** - Work experience, lessons learned, insights
- **`projects/`** - Project documentation, case studies, solutions
- **`notes/`** - Quick notes, ideas, thoughts
- **`resources/`** - Useful links, references, tools
- **`templates/`** - Templates for documentation, planning, etc.

### Programming Knowledge Areas

#### Languages
- **JavaScript/TypeScript** - Modern web development
- **Python** - Data science, automation, backend
- **Java** - Enterprise applications
- **Go** - Systems programming, microservices
- **Rust** - Systems programming, performance-critical applications

#### Frameworks & Libraries
- **Frontend** - React, Vue, Angular, Next.js
- **Backend** - Express, Django, Spring Boot
- **Database** - PostgreSQL, MongoDB, Redis
- **DevOps** - Docker, Kubernetes, CI/CD

### Experience Categories

#### Work Experience
- **Project Management** - Team coordination, timeline management
- **Problem Solving** - Technical challenges and solutions
- **Communication** - Team collaboration, client interactions
- **Leadership** - Mentoring, decision making

#### Lessons Learned
- **Technical Lessons** - Architecture decisions, debugging insights
- **Process Improvements** - Workflow optimizations
- **Team Dynamics** - Collaboration patterns
- **Career Growth** - Skill development, networking

---

## � Agent Spawning Patterns

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

---

## 📈 Parallelization Strategy

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

---

## 🔄 Inter-Layer Data Contracts

### explore_output
```yaml
findings: [list]
context: { files, dependencies, constraints }
identified_tasks: [{ desc, target_files, dependencies }]
parallel_opportunities: [task groups]
```

### implement_output
```yaml
created_files: [list]
modified_files: [list]
changed_files: [list]  # for next layer
summary: "..."
failed_tasks: [list]
```

### verify_output
```yaml
rule_files: [list]
passed: [list]
violations: [{ file, line, rule, violation, fix }]
warnings: [list]
status: "pass" | "fail" | "skipped"
```

### simplify_output
```yaml
optimized_files: [list]
refactors: [list]
total_lines_removed: N
status: "completed" | "skipped"
```

---

## ⚠️ Error Handling

| Layer | On Failure | Retry | Continue Pipeline? |
|-------|-----------:|:-----:|-------------------|
| Explore | Abort | 2 | ❌ No |
| Implement | Abort | 2 | ❌ No (if all fail) |
| Implement (partial) | Continue | 1 | ✅ Yes |
| Verify-Rule | Warning | 1 | ✅ Yes |
| Simplify | Warning | 1 | ✅ Yes |

---

## 📋 Output Format

```
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

---

## 🎯 Key Design Decisions

1. **Orchestrator spawns all workers** — subagents cannot spawn subagents
2. **Layers are sequential** — explore→implement→verify→simplify
3. **Within layers are parallel** — independent tasks run simultaneously
4. **Dynamic rule detection** — verify-rule layer is conditional
5. **Graceful degradation** — advisory layers (verify/simplify) don't block pipeline
6. **Structured handoffs** — each layer receives previous output as structured data

---

## 📚 Usage Examples

### User triggers orchestrator
```markdown
"Triển khai tính năng X cho project Y"
```

### Orchestrator flow
1. Spawn explore-worker(s) → get context
2. Spawn impl-worker(s) → implement in parallel
3. Spawn verify-worker(s) → check rules
4. Spawn simplify-worker(s) → optimize code
5. Aggregate results → final report

---

## 🔄 Quy trình làm việc

1. **Tạo ý tưởng**: Ghi lại ý tưởng mới vào thư mục tương ứng
2. **Phát triển**: Xây dựng và hoàn thiện ý tưởng
3. **Xem xét**: Review và feedback
4. **Chuyển đổi**: Chuyển ý tưởng đã hoàn thiện sang `docs/specs/`
5. **Dọn dẹp**: Xóa hoặc archive các file không còn cần thiết

## 📝 Hướng dẫn đặt tên file

- Sử dụng format: `YYYY-MM-DD-ten-file.md`
- Ví dụ: `2026-05-09-ai-skill-idea.md`
- Thêm tiền tố cho từng loại:
  - `idea-`: Ý tưởng mới
  - `design-`: Thiết kế, mockup
  - `research-`: Nghiên cứu
  - `brainstorm-`: Brainstorm

## 🚀 Lưu ý

- Đây là thư mục "work in progress" - không cần hoàn hảo
- Khuyến khích ghi lại mọi ý tưởng dù nhỏ nhất
- Sử dụng markdown, text, hoặc bất kỳ format nào phù hợp
- File có thể không được tổ chức hoàn hảo - điều này được chấp nhận

---

*"Mọi hệ thống agent vĩ đại đều bắt đầu từ một tài liệu kiến trúc rõ ràng"*
