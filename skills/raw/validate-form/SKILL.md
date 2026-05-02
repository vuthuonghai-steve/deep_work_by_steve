---
name: validate-form
description: Phân tích PayloadCMS collection và tạo Zod validation schemas với error messages rõ ràng. Sử dụng khi cần xây dựng validation cho admin form create/update.
---

# Validate Form — PayloadCMS Form Validation Builder

> Tự động phân tích collection schema và tạo validation code với error messages cho người dùng.

---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file) - luôn được load

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
- [knowledge/payload-fields.md](knowledge/payload-fields.md) - Mapping Payload fields → Zod validators
- [data/field-validators.yaml](data/field-validators.yaml) - Config mapping field types

### Tier 3: Optional (load when needed)
- [knowledge/error-messages.md](knowledge/error-messages.md) - Khi cần customize error messages
- [knowledge/validation-structure.md](knowledge/validation-structure.md) - Khi cần tổ chức validation files
- [templates/zod-schema.template](templates/zod-schema.template) - Khi cần template output
- [loop/verify-checklist.md](loop/verify-checklist.md) - Khi cần verify output

---

## Workflow Progress Tracker

```markdown
### [validate-form] Progress:
- [ ] Phase 1: Nhận collection name và kiểm tra registry
- [ ] Phase 2: Phân tích collection với /payload skill
- [ ] Phase 3: Map fields → Zod validators và tạo code
- [ ] Phase 4: Preview và xác nhận từ user
- [ ] Phase 5: Ghi files và cập nhật registry
```

---

## Phase 1: Nhận Input và Kiểm tra Registry

### Nhận Input
- **Input**: Tên collection cần validate (vd: `products`, `orders`, `customers`)
- **Location**: Xác định project path (sử dụng cwd)

### Kiểm tra Registry
1. Đọc file `.validate/validation-registry.yaml` trong project
2. Kiểm tra xem collection đã có validation chưa
3. Liệt kê các fields đã có validation

**Nếu collection đã có trong registry**:
- Hiển thị "Đã có validation cho collection X"
- Liệt kê fields đã validate
- Hỏi user: "Tiếp tục update hay tạo mới?"

**Nếu collection chưa có**:
- Tiến hành Phase 2

---

## Phase 2: Phân tích Collection với /payload

Gọi **skill /payload** để phân tích collection:

```
Sử dụng /payload skill để:
1. Đọc collection schema
2. Liệt kê tất cả fields với types
3. Xác định relationships
4. Trả về field definitions
```

**Output từ /payload**:
- Tên collection
- Danh sách fields: name, type, required, validation options
- Relationships: related collections, field names

---

## Phase 3: Map Fields → Zod Validators

### Đọc Knowledge Files
- [knowledge/payload-fields.md](knowledge/payload-fields.md) - Mapping rules
- [data/field-validators.yaml](data/field-validators.yaml) - Config

### Mapping Logic

| Payload Field Type | Zod Validator |
|-------------------|---------------|
| text | `zod.string()` |
| number | `zod.number()` |
| email | `zod.string().email()` |
| select | `zod.enum([...])` |
| relationship | `zod.string()` (ID) |
| date | `zod.string().datetime()` |
| checkbox | `zod.boolean()` |
| upload | `zod.string()` (file ID) |

### Sinh Validation Code

```typescript
// Ví dụ output cho field "name" (text, required, max 100)
export const productNameSchema = zod.string()
  .min(1, "Tên sản phẩm là bắt buộc")
  .max(100, "Tên sản phẩm không được quá 100 ký tự")

// Ví dụ output cho field "price" (number, min 0)
export const productPriceSchema = zod.number()
  .min(0, "Giá sản phẩm không được âm")
```

---

## Phase 4: Preview và Xác nhận

### Hiển thị Preview
- Hiển thị Zod schema sẽ được tạo
- Hiển thị file output path
- Hiển thị các fields sẽ reuse từ registry

### Xác nhận User
- Chờ user xác nhận trước khi ghi file
- Nếu user từ chối → quay lại Phase 1

---

## Phase 5: Ghi Files và Cập nhật Registry

### Ghi Validation Files
Theo cấu trúc flat Level 3+:

```
src/
├── validations/
│   ├── validation.commerce.ts   # products, categories
│   ├── validation.orders.ts    # orders, payments
│   └── validation.auth.ts      # users, customers
└── utils/
    └── validate/
        ├── util.validate-phone.ts
        └── util.validate-email.ts
```

### Cập nhật Registry
Ghi vào `.validate/validation-registry.yaml`:

```yaml
validations:
  products:
    fields:
      name:
        type: text
        validator: "zod.string().min(1).max(100)"
        file: src/validations/validation.commerce.ts
        created: 2026-03-17
```

---

## Guardrails

| ID | Rule |
|----|------|
| G1 | **Reuse Validation** - BẮT BUỘC kiểm tra registry trước khi tạo mới |
| G2 | **Error Messages** - Thông báo lỗi phải rõ ràng bằng tiếng Việt |
| G3 | **No Overwrite** - Không ghi đè code hiện có, chỉ thêm mới |
| G4 | **Registry Update** - Sau khi tạo validation mới → cập nhật registry |
| G5 | **Project Path** - Sử dụng cwd làm project path, registry tại `.validate/` |

---

## Examples

### Example 1 — Validate Products Collection

**Input**: `products`

**Process**:
1. Đọc registry → chưa có
2. Gọi /payload → lấy fields: name, price, description, category, images
3. Map → Zod validators
4. Preview → chờ confirm

**Output**:
```typescript
// src/validations/validation.commerce.ts
export const productSchema = zod.object({
  name: zod.string()
    .min(1, "Tên sản phẩm là bắt buộc")
    .max(100, "Tên sản phẩm không được quá 100 ký tự"),
  price: zod.number()
    .min(0, "Giá sản phẩm không được âm"),
  description: zod.string().optional(),
  category: zod.string().min(1, "Danh mục là bắt buộc"),
  images: zod.array(zod.string()).optional(),
})
```

### Example 2 — Reuse Validation

**Input**: `categories` (cùng domain commerce)

**Process**:
1. Đọc registry → đã có `name` field từ products
2. Reuse: `name` validation từ products
3. Chỉ tạo mới các fields mới

**Output**: "Reusing existing validation for field: name"

---

## Error Handling

| Error | Handling |
|-------|----------|
| Collection không tồn tại | Thông báo lỗi, liệt kê collections có sẵn |
| Registry file lỗi | Tạo mới registry |
| Ghi file thất bại | Thông báo lỗi, dừng lại |

---

## Notes

- Registry path: `{project}/.validate/validation-registry.yaml`
- Sử dụng /payload skill để phân tích collection
- Validation files theo cấu trúc flat Level 3+
- Error messages bằng tiếng Việt, rõ ràng cho người dùng
