---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "ba-elicitor"
generated_by: "skill-planner"
generated_at: "2026-06-07T18:37:36+07:00"
stage: "planner"
status: "ready_for_builder"
trace_to_design: ".skill-context/ba-elicitor/design.md"
phases:
  - id: "PH0"
    name: "Phase 0: Domain & Resource Preparation"
    tasks:
      - id: "T0.1"
        title: "Chuẩn bị tri thức về Mindset Keywords"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        status: "done"
        file_target: knowledge/mindset-keywords.md
        acceptance_criteria:
          - "Extract 6 keywords and vector anchors from 01-mindset-keywords-extracted.md"
      - id: "T0.2"
        title: "Chuẩn bị tri thức về Elicitation Rules"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        status: "done"
        file_target: knowledge/elicitation-rules.md
        acceptance_criteria:
          - "Extract elicitation rules, anti-hallucination rules, and 5W1H questionnaires from 02-elicitation-rules-mined.md"
  - id: "PH1"
    name: "Phase 1: Core Implementation"
    tasks:
      - id: "T1.1"
        title: "Tạo file L0 Core Anchor SKILL.md"
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1", "T0.2"]
        status: "pending"
        file_target: SKILL.md
        acceptance_criteria:
          - "Include Persona Elicitor, 4-phase process, Must/Must Not, and Limitations"
      - id: "T1.2"
        title: "Tạo file knowledge/mindset-keywords.md"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: knowledge/mindset-keywords.md
        acceptance_criteria:
          - "Define 6 mindset keywords with vector anchors"
      - id: "T1.3"
        title: "Tạo file knowledge/elicitation-rules.md"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: knowledge/elicitation-rules.md
        acceptance_criteria:
          - "Implement normalizations rules, anti-hallucination logic, and 5W1H templates"
      - id: "T1.4"
        title: "Tạo file knowledge/question-framework.md"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: knowledge/question-framework.md
        acceptance_criteria:
          - "Implement question framework"
      - id: "T1.5"
        title: "Tạo file knowledge/normalization-logic.md"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: knowledge/normalization-logic.md
        acceptance_criteria:
          - "Implement normalization logic"
      - id: "T1.6"
        title: "Tạo file knowledge/scope-definition.md"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: knowledge/scope-definition.md
        acceptance_criteria:
          - "Implement scope definition"
  - id: "PH2"
    name: "Phase 2: Templates & Data Schema"
    tasks:
      - id: "T2.1"
        title: "Tạo file templates/elicitation-report.md.template"
        zone: "templates"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: templates/elicitation-report.md.template
        acceptance_criteria:
          - "Define MD format with sections and trace tags for report output"
      - id: "T2.2"
        title: "Tạo file data/input-schema.yaml"
        zone: "data"
        priority: "low"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: data/input-schema.yaml
        acceptance_criteria:
          - "Build YAML schema for input structured mapping"
  - id: "PH3"
    name: "Phase 3: Validation & Quality Control"
    tasks:
      - id: "T3.1"
        title: "Tạo file loop/elicitor-checklist.md"
        zone: "loop"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: loop/elicitor-checklist.md
        acceptance_criteria:
          - "Provide self-checklist for validating the output quality"
blockers: []
prerequisites:
  - item: "Mindset keywords resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-elicitor/resources/01-mindset-keywords-extracted.md"
  - item: "Elicitation rules resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-elicitor/resources/02-elicitation-rules-mined.md"
  - item: "Question framework resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-elicitor/resources/03-question-framework.md"
  - item: "Normalization logic resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-elicitor/resources/04-normalization-logic.md"
  - item: "Scope definition resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-elicitor/resources/05-scope-definition.md"
handoff:
  next_stage: "builder"
  ready_condition:
    required:
      blockers_empty: true
      phase0_done: true
      prerequisites_ready: true
      schema_valid: true
      design_zones_covered: true
---

# Kế Hoạch Triển Khai: ba-elicitor (Micro-Skill Elicitor)

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier (Domain/Technical/Packaging) | Mục đích | Trace | Status |
|---|---|---|---|---|---|
| 1 | `01-mindset-keywords-extracted.md` | domain | Định nghĩa 6 mindset keywords vàng | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 2 | `02-elicitation-rules-mined.md` | domain | Quy tắc chuẩn hóa, anti-hallucination và master prompt | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 3 | `03-question-framework.md` | domain | Cấu trúc câu hỏi 5W1H và 3 paths | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 4 | `04-normalization-logic.md` | domain | Logic chuẩn hóa đầu vào tự do | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 5 | `05-scope-definition.md` | domain | Đặc tả scope, input/output contract và handoff | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 6 | `design.md` | packaging | Quy hoạch 7 Zones cho micro-skill | [TỪ DESIGN §3] | Ready |

## 2. Phase Breakdown

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|---|---|---|---|---|
| T0.1 | Chuẩn bị tri thức về Mindset Keywords | Medium | 1.0 | None | [TỪ AUDIT TÀI NGUYÊN] |
| T0.2 | Chuẩn bị tri thức về Elicitation Rules | Medium | 1.0 | None | [TỪ AUDIT TÀI NGUYÊN] |
| T1.1 | Tạo file L0 Core Anchor SKILL.md | Critical | 2.5 | T0.1, T0.2 | [TỪ DESIGN §3] |
| T1.2 | Tạo file knowledge/mindset-keywords.md | High | 2.0 | T1.1 | [TỪ DESIGN §3] |
| T1.3 | Tạo file knowledge/elicitation-rules.md | High | 2.0 | T1.1 | [TỪ DESIGN §3] |
| T1.4 | Tạo file knowledge/question-framework.md | Medium | 1.5 | T1.1 | [TỪ DESIGN §3] |
| T1.5 | Tạo file knowledge/normalization-logic.md | Medium | 1.5 | T1.1 | [TỪ DESIGN §3] |
| T1.6 | Tạo file knowledge/scope-definition.md | Medium | 1.5 | T1.1 | [TỪ DESIGN §3] |
| T2.1 | Tạo file templates/elicitation-report.md.template | Medium | 1.5 | T1.1 | [TỪ DESIGN §3] |
| T2.2 | Tạo file data/input-schema.yaml | Low | 1.0 | T1.1 | [TỪ DESIGN §3] |
| T3.1 | Tạo file loop/elicitor-checklist.md | Medium | 1.5 | T1.1 | [TỪ DESIGN §3] |

### Chi tiết các nhiệm vụ (Checklist)

#### Phase 0: Domain & Resource Preparation
- [ ] T0.1: Phân tích và nạp 6 từ khóa tư duy vàng [TỪ AUDIT TÀI NGUYÊN]
- [ ] T0.2: Phân tích và cấu trúc hóa quy tắc khơi gợi [TỪ AUDIT TÀI NGUYÊN]

#### Phase 1: Core Implementation
- [ ] T1.1: Thiết lập cấu trúc Core SKILL.md [TỪ DESIGN §3]
- [ ] T1.2: Triển khai chi tiết mindset-keywords.md [TỪ DESIGN §3]
- [ ] T1.3: Triển khai chi tiết elicitation-rules.md [TỪ DESIGN §3]
- [ ] T1.4: Triển khai chi tiết question-framework.md [TỪ DESIGN §3]
- [ ] T1.5: Triển khai chi tiết normalization-logic.md [TỪ DESIGN §3]
- [ ] T1.6: Triển khai chi tiết scope-definition.md [TỪ DESIGN §3]

#### Phase 2: Templates & Data Schema
- [ ] T2.1: Triển khai mẫu elicitation-report.md.template [TỪ DESIGN §3]
- [ ] T2.2: Triển khai data/input-schema.yaml [TỪ DESIGN §3]

#### Phase 3: Validation & Quality Control
- [ ] T3.1: Triển khai checklist chốt chất lượng [TỪ DESIGN §3]

## 3. Knowledge & Resources Needed

| Tên tài liệu / Tài nguyên | Đường dẫn vật lý | Vai trò trong triển khai |
|---|---|---|
| Mindset Keywords | `.skill-context/ba-elicitor/resources/01-mindset-keywords-extracted.md` | Cung cấp tri thức cho `knowledge/mindset-keywords.md` |
| Elicitation Rules | `.skill-context/ba-elicitor/resources/02-elicitation-rules-mined.md` | Cung cấp tri thức cho `knowledge/elicitation-rules.md` |
| Question Framework | `.skill-context/ba-elicitor/resources/03-question-framework.md` | Cấu trúc câu hỏi khơi gợi và phân rã các path |
| Normalization Logic | `.skill-context/ba-elicitor/resources/04-normalization-logic.md` | Logic chuẩn hóa đầu vào và trace tags cho report |
| Scope Definition | `.skill-context/ba-elicitor/resources/05-scope-definition.md` | Khung hoạt động, trigger, handoff và tiêu chuẩn chất lượng |

## 4. Definition of Done

- [ ] Hoàn thành và tạo đầy đủ 9 tệp tin được phân vùng trong bản thiết kế [TỪ DESIGN §3]
- [ ] Tệp tin `SKILL.md` không vượt quá giới hạn 700 tokens [TỪ DESIGN §3]
- [ ] Không có placeholder (`TODO`, `pass`, `mock`) trong bất kỳ file code hay cấu trúc nào [TỪ DESIGN §3]
- [ ] File output `elicitation-report.md` tuân thủ đúng template và trace tags [TỪ DESIGN §3]
- [ ] Bộ câu hỏi 5W1H và cơ chế phân rã 3 paths được cài đặt hoàn tất [TỪ DESIGN §3]
- [ ] Chạy qua validator của Stage 4 và đạt kết quả PASS [TỪ DESIGN §3]

## 5. Notes

### Câu hỏi mở và điểm cần làm rõ
- [ ] Có nên tích hợp sẵn một script python để validate tính MECE của input-schema không? [CẦN LÀM RÕ]
- [ ] Làm sao để tự động trigger `ba-analyst` sau khi `ba-elicitor` ghi file xong? [CẦN LÀM RÕ]

## 6. Builder Feedback Integration

### Phản hồi và Điều chỉnh
- [ ] Chưa có phản hồi từ Builder. Sẽ được cập nhật khi Builder chạy thực tế. [GỢI Ý BỔ SUNG]
