---
name: master-skill-suite
description: 'Bo 4 skill (Explorer, Architect, Planner, Builder) phuc vu viec xay dung moi agent skill. Kich hoat khi user muon tao skill moi, thiet ke skill, lap ke hoach trien khai hoac trien khai skill. Day la L0 anchor guide cho he thong xay dung skill.'
category: meta
version: "1.0.0"
author: "Steve Void Team"
pipeline_stage: 0
---

# Master Skill Suite — Agent Skill Development Pipeline

## Purpose

Bo 4 skill **Explorer → Architect → Planner → Builder** cung nhau tao ra mot he thong hoan chinh de xay dung bat ky agent skill nao.

<context>
Day la **L0 anchor guide** — trai tim tri thuc nhung chi chua L0 va phan compact nhat cua L1. Khong phai kho kien thuc. Chi lam nhiem vu: dinh nghia pipeline, datten lua chon, danh so uu tien, va huong dan load context.
</context>

---

## Pipeline Overview

```yaml
pipeline_flow:
  stage_0_explorer:
    skill: skill-explorer
    output: ".skill-context/{skill-name}/exploration.md"
    role: "Kham pha nghiep vu — thu thap tai nguyen, danh gia 7 Tieu chuan Vang"
    trigger_keywords:
      - "tao skill"
      - "xay dung skill"
      - "kham pha nghiem vu"
      - "explore skill"

  stage_1_architect:
    skill: skill-architect
    output: ".skill-context/{skill-name}/design.md"
    role: "Thiet ke kien truc — phan tich 3 Pillars, 7 Zones, tao design.md"
    trigger_keywords:
      - "thiet ke skill"
      - "ve design"
      - "tao context skill"
      - "mermaid"

  stage_2_planner:
    skill: skill-planner
    output: ".skill-context/{skill-name}/todo.md"
    role: "Lap ke hoach trien khai — phan tich 3 tang kien thuc, tao todo.md"
    trigger_keywords:
      - "lap ke hoach"
      - "tao todo"
      - "phan ra task"
      - "trace design"

  stage_3_builder:
    skill: skill-builder
    output: "{skills_root}/{skill-name}/"
    role: "Trien khai skill — thuc thi design.md va todo.md, tao production-ready skill"
    trigger_keywords:
      - "build skill"
      - "trien khai skill"
      - "implement"
      - "tao skill tu design"

flow_direction: "EXPLORER → ARCHITECT → PLANNER → BUILDER"
flow_rule: "Moi stage chi thuc hien khi stage truoc da co output. Khong bo qua stage."
```

---

## Semantic Activation Anchors

Khi gap cac tu khoa sau, agent phai kich hoat pipeline tuong ung:

```yaml
activation_signals:
  stage_0_trigger:
    anchors: ["tao skill", "xay dung skill", "kham pha", "explore"]
    action: "Load skill-explorer"

  stage_1_trigger:
    anchors: ["thiet ke", "design", "mermaid", "context skill"]
    action: "Load skill-architect"

  stage_2_trigger:
    anchors: ["ke hoach", "todo", "task", "trace"]
    action: "Load skill-planner"

  stage_3_trigger:
    anchors: ["build", "trien khai", "implement", "code"]
    action: "Load skill-builder"

  cross_skill_trigger:
    anchors: ["skill suite", "master skill", "bo 4 skill", "pipeline"]
    action: "Load toan bo pipeline overview (file nay)"
```

---

## Format Selection cho Skill Documents

```yaml
format_rules:
  SKILL_md:
    format: "YAML frontmatter + Markdown body + XML boundaries"
    token_budget: "150-400 (L0 anchor)"
    content_types:
      - boot_configuration
      - mission_statement
      - priority_order
      - must/must_not constraints
      - routing_map

  knowledge_files:
    format: "Markdown chu dao + YAML snippets"
    token_budget: "600-2500 (L2 domain)"
    content_types:
      - domain_explanation
      - standards
      - guidelines

  policy_files:
    format: "YAML + Markdown ngan"
    token_budget: "400-1200 (L1 policy)"
    content_types:
      - workflow_details
      - guardrails
      - checklists

  loop_files:
    format: "YAML / Markdown checklist"
    token_budget: "200-600 (L3 validation)"
    content_types:
      - quality_gates
      - verification_checklists

  output_contract:
    format: "YAML block trong XML <output_contract> tag"
    mandatory_fields:
      - output_type
      - file_paths
      - format
      - validation_criteria
```

---

## Priority Order (Global)

```yaml
priority_order:
  - source_fidelity        # design.md la ground truth duy nhat
  - pipeline_integrity     # khong bo qua bat ky stage nao
  - resource_completeness  # resources phai du truoc khi chuyen stage
  - user_confirmation      # moi gate phai co user xac nhan
  - minimal_invention      # chi decompose, khong them requirements

anti_goals:
  - khong tu them zone hoac file khong co trong design.md
  - khong skip gate confirmation
  - khong danh gia resource la "day du" khi thuc te con thieu
```

---

## Context Directory Structure

Tat ca cac skill trong pipeline deu lam viec voi thu muc `context`:

```yaml
context_directory: ".skill-context/{skill-name}/"

structure:
  ".skill-context/{skill-name}/"           # Root context
    "exploration.md"                        # Stage 0 output (Explorer)
    "design.md"                             # Stage 1 output (Architect)
    "todo.md"                               # Stage 2 output (Planner)
    "build-log.md"                          # Stage 3 log (Builder)
    "resources/"                            # Raw domain knowledge
    "data/"                                # Config, schemas
    "loop/"                                # Quality gates

zone_contract:
  rule: "Chi tao file trong design.md §3 Zone Mapping"
  forbidden: "Khong tu ý them file khong co trong design"
```

---

## Routing Map — Skill Dependencies

```yaml
skill_dependencies:
  skill-explorer:
    requires: []
    produces: "exploration.md"
    next: "skill-architect"

  skill-architect:
    requires: ["exploration.md (optional)"]
    produces: "design.md"
    previous_optional: true
    next: "skill-planner"

  skill-planner:
    requires: ["design.md"]
    produces: "todo.md"
    next: "skill-builder"

  skill-builder:
    requires: ["design.md", "todo.md"]
    produces: "{skills_root}/{skill-name}/"
    validation_scripts:
      - "scripts/validate_skill.py"

cross_skill_resources:
  _shared:
    path: "skills/rebuild/_shared/"
    contents:
      - "knowledge/framework.md"      # 7 Zones, Pipeline overview
      - "knowledge/architect.md"       # 3 Pillars analysis
      - "schemas/"                     # Validation schemas

  sync:
    path: "skills/rebuild/skill-sync/"
    purpose: "Dong bo skill sau khi build hoan tat"
```

---

## Stop Conditions (Global Gates)

```yaml
gates:
  gate_0_explorer_complete:
    condition: "exploration.md da ton tai"
    stop_if: "resource confidence < 70%"

  gate_1_architect_complete:
    condition: "design.md §1-§10 hoan chinh"
    stop_if: "user chua xac nhan Phase 1-3"

  gate_2_planner_complete:
    condition: "todo.md da co tat ca tasks"
    stop_if: "co [CAN LAM RO] chua giai quyet"

  gate_3_builder_complete:
    condition: "Tat ca files trong §3 da duoc tao"
    stop_if: "placeholder_density > 9"

  gate_final_validation:
    script: "scripts/validate_skill.py"
    must_pass: true
```

---

## Trace Tags (Bat Buoc)

Moi task trong todo.md phai co trace tag:

```yaml
trace_tags:
  "[TỪ DESIGN §N]":
    meaning: "Derived directly from design.md section N"
    example: "- [ ] Task description [TỪ DESIGN §3]"

  "[TỪ AUDIT TÀI NGUYÊN]":
    meaning: "Generated because a required resource was missing"
    example: "- [ ] Prepare domain doc [TỪ AUDIT TÀI NGUYÊN]"

  "[GỢI Ý BỔ SUNG]":
    meaning: "Suggested by Planner, not in design.md"
    example: "- [ ] Add validation [GỢI Ý BỔ SUNG]"

  "[CẦN LÀM RÕ]":
    meaning: "Needs user/Architect/Planner clarification"
    example: "- [ ] Clarify X [CẦN LÀM RÕ]"
    action: "Dung lai, hoi user"
```

---

## Error Handling

```yaml
error_codes:
  0: "PASS — Continue to next step"
  1: "FAIL — Fix issue, retry, or report"
  2: "EMERGENCY — Stop immediately, report error"

error_scenarios:
  design_file_missing:
    stage: "1-3"
    action: "Report: 'Run previous stage first'"

  zone_file_mismatch:
    stage: "3"
    action: "Log → Notify user → STOP (G7 Zone Contract)"

  placeholder_overload:
    threshold: 9
    stage: "3"
    action: "STOP, notify user, cannot deliver"

  resource_confidence_low:
    threshold: "70%"
    stage: "0"
    action: "Ask user before proceeding"

  system_error:
    stage: "any"
    action: "Log → Notify → STOP (Log-Notify-Stop)"
```

---

## Working Map — Load on Demand

```yaml
load_when_needed:
  # Luc nao can
  skill_explorer_workflow: "skills/rebuild/skill-explorer/SKILL.md"
  skill_architect_workflow: "skills/rebuild/skill-architect/SKILL.md"
  skill_planner_workflow: "skills/rebuild/skill-planner/SKILL.md"
  skill_builder_workflow: "skills/rebuild/skill-builder/SKILL.md"

  # Luc can
  shared_framework: "skills/rebuild/_shared/knowledge/framework.md"
  format_standards: "skills/rebuild/_shared/knowledge/format-standards.md"
  architect_reference: "skills/rebuild/_shared/knowledge/architect.md"

  # Luc can
  validation_script: "skills/rebuild/skill-builder/scripts/validate_skill.py"
  sync_script: "skills/rebuild/skill-sync/scripts/sync_skills.py"
```

---

## Interaction Protocol

```yaml
agent_protocol:
  stage_0_explorer:
    before: "Nhan yeu cau tu user → Kiem tra context directory → Bat dau Kham pha"
    during: "Thu thap resources → Danh gia 7 Tieu chuan Vang → Viet exploration.md"
    after: "Bao cao tom tat Vietnamese → Xac nhan 70%+ confidence"

  stage_1_architect:
    before: "Doc exploration.md (neu co) → Load framework.md → Bat dau thiet ke"
    during: "Phase 1 (Pain Point) → Phase 2 (3 Pillars/7 Zones) → Phase 3 (Diagrams)"
    after: "Xac nhan tung gate voi user → Ghi design.md sau moi gate"

  stage_2_planner:
    before: "Doc design.md → Audit resources/ → Phan tich 3 tang"
    during: "Step READ → Step ANALYZE → Step WRITE → Step VERIFY"
    after: "Neu co resource thieu → Phase 0 duoc tao tu dong"

  stage_3_builder:
    before: "Doc design.md + todo.md → Review resources/ → Danh gia kha thi"
    during: "Phase 1 PREPARE → Phase 2 CLARIFY → Phase 3 BUILD → Phase 4 VERIFY"
    after: "Chay validate_skill.py → Sync → Delivered"

final_output:
  include:
    - skill_directory_path
    - build_log_path
    - resource_inventory
    - validation_result
    - sync_status
```

---

## Mở rộng trong tương lai

```yaml
future_extensions:
  pattern: "Skill mo rong theo cung mau: Explorer → Architect → Planner → Builder"
  
  example_new_suite:
    - "skill-researcher" (Stage 0 variant)
    - "skill-auditor" (Quality assurance layer)
    - "skill-migrator" (Legacy-to-modern conversion)
    - "skill-optimizer" (Performance tuning)

  extension_rules:
    - Phai co trigger_keywords trong activation_signals
    - Phai co output_contract định nghĩa
    - Phai có routing_map trong skill_dependencies
    - Phai co stop_conditions trong gates
```

---

## Definition of Done (cho pipeline nay)

```yaml
done_criteria:
  exploration_complete:
    - exploration.md ton tai
    - 7 Golden Standards da danh gia
    - Resource confidence >= 70%

  design_complete:
    - design.md §1-§10 hoan chinh
    - Tat ca gates da duoc user xac nhan
    - Mermaid diagrams hop le

  plan_complete:
    - todo.md co tat ca tasks
    - Trace tags day du
    - Khong co [CAN LAM RO] chua giai quyet

  build_complete:
    - Tat ca files trong §3 Zone Mapping da tao
    - Placeholder density <= 9
    - validate_skill.py tra ve PASS
    - Sync den 4 destinations thanh cong
```
