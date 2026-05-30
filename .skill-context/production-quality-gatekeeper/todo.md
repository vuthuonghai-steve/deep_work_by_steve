# 📋 Phased Implementation Plan: production-quality-gatekeeper

> **Stage**: 2 — Planner Roadmap Complete
> **Target Path**: `.skill-context/production-quality-gatekeeper/todo.md`

---

## 1. Pre-requisites & Resource Audit

All necessary files, schemas, and validators from the upgraded suite (`ver-1`) are evaluated for readiness:

| Resource | Path | Type | Status | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Stage framework** | `ver-1/_shared/knowledge/framework.md` | Shared | ✅ Rich | Ready to import |
| **CASE Standard** | `ver-1/_shared/knowledge/case-system.md` | Shared | ✅ Rich | Ready to import |
| **Check status** | `ver-1/_shared/validators/check_status.py` | Script | ✅ Rich | Ready to call at boot |
| **Handoff validator**| `ver-1/_shared/validators/handoff_validator.py`| Script | ✅ Rich | Ready to call at Quality Gate |
| **Rollback engine** | `ver-1/_shared/validators/rollback_engine.py` | Script | ✅ Rich | Ready to call on failure |

---

## 2. Phase Breakdown & Tasks

### Phase 1: Setup & Initialization (DoD: Context ready)
- [ ] **Task 1.1**: Initialize the final package folder structure under `skills/rebuild/production-quality-gatekeeper/` `[TỪ DESIGN §3]`
- [ ] **Task 1.2**: Copy and register schemas/rules in the package context `[TỪ DESIGN §3]`
- [ ] **Task 1.3**: Perform boot sequence verification using the unified status script `[TỪ DESIGN §10]`

### Phase 2: Domain Knowledge Construction (DoD: All knowledge markdown files written)
- [ ] **Task 2.1**: Implement `knowledge/creative-standards.md` detailing strict narrative structures, pacing, and cliché filters `[TỪ DESIGN §3, §7]`
- [ ] **Task 2.2**: Implement `knowledge/dev-standards.md` detailing SOLID rules, robust error boundary requirements, idempotency keys, and security benchmarks `[TỪ DESIGN §3, §7]`
- [ ] **Task 2.3**: Implement `knowledge/llm-evaluator.md` detailing XML boundaries, instruction weight, and prompt-injection mitigations `[TỪ DESIGN §3, §7]`

### Phase 3: Loop Engine & Scripts (DoD: loop_refiner.py written and unit tested)
- [ ] **Task 3.1**: Create `data/quality-matrix.yaml` defining the binary check scoring schema for each of the three fields `[TỪ DESIGN §3, §7]`
- [ ] **Task 3.2**: Create `loop/gate-checklist.yaml` to specify the automated criteria checks `[TỪ DESIGN §3, §7]`
- [ ] **Task 3.3**: Write the core loop script `scripts/loop_refiner.py` to: `[TỪ DESIGN §3, §5]`
  - Parse the `quality-matrix.yaml` and load the appropriate domain knowledge block.
  - Grade a draft output against the active criteria with binary (Pass/Fail) scores.
  - Compile structured feedback for failed criteria.
  - Feed the feedback into an LLM refinement prompt and loop iteratively for up to 10 turns.
  - Limit context bloat by discarding intermediate histories.
  - Trigger mitigation steps if max turns are reached.
- [ ] **Task 3.4**: Make `loop_refiner.py` executable `[TỪ DESIGN §3]`

### Phase 4: Core Skill Definition & Templating (DoD: SKILL.md and report template complete)
- [ ] **Task 4.1**: Create `templates/evaluation-report.md.template` for rendering the layered evaluation metrics `[TỪ DESIGN §3, §7]`
- [ ] **Task 4.2**: Write `SKILL.md` specifying: `[TỪ DESIGN §3]`
  - Standard native frontmatter metadata.
  - A single, powerful `<instructions>` XML tag wrapping the YAML must/must_not constraints.
  - A single `<context>` tag wrapping the Boot Sequence (calling the unified `check_status.py` script) and the Progressive Disclosure triggers.
  - Clear phase-by-phase execution directions to guide the LLM when acting as the quality critic.
  - An `<output_contract>` tag specifying the delivery formats.

### Phase 5: Verification & Testing (DoD: Successful subagent test execution)
- [ ] **Task 5.1**: Run `handoff_validator.py` to ensure the completed package meets the standard 7-Zone structure `[TỪ DESIGN §10]`
- [ ] **Task 5.2**: Test the skill with a specialized subagent against a complex coding or writing task to verify that the self-refining loop successfully executes multiple turns and polishes the draft to a high-quality standard `[GỢI Ý BỔ SUNG]`
- [ ] **Task 5.3**: Write the test results and logs to `.skill-context/production-quality-gatekeeper/test-evidence.md` `[GỢI Ý BỔ SUNG]`

---

## 3. Definition of Done (DoD)
* All files specified in the **Zone Mapping** (§3 of `design.md`) are created, formatted cleanly, and placed under the final package directory.
* The script `loop_refiner.py` runs without errors, correctly evaluates drafts, and successfully executes up to 10 refinement loop turns.
* The final package passes the `handoff_validator.py --stage builder-complete` programmatic gate check with zero failures.
