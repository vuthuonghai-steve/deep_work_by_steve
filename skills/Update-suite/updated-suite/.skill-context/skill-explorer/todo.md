---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "skill-explorer"
generated_by: "skill-planner"
generated_at: "2026-05-27T01:52:00Z"
stage: "planner"
status: "ready_for_builder"
trace_to_design: "design.md"
phases:
  - id: "PH1"
    name: "Foundation & Core Setup"
    tasks:
      - id: "T1.1"
        title: "Tạo SKILL.md L0 Anchor tinh gọn"
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3 & §4]"
        status: "done"
        depends_on: []
        file_target: "SKILL.md"
        acceptance_criteria:
          - "Token count <= 700 tokens thực chất"
          - "YAML frontmatter đầy đủ"
          - "Chứa Boot Sequence và Routing Map rõ ràng"
      - id: "T1.2"
        title: "Tạo policy/guardrails.md cho các ràng buộc an toàn"
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3 & §8]"
        status: "done"
        depends_on: []
        file_target: "policy/guardrails.md"
        acceptance_criteria:
          - "Chứa đầy đủ các luật must và must_not"
          - "Tích hợp ràng buộc Sổ cái JSON"
  - id: "PH2"
    name: "Knowledge & Operating Policies"
    tasks:
      - id: "T2.1"
        title: "Xây dựng knowledge/exploration-standards.md"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3 & §4]"
        status: "done"
        depends_on: ["T1.1"]
        file_target: "knowledge/exploration-standards.md"
        acceptance_criteria:
          - "Kế thừa 100% 7 Tiêu chuẩn Vàng bằng tiếng Việt"
          - "Đầy đủ thang đo SCS và các orchestration patterns"
      - id: "T2.2"
        title: "Xây dựng knowledge/security-standards.md"
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3 & §8]"
        status: "done"
        depends_on: ["T1.1", "T1.2"]
        file_target: "knowledge/security-standards.md"
        acceptance_criteria:
          - "Mô tả chi tiết phòng chống Prompt Injection bằng XML boundaries"
          - "Chi tiết môi trường Sandbox Docker biệt lập"
      - id: "T2.3"
        title: "Tạo policy/workflow.md mô tả 4 Phase vận hành"
        zone: "core"
        priority: "medium"
        trace: "[TỪ DESIGN §5]"
        status: "done"
        depends_on: ["T2.1"]
        file_target: "policy/workflow.md"
        acceptance_criteria:
          - "Mô tả chi tiết 4 Phase làm việc"
          - "Tương thích với Sổ cái JSON specs"
      - id: "T2.4"
        title: "Tạo policy/output-spec.md mô tả đặc tả JSON"
        zone: "core"
        priority: "high"
        trace: "[TỪ DESIGN §2]"
        status: "done"
        depends_on: ["T1.2", "T2.1"]
        file_target: "policy/output-spec.md"
        acceptance_criteria:
          - "Đặc tả cấu trúc exploration.json và criteria.json để AI sinh chuẩn xác"
  - id: "PH3"
    name: "Automation Scripts Implementation"
    tasks:
      - id: "T3.1"
        title: "Phát triển scripts/init_context.py nâng cấp"
        zone: "scripts"
        priority: "critical"
        trace: "[TỪ DESIGN §2 & §3]"
        status: "done"
        depends_on: ["T1.1", "T2.4"]
        file_target: "scripts/init_context.py"
        acceptance_criteria:
          - "Khởi tạo thư mục bối cảnh .skill-context/{name}/ và resources/"
          - "Tạo exploration.json và criteria.json mẫu khớp 100% schema JSON"
          - "Smart Context Splitter: đọc exploration.json, phân tách tài nguyên và tự động tạo design.md cho các micro-skills"
  - id: "PH4"
    name: "Templates, Data & Loop Quality Gate"
    tasks:
      - id: "T4.1"
        title: "Tạo templates/exploration.json.template"
        zone: "templates"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        status: "done"
        depends_on: ["T2.4"]
        file_target: "templates/exploration.json.template"
        acceptance_criteria:
          - "Mẫu JSON chuẩn khớp schema exploration"
      - id: "T4.2"
        title: "Tạo templates/criteria.json.template"
        zone: "templates"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        status: "done"
        depends_on: ["T2.4"]
        file_target: "templates/criteria.json.template"
        acceptance_criteria:
          - "Mẫu JSON chuẩn khớp schema criteria"
      - id: "T4.3"
        title: "Tạo data/search-blacklist.yaml"
        zone: "data"
        priority: "medium"
        trace: "[TỪ DESIGN §3]"
        status: "done"
        depends_on: ["T1.1"]
        file_target: "data/search-blacklist.yaml"
        acceptance_criteria:
          - "Kế thừa danh sách blacklist lọc file rác"
      - id: "T4.4"
        title: "Tạo loop/exploration-checklist.md"
        zone: "loop"
        priority: "high"
        trace: "[TỪ DESIGN §3 & §8]"
        status: "done"
        depends_on: ["T2.3", "T2.4"]
        file_target: "loop/exploration-checklist.md"
        acceptance_criteria:
          - "Bản checklist tự kiểm tra Stage 0 chất lượng cao"
blockers: []
prerequisites:
  - item: "Sổ cái JSON Schemas"
    tier: "domain"
    status: "ready"
    resource_file: "_shared/schemas/"
    action_if_missing: "N/A"
  - item: "Báo cáo khảo sát Stage 0 gốc"
    tier: "technical"
    status: "ready"
    resource_file: ".skill-context/skill-explorer/resources/skill-explorer-scout-report.md"
    action_if_missing: "N/A"
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

