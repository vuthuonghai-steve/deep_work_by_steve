---
title: "Design: Install Target Resolution"
date: 2026-05-09
version: 1.0.0
status: draft
authors:
  - pipeline-steve
tags:
  - skill-installation
  - resolution
  - platform
  - scope
  - hermes
  - claude
---

# Install Target Resolution

## 1. Tổng quan

Tài liệu này mô tả cơ chế **Install Target Resolution** — quyết định skill được cài đặt vào đâu khi có yêu cầu cài đặt. Hệ thống hỗ trợ 4 mức ưu tiên và 2 platform chính.

---

## 2. Decision Tree — 4 Priority Levels

```
Install Request
      │
      ▼
┌─────────────────────────┐
│ 1. HERMES_USER_LOCAL    │  ← Ưu tiên cao nhất
│    ~/.hermes/skills/    │
└───────────┬─────────────┘
            │ not found / explicit skip
            ▼
┌─────────────────────────┐
│ 2. HERMES_PROJECT_LOCAL │
│    ./.hermes/skills/    │
└───────────┬─────────────┘
            │ not found / explicit skip
            ▼
┌─────────────────────────┐
│ 3. REPO_LOCAL           │
│    ~/.claude/skills/    │
└───────────┬─────────────┘
            │ not found / explicit skip
            ▼
┌─────────────────────────┐
│ 4. CLAUDE_USER_LOCAL    │  ← fallback cuối cùng
│    ~/.claude/skills/    │
└─────────────────────────┘
```

### Priority Order (cao → thấp)

| Level | Tên | Mô tả |
|-------|-----|-------|
| 1 | `HERMES_USER_LOCAL` | User-local cho Hermes (mặc định) |
| 2 | `HERMES_PROJECT_LOCAL` | Project-local cho Hermes |
| 3 | `REPO_LOCAL` | Repo-local (legacy Claude) |
| 4 | `CLAUDE_USER_LOCAL` | User-local cho Claude (fallback) |

---

## 3. Platform vs Scope Matrix

### Platform

| Platform | Mô tả | Root path |
|----------|-------|-----------|
| **Hermes** | Nền tảng agent-based của project | `~/.hermes/` |
| **Claude** | Native Claude Code platform | `~/.claude/` |

### Scope

| Scope | Mô tả | Lưu trữ |
|-------|-------|---------|
| **USER_LOCAL** | Cài đặt cho toàn bộ user | Per-user, shared across all projects |
| **PROJECT_LOCAL** | Cài đặt trong project hiện tại | Trong thư mục project (`./.hermes/`) |
| **REPO_LOCAL** | Cài đặt trong repo (legacy) | Trong thư mục repo (`./.claude/`) |

### Matrix

| | USER_LOCAL | PROJECT_LOCAL | REPO_LOCAL |
|---|:----------:|:-------------:|:----------:|
| **Hermes** | ✅ `~/.hermes/skills/` | ✅ `./.hermes/skills/` | N/A |
| **Claude** | ✅ `~/.claude/skills/` | N/A | ✅ `./.claude/skills/` |

---

## 4. Path Templates

### Hermes Platform

```
~/.hermes/skills/{category}/{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
└── loop/

./.hermes/skills/{category}/{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
└── loop/
```

### Claude Platform

```
~/.claude/skills/{category}/{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
└── loop/

./.claude/skills/{category}/{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
└── loop/
```

---

## 5. Examples

### Example 1: Hermès User-Local (mặc định)

```
~/.hermes/skills/category/skill-name/
├── SKILL.md
└── ...
```

**Install command:**
```bash
hermes skill install skill-name --category category
# hoặc ngắn gọn
hermes install skill-name
```

### Example 2: Hermes Project-Local

```
/home/steve/Work-space/my-project/.hermes/skills/category/skill-name/
├── SKILL.md
└── ...
```

**Install command:**
```bash
hermes skill install skill-name --category category --target project-local
```

### Example 3: Claude User-Local

```
~/.claude/skills/category/skill-name/
├── SKILL.md
└── ...
```

**Install command:**
```bash
claude skill install skill-name --platform claude
```

### Example 4: Repo-Local (Legacy)

```
/home/steve/Work-space/my-repo/.claude/skills/category/skill-name/
├── SKILL.md
└── ...
```

**Install command:**
```bash
claude skill install skill-name --platform claude --target repo-local
```

---

## 6. Frontmatter Schema cho `install_target`

```yaml
install_target:
  type: string
  enum:
    - hermes_user_local
    - hermes_project_local
    - repo_local
    - claude_user_local
  default: hermes_user_local
  description: |
    Nơi cài đặt skill:
    - hermes_user_local: ~/.hermes/skills/ (mặc định, ưu tiên cao nhất)
    - hermes_project_local: ./.hermes/skills/ (project hiện tại)
    - repo_local: ./.claude/skills/ (legacy, trong repo)
    - claude_user_local: ~/.claude/skills/ (Claude native, fallback cuối)
```

### Full Frontmatter Schema

```yaml
---
name: skill-name
version: 1.0.0
category: category
install_target:
  type: string
  enum:
    - hermes_user_local
    - hermes_project_local
    - repo_local
    - claude_user_local
  default: hermes_user_local
  description: Nơi cài đặt skill trong hệ thống
platform:
  type: string
  enum:
    - hermes
    - claude
  default: hermes
  description: Nền tảng mục tiêu
dependencies:
  type: array
  items:
    type: string
  description: Danh sách skill phụ thuộc
---
```

---

## 7. Resolution Logic (Pseudocode)

```python
def resolve_install_target(requested_target=None, platform=None):
    """
    Quyết định install target cuối cùng dựa trên:
    - requested_target (từ frontmatter hoặc CLI)
    - platform (hermes hoặc claude)
    - project context (có .hermes/ trong project không)
    """

    # 1. Nếu có explicit target, dùng nó
    if requested_target:
        return requested_target

    # 2. Default: hermes_user_local
    return "hermes_user_local"

def get_installation_path(target, platform="hermes"):
    """
    Trả về đường dẫn cài đặt dựa trên target và platform.
    """
    templates = {
        "hermes_user_local":    "~/.hermes/skills/{category}/{skill-name}/",
        "hermes_project_local": "./.hermes/skills/{category}/{skill-name}/",
        "repo_local":           "./.claude/skills/{category}/{skill-name}/",
        "claude_user_local":    "~/.claude/skills/{category}/{skill-name}/",
    }

    return templates.get(target)
```

---

## 8. Compatibility Notes

| Target | Hermes Support | Claude Support | Ghi chú |
|--------|:--------------:|:--------------:|---------|
| `hermes_user_local` | ✅ | ❌ | Mặc định khuyến nghị |
| `hermes_project_local` | ✅ | ❌ | Cần `.hermes/` trong project |
| `repo_local` | ❌ | ✅ | Legacy, dùng `.claude/` |
| `claude_user_local` | ❌ | ✅ | Claude native fallback |

---

## 9. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-09 | Initial draft |
