# Flutter SDK Compatibility

> **Mục tiêu**: Xử lý các xung đột API do sự chênh lệch phiên bản Flutter SDK giữa Source project (thường là bản mới nhất) và Target project (bản production ổn định).

## 1. Nguyên tắc Khả năng Tương thích (Backward Compatibility)

- Khi AI Agent phát hiện một API hoặc thuộc tính UI không tồn tại trong Target project, KHÔNG ĐƯỢC đề xuất nâng cấp Flutter SDK.
- Giải pháp bắt buộc là: Tìm API tương đương (fallback) hỗ trợ trên phiên bản SDK cũ hơn đang được dùng ở Target project.

## 2. Các Case Xung đột Phổ biến và Cách Xử lý

| API mới (Source Project) | API cũ thay thế (Target Project) | Ghi chú |
| :--- | :--- | :--- |
| `Color.withValues(alpha: ...)` | `Color.withOpacity(...)` hoặc `.withAlpha(...)` | Đây là thay đổi rất phổ biến ở Flutter 3.27+. Hãy ưu tiên dùng `withOpacity` ở codebase cũ. |
| `ThemeData.useMaterial3: true` | Kiểm tra config của `tranphueco` | Nếu target project chưa bật Material 3, màu sắc và spacing của một số widget (Card, Button) sẽ khác. Agent cần chỉnh style thủ công (padding, shape, elevation) để giống UI Source thay vì bật cờ Material 3. |
| TextTheme properties mới | Sử dụng properties cũ | Ví dụ: `bodyMedium` thay cho `bodyText2` (nếu dự án Target đã migrate), hoặc ngược lại tùy thuộc vào version của Target. Agent nên scan một file UI có sẵn trong Target để xem pattern đang dùng là gì. |

## 3. Xử lý UI Packages khác biệt

Nếu Source project sử dụng các feature mới từ các package phổ biến (e.g., `cached_network_image`, `flutter_svg`), Agent phải kiểm tra phiên bản của package đó trong `pubspec.yaml` của Target project.
- Không dùng các tham số mới chưa được hỗ trợ ở bản cũ.
- Nếu thuộc tính UI đó quá quan trọng để tái tạo thiết kế, Agent nên tự viết một custom widget đơn giản thay vì bắt ép nâng cấp package.

---

## Reference Data

- **Data file**: `data/forbidden-patterns.yaml` → mục `dependency_patterns` (package version conflicts)
- **Data file**: `data/known-issues.yaml` — documented SDK compatibility issues and workarounds
- **Related knowledge**: `component-mapping-guide.md` — fallback widget strategies
- **Related knowledge**: `conversion-rules.md` — zero new dependencies constraint
