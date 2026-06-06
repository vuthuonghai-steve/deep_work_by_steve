---
skill_name: "ba-analyst"
version: "1.0.0"
artifact_type: "criteria"
created_at: "2026-06-06"
---

# 🎯 Tiêu Chí Nghiệm Thu & Kịch Bản Kiểm Thử: ba-analyst

Tài liệu này xác định các tiêu chí chất lượng và kịch bản chạy thử để nghiệm nghiệm thu micro-skill `ba-analyst` (MS-2).

---

## 1. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

| ID | Tiêu chí chất lượng | Chi tiết yêu cầu | Loại |
|:---|:---|:---|:---|
| **AC-1** | Alignment Handoff | Phát hiện và tự động điều chỉnh lệch pha frontmatter (`analyzed_at` -> `elicited_at` và status). | Must |
| **AC-2** | Phân loại & MoSCoW | 100% yêu cầu được phân loại thành FR/NFR định lượng và gán MoSCoW priority kèm lý do kỹ thuật rõ ràng. | Must |
| **AC-3** | Sơ đồ hệ thống | Sinh đủ 3 sơ đồ Mermaid: Sequence (>=3 actors), Flowchart (3 paths), ERD (có data type & PK/FK). | Must |
| **AC-4** | Acceptance Criteria | Viết ít nhất 3 kịch bản Given-When-Then chuẩn Gherkin đại diện cho 3 paths xử lý. | Must |
| **AC-5** | Ma trận Rủi ro | Lập bảng đánh giá rủi ro (Risk Matrix) gồm Mã rủi ro, Mô tả, Xác suất, Tác động và Giải pháp giảm thiểu. | Must |
| **AC-6** | Traceability | Toàn bộ thực thể trong data schema và scenario phải có trace tag gắn ngược về `elicitation-report.md`. | Must |

---

## 2. Kịch Bản Kiểm Thử (Test Scenarios)

### Kịch bản 1: Phân tích nghiệp vụ "Auto DB Backup to S3"

- **Đầu vào (Input)**:
  `elicitation-report.md` từ Elicitor với frontmatter:
  ```yaml
  skill_name: "auto-backup-db"
  analyzed_at: "2026-06-06"
  status: "completed"
  ```
  Nội dung bóc tách yêu cầu Postgres backup lúc 2:00 AM hằng ngày lên AWS S3, retention 30 ngày. Khoảng trống: Cần credential quản lý S3, cơ chế xử lý khi S3 lỗi.

- **Kết quả mong đợi (Expected Output)**:
  - Tự động align frontmatter sang `elicited_at: "2026-06-06"`.
  - Phân loại FR/NFR và MoSCoW:
    - *FR-1 (Must)*: Đọc DB Postgres và nén file backup.
    - *FR-2 (Must)*: Upload file nén lên AWS S3.
    - *NFR-1 (Should)*: Thời gian backup tối đa < 15 phút.
    - *NFR-2 (Should)*: Sử dụng AWS IAM role/secret key an toàn.
  - Sơ đồ Mermaid:
    - *Sequence*: User ──► backup-script ──► S3 ──► DB Postgres.
    - *Flowchart*: Happy (backup & upload thành công), Alternative (backup thành công, upload lần 2 thành công), Exception (DB backup lỗi hoặc S3 từ chối kết nối).
    - *ERD*: Thực thể `BackupJob` (id, status, file_size, created_at, s3_url).
  - Gherkin Scenarios:
    - Scenario Happy Path (backup & upload thành công).
    - Scenario Exception Path (S3 đầy bộ nhớ hoặc lỗi kết nối).
  - Risk Matrix: RR-01 (Lỗi rò rỉ credential AWS), RR-02 (DB quá dung lượng làm backup timeout).

### Kịch bản 2: Tiếp nhận Elicitor report có trạng thái `pending_clarification`

- **Đầu vào (Input)**:
  `elicitation-report.md` có:
  ```yaml
  skill_name: "deploy-service"
  analyzed_at: "2026-06-06"
  status: "pending_clarification"
  ```
- **Kết quả mong đợi (Expected Output)**:
  - Agent nhận diện trạng thái `pending_clarification` của Elicitor.
  - Dừng pipeline phân tích (Stop Condition kích hoạt).
  - Output ra file `analysis-report.md` với status là `pending_clarification` và ghi chú: `Chờ người dùng trả lời câu hỏi phản biện ở Elicitor stage.`
  - Không sinh sơ đồ hay data schema giả định.
