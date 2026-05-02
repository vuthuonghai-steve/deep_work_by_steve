# Mapping Rules: Schema Field Type → UI Component

> Source: design.md §3 (Knowledge Zone), §2.1 (Pillar 1 — Knowledge)
> Fidelity: 1:1 transform — mỗi Payload field type → UI Component + Required/Optional behavior + Validation

---

## 1. Core Lookup Table

Dùng bảng này để map mỗi field trong Schema YAML sang UI Component tương ứng.

| Schema Type (Payload) | UI Component | Input ID Prefix | Required behavior | Optional behavior | Notes |
|-----------------------|-------------|-----------------|------------------|-------------------|-------|
| `text` | `<Input type="text">` | `input-` | Outlined red border nếu empty submit | Placeholder hint visible | Dùng `Input` của Radix UI |
| `email` | `<Input type="email">` | `input-` | Validate RFC 5321 format + required border | Placeholder: `user@example.com` | Browser auto-validate + custom check |
| `password` | `<Input type="password">` | `input-` | Min 8 chars, show/hide toggle | N/A (password luôn required) | Thêm `Eye` icon toggle |
| `number` | `<Input type="number">` | `input-` | Min/Max constraints từ schema | 0 là default nếu optional | Thêm `min`/`max` attributes |
| `textarea` / `richText` (plain) | `<Textarea>` | `textarea-` | Required nếu field `required: true` | Placeholder hint, auto-resize | Dùng `Textarea` của Radix UI |
| `richText` (lexical/slate) | `RichTextEditor` (custom) | `editor-` | Required nếu field `required: true` | Empty state: toolbar visible | Integrate Lexical editor |
| `select` (single) | `<Select>` | `select-` | Placeholder: "-- Chọn --" required | Placeholder "-- Không chọn --" | Options từ `options[]` trong schema |
| `select` (multi / `hasMany: true`) | `MultiSelect` hoặc `CheckboxGroup` | `multi-select-` | At least 1 required | 0 selections allowed | Render as tags hoặc checkboxes |
| `checkbox` | `<Checkbox>` | `checkbox-` | N/A (boolean, no required) | Unchecked = false | Dùng `Checkbox` của Radix UI |
| `date` | `<DatePicker>` | `date-` | Required nếu field `required: true` | Placeholder: "DD/MM/YYYY" | ISO 8601 format khi submit |
| `upload` (image) | `ImageUpload` (custom) | `upload-` | Required nếu field `required: true` | Drop zone visible, preview | Accept: `image/*`, max size từ schema |
| `upload` (file generic) | `FileUpload` (custom) | `upload-` | Required nếu field `required: true` | Drop zone visible | Accept types từ schema config |
| `relationship` (single) | `RelationPicker` / `<Select>` async | `relation-` | Required nếu field `required: true` | Clearable select | Search-as-you-type từ related collection |
| `relationship` (hasMany) | `RelationMultiPicker` / `MultiSelect` async | `relation-multi-` | At least 1 required | 0 selections allowed | Add/remove chips |
| `array` (list of objects) | Repeater / `ArrayField` (custom) | `array-` | Min items nếu `minRows` set | Empty state: "Add item" button | Each row = sub-form |
| `group` | FormSection (visual grouping) | *(no prefix, use section label)* | N/A (container) | N/A (container) | Group fields inside a `<fieldset>` or Card |
| `blocks` (content blocks) | BlockEditor (custom) | `block-` | N/A (optional by default) | Empty state: block type picker | Complex — treat as rich content area |
| `json` | `<Textarea>` (code mode) | `json-` | Valid JSON required | Empty = `null` | Syntax highlight optional |
| `point` (geo) | `CoordinateInput` hoặc Map picker | `coord-` | Lat/Lng both required | Empty = no location | Double field (lat + lng) |

---

## 2. Required vs Optional — Decision Rules

```
field.required === true  → UI must show:
  - Required indicator (asterisk * hoặc "Bắt buộc" label)
  - Validation error on blur or submit attempt
  - Error message: "[Tên field] là bắt buộc"

field.required === false (hoặc không set) → UI may show:
  - Optional label "(Tùy chọn)" hoặc không có label
  - No error on empty submit
  - Placeholder hint để guide user
```

---

## 3. Validation Constraint Mapping

| Schema constraint | Validation Rule | Error Message pattern |
|------------------|-----------------|-----------------------|
| `minLength: N` | `value.length >= N` | "[Field] phải có ít nhất N ký tự" |
| `maxLength: N` | `value.length <= N` | "[Field] không được vượt quá N ký tự" |
| `min: N` (number) | `value >= N` | "[Field] phải lớn hơn hoặc bằng N" |
| `max: N` (number) | `value <= N` | "[Field] phải nhỏ hơn hoặc bằng N" |
| `unique: true` | Server-side check on submit | "[Field] này đã được sử dụng" |
| `validate: fn` | Custom function — note rule in spec | Custom message từ function |
| `enum` values | Only allow listed options | "Giá trị không hợp lệ" |
| `admin.readOnly` | Render as `<Text>` display only | N/A |

---

## 4. Display-Only Fields (Read Mode)

Khi màn hình ở **View/Read mode** (không phải Edit):

| Schema Type | Display Component | Notes |
|-------------|------------------|-------|
| `text` / `email` | `<Text>` / `<p>` | Plain text |
| `richText` | RichTextRenderer | Render HTML/Markdown |
| `select` | `<Badge>` hoặc `<Text>` | Show option label, not value |
| `checkbox` | `<Badge variant="success/error">` | "Có" / "Không" |
| `date` | Formatted `<Text>` | VD: "21 tháng 2, 2026" |
| `upload` | `<img>` hoặc file link | Preview image / download link |
| `relationship` | Linked text hoặc `<AvatarWithName>` | Hiển thị tên entity, không ID |
| `array` | `<List>` hoặc table rows | Render từng item |

---

## 5. Traceability Column — Bắt buộc trong mọi Data Binding Table

Mỗi row trong Data-Component Binding table phải có cột **Source Field**:

```
| UI Element ID     | Component       | Source Field (Schema) | Required | Validation     |
|-------------------|-----------------|-----------------------|----------|----------------|
| input-email       | Input[email]    | User.email            | ✅       | RFC 5321       |
| input-password    | Input[password] | User.password         | ✅       | min 8 chars    |
| select-role       | Select          | User.role             | ✅       | enum [admin,user]|
| input-displayName | Input[text]     | User.displayName      | ✅       | maxLength: 50  |
| textarea-bio      | Textarea        | User.bio              | ❌       | maxLength: 500 |
```

**Rule**: Nếu muốn thêm UI element mà không có source field trong Schema → ghi `[SOURCE MISSING]` vào cột Source Field. **Tuyệt đối không tự bịa field.** (G1)
