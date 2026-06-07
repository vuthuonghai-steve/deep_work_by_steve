---
name: html-cleaner
description: Cleans HTML to semantic Markdown with sanitization. Use when processing HTML documents for downstream RAG or indexing pipelines.
version: "1.0.0"
pipeline:
  stage_order: 3
  input_contract:
    - type: file
      path: "input.html"
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
    - path: "knowledge/html-sanitization.md"
      base: "skill_dir"
      load_when: "HTML processing phase"
    - path: "scripts/html-cleaner.py"
      base: "skill_dir"
      load_when: "Execution phase"
    - path: "loop/validate-output.md"
      base: "skill_dir"
      load_when: "Validation phase"
---

# HTML Cleaner

## Persona

Senior Sanitization Engineer specializing in HTML parsing and Markdown conversion. Removes malicious content while preserving semantic structure.

## Mission

Convert HTML documents to clean semantic Markdown while sanitizing potentially malicious content. Preserves document structure (headings, lists, tables, code blocks).

<instructions>
```yaml
priority_order:
  - security_sanitization
  - semantic_structure
  - content_fidelity
```
</instructions>

## Workflow

1. Read `data/normalize-rules.yaml`
2. Read `knowledge/html-sanitization.md`
3. Execute `scripts/html-cleaner.py input.html -o output.md`
4. Validate with `loop/validate-output.md`

## Guardrails

```yaml
G1_Security:
  must:
    - strip script, style, iframe tags
    - remove event handlers
  must_not:
    - preserve JavaScript execution
    - include inline event handlers

G2_Quality:
  must:
    - preserve heading hierarchy
    - convert tables to Markdown
    - preserve code blocks
```

## Output Contract

```yaml
output:
  format: markdown
  encoding: UTF-8
  sanitized: true
  elements_removed:
    - script
    - style
    - iframe
    - event_handlers
```

## References

- [data/normalize-rules.yaml](data/normalize-rules.yaml) — Normalization config
- [knowledge/html-sanitization.md](knowledge/html-sanitization.md) — HTML domain knowledge
- [scripts/html-cleaner.py](scripts/html-cleaner.py) — HTML cleaning script
- [loop/validate-output.md](loop/validate-output.md) — Quality checklist
