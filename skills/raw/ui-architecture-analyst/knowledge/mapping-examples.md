# Mapping Examples — Concrete Schema → UI Component Reference

> **Usage**: Load in Phase 3 when mapping schema fields to UI components. Contains verified input→output pairs for common and edge-case scenarios. Reference this file BEFORE making mapping decisions for nested objects, arrays, relationship fields, or any ambiguous type.

---

## Example 1: User Authentication Screen — Simple Fields

**Source Schema** (Users collection):
```yaml
fields:
  - name: email
    type: email
    required: true
  - name: password
    type: password
    required: true
  - name: displayName
    type: text
    required: true
    maxLength: 50
  - name: bio
    type: textarea
    required: false
    maxLength: 500
  - name: role
    type: select
    required: true
    options:
      - label: Admin
        value: admin
      - label: User
        value: user
```

**Output Data-Component Binding Table**:

| UI Element ID | Component Type | Source Field | Required | Validation |
|---|---|---|---|---|
| `input-email` | `Input[type=email]` | `User.email` | ✅ | RFC 5321 format |
| `input-password` | `Input[type=password]` | `User.password` | ✅ | min 8 chars, show/hide toggle |
| `input-displayName` | `Input[type=text]` | `User.displayName` | ✅ | maxLength: 50 |
| `textarea-bio` | `Textarea` | `User.bio` | ❌ | maxLength: 500 |
| `select-role` | `Select` | `User.role` | ✅ | enum: [admin, user] |

---

## Example 2: Post Create Screen — Mixed Types Including RichText & Upload

**Source Schema** (Posts collection):
```yaml
fields:
  - name: title
    type: text
    required: true
    maxLength: 200
  - name: content
    type: richText
    editor: lexical
    required: true
  - name: tags
    type: relationship
    relationTo: tags
    hasMany: true
    required: false
  - name: coverImage
    type: upload
    relationTo: media
    required: false
  - name: visibility
    type: select
    options: [public, friends, private]
    required: true
  - name: publishedAt
    type: date
    required: false
```

**Output Data-Component Binding Table**:

| UI Element ID | Component Type | Source Field | Required | Validation |
|---|---|---|---|---|
| `input-title` | `Input[type=text]` | `Post.title` | ✅ | maxLength: 200 |
| `editor-content` | `RichTextEditor (Lexical)` | `Post.content` | ✅ | Non-empty check |
| `relation-multi-tags` | `RelationMultiPicker` | `Post.tags` | ❌ | 0 selections allowed |
| `upload-coverImage` | `ImageUpload` | `Post.coverImage` | ❌ | Accept: image/*, max 5MB |
| `select-visibility` | `Select` | `Post.visibility` | ✅ | enum: [public, friends, private] |
| `date-publishedAt` | `DatePicker` | `Post.publishedAt` | ❌ | ISO 8601, future date only |

---

## Example 3: Nested Group Field (Edge Case — Dot Notation)

**Source Schema** (Profile collection with nested group):
```yaml
fields:
  - name: socialLinks
    type: group
    fields:
      - name: twitter
        type: text
        required: false
      - name: github
        type: text
        required: false
      - name: linkedin
        type: text
        required: false
```

**Mapping Rule**: `group` type → `FormSection` (visual grouping container, not an input itself)

**Output Data-Component Binding Table**:

| UI Element ID | Component Type | Source Field | Required | Validation |
|---|---|---|---|---|
| *(section label: "Mạng xã hội")* | `FormSection` | `Profile.socialLinks` (group) | ❌ | N/A (container) |
| `input-twitter` | `Input[type=text]` | `Profile.socialLinks.twitter` | ❌ | URL format (optional) |
| `input-github` | `Input[type=text]` | `Profile.socialLinks.github` | ❌ | URL format (optional) |
| `input-linkedin` | `Input[type=text]` | `Profile.socialLinks.linkedin` | ❌ | URL format (optional) |

**Key Rule**: Nested group field paths use **dot notation**: `Parent.group.child`.
`group` itself maps to `FormSection` — no input, no validation, no Required flag.

---

## Example 4: Array of Objects — Repeater Pattern (Edge Case)

**Source Schema** (Work experience array):
```yaml
fields:
  - name: experience
    type: array
    minRows: 0
    maxRows: 10
    fields:
      - name: company
        type: text
        required: true
      - name: position
        type: text
        required: true
      - name: startDate
        type: date
        required: true
      - name: endDate
        type: date
        required: false
```

**Mapping Rule**: `array` type → `ArrayField` (Repeater container). Child fields listed with `[n]` index placeholder.

**Output Data-Component Binding Table**:

| UI Element ID | Component Type | Source Field | Required | Validation |
|---|---|---|---|---|
| `array-experience` | `ArrayField` (Repeater) | `User.experience` | ❌ | maxRows: 10 |
| ↳ `input-company` | `Input[type=text]` | `User.experience[n].company` | ✅ | Non-empty |
| ↳ `input-position` | `Input[type=text]` | `User.experience[n].position` | ✅ | Non-empty |
| ↳ `date-startDate` | `DatePicker` | `User.experience[n].startDate` | ✅ | Before endDate |
| ↳ `date-endDate` | `DatePicker` | `User.experience[n].endDate` | ❌ | After startDate if set |

**Key Rules**:
- Array child field paths use **bracket notation**: `Parent.array[n].child`
- `ArrayField` itself: Required = ❌ (the array container), Validation = minRows/maxRows
- Child fields: each has its own Required/Validation from their schema definition

---

## Example 5: Polymorphic Blocks (Edge Case — Complex)

**Source Schema** (blocks field):
```yaml
fields:
  - name: pageContent
    type: blocks
    blocks:
      - slug: textBlock
        fields:
          - name: text
            type: richText
      - slug: imageBlock
        fields:
          - name: image
            type: upload
            relationTo: media
          - name: caption
            type: text
            required: false
```

**Mapping Rule**: `blocks` type → `BlockEditor` (custom block picker + per-block sub-forms)

**Output Data-Component Binding Table**:

| UI Element ID | Component Type | Source Field | Required | Validation |
|---|---|---|---|---|
| `block-pageContent` | `BlockEditor` (block picker) | `Post.pageContent` | ❌ | N/A (container) |
| ↳ *(textBlock)* `editor-text` | `RichTextEditor` | `Post.pageContent[n].text` | ✅ | Non-empty |
| ↳ *(imageBlock)* `upload-image` | `ImageUpload` | `Post.pageContent[n].image` | ✅ | Accept: image/* |
| ↳ *(imageBlock)* `input-caption` | `Input[type=text]` | `Post.pageContent[n].caption` | ❌ | maxLength hint |

**Key Rule**: Mark block slug in italics as context: `*(textBlock)*`, `*(imageBlock)*`.

---

## Example 6: [SOURCE MISSING] Pattern

When a UI element appears in a flow diagram but has NO corresponding schema field:

**Scenario**: Designer wants a search bar on list screen, but `search` field doesn't exist in schema.

| UI Element ID | Component Type | Source Field | Required | Validation |
|---|---|---|---|---|
| `input-search` | `Input[type=search]` | `[SOURCE MISSING]` | N/A | Flagged as spec gap |

**Action**:
1. Write `[SOURCE MISSING]` in Source Field column — never invent a field name
2. Log the gap at end of Phase 3: "Element `input-search` has no source field in schema"
3. Report to user at IP-1 or before Phase 4: "Found N `[SOURCE MISSING]` elements — spec gap exists"
4. Do NOT block Phase 3 progress — continue mapping other fields, consolidate gap report

---

## Quick Reference: Type → Component Cheatsheet

| If schema type is... | Use component... | Prefix |
|---|---|---|
| `text` | `Input[type=text]` | `input-` |
| `email` | `Input[type=email]` | `input-` |
| `password` | `Input[type=password]` | `input-` |
| `number` | `Input[type=number]` | `input-` |
| `textarea` | `Textarea` | `textarea-` |
| `richText` (lexical) | `RichTextEditor` | `editor-` |
| `select` (single) | `Select` | `select-` |
| `select` (hasMany) | `MultiSelect` / `CheckboxGroup` | `multi-select-` |
| `checkbox` | `Checkbox` | `checkbox-` |
| `date` | `DatePicker` | `date-` |
| `upload` (image) | `ImageUpload` | `upload-` |
| `upload` (file) | `FileUpload` | `upload-` |
| `relationship` (single) | `RelationPicker` | `relation-` |
| `relationship` (hasMany) | `RelationMultiPicker` | `relation-multi-` |
| `array` | `ArrayField` (Repeater) | `array-` |
| `group` | `FormSection` (container) | *(no prefix)* |
| `blocks` | `BlockEditor` | `block-` |
| `json` | `Textarea` (code mode) | `json-` |
| `point` | `CoordinateInput` | `coord-` |
