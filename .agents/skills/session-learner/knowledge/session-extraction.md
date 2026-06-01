# Session Extraction Guide v2.0

Hướng dẫn cách trích xuất kiến thức từ session chat — tối ưu cho 1-PASS execution.

---

## Core Principles

1. **1-PASS execution** — Scan → Extract → Write → Verify trong 1 lần, không pause giữa các bước
2. **Auto-categorization** — Không hỏi user, tự động detect category từ content
3. **Parallel extraction** — Nếu session có nhiều categories, extract song song
4. **Session-specific naming** — Format `YYYY-MM-DD.{session-name}.md`

---

## Categories & Auto-Detection

### `experience/` — Personal Lessons

**Keywords trigger:** mistake, learned, insight, discovery, aha, phát hiện, hiểu rồi, workflow cũ/không tốt

**What to extract:**
- Mistake + Fix pairs: "Tôi đã sai ở chỗ X, cách sửa là Y"
- Discoveries: "Tôi phát hiện ra rằng X"
- Insights: "X có vẻ đúng, nhưng thực ra Y mới đúng"
- Workflow improvements: "Cách cũ X không tốt, cách mới Y hiệu quả hơn"

### `projects/` — Project Knowledge

**Keywords trigger:** project, architecture, ADR, decision, design, setup, config

**What to extract:**
- Architecture decisions: "Chọn X thay vì Y vì Z"
- Technical approaches: "Cách implement feature này là..."
- Gotchas: "Cẩn thận X — nó gây ra Y"
- Dependencies: "Cần X trước khi làm Y"

### `notes/` — Quick Notes

**Keywords trigger:** todo, reminder, question, idea, thử, câu hỏi

**What to extract:**
- TODO items: "Cần làm X"
- Questions: "Tại sao X lại hoạt động như vậy?"
- Ideas: "Thử X xem sao"
- Reminders: "X — đừng quên"

### `programming/` — Technical Patterns

**Keywords trigger:** pattern, command, code, tool, function, script, algorithm

**What to extract:**
- Commands: "Lệnh `X` làm Y"
- Patterns: "Pattern X giải quyết vấn đề Y"
- Tool usage: "Cách dùng tool X hiệu quả"
- Code snippets: "Đoạn code này làm X"

### `resources/` — References

**Keywords trigger:** link, url, doc, documentation, reference

**What to extract:**
- URLs: "Link này hữu ích cho X"
- Documentation: "Doc của X có section về Y"
- Tools: "Tool X hữu ích cho Y"

---

## Parallel Extraction Pattern

### When to Use

Khi session chứa content thuộc **2+ categories**, sử dụng parallel extraction:

```
Session có content:
  - experience/ (insights về delegation pattern)
  - programming/ (technical patterns về YAML frontmatter)
  → Extract 2 files song song
```

### Implementation

```python
# 1. Scan session → collect all candidates
# 2. Detect unique categories từ candidates
# 3. Nếu categories > 1:
#      delegate_task per category (parallel)
#    Else:
#      extract directly (single pass)
```

### Example Output Structure

**File 1:** `knowledge/experience/2026-05-09.skill-suite-v3-upgrade-learnings.md`
**File 2:** `knowledge/programming/2026-05-09.hermes-skill-v3-patterns.md`
**File 3:** `knowledge/projects/2026-05-09.skill-suite-v3-upgrade.md`

---

## Quality Checklist (Automated)

- [ ] Session có nội dung để extract
- [ ] Đã xác định category phù hợp
- [ ] Filename đúng format `YYYY-MM-DD.{session-name}.md`
- [ ] Knowledge folder tồn tại (auto-create nếu không)
- [ ] Không trùng lặp với file có sẵn (auto-append `_v2` nếu trùng)
- [ ] Markdown syntax đúng
- [ ] Không có placeholder chưa fill (`{...}`)
- [ ] File size <100KB
- [ ] Ngữ cảnh đầy đủ để hiểu sau này
- [ ] Tiêu đề mô tả rõ nội dung

---

## Anti-Patterns

| ❌ Don't Extract | ✅ Do Instead |
|-----------------|--------------|
| Generic info có sẵn ở docs | Chỉ extract nếu có context cụ thể |
| Nội dung quá dài (>500 words) | Tóm tắt, giữ essence |
| Duplicate kiến thức đã có | Check trước, skip nếu trùng |
| Opinion mà không có basis | Ghi rõ đây là opinion, không phải fact |
| Fragment không đủ context | Bỏ qua, không force extract |

---

## Session-Specific Naming

**Format:** `YYYY-MM-DD.{session-name}.md`

**Examples:**
```
2026-05-09.skill-suite-v3-upgrade.md
2026-05-08.docker-debugging-session.md
2026-05-07.architecture-design-review.md
2026-05-06.telegram-bot-setup.md
```

**How to derive session-name:**
1. Lấy topic/keyword chính từ session
2. Lowercase
3. Hyphenate spaces
4. Nếu trùng → append `_v2`, `_v3`, etc.

---

## Source

Adapted from: session-learner v1.0
Session: skill-suite-v3-upgrade (2026-05-09)
Pattern: 1-PASS execution with parallel extraction