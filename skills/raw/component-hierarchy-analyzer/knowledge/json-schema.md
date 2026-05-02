# JSON Schema - Component Hierarchy Output

> **Usage**: Load when converting or validating output in Phase 4/5
> **Source**: Derived from design.md §2.4 and resources/sample-output.md

---

## 1. JSON Output Contract

Minimum JSON shape that must be supported:

```json
{
  "query": {
    "src": "string",
    "entry": "string",
    "focus": "string | null",
    "scope": "up | full | down",
    "layoutOnly": "boolean",
    "alias": "record<string,string>"
  },
  "root": {
    "name": "string",
    "type": "screen | component | layout | provider | framework | unknown",
    "filePath": "string | null",
    "depth": 0,
    "relationship": "root",
    "layout": "string | null",
    "module": "string | null",
    "recursive": "boolean",
    "duplicate": "boolean",
    "children": []
  },
  "metadata": {
    "command": "string",
    "exitCode": 0,
    "parserVersion": "string",
    "sourceFormat": "ascii-tree"
  },
  "warnings": [],
  "errors": []
}
```

---

## 2. Field Definitions

### 2.1 Query Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `src` | string | Yes | Source directory path |
| `entry` | string | Yes | Entry file path |
| `focus` | string \| null | Yes | Component name to focus on, or null |
| `scope` | "up" \| "full" \| "down" | Yes | Focus scope mode |
| `layoutOnly` | boolean | Yes | Whether layout-only mode was enabled |
| `alias` | record<string,string> | Yes | Path alias mappings |

### 2.2 Node Object (root and children)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Component name |
| `type` | string | Yes | Component type classification |
| `filePath` | string \| null | Yes | Relative file path, or null for framework components |
| `depth` | number | Yes | Tree depth level (0 for root) |
| `relationship` | string | Yes | Relationship to parent: "root", "child" |
| `layout` | string \| null | No | Layout classes/styles string |
| `module` | string \| null | No | Module name for framework components |
| `recursive` | boolean | No | True if component is recursive (self-referencing) |
| `duplicate` | boolean | No | True if component appears multiple times in tree |
| `children` | Node[] | Yes | Array of child nodes |

### 2.3 Type Classifications

Allowed values for `type` field:
- `screen`: Screen/page component (entry points, routes)
- `component`: Custom component from project source
- `framework`: Framework/library component (React Native, expo-router, etc.)
- `layout`: Layout wrapper component
- `provider`: Context provider or HOC
- `unknown`: Could not determine type

### 2.4 Metadata Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string | Yes | Full command that was executed |
| `exitCode` | number | Yes | Process exit code (0 = success) |
| `parserVersion` | string | Yes | Version string of the parser |
| `sourceFormat` | string | Yes | Format of source output (always "ascii-tree") |

### 2.5 Error/Warning Arrays

- `warnings`: Array of non-fatal issues (e.g., recursive component detected)
- `errors`: Array of fatal issues (e.g., parse failure, execution error)

---

## 3. Special Markers in ASCII Output

### 3.1 Recursive Marker
**ASCII**: `↺` at end of line
**JSON**: Set `recursive: true` on node
**Warning**: "Recursive component detected - expansion stopped"

### 3.2 Ancestor Chain Marker
**ASCII**: `★` prefix for ancestor chain in "up" scope
**JSON**: Normal tree structure, `relationship: "child"` for all nodes
**Note**: Children collapsed in "up" scope, shown as `[N children]` count

### 3.3 Duplicate Marker
**ASCII**: Not explicitly marked in current script
**JSON**: Set `duplicate: true` if same component key appears multiple times
**Detection**: Compare `name@filePath` keys across tree

---

## 4. Layout Field Format

Layout field combines className and style information:

**Format**: `className | styleProp={key:value, ...}`

**Examples**:
- `"flex flex-col p-4"` - className only
- `"flex | style={width:100,height:50}"` - className + style
- `"style={display:flex,flexDirection:column}"` - style only
- `null` - No layout information

**Layout-only mode**: When `layoutOnly: true`, only layout-relevant classes are included (filtered by layout class prefixes).

---

## 5. Validation Rules

### 5.1 Required Fields Check
- `query` object must exist with all 6 fields
- `root` object must exist with all required fields
- `metadata` object must exist with all 4 fields
- `warnings` and `errors` must be arrays (can be empty)

### 5.2 Tree Structure Check
- `depth` must increment by 1 for each child level
- `relationship` must be "root" for root node, "child" for all others
- `children` must be array (can be empty)
- No circular references in tree (except `recursive: true` marker)

### 5.3 Type Validation
- `type` must be one of allowed values
- `scope` in query must be "up", "full", or "down"
- `depth` must be non-negative integer

### 5.4 Fallback Validation
When parsing fails, output must include:
- `rawOutput` field with original ASCII text
- `errors` array with parse error message
- `query` and `metadata` still populated

---

## 6. Example: Full Success JSON

```json
{
  "query": {
    "src": "apps/mobile/src",
    "entry": "apps/mobile/src/app/_layout.tsx",
    "focus": null,
    "scope": "down",
    "layoutOnly": false,
    "alias": {
      "@": "apps/mobile/src"
    }
  },
  "root": {
    "name": "RootComponent",
    "type": "screen",
    "filePath": "apps/mobile/src/app/_layout.tsx",
    "depth": 0,
    "relationship": "root",
    "layout": "flex flex-1",
    "module": null,
    "recursive": false,
    "duplicate": false,
    "children": [
      {
        "name": "Stack",
        "type": "framework",
        "filePath": null,
        "depth": 1,
        "relationship": "child",
        "layout": null,
        "module": "expo-router",
        "recursive": false,
        "duplicate": false,
        "children": [
          {
            "name": "HomeScreen",
            "type": "screen",
            "filePath": "apps/mobile/src/app/home.tsx",
            "depth": 2,
            "relationship": "child",
            "layout": "flex flex-col p-4",
            "module": null,
            "recursive": false,
            "duplicate": false,
            "children": []
          }
        ]
      }
    ]
  },
  "metadata": {
    "command": "bun generate-component-hierarchy.ts",
    "exitCode": 0,
    "parserVersion": "0.1.0",
    "sourceFormat": "ascii-tree"
  },
  "warnings": [],
  "errors": []
}
```

---

## 7. Example: Fallback JSON (Parse Failure)

```json
{
  "query": {
    "src": "apps/mobile/src",
    "entry": "apps/mobile/src/app/_layout.tsx",
    "focus": null,
    "scope": "down",
    "layoutOnly": false,
    "alias": {}
  },
  "rawOutput": "[RootComponent] - apps/mobile/src/app/_layout.tsx\n└── [Stack]\n    └── [HomeScreen]",
  "metadata": {
    "command": "bun generate-component-hierarchy.ts",
    "exitCode": 0,
    "parserVersion": "0.1.0",
    "sourceFormat": "ascii-tree"
  },
  "warnings": [],
  "errors": [
    "Parse error: Unexpected format at line 2"
  ]
}
```
