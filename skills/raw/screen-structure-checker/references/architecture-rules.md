# Kiến Trúc Quản Lý Tập Trung cho Screens

Tài liệu này mô tả chi tiết kiến trúc chuẩn cho thư mục screens trong dự án.

## Nguyên Tắc Cốt Lõi

### 1. Separation of Concerns (Tách Biệt Trách Nhiệm)

Mỗi file/thư mục đảm nhận một chức năng riêng biệt:

| Thư mục/File | Trách nhiệm |
|--------------|-------------|
| `index.tsx` | Component chính, composition UI |
| `components/` | Sub-components đặc thù |
| `hooks/` | Custom hooks, logic xử lý |
| `types/` | TypeScript interfaces/types |
| `utils/` | Helper functions |
| `constants/` | Hằng số |

### 2. Single Responsibility (Đơn Trách Nhiệm)

- Mỗi file chỉ làm một việc
- Mỗi component chỉ render một phần UI
- Mỗi hook chỉ quản lý một nhóm logic liên quan

### 3. Centralized Management (Quản Lý Tập Trung)

- Export tập trung qua `index.ts` (barrel exports)
- Types tập trung trong `types/`
- Constants tập trung trong `constants/`

---

## Cấu Trúc Thư Mục Chuẩn

```text
{ScreenName}/
├── index.tsx              # [BẮT BUỘC] Component chính
├── {ScreenName}.tsx       # [ALT] Hoặc file này thay cho index.tsx
│
├── components/            # [KHUYÊN DÙNG] Sub-components
│   ├── cards/             # Nhóm card components
│   │   ├── ProductCard.tsx
│   │   └── index.ts       # Export: export * from './ProductCard'
│   ├── sections/          # Nhóm section components
│   │   ├── HeroSection.tsx
│   │   └── index.ts
│   ├── ui/                # UI components đặc thù
│   └── index.ts           # Barrel export tất cả
│
├── hooks/                 # [KHUYÊN DÙNG] Custom hooks
│   ├── useScreenData.ts   # Fetch data
│   ├── useScreenActions.ts# Actions (CRUD, etc)
│   └── index.ts           # Barrel export
│
├── types/                 # [NÊN CÓ] TypeScript types
│   └── index.ts           # Export interfaces, types
│
├── utils/                 # [TÙY CHỌN] Helper functions
│   └── helpers.ts
│
├── constants/             # [TÙY CHỌN] Constants
│   └── index.ts
│
└── README.md              # [TÙY CHỌN] Documentation
```

---

## Quy Ước Đặt Tên

### Components (`.tsx`)

- **PascalCase**: `ProductCard.tsx`, `HeroSection.tsx`
- Tên mô tả chức năng: `OrderSummaryCard.tsx`
- Tránh tên chung chung: ~~`Card.tsx`~~, ~~`Component.tsx`~~

### Hooks (`.ts`)

- **use prefix**: `useScreenData.ts`, `useProductActions.ts`
- Mô tả chức năng rõ ràng
- Pattern: `use{Feature}{Action}.ts`

### Types/Interfaces (`.ts`)

- **PascalCase** cho type names: `ProductType`, `OrderItem`
- `I` prefix hoặc `Type` suffix: `IProduct`, `ProductType`
- Export từ `types/index.ts`

### Thư mục

- **kebab-case** hoặc **PascalCase** cho screens
- **lowercase** cho sub-directories: `components/`, `hooks/`

---

## Giới Hạn Kích Thước

| Loại | Giới hạn | Hành động khi vượt |
|------|----------|-------------------|
| Component file | 200 lines | Tách thành thư mục riêng |
| Hook file | 100 lines | Tách thành nhiều hooks |
| Total screen | 500 lines | Tách logic vào hooks/services |

### Khi File Vượt 200 Lines

```text
Trước:
  components/
    ComplexComponent.tsx (400 lines)

Sau:
  components/
    ComplexComponent/
      index.tsx (100 lines)
      components/
        SubComponent.tsx
        AnotherSub.tsx
      hooks/
        useComplexLogic.ts
```

---

## Barrel Exports Pattern

### components/index.ts

```typescript
// Re-export từ sub-directories
export * from './cards'
export * from './sections'
export * from './ui'

// Hoặc export trực tiếp
export { ProductCard } from './cards/ProductCard'
export { HeroSection } from './sections/HeroSection'
```

### hooks/index.ts

```typescript
export { useScreenData } from './useScreenData'
export { useScreenActions } from './useScreenActions'
export type { UseScreenDataReturn } from './useScreenData'
```

---

## Ví Dụ Tốt vs Xấu

### ✅ Tốt

```text
CheckoutScreen/
├── index.tsx              # Composition only
├── components/
│   ├── CartSummary.tsx
│   ├── PaymentForm.tsx
│   └── index.ts
├── hooks/
│   ├── useCheckout.ts
│   └── index.ts
└── types/
    └── index.ts
```

### ❌ Xấu

```text
checkout/
├── checkout.tsx           # Tên không chuẩn
├── form.tsx               # Không có components/
├── helpers.js             # Nên dùng .ts
└── types.ts               # Nên có types/index.ts
```

---

## Checklist Audit

Khi review một screen, kiểm tra:

- [ ] Có `index.tsx` hoặc `{ScreenName}.tsx`?
- [ ] Có `components/` với `index.ts`?
- [ ] Có `hooks/` với naming `use*.ts`?
- [ ] Types được tập trung trong `types/`?
- [ ] Không có file > 200 lines?
- [ ] Naming đúng convention (PascalCase, useXxx)?
- [ ] Barrel exports hoạt động đúng?

---

## Tham Chiếu

- [screens/GEMINI.md](../../../Agent-skill-web/src/screens/GEMINI.md) - Tài liệu gốc
- [services/GEMINI.md](../../../Agent-skill-web/src/services/GEMINI.md) - Architecture services
