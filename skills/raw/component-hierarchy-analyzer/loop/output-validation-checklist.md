# Output Validation Checklist

> **Usage**: Load in Phase 5 before delivering JSON to user
> **Source**: Derived from design.md §2.4 and knowledge/json-schema.md

---

## JSON Structure Validation

Before delivering the result, verify the following:

### 1. Required Top-Level Fields
- [ ] `query` object exists
- [ ] `root` object exists OR `rawOutput` string exists (fallback mode)
- [ ] `metadata` object exists
- [ ] `warnings` array exists (can be empty)
- [ ] `errors` array exists (can be empty)

### 2. Query Object Validation
- [ ] `query.src` is a string
- [ ] `query.entry` is a string
- [ ] `query.focus` is either a string or null
- [ ] `query.scope` is one of: "up", "full", "down"
- [ ] `query.layoutOnly` is a boolean
- [ ] `query.alias` is an object (record<string,string>)

### 3. Root Object Validation (if not fallback mode)
- [ ] `root.name` is a non-empty string
- [ ] `root.type` is one of: "screen", "component", "layout", "provider", "framework", "unknown"
- [ ] `root.filePath` is either a string or null
- [ ] `root.depth` is a number (should be 0 for root)
- [ ] `root.relationship` is "root" for root node
- [ ] `root.layout` is either a string or null
- [ ] `root.module` is either a string or null
- [ ] `root.recursive` is a boolean
- [ ] `root.duplicate` is a boolean
- [ ] `root.children` is an array (can be empty)

### 4. Child Node Validation
- [ ] All child nodes have the same structure as root
- [ ] `depth` increments by 1 for each level
- [ ] `relationship` is "child" for all non-root nodes
- [ ] No circular references in tree (except `recursive: true` marker)
- [ ] `type` is one of allowed values

### 5. Metadata Object Validation
- [ ] `metadata.command` is a string (the executed command)
- [ ] `metadata.exitCode` is a number (0 for success)
- [ ] `metadata.parserVersion` is a string (e.g., "0.1.0")
- [ ] `metadata.sourceFormat` is "ascii-tree"

### 6. Fallback Mode Validation (if parsing failed)
- [ ] `rawOutput` field exists with original ASCII text
- [ ] `errors` array contains parse error message
- [ ] `query` and `metadata` are still populated
- [ ] `root` field does NOT exist (or is null)

---

## Tree Structure Validation

### Depth Consistency
- [ ] Root node has `depth: 0`
- [ ] Each child's `depth` is parent's `depth + 1`
- [ ] No gaps in depth sequence (e.g., 0 → 2 without 1)

### Relationship Consistency
- [ ] Root node has `relationship: "root"`
- [ ] All other nodes have `relationship: "child"`

### Type Classification Consistency
- [ ] Framework components have `module` field and `filePath: null`
- [ ] Project components have `filePath` field
- [ ] Screens have "screen" or "page" in file path or name
- [ ] Layout components have "layout" in file path or name

### Special Markers
- [ ] If `recursive: true`, node should have no children (expansion stopped)
- [ ] If `duplicate: true`, same component appears elsewhere in tree
- [ ] Recursive nodes should have warning in `warnings` array

---

## Schema Validation Against Contract

### Minimum Contract (from design.md §2.4)
- [ ] `query` object with all 6 fields present
- [ ] `root` object with minimum fields: name, type, filePath, depth, relationship, children
- [ ] `metadata` object with all 4 fields present
- [ ] Child nodes have same minimum fields as root

### Extended Fields (from sample-output.md)
- [ ] `layout` field present (can be null)
- [ ] `module` field present for framework components (can be null)
- [ ] `recursive` field present (boolean)
- [ ] `duplicate` field present (boolean)

---

## Error Handling Validation

### Execution Errors
- [ ] If `exitCode != 0`, `errors` array contains error message
- [ ] Error message is user-friendly (not just raw stderr)
- [ ] Error message includes actionable suggestion

### Parse Errors
- [ ] If parsing failed, `rawOutput` contains original ASCII
- [ ] `errors` array contains specific parse error
- [ ] Parse error indicates what went wrong (e.g., "Unexpected format at line 2")

### Validation Errors
- [ ] If JSON validation fails, `errors` array contains validation error
- [ ] Validation error specifies which field failed and why

---

## Fallback Verification

### When to Use Fallback
- [ ] ASCII output format doesn't match expected pattern
- [ ] Parser encounters unexpected characters
- [ ] Tree structure cannot be built (e.g., inconsistent depth)

### Fallback Requirements
- [ ] `rawOutput` field contains complete original output
- [ ] `query` object is still populated with input parameters
- [ ] `metadata` object is still populated
- [ ] `errors` array explains why fallback was used
- [ ] `warnings` array may contain partial parsing results

### Fallback Example
```json
{
  "query": { ... },
  "rawOutput": "[RootComponent] - apps/mobile/src/app/_layout.tsx\n└── [Stack]",
  "metadata": { ... },
  "warnings": [],
  "errors": ["Parse error: Unexpected format at line 2"]
}
```

---

## Validation Results

### Pass Criteria
- All required fields present
- All field types correct
- Tree structure consistent
- No validation errors in `errors` array
- Exit code is 0

### Warning Criteria
- All required fields present
- Minor issues (e.g., recursive component detected)
- `warnings` array non-empty but `errors` array empty
- Exit code is 0

### Fail Criteria
- Missing required fields
- Incorrect field types
- Tree structure inconsistent
- `errors` array non-empty
- Exit code is not 0

---

## Delivery Decision

### If Validation Passes
- Deliver JSON to user
- No additional context needed

### If Validation Has Warnings
- Deliver JSON to user
- Include note about warnings (e.g., "Note: Recursive component detected")

### If Validation Fails
- If fallback available: Deliver fallback JSON with error explanation
- If no fallback: Report error to user with suggestion to:
  - Check script output format
  - Update sample-output.md resource
  - Run script manually to debug

---

## Examples

### Example 1 - Valid Output
```json
{
  "query": { "src": "apps/mobile/src", "entry": "...", "focus": null, "scope": "down", "layoutOnly": false, "alias": {} },
  "root": { "name": "RootComponent", "type": "screen", "filePath": "...", "depth": 0, "relationship": "root", "children": [] },
  "metadata": { "command": "...", "exitCode": 0, "parserVersion": "0.1.0", "sourceFormat": "ascii-tree" },
  "warnings": [],
  "errors": []
}
```
**Validation**: ✅ Pass - All fields present and correct

### Example 2 - Output with Warning
```json
{
  "query": { ... },
  "root": { "name": "RecursiveComponent", "type": "component", "recursive": true, "children": [] },
  "metadata": { ... },
  "warnings": ["Recursive component detected: RecursiveComponent"],
  "errors": []
}
```
**Validation**: ⚠️ Warning - Valid but has warning

### Example 3 - Fallback Output
```json
{
  "query": { ... },
  "rawOutput": "[RootComponent] - apps/mobile/src/app/_layout.tsx",
  "metadata": { ... },
  "warnings": [],
  "errors": ["Parse error: Unexpected format at line 2"]
}
```
**Validation**: ❌ Fail - Parsing failed, fallback used

### Example 4 - Invalid Output
```json
{
  "query": { "src": "apps/mobile/src" },
  "root": { "name": "RootComponent" },
  "metadata": { "exitCode": 1 }
}
```
**Validation**: ❌ Fail - Missing required fields (entry, focus, scope, etc.)
