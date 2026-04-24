---
name: component-hierarchy-analyzer
description: Analyzes React/React Native component hierarchies by executing the generate-component-hierarchy Bun script and converting ASCII tree output to structured JSON. Use when frontend developers need to inspect component structure, debug UI layout issues, or understand component relationships in a codebase.
---

# Component Hierarchy Analyzer

## Workflow Progress Tracker

Copy this checklist into your response and mark off progress:

```markdown
### [component-hierarchy-analyzer] Progress:
- [ ] Phase 1: Input Clarification
- [ ] Phase 2: Argument Mapping → [⏸️ Gate: Confirmation if needed]
- [ ] Phase 3: Script Execution
- [ ] Phase 4: Output Parsing & JSON Conversion
- [ ] Phase 5: Validation & Delivery
```

---

## Mandatory Boot Sequence

Read these files before starting any analysis:

- [knowledge/script-reference.md](knowledge/script-reference.md) - CLI options, executable discovery, examples, exit codes
- [data/default-config.yaml](data/default-config.yaml) - Default args, allowed scopes, aliases, confidence threshold
- [loop/input-clarification-checklist.md](loop/input-clarification-checklist.md) - Input validation and confidence scoring rules

---

## Phase 1: Input Clarification

When a developer requests component hierarchy analysis:

1. **Extract request parameters**:
   - `src`: Source directory (optional, default from config)
   - `entry`: Entry file path (optional, default from config)
   - `focus`: Specific component name to focus on (optional)
   - `scope`: Focus mode - `up`, `full`, or `down` (optional, default: `down`)
   - `layoutOnly`: Boolean flag to show only layout-relevant signals (optional, default: `false`)
   - `alias`: Path alias mappings (optional, default from config)

2. **Score input confidence** using [loop/input-clarification-checklist.md](loop/input-clarification-checklist.md):
   - Base score: 0%
   - Has `src` path: +25%
   - Has `entry` path: +25%
   - Has component/screen name (in focus or context): +20%
   - Has valid `scope`: +20%
   - Has `alias` if needed: +10%

3. **Apply confidence gate**:
   - If confidence >= 70% AND command is read-only → proceed to Phase 2 without confirmation
   - If confidence < 70% OR missing critical information → ask targeted clarifying questions

4. **Clarification questions** (ask only what's missing):
   - "What is the source directory path? (e.g., `apps/mobile/src`)"
   - "What is the entry file path? (e.g., `apps/mobile/src/app/_layout.tsx`)"
   - "Which component or screen should I focus on?"
   - "What scope do you need? (`up` for ancestors only, `full` for ancestors+subtree, `down` for subtree only)"

---

## Phase 2: Argument Mapping

Map clarified input to CLI arguments for `generate-component-hierarchy.ts`:

1. **Build command array**:
   ```bash
   bun generate-component-hierarchy.ts \
     --src <src> \
     --entry <entry> \
     --focus <focus> \
     --scope <scope> \
     --layoutOnly \
     --alias <key=value>
   ```

2. **Validation**:
   - Ensure `scope` is one of: `up`, `full`, `down` (validate against [data/default-config.yaml](data/default-config.yaml))
   - Resolve absolute paths for `src` and `entry` relative to project root
   - Format `alias` as `key=value` pairs

3. **Confirmation gate**:
   - If command is read-only (always true for this script) and confidence >= 70% → auto-run
   - If user requested review → show mapped command and wait for confirmation

---

## Phase 3: Script Execution

Execute the script using [scripts/execute-script.py](scripts/execute-script.py):

1. **Check executable availability**:
   - Verify `bun` is available in PATH
   - Check if `generate-component-hierarchy.ts` exists at project root
   - If missing → copy from skill assets: `cp .windsurf/skills/component-hierarchy-analyzer/assets/generate-component-hierarchy.ts ./`
   - If assets also missing → report blocker with setup instructions

2. **Run command**:
   - Execute in subprocess with timeout (30s default)
   - Capture stdout, stderr, and exit code
   - Ensure working directory is project root

3. **Handle execution results**:
   - **Exit code 0**: Proceed to Phase 4 with stdout
   - **Exit code 1**: Parse stderr for error message, provide user-friendly suggestions
   - **Timeout**: Report timeout and suggest simplifying scope or entry point

---

## Phase 4: Output Parsing & JSON Conversion

Parse ASCII tree output and convert to structured JSON:

1. **Read parsing rules** from [knowledge/json-schema.md](knowledge/json-schema.md)

2. **Parse ASCII tree** using [scripts/parse-output.py](scripts/parse-output.py):
   - Identify root component line: `[ComponentName] - filePath (layout)`
   - Parse child nodes using tree characters (`├──`, `└──`, indentation levels)
   - Extract component metadata: name, type, filePath, module, layout
   - Detect special markers: `↺` (recursive), `★` (ancestor chain)

3. **Convert to JSON**:
   - Build hierarchical tree structure matching schema
   - Include `query` object with all input parameters
   - Include `metadata` with command, exitCode, parserVersion
   - Add `warnings` array for non-fatal issues
   - Add `errors` array for parsing failures

4. **Handle edge cases**:
   - Empty output → return minimal JSON with error
   - Unparseable format → return raw output in `rawOutput` field with parse error
   - Recursive detection → set `recursive: true` and add warning

---

## Phase 5: Validation & Delivery

Validate and deliver the final JSON:

1. **Read validation rules** from [loop/output-validation-checklist.md](loop/output-validation-checklist.md)

2. **Validate JSON structure**:
   - Verify required fields: `query`, `root`, `metadata`
   - Verify `root` has: `name`, `type`, `filePath`, `depth`, `relationship`, `children`
   - Verify child nodes have same structure as root
   - Check `depth` increments correctly
   - Validate `type` is one of: `screen`, `component`, `framework`, `layout`, `provider`, `unknown`

3. **Deliver result**:
   - If validation passes → return JSON
   - If validation fails → return partial JSON with validation errors in `errors` array
   - Always include `rawOutput` field if parsing had issues

4. **Fallback behavior**:
   - When JSON conversion fails → return:
     ```json
     {
       "query": { ... },
       "rawOutput": "<ascii tree>",
       "metadata": { ... },
       "errors": ["Parse error: ..."],
       "warnings": []
     }
     ```

---

## Runtime Guardrails

**DO NOT execute if**:
- Script reference not loaded ([knowledge/script-reference.md](knowledge/script-reference.md))
- Executable path not verified
- Input validation fails (confidence < 70% and user doesn't provide clarification)

**ALWAYS**:
- Validate input before mapping arguments
- Run commands in read-only mode (script is guaranteed read-only)
- Include `errors` and `warnings` in output JSON when fallback occurs
- Report specific error messages with actionable suggestions

**NEVER**:
- Guess file paths when input is ambiguous
- Execute commands with side effects (this script is read-only by design)
- Return JSON without `errors` field when parsing/execution fails

---

## Error Handling

| Error Type | Detection | Response |
|------------|-----------|----------|
| Script not found | `bun` or `.ts` file missing | Report blocker with setup instructions |
| Invalid scope | `--scope` not in allowed set | Show allowed values from config |
| Entry file missing | Exit code 1 with entry error | Suggest using `--rootComponent` or check path |
| Parse error | Exit code 1 with parse warning | Show file path and error, continue with other files |
| Timeout | Script runs > 30s | Suggest simplifying scope or entry point |
| Output parse fail | ASCII format doesn't match expected | Return raw output with parse error metadata |

---

## Examples

**Example 1 - Simple hierarchy request**:
```
User: "Show me the component hierarchy for the home screen"
AI: [Scores confidence: 60% - missing src/entry]
AI: "What is the source directory and entry file path?"
User: "src: apps/mobile/src, entry: apps/mobile/src/app/_layout.tsx"
AI: [Confidence: 90% - auto-run]
AI: [Executes script, returns JSON]
```

**Example 2 - Focused analysis**:
```
User: "Analyze Button component with full scope"
AI: [Scores confidence: 70% - has focus+scope, missing src/entry uses defaults]
AI: [Auto-run with defaults]
AI: [Executes: bun generate-component-hierarchy.ts --focus Button --scope full]
AI: [Returns JSON with Button as focus point]
```

**Example 3 - Layout-only inspection**:
```
User: "Show layout structure for LoginScreen"
AI: [Scores confidence: 75%]
AI: [Executes: bun generate-component-hierarchy.ts --focus LoginScreen --layoutOnly]
AI: [Returns JSON with only layout-relevant classes/styles]
```
