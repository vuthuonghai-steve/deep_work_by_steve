---
description: Chuẩn format đầu ra cho file Markdown trong workspace — phục vụ AI agent và người đọc.
---

# Output Format Rules

## Nguyên tắc nền tảng

- Format tốt nhất là format giúp mô hình trả lời nhanh: đâu là lệnh, đâu là tham chiếu, đâu là ví dụ.
- Tách rõ: luật (rule) vs giải thích (context) vs ví dụ (examples) vs tiêu chí (acceptance).
- Ưu tiên YAML cho ràng buộc, Markdown cho giải thích, XML cho ranh giới ngữ nghĩa khi cần.

---

## Chọn đúng format

**Markdown** — dùng cho:
- overview, rationale, architecture explanation
- onboarding, walkthrough, decision notes
- bảng so sánh, ví dụ có ngữ cảnh

**YAML block** — dùng cho:
- constraints, policies, checklists
- must / must_not / should / should_not
- output_contract, acceptance_criteria, priority_order
- allowed_tools, forbidden_patterns, stop_conditions

**XML-like tags** — dùng làm ranh giới khối lớn:
- `<task>` — mô tả tác vụ
- `<context>` — dữ liệu tham chiếu
- `<instructions>` — luật điều khiển hành vi
- `<constraints>` — ràng buộc phạm vi
- `<acceptance_criteria>` — tiêu chí nghiệm thu
- `<examples>` — ví dụ minh họa

---

## Schema key chuẩn cho YAML

Dùng nhất quán toàn project. Không dùng nhiều biến thể cho cùng một ý nghĩa.

```
must           → hành động bắt buộc
must_not       → hành động cấm
should         → khuyến nghị mạnh
should_not     → khuyến nghị tránh
scope          → phạm vi áp dụng
priority_order → thứ tự ưu tiên khi xung đột
output_contract → hình thức đầu ra bắt buộc
acceptance_criteria → tiêu chí nghiệm thu
stop_conditions   → điều kiện dừng
load_when_needed  → bản đồ nạp context
```

---

## Token budget — ngưỡng vận hành

| Khối | Tốt | Cảnh báo | Nên tách |
|---|---|---|---|
| Root guide (L0) | 300-900 tokens | 900-1800 | >1800 |
| YAML block | 80-300 | 300-700 | >700 |
| Markdown section | 100-400 | 400-900 | >900 |

---

## Phân lớp tài liệu

- **L0** — Luật nền, non-negotiables → `CLAUDE.md` / `AGENT.md`
- **L1** — Policy, coding rules → `.claude/rules/`
- **L2** — Kiến trúc, domain docs → `docs/`
- **L3** — Spec, examples, tickets → `specs/`, `examples/`

Root guide chỉ chứa L0 + phần cô đọng nhất của L1. Không nhét L2/L3 vào root.

---

## Task context template

Khi spec/ticket/log đi kèm prompt:

```markdown
<task>
[Mô tả tác vụ]
</task>

<constraints>
- must: [...]
- must_not: [...]
</constraints>

<acceptance_criteria>
- [...]
</acceptance_criteria>

<examples>
[ví dụ minh họa]
</examples>
```

---

## Tránh các sai lầm phổ biến

- **Flat markdown narrative** — trộn rule với giải thích với example trong cùng một block. Fix: tách YAML cho policy, Markdown cho explanation.

- **YAML nhồi prose dài** — mất lợi thế schema. Fix: YAML chỉ cho key-value ngắn gọn.

- **XML micro-tagging** — bọc từng dòng/bullet bằng tag. Fix: XML chỉ cho outer block, không vi mô.

- **Schema key không nhất quán** — hôm nay `must_not`, ngày mai `avoid`, hôm khác `never_do`. Fix: chọn một key và dùng xuyên suốt.

- **Root guide phình to** — chứa L2/L3 thay vì chỉ L0/L1. Fix: tách domain docs, spec, examples ra file riêng.

---

## Cấu trúc root guide chuẩn

```markdown
# Project Agent Guide

## Purpose
[Project, domain, định nghĩa thành công]

## Core Policy
[```yaml
priority_order: [...]
constraints:
  must: [...]
  must_not: [...]
output_contract: [...]
```]

## Working Map
[```yaml
load_when_needed:
  backend_rules: ".claude/rules/backend.md"
  output_format_rules: ".claude/rules/output-format.md"
```]

## Interaction Protocol
[Bước trước/sau khi sửa — inspect → scope → edit → validate]
```
