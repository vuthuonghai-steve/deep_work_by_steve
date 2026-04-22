# Activity Diagram Quality Checklist (High-Fidelity)

> **Mục tiêu**: Đảm bảo sơ đồ đạt chuẩn UML, logic nghiệp vụ phản biện chặt chẽ và tuân thủ Clean Architecture.

## 1. Kiểm tra Cấu trúc (Structural)
- [ ] Có đầy đủ Initial Node `((Start))` và ít nhất một Final Node `(((End)))`.
- [ ] Sử dụng đúng ký hiệu Mermaid: 
    - `[ ]` cho Action.
    - `{ }` cho Decision.
    - `(( ))` cho Fork/Join/Merge/Start.
    - `((( )))` cho Final.
- [ ] Mọi nút đều phải được kết nối (không có mẩu luồng bị mồ côi).
- [ ] Các mũi tên đi đúng chiều (Top-Down hoặc Left-Right).

## 2. Kiểm tra Ngữ nghĩa (Semantic & Logic)
- [ ] **CF-01 (Merge check)**: Mọi Decision rẽ nhánh đều được gộp lại bằng Merge Node trước khi vào luồng xử lý chung.
- [ ] **PL-01 (Parallel check)**: Fork Node chỉ dùng cho các hành động thực sự chạy đồng thời, không dùng cho lựa chọn (Choice).
- [ ] **DL-01 (Exhaustive check)**: Mọi Decision đều có ít nhất 2 nhánh rẽ bao phủ hết các trường hợp logic (VD: [Có]/[Không] hoặc [Hợp lệ]/[Lỗi]).
- [ ] Luồng ngoại lệ (Exception Path) được xử lý rõ ràng (Quay lại bắt đầu, Rollback, hoặc kết thúc an toàn).

## 3. Kiểm tra Clean Architecture (B-U-E)
- [ ] Chia Swimlane rõ ràng: **Actor**, **Application**, **Domain**, **External**.
- [ ] Kiểm tra trách nhiệm:
    - [ ] Lane **Actor**: Chỉ chứa các hành động tương tác (Input/Trigger).
    - [ ] Lane **Application**: Chứa logic điều phối và xác thực luồng.
    - [ ] Lane **Domain**: Chứa các Decision nghiệp vụ quan trọng và Business rules cốt lõi.
    - [ ] Lane **External**: Chỉ chứa các hành động I/O (Lưu DB, Gọi API, Gửi Mail).
- [ ] Không có các Action mang tính kỹ thuật UI (VD: "Mở Modal", "Hiển thị Spinner").

## 4. Kiểm tra Độ tin cậy (High-Fidelity & Traceability)
- [ ] Mọi Action/Decision Node đều có thể truy vết về một bước nhất định trong Context cung cấp.
- [ ] Các thuật ngữ nghiệp vụ được giữ nguyên hoặc dịch sát nghĩa (không dùng placeholder vô nghĩa).
- [ ] Các "Giả định" (Assumptions) được ghi chú rõ ràng cho người dùng.

## 5. Kiểm tra Cú pháp Kỹ thuật (Technical Mermaid Syntax)
- [ ] **TS-01 (Label Quoting)**: Tất cả các nhãn node (Action, Decision, Terminal) đều được bọc trong dấu ngoặc kép `""`.
- [ ] **TS-02 (Line Break)**: Không sử dụng `\n`, sử dụng thẻ `<br/>` để xuống dòng trong nhãn.
- [ ] **TS-03 (Special Characters)**: Kiểm tra các nhãn chứa dấu `()`, `:`, `?`, `_` đã được escaped hoặc bọc ngoặc kép an toàn chưa.

---
**Kết quả**: Nếu vi phạm bất kỳ mục nào ở phần 1, 2 hoặc 5 (mức Critical/Major), sơ đồ phải được Refactor lại.
