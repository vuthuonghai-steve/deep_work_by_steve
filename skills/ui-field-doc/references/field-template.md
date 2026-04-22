# Field Documentation — Template

> Template chuẩn cho output của skill `ui-field-doc`.
> Copy và điền thông tin thực tế từ codebase vào các phần `[...]`.

---

## Table of Contents

- [1. Entity Overview](#1-entity-overview)
- [2. `[PrimaryEntity]`](#2-primaryentity)
  - [2.1 Field Summary Table](#21-field-summary-table)
  - [2.2 Field Details](#22-field-details)
  - [2.3 UI Component Mapping](#23-ui-component-mapping)
  - [2.4 Sensitive Fields](#24-sensitive-fields)
- [3. Related Entities](#3-related-entities)
  - [Entity Relationship Diagram](#entity-relationship-diagram)
- [4. Summary & Recommendations](#4-summary--recommendations)

---

## 1. Entity Overview

**Module:** `[Tên module, ví dụ: Auth, Profile, Order, Task]`
**Mục đích:** `[Mô tả ngắn module làm gì]`
**Entities chính:**
| Entity | File | Mô tả |
|--------|------|--------|
| `[EntityA]` | `lib/data/models/a_model.dart` | `[Mô tả]` |
| `[EntityB]` | `lib/domain/entities/b_entity.dart` | `[Mô tả]` |

**Users / Actors:**
- `[Actor 1, ví dụ: Customer]` — có thể thao tác gì
- `[Actor 2, ví dụ: Admin]` — có thể thao tác gì

---

## 2. `[PrimaryEntity]`

**File:** `` `lib/data/models/[name]_model.dart` ``
**Entity type:** `[Data Model / Domain Entity / DTO]`
**Mô tả:** `[Mô tả entity này đại diện cho cái gì]`

### 2.1 Field Summary Table

| # | Field Name | Dart Type | Required | Default | Description | Source |
|---|------------|-----------|----------|---------|-------------|--------|
| 1 | `[fieldName]` | `[String]` | `[✓ / —]` | `[default]` | `[Mô tả ngắn]` | `` `[file:line]` `` |
| 2 | `[fieldName]` | `[int?]` | `[—]` | `null` | `[Mô tả ngắn]` | `` `[file:line]` `` |
| 3 | `[fieldName]` | `[List<T>]` | `[✓ / —]` | `[]` | `[Mô tả ngắn]` | `` `[file:line]` `` |
| 4 | `[fieldName]` | `[bool]` | `[✓]` | `false` | `[Mô tả ngắn]` | `` `[file:line]` `` |

> **Quy ước Required:** `✓` = bắt buộc (non-nullable, không default), `—` = optional (nullable hoặc có default)

### 2.2 Field Details

#### `[fieldName]`
- **Type:** `[String]`
- **Required:** `[✓ Yes / No]`
- **Default:** `[none / 'pending' / false / 0 / etc.]`
- **Constraints:** `[max length, pattern, enum values, etc.]`
- **Source:** `` `lib/data/models/xxx_model.dart:12` ``
- **Description:** `[Dịch comment/annotation từ code sang tiếng Việt rõ ràng]`
- **Relationships:** `[None / Belongs to User / Has many Tasks / etc.]`
- **UI Implication:** `[Field này hiển thị ở đâu trong UI, có thể edit không, có ảnh hưởng gì]`

---

#### `[fieldName]` `[Sensitive ⚠️]`
- **Type:** `[String]`
- **Required:** `[✓ Yes / No]`
- **Sensitive:** `true` — trường chứa dữ liệu nhạy cảm
- **Source:** `` `lib/data/models/xxx_model.dart:18` ``
- **Description:** `[Mô tả]`
- **UI Implication:** `[Nên dùng PasswordField / Masked input / không hiển thị raw]`

> ⚠️ **Lưu ý bảo mật:** Trường này không nên log ra console, không nên gửi raw qua network không mã hóa, UI không hiển thị đầy đủ khi không cần thiết.

---

#### `[fieldName]` `[Enum]`
- **Type:** `[TaskStatus enum]`
- **Values:**
  | Value | Mô tả |
  |-------|--------|
  | `pending` | Chờ xử lý |
  | `inProgress` | Đang thực hiện |
  | `completed` | Hoàn thành |
  | `cancelled` | Đã hủy |
- **Source:** `` `lib/domain/entities/xxx.dart:5` ``
- **Default:** `pending`
- **UI Implication:** `[RadioGroup / Dropdown / Chip — chọn loại phù hợp với số lượng values]`

---

#### `[fieldName]` `[Nested Object]`
- **Type:** `[Address]`
- **Source:** `` `lib/data/models/xxx_model.dart:22` ``
- **Nested fields:**
  | Field | Type | Required |
  |-------|------|----------|
  | `street` | `String` | ✓ |
  | `city` | `String` | ✓ |
  | `district` | `String?` | — |
  | `zipCode` | `String?` | — |
- **UI Implication:** `[Có thể là Section với nhiều TextField bên trong / Nested Form / Expandable Card]`

---

#### `[fieldName]` `[List Reference]`
- **Type:** `[List<Task>]`
- **Source:** `` `lib/data/models/xxx_model.dart:30` ``
- **Relationship:** `User` has many `Task` (1:N)
- **UI Implication:** `[Danh sách có thể scroll / Repeatable fields / Chip tags]`

---

### 2.3 UI Component Mapping

| Field | Type | UI Component | Props / Notes |
|-------|------|-------------|---------------|
| `id` | `String` | `Text` (display only) | Format: read-only, không editable |
| `name` | `String` | `AppTextField` | Max 100 chars, required |
| `email` | `String` | `AppTextField` | Keyboard: email, validation: email format |
| `password` | `String` | `AppPasswordField` | Obscure text, min 8 chars |
| `phone` | `String` | `AppTextField` | Keyboard: phone, mask: `(###) ###-####` |
| `status` | `Enum` | `Dropdown` | 4+ values → Dropdown; <4 values → `ChipGroup` |
| `isActive` | `bool` | `Switch` | Toggle switch |
| `tags` | `List<String>` | `ChipGroup` | Thêm / xóa tag |
| `bio` | `String` (dài) | `AppTextArea` | Multi-line, max 500 chars |
| `birthDate` | `DateTime` | `DatePicker` | Format: `dd/MM/yyyy` |
| `avatarUrl` | `String` | `ImagePicker` + `CachedNetworkImage` | Preview thumbnail, tap to change |
| `metadata` | `Map` | `Expandable JSON viewer` | Chỉ admin, read-only |

### 2.4 Sensitive Fields

| Field | Type | Reason | Handling |
|-------|------|--------|----------|
| `password` | `String` | Chứa credential | Hash trước khi gửi, không hiển thị raw |
| `refreshToken` | `String` | Security token | Lưu secure storage, không log |
| `bankAccount` | `String` | Financial data | Mask: `****1234`, chỉ hiển thị 4 số cuối |
| `email` | `String` | PII (Personally Identifiable Information) | Có thể mask một phần: `j***@example.com` |
| `phone` | `String` | PII | Mask: `(***) ***-1234` |

---

## 3. Related Entities

### Entity Relationship Diagram

```
┌─────────────────────────────┐
│      [PrimaryEntity]         │
│  id: String                  │
│  name: String                │
│  userId: String (FK)         │──────────┐
│  createdAt: DateTime         │          │
└─────────────────────────────┘          │
         │                               │
         │ 1:N                           │ references
         ▼                               ▼
┌─────────────────┐            ┌─────────────────────┐
│ [RelatedEntity] │            │    [UserEntity]     │
│ taskId: String  │            │  id: String         │
│ title: String    │            │  name: String       │
│ status: Enum    │            │  email: String      │
└─────────────────┘            └─────────────────────┘
```

### Entities chi tiết

#### `[RelatedEntity]` — `` `lib/data/models/related_model.dart` ``
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `String` | ✓ | Primary key |
| `title` | `String` | ✓ | Tiêu đề |
| `status` | `TaskStatus` | ✓ | Trạng thái |

---

## 4. Summary & Recommendations

### Field Count Summary
- **Tổng số entity:** `[N]`
- **Tổng số fields:** `[N]`
- **Fields bắt buộc:** `[N]`
- **Fields optional:** `[N]`
- **Fields nhạy cảm:** `[N]`
- **Enum fields:** `[N]`

### UI Sections gợi ý

| Section | Fields | UI Pattern |
|---------|--------|------------|
| `[Section 1]` | `name`, `email`, `phone` | `Form` với labeled `TextField` |
| `[Section 2]` | `status`, `isActive` | `Switch` + `Dropdown` |
| `[Section 3]` | `tags`, `categories` | `ChipGroup` với add/remove |

### Recommendations cho Designer

1. **Form layout:** Nên chia thành sections rõ ràng (Personal Info → Contact → Authentication)
2. **Validation UX:** Hiển thị error ngay dưới field, không alert dialog
3. **Sensitive fields:** Dùng icon toggle để show/hide password
4. **Enum fields:** `<4 values` dùng `Chip`/`Radio`, `≥4 values` dùng `Dropdown`
5. **List fields:** Dùng `Chip` với remove button cho tags, `+ Add` button cho repeatable
6. **Read-only fields:** Style khác (italic, muted color) để phân biệt với editable fields

### Audit Checklist

- [ ] Tất cả fields đã được map sang UI component
- [ ] Sensitive fields đã có masking/obscuring
- [ ] Enum fields đã chọn UI pattern phù hợp
- [ ] Relationships đã được reflect đúng trong navigation
- [ ] Read-only fields đã được style riêng

---

## 5. File Output

**Đường dẫn:** `{workspace_root}/.claude/docs/{module}-{entity}-fields.md`

**Quy tắc đặt tên:** `{module}-{entity}-fields.md`

| Trường hợp | module | entity | Ví dụ |
|------------|--------|--------|--------|
| Partner detail | `partner` | `account` | `partner-account-fields.md` |
| Customer profile | `customer` | `profile` | `customer-profile-fields.md` |
| Company detail | `company` | `detail` | `company-detail-fields.md` |
| Auth login | `auth` | `login` | `auth-login-fields.md` |
| Order | `order` | `order` | `order-fields.md` |
| Membership | `membership` | `subscription` | `membership-subscription-fields.md` |

---

> **Generated by:** `ui-field-doc` skill
> **Date:** `[YYYY-MM-DD]`
> **Output path:** `{workspace_root}/.claude/docs/{module}-{entity}-fields.md`
> **Source paths:** `[lib/data/models/]`, `[lib/domain/entities/]`
