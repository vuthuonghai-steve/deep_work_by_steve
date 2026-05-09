# Skill Registry

> **Mục đích:** Đăng ký và quản lý tất cả skills của dự án theo loại chức năng.
> **Đường dẫn:** `.skill-context/registry/`
> **Ngày tạo:** 2026-05-09

## Cấu trúc

```
registry/
├── README.md              # Index tổng quan
├── mobile/                # Skills cho nền tảng Mobile
│   ├── giao-dien.md       # Giao diện (UI/UX)
│   ├── pattern.md         # Pattern kiến trúc
│   ├── rule.md            # Rule/nguyên tắc
│   └── coding.md          # Coding/thực thi
├── web/                   # Skills cho nền tảng Web
│   ├── giao-dien.md       # Giao diện (UI/UX)
│   ├── pattern.md         # Pattern kiến trúc
│   ├── rule.md            # Rule/nguyên tắc
│   └── coding.md          # Coding/thực thi
└── thread/                # Skills bổ trợ AI (ngoài code)
    ├── session-learner.md # Trích xuất kiến thức từ session
    └── spec-generator.md  # Sinh feature specifications
```

## Trường thông tin đăng ký

Mỗi skill được đăng ký với các trường YAML sau:

| Field | Bắt buộc | Mô tả |
|-------|----------|-------|
| `name` | ✅ | Tên skill duy nhất |
| `status` | ✅ | `active` / `draft` / `archived` |
| `source` | ✅ | Đường dẫn gốc (file hoặc thư mục) |
| `context` | ✅ | Ngữ cảnh sử dụng / mục đích |
| `package` | ✅ | Đường dẫn package skill hoàn chỉnh |
| `runtime_target` | ✅ | Nền tảng đích (flutter, react-native, react, next.js, ...) |
| `last_verified` | ✅ | Ngày verify gần nhất (YYYY-MM-DD) |
| `known_gaps` | ✅ | Khoảng trống / hạn chế / TODO |

## Lifecycle

```
registry (đăng ký)
  │
  ▼
.skill-context/{name}/design.md (thiết kế)
  │
  ▼
.skill-context/{name}/todo.md (kế hoạch)
  │
  ▼
skills/rebuild/{name}/ (build)
  │
  ▼
install & sử dụng
```

## Thread Category

Skills trong `thread/` là các skill **bổ trợ cho AI**, không thuộc mobile hay web:

- **session-learner:** Trích xuất insights từ session chat → knowledge base
- **spec-generator:** Sinh feature specifications (api.json, business.md, flow.md, tasks.md)

Các skill này thuộc loại "meta-skill" — hỗ trợ quy trình làm việc của AI thay vì xây dựng UI/UX trực tiếp.
