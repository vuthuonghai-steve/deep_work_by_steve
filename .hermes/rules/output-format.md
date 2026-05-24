# Output Format Rules — AI-Agent-Centric Markdown Standard

## Mục đích

Tài liệu này quy định **chuẩn format đầu ra** cho mọi file Markdown được viết trong workspace `deep_work_by_steve`. Đối tượng phục vụ chính là **AI agent** — tài liệu phải đủ rõ để agent tuân thủ mà không cần suy đoán, đồng thời vẫn đọc được bởi con người.

---

## Nguyên lý nền tảng

```yaml
core_principles:
  encode_intent_over_decoration: >
    Format tốt không phải format đẹp nhất, mà là format giúp mô hình trả lời nhanh:
    đâu là lệnh, đâu là tham chiếu, đâu là ví dụ, đâu là tiêu chí chấp nhận.
  separate_rules_from_context: true
  separate_examples_from_instructions: true
  keep_root_guide_compact: true
  load_domain_context_on_demand: true
  prefer_named_schema_over_implicit_notes: true
  avoid_large_flat_markdown: true
```

---

## 1. Phân lớp tài liệu (Knowledge Layers)

Mọi file phải được gán đúng lớp. Không nhét L2/L3 vào file L0/L1.

```yaml
layer_definitions:
  L0_anchor_rules:
    purpose: "Luật nền, mục tiêu, giới hạn tuyệt đối, anti-goals."
    load_policy: always
    location: "CLAUDE.md, AGENT.md, SYSTEM.md ở root"
    preferred_format: "Markdown ngắn + YAML ngắn + XML boundary"

  L1_working_policy:
    purpose: "Quy ước làm việc, coding rules, review rules, tool rules, output contract."
    load_policy: "frequent_or_scoped"
    location: ".hermes/rules/"
    preferred_format: "YAML + Markdown ngắn"

  L2_domain_context:
    purpose: "Kiến trúc, domain glossary, data flow, ADR, subsystem notes."
    load_policy: "on_demand"
    location: "docs/architecture/, docs/domains/, docs/runbooks/"
    preferred_format: "Markdown chủ đạo, có YAML snippets khi cần"

  L3_evidence_examples:
    purpose: "Spec, ticket, logs, examples, fixtures, reference docs."
    load_policy: "task_specific_only"
    location: "specs/, examples/, tmp/context/"
    preferred_format: "XML wrapper + Markdown/YAML bên trong"
```

**Luật vận hành:** Root guide (L0) chỉ chứa L0 + phần cô đọng nhất của L1. L2 và L3 phải tách file riêng, nạp theo task.

---

## 2. Chọn đúng format theo loại thông tin

```yaml
format_selection:
  markdown:
    use_for:
      - overview / giới thiệu
      - rationale / lý do quyết định
      - architecture explanation
      - onboarding
      - glossary
      - domain explanation
      - walkthrough
      - decision notes
      - bảng so sánh
      - ví dụ có ngữ cảnh
    avoid_for:
      - hard_rules_without_schema
      - long_mixed_policy_blocks
      - constraint mà không có key rõ ràng

  yaml:
    use_for:
      - constraints
      - policies
      - checklists
      - routing
      - permission_maps
      - output_contracts
      - acceptance_criteria
      - must / must_not / should
      - allowed_tools
      - forbidden_patterns
      - priority_order
      - stop_conditions
      - validation_checklist
    avoid_for:
      - long_prose
      - complex_narrative_context
      - deeply_nested_documents (>4 cấp indentation)

  xml_like_tags:
    use_for:
      - semantic_boundaries (tách instruction khỏi context)
      - separating_context_from_instruction
      - wrapping_examples
      - wrapping_external_input
      - wrapping_task_specs
      - parseable_output_sections
    avoid_for:
      - excessive_micro_tagging (bọc từng dòng/đoạn nhỏ)
      - replacing_all_markdown
      - deeply_nested_prompt_trees
```

---

## 3. XML Tag chuẩn — Semantic Delimiters

Dùng để phân ranh khối lớn. Tên tag phải mang nghĩa rõ.

```xml
<instructions>Luật điều khiện hành vi — agent phải tuân thủ.</instructions>
<context>Dữ liệu tham chiếu, không phải lệnh.</context>
<examples>Ví dụ minh họa pattern đúng/sai.</examples>
<input>Thông tin người dùng hoặc tài liệu nguồn được cung cấp.</input>
<output_contract>Định dạng đầu ra bắt buộc.</output_contract>
<task>Mô tả tác vụ cần thực hiện.</task>
<constraints>Ràng buộc phạm vi, kỹ thuật, hoặc nghiệp vụ.</constraints>
<acceptance_criteria>Tiêu chí để xác nhận task hoàn thành đúng.</acceptance_criteria>
```

**Nguyên tắc:**
- Tag ngoài cùng (outer block) cho toàn bộ section.
- Không bọc vi mô từng bullet point hoặc từng câu.
- Tên tag phải tự giải thích — tránh `<data1>`, `<part2>`, `<misc>`.

---

## 4. Schema key chuẩn cho YAML

Dùng nhất quán. Không dùng nhiều biến thể cho cùng một ý nghĩa.

```yaml
# ── Hard rules (bắt buộc tuyệt đối) ──
must:          # hành động phải thực hiện
must_not:      # hành động cấm

# ── Soft rules (nên / khuyến nghị) ──
should:        # khuyến nghị mạnh
should_not:    # khuyến nghị tránh

# ── Scope & routing ──
scope:         # phạm vi áp dụng
priority_order: # thứ tự ưu tiên khi xung đột
allowed_tools:  # công cụ được phép dùng
forbidden_patterns: # pattern cấm

# ── Output & validation ──
output_contract:    # hình thức đầu ra bắt buộc
acceptance_criteria: # tiêu chí nghiệm thu
validation_checklist: # bước kiểm tra trước khi trả lời
stop_conditions:   # điều kiện dừng / kết thúc

# ── Navigation ──
load_when_needed:  # bản đồ nạp context
routing_rules:     # quy tắc định tuyến
```

**Cấm:** Không dùng `avoid`, `do_not`, `never_do`, `forbidden` thay cho `must_not` hoặc `should_not`. Chọn một schema và dùng nhất quán toàn bộ project.

---

## 5. Token Budget — Ngưỡng vận hành theo layer

Dùng làm **hệ quy chiếu**, không phải giới hạn tuyệt đối.

```yaml
token_budget_by_layer:
  L0_anchor_rules:
    good: "150-400 tokens"
    warning: "500-700 tokens"
    split_when: ">700 tokens"

  L1_working_policy:
    good: "400-1200 tokens"
    warning: "1200-2000 tokens"
    split_when: ">2000 tokens"

  L2_domain_context:
    good: "600-2500 tokens"
    warning: "2500-5000 tokens"
    split_when: ">5000 tokens"

  L3_evidence_examples:
    good: "300-2000 tokens"
    warning: "2000-6000 tokens"
    split_when: ">6000 tokens"

token_budget_by_format:
  markdown_section:
    light: "100-400 tokens"
    medium: "400-900 tokens"
    heavy: "900-1800 tokens"
    overloaded: ">1800 tokens"

  yaml_block:
    light: "80-300 tokens"
    medium: "300-700 tokens"
    heavy: "700-1200 tokens"
    overloaded: ">1200 tokens"

  xml_block:
    light: "50-250 tokens"
    medium: "250-800 tokens"
    heavy: "800-1500 tokens"
    overloaded: ">1500 tokens"

  root_guide_total:
    excellent: "300-900 tokens"
    good: "900-1800 tokens"
    warning: "1800-3000 tokens"
    heavy: "3000-5000 tokens"
    overloaded: ">5000 tokens"
```

**Quy tắc ứng xử:**
- Markdown section >900 tokens → xem xét tách hoặc chuyển policy sang YAML.
- YAML block >700-1200 tokens hoặc indentation >3-4 cấp → tách theo domain.
- XML chiếm tỉ lệ lớn hơn nội dung → bỏ bớt tag, chỉ giữ outer boundary.
- Root guide >1800-3000 tokens mà tăng đều → dấu hiệu thiếu phân tầng → tái cấu trúc.

---

## 6. Tỷ lệ phân bổ trong root guide

```yaml
root_guide_allocation:
  anchor_rules:    "15-25%  (L0 — luật nền, non-negotiables)"
  working_policy:  "35-50%  (L1 — constraints, policy, workflow)"
  architecture:    "20-30%  (L2 overview — bản đồ kiến trúc mức cao)"
  examples:        "5-15%   (L3 — tối thiểu, có thì bọc <examples>)"
```

**Cảnh báo:** Phần examples/reference vượt 15% → root đang biến thành kho tri thức, không phải bảng điều hướng.

---

## 7. Cấu trúc root guide chuẩn

Root guide (CLAUDE.md / AGENT.md) phải có 4 vùng cố định:

```markdown
# Project Agent Guide

## Purpose
Mô tả dự án, domain, định nghĩa thành công.

<instructions>
Luật điều khiển hành vi bắt buộc — XML boundary cho non-negotiables.
</instructions>

## Core Policy

```yaml
priority_order:
  - user_task
  - source_fidelity
  - safety
  - maintainability
  - minimal_change

constraints:
  must:
    - ...
  must_not:
    - ...

output_contract:
  include:
    - summary_of_changes
    - files_changed
    - validation_performed
    - remaining_risks
```

## Working Map

```yaml
load_when_needed:
  backend_rules:  ".hermes/rules/backend.md"
  frontend_rules: ".hermes/rules/frontend.md"
  testing_policy: "docs/agent/test-policy.yaml"
  architecture_overview: "docs/architecture/overview.md"
  domain_docs: "docs/domains/"
  examples: "examples/"
```

## Interaction Protocol

```yaml
agent_protocol:
  before_editing:
    - inspect relevant files
    - identify scope and risk
    - load scoped rules if available
  during_editing:
    - prefer minimal safe changes
    - preserve existing patterns
    - document assumptions
  before_final_response:
    - run available validation when practical
    - state what was and was not verified
```

---

## 8. Task Context Template — Dùng khi spec/ticket/log đi kèm prompt

```xml
<task>
[Mô tả tác vụ cần thực hiện — ngắn gọn, rõ mục tiêu]
</task>

<context>
[Trích đoạn kiến trúc, module liên quan, ràng buộc hệ thống, hoặc tài liệu nguồn]
</context>

<constraints>
```yaml
must:
  - [ràng buộc bắt buộc 1]
  - [ràng buộc bắt buộc 2]
must_not:
  - [điều cấm 1]
  - [điều cấm 2]
```
</constraints>

<acceptance_criteria>
```yaml
criteria:
  - [tiêu chí 1]
  - [tiêu chí 2]
  - [tiêu chí 3]
```
</acceptance_criteria>

<examples>
[Ví dụ request/response hoặc pattern đúng — bọc outer tag nếu dùng XML]
</examples>
```

---

## 9. Anti-patterns — Những sai lầm phổ biến cần tránh

```yaml
anti_patterns:
  flat_markdown_narrative:
    problem: "Toàn bộ file viết bằng Markdown prose, trộn rule với giải thích với example"
    fix: "Tách YAML block cho policy, XML cho examples, Markdown chỉ dùng cho explanation"

  yaml_prose_overload:
    problem: "YAML nhồi prose dài → mất lợi thế schema, khó đọc và bảo trì"
    fix: "Chỉ dùng YAML cho key-value ngắn gọn; giải thích sang Markdown"

  xml_micro_tagging:
    problem: "Bọc XML quanh từng dòng/bullet → token overhead cao, tag mất ý nghĩa"
    fix: "XML chỉ bọc outer block; không micro-tag nội dung bên trong"

  inconsistent_schema_keys:
    problem: "Hôm nay must_not, ngày mai avoid, hôm khác never_do → agent không học được pattern"
    fix: "Chọn một schema key (xem mục 4) và dùng NHẤT QUÁN toàn project"

  oversized_root_guide:
    problem: "Root guide >3000 tokens, chứa L2+L3 thay vì chỉ L0+L1"
    fix: "Tách L2→docs/, L3→specs/examples/; root chỉ giữ L0 + navigation map"

  no_delimiter_between_context_and_instruction:
    problem: "Dữ liệu tham chiếu (docs, logs, user input) không được phân cách → bị nhầm là lệnh"
    fix: "Dùng XML <context> hoặc <input> bọc dữ liệu tham chiếu"

  mixing_task_context_with_root_guide:
    problem: "Spec/ticket cụ thể được nhét vào root guide → phình to, giảm tuân thủ"
    fix: "Task context đi cùng prompt mỗi phiên, không lưu trong root"
```

---

## 10. Định nghĩa hoàn thành (Definition of Done)

Một file Markdown đạt chuẩn khi thỏa tất cả:

```yaml
definition_of_done:
  source_fidelity:
    - giữ nguyên ý nghĩa gốc, không bịa đặt requirement
    - đánh dấu assumption rõ ràng nếu có

  structure:
    - tách instruction, context, examples, output_contract đúng cách
    - dùng Markdown cho explanation
    - dùng YAML cho policy/schema
    - dùng XML-like tags cho semantic boundaries

  layer_discipline:
    - L0 chỉ ở root guide (CLAUDE.md)
    - L1 ở .hermes/rules/ — gọi theo scope
    - L2 ở docs/architecture, docs/domains — nạp khi cần
    - L3 ở specs/, examples/ — nạp theo task

  token_awareness:
    - root guide ≤1800-3000 tokens (vùng tốt đến warning)
    - markdown section ≤900-1800 tokens
    - yaml block ≤700-1200 tokens
    - xml dùng outer boundary, không micro-tag

  agent_usability:
    - chứa priority_order khi có nhiều hơn 1 constraint
    - chứa must/must_not khi có hard rules
    - chứa acceptance_criteria hoặc validation_checklist
    - có working map / routing để agent biết nạp thêm gì

  maintainability:
    - con người có thể đọc và chỉnh sửa mà không cần hướng dẫn thêm
    - mỗi file có một vai trò rõ ràng, không trộn quá nhiều loại thông tin
```

---

## Tóm tắt nhanh

```text
Markdown  → giải thích, rationale, overview, walkthrough
YAML      → constraints, policy, checklist, output_contract, routing
XML tags  → phân cách instruction / context / examples / input / task

Luật nền (L0) → root guide, luôn nạp
Policy (L1)    → .hermes/rules/, nạp theo scope
Domain (L2)    → docs/, nạp khi cần
Evidence (L3)  → specs/, examples/, nạp theo task

Token budget: root guide ≤1800-3000 | MD section ≤900-1800 | YAML block ≤700-1200
```
