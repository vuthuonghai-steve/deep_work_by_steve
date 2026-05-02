# Findings Report: Activity Diagram Analysis
> **Trace Target**: Tài liệu này liên kết trực tiếp với `data/rules.yaml` và `data/severity-matrix.yaml`.

---

## 1. Quality Summary
- **Evaluation Time**: {{current_time}}
- **Quality Band**: [Excellent | Acceptable | Risky | Blocked]
- **Final Score**: {{calculated_score}} / 100
- **Pass Gate**: [PASSED | FAILED]

---

## 2. Issues by Severity

### 🔴 Critical Findings (Penalty: -20đ/lỗi)
| Rule ID | Finding | Consequence | Refactor Suggestion | Trace |
| :--- | :--- | :--- | :--- | :--- |
| {{Rule_ID}} | {{Mô tả lỗi cụ thể trên sơ đồ}} | {{Gây Deadlock/Sai logic nghiệp vụ}} | {{Cách sửa dựa trên Rules.yaml}} | {{Trích từ context}} |

### 🟠 Major Findings (Penalty: -10đ/lỗi)
| Rule ID | Finding | Consequence | Refactor Suggestion | Trace |
| :--- | :--- | :--- | :--- | :--- |
| {{Rule_ID}} | {{Mô tả lỗi cụ thể trên sơ đồ}} | {{Dễ implement sai/Sai phân lớp}} | {{Cách sửa dựa trên Rules.yaml}} | {{Trích từ context}} |

### 🟡 Minor Findings (Penalty: -4đ/lỗi)
| Rule ID | Finding | Consequence | Refactor Suggestion | Trace |
| :--- | :--- | :--- | :--- | :--- |
| {{Rule_ID}} | {{Mô tả lỗi cụ thể trên sơ đồ}} | {{Khó đọc/Quy chuẩn naming}} | {{Cách sửa dựa trên Rules.yaml}} | {{Trích từ context}} |

---

## 3. Clean Architecture Guidance
{{Phân tích chi tiết về sự phân tách layers (B-U-E). Chỉ ra các điểm Action Node đang bị UI-Driven hoặc DB-Driven và hướng giải quyết.}}

---

## 4. Assumptions & Open Questions [CẦN LÀM RÕ]
- **Assumed Logic**: {{Các giả định về nghiệp vụ khi tài liệu context chưa rõ ràng.}}
- **User Questions**: {{Câu hỏi cụ thể để hoàn thiện sơ đồ.}}
