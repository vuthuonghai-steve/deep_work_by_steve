# Session Tổng Kết — Cải Tiến Skill Suite với Format Knowledge

> **Date**: 2026-05-18
> **Workspace**: `/home/steve/Work-space/deep_work_by_steve`
> **Target**: `skills/rebuild/skill-architect`
> **Mục tiêu**: Embed format knowledge (YAML/XML/Token/Trace) vào bộ 3 skill để AI agent output đúng chuẩn

---

## 1. ROOT CAUSE ĐÃ XÁC ĐỊNH

**Vấn đề**: Skill tạo ra bởi bộ 3 skill (skill-architect → skill-planner → skill-builder) không đạt chất lượng:
- AI agent ảo giác, làm sai
- Không dùng XML tags (`<instructions>`, `<context>`, `<output_contract>`)
- Không dùng YAML blocks (`must:`, `must_not:`, `priority_order:`)
- Không dùng trace tags (`[TỪ DESIGN §N]`)
- Token budget bị phớt lờ

**Root cause**: Format knowledge từ `/CLAUDE.md` (LLM Knowledge Activation Documentation Standard) bị cô lập — KHÔNG được reference trong bộ 3 skill. Agent không có kiến thức về cách chọn format, semantic anchors, hay token budget.

---

## 2. FORMAT KNOWLEDGE ĐÃ NHÚNG (từ CLAUDE.md)

### 2.1 Ba loại format và vai trò

| Format | Dùng cho | Tránh dùng cho |
|--------|----------|----------------|
| **Markdown** | Explanation, rationale, overview, examples | Hard rules, policy blocks |
| **YAML** | Constraints, policies, checklists, output contracts | Long prose, complex narrative |
| **XML-like tags** | Semantic boundaries, separating instruction vs context | Micro-tagging, replacing all content |

### 2.2 XML Tags chuẩn

```xml
<instructions>Luật điều khiển hành vi (imperative mode)</instructions>
<context>Dữ liệu tham chiếu, không phải lệnh</context>
<examples>Ví dụ minh họa pattern đúng</examples>
<input>Thông tin người dùng hoặc tài liệu nguồn</input>
<output_contract>Định dạng đầu ra bắt buộc — AI MUST comply</output_contract>
```

### 2.3 YAML Keys chuẩn

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

### 2.4 Semantic Activation Anchors

Những từ khóa TRIGGER mode xử lý đặc biệt trong LLM:

```yaml
imperative: [must, must_not, priority_order, constraints, stop_conditions]
contextual: [context, reference, examples, evidence]
quality: [output_contract, acceptance_criteria, validation_checklist, definition_of_done]
```

### 2.5 Token Budget

```yaml
token_budget:
  L0_limit: 600    # Root guide / SKILL.md boot (150-400 good, 500-700 warning)
  L1_limit: 1500   # Policy files (400-1200 good)
  L2_limit: 2500   # Domain context (600-2500 good)
  enforcement: hard # REJECT if exceeded
```

### 2.6 Trace Tags

```markdown
[TỪ USER INPUT]        # Từ user request — verified
[TỪ DESIGN §N]         # Từ design section N — contract-bound
[TỪ NGUỒN EXTERNAL]    # Từ tài liệu bên ngoài — referenced
[GỢI Ý BỔ SUNG]        # Suy luận của AI — PHẢI flag để user verify
[CẦN LÀM RÕ]           # Chưa rõ — BLOCKER, must resolve
```

### 2.7 4 Lớp tri thức

```yaml
L0_anchor_rules:    # Luật nền, load always, format: Markdown+YAML+XML
L1_working_policy:  # Quy ước làm việc, load frequent, format: YAML+Markdown
L2_domain_context:  # Kiến trúc, domain, load on-demand, format: Markdown
L3_evidence:        # Spec, examples, load task-specific, format: XML+Markdown/YAML
```

---

## 3. THAY ĐỔI ĐÃ THỰC HIỆN

### Vị trí: `skills/rebuild/skill-architect/`

| # | File | Thay đổi | Tác động |
|---|------|----------|----------|
| 1 | **SKILL.md** | Trim 9489→5063 bytes (~2000→~1200 tokens). Thêm `format-standards.md` vào Tier 1 boot. Thêm G7 Format Compliance. Thêm `<output_contract>` tag. | SKILL.md giờ là L0 compact, chỉ routing + guardrails |
| 2 | **knowledge/format-standards.md** | `enforcement: soft→hard`. Thêm `<output_contract>` tag. Thêm §5.1 Semantic Activation Anchors. Thêm §5.2 Format Selection Rules. | Format rules giờ đầy đủ và được enforce |
| 3 | **policy/guardrails.md** | Thêm G7: Format Compliance (`must`/`must_not`/`reject_if`) | Guardrails giờ bao gồm format enforcement |
| 4 | **loop/design-checklist.yaml** | Thêm `[TỪ USER INPUT]` tag. Thêm T3 rule. `trace_validation: SHOULD→MUST` | Machine-readable validation giờ bắt buộc trace |

### Cấu trúc skill sau khi cải tiến:

```
skills/rebuild/skill-architect/
├── SKILL.md (v4.0.0, 5063 bytes) — L0: compact anchor + routing
├── policy/
│   ├── workflow.md — Phase 1-3 detail
│   ├── output-spec.md — Output contract + 10 sections
│   └── guardrails.md — G1-G7 (thêm format compliance)
├── knowledge/
│   ├── format-standards.md — YAML/XML/Token/Trace rules + anchors
│   ├── architect.md — Source attribution + 3 Pillars
│   └── visualization-guidelines.md — Mermaid skeletons
├── loop/
│   ├── design-checklist.md — Human-readable QA
│   └── design-checklist.yaml — Machine-readable (trace: MUST)
├── scripts/
│   └── init_context.py
├── templates/
│   └── design.md.template
└── references/
    └── examples/
```

---

## 4. NHỮNG GÌ CÒN CẦN LÀM

### 4.1 Cần cải tiến tiếp cho skill-architect:
- [ ] Kiểm tra `knowledge/architect.md` — thiếu `<instructions>` tag, chỉ có `<context>`
- [ ] Tạo `references/examples/good-design.md` — ví dụ design.md output chuẩn
- [ ] Tạo `references/examples/bad-design.md` — ví dụ vi phạm format
- [ ] Sync format standards giữa `SKILL.md` và `policy/` files (hiện có overlap)

### 4.2 Cần cải tiến skill-planner (`skills/rebuild/skill-planner/`):
- [ ] Thêm `knowledge/format-standards.md` vào Tier 1 boot
- [ ] Thêm G7 Format Compliance vào guardrails
- [ ] Cập nhật trace tags trong todo.md output (`[TỪ USER INPUT]`, v.v.)
- [ ] Thêm `enforcement: hard` vào token budget

### 4.3 Cần cải tiến skill-builder (`skills/rebuild/skill-builder/`):
- [ ] Thêm `knowledge/format-standards.md` vào Tier 1 boot
- [ ] Thêm G7 Format Compliance vào guardrails
- [ ] `validate_skill.py` — cập nhật để kiểm tra format compliance (XML tags, YAML blocks)
- [ ] Build checklist — thêm format compliance items

### 4.4 Cần đồng bộ giữa các vị trí skill:
- `skills/rebuild/` ← **đang làm việc** (đã cập nhật)
- `.claude/skills/` ← bản cũ (cần sync hoặc xóa)
- `~/.claude/skills/` ← bản global của Claude Code (cần sync)
- `.hermes/skills/` ← bản Hermes (có thể outdated)

---

## 5. KIẾN TRÚC TỔNG THỂ

```
CLAUDE.md (Format Knowledge Source)
    │
    ├──→ skills/rebuild/skill-architect/knowledge/format-standards.md (EMBEDDED)
    │       └──→ SKILL.md (Tier 1 boot, enforcement: hard)
    │
    ├──→ skills/rebuild/skill-planner/ (CHƯA UPDATE)
    │
    └──→ skills/rebuild/skill-builder/ (CHƯA UPDATE)

Pipeline: architect → [design.md] → planner → [todo.md] → builder → [skill files]
```

---

## 6. KEY TAKEAWAY CHO SESSION MỚI

1. **Format knowledge đã được embed** vào `skills/rebuild/skill-architect/knowledge/format-standards.md`
2. **Enforcement đã được bật** (`enforcement: hard` trong cả SKILL.md và format-standards.md)
3. **Trace validation đã nâng lên MUST** (không còn SHOULD)
4. **Cần update skill-planner và skill-builder** với cùng format standards
5. **Luôn đọc toàn bộ skill** (không chỉ SKILL.md) trước khi sửa — mỗi file có vai trò riêng
6. **SKILL.md là L0** (compact anchor) — detail ở policy/ và knowledge/ files
