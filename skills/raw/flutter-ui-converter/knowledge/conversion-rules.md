# Conversion Rules (Quy tắc Convert UI)

> **Mục tiêu**: Đảm bảo quá trình convert UI từ `tranphueco-redo-AI` sang `tranphueco` diễn ra an toàn, tuyệt đối không làm gãy vỡ (break) business logic hoặc cấu trúc project hiện tại.

## 1. UI-Only Constraint (Nguyên tắc Bất khả xâm phạm)

Skill này **CHỈ** được phép thay đổi Presentation Layer. 
Khi phân tích và generate code, Agent **TUYỆT ĐỐI KHÔNG**:
- Sửa đổi các file thuộc Data Layer (Models, Repositories, API Clients).
- Sửa đổi các hàm chứa Business Logic (hàm gọi API, hàm xử lý dữ liệu phức tạp).
- Đổi tên các biến state được sử dụng bởi hệ thống quản lý trạng thái.

**Dấu hiệu nhận biết Business Logic cần bảo tồn (READ-ONLY):**
- Hàm có từ khóa `async`, `await` gọi đến Service/Repository.
- Các hàm callback truyền dữ liệu quan trọng như `onSave`, `onSubmit`, `onDelete`.

## 2. Design System Alignment (Đồng bộ với DESIGN.md)

- Luôn đối chiếu với file `DESIGN.md` của dự án để sử dụng đúng bảng màu (`AppColors`), font chữ (`AppTextTheme`) và các hằng số thiết kế (`CommonConst`).
- Ưu tiên sử dụng các hằng số trong `DESIGN.md` thay vì hardcode giá trị HEX hoặc pixels.

## 3. Zero New Dependencies Constraint

Target project (`tranphueco`) là dự án production, mọi dependency mới đều mang lại rủi ro về conflict và security.
- **Không tự ý thêm thư viện mới** vào `pubspec.yaml` để phục vụ cho UI.
- Nếu Source project dùng một UI package không có trong Target project (ví dụ: `lucide_icons`), Agent phải tìm giải pháp thay thế tương đương bằng các thư viện đã có sẵn trong Target (ví dụ: dùng `Icons` mặc định của Material hoặc package icon đang có sẵn).
- Trong trường hợp bất khả kháng không thể thay thế, Agent **PHẢI** tạm dừng và hỏi ý kiến người dùng.

## 3. Preservation of File Structure

- Khi ghi đè file UI trong `tranphueco`, phải giữ nguyên cấu trúc thư mục hiện tại của màn hình đó.
- Không tự ý di chuyển file sang thư mục khác trừ khi có yêu cầu cụ thể từ người dùng.

## 4. Hardcoded Data Replacement
- Source project (`tranphueco-redo-AI`) thường chứa các dữ liệu mẫu (mock data) cứng trong giao diện.
- Khi mang UI sang Target project, Agent phải **bóc tách mock data** và gán lại các biến dữ liệu thật (từ Cubit/Bloc state) vào đúng vị trí UI tương ứng.

## 5. Traceability
- Bất cứ đoạn code nào có sự điều chỉnh đáng kể giữa Source và Target do xung đột logic/UI, Agent nên thêm một comment nhỏ bắt đầu bằng `// [CONVERTED]: ` để developer dễ dàng theo dõi.

---

## Reference Data

- **Data file**: `data/forbidden-patterns.yaml` — patterns cấm (business logic, dependencies, hardcoded values)
- **Data file**: `data/project-config.yaml` — project paths configuration
- **Template**: `templates/conversion-log.md.template` — conversion log output format
- **Related knowledge**: `state-management-preservation.md` — Bloc/Cubit preservation rules
- **Related knowledge**: `component-mapping-guide.md` — widget substitution guidelines
