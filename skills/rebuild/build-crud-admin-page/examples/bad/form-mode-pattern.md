# ❌ Bad Examples: build-crud-admin-page

## 1. Form Mode Pattern

### ❌ Wrong: Boolean props instead of FormMode

```typescript
// DON'T ❌
interface ProductFormViewProps {
  isReadOnly: boolean
  isEditing: boolean
  isCreating: boolean
}

// Usage — confusing!
<ProductFormView isReadOnly={true} isEditing={false} isCreating={false} />
```

### ❌ Wrong: Hardcoded mode strings

```typescript
// DON'T ❌
const mode = 'create' // hardcoded

// DON'T ❌
if (mode === 'create') { // hardcoded literals
  // ...
}
```

### ❌ Wrong: No mode determination from URL

```typescript
// DON'T ❌ — doesn't read URL params
export function ProductFormView({ productId }: { productId?: string }) {
  const mode = 'view' // hardcoded!
  // ...
}
```

---

## 2. Folder Structure

### ❌ Wrong: Skipping index.ts exports

```
src/screens/Admin/BouquetScreen/
├── index.tsx                    # ❌ Empty or missing exports
├── views/
│   ├── ProductListView.tsx    # ❌ No index.ts
│   └── ProductFormView.tsx
├── hooks/
│   ├── useProductMetadata.ts  # ❌ No index.ts
│   └── useProductData.ts
```

### ❌ Wrong: Putting unrelated files in component dirs

```
src/screens/Admin/BouquetScreen/
├── components/
│   ├── ProductForm/
│   │   ├── ProductFormHeader.tsx
│   │   ├── Button.tsx           # ❌ Unrelated!
│   │   └── Modal.tsx            # ❌ Unrelated!
│   └── OtherComponent.tsx       # ❌ Should be separate
```

---

## 3. API Integration

### ❌ Wrong: No error handling

```typescript
// DON'T ❌
const { data } = useQuery({
  queryKey: ['product', productId],
  queryFn: () => fetchProduct(productId),
})

// What if fetchProduct throws? No error handling!
```

### ❌ Wrong: Sequential fetches instead of parallel

```typescript
// DON'T ❌ — waterfall!
const categories = await fetchCategories()
const tags = await fetchTags()    // Waits for categories
const occasions = await fetchOccasions()  // Waits for tags
```

### ❌ Wrong: Direct API call without hook

```typescript
// DON'T ❌ — logic in component
function ProductForm() {
  const [categories, setCategories] = useState([])

  useEffect(() => {
    fetch('/api/categories')  // Direct API call!
      .then(res => res.json())
      .then(setCategories)
  }, [])

  // ...
}
```

---

## 4. Form Validation

### ❌ Wrong: Skipping zod validation

```typescript
// DON'T ❌ — no validation!
const form = useForm({
  defaultValues: { name: '', price: 0 },
})

// Just submits without checking!
const onSubmit = (data: unknown) => {
  api.createProduct(data) // No validation!
}
```

### ❌ Wrong: Not resetting form when data loads

```typescript
// DON'T ❌
useEffect(() => {
  if (product) {
    // Forgot to reset! Form keeps old values
  }
}, [product])
```

### ❌ Wrong: Mutating array directly

```typescript
// DON'T ❌
const updateBomItem = (index: number, field: string, value: unknown) => {
  const current = form.getValues('bomItems')
  current[index][field] = value  // ❌ MUTATION!
  form.setValue('bomItems', current)
}
```

---

## 5. Unsaved Changes

### ❌ Wrong: Not checking dirty state

```typescript
// DON'T ❌
const handleBack = () => {
  router.back() // No check! User loses data!
}

// DON'T ❌ — only checking one condition
if (form.isValid) { // Wrong check!
  // Still can lose data
}
```

---

## 6. Category Scoping (Accessory)

### ❌ Wrong: Getting all categories

```typescript
// DON'T ❌ — gets ALL categories, not just Accessory's
const { data: categories } = useQuery({
  queryKey: ['categories'],
  queryFn: () => fetchCategories(),
})

// User sees "Bó hoa", "Hoa lẻ" when managing Accessories!
```

### ❌ Wrong: Hardcoded category slug

```typescript
// DON'T ❌
const categories = await fetchCategories({
  'parent.slug': 'phu-kien', // Magic string in code!
})

// Should be in config!
const { accessoryCategorySlug } = await getAppConfig()
```

---

## 7. Loading States

### ❌ Wrong: No loading state

```typescript
// DON'T ❌
const { data } = useQuery({ ... })

return (
  <div>
    {/* What shows while loading? Nothing! */}
    {data?.docs.map(product => <ProductRow product={product} />)}
  </div>
)
```

### ❌ Wrong: Spinner instead of skeleton

```typescript
// DON'T ❌ — skeleton is better UX
if (isLoading) {
  return <Spinner />  // Layout shift!
}
```

---

## 8. TypeScript Errors

### ❌ Wrong: Missing type annotation

```typescript
// DON'T ❌ — inferred as SetStateAction<number>
const [page, setPage] = useState(1)

// Later:
setPage(2) // Error if limit was 1!

// FIX:
const [page, setPage] = useState<number>(1)
```

### ❌ Wrong: Using any type

```typescript
// DON'T ❌
const handleSubmit = (data: any) => {
  api.createProduct(data) // No type safety!
}

// FIX:
const handleSubmit = (data: ProductFormData) => {
  api.createProduct(data)
}
```

---

## 9. Route → Component Mapping

### ❌ Wrong: Different components per mode

```typescript
// DON'T ❌ — inconsistent
/manager/products          → ProductListView
/manager/products/new     → ProductCreateView    // Different component!
/manager/products/[id]    → ProductEditView      // Different component!
/manager/products/[id]    → ProductDetailView    // Different component!

// Should use ONE component with mode prop!
```

---

## 10. Route Structure

### ❌ Wrong: Not handling ?mode=edit

```typescript
// DON'T ❌ — ignores mode param
export default function ProductDetailPage({ params }: { params: { id: string } }) {
  return <ProductFormView productId={params.id} />
  // Mode is always 'view' even with ?mode=edit!
}
```

### ❌ Wrong: No useSearchParams

```typescript
// DON'T ❌ — static params only
export default function ProductDetailPage({ params }: { params: { id: string } }) {
  // Can't read ?mode=edit because searchParams is not used!
}
```
