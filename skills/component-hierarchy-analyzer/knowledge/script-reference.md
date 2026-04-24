# Script Reference - generate-component-hierarchy.ts

> **Usage**: Load at boot sequence with SKILL.md
> **Source**: Transform 100% from `resources/script-help.md`

---

## 1. Executable Discovery

**Script name**: `generate-component-hierarchy.ts` (Bun script)

**Invocation from repo root**:
```bash
bun generate-component-hierarchy.ts [options]
```

**Required runtime**: Bun (JavaScript/TypeScript runtime)

**Default configuration**:
- Default src: `apps/mobile/src`
- Default entry: `apps/mobile/src/app/_layout.tsx`
- Default alias: `@=apps/mobile/src`

---

## 2. Help Output

```text
Usage: bun generate-component-hierarchy.ts [options]
Options:
 --src <path> Source directory (default: apps/mobile/src)
 --entry <path> Entry file (default: apps/mobile/src/app/_layout.tsx)
 --rootComponent <name> Root component name override
 --alias <key=value> Path aliases, repeatable (default: @=apps/mobile/src)
 --focus <name> Focus on a specific component
 --scope <mode> Focus scope: up|full|down (default: down)
   up = ancestors → target (children collapsed)
   full = ancestors → target → full subtree
   down = target as root → full subtree
 --layoutOnly Keep only layout-relevant class/style signals
 -h, --help Show this help
```

---

## 3. CLI Contract

**Supported flags**:
- `--src <path>`: Source directory (optional, default: `apps/mobile/src`)
- `--entry <path>`: Entry file (optional, default: `apps/mobile/src/app/_layout.tsx`)
- `--rootComponent <name>`: Root component name override (optional)
- `--alias <key=value>`: Path aliases, repeatable (optional, default: `@=apps/mobile/src`)
- `--focus <name>`: Focus on specific component (optional)
- `--scope <mode>`: Focus scope (optional, default: `down`)
- `--layoutOnly`: Keep only layout-relevant signals (optional, boolean flag)
- `-h, --help`: Show help (optional)

**Allowed values for `--scope`**:
- `up`: Ancestors → target (children collapsed)
- `full`: Ancestors → target → full subtree
- `down`: Target as root → full subtree

**Exit codes**:
- `0`: Success
- `1`: Error (invalid scope, missing file, parse error)

**Stdout behavior**:
- Success: ASCII tree representation of component hierarchy
- Error: Error message to stderr

**Stderr behavior**:
- Parse errors: `[warn] skipping unparseable file {path}: {error}`
- Validation errors: `Error: --scope must be one of {scopes}`
- Entry errors: `Cannot determine root component for {path}. Use --rootComponent.`

---

## 4. Read-only Guarantee

**Read-only**: YES - Script only reads files for AST analysis

**No write operations**:
- Does not modify any files
- Does not generate output files
- Does not create cache
- Does not mutate project state

**File operations**:
- Reads source files (.ts, .tsx, .js, .jsx)
- Parses AST using Babel
- Traverses directory structure using Bun.Glob

---

## 5. Example Commands

**Minimal success command**:
```bash
bun generate-component-hierarchy.ts
```
Output: Full hierarchy from default entry

**Focused component command**:
```bash
bun generate-component-hierarchy.ts --focus HomeScreen --scope full
```
Output: Ancestors → HomeScreen → full subtree

**Layout-only command**:
```bash
bun generate-component-hierarchy.ts --layoutOnly
```
Output: Hierarchy with only layout-related classes/styles

**Custom source command**:
```bash
bun generate-component-hierarchy.ts --src src --entry src/app/_layout.tsx --alias @=src
```
Output: Hierarchy from custom source directory

**Failure example**:
```bash
bun generate-component-hierarchy.ts --entry nonexistent.tsx
```
Output: Error: Cannot determine root component for nonexistent.tsx. Use --rootComponent.

---

## 6. Error Message Mapping

| Error Pattern | Stderr Message | User-Friendly Suggestion |
|---------------|----------------|-------------------------|
| Invalid scope | `Error: --scope must be one of up, full, down` | Use one of: `up`, `full`, `down` |
| Missing entry | `Cannot determine root component for {path}. Use --rootComponent.` | Provide `--rootComponent` flag or check entry path |
| Parse error | `[warn] skipping unparseable file {path}: {error}` | File has syntax errors, script continues with other files |
| File not found | (Exit code 1, empty stdout) | Check that entry file exists at specified path |
