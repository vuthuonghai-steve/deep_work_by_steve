# Normalization Standards

> **Usage**: Reference for data normalization rules and field conventions. Load when normalizing input documents.

---

## 1. Standard Field Naming

| Concept | Standard | Example |
|---------|----------|---------|
| Entity ID | `{entity}_id` | `user_id`, `post_id` |
| Timestamp | `createdAt`, `updatedAt` | ISO 8601 format |
| Foreign Key | `{relatedEntity}Id` | `authorId`, `categoryId` |
| Boolean | `is{Action}`, `has{Thing}` | `isActive`, `hasChildren` |
| Status | `status` | Enum: `draft`, `published`, `archived` |

---

## 2. Document Type Standards

### 2.1 Functional Requirement (FR)

**Required Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier: `FR-{sequence}` |
| `title` | string | FR title |
| `description` | string | Full description |
| `priority` | enum | `critical`, `high`, `medium`, `low` |
| `module` | string | Related module (M1-M6) |
| `source` | object | `{file: path, line: number}` |
| `createdAt` | timestamp | ISO 8601 |

**Optional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `dependencies` | array | Related FR IDs |
| `tags` | array | Categorization tags |
| `originalContent` | string | Preserved raw content |

---

### 2.2 User Story (US)

**Required Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Format: `US-{module}-{sequence}` |
| `title` | string | Story title |
| `description` | string | As a/I want/so that format |
| `acceptanceCriteria` | array | List of criteria |
| `priority` | enum | `must-have`, `should-have`, `could-have`, `won't-have` |
| `module` | string | Related module |
| `source` | object | `{file: path, line: number}` |

**Optional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `labels` | array | Story labels |
| `assignee` | string | Responsible person |
| `storyPoints` | number | Complexity estimate |

---

### 2.3 Use Case (UC)

**Required Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Format: `UC-{module}-{sequence}` |
| `name` | string | Use case name |
| `actor` | string | Primary actor |
| `preconditions` | array | Prerequisites |
| `postconditions` | array | Expected outcomes |
| `flow` | object | Main and alternative flows |
| `module` | string | Related module |
| `source` | object | `{file: path, line: number}` |

**Flow Structure:**

```yaml
flow:
  main:
    - step: 1
      action: Description
      actor: Actor name
  alternative:
    - condition: Condition description
      steps: [list of step numbers]
```

---

## 3. Metadata Enrichment

### 3.1 Traceability ID Generation

**Format:** `{module}-{docType}-{sequence}`

| Module | DocType | Example |
|--------|---------|---------|
| m1 | fr, us, uc | m1-fr-001 |
| m2 | fr, us, uc | m2-us-002 |
| m3 | fr, us, uc | m3-uc-003 |

### 3.2 Source Citation

```json
{
  "source": {
    "file": "Docs/life-1/01-vision/FR/feature-map.md",
    "line": 42,
    "section": "Authentication"
  }
}
```

---

## 4. Validation Rules

### 4.1 Required Field Validation

- Every document MUST have: `id`, `title`, `module`, `source`
- User Stories MUST have: `acceptanceCriteria` (non-empty array)
- Use Cases MUST have: `preconditions`, `postconditions`, `flow`

### 4.2 Format Validation

- IDs must match pattern: `^(FR|US|UC)-[a-z0-9]+-\d{3}$`
- Timestamps must be ISO 8601 format
- Priority must be from allowed enum values

---

## 5. Non-Destructive Rules

1. **Never modify original content** - Always preserve in `originalContent` field
2. **Always create output files** - Never overwrite input files
3. **Idempotent operations** - Running multiple times produces same output
4. **Generate warnings** - For non-critical issues, continue with warning
