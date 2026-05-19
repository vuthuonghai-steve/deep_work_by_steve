# LLM Prompt Formatting — Domain Knowledge

> **Usage**: Load when executing Phase 2 (ANALYZE) — needed for understanding format selection and prompt structuring.
> **Source**: CLAUDE.md format selection rules + resources/llm-prompt-formatting.md

---

## 1. Core Principle

> **Format tốt không phải format đẹp nhất, mà là format giúp model trả lời nhanh câu hỏi semantic.**

---

## 2. Semantic Questions

Each prompt must help the model answer:

```yaml
semantic_questions:
  - "Đây là mệnh lệnh hay dữ liệu tham chiếu?"
  - "Đây là luật bắt buộc hay gợi ý mềm?"
  - "Thông tin này luôn cần dùng hay chỉ theo ngữ cảnh?"
  - "Phần nào là ví dụ, phần nào là tiêu chí chấp nhận?"
  - "Khi có xung đột, ưu tiên nào cao hơn?"
```

---

## 3. Format Selection Matrix

### 3.1 Markdown — When to Use

**Use for:**
- Overview, rationale, explanation
- Architecture explanation
- Onboarding, glossary
- Domain explanation, walkthrough
- Decision notes, comparison tables
- Contextual examples

**Avoid for:**
- Hard rules without schema
- Long mixed policy blocks

### 3.2 YAML — When to Use

**Use for:**
- Constraints, policies, checklists
- Routing rules, permission maps
- Output contracts, acceptance criteria
- Structured configuration

**Avoid for:**
- Long prose
- Complex narrative context
- Deeply nested documents

### 3.3 JSON — When to Use

**Use for:**
- Structured data serialization
- API-like output contracts
- Machine-readable configurations

---

## 4. Design Principles

```yaml
encode_intent_over_decoration: true
separate_rules_from_context: true
separate_examples_from_instructions: true
keep_root_guide_compact: true
load_domain_context_on_demand: true
prefer_named_schema_over_implicit_notes: true
avoid_large_flat_markdown: true
```

### Recommended YAML Keys

```yaml
recommended_yaml_keys:
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
  - routing_rules
  - stop_conditions
  - validation_checklist
```

---

## 5. 4-Layer Knowledge Model

### L0: Anchor Rules
- **Purpose:** Core rules, objectives, absolute limits, anti-goals
- **Load:** always
- **Location:** root guide (CLAUDE.md, AGENT.md, SYSTEM.md)

### L1: Working Policy
- **Purpose:** Coding rules, review rules, tool rules, output contract
- **Load:** frequent_or_scoped
- **Format:** YAML + short Markdown

### L2: Domain Context
- **Purpose:** Architecture, domain glossary, data flow, ADR
- **Load:** on_demand
- **Format:** Markdown primary, YAML snippets as needed

### L3: Evidence Examples
- **Purpose:** Spec, ticket, logs, examples, fixtures
- **Load:** task_specific_only
- **Format:** XML wrapper + Markdown/YAML inside

---

## 6. Prompt Structure Best Practices

### 6.1 Goal-First Ordering

```
1. <goal> — Primary objective (1-3 lines)
2. <context> — Available information
3. <constraints> — Rules, limitations
4. <output_format> — Expected output format
```

### 6.2 Required Components

| Component | Required? | Description |
|-----------|-----------|-------------|
| Goal | ✅ | Clear, measurable objective |
| Context | ✅ | Sufficient background information |
| Constraints | ⚠️ | If special limitations exist |
| Output Format | ⚠️ | If specific format required |

### 6.3 Context Augmentation Rules

When adding context:
- **Must:** Cite source:line for all added information
- **Must:** Use subagent explore (max 5 files)
- **Forbidden:** Adding information without source

---

## 7. Token Budget Guidelines

| Layer | Good | Warning | Split When |
|-------|------|---------|------------|
| L0 | 150-400 | 500-700 | >700 tokens |
| L1 | 400-1200 | 1200-2000 | >2000 tokens |
| L2 | 600-2500 | 2500-5000 | >5000 tokens |

---

## 8. Anti-Hallucination Rules

### AH1: Traceability
Every task must trace to source: `[TỪ DESIGN §N]`

### AH2: No Requirement Addition
Only decompose, don't add new requirements

### AH3: No Domain Guessing
Don't write domain knowledge without resources

### AH4: Source Labeling
Distinguish: `[TỪ DESIGN]` vs `[GỢI Ý]` vs `[TỪ AUDIT TÀI NGUYÊN]`

### AH5: Resource Verification
Verify resources before completing

---

## 9. Standard Task Context Template

```xml
<task>
[Clear, concise task description]
</task>

<context>
[Architecture info, related modules, system constraints]
</context>

<constraints>
```yaml
must:
  - [requirement 1]
  - [requirement 2]
must_not:
  - [forbidden 1]
```
</constraints>

<acceptance_criteria>
```yaml
criteria:
  - [criterion 1]
  - [criterion 2]
```
</acceptance_criteria>

<examples>
[Examples illustrating correct/incorrect patterns]
</examples>
```

---

## 10. Quick Reference

| Situation | Format | Example |
|-----------|--------|---------|
| Explanation, context | Markdown | Overview, rationale |
| Rules, constraints | YAML | must/must_not, policies |
| Semantic boundaries | XML tags | `<task>`, `<context>` |
| Structured output | YAML | output_contract, acceptance_criteria |
