# Spec Generator v2.0.0 — Implementation Todo

> **Trace**: Design §1-12 → Tasks  
> **Status**: Ready for Implementation  
> **Last Updated**: 2026-05-07

---

## 1. Pre-requisites

### 1.1 Knowledge Requirements

| # | Knowledge | Source | Priority |
|---|-----------|--------|----------|
| P1 | PayloadCMS 3.x spec-generation patterns | Project experience | Required |
| P2 | JSON Schema YAML structure | `templates/*.schema.yaml` | Required |
| P3 | Mermaid diagram syntax (flow.md) | `knowledge/spec-structure.md` | Required |
| P4 | Phase-gate validation patterns | `data/phase-gates.yaml` | Required |
| P5 | Ambiguity detection techniques | `loop/ambiguity-detector.md` | Required |

### 1.2 External Dependencies

| # | Dependency | Purpose | Blocker |
|---|------------|---------|---------|
| D1 | skill-builder skill | Handoff target | Yes |
| D2 | Python 3.x (for scripts) | validate-spec.py, check-consistency.py | Yes |
| D3 | Existing spec-generator-v1 | Migration reference | No |

---

## 2. Phase Breakdown

### Phase 0: Parallel Development Setup
**Objective**: Prepare v2 alongside v1 without disruption

- [ ] **P0-T1**: Create `skills/spec-generator/` directory structure  
  **Trace**: [TỪ DESIGN §10]  
  **Priority**: Critical

- [ ] **P0-T2**: Create `skills/spec-generator-v1/legacy/` for v1 backup  
  **Trace**: [TỪ DESIGN §10 Phase 0]  
  **Priority**: High

---

### Phase 1: Core Zone Implementation
**Objective**: Create SKILL.md with 5-phase workflow and persona

- [ ] **P1-T1**: Create `SKILL.md` with AI-first persona definition  
  **Trace**: [TỪ DESIGN §2 Pillar 1], [TỪ DESIGN §3 Core Zone]  
  **Priority**: Critical | **Blocks**: P2, P3, P4

- [ ] **P1-T2**: Define 5-phase workflow in SKILL.md  
  **Trace**: [TỪ DESIGN §2 PROCESS table]  
  **Priority**: Critical

- [ ] **P1-T3**: Define guardrails section in SKILL.md  
  **Trace**: [TỪ DESIGN §2 GUARDRAILS]  
  **Priority**: Critical

- [ ] **P1-T4**: Define progressive disclosure tiers (Tier 1/2/3) in SKILL.md  
  **Trace**: [TỪ DESIGN §7]  
  **Priority**: High

---

### Phase 2: Knowledge Zone Implementation
**Objective**: Create 3 knowledge files for spec anatomy and validation

- [ ] **P2-T1**: Create `knowledge/spec-structure.md` with complete spec anatomy  
  **Trace**: [TỪ DESIGN §3 Knowledge Zone], [TỪ DESIGN §11 Output Spec]  
  **Priority**: Critical | **Blocks**: P3-T2, P4-T1  
  **Content**:  
  - api.json schema anatomy  
  - business.md section structure  
  - flow.md diagram requirements  
  - tasks.md phase template  
  - spec-meta.yaml metadata

- [ ] **P2-T2**: Create `knowledge/validation-rules.md` with cross-reference rules  
  **Trace**: [TỪ DESIGN §3 Knowledge Zone], [TỪ DESIGN §4.2 Validation Pipeline]  
  **Priority**: Critical | **Blocks**: P3-T2  
  **Content**:  
  - api.json → business.md cross-check  
  - business.md → flow.md consistency  
  - flow.md → tasks.md mapping rules

- [ ] **P2-T3**: Create `knowledge/ai-prompts.md` with structured prompts per phase  
  **Trace**: [TỪ DESIGN §3 Knowledge Zone]  
  **Priority**: High | **Blocks**: P4-T1  
  **Content**:  
  - Phase 0: Ambiguity detection prompt  
  - Phase 1: api.json generation prompt  
  - Phase 2: business.md generation prompt  
  - Phase 3: flow.md generation prompt  
  - Phase 4: tasks.md generation prompt

---

### Phase 3: Validation Infrastructure
**Objective**: Create templates and loop files for validation gates

- [ ] **P3-T1**: Create `templates/api-json.schema.yaml` (JSON Schema v2.0.0)  
  **Trace**: [TỪ DESIGN §3 Templates Zone], [TỪ DESIGN §11 Appendix B]  
  **Priority**: Critical | **Blocks**: P4-T2

- [ ] **P3-T2**: Create `templates/business-md.schema.yaml`  
  **Trace**: [TỪ DESIGN §3 Templates Zone]  
  **Priority**: Critical

- [ ] **P3-T3**: Create `templates/flow-md.schema.yaml`  
  **Trace**: [TỪ DESIGN §3 Templates Zone]  
  **Priority**: Critical

- [ ] **P3-T4**: Create `templates/tasks-md.schema.yaml` with trace field requirement  
  **Trace**: [TỪ DESIGN §4.2 Validation Pipeline], [TỪ DESIGN §8 R4]  
  **Priority**: Critical

- [ ] **P3-T5**: Create `templates/clarity-questions.yaml`  
  **Trace**: [TỪ DESIGN §3 Templates Zone], [TỪ DESIGN §4.1]  
  **Priority**: High

- [ ] **P3-T6**: Create `loop/ambiguity-detector.md`  
  **Trace**: [TỪ DESIGN §2 GUARDRAILS], [TỪ DESIGN §4.1]  
  **Priority**: Critical | **Blocks**: P4-T1

- [ ] **P3-T7**: Create `loop/cross-reference-checker.md`  
  **Trace**: [TỪ DESIGN §2 GUARDRAILS], [TỪ DESIGN §4.2]  
  **Priority**: Critical

- [ ] **P3-T8**: Create `loop/completeness-checklist.md`  
  **Trace**: [TỪ DESIGN §2 GUARDRAILS]  
  **Priority**: High

---

### Phase 4: Scripts & Automation
**Objective**: Create Python validation scripts

- [ ] **P4-T1**: Create `scripts/validate-spec.py`  
  **Trace**: [TỪ DESIGN §3 Scripts Zone], [TỪ DESIGN §4.2]  
  **Priority**: High | **Blocks**: P5-T1  
  **Features**:  
  - Schema validation for all 4 artifacts  
  - Required field checks  
  - Trace field coverage check

- [ ] **P4-T2**: Create `scripts/check-consistency.py`  
  **Trace**: [TỪ DESIGN §3 Scripts Zone], [TỪ DESIGN §5.3]  
  **Priority**: High  
  **Features**:  
  - Cross-artifact consistency verification  
  - api.json ↔ business.md consistency  
  - flow.md ↔ business.md consistency  
  - tasks.md trace coverage

---

### Phase 5: Data Zone & Migration
**Objective**: Complete data files and deprecate v1

- [ ] **P5-T1**: Create `data/phase-gates.yaml`  
  **Trace**: [TỪ DESIGN §3 Data Zone], [TỪ DESIGN §2 PROCESS]  
  **Priority**: High

- [ ] **P5-T2**: Create `data/complexity-matrix.yaml`  
  **Trace**: [TỪ DESIGN §3 Data Zone], [TỪ DESIGN §4.3]  
  **Priority**: High

- [ ] **P5-T3**: Move v1 to `skills/spec-generator-v1/legacy/`  
  **Trace**: [TỪ DESIGN §10 Phase 4]  
  **Priority**: Medium

- [ ] **P5-T4**: Promote v2 to `skills/spec-generator/`  
  **Trace**: [TỪ DESIGN §10 Phase 4]  
  **Priority**: Medium

---

## 3. Knowledge & Resources Needed

### 3.1 Reference Materials

| # | Resource | Purpose | Location |
|---|----------|---------|----------|
| R1 | v1 spec-generator implementation | Migration reference | `skills/spec-generator/` (existing) |
| R2 | JSON Schema specification | Template authoring | External |
| R3 | Mermaid diagram guide | flow.md authoring | External |
| R4 | skill-builder interface spec | Handoff protocol | `.skill-context/skill-builder/` |
| R5 | build-log.md format | Handoff evidence | From skill-builder design |

### 3.2 Skill Context Dependencies

| # | Dependency | Purpose |
|---|------------|---------|
| S1 | `spec-generator` (existing v1) | Compare/contrast v1 features |
| S2 | `skill-builder` skill | Handoff target |
| S3 | `skill-architect` skill | Design consultation |

---

## 4. Definition of Done

### 4.1 Core Deliverables

- [ ] **SKILL.md** loads and defines 5-phase workflow correctly
- [ ] All 5 template schemas validate against JSON Schema standard
- [ ] `knowledge/spec-structure.md` covers all 5 artifacts completely
- [ ] `knowledge/validation-rules.md` defines all cross-reference checks
- [ ] `loop/ambiguity-detector.md` catches ≥90% of vague requests (design target)

### 4.2 Validation Gates

- [ ] **Phase 0 gate**: Ambiguity detection runs before any generation
- [ ] **Phase 1 gate**: api.json passes schema validation
- [ ] **Phase 2 gate**: business.md passes cross-reference check
- [ ] **Phase 3 gate**: flow.md passes diagram consistency check
- [ ] **Phase 4 gate**: tasks.md passes completeness check with trace coverage

### 4.3 Integration Points

- [ ] Handoff to skill-builder produces `build-log.md` with validation evidence
- [ ] Complexity adaptation works for Low/Medium/High features
- [ ] Progressive disclosure loads Tier 1 → Tier 2 → Tier 3 correctly

### 4.4 Success Metrics (from design)

| Metric | Target | Verification |
|--------|--------|--------------|
| Ambiguity Detection Rate | ≥90% | User feedback survey |
| Cross-Artifact Consistency | 100% | Automated validation gate |
| Trace Coverage | 100% tasks have trace field | Schema validation |
| skill-builder Satisfaction | ≥80% | Builder feedback |

---

## 5. Notes

### 5.1 Open Questions (from design)

| # | Question | Recommendation | Priority |
|---|----------|----------------|----------|
| Q1 | Create folder directly or return for confirmation? | Create folder only after Phase 1 validation | HIGH |
| Q2 | How to handle backend TBD features? | Use `engine: TBD` pattern, defer validation gate | MEDIUM |
| Q3 | Support incremental spec updates? | Full regeneration (no merge logic) | LOW |
| Q4 | Version output spec folder? | No versioning in folder name, changelog in build-log.md | LOW |

### 5.2 Risks & Mitigations

| # | Risk | Mitigation | Severity |
|---|------|------------|----------|
| R1 | User provides vague requirements | Phase 0 ambiguity detector MUST run before any generation | HIGH |
| R2 | AI generates inconsistent cross-artifacts | Mandatory cross-reference gate between Phase 2→3 | HIGH |
| R3 | Complexity mis-assessment | User can override complexity tag in tasks.md | MEDIUM |
| R4 | skill-builder cannot trace task→code | Every task MUST have `trace` field | MEDIUM |
| R5 | Schema evolution | Version each template schema, maintain changelog | LOW |
| R6 | Over-engineering for simple features | Skip logic for Low complexity features | MEDIUM |

### 5.3 Implementation Hints

- **5 conversion questions** per Zone (from design §1):
  1. KNOWLEDGE: What does the AI need to know vs. assume?
  2. PROCESS: What triggers each phase? What validates the output?
  3. GUARDRAILS: When should the AI STOP and ask?

- **Trace tag format**: `[TỪ DESIGN §N]` for design citations, `[GỢI Ý BỔ SUNG]` for implementation notes

---

## 6. Builder Feedback Integration

### 6.1 Handoff Checklist (for skill-builder)

| # | Item | Expected Output |
|---|------|-----------------|
| H1 | Signal | `handoff.ready` |
| H2 | Content | All 4 artifacts in `spec-<feature>/` |
| H3 | Evidence | `build-log.md` with validation passes |
| H4 | Schema version | `spec_schema_version: "2.0.0"` |
| H5 | Trace coverage | 100% tasks have `trace` field |

### 6.2 Builder Feedback Loop

| # | Feedback | Action |
|---|----------|--------|
| B1 | skill-builder starts without questions | Target: ≥80% |
| B2 | User confirms Phase 1-4 without major changes | Target: ≥70% |
| B3 | Trace field coverage | Must be 100% per schema |

### 6.3 Post-Implementation Review

- [ ] Review with skill-builder on first handoff
- [ ] Collect ambiguity detection rate feedback
- [ ] Measure cross-artifact consistency pass rate
- [ ] Iterate on clarifying questions templates based on Q1-Q4

---

**End of Todo**
