# Skill Suite Format Standards

> **Usage**: Load at Boot — REQUIRED for AI-first format knowledge

---

## The Problem

LLM không xử lý Markdown, YAML hay XML như compiler. Mô hình phản ứng với các mẫu cấu trúc đã gặp trong huấn luyện và với ranh giới ngữ nghĩa được prompt thể hiện.

## The Solution: Hybrid Format

Use this structure for ALL skill outputs (design.md, todo.md, SKILL.md):

```xml
<task>Concise problem statement — what to do</task>
<constraints>
```yaml
must:
  - hard requirement 1
  - hard requirement 2
must_not:
  - prohibition 1
priority_order:
  - first_priority
  - second_priority
```
</constraints>
<examples>Concrete usage examples with real values</examples>
<output_contract>Expected output format and success criteria</output_contract>
```

## Format Selection Rules

| Format | Use For |
|--------|---------|
| **YAML** | Constraints, policies, checklists, routing, permission maps, output contracts |
| **XML tags** | Semantic boundaries: `<task>`, `<context>`, `<constraints>`, `<examples>`, `<input>`, `<output_contract>` |
| **Markdown** | Explanation, architecture, rationale, domain knowledge, tables, diagrams |

## Why This Matters

The format MUST help the model answer:
1. Is this a command or reference data?
2. Is this a hard rule or soft suggestion?
3. When is this information needed — always or contextually?
4. What's an example vs. acceptance criteria?
5. When there's conflict, what takes priority?

## Token Budget (Root Guide)

| Layer | Good | Warning | Split When |
|-------|------|---------|------------|
| L0 anchor | 150-400 | 500-700 | >700 tokens |
| L1 policy | 400-1200 | 1200-2000 | >2000 tokens |
| L2 domain | 600-2500 | 2500-5000 | >5000 tokens |

## Anti-Hallucination Tags

```
[TỪ DESIGN §N]      — Derived directly from design.md section N
[GỢI Ý BỔ SUNG]     — Suggested by skill, not in design.md
[TỪ AUDIT TÀI NGUYÊN] — Generated because resource was missing
[CẦN LÀM RÕ]        — Needs user clarification
```

> **Non-negotiable**: Skills that don't follow this format should be patched.
