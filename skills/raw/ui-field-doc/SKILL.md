---
name: ui-field-doc
description: Phân tích codebase (data models, domain entities, repositories) để trích xuất cấu trúc các trường thông tin (fields) và sinh tài liệu markdown theo template chuẩn. Hỗ trợ designer nắm bắt toàn bộ trường thông tin tham gia vào UI trước khi xây dựng giao diện. Trigger khi user nói "phân tích field cho UI", "tạo tài liệu field", "extract field schema", "liệt kê trường thông tin".
---

# UI Field Doc

## Overview

Skill phân tích các data models và domain entities trong codebase, trích xuất thông tin chi tiết từng field (name, type, constraints, relationships, description) và sinh tài liệu markdown cấu trúc theo template chuẩn. Kết quả giúp designer nắm rõ schema dữ liệu trước khi thiết kế UI.

---

## When to Use

- User cần tạo tài liệu mô tả fields cho một module/tính năng cụ thể
- Designer cần biết schema dữ liệu trước khi xây dựng giao diện
- Cần trích xuất field list từ codebase để phục vụ thiết kế hoặc validation
- Cần audit fields giữa backend và frontend
- Khởi tạo tài liệu cho feature mới trước khi viết code

---

## Example Triggers

- "Phân tích field cho module auth"
- "Tạo field doc cho profile page"
- "/ui-field-doc --module customer"
- "Extract fields từ User model"
- "Field documentation cho order feature"
- "Liệt kê trường thông tin cho task entity"

---

## Workflow

### Bước 1 — Xác định scope phân tích

- Xác định module/feature/entity cần phân tích từ yêu cầu user hoặc suy luận ngữ cảnh
- Xác định đường dẫn cần scan:
  - `lib/data/models/` — DTOs với fromJson/toJson
  - `lib/data/repositories/` — Repository implementations
  - `lib/domain/entities/` — Domain entities (pure Dart)
  - `lib/domain/repositories/` — Repository interfaces
- Nếu user không chỉ rõ module, hỏi hoặc quét toàn bộ features/

### Bước 2 — Scan codebase bằng Explore agent

Gọi Explore agent với `subagent_type: "Explore"` để quét đồng thời:

- Tất cả files trong `data/models/` (entity-related)
- Tất cả files trong `domain/entities/` (entity definitions)
- Các repository liên quan trong `data/repositories/` và `domain/repositories/`

Thu thập: class name, field name, field type, annotations (`@required`, `@JsonKey`, default values), comments (`///`).

**Depth: rất kỹ (very thorough)** — đọc toàn bộ model files.

### Bước 3 — Trích xuất field metadata

Với mỗi model/entity, ghi nhận:

| Thuộc tính | Mô tả |
|---|---|
| `fieldName` | Tên trường (camelCase) |
| `dartType` | Kiểu Dart thực tế: `String`, `int`, `DateTime`, `bool`, enum, `List<T>`, `Map`, custom class |
| `source` | File + dòng (citations), ví dụ: `lib/data/models/user_model.dart:24` |
| `constraints` | Default value, nullable (`?`), required, validation annotations |
| `relationships` | Foreign key, nested object, list reference, enum reference |
| `description` | Comment/annotation mô tả nếu có |
| `isSensitive` | `true` nếu trường chứa dữ liệu nhạy cảm (password, token, số tài khoản, email, phone) |

### Bước 4 — Nhóm fields theo entity/module

- Gom nhóm fields theo entity/class gốc
- Đánh dấu primary entity vs. related entities
- Xác định UI section mapping (ví dụ: "Personal Info", "Address", "Authentication")
- Vẽ sơ đồ quan hệ entity đơn giản bằng ASCII

### Bước 5 — Áp dụng template chuẩn

- Đọc template từ `references/field-template.md`
- Mỗi entity: sinh bảng fields + prose description
- Đánh dấu fields bắt buộc (`required`) vs. optional
- Ghi chú relationships và navigation implications

### Bước 6 — Bổ sung UI recommendations

Với mỗi field, đề xuất UI component phù hợp:

| Dart Type | UI Component đề xuất |
|---|---|
| `String` (ngắn, <50 chars) | `TextField` |
| `String` (dài, mô tả) | `TextArea` / `Multi-line TextField` |
| `DateTime` | `DatePicker` |
| `DateTime?` (nullable) | `DatePicker` + "Không có" placeholder |
| Enum ( ít lựa chọn, <4) | `RadioGroup` / `Chip` |
| Enum (nhiều lựa chọn, ≥4) | `Dropdown` |
| `bool` | `Switch` (toggle) hoặc `Checkbox` |
| `List<T>` (tags) | `ChipGroup` / `TagInput` |
| `List<T>` (repeatable) | `Repeatable fields` / `ListBuilder` |
| Sensitive (`isSensitive: true`) | `PasswordField` / `MaskedTextField` |
| `int` / `double` | `NumberField` với validation |
| `Map<String, dynamic>` | `Expandable JSON viewer` (admin) |

### Bước 7 — Sinh markdown output

- Xuất markdown hoàn chỉnh theo template
- Ghi rõ source citations cho mỗi field
- **Lưu file theo quy tắc:**
     - Thư mục gốc: `{workspace_root}/.claude/docs/`
     - Tên file: `{module}-{entity}-fields.md`
     - Ví dụ: `.claude/docs/partner-account-fields.md`, `.claude/docs/auth-login-fields.md`
     - Nếu user chỉ định thư mục khác → dùng thư mục user chỉ định
     - Nếu thư mục `.claude/docs/` chưa tồn tại → tạo trước khi ghi file
- Format: table-of-contents → entity sections → summary

---

## Output Structure

Tài liệu sinh ra có cấu trúc:

```markdown
# {Module} — Field Documentation

## Table of Contents
## 1. Entity Overview
## 2. {EntityName} [`file_path`]
   ### 2.1 Field Summary Table
   ### 2.2 Field Details
   ### 2.3 UI Component Mapping
   ### 2.4 Sensitive Fields
## 3. Related Entities
   ### Entity Relationship Diagram
## 4. Summary & Recommendations
```

**Đường dẫn file:** `{workspace_root}/.claude/docs/{module}-{entity}-fields.md`

---

## Quality Rules

- **Mỗi field PHẢI có source citation** (file + dòng), ví dụ: `` `lib/data/models/user_model.dart:31` ``
- **KHÔNG tự bịa field** không có trong code — chỉ ghi nhận những gì thực sự có trong Dart source
- **KHÔNG phỏng đoán kiểu** — chỉ ghi nhận type thực tế từ Dart code
- **Enum**: ghi rõ tất cả values của enum
- **Relationships**: ghi rõ entity liên quan và cardinality (1-1, 1-N, N-N)
- **Nếu field ambiguous**: mark là `[UNVERIFIED]` và note rõ lý do
- **Sensitive fields**: PHẢI đánh dấu `isSensitive: true` và ghi chú riêng
- **Null-safety**: phân biệt rõ `String` (required) vs `String?` (optional)
- **Default values**: ghi nhận nếu có, ví dụ: `default: false`, `default: 'pending'`

---

## Output & Naming Conventions

### Đường dẫn xuất file

**Thư mục gốc:** `{workspace_root}/.claude/docs/`

Tất cả tài liệu field documentation phải được lưu vào thư mục `.claude/docs/` theo cấu trúc phẳng (không subfolder) để dễ quản lý và tìm kiếm.

### Quy tắc đặt tên file

```
{module}-{entity}-fields.md
```

| module | entity | Ví dụ file |
|--------|--------|------------|
| Tên module (feature) viết thường, gạch nối | Tên entity chính viết thường | `partner-account-fields.md` |
| `auth` | `login`, `register` | `auth-login-fields.md` |
| `customer` | `profile`, `account` | `customer-profile-fields.md` |
| `company` | `detail`, `employee` | `company-detail-fields.md` |
| `order` | `order`, `item` | `order-fields.md` |
| `membership` | `subscription`, `plan` | `membership-subscription-fields.md` |

**Anti-patterns (KHÔNG dùng):**
- ❌ `field-doc-customer-2024-03-24.md` (có date)
- ❌ `customer_fields.md` (underscore)
- ❌ `CustomerProfileFieldDocumentation.md` (PascalCase)
- ❌ `.claude/docs/customer/profile-fields.md` (subfolder)

### Đường dẫn đầy đủ

```
{workspace_root}/.claude/docs/{module}-{entity}-fields.md
```

Ví dụ đầy đủ:
```
/home/stveve/WorkSpave-by-steve/ktx-app/ktx-app/.claude/docs/partner-account-fields.md
```

**Lưu ý:** Thư mục `.claude/docs/` nằm trong workspace root của dự án, cùng cấp với `lib/`, `pubspec.yaml`.

---

## Template Reference

Template markdown chuẩn cho output nằm tại:

```
references/field-template.md
```

Đọc file này trước khi sinh output để đảm bảo format nhất quán.

---

## Quick Command Reference

| Trigger | Action |
|---|---|
| `phân tích field cho module X` | Bắt đầu workflow bước 1-7 cho module X |
| `tạo field doc cho Y` | Sinh tài liệu markdown cho entity Y |
| `extract field schema` | Trích xuất toàn bộ field metadata dạng bảng |
| `liệt kê trường thông tin` | Liệt kê tất cả fields của một feature |
