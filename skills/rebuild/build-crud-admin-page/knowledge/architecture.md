# Architecture: Bouquet UI Module

## Overview

Module quản lý sản phẩm bó hoa với full-page views thay vì modal-based approach.

## Folder Structure

```
src/screens/Admin/BouquetScreen/
├── index.tsx                    # Entry point, re-exports views
├── views/
│   ├── index.ts                 # Export views
│   ├── ProductListView.tsx      # Danh sách sản phẩm
│   └── ProductFormView.tsx      # Form tạo/xem/sửa
├── components/
│   └── ProductForm/
│       ├── index.ts
│       ├── ProductFormHeader.tsx
│       ├── ProductFormActions.tsx
│       ├── hooks/
│       │   ├── index.ts
│       │   └── useProductForm.ts
│       └── sections/
│           ├── index.ts
│           ├── BasicInfoSection.tsx
│           ├── PricingSection.tsx
│           ├── BomSection.tsx
│           ├── ImagesSection.tsx
│           ├── TagsSection.tsx
│           ├── StatusSection.tsx
│           └── SeoSection.tsx
├── hooks/
│   ├── index.ts
│   ├── useProductMetadata.ts    # Fetch metadata (categories, tags...)
│   └── useProductData.ts        # Fetch product by ID
├── types/
│   └── index.ts                 # TypeScript types
└── constants/
    └── index.ts                 # Routes, tabs, messages
```

## Route Structure

| Route | Component | Mode |
|-------|-----------|------|
| `/manager/products-bouquet` | ProductListView | List |
| `/manager/products-bouquet/new` | ProductFormView | Create |
| `/manager/products-bouquet/[id]` | ProductFormView | View |
| `/manager/products-bouquet/[id]?mode=edit` | ProductFormView | Edit |

## Data Flow

```
┌──────────────────┐
│   Route Page     │
│  (Next.js App)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  ProductFormView │ ◄── mode, productId props
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│useProduct│ │useProduct   │
│Data     │ │Metadata     │
└────┬───┘ └──────┬───────┘
     │            │
     ▼            ▼
┌────────────────────┐
│   PayloadCMS API   │
└────────────────────┘
```

## Form Mode Pattern

```typescript
type FormMode = 'create' | 'view' | 'edit'

// Mode determination
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'

// Mode-based behavior
const isReadOnly = mode === 'view'
const isEditing = mode === 'edit'
const isCreating = mode === 'create'
```

## Component Responsibilities

### ProductListView
- Fetch và hiển thị danh sách sản phẩm
- Filters (search, status, category, trend)
- Pagination
- Actions (view, edit, delete)
- Navigate đến form views

### ProductFormView
- Orchestrate form state và submission
- Handle mode switching (view ↔ edit)
- Unsaved changes warning
- Loading/error states

### Form Sections
- Mỗi section xử lý 1 nhóm fields
- Nhận `form` và `isReadOnly` props
- Self-contained logic

### Hooks
- `useProductForm`: Form state, validation, handlers
- `useProductData`: Fetch product by ID
- `useProductMetadata`: Fetch dropdown options

## Key Technologies

- **Form**: react-hook-form + zod validation
- **UI**: shadcn/ui (Tabs, Form, Input...)
- **State**: React hooks (local state)
- **API**: PayloadCMS REST API

## Best Practices Applied

1. **Single Responsibility**: Mỗi component/hook 1 nhiệm vụ
2. **Colocation**: Related files gần nhau
3. **Type Safety**: Full TypeScript coverage
4. **Reusability**: Hooks và sections có thể reuse
5. **Mode-based UI**: Cùng component, behavior khác nhau theo mode
