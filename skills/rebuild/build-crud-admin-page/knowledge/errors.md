# Errors & Solutions: Bouquet UI Module

## Common Errors

### 1. TypeScript: SetStateAction type error

**Error:**
```
error TS2345: Argument of type 'number' is not assignable to parameter of type 'SetStateAction<1>'
```

**Cause:** useState với const value inference
```typescript
// Wrong
const [page, setPage] = useState(PAGINATION.DEFAULT_PAGE)
```

**Solution:** Explicit type annotation
```typescript
// Correct
const [page, setPage] = useState<number>(PAGINATION.DEFAULT_PAGE)
```

### 2. Form không reset khi product data load

**Cause:** useEffect dependency không đúng

**Solution:**
```typescript
useEffect(() => {
  if (product) {
    resetForm(product)
  }
}, [product, resetForm])
```

### 3. Image preview không hiển thị

**Cause:** Không extract URL từ Media object

**Solution:**
```typescript
const getImageUrl = (img: any, index: number): string | null => {
  if (previewImages[index]) return previewImages[index]
  if (typeof img === 'object' && img?.url) return img.url
  if (typeof img === 'object' && img?.preview) return img.preview
  return null
}
```

### 4. BOM items không update

**Cause:** Mutate array trực tiếp thay vì spread

**Solution:**
```typescript
// Wrong
current[index] = newValue
form.setValue('bomItems', current)

// Correct
current[index] = { ...current[index], [field]: value }
form.setValue('bomItems', [...current])
```

### 5. Mode switching không work

**Cause:** URL query params không được đọc đúng

**Solution:**
```typescript
const searchParams = useSearchParams()
const urlMode = searchParams.get('mode')
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'
```

### 6. Unsaved changes warning không trigger

**Cause:** Không track form dirty state

**Solution:**
```typescript
const { formState: { isDirty } } = form

if (isDirty && currentMode !== 'view') {
  const confirmed = await confirm({...})
  if (!confirmed) return
}
```

### 7. Metadata không load

**Cause:** API endpoints incorrect hoặc collection không tồn tại

**Solution:** Kiểm tra METADATA_ENDPOINTS trong useProductMetadata.ts
```typescript
const METADATA_ENDPOINTS = {
  categories: '/categories?limit=100&depth=0&where[status][equals]=active',
  // ...
}
```

**Với Accessory:** Kiểm tra `useAccessoryCategories` — config `accessoryCategorySlug` trong `app.ts`, fallback 2 bước nếu nested slug không hoạt động.

### 8. ProductFilters hiển thị sai danh mục (Accessory)

**Cause:** Không truyền `categoryOptions` từ `useAccessoryCategories`

**Solution:** ProductListView (Accessory) phải truyền:
```typescript
const { categories } = useAccessoryCategories()
<ProductFilters
  categoryOptions={categories.map((c) => ({ value: c.id, label: c.name }))}
  ...
/>
```

### 9. Zod validation error không hiển thị

**Cause:** Không dùng zodResolver

**Solution:**
```typescript
import { zodResolver } from '@hookform/resolvers/zod'

const form = useForm({
  resolver: zodResolver(productFormSchema),
  // ...
})
```

## Debug Tips

1. **Console log response structure:**
```typescript
console.log('API response:', response)
```

2. **Check form state:**
```typescript
console.log('Form values:', form.getValues())
console.log('Form errors:', form.formState.errors)
```

3. **Check mode:**
```typescript
console.log('Current mode:', currentMode)
console.log('URL mode param:', searchParams.get('mode'))
```

4. **Check metadata loading:**
```typescript
console.log('Metadata:', metadata)
console.log('Metadata loading:', metadataLoading)
```
