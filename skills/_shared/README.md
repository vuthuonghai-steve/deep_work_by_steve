# _shared — Shared Knowledge Base for Meta-Skills

> Centralized knowledge repository used by skill-architect, skill-planner, and skill-builder

## Purpose

This directory contains the single source of truth for framework knowledge that all three meta-skills share. Eliminating duplication ensures consistency and easier maintenance.

## Contents

| File | Purpose |
|------|---------|
| `knowledge/framework.md` | Core framework (7 Zones, Pipeline, Naming, Anti-hallucination) |

## Usage

Each skill should reference `../../_shared/knowledge/framework.md` as the primary source for:
- Zone definitions
- Pipeline flow
- Naming conventions
- Anti-hallucination rules

## When to Update

Update this shared knowledge when:
1. Zone structure changes
2. Pipeline flow changes
3. New anti-hallucination rules are added
4. Naming conventions change

Do NOT update for skill-specific knowledge (keep in individual skill's knowledge/).

## Architecture

```
.claude/skills/
├── _shared/                    ← SHARED (single source)
│   └── knowledge/
│       └── framework.md
├── skill-architect/            ← References _shared
│   └── knowledge/
├── skill-planner/              ← References _shared
│   └── knowledge/
└── skill-builder/              ← References _shared
    └── knowledge/
```

---

**Rationale**: DRY (Don't Repeat Yourself) principle applied to skill development.
