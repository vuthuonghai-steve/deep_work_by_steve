# Plan Quality & Resource Checklist

> Dùng trong Step VERIFY của Skill Planner

## 1. Resource Verification (Cốt lõi)

- [ ] **Existence**: Mọi tài nguyên liệt kê trong `todo.md` §Pre-requisites đều có file tương ứng trong `resources/`.
- [ ] **Richness**: Tài liệu trong `resources/` không phải là file rỗng. Có đủ thông tin "hành động được" (actionable).
- [ ] **Traceability**: `todo.md` chỉ ra rõ task nào sử dụng tài nguyên nào tại §3 Knowledge & Resources.

## 2. Structure & Standard Alignment

- [ ] **7-Zone Check**: Kế hoạch có bao phủ đủ các Zone quan trọng đã định nghĩa trong `design.md §3`.
- [ ] **Phase Order**: Các phase được sắp xếp theo trình tự logic (Knowledge/Audit → Setup → Build → Verify).
- [ ] **Trace Tag Check**: Mọi task đều có tag `[TỪ DESIGN]`, `[GỢI Ý]`, hoặc `[TỪ AUDIT]`.

## 3. Definition of Done (DoD)

- [ ] DoD có bao gồm tiêu chí về chất lượng tài nguyên kiến thức không?
- [ ] DoD có yêu cầu Builder phải chạy script verify trước khi bàn giao không?

## 4. Gatekeeper Rule

- [ ] Planner có đang để trạng thái `🟢 COMPLETE` trong khi tài nguyên quan trọng vẫn là `⬜ Missing` không? (NẾU CÓ -> Chuyển về `⚪ PENDING`).
