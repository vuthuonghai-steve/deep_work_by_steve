# Context Management — Token Optimization Strategy

> Usage: Load at boot or when token pressure detected
> Purpose: Guide AI to manage context window efficiently

---

## Token Budget Framework

```markdown
| Budget Level | Threshold | Action |
|-------------|-----------|--------|
| Green | < 50% | Normal operation, load Tier 2 on-demand |
| Yellow | 50-80% | Skip non-essential Tier 2, enable compression hints |
| Red | > 80% | Run compress_context.py, load only critical files |
| Critical | > 95% | Emergency: summarize everything, drop all non-essential |
```

---

## Compression Techniques

### 1. Remove Redundancy

- **HTML Comments in Templates**: Remove `<!-- -->` after rendering
- **Duplicate Explanations**: architect.md và SKILL.md có overlap → reference thay vì duplicate
- **Verbose Descriptions**: Replace với bullet points hoặc tables

### 2. Lazy Loading

- Tier 2 files chỉ load khi thực sự cần
- Tier 3 files chỉ load khi verify/recover
- Không preload tất cả knowledge files

### 3. Summary Mode

Khi Red budget:
- Load "executive summary" (first 20% của file)
- Skip examples và detailed explanations
- Use abbreviations where context allows

### 4. File Selection Heuristics

| Task Type | Required Files | Optional Files |
|-----------|---------------|----------------|
| Simple skill (< 5 zones) | Tier 1 only | None |
| Medium skill (5-7 zones) | Tier 1 + relevant Tier 2 | Other Tier 2 |
| Complex skill (> 7 zones) | Tier 1 + all Tier 2 | Tier 3 when needed |

---

## Token Estimation

| File | Est. Tokens | Priority |
|------|-------------|----------|
| SKILL.md | ~300 | Critical |
| architect.md | ~150 | Critical |
| design-checklist.md | ~150 | Critical |
| visualization-guidelines.md | ~400 | High |
| context-management.md | ~300 | Medium |
| agent-strength-patterns.md | ~350 | Medium |
| design.md.template | ~500 | High (when writing) |
| validate_design.py | ~300 | Medium |
| verification-rules.md | ~250 | Medium |
| error-recovery.md | ~200 | Low |

---

## Monitoring Commands

```python
# Pseudo-code for context monitoring
def check_token_pressure(loaded_files):
    total_tokens = sum(f.estimated_tokens for f in loaded_files)
    window_size = get_context_window_size()  # e.g., 200000 for Claude
    usage_pct = (total_tokens / window_size) * 100
    
    if usage_pct < 50:
        return BudgetLevel.GREEN
    elif usage_pct < 80:
        return BudgetLevel.YELLOW
    else:
        return BudgetLevel.RED
```

---

## Best Practices

1. **Always monitor**: Theo dõi token usage sau mỗi file load
2. **Compress proactively**: Đừng đợi đến Red budget
3. **Keep Tier 1 small**: Tier 1 phải < 1000 tokens
4. **Reference, don't duplicate**: Dùng cross-reference thay vì copy content
5. **Drop gracefully**: Khi cần, drop optional files trước critical files
