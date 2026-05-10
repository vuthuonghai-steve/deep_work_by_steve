# Hermes Skill Development Patterns

**Extracted from:** skill-suite-upgrade-session
**Date:** 2026-05-09
**Category:** programming

---

## Overview

Technical patterns cho việc phát triển Hermes-native skills với v3.0 upgrade.

---

## Patterns

### Pattern 1: 3-Tier Progressive Disclosure Loading

**Problem:** Skills quá lớn để load full content luôn luôn
**Solution:** Token-efficient multi-level loading

```
Level 0: skills_list() → [{name, description, category}, ...]
Level 1: skill_view(name) → Full content + metadata
Level 2: skill_view(name, path) → Specific reference file
```

**Usage:** Hermes skill framework tự động manage loading tiers

---

### Pattern 2: YAML Frontmatter Contract

**Problem:** Markdown tables không machine-readable
**Solution:** YAML frontmatter là canonical contract giữa các stage

```yaml
---
name: skill-name
version: "1.0.0"
platform_target: hermes | claude | both
operation_type: create_new | patch_existing | ...
execution_mode: lightweight | standard | strict
install_target:
  platform: hermes
  scope: user-local | repo | project-local
---
```

---

### Pattern 3: Platform Detection Algorithm

**Problem:** Cần xác định target platform một cách tự động
**Solution:** Environment variable → path check → default

```
1. HERMES_SKILL_PATH env var → hermes
2. CLAUDE_SKILL_PATH env var → claude
3. ~/.hermes/skills/ exists → hermes
4. ~/.claude/skills/ exists → claude
5. Default: hermes
```

---

### Pattern 4: Install Target Resolution (4 Priority Levels)

**Problem:** User có thể muốn override platform detection
**Solution:** Explicit override wins over auto-detection

```
Priority 1: Explicit CLI flag (--install-target)
Priority 2: Frontmatter design.install_target
Priority 3: Platform detection
Priority 4: Default fallback (hermes)
```

---

### Pattern 5: Operation Type Detection

**Problem:** Builder cần adapt workflow dựa trên operation type
**Solution:** Detect từ context và apply appropriate workflow

```python
def detect_operation_type(context):
    if not context.get('existing_skill_path'):
        return 'create_new'
    # ... detection logic per type
```

| Operation | Workflow Adaptation |
|-----------|-------------------|
| create_new | Full 3-stage pipeline |
| patch_existing | Minimal delta, skip design phase |
| refactor_existing | Full + behavior preservation check |
| migrate_platform | Platform path mapping |
| consolidate_skills | Overlap analysis + merge |
| deprecate_skill | Deprecation notice only |

---

### Pattern 6: Refinement Loop (6-Step)

**Problem:** Skills cần cải thiện liên tục sau deployment
**Solution:** Formalized feedback loop

```
[1. OBSERVE] → [2. IDENTIFY] → [3. DECIDE] → [ACTION]
      ↑                                    ↓
[6. VERIFY] ← [5. DOCUMENT] ← [4. APPLY] ←
```

**Actions:** memory_update, patch_existing, create_new, refactor_existing, deprecate_skill

---

### Pattern 7: Execution Mode Gates

**Problem:** Không phải task nào cũng cần full validation
**Solution:** Adaptive gates theo execution mode

| Mode | Gates | Timeout | Output |
|------|-------|---------|--------|
| lightweight | None | 5 min | Patch delta |
| standard | Phase confirmations | 30 min | Full package |
| strict | Full review + signoff | 60 min | Package + audit |

---

## Related

- [[skill-suite-v3-upgrade-learnings]] — Key insights từ upgrade session
- [[skill-suite-v3-upgrade]] — Project documentation

---

## Source

Session: skill-suite-upgrade-session
Patterns extracted from: research/design/brainstorm raw documents