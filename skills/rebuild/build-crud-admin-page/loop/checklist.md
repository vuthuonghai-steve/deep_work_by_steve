# Checklist: Bouquet UI Module

## Pre-Implementation

- [ ] Đọc design.md để hiểu architecture
- [ ] Đọc spec files để hiểu requirements
- [ ] Review existing code trong BouquetScreen/
- [ ] Xác định PayloadCMS endpoints cần dùng

## Setup

- [ ] Tạo folder structure theo architecture.md
- [ ] Tạo types/index.ts với FormMode và interfaces
- [ ] Tạo constants/index.ts với routes, tabs, messages
- [ ] Verify imports và exports

## ProductListView

- [ ] Layout cơ bản với header và table
- [ ] ProductFilters component (search, status, category, trend)
- [ ] ProductTable với columns đầy đủ
- [ ] Pagination với meta info
- [ ] Actions (view, edit, delete) hoạt động
- [ ] Empty state hiển thị đúng
- [ ] Loading skeleton hiển thị

## ProductFormView

- [ ] Mode handling (create/view/edit) đúng
- [ ] Header thay đổi theo mode
- [ ] Actions buttons thay đổi theo mode
- [ ] Mode switching (view ↔ edit) hoạt động
- [ ] URL update khi switch mode

## Form Sections (7 Tabs)

### Tab 1: Thông tin chung
- [ ] name field (required)
- [ ] type field (fixed: bouquet)
- [ ] sku field (auto-generated)
- [ ] slug field (auto-generated từ name)
- [ ] category dropdown (required)
- [ ] unit dropdown (required)
- [ ] shortDescription textarea
- [ ] fullDescription rich text

### Tab 2: Giá và Kích thước
- [ ] price field (required, số dương)
- [ ] commissionRate field (0-100%)
- [ ] ProductSize variants hiển thị

### Tab 3: Thành phần (BOM)
- [ ] bomItems array hiển thị
- [ ] Add/remove BOM items
- [ ] Material dropdown (filter type=single/accessory)
- [ ] Quantity field

### Tab 4: Hình ảnh
- [ ] images gallery upload
- [ ] Image preview hiển thị
- [ ] Remove image hoạt động
- [ ] deliveryGallery (read-only)

### Tab 5: Phân loại
- [ ] occasions multi-select
- [ ] targetAges multi-select
- [ ] targetCustomers multi-select
- [ ] tags multi-select (filter type=style)

### Tab 6: Trạng thái
- [ ] status dropdown (required)
- [ ] trend dropdown
- [ ] featured checkbox
- [ ] Read-only stats (soldCount, rating, reviews)

### Tab 7: SEO
- [ ] seoTitle (60 char limit + counter)
- [ ] seoDescription (160 char limit + counter)
- [ ] Collapsible section hoạt động

## Form Validation

- [ ] Required fields validation
- [ ] Error messages tiếng Việt
- [ ] Focus vào field lỗi đầu tiên
- [ ] Field highlight đỏ khi lỗi
- [ ] Zod schema validation

## Form Submission

- [ ] Create mode: POST API hoạt động
- [ ] Edit mode: PATCH API hoạt động
- [ ] Loading state trên submit button
- [ ] Success toast hiển thị
- [ ] Error toast hiển thị
- [ ] Redirect sau create thành công
- [ ] Mode switch về view sau edit thành công

## UX Features

- [ ] Unsaved changes warning hoạt động
- [ ] Loading skeleton hiển thị đúng
- [ ] Disabled fields trong view mode
- [ ] Enabled fields trong create/edit mode

## Routes

- [ ] `/manager/products-bouquet` → List view
- [ ] `/manager/products-bouquet/new` → Create form
- [ ] `/manager/products-bouquet/[id]` → View form
- [ ] `/manager/products-bouquet/[id]?mode=edit` → Edit form
- [ ] Navigation giữa routes hoạt động

## Responsive

- [ ] Mobile (375px) - layout stack
- [ ] Tablet (768px) - layout adjust
- [ ] Desktop (1024px) - full layout
- [ ] Large (1440px) - max-width contained

## Accessibility

- [ ] Labels cho tất cả inputs
- [ ] ARIA attributes đầy đủ
- [ ] Keyboard navigation hoạt động
- [ ] Focus visible states
- [ ] Error messages accessible

## Performance

- [ ] Parallel fetching metadata
- [ ] Lazy load heavy sections
- [ ] React.memo cho static components
- [ ] Avoid unnecessary re-renders

## Final Review

- [ ] Linter không có errors
- [ ] TypeScript không có errors
- [ ] Console không có warnings
- [ ] UI/UX consistent với design system
- [ ] Test tất cả flows thành công
