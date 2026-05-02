# Verify Checklist

> Checklist để verify output của validate-form skill
> Usage: Chạy sau khi tạo validation code

---

## Pre-Generation Verification

- [ ] Collection tồn tại trong PayloadCMS
- [ ] Fields đã được phân tích đầy đủ
- [ ] Registry đã được kiểm tra

---

## Post-Generation Verification

### Code Quality

- [ ] Zod schema syntax đúng
- [ ] Error messages bằng tiếng Việt
- [ ] Error messages rõ ràng, hữu ích cho người dùng
- [ ] Type inference hoạt động (`z.infer<typeof schema>`)

### File Structure

- [ ] File được tạo đúng location (`src/validations/` hoặc `src/utils/validate/`)
- [ ] Tên file đúng convention (flat Level 3+)
- [ ] Import path chính xác

### Registry

- [ ] Registry file được cập nhật
- [ ] Mỗi field có validator được ghi vào registry
- [ ] File path chính xác trong registry

---

## Error Detection

### Syntax Errors

| Error | How to Check |
|-------|-------------|
| Invalid Zod syntax | Run TypeScript compiler |
| Missing import | Check `z` is imported |
| Wrong validator | Verify against field type |

### Logic Errors

| Error | How to Check |
|-------|-------------|
| Wrong field mapping | Verify field type → validator mapping |
| Missing validation | Check all fields have validators |
| Wrong error message | Test with invalid input |

---

## Manual Test Cases

### Test 1: Required Field

```typescript
const schema = productSchema
const result = schema.safeParse({})
// Should return error: "Tên sản phẩm là bắt buộc"
```

### Test 2: Invalid Email

```typescript
const schema = z.object({ email: z.string().email() })
const result = schema.safeParse({ email: "invalid" })
// Should return error: "Email không hợp lệ"
```

### Test 3: Number Range

```typescript
const schema = z.number().min(0).max(100)
const result = schema.safeParse(-1)
// Should return error: "Giá trị phải lớn hơn hoặc bằng 0"
```

---

## Common Issues

### Issue 1: Schema không hoạt động

**Nguyên nhân**: Thiếu import `z` từ zod

**Fix**:
```typescript
import { z } from "zod"
```

### Issue 2: Error message không hiển thị

**Nguyên nhân**: Sử dụng `.refine()` thay vì `.min()`/.max()

**Fix**:
```typescript
// Thay vì
z.string().refine(val => val.length > 0)

// Sử dụng
z.string().min(1, "Trường này là bắt buộc")
```

### Issue 3: Registry không được cập nhật

**Nguyên nhân**: Quên ghi sau khi tạo validation mới

**Fix**: Luôn gọi cập nhật registry sau khi tạo validation

---

## Success Criteria

- [ ] Tất cả fields trong collection đều có validation
- [ ] Error messages rõ ràng, người dùng hiểu được lỗi
- [ ] Validation có thể tái sử dụng (qua registry)
- [ ] Code TypeScript type-safe
- [ ] Không có syntax errors
