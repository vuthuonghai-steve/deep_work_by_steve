# ARCHITECT FRAMEWORK — Architect's Knowledge Base

> **Usage**: Read at boot time
> **Shared Source**: `../../_shared/knowledge/framework.md`

---

## Quick Reference

For complete framework details (7 Zones, Pipeline Flow, Naming Conventions, Anti-hallucination), see:
```
../../_shared/knowledge/framework.md
```

---

## Architect-Specific Sections

### §1 Zone Mapping Contract (for design.md §3)

| Zone | Files cần tạo | Nội dung | Bắt buộc? |
|------|---------------|----------|-----------|
| Core | `SKILL.md` | Persona, phases, guardrails | ✅ |
| Knowledge | `knowledge/xxx.md` | Domain standards | ✅ / ❌ |
| Scripts | `scripts/xxx.py` | Automation tools | ✅ / ❌ |
| Templates | `templates/xxx.template` | Output formats | ✅ / ❌ |
| Data | `data/xxx.yaml` | Config, schema | ✅ / ❌ |
| Loop | `loop/xxx.md` | Checklists, verify rules | ✅ / ❌ |
| Assets | N/A | Not needed | ❌ |

---

### §2 Design Output Sections

| # | Section | Purpose | Write After Phase |
|---|---------|---------|------------------|
| §1 | Problem Statement | Pain point, users, rationale | Phase 1 |
| §2 | Capability Map | 3 Pillars analysis | Phase 2 |
| §3 | Zone Mapping | Contract Architect→Planner | Phase 2 |
| §4 | Folder Structure | Mindmap diagram | Phase 3 |
| §5 | Execution Flow | Sequence diagram | Phase 3 |
| §6 | Interaction Points | When to ask user | Phase 3 |
| §7 | Progressive Disclosure Plan | Tier 1/2 files | Phase 3 |
| §8 | Risks & Blind Spots | Risks + mitigation | Phase 2 |
| §9 | Open Questions | Unclear points | Phase 3 |
| §10 | Metadata | Name, date, status | Phase 1 + update |
| §10.1 | Version & Dependencies | Version mgmt | v2.0 |
| §11 | Naming Conventions | Skill naming rules | v2.0 |
| §12 | Rollback Procedures | Rollback for each phase | v2.0 |

---

## Workflow Phases

### Phase 1: Collect

1. Determine **skill-name** (kebab-case)
2. Collect from user:
   - **Pain Point**: What problem needs solving?
   - **User & Context**: Who will use? In what context?
   - **Expected Output**: What is final output? (Mermaid? Markdown? JSON?)
3. Confidence < 70% → Ask clarifying questions

**Gate 1**: Summarize → Wait for confirm → Write §1 + §10 to design.md

---

### Phase 2: Analyze

1. **3 Pillars Analysis**:
   - Pillar 1 – Knowledge: What domain knowledge is needed?
   - Pillar 2 – Process: What is workflow logic? Branching conditions?
   - Pillar 3 – Guardrails: Where does AI typically fail?

2. **7 Zones Mapping**: Fill Zone Mapping table

3. **Risks Identification**: List ≥3 specific risks

**Gate 2**: Present analysis → Wait for confirm → Write §2 + §3 + §8 to design.md

---

### Phase 3: Design & Output

1. Read `knowledge/visualization-guidelines.md` for diagram standards
2. Create ≥3 Mermaid diagrams:
   - D1 — Folder Structure (mindmap)
   - D2 — Execution Flow (sequenceDiagram)
   - D3 — Workflow Phases (flowchart LR)
3. Design §6 Interaction Points
4. Design §7 Progressive Disclosure Plan (Tier 1 vs Tier 2)
5. Fill §9 Open Questions

**Gate 3**: Present full design → Wait for confirm → Write §4 + §5 + §6 + §7 + §9 + §10 to design.md

---

## Pipeline Integration

```
skill-architect  ──→  skill-planner  ──→  skill-builder
    [design.md]            [todo.md]         [skill files]

Handoff A→P:
  § design.md §2 (Capability Map)  → Planner audit 3 Tiers
  § design.md §3 (Zone Mapping)    → Planner decompose to Tasks
  § design.md §7 (PD Plan)         → Planner + Builder know Tier 1/2
  § design.md §8 (Risks)           → Builder reference for Guardrails
```

**Architect must ensure before handoff**:
- [ ] §3 has specific filenames (not placeholders)
- [ ] §7 distinguishes Tier 1 and Tier 2
- [ ] §8 has ≥3 risks with mitigation
- [ ] §9 Open Questions resolved or flagged for Builder

---

## Guardrails

| ID | Rule |
|----|------|
| G1 | **Design Only** — No code writing |
| G2 | **Gate Enforcement** — Each Phase ends with user interaction |
| G3 | **Diagrams First** — Minimum 3 Mermaid diagrams |
| G4 | **Confidence Threshold** — <70% = ask more questions |
| G5 | **Zone Mapping Contract** — §3 must have specific filenames |
| G6 | **Single Context Rule** — One skill at a time |
| G7 | **Checklist Gate** — Review `loop/design-checklist.md` before deliver |

---

## Quality Gate

Run through `loop/design-checklist.md` before declaring completion.

---

> **Framework Source**: See `../../_shared/knowledge/framework.md` for complete reference
