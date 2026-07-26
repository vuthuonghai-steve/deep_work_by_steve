# Thiết Kế Kiến Trúc Micro Skill Suite: `feature-spec-suite`

**Target Suite Name:** `feature-spec-suite`  
**Stage:** Stage 1 (Architect) + Stage 1.5 (Quality Gatekeeper)  
**Status:** `COMPLETED`  
**Quality Score:** 100% (PASS)  

```yaml
---
suite_architecture:
  suite_name: "feature-spec-suite"
  version: "1.0.0"
  scs_complexity_score: 0.85
  sub_skills:
    - name: "spec-elicitor-clarifier"
      steps_assigned: [1, 2, 3]
      responsibility: "Input Analysis, Requirements Normalization & Interactive Clarification"
    - name: "spec-architect-designer"
      steps_assigned: [4, 5]
      responsibility: "BA Use Cases Breakdown, Quantified NFRs & Mermaid Diagrams Architecture"
    - name: "spec-synthesizer-evaluator"
      steps_assigned: [6]
      responsibility: "Final Spec Synthesis, standards.md Format Compliance & Quality Gate Evaluation"
  execution_constraints:
    validation_timing: "END_OF_STEP"
    starter_validation_burden: 0.0
    storage_isolation_path: "Docs/Specs/{feature-name}/"
    mermaid_storage_path: "Docs/Specs/{feature-name}/diagrams/"
    quality_gate_threshold: 0.80
---
```

## 1. Phân rã Micro Skill Suite

Hệ thống `feature-spec-suite` được phân rã thành 3 Micro Skills:
1. `spec-elicitor-clarifier` (Steps 1, 2, 3)
2. `spec-architect-designer` (Steps 4, 5)
3. `spec-synthesizer-evaluator` (Step 6)

## 2. Dynamic Depth Signals & Anchors
- **S1 Negation Density**: Cấm starter validation burden, cấm ghi file ngoài `Docs/Specs/{feature-name}/`, cấm unquoted Mermaid labels.
- **S2 Reverse Questioning**: 300s timeout fallback tại Step 3.
- **S3 Multi-Stakeholder**: Developer, PM, Architect, LLM Executor views.
- **S4 Constraint Anchoring**: End-of-step validation gates, hardcoded output paths.
