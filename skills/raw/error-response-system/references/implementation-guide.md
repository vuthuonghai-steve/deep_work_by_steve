# Implementation Guide - Error Response System

## Muc Luc

1. [Architecture Overview](#architecture-overview)
2. [File Structure](#file-structure)
3. [Error Codes Reference](#error-codes-reference)
4. [Implementation Patterns](#implementation-patterns)
5. [Frontend Integration](#frontend-integration)

---

## Architecture Overview

### Nguyen Tac Thiet Ke

1. **Single Source of Truth**: Tat ca error codes nam trong `error-codes.json`
2. **Type Safety**: TypeScript types duoc generate tu JSON
3. **Backward Compatible**: Code cu van hoat dong binh thuong
4. **Developer Experience**: Debug de dang voi error codes cu the
5. **User Experience**: Message va suggestion ro rang bang tieng Viet

### Data Flow

```
error-codes.json
       |
       v
generate-types.py --> types.ts
       |
       v
helpers.ts (su dung types)
       |
       v
API Routes (su dung helpers)
       |
       v
Error Response --> Frontend
```

---

## File Structure

### Skill Files

```
.claude/skills/error-response-system/
├── SKILL.md                        # Huong dan skill
├── scripts/
│   ├── validate-error-codes.py     # Validate JSON
│   └── generate-types.py           # Generate types
├── references/
│   ├── implementation-guide.md     # (file nay)
│   └── migration-guide.md          # Huong dan migration
└── assets/
    └── error-codes-template.json   # Template error codes
```

### Implementation Files (Khi Deploy)

```
src/lib/errors/
├── index.ts              # Re-export module
├── types.ts              # Generated types
├── helpers.ts            # Helper functions
├── handler.ts            # Global error handler
└── error-codes.json      # Error codes config
```

---

## Error Codes Reference

### HTTP Errors

| Key | Code | Status | Khi nao su dung |
|-----|------|--------|-----------------|
| BAD_REQUEST | HTTP_400 | 400 | Request sai format |
| UNAUTHORIZED | HTTP_401 | 401 | Chua dang nhap |
| FORBIDDEN | HTTP_403 | 403 | Khong co quyen |
| NOT_FOUND | HTTP_404 | 404 | Resource khong ton tai |
| CONFLICT | HTTP_409 | 409 | Data bi trung |
| VALIDATION_ERROR | HTTP_422 | 422 | Validation failed |
| RATE_LIMITED | HTTP_429 | 429 | Rate limit |
| INTERNAL_ERROR | HTTP_500 | 500 | Server error |
| SERVICE_UNAVAILABLE | HTTP_503 | 503 | Service down |

### Business Error Prefixes

| Prefix | Domain | Mo ta |
|--------|--------|-------|
| AUTH_ | Authentication | Dang nhap, dang ky, tai khoan |
| ORD_ | Orders | Don hang, gio hang |
| PAY_ | Payment | Thanh toan, giao dich |
| PTS_ | Points | Diem thuong |
| VCH_ | Voucher | Ma giam gia |
| STR_ | Store | Cua hang |
| PRD_ | Product | San pham |
| SYS_ | System | He thong |

---

## Implementation Patterns

### Pattern 1: HTTP Error

Khi error lien quan den HTTP protocol (401, 404, etc.):

```typescript
import { httpError } from '@/lib/errors'

export async function GET(req: Request) {
  const user = await getCurrentUser(req)

  // 401 Unauthorized
  if (!user) {
    return httpError('UNAUTHORIZED')
  }

  const resource = await getResource(id)

  // 404 Not Found
  if (!resource) {
    return httpError('NOT_FOUND')
  }

  // 403 Forbidden
  if (resource.ownerId !== user.id) {
    return httpError('FORBIDDEN')
  }

  return successResponse(resource)
}
```

### Pattern 2: Business Error

Khi error lien quan den business logic:

```typescript
import { businessError } from '@/lib/errors'

export async function POST(req: Request) {
  const { email } = await req.json()

  // Check email exists
  const existing = await findUserByEmail(email)
  if (existing) {
    return businessError('AUTH', 'AUTH_002')
    // Response: { code: "AUTH_002", message: "Email da duoc su dung", ... }
  }

  // Check account locked
  if (user.isLocked) {
    return businessError('AUTH', 'AUTH_006')
  }

  // ...
}
```

### Pattern 3: Validation Error

Khi form/request validation that bai:

```typescript
import { validationError, formatZodErrors } from '@/lib/errors'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Email khong hop le'),
  password: z.string().min(8, 'Mat khau phai co it nhat 8 ky tu'),
})

export async function POST(req: Request) {
  const data = await req.json()

  // Validate with Zod
  const result = schema.safeParse(data)
  if (!result.success) {
    return validationError(formatZodErrors(result.error))
    // Response: { code: "HTTP_422", errors: { email: ["Email khong hop le"] } }
  }

  // Or single field
  if (data.email.includes('spam')) {
    return validationError('email', 'Email khong duoc phep')
  }

  // ...
}
```

### Pattern 4: Custom Error voi Details

Khi can them thong tin context:

```typescript
import { businessError } from '@/lib/errors'

export async function POST(req: Request) {
  const { productId, quantity } = await req.json()

  const product = await getProduct(productId)
  if (product.stock < quantity) {
    return businessError('PRD', 'PRD_003', {
      details: `San pham "${product.name}" chi con ${product.stock} san pham`,
      field: 'quantity',
    })
  }

  // ...
}
```

### Pattern 5: Global Error Handler

Wrap route voi global error handling:

```typescript
import { withErrorHandler } from '@/lib/errors'

export const POST = withErrorHandler(async (req: Request) => {
  // Logic co the throw error
  const data = await processData(req)

  // Error tu third-party se duoc catch va format
  await externalService.call(data)

  return successResponse(data)
})
```

---

## Frontend Integration

### TypeScript Types

Frontend co the import types tu shared package hoac copy:

```typescript
// Frontend types/api-error.ts
interface ApiError {
  code: string
  message: string
  details?: string
  field?: string
  suggestion?: string
  timestamp: string
}

interface ApiErrorResponse {
  success: false
  error: ApiError
}
```

### Error Handling Hook

```typescript
// hooks/useApiError.ts
import { useToast } from '@/hooks/useToast'

export function useApiError() {
  const { toast } = useToast()

  const handleError = (error: ApiError) => {
    // Hien thi toast voi message
    toast({
      variant: 'destructive',
      title: error.message,
      description: error.suggestion,
    })

    // Log chi tiet cho developer
    console.error(`[${error.code}]`, error.details)
  }

  return { handleError }
}
```

### Error Display Component

```tsx
// components/ErrorAlert.tsx
interface Props {
  error: ApiError
}

export function ErrorAlert({ error }: Props) {
  return (
    <Alert variant="destructive">
      <AlertTitle>{error.message}</AlertTitle>
      {error.suggestion && (
        <AlertDescription>{error.suggestion}</AlertDescription>
      )}
      {error.field && (
        <p className="text-xs text-muted-foreground">
          Truong loi: {error.field}
        </p>
      )}
    </Alert>
  )
}
```

### Form Field Error

```tsx
// components/FormField.tsx
interface Props {
  error?: ApiError
  fieldName: string
}

export function FormFieldError({ error, fieldName }: Props) {
  if (!error || error.field !== fieldName) return null

  return (
    <p className="text-sm text-destructive">
      {error.message}
    </p>
  )
}
```

### Service Error Handling

```typescript
// services/api-client.ts
import type { ApiErrorResponse } from '@/types/api-error'

async function fetchApi<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options)
  const data = await response.json()

  if (!data.success) {
    const error = data as ApiErrorResponse

    // Map error code to specific handler
    switch (error.error.code) {
      case 'HTTP_401':
        // Redirect to login
        window.location.href = '/login'
        break

      case 'HTTP_429':
        // Show rate limit message
        await sleep(5000)
        return fetchApi(url, options) // Retry
        break
    }

    throw new ApiError(error.error)
  }

  return data.data
}
```

---

## Them Error Code Moi

### Buoc 1: Update error-codes.json

```json
{
  "BUSINESS_ERRORS": {
    "NEW_DOMAIN": {
      "_description": "Mo ta domain moi",
      "NEW_001": {
        "code": "NEW_001",
        "status": 400,
        "message": "Thong bao cho user",
        "details": "Chi tiet cho developer",
        "suggestion": "Cach khac phuc"
      }
    }
  }
}
```

### Buoc 2: Validate

```bash
python scripts/validate-error-codes.py src/lib/errors/error-codes.json
```

### Buoc 3: Generate Types

```bash
python scripts/generate-types.py src/lib/errors/error-codes.json src/lib/errors/
```

### Buoc 4: Su Dung

```typescript
import { businessError } from '@/lib/errors'

return businessError('NEW_DOMAIN', 'NEW_001')
```

---

## Best Practices

### Do

- ✅ Su dung error codes tu error-codes.json
- ✅ Viet message bang tieng Viet
- ✅ Them suggestion huu ich
- ✅ Validate truoc khi commit
- ✅ Generate types sau khi them code moi

### Don't

- ❌ Hardcode error message trong code
- ❌ Su dung error code khong co trong JSON
- ❌ Viet message bang tieng Anh
- ❌ Quen validate va generate types
- ❌ Xoa code cu truoc khi migration xong
