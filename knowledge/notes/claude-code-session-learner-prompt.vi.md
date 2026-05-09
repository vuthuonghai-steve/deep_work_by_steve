# Prompt cho Claude Code: Học từ session-learner skill

## Mục tiêu

Dùng `session-learner` skill để trích xuất và đóng gói kiến thức từ session làm việc hiện tại.

---

## Prompt chuẩn cho Claude Code

```
Hãy đọc skill tại:
`/home/steve/Work-space/deep_work_by_steve/skills/rebuild/session-learner/SKILL.md`

Sau đó thực hiện theo workflow của skill này để trích xuất kiến thức từ session hiện tại.

**Quy trình:**
1. Đọc `knowledge/session-extraction.md` — hướng dẫn trích xuất
2. Đọc `templates/knowledge-entry.template` — format output
3. Đọc `loop/learn-checklist.md` — quality gate
4. Scan session hiện tại để tìm insights, lessons learned, patterns, commands, decisions
5. Áp dụng template và ghi vào knowledge base

**Lưu ý:**
- Chỉ trích xuất giá trị — không phải mọi thứ đều worth saving
- Ghi WHY, không chỉ WHAT
- Kiến thức phải actionable
- Ưu tiên unique insights
```

---

## Cách dùng với prompt-cleaner

Nếu muốn clean prompt hơn nữa, dùng:

```
/skill prompt-cleaner

Prompt: Trích xuất kiến thức từ session hiện tại dùng session-learner skill tại /home/steve/Work-space/deep_work_by_steve/skills/rebuild/session-learner/
```

---

## Các file cần đọc của session-learner

| File | Vai trò |
|------|---------|
| `SKILL.md` | Persona, workflow, guardrails |
| `knowledge/session-extraction.md` | Extraction guidelines |
| `templates/knowledge-entry.template` | Output format |
| `loop/learn-checklist.md` | Quality gate checklist |

---

## Knowledge Base Structure

```
/home/steve/Work-space/deep_work_by_steve/knowledge/
├── experience/       # Personal lessons, insights
├── projects/          # Project-specific knowledge  
├── notes/             # Quick notes, ideas
├── programming/       # Technical patterns
└── resources/         # References, links
```

---

## Key Insights từ session này

### Keywords đạt được kết quả:

1. **parallel delegation** — orchestrator spawns multiple agents simultaneously
2. **YAML-first validation** — frontmatter as canonical contract
3. **Hermes-native paths** — `~/.hermes/skills/` vs `~/.claude/skills/`
4. **operation_type enum** — 6 types (create_new, patch_existing, refactor_existing, migrate_platform, consolidate_skills, deprecate_skill)
5. **execution_mode** — 3 modes (lightweight, standard, strict)
6. **install_target resolution** — 4 priority levels
7. **refinement_loop** — 6-step continuous improvement
8. **progressive_disclosure tiering** — 3-tier skill loading

---

## Sử dụng với CLAUDE.md

Thêm vào `CLAUDE.md` trong project:

```markdown
## Session Learning

Khi user yêu cầu "học từ session", "trích xuất kiến thức", "lưu vào knowledge":
- Đọc skill: `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/session-learner/SKILL.md`
- Thực hiện SCAN → EXTRACT → WRITE → VERIFY workflow
- Output vào: `/home/steve/Work-space/deep_work_by_steve/knowledge/{category}/`
```