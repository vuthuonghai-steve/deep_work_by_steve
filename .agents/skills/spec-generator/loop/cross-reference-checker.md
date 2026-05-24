# Cross-Reference Checker

> Validate consistency between artifacts. Run after Phase 2 (business.md) is approved.

---

## Validation Rules Summary

### Category A: api.json ↔ business.md

| Rule | Description | Check Method |
|------|-------------|--------------|
| A1 | Entity name match | Compare api.json entities[].name vs business.md entity_definitions[].name |
| A2 | Collection slug match | Compare api.json entities[].collection vs business.md entity_definitions[].collection |
| A3 | Field presence | Every field in business.md must exist in api.json |
| A4 | Field type match | Field type in business.md must match api.json field type |
| A5 | Endpoint ↔ Permissions | Endpoint auth must match permissions matrix in business.md |
| A6 | Status ↔ Actions | Status transitions must map to endpoint actions |
| A7 | Actor ↔ Auth | Every actor in business.md must have auth in api.json |

### Category B: business.md ↔ flow.md

| Rule | Description | Check Method |
|------|-------------|--------------|
| B1 | Actor naming | Participant names in flow diagrams must match Actor table exactly |
| B2 | Status transitions | stateDiagram transitions must match Status Workflow table |
| B3 | Sequence steps | Steps must reflect Business Rules (BR-### references) |
| B4 | Entity reference | Data flow entities must match Entity Definitions |
| B5 | Edge case coverage | Error flows must cover Edge Cases in business.md |

### Category C: flow.md ↔ tasks.md

| Rule | Description | Check Method |
|------|-------------|--------------|
| C1 | Phase coverage | Every diagram section must have corresponding task |
| C2 | Actor assignment | Actors in diagrams must be assigned in tasks |
| C3 | Trace field presence | Every task must have trace field |
| C4 | Artifact section ref | Trace must reference specific section |

---

## Validation Process

### Step 1: Load Artifacts
```
1. Read api.json
2. Read business.md
3. Read flow.md
4. Read tasks.md
```

### Step 2: Run Category A Checks
```
For each entity in business.md:
  - Match to api.json entity by name
  - Verify collection slug matches
  - For each field in business.md:
    - Find field in api.json
    - Verify type matches
  - If any mismatch → FAIL

For each actor in business.md:
  - Find corresponding auth config in api.json
  - If not found → FAIL
```

### Step 3: Run Category B Checks
```
For each participant in flow.md sequence diagrams:
  - Match to Actors table in business.md
  - If name differs → FAIL

For each state transition in flow.md state diagrams:
  - Match to Status Workflow in business.md
  - If transition not in workflow → FAIL
```

### Step 4: Run Category C Checks
```
For each section in flow.md:
  - Find corresponding task in tasks.md
  - If not found → FAIL

For each task in tasks.md:
  - If trace field missing → FAIL
  - If trace doesn't reference valid artifact → FAIL
```

---

## Output Format

```
## Cross-Reference Validation Result

### Category A: api.json ↔ business.md
| Rule | Status | Details |
|------|--------|---------|
| A1 | PASS/FAIL | ... |
| A2 | PASS/FAIL | ... |

### Category B: business.md ↔ flow.md
| Rule | Status | Details |
|------|--------|---------|
| B1 | PASS/FAIL | ... |
| B2 | PASS/FAIL | ... |

### Category C: flow.md ↔ tasks.md
| Rule | Status | Details |
|------|--------|---------|
| C1 | PASS/FAIL | ... |
| C3 | PASS/FAIL | ... |

### Overall Result
[ ] PASS — all checks passed, proceed to next phase
[ ] FAIL — N checks failed, fix errors before proceeding
```

---

## Error Details Format

For each failure, report:
```yaml
error:
  category: "A|B|C"
  rule_id: "A1"
  message: "Entity 'User' in business.md does not match api.json"
  location:
    artifact: "business.md"
    section: "entity_definitions[0].name"
    expected: "User"
    actual: "Users"
  suggestion: "Rename entity in business.md to 'User' to match api.json"
```
