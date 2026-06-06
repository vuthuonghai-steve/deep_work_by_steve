---
skill_name: "ba-elicitor"
version: "1.0.0"
artifact_type: "criteria"
created_at: "2026-06-06"
---

# 🎯 Tiêu Chí Nghiệm Thu & Kịch Bản Kiểm Thử: ba-elicitor

Tài liệu này xác định các tiêu chí chất lượng và kịch bản chạy thử để nghiệm nghiệm thu micro-skill `ba-elicitor` (MS-1).

---

## 1. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

| ID | Tiêu chí chất lượng | Chi tiết yêu cầu | Loại |
|:---|:---|:---|:---|
| **AC-1** | XML Boundary | Mọi input tự do phải được bọc và bóc tách từ thẻ `<user_skill_request>...</user_skill_request>`. | Must |
| **AC-2** | Phân tích Khoảng trống | Phát hiện ít nhất 3 khoảng trống nghiệp vụ hoặc yêu cầu cảm tính định tính. | Must |
| **AC-3** | Bộ câu hỏi 5W1H | Sinh đầy đủ câu hỏi 5W1H lượng hóa NFR định lượng kèm theo gợi ý lựa chọn (Multiple-choice). | Must |
| **AC-4** | Phân tách 3 Luồng | Phân tách nghiệp vụ thành 3 luồng rõ ràng: Happy Path, Alternative Path, Exception Path. | Must |
| **AC-5** | Cấu trúc State Ledger | Kết quả xuất ra đúng file `.skill-context/ba-elicitor/elicitation-report.md` với đầy đủ YAML frontmatter và trace tags. | Must |
| **AC-6** | Token Economics | Kích thước file `SKILL.md` của `ba-elicitor` sau khi build phải $\le$ 500 tokens. | Must |

---

## 2. Kịch Bản Kiểm Thử (Test Scenarios)

### Kịch bản 1: Tiếp nhận yêu cầu cảm tính mơ hồ (Hiệu năng)

- **Đầu vào (Input)**:
  ```xml
  <user_skill_request>
  Mình muốn tạo một skill có chức năng deploy mã nguồn tự động lên server. Yêu cầu hệ thống phải deploy thật nhanh và mượt mà, không bị lỗi.
  </user_skill_request>
  ```
- **Kết quả mong đợi (Expected Output)**:
  - Báo cáo normalized bóc tách được: `deploy mã nguồn tự động lên server`.
  - Phát hiện và phản biện từ khóa cảm tính: `deploy thật nhanh`, `mượt mà`, `không bị lỗi`.
  - Bộ câu hỏi 5W1H yêu cầu lượng hóa:
    - *How / What*: Định nghĩa "thật nhanh" (ví dụ: < 2 phút, < 5 phút?).
    - *Exception*: "không bị lỗi" nghĩa là tỷ lệ thành công bao nhiêu? Quy trình rollback tự động ra sao nếu lỗi?
    - *Where*: Deploy lên môi trường nào (Staging, Production)? Nhà cung cấp cloud là gì (AWS, Vercel, VPS)?
  - Phân tách luồng dự kiến:
    - *Happy Path*: Deploy thành công lên server.
    - *Alternative Path*: Deploy thành công từ nhánh phụ.
    - *Exception Path*: Deploy thất bại và tự động kích hoạt rollback.

### Kịch bản 2: Tiếp nhận yêu cầu có cấu trúc đầy đủ

- **Đầu vào (Input)**:
  ```xml
  <user_skill_request>
  skill_name: auto-backup-db
  core_objective: Tự động backup cơ sở dữ liệu PostgreSQL hàng ngày vào lúc 2 giờ sáng.
  destination: AWS S3 bucket
  retention: Lưu trữ trong vòng 30 ngày.
  </user_skill_request>
  ```
- **Kết quả mong đợi (Expected Output)**:
  - Báo cáo normalized ghi nhận đầy đủ cấu trúc có sẵn từ YAML.
  - Đánh giá khoảng trống (Gap Analysis):
    - Thiếu cơ chế thông báo khi backup xong hoặc khi lỗi (Slack, Email).
    - Thiếu cấu trúc lưu trữ và phân quyền IAM để ghi dữ liệu vào S3.
  - Sinh câu hỏi 5W1H lượng hóa:
    - *Who*: Agent sử dụng credential/secret key nào để truy cập S3?
    - *Exception*: Nếu S3 không khả dụng, DB backup có lưu tạm trên local host không?
  - Tích hợp trace tags đầy đủ: `[TỪ INPUT]`, `[SUY LUẬN]` thích hợp cho từng trường.
