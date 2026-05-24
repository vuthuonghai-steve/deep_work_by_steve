# Chắt Lọc Tri Thức: So Sánh & Lựa Chọn Định Dạng Tối Ưu Cho AI (Markdown vs YAML vs XML)

> **Mã tài nguyên**: KD-RES-01
> **Mục tiêu**: Hướng dẫn chi tiết cách AI agent lựa chọn và kết hợp các định dạng Markdown, YAML, và XML để biểu diễn tri thức một cách hiệu quả, rõ ràng, và tiết kiệm token nhất.

---

## 1. Bản chất Phản Ứng Ngữ Nghĩa của LLM

Các mô hình ngôn ngữ lớn (LLM) không biên dịch mã nguồn như trình biên dịch (compiler) truyền thống. Chúng hoạt động dựa trên:
1. **Mẫu cấu trúc đã học (Pattern Matching)**: Nhận diện các định dạng dữ liệu quen thuộc trong tập huấn luyện (Markdown, YAML, XML, JSON).
2. **Ranh giới ngữ nghĩa (Semantic Boundaries)**: Phân tách rõ ràng giữa đâu là chỉ thị điều khiển (instruction) và đâu là dữ liệu tham chiếu (context/input).
3. **Mức độ cô đọng (Token Economics)**: Hiệu quả sử dụng token để tránh pha loãng sự chú ý (attention dilution) của mô hình.

Vì vậy, một định dạng chắt lọc tri thức tốt không chỉ cần "đẹp" với mắt người, mà phải giúp AI trả lời nhanh 5 câu hỏi cốt lõi:
- Đây là **chỉ thị hành vi (mệnh lệnh)** hay **dữ liệu tham chiếu**?
- Đây là **luật bắt buộc (phải tuân thủ)** hay **gợi ý mềm (khuyến nghị)**?
- Dữ liệu này **luôn cần sử dụng** hay **chỉ nạp khi có ngữ cảnh cụ thể**?
- Phần nào là **ví dụ minh họa (example)**, phần nào là **tiêu chí nghiệm thu (acceptance criteria)**?
- Khi xảy ra xung đột hướng dẫn, **luật nào có ưu tiên cao hơn**?

---

## 2. Phân tích Sâu 3 Định Dạng Cốt Lõi

### A. Markdown — Định dạng dành cho Đọc Hiểu & Bối Cảnh Tự Nhiên

Markdown là ngôn ngữ đánh dấu siêu nhẹ, hoàn hảo để truyền tải các thông tin mang tính mô tả và giải thích.

*   **Trường hợp sử dụng tốt nhất (Use For)**:
    *   Tổng quan dự án (overview), lý do thiết kế (rationale).
    *   Giải thích kiến trúc (architecture explanation) và sơ đồ luồng dữ liệu (data flow).
    *   Tài liệu tích hợp thành viên mới (onboarding) và thuật ngữ chuyên ngành (glossary).
    *   Bảng so sánh đa chiều và ví dụ thực tế có giải thích chi tiết.
*   **Trường hợp nên tránh (Avoid For)**:
    *   Chứa danh sách luật cứng (hard rules) dày đặc không có schema rõ ràng. AI dễ coi các luật này như những đoạn văn mô tả mềm.
    *   Các checklist xác thực và quy trình kiểm duyệt (validation checklist).
*   **Mức tiêu thụ Token (Token Budget)**:
    *   *Light (Nhẹ)*: 100 - 400 tokens (Dưới 1,500 ký tự tiếng Việt) cho một mục giải thích ngắn.
    *   *Heavy (Nặng)*: 900 - 1800 tokens. Vượt quá ngưỡng này cần tách nhỏ tài liệu để tránh quá tải ngữ cảnh.

### B. YAML — Định dạng dành cho Luật Cứng, Policy & Cấu Hình Hành Vi

YAML cực kỳ mạnh mẽ trong việc thiết lập tư duy cấu hình cho AI. Nhờ cấu trúc Key-Value rõ ràng, nó buộc AI phải tuân thủ nghiêm ngặt các cặp thuộc tính.

*   **Trường hợp sử dụng tốt nhất (Use For)**:
    *   Quy định bắt buộc (`must`) và cấm kỵ (`must_not`).
    *   Danh sách công cụ được phép sử dụng (`allowed_tools`) và các mẫu bị cấm (`forbidden_patterns`).
    *   Hợp đồng đầu ra (`output_contract`) và tiêu chí nghiệm thu (`acceptance_criteria`).
    *   Điều kiện dừng (`stop_conditions`) và checklist xác thực (`validation_checklist`).
*   **Trường hợp nên tránh (Avoid For)**:
    *   Các đoạn văn mô tả dài (prose), lập luận dài dòng. Nhét văn xuôi vào YAML làm hỏng tính schema và gây khó khăn khi bảo trì.
    *   Cấu trúc lồng nhau quá sâu (quá 3-4 cấp độ lồng).
*   **Mức tiêu thụ Token (Token Budget)**:
    *   *Light*: 80 - 300 tokens cho một block cấu hình chuẩn.
    *   *Heavy*: 700 - 1200 tokens. Nếu vượt quá, AI sẽ bắt đầu lờ đi các key nằm sâu hoặc ở cuối danh sách.

### C. XML-like Tags — Định dạng Thiết Lập Ranh Giới Ngữ Nghĩa Cứng

Thẻ dạng XML (`<instructions>`, `<context>`, `<external_input>`) hoạt động như những bức tường ngăn cách tuyệt đối, giúp AI phân định rõ ràng các khối thông tin khác nhau.

*   **Trường hợp sử dụng tốt nhất (Use For)**:
    *   Phân tách rạch ròi giữa Chỉ thị hệ thống (System Instructions) và Dữ liệu từ bên ngoài (User Inputs/RAG/Web Docs) nhằm chống Prompt Injection.
    *   Bọc các khối ví dụ minh họa (`<examples>...</examples>`) để AI hiểu đây là dữ liệu tham chiếu chứ không phải lệnh thực thi trực tiếp.
    *   Đánh dấu các phần đầu ra cần phân tích tự động bằng công cụ (parser friendly).
*   **Trường hợp nên tránh (Avoid For)**:
    *   Bọc quá chi tiết (micro-tagging) từng dòng code hoặc từng câu ngắn làm loãng cấu trúc.
    *   Thay thế hoàn toàn cấu trúc Markdown hoặc YAML.
*   **Mức tiêu thụ Token (Token Budget)**:
    *   *Light*: 50 - 250 tokens cho cặp thẻ đóng mở bọc dữ liệu.
    *   *Heavy*: Trên 1500 tokens thường là do chứa dữ liệu thô quá lớn, cần áp dụng chắt lọc hoặc chunking trước khi bọc XML.

---

## 3. Ma Trận Phối Hợp Định Dạng (Hybrid Format Design)

Để chắt lọc tri thức đạt hiệu suất cao nhất, ta nên áp dụng thiết kế lai (Hybrid):

```markdown
# [MARKDOWN] Tiêu đề & Giải thích bối cảnh nghiệp vụ
Giới thiệu ngắn gọn cho AI hiểu "Tại sao" chúng ta cần làm nghiệp vụ này.

<instructions>
[XML] Bọc toàn bộ phần chỉ thị cốt lõi của hệ thống.
```

```yaml
# [YAML] Cấu hình quy tắc cứng bên trong thẻ XML
constraints:
  must:
    - Thực hiện bước A trước bước B.
  must_not:
    - Sử dụng thư viện ngoài không được duyệt.
```

```markdown
</instructions>

<examples>
[XML] Bọc các mẫu thực tế.
```

```javascript
// Mã mẫu minh họa pattern chuẩn
function runTask() { ... }
```

```markdown
</examples>
```

Sự phối hợp này mang lại 3 ưu điểm vượt trội:
1. **Phân tách trách nhiệm rõ ràng (Separation of Concerns)**: Markdown giải thích bối cảnh, YAML quản lý luật cứng, XML tạo ranh giới bảo mật.
2. **Kích hoạt đúng vùng tri thức**: Khi gặp cấu trúc YAML, AI tự động kích hoạt chế độ "tuân thủ luật" (rule-abiding mode). Khi gặp XML, nó hiểu đây là "hộp chứa dữ liệu" (data container).
3. **Dễ bảo trì và kiểm định tự động**: Con người có thể dùng schema validator (như JSON schema hoặc YAML linter) để quét các tệp cấu hình tri thức mà không bị nhiễu bởi các đoạn văn xuôi dài dòng.
