---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "example-skill"
generated_by: "skill-planner"
generated_at: "2026-05-03T11:00:00Z"
stage: "planner"
status: "ready_for_builder"
trace_to_design: "design.md"

phases:
  - id: "PH0"
    name: "PREPARE"
    tasks:
      - id: "T0.1"
        title: "Audit domain knowledge"
        zone: "knowledge"
        priority: "critical"
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        depends_on: []
        status: "done"
        file_target: "resources/domain.md"
        acceptance_criteria:
          - "File exists and content > 100 lines"

  - id: "PH1"
    name: "BUILD_CORE"
    tasks:
      - id: "T1.1"
        title: "Write SKILL.md"
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: "SKILL.md"
        acceptance_criteria:
          - "YAML frontmatter valid per design.schema.yaml"

blockers: []

prerequisites:
  - item: "Domain knowledge về example domain"
    tier: "domain"
    status: "ready"
    resource_file: "resources/domain.md"

handoff:
  next_stage: "builder"
  ready_condition:
    required:
      blockers_empty: true
      phase0_done: true
      prerequisites_ready: true
      schema_valid: true
      design_zones_covered: true
---
