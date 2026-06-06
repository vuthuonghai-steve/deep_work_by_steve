---
skill_name: "ba-synthesizer"
version: "1.0.0"
artifact_type: "criteria"
created_at: "2026-06-06"
---

# 🎯 Tiêu Chí Nghiệm Thu & Kịch Bản Kiểm Thử: ba-synthesizer

Tài liệu này xác định các tiêu chí chất lượng và kịch bản chạy thử để nghiệm nghiệm thu micro-skill `ba-synthesizer` (MS-3).

---

## 1. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

| ID | Tiêu chí chất lượng | Chi tiết yêu cầu | Loại |
|:---|:---|:---|:---|
| **AC-1** | Kiểm định chéo SD-ERD | Quét và phát hiện lỗi mâu thuẫn nghiệp vụ nếu Sequence Diagram gọi thực thể không có trong ERD. | Must |
| **AC-2** | Kiểm định chéo MoSCoW-Gherkin | Phát hiện và cảnh báo nếu một yêu cầu `Must-Have` không có kịch bản kiểm thử Gherkin tương ứng. | Must |
| **AC-3** | Điểm chất lượng Weighted | Tính điểm chất lượng dựa trên ma trận weighted sum của 7 deliverables và xếp loại PASS/WARNING chính xác. | Must |
| **AC-4** | YAML Handoff Metadata | Đầu ra `business-analysis.md` phải có YAML frontmatter chứa đủ trường: SCS score, decomposition recommend, quality status, và quality score. | Must |
| **AC-5** | Hợp nhất tài liệu | Hợp nhất thành công 2 báo cáo thô thành một file duy nhất sạch sẽ, không có TODO/TBD hay placeholder. | Must |
| **AC-6** | Traceability | Toàn bộ tài liệu hợp nhất phải bảo toàn trace tags nghiệp vụ. | Must |

---

## 2. Kịch Bản Kiểm Thử (Test Scenarios)

### Kịch bản 1: Đầu vào hoàn toàn nhất quán (Happy Path)

- **Đầu vào (Input)**:
  `elicitation-report.md` và `analysis-report.md` hợp lệ, trong đó:
  - Sequence Diagram gọi các actors: User, backup-script, PostgresDB và thực thể `BackupJob`.
  - ERD chứa thực thể `BackupJob`.
  - Bảng MoSCoW chỉ có 1 Must-Have là `Tự động backup DB`.
  - Gherkin Acceptance Criteria chứa scenario `Happy Path - Backup thành công` tương ứng với tính năng backup.
  - Điểm tự đánh giá cho 7 deliverables đạt điểm tối đa (1.0).

- **Kết quả mong đợi (Expected Output)**:
  - Kiểm định chéo: Nhất quán 100%, không có tag cảnh báo.
  - Điểm chất lượng: 100% (PASS).
  - Đầu ra `business-analysis.md` có:
    - YAML frontmatter: `quality_gate_status: "PASS"`, `quality_score_percentage: 100.0`.
    - Toàn bộ nội dung của Elicitor và Analyst được hợp nhất mạch lạc.
    - Zero placeholders.

### Kịch bản 2: Phát hiện mâu thuẫn chéo giữa SD và ERD (Exception Path)

- **Đầu vào (Input)**:
  `elicitation-report.md` và `analysis-report.md` trong đó:
  - Sequence Diagram thể hiện tương tác: `PaymentGateway ──► TransactionTable: Save Transaction` (gọi thực thể `Transaction`).
  - Tuy nhiên, ERD chỉ định nghĩa thực thể `User` và `Product`, không có thực thể `Transaction`.
  - Các phần khác hợp lệ.

- **Kết quả mong đợi (Expected Output)**:
  - Kiểm định chéo: Phát hiện mâu thuẫn SD-ERD. Inject tag cảnh báo `[MAU THUẪN NGHIỆP VỤ: Thực thể Transaction xuất hiện trong Sequence Diagram nhưng thiếu trong CSDL ERD]` vào báo cáo.
  - Tính điểm chất lượng: Điểm của deliverable `erd_schema` bị trừ nặng (ví dụ: chỉ đạt 0.3/1.0). Điểm tổng hợp weighted sum bị kéo xuống dưới 80% (ví dụ: đạt 75%).
  - Đầu ra `business-analysis.md` có:
    - YAML frontmatter: `quality_gate_status: "WARNING"`, `quality_score_percentage: 75.0`.
    - Phần "Kết quả kiểm định chéo" ghi nhận rõ ràng lỗi mâu thuẫn trên.
