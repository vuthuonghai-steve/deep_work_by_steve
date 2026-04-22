# Pipeline Configuration — pipeline.yaml Schema

> Source: arc-1.md §3.1

---

## Overview

`pipeline.yaml` is the single source of truth for pipeline ORDER. It defines stages, dependencies, and validation criteria.

## Schema

```yaml
pipeline_name: string          # Unique identifier for pipeline
project: string               # Project name (e.g., "life-2")
version: string               # Pipeline version (e.g., "1.0")

stages:
  - id: string               # Unique stage ID (e.g., "stage_01")
    skill: string             # Skill name to invoke
    depends_on: [string]     # Array of stage IDs this depends on
    checkpoint: boolean       # Pause for user review after this stage
    completion_criteria:
      required_outputs:       # List of expected output files
        - string
      validation_script: string   # Script to run for validation
      lint_exit_code: integer      # Expected exit code (usually 0)
```

## Example

```yaml
pipeline_name: uml-documentation
project: life-2
version: "1.0"

stages:
  - id: stage_01
    skill: flow-design-analyst
    depends_on: []
    checkpoint: false
    completion_criteria:
      required_outputs:
        - "Docs/life-2/diagrams/flow/index.md"
      validation_script: "scripts/flow_lint.py"
      lint_exit_code: 0

  - id: stage_02
    skill: sequence-design-analyst
    depends_on: [stage_01]
    checkpoint: true
    completion_criteria:
      required_outputs:
        - "Docs/life-2/diagrams/sequence/index.md"
      validation_script: "scripts/validate_syntax.py"
      lint_exit_code: 0
```

## Variable Resolution

Pipeline runner supports `{}` placeholders:

| Variable | Example | Description |
|----------|---------|-------------|
| `{pipeline_name}` | uml-documentation | Current pipeline name |
| `{project}` | life-2 | Project identifier |
| `{input_base}` | Docs/life-1/ | Base input directory |
| `{output_base}` | Docs/life-2/ | Base output directory |
| `{stage_id}` | stage_01 | Current stage ID |

## Design Principles

1. **Separation of Concerns**:
   - `pipeline.yaml` → controls ORDER
   - `SKILL.md` → controls CONTRACT

2. **DAG-Ready**: Dependencies form a DAG (Directed Acyclic Graph). Parallel execution can be added in v2+.

3. **Checkpoint**: Set `checkpoint: true` to pause after a stage for user review.
