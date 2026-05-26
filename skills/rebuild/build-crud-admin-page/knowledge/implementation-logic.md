# Implementation Logic: Product UI Module

Logic hoạt động tổng hợp từ các changes đã triển khai.

---

## 1. Form Mode Pattern

### Xác định mode từ route

```typescript
type FormMode = 'create' | 'view' | 'edit'

// Mode determination
const urlMode = searchParams.get('mode')
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'

// Behavior
const isReadOnly = currentMode === 'view'
const isEditing = currentMode === 'edit'
const isCreating = currentMode === 'create'
```

### Route → Mode mapping

| Route | Mode |
|-------|------|
| `/admin/accessories` hoặc `/manager/products-bouquet` | List |
| `.../new` | create |
| `.../[id]` | view |
| `.../[id]?mode=edit` | edit |

### Lưu ý

- URL shareable, bookmarkable
- `useSearchParams()` để đọc query
- Unsaved changes: check `form.formState.isDirty` trước khi rời trang

---

## 2. Metadata & Categories

### useProductMetadata (Bouquet, SingleFlower)

- **File:** `hooks/useProductMetadata.ts`
- **Fetch:** Tất cả metadata (categories, occasions, tags, products...) song song
- **Endpoint categories:** `/categories?limit=100&depth=0&where[status][equals]=active`
- **Dùng chung** cho BouquetScreen, ProductModal

### useAccessoryCategories (Accessory)

- **File:** `AccessoryScreen/hooks/useAccessoryCategories.ts`
- **Fetch:** Chỉ danh mục con của "Phụ kiện"
- **Config:** `accessoryCategorySlug` từ `app.ts`
- **API ưu tiên:** `where[parent.slug][equals]=phu-kien`
- **Fallback 2 bước:** (1) GET root by slug → (2) GET children by `parent[equals]=<id>`

```typescript
// Endpoint chính
/categories?limit=100&depth=0&where[status][equals]=active&where[parent.slug][equals]=phu-kien

// Fallback
/categories?where[slug][equals]=phu-kien&limit=1  // lấy id
/categories?where[parent][equals]=<id>&limit=100  // lấy con
```

### Chọn hook theo loại product

| Screen | Hook categories | Ghi chú |
|--------|-----------------|---------|
| BouquetScreen | useProductMetadata | Toàn bộ danh mục |
| AccessoryScreen | useAccessoryCategories | Chỉ con của Phụ kiện |
| SingleFlowerScreen | useProductMetadata | Toàn bộ danh mục |

---

## 3. ProductFilters — Categories

### Prop categoryOptions (optional)

- **Nếu có:** Dùng options truyền vào, không fetch
- **Nếu không có:** Tự fetch `/categories?limit=100` (hành vi cũ)

```typescript
// AccessoryScreen: truyền từ useAccessoryCategories
<ProductFilters
  categoryOptions={categories.map((c) => ({ value: c.id, label: c.name }))}
  // ...other props
/>

// BouquetScreen: không truyền → ProductFilters tự fetch
<ProductFilters ... />
```

---

## 4. Data Flow

### ProductFormView

```
Route (productId, mode)
    ↓
useAccessoryCategories() hoặc useProductMetadata()
    ↓
useAccessoryProductData(productId) hoặc useProductData(productId)
    ↓
useAccessoryForm({ initialData: product, onSubmit })
    ↓
BasicInfoSection, PricingSection, ImagesSection...
```

### ProductListView

```
fetchProducts(page, limit, search, category, status, type, trend)
    ↓
ProductFilters (categoryOptions nếu Accessory)
    ↓
ProductsTable
```

---

## 5. Field sets theo loại product

### Bouquet

- BasicInfo, Pricing, BOM, Images, Tags, Status, SEO
- Tab-based form

### Accessory

- BasicInfo (Name, Slug, SKU, Status, **Category scoped**), Pricing, Images, MetaInfo
- Inline sections, không tabs
- Không: BOM, Occasions, Target Ages, SEO, Full Description

---

## 6. Config liên quan

| Config | File | Mục đích |
|--------|------|----------|
| `accessoryCategorySlug` | `configs/app.ts` | Slug danh mục gốc Phụ kiện (`'phu-kien'`) |

**Quy ước:** Magic values phải đưa vào config, không hardcode.

---

## 7. Payload CMS Query

### Nested properties (relationship)

```ts
// Query categories có parent.slug = phu-kien
where[parent.slug][equals]=phu-kien

// Query by parent id
where[parent][equals]=<id>
```

REST API dùng query string; `qs-esm` serialize object → query string.
