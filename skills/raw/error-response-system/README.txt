# Error Response System - Skill Package

Version: 2.0.0
Date: 2026-02-06
Optimized for: AI Agents (Claude, GPT-4, etc.)

## 📦 Package Contents

error-response-system/
├── SKILL.md                          # Main skill documentation
├── assets/
│   └── error-codes-template.json    # Error codes template
├── scripts/
│   ├── validate-error-codes.py      # Validation script
│   └── generate-types.py            # Type generation script
└── references/
    ├── README.md                     # Overview & quick start
    ├── AI-AGENT-GUIDE.md            # AI agent instructions
    ├── implementation-guide.md       # Detailed implementation
    └── migration-guide.md            # Migration from v1.x

## 🚀 Quick Installation

### For Claude Projects

1. Copy this entire folder to your Claude skills directory:
   ```bash
   cp -r error-response-system ~/.claude/skills/
   ```

2. Claude will automatically detect and use this skill when working with API code.

### For Your Project

1. Install the implementation files:
   ```bash
   # Copy error codes
   mkdir -p src/lib/errors
   cp error-response-system/assets/error-codes-template.json \
      src/lib/errors/error-codes.json
   
   # Copy scripts
   mkdir -p scripts
   cp error-response-system/scripts/*.py scripts/
   
   # Generate types
   python scripts/generate-types.py
   ```

2. Create helper files (see implementation-guide.md)

3. Start using in your API routes!

## 📚 Documentation

Start here based on your role:

### For AI Agents (Claude, GPT-4, etc.)
1. **Read first**: `SKILL.md` - Auto-activation rules and quick patterns
2. **Deep dive**: `references/AI-AGENT-GUIDE.md` - Complete AI instructions

### For Developers
1. **Overview**: `references/README.md` - Quick start guide
2. **Setup**: `references/implementation-guide.md` - Detailed setup
3. **Migration**: `references/migration-guide.md` - Upgrade from v1.x

## 🎯 What This Skill Does

This skill provides a standardized error response system for APIs with:

✅ Type-safe error codes (TypeScript)
✅ Vietnamese user messages
✅ Automatic AI agent activation
✅ Validation & type generation scripts
✅ Frontend integration helpers
✅ 100% backward compatible

## 🤖 AI Auto-Activation

This skill automatically activates when:

**File paths contain:**
- `src/app/api/**`
- `src/services/**`
- `src/collections/**/hooks/**`

**User mentions:**
- "API", "endpoint", "error handling"
- "validation", "authentication"

**Code patterns:**
- `if (!user)` → Suggests `httpError('UNAUTHORIZED')`
- `if (existingEmail)` → Suggests `businessError('AUTH', 'AUTH_002')`
- `schema.safeParse()` → Suggests `validationError(...)`

## 📊 Error Categories

| Category | Prefix | Example |
|----------|--------|---------|
| Authentication | AUTH_ | AUTH_002 - Email exists |
| Orders | ORD_ | ORD_002 - Empty cart |
| Payment | PAY_ | PAY_001 - Insufficient balance |
| Points | PTS_ | PTS_001 - Insufficient points |
| Vouchers | VCH_ | VCH_001 - Expired voucher |
| Store | STR_ | STR_001 - Store inactive |
| Products | PRD_ | PRD_001 - Out of stock |
| System | SYS_ | SYS_001 - Service unavailable |

## 💡 Quick Example

```typescript
import { httpError, businessError, validationError } from '@/lib/errors'

export async function POST(req: Request) {
  // Auth check
  const user = await getCurrentUser(req)
  if (!user) {
    return httpError('UNAUTHORIZED')
  }

  // Validation
  const result = schema.safeParse(data)
  if (!result.success) {
    return validationError(formatZodErrors(result.error))
  }

  // Business logic
  const existing = await findUser({ email: data.email })
  if (existing) {
    return businessError('AUTH', 'AUTH_002')
  }

  return successResponse(user)
}
```

## 🔧 Key Scripts

### Validate Error Codes
```bash
python scripts/validate-error-codes.py
```

Checks:
- JSON syntax
- Required fields
- Error code format
- Vietnamese messages
- Duplicate codes

### Generate Types
```bash
python scripts/generate-types.py
```

Generates:
- TypeScript interfaces
- Union types
- Type guards
- Helper functions

## 🆕 What's New in v2.0

- ✅ AI-first design with auto-activation
- ✅ Enhanced error code metadata
- ✅ Better validation with severity levels
- ✅ Improved type generation with JSDoc
- ✅ Dedicated AI Agent Guide
- ✅ Pattern recognition matrix
- ✅ 100% backward compatible with v1.x

## 📞 Support

Need help?

1. Check the relevant documentation in `references/`
2. Run validation to catch errors
3. Review examples in implementation-guide.md

## 📄 License

MIT License - Free to use and modify

---

Made with ❤️ for AI-assisted development

For the latest version, visit: [Your Repository URL]
