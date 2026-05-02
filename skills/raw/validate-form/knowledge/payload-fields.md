# Payload Fields to Zod Mapping

> Hướng dẫn mapping từ PayloadCMS field types sang Zod validators
> Usage: Đọc khi cần map fields → Zod validators

---

## Field Type Mapping

| Payload Type | Zod Validator | Example |
|-------------|---------------|---------|
| `text` | `zod.string()` | `zod.string().min(1)` |
| `textarea` | `zod.string()` | `zod.string().max(1000)` |
| `number` | `zod.number()` | `zod.number().min(0)` |
| `email` | `zod.string().email()` | `zod.string().email()` |
| `password` | `zod.string().min(8)` | `zod.string().min(8).max(100)` |
| `select` | `zod.enum()` | `zod.enum(['active', 'inactive'])` |
| `radio` | `zod.enum()` | `zod.enum(['yes', 'no'])` |
| `checkbox` | `zod.boolean()` | `zod.boolean()` |
| `date` | `zod.string().datetime()` | `zod.string().datetime()` |
| `upload` | `zod.string()` | `zod.string()` (media ID) |
| `relationship` | `zod.string()` | `zod.string()` (related ID) |
| `array` | `zod.array()` | `zod.array(zod.string())` |
| `json` | `zod.any()` | `zod.any()` |

---

## Validation Options

### Required Fields

```typescript
// Text required
zod.string().min(1, "Trường này là bắt buộc")

// Number required
zod.number().min(0, "Giá trị phải lớn hơn 0")
```

### Optional Fields

```typescript
// Text optional
zod.string().optional()

// Number optional
zod.number().optional()
```

### With Custom Validation

```typescript
// Phone number
zod.string().regex(/^0\d{9}$/, "Số điện thoại không hợp lệ")

// URL
zod.string().url("URL không hợp lệ")

// Max length
zod.string().max(100, "Không được quá 100 ký tự")
```

---

## Relationship Fields

### Single Relationship

```typescript
// Belongs to one
zod.string().min(1, "Vui lòng chọn")
```

### Multiple Relationship

```typescript
// Has many
zod.array(zod.string()).min(1, "Vui lòng chọn ít nhất 1")
```

---

## Array Fields

### Simple Array

```typescript
// Array of strings
zod.array(zod.string())

// Array of numbers
zod.array(zod.number())
```

### Array with Validation

```typescript
// Array with min items
zod.array(zod.string())
  .min(1, "Vui lòng thêm ít nhất 1 item")

// Array with max items
zod.array(zod.string())
  .max(10, "Không được quá 10 items")
```

---

## Conditional Validation

### With Transform

```typescript
// Trim and validate
zod.string().trim().min(1)
```

### With Refine

```typescript
// Custom validation
zod.object({
  password: zod.string().min(8),
  confirmPassword: zod.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Mật khẩu không khớp",
  path: ["confirmPassword"],
})
```

---

## Error Message Guidelines

### Vietnamese Error Messages

| Field Type | Required Message | Invalid Message |
|------------|-----------------|-----------------|
| Text | "Trường này là bắt buộc" | "Giá trị không hợp lệ" |
| Email | "Email là bắt buộc" | "Email không hợp lệ" |
| Number | "Giá trị là bắt buộc" | "Phải là số" |
| Select | "Vui lòng chọn" | "Giá trị không hợp lệ" |
| Date | "Ngày là bắt buộc" | "Ngày không hợp lệ" |
| Phone | "Số điện thoại là bắt buộc" | "Số điện thoại không hợp lệ" |

### Best Practices

1. **Specific**: "Email không hợp lệ" thay vì "Giá trị không hợp lệ"
2. **Helpful**: "Mật khẩu phải có ít nhất 8 ký tự"
3. **Vietnamese**: Sử dụng tiếng Việt cho người dùng
