# Completeness Checklist — Final Gate

> Run this check after Phase 4 (tasks.md) is approved. All items must pass.

---

## Checklist

### Artifact Presence

| # | Check | Expected | Error If Missing |
|---|-------|----------|------------------|
| C1 | api.json exists | File present | No api.json in spec folder |
| C2 | business.md exists | File present | No business.md in spec folder |
| C3 | flow.md exists | File present | No flow.md in spec folder |
| C4 | tasks.md exists | File present | No tasks.md in spec folder |

### Schema Version

| # | Check | Expected | Error If Wrong |
|---|-------|----------|----------------|
| S1 | api.json version | "2.0.0" | Wrong or missing spec_version |
| S2 | business.md version | Present in frontmatter or meta | Missing version |
| S3 | flow.md version | Present in frontmatter or meta | Missing version |
| S4 | tasks.md version | "2.0.0" | Wrong or missing spec_version |

### Required Sections (business.md)

| # | Section | Error If Missing |
|---|---------|------------------|
| BS1 | Overview | Missing ## 1. Overview |
| BS2 | Actors | Missing ## 2. Actors |
| BS3 | Entity Definitions | Missing ## 3. Entity Definitions |
| BS4 | Business Rules | Missing ## 5. Business Rules |
| BS5 | Permissions Matrix | Missing ## 8. Permissions Matrix |

### Required Diagrams (flow.md)

| # | Diagram Type | Minimum Required |
|---|-------------|-----------------|
| FD1 | Sequence Diagram | At least 1 |
| FD2 | Error Handling | At least 1 error flow |

### Phase Structure (tasks.md)

| # | Check | Requirement |
|---|-------|-------------|
| TP1 | Phase 1 present | phase_1 with at least 1 task |
| TP2 | Phase 2 present | phase_2 with at least 1 task |
| TP3 | Phase 4 present | phase_4 with at least 1 task |
| TP4 | Phase 3 skip check | phase_3 only if complexity != LOW |

### Trace Coverage

| # | Check | Requirement |
|---|-------|-------------|
| TC1 | All tasks have trace | 100% of tasks have trace field |
| TC2 | Trace format valid | Matches pattern P{phase}-T{phase}-{###} |
| TC3 | Trace references valid artifact | api.json, business.md, flow.md, or tasks.md |

### Complexity Consistency

| # | Check | Validation |
|---|-------|------------|
| CC1 | Entity count matches complexity | 1 entity → LOW, 2-3 → MEDIUM, 4+ → HIGH |
| CC2 | Phase structure matches complexity | LOW skips Phase 3, HIGH may split phases |
| CC3 | tasks.md complexity tag | Must match data/complexity-matrix.yaml criteria |

### Cross-Reference Integrity

| # | Check | Validation |
|---|-------|------------|
| CR1 | Entity names consistent | api.json ↔ business.md entity names match |
| CR2 | Actor names consistent | flow.md participants match business.md actors |
| CR3 | Status transitions consistent | flow.md state diagram matches business.md workflow |

---

## Output Format

```
## Completeness Gate Result

### Artifacts
- [x] api.json
- [x] business.md
- [x] flow.md
- [x] tasks.md

### Schema Versions
- [x] api.json: 2.0.0
- [x] business.md: present
- [x] flow.md: present
- [x] tasks.md: 2.0.0

### Required Sections (business.md)
- [x] Overview
- [x] Actors
- [x] Entity Definitions
- [x] Business Rules
- [x] Permissions Matrix

### Trace Coverage
- [x] 100% tasks have trace field
- [x] All trace formats valid
- [x] All traces reference valid artifacts

### Overall Result
[ ] PASS — spec folder is complete and ready for handoff
[ ] FAIL — N items failed, fix before handoff
```

---

## Failed Check Format

```yaml
failed_check:
  id: "TC1"
  check: "All tasks have trace"
  expected: "100% coverage"
  actual: "95% (1 task missing trace)"
  location: "tasks.md phase_2.tasks[3]"
  fix: "Add trace: 'P2-T2-004' to task T2-004"
```
