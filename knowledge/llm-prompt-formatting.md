# LLM Prompt Formatting — Domain Knowledge

> **Source:** CLAUDE.md (format selection rules) + HeavySkill research (reasoning patterns)
> **Purpose:** Domain knowledge for prompt-cleaner skill

---

## 1. Tổng quan

Tài liệu này chuẩn hóa cách format prompt để LLM hiểu đúng ý định với ít suy đoán nhất.

**Nguyên tắc cốt lõi:**
- Format không phải "đẹp nhất" mà là format giúp model trả lời nhanh các câu hỏi semantic
- Phân biệt rõ: instruction, context, example, evidence, output contract

---

## 2. Semantic Questions (Câu hỏi ngữ nghĩa)

Mỗi prompt cần giúp model trả lời:

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

### 3.1 Markdown — Khi nào dùng

**Dùng cho:**
- Overview, rationale, explanation
- Architecture explanation
- Onboarding, glossary
- Domain explanation, walkthrough
- Decision notes, bảng so sánh
- Ví dụ có ngữ cảnh

**Không dùng cho:**
- Hard rules không có schema
- Policy blocks dài và hỗn hợp

### 3.2 YAML — Khi nào dùng

**Dùng cho:**
- Constraints, policies, checklists
- Routing rules, permission maps
- Output contracts, acceptance criteria
- Configuration có tính cấu trúc

**Không dùng cho:**
- Prose dài
- Narrative context phức tạp
- Documents lồng sâu

### 3.3 XML-like Tags — Khi nào dùng

**Dùng cho:**
- Semantic boundaries giữa các khối lớn
- Tách context khỏi instruction
- Wrapping examples
- Wrapping external input
- Parseable output sections

**Không dùng cho:**
- Micro-tagging từng dòng
- Thay thế hoàn toàn markdown
- Prompt trees lồng sâu

---

## 4. CLAUDE.md Format Alignment

### 4.1 Core Principle

> **Format tốt không phải format đẹp nhất, mà là format giúp model trả lời nhanh câu hỏi semantic.**

### 4.2 Design Principles

```yaml
encode_intent_over_decoration: true
separate_rules_from_context: true
separate_examples_from_instructions: true
keep_root_guide_compact: true
load_domain_context_on_demand: true
prefer_named_schema_over_implicit_notes: true
avoid_large_flat_markdown: true
```

### 4.3 Recommended YAML Keys

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

### L0: Anchor Rules (Luật nền)
- **Purpose:** Luật nền, mục tiêu, giới hạn tuyệt đối, anti-goals
- **Load:** always
- **Location:** root guide (CLAUDE.md, AGENT.md, SYSTEM.md)
- **Format:** Markdown ngắn + YAML ngắn + XML boundary

### L1: Working Policy (Quy ước làm việc)
- **Purpose:** Coding rules, review rules, tool rules, output contract
- **Load:** frequent_or_scoped
- **Location:** docs/agent/policies, .claude/rules
- **Format:** YAML + Markdown ngắn

### L2: Domain Context (Ngữ cảnh domain)
- **Purpose:** Kiến trúc, domain glossary, data flow, ADR
- **Load:** on_demand
- **Location:** docs/architecture, docs/domains
- **Format:** Markdown chủ đạo, YAML snippets khi cần

### L3: Evidence Examples (Bằng chứng/Ví dụ)
- **Purpose:** Spec, ticket, logs, examples, fixtures
- **Load:** task_specific_only
- **Location:** specs, examples, tickets, tmp/context
- **Format:** XML wrapper + Markdown/YAML bên trong

---

## 6. Prompt Structure Best Practices

### 6.1 Goal-First Ordering

```
1. <goal> — Mục tiêu chính (1-3 dòng)
2. <context> — Thông tin hiện có
3. <constraints> — Rules, giới hạn
4. <output_format> — Kỳ vọng định dạng đầu ra
```

### 6.2 Required Components

| Component | Bắt buộc? | Mô tả |
|-----------|-----------|--------|
| Goal | ✅ | Mục tiêu rõ ràng, đo lường được |
| Context | ✅ | Thông tin nền đủ để hiểu task |
| Constraints | ⚠️ | Nếu có giới hạn đặc biệt |
| Output Format | ⚠️ | Nếu cần định dạng cụ thể |

### 6.3 Context Augmentation

Khi bổ sung context:
- **Phải:** Cite source:line cho mọi thông tin thêm
- **Phải:** Dùng subagent explore (max 5 files)
- **Không được:** Tự thêm thông tin không có nguồn

---

## 7. Token Budget Guidelines

### 7.1 By Layer

| Layer | Good | Warning | Split When |
|-------|------|---------|------------|
| L0 | 150-400 | 500-700 | >700 |
| L1 | 400-1200 | 1200-2000 | >2000 |
| L2 | 600-2500 | 2500-5000 | >5000 |
| L3 | 300-2000 | 2000-6000 | >6000 |

### 7.2 By Format

| Format | Light | Medium | Heavy | Overloaded |
|--------|-------|--------|-------|------------|
| Markdown section | 100-400 | 400-900 | 900-1800 | >1800 |
| YAML block | 80-300 | 300-700 | 700-1200 | >1200 |
| XML block | 50-250 | 250-800 | 800-1500 | >1500 |

---

## 8. Anti-Hallucination Rules

### AH1: Traceability
Mọi task phải trace về nguồn: `[TỪ DESIGN §N]`

### AH2: No Requirement Addition
Chỉ decompose, không thêm requirements mới

### AH3: No Domain Guessing
Không viết domain knowledge khi không có tài nguyên

### AH4: Source Labeling
Phân biệt rõ: `[TỪ DESIGN]` vs `[GỢI Ý]` vs `[TỪ AUDIT TÀI NGUYÊN]`

### AH5: Resource Verification
Verify resources trước khi complete

---

## 9. Standard Task Context Template

```xml
<task>
[Mô tả task rõ ràng, ngắn gọn]
</task>

<context>
[Thông tin kiến trúc, module liên quan, ràng buộc hệ thống]
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
[Ví dụ minh họa pattern đúng/sai]
</examples>
```

---

## 10. Quick Reference

| Situation | Format | Example |
|-----------|--------|---------|
| Giải thích, bối cảnh | Markdown | Overview, rationale |
| Luật, constraints, checklist | YAML | must/must_not, policies |
| Phân tách semantic lớn | XML tags | `<task>`, `<context>` |
| Output có cấu trúc | YAML | output_contract, acceptance_criteria |

---

## Liên quan

- [CLAUDE.md](../../CLAUDE.md) — Root guide cho format selection rules
- [Heavy Thinking](../ai-agents/haevy-thinking/heavy-thinking.md) — Parallel reasoning research
- [AI Agents](../ai-agents/ai-agents.md) — LLM reasoning fundamentals
