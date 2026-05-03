# MASTER FRAMEWORK — Shared Knowledge Base

> **Purpose**: Single source of truth for all 3 meta-skills
> **Location**: `_shared/knowledge/framework.md` (portable, resolved relative to skills-root)
> **Path from SKILL.md**: `../_shared/knowledge/framework.md` (1 level up)
> **Path from knowledge/*.md**: `../../_shared/knowledge/framework.md` (2 levels up)
> **Usage**: Read this FIRST when working with skill-architect, skill-planner, or skill-builder

---

## 1. SEVEN ZONES STRUCTURE

Every skill package MUST follow this directory structure:

| Zone | Folder | Purpose | Required |
|------|--------|---------|----------|
| **Core** | `SKILL.md` | Orchestration, persona, workflow, guardrails | ✅ Always |
| **Knowledge** | `knowledge/` | References, standards, guidelines | ✅ Usually |
| **Scripts** | `scripts/` | Executable automation (Python, Bash) | As needed |
| **Templates** | `templates/` | Output format templates | As needed |
| **Data** | `data/` | Config, static data, schemas | As needed |
| **Loop** | `loop/` | Checklists, logs, test cases | ✅ Usually |
| **Assets** | `assets/` | Images, icons, static files | Rarely |

---

## 2. PIPELINE FLOW

```
skill-architect          skill-planner           skill-builder
     │                        │                        │
     ▼                        ▼                        ▼
design.md §3       →    todo.md tasks      →   <skills-root>/{name}/
(Zone Mapping)         (phase breakdown)          (skill package)
     │                        │
     ▼                        ▼
design.md §7       →    Pre-req table
(PD Plan)               (resources audit)
```

### Handoff Contracts

**Architect → Planner** (design.md sections):
- §3 Zone Mapping → Planner creates task breakdown
- §7 Progressive Disclosure → Planner audit resources
- §8 Risks → Planner creates mitigation tasks

**Planner → Builder** (todo.md):
- Phase tasks with priorities
- Pre-requisites table
- Resource readiness status

---

## 3. ZONE MAPPING CONTRACT

When reading `design.md §3`, all skills must follow this format:

| Zone | Files cần tạo | Nội dung | Bắt buộc? |
|------|--------------|----------|-----------|
| Core | `SKILL.md` | Persona, phases, guardrails | ✅ |
| Knowledge | `knowledge/xxx.md` | Domain, standards | ✅/❌ |
| Scripts | `scripts/xxx.py` | Automation tools | ✅/❌ |
| Templates | `templates/xxx.template` | Output formats | ✅/❌ |
| Data | `data/xxx.yaml` | Config, schema | ✅/❌ |
| Loop | `loop/xxx.md` | Checklists, verify rules | ✅/❌ |
| Assets | N/A | Not needed | ❌ |

**Rules**:
- "Files cần tạo" column → direct input for task creation
- "Không cần" → skip that zone
- Builder MUST NOT add files not in §3 (except with documented rationale)

---

## 4. PROGRESSIVE DISCLOSURE (PD)

Three-tier loading system:

| Tier | Name | When to Load | Examples |
|------|------|--------------|----------|
| **Tier 1** | Mandatory | Always, at boot | `SKILL.md`, core knowledge |
| **Tier 2** | Conditional | When context requires | Domain docs, templates |
| **Tier 3** | Optional | On-demand | Assets, edge-case references |

**PD in SKILL.md**:
- Boot Sequence → Tier 1 files only
- Each Phase → Reference Tier 2 files as needed

---

## 5. PIPELINE STAGE DEFINITIONS

| Stage | Skill | Input | Output | Key Sections |
|-------|-------|-------|--------|--------------|
| **1** | skill-architect | User requirements | `design.md` | §1-§12 |
| **2** | skill-planner | `design.md` | `todo.md` | Pre-reqs, Phase Breakdown |
| **3** | skill-builder | `design.md` + `todo.md` | Skill files | SKILL.md, knowledge/*, loop/* |

---

## 6. NAMING CONVENTIONS

### Skill Names
- **Pattern**: `kebab-case` (lowercase, hyphen-separated)
- ✅ `skill-planner`, `api-integrator`, `flow-design-analyst`
- ❌ `SkillPlanner`, `skill_planner`, `skill planner`

### File Names in Zones
| Zone | Pattern | Example |
|------|---------|---------|
| knowledge/ | `domain-topic.md` | `uml-rules.md`, `api-standards.md` |
| scripts/ | `action-target.py` | `init-context.py`, `validate-skill.py` |
| templates/ | `output-format.template` | `design-md.template` |
| loop/ | `purpose-checklist.md` | `design-checklist.md`, `plan-checklist.md` |
| data/ | `config-name.yaml` | `skill-config.yaml` |

---

## 7. ANTI-HALLUCINATION RULES

| Rule | Description | Violation |
|------|-------------|-----------|
| **AH1** | Every task MUST trace to source | Task without `[TỪ DESIGN §N]` |
| **AH2** | Only decompose, don't add requirements | New requirement not in design.md |
| **AH3** | Don't guess domain knowledge | Writing domain content without resources |
| **AH4** | Always label sources | No `[TỪ DESIGN]` / `[GỢI Ý]` distinction |
| **AH5** | Verify resources before completion | Planning complete with missing critical resources |

### Trace Tags Standard

```
[TỪ DESIGN §N]      — Derived directly from design.md section N (regex: ^\[TỪ DESIGN §[0-9]+(\.[0-9]+)?\]$)
[GỢI Ý BỔ SUNG]     — Suggested by skill, not in design.md
[TỪ AUDIT TÀI NGUYÊN] — Generated because resource was missing
[CẦN LÀM RÕ]        — Needs user clarification
```

---

## 8. VERSION MANAGEMENT

All skills use Semantic Versioning:

```
MAJOR.MINOR.PATCH
- MAJOR: Breaking changes (output format, workflow)
- MINOR: Backward-compatible (new features)
- PATCH: Bug fixes, documentation
```

**Version update rules**:
- New section (§11, §12) → MINOR
- Zone Mapping format change → MAJOR
- Typo fix, add example → PATCH

---

## 9. CONTEXT DIRECTORY STRUCTURE

```
.skill-context/{skill-name}/
├── design.md        # Architect's output (INPUT)
├── todo.md          # Planner's output (INPUT)
├── build-log.md     # Builder's output (EVIDENCE)
├── resources/       # User-provided domain docs (INPUT)
├── data/            # Rule configs, scoring matrix (INPUT)
└── loop/            # Prior checks, phase logs (SUPPORTIVE)
```

### Resource Priority Classification

| Priority | Contents | Must Appear In |
|----------|----------|----------------|
| **Critical** | design.md, todo.md, resources/*, data/* | Resource Usage Matrix |
| **Supportive** | loop/*, proof/snapshots | Optional |

---

## 10. QUALITY GATES

### Architect → Planner Gate
- [ ] §3 Zone Mapping has specific filenames (no placeholders)
- [ ] §7 distinguishes Tier 1 vs Tier 2
- [ ] §8 has ≥3 risks with mitigation
- [ ] §9 open questions resolved or flagged

### Planner → Builder Gate
- [ ] All §3 files mapped to specific tasks
- [ ] Pre-requisites table complete
- [ ] Resource audit shows "Rich" status
- [ ] Phase breakdown has priorities and dependencies

### Builder → Complete Gate
- [ ] Placeholder density <5 (WARNING at 5-9, FAIL at 10+)
- [ ] All files in §3 created
- [ ] Resource Usage Matrix populated
- [ ] build-log.md contains evidence

---

> **Last Updated**: 2026-05-03
> **Maintained By**: Meta-Skill Suite
