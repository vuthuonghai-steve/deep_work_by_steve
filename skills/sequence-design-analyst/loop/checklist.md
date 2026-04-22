# Sequence Quality Checklist

Sử dụng bảng này để hậu kiểm sơ đồ đã vẽ. Mỗi tiêu chí phải đạt trạng thái ✅.

| ID | Tiêu chí | Mô tả | Trạng thái |
|---|---|---|---|
| QC01 | **Scenario Base** | Sơ đồ có tiêu đề và mô tả kịch bản cụ thể (success/fail). | ⬜ |
| QC02 | **No Skip DB** | Tuyệt đối không có mũi tên gọi trực tiếp từ UI vào Database. | ⬜ |
| QC03 | **Layer Order** | Lifelines sắp xếp đúng: Actor -> Page -> Service -> Payload -> DB. | ⬜ |
| QC04 | **Fragment Usage** | Sử dụng `alt`, `opt`, `loop` đúng mục đích UML. | ⬜ |
| QC05 | **Activation** | Sự kiện `activate/deactivate` thể hiện đúng vùng xử lý. | ⬜ |
| QC06 | **Naming Truth** | Tên các lifelines và messages khớp với codebase thực tế. | ⬜ |
| QC07 | **Verb + Object** | Label của message tuân thủ quy tắc Động từ + Tân ngữ. | ⬜ |
| QC08 | **Complexity Warn** | Cảnh báo nỗ lực đọc nếu lifeline > 8. | ⬜ |
| QC09 | **Payload CMS Logic** | Luồng dữ liệu đi qua `payload` client client API hoặc REST. | ⬜ |
| QC10 | **Mermaid Validity** | Code Mermaid không bị lỗi syntax khi render. | ⬜ |

---
*Fidelity Check: Đã đối soát 100% với uml-rules.md và project-patterns.md.*
