# Template Guide: Áp dụng cho Collections khác

## Overview

Hướng dẫn này giúp bạn tái sử dụng pattern từ BouquetScreen cho các collection khác như SingleFlowerScreen, AccessoryScreen, v.v.

## Step 1: Copy Folder Structure

```bash
cp -r src/screens/Admin/BouquetScreen src/screens/Admin/{NewCollection}Screen
```

## Step 2: Update Types (types/index.ts)

```typescript
// 1. Đổi tên types
export type ProductFormMode = 'create' | 'view' | 'edit'

// 2. Update ProductFormData cho collection mới
export interface ProductFormData {
  // Giữ các fields chung
  name: string
  slug: string
  // ...

  // Thêm/bỏ fields specific cho collection
  // VD: Accessory không cần bomItems
}

// 3. Update labels
export const productTypeLabels = {
  // ...
}
```

## Step 3: Update Constants (constants/index.ts)

```typescript
// 1. Update routes
export const ROUTES = {
  LIST: '/manager/products-{collection}',
  NEW: '/manager/products-{collection}/new',
  DETAIL: (id: string) => `/manager/products-{collection}/${id}`,
  EDIT: (id: string) => `/manager/products-{collection}/${id}?mode=edit`,
}

// 2. Update messages
export const MESSAGES = {
  CREATE_SUCCESS: 'Tạo {tên collection} thành công',
  // ...
}

// 3. Update form tabs nếu cần
export const FORM_TABS = {
  // Bỏ/thêm tabs không cần thiết
}
```

## Step 4: Update Hooks

### useProductMetadata.ts
- Giữ nguyên nếu dùng chung metadata (Bouquet, SingleFlower)
- Hoặc tạo hook mới nếu cần metadata khác

### useAccessoryCategories.ts (nếu scope danh mục)
- Dùng cho Accessory: chỉ lấy danh mục con của root (config `accessoryCategorySlug`)
- API: `where[parent.slug][equals]=phu-kien` hoặc fallback 2 bước
- Xem `implementation-logic.md` và `notes-product-workflow.md`

### useProductData.ts
- Update fetch function nếu API khác
- Update data transformation

### useProductForm.ts
- Update Zod schema cho fields mới
- Update default values
- Bỏ/thêm handlers (VD: không cần BOM handlers cho Accessory)

## Step 5: Update Form Sections

### Sections có thể reuse:
- BasicInfoSection (đổi type fixed)
- PricingSection
- ImagesSection
- TagsSection
- StatusSection
- SeoSection

### Sections cần modify:
- BomSection - Chỉ dùng cho Bouquet
- Các section specific cho collection mới

```typescript
// VD: Accessory không cần BOM, thay bằng section khác
<TabsContent value={FORM_TABS.SPECIFICATIONS}>
  <SpecificationsSection form={form} isReadOnly={isReadOnly} />
</TabsContent>
```

## Step 6: Update Views

### ProductListView.tsx
```typescript
// 1. Update fetchProducts call
const response = await fetchProductsService(
  page, limit, search, category, status,
  '{collection-type}', // bouquet -> single/accessory
  trend,
)

// 2. Update labels
productLabel="{Tên collection}"
emptyStateTitle="Không có {collection}"

// 3. Nếu scope categories (vd: Accessory): truyền categoryOptions
const { categories } = useAccessoryCategories()
<ProductFilters
  categoryOptions={categories.map((c) => ({ value: c.id, label: c.name }))}
  ...
/>
```

### ProductFormView.tsx
```typescript
// 1. Update submit handler
await createProduct({ ...data, type: '{collection-type}' })

// 2. Update tabs (bỏ/thêm sections)
```

## Step 7: Create Route Files

```
src/app/(frontend)/manager/products-{collection}/
├── page.tsx              # List view
├── new/
│   └── page.tsx          # Create mode
└── [id]/
    └── page.tsx          # View/Edit mode
```

## Step 8: Update Entry Point (index.tsx)

```typescript
export { ProductListView, ProductFormView } from './views'
// Export thêm components nếu cần
```

## Checklist

- [ ] Copy folder structure
- [ ] Update types/index.ts
- [ ] Update constants/index.ts
- [ ] Update/create hooks
- [ ] Modify form sections
- [ ] Update views
- [ ] Create route files
- [ ] Test all modes (create/view/edit)
- [ ] Test navigation
- [ ] Test form validation
- [ ] Test API integration

## Example: AccessoryScreen

```typescript
// types/index.ts
export interface AccessoryFormData {
  name: string
  slug: string
  sku: string
  // ... (không có bomItems)
  specifications?: {
    material?: string
    dimensions?: string
    weight?: string
  }
}

// constants/index.ts
export const FORM_TABS = {
  BASIC_INFO: 'basic-info',
  PRICING: 'pricing',
  SPECIFICATIONS: 'specifications', // Thay BOM
  IMAGES: 'images',
  TAGS: 'tags',
  STATUS: 'status',
  SEO: 'seo',
}
```
