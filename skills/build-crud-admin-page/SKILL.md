---
name: build-crud-admin-page
description: "Skill xay dung trang quan ly CRUD cho PayloadCMS collection. Trigger khi: tao trang admin, build CRUD page, tao man hinh quan ly, new admin screen. Ap dung BouquetScreen pattern: List view voi filter/pagination, Form view voi create/view/edit modes."
category: admin
version: "2.0.0"
author: "Steve Void Team"
pipeline: 3
input_params:
  - collection (required)
  - fields (optional)
  - docsPath (optional)
---

# Build CRUD Admin Page

## Mission

Help AI Agent build full CRUD admin pages for any PayloadCMS collection, following BouquetScreen pattern.

## Boot Sequence

```
1. Read SKILL.md (this file)
2. Read knowledge/README.md (references index)
3. Proceed to Phase 1
```

## Workflow

### Phase 1: Research & Analysis

1. Confirm collection name & fields
2. Read `knowledge/architecture.md` (folder structure)
3. Read `knowledge/template-guide.md` (step-by-step)
4. Reference existing BouquetScreen in codebase

### Phase 2: Implementation

1. Create folder structure
2. Implement types/constants
3. Build ListView + Filters
4. Build FormView (create/view/edit modes)
5. Create route files

## Key Patterns

### Form Mode (from knowledge/implementation-logic.md)

```typescript
type FormMode = 'create' | 'view' | 'edit'
const currentMode = productId
  ? (urlMode === 'edit' ? 'edit' : 'view')
  : 'create'
```

### Route Structure

| Route | Component | Mode |
|-------|-----------|------|
| `/manager/products-{collection}` | ListView | List |
| `/manager/products-{collection}/new` | FormView | Create |
| `/manager/products-{collection}/[id]` | FormView | View |
| `/manager/products-{collection}/[id]?mode=edit` | FormView | Edit |

## Guardrails

```yaml
must:
  - read knowledge/architecture.md before implementing
  - read knowledge/implementation-logic.md for form mode
  - use FormMode type, not boolean props
must_not:
  - skip form validation
  - hardcode fields (read from PayloadCMS schema)
```

## References

| File | Purpose |
|------|---------|
| `knowledge/README.md` | References index |
| `knowledge/architecture.md` | Folder structure, data flow |
| `knowledge/template-guide.md` | Step-by-step guide |
| `knowledge/implementation-logic.md` | Form mode, metadata |
| `knowledge/errors.md` | Common errors |
| `knowledge/ui-skills-summary.md` | UI/UX skills |
| `loop/checklist.md` | Implementation checklist |

## Quality Gate

Before delivery: Run through `loop/checklist.md`

## Success Criteria

- [ ] Folder structure follows architecture.md
- [ ] ProductListView with filters + pagination
- [ ] ProductFormView with 3 modes
- [ ] Route files created
- [ ] Form validation works
- [ ] UI/UX reviewed
