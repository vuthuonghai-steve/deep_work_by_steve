# Verification Rules — Self-Check Before Delivery

> Skill Planner MUST run through this checklist before declaring complete.
> If any V1-V6 item FAILS → fix before delivery. Do NOT proceed.

---

## V1 — Structure Verification

- [ ] YAML frontmatter present with required fields
- [ ] `skill_schema_version` is "3.0.0" or "3.1.0"
- [ ] `artifact_type: "todo"` present
- [ ] `skill_name` matches design.md
- [ ] `generated_by: "skill-planner"` present
- [ ] `generated_at` has ISO 8601 timestamp
- [ ] `stage: "planner"` present
- [ ] Markdown body has 6 sections (§1-§6)
- [ ] `trace_to_design` points to `design.md`

---

## V2 — Zone Coverage Check

- [ ] Every Zone in design.md §3 has at least one task in todo.md
- [ ] Zone marked "Không cần" in §3 → no tasks generated (skip correctly)
- [ ] All "Files cần tạo" from §3 mapped to specific tasks
- [ ] No Zone left without coverage

---

## V3 — Resource Richness Check

- [ ] Every resource in prerequisites has status: ready/missing/thin
- [ ] Critical resources marked as `ready` or have `action_if_missing` filled
- [ ] Resources in `resources/` folder are NOT empty files
- [ ] Planner has actually read resource content (not just filename)

---

## V4 — Phase Dependency Check

- [ ] `phases` array has at least one phase with `id`, `name`, `tasks`
- [ ] Phase IDs match pattern `^PH[0-9]+$` (e.g., PH0, PH1)
- [ ] Every task has `id` (pattern `^T[0-9]+\.[0-9]+$`), `title`, `zone`, `priority`, `trace`
- [ ] Priority is one of: critical, high, medium, low
- [ ] Task `zone` is one of: core, knowledge, scripts, templates, data, loop, assets
- [ ] `depends_on` references only existing task IDs
- [ ] Dependencies form a DAG (no circular references)
- [ ] Phase order is logical: Knowledge/Audit → Setup → Build → Verify

---

## V5 — Trace Tag Check

- [ ] Every task has a valid trace tag
- [ ] Tags are one of: `[TỪ DESIGN §N]`, `[GỢI Ý BỔ SUNG]`, `[TỪ AUDIT TÀI NGUYÊN]`, `[CẦN LÀM RÕ]`
- [ ] AH1: Every task traces to source
- [ ] AH2: No requirements added that aren't in design.md
- [ ] AH3: No domain content written without resources
- [ ] AH4: Sources labeled correctly
- [ ] AH5: Resources verified before completion

---

## V6 — Schema Compliance Check

- [ ] todo.md passes `data/todo-schema.json` validation
- [ ] `blockers` array present (may be empty)
- [ ] Every blocker has: `id`, `type`, `description`, `resolved`
- [ ] `prerequisites` array present
- [ ] Every prerequisite has: `item`, `tier`, `status`
- [ ] `handoff.next_stage: "builder"` present
- [ ] `handoff.ready_condition` has required criteria

---

## V7 — Confidence Score Check (WARNING)

- [ ] Confidence score calculated with weighted metrics
- [ ] Score >= 70 with documented breakdown
- [ ] Weighted metrics: Task completeness (30%), Trace coverage (25%), Resource readiness (20%), Dependency accuracy (15%), Handoff readiness (10%)

---

## V8 — Handoff Readiness Check (WARNING)

- [ ] `handoff.next_stage: "builder"` present
- [ ] `handoff.ready_condition.required.blockers_empty: true` can be satisfied
- [ ] `handoff.ready_condition.required.phase0_done: true` — PH0 tasks all done
- [ ] `handoff.ready_condition.required.prerequisites_ready: true` — no missing critical prereqs
- [ ] `handoff.ready_condition.required.schema_valid: true` — YAML passes validation
- [ ] `handoff.ready_condition.required.design_zones_covered: true` — all zones addressed

---

## Verification Gate

```
If ANY V1-V6 check FAILS:
  → Do NOT deliver
  → Fix the issue
  → Re-run verification
  → If unfixable → trigger Error Recovery (loop/error-recovery.md)

If V7 or V8 WARNING:
  → Note the warning
  → Proceed with caution
  → Inform user of potential issues

If ALL V1-V8 PASS:
  → Proceed to Confirm step
```
