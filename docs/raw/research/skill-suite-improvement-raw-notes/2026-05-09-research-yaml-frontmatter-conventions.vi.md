# Research: YAML Frontmatter Conventions cho Skill Metadata

**Ngày:** 2026-05-09  
**Chủ đề:** YAML Frontmatter Conventions cho Agent Skill Metadata  
**Ngôn ngữ:** Vietnamese

---

## 1. Tổng quan YAML Frontmatter

### 1.1 Định nghĩa

YAML frontmatter là block YAML được đặt ở đầu file, được phân cách bởi `---`. Cấu trúc này phổ biến trong các static site generators (Jekyll, Hugo, Gatsby) và documentation tools.

```yaml
---
title: Skill Name
version: 1.0.0
description: Mô tả ngắn về skill
---
```

### 1.2 Cú pháp cơ bản

```yaml
---
# YAML Frontmatter Block
key: value
nested:
  key: value
array:
  - item1
  - item2
---
```

---

## 2. Skill Metadata Schema Patterns

### 2.1 Common Metadata Fields

| Field | Type | Mô tả | Ví dụ |
|-------|------|--------|-------|
| `name` | string | Tên skill | `"skill-architect"` |
| `version` | semver | Phiên bản | `"1.0.0"` |
| `description` | string | Mô tả ngắn | `"Thiết kế skill"` |
| `author` | string | Tác giả | `"steve"` |
| `tags` | array | Tags phân loại | `["design", "planning"]` |
| `dependencies` | array | Skills phụ thuộc | `["skill-planner"]` |
| `inputs` | object | Schema input | xem 2.2 |
| `outputs` | object | Schema output | xem 2.2 |
| `permissions` | array | Quyền truy cập | `["read", "write"]` |
| `constraints` | object | Ràng buộc | xem 2.3 |

### 2.2 Input/Output Schema Pattern

```yaml
inputs:
  type: object
  properties:
    requirement:
      type: string
      description: Yêu cầu từ user
    context:
      type: object
      description: Context bổ sung
  required:
    - requirement

outputs:
  type: object
  properties:
    design_md:
      type: string
      description: Đường dẫn file design.md
    status:
      type: string
      enum: ["success", "failed"]
```

### 2.3 Constraints Pattern

```yaml
constraints:
  max_tokens: 4000
  timeout_seconds: 300
  retry_on_failure: true
  max_retries: 3
  required_tools:
    - read
    - write
    - glob
```

---

## 3. JSON Schema cho Agent Skill Definitions

### 3.1 Core Schema Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Agent Skill Definition",
  "required": ["name", "version", "workflow"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "Tên skill theo kebab-case"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic versioning"
    },
    "description": {
      "type": "string"
    },
    "workflow": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["phase", "action"],
        "properties": {
          "phase": {
            "type": "string",
            "enum": ["PREPARE", "CLARIFY", "BUILD", "VERIFY", "DELIVER"]
          },
          "action": {
            "type": "string"
          },
          "output": {
            "type": "string"
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "author": { "type": "string" },
        "created": { "type": "string", "format": "date-time" },
        "updated": { "type": "string", "format": "date-time" },
        "tags": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

### 3.2 Validation Example

```yaml
# skill-architect/SKILL.md frontmatter
---
name: skill-architect
version: 1.0.0
description: Senior Design Architect cho skill development
author: steve
created: 2026-01-15T10:00:00Z
updated: 2026-05-09T14:30:00Z

workflow:
  - phase: COLLECT
    action: gather_requirements
    output: requirements_raw
  - phase: ANALYZE
    action: map_pillars_zones
    output: analysis_report
  - phase: DESIGN
    action: generate_design_md
    output: design.md

inputs:
  requirement: string (required)
  user_context: object (optional)

outputs:
  design_md: file path
  analysis_json: object

constraints:
  max_tokens: 8000
  timeout_seconds: 600
  quality_gate: placeholder_scale_le_9

tags:
  - design
  - architecture
  - skill-development
---
```

---

## 4. Contract Versioning Strategies

### 4.1 Semantic Versioning (SemVer)

```yaml
# Version format: MAJOR.MINOR.PATCH
version: 1.2.3

# MAJOR: Breaking changes
# MINOR: New features, backwards compatible
# PATCH: Bug fixes, backwards compatible
```

### 4.2 Contract Schema Evolution

```yaml
# Version compatibility matrix
compatibility:
  v1.0.0:
    accepts: ["v1.x.x"]
    breaks_after: null
  v2.0.0:
    accepts: ["v2.x.x"]
    breaks_after: ["v1.x.x"]
    migration_path: "v1_to_v2.md"
```

### 4.3 API Contract Versioning Patterns

| Strategy | Pattern | Use Case |
|----------|---------|----------|
| URL Path | `/api/v1/skills` | Public APIs |
| Header | `Accept: application/vnd.skill.v1+json` | Flexible versioning |
| Query Param | `?version=1.0` | Simple, cache-friendly |
| Content Negotiation | `Accept: application/json` | REST best practice |

### 4.4 Skill Contract Versioning

```yaml
# skill contract versioning example
contract:
  version: "1.0"
  deprecated: false
  sunset_date: null
  
  input_contract:
    version: "1.0"
    schema: "./schemas/input-v1.schema.json"
    
  output_contract:
    version: "1.0"
    schema: "./schemas/output-v1.schema.json"

  breaking_changes:
    - version: "2.0"
      reason: "Redesigned workflow phases"
      migration_guide: "./MIGRATION_v1_to_v2.md"
```

### 4.5 Changelog Pattern

```yaml
# CHANGELOG.md frontmatter
---
document: CHANGELOG
version: 1.0.0
date: 2026-05-09

entries:
  - version: 1.2.0
    date: 2026-05-01
    changes:
      - type: feature
        description: Thêm phase VERIFY
      - type: improvement
        description: Cải thiện placeholder scale

  - version: 1.1.0
    date: 2026-04-15
    changes:
      - type: bugfix
        description: Sửa lỗi timeout
---
```

---

## 5. Best Practices

### 5.1 Frontmatter Conventions

1. **Luôn dùng `---` delimiters** ở đầu và cuối block
2. **Kebab-case cho tên field**: `max-retries`, `timeout-seconds`
3. **Indent bằng 2 spaces** (không dùng tab)
4. **String giá trị không cần quotes** trừ khi có ký tự đặc biệt
5. **Document type** nên đặt ở top: `document: skill-definition`

### 5.2 Schema Validation

```yaml
# Áp dụng JSON Schema cho type checking
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required:
  - name
  - version
  - workflow
```

### 5.3 Documentation Structure

```yaml
# Multi-document frontmatter pattern
---
document: skill-definition
type: workflow
version: 1.0.0
layer: 1
role: architect
---

# Content after frontmatter
```

---

## 6. Tools và References

### 6.1 Validation Tools

- **yamllint**: YAML syntax validation
- **jsonschema**: JSON Schema validation
- **ajv**: JSON Schema validator (JavaScript)

### 6.2 Reference Specifications

- [YAML 1.2 Specification](https://yaml.org/spec/1.2.2/)
- [JSON Schema Draft-07](https://json-schema.org/draft-07/draft-hierarchic-value-01.html)
- [Semantic Versioning 2.0.0](https://semver.org/)

---

## 7. Kết luận

YAML frontmatter là tiêu chuẩn phổ biến để định nghĩa metadata cho skill systems. Việc áp dụng:

- **JSON Schema** để validate structure
- **Semantic Versioning** để track changes
- **Contract versioning** để đảm bảo backwards compatibility

sẽ giúp xây dựng một skill system bài bản và dễ maintain.

---

**References:**
- YAML 1.2/1.3 specifications
- JSON Schema standard (draft-07)
- Semantic Versioning 2.0
- Common metadata conventions (Dublin Core, JSON-LD)