---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "ba-synthesizer"
generated_by: "skill-planner"
generated_at: "2026-06-07T18:37:00+07:00"
stage: "planner"
status: "ready_for_builder"
trace_to_design: ".skill-context/ba-synthesizer/design.md"
phases:
  - id: "PH0"
    name: "Phase 0: Prerequisite Audit & Setup"
    tasks:
      - id: "T0.1"
        title: "Verify and register rich resource files"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        depends_on: []
        status: "pending"
        file_target: knowledge/cross-ref-rules.md
        acceptance_criteria:
          - "Check resource folder holds all 4 necessary files."
          - "Verify that all resources are marked as Rich."
  - id: "PH1"
    name: "Phase 1: Knowledge & Data Setup (Tier 1 & 2)"
    tasks:
      - id: "T1.1"
        title: "Build knowledge/quality-criteria.md"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: knowledge/quality-criteria.md
        acceptance_criteria:
          - "Implement quality criteria based on resources/01-quality-matrix-extracted.md"
          - "Verify formatting matches LLM standards"
      - id: "T1.2"
        title: "Build knowledge/cross-ref-rules.md"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: knowledge/cross-ref-rules.md
        acceptance_criteria:
          - "Implement cross-validation logic (SD-ERD, MoSCoW-Gherkin) from resources/02-cross-ref-validation-rules.md"
      - id: "T1.3"
        title: "Build data/quality-matrix.yaml"
        zone: "data"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: data/quality-matrix.yaml
        acceptance_criteria:
          - "Define quality-matrix YAML structure matching weights and thresholds from resources/01-quality-matrix-extracted.md"
  - id: "PH2"
    name: "Phase 2: Templates & Process Loop (Tier 3)"
    tasks:
      - id: "T2.1"
        title: "Build templates/business-analysis.md.template"
        zone: "templates"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: templates/business-analysis.md.template
        acceptance_criteria:
          - "Define consolidated report structure following resources/03-handoff-metadata-schema.md"
      - id: "T2.2"
        title: "Build loop/synthesizer-checklist.md"
        zone: "loop"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: loop/synthesizer-checklist.md
        acceptance_criteria:
          - "Include completeness self-checklist for the 7 deliverables"
  - id: "PH3"
    name: "Phase 3: Core Implementation & Integration (Tier 3)"
    tasks:
      - id: "T3.1"
        title: "Build SKILL.md L0 Core rules"
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.2", "T1.3", "T2.1", "T2.2"]
        status: "pending"
        file_target: SKILL.md
        acceptance_criteria:
          - "Integrate character persona, 4-phase execution flow, dynamic disclosure rules, and limitations."
          - "Strictly follow SKILL.md token limit guidelines (max 700 tokens)."
blockers:
  - id: "B1"
    type: "CLARIFICATION_NEEDED"
    description: "Làm rõ cách Explorer nhận diện file business-analysis.md trong .skill-context/"
    raised_by: "design §9"
    trace: "[CẦN LÀM RÕ]"
    blocks_tasks: ["T3.1"]
    resolved: false
    resolution: null
  - id: "B2"
    type: "CLARIFICATION_NEEDED"
    description: "Xác nhận điểm chất lượng (Quality Score) có quy đổi thành điểm SCS (Stage 0) hay không"
    raised_by: "design §9"
    trace: "[CẦN LÀM RÕ]"
    blocks_tasks: ["T1.3"]
    resolved: false
    resolution: null
prerequisites:
  - item: "Tài liệu ma trận chất lượng"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-synthesizer/resources/01-quality-matrix-extracted.md"
    action_if_missing: "Xem nguồn ba-synthesizer-analysis.md §3.2 và tạo lại"
  - item: "Quy tắc kiểm định chéo SD-ERD & MoSCoW-Gherkin"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-synthesizer/resources/02-cross-ref-validation-rules.md"
    action_if_missing: "Xem nguồn ba-synthesizer-analysis.md §4 và tạo lại"
  - item: "Schema YAML frontmatter bàn giao"
    tier: "packaging"
    status: "ready"
    resource_file: ".skill-context/ba-synthesizer/resources/03-handoff-metadata-schema.md"
    action_if_missing: "Xem nguồn ba-synthesizer-analysis.md §6.2 và tạo lại"
  - item: "Phạm vi, Rủi ro & Scenario nghiệm thu"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-synthesizer/resources/04-scope-definition.md"
    action_if_missing: "Xem nguồn ba-synthesizer-analysis.md và tạo lại"
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

# Kế hoạch Triển khai: ba-synthesizer

> **Micro-skill**: ba-synthesizer (MS-3)  
> **Traceability**: [TỪ DESIGN §1-10]  

---

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|---|---|---|---|---|
| 1 | Tài liệu ma trận chất lượng | Domain | Làm căn cứ để thiết lập bộ tiêu chuẩn chất lượng (criteria) và ma trận trọng số (quality-matrix) | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 2 | Quy tắc kiểm định chéo SD-ERD & MoSCoW-Gherkin | Domain | Xác định logic so khớp giữa Sequence Diagram - ERD và MoSCoW - Gherkin Scenarios | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 3 | Schema YAML frontmatter bàn giao | Packaging | Đảm bảo định dạng frontmatter trong business-analysis.md hợp lệ để Explorer có thể nạp được | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 4 | Phạm vi, Rủi ro & Scenario nghiệm thu | Domain | Cung cấp kịch bản kiểm thử tích hợp (Happy Path và Warning Path) cho micro-skill | [TỪ AUDIT TÀI NGUYÊN] | Ready |

---

## 2. Phase Breakdown

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|---|---|---|---|---|
| T0.1 | Verify and register rich resource files | Medium | 0.5 | None | [TỪ AUDIT TÀI NGUYÊN] |
| T1.1 | Build knowledge/quality-criteria.md | High | 1.5 | T0.1 | [TỪ DESIGN §3] |
| T1.2 | Build knowledge/cross-ref-rules.md | High | 1.5 | T0.1 | [TỪ DESIGN §3] |
| T1.3 | Build data/quality-matrix.yaml | Critical | 1.0 | T1.1 | [TỪ DESIGN §3] |
| T2.1 | Build templates/business-analysis.md.template | Medium | 1.0 | T0.1 | [TỪ DESIGN §3] |
| T2.2 | Build loop/synthesizer-checklist.md | Medium | 1.0 | T0.1 | [TỪ DESIGN §3] |
| T3.1 | Build SKILL.md L0 Core rules | Critical | 2.0 | T1.2, T1.3, T2.1, T2.2 | [TỪ DESIGN §3] |

- [ ] T0.1: Verify and register rich resource files [TỪ AUDIT TÀI NGUYÊN]
- [ ] T1.1: Build knowledge/quality-criteria.md [TỪ DESIGN §3]
- [ ] T1.2: Build knowledge/cross-ref-rules.md [TỪ DESIGN §3]
- [ ] T1.3: Build data/quality-matrix.yaml [TỪ DESIGN §3]
- [ ] T2.1: Build templates/business-analysis.md.template [TỪ DESIGN §3]
- [ ] T2.2: Build loop/synthesizer-checklist.md [TỪ DESIGN §3]
- [ ] T3.1: Build SKILL.md L0 Core rules [TỪ DESIGN §3]

---

## 3. Knowledge & Resources Needed

Dưới đây là các tài nguyên và tài liệu liên quan dùng cho quá trình thực hiện:
- **Ma trận chất lượng**: `.skill-context/ba-synthesizer/resources/01-quality-matrix-extracted.md`
- **Quy tắc kiểm định**: `.skill-context/ba-synthesizer/resources/02-cross-ref-validation-rules.md`
- **Schema frontmatter bàn giao**: `.skill-context/ba-synthesizer/resources/03-handoff-metadata-schema.md`
- **Định nghĩa phạm vi & scenarios**: `.skill-context/ba-synthesizer/resources/04-scope-definition.md`
- **Bản thiết kế (Design Specification)**: `.skill-context/ba-synthesizer/design.md`

---

## 4. Definition of Done

Cần đảm bảo hoàn thành tất cả các mục sau để bàn giao sang Stage 3 (Builder):
- [ ] Tạo đầy đủ 6 tệp tin được quy hoạch tại Zone Mapping (design.md §3) bao gồm:
  - `skills/rebuild/ba-synthesizer/SKILL.md` [TỪ DESIGN §3]
  - `skills/rebuild/ba-synthesizer/knowledge/quality-criteria.md` [TỪ DESIGN §3]
  - `skills/rebuild/ba-synthesizer/knowledge/cross-ref-rules.md` [TỪ DESIGN §3]
  - `skills/rebuild/ba-synthesizer/templates/business-analysis.md.template` [TỪ DESIGN §3]
  - `skills/rebuild/ba-synthesizer/data/quality-matrix.yaml` [TỪ DESIGN §3]
  - `skills/rebuild/ba-synthesizer/loop/synthesizer-checklist.md` [TỪ DESIGN §3]
- [ ] Định dạng tệp tin `SKILL.md` tuân thủ giới hạn kích thước tối đa 700 tokens. [TỪ DESIGN §3]
- [ ] Các tệp cấu hình (YAML, JSON) vượt qua kiểm định schema. [TỪ DESIGN §3]
- [ ] Không chứa bất kỳ placeholder nào (`TODO`, `mock`, `pass`) trong mã nguồn hoặc tài liệu của skill. [TỪ DESIGN §3]
- [ ] Đã chạy thử nghiệm và kiểm chứng thành công 2 scenarios nghiệm thu từ tài liệu phạm vi (Happy path & Warning path). [TỪ DESIGN §3]

---

## 5. Notes

Các vấn đề cần làm rõ [CẦN LÀM RÕ]:
- **Câu hỏi mở #1**: Điểm chất lượng có nên quy đổi thành điểm SCS ở Stage 0 không? Hiện tại giữ tách biệt để phân định rõ độ hoàn thiện và độ phức tạp. [CẦN LÀM RÕ]
- **Câu hỏi mở #2**: Làm sao Explorer tự động nhận diện file `business-analysis.md` đã có sẵn? Giải pháp đề xuất là cấu hình Explorer Phase 1 tự động tìm file trong thư mục bối cảnh `.skill-context/` trước khi chạy khảo sát. [CẦN LÀM RÕ]

---

## 6. Builder Feedback Integration

Mục này dùng để ghi nhận các phản hồi từ Stage 3 (Builder) trong quá trình triển khai thực tế. Hiện tại chưa có phản hồi nào. [TỪ DESIGN §3] [GỢI Ý BỔ SUNG]
