---
skill_schema_version: "3.0.0"
artifact_type: "design"
skill_name: "production-quality-gatekeeper"
generated_by: "skill-architect"
generated_at: "2026-05-30T21:55:00+07:00"
stage: "Stage 3: Builder Complete"
status:
  phase: 4
  gates_passed: [1, 2, 3, 4]
  last_actor: "builder"
  confidence: 100
  created: "2026-05-30T21:55:00+07:00"
  updated: "2026-05-30T22:00:00+07:00"
zone_mapping:
  core: "SKILL.md"
  knowledge:
    - "knowledge/creative-standards.md"
    - "knowledge/dev-standards.md"
    - "knowledge/llm-evaluator.md"
  scripts:
    - "scripts/loop_refiner.py"
  data:
    - "data/quality-matrix.yaml"
  loop:
    - "loop/gate-checklist.yaml"
  templates:
    - "templates/evaluation-report.md.template"
---

# 🏗️ Architectural Design Specification: production-quality-gatekeeper

> **Stage**: 1 — Architect Design Complete
> **Target Path**: `/skills/rebuild/production-quality-gatekeeper/`

---

## 1. Problem Statement

* **Context**: Human developers and AI users face low-quality, generic outputs from AI Agents that fall short of "production-grade" standards. 
* **The Core Pain Point**: AI inputs usually lack robust, structured criteria to measure success, and humans have limited time or domain knowledge to detail them. Manual iterative cycles take at least 10 rounds of back-and-forth prompting, wasting resources and context space.
* **The Solution**: Build `production-quality-gatekeeper`, a micro-skill that automatically generates a multi-dimensional, layered quality matrix (across Creative, Dev, and LLM domains) and manages an automated, local self-refining loop to iteratively edit and polish the output until 100% of the criteria are met, ensuring production quality in a single prompt transaction.

---

## 2. Capability Map (3 Pillars of Design)

```
┌─────────────────────────────────────────────────────────────────┐
│              production-quality-gatekeeper                      │
├───────────────────┬──────────────────────┬──────────────────────┤
│     KNOWLEDGE     │       PROCESS        │      GUARDRAILS      │
│  Domain standards │  Iterative refinement│  Strict pass criteria│
│  & Quality Matrix │  loop (1-10 turns)   │  & error mitigation  │
└───────────────────┴──────────────────────┴──────────────────────┘
```

* **Pillar 1: Knowledge (Domain Expertise)**:
  * Codifies industry-standard guidelines for Creative writing (Pacing, Narrative Arc, Cliché avoidance), Dev/Coding (SOLID, Exception Handling, Edge cases, Security), and LLM Evaluation (Rule enforcement, System isolation).
* **Pillar 2: Process (The Loop Engine)**:
  * Orchestrates the 10-turn self-refining loop. Programmatically identifies failed criteria, compiles detailed feedback, and feeds it back to the drafting agent to perform highly targeted incremental edits.
* **Pillar 3: Guardrails (Quality Gates)**:
  * Implements strict binary check policies (Pass/Fail) to remove model ambiguity. If a critical criterion fails 3 times in a row, it triggers mitigation steps to prevent infinite looping.

---

## 3. Zone Mapping

Every file of the skill package is mapped below following the 7 Zones framework:

| Zone | Path | Content / Purpose | Required |
| :--- | :--- | :--- | :--- |
| **Core** | `SKILL.md` | Persona, orchestration rules, and progressive disclosure | ✅ Yes |
| **Knowledge** | `knowledge/creative-standards.md` | Rules for Creative writing, avoiding sáo ngữ AI | ✅ Yes |
| **Knowledge** | `knowledge/dev-standards.md` | Rules for production-grade coding, safety, solid | ✅ Yes |
| **Knowledge** | `knowledge/llm-evaluator.md` | Standard evaluations for prompt-engineering/XML | ✅ Yes |
| **Scripts** | `scripts/loop_refiner.py` | Local python engine that automates the 1-10 self-refinement loops | ✅ Yes |
| **Data** | `data/quality-matrix.yaml` | Static YAML configurations of scoring parameters | ✅ Yes |
| **Templates** | `templates/evaluation-report.md.template` | Document layout for the evaluation report output | ✅ Yes |
| **Loop** | `loop/gate-checklist.yaml` | Machine-readable checklist to audit output readiness | ✅ Yes |
| **Assets** | N/A | Not required | ❌ No |

---

## 4. Folder Structure

```mermaid
mindmap
  root((production-quality-gatekeeper))
    Core
      SKILL.md
    Knowledge
      creative-standards.md
      dev-standards.md
      llm-evaluator.md
    Scripts
      loop_refiner.py
    Data
      quality-matrix.yaml
    Templates
      evaluation-report.md.template
    Loop
      gate-checklist.yaml
```

---

## 5. Execution Flow

The sequence diagram below shows how the self-refining loop operates programmatically using `loop_refiner.py`:

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Main Agent
    participant GK as quality-gatekeeper (SKILL.md)
    participant Engine as scripts/loop_refiner.py
    participant LLM as Refiner (Draft Agent)

    User->>GK: Trigger Skill with input & context
    GK->>GK: Run Boot Check (check_status)
    GK->>Engine: Initialize Loop with target draft
    Loop 1 to 10 Turns
        Engine->>Engine: Run Handoff Gate (Binary Score check)
        alt All Criteria Passed (100% Score)
            Engine->>GK: Return flawless production draft
            GK->>User: Deliver output + Evaluation Report
        else Some Criteria Failed
            Engine->>Engine: Compile failed criteria into Feedback
            Engine->>LLM: Send Feedback (targeted edit prompt)
            LLM->>Engine: Return refined draft (incrementally edited)
        end
    end
    alt Max Turns Reached & Fails
        Engine->>GK: Trigger Mitigation: Return best draft + warning
        GK->>User: Deliver draft with incomplete criteria report
    end
```

---

## 6. Interaction Points

| Trigger / Command | Actor | Action / Purpose | Expected Output |
| :--- | :--- | :--- | :--- |
| `/quality-gatekeeper [target_file]` | User / Agent | Manually runs the quality evaluation on a specific file | Detailed `evaluation-report.md` |
| `--refine` argument | Agent | Starts the 10-turn self-refinement loop on the target draft | Perfected draft + report |

---

## 7. Progressive Disclosure Plan

To optimize token usage, the skill loads its files incrementally:

```yaml
progressive_disclosure:
  tier1: # Loaded at Boot
    - "SKILL.md"
    - "data/quality-matrix.yaml"
  tier2: # Loaded Conditionally
    - "knowledge/creative-standards.md" # Triggered when: domain == creative
    - "knowledge/dev-standards.md"      # Triggered when: domain == dev
    - "knowledge/llm-evaluator.md"      # Triggered when: domain == llm
  tier3: # Loaded On-Demand
    - "templates/evaluation-report.md.template" # Loaded when: generating report
    - "loop/gate-checklist.yaml"                 # Loaded when: validating gate
```

---

## 8. Risks & Mitigations

| Risk / Blind Spot | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Infinite LLM Loop**: LLM refines endlessly without passing a minor criteria. | High | **Turn Cap**: Strict limit of 10 turns managed by `loop_refiner.py`. **Targeted Editing**: Forcing the refiner to only touch the failed lines, protecting already passed lines. |
| **Context Bloat**: Feeding the entire history of 10 loops into the LLM context. | Medium | **Compaction**: The script compiles *only* the current draft and the active failed criteria feedback list for the next turn, discarding previous intermediates. |
| **Criterion Ambiguity**: LLM grades too leniently (hallucinates success). | High | **Binary strictly check**: All criteria must be written as testable, non-ambiguous parameters, evaluated with strict regex or binary rules in `loop_refiner.py`. |

---

## 9. Open Questions

| Question | Status | Planned Resolution |
| :--- | :--- | :--- |
| Should we integrate Python AST parsing for coding checks? | Deferred | For `ver-1`, we will use regex and LLM binary checking. In `ver-2`, we can hook AST/linters to the validator. |

---

## 10. Metadata

* **Stage Order**: 1 (Architect Design Complete)
* **Successor Stage**: Stage 2 (Planner - todo.md creation)
* **Approval Date**: 2026-05-30
* **Author**: Steve Void Team
