# Format Standards — skill-builder

## Nguồn gốc

Format standards này embed từ `/CLAUDE.md` §3, §4, §10 để đảm bảo skill-builder output đúng format.

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

## 6. Output Contract cho built Skill

Built skill phải tuân thủ Anthropic Skill Standards:

### SKILL.md Requirements

| Requirement | Rule |
|-------------|------|
| YAML frontmatter | Line 1 phải là `---` |
| name field | lowercase-kebab-case, ≤64 chars |
| description | ngôi thứ 3, WHAT + WHEN trigger, ≤1024 chars |
| body | ≤500 lines |
| Tier 1 files | Phải có trong Boot Sequence |

### Knowledge Files

| Requirement | Rule |
|-------------|------|
| Usage header | Mỗi file phải có header mô tả khi nào load |
| No orphan files | Mọi file phải được link từ SKILL.md |

### Loop Files

| Requirement | Rule |
|-------------|------|
| YAML format | Machine-readable validation |
| trace_validation | MUST compliance |

---

## 7. Enforce: Hard

**Format compliance là bắt buộc tuyệt đối.** Không có ngoại lệ.

```yaml
enforcement: hard
reject_if:
  - missing_trace_tags
  - missing_xml_boundaries_in_output
  - missing_yaml_blocks_in_constraints
  - token_budget_exceeded
  - yaml_frontmatter_missing_line1
  - orphan_files_detected
```
