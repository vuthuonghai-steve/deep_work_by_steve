# Error Response System - Refactored for AI Agents

> **Version 2.0** - Optimized for AI-assisted development

## 🎯 What Changed in v2.0

### Key Improvements

1. **AI-First Design**: Auto-activation rules and clear triggers for AI agents
2. **Better Documentation**: AI Agent Guide with decision trees and patterns
3. **Enhanced Validation**: More detailed error messages with actionable suggestions
4. **Type Generation**: Improved TypeScript types with JSDoc and helper functions
5. **Error Code Metadata**: Added `useCases`, `relatedCodes`, and `_aiGuidance` fields

### Migration from v1.x

All v1.x features are preserved. The refactor is **100% backward compatible**.

## 📁 File Structure

```
error-response-system/
├── SKILL.md                    # Main skill documentation (AI-optimized)
├── AI-AGENT-GUIDE.md          # Dedicated guide for AI agents
├── error-codes.json           # Error codes database (enhanced metadata)
├── validate-error-codes.py    # Validator (better error reporting)
├── generate-types.py          # Type generator (improved output)
└── README.md                  # This file
```

## 🤖 For AI Agents

### Auto-Activation

This skill should automatically activate when:

**File paths contain:**
- `src/app/api/**`
- `src/services/**`
- `src/collections/**/hooks/**`

**User mentions:**
- "API", "endpoint", "route", "error handling"
- "validation", "authentication", "authorization"

**Code contains:**
- `errorResponse()`, `throw error`, `return error`
- Authentication checks, validation logic

### Quick Decision Tree

```
Error Detected
    ├─ HTTP Protocol? → httpError('UNAUTHORIZED')
    ├─ Form Validation? → validationError(errors)
    └─ Business Logic? → LOOKUP error-codes.json
                         ├─ Found? → businessError('CAT', 'CODE')
                         └─ Not Found? → Propose new code
```

### Pattern Recognition

| When you see... | Use this... |
|-----------------|-------------|
| `if (!user)` | `httpError('UNAUTHORIZED')` |
| `if (existingEmail)` | `businessError('AUTH', 'AUTH_002')` |
| `if (cart.items.length === 0)` | `businessError('ORD', 'ORD_002')` |
| `if (balance < amount)` | `businessError('PAY', 'PAY_001')` |
| `schema.safeParse()` | `validationError(...)` |

**See [AI-AGENT-GUIDE.md](./AI-AGENT-GUIDE.md) for complete patterns.**

## 👨‍💻 For Developers

### Installation

1. Copy files to your project:
   ```bash
   # Skill files (for Claude Projects)
   .claude/skills/error-response-system/
   
   # Implementation files
   src/lib/errors/
   ├── error-codes.json
   ├── types.ts (generated)
   ├── helpers.ts
   └── index.ts
   ```

2. Install scripts:
   ```bash
   scripts/
   ├── validate-error-codes.py
   └── generate-types.py
   ```

### Usage

#### Basic HTTP Error

```typescript
import { httpError } from '@/lib/errors'

export async function GET(req: Request) {
  const user = await getCurrentUser(req)
  if (!user) {
    return httpError('UNAUTHORIZED')
  }
  // ...
}
```

#### Business Error

```typescript
import { businessError } from '@/lib/errors'

export async function POST(req: Request) {
  const existing = await findUser({ email: data.email })
  if (existing) {
    return businessError('AUTH', 'AUTH_002')
  }
  // ...
}
```

#### Validation Error

```typescript
import { validationError, formatZodErrors } from '@/lib/errors'

const result = schema.safeParse(data)
if (!result.success) {
  return validationError(formatZodErrors(result.error))
}
```

### Adding New Error Codes

1. **Edit error-codes.json:**
   ```json
   {
     "BUSINESS_ERRORS": {
       "ORD": {
         "ORD_008": {
           "code": "ORD_008",
           "status": 400,
           "message": "Thiếu email người nhận",
           "details": "Email người nhận là bắt buộc",
           "suggestion": "Vui lòng cung cấp email người nhận"
         }
       }
     }
   }
   ```

2. **Validate:**
   ```bash
   python scripts/validate-error-codes.py
   ```

3. **Generate types:**
   ```bash
   python scripts/generate-types.py
   ```

4. **Use in code:**
   ```typescript
   return businessError('ORD', 'ORD_008')
   ```

## 📊 Error Code Categories

| Category | Prefix | Domain | Example |
|----------|--------|--------|---------|
| Authentication | `AUTH_` | Login, registration, accounts | `AUTH_002` - Email exists |
| Orders | `ORD_` | Shopping cart, checkout | `ORD_002` - Empty cart |
| Payment | `PAY_` | Transactions, balance | `PAY_001` - Insufficient balance |
| Points | `PTS_` | Loyalty rewards | `PTS_001` - Insufficient points |
| Vouchers | `VCH_` | Discounts, promos | `VCH_001` - Expired voucher |
| Store | `STR_` | Branches, locations | `STR_001` - Store inactive |
| Products | `PRD_` | Inventory, stock | `PRD_001` - Out of stock |
| System | `SYS_` | Infrastructure | `SYS_001` - Service unavailable |

## 🔧 Scripts Reference

### validate-error-codes.py

Validates error codes JSON structure and conventions.

```bash
# Default location
python validate-error-codes.py

# Custom location
python validate-error-codes.py path/to/error-codes.json
```

**Features:**
- ✅ JSON syntax validation
- ✅ Required fields check
- ✅ Error code format validation
- ✅ HTTP status code validation
- ✅ Vietnamese message detection
- ✅ Duplicate code detection
- ✅ Category prefix validation
- ✅ Severity levels (CRITICAL, ERROR, WARNING, INFO)

### generate-types.py

Generates TypeScript types from error codes JSON.

```bash
# Default
python generate-types.py

# Custom
python generate-types.py input.json output/dir/
```

**Generates:**
- `ErrorDetail` interface
- `ErrorResponse` interface
- `ErrorConfig` interface
- `HttpErrorType` union type
- `BusinessErrorCategory` union type
- Category-specific error code types (e.g., `AUTHErrorCode`)
- `BusinessErrorCode` union type
- Type guards (`isHttpError`, `isBusinessError`)
- Helper functions (`getErrorConfig`, `searchErrorCodes`)

## 📖 Documentation

| File | Purpose | Audience |
|------|---------|----------|
| [SKILL.md](./SKILL.md) | Main skill documentation | AI Agents & Developers |
| [AI-AGENT-GUIDE.md](./AI-AGENT-GUIDE.md) | Detailed AI instructions | AI Agents |
| [README.md](./README.md) | Overview & quick start | Everyone |

## 🎓 Examples

### Complete API Endpoint

```typescript
import {
  httpError,
  businessError,
  validationError,
  formatZodErrors
} from '@/lib/errors'

export async function POST(req: Request) {
  // Parse request
  const data = await req.json()
  
  // Validate
  const result = registerSchema.safeParse(data)
  if (!result.success) {
    return validationError(formatZodErrors(result.error))
  }
  
  // Auth check
  const user = await getCurrentUser(req)
  if (!user) {
    return httpError('UNAUTHORIZED')
  }
  
  // Business logic
  const existing = await findUser({ email: data.email })
  if (existing) {
    return businessError('AUTH', 'AUTH_002')
  }
  
  // Success
  const newUser = await createUser(result.data)
  return successResponse(newUser)
}
```

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "AUTH_002",
    "message": "Email đã được sử dụng",
    "details": "Email: user@example.com đã tồn tại trong hệ thống",
    "suggestion": "Sử dụng email khác hoặc đăng nhập nếu đã có tài khoản",
    "timestamp": "2026-02-06T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

## 🚀 Best Practices

### Do ✅

- Use specific error codes from JSON
- Write messages in Vietnamese
- Provide actionable suggestions
- Validate JSON after changes
- Generate types after adding codes
- Use type-safe helpers

### Don't ❌

- Hardcode error messages
- Use generic HTTP errors for business logic
- Skip validation/generation steps
- Delete old code before migration complete
- Use English messages
- Invent error codes not in JSON

## 🔄 Workflow

### For AI Agents

```
1. Detect error scenario
2. Classify error type (HTTP/Validation/Business)
3. Lookup error-codes.json
4. Use appropriate helper function
5. Generate type-safe code
```

### For Developers

```
1. Write API logic
2. Identify error cases
3. Find/create error codes
4. Validate & generate types
5. Use in code
6. Test error responses
```

## 🤝 Contributing

When adding new error codes:

1. Follow naming convention: `CATEGORY_NNN`
2. Write Vietnamese messages
3. Add helpful suggestions
4. Include use cases in `_aiGuidance`
5. Run validation
6. Generate types
7. Test in code

## 📝 Version History

### v2.0.0 (2026-02-06)

**Major refactor for AI agents:**
- AI-first documentation structure
- Enhanced error code metadata
- Improved validation with severity levels
- Better type generation with JSDoc
- Dedicated AI Agent Guide
- Pattern recognition matrix
- Auto-activation rules

### v1.0.0 (2026-01-16)

- Initial release
- Basic error code system
- JSON-based configuration
- Type generation
- Validation script

## 📞 Support

For issues or questions:

1. Check [AI-AGENT-GUIDE.md](./AI-AGENT-GUIDE.md) for common patterns
2. Run validation to find errors
3. Review examples in documentation
4. Consult error codes JSON for available codes

## 📄 License

MIT License - Feel free to use and modify for your projects.

---

**Made with ❤️ for AI-assisted development**
