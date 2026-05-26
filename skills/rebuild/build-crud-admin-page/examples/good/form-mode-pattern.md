# ✅ Good Examples: build-crud-admin-page

## 1. Form Mode Pattern

### ✅ Correct: Using FormMode type

```typescript
// types/index.ts
export type FormMode = 'create' | 'view' | 'edit'

// Component
interface ProductFormViewProps {
  mode: FormMode
  productId?: string
}

export function ProductFormView({ mode, productId }: ProductFormViewProps) {
  const isReadOnly = mode === 'view'
  const isEditing = mode === 'edit'
  const isCreating = mode === 'create'
  // ...
}
```

### ✅ Correct: Mode determination from URL

```typescript
export function ProductFormPage() {
  const params = useParams()
  const searchParams = useSearchParams()
  const productId = params.id as string | undefined
  const urlMode = searchParams.get('mode')

  const currentMode = productId
    ? (urlMode === 'edit' ? 'edit' : 'view')
    : 'create'

  return <ProductFormView mode={currentMode} productId={productId} />
}
```

---

## 2. Folder Structure

### ✅ Correct: Following architecture exactly

```
src/screens/Admin/BouquetScreen/
├── index.tsx                    # ✅ Re-exports
├── views/
│   ├── index.ts               # ✅ Export views
│   ├── ProductListView.tsx    # ✅ List view
│   └── ProductFormView.tsx    # ✅ Form view
├── components/
│   └── ProductForm/
│       ├── index.ts           # ✅
│       ├── ProductFormHeader.tsx
│       └── sections/
│           ├── index.ts       # ✅
│           └── BasicInfoSection.tsx
├── hooks/
│   ├── index.ts               # ✅
│   ├── useProductMetadata.ts  # ✅
│   └── useProductData.ts      # ✅
├── types/
│   └── index.ts               # ✅
└── constants/
    └── index.ts               # ✅
```

### ✅ Correct: index.ts exports

```typescript
// hooks/index.ts
export { useProductMetadata } from './useProductMetadata'
export { useProductData } from './useProductData'

// views/index.ts
export { ProductListView } from './ProductListView'
export { ProductFormView } from './ProductFormView'
```

---

## 3. API Integration

### ✅ Correct: Parallel metadata fetching

```typescript
export function useProductMetadata() {
  return useQuery({
    queryKey: ['product-metadata'],
    queryFn: async () => {
      const [categories, tags, occasions, materials] = await Promise.all([
        fetchCategories(),
        fetchTags(),
        fetchOccasions(),
        fetchMaterials(),
      ])
      return { categories, tags, occasions, materials }
    },
  })
}
```

### ✅ Correct: Proper error handling

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['product', productId],
  queryFn: () => fetchProduct(productId),
  enabled: !!productId, // Only fetch if productId exists
})

if (error) {
  return <ErrorState message="Failed to load product" />
}
```

---

## 4. Form Validation

### ✅ Correct: Zod with resolver

```typescript
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'

const productSchema = z.object({
  name: z.string().min(1, 'Tên sản phẩm là bắt buộc'),
  price: z.number().positive('Giá phải lớn hơn 0'),
  categoryId: z.string().min(1, 'Danh mục là bắt buộc'),
})

export function ProductForm() {
  const form = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: { name: '', price: 0 },
  })
  // ...
}
```

### ✅ Correct: Form reset on data load

```typescript
useEffect(() => {
  if (product) {
    form.reset({
      name: product.name,
      price: product.price,
      categoryId: product.category?.id,
    })
  }
}, [product, form.reset])
```

---

## 5. BOM Array Mutation

### ✅ Correct: Spread instead of mutate

```typescript
// Adding item
const addBomItem = (newItem: BomItem) => {
  const current = form.getValues('bomItems') || []
  form.setValue('bomItems', [...current, newItem])
}

// Updating item
const updateBomItem = (index: number, field: string, value: unknown) => {
  const current = form.getValues('bomItems')
  const updated = [...current]
  updated[index] = { ...updated[index], [field]: value }
  form.setValue('bomItems', updated)
}

// Removing item
const removeBomItem = (index: number) => {
  const current = form.getValues('bomItems')
  form.setValue('bomItems', current.filter((_, i) => i !== index))
}
```

---

## 6. Unsaved Changes Warning

### ✅ Correct: Using form dirty state

```typescript
const { formState: { isDirty } } = form

const handleNavigate = async (path: string) => {
  if (isDirty && currentMode !== 'view') {
    const confirmed = await confirm({
      title: 'Unsaved Changes',
      message: 'You have unsaved changes. Leave anyway?',
    })
    if (!confirmed) return
  }
  router.push(path)
}
```

---

## 7. Category Scoping (Accessory)

### ✅ Correct: Scoped categories for Accessory

```typescript
// useAccessoryCategories.ts
export function useAccessoryCategories() {
  return useQuery({
    queryKey: ['accessory-categories'],
    queryFn: async () => {
      // Try direct nested query first
      const categories = await fetchCategories({
        'parent.slug': 'phu-kien',
        status: 'active',
      })

      if (categories.length > 0) return categories

      // Fallback: 2-step
      const parent = await fetchCategoryBySlug('phu-kien')
      return fetchCategories({ parent: parent.id })
    },
  })
}
```

---

## 8. Route Structure

### ✅ Correct: App Router with mode param

```typescript
// app/(frontend)/manager/products-accessory/[id]/page.tsx
export default async function AccessoryDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>
  searchParams: Promise<{ mode?: string }>
}) {
  const { id } = await params
  const { mode } = await searchParams

  return <AccessoryFormView mode={mode} productId={id} />
}
```

---

## 9. Loading States

### ✅ Correct: Loading skeleton

```typescript
function ProductFormSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-10 w-full" />
      <Skeleton className="h-10 w-1/2" />
      <Skeleton className="h-20 w-full" />
      <div className="flex gap-2">
        <Skeleton className="h-10 w-24" />
        <Skeleton className="h-10 w-24" />
      </div>
    </div>
  )
}
```

---

## 10. Route → Component Mapping

### ✅ Correct: Clear route-component mapping

| Route | Component | Mode |
|-------|-----------|------|
| `/manager/products` | ProductListView | List |
| `/manager/products/new` | ProductFormView | Create |
| `/manager/products/[id]` | ProductFormView | View |
| `/manager/products/[id]?mode=edit` | ProductFormView | Edit |
