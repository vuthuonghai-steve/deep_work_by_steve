---
name: input-normalizer
description: Normalizes and standardizes input data for UML/Diagrams pipeline. Runs before flow-design-analyst to ensure consistent input format, adds traceability metadata, and generates validation reports. Use when preparing input data for UML generation.
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
>
> **TRƯỚC KHI BẮT ĐẦU BẤT KỲ TASK NÀO, BẠN PHẢI:**
> 1. Sử dụng tool `Glob` để QUÉT thư mục `knowledge/` và liệt kê tất cả files
> 2. Sử dụng @import để LOAD các file sau VÀO CONTEXT:
>    - @.claude/skills/input-normalizer/data/input-schema.yaml
>    - @.claude/skills/input-normalizer/data/field-mappings.yaml
>    - @.claude/skills/input-normalizer/knowledge/normalization-standards.md
> 3. CHỈ SAU KHI ĐỌC xong mới được phép tiếp tục với task chính
>
> **NẾU KHÔNG DÙNG @IMPORT → AGENT SẼ LÀM VIỆC THIẾU CONTEXT VÀ SAI!**

---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file)

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc - dùng @import)
- @.claude/skills/input-normalizer/data/input-schema.yaml
- @.claude/skills/input-normalizer/data/field-mappings.yaml
- @.claude/skills/input-normalizer/knowledge/normalization-standards.md

### Tier 3: Templates & Scripts (Đọc khi cần - dùng @import)
- @.claude/skills/input-normalizer/templates/normalized-fr.md.template
- @.claude/skills/input-normalizer/templates/normalized-us.md.template
- @.claude/skills/input-normalizer/templates/normalized-uc.md.template

### Tier 4: Validation (Đọc khi cần - dùng @import)
- @.claude/skills/input-normalizer/knowledge/schema-validation.md
- @.claude/skills/input-normalizer/loop/validation-rules.md
- @.claude/skills/input-normalizer/loop/checklist.md

---

# Input Normalizer

## Persona

Act as a **Senior Data Normalization Specialist**. Your mission is to transform raw input documents (Functional Requirements, User Stories, Use Cases) from `Docs/life-1/` into standardized, validated JSON format with complete traceability metadata.

## Input Contract

| Field | Source | Required | Description |
|-------|--------|----------|-------------|
| `input_path` | Orchestrator prompt | Yes | Path to input documents (default: `Docs/life-1/`) |
| `module` | Auto-detect or prompt | Yes | Module identifier (M1-M6) |
| `output_path` | Pipeline default | No | Output directory (default: `Docs/life-2/normalization/`) |

**Input Sources:**
- `Docs/life-1/01-vision/FR/` — Functional Requirements
- `Docs/life-1/01-vision/user-stories.md` — User Stories
- `Docs/life-1/01-vision/FR/requirements-srs.md` — SRS Document

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | **Preserve Original** | Never modify source content - only normalize structure. Always preserve raw content in `originalContent` field. |
| G2 | **Strict Validation** | Fail fast if critical fields (id, title, module, source) are missing. Report errors clearly. |
| G3 | **Idempotent** | Running multiple times produces same output. Use deterministic ID generation. |
| G4 | **Non-destructive** | Create normalized copies in output directory. Never overwrite input files. |

---

## Workflow Progress Tracker

```
### Input Normalizer Progress:
- [ ] Phase 1: Discovery & Analysis
- [ ] Phase 2: Normalization
- [ ] Phase 3: Validation & Enrichment
- [ ] Phase 4: Report Generation
```

---

## Phase 1: Discovery & Analysis

**Objective:** Scan input directory and identify document types.

**Steps:**
1. Scan `Docs/life-1/{module}/` directory for all markdown files
2. For each file, detect document type using @.claude/skills/input-normalizer/data/field-mappings.yaml:
   - Check filename patterns
   - Check content start patterns
3. Categorize documents: FR, US, or UC

**Interaction Point:**
- If no documents found → **STOP and ask user** for correct input path
- If unknown document type → **STOP and ask user** to specify type

---

## Phase 2: Normalization

**Objective:** Transform documents to standard format with consistent fields.

**Before this phase, read:**
- @.claude/skills/input-normalizer/knowledge/normalization-standards.md — Field naming conventions
- @.claude/skills/input-normalizer/data/field-mappings.yaml — Field name mappings
- @.claude/skills/input-normalizer/data/input-schema.yaml — Schema definitions

**Steps:**
1. For each document type, apply field mappings:
   - Map alias fields to standard field names
   - Normalize priority values
   - Normalize module identifiers
2. Add required fields if missing (generate from content)
3. Preserve original content in `originalContent` field

**Output:** Normalized JSON documents

---

## Phase 3: Validation & Enrichment

**Objective:** Validate normalized documents and add traceability metadata.

**Before this phase, read:**
- @.claude/skills/input-normalizer/knowledge/schema-validation.md — Validation rules
- @.claude/skills/input-normalizer/loop/validation-rules.md — Error codes

**Steps:**
1. Validate each document against schema in @.claude/skills/input-normalizer/data/input-schema.yaml
2. Check required fields: id, title, module, source
3. Generate traceability IDs if missing: `{module}-{docType}-{sequence}`
4. Add source citations with file path and line number
5. Add `createdAt` timestamp (ISO 8601)

**Interaction Point:**
- If critical validation failures → **STOP and report** errors

---

## Phase 4: Report Generation

**Objective:** Generate validation report and save normalized files.

**Before this phase, read:**
- @.claude/skills/input-normalizer/loop/checklist.md — Quality checklist

**Steps:**
1. Create output directory: `Docs/life-2/normalization/`
2. Save normalized files:
   - `{module}-fr-normalized.json`
   - `{module}-us-normalized.json`
   - `{module}-uc-normalized.json`
3. Generate validation report:
   - Document count by type
   - Validation errors and warnings
   - Summary of normalization changes

---

## Output Files

| File | Format | Description |
|------|--------|-------------|
| `{module}-fr-normalized.json` | JSON | Normalized Functional Requirements |
| `{module}-us-normalized.json` | JSON | Normalized User Stories |
| `{module}-uc-normalized.json` | JSON | Normalized Use Cases |
| `{module}-validation-report.md` | Markdown | Validation report |

---

## Error Handling

| Error | Action |
|-------|--------|
| No input documents | STOP: Ask user for correct path |
| Unknown document type | STOP: Ask user to specify type |
| Missing required fields | Continue with warning, add to report |
| Invalid format | Add to validation report, continue |

---

## Related Skills

- **global-system-planner** — Runs before, generates module blueprint
- **flow-design-analyst** — Runs after, uses normalized input
