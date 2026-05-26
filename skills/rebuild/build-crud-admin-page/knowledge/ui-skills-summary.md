# UI Skills Summary

Tóm tắt 4 skills UI/UX cần tham khảo khi xây dựng trang admin CRUD.

---

## 1. ui-ux-pro-max

**Mục đích:** Design system intelligence - cung cấp styles, color palettes, font pairings.

### Khi nào dùng

- Trước khi code: tìm design inspiration
- Chọn color palette phù hợp với product type
- Chọn typography (font pairings)
- Review UI cuối cùng

### Commands chính

```bash
# Search theo domain
python3 <skill-path>/scripts/search.py "<keyword>" --domain <domain>

# Domains: product, style, typography, color, landing, chart, ux, prompt
# Stacks: html-tailwind, react, nextjs, vue, svelte
```

### Pre-Delivery Checklist quan trọng

- [ ] No emojis as icons (dùng SVG)
- [ ] All clickable elements có `cursor-pointer`
- [ ] Light/dark mode contrast đủ
- [ ] Hover states không gây layout shift
- [ ] Transitions smooth (150-300ms)

---

## 2. vercel-react-best-practices

**Mục đích:** Performance optimization cho React/Next.js.

### Rule Categories by Priority

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Eliminating Waterfalls | CRITICAL |
| 2 | Bundle Size Optimization | CRITICAL |
| 3 | Server-Side Performance | HIGH |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH |
| 5 | Re-render Optimization | MEDIUM |

### Rules quan trọng cho Admin CRUD

**CRITICAL:**
- `async-parallel` - Promise.all() cho independent operations
- `bundle-barrel-imports` - Import trực tiếp, tránh barrel files
- `bundle-dynamic-imports` - next/dynamic cho heavy components

**HIGH:**
- `server-parallel-fetching` - Parallelize fetches
- `server-serialization` - Minimize data to client

**MEDIUM:**
- `rerender-memo` - Memoize expensive components
- `rerender-dependencies` - Primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans

---

## 3. vercel-composition-patterns

**Mục đích:** Component architecture - tránh boolean prop proliferation.

### Rule Categories

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Component Architecture | HIGH |
| 2 | State Management | MEDIUM |
| 3 | Implementation Patterns | MEDIUM |

### Patterns quan trọng cho Admin CRUD

**HIGH:**
- `architecture-avoid-boolean-props` - Dùng composition thay vì boolean props
- `architecture-compound-components` - Compound components với shared context

**MEDIUM:**
- `state-lift-state` - Move state vào provider cho sibling access
- `patterns-explicit-variants` - Explicit variant components thay vì boolean modes
- `patterns-children-over-render-props` - Children > renderX props

### Áp dụng cho Form

```typescript
// Thay vì:
<ProductForm isReadOnly={true} isEditing={false} />

// Dùng:
<ProductForm mode="view" />
// hoặc compound components:
<ProductForm.View data={product} />
<ProductForm.Edit data={product} onSubmit={handleSubmit} />
```

---

## 4. web-design-guidelines

**Mục đích:** Review UI code theo Web Interface Guidelines.

### Workflow

1. Fetch guidelines từ source URL
2. Read files cần review
3. Check against all rules
4. Output findings theo format `file:line`

### Khi nào dùng

- Sau khi hoàn thành UI
- Review accessibility
- Audit design consistency
- Check responsive behavior

### Source URL

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

---

## Thứ tự áp dụng cho CRUD Admin

1. **ui-ux-pro-max** - Generate design system TRƯỚC khi code
2. **vercel-composition-patterns** - Thiết kế component architecture
3. **vercel-react-best-practices** - Trong quá trình implement
4. **web-design-guidelines** - Review cuối cùng

---

## Quick Reference: Form Mode Pattern

```typescript
// Types
type FormMode = 'create' | 'view' | 'edit'

// Mode-based behavior (không dùng boolean props)
const isReadOnly = mode === 'view'
const isEditing = mode === 'edit'
const isCreating = mode === 'create'

// URL-based mode determination
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'
```
