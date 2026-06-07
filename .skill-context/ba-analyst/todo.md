---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "ba-analyst"
generated_by: "skill-planner"
generated_at: "2026-06-07T18:37:36+07:00"
stage: "planner"
status: "ready_for_builder"
trace_to_design: ".skill-context/ba-analyst/design.md"
phases:
  - id: PH0
    name: "Phase 0: Domain & Resource Preparation"
    tasks:
      - id: T0.1
        title: "Verify domain resources and analyze handoff mismatch between elicitor and analyst"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        status: "pending"
        file_target: knowledge/
        acceptance_criteria:
          - "All 6 resources are audited and categorized as Rich"
          - "Elicitor-Analyst mismatch is resolved via normalization rules"
  - id: PH1
    name: "Phase 1: Knowledge & Template Construction"
    tasks:
      - id: T1.1
        title: "Build classification-rules.md defining FR/NFR logic and MoSCoW matrix"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: knowledge/classification-rules.md
        acceptance_criteria:
          - "File classification-rules.md is created with FR/NFR definitions"
          - "MoSCoW matrix and sample technical justifications are included"
      - id: T1.2
        title: "Build mermaid-syntax.md specifying Mermaid.js syntax and templates"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: knowledge/mermaid-syntax.md
        acceptance_criteria:
          - "File mermaid-syntax.md is created with templates for Sequence, Flowchart, and ERD"
          - "Syntax guidelines to avoid rendering errors are documented"
      - id: T1.3
        title: "Build gherkin-guide.md providing standards for Given-When-Then scenarios"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: knowledge/gherkin-guide.md
        acceptance_criteria:
          - "File gherkin-guide.md is created with Gherkin writing rules"
          - "Minimum of 3 scenarios (Happy, Alt, Exception) rule is specified"
      - id: T1.4
        title: "Build risk-assessment.md defining the risk matrix and mitigation rules"
        zone: "knowledge"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: knowledge/risk-assessment.md
        acceptance_criteria:
          - "File risk-assessment.md is created with Probability x Impact matrix"
          - "Integration guidelines with MoSCoW priorities are detailed"
      - id: T1.5
        title: "Build analysis-report.md.template as a structured output blueprint"
        zone: "templates"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.1", "T1.2", "T1.3", "T1.4"]
        status: "pending"
        file_target: templates/analysis-report.md.template
        acceptance_criteria:
          - "Template file is created matching the 7 deliverables from design spec"
          - "Includes structure for frontmatter, classification, diagrams, schema, Gherkin, risk, and trace mapping"
  - id: PH2
    name: "Phase 2: Core Rules & Flow Implementation"
    tasks:
      - id: T2.1
        title: "Build SKILL.md defining character persona and 7-phase execution flow"
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T1.5"]
        status: "pending"
        file_target: SKILL.md
        acceptance_criteria:
          - "File SKILL.md is created within 700 tokens limit"
          - "Defines the 7-phase analysis process and frontmatter alignment logic"
          - "Specifies execution triggers and handoff criteria"
  - id: PH3
    name: "Phase 3: Verification & Loop Quality Gate"
    tasks:
      - id: T3.1
        title: "Build analyst-checklist.md specifying quality gate checkpoints"
        zone: "loop"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T2.1"]
        status: "pending"
        file_target: loop/analyst-checklist.md
        acceptance_criteria:
          - "File analyst-checklist.md is created with checkpoints for all 7 deliverables"
          - "Verification criteria for Mermaid syntax and Gherkin scenarios are detailed"
blockers: []
prerequisites:
  - item: "classification-rules resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-analyst/resources/01-classification-rules-extracted.md"
    action_if_missing: "Extract FR/NFR and MoSCoW rules from deep_work_by_steve knowledge base"
  - item: "mermaid-syntax resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-analyst/resources/02-mermaid-syntax-reference.md"
    action_if_missing: "Obtain Mermaid syntax rules for Sequence, Flowchart, and ERD"
  - item: "gherkin-guide resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-analyst/resources/03-gherkin-guide-mined.md"
    action_if_missing: "Obtain Gherkin writing rules and standard templates"
  - item: "risk-assessment resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-analyst/resources/04-risk-assessment-framework.md"
    action_if_missing: "Obtain Risk Assessment framework rules"
  - item: "data-schema resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-analyst/resources/05-data-schema-patterns.md"
    action_if_missing: "Obtain Data Schema patterns and Quality Gate specifications"
  - item: "scope-definition resource"
    tier: "domain"
    status: "ready"
    resource_file: ".skill-context/ba-analyst/resources/06-scope-definition.md"
    action_if_missing: "Define the scope boundaries and handoff alignment guidelines"
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

# Kế Hoạch Triển Khai: ba-analyst (Micro-Skill Analyst)

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | 01-classification-rules-extracted.md | Domain | Quy tắc phân loại FR/NFR & MoSCoW | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 2 | 02-mermaid-syntax-reference.md | Domain | Chuẩn cú pháp vẽ Mermaid.js hệ thống | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 3 | 03-gherkin-guide-mined.md | Domain | Chuẩn viết Acceptance Criteria bằng Gherkin | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 4 | 04-risk-assessment-framework.md | Domain | Khung ma trận rủi ro hệ thống & mitigation | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 5 | 05-data-schema-patterns.md | Domain | Đặc tả 7 deliverables và Quality Gates đầu ra | [TỪ AUDIT TÀI NGUYÊN] | Ready |
| 6 | 06-scope-definition.md | Domain | Phân tích lệch pha handoff elicitor -> analyst | [TỪ AUDIT TÀI NGUYÊN] | Ready |

## 2. Phase Breakdown

**Bảng Kế Hoạch Các Phase**
| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| T0.1 | Verify domain resources and analyze handoff mismatch | High | 1.0 | None | [TỪ AUDIT TÀI NGUYÊN] |
| T1.1 | Build classification-rules.md (FR/NFR & MoSCoW rules) | High | 2.0 | T0.1 | [TỪ DESIGN §3] |
| T1.2 | Build mermaid-syntax.md (Mermaid diagram standards) | High | 2.0 | T0.1 | [TỪ DESIGN §3] |
| T1.3 | Build gherkin-guide.md (Given-When-Then rules) | High | 2.0 | T0.1 | [TỪ DESIGN §3] |
| T1.4 | Build risk-assessment.md (Risk matrix standards) | Medium | 1.5 | T0.1 | [TỪ DESIGN §3] |
| T1.5 | Build analysis-report.md.template (Output template) | High | 2.0 | T1.1, T1.2, T1.3, T1.4 | [TỪ DESIGN §3] |
| T2.1 | Build SKILL.md (Persona & execution flow) | Critical | 3.0 | T1.5 | [TỪ DESIGN §3] |
| T3.1 | Build analyst-checklist.md (Quality gates checklist) | Medium | 1.5 | T2.1 | [TỪ DESIGN §3] |

**Chi Tiết Công Việc (Checklist)**
- [ ] T0.1: Verify domain resources and analyze handoff mismatch [TỪ AUDIT TÀI NGUYÊN]
- [ ] T1.1: Build classification-rules.md (FR/NFR & MoSCoW rules) [TỪ DESIGN §3]
- [ ] T1.2: Build mermaid-syntax.md (Mermaid diagram standards) [TỪ DESIGN §3]
- [ ] T1.3: Build gherkin-guide.md (Given-When-Then rules) [TỪ DESIGN §3]
- [ ] T1.4: Build risk-assessment.md (Risk matrix standards) [TỪ DESIGN §3]
- [ ] T1.5: Build analysis-report.md.template (Output template) [TỪ DESIGN §3]
- [ ] T2.1: Build SKILL.md (Persona & execution flow) [TỪ DESIGN §3]
- [ ] T3.1: Build analyst-checklist.md (Quality gates checklist) [TỪ DESIGN §3]

## 3. Knowledge & Resources Needed

| Resource / Document | Location | Purpose / Content |
|---------------------|----------|-------------------|
| Classification Rules | `.skill-context/ba-analyst/resources/01-classification-rules-extracted.md` | FR/NFR definitions & MoSCoW matrix logic |
| Mermaid Syntax | `.skill-context/ba-analyst/resources/02-mermaid-syntax-reference.md` | Syntactical rules for rendering diagrams |
| Gherkin Guide | `.skill-context/ba-analyst/resources/03-gherkin-guide-mined.md` | Given-When-Then templates and scenario constraints |
| Risk Assessment | `.skill-context/ba-analyst/resources/04-risk-assessment-framework.md` | Probability and impact scoring rules |
| Data Schema Patterns | `.skill-context/ba-analyst/resources/05-data-schema-patterns.md` | 7 required deliverables and quality gates |
| Scope Definition | `.skill-context/ba-analyst/resources/06-scope-definition.md` | Input/Output contract details and handoff alignments |

## 4. Definition of Done

- Toàn bộ các files được định nghĩa trong §3 Zone Mapping được khởi tạo thành công và chứa đầy đủ nội dung nghiệp vụ:
  - `skills/rebuild/ba-analyst/SKILL.md` (L0: Core)
  - `skills/rebuild/ba-analyst/knowledge/classification-rules.md` (L1: Knowledge)
  - `skills/rebuild/ba-analyst/knowledge/mermaid-syntax.md` (L1: Knowledge)
  - `skills/rebuild/ba-analyst/knowledge/gherkin-guide.md` (L1: Knowledge)
  - `skills/rebuild/ba-analyst/knowledge/risk-assessment.md` (L1: Knowledge)
  - `skills/rebuild/ba-analyst/templates/analysis-report.md.template` (L2: Templates)
  - `skills/rebuild/ba-analyst/loop/analyst-checklist.md` (L4: Loop)
- Logic align lệch pha dữ liệu frontmatter (`analyzed_at` vs `elicited_at` và status enum) từ elicitor được cài đặt thành công ở SKILL.md.
- Sơ đồ Mermaid vẽ mẫu đáp ứng các điều kiện: Sequence ≥ 3 actors, Flowchart đầy đủ Happy/Alt/Exception, ERD có PK/FK & data types rõ ràng.
- Không chứa bất kỳ placeholder dạng `TODO`, `TBD`, hoặc mã giả `pass` nào.
- Vượt qua vòng kiểm thử tĩnh và schema validation.

## 5. Notes

- **Câu hỏi mở 1:** Làm thế nào để validate cú pháp Mermaid tự động tại runtime? [CẦN LÀM RÕ]
  - *Giải pháp tạm thời:* Builder sẽ sử dụng công cụ hoặc script test nhỏ (nếu có sandbox) để parse thử cấu trúc Mermaid, hoặc rely vào regex chắt lọc chặt chẽ nhằm tránh ký tự đặc biệt ngoài nhãn.
- **Câu hỏi mở 2:** Định nghĩa Data Schema dưới dạng JSON Schema hay Markdown Table? [CẦN LÀM RÕ]
  - *Giải pháp tạm thời:* Sẽ sử dụng bảng Markdown làm đại diện chính trực quan, đồng thời đính kèm block code JSON Schema cho máy đọc khi cần.
- **Lệch pha Handoff:** Builder cần chú ý xử lý normalize hai trường frontmatter `analyzed_at` (sang `elicited_at`) và map `elicitation-completed` (sang `completed`) trong bước đầu tiên của flow xử lý.
- **Đề xuất mở rộng:** Có thể sinh thêm Use Case Diagram để làm rõ mối quan hệ actor-system. [GỢI Ý BỔ SUNG]

## 6. Builder Feedback Integration

| # | Phase / Task | Builder Feedback | Actions Taken | Status |
|---|--------------|------------------|---------------|--------|
| 1 | N/A | Chưa có phản hồi từ Builder | Sẽ cập nhật khi Builder bắt đầu thực hiện | Pending |
