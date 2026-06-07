# Build CRUD Admin Page — References

## Overview

Skill này giúp AI Agent xây dựng trang quản lý CRUD cho bất kỳ PayloadCMS collection nào, theo đúng pattern của BouquetScreen.

## Cấu trúc tài liệu

| File | Mô tả |
|------|--------|
| `architecture.md` | Cấu trúc thư mục, data flow, form mode pattern, component responsibilities |
| `template-guide.md` | Hướng dẫn từng bước áp dụng cho collection mới |
| `implementation-logic.md` | Chi tiết logic (form mode, metadata, categories, BOM) |
| `errors.md` | Lỗi thường gặp và cách xử lý |
| `ui-skills-summary.md` | Tóm tắt 4 UI/UX skills cần tham khảo |

## Modules áp dụng

- **BouquetScreen** — Bó hoa: full-page, 7 tabs
- **AccessoryScreen** — Phụ kiện: full-page, inline sections, danh mục scoped
- **SingleFlowerScreen** — Hoa lẻ: (tham chiếu BouquetScreen)

## Đọc theo thứ tự

```
1. architecture.md     → Hiểu folder structure
2. template-guide.md   → Áp dụng cho collection mới
3. implementation-logic.md → Chi tiết form mode, metadata
4. errors.md           → Khi gặp lỗi
5. ui-skills-summary.md → Trước khi implement UI
```

## Quick Reference

### Form Mode Pattern

```typescript
type FormMode = 'create' | 'view' | 'edit'
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'
```

### Route Structure

| Route | Mode |
|-------|------|
| `/manager/products-{collection}` | List |
| `/manager/products-{collection}/new` | Create |
| `/manager/products-{collection}/[id]` | View |
| `/manager/products-{collection}/[id]?mode=edit` | Edit |
