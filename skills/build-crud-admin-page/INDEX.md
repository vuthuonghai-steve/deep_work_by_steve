# SKILL Index: build-crud-admin-page

## File Map

| File | Zone | Tier | Purpose |
|------|------|------|---------|
| `SKILL.md` | Core | 1 | Core orchestration |
| `knowledge/README.md` | Knowledge | 1 | References index |
| `knowledge/architecture.md` | Knowledge | 2 | Folder structure, data flow |
| `knowledge/template-guide.md` | Knowledge | 2 | Step-by-step guide |
| `knowledge/implementation-logic.md` | Knowledge | 2 | Form mode, metadata |
| `knowledge/errors.md` | Knowledge | 2 | Error solutions |
| `knowledge/ui-skills-summary.md` | Knowledge | 2 | UI/UX skills |
| `patterns/form-mode-pattern.md` | Patterns | 2 | Core patterns |
| `rules/anti-patterns.md` | Rules | 2 | Anti-patterns |
| `templates/output-templates.md` | Templates | 2 | Output templates |
| `examples/good/form-mode-pattern.md` | Examples | 3 | Good examples |
| `examples/bad/form-mode-pattern.md` | Examples | 3 | Bad examples |
| `schemas/skill-schema.yaml` | Schemas | 2 | SKILL.md schema |
| `loop/checklist.md` | Loop | 1 | Checklist |
| `loop/checklist.yaml` | Loop | 2 | Machine-readable |

## Zone Structure

```
build-crud-admin-page/
├── SKILL.md                    # Core (Tier 1)
├── knowledge/                  # Knowledge (Tier 1-2)
│   ├── README.md              # Index (Tier 1)
│   ├── architecture.md        # Structure (Tier 2)
│   ├── template-guide.md      # Guide (Tier 2)
│   ├── implementation-logic.md # Logic (Tier 2)
│   ├── errors.md              # Errors (Tier 2)
│   └── ui-skills-summary.md   # UI skills (Tier 2)
├── patterns/                   # Patterns (Tier 2)
│   └── form-mode-pattern.md
├── rules/                      # Rules (Tier 2)
│   └── anti-patterns.md
├── templates/                  # Templates (Tier 2)
│   └── output-templates.md
├── examples/                   # Examples (Tier 3)
│   ├── good/
│   │   └── form-mode-pattern.md
│   └── bad/
│       └── form-mode-pattern.md
├── schemas/                    # Schemas (Tier 2)
│   └── skill-schema.yaml
└── loop/                      # Quality gates (Tier 1)
    ├── checklist.md
    └── checklist.yaml
```

## Progressive Disclosure

### Tier 1 (Boot — always load)
- SKILL.md
- knowledge/README.md
- loop/checklist.md

### Tier 2 (Load when needed)
- knowledge/architecture.md (understanding structure)
- knowledge/implementation-logic.md (form mode)
- knowledge/template-guide.md (creating new collection)
- patterns/form-mode-pattern.md (implementing patterns)
- rules/anti-patterns.md (avoiding mistakes)
- templates/output-templates.md (writing code)
- schemas/skill-schema.yaml (validating SKILL.md)

### Tier 3 (On-demand)
- examples/good/ (reference)
- examples/bad/ (reference)

## Dependencies

```
SKILL.md
    ↓ reads
knowledge/README.md
    ↓ links to
knowledge/architecture.md
knowledge/template-guide.md
    ↓ used by
patterns/form-mode-pattern.md
templates/output-templates.md
    ↓ guided by
rules/anti-patterns.md

loop/checklist.md
    ↓ validates against
All zones
```
