# Format Standards — skill-architect

## Nguồn gốc

Format standards này embed từ `/CLAUDE.md` §3, §4, §10 để đảm bảo skill-architect output đúng format.

---

## 1. Chọn Format

| Khi cần | Dùng format | Lý do |
|---------|-------------|-------|
| Giải thích, rationale, overview | Markdown | Đọc tự nhiên |
| Luật, constraints, policy, checklist | YAML | Ép cấu trúc, giảm ambiguity |
| Tạo ranh giới ngữ nghĩa | XML-like tags | Phân biệt instruction vs reference |

---

## 2. YAML Keys cho Policy

```yaml
must:           # Hành vi bắt buộc
must_not:       # Hành vi cấm
should:         # Best practice
priority_order: # Thứ tự ưu tiên khi xung đột
constraints:    # Ràng buộc
scope:          # Phạm vi áp dụng
output_contract:# Định dạng đầu ra bắt buộc
acceptance_criteria: # Tiêu chí chấp nhận
stop_conditions:# Điều kiện dừng
validation:     # Kiểm tra
```

---

## 3. XML-like Tags

```xml
<instructions>Luật điều khiển hành vi (imperative mode)</instructions>
<context>Dữ liệu tham chiếu, không phải lệnh</context>
<examples>Ví dụ minh họa pattern đúng</examples>
<input>Thông tin người dùng hoặc tài liệu nguồn</input>
<output_contract>Định dạng đầu ra bắt buộc — AI MUST comply</output_contract>
```

---

## 4. Token Budget

```yaml
L0_limit: 600    # Root guide / SKILL.md boot
L1_limit: 1500   # Policy files
L2_limit: 2500   # Domain context
tokenizer: cl100k_base
enforcement: hard  # REJECT if exceeded, return to agent for fix
```

---

## 5. Trace Tags (Anti-hallucination)

Mọi content phải có source attribution:

```markdown
[TỪ USER INPUT]        # Từ user request — verified
[TỪ DESIGN §N]         # Từ design section N — contract-bound
[TỪ NGUỒN EXTERNAL]    # Từ tài liệu bên ngoài — referenced
[GỢI Ý BỔ SUNG]        # Suy luận của AI — PHẢI flag để user verify
[CẦN LÀM RÕ]           # Chưa rõ — BLOCKER, must resolve before next phase
```

## 5.1 Semantic Activation Anchors

Từ CLAUDE.md §9: những từ khóa này TRIGGER mode xử lý đặc biệt trong LLM.

```yaml
activation_anchors:
  imperative:
    - must
    - must_not
    - priority_order
    - constraints
    - stop_conditions
  contextual:
    - context
    - reference
    - examples
    - evidence
  quality:
    - output_contract
    - acceptance_criteria
    - validation_checklist
    - definition_of_done
```

Dùng các anchor này trong output để đảm bảo LLM hiểu đúng intent:
- `must:` → Hành vi bắt buộc (YAML block)
- `must_not:` → Hành vi cấm (YAML block)
- `stop_conditions:` → Khi nào PHẢI dừng (YAML list)
- `<output_contract>` → Output format bắt buộc (XML tag)

## 5.2 Format Selection Rules

Từ CLAUDE.md §4: khi nào dùng format gì.

```yaml
format_selection:
  markdown:
    use_for: [explanation, rationale, overview, onboarding, domain_knowledge]
    avoid_for: [hard_rules_without_schema, long_mixed_policy_blocks]
  yaml:
    use_for: [constraints, policies, checklists, routing, output_contracts, acceptance_criteria]
    avoid_for: [long_prose, complex_narrative_context]
  xml_tags:
    use_for: [semantic_boundaries, separating_context_from_instruction, wrapping_examples]
    avoid_for: [excessive_micro_tagging, replacing_all_markdown]
```

---

## 6. Output Contract cho design.md

| Section | Format | Must have |
|---------|--------|-----------|
| §1 Problem Statement | Markdown | Pain point, User, Expected Output |
| §2 Capability Map | Markdown + YAML table | 3 Pillars |
| §3 Zone Mapping | Markdown table | Specific filenames, no placeholders |
| §4 Folder Structure | Mermaid mindmap | Match §3 exactly |
| §5 Execution Flow | Mermaid sequenceDiagram | Runtime flow |
| §6 Interaction Points | Markdown table | Stop conditions |
| §7 Progressive Disclosure | YAML | Tier 1 vs Tier 2 |
| §8 Risks | Markdown table | ≥3 risks + mitigation |
| §9 Open Questions | Markdown table | Status flags |
| §10 Metadata | YAML | skill-name, date, status |
