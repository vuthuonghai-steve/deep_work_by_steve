# Validation Structure — Flat Level 3+

> Cấu trúc tổ chức validation files trong dự án
> Usage: Đọc khi cần tổ chức validation files

---

## Nguyên tắc Flat Level 3+

### Quy tắc đặt tên

| Loại | Pattern | Ví dụ |
|------|---------|--------|
| Domain validation | `validation.<domain>.ts` | `validation.commerce.ts` |
| Reusable validator | `util.validate-<name>.ts` | `util.validate-phone.ts` |

### Folder Structure

```
src/
├── validations/                    # Level 1 - Nhóm validation
│   ├── validation.auth.ts         # Auth: users, customers, login
│   ├── validation.commerce.ts    # Commerce: products, categories
│   ├── validation.orders.ts       # Orders: orders, payments
│   ├── validation.stores.ts      # Stores: stores, inventory
│   └── validation.marketing.ts   # Marketing: vouchers, campaigns
└── utils/
    └── validate/                  # Reusable validators
        ├── util.validate-phone.ts
        ├── util.validate-email.ts
        ├── util.validate-url.ts
        └── util.validate-date-range.ts
```

---

## Domain Mapping

### Collection → Domain → File

| Collection Domain | Collections | Validation File |
|------------------|-------------|----------------|
| auth | users, customers, devices | `validation.auth.ts` |
| commerce | products, categories, tags, reviews | `validation.commerce.ts` |
| orders | orders, payment-sessions, assignments | `validation.orders.ts` |
| stores | stores, inventory, bank-accounts | `validation.stores.ts` |
| marketing | vouchers, campaigns, notifications | `validation.marketing.ts` |

---

## Import Pattern

### Import từ domain validation

```typescript
// Import toàn bộ schema
import { productSchema } from "@/validations/validation.commerce"

// Import specific schema
import { productSchema, categorySchema } from "@/validations/validation.commerce"
```

### Import từ reusable validator

```typescript
// Import validator function
import { validatePhone } from "@/utils/validate/util.validate-phone"

// Sử dụng trong Zod
import { z } from "zod"
const phoneSchema = z.string().refine(validatePhone, {
  message: "Số điện thoại không hợp lệ"
})
```

---

## File Content Structure

### Domain Validation File

```typescript
// src/validations/validation.commerce.ts

import { z } from "zod"

// ============================================================================
// PRODUCT VALIDATION
// ============================================================================

export const productSchema = z.object({
  name: z.string()
    .min(1, "Tên sản phẩm là bắt buộc")
    .max(100, "Tên sản phẩm không được quá 100 ký tự"),
  price: z.number()
    .min(0, "Giá sản phẩm không được âm"),
  description: z.string().optional(),
  category: z.string().min(1, "Danh mục là bắt buộc"),
  images: z.array(z.string()).optional(),
})

export type ProductFormData = z.infer<typeof productSchema>

// ============================================================================
// CATEGORY VALIDATION
// ============================================================================

export const categorySchema = z.object({
  name: z.string()
    .min(1, "Tên danh mục là bắt buộc")
    .max(50, "Tên danh mục không được quá 50 ký tự"),
  slug: z.string()
    .min(1, "Slug là bắt buộc")
    .regex(/^[a-z0-9-]+$/, "Slug chỉ chứa chữ thường, số và dấu gạch ngang"),
  parent: z.string().optional(),
})

export type CategoryFormData = z.infer<typeof categorySchema>
```

### Reusable Validator File

```typescript
// src/utils/validate/util.validate-phone.ts

/**
 * Validate Vietnamese phone number
 * Accepts: 0xxxxxxxxx (10 digits starting with 0)
 */
export function validatePhone(value: string): boolean {
  return /^0\d{9}$/.test(value)
}

/**
 * Validate phone with message
 */
export const phoneSchema = z.string()
  .regex(/^0\d{9}$/, "Số điện thoại không hợp lệ (vd: 0912345678)")
```

---

## Registry Integration

### Cập nhật Registry

Sau khi tạo validation mới, cập nhật `.validate/validation-registry.yaml`:

```yaml
validations:
  products:
    fields:
      name:
        type: text
        validator: "zod.string().min(1).max(100)"
        file: src/validations/validation.commerce.ts
        created: 2026-03-17
      price:
        type: number
        validator: "zod.number().min(0)"
        file: src/validations/validation.commerce.ts
        created: 2026-03-17

reusableValidators:
  phone:
    file: src/utils/validate/util.validate-phone.ts
    validator: "regex(/^0\\d{9}$/)"
```

---

## Best Practices

1. **Một file = Một domain**: Group theo business domain
2. **Schema exports**: Luôn export cả schema và type
3. **Error messages**: Tiếng Việt, rõ ràng
4. **Registry update**: Luôn cập nhật sau khi tạo mới
5. **Reuse**: Kiểm tra registry trước khi tạo mới
