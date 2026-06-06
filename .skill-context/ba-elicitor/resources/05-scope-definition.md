---
scope_for: "ba-elicitor (MS-1)"
source: "exploration.md §6.1 + ba-elicitor-analysis.md §6"
confidence: "85%"
---

## Entry Point

**Skill**: ba-elicitor — Tầng Tư duy, filter đầu tiên của pipeline Stage -1. [TỪ exploration §3.3]

**Trigger**: User gửi raw text về skill cần tạo.
**Boot sequence**: `SKILL.md` → knowledge/mindset-keywords.md → knowledge/elicitation-rules.md

## Input Contract

- **Format**: Free-text hoặc structured YAML, bọc trong `<user_skill_request>`
- **Source**: User direct input
- **Schema tham chiếu**: `file:///home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-business-analyst/ba-elicitor/data/input-schema.yaml`

## Output Contract

- **File**: `elicitation-report.md` tại `.skill-context/skill-business-analyst/` [TỪ analysis §6.2]
- **Format**: Markdown + YAML Frontmatter
- **Required sections**: frontmatter, normalized_input, gap_analysis, elicitation_questionnaires, initial_impact_assessment, self_verification_checklist
- **Trace tags**: `[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`

## Dependencies

| File | Vai trò | Bắt buộc |
|------|---------|----------|
| SKILL.md | Core persona + phases | ✅ |
| knowledge/mindset-keywords.md | 6 keywords + vector anchors | ✅ |
| knowledge/elicitation-rules.md | 5W1H question templates | ✅ |

## Handoff

→ `elicitation-report.md` → **ba-analyst (MS-2)** [TỪ exploration §3.3]

## Risks & Mitigations

| Risk | Level | Mitigation |
|------|-------|------------|
| Input quá mơ hồ → ko normalize được | **Cao** | Confidence < 60% → dừng, sinh câu hỏi HITL |
| Prompt Injection qua input | **Cao** | XML boundary `<user_skill_request>` |
| Hallucination — tự bịa chi tiết | **Med** | Trace tags bắt buộc, [SUY LUẬN] ≠ [TỪ INPUT] |
| Context overflow | **Med** | Progressive Disclosure: chỉ nạp knowledge per phase |

## Quality Checklist

- [ ] XML boundary enforced (`<user_skill_request>`)
- [ ] ≥3 [CẦN LÀM RÕ] tags nếu input mơ hồ
- [ ] 5W1H questionnaire đầy đủ
- [ ] Confidence score trong frontmatter
- [ ] Zero placeholder trong output
