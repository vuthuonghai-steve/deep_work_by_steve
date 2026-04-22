# Refactor Risk Patterns for Activity Diagram (v2.0)

> **Usage Reference**: Bộ từ điển rủi ro này dùng để nhận diện các lỗi logic, sai lệch bản chất (Semantics) và rủi ro nghiệp vụ khi Audit hoặc Refactor sơ đồ (Mode B).

---

## 1. Catalog Pattern Chi tiết (Expert Classification)

### 2.1 Nhóm Control-flow (CF)
| ID | Tên Rủi Ro | Mô tả & Hệ quả | Cách Refactor |
|:---|:---|:---|:---|
| **CF-01** | **Implicit AND (Merge thiếu)** | 2+ nhánh đi vào 1 Action mà không qua Merge Node. Hệ quả: Bị treo luồng (Deadlock) vì chờ đủ token. | Thêm Diamond Node (Merge) để gộp luồng. |
| **CF-02** | **Lửng lơ (Missing Final)** | Luồng kết thúc mà không dẫn về Activity Final hoặc Flow Final. | Nối các nhánh kết thúc vào `(((End)))`. |
| **CF-03** | **Infinite Loop** | Một nhánh lỗi quay lại một điểm mà không có sự thay đổi trạng thái, gây lặp vô hạn. | Thêm bước "Xóa cache" hoặc "Reset form" trước khi quay lại. |

### 2.2 Nhóm Decision-logic (DL)
| ID | Tên Rủi Ro | Mô tả & Hệ quả | Cách Refactor |
|:---|:---|:---|:---|
| **DL-01** | **Missing Else** | Các nhánh rẽ không bao phủ hết các trường hợp (VD: chỉ có [Đúng]). | Bổ sung nhánh `[Sai]` hoặc `[Else]`. |
| **DL-02** | **Guard Mơ Hồ** | Dùng từ ngữ không mang tính định lượng hoặc nghiệp vụ (VD: [OK], [Làm tiếp]). | Đổi thành: [Hợp lệ], [Đủ số dư], [Admin duyệt]. |
| **DL-03** | **Logic mâu thuẫn** | Nhanh rẽ có Guard overlap (VD: `[x > 5]` và `[x < 10]`). | Chuẩn hóa lại điều kiện loại trừ tương hỗ. |

### 2.3 Nhóm Parallelism (PL)
| ID | Tên Rủi Ro | Mô tả & Hệ quả | Cách Refactor |
|:---|:---|:---|:---|
| **PL-01** | **Fork thay vì Decision** | Dùng thanh Fork cho việc chọn 1 trong N hướng. Gây sai bản chất (User sẽ phải làm cả N việc). | Thay thanh ngang bằng hình thoi Decision. |
| **PL-02** | **Join Deadlock** | Một nhánh đi vào Join nhưng bị chặn bởi logic rẽ phía trước. Luồng sẽ bị treo vĩnh viễn. | Chuyển sang dùng Merge nếu không thực sự cần đồng bộ song song. |

### 2.4 Nhóm Clean Architecture & Responsibility (RS)
| ID | Tên Rủi Ro | Mô tả & Hệ quả | Cách Refactor |
|:---|:---|:---|:---|
| **RS-01** | **Sai Lane Trách Nhiệm** | Logic DB nằm ở lane User, hoặc logic nghiệp vụ nằm ở lane External. | Di chuyển Action Node về đúng Swimlane (B-U-E). |
| **RS-02** | **UI-Driven Flow** | Chứa các Action như "Click nút", "Mở Popup". Hệ quả: Mất tính trừu tượng nghiệp vụ. | Đổi thành: "Yêu cầu đăng bài", "Hiển thị thông tin". |

---

## 2. Severity Matrix (Bảng đánh giá mức độ)

| Cấp độ | Định nghĩa | Hành động bắt buộc |
|:---|:---|:---|
| **🔴 Critical** | Gây Deadlock, sai Semantics UML nghiêm trọng, hoặc bỏ qua luật bảo mật/thanh toán. | Không được xuất bản sơ đồ. Phải sửa ngay. |
| **🟠 Major** | Sai Swimlane, thiếu luồng lỗi quan trọng, hoặc đặt tên action gây hiểu lầm nghiêm trọng. | Cần có ghi chú Findings và đề xuất phương án ưu tiên. |
| **🟡 Minor** | Lỗi naming, thiếu Flow Final (nhưng logic vẫn hiểu được), typo. | Ghi nhận trong báo cáo nhưng không chặn process. |

---

## 3. Playbook: Quy trình Audit chuyên sâu (6 Bước)

1. **Structural Scan**: Kiểm tra Initial/Final Nodes và tính liên tục của mũi tên.
2. **Semantic Check**: Đối chiếu Fork/Join và Decision/Merge. Tìm kiếm Deadlocks.
3. **B-U-E Alignment**: Review Swimlanes. Đảm bảo logic nghiệp vụ nằm ở lane Application/Domain.
4. **Exception Path Audit**: Kiểm tra mọi Branching. Đã có luồng cho trường hợp "Không/Lỗi" chưa?
5. **Traceability Trace**: Trình bày mỗi Node khớp với bước nào trong Use Case Spec.
6. **Findings Generation**: Sử dụng mã lỗi (CF-01...) để lập báo cáo theo template.
