# Skill Suite v3.0 Upgrade — Project Documentation

**Extracted from:** skill-suite-upgrade-session
**Date:** 2026-05-09
**Category:** projects

---

## Overview

Nâng cấp bộ skill (skill-architect, skill-planner, skill-builder) từ v2.x lên v3.0. Mục tiêu: Hermes-native, multi-operation types support, YAML-first contracts.

---

## Architecture Decision Records

### ADR-001: Hermes-Native as Default Platform

**Decision:** Hermes là default platform target, Claude là secondary
**Rationale:** Project dùng Hermes làm primary framework
**Consequences:**
- Default install path: `~/.hermes/skills/`
- Platform detection: HERMES_SKILL_PATH env var check first

### ADR-002: YAML Frontmatter as Canonical Contract

**Decision:** Thay thế Markdown table contracts bằng YAML frontmatter
**Rationale:** Machine-readable, validated, consistent format
**Consequences:**
- design.md và todo.md phải có YAML frontmatter
- Validator check frontmatter schema trước content

### ADR-003: 6 Operation Types

**Decision:** Mở rộng từ chỉ `create_new` thành 6 operation types
**Rationale:** Skill lifecycle đa dạng — patch, refactor, migrate, consolidate, deprecate
**Consequences:**
- Builder adapt workflow theo operation_type
- Gates và outputs thay đổi theo type

### ADR-004: 3 Execution Modes

**Decision:** `lightweight`, `standard`, `strict` modes
**Rationale:** Không overhead cho task nhỏ, nhưng đủ validation cho critical tasks
**Consequences:**
- User chọn mode phù hợp với task scope
- Strict mode cho production skills

---

## Deliverables

### Research Documents (3 files)
- `docs/raw/research/2026-05-09-research-skill-validation-patterns.vi.md`
- `docs/raw/research/2026-05-09-research-yaml-frontmatter-conventions.vi.md`
- `docs/raw/research/2026-05-09-research-refinement-loop-patterns.vi.md`

### Design Documents (3 files)
- `docs/raw/designs/2026-05-09-design-hermes-skill-v3-architecture.vi.md`
- `docs/raw/designs/2026-05-09-design-install-target-resolution.vi.md`
- `docs/raw/designs/2026-05-09-design-operation-state-machine.vi.md`

### Brainstorm Documents (3 files)
- `docs/raw/brainstorm/2026-05-09-brainstorm-migration-strategy.vi.md`
- `docs/raw/brainstorm/2026-05-09-brainstorm-testing-strategy.vi.md`
- `docs/raw/brainstorm/2026-05-09-brainstorm-future-extensions.vi.md`

### Proposal Documents (6 files)
- `docs/raw/ideas/2026-05-09-proposal-operation-types-execution-modes-refinement-loop.vi.md`
- `docs/raw/ideas/2026-05-09-claude-code-upgrade-architect.vi.md`
- `docs/raw/ideas/2026-05-09-codex-upgrade-builder.vi.md`
- `docs/raw/ideas/2026-05-09-master-skill-suite-v3-upgrade-spec.vi.md`
- `docs/raw/ideas/2026-05-09-research-master-skill-suite-evaluation.vi.md`
- `docs/raw/ideas/2026-05-09-research-master-skill-suite-evaluation.md`

---

## Key Concepts

### 3-Phase Pipeline

```
User Request → skill-architect → design.md
                              ↓
              skill-planner → todo.md
                              ↓
              skill-builder → skill-package
```

### Hermes Skill Package Structure

```
{skill-name}/
├── SKILL.md           # Zone: core (mandatory, tier 1)
├── knowledge/         # Zone: knowledge (tier 2)
├── scripts/           # Zone: scripts
├── templates/         # Zone: templates
├── data/              # Zone: data
└── loop/              # Zone: loop
```

### Operation Type Workflows

| Operation Type | Pipeline | Gates |
|----------------|----------|-------|
| create_new | Full 3-stage | Design, Plan, Build, Verify |
| patch_existing | Minimal delta | Verify only |
| refactor_existing | Full + audit | Design, Build, Verify |
| migrate_platform | Full + analysis | Verify |
| consolidate_skills | Full + inventory | Design, Build, Verify |
| deprecate_skill | Minimal | None |

---

## Status

**Phase:** Research & Design Complete
**Next:** Implementation planning
**Blockers:** None identified

---

## Source

Session: skill-suite-upgrade-session
Created: 2026-05-09
Documentation: 11 raw files + 2 knowledge entries