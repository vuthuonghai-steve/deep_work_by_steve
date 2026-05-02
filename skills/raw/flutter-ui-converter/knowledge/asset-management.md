# Asset Management (Quản lý Tài nguyên)

> **Mục tiêu**: Đảm bảo tất cả hình ảnh, icon, font chữ được copy từ Source sang Target đúng quy chuẩn và hoạt động ổn định.

## 1. Quản lý Hình ảnh (Images & SVGs)

**Bất đồng bộ cấu trúc thư mục:**
Source project và Target project có thể có cấu trúc thư mục `assets/` khác nhau.
- *Ví dụ Source:* `assets/images/logo.png`
- *Ví dụ Target:* `assets/img/logo.png` hoặc `assets/images/core/logo.png`

**Quy tắc xử lý của AI Agent:**
1. Không copy mù quáng chuỗi path `Image.asset('path_tu_source')`.
2. Đối chiếu tên file hình ảnh. 
3. Kiểm tra xem hình ảnh đó đã tồn tại trong Target chưa. Nếu rồi, dùng path của Target.
4. Nếu hình ảnh hoàn toàn mới, Agent phải liệt kê nó vào "Asset Checklist" để báo cho người dùng copy file vật lý sang đúng cấu trúc của Target project, sau đó khai báo path mới vào code.

## 2. Icon Substitution (Thay thế Icon)

Rất nhiều Prototype UI sử dụng các bộ icon đẹp (như `lucide_icons`, `feather_icons`, `cupertino_icons`) nhưng Production app thường chuẩn hóa bằng 1 bộ duy nhất (như FontAwesome, Material Icons, hoặc Custom SVG).

- **Hạn chế add thêm thư viện icon:** Nếu Source dùng `lucide_icons` nhưng Target đang dùng Material Icons, AI phải tự động map `LucideIcons.home` sang `Icons.home_outlined`.
- Nếu icon là một custom SVG (`flutter_svg`), hãy đối xử với nó như một Image Asset (xem mục 1).

## 3. Khai báo Pubspec.yaml

Bất kỳ hình ảnh/font nào mới được mang từ Source sang Target đều phải được đảm bảo đã khai báo trong block `flutter: assets:` hoặc `flutter: fonts:` của `pubspec.yaml` ở Target project. Agent cần nhắc nhở User thông qua check-list Phase 1.

---

## Reference Data

- **Data file**: `data/widget-equivalents.yaml` — chứa icon substitution mappings
- **Forbidden patterns**: `data/forbidden-patterns.yaml` → mục `hardcoded_values` (asset path patterns)
- **Template**: `templates/asset-checklist.md.template` — template cho asset checklist output
- **Related knowledge**: `component-mapping-guide.md` — widget substitution rules
