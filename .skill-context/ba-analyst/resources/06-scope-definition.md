# Scope Definition — ba-analyst (Context-Before-Fix)

## Entry Point

- SKILL.md tại `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-business-analyst/ba-analyst/SKILL.md` [TỪ analysis §5]

## Input Contract (từ ba-elicitor) [TỪ analysis §6.1]

Tệp `elicitation-report.md` gồm:
1. YAML Frontmatter: skill_name, elicited_by, elicited_at, status ("completed" / "pending_clarification")
2. Part 1: User Request Overview
3. Part 2: Normalized Requirements
4. Part 3: Identified Gaps & Ambiguities (kèm [CẦN LÀM RÕ] tags)
5. Part 4: Actors and Systems

## Output Contract (cho ba-synthesizer) [TỪ analysis §6.2]

Tệp `analysis-report.md` với 7 deliverables: Classification Table, 3 Mermaid Diagrams, Data Schema, Gherkin, Risk Matrix, Traceability Map.

## Cross-Reference: Elicitor → Analyst Handoff [TỪ elicitor §6]

### Phân tích khớp/nợ:

| Elicitor Output Field | Analyst Input Expected | Khớp? |
|-----------------------|----------------------|-------|
| `analyzed_at` | `elicited_at` | **LỆCH TÊN** — elicitor dùng `analyzed_at`, analyst expect `elicited_at` |
| status: "elicitation-completed" | status: "completed" | **LỆCH GIÁ TRỊ** — khác enum value |
| Actor mapping (từ 5W1H who) | Part 4: Actors & Systems | **KHỚP** (suy luận) |
| Gap Analysis & Ambiguities | Part 3: Identified Gaps | **KHỚP** |
| Elicitation Questionnaires | Không map rõ | **RỦI RO** — không có section tương ứng trong analyst input schema |

### Rủi ro Handoff:

1. **Frontmatter field mismatch:** `analyzed_at` vs `elicited_at` — có thể gây parse lỗi [TỪ elicitor §6.2 → analysis §6.1]
2. **Status enum mismatch:** elicitor xuất "elicitation-completed" nhưng analyst expect "completed" — cần align [TỪ elicitor §6.2 → analysis §6.1]
3. **Thiếu Actors section:** elicitor không bắt buộc xuất Actors & Systems section riêng (chỉ trong 5W1H) — analyst có thể thiếu dữ liệu [TỪ elicitor §3.2 → analysis §6.1]
4. **Elicitation Questionnaires bị bỏ qua:** analyst input schema không map section này — thông tin khảo sát có thể mất [TỪ elicitor §6.2 → analysis §6.1]

### Mitigation:

- Thêm normalization step trong analyst: tự động align field names trước khi xử lý
- Nếu elicitor status là "pending", analyst chuyển thẳng output status thành "pending_clarification" và dừng pipeline

### Dependencies on Knowledge Files [TỪ analysis §3]

| File | Đường dẫn | Mục đích |
|------|-----------|----------|
| classification-rules.md | `skills/rebuild/skill-business-analyst/ba-analyst/knowledge/classification-rules.md` | FR/NFR + MoSCoW |
| mermaid-syntax.md | `skills/rebuild/skill-business-analyst/ba-analyst/knowledge/mermaid-syntax.md` | Diagram syntax rules |
| gherkin-guide.md | `skills/rebuild/skill-business-analyst/ba-analyst/knowledge/gherkin-guide.md` | Gherkin writing standard |
| risk-assessment.md | `skills/rebuild/skill-business-analyst/ba-analyst/knowledge/risk-assessment.md` | Risk assessment framework |

### Risks & Mitigations [TỪ analysis §7]

- **R-1 (High):** Lỗi Mermaid syntax → syntax_validator.py + quote wrapping
- **R-2 (High):** Scope creep do tự suy đoán → Simplicity First + tag [CẦN LÀM RÕ]
- **R-3 (Medium):** Traceability loss → trace tags bắt buộc mọi entity
- **R-4 (Medium):** Context overflow → Progressive Disclosure

### Confidence Assessment

- Nguồn tài liệu analysis đã hoàn chỉnh (Definition of Done đạt 5/5) [TỪ analysis §9]
- Handoff contract có 3 mismatch đã phát hiện → cần align trước production
- **Confidence:** 85% (thiếu alignment elicitor→analyst frontmatter)
