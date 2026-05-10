# Master Skill Suite — Rebuild

Bộ công cụ xây dựng Agent Skill bài bản, chạy theo pipeline 3 giai đoạn.

---

## Pipeline

```
Yêu cầu  →  skill-architect  →  design.md
                                ↓
           skill-planner  →  todo.md
                                ↓
           skill-builder  →  <skill-package>
```

| Stage | Skill | Input | Output |
|-------|-------|-------|--------|
| 1 | `skill-architect` | Yêu cầu người dùng | `design.md` |
| 2 | `skill-planner` | `design.md` | `todo.md` |
| 3 | `skill-builder` | `design.md` + `todo.md` | Skill hoàn chỉnh |

---

## skill-architect (Stage 1)

**Vai trò:** Senior Design Architect — phân tích yêu cầu, thiết kế kiến trúc skill.

**3 Phase có Gate:**

1. **Collect** — Thu thập Pain Point, User, Expected Output
2. **Analyze** — Map vào 3 Pillars & 7 Zones
3. **Design** — Xuất sơ đồ Mermaid + design.md hoàn chỉnh

**Output:** `design.md` với 10+ sections (§1-§12)

---

## skill-planner (Stage 2)

**Vai trò:** Senior Skill Planner — đọc design.md, phân tích kiến thức cần thiết, tạo kế hoạch triển khai.

**Core tasks:**

- Audit tài nguyên (Rich vs Thin)
- Phân tích 3-tier knowledge: Domain → Technical → Packaging
- Sinh task list với trace tags

**Output:** `todo.md` với Phase Breakdown + Pre-requisites table

---

## skill-builder (Stage 3)

**Vai trò:** Senior Implementation Engineer — transform design thành skill hoàn chỉnh.

**5 Phase:**

1. **PREPARE** — Đọc inputs, assess feasibility
2. **CLARIFY** — Hỏi user về ambiguities
3. **BUILD** — Implement theo todo.md phase-by-phase
4. **VERIFY** — Quality gate với Placeholder Scale
5. **DELIVER** — Hoàn thiện build-log.md

**Placeholder Scale:** <5 ✅ → 5-9 ⚠️ → 10+ ❌

---

## spec-generator

Công cụ bổ trợ — generate feature specs độc lập với pipeline chính.

**5 Phase:** Ambiguity Detection → api.json → business.md → flow.md → tasks.md

**Output:** `spec-<feature>/` folder với đầy đủ artifacts

---

## Cấu trúc Skill hoàn thiện (7 Zones)

```
{skill-name}/
├── SKILL.md           # Core: persona, workflow, guardrails
├── knowledge/         # Domain knowledge, standards
├── scripts/           # Automation tools
├── templates/         # Output format templates
├── data/              # Config, schemas
└── loop/              # Checklists, verify rules
```

---

## Shared Framework

`_shared/knowledge/framework.md` chứa single source of truth cho cả bộ:

- 7 Zones Structure
- Pipeline Flow & Handoff Contracts
- Naming Conventions (kebab-case)
- Anti-Hallucination Rules
- Quality Gates
