# Patterns: build-crud-admin-page

## Core Patterns

### 1. Form Mode Pattern

**Pattern Name:** Form Mode String

**Problem:** Need to show different UI based on whether user is creating, viewing, or editing.

**Solution:**
```typescript
type FormMode = 'create' | 'view' | 'edit'

// Mode determination from URL
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'

// Mode-based booleans
const isReadOnly = mode === 'view'
const isEditing = mode === 'edit'
const isCreating = mode === 'create'
```

**Usage:**
```tsx
<ProductFormView mode={currentMode} productId={productId} />
```

---

### 2. Folder Structure Pattern

**Pattern Name:** Screen Directory

**Structure:**
```
src/screens/Admin/{Collection}Screen/
├── index.tsx                    # Re-exports
├── views/
│   ├── index.ts
│   ├── {Collection}ListView.tsx
│   └── {Collection}FormView.tsx
├── components/
│   └── {Collection}Form/
│       ├── index.ts
│       ├── {Collection}FormHeader.tsx
│       ├── {Collection}FormActions.tsx
│       ├── hooks/
│       │   ├── index.ts
│       │   └── use{Collection}Form.ts
│       └── sections/
│           ├── index.ts
│           └── ...Section.tsx
├── hooks/
│   ├── index.ts
│   ├── use{Collection}Metadata.ts
│   └── use{Collection}Data.ts
├── types/
│   └── index.ts
└── constants/
    └── index.ts
```

---

### 3. Route → Mode Pattern

**Pattern:** Route determines form mode

| Route | Mode | productId |
|-------|------|-----------|
| `/manager/products-{collection}` | List | - |
| `/manager/products-{collection}/new` | Create | - |
| `/manager/products-{collection}/[id]` | View | ✅ |
| `/manager/products-{collection}/[id]?mode=edit` | Edit | ✅ |

**Implementation:**
```typescript
// In page.tsx
const searchParams = useSearchParams()
const params = useParams()
const productId = params.id as string | undefined
const urlMode = searchParams.get('mode')

const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'
```

---

### 4. Data Fetching Pattern

**Pattern:** Parallel metadata + product data

```typescript
// useProductMetadata.ts
export function useProductMetadata() {
  return useQuery({
    queryKey: ['product-metadata'],
    queryFn: async () => {
      const [categories, tags, occasions] = await Promise.all([
        fetchCategories(),
        fetchTags(),
        fetchOccasions(),
      ])
      return { categories, tags, occasions }
    },
  })
}
```

---

### 5. Form Reset Pattern

**Pattern:** Reset form when product data loads

```typescript
useEffect(() => {
  if (product) {
    reset(product)
  }
}, [product, reset])

// Or with dependencies
useEffect(() => {
  if (product) {
    form.reset({
      name: product.name,
      price: product.price,
      // ...
    })
  }
}, [product])
```

---

### 6. Category Scoping Pattern

**Pattern:** Accessory needs scoped categories (children of "Phụ kiện")

```typescript
// useAccessoryCategories.ts
export function useAccessoryCategories() {
  return useQuery({
    queryKey: ['accessory-categories'],
    queryFn: async () => {
      // Primary: nested slug query
      const categories = await fetchCategories({
        where: 'parent.slug equals phu-kien',
      })
      if (categories.length > 0) return categories

      // Fallback: 2-step
      const parent = await fetchCategoryBySlug('phu-kien')
      return fetchCategories({ where: `parent equals ${parent.id}` })
    },
  })
}
```

---

### 7. BOM Array Mutation Pattern

**Pattern:** Never mutate arrays directly

```typescript
// Wrong ❌
current[index] = newValue
form.setValue('bomItems', current)

// Correct ✅
current[index] = { ...current[index], [field]: newValue }
form.setValue('bomItems', [...current])
```

---

### 8. Unsaved Changes Pattern

**Pattern:** Warn before leaving with unsaved changes

```typescript
const { formState: { isDirty } } = form

// In navigation handler
if (isDirty && currentMode !== 'view') {
  const confirmed = await confirm({
    title: 'Unsaved changes',
    message: 'You have unsaved changes. Leave anyway?',
  })
  if (!confirmed) return
}
```
