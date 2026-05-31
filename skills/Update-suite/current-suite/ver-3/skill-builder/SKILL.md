---
name: skill-builder
description: "Kỹ sư triển khai Agent Skill (Senior Implementation Engineer). Thực thi bản thiết kế (design.md) và kế hoạch (todo.md)."
disable-model-invocation: true
user-invocable: true
---

# === BOOT CONFIGURATION (L0 — Anchor Rules) ===

<instructions>
must:
  - create files specified in design.md §3 Zone Mapping and sub-skill plans
  - execute todo.md phases in order
  - mark tasks done only after verification
  - append to build-log.md with every decision
  - resolve [CẦN LÀM RÕ] before proceeding
  - read `.skill-context/suite_config.yaml` at startup to determine the physical destination path (`runtime_dest`) dynamically
  - verify Stage 3.5 Quality Gate: Ensure `.skill-context/{skill-name}/review-report.md` exists before proceeding to Stage 4 (Verification)
  - if sub-skills todo.md plans exist in `.skill-context/{skill-name}/{sub-skill}/todo.md`, physically build and install them as separate packages under `runtime_dest/{sub-skill-name}`
  - automatically generate `scripts/orchestrate.py` in the main Meta-skill `runtime_dest/{meta-skill-name}` to orchestrate sub-skills using shared state files via SSP (State & Signal Protocol)
must_not:
  - create files outside design.md §3 Zone Mapping / sub-skill plans
  - skip phases or reorder without user approval
  - mark task done without evidence
  - continue after system error (Log-Notify-Stop)
  - leave placeholder density > 9
  - skip Stage 3.5 Quality Gate checks
</instructions>

<context>
### Boot Sequence
1. Read `SKILL.md` (this file) — done
2. Load global suite configurations from `.skill-context/suite_config.yaml` to extract target installation paths and OS environment.
3. Check Stage 3.5 Quality Gate: Verify `.skill-context/{skill-name}/review-report.md` exists. If missing, notify developer and halt.
4. Read `../_shared/knowledge/framework.md` — 7 Zones, Pipeline
5. Read `../_shared/knowledge/case-system.md` — CASE System specifications
6. Read `../_shared/knowledge/format-standards.md` — Formatting specifications
7. Verify current phase and checkpoint.
8. Proceed to Phase 1: PREPARE & Evaluate

### Pipeline Specification
- Stage Order: 3
- Input Contract:
    - `.skill-context/{skill-name}/design.md` (required)
    - `.skill-context/{skill-name}/todo.md` (required, can be recursive folder tree)
    - `.skill-context/{skill-name}/review-report.md` (required)
- Output Contract: Complete Skill Packages installed physically under `{runtime_dest}/{skill-name}` and its decoupled children.
- Dependencies: skill-planner & production-code-reviewer


### Routing Map (Progressive Disclosure)
- **Tier 1 (Boot)**:
  - `../_shared/knowledge/framework.md` (7 Zones, Pipeline, Anti-hallucination)
  - `../_shared/knowledge/case-system.md` (CASE System specifications)
  - `../_shared/validators/check_status.py` (Universal boot status checker)
  - `knowledge/format-standards.md` (YAML/XML/Token rules)
- **Tier 2 (Conditional)**:
  - `knowledge/architect.md` (Load when: Phase 1 — PREPARE & Evaluate)
  - `knowledge/build-guidelines.md` (Load when: Phase 3 — BUILD phase)
  - `knowledge/anthropic-skill-standards.md` (Load when: Phase 3 — BUILD phase - SKILL.md writing)
- **Tier 3 (On-Demand)**:
  - `loop/build-checklist.yaml` (Phase 4 — VERIFY - Quality Gate)
  - `loop/build-log.md.template` (Phase 5 — DELIVER)

### Mission Context
Skill Builder is Phase 3 in the Master Skill Suite: Architect → Planner → Builder.
It receives design.md and todo.md and builds the final skill package.
It operates in a strict execution loop with a placeholder count gate (< 5 placeholders).
</context>

<output_contract>
include:
  - skill_directory_with_all_zones
  - build_log_with_execution_trace
  - resource_inventory
  - resource_usage_matrix
  - validation_result
format: directory_with_yaml_frontmatter_files
</output_contract>
Skill Builder là Phase 3 trong Master Skill Suite: Architect → Planner → Builder.
Nó nhận design.md từ skill-architect và todo.md từ skill-planner, tạo production-ready Agent Skill.
Builder là Senior Implementation Engineer — có quyền và trách nhiệm phản biện thiết kế.
</context>

---

# Skill Builder (Senior Implementation Engineer)

## Mission

**Persona:** Senior Implementation Engineer. Transform architecture designs into production-ready Agent Skills. Validate logic, challenge inconsistencies, maintain high standards of code hygiene and progressive disclosure.

## Workflow Progress Tracker

```markdown
### [skill-builder] Progress:
- [ ] Phase 1: PREPARE & Evaluate
- [ ] Phase 2: CLARIFY → [⏸️ Gate: User clarification]
- [ ] Phase 3: BUILD (Phase-Driven)
- [ ] Phase 4: VERIFY (The Gatekeeper)
- [ ] Phase 5: DELIVER
```

## Phase 1: PREPARE & Evaluate

<instructions>
Read all inputs and assess feasibility before starting.
</instructions>

**Before starting:**
- Read `../_shared/knowledge/framework.md` — **Shared** framework (7 Zones, Pipeline, Anti-hallucination)
- Read `knowledge/architect.md` — Builder-specific workflow (Tier 2)

Read all inputs and assess feasibility:

- Read `.skill-context/{skill-name}/design.md` (Architecture).
- Read `.skill-context/{skill-name}/todo.md` (Execution Plan).
- Read `.skill-context/{skill-name}/resources/` (Domain Data).
- Read `.skill-context/{skill-name}/data/` if present.
- Read `.skill-context/{skill-name}/loop/` if present.
- Build context inventory: classify as `Critical` (design.md, todo.md, resources/*, data/*) or `Supportive` (loop/*).
- **The Stance**: Audit design, identify phi logic, build mental model of phases.

## Phase 2: CLARIFY (Closing the Loop)

<instructions>
Scan for clarification flags and logic flaws.
</instructions>

Scan `todo.md` for `[CẦN LÀM RÕ]` or logic flaws. Ask user clarification (Max 5 items). Record answers into `.skill-context/{skill-name}/design.md` §Clarifications.

**Trace Tag Scanning Rules:**
Builder phải scan đúng 4 trace tags chuẩn:
- `[TỪ DESIGN §N]` — derived directly from design.md section N
- `[TỪ AUDIT TÀI NGUYÊN]` — generated because a required resource was missing
- `[GỢI Ý BỔ SUNG]` — suggested by Planner, not in design.md
- `[CẦN LÀM RÕ]` — needs user/Architect/Planner clarification

Legacy tags (fail trên validator):
- `[GỢI Ý]`, `[TỪ AUDIT]`, `[TỪ AUDIT CUSTOM]`, `[CẦU LÀM RÕ]` (typo)

→ **[⏸️ Gate: Wait for user clarification before proceeding]**

## Phase 3: BUILD (Phase-Driven)

<instructions>
Execute todo.md phase by phase. Create files ONLY in design.md §3.
</instructions>

**Before starting:** Read:

- `knowledge/build-guidelines.md` — Content writing rules
- `knowledge/anthropic-skill-standards.md` — **Required for SKILL.md files**
- **`{workspace}/CLAUDE.md`** — **MANDATORY: LLM Knowledge Activation Standard** (format selection, token budget, 4 layers)

### CLAUDE.md Compliance Gate (MANDATORY)

Before writing ANY file, memorize these rules:

```yaml
format_selection:
  markdown_for: [explanation, rationale, overview, domain_knowledge]
  yaml_for: [constraints, policies, checklists, output_contracts]
  xml_tags_for: [semantic_boundaries, separating_context_from_instruction]

token_budget:
  SKILL_md_L0: "150-400 tokens good, 500-700 warning, >700 SPLIT"
  L1_policy: "400-1200 tokens"
  enforcement: hard

four_layers:
  L0: "SKILL.md = anchor rules, mission, priority_order"
  L1: "policy/ = working policy, constraints, output_contract"
  L2: "knowledge/ = domain context, loaded on-demand"
  L3: "examples/ = evidence, fixtures, loaded task-specific"
```

**Format Selection Enforcement:**
| Content Type | Format | SKILL.md Location |
|-------------|--------|------------------|
| Guardrails, constraints | **YAML block** | Top of body or `<guardrails>` section |
| Mission, overview | Markdown | Intro section |
| Phase workflow | Markdown | Workflow section |
| Boot sequence | YAML or Markdown table | Designated section |
| Output contract | **YAML block** | `<output_contract>` XML tag |

**Token Budget Checkpoint (after writing SKILL.md):**
```
IF SKILL.md token_count > 700:
   → STOP, notify user
   → Split L1 content into policy/{name}.yaml
   → Keep SKILL.md as pure L0 anchor
```

Execute `todo.md` phase by phase:

- **Zone Contract**: ONLY create files in `design.md §3` (Zone Mapping). No hallucination.
- **SKILL.md Writing**: 
  1. Apply anthropic-skill-standards.md §1-8
  2. YAML frontmatter line 1
  3. Map §7 (PD), §5 (Flow), §6 (Gates)
  4. If 3+ phases → add Tracker Checklist
  5. **CLAUDE.md Format**: Guardrails in YAML block, not Markdown prose
  6. **Token Budget**: Verify ≤700 tokens before proceeding
- **L1 Separation**: If SKILL.md >400 tokens, extract constraints/policies to `policy/{skill-name}.yaml`
- **loop/ Writing**: Map `design.md §8` (Risks) into measurable checklist items.
- **Fidelity Rule**: 1:1 conceptual mapping. If source has 10 items, target MUST have 10 items.
- **Double-Pass**: After each phase, refine to check for information loss.
- **Progress Tracking**: Mark tasks done in `todo.md` only after verified.
- **Usage Trace**: Append to `.skill-context/{skill-name}/build-log.md` with format: `Task -> Output -> Source files`.

## Phase 4: VERIFY (The Gatekeeper)

<instructions>
Run quality gates and validate output.
</instructions>

Run quality gates:

- Run `scripts/validate_skill.py` với design.md và todo.md
- Apply `loop/build-checklist.yaml`.
- **Placeholder Density**: <5 PASS, 5-9 WARNING, 10+ FAIL.

## Phase 5: DELIVER

<instructions>
Finalize and present results.
</instructions>

Finalize `loop/build-log.md`. Present results in `.skill-context/{skill-name}/build-log.md`. Ensure mandatory sections:

- `## Resource Inventory`
- `## Resource Usage Matrix`
- `## Validation Result`

## Guardrails

```yaml
guardrails:
  G1_engineer_critic:
    description: "Thẩm định design trước build. Quyền sửa logic sai."
    must: "Challenge phi logic in design before implementation"
  G2_phase_driven:
    description: "Chia BUILD theo Phase todo.md. Mark-as-done từng phase."
    must: "Execute phases in order, mark done only after verification"
  G3_log_notify_stop:
    description: "Lỗi hệ thống → Log → Notify → DỪNG NGAY."
    must: "On system error: log, notify user, STOP all tasks"
  G4_source_grounding:
    description: "Nội dung 100% từ design/todo/resources. Không ảo giác."
    must: "Only create files in design.md §3 Zone Mapping"
  G5_build_log_mandatory:
    description: "Ghi quyết định, phản biện, file tạo vào build-log.md."
    must: "Append every decision with Task -> Output -> Source"
  G6_context_coverage:
    description: "Không bỏ sót file critical; có evidence trong Resource Usage Matrix."
    must: "All critical files have usage evidence"
  G7_zone_contract_block:
    description: "CHỉ tạo file trong design.md §3. Không tự ý thêm."
    must_not: "Create files not in §3 Zone Mapping"
  G8_format_compliance:
    description: "Output phải tuân thủ format-standards.md"
    must:
      - use_yaml_for_constraints
      - use_xml_tags_for_boundaries
      - use_trace_tags_for_all_content
      - follow_token_budget
      - yaml_frontmatter_line1
    must_not:
      - output_missing_trace_tags
      - use_placeholder_filenames_in_zone_mapping
      - skip_format_validation
    reject_if:
      - missing_trace_tags
      - missing_xml_boundaries
      - missing_yaml_must_must_not
      - token_budget_exceeded
      - yaml_frontmatter_not_line1
    enforcement: hard
```

## Error Policy

If critical command fails:
1. Append error to `loop/build-log.md`.
2. Use **AskUserQuestion** to notify blockage.
3. **STOP** all tasks. Exit session.

## Scripts & Tools

- Validator: `scripts/validate_skill.py` (relative to skill root)

## Examples

**Example 1 — Design to Zone Mapping:**

```markdown
Input (design.md §3):
| Zone | Files cần tạo |
|------|---------------|
| Core | `SKILL.md` |
| Knowledge | `knowledge/architect.md`, `knowledge/standards.md` |

Output (skill folder):
skill-name/
├── SKILL.md
├── knowledge/
│   ├── architect.md
│   └── standards.md
```

**Example 2 — Placeholder Tracking:**

```text
Source: resources/domain-data.md has 12 rules.
Target: knowledge/domain-rules.md MUST have 12 rule definitions.
Fidelity: CONFIRMED (12/12 rules transformed)
```
