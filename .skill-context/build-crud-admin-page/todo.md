---
name: build-crud-admin-page-todo
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "build-crud-admin-page"
generated_by: "skill-planner"
generated_at: "2026-05-16T22:35:00+07:00"
stage: "planner"
status: "in_progress"
trace_to_design: "design.md"
---

# §1 Pre-requisites

## Pre-requisites Table

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | Original skill zip content | Domain | Source content to rebuild | [TỪ DESIGN §1] | ✅ Rich |
| 2 | knowledge/README.md | Domain | Overview & references index | [TỪ DESIGN §3] | ⬜ Pending |
| 3 | knowledge/architecture.md | Domain | Folder structure, data flow | [TỪ DESIGN §3] | ⬜ Pending |
| 4 | knowledge/template-guide.md | Domain | Step-by-step guide | [TỪ DESIGN §3] | ⬜ Pending |
| 5 | knowledge/implementation-logic.md | Domain | Form mode, metadata | [TỪ DESIGN §3] | ⬜ Pending |
| 6 | knowledge/errors.md | Domain | Error handling | [TỪ DESIGN §3] | ⬜ Pending |
| 7 | knowledge/ui-skills-summary.md | Domain | UI/UX skills reference | [TỪ DESIGN §3] | ⬜ Pending |
| 8 | loop/checklist.md | Technical | Implementation checklist | [TỪ DESIGN §3] | ⬜ Pending |
| 9 | loop/checklist.yaml | Technical | Machine-readable validation | [TỪ DESIGN §3] | ⬜ Pending |

---

# §2 Phase Breakdown

## PH0: Resource Preparation

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| T0.1 | Create knowledge/ directory | Low | 0.1 | - | [TỪ DESIGN §3] |
| T0.2 | Create loop/ directory | Low | 0.1 | - | [TỪ DESIGN §3] |

## PH1: Core Skill File (SKILL.md)

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| T1.1 | Create SKILL.md with YAML frontmatter | High | 0.5 | - | [TỪ DESIGN §3:Core] |
| T1.2 | Add triggers, workflow phases | High | 0.3 | T1.1 | [TỪ DESIGN §6] |
| T1.3 | Add guardrails | High | 0.2 | T1.1 | [TỪ DESIGN §8] |
| T1.4 | Add boot sequence | Medium | 0.2 | T1.1 | [TỪ DESIGN §7] |
| T1.5 | Verify SKILL.md < 150 lines | High | 0.1 | T1.4 | [TỪ DESIGN §7] |

## PH2: Knowledge Files

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| T2.1 | Create knowledge/README.md | Medium | 0.3 | - | [TỪ DESIGN §3:Knowledge] |
| T2.2 | Create knowledge/architecture.md | High | 1.0 | - | [TỪ DESIGN §3:Knowledge] |
| T2.3 | Create knowledge/template-guide.md | High | 1.0 | T2.2 | [TỪ DESIGN §3:Knowledge] |
| T2.4 | Create knowledge/implementation-logic.md | High | 1.0 | T2.2 | [TỪ DESIGN §3:Knowledge] |
| T2.5 | Create knowledge/errors.md | Medium | 0.5 | - | [TỪ DESIGN §3:Knowledge] |
| T2.6 | Create knowledge/ui-skills-summary.md | Medium | 0.5 | - | [TỪ DESIGN §3:Knowledge] |

## PH3: Loop Files (Quality Gates)

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| T3.1 | Create loop/checklist.md | High | 0.5 | T2.2, T2.3 | [TỪ DESIGN §3:Loop] |
| T3.2 | Create loop/checklist.yaml | High | 0.5 | T3.1 | [TỪ DESIGN §3:Loop] |
| T3.3 | Add quality gates to checklist.yaml | High | 0.3 | T3.2 | [GỢI Ý BỔ SUNG] |

## PH4: Validation & Documentation

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| T4.1 | Validate zone mapping matches design §3 | High | 0.2 | PH1, PH2, PH3 | [TỪ DESIGN §3] |
| T4.2 | Run trace tag validation | Medium | 0.2 | T4.1 | [TỪ DESIGN §8] |
| T4.3 | Update design.md status to ready_for_builder | Low | 0.1 | T4.2 | [TỪ DESIGN §10] |

---

# §3 Knowledge & Resources Needed

## Input Resources

| Resource | Source | Purpose |
|----------|--------|---------|
| Original references/architecture.md | build-crud-admin-page.zip | Content for knowledge/architecture.md |
| Original references/template-guide.md | build-crud-admin-page.zip | Content for knowledge/template-guide.md |
| Original references/implementation-logic.md | build-crud-admin-page.zip | Content for knowledge/implementation-logic.md |
| Original references/errors.md | build-crud-admin-page.zip | Content for knowledge/errors.md |
| Original references/ui-skills-summary.md | build-crud-admin-page.zip | Content for knowledge/ui-skills-summary.md |
| Original references/checklist.md | build-crud-admin-page.zip | Content for loop/checklist.md |
| Original references/README.md | build-crud-admin-page.zip | Content for knowledge/README.md |

## Output Artifacts

| Artifact | Location |
|----------|----------|
| SKILL.md | {skill-root}/SKILL.md |
| knowledge/README.md | {skill-root}/knowledge/README.md |
| knowledge/architecture.md | {skill-root}/knowledge/architecture.md |
| knowledge/template-guide.md | {skill-root}/knowledge/template-guide.md |
| knowledge/implementation-logic.md | {skill-root}/knowledge/implementation-logic.md |
| knowledge/errors.md | {skill-root}/knowledge/errors.md |
| knowledge/ui-skills-summary.md | {skill-root}/knowledge/ui-skills-summary.md |
| loop/checklist.md | {skill-root}/loop/checklist.md |
| loop/checklist.yaml | {skill-root}/loop/checklist.yaml |

---

# §4 Definition of Done

## Checklist

- [ ] SKILL.md < 150 lines
- [ ] SKILL.md has valid YAML frontmatter (name, description, category)
- [ ] SKILL.md has triggers listed
- [ ] SKILL.md has 2 workflow phases documented
- [ ] SKILL.md has guardrails defined
- [ ] SKILL.md has boot sequence documented
- [ ] knowledge/README.md created with references index
- [ ] knowledge/architecture.md has folder structure + data flow
- [ ] knowledge/template-guide.md has 8 steps for new collection
- [ ] knowledge/implementation-logic.md has form mode pattern
- [ ] knowledge/errors.md has common errors + solutions
- [ ] knowledge/ui-skills-summary.md has 4 UI/UX skills
- [ ] loop/checklist.md has all checklist items
- [ ] loop/checklist.yaml is machine-readable YAML
- [ ] All trace tags present
- [ ] All zone_mapping files created as per design §3

---

# §5 Notes

## Observations

| # | Note | Flag |
|---|------|------|
| 1 | Original skill has 6 reference files that map to 7 Zone structure | [TỪ AUDIT TÀI NGUYÊN] |
| 2 | Original checklist.md is Bouquet-specific — needs generalization for any collection | [GỢI Ý BỔ SUNG] |
| 3 | Original errors.md has TypeScript-specific errors — valuable content | [TỪ AUDIT TÀI NGUYÊN] |
| 4 | UI skills summary references 4 external skills — needs to be in knowledge/ | [GỢI Ý BỔ SUNG] |

## Trace Tag Format

```
[TỪ DESIGN §N]      — From design.md section N
[GỢI Ý BỔ SUNG]     — Planner suggestion, not in design
[TỪ AUDIT TÀI NGUYÊN] — Generated from resource audit
[CẦN LÀM RÕ]       — Needs clarification
```

---

# §6 Builder Feedback Integration

## Handoff to Builder

**Input for Builder:**
- design.md (this file's parent)
- todo.md (this file)
- Original skill content at /tmp/skill-to-rebuild/build-crud-admin-page/

**Skills root location:**
```
{workspace}/skills/build-crud-admin-page/
```

**Successor:**
skill-builder (for actual implementation if needed)
