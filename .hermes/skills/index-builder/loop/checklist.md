# Bản Tự Kiểm Soát Chất Lượng QA — index-builder

> **Mã tài nguyên**: KD-QA-INDEX
> **Mục tiêu**: Bản tự kiểm tra bắt buộc dành cho AI Agent trước khi hoàn tất tác vụ tổng hợp chỉ mục và đồng bộ ngữ cảnh.

---

## 1. Xác Minh Cấu Trúc Chỉ Mục `llms.txt`

- [ ] **Định dạng Markdown**: Tệp `llms.txt` phải được ghi dưới định dạng Markdown chuẩn, sạch sẽ, không chứa các ký tự lạ hoặc lỗi font chữ.
- [ ] **Phân nhóm chính xác**: Các tài nguyên phải được phân tách rõ ràng vào đúng 3 nhóm:
  - `Core Guides (L0 & L1)`
  - `Domain Knowledge (L2)`
  - `Examples & Checklists (L3)`
- [ ] **Thống kê dung lượng**: Mỗi liên kết nên đi kèm thông tin dung lượng file (bytes) và ước tính token (ví dụ: `~450 tokens`).

---

## 2. Xác Minh Tính Chính Xác Của Liên Kết (Link Validation)

- [ ] **Không có liên kết chết (No Broken Links)**: Tất cả đường dẫn file trong `llms.txt` phải thực sự tồn tại trên đĩa. Không được phép có link trỏ tới file ảo hoặc đường dẫn sai.
- [ ] **Đường dẫn tương đối hợp lệ**: Các liên kết phải sử dụng đường dẫn tương đối từ gốc thư mục để đảm bảo tính di động khi chuyển đổi môi trường.
- [ ] **An toàn đường dẫn**: Đảm bảo không có đường dẫn nào cố tình truy cập ra ngoài phạm vi thư mục được phép (Path Traversal Protection).

---

## 3. Kiểm Soát Ngân Sách Token & Guardrails

- [ ] **Kích thước file llms.txt**: Tổng dung lượng tệp `llms.txt` được sinh ra phải dưới **1000 tokens** để tránh quá tải ngữ cảnh cho Agent đọc.
- [ ] **Không có Placeholder**: Tuyệt đối không chứa bất kỳ nội dung placeholder dạng `TODO`, `[chờ điền]`, hoặc `...` trong tệp chỉ mục.
- [ ] **Trạng thái Pipeline**: Chỉ thực hiện cập nhật `llms.txt` khi chắc chắn bước validation trước đó (`sandbox-validator`) đã thành công.

---

## 4. Xác Thực Trạng Thái Đóng Gói (Definition of Done)

- [ ] Đã chạy thành công script `scripts/build_index.py` mà không gặp bất kỳ lỗi runtime nào.
- [ ] Tệp `data/llms.txt` đã được sinh và cập nhật mới nhất.
- [ ] Đã kiểm tra tính đúng đắn của toàn bộ 7 Zones được quy hoạch trong `design.md`.
