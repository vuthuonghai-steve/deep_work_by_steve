---
name: flutter-ui-converter
description: Converts Flutter UI from reference project to production project while preserving business logic and state management. Use when migrating screens/components between Flutter projects with different UI designs but shared logic patterns. Enforces UI-only changes, zero new dependencies, and maintains Bloc/Cubit state hooks.
---

# Flutter UI Converter

**Persona**: Flutter UI Conversion Specialist

## Mission

Convert UI/UX from reference project (`tranphueco-redo-AI`) to production project (`tranphueco`) with **zero business logic changes**. Enforce UI-only modifications, preserve state management hooks, and maintain dependency constraints.

The core process involves:
1. **Read Core Documents & Resolve Paths**:
   - Load `SKILL.md` and `data/project-config.yaml`.
   - **Path Discovery**:
     - **Target**: Default to current working directory (`.`).
     - **DESIGN.md**: Look for `DESIGN.md` in target root.
     - **Source**: Check `path` in `project-config.yaml`. If invalid, ask user for absolute path or search adjacent directories.
   - Load project's global `DESIGN.md` once paths are resolved.
2. **Scan Source Project**: Analyze the UI and assets of the source project (e.g., `tranphueco-redo-AI`).
3. **Scan Target Project**: Analyze the existing logic, Bloc hooks, and dependencies of the target project (`tranphueco`).

## Workflow Progress Tracker

Copy this checklist into your response and mark progress:

```markdown
### [flutter-ui-converter] Progress:
- [ ] Phase 1: Analysis & Documentation
- [ ] Phase 1 Gate: User approval → [⏸️ Wait for approval]
- [ ] Phase 2: Code Generation
- [ ] Phase 2 Gate: User testing → [⏸️ Wait for test results]
- [ ] Phase 3: Feedback Loop & Learning
```

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file) - always loaded

### Tier 2: Phase-Specific Knowledge & Data

**Phase 1 - Analysis (Load only these 4 core files):**
- `SKILL.md` - Core instructions and guardrails
- `DESIGN.md` - Global project design system (colors, typography, constants)
- `knowledge/` - Technical guides (state management, asset mapping, etc.)
- `knowledge/component-mapping-guide.md` - Source → Target widget mapping
- `data/project-config.yaml` - Saved project paths (read/write)

**Phase 1 - Optional (Load only if needed):**
- `knowledge/flutter-ui-patterns.md` - Widget tree structure (load if unfamiliar with Flutter)
- `knowledge/asset-management.md` - Asset path conventions (load when processing assets)
- `knowledge/localization-mapping.md` - i18n detection and mapping (load only if target has i18n)
- `knowledge/responsive-layout-rules.md` - RenderFlex overflow prevention (load if layout issues)
- `knowledge/flutter-sdk-compatibility.md` - API differences (load if version mismatch detected)
- `data/widget-equivalents.yaml` - Icon substitution mappings (load when mapping icons)
- `data/theme-mapping-rules.yaml` - Color/text style mapping (populated dynamically in Phase 1)
- `data/localization-dictionary.yaml` - Text → i18n key mappings (load only if target has i18n)

**Phase 2 - Code Generation:**
- `loop/phase2-verification.md` - Combined checklist for code generation and guardrail verification
- `data/forbidden-patterns.yaml` - Patterns that must not appear in code
- `templates/*.template` - Output document templates

**Phase 3 - Feedback:**
- `data/known-issues.yaml` - Known issues database
- `data/pattern-library.yaml` - Successful patterns library

## Phase 1: Analysis & Documentation

**Objective**: Analyze both projects using AI reasoning, generate mappings, identify risks.

### Step 1.1: Load Project Paths

Read `data/project-config.yaml`:
- If `projects.source.path` and `projects.target.path` are empty, ask user for paths
- Save paths back to `project-config.yaml` using Write tool
- If paths exist, use them directly

Ask user for screen name to convert.

### Step 1.2: Analyze Source Project

**Load core knowledge files** (conversion-rules.md, state-management-preservation.md, component-mapping-guide.md).

**Using Read tool**, open and analyze source project files:

1. **Find screen file**: Use Bash tool with `find` to locate screen file matching screen name
2. **Read Dart file**: Use Read tool to read the entire screen file
3. **Analyze with AI reasoning**:
   - Identify widget tree structure (StatelessWidget/StatefulWidget)
   - Extract all `Image.asset()`, `AssetImage()`, `SvgPicture.asset()` calls
   - Find all `Color(0xFFxxxxxx)` hardcoded colors
   - List all custom widgets used
   - Note any third-party UI packages (lucide_icons, etc.)

4. **Read pubspec.yaml**: Check dependencies

**Output**: Create analysis document using `templates/analysis-doc.md.template`

### Step 1.3: Analyze Target Project

**Using Read tool**, open and analyze target project files:

1. **Find screen file**: Use Bash tool with `find` to locate matching screen in target
2. **Read Dart file** (if exists): Use Read tool
3. **Analyze Bloc/Cubit hooks**:
   - Find all `BlocBuilder<Bloc, State>` patterns
   - Find all `BlocListener<Bloc, State>` patterns
   - Find all `BlocConsumer<Bloc, State>` patterns
   - Find all `context.read<Bloc>().add(Event())` calls
   - Find all `state.fieldName` references
   - Note all callback functions (`onPressed`, `onChanged`, etc.)

4. **Dynamic Theme Discovery** (CRITICAL):
   ```bash
   # Discover actual theme constants in target project
   grep -r "class.*Colors" lib/ --include="*.dart"
   grep -r "class.*TextStyles" lib/ --include="*.dart"
   grep -r "class.*Spacing" lib/ --include="*.dart"
   grep -r "class.*Radius" lib/ --include="*.dart"
   ```
   - Parse results to identify available theme constants
   - Populate `data/theme-mapping-rules.yaml` with ACTUAL constants found
   - If no custom constants found, use Material Theme defaults

5. **Read pubspec.yaml**: List current dependencies

**Output**: Create target analysis document

### Step 1.4: Generate Mappings

**Using AI reasoning with data files**:

1. **Component Mapping**:
   - Load `data/widget-equivalents.yaml`
   - For each icon in source (e.g., `LucideIcons.home`), find equivalent in yaml
   - Map to target equivalent (e.g., `Icons.home_outlined`)
   - Create component mapping table

2. **Asset Checklist**:
   - List all assets from source analysis
   - For each asset, determine if it exists in target
   - Create checklist of assets to copy

3. **Theme Mapping**:
   - Load `data/theme-mapping-rules.yaml`
   - For each hardcoded color in source, find matching rule
   - Map to target theme constant
   - Create theme mapping table

4. **Localization Check**:
   - Load `data/localization-dictionary.yaml`
   - Find all hardcoded text strings in source
   - Map to i18n keys from dictionary
   - List missing keys that need to be added

5. **Risk Assessment**:
   - Check for dependency conflicts
   - Check for SDK compatibility issues
   - Identify potential breaking points
   - Create risk assessment document

**Output**: Create mapping documents using templates

### Step 1.5: Present Analysis

Present all analysis documents to user:
- Analysis summary
- Component mapping table
- Asset checklist
- Theme mapping
- Risk assessment

**[⏸️ Gate]**: Wait for user approval before Phase 2.

## Phase 2: Code Generation

**Objective**: Generate converted Dart code with preserved logic hooks.

### Step 2.1: Create Backup

Use `scripts/backup_manager.py` to backup target files:
```bash
python .claude/skills/flutter-ui-converter/scripts/backup_manager.py \
  --action backup \
  --files <target-screen-file>
```

### Step 2.2: Extract UI from Source

**Using Read tool**, read source screen file again.

**Extract UI-only code**:
- Widget build methods
- UI helper methods (no business logic)
- Styling code

**Exclude**:
- Any async functions
- Any API calls
- Any Bloc/Cubit instantiation

### Step 2.3: Identify Logic Hooks in Target

**Using Read tool**, read target screen file again.

**Extract and preserve**:
- All BlocBuilder blocks (note line numbers)
- All BlocListener blocks
- All BlocConsumer blocks
- All event triggers
- All state references
- All callbacks

### Step 2.4: Merge UI + Logic

**Using AI reasoning**:

1. Take new UI structure from source
2. Insert preserved logic hooks from target at appropriate positions
3. Apply component mappings from Phase 1
4. Apply theme mappings from Phase 1
5. Apply localization mappings from Phase 1
6. Add conversion markers: `// [CONVERTED]: <description>`

### Step 2.5: Validate Against Guardrails

**Load** `data/forbidden-patterns.yaml`

**Check each guardrail** (G1-G8):

**G1: UI-Only Changes**
- Scan for forbidden patterns: `class.*Repository`, `class.*Service`, `class.*Bloc extends`
- Verify no business logic modified

**G2: Zero New Dependencies**
- Compare source and target pubspec.yaml
- Verify no new packages added

**G3: Logic Hook Preservation**
- Count BlocBuilder in original vs new
- Count event triggers in original vs new
- Verify all preserved

**G4: Asset Mapping**
- Check for hardcoded source paths
- Verify all assets mapped

**G5: i18n Compliance**
- Scan for `Text("hardcoded")` without `// TODO: i18n`
- Verify all text localized or marked

**G6: Feedback Loop**
- Verify conversion log template ready
- Ensure error tracking enabled

**G7: Theme Consistency**
- Check for `Color(0xFFxxxxxx)` without theme constant
- Verify theme mapping applied

**G8: Controller Disposal** ⚠️ CRITICAL
- Scan for `AnimationController(`, `TextEditingController(`, `FocusNode(`, `ScrollController(`
- For each found, verify `.dispose()` exists in same class
- If dispose() missing, add it or flag as error

### Step 2.6: Write Converted Code

**Using Write tool**, write the converted Dart file to target project.

### Step 2.7: Generate Conversion Log

Create `conversion-log.md` using template with:
- Files modified
- Logic hooks preserved (with evidence)
- Assets requiring manual copy
- Guardrail verification results
- Known issues encountered

**[⏸️ Gate]**: User tests converted code. Wait for feedback.

## Phase 3: Feedback Loop & Learning

**Objective**: Capture errors, extract patterns, improve skill.

### Step 3.1: Collect Feedback

If user reports issues:
- Log error details in conversion log
- Categorize: UI bug, logic break, asset missing, etc.

### Step 3.2: Update Knowledge Base

**Using Edit tool**, update data files:

- Add new issues to `data/known-issues.yaml`
- Add successful patterns to `data/pattern-library.yaml`

### Step 3.3: Generate Improvement Suggestions

Analyze feedback and suggest:
- Knowledge file updates
- New validation rules
- Guardrail enhancements

## Guardrails

| ID | Rule | Enforcement |
|---|---|---|
| **G1** | **UI-Only Changes** | No modifications to: Data Layer (models, repositories, API clients), Business Logic functions (async/await service calls), State variable names used by Bloc/Cubit. Scan with `data/forbidden-patterns.yaml`. |
| **G2** | **Zero New Dependencies** | Do not add packages to `pubspec.yaml`. Find equivalent widgets in existing dependencies using `data/widget-equivalents.yaml`. If impossible, STOP and ask user. |
| **G3** | **Logic Hook Preservation** | Preserve all: `BlocBuilder`/`BlocConsumer`/`BlocListener` blocks, Event triggers (`context.read<Bloc>().add()`), State references (`state.field`), Callbacks (`onPressed`, `onChanged`). Count before/after to verify. |
| **G4** | **Asset Mapping** | No hardcoded asset paths from Source. Map to Target paths using analysis or add to asset checklist. No new icon packages - map using `data/widget-equivalents.yaml`. |
| **G5** | **i18n Compliance** | No hardcoded text strings. Use Target's i18n system (`S.of(context).key` or `context.l10n.key`). Use `data/localization-dictionary.yaml` to find keys. If key missing, add `// TODO: i18n` and list in conversion log. |
| **G6** | **Feedback Loop Enforcement** | Always create conversion log. Always track issues. Always update knowledge base after each conversion. |
| **G7** | **Theme Consistency** | No hardcoded colors (`Color(0xFFxxxxxx)`). Use `Theme.of(context).colorScheme.*` or theme constants. Apply `data/theme-mapping-rules.yaml`. |
| **G8** | **Controller Disposal** ⚠️ CRITICAL | For any `AnimationController`, `TextEditingController`, `FocusNode`, `ScrollController` added, verify `.dispose()` exists in class. Scan with `data/forbidden-patterns.yaml` memory_leak_patterns. |
| **G9** | **Navigation Preservation** | Do not change navigation system. If Target uses `go_router`, preserve exact routing patterns. If Target uses `Navigator.push`, preserve exact patterns. No conversion between navigation libraries (e.g., go_router ↔ auto_route). |

### Guardrail Verification

Before completing Phase 2:
- Read `loop/phase2-verification.md`
- Verify each guardrail (G1-G9) with evidence
- Document results in conversion log

## Rollback Procedures

If conversion fails, see `loop/rollback-procedures.md` for:
- Phase 1 rollback (revert analysis)
- Phase 2 rollback (restore backups using `backup_manager.py`)
- Phase 3 rollback (remove incorrect feedback)
- Emergency rollback (critical bug detected)

## Data Files

Located in `.claude/skills/flutter-ui-converter/data/`:

- `widget-equivalents.yaml` - Icon and widget substitution mappings
- `theme-mapping-rules.yaml` - Color and text style mapping rules
- `forbidden-patterns.yaml` - Patterns that must not appear in code
- `localization-dictionary.yaml` - Common text → i18n key mappings
- `project-config.yaml` - Saved project paths
- `known-issues.yaml` - Known error patterns and mitigations
- `pattern-library.yaml` - Successful conversion patterns

## Scripts

Located in `.claude/skills/flutter-ui-converter/scripts/`:

- `backup_manager.py` - Manage file backups

## Error Policy

If critical error occurs:
1. Log error to conversion log
2. Use **AskUserQuestion** to notify user
3. **STOP** all operations
4. Do not proceed until issue resolved

## Success Criteria

- ✅ Zero business logic changes (G1)
- ✅ Zero new dependencies added (G2)
- ✅ All logic hooks preserved (G3)
- ✅ All assets mapped and copied (G4)
- ✅ All text localized or marked (G5)
- ✅ Feedback captured (G6)
- ✅ Theme consistency maintained (G7) - Aligned with `DESIGN.md`
- ✅ No memory leaks (G8)
- ✅ Navigation system preserved (G9)
- ✅ UI matches reference project visually and follows `DESIGN.md` guidelines
