# Skill Suite Upgrade Design

## §1 Problem Statement

**Pain Point**: Bộ 3 skill (skill-architect, skill-planner, skill-builder) trong `/skills/rebuild/` không tuân thủ format standards từ CLAUDE.md. Agent không biết phải tạo output format như thế nào khi build skill.

**User & Context**: Developer đang cải tiến skill suite cho Claude Code.

**Expected Output**: 3 skills tuân thủ YAML/XML format standards, có format validator, và reference examples đầy đủ.

---

## §2 Capability Map

### Pillar 1 - Knowledge
| Knowledge Area | Current State | Target State |
|---------------|---------------|--------------|
| Format Selection Rules | Isolated in CLAUDE.md | Embedded per skill |
| Token Budget Guidelines | Not referenced | Enforced per skill |
| YAML/XML Format Standards | Declared but not enforced | Active enforcement |

### Pillar 2 - Process
| Process | Current State | Target State |
|---------|---------------|--------------|
| Boot Sequence | Declarative only | Enforced by validator |
| Progressive Disclosure | Tier declaration | Tier validation |
| Format Output | Plain markdown | XML tags + YAML blocks |
| Validation | Structural only | + Format compliance |

### Pillar 3 - Guardrails
| Risk | Current State | Target State |
|------|---------------|--------------|
| Format knowledge isolation | R1: CLAUDE.md not referenced | R1: Embed in skill knowledge/ |
| No enforcement | R3: PD is declaration | R3: Validator enforces tiers |
| Missing examples | A2: No reference impl | A2: Add reference examples |

---

## §3 Zone Mapping

| Zone | Files cần tạo | Nội dung | Bắt buộc? |
|------|--------------|----------|-----------|
| Core | `format-standards.md` (shared ref) | YAML/XML/Token standards | ✅ |
| Knowledge | Per-skill: `knowledge/format-standards.md` | Embed CLAUDE.md format knowledge | ✅ |
| Scripts | `validate_format.py` | Format compliance validator | ✅ |
| Loop | `build-checklist.yaml` (update) | Add format checks | ✅ |
| References | `references/examples/*.md` | Reference implementations | ✅ |

**Files cần tạo cho từng skill:**

**skill-architect:**
- `skill-architect/knowledge/format-standards.md` (embed from CLAUDE.md)
- `skill-architect/references/examples/design-example.md` (full format reference)
- Update `skill-architect/loop/design-checklist.yaml` (add format checks)

**skill-planner:**
- `skill-planner/knowledge/format-standards.md` (embed from CLAUDE.md)
- `skill-planner/references/examples/todo-example.md` (full format reference)
- Update `skill-planner/loop/plan-checklist.yaml` (add trace tag validation)

**skill-builder:**
- `skill-builder/knowledge/format-standards.md` (embed from CLAUDE.md)
- `skill-builder/references/examples/skill-example.md` (full format reference)
- `skill-builder/scripts/validate_format.py` (NEW - format validator)
- Update `skill-builder/loop/build-checklist.yaml` (add format compliance)

**Shared:**
- `_shared/knowledge/format-standards.md` (single source of truth)

---

## §4 Folder Structure

```
skills/rebuild/
├── _shared/
│   └── knowledge/
│       └── format-standards.md          # [NEW] Single source of truth
├── skill-architect/
│   ├── knowledge/
│   │   └── format-standards.md          # [NEW] Embed from CLAUDE.md
│   ├── references/
│   │   └── examples/
│   │       └── design-example.md        # [NEW] Reference design.md
│   └── loop/
│       └── design-checklist.yaml       # [UPDATE] Add format checks
├── skill-planner/
│   ├── knowledge/
│   │   └── format-standards.md        # [NEW] Embed from CLAUDE.md
│   ├── references/
│   │   └── examples/
│   │       └── todo-example.md         # [NEW] Reference todo.md
│   └── loop/
│       └── plan-checklist.yaml         # [UPDATE] Add trace tag validation
├── skill-builder/
│   ├── knowledge/
│   │   └── format-standards.md         # [NEW] Embed from CLAUDE.md
│   ├── references/
│   │   └── examples/
│   │       └── skill-example.md        # [NEW] Reference SKILL.md
│   ├── scripts/
│   │   └── validate_format.py         # [NEW] Format validator
│   └── loop/
│       └── build-checklist.yaml        # [UPDATE] Add format compliance
```

---

## §5 Execution Flow

```
Phase 1: Embed Format Knowledge
  → Create _shared/knowledge/format-standards.md
  → Create per-skill knowledge/format-standards.md

Phase 2: Create Format Validator
  → Create validate_format.py in skill-builder/scripts/

Phase 3: Update Checklists
  → Update skill-architect/loop/design-checklist.yaml
  → Update skill-planner/loop/plan-checklist.yaml
  → Update skill-builder/loop/build-checklist.yaml

Phase 4: Add Reference Examples
  → Create references/examples/design-example.md (skill-architect)
  → Create references/examples/todo-example.md (skill-planner)
  → Create references/examples/skill-example.md (skill-builder)

Phase 5: Enforce Progressive Disclosure
  → Add tier validation to validate_format.py
```

---

## §6 Interaction Points

| Interaction | Trigger | Action |
|-------------|---------|--------|
| Format knowledge embed | Before starting fix | Reference CLAUDE.md sections 3,4,10,11,12 |
| Validator creation | After Phase 2 | Test with existing skill outputs |
| Checklist update | After Phase 3 | Verify format checks work |
| Reference examples | After Phase 4 | Validate examples match standards |

---

## §7 Progressive Disclosure

**Tier 1 (Mandatory):**
- `_shared/knowledge/format-standards.md` - single source of truth
- `validate_format.py` - validator script

**Tier 2 (Conditional):**
- Per-skill `knowledge/format-standards.md` - skill-specific reference
- Updated checklists - format enforcement

**Tier 3 (Optional):**
- Reference examples - only needed for future skill development

---

## §8 Risks & Blind Spots

| Risk | Mitigation |
|------|------------|
| Format knowledge bị duplicated | Use `_shared/` as single source, per-skill files reference it |
| Validator không cover hết cases | Start with essential checks (XML tags, YAML blocks, trace tags) |
| Reference examples không accurate | Match examples against actual CLAUDE.md standards |
| Agent vẫn ignore tier loading | Add validator check for tier compliance |

---

## §9 Open Questions

| Question | Status |
|----------|--------|
| Token budget per skill file? | Cần define: SKILL.md <500 lines, knowledge <200 lines |
| XML tags mandatory cho tất cả? | Chỉ required cho `<instructions>`, `<context>`, `<examples>` |
| Legacy trace tags support? | Continue support `[GỢI Ý]`, `[TỪ AUDIT]` với deprecation warning |

---

## §10 Metadata

- **skill-name**: skill-suite-upgrade
- **date**: 2026-05-18
- **author**: Claude Code
- **status**: IN PROGRESS
- **version**: 1.0.0
