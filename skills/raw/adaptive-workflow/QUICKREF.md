# Adaptive Workflow Quick Reference

## Quick Commands

| Command | Usage | Example |
|---------|-------|---------|
| `/btw` | Quick question, non-blocking | `/btw password policy là gì?` |
| `/continue` | Continue với assumption | `/continue using default timeout` |
| `/parallel` | Run tasks in parallel | `/parallel analyze code | research` |
| `/checkpoint` | Save state before risk | `/checkpoint before big refactor` |
| `/adapt` | Update with new info | `/adapt now requires 2FA` |

## Decision Tree

```
Cần hỏi user?
    │
    ├── Câu hỏi ngắn (< 10 words)
    │       └── → /btw [question]
    │
    ├── Câu hỏi phức tạp
    │       ├── → Spawn background agent
    │       └── → Tiếp tục workflow chính
    │
    └── Không cần hỏi
            └── → Tiếp tục với assumption + log

Có new information?
    │
    ├── Contradicts current approach?
    │       ├── Yes → Adapt, re-evaluate
    │       └── No → Continue
    │
    └── No new info → Continue
```

## Log Format

```
## Working Assumptions
- [ ] Assumption: Mô tả assumption
- [ ] Assumption: Mô tả assumption

## Pending Questions
- Q1: Câu hỏi chờ trả lời

## Checkpoint
- Saved at: [timestamp]
- Reason: [tại sao cần checkpoint]
```

## Example Flow

```
User: "Refactor auth module"

Claude (thinking):
- Cần clarify: password policy, token expiry, 2FA?
- But KHÔNG dừng lại

→ /btw Password policy requirements?

→ Continue với assumption:
## Working Assumptions
- [ ] Password: 8+ chars (default)
- [ ] Token expiry: 24h (common)
- [ ] 2FA: optional

→ Tiếp tục analyze code...

→ Khi user respond:
/adapt Password must be 12+ chars with special chars

→ Re-evaluate approach, adjust nếu cần
```

---

*Quick Reference v1.0*
