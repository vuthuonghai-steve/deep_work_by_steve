---
name: agent-skill-builder
description: 'He thong xay dung agent skill cho AI Agent. Bo 4 skill (Explorer, Architect, Planner, Builder) giup tao moi agent skill. Kich hoat khi user muon tao skill moi, thiet ke, lap ke hoach hoac trien khai mot agent skill.'
category: meta
version: "1.0.0"
author: "Steve Void Team"
---

# Agent Skill Builder — He Thong Xay Dung Agent Skill

## 1. Muc dich

He thong nay phuc vu viec **xay dung agent skill** — mot don vi tri thuc huong hanh vi, duoc AI Agent doc va su dung de thuc hien mot cong viec cu the.

<context>
Agent skill khac voi code thong thuong. No la mot tai lieu huong dan AI cach thuc lam viec, goi y hanh vi, dinh nghia dau ra, va rang buoc. Bo 4 skill nay giup tao ra agent skill theo quy trinh chuan.
</context>

---

## 2. Bo 4 Skill Hien Tai

```yaml
skill_inventory:
  skill-explorer:
    stage: 0
    role: "Kham pha nghiep vu"
    muc_dich: "Thu thap tai nguyen, tim hieu yeu cau, danh gia 7 Tieu chuan Vang"
    output: "exploration.md"
    vi_tri: "skills/rebuild/skill-explorer/SKILL.md"

  skill-architect:
    stage: 1
    role: "Thiet ke kien truc"
    muc_dich: "Phan tich yeu cau, thiet ke 3 Pillars, 7 Zones, tao design.md"
    output: "design.md"
    vi_tri: "skills/rebuild/skill-architect/SKILL.md"

  skill-planner:
    stage: 2
    role: "Lap ke hoach trien khai"
    muc_dich: "Chuyen design thanh task list, xac dinh tai nguyen can thiet"
    output: "todo.md"
    vi_tri: "skills/rebuild/skill-planner/SKILL.md"

  skill-builder:
    stage: 3
    role: "Trien khai skill"
    muc_dich: "Thuc thi task, tao file skill, kiem tra chat luong"
    output: "{skill-name}/"
    vi_tri: "skills/rebuild/skill-builder/SKILL.md"
```

---

## 3. Quy Trinh Pipeline

```
User yeu cau tao skill
         │
         ▼
┌─────────────────────────┐
│  Stage 0: EXPLORER      │  ← Kham pha nghiem vu
│  Output: exploration.md │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Stage 1: ARCHITECT     │  ← Thiet ke kien truc
│  Output: design.md      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Stage 2: PLANNER       │  ← Lap ke hoach
│  Output: todo.md        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Stage 3: BUILDER       │  ← Trien khai
│  Output: {skill-name}/  │
└────────────┬────────────┘
             │
             ▼
      Dong bo (sync)
         │
         ▼
   Skill hoan chinh
```

---

## 4. Trigger Keywords

```yaml
trigger_map:
  skill-explorer:
    keywords: ["tao skill", "xay dung skill", "kham pha nghiem vu", "explore"]
    tu dong: "Khi user yeu cau tao skill moi nhung chua co thong tin gi"

  skill-architect:
    keywords: ["thiet ke skill", "design.md", "mermaid", "tao context"]
    tu dong: "Khi can tao design cho skill"

  skill-planner:
    keywords: ["lap ke hoach", "tao todo", "phan task", "trace design"]
    tu dong: "Khi da co design.md va can tao ke hoach trien khai"

  skill-builder:
    keywords: ["build skill", "trien khai", "implement", "tao skill"]
    tu dong: "Khi da co design.md + todo.md va san sang trien khai"

  full_pipeline:
    keywords: ["tao agent skill", "xay dung agent skill", "bo skill"]
    tu dong: "Khi user yeu cau day du tu dau"
```

---

## 5. Output Contract

```yaml
output_files:
  exploration_md:
    noi_dung: "Tai nguyen thu thap, 7 Tieu chuan Vang, danh gia"
    dinh_dang: "Markdown + YAML"
    buoc: "Stage 0"

  design_md:
    noi_dung: "§1 Problem Statement, §2 Capability Map, §3 Zone Mapping, §4-6 Diagrams, §7-9 Analysis"
    dinh_dang: "Markdown + YAML + Mermaid"
    buoc: "Stage 1"
    so_sections: 10

  todo_md:
    noi_dung: "Task list, Pre-requisites, Definition of Done, Trace tags"
    dinh_dang: "Markdown + YAML"
    buoc: "Stage 2"

  skill_files:
    noi_dung: "SKILL.md + knowledge/ + policy/ + loop/ + scripts/"
    dinh_dang: "Directory structure"
    buoc: "Stage 3"
```

---

## 6. Context Directory

```yaml
context_root: ".skill-context/{skill-name}/"

structure:
  ".skill-context/{skill-name}/"
    "exploration.md"              # Stage 0 output
    "design.md"                  # Stage 1 output
    "todo.md"                    # Stage 2 output
    "build-log.md"               # Stage 3 execution log
    "resources/"                 # Raw domain knowledge
    "data/"                     # Config, schemas
    "loop/"                     # Quality gates

rule: "Chi tao file trong design.md §3 Zone Mapping"
```

---

## 7. Format Quy Chuẩn

```yaml
format_selection:
  SKILL_md:
    mau: "YAML frontmatter + Markdown body + XML boundaries"
    token_budget: "150-400 (L0 anchor)"
    dung_cho: "Boot config, mission, constraints"

  knowledge_files:
    mau: "Markdown chu dao + YAML snippets"
    dung_cho: "Domain explanation, standards"

  policy_files:
    mau: "YAML + Markdown ngan"
    dung_cho: "Workflow, guardrails, checklists"

  loop_files:
    mau: "YAML / Markdown checklist"
    dung_cho: "Quality gates, verification"

format_anchors:
  must: ["must", "must_not", "priority_order", "constraints"]
  boundaries: ["<instructions>", "<context>", "<output_contract>"]
  trace: ["[TỪ DESIGN §N]", "[TỪ AUDIT TÀI NGUYÊN]", "[GỢI Ý BỔ SUNG]", "[CẦN LÀM RÕ]"]
```

---

## 8. Priority Order

```yaml
priority_order:
  - source_fidelity        # design.md la ground truth duy nhat
  - pipeline_integrity     # Khong bo qua bat ky stage nao
  - resource_completeness  # Tai nguyen phai du truoc khi chuyen stage
  - user_confirmation      # Moi gate phai co user xac nhan
  - minimal_invention      # Chi decompose, khong them requirements

anti_goals:
  - Khong tu them zone hoac file khong co trong design
  - Khong skip gate confirmation
  - Khong danh gia tai nguyen la "day du" khi con thieu
```

---

## 9. Error Handling

```yaml
error_codes:
  0: "PASS — Tiep tuc step tiep theo"
  1: "FAIL — Sua loi, thu lai, hoac bao cao"
  2: "EMERGENCY — Dung ngay, bao loi"

common_errors:
  design_file_missing:
    message: "Chay skill-architect truoc de tao design.md"
    stage: "2-3"

  zone_contract_violation:
    message: "Chi tao file trong §3 Zone Mapping"
    stage: "3"

  placeholder_overload:
    threshold: 9
    message: "Dung trien khai — qua nhieu placeholder"

  low_confidence:
    threshold: "70%"
    message: "Hoi xac nhan user truoc khi tiep tuc"
```

---

## 10. Mo Rong Trong Tuong Lai

```yaml
extension_model:
  nguyen_tac: "Mo rong theo cuing cau truc: Explorer → Architect → Planner → Builder"

  vi_du_moi_skill:
    - "skill-researcher"      # Giai doan 0 nang cao
    - "skill-auditor"         # Kiem tra chat luong skill
    - "skill-migrator"        # Chuyen doi skill cu
    - "skill-optimizer"       # Toi uu hieu suat skill

  khi_tao skill_moi:
    1. Tu dong kich hoat trigger keywords tuong ung
    2. Co output_contract dinh nghia ro
    3. Co routing_map trong skill_dependencies
    4. Co stop_conditions trong gates
```

---

## 11. Working Map

```yaml
load_when_needed:
  # Chi tiet workflow
  explorer_workflow: "skills/rebuild/skill-explorer/SKILL.md"
  architect_workflow: "skills/rebuild/skill-architect/SKILL.md"
  planner_workflow: "skills/rebuild/skill-planner/SKILL.md"
  builder_workflow: "skills/rebuild/skill-builder/SKILL.md"

  # Tai nguyen chia se
  shared_framework: "skills/rebuild/_shared/knowledge/framework.md"
  format_standards: "skills/rebuild/_shared/knowledge/format-standards.md"

  # Cong cu
  validate_script: "skills/rebuild/skill-builder/scripts/validate_skill.py"
  sync_script: "skills/rebuild/skill-sync/scripts/sync_skills.py"
```

---

## 12. Definition of Done

```yaml
skill_complete:
  stage_0:
    - exploration.md ton tai
    - Danh gia 7 Tieu chuan Vang hoan chinh
    - Confidence >= 70%

  stage_1:
    - design.md §1-§10 hoan chinh
    - Tat ca gates da duoc user xac nhan
    - Mermaid diagrams hop le

  stage_2:
    - todo.md co tat ca tasks
    - Trace tags day du
    - Khong con [CẦN LÀM RÕ] chua giai quyet

  stage_3:
    - Tat ca files trong §3 da duoc tao
    - Placeholder density <= 9
    - validate_skill.py tra ve PASS
    - Da dong bo den 4 destinations
```
