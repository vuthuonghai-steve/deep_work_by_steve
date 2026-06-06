---
skill_schema_version: "3.0.0"
artifact_type: "exploration"
skill_name: "ba-analyst"
generated_by: "skill-explorer"
generated_at: "2026-06-06T22:15:00+07:00"
stage: "exploration"
status: "completed"
required_sections:
  - "1_pain_point_and_core_objective"
  - "2_existing_resources_audit"
  - "3_seven_golden_standards_assessment"
  - "4_ai_instruction_standards_and_rules"
  - "5_process_flow_and_automation_mapping"
  - "6_architectural_recommendations"
  - "7_risks_and_open_questions"
  - "8_production_quality_criteria"
  - "9_metadata"
handoff:
  next_stage: "architect"
  ready_condition:
    required:
      frontmatter_valid: true
      resources_audited: true
      seven_standards_assessed: true
      quality_criteria_defined: true
      no_blockers: true
---

# ba-analyst — Báo Cáo Khảo Sát Nghiệp Vụ & Khai Thác Tài Nguyên (Micro-Skill Analyst)

> **Ngày khảo sát**: 2026-06-06
> **Trạng thái**: Hoàn thành (`completed`)
> **Tài liệu cha**: `skill-business-analyst/exploration.md`
> **Mục tiêu**: Bóc tách tài liệu khảo sát và bối cảnh hoạt động độc lập cho micro-skill thứ hai (ba-analyst).

---

## 1. Pain Point & Core Objective

### A. Vấn đề thực tế (Pain Points)
1. **Khó khăn trong mô hình hóa kỹ thuật**: AI Agent thường gặp lỗi cú pháp khi vẽ sơ đồ (Mermaid.js) hoặc thiết kế cấu trúc dữ liệu thô dẫn đến việc render bị hỏng.
2. **Thiếu phân loại yêu cầu cụ thể (FR/NFR)**: Không phân tách rõ ràng hành vi hệ thống (Functional) với các ràng buộc chất lượng (Non-Functional) và mức độ ưu tiên MoSCoW, gây khó khăn cho việc kiểm thử sau này.
3. **Mất liên kết (Traceability)**: Thiếu các liên kết ngược từ thiết kế kỹ thuật về yêu cầu nghiệp vụ ban đầu, dẫn đến nguy cơ sai lệch chức năng (scope creep).
4. **Handoff không đồng bộ từ Elicitor**: Có sự không đồng nhất về mặt trường thông tin (metadata mismatch) khi nhận dữ liệu từ `ba-elicitor` chuyển giao qua.

### B. Mục tiêu tự động hóa (Core Objective)
Xây dựng micro-skill **ba-analyst** (MS-2) tại Stage -1 nhằm:
1. Tiếp nhận tài liệu `elicitation-report.md` từ `ba-elicitor`.
2. Tự động chuẩn hóa và phân loại các yêu cầu chức năng (FR) & phi chức năng (NFR), áp dụng ma trận độ ưu tiên MoSCoW.
3. Tạo ra 3 sơ đồ hệ thống Mermaid.js hợp lệ (Sequence Diagram, Flowchart, ERD).
4. Viết kịch bản kiểm thử Acceptance Criteria dạng Gherkin (tối thiểu 3 kịch bản Given-When-Then).
5. Thực hiện phân tích rủi ro và tác động (Risk Matrix).
6. Xuất ra tài liệu phân tích kỹ thuật chuẩn `analysis-report.md`.

---

## 2. Existing Resources Audit

Các tài nguyên nghiệp vụ của `ba-analyst` đã được chuyển dịch sang bối cảnh cục bộ:

| Đường dẫn tài nguyên | Nội dung tóm tắt | Vai trò trong thiết kế |
|----------------------|------------------|------------------------|
| [`01-classification-rules-extracted.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-analyst/resources/01-classification-rules-extracted.md) | Các quy tắc phân loại FR/NFR, MoSCoW priority matrix. | Hướng dẫn Agent phân loại và xếp độ ưu tiên yêu cầu. |
| [`02-mermaid-syntax-reference.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-analyst/resources/02-mermaid-syntax-reference.md) | Cú pháp Mermaid.js chuẩn cho Sequence, Flowchart và ERD, cùng các ràng buộc kỹ thuật (≥ 3 actors, zero placeholder). | Chuẩn hóa cú pháp vẽ sơ đồ, giảm thiểu lỗi render. |
| [`03-gherkin-guide-mined.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-analyst/resources/03-gherkin-guide-mined.md) | Định dạng Given-When-Then, số lượng scenario tối thiểu (≥3: Happy, Alternative, Exception paths). | Hướng dẫn viết test cases chuẩn Gherkin. |
| [`04-risk-assessment-framework.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-analyst/resources/04-risk-assessment-framework.md) | Ma trận Rủi ro (Xác suất x Mức ảnh hưởng) và liên kết với MoSCoW priority. | Hướng dẫn Agent phân tích rủi ro và giải pháp giảm thiểu. |
| [`05-data-schema-patterns.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-analyst/resources/05-data-schema-patterns.md) | 7 Deliverables bắt buộc và Schema cấu trúc hóa đầu ra. | Định hình cấu trúc và kiểm soát chất lượng file output. |
| [`06-scope-definition.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-analyst/resources/06-scope-definition.md) | Ranh giới, dependencies, và phân tích rủi ro lệch pha handoff từ `ba-elicitor`. | Xác định điểm liên kết và giải quyết lệch pha dữ liệu. |

---

## 3. Seven Golden Standards Assessment

### A. Khả năng tái sử dụng (Reusability) — ✅ Rich
- Kỹ năng phân tích, phân loại MoSCoW, mô hình hóa hệ thống bằng Mermaid.js và viết Gherkin scenarios là hoàn toàn độc lập với ngôn ngữ lập trình hay công nghệ.

### B. Khả năng kết hợp (Composability) — ✅ Rich
- Nhận input từ `ba-elicitor` (`elicitation-report.md`) và xuất ra `analysis-report.md` làm đầu vào trực tiếp cho `ba-synthesizer`. Tương tác hoàn toàn qua các file trạng thái trong `.skill-context/`.

### C. Khả năng bảo trì (Maintainability) — ✅ Rich
- Phân tách 7 Zones rõ ràng. Khi cú pháp Mermaid.js hoặc tiêu chuẩn viết Gherkin thay đổi, chỉ cần cập nhật các file tri thức tương ứng trong `resources/`.

### D. Độ an toàn và bảo mật (Security) — ✅ Rich
- Phân tích nghiệp vụ thuần túy, không thực thi shell commands hay code bên thứ ba.
- Rủi ro duy nhất: Lỗi render Mermaid.js, giải quyết bằng việc nạp các cú pháp mẫu đã được kiểm chứng.

### E. Hiệu suất ngữ cảnh (Context Efficiency) — ✅ Rich
- Áp dụng Progressive Disclosure: Chỉ nạp tri thức vẽ Mermaid hoặc viết Gherkin khi bắt đầu pha tương ứng, giúp giảm thiểu token của mỗi lượt tương tác của Agent.

### F. Tính di động (Portability) — ✅ Rich
- Định dạng Markdown/YAML chuẩn hóa, hoạt động tốt trên mọi nền tảng Agent AI hỗ trợ Skill Files.

### G. Độ tin cậy & Luồng dự phòng (Reliability & Fallback) — ✅ Rich
- Giải quyết rủi ro lệch pha Frontmatter từ `ba-elicitor` bằng bộ quy tắc tự động căn chỉnh (alignment rules).
- Nếu phát hiện cú pháp Mermaid bị lỗi, Agent sẽ tự động chạy vòng lặp kiểm tra và tự sửa đổi (Self-correct loop).

---

## 4. AI Instruction Standards & Rules

```yaml
rules_for_analyst:
  must:
    - Tiếp nhận duy nhất file .skill-context/ba-elicitor/elicitation-report.md làm đầu vào
    - Thực hiện bước tự động sửa đổi lệch pha (Frontmatter Alignment): ánh xạ analyzed_at -> elicited_at và normalize status trước khi chạy tiếp
    - Xuất đầy đủ 7 deliverables cam kết tại đầu ra .skill-context/ba-analyst/analysis-report.md
    - Viết Tiếng Việt cho các phần giải thích, bảng phân loại, bảng rủi ro
    - Viết Tiếng Anh cho nhãn sơ đồ Mermaid, Gherkin Scenarios, và data types
    - Mọi Mermaid diagram phải có cấu trúc validated và không chứa bất kỳ placeholder (TODO, TBD) nào
    - Gắn trace tags đầy đủ: [TỪ ELICITOR], [SUY LUẬN], [CẦN LÀM RÕ]
  must_not:
    - Bỏ qua bất kỳ deliverable nào trong số 7 deliverables bắt buộc
    - Tự ý suy đoán cấu trúc dữ liệu (Data Schema) phức tạp khi không có cơ sở nghiệp vụ
    - Bỏ sót luồng Exception Path khi vẽ Sequence/Flowchart hoặc viết Gherkin scenarios
```

---

## 5. Process Flow & Automation Mapping

```
[elicitation-report.md] 
      │
      ▼
[1. Frontmatter Alignment] ── (Sửa lệch pha: analyzed_at -> elicited_at, status map)
      │
      ▼
[2. Requirements Classification] ── (Phân loại FR/NFR & MoSCoW priority)
      │
      ▼
[3. System Modeling] ── (Sinh 3 sơ đồ Mermaid: Sequence, Flowchart, ERD)
      │
      ▼
[4. Data Schema Design] ── (Định nghĩa kiểu dữ liệu & ràng buộc thực thể)
      │
      ▼
[5. Acceptance Criteria] ── (Viết ≥ 3 kịch bản Gherkin)
      │
      ▼
[6. Risk Assessment Matrix] ── (Lập ma trận rủi ro & giải pháp)
      │
      ▼
[7. Đóng gói Report] ──► (Kiểm tra chất lượng & ghi file analysis-report.md)
```

---

## 6. Architectural Recommendations

Đề xuất quy hoạch 7 Zones cho `ba-analyst` khi build:

| Zone | File đề xuất | Vai trò / Nội dung | Bắt buộc? |
|------|--------------|---------------------|-----------:|
| Core | `SKILL.md` | Persona Analyst, quy trình 7 pha phân tích, instructions chính | ✅ |
| Knowledge | `knowledge/classification-rules.md` | Quy tắc phân loại FR/NFR và MoSCoW prioritization matrix | ✅ |
| Knowledge | `knowledge/mermaid-syntax.md` | Tiêu chuẩn vẽ sơ đồ Mermaid.js cho Sequence, Flowchart, ERD | ✅ |
| Knowledge | `knowledge/gherkin-guide.md` | Chuẩn viết Acceptance Criteria dạng Given-When-Then | ✅ |
| Knowledge | `knowledge/risk-assessment.md` | Khung phân tích rủi ro và tác động | ✅ |
| Templates | `templates/analysis-report.md.template` | Mẫu cấu trúc chuẩn cho analysis-report.md | ✅ |
| Loop | `loop/analyst-checklist.md` | Checklist tự kiểm định 7 deliverables trước khi xuất xưởng | ✅ |

---

## 7. Risks & Open Questions

### A. Bảng rủi ro & Giải pháp giảm thiểu
| # | Rủi ro tiềm ẩn | Mức độ | Giải pháp giảm thiểu |
|---|----------------|--------|---------------------|
| 1 | Lệch pha trường dữ liệu từ Elicitor gây lỗi parsing | Cao | Tích hợp pha "Frontmatter Alignment" ở đầu quy trình xử lý của Analyst. |
| 2 | Sơ đồ Mermaid lỗi cú pháp | Cao | Nạp các pattern cú pháp hợp lệ vào `knowledge/mermaid-syntax.md`; cấm các ký tự đặc biệt không bọc ngoặc kép. |
| 3 | Mất liên kết nghiệp vụ (Traceability) | Trung bình | Yêu cầu gắn trace tag cho từng thực thể trong data schema và kịch bản Gherkin ngược về Elicitor report. |

### B. Các câu hỏi mở (Open Questions)
1. **[CẦN XÁC NHẬN]**: Cú pháp Mermaid ERD trong các Agent thường có sự khác biệt nhẹ, có nên sử dụng JSON Schema làm định dạng cấu trúc dữ liệu chuẩn thay thế?
   * *Giải pháp tạm thời*: Sử dụng song song cả hai: Sơ đồ ERD trực quan bằng Mermaid và bảng chi tiết thuộc tính kiểu dữ liệu bằng Markdown table để đảm bảo độ tin cậy.

---

## 8. Production Quality Criteria

Các tiêu chí chất lượng bắt buộc phải đạt cho `ba-analyst` (MS-2):
- **Q1**: Đầu ra `analysis-report.md` phải có đầy đủ 7 phần (deliverables) không được khuyết thiếu bất kỳ phần nào.
- **Q2**: `SKILL.md` của `ba-analyst` không vượt quá 600 tokens (L0 anchor).
- **Q3**: Toàn bộ sơ đồ Mermaid phải được validate cú pháp hợp lệ, không chứa ký tự lỗi hay placeholder.
- **Q4**: Acceptance Criteria phải phủ đủ 3 luồng (Happy, Alternative, Exception) với cú pháp Gherkin chuẩn xác.
- **Q5**: Có trace tag chi tiết ánh xạ ngược về `elicitation-report.md`.

---

## 9. Metadata

- **Skill Name**: ba-analyst
- **Stage**: exploration (Stage 0)
- **Pipeline Position**: Stage -1 (MS-2)
- **Handoff Target**: skill-architect (Stage 1)
- **State Ledger**: `.skill-context/ba-analyst/`
