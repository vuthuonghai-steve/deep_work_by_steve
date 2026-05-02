# Component Mapping Guide

> **Mục tiêu**: Hướng dẫn AI Agent cách ánh xạ (map) các UI component từ Source project (`tranphueco-redo-AI`) sang các widget tương ứng trong Target project (`tranphueco`).

## 1. Nguyên tắc Ánh xạ Chung (General Mapping Principles)

- **Ưu tiên Native/Material/Cupertino widgets:** Nếu Source sử dụng một custom widget phức tạp chỉ để bọc styling, hãy kiểm tra xem Target có widget cơ bản nào đáp ứng được không (ví dụ: dùng `Container` thay cho một custom `CardView` nếu `CardView` không có sẵn trong Target).
- **Tuân thủ Design System của Target:** Nếu Target project có thư mục `widgets/` hoặc thư viện component nội bộ dùng chung, ưu tiên sử dụng chúng thay vì viết lại từ đầu.

## 2. Mapping Styling & Colors (Themes)

Tuyệt đối KHÔNG sử dụng mã màu hardcoded (ví dụ: `Color(0xFF123456)`).

**Quy tắc:**
- Source: Thường dùng mã hex trực tiếp hoặc custom colors cho prototype.
- Target: Luôn sử dụng Theme đang có sẵn, ví dụ: `Theme.of(context).colorScheme.primary` hoặc `AppColors.primary`.
- Khi mapping, AI Agent cần đối chiếu mã màu trong Source với bảng màu của Target để tìm ra Color constant phù hợp nhất.

## 3. Mapping Typography (Text Styles)

Tuyệt đối KHÔNG sử dụng `TextStyle` lặp lại nhiều lần với các thuộc tính hardcode (`fontSize`, `fontWeight`).

**Quy tắc:**
- Sử dụng TextTheme của Material: `Theme.of(context).textTheme.bodyLarge` hoặc các TextStyles custom có sẵn trong Target (ví dụ `AppTextStyles.heading1`).
- Nếu Source có một style không khớp hoàn toàn, hãy chọn style gần giống nhất trong Target thay vì tạo mới.

## 4. Widget Structure Substitution (Thay thế cấu trúc Widget)

| Source Pattern (tranphueco-redo-AI) | Target Equivalent (tranphueco) | Ghi chú |
| :--- | :--- | :--- |
| `LucideIcons.home` (hoặc package icon mới) | `Icons.home` (Material Icons) | Tránh cài thêm package icon. |
| Custom Button tự build (InkWell + Container) | `ElevatedButton`, `TextButton`, hoặc Custom Button component có sẵn của Target | Khuyến khích tái sử dụng Button component của dự án. |
| Padding tĩnh (e.g., `Padding(padding: EdgeInsets.all(16))`) | `Padding` hoặc `SizedBox` | Ưu tiên dùng các constant spacing nếu Target có (e.g., `AppSpacing.p16`). |

## 5. Xử lý Component không tồn tại trong Target

- **Trường hợp 1:** Component đó chỉ là UI đơn giản (hiển thị) -> Copy toàn bộ code UI của component đó sang Target, đổi tên và đưa vào thư mục `widgets/` hợp lý.
- **Trường hợp 2:** Component đó chứa logic phức tạp hoặc phụ thuộc thư viện thứ 3 -> Báo cáo rủi ro (Risk) cho User và không tự ý copy.

---

## Reference Data

- **Data file**: `data/widget-equivalents.yaml` — chứa bảng ánh xạ icon và widget substitution
- **Data file**: `data/theme-mapping-rules.yaml` — quy tắc mapping colors và text styles
- **Forbidden patterns**: `data/forbidden-patterns.yaml` → mục `dependency_patterns` (icon packages)
- **Related knowledge**: `flutter-ui-patterns.md` — cấu trúc widget tree cơ bản
