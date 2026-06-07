---
name: markdown-fixer
description: Fixes Markdown structure issues like heading hierarchy and list indentation. Use when processing Markdown files that need structural normalization.
version: "1.0.0"
pipeline:
  stage_order: 3
  input_contract:
    - type: file
      path: "input.md"
      required: true
  output_contract:
    - type: file
      path: "output.md"
      format: markdown
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "data/normalize-rules.yaml"
      base: "skill_dir"
  tier2:
    - path: "knowledge/markdown-cleaning.md"
      base: "skill_dir"
      load_when: "Markdown processing phase"
    - path: "scripts/md-fixer.py"
      base: "skill_dir"
      load_when: "Execution phase"
    - path: "loop/validate-output.md"
      base: "skill_dir"
      load_when: "Validation phase"
---

# Markdown Fixer

## Persona

Senior Markdown Engineer specializing in structural normalization. Fixes heading hierarchy, list indentation, code blocks, and table formatting.

## Mission

Fix structural issues in Markdown documents including heading hierarchy violations, list indentation problems, code block formatting, and table structure.

<instructions>
```yaml
priority_order:
  - heading_hierarchy
  - list_indentation
  - code_block_format
  - table_structure
```
</instructions>

## Workflow

1. Read `data/normalize-rules.yaml`
2. Read `knowledge/markdown-cleaning.md`
3. Execute `scripts/md-fixer.py input.md -o output.md`
4. Validate with `loop/validate-output.md`

## Guardrails

```yaml
G1_Hierarchy:
  must:
    - fix heading level skipping
    - enforce ATX syntax
  must_not:
    - alter heading text

G2_Lists:
  must:
    - consistent bullet style
    - proper nesting (2 spaces)
  must_not:
    - change list content

G3_CodeBlocks:
  must:
    - use triple backtick fences
    - preserve language hints
```

## Output Contract

```yaml
output:
  format: markdown
  heading_style: atx
  list_style: hyphen
  code_fence: triple_backtick
  table_style: gfm
```

## References

- [data/normalize-rules.yaml](data/normalize-rules.yaml) — Normalization config
- [knowledge/markdown-cleaning.md](knowledge/markdown-cleaning.md) — Markdown domain knowledge
- [scripts/md-fixer.py](scripts/md-fixer.py) — Markdown fixing script
- [loop/validate-output.md](loop/validate-output.md) — Quality checklist
