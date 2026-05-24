---
skill_schema_version: "3.0.0"
artifact_type: "design"
skill_name: "format-converter"
generated_by: "skill-explorer"
generated_at: "2026-05-24T19:50:11.324680+00:00"
stage: "architect"
status: "in_progress"
is_micro_skill: true
parent_skill: "knowledge-distiller"
canonical_source:
  zone_mapping: "frontmatter.zone_mapping"
  progressive_disclosure: "frontmatter.progressive_disclosure"
zone_mapping:
  core:
    files:
      - path: "SKILL.md"
        file_required: true
        content_type: "persona-definition"
    zone_required: true
  knowledge:
    files:
      - path: "knowledge/standards.md"
        file_required: true
        content_type: "domain-knowledge"
    zone_required: true
  scripts:
    files: []
    zone_required: false
  templates:
    files: []
    zone_required: false
  data:
    files: []
    zone_required: false
  loop:
    files:
      - path: "loop/checklist.md"
        file_required: true
        content_type: "quality-gate"
    zone_required: true
  assets:
    files: []
    zone_required: false
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "loop/checklist.md"
      base: "skill_dir"
  tier2:
    - path: "knowledge/standards.md"
      base: "skill_dir"
      load_when: "Executing core logic"
  tier3: []
required_sections:
  - "1_problem_statement"
  - "2_capability_map"
  - "3_zone_mapping"
  - "4_folder_structure"
  - "5_execution_flow"
  - "6_interaction_points"
  - "7_progressive_disclosure"
  - "8_risks"
  - "9_open_questions"
  - "10_metadata"
handoff:
  next_stage: "planner"
  ready_condition:
    required:
      frontmatter_valid: true
      zone_mapping_complete: true
      required_sections_present: true
      no_blockers: true
---

# format-converter — Phân Rã Kiến Trúc Micro-Skill

> **Khởi tạo**: 2026-05-24
> **Nguồn gốc**: Báo cáo Stage 0 của master skill 'knowledge-distiller'
> **Bản đồ chỉ dẫn cha**: [master-exploration](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/knowledge-distiller/exploration.md)
> **Quy tắc đệ quy**: [CẤM PHÂN RÃ] Đây là nút lá của hệ thống.

---

## 1. Problem Statement

### A. Vấn đề thực tế (Pain Points)
[TỪ EXPLORATION §1 & §3.3]
Kế thừa từ Master Skill 'knowledge-distiller' để giải quyết độc lập tác vụ chuyên biệt sau:
- **Tác vụ**: Phân tích ngữ nghĩa dữ liệu thô, chuyển đổi định dạng và phân tách bối cảnh sang Markdown, luật bắt buộc sang YAML, ví dụ sang XML templates.

### B. Vai trò trong Orchestration Flow
[TỪ EXPLORATION §5]
Quy hoạch khuyến nghị phân vùng Zones ban đầu: Core (SKILL.md), Knowledge (knowledge/standards.md), Templates (templates/policy.yaml.template, templates/domain.md.template), Data (data/distilled_draft.yaml), Loop (loop/checklist.md)

## 2. Capability Map

[TỪ EXPLORATION §3.3 & §4]
- **Nhiệm vụ nghiệp vụ chính**: Phân tích ngữ nghĩa dữ liệu thô, chuyển đổi định dạng và phân tách bối cảnh sang Markdown, luật bắt buộc sang YAML, ví dụ sang XML templates.
- **Ràng buộc AI chuyên biệt**: Xem chỉ dẫn tương ứng trong tài liệu resources/ đã kế thừa.

## 3. Zone Mapping

## 4. Folder Structure

## 5. Execution Flow

## 6. Interaction Points

## 7. Progressive Disclosure Plan

## 8. Risks & Blind Spots

## 9. Open Questions

## 10. Metadata
