# AI Prompts — Structured Prompts Per Phase

> Templates for generating each artifact. Replace `<...>` placeholders.

---

## Phase 0: Ambiguity Detection Prompt

```
You are an ambiguity detector for feature specifications.

Analyze the following feature request for vagueness, undefined terms, or missing information:

---
<USER REQUEST>
---

Check for:
1. Undefined actors (who performs actions?)
2. Missing data fields (what data is needed?)
3. Unclear auth requirements (who can access?)
4. Unspecified edge cases (what happens when X?)
5. Missing relationships (how do entities connect?)
6. Ambiguous business rules (what triggers what?)

If ambiguity found:
- List each ambiguity with specific location in the request
- Generate clarifying questions from templates/clarity-questions.yaml
- Do NOT make assumptions to fill gaps

If context is sufficient:
- Confirm with: "Context sufficient for Phase 1. Proceeding to api.json generation."
```

---

## Phase 1: api.json Generation Prompt

```
Generate a backend API specification (api.json) for the following feature:

---
<FEATURE REQUEST>
<CLARIFIED CONTEXT from Phase 0>
---

Requirements:
1. Follow templates/api-json.schema.yaml exactly
2. Include all required fields: spec_version, feature, engine, entities, endpoints
3. For PayloadCMS: use collection field types (text, number, relationship, etc.)
4. Define endpoints for all CRUD operations needed
5. Specify auth for each endpoint (public, authenticated, admin)
6. Include response schemas for 200, 400, 401, 403
7. Add trace field to each endpoint: "P1-<endpoint-name>"

Output format: Valid JSON matching api-json.schema.yaml
```

---

## Phase 2: business.md Generation Prompt

```
Generate a business rules document (business.md) for the following feature:

---
<FEATURE REQUEST>
<API.JSON from Phase 1>
---

Requirements:
1. Follow templates/business-md.schema.yaml section structure
2. Include all required sections: Overview, Actors, Entity Definitions, Business Rules, Permissions Matrix
3. Define actors matching the auth in api.json
4. List business rules with format:
   - Rule ID (BR-001, BR-002, ...)
   - Condition, Action, Actor
   - Trace to api.json section
5. Define status workflow table
6. List all edge cases from the feature request
7. Cross-reference all entities and endpoints with api.json

Output format: Markdown following business-md.schema.yaml
```

---

## Phase 3: flow.md Generation Prompt

```
Generate Mermaid flow diagrams (flow.md) for the following feature:

---
<FEATURE REQUEST>
<API.JSON from Phase 1>
<BUSINESS.MD from Phase 2>
<COMPLEXITY: LOW|MEDIUM|HIGH>
---

Requirements:
1. Follow templates/flow-md.schema.yaml structure
2. Include sequence diagram showing actor interactions
3. Include activity diagram for main workflow
4. Include state diagram for entity status transitions
5. Include data flow diagram showing input→process→storage
6. Include error handling flow for all edge cases
7. Actor names must match Actors table in business.md EXACTLY
8. Status transitions must match Status Workflow in business.md EXACTLY
9. All endpoints referenced must exist in api.json

Complexity adaptation:
- LOW: 1 sequence + 1 activity + minimal error flow
- MEDIUM: 2-3 diagrams covering all sub-flows
- HIGH: Multiple diagrams per entity + sub-phase splitting

Output format: Markdown with Mermaid code blocks
```

---

## Phase 4: tasks.md Generation Prompt

```
Generate implementation task list (tasks.md) for the following feature:

---
<FEATURE REQUEST>
<API.JSON from Phase 1>
<BUSINESS.MD from Phase 2>
<FLOW.MD from Phase 3>
<COMPLEXITY: LOW|MEDIUM|HIGH>
---

Requirements:
1. Follow templates/tasks-md.schema.yaml structure
2. Create phases matching complexity adaptation:
   - LOW: Phase 1 (Backend) → Phase 2 (Business) → Phase 4 (Testing) [skip Phase 3]
   - MEDIUM: Phase 1 → Phase 2 → Phase 3 → Phase 4
   - HIGH: Phase 1 → Phase 2 → Phase 3 → Phase 4 + sub-phases
3. Every task MUST have:
   - id: "T{phase}-###" format
   - title: Clear action title
   - artifact: Which spec artifact it implements
   - artifact_section: Specific section reference
   - trace: "{Phase}-{TaskID}" format (e.g., "P1-T1-001")
   - dependencies: List of prerequisite task IDs
   - estimated_hours: Realistic estimate
   - acceptance_criteria: At least 2 criteria per task
4. Map every diagram in flow.md to at least one task
5. Ensure 100% trace coverage (every task traced to source)

Output format: YAML following tasks-md.schema.yaml
```

---

## Phase 5: Completeness Gate Prompt

```
Run completeness validation for the following spec folder:

---
<SPEC-FOLDER-PATH>
---

Run all validation checks in order:
1. All 4 artifacts present (api.json, business.md, flow.md, tasks.md)
2. Required sections in each markdown artifact
3. Schema version = "2.0.0" in all artifacts
4. Trace coverage = 100% in tasks.md
5. Cross-reference consistency:
   - api.json ↔ business.md (Category A rules)
   - business.md ↔ flow.md (Category B rules)
   - flow.md ↔ tasks.md (Category C rules)
6. Complexity matches complexity-matrix.yaml criteria

If ALL checks pass:
- Generate spec-meta.yaml
- Generate build-log.md with evidence
- Signal handoff.ready

If any check fails:
- Report which rule failed
- Do NOT complete handoff
```

---

## Template Selection Prompt

```
Select appropriate templates based on feature type:

---
<FEATURE REQUEST>
---

Feature type detection:
- E-commerce (orders, payments, carts) → standard templates
- User management (auth, profiles, roles) → auth-enhanced templates
- Content management (CRUD, media) → lightweight templates
- Real-time (websockets, notifications) → real-time templates

Apply selected template set to Phase 1-4 prompts.
```
