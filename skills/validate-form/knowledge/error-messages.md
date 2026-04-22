# Error Messages Standards

> Tiêu chuẩn error messages cho form validation
> Usage: Đọc khi cần customize error messages

---

## Nguyên tắc Error Messages

### 1. Rõ ràng và cụ thể

| ❌ Không nên | ✅ Nên |
|-------------|--------|
| "Giá trị không hợp lệ" | "Email không hợp lệ" |
| "Dữ liệu lỗi" | "Số điện thoại phải có 10 chữ số" |
| "Nhập liệu sai" | "Mật khẩu phải có ít nhất 8 ký tự" |

### 2. Helpful - Giúp người dùng sửa

| ❌ Không nên | ✅ Nên |
|-------------|--------|
| "Trường bắt buộc" | "Tên sản phẩm là bắt buộc" |
| "Giá trị quá lớn" | "Giá sản phẩm không được vượt quá 1.000.000 VNĐ" |
| "Email lỗi" | "Vui lòng nhập địa chỉ email hợp lệ (ví dụ: example@email.com)" |

### 3. Vietnamese - Tiếng Việt

Sử dụng tiếng Việt cho tất cả error messages:
- "Trường này là bắt buộc"
- "Vui lòng nhập..."
- "Giá trị không hợp lệ"

---

## Error Messages theo Field Type

### Text Fields

| Validation | Error Message |
|------------|--------------|
| Required | "{Tên trường} là bắt buộc" |
| Min length | "{Tên trường} phải có ít nhất {min} ký tự" |
| Max length | "{Tên trường} không được quá {max} ký tự" |
| Pattern | "{Tên trường} không đúng định dạng" |

### Number Fields

| Validation | Error Message |
|------------|--------------|
| Required | "{Tên trường} là bắt buộc" |
| Min | "{Tên trường} phải lớn hơn hoặc bằng {min}" |
| Max | "{Tên trường} phải nhỏ hơn hoặc bằng {max}" |
| Integer | "{Tên trường} phải là số nguyên" |

### Email Fields

| Validation | Error Message |
|------------|--------------|
| Required | "Email là bắt buộc" |
| Invalid | "Email không hợp lệ" |
| Already exists | "Email đã được sử dụng" |

### Phone Fields

| Validation | Error Message |
|------------|--------------|
| Required | "Số điện thoại là bắt buộc" |
| Invalid | "Số điện thoại không hợp lệ (vd: 0912345678)" |
| Pattern | "Số điện thoại phải có 10 chữ số, bắt đầu bằng 0" |

### Select Fields

| Validation | Error Message |
|------------|--------------|
| Required | "Vui lòng chọn {tên trường}" |
| Invalid | "Giá trị không hợp lệ" |

### Date Fields

| Validation | Error Message |
|------------|--------------|
| Required | "Ngày là bắt buộc" |
| Invalid | "Ngày không hợp lệ" |
| Future | "Ngày phải ở tương lai" |
| Past | "Ngày phải ở quá khứ" |

### Password Fields

| Validation | Error Message |
|------------|--------------|
| Required | "Mật khẩu là bắt buộc" |
| Min length | "Mật khẩu phải có ít nhất 8 ký tự" |
| Match | "Mật khẩu không khớp" |

### Confirm Fields

| Validation | Error Message |
|------------|--------------|
| Match | "{Tên trường} không khớp" |

---

## Form-Level Errors

### General Errors

| Error | Message |
|-------|---------|
| Submit failed | "Đã xảy ra lỗi. Vui lòng thử lại sau." |
| Network error | "Không thể kết nối máy chủ. Vui lòng kiểm tra kết nối internet." |
| Unauthorized | "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại." |

### Success Messages

| Action | Message |
|--------|---------|
| Create | "Tạo thành công!" |
| Update | "Cập nhật thành công!" |
| Delete | "Xóa thành công!" |

---

## Implementation Example

```typescript
// Viet hoa loi theo field
const fieldErrors = {
  required: "{label} là bắt buộc",
  email: "Email không hợp lệ",
  minLength: "{label} phải có ít nhất {min} ký tự",
  maxLength: "{label} không được quá {max} ký tự",
}

// Su dung
function getErrorMessage(validation: string, label: string, params?: object) {
  let message = fieldErrors[validation] || "Giá trị không hợp lệ"
  message = message.replace("{label}", label)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      message = message.replace(`{${key}}`, String(value))
    })
  }
  return message
}
```
