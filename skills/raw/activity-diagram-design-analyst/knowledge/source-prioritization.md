# Source Prioritization & Conflict Resolution Guide
> **Usage**: Hướng dẫn thứ tự ưu tiên khi tiếp nhận dữ liệu từ nhiều nguồn khác nhau để đảm bảo sơ đồ phản ánh đúng nhất thực tế nghiệp vụ và chống ảo giác (Anti-hallucination).

---

## 1. Thứ tự ưu tiên (Taxonomy of Truth)
1. **User Current Intent (P0)**: Các yêu cầu, đính chính hoặc giả định trực tiếp từ người dùng trong phiên hội thoại hiện tại.
2. **Project Specification (P1)**: Tài liệu đặc tả Use Case, Business Rules chính thức trong repository.
3. **Reference Data (P2)**: Các file YAML trong `data/` (Rules, Severity) và Knowledge Base của skill.
4. **Existing Artifacts (P3)**: Sơ đồ Mermaid hiện có (nếu đang ở Mode B).
5. **Heuristic/General Knowledge (P4)**: Kiến thức ngành phổ thông (Sẽ được gắn nhãn giả định).

---

## 2. Quy tắc ghi nhãn Traceability (Evidence Tagging)
Để đảm bảo tính minh bạch, mọi Node và Finding phải được gắn nhãn nguồn gốc:
- `[TỪ USER]`: Trích dẫn trực tiếp từ yêu cầu chat.
- `[TỪ SPECS]`: Dựa trên nội dung trong tài liệu đặc tả (Vd: `use-case.md`).
- `[TỪ THIẾT KẾ]`: Dựa trên logic UML chuẩn (Vd: "Thêm Merge để tránh Deadlock").
- `[CẦN LÀM RÕ]`: Khi dữ liệu bị thiếu hoặc có sự mâu thuẫn cao.

---

## 3. Quy trình Xử lý mâu thuẫn (Conflict Resolution)

### Kịch bản A: User mâu thuẫn với Specs
- **Hành động**: Ưu tiên **User Intent** nhưng **BẮT BUỘC** phải ghi chú lại điểm mâu thuẫn này vào mục *Assumptions & Questions* để người dùng xác nhận lại một lần nữa.
- **Tag**: `[ƯU TIÊN USER - Mâu thuẫn với SPECS]`

### Kịch bản B: Diagram hiện có mâu thuẫn với UML Semantics
- **Hành động**: Ưu tiên **UML Rules** (để đảm bảo sơ đồ chạy được). Giải thích rõ lỗi kỹ thuật (Vd: CF-01) và cách refactor.
- **Tag**: `[SỬA LỖI SEMANTICS]`

### Kịch bản C: Thếu thông tin (Missing Link)
- **Hành động**: Không được tự ý "bịa" nghiệp vụ. Hãy sử dụng giá trị mặc định của hệ thống (nếu biết) hoặc đánh dấu `[MISSING_DOMAIN_DATA]` và chuyển sang Interaction Gate để hỏi.

---

## 4. Confidence Gate (Guardrail G5)
- Nếu việc hiểu luồng nghiệp vụ dựa trên các nguồn có độ tin cậy **< 70%**:
  - KHÔNG trả về Mermaid hoàn chỉnh ngay.
  - Hãy liệt kê các **Business Logic Gaps** và yêu cầu người dùng lấp đầy trước khi thiết kế.
