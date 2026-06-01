# Implementation Plan: Dynamic Quality Gates Synthesis Implementation (todo.md)

This plan maps design goals to concrete tasks to upgrade the `production-quality-gatekeeper` skill.

---

## §1. Pre-requisites & Resource Checklist
| Component / File | Role | Traceability | Status |
| --- | --- | --- | --- |
| `/home/steve/Work-space/deep_work_by_steve/.skill-context/karpathy-standards.md` | Core standards guidelines. | Upstream reference | ✅ Available |
| `skills/production-quality-gatekeeper/SKILL.md` | Main instruction file to rewrite. | Zone 1 | ✅ Loaded |
| `skills/production-quality-gatekeeper/scripts/loop_refiner.py` | Legacy critic file to deprecate or wrap. | Zone 3 | ✅ Loaded |

---

## §2. Progressive Implementation Roadmap

### Phase 1: Core Synthesis Engine Setup (High Priority)
* **Goal**: Build the Parallel Reasoning + Deliberation generator to dynamically output targeted gates.
* **Tasks**:
  1. **Task 1.1**: Create the dynamic schema template at `skills/production-quality-gatekeeper/data/dynamic-gates.yaml` defining rule structures, AST validations, and messages.
     - *Trace*: [DESIGN §2, DESIGN §3]
  2. **Task 1.2**: Implement `skills/production-quality-gatekeeper/scripts/gate_synthesizer.py`.
     - *Details*: This script reads the user task requirements and matches them against pre-defined domains or runs parallel thinking prompts. If offline or dynamic, it parses keywords (`stripe`, `webhook`, `atomic`, `concurrency`, `threading`, `asyncio`, `encrypt`) to auto-synthesize the 5-10 business gates in `dynamic-gates.yaml`.
     - *Trace*: [DESIGN §4, DESIGN §5]

### Phase 2: Dynamic Programmatic Critic Engine (High Priority)
* **Goal**: Build the critic engine to load the synthesized YAML and inspect python files using AST and semantic regex rules.
* **Tasks**:
  1. **Task 2.1**: Implement `skills/production-quality-gatekeeper/scripts/dynamic_critic.py`.
     - *Details*: Load `data/dynamic-gates.yaml`. Read targeted code using `ast.parse()`. Run structural assertions (e.g., matching function definitions, ensuring calls to signature functions, verifying lock structures, identifying PII logging, finding missing db transaction boundaries).
     - *Trace*: [DESIGN §3, DESIGN §5, DESIGN §6]
  2. **Task 2.2**: Integrate `dynamic_critic.py` with standard Karpathy-compliant feedback.
     - *Details*: On failures, write specific, clear errors with exact line context and fix hints into `.skill-context/production-quality-gatekeeper/feedback.yaml`.
     - *Trace*: [DESIGN §6, HANDBOOK §4]

### Phase 3: Instruction Set Refactor (Medium Priority)
* **Goal**: Update the main SKILL.md rules to point to the new dynamic pipeline.
* **Tasks**:
  1. **Task 3.1**: Edit `skills/production-quality-gatekeeper/SKILL.md`.
     - *Details*: Remove all references to static `loop_refiner.py --domain`. Update instructions to run `gate_synthesizer.py` first, then run the dynamic loop with `dynamic_critic.py`.
     - *Trace*: [DESIGN §1, DESIGN §3]

### Phase 4: Integration & Test Verification (Medium Priority)
* **Goal**: Verify correctness against our test scenarios.
* **Tasks**:
  1. **Task 4.1**: Create testing sandbox files inside `skills/production-quality-gatekeeper/tests/` replicating insecure/secure Stripe configurations and threading codes.
     - *Trace*: [QUALITY-MATRIX §1]
  2. **Task 4.2**: Run dynamic validation checks, verify exit codes, and generate final reports.
     - *Trace*: [QUALITY-MATRIX §3]

---

## §3. Definition of Done (DoD)
The upgrade is considered fully complete and successful when:
1. `gate_synthesizer.py` automatically compiles a unique list of 5-10 business/security gates based on domain keywords in less than 2 seconds.
2. `dynamic_critic.py` correctly parses python scripts with AST and flags missing structures without throwing compilation errors.
3. Test suite returns PASS for TC-GATE-02 & TC-GATE-04, and FAIL for TC-GATE-01 & TC-GATE-03 with 100% precision.
4. The final markdown evaluation report lists the exact status of the customized business gates.

---
*Implementation Plan completed by Stage 3 (Skill Planner).*
*Stored under: `/home/steve/Work-space/deep_work_by_steve/.skill-context/gatekeeper-upgrade-loop/todo.md`*
