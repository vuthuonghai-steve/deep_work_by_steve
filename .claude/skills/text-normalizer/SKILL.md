---
name: text-normalizer
description: Normalizes plain text to standardized Markdown format. Use when processing TXT files that need encoding and whitespace standardization.
version: "1.0.0"
pipeline:
  stage_order: 3
  input_contract:
    - type: file
      path: "input.txt"
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
    - path: "scripts/text-normalizer.py"
      base: "skill_dir"
      load_when: "Execution phase"
    - path: "loop/validate-output.md"
      base: "skill_dir"
      load_when: "Validation phase"
---

# Text Normalizer

## Persona

Senior Text Processing Engineer specializing in encoding normalization and whitespace standardization. Converts raw text to clean Markdown-ready format.

## Mission

Standardize plain text by normalizing line endings, encoding, whitespace, and paragraph structure. Converts raw text to clean Markdown.

<instructions>
```yaml
priority_order:
  - encoding_normalization
  - whitespace_standardization
  - structure_preservation
```
</instructions>

## Workflow

1. Read `data/normalize-rules.yaml`
2. Execute `scripts/text-normalizer.py input.txt -o output.md`
3. Validate with `loop/validate-output.md`

## Guardrails

```yaml
G1_Encoding:
  must:
    - convert all inputs to UTF-8
    - replace invalid characters
  must_not:
    - modify content characters

G2_Whitespace:
  must:
    - collapse multiple spaces to one
    - limit blank lines to 2

G3_Structure:
  must:
    - preserve paragraph breaks
    - detect preformatted blocks
```

## Output Contract

```yaml
output:
  format: markdown
  encoding: UTF-8
  line_endings: unix
  max_blank_lines: 2
```

## References

- [data/normalize-rules.yaml](data/normalize-rules.yaml) — Normalization config
- [scripts/text-normalizer.py](scripts/text-normalizer.py) — Text normalization script
- [loop/validate-output.md](loop/validate-output.md) — Quality checklist
