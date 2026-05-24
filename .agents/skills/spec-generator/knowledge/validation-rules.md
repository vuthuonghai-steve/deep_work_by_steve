# Validation Rules — Cross-Reference Checks

> Rules for validating consistency between spec artifacts

---

## Rule Categories

### Category A: api.json → business.md Cross-Checks

| Rule ID | Check | Error If |
|---------|-------|----------|
| **A1** | Entity name match | Entity name in api.json != entity name in business.md |
| **A2** | Collection slug match | Collection slug differs between api.json and business.md |
| **A3** | Field presence | Every field in business.md entity must exist in api.json entity |
| **A4** | Field type match | Field type in business.md must match api.json field type |
| **A5** | Endpoint ↔ Permissions | Endpoint auth must match permissions in business.md |
| **A6** | Status ↔ Actions | Status transitions in business.md must map to endpoint actions |
| **A7** | Actor ↔ Auth | Every actor in business.md must have corresponding auth in api.json |

### Category B: business.md → flow.md Consistency

| Rule ID | Check | Error If |
|---------|-------|----------|
| **B1** | Actor naming | Actor name in flow diagrams must match Actor table in business.md |
| **B2** | Status transitions | State diagram transitions must match Status Workflow in business.md |
| **B3** | Sequence steps | Sequence diagram steps must reflect Business Rules in business.md |
| **B4** | Entity reference | Data flow must show entities matching Entity Definitions in business.md |
| **B5** | Edge case coverage | Edge cases listed in business.md must be represented in flow error handling |

### Category C: flow.md → tasks.md Mapping

| Rule ID | Check | Error If |
|---------|-------|----------|
| **C1** | Phase coverage | Every diagram section in flow.md must have corresponding tasks |
| **C2** | Actor → Task assignment | Actors in flow.md must be assigned in tasks |
| **C3** | Trace field presence | Every task must have `trace` field referencing source artifact |
| **C4** | Artifact section ref | Trace must include specific artifact section (e.g., P1, B2, F3) |

### Category D: Completeness Gates

| Rule ID | Check | Error If |
|---------|-------|----------|
| **D1** | All 4 artifacts present | Any artifact missing from spec folder |
| **D2** | Required sections | Required sections missing from any markdown artifact |
| **D3** | Schema version | spec_version missing or not "2.0.0" |
| **D4** | Trace coverage | Any task missing `trace` field |
| **D5** | Complexity consistency | Complexity tag must match complexity-matrix criteria |

---

## Validation Pipeline

### Phase 1 → Phase 2 Gate (api.json → business.md)

```
api.json validated OK
        │
        ▼
Run Category A rules (A1-A7)
        │
    ┌───┴───┐
    ▼       ▼
  PASS    FAIL
    │       │
    ▼       ▼
Proceed   Return errors:
to P2     - List A-rule failures
          - Highlight mismatch locations
```

### Phase 2 → Phase 3 Gate (business.md → flow.md)

```
business.md validated OK
        │
        ▼
Run Category B rules (B1-B5)
        │
    ┌───┴───┐
    ▼       ▼
  PASS    FAIL
    │       │
    ▼       ▼
Proceed   Return errors:
to P3     - List B-rule failures
          - Show diagram section mismatch
```

### Phase 3 → Phase 4 Gate (flow.md → tasks.md)

```
flow.md validated OK
        │
        ▼
Run Category C rules (C1-C4)
        │
    ┌───┴───┐
    ▼       ▼
  PASS    FAIL
    │       │
    ▼       ▼
Proceed   Return errors:
to P4     - List C-rule failures
          - Show missing trace fields
```

### Phase 4 → Phase 5 Gate (Final Completeness)

```
tasks.md validated OK
        │
        ▼
Run Category D rules (D1-D5)
        │
    ┌───┴───┐
    ▼       ▼
  PASS    FAIL
    │       │
    ▼       ▼
Complete  Return errors:
spec      - List D-rule failures
folder    - Block handoff to skill-builder
```

---

## Error Message Format

```yaml
validation_error:
  phase: <phase-number>
  category: <A|B|C|D>
  rule_id: "<Rule-ID>"
  message: "<human-readable error>"
  location:
    artifact: "<artifact-name>"
    section: "<section or line>"
    expected: "<expected value>"
    actual: "<actual value>"
  suggestion: "<how to fix>"
```

---

## Validation Checklist Per Phase

### Phase 1 Complete (api.json)
- [ ] JSON Schema validation passes
- [ ] All required fields present
- [ ] Every entity has at least one endpoint
- [ ] Auth configuration is complete
- [ ] Response schemas defined for all endpoints

### Phase 2 Complete (business.md)
- [ ] All Category A rules pass (A1-A7)
- [ ] Actors table complete
- [ ] Business Rules numbered and traceable
- [ ] Permissions Matrix complete
- [ ] Edge cases listed

### Phase 3 Complete (flow.md)
- [ ] All Category B rules pass (B1-B5)
- [ ] Sequence diagrams consistent with business rules
- [ ] State diagrams match status workflow
- [ ] Error handling flows cover edge cases

### Phase 4 Complete (tasks.md)
- [ ] All Category C rules pass (C1-C4)
- [ ] Trace coverage = 100%
- [ ] Complexity matches matrix criteria
- [ ] Phase structure matches complexity adaptation

### Phase 5 Complete (Final)
- [ ] All Category D rules pass (D1-D5)
- [ ] build-log.md created with evidence
- [ ] spec-meta.yaml complete
- [ ] handoff.ready signal set
