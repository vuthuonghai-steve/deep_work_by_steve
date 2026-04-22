# Mode B: Audit & Refactor Report
> **Source**: {{Original Diagram Reference}}

---

## 1. Analysis Result (Findings)
{{Sử dụng nội dung từ findings-report.template.md để liệt kê lỗi theo mức độ Critical, Major, Minor.}}

---

## 2. Refactored Diagram (Proposed)
```mermaid
flowchart TD
    %% Sơ đồ đã được refactor để sửa các lỗi CF-01, PL-01, RS-01...
    %% Áp dụng Clean Architecture Lens
```

---

## 3. Compare & Contrast
| Aspect | Before (Risk) | After (Mitigation) |
| :--- | :--- | :--- |
| **Logic** | {{Lỗi logic/Semantics}} | {{Cách sửa lỗi}} |
| **Layering** | {{UI/DB Driven}} | {{B-U-E Alignment}} |
| **Domain** | {{Missing Rules}} | {{Rule Gates Added}} |

---

## 4. Refactor Log (Traceability)
- **Change RS-01**: Chuyển action X từ Lane User sang Lane Domain để bảo vệ nghiệp vụ.
- **Change CF-01**: Thêm Merge Node tại điểm gộp luồng Y để tránh Implicit AND Deadlock.
- **Change EX-01**: Bổ sung nhánh lỗi cho kịch bản Z theo Use Case Spec.
