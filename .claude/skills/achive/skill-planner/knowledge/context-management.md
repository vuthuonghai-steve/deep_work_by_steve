# Context Management — Token Optimization Strategy

> Usage: Load at boot when token pressure detected
> Purpose: Guide planner to manage context window efficiently

---

## Token Budget Framework

| Budget Level | Threshold | Action |
|-------------|-----------|--------|
| Green | < 50% | Normal operation, load Tier 2 on-demand |
| Yellow | 50-80% | Skip non-essential Tier 2, enable compression hints |
| Red | > 80% | Load only critical files, summary mode |
| Critical | > 95% | Emergency: summarize everything, drop all non-essential |

---

## Planner-Specific Token Estimates

| File | Est. Tokens | Priority |
|------|-------------|----------|
| SKILL.md | ~350 | Critical |
| architect.md | ~100 | Critical |
| plan-checklist.md | ~200 | Critical |
| skill-packaging.md | ~300 | High |
| context-management.md | ~250 | Medium |
| planner-strength-patterns.md | ~300 | Medium |
| todo.md.template | ~400 | High (when writing) |
| validate-todo.py | ~350 | Medium |
| verification-rules.md | ~200 | Medium |
| error-recovery.md | ~200 | Low |

---

## Compression Techniques

### 1. Lazy Loading
- Tier 2 files only load when Step requires them
- Tier 3 files only load during verification or recovery
- Never preload all knowledge files

### 2. Reference, Don't Duplicate
- architect.md references framework.md, not copies content
- Cross-reference between knowledge files where possible

### 3. Summary Mode (Red Budget)
- Load "executive summary" (first 20% of file)
- Skip examples and detailed explanations
- Use abbreviations where context allows

### 4. Drop Gracefully
- Non-essential Tier 2 dropped before critical files
- If design.md is very large, focus on §3 (Zone Mapping) first

---

## File Selection by Complexity

| Skill Complexity | Required Files | Optional Files |
|-----------------|---------------|----------------|
| Simple (< 5 zones) | Tier 1 only | None |
| Medium (5-7 zones) | Tier 1 + relevant Tier 2 | Other Tier 2 |
| Complex (> 7 zones) | Tier 1 + all Tier 2 | Tier 3 when needed |

---

## Monitoring

Check token pressure at each Step transition:
- **After Step READ**: Estimate size of design.md + resources
- **After Step ANALYZE**: Track accumulated context from zone analysis
- **Before Step WRITE**: Ensure room for todo.md generation

---

## Best Practices

1. **Always monitor**: Track token usage after each file load
2. **Compress proactively**: Don't wait for Red budget
3. **Keep Tier 1 small**: Tier 1 must be < 800 tokens total
4. **Reference, don't duplicate**: Use cross-references
5. **Drop gracefully**: Drop optional files before critical files
