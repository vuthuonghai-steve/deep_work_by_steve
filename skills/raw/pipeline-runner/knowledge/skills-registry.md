# Skills Registry — skills.yaml Format

> Source: arc-1.md §3.3, pipeline-commands.md

---

## Overview

Skills registry provides metadata about available skills. Pipeline runner queries this to validate skill existence and get skill contracts.

## skills.yaml Schema

```yaml
skills:
  - name: string              # Skill name (kebab-case)
    description: string        # What the skill does
    path: string             # Path to SKILL.md
    input_contract:           # What this skill expects
      - type: file|directory
        path: string
        required: boolean
    output_contract:          # What this skill produces
      - type: file|directory
        path: string
        format: string
```

## Example

```yaml
skills:
  - name: flow-design-analyst
    description: Analyzes requirements and generates flow diagrams
    path: .claude/skills/flow-design-analyst/SKILL.md
    input_contract:
      - type: file
        path: Docs/life-2/specs/requirements.md
        required: true
    output_contract:
      - type: directory
        path: Docs/life-2/diagrams/flow/
        format: markdown

  - name: sequence-design-analyst
    description: Generates UML sequence diagrams
    path: .claude/skills/sequence-design-analyst/SKILL.md
    input_contract:
      - type: directory
        path: Docs/life-2/diagrams/flow/
        required: true
    output_contract:
      - type: directory
        path: Docs/life-2/diagrams/sequence/
        format: markdown
```

## Query Methods

### Find Skill by Name

```python
def find_skill(skills_yaml, skill_name):
    for skill in skills_yaml.get('skills', []):
        if skill['name'] == skill_name:
            return skill
    return None
```

### Validate Skill Exists

```python
def validate_skill_exists(skills_yaml, skill_name):
    skill = find_skill(skills_yaml, skill_name)
    if not skill:
        raise SkillNotFoundError(f"Skill '{skill_name}' not found")
    return skill
```

### Get Skill Contract

```python
def get_skill_contract(skills_yaml, skill_name):
    skill = find_skill(skills_yaml, skill_name)
    return {
        'input': skill.get('input_contract', []),
        'output': skill.get('output_contract', [])
    }
```

## Skill Path Resolution

Pipeline runner searches in order:

1. `.claude/skills/{skill_name}/SKILL.md`
2. `.agent/skills/{skill_name}/SKILL.md`
3. `.codex/skills/{skill_name}/SKILL.md`
