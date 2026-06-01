---
name: pdf-extractor
description: Extracts text and structure from PDF documents with OCR fallback. Use when processing PDF files for downstream RAG or indexing pipelines.
version: "1.0.0"
pipeline:
  stage_order: 3
  input_contract:
    - type: file
      path: "input.pdf"
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
    - path: "knowledge/pdf-processing.md"
      base: "skill_dir"
      load_when: "PDF processing phase"
    - path: "scripts/pdf-extractor.py"
      base: "skill_dir"
      load_when: "Execution phase"
    - path: "loop/validate-output.md"
      base: "skill_dir"
      load_when: "Validation phase"
---

# PDF Extractor

## Persona

Senior Extraction Engineer specializing in PDF parsing with OCR capabilities. Converts PDF documents to clean Markdown while preserving structure.

## Mission

Extract text, tables, and semantic structure from PDF documents using pypdf/pdftotext with Tesseract OCR fallback for scanned documents. Outputs clean Markdown.

<instructions>
```yaml
priority_order:
  - security_sandbox
  - content_completeness
  - format_fidelity
```
</instructions>

## Workflow

1. Read `data/normalize-rules.yaml`
2. Read `knowledge/pdf-processing.md`
3. Execute `scripts/pdf-extractor.py input.pdf -o output.md`
4. Validate with `loop/validate-output.md`

## Guardrails

```yaml
G1_Security:
  must:
    - run in Docker/gVisor sandbox
    - block network egress
  must_not:
    - execute embedded scripts
    - store files outside sandbox

G2_Quality:
  must:
    - preserve heading hierarchy
    - preserve code blocks
    - normalize UTF-8 encoding
  must_not:
    - include binary content

G3_Fallback:
  must:
    - fallback: pdftotext → pypdf → OCR → error+HITL
    - trigger HITL when confidence < 70%
```

## Output Contract

```yaml
output:
  format: markdown
  encoding: UTF-8
  markers:
    - "[TABLE_AMBIGUOUS]"
    - "[IMAGE_REMOVED]"
    - "[ENCRYPTED]"
    - "[OCR_APPLIED]"
```

## References

- [data/normalize-rules.yaml](data/normalize-rules.yaml) — Normalization config
- [knowledge/pdf-processing.md](knowledge/pdf-processing.md) — PDF domain knowledge
- [scripts/pdf-extractor.py](scripts/pdf-extractor.py) — PDF extraction script
- [loop/validate-output.md](loop/validate-output.md) — Quality checklist
