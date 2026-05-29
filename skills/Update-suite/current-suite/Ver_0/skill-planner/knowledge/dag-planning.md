# DAG Planning — Directed Acyclic Graph for Skill Build

> **Framework**: Planner's core knowledge for DAG construction
> **Purpose**: Convert blueprint Zone Mapping into executable task DAG

---

## 1. What is a DAG?

**DAG = Directed Acyclic Graph**

A task dependency graph where:
- **Nodes** = Tasks (T0.1, T1.2, etc.)
- **Edges** = Dependencies (Task A must complete before Task B)
- **Acyclic** = No cycles allowed (can't depend on yourself indirectly)

```
Valid DAG:          Invalid DAG (Cycle):
T0.1 → T1.1        T0.1 → T1.1
    ↘ T1.2             ↘ T1.1 → T0.1 (CYCLE!)
```

---

## 2. Why DAG for Skill Planning?

| Aspect | Without DAG | With DAG |
|--------|------------|----------|
| **Dependency** | Implicit, error-prone | Explicit, validated |
| **Parallelization** | Can't identify | Can run independent tasks |
| **Risk** | Hidden circular deps | Detected automatically |
| **Builder Experience** | Unclear ordering | Clear execution order |

---

## 3. DAG Construction Rules

### Rule 1: Identify Task Dependencies

Task A depends on Task B when:
1. **Output Dependency**: A needs output file from B
2. **Prerequisite Dependency**: A needs B's knowledge to execute
3. **Temporal Dependency**: A logically must happen after B

### Rule 2: Build Adjacency List

```yaml
task_dependencies:
  T1.1: []              # T1.1 has no dependencies
  T1.2: [T1.1]         # T1.2 depends on T1.1
  T2.1: [T1.1, T1.2]   # T2.1 depends on both
```

### Rule 3: Validate Acyclicity

Before outputting, run topological sort:
1. If all tasks can be ordered → Valid DAG
2. If cycle detected → Reject, fix dependencies

### Rule 4: Assign Priority by Blocking Power

A task is **Critical** if:
- It blocks 3+ other tasks
- It's on the critical path (longest sequence)

---

## 4. Phase Structure

### PH0: Resource Preparation
- Audit existing resources
- Create missing domain documents
- Prepare thin resources

### PH1: Core Implementation
- SKILL.md (L0 anchor)
- Core zone files

### PH2: Supporting Zones
- knowledge/
- loop/
- scripts/
- templates/

### PH3: Integration & Polish
- Validation scripts
- Final verification
- Documentation

---

## 5. Trace Tags for DAG

Every task MUST have a trace tag:

| Tag | Meaning | Example |
|-----|---------|---------|
| `[TỪ DESIGN §N]` | From blueprint section N | `[TỪ DESIGN §3.1]` |
| `[TỪ AUDIT TÀI NGUYÊN]` | Generated from resource gap | `[TỪ AUDIT TÀI NGUYÊN]` |
| `[GỢI Ý BỔ SUNG]` | Planner suggestion | `[GỢI Ý BỔ SUNG]` |
| `[CẦN LÀM RÕ]` | Needs clarification | `[CẦN LÀM RÕ]` |

---

## 6. DAG Validation Checklist

```yaml
dag_validation:
  structure:
    - task_dependencies is adjacency list (object)
    - all task_ids in dependencies exist in phases
    - no self-references (T1.1 cannot depend on T1.1)
    - no circular dependencies

  trace:
    - every task has trace tag
    - trace tag format is valid
    - trace references exist in blueprint

  readiness:
    - PH0 tasks generate resources for PH1+
    - critical path tasks identified
    - blockers tracked in array
```

---

## 7. Example: DAG for skill-architect

```json
{
  "phases": [
    {
      "phase_id": "PH0",
      "phase_name": "Resource Preparation",
      "tasks": [
        {
          "task_id": "T0.1",
          "description": "Audit existing resources and identify gaps",
          "priority": "critical",
          "zone": "knowledge"
        }
      ]
    },
    {
      "phase_id": "PH1",
      "phase_name": "Core Implementation",
      "tasks": [
        {
          "task_id": "T1.1",
          "description": "Create SKILL.md with 7-Zone structure",
          "priority": "critical",
          "zone": "core",
          "files": ["SKILL.md"],
          "dependencies": ["T0.1"]
        }
      ]
    }
  ],
  "task_dependencies": {
    "T1.1": ["T0.1"]
  }
}
```

---

## Key Takeaways

1. **DAG is the core output** — not a flat task list
2. **Adjacency list format** — `task_dependencies` object
3. **Validation is mandatory** — check for cycles before output
4. **Every task traces to blueprint** — no orphan tasks
5. **Phase structure enables parallelization** — PH0 before PH1+
