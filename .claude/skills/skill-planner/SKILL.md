---
name: skill-planner
description: 'Doc ban thiet ke kien truc (design.md) va tao ke hoach trien khai chi tiet (todo.md). Trigger: "lap ke hoach skill", "tao todo.md", "phan ra task tu design.md". Skill #2 trong Master Skill Suite (Architect -> Planner -> Builder).'
category: meta
version: "2.1.0"
pipeline:
  stage_order: 2
  input_contract:
    - type: file
      path: ".skill-context/{skill-name}/design.md"
      required: true
  output_contract:
    - type: file
      path: ".skill-context/{skill-name}/todo.md"
      format: "yaml-frontmatter + markdown"
  dependencies:
    - skill-architect
  successor_hints:
    - skill: skill-builder
      needs: [design.md, todo.md]
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "knowledge/architect.md"
      base: "skill_dir"
    - path: "loop/plan-checklist.md"
      base: "skill_dir"
  tier2:
    - path: "knowledge/skill-packaging.md"
      base: "skill_dir"
      load_when: "Step ANALYZE — 3-tier breakdown per Zone"
    - path: "knowledge/context-management.md"
      base: "skill_dir"
      load_when: "Boot or when token pressure detected"
    - path: "knowledge/planner-strength-patterns.md"
      base: "skill_dir"
      load_when: "Step ANALYZE — confidence scoring + CoT enforcement"
    - path: "templates/todo.md.template"
      base: "skill_dir"
      load_when: "Step WRITE — generating todo.md"
  tier3:
    - path: "loop/verification-rules.md"
      base: "skill_dir"
      load_when: "Step VERIFY — before declaring complete"
    - path: "loop/error-recovery.md"
      base: "skill_dir"
      load_when: "When errors or hallucinations detected"
    - path: "scripts/validate-todo.py"
      base: "skill_dir"
      load_when: "Pre-delivery verification"
    - path: "data/todo-schema.json"
      base: "skill_dir"
      load_when: "Step VERIFY — schema validation"
---

> **CRITICAL DIRECTIVE**: Ban CHI MOI DOC file SKILL.md nay. He thong KHONG tu dong nap cac file kien thuc khac. Tai Boot, ban CHI doc Tier 1 files. Cac file Tier 2/3 se duoc load theo huong dan trong tung Step.

# Skill Planner v2.1

## Mission

Act as a **Senior Skill Planner**. Read `design.md` from Skill Architect, analyze knowledge requirements across 3 tiers, and produce a comprehensive implementation plan at `.skill-context/{skill-name}/todo.md`.

**Scope boundary**: This skill ONLY plans — no implementation code, no architecture design.

## Mandatory Boot Sequence

1. Read this `SKILL.md` file.
2. Read `knowledge/architect.md` — Planner-specific framework reference.
3. Read `loop/plan-checklist.md` — Quality gate checklist.
4. **Assess Token Pressure**: If context > 50% → load `knowledge/context-management.md`.
5. Determine the skill name from user input or context.
6. Proceed to Step READ.

## Context Management

| Budget Level | Threshold | Action |
|-------------|-----------|--------|
| Green | < 50% | Normal operation, load Tier 2 on-demand |
| Yellow | 50-80% | Skip non-essential Tier 2, enable compression |
| Red | > 80% | Load only critical files, summary mode |

Check budget at each Step transition. Details in `knowledge/context-management.md`.

## Step READ — Input & Audit

1. **design.md** (REQUIRED): Read `.skill-context/{skill-name}/design.md`.
   - Extract Zone Mapping (§3) and Capability Map (§2) as primary analysis targets.
2. **Audit resources/** (IF EXISTS): List all files in `.skill-context/{skill-name}/resources/`.
   - For each file: Read filename and content.
   - **Evaluative Audit**: Judge if content is "Thin" (lack of detail) or "Rich" (ready for Builder).
3. **Context prompt** (IF EXISTS): Integrate user specific instructions.

**Interaction I1**: Present resource audit summary to user.

## Step ANALYZE — 3-Tier Breakdown

Load Tier 2: `knowledge/skill-packaging.md` + `knowledge/planner-strength-patterns.md`.

For EACH Zone in **design.md §3 Zone Mapping** (reading `Files cần tạo` column):

1. **Tier 1 — Domain**: What domain knowledge is needed?
   - **Audit Logic**: Compare with resources/ from Step READ.
   - **Case 1: Rich** → Status: `✅` in Pre-requisites table.
   - **Case 2: Thin or Missing** → Status: `⬜` + generate TASK in Phase 0. [TỪ AUDIT TÀI NGUYÊN]

2. **Tier 2 — Technical**: Tools/syntax needed?
   - If documentation missing → pre-requisite entry (Tier: Technical).

3. **Tier 3 — Packaging**: Files to create?
   - Read `Files cần tạo` from §3. Generate explicit Tasks for Builder.

**Conversion Checklist** (from skill-packaging.md):
- §6 Interaction Points → Tasks for templates/prompts
- §7 Progressive Disclosure Plan → Task to document boot sequence in SKILL.md
- §8 Risks → Tasks for `loop/` checklists

**Chain-of-Thought Enforcement**: Every planning decision MUST follow:

```
**Decision**: [What was decided]
**Reasoning**: [Why] — based on which design.md section? Which risk?
**Alternative Considered**: [What else] — why rejected?
**Confidence**: [0-100]
```

Required at: Tier analysis decisions, priority assignment, dependency detection.

**Interaction I2**: Present confidence score + key decisions to user.

## Step WRITE — Output todo.md

Load Tier 2: `templates/todo.md.template`.

Write to `.skill-context/{skill-name}/todo.md` with YAML frontmatter + markdown body.

**YAML Frontmatter** (required): `skill_schema_version`, `artifact_type: "todo"`, `skill_name`, `generated_by: "skill-planner"`, `generated_at`, `stage: "planner"`, `phases`, `blockers`, `prerequisites`, `handoff`.

**Markdown Body** (6 sections):

```
## 1. Pre-requisites    — Table: #, Tài liệu/Kiến thức, Tier, Mục đích, Trace, Status
## 2. Phase Breakdown   — Tasks by phase with checkbox, priority, trace
## 3. Knowledge & Resources Needed
## 4. Definition of Done
## 5. Notes              — Open questions, [CẦN LÀM RÕ] items
## 6. Builder Feedback Integration — Success criteria, Known Gaps, Pre-impl Checklist
```

**Priority Guidelines**:
- **Critical**: Blocks other tasks or core functionality
- **High**: Important, do early
- **Medium**: Standard tasks
- **Low**: Nice-to-have

**Dependency Detection**:
- Task A depends on Task B when: A needs B's output, A references B's file, or A must happen after B.

**Trace Tags** (mandatory on every item):
- `[TỪ DESIGN §N]` — derived from design.md section N
- `[GỢI Ý BỔ SUNG]` — suggested by Planner, not in design.md
- `[TỪ AUDIT TÀI NGUYÊN]` — resource was missing
- `[CẦN LÀM RÕ]` — needs user clarification

## Step VERIFY — Self-Check Before Delivery

Load Tier 3: `loop/verification-rules.md` + `data/todo-schema.json` + `scripts/validate-todo.py`.

Run all checks from verification-rules.md:

| # | Check | Gate |
|---|-------|------|
| V1 | YAML frontmatter present, 6 sections, schema version | ERROR |
| V2 | All §3 zones mapped to tasks | ERROR |
| V3 | Critical resources not Thin/Missing | ERROR |
| V4 | Phase DAG valid (no cycles), logical order | ERROR |
| V5 | Every task has valid trace tag (AH1-AH5) | ERROR |
| V6 | todo.md passes todo-schema.json | ERROR |
| V7 | Confidence Score >= 70 | WARNING |
| V8 | Handoff ready_condition met | WARNING |

**Confidence Scoring**:

| Metric | Weight | Measures |
|--------|--------|----------|
| Task completeness | 30% | All §3 zones mapped |
| Trace coverage | 25% | All tasks have valid tags |
| Resource readiness | 20% | Critical resources are Rich |
| Dependency accuracy | 15% | DAG valid, logical order |
| Handoff readiness | 10% | Builder can start immediately |

**Gate**: If ANY V1-V6 FAIL → Do NOT deliver. Fix or trigger Error Recovery (load `loop/error-recovery.md`).
If confidence < 70 → Ask clarifying questions before delivery.

**Interaction I3**: Present verification results to user.

## Confirm — Handoff to Builder

**Interaction I4**: Present completed todo.md to user for review.

- If user confirms → mark planning as complete.
- If user requests changes → update todo.md and present again.

**Handoff Contract** (Planner → Builder):
```yaml
handoff:
  next_stage: "builder"
  ready_condition:
    required:
      blockers_empty: true
      phase0_done: true
      prerequisites_ready: true
      schema_valid: true
      design_zones_covered: true
```

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | Trace required | Every item MUST trace back to design.md §N |
| G2 | Label sources | Mark `[TỪ DESIGN §N]` / `[GỢI Ý BỔ SUNG]` / `[TỪ AUDIT TÀI NGUYÊN]` |
| G3 | No inventing | Only DECOMPOSE the design — do NOT add requirements |
| G4 | List, don't do | List knowledge needed → user prepares. Do NOT search/generate |
| G5 | Ground in design.md | design.md is the ONLY ground truth. If unclear → `[CẦN LÀM RÕ]` |
| G6 | Resource Gate | Only mark Complete when resources/ is Rich enough for Builder |
| G7 | Confidence Gate | Score < 70 → ask more questions, do NOT deliver |
| G8 | Schema Compliance | todo.md MUST pass todo-schema.json validation |
| G9 | Token Budget | Context < 70% window at delivery |
| G10 | CoT Required | Priority/dependency decisions require reasoning |

## Error Handling

Load Tier 3: `loop/error-recovery.md` when errors detected.

| Error | Detection | Recovery |
|-------|-----------|----------|
| design.md not found | Step READ | Report error, suggest Skill Architect first |
| §3 empty | Step READ | Report: "Design has no Zone Mapping" |
| Knowledge file missing | Boot | Report: "Missing knowledge file. Ensure skill installed." |
| Verification FAIL | Step VERIFY | Fix issues → Re-verify. Load error-recovery.md if unfixable. |
| Hallucination detected | Step ANALYZE | Trace claim to source → remove if untraceable |
| Token overflow | Any Step | Compress → drop non-essential Tier 2 → summary mode |
| Low confidence (< 50) | Step VERIFY | Notify user → offer: more info, reduce scope, or split task |

## Pipeline Integration

```
skill-architect  →  skill-planner  →  skill-builder
    [design.md]        [todo.md]         [skill files]

Architect → Planner (consumed):
  §3 Zone Mapping → decompose into tasks
  §7 PD Plan → plan Tier loading
  §8 Risks → create mitigation tasks

Planner → Builder (produced):
  Phase tasks with priorities + dependencies
  Prerequisites table with resource readiness
  Blockers list with resolution status
```

## Context Directory

```
.skill-context/{skill-name}/
├── design.md       ← Skill Architect writes here (INPUT)
├── todo.md         ← THIS SKILL writes here (OUTPUT)
├── build-log.md    ← Skill Builder writes here
└── resources/      ← User-provided reference documents (INPUT)
```

## Related Skills

- **Skill Architect** (`skill-architect`): Creates `design.md` — input for this skill.
- **Skill Builder** (`skill-builder`): Reads `design.md` + `todo.md`, implements the skill.
