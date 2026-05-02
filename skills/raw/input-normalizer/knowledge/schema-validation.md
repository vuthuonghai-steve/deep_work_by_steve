# Schema Validation

> **Usage**: JSON Schema validation rules for input data. Load when implementing validation logic.

---

## 1. Functional Requirement Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "title", "description", "priority", "module", "source"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^FR-[a-z0-9]+-\\d{3}$"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "priority": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low"]
    },
    "module": {
      "type": "string",
      "pattern": "^M[1-6]$"
    },
    "source": {
      "type": "object",
      "required": ["file"],
      "properties": {
        "file": { "type": "string" },
        "line": { "type": "integer" },
        "section": { "type": "string" }
      }
    },
    "dependencies": {
      "type": "array",
      "items": { "type": "string" }
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "originalContent": {
      "type": "string"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---

## 2. User Story Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "title", "description", "acceptanceCriteria", "priority", "module", "source"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^US-M[1-6]-\\d{3}$"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "acceptanceCriteria": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "priority": {
      "type": "string",
      "enum": ["must-have", "should-have", "could-have", "won't-have"]
    },
    "module": {
      "type": "string",
      "pattern": "^M[1-6]$"
    },
    "source": {
      "type": "object",
      "required": ["file"],
      "properties": {
        "file": { "type": "string" },
        "line": { "type": "integer" },
        "section": { "type": "string" }
      }
    },
    "labels": {
      "type": "array",
      "items": { "type": "string" }
    },
    "assignee": {
      "type": "string"
    },
    "storyPoints": {
      "type": "integer",
      "minimum": 1,
      "maximum": 21
    },
    "originalContent": {
      "type": "string"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---

## 3. Use Case Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "name", "actor", "preconditions", "postconditions", "flow", "module", "source"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^UC-M[1-6]-\\d{3}$"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "actor": {
      "type": "string",
      "minLength": 1
    },
    "preconditions": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "postconditions": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "flow": {
      "type": "object",
      "required": ["main"],
      "properties": {
        "main": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["step", "action"],
            "properties": {
              "step": { "type": "integer" },
              "action": { "type": "string" },
              "actor": { "type": "string" }
            }
          }
        },
        "alternative": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "condition": { "type": "string" },
              "steps": { "type": "array", "items": { "type": "integer" } }
            }
          }
        }
      }
    },
    "module": {
      "type": "string",
      "pattern": "^M[1-6]$"
    },
    "source": {
      "type": "object",
      "required": ["file"],
      "properties": {
        "file": { "type": "string" },
        "line": { "type": "integer" },
        "section": { "type": "string" }
      }
    },
    "originalContent": {
      "type": "string"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---

## 4. Validation Error Codes

| Code | Type | Description |
|------|------|-------------|
| E001 | ERROR | Missing required field: {field} |
| E002 | ERROR | Invalid format: {field} - expected {expected} |
| E003 | ERROR | Invalid enum value: {field} - allowed: {allowed} |
| W001 | WARNING | Optional field missing: {field} |
| W002 | WARNING | Non-standard format detected: {field} |
| W003 | WARNING | Empty array: {field} |
| I001 | INFO | Field auto-generated: {field} |

---

## 5. Validation Levels

| Level | Action | Exit Code |
|-------|--------|-----------|
| ERROR | Stop processing, report failure | 1 |
| WARNING | Continue with warning in report | 0 |
| INFO | Log only, continue | 0 |
