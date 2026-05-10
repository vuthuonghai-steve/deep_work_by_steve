# Hermes-Native Skill Suite v3.0 — Architecture Design

> **Ngày:** 2026-05-09
> **Phiên bản:** 3.0
> **Tác giả:** Steve Void Team
> **Trạng thái:** Final Draft

---

## Tóm tắt Executive

Tài liệu này trình bày kiến trúc tổng thể của **Hermes-Native Skill Suite v3.0** — hệ thống xây dựng skill bài bản cho nền tảng Hermes. Kiến trúc gồm 4 thành phần chính: **Architect**, **Planner**, **Builder**, và **Validator**, hoạt động theo pipeline 3 giai đoạn với data flow rõ ràng.

**Các cải tiến chính so với v2.x:**
- Hỗ trợ multi-platform (Hermes + Claude) với Hermes là default
- YAML frontmatter là contract chính thức (thay thế Markdown table)
- 6 operation types: `create_new`, `patch_existing`, `refactor_existing`, `migrate_platform`, `consolidate_skills`, `deprecate_skill`
- Platform detection tự động dựa trên environment
- Hermes-native path conventions với `.hermes/skills/`

---

## 1. Component Architecture

### 1.1 Tổng quan 4 Component

```mermaid
graph TB
    subgraph "Hermes-Native Skill Suite v3.0"
        A["👤 User Request"] --> B["🏗️ Architect<br/><small>Stage 1</small>"]
        B --> C["📋 Planner<br/><small>Stage 2</small>"]
        C --> D["🔨 Builder<br/><small>Stage 3</small>"]
        D --> E["✅ Validator<br/><small>Quality Gate</small>"]
        
        B -->|design.md| C
        C -->|todo.md| D
        D -->|skill-package| E
        E -->|feedback| D
    end
    
    style B fill:#ff6b6b,color:#000
    style C fill:#ffd93d,color:#000
    style D fill:#6bcb77,color:#000
    style E fill:#4d96ff,color:#000
```

### 1.2 Chi tiết từng Component

#### 1.2.1 Architect (Stage 1)

```mermaid
graph LR
    subgraph "skill-architect"
        A1["📥 Input: User Request"] --> A2["🔍 Phase 1: Collect<br/>Pain Point + User + Output"]
        A2 -->|Gate 1<br/>User Confirm| A3["⚙️ Phase 2: Analyze<br/>3 Pillars + 7 Zones"]
        A3 -->|Gate 2<br/>Design Review| A4["🎨 Phase 3: Design<br/>Mermaid + design.md"]
        A4 -->|output| A5["📄 design.md"]
    end
    
    style A2 fill:#ff6b6b,color:#000
    style A3 fill:#ffd93d,color:#000
    style A4 fill:#6bcb77,color:#000
```

**Vai trò:** Senior Design Architect — phân tích yêu cầu, thiết kế kiến trúc skill.

**Input bắt buộc:**
- `platform_target`: `hermes` | `claude` | `both` (default: `both`)
- `operation_type`: `create_new` | `patch_existing` | `refactor_existing` | `migrate_platform` | `consolidate_skills` | `deprecate_skill`
- `execution_mode`: `lightweight` | `standard` | `strict`

**Output:** `design.md` với YAML frontmatter + 10+ sections (§1-§12)

---

#### 1.2.2 Planner (Stage 2)

```mermaid
graph LR
    subgraph "skill-planner"
        P1["📄 design.md"] --> P2["🔎 Audit Resources<br/>Rich vs Thin vs Missing"]
        P2 --> P3["📊 3-Tier Knowledge Analysis<br/>Domain → Technical → Packaging"]
        P3 --> P4["📝 Generate Task List<br/>với trace tags"]
        P4 -->|output| P5["📋 todo.md"]
    end
    
    style P2 fill:#ffd93d,color:#000
    style P3 fill:#ffd93d,color:#000
    style P4 fill:#ffd93d,color:#000
```

**Vai trò:** Senior Skill Planner — đọc design.md, phân tích kiến thức cần thiết, tạo kế hoạch triển khai.

**6 Sections bắt buộc:**
```markdown
## 1. Pre-requisites
## 2. Phase Breakdown
## 3. Knowledge & Resources Needed
## 4. Definition of Done
## 5. Notes
## 6. Builder Feedback Integration
```

**Output:** `todo.md` với YAML frontmatter + phase breakdown

---

#### 1.2.3 Builder (Stage 3)

```mermaid
graph LR
    subgraph "skill-builder"
        B1["📄 design.md + todo.md"] --> B2["📖 PREPARE<br/>Read inputs, assess feasibility"]
        B2 --> B3["❓ CLARIFY<br/>Hỏi user về ambiguities"]
        B3 --> B4["🏗️ BUILD<br/>Implement phase-by-phase"]
        B4 --> B5["🔍 VERIFY<br/>Quality gate + Placeholder Scale"]
        B5 --> B6["📦 DELIVER<br/>build-log.md + skill package"]
    end
    
    style B2 fill:#4d96ff,color:#000
    style B3 fill:#4d96ff,color:#000
    style B4 fill:#6bcb77,color:#000
    style B5 fill:#ffd93d,color:#000
    style B6 fill:#6bcb77,color:#000
```

**Placeholder Scale:**
- `<5 placeholders` ✅ Pass
- `5-9 placeholders` ⚠️ Warning
- `≥10 placeholders` ❌ Fail

---

#### 1.2.4 Validator (Quality Gate)

```mermaid
graph TB
    subgraph "HermesSkillValidator"
        V1["📥 Input: skill-package"] --> V2["📋 Parse YAML Frontmatter"]
        V2 --> V3["✅ Zone Mapping Validation"]
        V3 --> V4["🔗 Progressive Disclosure Check"]
        V4 --> V5["📁 Install Target Contract"]
        V5 --> V6["📊 Structure Validation"]
        V6 --> V7["📝 SKILL.md Constraints"]
        V7 --> V8["🔍 Report: Pass/Warn/Fail"]
    end
    
    style V2 fill:#4d96ff,color:#fff
    style V8 fill:#6bcb77,color:#000
```

---

## 2. Data Flow Diagrams

### 2.1 Pipeline Data Flow

```mermaid
flowchart LR
    subgraph "Input Layer"
        U["👤 User Request"]
    end
    
    subgraph "Stage 1: Architect"
        A["🏗️ Architect"]
        DM["📄 design.md"]
    end
    
    subgraph "Stage 2: Planner"
        P["📋 Planner"]
        TM["📋 todo.md"]
    end
    
    subgraph "Stage 3: Builder"
        B["🔨 Builder"]
        SP["📦 Skill Package"]
    end
    
    subgraph "Quality Gate"
        V["✅ Validator"]
        FB["📝 Feedback"]
    end
    
    U -->|Yêu cầu| A
    A -->|design.md| P
    P -->|todo.md| B
    B -->|skill-package| V
    V -->|feedback| B
    V -->|approved| SP
    
    style U fill:#e0e0e0
    style A fill:#ff6b6b,color:#000
    style P fill:#ffd93d,color:#000
    style B fill:#6bcb77,color:#000
    style V fill:#4d96ff,color:#fff
```

### 2.2 design.md → todo.md → skill-package Flow

```mermaid
flowchart TB
    subgraph "design.md (Architect Output)"
        D1["YAML Frontmatter<br/>zone_mapping, pillars, install_target"]
        D2["§1-§12 Markdown Body<br/>Human-readable design"]
    end
    
    subgraph "todo.md (Planner Output)"
        T1["YAML Frontmatter<br/>phases, prerequisites, blockers"]
        T2["6 Sections<br/>Task list với trace tags"]
    end
    
    subgraph "skill-package (Builder Output)"
        S1["SKILL.md<br/>Core persona + workflow"]
        S2["knowledge/<br/>Domain knowledge"]
        S3["scripts/<br/>Automation tools"]
        S4["templates/<br/>Output formats"]
        S5["data/<br/>Config + schemas"]
        S6["loop/<br/>Checklists + verify rules"]
    end
    
    D1 -->|zone_mapping| T1
    D2 -->|zone details| T2
    T1 -->|phase tasks| S1
    T2 -->|task details| S2
    T2 -->|task details| S3
    T2 -->|task details| S4
    T2 -->|task details| S5
    T2 -->|task details| S6
```

### 2.3 Contract Handoff giữa các Stage

```mermaid
sequenceDiagram
    participant User
    participant Architect
    participant Planner
    participant Builder
    participant Validator
    
    User->>Architect: Yêu cầu skill mới
    Architect->>Architect: Phase 1: Collect
    Architect->>Architect: Phase 2: Analyze
    Architect->>Architect: Phase 3: Design
    Architect-->>User: Xác nhận design?
    User->>Architect: ✅ Confirm
    Architect->>Planner: design.md
    
    Planner->>Planner: Audit resources
    Planner->>Planner: 3-tier knowledge analysis
    Planner->>Planner: Generate task list
    Planner->>Builder: todo.md
    
    Builder->>Builder: PREPARE phase
    Builder->>Builder: CLARIFY phase
    Builder->>Builder: BUILD phase
    Builder->>Validator: skill-package
    
    Validator->>Validator: YAML-first validation
    Validator-->>Builder: Feedback (nếu có)
    
    alt Validation Pass
        Validator-->>User: ✅ Skill hoàn chỉnh
    else Validation Fail
        Builder->>Builder: Fix issues
        Builder->>Validator: Re-validate
    end
```

---

## 3. Platform Detection Flow

### 3.1 Platform Detection Algorithm

```mermaid
flowchart TD
    PD1["🔍 Bắt đầu Detection"] --> PD2{"Biến môi trường<br/>HERMES_SKILL_PATH?"}
    PD2 -->|Có| PD3["✅ Platform: hermes"]
    PD2 -->|Không| PD4{"Biến môi trường<br/>CLAUDE_SKILL_PATH?"}
    PD4 -->|Có| PD5["✅ Platform: claude"]
    PD4 -->|Không| PD6{"File kiểm tra<br/>~/.hermes/skills/?"}
    PD6 -->|Tồn tại| PD3
    PD6 -->|Không| PD7{"File kiểm tra<br/>~/.claude/skills/?"}
    PD7 -->|Tồn tại| PD5
    PD7 -->|Không| PD8["⚠️ Không detect được<br/>Default: hermes"]
    
    style PD3 fill:#6bcb77,color:#000
    style PD5 fill:#4d96ff,color:#fff
    style PD8 fill:#ffd93d,color:#000
```

### 3.2 install_target Resolution Priority

```mermaid
flowchart LR
    R1["1️⃣ Explicit User Override<br/>CLI flag --install-target"] --> R5["Final install_target"]
    R2["2️⃣ Frontmatter<br/>design.md install_target"] --> R5
    R3["3️⃣ Platform Detection<br/>Hermes vs Claude"] --> R5
    R4["4️⃣ Default Fallback<br/>Platform-specific"] --> R5
    
    style R5 fill:#6bcb77,color:#000
```

### 3.3 Platform vs Scope Matrix

| Platform | Scope | Target Path |
|----------|-------|-------------|
| **hermes** | user-local | `~/.hermes/skills/{category}/{skill-name}/` |
| **hermes** | repo | `{repo}/skills/{category}/{skill-name}/` |
| **hermes** | project-local | `{project}/.hermes/skills/{skill-name}/` |
| **claude** | user-local | `~/.claude/skills/{skill-name}/` |
| **both** | user-local | `~/.hermes/skills/...` (preferred) |

---

## 4. Hermes-Native Path Conventions

### 4.1 Directory Structure

```mermaid
graph TD
    ROOT["~"] --> H[".hermes/"]
    H --> HS["skills/"]
    HS --> CAT1["{category}/"]
    CAT1 --> SN1["{skill-name}/"]
    SN1 --> SKILL["SKILL.md"]
    SN1 --> KNOW["knowledge/"]
    SN1 --> SCRIPTS["scripts/"]
    SN1 --> TEMP["templates/"]
    SN1 --> DATA["data/"]
    SN1 --> LOOP["loop/"]
    
    CAT1 --> CAT2["{category-2}/"]
    CAT2 --> SN2["{skill-name-2}/"]
    
    KNOW --> K1["architect.md"]
    KNOW --> K2["domain.md"]
    SCRIPTS --> S1["validate_skill.py"]
    SCRIPTS --> S2["helper.sh"]
    TEMP --> TP1["output_template.md"]
    DATA --> D1["config.yaml"]
    LOOP --> L1["verify_rules.md"]
    LOOP --> L2["checklist.md"]
    
    style H fill:#ff6b6b,color:#000
    style HS fill:#ff6b6b,color:#000
```

### 4.2 Hermes Skill Package Template

```
{skill-name}/
├── SKILL.md                    # Zone: core (mandatory, tier 1)
├── knowledge/
│   ├── architect.md            # Zone: knowledge (tier 2)
│   └── {domain-specific}.md    # Zone: knowledge
├── scripts/
│   ├── validate_skill.py       # Validation script
│   └── {helper-scripts}.sh     # Automation tools
├── templates/
│   └── {output-template}.md    # Output format templates
├── data/
│   └── config.yaml             # Configuration + schemas
└── loop/
    ├── verify_rules.md         # Verification rules
    └── checklist.md            # Phase checklists
```

### 4.3 Naming Conventions

| Element | Convention | Ví dụ |
|---------|------------|-------|
| Skill name | kebab-case | `session-learner`, `spec-generator` |
| Category | kebab-case | `mobile`, `web`, `thread` |
| Zone directories | snake_case | `knowledge/`, `scripts/` |
| Files | kebab-case hoặc snake_case | `SKILL.md`, `validate_skill.py` |
| Frontmatter fields | snake_case | `platform_target`, `install_target` |

---

## 5. Operation Types & Adaptive Workflows

### 5.1 Operation Types Overview

```mermaid
flowchart TD
    OT1["create_new"] -->|"Standard full pipeline"| B1["BUILDER: Full 5-phase"]
    OT2["patch_existing"] -->|"Minimal delta"| B2["BUILDER: 4-phase (skip Phase 0)"]
    OT3["refactor_existing"] -->|"Behavior preservation"| B3["BUILDER: +audit step"]
    OT4["migrate_platform"] -->|"Platform adaptation"| B4["BUILDER: +analysis step"]
    OT5["consolidate_skills"] -->|"Overlap analysis"| B5["BUILDER: +inventory step"]
    OT6["deprecate_skill"] -->|"Minimal plan"| B6["BUILDER: Only deprecation notice"]
    
    style OT1 fill:#6bcb77,color:#000
    style OT2 fill:#ffd93d,color:#000
    style OT6 fill:#ff6b6b,color:#000
```

### 5.2 Execution Modes

| Mode | Gates | Behavior |
|------|-------|----------|
| **lightweight** | Không có gate | Tự động proceed |
| **standard** | Confirm sau mỗi phase | User interaction |
| **strict** | Full review + signoff | Formal approval |

---

## 6. YAML Frontmatter Contract

### 6.1 design.md Frontmatter Schema

```yaml
---
name: {skill-name}
version: "1.0.0"
status: in-progress | complete | deprecated

# Operation context
platform_target: hermes | claude | both
operation_type: create_new | patch_existing | refactor_existing | migrate_platform | consolidate_skills | deprecate_skill
execution_mode: lightweight | standard | strict

# Install target
install_target:
  platform: hermes | claude | both
  scope: user-local | repo | project-local
  path: ~/.hermes/skills/{category}/{skill-name}/

# Zone Mapping (machine-readable contract)
zone_mapping:
  - zone: core
    files:
      - path: SKILL.md
        tier: 1
        mandatory: true
        content_summary: "Persona, phases, guardrails"

# 3 Pillars Analysis
pillars:
  knowledge:
    domains: [list]
    gaps: [list]
  process:
    phases: [list]
    branches: [list]
  guardrails:
    risks: [list]
    mitigations: [list]

# Progressive Disclosure
progressive_disclosure:
  tier1:
    - SKILL.md
    - ../_shared/knowledge/framework.md

# Metadata
metadata:
  author: Steve Void Team
  date_created: YYYY-MM-DD
  date_modified: YYYY-MM-DD
---
```

### 6.2 todo.md Frontmatter Schema

```yaml
---
name: {skill-name}
version: "1.0.0"
date_created: YYYY-MM-DD
status: draft | complete | in-progress

operation_type: create_new
execution_mode: standard

phases:
  - id: 0
    name: Resource Preparation
    tasks:
      - id: "0.1"
        description: "Task description"
        priority: critical | high | medium | low
        estimated_hours: 4-8
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        dependencies: []
        status: pending | in-progress | done

prerequisites:
  - tier: domain
    topic: "Topic name"
    resource_path: "resources/topic.md"
    status: rich | thin | missing

blockers:
  - id: "B1"
    description: "Blocker description"
    resolved: false

traceability:
  task_to_design:
    "0.1": ["§3 Zone Mapping"]
---
```

---

## 7. Validator Architecture

### 7.1 HermesSkillValidator Flow

```mermaid
flowchart TD
    V1["📥 Input: skill-path + design-path"] --> V2["📄 Parse design.yaml frontmatter"]
    V2 --> V3["📄 Parse skill SKILL.md frontmatter"]
    V3 --> V4{"design_frontmatter<br/>exists?"}
    V4 -->|Có| V5["🎯 Extract zone_mapping"]
    V4 -->|Không| V6["⚠️ Skip zone validation"]
    V5 --> V7["✅ Validate expected zones"]
    V7 --> V8["🔗 Validate progressive disclosure"]
    V8 --> V9["📁 Validate install target contracts"]
    V9 --> V10["📋 Run structure checks"]
    V10 --> V11["📝 SKILL.md constraints check"]
    V11 --> V12["🔍 Report: errors + warnings"]
    
    style V2 fill:#4d96ff,color:#fff
    style V12 fill:#6bcb77,color:#000
```

### 7.2 Validation Rules Priority

1. **YAML Frontmatter** (canonical contract) — parse trước
2. **Zone Mapping** — check expected files exist
3. **Progressive Disclosure** — tier1 files load at boot
4. **Install Target Contract** — path resolution validation
5. **SKILL.md Constraints** — persona, phases, guardrails presence
6. **Structure Validation** — directory + file naming

---

## 8. Complete System Diagram

### 8.1 Full Pipeline v3.0

```mermaid
flowchart TB
    subgraph "USER LAYER"
        U["👤 User"]
    end
    
    subgraph "SKILL SUITE v3.0"
        subgraph "Stage 1: Architect"
            A1["Collect Phase"]
            A2["Analyze Phase"]
            A3["Design Phase"]
            A1 -->|Gate 1| A2
            A2 -->|Gate 2| A3
        end
        
        subgraph "Stage 2: Planner"
            P1["Audit Resources"]
            P2["Knowledge Analysis"]
            P3["Task Generation"]
            P1 --> P2 --> P3
        end
        
        subgraph "Stage 3: Builder"
            B1["PREPARE"]
            B2["CLARIFY"]
            B3["BUILD"]
            B4["VERIFY"]
            B5["DELIVER"]
            B1 --> B2 --> B3 --> B4 --> B5
        end
        
        subgraph "Quality Gate"
            V1["HermesSkillValidator"]
            V2["YAML-first Validation"]
            V3["Zone Mapping Check"]
            V4["Progressive Disclosure"]
            V1 --> V2 --> V3 --> V4
        end
    end
    
    subgraph "OUTPUTS"
        D["design.md"]
        T["todo.md"]
        S["skill-package/"]
        L["build-log.md"]
    end
    
    U -->|Request| A1
    A3 -->|design.md| D
    D -->|Input| P1
    P3 -->|todo.md| T
    T -->|Input| B1
    B5 -->|skill-package| V1
    V4 -->|feedback loop| B3
    V4 -->|approved| S
    B5 -->|log| L
    
    style U fill:#e0e0e0
    style A1 fill:#ff6b6b,color:#000
    style P1 fill:#ffd93d,color:#000
    style B1 fill:#4d96ff,color:#fff
    style V1 fill:#4d96ff,color:#fff
```

---

## 9. Hermes-Path Resolution Context

### 9.1 Environment Variables

| Variable | Mặc định | Mô tả |
|----------|-----------|-------|
| `HERMES_SKILL_PATH` | `~/.hermes/skills/` | Base path cho Hermes skills |
| `HERMES_SKILL_CATEGORY` | `{auto-detect}` | Category của skill đang active |
| `HERMES_CONFIG_PATH` | `~/.hermes/config/` | Config directory |

### 9.2 Shared Framework Location

```
_shared/
└── knowledge/
    └── framework.md    # Single source of truth cho cả bộ skill suite
```

**Framework chứa:**
- 7 Zones Structure
- Pipeline Flow & Handoff Contracts
- Naming Conventions (kebab-case)
- Anti-Hallucination Rules
- Quality Gates

---

## 10. Error Handling & Rollback

### 10.1 Per-Stage Error Handling

| Stage | On Failure | Retry | Continue? |
|-------|-----------|:-----:|----------|
| Architect | Abort | 2 | ❌ No |
| Planner | Abort | 2 | ❌ No |
| Builder (all fail) | Abort | 2 | ❌ No |
| Builder (partial) | Warning | 1 | ✅ Yes |
| Validator | Warning | 1 | ✅ Yes |

### 10.2 Rollback Procedures

**Phase 0 Rollback (Operation Context):**
```
Trigger: User muốn thay đổi platform_target, operation_type, hoặc execution_mode

Rollback Steps:
1. Reset § Metadata (operation context fields)
2. Quay lại Phase 1: Collect — thu thập lại operation context
```

**Stage Rollback:**
```
Trigger: Error at any gate

Steps:
1. Log error details vào build-log.md
2. Restore previous state (design.md hoặc todo.md)
3. Notify user với error summary
4. Chờ user instruction
```

---

## 11. Refinement Loop

```mermaid
flowchart LR
    subgraph "Refinement Loop"
        R1["Builder output"] --> R2["Validator check"]
        R2 --> R3{"Pass?"}
        R3 -->|Có| R4["✅ Approve"]
        R3 -->|Không| R5["📝 Feedback"]
        R5 --> R6["Builder fixes"]
        R6 --> R1
    end
    
    style R4 fill:#6bcb77,color:#000
    style R5 fill:#ffd93d,color:#000
```

**Refinement triggers:**
- Placeholder count ≥ 10
- Zone files missing
- Validation errors
- User feedback

---

## 12. Glossary

| Term | Định nghĩa |
|------|------------|
| **Zone** | Logical grouping của files trong skill package |
| **Tier** | Load priority cho progressive disclosure |
| **Contract** | YAML frontmatter là canonical agreement giữa stages |
| **Placeholder** | `[TODO]` hoặc `[PLACEHOLDER]` markers trong code |
| **Hermes-native** | Path conventions và tools riêng của Hermes platform |

---

## 13. Related Documents

- `docs/raw/ideas/skill-suite-improvement-raw-notes/2026-05-09-master-skill-suite-v3-upgrade-spec.vi.md`
- `docs/raw/AGENTS.md` — Agent Architecture Documentation
- `.skill-context/registry/README.md` — Skill Registry

---

*Document generated: 2026-05-09*
*Hermes-Native Skill Suite v3.0 Architecture*
