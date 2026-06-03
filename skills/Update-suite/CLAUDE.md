# Update-suite — Skill Suite Upgrade Workspace

> **Purpose**: Nâng cấp bộ skill suite từ ver-3 lên hybrid architecture
> **Target**: current-suite/ver-3/

---

## Mục tiêu

1. **skill-security-reviewer** — OWASP-based security review skill (NEW)
2. **Gate X** — Mandatory Human Confirmation trước Builder stage
3. **Rule Hierarchy** — `.mdc > SKILL.md > knowledge/*.md`
4. **20-point Quality Gates** — Thay thế 50-point gates
5. **Ambiguity BLOCKED Gate** — Pipeline dừng nếu có OPEN ambiguity

---

## Cấu trúc

```
Update-suite/
├── current-suite/ver-3/           # Baseline (ver-3)
│   ├── _shared/
│   │   ├── rules/                  # NEW: Rule hierarchy
│   │   │   ├── suite-rules.mdc
│   │   │   └── quality-gates.mdc
│   │   ├── knowledge/              # framework.md (updated)
│   │   └── validators/
│   ├── skill-security-reviewer/    # NEW
│   └── [existing skills]
├── updated-suite/                  # Output sau upgrade
└── lifecycle-docs/                 # Documentation
```

---

## Deliverables Status

| # | Deliverable | Status | Location |
|---|-------------|--------|----------|
| 1 | skill-security-reviewer (OWASP) | ✅ DONE | `current-suite/ver-3/skill-security-reviewer/` |
| 2 | Gate X (Human Confirm) | ✅ DONE | framework.md §5 |
| 3 | Rule Hierarchy | ✅ DONE | `_shared/rules/suite-rules.mdc` |
| 4 | 20-point Quality Gates | ✅ DONE | `_shared/rules/quality-gates.mdc` |
| 5 | Updated Documentation | ✅ DONE | framework.md (Section 5 & 10 updated) |

---

## Validation

```bash
# Validate all SKILL.md files
python _shared/validators/schema_validator.py --schema _shared/schemas/exploration.schema.yaml skill-security-reviewer/SKILL.md

# Validate security reviewer structure
ls -la skill-security-reviewer/
```

---

## Architecture Reference

Hybrid architecture details: `knowledge/experience/skill-suite-comparison/experience-report-ver-1.md`
