---
name: error-response-system
description: Skill chuan hoa Error Response cho API. Su dung khi can (1) tao error response moi, (2) them error code cho feature, (3) debug loi API, (4) migration tu format cu sang format moi. Skill nay nen duoc su dung khi nguoi dung can thong nhat error response format hoac tao he thong error handling moi.
category: implementation
pipeline:
  stage_order: 11
  input_contract: []
  output_contract:
    - type: directory
      path: "src/lib/errors"
      format: directory
  dependencies: []
---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file)

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
- [references/AI-AGENT-GUIDE.md](references/AI-AGENT-GUIDE.md) - Hướng dẫn sử dụng cho AI Agent
- [references/implementation-guide.md](references/implementation-guide.md) - Chi tiết implementation patterns

### Tier 3: Optional (load when needed)
- [references/migration-guide.md](references/migration-guide.md) - Hướng dẫn migration từ format cũ
- @.claude/skills/error-response-system/scripts/generate-types.py - Script generate TypeScript types
- @.claude/skills/error-response-system/scripts/validate-error-codes.py - Script validate error codes JSON
- [assets/error-codes-template.json](assets/error-codes-template.json) - Template cho error codes

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào. 
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!


# Error Response System

## Overview

Skill nay cung cap he thong chuan hoa error responses cho toan bo API cua Agent-skill. No giup:

1. **Developer**: Debug nhanh hon voi error codes cu the
2. **Frontend**: Hien thi message va suggestion cho user
3. **Team**: Thong nhat format error response toan project
4. **Maintenance**: De dang them error codes moi qua JSON config

---

## Khi Nao Su Dung Skill Nay

### 1. Tao Error Response Moi

- Khi can tra ve error tu API endpoint
- Khi can validation error voi field cu the
- Khi can business logic error (AUTH, ORD, PAY, etc.)

### 2. Them Error Code Cho Feature

- Khi phat trien feature moi can error handling
- Khi can error code cho nghiep vu cu the
- Khi can thong bao loi co y nghia cho user

### 3. Debug Loi API

- Khi can hieu y nghia cua error code
- Khi can tim nguyen nhan loi tu code
- Khi can goi y khac phuc loi

### 4. Migration Tu Format Cu

- Khi can chuyen doi errorResponse() -> businessError()
- Khi can them error code cho API hien tai
- Khi can thong nhat format toan project

---

## Workflow Tong Quan

```
[Trigger: Can error handling]
         |
         v
[PHASE 1: Xac Dinh Error Type]
- HTTP Error (400, 401, 404, 500)?
- Business Error (AUTH, ORD, PAY)?
- Validation Error?
         |
         v
[PHASE 2: Chon/Tao Error Code]
- Tim trong error-codes.json
- Tao code moi neu chua co
- Dung dung prefix (AUTH_, ORD_, PAY_)
         |
         v
[PHASE 3: Su Dung Helper]
- httpError() cho HTTP errors
- businessError() cho business logic
- validationError() cho form validation
         |
         v
[Output: Structured Error Response]
```

---

## PHASE 1: Xac Dinh Error Type

### HTTP Errors (4xx, 5xx)

Su dung khi error lien quan den HTTP protocol:

| Code | Su dung khi |
|------|-------------|
| 400 | Request sai format, thieu params |
| 401 | Chua dang nhap, token het han |
| 403 | Khong co quyen truy cap |
| 404 | Resource khong ton tai |
| 409 | Conflict (duplicate, da ton tai) |
| 422 | Validation failed |
| 429 | Rate limit exceeded |
| 500 | Server error |

### Business Errors

Su dung khi error lien quan den nghiep vu:

| Prefix | Domain | Vi du |
|--------|--------|-------|
| AUTH_ | Authentication | AUTH_001: Email da ton tai |
| ORD_ | Orders | ORD_001: Don hang da huy |
| PAY_ | Payment | PAY_001: So du khong du |
| PTS_ | Points | PTS_001: Diem khong du |
| VCH_ | Voucher | VCH_001: Voucher het han |
| STR_ | Store | STR_001: Cua hang khong hoat dong |
| PRD_ | Product | PRD_001: San pham het hang |
| SYS_ | System | SYS_001: Service khong kha dung |

### Validation Errors

Su dung khi form/request validation that bai:

- Field-level validation (email, password, etc.)
- Business rules validation
- Format validation (phone, date, etc.)

---

## PHASE 2: Chon/Tao Error Code

### Buoc 2.1: Tim Error Code Co San

Doc file `src/lib/errors/error-codes.json`:

```bash
# Tim error code theo keyword
grep -r "AUTH_" src/lib/errors/error-codes.json
```

### Buoc 2.2: Tao Error Code Moi (Neu Can)

Neu chua co error code phu hop, them vao file `error-codes.json`:

```json
{
  "BUSINESS_ERRORS": {
    "AUTH": {
      "AUTH_010": {
        "code": "AUTH_010",
        "status": 400,
        "message": "Thong bao cho user",
        "details": "Chi tiet ky thuat cho developer",
        "suggestion": "Goi y cach khac phuc"
      }
    }
  }
}
```

**Quy tac dat ten:**
- Prefix: 3 ky tu viet hoa (AUTH, ORD, PAY, etc.)
- Number: 3 chu so (001, 002, 010, etc.)
- Format: `PREFIX_NNN`

### Buoc 2.3: Generate Types

Sau khi them error code moi, chay:

```bash
python scripts/generate-types.py
```

---

## PHASE 3: Su Dung Helper Functions

### HTTP Errors

```typescript
import { httpError } from '@/lib/errors'

// 400 Bad Request
return httpError('BAD_REQUEST')

// 401 Unauthorized
return httpError('UNAUTHORIZED')

// 404 Not Found
return httpError('NOT_FOUND')

// Custom message
return httpError('NOT_FOUND', 'San pham khong ton tai')
```

### Business Errors

```typescript
import { businessError } from '@/lib/errors'

// Voi error code
return businessError('AUTH', 'AUTH_002')

// Voi custom message
return businessError('ORD', 'ORD_001', {
  details: 'Order ID: 12345'
})
```

### Validation Errors

```typescript
import { validationError, formatZodErrors } from '@/lib/errors'

// Single field
return validationError('email', 'Email khong hop le')

// Multiple fields (tu Zod)
const result = schema.safeParse(data)
if (!result.success) {
  return validationError(formatZodErrors(result.error))
}
```

### Custom Errors

```typescript
import { createError } from '@/lib/errors'

return createError('CUSTOM_ERROR', 'Custom message', {
  status: 418,
  details: 'Technical details',
  suggestion: 'How to fix'
})
```

---

## Response Format

### Success Response (Giu Nguyen)

```json
{
  "success": true,
  "data": { ... },
  "message": "Thanh cong"
}
```

### Error Response (Moi)

```json
{
  "success": false,
  "error": {
    "code": "AUTH_002",
    "message": "Email da duoc su dung",
    "details": "Email: user@example.com da ton tai trong he thong",
    "field": "email",
    "suggestion": "Su dung email khac hoac dang nhap",
    "timestamp": "2026-01-16T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

## Migration Guide

### Tu Format Cu Sang Format Moi

**Truoc (cu - van hoat dong):**
```typescript
return errorResponse('Email da ton tai', 409)
```

**Sau (moi - khuyen nghi):**
```typescript
return businessError('AUTH', 'AUTH_002')
```

### Backward Compatibility

Code cu van hoat dong binh thuong. `api-response.ts` da re-export tu `./errors`:

```typescript
// File: src/lib/api-response.ts
export {
  createError,
  httpError,
  validationError,
  businessError,
  withErrorHandler,
} from './errors'
```

---

## Files Quan Trong

### Skill Resources

| File | Muc dich |
|------|----------|
| `assets/error-codes-template.json` | Template error codes |
| `scripts/validate-error-codes.py` | Validate JSON format |
| `scripts/generate-types.py` | Generate TypeScript types |
| `references/implementation-guide.md` | Patterns chi tiet |
| `references/migration-guide.md` | Huong dan migration |

### Implementation Files (Khi Deploy)

| File | Muc dich |
|------|----------|
| `src/lib/errors/index.ts` | Re-export module |
| `src/lib/errors/types.ts` | TypeScript interfaces |
| `src/lib/errors/helpers.ts` | Helper functions |
| `src/lib/errors/handler.ts` | Global error handler |
| `src/lib/errors/error-codes.json` | Error codes config |

---

## Vi Du Cu The

### 1. Dang Ky Nguoi Dung

```typescript
// src/app/api/v1/auth/register/route.ts
import { businessError, validationError } from '@/lib/errors'

export async function POST(req: Request) {
  const data = await req.json()

  // Validation error
  const result = registerSchema.safeParse(data)
  if (!result.success) {
    return validationError(formatZodErrors(result.error))
  }

  // Check email exists
  const existing = await payload.find({
    collection: 'users',
    where: { email: { equals: data.email } }
  })

  if (existing.docs.length > 0) {
    return businessError('AUTH', 'AUTH_002')
  }

  // ... create user
}
```

### 2. Tao Don Hang

```typescript
// src/app/api/v1/orders/route.ts
import { businessError, httpError } from '@/lib/errors'

export async function POST(req: Request) {
  const user = await getCurrentUser(req)
  if (!user) {
    return httpError('UNAUTHORIZED')
  }

  const cart = await getCart(user.id)
  if (cart.items.length === 0) {
    return businessError('ORD', 'ORD_002')
  }

  // Check stock
  for (const item of cart.items) {
    const product = await getProduct(item.productId)
    if (product.stock < item.quantity) {
      return businessError('PRD', 'PRD_001', {
        details: `San pham: ${product.name}`
      })
    }
  }

  // ... create order
}
```

---

## Trigger Phrases

Skill nay duoc kich hoat khi:

### Tao Error Response

- "tao error response"
- "tra ve loi tu API"
- "error handling cho endpoint"

### Them Error Code

- "them error code"
- "tao error code moi"
- "error cho feature X"

### Debug Loi

- "error code X nghia la gi"
- "debug loi API"
- "hieu error response"

### Migration

- "migration error response"
- "chuyen doi sang format moi"
- "thong nhat error format"

---

## Luu Y Quan Trong

1. **LUON dung error code tu error-codes.json** - Khong hardcode message
2. **GIU nguyen code cu** - Format moi la bo sung, khong thay the
3. **Validate truoc khi commit** - Chay `scripts/validate-error-codes.py`
4. **Generate types sau khi them code** - Chay `scripts/generate-types.py`
5. **Message bang tieng Viet** - De user hieu
6. **Suggestion co ich** - Giup user biet cach khac phuc
