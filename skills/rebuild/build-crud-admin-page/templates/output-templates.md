# Templates: build-crud-admin-page

## Output Templates

### 1. SKILL.md Template

```markdown
---
name: {skill-name}
description: "Skill mo ta chuc nang. Trigger khi: trigger phrases. Ap dung cho: use case."
category: {category}
version: "1.0.0"
author: "Steve Void Team"
---

# {Skill Name}

## Mission

[Mission statement - 1-2 sentences]

## Boot Sequence

```
1. Read SKILL.md (this file)
2. Read knowledge/README.md (references index)
3. Proceed to Phase 1
```

## Workflow

### Phase 1: [Name]

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Phase 2: [Name]

1. [Step 1]
2. [Step 2]

## Key Patterns

### [Pattern Name]

[Code example]

## Guardrails

```yaml
must:
  - [Requirement 1]
  - [Requirement 2]
must_not:
  - [Forbidden 1]
```

## References

| File | Purpose |
|------|---------|
| `knowledge/README.md` | Overview |
| `knowledge/architecture.md` | Structure |
| `loop/checklist.md` | Checklist |

## Quality Gate

Before delivery: Run through `loop/checklist.md`
```

---

### 2. types/index.ts Template

```typescript
// types/index.ts

export type {FormMode} from '{path-to-original}'

// Collection-specific types
export interface {Collection}FormData {
  // Fields
  name: string
  slug: string
  status: 'active' | 'draft' | 'archived'
  // ... other fields
}

export interface {Collection}ListItem {
  id: string
  name: string
  slug: string
  status: string
  createdAt: string
  updatedAt: string
}

// Filter types
export interface {Collection}Filters {
  search?: string
  status?: string
  category?: string
  page?: number
  limit?: number
}

// API Response types
export interface {Collection}ListResponse {
  docs: {Collection}ListItem[]
  totalDocs: number
  page: number
  limit: number
}
```

---

### 3. constants/index.ts Template

```typescript
// constants/index.ts

import { FormMode } from '../types'

// Routes
export const ROUTES = {
  LIST: '/manager/products-{collection}',
  NEW: '/manager/products-{collection}/new',
  DETAIL: (id: string) => `/manager/products-{collection}/${id}`,
  EDIT: (id: string) => `/manager/products-{collection}/${id}?mode=edit`,
} as const

// Form Tabs (if using tabs)
export const FORM_TABS = {
  BASIC_INFO: 'basic-info',
  PRICING: 'pricing',
  IMAGES: 'images',
  STATUS: 'status',
  SEO: 'seo',
} as const

// Messages
export const MESSAGES = {
  CREATE_SUCCESS: 'Tạo {collection} thành công',
  UPDATE_SUCCESS: 'Cập nhật {collection} thành công',
  DELETE_SUCCESS: 'Xóa {collection} thành công',
  CREATE_ERROR: 'Tạo {collection} thất bại',
  UPDATE_ERROR: 'Cập nhật {collection} thất bại',
  DELETE_ERROR: 'Xóa {collection} thất bại',
  UNSAVED_CHANGES: 'Bạn có thay đổi chưa lưu. Rời trang?',
} as const

// Pagination defaults
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_LIMIT: 20,
  MAX_LIMIT: 100,
} as const
```

---

### 4. Route page.tsx Template

```typescript
// app/(frontend)/manager/products-{collection}/page.tsx

import { ProductListView } from '@/screens/Admin/{Collection}Screen'

interface PageProps {
  searchParams: Promise<{
    page?: string
    limit?: string
    search?: string
    status?: string
    category?: string
  }>
}

export default async function {Collection}ListPage({ searchParams }: PageProps) {
  const params = await searchParams

  return (
    <ProductListView
      initialPage={Number(params.page) || 1}
      initialLimit={Number(params.limit) || 20}
      initialSearch={params.search}
      initialStatus={params.status}
      initialCategory={params.category}
    />
  )
}
```

---

### 5. ProductListView.tsx Template

```typescript
// views/{Collection}ListView.tsx

'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ProductFilters } from '@/components/ProductFilters'
import { ProductTable } from '@/components/ProductTable'
import { Pagination } from '@/components/ui/pagination'
import { fetch{Collection}List } from '@/services/{collection}-api'
import { PAGINATION } from '../constants'

interface {Collection}ListViewProps {
  initialPage?: number
  initialLimit?: number
  initialSearch?: string
  initialStatus?: string
  initialCategory?: string
}

export function {Collection}ListView({
  initialPage = PAGINATION.DEFAULT_PAGE,
  initialLimit = PAGINATION.DEFAULT_LIMIT,
  initialSearch = '',
  initialStatus = '',
  initialCategory = '',
}: {Collection}ListViewProps = {}) {
  const [page, setPage] = useState(initialPage)
  const [limit, setLimit] = useState(initialLimit)
  const [search, setSearch] = useState(initialSearch)
  const [status, setStatus] = useState(initialStatus)
  const [category, setCategory] = useState(initialCategory)

  const { data, isLoading } = useQuery({
    queryKey: ['{collection}', { page, limit, search, status, category }],
    queryFn: () => fetch{Collection}List({ page, limit, search, status, category }),
  })

  return (
    <div className="space-y-4">
      <ProductFilters
        search={search}
        onSearchChange={setSearch}
        status={status}
        onStatusChange={setStatus}
        category={category}
        onCategoryChange={setCategory}
      />

      <ProductTable
        data={data?.docs || []}
        isLoading={isLoading}
      />

      {data && (
        <Pagination
          page={page}
          limit={limit}
          total={data.totalDocs}
          onPageChange={setPage}
          onLimitChange={setLimit}
        />
      )}
    </div>
  )
}
```

---

### 6. ProductFormView.tsx Template

```typescript
// views/{Collection}FormView.tsx

'use client'

import { useParams, useRouter, useSearchParams } from 'next/navigation'
import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { use{Collection}Data } from '../hooks/use{Collection}Data'
import { use{Collection}Metadata } from '../hooks/use{Collection}Metadata'
import { {collection}FormSchema, type {Collection}FormData } from '../types'
import { FormMode } from '../types'

export function {Collection}FormView() {
  const params = useParams()
  const router = useRouter()
  const searchParams = useSearchParams()

  const productId = params.id as string | undefined
  const urlMode = searchParams.get('mode')
  const currentMode = productId
    ? (urlMode === 'edit' ? 'edit' : 'view')
    : 'create'

  const isReadOnly = currentMode === 'view'
  const isEditing = currentMode === 'edit'
  const isCreating = currentMode === 'create'

  const form = useForm<{Collection}FormData>({
    resolver: zodResolver({collection}FormSchema),
    defaultValues: { /* default values */ },
  })

  const { product, isLoading: productLoading } = use{Collection}Data(productId)
  const { metadata, isLoading: metadataLoading } = use{Collection}Metadata()

  // Reset form when product loads
  useEffect(() => {
    if (product) {
      form.reset(product)
    }
  }, [product, form])

  const onSubmit = async (data: {Collection}FormData) => {
    try {
      if (isCreating) {
        // POST
      } else {
        // PATCH
      }
    } catch (error) {
      // Handle error
    }
  }

  if (productLoading || metadataLoading) {
    return <FormSkeleton />
  }

  return (
    <Form form={form} onSubmit={onSubmit} isReadOnly={isReadOnly}>
      {/* Form content */}
    </Form>
  )
}
```
