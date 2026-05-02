# Input Clarification Checklist

> **Usage**: Load in Phase 1 to score input confidence before execution
> **Source**: Derived from design.md §2.2 and data/default-config.yaml

---

## Required Input Checks

Before executing the script, verify the following:

### 1. Source Directory (`src`)
- [ ] Is `src` provided explicitly?
- [ ] If not provided, can we use default from config (`apps/mobile/src`)?
- [ ] Does the path look valid (contains directory separators or is simple name)?
- [ ] Is the path relative to project root?

### 2. Entry File (`entry`)
- [ ] Is `entry` provided explicitly?
- [ ] If not provided, can we use default from config (`apps/mobile/src/app/_layout.tsx`)?
- [ ] Does the path have a valid extension (.tsx, .ts, .jsx, .js)?
- [ ] Is the path relative to project root or src directory?

### 3. Component/Screen Name (for `focus`)
- [ ] Is there a component or screen name mentioned in the request?
- [ ] If yes, is it a valid component name (PascalCase)?
- [ ] Can we infer the component name from context (e.g., "home screen" → "HomeScreen")?

### 4. Scope Mode (`scope`)
- [ ] Is `scope` provided explicitly?
- [ ] If provided, is it one of: `up`, `full`, `down`?
- [ ] If not provided, can we use default (`down`)?
- [ ] Does the scope make sense for the request context?

### 5. Layout-Only Flag (`layoutOnly`)
- [ ] Is `layoutOnly` requested explicitly?
- [ ] If not, default to `false`

### 6. Path Aliases (`alias`)
- [ ] Are custom aliases needed for the project?
- [ ] If not provided, can we use default from config (`@=apps/mobile/src`)?
- [ ] Are alias pairs in correct format (`key=value`)?

---

## Confidence Scoring Algorithm

Calculate confidence score (0-100%):

### Base Score
- Start with: 0%

### Add Points
- Has `src` path: +25%
- Has `entry` path: +25%
- Has component/screen name (in focus or context): +20%
- Has valid `scope`: +20%
- Has `alias` if needed: +10%

### Maximum Score
- 100% (all criteria met)

### Thresholds
- **>= 70%**: Auto-run (command is read-only)
- **< 70%**: Ask clarifying questions

---

## Clarification Questions

Ask only what's missing based on confidence score:

### Missing `src`
"What is the source directory path? (e.g., `apps/mobile/src`, `src`)"

### Missing `entry`
"What is the entry file path? (e.g., `apps/mobile/src/app/_layout.tsx`, `src/app/_layout.tsx`)"

### Missing component name
"Which component or screen should I focus on? (e.g., `HomeScreen`, `Button`)"

### Missing scope
"What scope do you need?
- `up`: Show ancestors only (children collapsed)
- `full`: Show ancestors → target → full subtree
- `down`: Show target as root → full subtree (default)"

### Missing alias (if project uses custom aliases)
"What path aliases should I use? (e.g., `@=apps/mobile/src`, `@components=src/components`)"

---

## Examples

### Example 1 - High Confidence (90%)
```
Request: "Show hierarchy for HomeScreen with full scope"
Checklist:
- [x] src: Use default (apps/mobile/src)
- [x] entry: Use default (apps/mobile/src/app/_layout.tsx)
- [x] component: HomeScreen
- [x] scope: full
- [x] alias: Use default
Score: 25 + 25 + 20 + 20 = 90%
Action: Auto-run
```

### Example 2 - Medium Confidence (50%)
```
Request: "Analyze the button component"
Checklist:
- [x] src: Use default
- [x] entry: Use default
- [x] component: Button
- [ ] scope: Not specified
- [x] alias: Use default
Score: 25 + 25 + 20 = 70%
Action: Auto-run with default scope (down)
```

### Example 3 - Low Confidence (25%)
```
Request: "Show me the hierarchy"
Checklist:
- [x] src: Use default
- [x] entry: Use default
- [ ] component: Not specified
- [ ] scope: Not specified
- [x] alias: Use default
Score: 25 + 25 = 50%
Action: Ask: "Which component should I focus on? What scope do you need?"
```

### Example 4 - Very Low Confidence (0%)
```
Request: "debug layout"
Checklist:
- [ ] src: Not specified
- [ ] entry: Not specified
- [ ] component: Not specified
- [ ] scope: Not specified
- [ ] alias: Not specified
Score: 0%
Action: Ask: "What is the source directory and entry file path? Which component should I focus on?"
```

---

## Edge Cases

### Custom Project Structure
If user mentions non-standard structure (e.g., "my project uses `frontend/` instead of `apps/"):
- Ask for explicit `src` and `entry` paths
- Ask for custom `alias` mappings if needed

### Multiple Components
If user mentions multiple components (e.g., "Button and TextInput"):
- Ask which one to focus on, or
- Suggest running analysis for each separately

### Relative vs Absolute Paths
- Always treat paths as relative to project root
- If user provides absolute path, convert to relative

### File Extension Variations
- Accept: .tsx, .ts, .jsx, .js
- If extension missing, assume .tsx for React Native projects
