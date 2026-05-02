# Migration Guide - Error Response System

## Muc Luc

1. [Overview](#overview)
2. [Backward Compatibility](#backward-compatibility)
3. [Migration Strategy](#migration-strategy)
4. [Code Examples](#code-examples)
5. [Migration Checklist](#migration-checklist)

---

## Overview

### Muc Tieu

- Chuyen doi tu `errorResponse()` sang `businessError()` / `httpError()`
- Giu nguyen backward compatibility
- Khong break code hien tai
- Migration tung phan (incremental)

### Timeline Khuyen Nghi

1. **Phase 1**: Setup errors module (ngay)
2. **Phase 2**: Su dung format moi cho code moi (1 tuan)
3. **Phase 3**: Migration code cu (2-4 tuan)
4. **Phase 4**: Cleanup (sau khi tat ca stable)

---

## Backward Compatibility

### Nguyen Tac

```
Code cu van hoat dong 100%
Format moi chi la bo sung, khong thay the
errorResponse() van duoc export va su dung duoc
```

### Implementation

File `src/lib/api-response.ts` se re-export tu errors module:

```typescript
// src/lib/api-response.ts

// Keep existing exports
export function successResponse<T>(data: T, message?: string, status = 200) {
  // ... existing implementation
}

export function errorResponse(error: string, status = 400) {
  // ... existing implementation
}

// ... other existing exports

// NEW: Re-export from errors module
export {
  createError,
  httpError,
  validationError,
  businessError,
  withErrorHandler,
} from './errors'
```

### Response Format Comparison

**Format cu:**
```json
{
  "success": false,
  "error": "Email da ton tai"
}
```

**Format moi:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_002",
    "message": "Email da duoc su dung",
    "details": "Email: user@example.com da ton tai trong he thong",
    "suggestion": "Su dung email khac hoac dang nhap neu da co tai khoan",
    "timestamp": "2026-01-16T10:30:00.000Z"
  }
}
```

Frontend can handle ca 2 format trong transition period.

---

## Migration Strategy

### Strategy 1: New Code First

Chi su dung format moi cho code moi:

```typescript
// Route moi - su dung format moi
export async function POST(req: Request) {
  // ...
  return businessError('AUTH', 'AUTH_002')
}

// Route cu - giu nguyen
export async function GET(req: Request) {
  // ...
  return errorResponse('Khong tim thay', 404)  // Van OK
}
```

### Strategy 2: Feature-by-Feature

Migration theo feature/module:

```
Week 1: Auth module
Week 2: Orders module
Week 3: Products module
Week 4: Payment module
```

### Strategy 3: Priority-Based

Migration theo muc do quan trong:

1. **High Priority**: APIs thuong gap loi nhieu
2. **Medium Priority**: APIs core business
3. **Low Priority**: Admin APIs, internal APIs

---

## Code Examples

### Example 1: Auth API

**TRUOC:**
```typescript
// src/app/api/v1/auth/register/route.ts
import { successResponse, errorResponse, validationErrorResponse } from '@/lib/api-response'
import { registerSchema, formatZodErrors } from '@/lib/validation'

export async function POST(req: Request) {
  const data = await req.json()

  // Validation
  const result = registerSchema.safeParse(data)
  if (!result.success) {
    return validationErrorResponse(formatZodErrors(result.error))
  }

  // Check email
  const existing = await payload.find({
    collection: 'users',
    where: { email: { equals: data.email } },
  })

  if (existing.docs.length > 0) {
    return errorResponse('Email da ton tai', 409)
  }

  // Create user
  const user = await payload.create({
    collection: 'users',
    data: result.data,
  })

  return successResponse(user, 'Dang ky thanh cong')
}
```

**SAU:**
```typescript
// src/app/api/v1/auth/register/route.ts
import { successResponse } from '@/lib/api-response'
import { validationError, businessError, formatZodErrors } from '@/lib/errors'
import { registerSchema } from '@/lib/validation'

export async function POST(req: Request) {
  const data = await req.json()

  // Validation - su dung validationError moi
  const result = registerSchema.safeParse(data)
  if (!result.success) {
    return validationError(formatZodErrors(result.error))
  }

  // Check email - su dung businessError
  const existing = await payload.find({
    collection: 'users',
    where: { email: { equals: data.email } },
  })

  if (existing.docs.length > 0) {
    return businessError('AUTH', 'AUTH_002')
  }

  // Create user
  const user = await payload.create({
    collection: 'users',
    data: result.data,
  })

  return successResponse(user, 'Dang ky thanh cong')
}
```

### Example 2: Order API

**TRUOC:**
```typescript
// src/app/api/v1/orders/route.ts
export async function POST(req: Request) {
  const user = await getCurrentUser(req)
  if (!user) {
    return errorResponse('Vui long dang nhap', 401)
  }

  const cart = await getCart(user.id)
  if (cart.items.length === 0) {
    return errorResponse('Gio hang trong', 400)
  }

  for (const item of cart.items) {
    const product = await getProduct(item.productId)
    if (product.stock < item.quantity) {
      return errorResponse(`San pham ${product.name} het hang`, 400)
    }
  }

  // ...
}
```

**SAU:**
```typescript
// src/app/api/v1/orders/route.ts
import { httpError, businessError } from '@/lib/errors'

export async function POST(req: Request) {
  const user = await getCurrentUser(req)
  if (!user) {
    return httpError('UNAUTHORIZED')
  }

  const cart = await getCart(user.id)
  if (cart.items.length === 0) {
    return businessError('ORD', 'ORD_002')
  }

  for (const item of cart.items) {
    const product = await getProduct(item.productId)
    if (product.stock < item.quantity) {
      return businessError('PRD', 'PRD_001', {
        details: `San pham: ${product.name}`,
      })
    }
  }

  // ...
}
```

### Example 3: Payment API

**TRUOC:**
```typescript
// src/app/api/v1/payment/process/route.ts
export async function POST(req: Request) {
  const { amount, method } = await req.json()

  if (amount <= 0) {
    return errorResponse('So tien khong hop le', 400)
  }

  const wallet = await getUserWallet(user.id)
  if (wallet.balance < amount) {
    return errorResponse('So du khong du', 400)
  }

  const supported = ['MOMO', 'VNPAY', 'WALLET']
  if (!supported.includes(method)) {
    return errorResponse('Phuong thuc thanh toan khong ho tro', 400)
  }

  // ...
}
```

**SAU:**
```typescript
// src/app/api/v1/payment/process/route.ts
import { validationError, businessError } from '@/lib/errors'

export async function POST(req: Request) {
  const { amount, method } = await req.json()

  if (amount <= 0) {
    return businessError('PAY', 'PAY_005')
  }

  const wallet = await getUserWallet(user.id)
  if (wallet.balance < amount) {
    return businessError('PAY', 'PAY_001', {
      details: `So du hien tai: ${wallet.balance}`,
    })
  }

  const supported = ['MOMO', 'VNPAY', 'WALLET']
  if (!supported.includes(method)) {
    return businessError('PAY', 'PAY_002')
  }

  // ...
}
```

---

## Migration Checklist

### Pre-Migration

- [ ] Setup errors module (`src/lib/errors/`)
- [ ] Copy error-codes.json tu template
- [ ] Generate types (`python generate-types.py`)
- [ ] Update api-response.ts de re-export
- [ ] Test backward compatibility

### Per-File Migration

- [ ] Import moi tu `@/lib/errors`
- [ ] Map `errorResponse()` -> `httpError()` hoac `businessError()`
- [ ] Map `validationErrorResponse()` -> `validationError()`
- [ ] Tim error code phu hop trong error-codes.json
- [ ] Them error code moi neu can
- [ ] Test API response format

### Post-Migration

- [ ] Update frontend error handling
- [ ] Test tat ca error cases
- [ ] Document bat ky error codes moi
- [ ] Remove unused old error messages

---

## Mapping Table

### HTTP Status Codes

| Truoc | Sau |
|-------|-----|
| `errorResponse(msg, 400)` | `httpError('BAD_REQUEST')` |
| `errorResponse(msg, 401)` | `httpError('UNAUTHORIZED')` |
| `errorResponse(msg, 403)` | `httpError('FORBIDDEN')` |
| `errorResponse(msg, 404)` | `httpError('NOT_FOUND')` |
| `errorResponse(msg, 409)` | `httpError('CONFLICT')` hoac `businessError()` |
| `errorResponse(msg, 500)` | `httpError('INTERNAL_ERROR')` |
| `validationErrorResponse(errors)` | `validationError(errors)` |

### Common Business Errors

| Truoc | Sau |
|-------|-----|
| `'Email da ton tai'` | `businessError('AUTH', 'AUTH_002')` |
| `'Mat khau khong dung'` | `businessError('AUTH', 'AUTH_001')` |
| `'Gio hang trong'` | `businessError('ORD', 'ORD_002')` |
| `'So du khong du'` | `businessError('PAY', 'PAY_001')` |
| `'Voucher het han'` | `businessError('VCH', 'VCH_001')` |
| `'San pham het hang'` | `businessError('PRD', 'PRD_001')` |

---

## Troubleshooting

### Issue: Type Error sau khi generate

**Nguyen nhan:** types.ts chua duoc generate hoac outdated

**Fix:**
```bash
python scripts/generate-types.py
```

### Issue: Error code khong ton tai

**Nguyen nhan:** Su dung code chua co trong JSON

**Fix:**
1. Tim error code phu hop trong error-codes.json
2. Hoac them error code moi

### Issue: Frontend khong hieu format moi

**Nguyen nhan:** Frontend chua update error handling

**Fix:** Update frontend de handle ca 2 format:

```typescript
function isNewErrorFormat(error: any): error is ApiError {
  return typeof error === 'object' && 'code' in error
}

function handleError(response: any) {
  if (response.error) {
    if (isNewErrorFormat(response.error)) {
      // New format
      showError(response.error.message, response.error.suggestion)
    } else {
      // Old format (string)
      showError(response.error)
    }
  }
}
```

---

## FAQ

### Q: Co can migration ngay khong?

A: Khong. Code cu van hoat dong binh thuong. Migration khi co thoi gian.

### Q: Lam sao biet error code nao phu hop?

A: Xem `error-codes.json` hoac chay:
```bash
grep -r "keyword" src/lib/errors/error-codes.json
```

### Q: Neu khong co error code phu hop?

A: Them error code moi:
1. Edit error-codes.json
2. Chay validate-error-codes.py
3. Chay generate-types.py
4. Su dung error code moi

### Q: Frontend can thay doi gi?

A: Update error handling de:
1. Parse error.code thay vi error string
2. Hien thi error.message
3. Hien thi error.suggestion (neu co)
