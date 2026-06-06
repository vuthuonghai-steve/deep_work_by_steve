---
skill_schema_version: "3.0.0"
artifact_type: "exploration"
skill_name: "ba-synthesizer"
generated_by: "skill-explorer"
generated_at: "2026-06-06T22:25:00+07:00"
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

# ba-synthesizer — Báo Cáo Khảo Sát Nghiệp Vụ & Khai Thác Tài Nguyên (Micro-Skill Synthesizer)

> **Ngày khảo sát**: 2026-06-06
> **Trạng thái**: Hoàn thành (`completed`)
> **Tài liệu cha**: `skill-business-analyst/exploration.md`
> **Mục tiêu**: Bóc tách tài liệu khảo sát và bối cảnh hoạt động độc lập cho micro-skill thứ ba (ba-synthesizer).

---

## 1. Pain Point & Core Objective

### A. Vấn đề thực tế (Pain Points)
1. **Thiếu sự nhất quán giữa các tài liệu nghiệp vụ**: Có sự mâu thuẫn chéo giữa thiết kế sơ đồ tương tác (Sequence Diagram) và thiết kế cơ sở dữ liệu (ERD) hoặc thiếu kịch bản kiểm thử (Gherkin Scenarios) cho các tính năng cốt lõi (Must-Have) nhưng không có cơ chế tự động phát hiện.
2. **Khó khăn trong tổng hợp thông tin**: Thiếu một bước hợp nhất tự động các báo cáo riêng lẻ từ Elicitor (Tư duy) và Analyst (Kiến thức/Kỹ năng) thành một tài liệu phân tích nghiệp vụ duy nhất (`business-analysis.md`).
3. **Thiếu chốt chặn chất lượng (Quality Gate) định lượng**: Chưa có cách tính điểm chất lượng (Quality Score) cụ thể dựa trên trọng số để đánh giá sự hoàn thiện của tài liệu nghiệp vụ trước khi chuyển giao sang Explorer (Stage 0).

### B. Mục tiêu tự động hóa (Core Objective)
Xây dựng micro-skill **ba-synthesizer** (MS-3) tại Stage -1 nhằm:
1. Tiếp nhận đồng thời hai báo cáo `elicitation-report.md` và `analysis-report.md`.
2. Thực hiện kiểm định nhất quán chéo (Cross-reference validation) giữa SD-ERD và MoSCoW-Gherkin.
3. Đánh giá chất lượng của toàn bộ 7 deliverables dựa trên ma trận chất lượng weighted sum (ngưỡng đạt là $\ge$ 80%).
4. Hợp nhất hai báo cáo thành tài liệu bàn giao duy nhất `business-analysis.md` kèm theo YAML frontmatter handoff metadata đầy đủ cho Explorer.

---

## 2. Existing Resources Audit

Các tài nguyên nghiệp vụ của `ba-synthesizer` đã được chuyển dịch sang bối cảnh cục bộ:

| Đường dẫn tài nguyên | Nội dung tóm tắt | Vai trò trong thiết kế |
|----------------------|------------------|------------------------|
| [`01-quality-matrix-extracted.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-synthesizer/resources/01-quality-matrix-extracted.md) | Ma trận trọng số chất lượng cho 7 deliverables và công thức tính điểm (Σ(weight × score)). | Định hình logic chấm điểm chất lượng tài liệu nghiệp vụ. |
| [`02-cross-ref-validation-rules.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-synthesizer/resources/02-cross-ref-validation-rules.md) | Các quy tắc kiểm định chéo SD-ERD và MoSCoW-Gherkin cùng hệ thống tag cảnh báo (`[MAU THUẪN NGHIỆP VỤ]`, `[THIẾU KỊCH BẢN KIỂM THỬ]`). | Hướng dẫn Agent kiểm định tính logic chéo của thiết kế. |
| [`03-handoff-metadata-schema.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-synthesizer/resources/03-handoff-metadata-schema.md) | Lược đồ dữ liệu YAML Frontmatter bàn giao và XML boundaries đầu vào. | Định nghĩa schema metadata đầu ra để handoff sang Stage 0. |
| [`04-scope-definition.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-synthesizer/resources/04-scope-definition.md) | Phạm vi, dependencies, bảng rủi ro, và kịch bản Gherkin cho chính synthesizer. | Xác định ranh giới và kiểm định chất lượng cho synthesizer. |

---

## 3. Seven Golden Standards Assessment

### A. Khả năng tái sử dụng (Reusability) — ✅ Rich
- Logic kiểm định chéo và hợp nhất tài liệu nghiệp vụ là hoàn toàn generic, áp dụng được cho mọi bộ tài liệu phân tích thiết kế của bất kỳ AI skill nào.

### B. Khả năng kết hợp (Composability) — ✅ Rich
- Đóng vai trò là chốt chặn cuối cùng (Stage -1 Gatekeeper) của suite BA. Nhận inputs từ MS-1 và MS-2, hợp nhất và ký số đầu ra `business-analysis.md` để tự động hóa bàn giao sang Explorer (Stage 0).

### C. Khả năng bảo trì (Maintainability) — ✅ Rich
- Các quy tắc kiểm định chéo, trọng số chất lượng được lưu trữ dưới dạng các files tri thức độc lập tại `resources/`, giúp cập nhật chất lượng nghiệp vụ dễ dàng mà không ảnh hưởng tới core logic.

### D. Độ an toàn và bảo mật (Security) — ✅ Rich
- Chạy phân tích văn bản tĩnh (Static Text Analysis), không thực thi mã nguồn hay shell commands, không có nguy cơ bảo mật hệ thống.

### E. Hiệu suất ngữ cảnh (Context Efficiency) — ✅ Rich
- Chỉ nạp các rules kiểm định chéo (cross-ref rules) và metadata schema khi thực sự bắt đầu pha kiểm định và pha viết metadata tương ứng.

### F. Tính di động (Portability) — ✅ Rich
- Cú pháp Markdown/YAML chuẩn hóa đảm bảo chạy mượt trên mọi môi trường Agent.

### G. Độ tin cậy & Luồng dự phòng (Reliability & Fallback) — ✅ Rich
- Khi phát hiện mâu thuẫn chéo nghiêm trọng, Agent sẽ không crash hệ thống mà chỉ đánh dấu trạng thái `quality_gate_status = WARNING`, kèm theo ghi chú lỗi để người dùng sửa đổi thủ công.

---

## 4. AI Instruction Standards & Rules

```yaml
rules_for_synthesizer:
  must:
    - Nhận đồng thời hai file .skill-context/ba-elicitor/elicitation-report.md và .skill-context/ba-analyst/analysis-report.md
    - Quét và đối chiếu chéo cấu trúc sơ đồ và độ ưu tiên theo đúng các quy tắc tại resources/02-cross-ref-validation-rules.md
    - Tính điểm chất lượng dựa trên ma trận weighted sum quy định tại resources/01-quality-matrix-extracted.md
    - Xuất báo cáo hợp nhất duy nhất business-analysis.md có YAML frontmatter đúng schema tại resources/03-handoff-metadata-schema.md
    - Viết Tiếng Việt cho phần tổng hợp giải thích và kết quả kiểm định chéo
    - Giữ nguyên tiếng Anh cho Technical Terms, nhãn sơ đồ, và Gherkin scenarios
    - Gắn tag cảnh báo thích hợp ([MAU THUẪN NGHIỆP VỤ], [THIẾU KỊCH BẢN KIỂM THỬ]) khi phát hiện sai lệch chéo
  must_not:
    - Tự động thay đổi nội dung kỹ thuật từ Elicitor và Analyst (chỉ merge, đánh giá chất lượng và ghi nhận mâu thuẫn)
    - Cho phép trạng thái PASS nếu điểm chất lượng weighted sum dưới 80% (buộc phải chuyển thành WARNING)
    - Bỏ sót bất kỳ rủi ro nào từ hai tài liệu thượng nguồn khi hợp nhất ma trận rủi ro
```

---

## 5. Process Flow & Automation Mapping

```
[elicitation-report.md] VÀ [analysis-report.md]
      │
      ▼
[1. Cross-Reference Validation] ── (Kiểm tra mâu thuẫn SD-ERD & MoSCoW-Gherkin)
      │
      ▼
[2. Quality Score Calculation] ── (Tính điểm theo trọng số cho 7 deliverables)
      │
      ▼
[3. Metadata Compilation] ── (Sinh YAML frontmatter handoff cho Explorer)
      │
      ▼
[4. Document Merger] ── (Hợp nhất 7 deliverables, chèn các tag cảnh báo nếu có)
      │
      ▼
[5. Đóng gói business-analysis.md] ──► (Ghi file bàn giao & hoàn tất Stage -1)
```

---

## 6. Architectural Recommendations

Đề xuất quy hoạch 7 Zones cho `ba-synthesizer` khi build:

| Zone | File đề xuất | Vai trò / Nội dung | Bắt buộc? |
|------|--------------|---------------------|-----------:|
| Core | `SKILL.md` | Persona Synthesizer, quy trình 4 pha hợp nhất, instructions chính | ✅ |
| Knowledge | `knowledge/quality-criteria.md` | Bộ tiêu chí chất lượng cho từng deliverable và trọng số tính điểm | ✅ |
| Knowledge | `knowledge/cross-ref-rules.md` | Các quy tắc logic kiểm định chéo và trigger cảnh báo | ✅ |
| Templates | `templates/business-analysis.md.template` | Mẫu cấu trúc chuẩn hợp nhất cho business-analysis.md | ✅ |
| Data | `data/quality-matrix.yaml` | Ma trận chất lượng định lượng dùng để tính điểm | ✅ |
| Loop | `loop/synthesizer-checklist.md` | Checklist kiểm tra tính toàn vẹn của metadata và tài liệu cuối | ✅ |

---

## 7. Risks & Open Questions

### A. Bảng rủi ro & Giải pháp giảm thiểu
| # | Rủi ro tiềm ẩn | Mức độ | Giải pháp giảm thiểu |
|---|----------------|--------|---------------------|
| 1 | Mâu thuẫn chéo bị bỏ qua do parser thô sơ | Cao | Sử dụng các regex có cấu trúc chặt chẽ để bóc tách Actor/Entity từ mã Mermaid.js; định dạng nhãn rõ ràng. |
| 2 | Tràn context window khi nạp cả 2 báo cáo lớn | Trung bình | Sequential pipeline — chỉ nạp báo cáo sau khi đã hoàn tất các bước phân tích đơn lẻ. |
| 3 | Lệch pha metadata bàn giao làm hỏng Explorer | Trung bình | Bắt buộc validate metadata đầu ra bằng loop checklist trước khi ghi đĩa. |

### B. Các câu hỏi mở (Open Questions)
1. **[CẦN XÁC NHẬN]**: Điểm chất lượng `quality_score_percentage` có nên được lưu vào cơ sở dữ liệu chung hay chỉ lưu trong file metadata?
   * *Giải pháp tạm thời*: Chỉ lưu tại file YAML frontmatter của `business-analysis.md` để đảm bảo tính tự đóng gói và dễ đọc.

---

## 8. Production Quality Criteria

Các tiêu chí chất lượng bắt buộc phải đạt cho `ba-synthesizer` (MS-3):
- **Q1**: Đầu ra `business-analysis.md` phải chứa đầy đủ YAML frontmatter với đầy đủ các trường handoff metadata.
- **Q2**: `SKILL.md` của `ba-synthesizer` không vượt quá 500 tokens (L0 anchor).
- **Q3**: Điểm chất lượng tính toán được phải phản ánh trung thực trạng thái tài liệu; nếu có tag lỗi -> chất lượng phải dưới 100%.
- **Q4**: Có phần "Kiểm định nhất quán chéo" (Cross-reference validation report) riêng biệt ghi nhận kết quả rà soát.

---

## 9. Metadata

- **Skill Name**: ba-synthesizer
- **Stage**: exploration (Stage 0)
- **Pipeline Position**: Stage -1 (MS-3)
- **Handoff Target**: skill-explorer (Stage 0)
- **State Ledger**: `.skill-context/ba-synthesizer/`
