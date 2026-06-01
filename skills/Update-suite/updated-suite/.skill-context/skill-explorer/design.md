---
skill_schema_version: "3.0.0"
artifact_type: "design"
skill_name: "skill-explorer"
generated_by: "skill-architect"
generated_at: "2026-05-27T01:51:00Z"
stage: "architect"
status: "ready_for_planner"
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
      - path: "knowledge/exploration-standards.md"
        file_required: true
        content_type: "domain-knowledge"
      - path: "knowledge/security-standards.md"
        file_required: true
        content_type: "domain-knowledge"
    zone_required: true
  scripts:
    files:
      - path: "scripts/init_context.py"
        file_required: true
        content_type: "automation-script"
    zone_required: true
  templates:
    files: []
    zone_required: false
  data:
    files:
      - path: "data/search-blacklist.yaml"
        file_required: true
        content_type: "configuration-data"
    zone_required: true
  loop:
    files:
      - path: "loop/exploration-checklist.md"
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
    - path: "policy/guardrails.md"
      base: "skill_dir"
  tier2:
    - path: "policy/workflow.md"
      base: "skill_dir"
      load_when: "Boot Sequence"
    - path: "policy/output-spec.md"
      base: "skill_dir"
      load_when: "Phase 4: Synthesis & Deliver"
    - path: "knowledge/exploration-standards.md"
      base: "skill_dir"
      load_when: "Phase 2: Golden Standards & Scale Assessment"
    - path: "knowledge/security-standards.md"
      base: "skill_dir"
      load_when: "Phase 2: Security & Isolation Analysis"
  tier3:
    - path: "_shared/templates/exploration.json.template"
      base: "skills_root"
      load_when: "Phase 4: Synthesis & Deliver"
    - path: "_shared/templates/criteria.json.template"
      base: "skills_root"
      load_when: "Phase 4: Synthesis & Deliver"
    - path: "loop/exploration-checklist.md"
      base: "skill_dir"
      load_when: "Before completeness verification"
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

# skill-explorer — Bản vẽ thiết kế kiến trúc (Stage 1)

> **Mã số**: STG1-ARCH-EXPLORER
> **Dự án**: Master Skill Suite Ver_2.0.0
> **Tầm nhìn**: Xây dựng lại kỹ năng Khảo sát nghiệp vụ Stage 0 vận hành hoàn toàn trên Sổ cái JSON và kế thừa 100% cơ chế Smart Context Splitter của Ver_0.

---

## 1. Problem Statement
*   **Vấn đề thực tế**: Phiên bản Ver_0 của `skill-explorer` sử dụng bối cảnh Markdown phẳng, dễ gây mơ hồ, sai lệch dữ liệu và khiến AI ảo giác (hallucinate).
*   **Giải pháp nâng cấp**: Chuyển dịch toàn bộ cơ chế lưu trữ bối cảnh sang **Sổ cái JSON** có cấu trúc (`exploration.json`, `criteria.json`) và Schemas nghiêm ngặt.
*   **Kế thừa**: Giữ nguyên cơ chế phân rã Micro-skills (Smart Context Splitter) nhưng nâng cấp để đọc và phân tách trên nền JSON Specs.

## 2. Capability Map
*   **Khởi tạo bối cảnh (Init Context)**: Tự động sinh folder `.skill-context/{skill-name}/` cùng các file JSON ledgers mẫu hợp lệ.
*   **Khảo sát Codebase & API (Internal Scout)**: Tìm kiếm code mẫu, APIs sử dụng các công cụ LSP và blacklist.
*   **Khảo sát Web (External Scout)**: Quét best practices và an toàn kỹ thuật.
*   **Phân rã bối cảnh (Smart Context Splitter)**: Phân tách một master-skill thành các micro-skills nhỏ hơn dựa trên JSON, tự động phân phối resources và tạo `design.md` ban đầu.

## 3. Zone Mapping
*(Đã được định nghĩa chi tiết trong frontmatter `zone_mapping`)*

## 4. Folder Structure
```text
skills/Update-suite/updated-suite/skill-explorer/
├── SKILL.md                          # Core Zone: Neo chỉ dẫn, boot và routing
├── policy/
│   ├── guardrails.md                 # Quy tắc an toàn & Ràng buộc cứng
│   ├── workflow.md                   # Mô tả quy trình làm việc 4 Phase chi tiết
│   └── output-spec.md                # Đặc tả chi tiết các file JSON đầu ra
├── knowledge/
│   ├── exploration-standards.md      # Khung 7 Tiêu chuẩn Vàng tiếng Việt
│   └── security-standards.md         # Chống Prompt Injection & Sandbox isolation
├── scripts/
│   └── init_context.py               # Script khởi tạo bối cảnh & Smart Splitter
├── templates/
│   ├── exploration.json.template     # Template JSON cho khảo sát nghiệp vụ
│   └── criteria.json.template        # Template JSON cho tiêu chí nghiệm thu
├── data/
│   └── search-blacklist.yaml         # Blacklist lọc file rác
└── loop/
    └── exploration-checklist.md      # Chốt chặn chất lượng Stage 0
```

## 5. Execution Flow
```mermaid
sequence-diagram
actor User
actor ExplorerAgent
database ContextLedger

User->>ExplorerAgent: Yêu cầu tạo skill mới
ExplorerAgent->>ExplorerAgent: Boot Sequence (Nạp SKILL.md & guardrails)
ExplorerAgent->>ExplorerAgent: Chạy scripts/init_context.py
ExplorerAgent->>ContextLedger: Khởi tạo exploration.json & criteria.json mẫu
ExplorerAgent->>ExplorerAgent: Phase 2 & 3: Quét codebase & Web qua XML boundaries
ExplorerAgent->>ContextLedger: Ghi tri thức thu thập được vào resources/
ExplorerAgent->>ExplorerAgent: Phase 4: Tổng hợp & Kiểm tra qua loop/checklist
ExplorerAgent->>ContextLedger: Đóng gói exploration.json & criteria.json
ExplorerAgent->>User: Báo cáo kết quả bằng Tiếng Việt & Sẵn sàng cho Stage 1
```

## 6. Interaction Points
*   **IP-01 (Boot Phase)**: Lập trình viên chạy lệnh khởi tạo `python3 scripts/init_context.py <skill-name>` để tạo thư mục bối cảnh.
*   **IP-02 (Golden Standards assessment)**: Dừng lại hỏi ý kiến lập trình viên nếu SCS > 3.0 và kích hoạt Smart Context Splitter để phân rã micro-skills.
*   **IP-03 (Completeness Verification)**: Bàn giao kết quả khảo sát bằng Tiếng Việt và yêu cầu người dùng xác nhận để chuyển sang Architect Stage.

## 7. Progressive Disclosure Plan
*(Đã được định nghĩa chi tiết trong frontmatter `progressive_disclosure`)*

## 8. Risks & Blind Spots
*   **Rủi ro 1: Prompt Injection từ Web Content** -> Khắc phục bằng thẻ XML bọc dữ liệu thô và chặn thực thi mã nguồn ngoài sandbox.
*   **Rủi ro 2: JSON Schema Validation Error** -> Khắc phục bằng cách tích hợp trực tiếp thư viện validation vào `init_context.py`.

## 9. Open Questions
*   Không có.

## 10. Metadata
*   **Version**: 2.0.0
*   **Lifecycle Phase**: designed
*   **Target Suite**: updated-suite
