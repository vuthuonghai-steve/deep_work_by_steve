# build-checklist — Admin List View Builder Verification Checklist

> **Usage**: Triggered **automatically** after Phase 3 (Generate) ends. No user request needed.
> Reference: design.md §2.2 Step 4, §3.5 Loop Zone Protocol, §2.3 Guardrails.

---

## Run Instructions

After Phase 3 completes, run this checklist **without prompting the user**:

1. Read all generated files.
2. Apply each checklist item below.
3. Interpret results:
   - **All pass** → proceed to Phase 5 DELIVER.
   - **Any fail** → show violated rules list → prompt: `Fix now? (Retry / Abort)`

---

## Checklist Items

### Item 1 — §3 Zone Files Completeness
**Rule**: All files listed in design.md §3 Zone Mapping must be created.

**Required files** (source: design.md §3):

| # | File | Location |
|---|------|----------|
| 1 | `*_bloc.dart` | `bloc/` |
| 2 | `*_event.dart` | `bloc/` |
| 3 | `*_state.dart` | `bloc/` |
| 4 | `*_page.dart` | `pages/` |
| 5 | `*_list_view.dart` | `widgets/` |
| 6 | `*_card.dart` | `widgets/` |
| 7 | `*_card_shimmer.dart` | `widgets/` |
| 8 | `*_status_filter_chip.dart` | `widgets/` |
| 9 | `*_constants.dart` | `constants/` |

**Pass criteria**: All 9 files exist at expected paths.
**Fail**: List missing files.

---

### Item 2 — BLoC Import Correctness
**Rule**: `*_event.dart` and `*_state.dart` must use `part of` directive referencing the correct `*_bloc.dart`.

**Pass criteria**: Both `*_event.dart` and `*_state.dart` contain `part of '<entity>_bloc.dart'` and `*_bloc.dart` contains `part '<entity>_event.dart'` and `part '<entity>_state.dart'`.
**Fail**: List files with incorrect `part` directives.

---

### Item 3 — Page Wiring Only (G1 Anti-Pattern)
**Rule**: `pages/*_page.dart` must contain ONLY `BlocProvider` + `Scaffold`. No UI widgets (no `ListView`, `Column` with children, `Card`, `Container` with children, etc.).

**Pass criteria**: `body:` in `Scaffold` contains exactly ONE widget: the `*_list_view.dart` widget. No conditional logic based on data.
**Fail**: List violations with line numbers.

**Concrete check** — search for forbidden patterns:
```dart
// ❌ FORBIDDEN in *page.dart body:
ListView.builder
ListView.separated
Column(children: [
Row(children: [
Card(
Container(
Text(   // any Text widget
```

---

### Item 4 — Shared Components (G2 Anti-Pattern)
**Rule**: `widgets/*_card.dart` must use shared design tokens. No raw `Color(0xFF...)`, `Colors.xxx`, `Colors.` in any `widgets/` file.

**Pass criteria**: Grep `widgets/` for the following forbidden patterns — zero matches:
- `Color(0xFF` — hard-coded hex color
- `Colors.` — Colors class reference (except `Colors.transparent` if explicitly allowed)
- `TextStyle(color:` — inline style with hard-coded color

**Fail**: List file + line number for each violation.

**Allowed** (correct usage):
```dart
ColorSkin.accentBlue()          // ✅ OK
ColorSkin.border()              // ✅ OK
TypoSkin.body()                 // ✅ OK
Theme.of(context).textTheme...   // ✅ OK
```

---

### Item 5 — Constants Isolation (C1 Rule)
**Rule**: `constants/*_constants.dart` must contain ONLY `const`/`static const` declarations. No logic (`if`, `else`, `switch`, functions, computed values). No imports from `bloc/`, `pages/`, `widgets/`.

**Pass criteria**: File contains only:
- `const List<String>`
- `const int`
- `const String`
- `// comments`

**Fail**: List non-const declarations or forbidden imports.

---

### Item 6 — Shimmer Present (R1)
**Rule**: If `*_state.dart` defines `Loading` state, then `*_card_shimmer.dart` must exist and be referenced in `*_list_view.dart`.

**Pass criteria**: Both conditions are true:
1. `*_state.dart` contains `<Entity>ListLoading` state.
2. `*_list_view.dart` imports and uses `<Entity>CardShimmer` when state is `Loading`.

**Fail**: Missing shimmer file or shimmer not used in list view.

---

### Item 7 — Line Count (R1)
**Rule**: No generated file may exceed **300 lines**.

**Pass criteria**: All files pass `wc -l` ≤ 300.

**Fail**: List files exceeding 300 lines with their line count.

---

## Violation Report Format

```markdown
## ❌ Verification Failed

| # | Item | File(s) | Details |
|---|------|---------|---------|
| 3 | Page Wiring Only | `pages/order_list_page.dart` | Line 12: ListView.builder found in body |
| 4 | Shared Components | `widgets/order_card.dart` | Line 7: `Color(0xFF1A73E8)` |
| 7 | Line Count | `widgets/order_list_view.dart` | 387 lines (exceeds 300) |

Total: 3 violations
```
