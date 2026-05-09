# Research Report: Master Skill Suite Understanding and Improvement Notes

> Date: 2026-05-09
> Author: Hermes Agent, written from the assistant's operational perspective
> Status: Raw improvement report
> Source directory: `docs/raw/ideas/skill-suite-improvement-raw-notes/`
> Purpose: Record what the assistant understood and received from the `skill-architect`, `skill-planner`, and `skill-builder` suite, plus improvement directions for the next iteration.

---

## 1. Context

This report records my understanding after reviewing and evaluating the 3-skill development suite requested by Steve:

1. `skill-architect`
2. `skill-planner`
3. `skill-builder`

The evaluation also used the raw architecture document:

- `/home/steve/Work-space/deep_work_by_steve/docs/raw/AGENTS.md`

And the main skill files reviewed earlier:

- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-architect/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-planner/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/_shared/knowledge/framework.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-planner/knowledge/skill-packaging.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/knowledge/build-guidelines.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/knowledge/anthropic-skill-standards.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/scripts/validate_skill.py`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/loop/build-checklist.md`

This is a raw report, not yet a finalized implementation spec. It should be treated as source material for improving the skill suite.

---

## 2. What I understood from `AGENTS.md`

`AGENTS.md` describes a broader agent architecture and places the skill suite inside a larger agent system.

### 2.1 Multi-layer orchestrator system

The project contains a `pipeline-steve` orchestrator pattern. It coordinates a 4-layer execution pipeline:

1. Explore
2. Implement
3. Verify Rule
4. Simplify

A critical platform constraint is explicitly documented:

> Subagents cannot spawn other subagents.

Therefore, the top-level orchestrator must spawn all worker subagents directly. This affects how any future skill-building automation should be designed. If the skill suite later uses subagents, it should not assume nested delegation unless the runtime explicitly supports it.

### 2.2 Skill development pipeline

`AGENTS.md` defines the Master Skill Suite as a 3-stage pipeline:

```text
User requirement
  -> skill-architect -> design.md
  -> skill-planner   -> todo.md
  -> skill-builder   -> completed skill package
```

Each stage has a distinct responsibility:

| Stage | Skill | Main role | Output |
|---|---|---|---|
| 1 | `skill-architect` | Analyze requirements and design skill architecture | `design.md` |
| 2 | `skill-planner` | Convert design into implementation tasks | `todo.md` |
| 3 | `skill-builder` | Build and validate the actual skill package | skill files + build log |

The suite is not only a writing assistant. It is intended to become a reusable meta-system for turning human-agent collaboration patterns into durable skills.

### 2.3 Seven-zone skill package structure

The expected skill package follows a 7-zone structure:

```text
{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
├── loop/
└── assets/   # sometimes omitted in examples, but part of the 7-zone model
```

The zones represent different kinds of reusable capability:

- `SKILL.md`: orchestration, persona, workflow, guardrails
- `knowledge/`: domain knowledge, standards, references
- `scripts/`: automation tools and validators
- `templates/`: output formats
- `data/`: config, schemas, static data
- `loop/`: checklists, logs, verification rules
- `assets/`: images or other static supporting files

### 2.4 Raw idea workflow

`AGENTS.md` also states that raw ideas should be written in `docs/raw/ideas/`, using names like:

- `YYYY-MM-DD-idea-name.md`
- `YYYY-MM-DD-research-name.md`
- `YYYY-MM-DD-design-name.md`
- `YYYY-MM-DD-brainstorm-name.md`

This report follows that convention by being stored under an English-named idea directory and using the `research-` prefix.

---

## 3. What I received from the 3-skill suite

From my operational perspective, the 3-skill suite gives me a structured way to turn repeated collaboration into reusable agent skills.

The most important thing I received is not just instructions for writing a skill. I received a full lifecycle:

1. Understand the pain point.
2. Design the skill architecture.
3. Convert architecture into implementation tasks.
4. Build the files.
5. Validate the output.
6. Record evidence and lessons.

This is valuable because it prevents skill creation from being a one-shot prompt-writing activity. It turns skill creation into an engineering process.

---

## 4. Understanding of `skill-architect`

### 4.1 Role

`skill-architect` acts as a Senior Skill Architect. Its job is design only.

It should not implement files directly and should not create the task list. Its output is `design.md`.

### 4.2 Workflow

The architect has 3 main phases:

1. Collect
   - Determine skill name.
   - Understand the pain point.
   - Identify the user and context.
   - Clarify the expected output.

2. Analyze
   - Map the requirement into 3 Pillars:
     - Knowledge
     - Process
     - Guardrails
   - Map the skill into the 7 Zones.
   - Identify risks and blind spots.

3. Design and output
   - Create Mermaid diagrams.
   - Define folder structure.
   - Define execution flow.
   - Define interaction points.
   - Define progressive disclosure tiers.
   - Write `design.md`.

### 4.3 Value received

The architect helps me avoid building a skill too early. It forces the system to ask:

- What is the actual problem?
- What knowledge must be explicit?
- What process should be encoded?
- Where will the model likely fail?
- Which files are actually needed?

This is useful because many weak skills fail not from poor wording, but from unclear architecture.

---

## 5. Understanding of `skill-planner`

### 5.1 Role

`skill-planner` reads `design.md` and produces `todo.md`.

Its purpose is decomposition, not implementation.

### 5.2 Workflow

The planner performs:

1. Read input and audit resources.
2. Analyze required knowledge using the 3-tier model:
   - Domain
   - Technical
   - Packaging
3. Generate tasks with trace tags.
4. Verify that tasks cover the design.
5. Prepare handoff for builder.

### 5.3 Value received

The planner is important because it creates a bridge between architecture and implementation.

The strongest idea in the planner is traceability. Every task should connect back to a source:

- `[TỪ DESIGN §N]`
- `[GỢI Ý BỔ SUNG]`
- `[TỪ AUDIT TÀI NGUYÊN]`
- `[CẦN LÀM RÕ]`

This helps reduce hallucination because the builder should not create files or requirements without a traceable reason.

---

## 6. Understanding of `skill-builder`

### 6.1 Role

`skill-builder` is the implementation engineer.

It reads:

- `design.md`
- `todo.md`
- `resources/`
- optional `data/`
- optional prior loop/proof files

Then it builds the skill package.

### 6.2 Workflow

The builder has 5 phases:

1. PREPARE and evaluate
2. CLARIFY unresolved issues
3. BUILD phase-by-phase
4. VERIFY using quality gates
5. DELIVER with build log

### 6.3 Value received

The builder contributes several strong engineering practices:

- It should challenge inconsistent design.
- It should not silently continue on critical errors.
- It should use build logs as evidence.
- It should check placeholder density.
- It should preserve fidelity from critical source resources.
- It should avoid inventing files outside the zone contract.

This gives the final stage a quality-control mindset instead of simply generating files.

---

## 7. Overall quality assessment

My overall assessment is:

```text
Architecture idea:          strong
Pipeline separation:        strong
Anti-hallucination intent:  strong
Runtime consistency:        medium
Hermes compatibility:       medium-low
Validator robustness:       medium-low
Feedback learning loop:     incomplete
```

The suite is conceptually strong. It already has the right direction: design first, plan second, build last.

However, it is not yet fully stable as a production-grade Hermes skill-building workflow. Several contracts are still ambiguous, markdown-heavy, or inherited from Claude-oriented assumptions.

---

## 8. Main strengths

### 8.1 Clear separation of responsibilities

The 3-stage separation is the strongest part:

- Architect designs.
- Planner decomposes.
- Builder implements.

This prevents one skill from trying to do everything at once.

### 8.2 Good anti-hallucination stance

The suite repeatedly emphasizes:

- Do not invent domain knowledge.
- Trace tasks to source sections.
- Audit resources before declaring readiness.
- Use checklists and validators.
- Stop when blocked.

This is exactly the right mindset for building reliable skills.

### 8.3 Good skill package model

The 7-zone model is useful because it separates instruction, knowledge, automation, templates, static data, feedback loops, and assets.

This makes skills easier to maintain and extend.

### 8.4 Progressive disclosure awareness

The suite understands that skills should not load everything at boot. It tries to define Tier 1, Tier 2, and Tier 3 loading.

This is good for token efficiency and reduces cognitive overload for the model.

### 8.5 Build evidence and validation

The builder's requirement for build logs, resource usage matrix, placeholder checks, and validation scripts is valuable.

It encourages the builder to prove what was done rather than just claim completion.

---

## 9. Main issues and gaps

### 9.1 Claude-oriented paths instead of Hermes-native paths

The builder currently uses `.claude/skills/{skill-name}` as an output contract in some places.

For Hermes, this is not ideal. Hermes skills usually live in:

```text
~/.hermes/skills/{category}/{skill-name}/
```

or inside a repository:

```text
skills/{category}/{skill-name}/SKILL.md
```

The suite should support a dynamic install target instead of hardcoding `.claude/skills`.

Recommended contract:

```yaml
install_target:
  platform: hermes
  scope: user-local
  path: ~/.hermes/skills/{category}/{skill-name}/
```

Possible values:

```yaml
platform: hermes | claude | both
scope: user-local | repo | project-local
```

### 9.2 Markdown tables are still treated as source of truth

The suite wants AI-first structured contracts, but much of the actual handoff still depends on Markdown tables.

This is fragile. A validator or agent can misread a Markdown table if:

- heading text changes
- formatting changes
- a file path appears in an example
- a zone is written in prose instead of table format
- a filename has an unusual extension

The better approach is YAML-first artifacts:

- `design.md` frontmatter contains canonical `zone_mapping`
- `todo.md` frontmatter contains canonical `phases`, `tasks`, `blockers`, `prerequisites`
- `build-log.md` frontmatter contains canonical `execution_trace`, `quality_metrics`, `resource_usage`

Markdown body should remain for explanation, but not as the machine contract.

### 9.3 Inconsistent internal contracts

Some instructions conflict with each other.

Examples:

1. `skill-planner` says `todo.md` must contain exactly 5 sections, but then defines a 6th section: Builder Feedback Integration.
2. `skill-architect` has conflicting signals about whether `knowledge/architect.md` is Tier 1 or Tier 2.
3. The shared framework treats scripts as optional, while some builder checklist wording implies scripts are mandatory.
4. The system sometimes says 7 zones, but some validator/checklist wording focuses on only 4 zones.
5. Build log location is not fully consistent: sometimes inside the generated skill package, sometimes inside `.skill-context/{skill-name}/build-log.md`.

These inconsistencies can cause me to choose the wrong rule during execution.

### 9.4 Validator is too regex-dependent

`validate_skill.py` is useful but currently depends too much on pattern matching.

Observed fragility:

- It parses `design.md` Zone Mapping using heading and backtick regex.
- It expects certain section keywords such as `## Persona`, `Workflow`, `Guardrails`.
- It checks progressive disclosure mostly through Markdown links.
- It hardcodes ignored extra files.
- It only counts `[MISSING_DOMAIN_DATA]` as placeholder evidence.

A stronger validator should read schema-backed YAML frontmatter first, then use Markdown only as secondary human-readable content.

### 9.5 Feedback learning loop is incomplete

The suite has build logs and some feedback fields, but the workflow for learning from actual usage is not yet strong enough.

The target goal is not only to create a skill once. The target goal is:

> Steve and the assistant work together, discover patterns, then continuously improve the skill system.

For that, the suite needs a formal refinement loop:

1. Observe a real session.
2. Identify recurring pain points or successful patterns.
3. Decide whether to save memory, patch a skill, create a new skill, or refactor an existing skill.
4. Apply the smallest safe patch.
5. Record why the change was made.
6. Verify that the skill still loads and remains concise.

### 9.6 Too many gates for small tasks

The architect currently requires multiple confirmation gates. This is good for strict workflows, but too heavy for small skill improvements.

The suite should support execution modes:

```yaml
mode: lightweight | standard | strict
```

Suggested behavior:

- `lightweight`: minimal questions, small patch-oriented output
- `standard`: normal 3-stage workflow
- `strict`: full gates, schemas, validators, build logs, and handoff checks

### 9.7 Create-new workflow dominates patch/refactor workflows

The current suite is strongest when creating a new skill from scratch.

But in real work, the common operations will often be:

- patch an existing skill
- add a pitfall
- add a missing command
- split a large skill
- merge duplicated skills
- migrate Claude-compatible skills into Hermes-compatible skills
- improve a validator after a bug

The suite should explicitly support:

```yaml
operation_type:
  - create_new
  - patch_existing
  - refactor_existing
  - migrate_platform
  - consolidate_skills
  - deprecate_skill
```

Without this, the builder may overbuild instead of making a focused patch.

---

## 10. Hermes-native improvements needed

Because this work is currently being used through Hermes Agent, the suite should encode Hermes-specific rules.

Recommended new knowledge file:

```text
skill-builder/knowledge/hermes-skill-standards.md
```

It should include:

1. User-local skills live under `~/.hermes/skills/`.
2. Skill creation via `skill_manage(action='create')` writes to the user-local tree.
3. In-repo skills require direct file writes under the repo `skills/` tree.
4. Current session may not see newly created skills because the loader can be cached.
5. Hermes frontmatter should include:
   - `name`
   - `description`
   - `version`
   - `author`
   - `license`
   - `metadata.hermes.tags`
   - `metadata.hermes.related_skills`
6. Supporting files should use allowed directories such as:
   - `references/`
   - `templates/`
   - `scripts/`
   - `assets/`
7. Small fixes should prefer targeted patching instead of full rewrites.
8. Do not assume `.claude/skills` unless platform is explicitly Claude.

This would make the builder safer in the current environment.

---

## 11. Recommended next improvement plan

### Phase 1: Fix contracts and contradictions

Patch the existing skill files to remove internal conflict:

- Fix `todo.md` section count: 5 vs 6 sections.
- Make `knowledge/architect.md` Tier 1 or Tier 2 consistently.
- Clarify scripts/templates/data/assets are optional unless declared in `zone_mapping`.
- Clarify build-log location.
- Replace `.claude/skills` hardcode with dynamic `install_target`.

### Phase 2: Introduce YAML-first artifacts

Add YAML frontmatter templates for:

- `design.md`
- `todo.md`
- `build-log.md`

Make YAML frontmatter the canonical source of truth. Markdown sections remain for human explanation.

### Phase 3: Add schemas and validators

Create or complete:

```text
_shared/schemas/design.schema.yaml
_shared/schemas/todo.schema.yaml
_shared/schemas/build-log.schema.yaml
_shared/validators/handoff_validator.py
_shared/validators/schema_validator.py
_shared/validators/trace_validator.py
```

Validators should read YAML contracts rather than parse Markdown tables.

### Phase 4: Add Hermes skill standards

Add Hermes-specific knowledge and make builder load it when target platform is Hermes.

Potential path:

```text
skill-builder/knowledge/hermes-skill-standards.md
```

### Phase 5: Add operation modes

Add:

```yaml
mode: lightweight | standard | strict
operation_type: create_new | patch_existing | refactor_existing | migrate_platform | consolidate_skills | deprecate_skill
```

This will let the assistant choose the appropriate level of ceremony.

### Phase 6: Add feedback/refinement loop

Create a formal post-use feedback mechanism.

Possible new stage:

```text
skill-refiner
```

or integrate into builder as:

```text
Phase 6: LEARN AND PATCH
```

Responsibilities:

- analyze session outcome
- capture pitfalls
- identify missing workflow steps
- propose skill patch
- update skill minimally
- record change rationale

---

## 12. Proposed target architecture

The future suite should look like this:

```text
User/session insight
  -> skill-architect
       outputs design.md with YAML contract
  -> skill-planner
       outputs todo.md with YAML tasks and blockers
  -> skill-builder
       outputs Hermes-compatible skill package
       outputs build-log.md with evidence
  -> skill-refiner or feedback loop
       patches existing skills based on real usage
```

Artifacts:

```text
.skill-context/{skill-name}/
├── design.md       # YAML contract + human explanation
├── todo.md         # YAML task graph + human checklist
├── build-log.md    # YAML execution trace + validation evidence
├── resources/      # domain source material
├── data/           # optional configs/schemas
└── loop/           # prior review notes, proofs, feedback
```

Skill output target:

```text
~/.hermes/skills/{category}/{skill-name}/
```

or, when building for a repo:

```text
{repo}/skills/{category}/{skill-name}/
```

---

## 13. Practical conclusion

The 3-skill suite already has a strong foundation. It gives me a valuable mental model for converting repeated collaboration into reusable, maintainable skills.

What I have received from it:

1. A staged process for skill creation.
2. A 7-zone package model.
3. A traceability-first planning method.
4. A builder mindset with validation and evidence.
5. A quality gate philosophy.
6. A clear direction toward AI-first, structured contracts.

What still needs improvement:

1. Make it Hermes-native.
2. Replace Markdown-as-contract with YAML-first contracts.
3. Remove internal contradictions.
4. Upgrade validators from regex parsing to schema validation.
5. Add execution modes for lightweight vs strict work.
6. Add patch/refactor workflows, not only create-new workflows.
7. Add a real learning loop so the suite improves through Steve-assistant collaboration.

Final assessment:

> The suite is a strong design draft with the right architecture. It should now be hardened into a Hermes-native, schema-backed, feedback-driven skill improvement system.

---

## 14. Short action checklist

- [ ] Patch output target from `.claude/skills` to dynamic `install_target`.
- [ ] Add Hermes Skill Standards knowledge file.
- [ ] Convert `design.md`, `todo.md`, and `build-log.md` into YAML-first artifacts.
- [ ] Add schema validators.
- [ ] Fix planner section count contradiction.
- [ ] Fix Tier 1/Tier 2 inconsistencies.
- [ ] Clarify optional vs mandatory zones.
- [ ] Add `mode` and `operation_type`.
- [ ] Add feedback/refinement loop.
- [ ] Use this report as raw material for the next spec in `docs/specs/`.
