# 📋 Phased Implementation Plan: production-code-reviewer

> **Stage**: 2 — Planner Roadmap Complete
> **Target Path**: `.skill-context/production-code-reviewer/todo.md`

---

## 1. Pre-requisites & Resource Audit

All necessary files, schemas, and validators from the upgraded suite (`ver-1`) are evaluated for readiness:

| Resource | Path | Type | Status | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Stage framework** | `ver-1/_shared/knowledge/framework.md` | Shared | ✅ Rich | Ready to import |
| **CASE Standard** | `ver-1/_shared/knowledge/case-system.md` | Shared | ✅ Rich | Ready to import |
| **Google Guidelines** | `.skill-context/production-code-reviewer/google-review-standards.md` | Doc | ✅ Rich | Ready to copy to skill package |
| **check_status** | `ver-1/_shared/validators/check_status.py` | Script | ✅ Rich | Ready to call at boot |
| **Handoff validator**| `ver-1/_shared/validators/handoff_validator.py`| Script | ✅ Rich | Ready to call at Quality Gate |

---

## 2. Phase Breakdown & Tasks

### Phase 1: Setup & Initialization (DoD: Context ready)
- [ ] **Task 1.1**: Initialize the final package folder structure under `skills/rebuild/production-code-reviewer/` `[TỪ DESIGN §3]`
- [ ] **Task 1.2**: Copy `google-review-standards.md` from `.skill-context/production-code-reviewer/` to the package directory as `knowledge/google-standards.md` `[TỪ DESIGN §3]`
- [ ] **Task 1.3**: Perform boot sequence verification using the unified status script `[TỪ DESIGN §10]`

### Phase 2: Domain Knowledge & Rules (DoD: YAML rules and loop checklist written)
- [ ] **Task 2.1**: Create `data/review-rules.yaml` defining Google Code Review rules, comment levels, and severity catalogs `[TỪ DESIGN §3, §7]`
- [ ] **Task 2.2**: Create `loop/gate-checklist.yaml` specifying report readiness metrics `[TỪ DESIGN §3, §7]`

### Phase 3: Linter & Auditor Scripts (DoD: code_auditor.py written and executable)
- [ ] **Task 3.1**: Write `scripts/code_auditor.py` to: `[TỪ DESIGN §3, §5]`
  - Parse Python code for syntax correctness.
  - Detect empty `except pass` blocks.
  - Detect raw file opens without `with` context manager.
  - Count public function lengths and flag violations (>50 lines).
  - Detect docstring presence on public classes and functions.
  - Count cyclomatic complexity heuristics (number of `if`, `for`, `while`, `and`, `or` statements).
- [ ] **Task 3.2**: Make `code_auditor.py` executable `[TỪ DESIGN §3]`

### Phase 4: Core Skill Definition & Templating (DoD: SKILL.md and report template complete)
- [ ] **Task 4.1**: Create `templates/review-report.md.template` for rendering the structured review feedback `[TỪ DESIGN §3, §7]`
- [ ] **Task 4.2**: Write `SKILL.md` specifying: `[TỪ DESIGN §3]`
  - Standard native frontmatter metadata.
  - A single, powerful `<instructions>` XML tag wrapping the YAML must/must_not constraints.
  - A single `<context>` tag wrapping the Boot Sequence (calling the unified `check_status.py` script) and the Progressive Disclosure triggers.
  - Clear phase-by-phase execution directions to guide the LLM when acting as the Google Code Reviewer.
  - An `<output_contract>` tag specifying the delivery formats.

### Phase 5: Verification & Quality Gate Validation (DoD: Passing all quality gates)
- [ ] **Task 5.1**: Run `handoff_validator.py` to ensure the completed package meets the standard 7-Zone structure `[TỪ DESIGN §10]`
- [ ] **Task 5.2**: Use the `production-quality-gatekeeper` skill package to run `loop_refiner.py` against the new skill's `SKILL.md` and scripts, ensuring that all code meets the absolute highest quality standards `[GỢI Ý BỔ SUNG]`
- [ ] **Task 5.3**: Test the new skill with a subagent on a real draft file to output a highly constructive review report, logging the evidence in `.skill-context/production-code-reviewer/test-evidence.md` `[GỢI Ý BỔ SUNG]`

---

## 3. Definition of Done (DoD)
* All files specified in the **Zone Mapping** (§3 of `design.md`) are created, formatted cleanly, and placed under the final package directory.
* The new skill package passes `handoff_validator.py --stage builder-complete` with zero failures.
* The skill is successfully validated using `production-quality-gatekeeper` and verified to run without errors.
