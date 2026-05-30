# 🛠️ Comprehensive Code-Level and Architectural Audit Report: ver-0 Skill Suite

> **Document Class**: L0 Architectural Audit & Refactoring Specification
> **Target Suite**: ver-0 Skill Suite (`skill-explorer`, `skill-architect`, `skill-planner`, `skill-builder`, `skill-suite-upgrade`)
> **Standards Reference**: Claude Code Native Agent/Skill Specifications & `xml_tags_standards.yaml`
> **Author**: Senior LLM Agent Architect & Suite Auditor

---

## 1. Executive Summary

An exhaustive, code-level and architectural audit of the **ver-0 Skill Suite** has revealed critical integration gaps, schema incompatibilities, and logical breaks. While the suite aims to implement a highly structured pipeline (Stage 0 to Stage 4) using the **CASE System** (Confidence-Aware Skill Execution) framework, the actual implementation exhibits severe asymmetry, broken paths, massive duplication, and a failure to utilize **Claude Code native subagent capabilities** (such as lifecycle hooks, native tool containment, and isolated git worktrees).

### Key Audit Findings:
1. **Broken Shared References (Catastrophic)**: All skills in ver-0 attempt to boot by reading `../_shared/knowledge/framework.md` and validating outputs with `../_shared/validators/schema_validator.py`. However, **no `_shared` directory exists** in the ver-0 workspace, leading to immediate "file not found" execution failures.
2. **Schema & YAML Frontmatter Violations**: The skills pack complex logic (e.g., progressive disclosure schemas, capability maps, and constraints) directly inside the YAML frontmatter. This violates official Claude Code skill/agent specifications, which restrict frontmatter to designated metadata keys (`name`, `description`, `when_to_use`, etc.).
3. **XML Tag Fragmentation & Mismatches**: Across all skills, standard XML boundaries (like `<instructions>` and `<context>`) are used as inline annotations rather than clean top-level L0 boundaries. The `skill-suite-upgrade` skill completely lacks any XML boundaries, violating the `xml_tags_standards.yaml` constitution.
4. **Severe CASE System Asymmetry**: The CASE mechanisms (PREVENT → DETECT → RECOVER) are severely fractured. `check_status.py` and gate validator scripts exist *only* in `skill-suite-upgrade`, yet are referenced by other skills (like `skill-planner`) which cannot find or execute them. Automated rollback and staleness recovery exist only as high-level design prose in `case-system.md` and are entirely unimplemented in code.
5. **Massive DRY Violations**: Widespread copy-pasting of core files (`case-system.md` in 2 folders, `architect.md` in 3 folders, `format-standards.md` in 3 folders, and `init_context.py` in 2 folders) causes severe context bloating and maintenance friction.

---

## 2. Schema and YAML Frontmatter Incompatibilities

The official standards (`configuration_and_variables.md` for skills and `configuration.md` for subagents) restrict the YAML frontmatter to specific runtime-resolved properties. Stuffer fields or complex object definitions are ignored or break the parser.

### Auditing ver-0 Frontmatter Fields against Official Specifications:

| Skill | Non-Standard / Legacy Fields Identified | Impact & Risks |
| :--- | :--- | :--- |
| **`skill-explorer`** | `category: meta`<br>`tags: [...]`<br>`author: "Steve Void Team"` | Custom fields are ignored by the native parser. Lack of `disable-model-invocation: true` permits unintended automatic background triggers. |
| **`skill-architect`** | `category: meta`<br>`tags: [...]`<br>`author: "Steve Void Team"` | Same as above. Contains no native permission or tool locks, allowing the LLM to run arbitrary host commands during design. |
| **`skill-planner`** | `category: meta`<br>`case_system: true`<br>`pipeline: { ... }`<br>`progressive_disclosure: { ... }`<br>`priority_order: [...]`<br>`constraints: { ... }`<br>`output_contract: { ... }` | **Critical Incompatibility**: Stuffs heavy behavioral constraints and schemas into the frontmatter. Claude's native parser ignores these fields; the agent never registers the constraints unless it actively views the raw file as a text block, rendering the safety hooks useless. |
| **`skill-builder`** | `category: meta`<br>`pipeline: { ... }`<br>`progressive_disclosure: { ... }`<br>`priority_order: [...]`<br>`constraints: { ... }`<br>`output_contract: { ... }` | Same as above. Prevents native preloading or validation. |
| **`skill-suite-upgrade`**| `author: "Steve Void Team"`<br>`pipeline: { ... }`<br>`progressive_disclosure: { ... }` | Bypasses standard skill configuration. Binds no native hooks, relying on the LLM to execute manual shell scripts. |

### Corrective Realignment (Unified Schema):
Under Claude Code native agent specifications, structural workflows (like `pipeline` and `progressive_disclosure`) and core rules (like `constraints` and `output_contract`) must reside inside the **Markdown body** wrapped in standardized **XML boundaries**—never inside the frontmatter. The frontmatter must strictly serve as a light metadata envelope:

```yaml
---
name: skill-planner
description: "Phân rã bản thiết kế design.md thành todo.md và chuẩn bị tài nguyên."
when_to_use:
  - "User explicitly asks to: 'lập kế hoạch skill' or 'tạo todo.md'"
  - "Working on files matching: '.skill-context/*/design.md'"
disable-model-invocation: true
user-invocable: true
effort: high
---
```

---

## 3. XML Tags Standardization Audit

The `xml_tags_standards.yaml` sets absolute formatting boundaries to isolate instructions, context, rules, and examples. The ver-0 implementation systematically violates these boundaries.

### Analysis of XML Tag Violations in ver-0:

1. **Monolithic instruction Pollution (in `skill-explorer` & `skill-architect`)**:
   - The `<instructions>` tag wraps mixed content (Markdown headers, numbered boot sequence steps, and nested ````yaml ```` code blocks).
   - *Standard violation*: The preferred format for `<instructions>` is structured YAML containing `must`, `must_not`, and `constraints`. Markdown prose belongs in `<context>` or the standard body.
2. **Scatter and Fragmentation (in `skill-planner` & `skill-builder`)**:
   - The files use multiple separate `<instructions>` and `<context>` blocks scattered down the body as inline section captions (e.g., `skill-planner/SKILL.md` has 3 distinct `<instructions>` and 3 `<context>` tags).
   - *Standard violation*: XML tags are meant to serve as stable L0 anchor boundaries. Scattering them dilutes their authority and forces the LLM to process fragmented prompts.
3. **Complete Absence of XML Boundaries (in `skill-suite-upgrade`)**:
   - `skill-suite-upgrade/SKILL.md` contains **no XML tags**. It uses Markdown blockquotes (`> 🚨 MỆNH LỆNH BẮT BUỘC`) to attempt rule enforcement.
   - *Standard violation*: Blockquotes carry zero structural weight for an LLM parser compared to designated XML boundaries. This completely bypasses the token containment rules.
4. **Spacing and Tag Proximity Issues**:
   - Tags are placed directly next to headers (e.g., `<instructions>## BOOT SEQUENCE`) without appropriate newlines, causing rendering issues in Claude's prompt assembly engine.
5. **Non-Standard Semantic Tags**:
   - `skill-explorer` specifies using `<external_input>...</external_input>` (line 45). The official standard tag is `<input>`.

---

## 4. CASE System Integration Gaps

The CASE (Confidence-Aware Skill Execution) System framework is conceptually strong but programmatically broken in ver-0 due to extreme asymmetry and a lack of unified shared utilities.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ver-0 Fractured CASE System                            │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│          PREVENT           │           DETECT            │           RECOVER           │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ ❌ check_status.py missing │ ❌ validate_gate.py is in   │ ❌ Rollback scripts only    │
│    from planner/builder.   │    suite-upgrade only.      │    pseudocode in case-sys.  │
│ ❌ _shared/framework.md    │ ❌ validate_zone_mapping.py │ ❌ Checkpoint staleness is  │
│    references are broken.  │    is siloed.               │    never acted upon.        │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

### Breakdown of CASE System Gaps:

#### A. PREVENT (State-Aware Boot & Progressive Disclosure)
* **Missing Boot Scripts**: `skill-planner/SKILL.md` (lines 31-33) instructs the agent to run `scripts/check_status.py` during boot. However, **`scripts/check_status.py` does not exist** inside `skill-planner/scripts/`! It is siloed inside `skill-suite-upgrade/scripts/`. Running this command will crash the agent session.
* **Asymmetric Boot Implementations**: `skill-explorer` has no boot sequence check or state-awareness whatsoever. `skill-architect` and `skill-builder` lack state-aware verification scripts.
* **Broken Shared Context Pathing**: `skill-explorer`, `skill-architect`, and `skill-builder` attempt to read `../_shared/knowledge/framework.md` to load pipeline rules. Because `_shared` is completely missing from the directory tree, the boot sequence immediately errors out.

#### B. DETECT (Gate Validators & Reverse Trace)
* **Siloed Validators**: `validate_gate.py` and `validate_zone_mapping.py` are exclusively present in `skill-suite-upgrade/scripts/`. The `skill-architect` and `skill-builder` files declare gates and check-conditions but cannot run any validation programmatically.
* **No Code-Level Reverse Tracing**: Automated reverse trace checking (checking if §3 Zone Mapping files resolve to §1 Pain Points) exists only as conceptual Python pseudocode in the `case-system.md` documentation. No script executes it, allowing scope drift to bypass undetected.

#### C. RECOVER (Rollback Procedures & Checkpoint Resumes)
* **Completely Unimplemented Rollbacks**: There are **zero scripts** or commands that implement actual file rollback (`rollback.py` or equivalent). If a validation fails, the agent has no automated recovery mechanism, violating the core pillar of the CASE specification.
* **Passive Staleness Checks**: `check_status.py` returns staleness alerts (warning/danger for checkpoints older than 7 or 30 days), but none of the skills have prompt loops or execution constraints configured to handle these outputs. The agent simply ignores staleness and proceeds.

#### D. Severe DRY Violations (Code Bloat)
Ver-0 duplicates files across skill directories to compensate for the missing shared framework:
* `knowledge/case-system.md` is duplicated in `skill-planner/` and `skill-suite-upgrade/`.
* `knowledge/architect.md` is duplicated in `skill-architect/`, `skill-builder/`, and `skill-planner/`.
* `knowledge/format-standards.md` is duplicated in `skill-architect/`, `skill-builder/`, and `skill-planner/`.
* `scripts/init_context.py` is duplicated in `skill-explorer/` and `skill-architect/`.

*Impact*: Modifying a core architectural design rule requires editing 3 separate markdown files. This bloats the repository size, causes immediate rule divergence, and degrades context window efficiency.

---

## 5. Claude Code Native Subagent Integration Gaps

The ver-0 suite treats skills as **passive Markdown prompts** rather than utilizing **Claude Code native Subagents** (detailed in `agents/configuration.md` and `agents/hooks_and_events.md`). This leaves severe capability gaps:

1. **Lack of Lifecycle Hook Integration**:
   - Claude Code native subagents support `hooks` (`PreToolUse`, `PostToolUse`, `Stop`) inside their YAML frontmatters.
   - *The Gap*: Ver-0 relies entirely on the LLM to remember to run validator scripts like `validate_gate.py` before seeking user approval. By wrapping validators in native `PreToolUse` hooks, **the Claude Code runtime itself** will intercept the `AskUserQuestion` tool, execute the python validator, and block user interaction if validation fails (returning exit code 2 and stderr directly to Claude for self-healing).
2. **Missing Tool containment Policies**:
   - Ver-0 fails to use native properties like `tools`, `disallowedTools`, or `allowed-tools` to enforce safety boundaries. For example, `skill-explorer` should explicitly disallow file-writing tools to ensure it remains a strictly read-only stage.
3. **No Workspace Isolation**:
   - The native `isolation: worktree` frontmatter property is completely ignored. This property is crucial for `skill-builder` and `skill-suite-upgrade` as it forces them to execute in isolated git worktrees, protecting the main developer checkout from corrupted test runs or incomplete builds.
4. **Ignored Concurrent Backgrounding**:
   - The native `background: true` property is never declared. For parallelized exploration and mining (e.g. running research in the background while compiling design in the foreground), this is a wasted performance opportunity.

---

## 6. Proposed Unified Architecture for ver-1

To resolve the schema incompatibilities, broken paths, and CASE system fragmentation, we propose a **fully unified, CASE-compliant, and XML-standardized architecture** for `ver-1`.

This architecture introduces:
1. A centralized `_shared/` directory at the suite root to house all common schemas, common python validators, and global markdown knowledge.
2. Conversion of the 5 skills into **Claude Code Native Subagents** utilizing lifecycle hooks for automatic gate validation.
3. A strict L0/L1 progressive disclosure layout using XML semantic tags.

### 6.1 ver-1 Directory Layout

```text
skills/rebuild/ver-1/
├── _shared/                           # Centralized Common Assets (DRY Compliant)
│   ├── knowledge/
│   │   ├── framework.md               # Pipeline stage rules & 7-Zone architecture
│   │   ├── case-system.md             # Consolidated CASE framework standard
│   │   └── format-standards.md        # XML & YAML token-optimization guidelines
│   ├── schemas/
│   │   ├── exploration.schema.yaml
│   │   ├── design.schema.yaml
│   │   └── todo.schema.yaml
│   └── validators/
│       ├── core_case.py               # Combined class for status, gate, & zone validation
│       ├── rollback_engine.py         # Automates checkpoint rollback & backups
│       └── init_context.py            # Global context bootstrapper
│
├── agent-explorer.md                  # Native Explorer Subagent (Stage 0)
├── agent-architect.md                 # Native Architect Subagent (Stage 1)
├── agent-planner.md                   # Native Planner Subagent (Stage 2)
├── agent-builder.md                   # Native Builder Subagent (Stage 3)
└── agent-suite-upgrade.md             # Native Upgrade Subagent (Stage 4)
```

### 6.2 Unified Pipeline & State Transitions (Mermaid Flow)

```mermaid
flowchart TD
    %% Define Pipeline Stages
    subgraph Stage0 [Stage 0: Explorer]
        E_Init[init_context.py] --> E_Scan[Scout & Mine Resources]
        E_Scan --> E_Explore[Generate exploration.md]
    end

    subgraph Stage1 [Stage 1: Architect]
        A_Boot[Boot: read status] --> A_Collect[Collect & Analyze]
        A_Collect --> A_Gate1{Gate 1: Problem}
        A_Gate1 -- PASS --> A_Pillars[Design: 3 Pillars]
        A_Pillars --> A_Gate2{Gate 2: Architecture}
        A_Gate2 -- PASS --> A_Diagrams[Design: Diagrams]
        A_Diagrams --> A_Gate3{Gate 3: Complete Design}
        A_Gate3 -- PASS --> A_Write[Write design.md with status: phase=1]
    end

    subgraph Stage2 [Stage 2: Planner]
        P_Boot[Boot: core_case.py status] --> P_Audit[Audit Resources Rich vs Thin]
        P_Audit --> P_Plan[Breakdown 3-Tier Tasks]
        P_Plan --> P_Gate4{Gate 4: Check todo.md}
        P_Gate4 -- PASS --> P_Write[Write todo.md with status: phase=2]
    end

    subgraph Stage3 [Stage 3: Builder]
        B_Boot[Boot: core_case.py status] --> B_Build[Build 7-Zone Skill Files]
        B_Build --> B_Validate[validate_skill.py]
        B_Validate --> B_Gate5{Gate 5: Delivery & DoD}
        B_Gate5 -- PASS --> B_Deliver[Write build-log.md with status: phase=3]
    end

    %% State and validator triggers
    E_Explore -->|exploration.md| A_Boot
    A_Write -->|design.md| P_Boot
    P_Write -->|todo.md| B_Boot

    %% CASE hook and script connections
    Validator([_shared/validators/core_case.py]) -.->|State checks| A_Boot
    Validator -.->|State checks| P_Boot
    Validator -.->|State checks| B_Boot
    
    Hook[PreToolUse: validate_gate] -->|Intercepts AskUserQuestion| Validator
    Validator -->|Success: exit 0| UserConfirm[User Approves Stage]
    Validator -->|Fail: exit 2 / Rollback| Rollback[rollback_engine.py]
    Rollback -->|Revert State| A_Collect
```

### 6.3 Progressive Disclosure XML Tag Blueprint

Under the realigned `ver-1` standards, each agent file (e.g., `agent-planner.md`) implements a clean L0 structure utilizing standard XML tags:

```markdown
---
name: planner-agent
description: "Phân tích design.md thành todo.md và đánh giá tài nguyên."
tools: Read, Write, Glob, Grep
disallowedTools: Bash
model: sonnet
hooks:
  PreToolUse:
    - matcher: "AskUserQuestion"
      hooks:
        - type: "command"
          command: "python3 _shared/validators/core_case.py --gate 4"
---

You are the Senior Planning Agent. You decompose architectural designs into concrete task items.

<instructions>
must:
  - trace every task in todo.md back to a design.md section using the format: [TỪ DESIGN §N]
  - label missing resource tasks using: [TỪ AUDIT TÀI NGUYÊN]
  - run the core_case.py status check at startup before taking any actions
must_not:
  - invent requirements or features not explicitly described in the design.md
  - proceed to Phase 3 if resource audits return any critical "Thin" status
</instructions>

<context>
### Unified Stage Context
This agent operates as Stage 2 of the unified CASE pipeline. It expects a validated `design.md` file located at the active `.skill-context/{skill-name}/` folder.
</context>

<output_contract>
include:
  - pre_requisites_table
  - phase_breakdown_with_traces
  - definition_of_done
  - notes_with_clarifications
format: markdown_with_yaml_frontmatter
</output_contract>
```

---

## 7. Actionable Implementation Roadmap to ver-1

To achieve full compliance and deploy a production-grade ver-1 Skill Suite, execute the following step-by-step roadmap:

### Step 1: Consolidate Common Context and DRY Assets
1. Create the unified `/home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/ver-1/_shared/` directory.
2. Relocate and consolidate the duplicated knowledge files:
   - Create `_shared/knowledge/framework.md` (combining the best features of L0 frameworks).
   - Create `_shared/knowledge/case-system.md` (unified CASE specifications).
   - Create `_shared/knowledge/format-standards.md` (XML and token standards).
3. Delete all duplicate knowledge files from the individual agent subdirectories.

### Step 2: Implement Centralized Validation and Rollback Scripts
1. Write a unified, production-grade validation python script at `_shared/validators/core_case.py` containing:
   - Status parser (extracting the `status` block from YAML frontmatter).
   - Gate validator (implementing machine-checkable assertions for Gates 1 to 5).
   - Zone mapping validator (verifying structural schemas).
   - Staleness checker (calculating epoch days and raising alerts).
2. Write `_shared/validators/rollback_engine.py` which:
   - Automatically archives the current `.skill-context/` state before modifying files.
   - Implements programmatic rollback to any valid previous stage checkpoint upon verification failure or user command.

### Step 3: Upgrade Skills to Claude Code Native Subagents
1. Convert each `SKILL.md` file in the 5 directories into native agent files under `ver-1/`:
   - Rename to `agent-explorer.md`, `agent-architect.md`, `agent-planner.md`, `agent-builder.md`, `agent-suite-upgrade.md`.
2. Extract all constraints, output contracts, and boot checklists out of YAML frontmatters and place them strictly within `<constraints>` and `<output_contract>` Markdown body tags.
3. Inject native Subagent hook mappings:
   - Bind `core_case.py --gate N` to the `PreToolUse` hook intercepting `AskUserQuestion`.
   - Bind specific tool restrictions (e.g. read-only tool list for explorer, worktree isolation for builder).

### Step 4: Validate and Deploy the Unified Suite
1. Setup a test-workspace in `skills/rebuild/ver-1/`.
2. Execute the entire pipeline end-to-end to create a mockup micro-skill:
   - Run Explorer → pass Stage 0.
   - Run Architect → validate Gates 1-3.
   - Run Planner → validate Gate 4 and trace todo.md.
   - Run Builder → implement mock, execute build-log, and validate Gate 5.
3. Run native testing suite inside a Docker/gVisor sandbox.
4. Deploy the validated suite to active project runtimes (`.claude/agents/` and global user spaces `~/.claude/agents/`) using a consolidated sync script.
