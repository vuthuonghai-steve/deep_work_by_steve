---
skill_schema_version: "3.0.0"
artifact_type: "exploration"
skill_name: "ba-elicitor"
generated_by: "skill-explorer"
generated_at: "2026-06-06T22:05:00+07:00"
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

# ba-elicitor — Báo Cáo Khảo Sát Nghiệp Vụ & Khai Thác Tài Nguyên (Micro-Skill Elicitor)

> **Ngày khảo sát**: 2026-06-06
> **Trạng thái**: Hoàn thành (`completed`)
> **Tài liệu cha**: `skill-business-analyst/exploration.md`
> **Mục tiêu**: Chuyển đổi từ tài liệu khảo sát tổng thể sang bối cảnh độc lập cho micro-skill đầu tiên (ba-elicitor).

---

## 1. Pain Point & Core Objective

### A. Vấn đề thực tế (Pain Points)
1. **Yêu cầu ban đầu cực kỳ mơ hồ**: Người dùng hoặc AI Agent khi bắt đầu thiết kế skill thường đưa ra mô tả rất sơ sài (ví dụ: "mình muốn làm skill deploy", "skill review code").
2. **Thiếu thông tin kỹ thuật định lượng (NFR)**: Các yêu cầu cảm tính như "chạy nhanh", "mượt mà", "an toàn" không có metric đo lường cụ thể khiến các stage thiết kế (Architect) và lập kế hoạch (Planner) bị mất phương hướng.
3. **Mất mát thông tin và thiếu cấu trúc chuẩn**: Chưa có một bộ lọc chuẩn hóa ở đầu vào để bóc tách thông tin thô thành các trường mục rõ ràng và phát hiện các khoảng trống thông tin (gap analysis).

### B. Mục tiêu tự động hóa (Core Objective)
Xây dựng micro-skill **ba-elicitor** hoạt động tại **Stage -1** (filter đầu tiên của pipeline) nhằm:
1. Tiếp nhận mọi yêu cầu tạo skill dạng tự do (raw text) hoặc YAML có cấu trúc.
2. Áp dụng các từ khóa tư duy cốt lõi (Systems Thinking, Root Cause, MECE, First Principles, Impact Analysis, Structural Decomposition) để phân tích khoảng trống nghiệp vụ.
3. Thực hiện phản biện chủ động, yêu cầu làm rõ (elicit) thông tin cảm tính bằng bộ câu hỏi 5W1H và phân rã quy trình thành 3 luồng (Happy, Alternative, Exception paths).
4. Xuất ra tài liệu báo cáo khơi gợi chuẩn `elicitation-report.md` đóng vai trò là input đầu vào sạch cho `ba-analyst` (MS-2).

---

## 2. Existing Resources Audit

Bảng khảo sát tài nguyên nghiệp vụ dành riêng cho `ba-elicitor` đã được khai thác và chuyển dịch sang bối cảnh cục bộ:

| Đường dẫn tài nguyên | Nội dung tóm tắt | Vai trò trong thiết kế |
|----------------------|------------------|------------------------|
| [`01-mindset-keywords-extracted.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-elicitor/resources/01-mindset-keywords-extracted.md) | 6 từ khóa tư duy (Systems Thinking, Root Cause, MECE, First Principles, Impact Analysis, Structural Decomposition) kèm vector anchors. | Cung cấp tri thức tư duy cốt lõi để Agent suy luận. |
| [`02-elicitation-rules-mined.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-elicitor/resources/02-elicitation-rules-mined.md) | Các quy tắc chuẩn hóa đầu vào, quy tắc chống ảo tưởng (anti-hallucination) và điều kiện dừng (stop conditions). | Định hình các ràng buộc logic cứng cho Agent. |
| [`03-question-framework.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-elicitor/resources/03-question-framework.md) | Khung câu hỏi 5W1H và cơ chế phân tách 3 luồng (Happy/Alternative/Exception paths). | Cấu trúc hóa câu hỏi phản biện gửi cho người dùng. |
| [`04-normalization-logic.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-elicitor/resources/04-normalization-logic.md) | Logic chuẩn hóa và bóc tách thông tin thô từ XML boundary. | Hướng dẫn luồng xử lý dữ liệu đầu vào. |
| [`05-scope-definition.md`](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/ba-elicitor/resources/05-scope-definition.md) | Ranh giới bối cảnh, Input/Output contract và sơ đồ luồng hoạt động của ba-elicitor. | Xác định phạm vi và ràng buộc đầu ra cho sản phẩm. |

---

## 3. Seven Golden Standards Assessment

### A. Khả năng tái sử dụng (Reusability) — ✅ Rich
- Logic khơi gợi và phản biện của `ba-elicitor` là generic, không phụ thuộc vào bất kỳ bài toán nghiệp vụ cụ thể nào. Nó có thể áp dụng để khai thác thông tin cho mọi loại AI skill.

### B. Khả năng kết hợp (Composability) — ✅ Rich
- Đầu vào nhận free-text bọc trong `<user_skill_request>...</user_skill_request>`.
- Đầu ra xuất ra `elicitation-report.md` tại một thư mục bối cảnh thống nhất.
- Handoff trơn tru cho `ba-analyst` mà không có sự chồng chéo chức năng.

### C. Khả năng bảo trì (Maintainability) — ✅ Rich
- Tuân thủ cấu trúc Progressive Disclosure (L0: `SKILL.md`, L1: `resources/` chứa các tri thức nghiệp vụ). Dễ dàng cập nhật các quy tắc câu hỏi hoặc từ khóa tư duy mà không cần sửa đổi core instructions.

### D. Độ an toàn và bảo mật (Security) — ✅ Rich
- Rủi ro duy nhất là Prompt Injection qua input tự do của người dùng.
- Biện pháp giảm thiểu: Bắt buộc bọc input trong XML boundaries và thực hiện trích xuất gián tiếp, không bao giờ eval hoặc ghép chuỗi trực tiếp vào instructions.

### E. Hiệu suất ngữ cảnh (Context Efficiency) — ✅ Rich
- Kích thước `SKILL.md` dự kiến dưới 500 tokens. Các tri thức về từ khóa tư duy, quy tắc phản biện được nạp động từ thư mục `resources/` theo nhu cầu từng pha.

### F. Tính di động (Portability) — ✅ Rich
- Định dạng chuẩn YAML/Markdown, không sử dụng các tính năng gọi hàm (function calling) đặc thù của API của OpenAI hay Anthropic, hoàn toàn tương thích với Antigravity, Claude Code, Hermes.

### G. Độ tin cậy & Luồng dự phòng (Reliability & Fallback) — ✅ Rich
- Nếu độ tin cậy thông tin (confidence score) tính toán được dưới 60% hoặc input hoàn toàn không có nghĩa, Agent sẽ dừng lại, chuyển sang chế độ câu hỏi HITL (Human-in-the-loop) để làm rõ, tránh việc suy đoán bừa bãi.

---

## 4. AI Instruction Standards & Rules

```yaml
rules_for_elicitor:
  must:
    - Bọc mọi input thô từ người dùng trong thẻ XML <user_skill_request>...</user_skill_request>
    - Ghi output duy nhất vào đường dẫn .skill-context/ba-elicitor/elicitation-report.md
    - Sử dụng Tiếng Việt cho toàn bộ phần giải thích, phân tích khoảng trống và câu hỏi phản biện
    - Sử dụng Tiếng Anh cho các nhãn phân tách luồng (Happy Path, Alternative Path, Exception Path) và technical terms
    - Gắn trace tag rõ ràng cho mọi thông tin: [TỪ INPUT], [SUY LUẬN], [CẦN LÀM RÕ]
    - Áp dụng triệt để 6 từ khóa tư duy trong resources/01-mindset-keywords-extracted.md khi phân tích
  must_not:
    - Tự suy đoán hoặc giả định thông tin critical thiếu hụt mà không gắn tag [CẦN LÀM RÕ]
    - Chấp nhận các yêu cầu định tính/cảm tính (VD: "chạy nhanh") mà không yêu cầu metrics cụ thể (latency, throughput)
    - Ghép trực tiếp nội dung user request vào prompt logic của Agent
```

---

## 5. Process Flow & Automation Mapping

```
[User Input (Raw/Structured)] 
      │
      ▼ (Bọc XML Boundary)
[1. Chuẩn hóa & Bóc tách (Normalization)] ── (Loại bỏ nhiễu, mapping thực thể)
      │
      ▼
[2. Phân tích Khoảng trống (Gap Analysis)] ── (Áp dụng 6 Mindset Keywords, đánh giá NFR)
      │
      ▼ (Confidence < 60%?)
      ├─► Có ──► [3. Elicitation Questions] ──► (Sinh bộ câu hỏi 5W1H chuẩn hóa + options)
      └─► Không ─► [Tự động tiếp tục luồng]
      │
      ▼
[4. Đóng gói Report] ──► (Ghi file elicitation-report.md kèm Trace Tags)
```

---

## 6. Architectural Recommendations

Đề xuất quy hoạch 7 Zones cho `ba-elicitor` khi build:

| Zone | File đề xuất | Vai trò / Nội dung | Bắt buộc? |
|------|--------------|---------------------|-----------:|
| Core | `SKILL.md` | L0 Anchor: Persona Elicitor, quy trình 4 pha, guardrails chính | ✅ |
| Knowledge | `knowledge/mindset-keywords.md` | Chứa 6 từ khóa tư duy cốt lõi và các vector anchors | ✅ |
| Knowledge | `knowledge/elicitation-rules.md` | Quy tắc phản biện, bóc tách và phân tách luồng | ✅ |
| Templates | `templates/elicitation-report.md.template` | Mẫu cấu trúc chuẩn cho elicitation-report.md | ✅ |
| Data | `data/input-schema.yaml` | Schema cấu trúc hóa dữ liệu đầu vào (nếu có) | ❌ |
| Loop | `loop/elicitor-checklist.md` | Checklist tự kiểm định chất lượng trước khi bàn giao | ✅ |

---

## 7. Risks & Open Questions

### A. Bảng rủi ro & Giải pháp giảm thiểu
| # | Rủi ro tiềm ẩn | Mức độ | Giải pháp giảm thiểu |
|---|----------------|--------|---------------------|
| 1 | Input đầu vào quá ngắn hoặc rác (ví dụ: "chấm") | Cao | Nếu không trích xuất được core objective -> confidence = 0% -> dừng ngay và yêu cầu nhập lại rõ ràng. |
| 2 | Prompt Injection hoặc rò rỉ prompt | Cao | Sử dụng XML delimiters và không thực thi bất kỳ lệnh shell/script nào trong phase này. |
| 3 | Khách hàng không trả lời đầy đủ câu hỏi phản biện | Trung bình | One-shot mode: các câu hỏi được ghi lại dưới dạng checklist mở [CẦN LÀM RÕ] trong report để MS-2 tiếp tục xử lý với các giả định an toàn. |

### B. Các câu hỏi mở (Open Questions)
1. **[CẦN XÁC NHẬN]**: Cần thiết lập cơ chế tương tác đa phiên (multi-turn chat) cho bước khơi gợi hay chỉ sinh báo cáo một lần (one-shot report)?
   * *Giải pháp tạm thời*: Mặc định sinh `elicitation-report.md` một lần (one-shot) và để các câu hỏi ở dạng mở trong file để người dùng có thể tùy ý sửa đổi trực tiếp vào report trước khi chạy MS-2.

---

## 8. Production Quality Criteria

Các tiêu chí chất lượng bắt buộc phải đạt cho `ba-elicitor` (MS-1):
- **Q1**: YAML frontmatter đầy đủ trong sản phẩm đầu ra `elicitation-report.md` (bao gồm `skill_name`, `core_objective`, `confidence_score`).
- **Q2**: `SKILL.md` của `ba-elicitor` không vượt quá 500 tokens (L0 anchor).
- **Q3**: Mọi thông tin được phân tích phải được gắn trace tags chuẩn xác (`[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`).
- **Q4**: Không có bất kỳ placeholder (`TODO`, `TBD`, `pass`) nào trong các tài liệu hoặc mã nguồn của skill khi đóng gói.
- **Q5**: Elicitation questionnaire phải bao gồm đầy đủ 5W1H và tối thiểu 3 câu hỏi lượng hóa NFR.

---

## 9. Metadata

- **Skill Name**: ba-elicitor
- **Stage**: exploration (Stage 0)
- **Pipeline Position**: Stage -1 (MS-1)
- **Handoff Target**: skill-architect (Stage 1)
- **State Ledger**: `.skill-context/ba-elicitor/`
