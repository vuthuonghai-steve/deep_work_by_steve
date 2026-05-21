# Rules: build-crud-admin-page

## Anti-Patterns

### Must Not Do

```yaml
anti_patterns:
  form_mode:
    - "Use boolean props (isReadOnly, isEditing) instead of FormMode string"
    - "Hardcode 'create'|'view'|'edit' literals instead of FormMode type"
    - "Skip mode determination from URL params"

  folder_structure:
    - "Create files outside folder structure defined in architecture.md"
    - "Skip creating types/index.ts or constants/index.ts"
    - "Put unrelated files in component directories"

  api:
    - "Hardcode API endpoints instead of using constants"
    - "Use wrong HTTP method (POST vs PATCH)"
    - "Skip error handling on API calls"

  form:
    - "Skip zod validation"
    - "Not reset form when product data loads"
    - "Mutate array directly instead of spread"

  ui:
    - "Use boolean props instead of composition"
    - "Skip loading/error states"
    - "No skeleton loading"
    - "Missing disabled state in view mode"
```

### Must Do

```yaml
requirements:
  folder:
    - "Follow architecture.md folder structure exactly"
    - "Create index.ts exports for each directory"
    - "Collocate related files"

  types:
    - "Define FormMode type as 'create' | 'view' | 'edit'"
    - "Export all types from types/index.ts"
    - "Use TypeScript strict mode"

  api:
    - "Use useProductData or useProductMetadata hooks"
    - "Handle loading/error states"
    - "Use Promise.all for parallel fetches"

  form:
    - "Use react-hook-form with zod validation"
    - "Reset form when initialData changes"
    - "Use zodResolver"

  routing:
    - "Use Next.js App Router"
    - "Handle ?mode=edit query param"
    - "Use useSearchParams for mode determination"
```

## Guardrails

```yaml
guardrails:
  G1:
    rule: "Form Mode"
    must: "Use FormMode type, determine mode from URL"
    must_not: ["boolean props for mode", "hardcode mode literals"]

  G2:
    rule: "Folder Structure"
    must: "Follow architecture.md exactly"
    must_not: ["create files outside structure", "skip index.ts exports"]

  G3:
    rule: "API Integration"
    must: ["use hooks for data fetching", "handle loading/error states"]
    must_not: ["direct API calls without hooks", "no error handling"]

  G4:
    rule: "Form Validation"
    must: ["zod validation", "reset form on data load"]
    must_not: ["skip validation", "mutate form state directly"]
```
