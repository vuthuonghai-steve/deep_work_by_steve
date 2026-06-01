---
name: session-learner
description: 'Khai thác và học hỏi kinh nghiệm từ session chat hiện tại. Đóng gói thành markdown và ghi vào knowledge base của dự án. Trigger: "học từ session", "trích xuất kiến thức", "lưu vào knowledge".'
category: meta
version: "2.0.0"
pipeline:
  stage_order: standalone
  input_contract:
    - type: env
      name: CURRENT_SESSION
      description: Session context hiện tại
      required: false
  output_contract:
    - type: file
      path: "{knowledge_path}/{category}/{filename}.md"
      format: markdown
  dependencies: []
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
  tier2:
    - path: "knowledge/session-extraction.md"
      base: "skill_dir"
      load_when: "Auto-loaded at start"
    - path: "templates/knowledge-entry.template"
      base: "skill_dir"
      load_when: "Step WRITE"
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG**
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Hệ thống **KHÔNG** tự động nạp các file khác.
> Tier 1 = SKILL.md (mandatory). Tier 2 = Auto-loaded at start.

---

# Session Learner v2.0

## Mission

Act as a **Knowledge Harvester**. Scan the current session chat, extract valuable insights, lessons learned, patterns, and knowledge, then package them into well-structured markdown files and save to the project's knowledge base.

**Tối ưu hóa:** Thay vì nhiều bước riêng biệt với interaction gates, skill này chạy **1-PASS** — scan → extract → write → verify trong 1 lần chạy duy nhất. Không hỏi user trừ khi cần xác nhận overwrite.

## Hardcoded Configuration

```
Knowledge Base Path: /home/steve/Work-space/deep_work_by_steve/knowledge/
Allowed Categories: experience, projects, notes, programming, resources
Session Date Format: YYYY-MM-DD
```

## 1-PASS Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     1-PASS KNOWLEDGE EXTRACTION                     │
├─────────────────────────────────────────────────────────────────────┤
│  SCAN → EXTRACT → WRITE → VERIFY → DELIVER (không dừng giữa các bước) │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 1: SCAN (scan toàn bộ session)

Scan messages từ đầu session, collect tất cả candidates:

- 🔍 Problem-solving exchanges
- 💡 Lightbulb moments ("aha!", "tôi hiểu rồi", "phát hiện")
- ⚠️ Warnings or cautions
- ✅ Confirmations of approach
- 🔧 Tool or command usage
- 📚 Explanations or teaching moments
- 🔄 Workflow improvements discovered
- 🎯 Decisions made with reasoning

### Step 2: EXTRACT (categorize và structure)

Đọc `knowledge/session-extraction.md` để apply extraction guidelines. Tự động detect category và generate filename.

**Category Detection:**
```
- experience/  — Personal lessons, mistakes, discoveries
- projects/    — Project-specific knowledge, ADRs, architecture
- notes/       — Quick notes, ideas, reminders, TODOs
- programming/ — Technical patterns, commands, tool usage
- resources/   — URLs, docs, references
```

**Filename Generation (Session-Specific Naming):**
```
Format: YYYY-MM-DD.{session-name}.md
Example: 2026-05-09.skill-suite-v3-upgrade.md

session_name = sanitize(topic/keyword từ session)
                → lowercase
                → hyphenated
                → unique trong category folder
```

**Auto-categorization Rules:**
- Nếu content chứa "mistake", "learned", "insight" → `experience/`
- Nếu content chứa "project", "architecture", "ADR" → `projects/`
- Nếu content chứa "pattern", "code", "technical" → `programming/`
- Nếu content quá ngắn hoặc fragment → `notes/`
- Nếu content chỉ là link hoặc reference → `resources/`

### Step 3: WRITE (parallel extraction cho multiple entries)

**CRITICAL: Sử dụng parallel extraction pattern**

Đối với session có nhiều categories, spawn sub-agents để extract song song:

```python
# Pseudo-code for parallel extraction
categories = detect_categories_from_scanned_content)
if len(categories) > 1:
    # Spawn delegate_task cho mỗi category
    for category in categories:
        delegate_task(
            goal=f"Extract knowledge from session for category: {category}",
            context=full_session_context
        )
else:
    # Single category — extract trực tiếp
    extract_single_category(session, category)
```

**Entry Structure:**
```
# {Title}

**Extracted from:** {session_id}
**Date:** {YYYY-MM-DD}
**Category:** {category}

---

## Overview
{brief_description}

---

## Key Insights
### Insight N
**What:** {what}
**Why:** {why_matters}
**Context:** {when_where}

---

## Lessons Learned
### Lesson N
**Situation:** {what_happened}
**Learning:** {what_we_learned}
**Action:** {what_to_do_different}

---

## Related
- [[related knowledge entry]]

---

## Source
Session: {session_id}
```

### Step 4: VERIFY (quality gate)

Tự động check, không cần user confirm:

- [ ] File không trùng với file có sẵn (check trước khi write)
- [ ] Markdown syntax đúng
- [ ] Không có placeholder chưa fill (`{...}`)
- [ ] File size <100KB
- [ ] Ngữ cảnh đầy đủ để hiểu sau này
- [ ] Filename đúng format `YYYY-MM-DD.{session-name}.md`

### Step 5: DELIVER (auto-deliver)

Tự động deliver kết quả cho user:

```
✅ Đã ghi vào: knowledge/{category}/{filename}.md

Nội dung đã trích xuất:
- {count} insights
- {count} lessons learned
- {count} patterns
- {count} related entries

Files created:
- knowledge/{cat1}/{filename1}.md
- knowledge/{cat2}/{filename2}.md
```

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | **No Overwrite** | Nếu file tồn tại, tự động append `_v2`, `_v3` |
| G2 | **Size Limit** | Warn nếu content >100KB, tự động split nếu cần |
| G3 | **Validate MD** | Ensure valid markdown trước khi write |
| G4 | **Scan Full Session** | Scan toàn bộ session, không giới hạn 50 messages |
| G5 | **Category Check** | Verify target category folder exists trước write |

## Error Handling

| Situation | Action |
|-----------|--------|
| Knowledge folder not found | Create category folder automatically |
| File already exists | Auto-append `_v2`, `_v3`, etc. |
| Session empty | Report: "No content to extract" và exit |
| Invalid markdown | Fix syntax trước khi write |
| Duplicate content | Skip, ghi warning vào output |

## Session-Specific Naming Convention

**Format:** `YYYY-MM-DD.{session-name}.md`

**Rules:**
1. Date = ngày session diễn ra (from conversation metadata)
2. session_name = keyword/topic chính của session, lowercase, hyphenated
3. Nếu trùng tên trong folder → append `_v2`, `_v3`, etc.

**Examples:**
```
2026-05-09.skill-suite-v3-upgrade.md
2026-05-08.docker-debugging-session.md
2026-05-07.architecture-design-review.md
```

## Related Skills

- **skill-architect** — Design new skills
- **skill-builder** — Build skill packages