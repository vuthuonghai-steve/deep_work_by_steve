# Phase 2: Code Generation & Verification Checklist

Use this checklist to verify Phase 2 completion before user testing.

---

## 1. Pre-Generation Backup

- [ ] Backup created using `backup_manager.py`
- [ ] Backup manifest generated
- [ ] Backup timestamp recorded in conversion log
- [ ] Verified backup contains all target files

---

## 2. Source UI Extraction

- [ ] Source Dart files read
- [ ] Widget build methods extracted
- [ ] UI-only helper methods identified
- [ ] Styling constants collected
- [ ] Non-UI code excluded

---

## 3. Target Logic Hook Identification

- [ ] Target Dart files read
- [ ] All `BlocBuilder` blocks identified
- [ ] All `BlocConsumer` blocks identified
- [ ] All `BlocListener` blocks identified
- [ ] All event triggers documented (`context.read<Bloc>().add()`)
- [ ] All state references documented (`state.field`)
- [ ] All callbacks documented (`onPressed`, `onChanged`, etc.)

---

## 4. UI + Logic Merge

- [ ] New UI structure from Source applied
- [ ] Existing logic hooks from Target preserved
- [ ] BlocBuilder builder functions updated (UI only)
- [ ] BlocListener listener functions preserved (no changes)
- [ ] Event triggers re-attached to new UI elements
- [ ] State references mapped to new widgets
- [ ] Callbacks preserved

---

## 5. Guardrail Verification (G1-G9)

### G1: UI-Only Changes

**Rule**: No modifications to Data Layer, Business Logic, or State Management classes.

- [ ] **Check modified files list**
  - [ ] No files in `lib/data/` or `lib/domain/`
  - [ ] No files in `lib/repositories/`
  - [ ] No files in `lib/services/`
  - [ ] Only files in `lib/presentation/` or `lib/ui/`

- [ ] **Scan for forbidden patterns**
  - [ ] No `class *Repository` modifications
  - [ ] No `class *Service` modifications
  - [ ] No `class *Bloc extends` modifications
  - [ ] No `class *Cubit extends` modifications
  - [ ] No `class *Event` modifications
  - [ ] No `class *State` modifications

**Verification command**:
```bash
grep -r "class.*Repository\|class.*Bloc extends" lib/presentation/
# Should return no results
```

**Status**: ⬜ PASS / ⬜ FAIL

---

### G2: Zero New Dependencies

**Rule**: No new packages added to pubspec.yaml.

- [ ] **Compare pubspec.yaml**
  - [ ] Read original pubspec.yaml (from backup)
  - [ ] Read current pubspec.yaml
  - [ ] Diff the dependencies section
  - [ ] Verify no new entries

- [ ] **Check for substitutions**
  - [ ] All icon packages substituted (lucide_icons → Icons)
  - [ ] All UI packages use existing dependencies

**Verification command**:
```bash
diff backups/{timestamp}/pubspec.yaml pubspec.yaml
# Should show no changes in dependencies section
```

**Status**: ⬜ PASS / ⬜ FAIL

---

### G3: Logic Hook Preservation

**Rule**: All Bloc/Cubit hooks, event triggers, state references, and callbacks preserved.

- [ ] **BlocBuilder preservation**
  - [ ] Count BlocBuilders in original: ___
  - [ ] Count BlocBuilders in new code: ___
  - [ ] Counts match

- [ ] **Event triggers preservation**
  - [ ] All `context.read<Bloc>().add()` calls preserved
  - [ ] Event types unchanged

- [ ] **State references preservation**
  - [ ] All `state.field` references preserved

- [ ] **Callbacks preservation**
  - [ ] All `onPressed`, `onChanged`, `onTap` callbacks preserved

**Verification command**:
```bash
grep -c "BlocBuilder<" lib/presentation/screens/[screen].dart
grep -c "\.add(" lib/presentation/screens/[screen].dart
```

**Status**: ⬜ PASS / ⬜ FAIL

---

### G4: Asset Mapping

**Rule**: No hardcoded source asset paths. All assets mapped or documented.

- [ ] **Check asset paths**
  - [ ] No source project paths (e.g., `assets/images/.*redo-AI`)
  - [ ] All assets mapped to target paths
  - [ ] Asset checklist created for manual copy

- [ ] **Check icon substitutions**
  - [ ] No `LucideIcons` or `FeatherIcons` imports
  - [ ] All icons mapped to Material Icons

**Verification command**:
```bash
grep -r "assets/.*redo-AI\|LucideIcons\|FeatherIcons" lib/presentation/
# Should return no results
```

**Status**: ⬜ PASS / ⬜ FAIL

---

### G5: i18n Compliance

**Rule**: No hardcoded text strings IF target project has i18n system.

- [ ] **Pre-Check: Detect i18n System (REQUIRED FIRST)**
  ```bash
  grep -r "S\.of(context)\|context\.l10n\|AppLocalizations" lib/ --include="*.dart" -l
  find . -name "*.arb"
  ```
  - [ ] **If NO i18n found** → SKIP G5, preserve hardcoded text as-is
  - [ ] **If i18n found** → ENFORCE rules below

- [ ] **Scan for hardcoded strings** (only if i18n exists)
  - [ ] All `Text()` widgets use i18n or have `// TODO: i18n`
  - [ ] All `hintText`, `labelText` use i18n

**Verification command**:
```bash
grep -n 'Text("[^"]*")' lib/presentation/screens/[screen].dart
# Should only return numbers/symbols or have TODO comment
```

**Status**: ⬜ PASS / ⬜ FAIL / ⬜ SKIPPED (no i18n system)

---

### G6: Feedback Loop Enforcement

**Rule**: Always create conversion log and track issues.

- [ ] **Check conversion log created**
  - [ ] File exists in `.skill-context/flutter-ui-converter/logs/`
  - [ ] Contains session ID and timestamp
  - [ ] Has all required sections filled

- [ ] **Check issues tracked**
  - [ ] "Issues to Report" section populated (or marked "None")
  - [ ] New issues documented with severity level

**Status**: ⬜ PASS / ⬜ FAIL

---

### G7: Theme Consistency

**Rule**: Use theme constants instead of hardcoded values.

- [ ] **Check color usage**
  - [ ] Prefer `Theme.of(context).colorScheme.*` over `Color(0xFFxxxxxx)`
  - [ ] Use discovered theme constants from Phase 1

- [ ] **Check text styles**
  - [ ] Prefer `Theme.of(context).textTheme.*` over hardcoded TextStyle

**Verification command**:
```bash
grep -c "Color(0x" lib/presentation/screens/[screen].dart
# Lower count is better
```

**Status**: ⬜ PASS / ⬜ FAIL

---

### G8: No Memory Leaks

**Rule**: All controllers must have dispose() methods.

- [ ] **Check controllers**
  - [ ] AnimationController has dispose()
  - [ ] TextEditingController has dispose()
  - [ ] FocusNode has dispose()
  - [ ] ScrollController has dispose()

**Verification command**:
```bash
grep "Controller(" lib/presentation/screens/[screen].dart
# Then verify each has corresponding dispose()
```

**Status**: ⬜ PASS / ⬜ FAIL

---

### G9: Navigation Consistency

**Rule**: Navigation pattern matches target project's existing system.

- [ ] **Check navigation pattern**
  - [ ] Uses same pattern as target (Navigator.pushNamed vs context.push vs AutoRouter)
  - [ ] No new navigation packages added

**Verification command**:
```bash
grep "Navigator\.\|context\.push\|AutoRouter" lib/presentation/screens/[screen].dart
# Verify pattern matches target project
```

**Status**: ⬜ PASS / ⬜ FAIL

---

## 6. Conversion Markers

- [ ] Added `// [CONVERTED]:` comments at key points
- [ ] Markers explain what changed
- [ ] Markers note preserved logic

---

## 7. Code Quality

### Formatting
- [ ] Code follows Dart formatting (dart format)
- [ ] Imports organized
- [ ] No unused imports/variables

### Best Practices
- [ ] Used `const` where possible
- [ ] Used `Expanded`/`Flexible` for responsive layout
- [ ] Added `SafeArea` where appropriate

### Widget Structure
- [ ] Extracted complex widgets into separate classes
- [ ] Preferred `StatelessWidget` over functions
- [ ] Avoided deep nesting (max 4-5 levels)

---

## 8. Conversion Log Generation

- [ ] `conversion-log.md` created using template
- [ ] Files modified listed
- [ ] Logic hooks preserved documented
- [ ] Assets requiring manual copy listed
- [ ] Known issues encountered documented
- [ ] Guardrail verification table filled
- [ ] Testing checklist included

---

## 9. Pre-Testing Verification

- [ ] Code compiles (no syntax errors)
- [ ] No analyzer errors
- [ ] No missing imports

**Run**:
```bash
flutter analyze
dart format --set-exit-if-changed .
```

---

## 10. User Testing Gate

- [ ] Present conversion log to user
- [ ] Highlight:
  - Files modified
  - Logic hooks preserved
  - Assets needing manual copy
  - Known issues
- [ ] Provide testing checklist
- [ ] Ask user to test converted screen

---

## Completion Criteria

✅ **Phase 2 is complete when**:
- All checkboxes above are marked
- All guardrails pass (or skipped with reason)
- User has tested the converted screen
- User reports success OR issues are logged for Phase 3

---

**Next Phase**: Phase 3 - Feedback Loop (if issues found) or Complete (if success)
