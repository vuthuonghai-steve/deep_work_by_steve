---
name: prompt-cleaner
description: Transforms raw unstructured prompts into CLAUDE.md-aligned structured prompts using format selection rules (Markdown/YAML/JSON). Use when user submits a messy or incomplete prompt before sending to Claude Code, or when you need to standardize a prompt's structure with goal, context, constraints, and output_format components.
---

# Prompt Cleaner — Architecture Design

## Mission

Transform raw prompts (Vietnamese/English) into structured prompts aligned with CLAUDE.md format selection rules. Multi-format output: Markdown for explanations, YAML for constraints, JSON for structured data.

---

## Workflow Progress Tracker

```
### [prompt-cleaner] Progress:
- [ ] Phase 1: COLLECT
- [ ] Phase 2: ANALYZE
- [ ] Phase 3: RESTRUCTURE
- [ ] Phase 4: OUTPUT
```

---

## Boot Sequence

Read Tier 1 files at boot:

- [data/format-selection-rules.yaml](data/format-selection-rules.yaml) — Always needed for format selection

---

## Phase 1: COLLECT

Receive raw prompt. Assess confidence level.

**Confidence Scoring Heuristic:**
```
Components detected (Goal, Context, Constraints, OutputFormat):
- 4/4 = ≥80% confidence
- 3/4 = 60-79% confidence  
- 2/4 = 40-59% confidence
- 1/4 = 20-39% confidence
- 0/4 = <20% confidence
```

**Decision Matrix:**

| Confidence | Action |
|------------|--------|
| < 40% | AskUserQuestion — 3 specific questions to clarify |
| 40-70% | Proceed to Phase 2 + Optional subagent explore |
| ≥ 70% | Proceed to Phase 2 directly |

**Interaction Point #1:** If confidence < 40%, ask user:
1. What is the main goal you want to achieve?
2. What context or information do you already have?
3. What output format do you expect?

---

## Phase 2: ANALYZE

Extract 4 required components:

| Component | Description | Prompt Question |
|-----------|-------------|-----------------|
| **GOAL** | Primary objective (1-3 lines) | "What should the AI do?" |
| **CONTEXT** | Available information (sufficient/insufficient?) | "What context exists?" |
| **CONSTRAINTS** | Rules, limitations | "What restrictions apply?" |
| **OUTPUT_FORMAT** | Expected output format | "What format should output be?" |

**Context Augmentation (Optional):**
- If confidence < 70% and related to codebase
- Use `delegate_task` subagent explore (max 5 files)
- Must cite source:line for all additions
- Forbidden: Adding information without source

**Interaction Point #2:** After extraction, if confidence 40-70%, present 4 components for user confirmation.

---

## Phase 3: RESTRUCTURE

### Step 3.1: Select Format

Read [data/format-selection-rules.yaml](data/format-selection-rules.yaml).

Apply format selection matrix:

| Content Type | Format | Template |
|-------------|--------|----------|
| Explanation, rationale, overview | Markdown | [cleaned-prompt-markdown.template](templates/cleaned-prompt-markdown.template) |
| Constraints, policies, checklists | YAML | [cleaned-prompt-yaml.template](templates/cleaned-prompt-yaml.template) |
| Structured data, output contracts | JSON | [cleaned-prompt-json.template](templates/cleaned-prompt-json.template) |

**Fallback:** If format does not match any rule, default to Markdown.

### Step 3.2: Apply Template

Load appropriate template. Fill placeholders:
- `{{GOAL}}` — from Phase 2 extraction
- `{{CONTEXT}}` — from Phase 2 extraction
- `{{CONSTRAINTS}}` — from Phase 2 extraction
- `{{OUTPUT_FORMAT}}` — from Phase 2 extraction

### Step 3.3: Validate

Read [loop/clean-checklist.md](loop/clean-checklist.md).

Run validation. Pass threshold: ≥5/6 items.

---

## Phase 4: OUTPUT

| Condition | Action |
|-----------|--------|
| Prompt already structured | Return as-is + note "Already well-structured" |
| Confidence < 40% | Return AskUserQuestion first |
| Validation PASS (≥5/6) | Deliver cleaned prompt |
| Validation FAIL (<3/6) | Retry restructure with checklist feedback |
| Validation PARTIAL (3-4/6) | Proceed but note improvement areas |

---

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | No hallucination | Must cite source:line for all context additions |
| G2 | Over-clean guard | If prompt already structured → return as-is + note |
| G3 | Format whitelist | Only use formats in data/format-selection-rules.yaml |
| G4 | Goal-first | `<goal>` MUST appear first in output |
| G5 | Ask when unsure | Confidence < 40% → AskUserQuestion, don't guess |
| G6 | Length budget | Cleaned prompt ≤ 3x original length |

---

## Placeholder Syntax

```
{{GOAL}}         — Primary objective
{{CONTEXT}}      — Background information
{{CONSTRAINTS}}  — Rules and limitations
{{OUTPUT_FORMAT}} — Expected output structure
{{CONFIDENCE}}   — Confidence score (0-100%)
{{CITE}}         — Source citation (file:line)
```

---

## Notes

- XML format has been deprecated per design.md §1 — use Markdown/YAML/JSON only
- Templates have backup fallback to Markdown if format does not match
- Subagent explore limited to 5 files maximum
