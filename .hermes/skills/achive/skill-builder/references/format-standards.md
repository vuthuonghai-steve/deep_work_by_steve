# AI-First Format Standards — Reference Guide

> **Purpose**: Condensed knowledge for creating LLM-optimized skill documents
> **Source**: Extracted from CLAUDE.md AI-first documentation standards
> **Usage**: Read at boot, reference when building SKILL.md outputs

---

## 1. Core Principle

Format must help LLM answer:
- Is this instruction or reference?
- Is this mandatory or suggestion?
- When to load this info?
- What is example vs criteria?

---

## 2. Three-Format System

### Markdown
**Use for**: explanation, architecture, rationale, onboarding, domain knowledge, walkthrough, decision notes, comparisons, contextual examples

**Avoid for**: hard rules without schema, long mixed policy blocks

### YAML
**Use for**: constraints, policies, checklists, routing, permission maps, output contracts, acceptance criteria

```yaml
recommended_keys:
  - must
  - must_not
  - should
  - priority_order
  - constraints
  - scope
  - allowed_tools
  - forbidden_patterns
  - output_contract
  - acceptance_criteria
```

### XML-like Tags
**Use for**: semantic boundaries, separating context from instruction, wrapping examples

```xml
<instructions>Behavioral rules.</instructions>
<context>Reference data, not a command.</context>
<examples>Illustrative patterns.</examples>
<input>User input or source documents.</input>
<output_contract>Mandatory output format.</output_contract>
```

---

## 3. SKILL.md Output Template (AI-First)

Every built SKILL.md MUST follow this structure:

```yaml
---
name: <skill-name>
description: <third-person, WHAT + WHEN trigger, <1024 chars>
---

<instructions>
MANDATORY rules. Use "must", "must_not", "never".
</instructions>

<context>
Reference data only. Use YAML for structured context.
</context>

<constraints>
```yaml
must:
  - rule 1
must_not:
  - prohibition 1
priority_order:
  - first
  - second
```
</constraints>

<output_contract>
Format of required output.
</output_contract>

## Workflow

[Phase-based steps with Tracker Checklist]

## Quality Gate

[Checklist]
```

---

## 4. YAML Frontmatter Requirements

```yaml
---
name: <skill-name>           # lowercase-kebab, max 64 chars
description: <third-person>  # WHAT + WHEN trigger, <1024 chars
---
```

**Name rules**:
- max 64 chars
- lowercase letters, numbers, hyphens only
- gerund form preferred: `processing-pdfs`, `analyzing-schemas`

**Description rules**:
- third-person: "Extracts...", "Analyzes...", "Builds..."
- NO: "I can help...", "You can use this to..."
- MUST include: WHAT it does + WHEN to trigger

---

## 5. SKILL.md Size Limits

| Metric | Target | Hard Limit |
|--------|--------|------------|
| SKILL.md body | < 300 lines | 500 lines |
| Single reference file | < 200 lines | unlimited with ToC |
| Boot Sequence files | ≤ 2 files | 3 files max |
| References per phase | ≤ 3 files | - |

---

## 6. Progressive Disclosure

| Tier | When to Load |
|------|--------------|
| Tier 1 | Boot — always load first |
| Tier 2 | When specific phase requires |
| Tier 3 | On-demand only |

---

## 7. Token Budget Quick Reference

| Layer | Good | Warning | Split When |
|-------|------|---------|------------|
| L0 (root) | 150-400 | 500-700 | >700 |
| L1 (policy) | 400-1200 | 1200-2000 | >2000 |
| L2 (domain) | 600-2500 | 2500-5000 | >5000 |

---

## 8. Anti-Patterns

```yaml
SKILL.md_smell:
  - exceeds 500 lines without split
  - mixes instructions with examples in same section
  - no XML tag boundaries
  - YAML frontmatter missing or malformed

format_smell:
  - prose where YAML would be clearer
  - no trace tags in task descriptions
  - placeholder density > 5
```

---

> **Last Updated**: 2026-05-18
> **Reason**: Embedded format knowledge directly into skill suite
