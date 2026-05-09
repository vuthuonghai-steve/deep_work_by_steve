# Research: Agent Skill Validation Patterns

**Ngày:** 2026-05-09  
**Chủ đề:** Skill Validation Patterns cho Agent Frameworks  
**Nguồn:** Hermes Agent Documentation, Nous Research, agent frameworks research

---

## 1. Tổng quan Skill Validation Patterns

### 1.1 Định nghĩa

Skill validation patterns là các cơ chế đảm bảo skill được author đúng cách, đáp ứng chuẩn chất lượng, và tương thích với agent framework trước khi được deploy hoặc publish.

### 1.2 Các cấp độ Validation

| Cấp độ | Mục đích | Ví dụ |
|--------|----------|-------|
| **Syntax Validation** | Kiểm tra format, schema | YAML frontmatter, required fields |
| **Semantic Validation** | Kiểm tra ngữ nghĩa, logic | Trigger conditions, procedure steps |
| **Security Validation** | Kiểm tra mã độc, quyền truy cập | Security scanner, dependency check |
| **Quality Validation** | Đánh giá độ hoàn thiện | Progressive disclosure, verification section |

---

## 2. Hermes Agent Skill Validation System

### 2.1 SKILL.md Format với YAML Frontmatter Schema

Hermes Agent sử dụng YAML frontmatter để định nghĩa metadata cho skill:

```yaml
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
author: Your Name
license: MIT
platforms: [macos, linux]  # Optional — restrict to specific OS platforms
metadata:
  hermes:
    tags: [Category, Subcategory, Keywords]
    category: devops
    related_skills: [other-skill-name]
    requires_toolsets: [web]        # Chỉ hiện khi web toolset active
    requires_tools: [web_search]     # Chỉ hiện khi web_search tool available
    fallback_for_toolsets: [browser] # Ẩn khi browser toolset active
    fallback_for_tools: [browser_navigate]
    config:                          # Optional — config.yaml settings
      - key: my.setting
        description: "What this controls"
        default: "value"
        prompt: "Prompt for setup"
---
```

### 2.2 Required Sections trong SKILL.md

Hermes quy định các section bắt buộc:

| Section | Mục đích |
|---------|----------|
| `# When to Use` | Trigger conditions — khi nào agent nên load skill |
| `# Quick Reference` | Bảng commands hoặc API calls thường dùng |
| `# Procedure` | Step-by-step instructions agent tuân theo |
| `# Pitfalls` | Known failure modes và cách xử lý |
| `# Verification` | Cách agent confirm skill đã hoạt động đúng |

### 2.3 Token-Efficient Loading Pattern

Hermes sử dụng 3-level progressive disclosure:

```
Level 0: skills_list() → [{name, description, category}, ...] (~3k tokens)
Level 1: skill_view(name) → Full content + metadata (varies)
Level 2: skill_view(name, path) → Specific reference file (varies)
```

Agent chỉ load full content khi thực sự cần.

---

## 3. Quality Gates cho Skill Authoring

### 3.1 Hermes Skill Guidelines

**3 nguyên tắc cốt lõi:**

1. **No External Dependencies**
   - Skill phải tự chứa tất cả dependencies
   - Không yêu cầu pip install hay npm install
   - Helper scripts được đặt trong `scripts/` directory

2. **Progressive Disclosure**
   - Structure theo 5 section: When to Use, Quick Reference, Procedure, Pitfalls, Verification
   - Người dùng nhìn thấy overview trước, details sau

3. **Include Helper Scripts**
   - Scripts nằm trong `scripts/` directory
   - Callable từ skill procedure
   - Không yêu cầu external dependencies

### 3.2 Security Scanner (Quality Gate cho Hub Skills)

Tất cả skills install qua Hub đều đi qua security scanner:

**Checklist security scanner:**
- **Malware detection** — phát hiện mã độc
- **Dependency vulnerability scan** — kiểm tra known vulnerabilities
- **Permission escalation check** — phát hiện yêu cầu quyền bất thường
- **Data exfiltration patterns** — phát hiện patterns gửi data ra ngoài

### 3.3 Placeholder Scale (Custom Quality Metric)

Dùng trong internal skill development pipeline:

| Điểm Placeholder | Status | Ý nghĩa |
|-----------------|--------|---------|
| < 5 | ✅ | Skill đạt chuẩn |
| 5-9 | ⚠️ | Cần cải thiện |
| 10+ | ❌ | Không đạt, cần rewrite |

---

## 4. Hermes Validator Patterns

### 4.1 Platform-Specific Validation

Skill có thể restrict theo OS platforms:

```yaml
platforms: [macos, linux]  # Valid: macos, linux, windows
```

- Khi set, skill tự động ẩn khỏi system prompt, `skills_list()`, và slash commands trên incompatible platforms
- Nếu omit, skill load trên tất cả platforms

### 4.2 Conditional Activation Validation

Hermes hỗ trợ 4 loại conditional activation:

| Field | Behavior |
|-------|----------|
| `fallback_for_toolsets` | Ẩn khi listed toolsets available. Hiện khi missing. |
| `fallback_for_tools` | Ẩn khi listed tools available. Hiện khi missing. |
| `requires_toolsets` | Hiện khi listed toolsets available. Ẩn khi missing. |
| `requires_tools` | Hiện khi listed tools available. Ẩn khi missing. |

**Ví dụ:** DuckDuckGo skill dùng `fallback_for_toolsets: [web]`:
- Khi có `FIRECRAWL_API_KEY` → web toolset active → DuckDuckGo skill ẩn
- Khi missing API key → web toolset unavailable → DuckDuckGo skill hiện như fallback

### 4.3 Environment Variable Validation

Skills có thể declare required environment variables:

```yaml
required_environment_variables:
  - name: MY_API_KEY
    prompt: "Enter your API key"
    help: "Get one at https://example.com"
    required_for: "API access"
```

- Missing values trigger `setup_needed` state
- Hermes không expose raw secret values cho model
- CLI local session sẽ ask for setup; messaging sessions chỉ show guidance

### 4.4 Credential File Requirements

Skills có thể define required credential files:

```yaml
credentials:
  - path: ~/.config/my-service/credentials.json
    required_for: "API authentication"
```

Khi load, Hermes check file existence → trigger `setup_needed` nếu missing.

---

## 5. Schema Validation cho Skill Metadata

### 5.1 Core Metadata Schema

```json
{
  "type": "object",
  "required": ["name", "description", "version"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "kebab-case skill identifier"
    },
    "description": {
      "type": "string",
      "maxLength": 200,
      "description": "Brief description shown in skill search"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semver format"
    },
    "author": { "type": "string" },
    "license": { "type": "string" },
    "platforms": {
      "type": "array",
      "items": { "enum": ["macos", "linux", "windows"] }
    }
  }
}
```

### 5.2 Hermes-Specific Metadata Schema

```json
{
  "metadata": {
    "hermes": {
      "tags": {
        "type": "array",
        "description": "Category, Subcategory, Keywords"
      },
      "category": {
        "type": "string",
        "description": "Primary category (e.g., devops, mlops, programming)"
      },
      "related_skills": {
        "type": "array",
        "items": { "type": "string" }
      },
      "requires_toolsets": {
        "type": "array",
        "items": { "type": "string" }
      },
      "requires_tools": {
        "type": "array",
        "items": { "type": "string" }
      },
      "fallback_for_toolsets": {
        "type": "array",
        "items": { "type": "string" }
      },
      "fallback_for_tools": {
        "type": "array",
        "items": { "type": "string" }
      },
      "config": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "key": { "type": "string" },
            "description": { "type": "string" },
            "default": { "type": "string" },
            "prompt": { "type": "string" }
          }
        }
      }
    }
  }
}
```

### 5.3 Validation Rules

| Field | Validation Rule |
|-------|----------------|
| `name` | kebab-case, lowercase, numbers và hyphens only |
| `version` | Semver format (x.y.z) |
| `platforms` | Must be subset of [macos, linux, windows] |
| `tags` | Array of strings, used for discovery |
| `category` | Must match existing categories or creates new one |
| `requires_toolsets` | Must reference valid toolset names |
| `fallback_for_toolsets` | Must reference valid toolset names |

---

## 6. Skill Directory Structure Validation

```
~/.hermes/skills/
├── {category}/
│   ├── {skill-name}/
│   │   ├── SKILL.md               # Required
│   │   ├── references/            # Optional docs
│   │   ├── templates/             # Output format templates
│   │   ├── scripts/               # Helper scripts
│   │   └── assets/                # Supplementary files
├── .hub/                           # Skills Hub state
│   ├── lock.json
│   ├── quarantine/                 # Quarantined skills
│   └── audit.log
└── .bundled_manifest
```

**Validation Rules:**
- Mỗi skill phải có `SKILL.md` ở root
- Không được có duplicate skill names trong cùng installation
- External dirs có thể được add qua `skills.external_dirs` config

---

## 7. External Skill Validation

Hermes cho phép scan external directories:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

**Validation rules cho external skills:**
- **Read-only**: External dirs chỉ dùng cho discovery, không edit
- **Local precedence**: Local skill cùng name sẽ override external
- **Full integration**: External skills appear trong system prompt, skills_list, skill_view, và slash commands

---

## 8. Skills Hub Validation Pipeline

### 8.1 Publishing to Hub

1. **Security Scan** — automated malware và vulnerability check
2. **Schema Validation** — verify SKILL.md format và required fields
3. **Category Assignment** — assign vào appropriate category
4. **Index Update** — update Hub index với metadata

### 8.2 Custom Repository Publishing

Skills có thể được serve từ custom endpoint ngoài GitHub:

```yaml
# Trong skill's repo metadata
x-hermes-endpoint: https://your-skill-server.com/skills/
```

---

## 9. So sánh các Agent Framework Validation

### 9.1 Hermes vs Other Frameworks

| Feature | Hermes | LangChain | AutoGPT |
|---------|--------|-----------|---------|
| YAML Frontmatter Schema | ✅ | ❌ | ❌ |
| Security Scanner | ✅ | ❌ | ❌ |
| Platform Restrictions | ✅ | ❌ | ❌ |
| Conditional Activation | ✅ | Partial | ❌ |
| Token-Efficient Loading | ✅ | ❌ | ❌ |
| External Dir Support | ✅ | ❌ | ❌ |

### 9.2 Common Validation Patterns Across Frameworks

1. **Schema-based validation** — JSON/YAML schema cho metadata
2. **Conditional loading** — dựa trên available tools
3. **Security scanning** — malware và vulnerability detection
4. **Progressive disclosure** — multi-level content loading

---

## 10. Best Practices cho Skill Validation

### 10.1 Pre-publication Checklist

- [ ] `name` đúng format (kebab-case)
- [ ] `version` đúng semver
- [ ] `description` ngắn gọn (<200 chars)
- [ ] Có đủ 5 required sections
- [ ] `Procedure` có numbered steps rõ ràng
- [ ] `Verification` section mô tả cách confirm success
- [ ] `Pitfalls` liệt kê known failure modes
- [ ] Không có external dependencies
- [ ] Helper scripts nằm trong `scripts/`
- [ ] Platform restrictions đúng enum values
- [ ] Conditional activation fields reference valid toolsets

### 10.2 Testing Recommendations

1. **Load test** — verify skill load được trong clean environment
2. **Conditional test** — verify skill hiện/ẩn đúng theo conditions
3. **Platform test** — verify platform restrictions hoạt động
4. **Security scan** — chạy full security scanner trước publish

---

## 11. Kết luận

Hermes Agent cung cấp một trong những validation systems toàn diện nhất cho agent skills:

1. **Schema validation** qua YAML frontmatter với required fields và type checking
2. **Security validation** qua automated scanner cho Hub-installed skills
3. **Quality gates** qua 5-section structure và progressive disclosure pattern
4. **Conditional validation** qua toolset/tool availability checks
5. **Platform validation** qua OS restrictions

Điều này đảm bảo skills không chỉ hoạt động đúng mà còn an toàn và maintainable trong môi trường production.

---

## Nguồn tham khảo

- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
- https://agentskills.io (Skills Hub)