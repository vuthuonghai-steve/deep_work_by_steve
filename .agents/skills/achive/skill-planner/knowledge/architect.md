# Planner Framework Reference

> **Usage**: Load at boot (Tier 1)
> **Source**: Adapted from `../../_shared/knowledge/framework.md` — planner-specific extracts only

---

## Pipeline Flow

```
skill-architect  →  skill-planner  →  skill-builder
    [design.md]        [todo.md]         [skill files]
```

**Planner consumes**:
- §3 Zone Mapping → decompose into tasks
- §7 Progressive Disclosure → plan Tier loading
- §8 Risks → create mitigation tasks
- §6 Interaction Points → tasks for templates/prompts

---

## Zone Mapping Contract

When reading `design.md §3`, follow this format:

| Zone | Purpose | Files Column |
|------|---------|-------------|
| Core | SKILL.md — persona, workflow, guardrails | Required |
| Knowledge | Domain references, standards | Usually required |
| Scripts | Automation tools | As needed |
| Templates | Output format templates | As needed |
| Data | Config, schemas | As needed |
| Loop | Checklists, verify rules | Usually required |
| Assets | Images, icons | Rarely |

**Rules**:
- "Files cần tạo" column → direct input for task creation
- "Không cần" → skip that zone entirely
- Builder MUST NOT add files not in §3 (without documented rationale)

---

## Anti-Hallucination Rules

| Rule | Description | Violation |
|------|-------------|-----------|
| AH1 | Every task MUST trace to source | Task without [TỪ DESIGN §N] |
| AH2 | Only decompose, don't add requirements | New requirement not in design.md |
| AH3 | Don't guess domain knowledge | Writing domain content without resources |
| AH4 | Always label sources | No [TỪ DESIGN] / [GỢI Ý] distinction |
| AH5 | Verify resources before completion | Planning complete with missing critical resources |

### Trace Tags

```
[TỪ DESIGN §N]      — From design.md section N
[GỢI Ý BỔ SUNG]     — Planner suggestion, not in design.md
[TỪ AUDIT TÀI NGUYÊN] — Resource was missing
[CẦN LÀM RÕ]        — Needs user clarification
```

---

## 3-Tier Knowledge Model

| Tier | Name | Question | Audit |
|------|------|----------|-------|
| 1 | Domain | What domain knowledge needed? | Audit resources/. Missing → TASK |
| 2 | Technical | What tools/syntax needed? | Missing docs → pre-req |
| 3 | Packaging | How to map to agent zone? | Generate Tasks from §3 |

---

## Naming Conventions

| Zone | Pattern | Example |
|------|---------|---------|
| knowledge/ | `domain-topic.md` | `uml-rules.md` |
| scripts/ | `action-target.py` | `validate-todo.py` |
| templates/ | `output-format.template` | `todo.md.template` |
| loop/ | `purpose-checklist.md` | `plan-checklist.md` |
| data/ | `config-name.yaml` | `todo-schema.json` |

---

## Quality Gates

### Planner → Builder Gate
- All §3 files mapped to specific tasks
- Pre-requisites table complete
- Resource audit shows "Rich" status for critical items
- Phase breakdown has priorities and dependencies
- Confidence score >= 70

> **Full framework**: See `../../_shared/knowledge/framework.md`
