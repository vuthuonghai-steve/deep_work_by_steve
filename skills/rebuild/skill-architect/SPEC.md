---
spec_version: "1.0.0"
skill_name: "skill-architect"
based_on:
  - "CLAUDE.md AI-First Documentation Standard v1.0"
  - "Heavy Thinking arXiv:2605.02396"
  - "Agent Skill Framework architure.md v2.0"
last_updated: "2026-05-15"
maintained_by: "Steve Void Team"
---

# skill-architect Technical Specification

## 1. Semantic Questions

When reading this skill, the LLM must be able to answer:

| # | Question | Answerable From |
|---|----------|-----------------|
| **Q1** | Is this a command or reference data? | SKILL.md `name` + `description` frontmatter |
| **Q2** | Is this a hard rule or soft suggestion? | SKILL.md `Guardrails` section (G1-G5) |
| **Q3** | When is this information always needed vs context-dependent? | SKILL.md `progressive_disclosure` tiers |
| **Q4** | What is example vs criteria? | templates/design.md.template `required_sections` vs `references/examples/` |
| **Q5** | When conflict occurs, which takes priority? | SKILL.md `priority_order` in Pipeline Integration |

---

## 2. Format Requirements

Based on CLAUDE.md §3 format selection:

```yaml
format_rules:
  markdown:
    use_for:
      - explanation: "SKILL.md workflow description, rationale, Phase instructions"
      - walkthrough: "Boot sequence, Progressive writing contract"
      - overview: "Contributing components table, Pipeline integration"
    avoid_for:
      - hard_rules_without_schema: "Use YAML in Guardrails table instead"

  yaml:
    use_for:
      - constraints: "progressive_disclosure tiers, output_contract"
      - checklists: "Guardrails G1-G5, Quality Gate checklist"
      - routing: "pipeline stage_order, dependencies, successor_hints"
    avoid_for:
      - long_prose: "Phase 1/2/3 instructions stay in Markdown"

  xml_like_tags:
    use_for:
      - semantic_boundaries: "<instructions>, <context>, <examples> in Phase descriptions"
      - separating_input: "When user input wraps requirements"
    avoid_for:
      - excessive_micro_tagging: "Phase steps already have clear boundaries"
```

---

## 3. Token Budget

Based on CLAUDE.md §6 Layer Model:

```yaml
token_budget:
  L0_anchor_rules:
    limit: 350 tokens
    actual: "~280 tokens (SKILL.md frontmatter + core directives)"
    status: "✅ GOOD"
    split_when: ">400 tokens"

  L1_working_policy:
    limit: 1000 tokens
    actual: "~650 tokens (Guardrails + Workflow Phases + Contributing Components)"
    status: "✅ GOOD"
    split_when: ">1200 tokens"

  L2_domain_context:
    limit: 2500 tokens
    actual: "~400 tokens (architect.md referenced, not inlined)"
    status: "✅ GOOD"
    split_when: ">3000 tokens"

  root_guide_total:
    limit: 1800 tokens
    actual: "~1330 tokens (SKILL.md full)"
    status: "✅ EXCELLENT"
    split_when: ">2500 tokens"

  format_distribution:
    markdown_body: "~1100 tokens (65%)"
    yaml_frontmatter: "~150 tokens (9%)"
    tables: "~180 tokens (11%)"
    mermaid_diagrams: "~0 tokens (rendered separately)")
```

---

## 4. Quality Gates

Based on CLAUDE.md §12 Definition of Done + architure.md §4:

```yaml
quality_gates:
  source_fidelity:
    - name: "Pipeline Contract Preserved"
      check: "§3 Zone Mapping has specific filenames (no placeholders)"
      ref: "architure.md §4.1 Gate A item 1"
    - name: "Progressive Disclosure分层"
      check: "§7 distinguishes Tier 1 vs Tier 2 clearly"
      ref: "architure.md §4.1 Gate A item 2"
    - name: "Risk Coverage"
      check: "§8 has ≥3 risks with specific mitigations"
      ref: "architure.md §4.1 Gate A item 3"
    - name: "Open Questions Tracked"
      check: "§9 Open Questions resolved or explicitly flagged"
      ref: "architure.md §4.1 Gate A item 4"

  structure:
    - name: "10 Required Sections Present"
      check: "§1-§10 all populated after respective phases"
      ref: "SKILL.md §10 Output Specification table"
    - name: "Zone Mapping Contract Format"
      check: "Table has Zone | Files cần tạo | Nội dung | Bắt buộc?"
      ref: "SKILL.md §2 Zone Mapping Contract"
    - name: "Phase Gates Enforced"
      check: "Each phase ends with ⏸️ Gate waiting for user confirm"
      ref: "SKILL.md Phase 1/2/3 end states"

  agent_usability:
    - name: "Priority Order Defined"
      check: "Guardrails G1-G5 explicitly ordered by importance"
      ref: "SKILL.md Guardrails section"
    - name: "Must/MustNot Rules Clear"
      check: "G1 Design Only, G2 Gate Enforcement, G4 Zone Contract"
      ref: "SKILL.md Guardrails table"
    - name: "Loading Guidance Present"
      check: "progressive_disclosure tier1/tier2/tier3 paths specified"
      ref: "SKILL.md frontmatter"

  token_awareness:
    - name: "Root Guide Compact"
      check: "SKILL.md stays within L0+L1 token budget"
      ref: "CLAUDE.md §6 token_budget.root_guide_total"
    - name: "Domain Context On-Demand"
      check: "architect.md, visualization-guidelines.md in Tier 2"
      ref: "SKILL.md progressive_disclosure.tier2"

  handoff_readiness:
    - name: "Architect→Planner Contract"
      check: "§3 Zone Mapping + §7 PD Plan + §8 Risks ready for Planner"
      ref: "SKILL.md Pipeline Integration Handoff A→P"
    - name: "Quality Gate Passed"
      check: "loop/design-checklist.md all items pass before delivery"
      ref: "SKILL.md Quality Gate section"
```

---

## 5. Anti-Hallucination Rules

Based on CLAUDE.md §9 Semantic Activation Anchors + architure.md anti-hallucination:

```yaml
anti_hallucination:
  AH1_source_trace:
    description: "Every task MUST trace to source"
    implementation: 
      - "§3 Zone Mapping derived directly from Phase 2 analysis"
      - "§5 Execution Flow traces to Phase 2 Process pillar"
      - "Trace tag format: [TỪ DESIGN §N] in generated design.md"
    violation: "Task without [TỪ DESIGN §N] annotation"

  AH2_no_requirement_inflation:
    description: "Only decompose, don't add requirements"
    implementation:
      - "Skill ONLY designs, never implements (G1 Guardrail)"
      - "New domain knowledge requires user-provided resources"
      - "§9 Open Questions flags unverified assumptions"
    violation: "Adding features not in Problem Statement §1"

  AH3_no_knowledge_guessing:
    description: "Don't guess domain knowledge"
    implementation:
      - "Knowledge zone loaded only when referenced in Phase"
      - "visualization-guidelines.md read at Phase 3 start"
      - "architect.md framework knowledge pre-loaded at Boot"
    violation: "Writing UML rules without reading knowledge/architect.md"

  AH4_source_labeling:
    description: "Always label sources"
    implementation:
      - "[TỪ DESIGN §N] — from confirmed design.md"
      - "[GỢI Ý BỔ SUNG] — skill's suggestion, not in design"
      - "[CẦN LÀM RÕ] — requires user clarification"
    violation: "Unlabeled content appearing as fact"

  AH5_resource_verification:
    description: "Verify resources before completion"
    implementation:
      - "Boot checks for ../_shared/knowledge/framework.md existence"
      - "init_context.py creates scaffolding, not content"
      - "Quality Gate requires loop/design-checklist.md pass"
    violation: "Declaring complete without running checklist"

  architect_specific:
    - name: "Zone File Naming Contract"
      description: "§3 must have specific filenames, not placeholders"
      enforcement: "Planner relies on §3 for task creation"
    - name: "Phase Gate Enforcement"
      description: "Cannot skip user confirm between phases"
      enforcement: "G2: Gate Enforcement guardrail"
```

---

## 6. Zone Structure Compliance

Based on architure.md §2 Zones:

```yaml
zone_compliance:
  required_zones:
    core:
      path: "SKILL.md"
      status: "✅ Present - Persona, Phases, Guardrails"
      mandatory: true
      
    knowledge:
      path: "knowledge/architect.md"
      status: "✅ Present - Framework reference + workflow"
      mandatory: true
      shared: "references/_shared/knowledge/framework.md"
      
    loop:
      path: "loop/design-checklist.md"
      status: "✅ Present - Quality gate checklist"
      mandatory: true
      
  conditional_zones:
    scripts:
      path: "scripts/init_context.py"
      status: "✅ Present - Context initialization automation"
      loaded_when: "After Phase 1 confirm (Boot Sequence step 3)"
      
    templates:
      path: "templates/design.md.template"
      status: "✅ Present - 10-section output structure"
      loaded_when: "When writing design.md output (Phase 3)"
      
    data:
      path: "data/"
      status: "❌ Not required for architect skill"
      note: "Architect produces documents, not configs"
      
    assets:
      path: "assets/"
      status: "❌ Not required"
      note: "Mermaid diagrams rendered, not stored as images"

  tier_structure:
    tier1_mandatory:
      - "SKILL.md"
      - "knowledge/architect.md"
      - "../_shared/knowledge/framework.md"
    tier2_conditional:
      - "knowledge/visualization-guidelines.md"  # Phase 3
      - "scripts/init_context.py"               # After Phase 1
      - "loop/design-checklist.md"              # Before deliver
      - "templates/design.md.template"          # Phase 3 output
    tier3_optional:
      - "references/examples/design-*.md"       # On-demand reference
```

---

## 7. Workflow Compliance

Based on architure.md §3 5-Step Workflow:

```yaml
workflow_compliance:
  step1_research:
    status: "✅ Implemented as Phase 1: Collect"
    requirements_met:
      - "Pain Point identification"
      - "User & Context collection"
      - "Expected Output definition"
    gate: "Gate 1 - User confirm before Phase 2"

  step2_design:
    status: "✅ Implemented as Phase 2: Analyze"
    requirements_met:
      - "3 Pillars Analysis (Knowledge, Process, Guardrails)"
      - "7 Zones Mapping with Contract format"
      - "Risks Identification (≥3 risks)"
    gate: "Gate 2 - User confirm before Phase 3"

  step3_build:
    status: "✅ Implemented as Phase 3: Design & Output"
    requirements_met:
      - "Mermaid diagrams (D1 Folder Structure, D2 Execution Flow, D3 Workflow Phases)"
      - "Interaction Points definition"
      - "Progressive Disclosure Plan (Tier 1/2)"
      - "Open Questions compilation"
    gate: "Gate 3 - User confirm before writing design.md"

  step4_verify:
    status: "✅ Implemented as Quality Gate"
    requirements_met:
      - "loop/design-checklist.md mandatory check"
      - "All items pass before delivery"
      - "Handoff checklist verified"

  step5_maintenance:
    status: "✅ Covered in §12 Rollback Procedures"
    requirements_met:
      - "Phase rollback procedures defined"
      - "Emergency rollback procedure specified"

  interaction_points:
    mandatory_stops:
      - "After Phase 1: Gate 1 - Confirm Problem Statement"
      - "After Phase 2: Gate 2 - Confirm Capability Map & Zone Mapping"
      - "After Phase 3: Gate 3 - Confirm full design before writing"
      - "Before deliver: Quality Gate checklist pass"
    
    confidence_threshold:
      rule: "Confidence < 70% = must ask user"
      location: "Phase 1, Phase 2 guardrail"
```

---

## 8. Heavy Thinking Integration

Based on Heavy Thinking arXiv:2605.02396 K=8 chains:

```yaml
heavy_thinking:
  activation_condition:
    description: "When to use K=8 parallel reasoning chains"
    threshold: "Task difficulty <85% confidence"
    skill_specific_triggers:
      - "Phase 2: 3 Pillars Analysis - multiple valid decomposition paths"
      - "Phase 2: Zone Mapping - determining which zones required vs optional"
      - "Phase 3: §8 Risks - identifying AI blind spots"
      - "Phase 3: §9 Open Questions - surfacing implicit assumptions"

  K8_chain_allocation:
    pillar1_knowledge:
      chains: 2
      focus: "Domain knowledge requirements, knowledge/ folder structure"
    pillar2_process:
      chains: 3
      focus: "Workflow logic, phase ordering, interaction points"
    pillar3_guardrails:
      chains: 3
      focus: "AI failure modes, blind spots, verification needs"

  two_stage_processing:
    stage1_parallel:
      description: "8 independent reasoning chains executed simultaneously"
      chains:
        - "Chain 1: Analyze Pain Point depth"
        - "Chain 2: Identify User segments"
        - "Chain 3: Map to Knowledge Pillar"
        - "Chain 4: Map to Process Pillar"
        - "Chain 5: Map to Guardrails Pillar"
        - "Chain 6: Zone applicability analysis"
        - "Chain 7: Risk identification"
        - "Chain 8: Open question surfacing"
    stage2_deliberation:
      description: "Synthesize 8 chains into unified analysis"
      integration: "Select best from each chain, resolve conflicts"
      output: "Phase 2/3 deliverables"

  task_difficulty_routing:
    easy_mode:
      condition: "All 3 Pain Point answers clear, confidence >85%"
      approach: "Direct 3-phase workflow, skip K=8"
      example: "Simple API client skill with well-defined input/output"
    hard_mode:
      condition: "Ambiguous requirements, multiple valid interpretations"
      approach: "Activate K=8 chains for comprehensive analysis"
      example: "Multi-agent orchestration skill with unclear boundaries"
```

---

## 9. Pipeline Integration

Based on architure.md §4 Pipeline Flow:

```yaml
pipeline:
  stage_order: 1
  predecessor: null
  successor: "skill-planner"
  
  handoff_to_planner:
    required_sections:
      - "§2 Capability Map → Planner audit 3 Tiers"
      - "§3 Zone Mapping → Planner decompose into Tasks"
      - "§7 Progressive Disclosure → Planner/Tier 1/2 awareness"
      - "§8 Risks → Builder guardrails reference"
      
    gate_criteria:
      - "§3 Zone Mapping has specific filenames (no placeholders)"
      - "§7 Tier 1 vs Tier 2 clearly distinguished"
      - "§8 contains ≥3 risks with mitigations"
      - "§9 Open Questions resolved or flagged"

  context_directory:
    path: ".skill-context/{skill-name}/"
    created_by: "scripts/init_context.py"
    contents:
      - "design.md (Architect output)"
      - "todo.md (Planner output)"
      - "build-log.md (Builder evidence)"
      - "resources/ (User-provided docs)"
      - "loop/ (Quality checks)"
```

---

## 10. Definition of Done

```yaml
definition_of_done:
  skill_architect_complete_when:
    - "✅ SKILL.md exists with all required frontmatter"
    - "✅ knowledge/architect.md documents workflow"
    - "✅ ../_shared/knowledge/framework.md accessible"
    - "✅ templates/design.md.template defines 10-section structure"
    - "✅ loop/design-checklist.md provides quality gate"
    - "✅ scripts/init_context.py creates scaffolding"
    - "✅ All 3 Phases implemented with Gate enforcement"
    - "✅ Guardrails G1-G5 prevent scope creep"
    - "✅ Progressive Disclosure tier1/tier2/tier3 defined"
    - "✅ Anti-hallucination rules AH1-AH5 integrated"

  design_md_handoff_ready_when:
    - "✅ All 10 sections populated"
    - "✅ §3 Zone Mapping has specific filenames"
    - "✅ §7 Tier 1 vs Tier 2 distinguished"
    - "✅ §8 has ≥3 risks with mitigations"
    - "✅ §9 Open Questions resolved or flagged"
    - "✅ loop/design-checklist.md passed"
    - "✅ User confirmed final design"
```

---

## References

| Source | File | Key Contribution |
|--------|------|------------------|
| CLAUDE.md AI-First Standard | `/CLAUDE.md` | §3 Format, §6 Token Budget, §12 DoD, §9 Anti-hallucination |
| Heavy Thinking | `arXiv:2605.02396` | K=8 chains, 2-stage processing, task difficulty routing |
| architure.md | `/architure.md` | 3 Pillars, 7 Zones, 5-Step Workflow, Pipeline |
| framework.md | `../_shared/knowledge/framework.md` | Zone contract, naming conventions, version mgmt |
| SKILL.md | `./SKILL.md` | skill-architect implementation |
| architect.md | `./knowledge/architect.md` | Architect-specific workflow |

---

> **Spec Status**: ✅ Complete
> **Next**: skill-architect implementation follows this spec; skill-planner consumes design.md from architect output
