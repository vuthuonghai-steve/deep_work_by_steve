---
name: admin-list-view-builder
description: Generates production-ready Flutter Clean Architecture list pages for any feature module. Use when creating a new list page with BLoC, paging, filter chips, shimmer loading, and card display in features/<feature>/<entity>/. BLoC pattern, shared components, and Clean Architecture rules are self-contained in knowledge/. Output: bloc/*_bloc.dart, *_event.dart, *_state.dart, pages/*_page.dart, widgets/*_list_view.dart, *_card.dart, *_card_shimmer.dart, *_status_filter_chip.dart, constants/*_constants.dart.
disable-model-invocation: true
---

# admin-list-view-builder

> **Persona**: Admin List Architect — generates boilerplate list pages with zero architectural drift.

> **Usage**: Invoke when creating a new list page for any `features/<feature>/<entity>/` module. Self-contained — no external project reference needed.

---

## Workflow Progress Tracker

Copy this checklist into your response and mark progress:

```markdown
### [admin-list-view-builder] Progress:
- [ ] Phase 1: BOOT
- [ ] Phase 2: ANALYZE → [⏸️ Gate: User confirm filter + card design]
- [ ] Phase 3: GENERATE → [⏸️ Gate: Partial failure?]
- [ ] Phase 4: VERIFY → [⏸️ Gate: Checklist fail?]
- [ ] Phase 5: DELIVER
```
---

## Boot Sequence (Tier 1 — Mandatory, every invocation)

> ⚠️ Read BOTH files before writing ANY code.

1. Read [knowledge/admin-list-page-pattern.md](knowledge/admin-list-page-pattern.md) — list-specific Clean Architecture pattern.
2. Read [knowledge/clean-architecture-rules.md](knowledge/clean-architecture-rules.md) — 300 lines limit, shared components, anti-pattern examples.

---

## Phase 1: BOOT

1. Receive user input: `entity name` + `repo path` OR `entity field list`.
2. If repo path provided: resolve to entity definition, extract field names and types.
3. If repo path invalid: return graceful error listing available entities in `features/`.
4. If entity has >20 fields: select top-N fields by business priority + mark others as "hidden detail fields" — user confirms at Gate 2.

---

## Phase 2: ANALYZE

**Before this phase**: No extra files needed (Tier 1 already loaded).

### Step 2a — Propose Filter Chips
Based on entity fields:
- Identify fields with finite enum/status values → propose as filter chips.
- Default: show all. Each chip filters one status value.
- Output: `<entity>_status_filter_options` list.

### Step 2b — Propose Card Fields
Based on entity fields:
- Select 4–6 most important display fields (name/id, status, date, summary field).
- Output: `<entity>_card_field_specs` list with field name + display label.

### Step 2c — Draft Spec Artifact
Generate `<entity>_draft_spec.md` as an artifact containing:
- Entity name, field list
- Proposed filter chips (name + values)
- Proposed card fields (field name + label)
- Pagination type: **offset-based** (default, per design.md §9 Q3)

---

### ⏸️ Gate 2 — User Confirm (Interaction Point #1)

**Hard rule**: DO NOT proceed to Phase 3 without user signal.

Display `<entity>_draft_spec.md` and prompt:
```
Filter + Card Design — choose one:
  (a) Confirm as-is
  (b) Modify filter chips
  (c) Modify card fields
  (d) Cancel
```

If user selects **(d)**: exit skill.
If **(b)** or **(c)**: collect modifications → regenerate draft → re-prompt until **(a)**.

---

## Phase 3: GENERATE

**Read before this phase** (Tier 2 — Conditional):
- [templates/admin-list-page-template.dart](templates/admin-list-page-template.dart) — code templates with Placeholder markers.

### Step 3a — Generate Files

Create the following files under `features/<feature>/<entity>/`:

| File | Content |
|------|---------|
| `bloc/<entity>_bloc.dart` | BLoC with `<Entity>List` state, `Load<Entity>List` event, `PaginationType.offset` |
| `bloc/<entity>_event.dart` | Events: `Load<Entity>List`, `Filter<Entity>ByStatus`, `Refresh<Entity>List` |
| `bloc/<entity>_state.dart` | States: `Initial`, `Loading`, `Loaded`, `Error` with `PagingController` |
| `pages/<entity>_page.dart` | **Wiring ONLY**: `BlocProvider` + `Scaffold` + `<Entity>ListView`. NO UI widgets. |
| `widgets/<entity>_list_view.dart` | `PagingView.builder` with `<Entity>Card`, shimmer, status filter chips |
| `widgets/<entity>_card.dart` | Card UI using **shared components only** (see anti-patterns below) |
| `widgets/<entity>_card_shimmer.dart` | Shimmer placeholder matching `<Entity>Card` layout |
| `widgets/<entity>_status_filter_chip.dart` | Horizontal chip list for status filter |
| `constants/<entity>_constants.dart` | Filter options, pagination config, date format constants. NO logic. |

### Step 3b — Partial Failure Handling

If any file fails to generate:
1. List all failed files with error reason.
2. Prompt: `Retry failed files? (Retry / Abort)`
3. Retry only failed files.
4. If retry succeeds: continue. If retry fails again: abort.

### ⏸️ Gate 3 — Post-Generate Review (Interaction Point #2)

After all files generated successfully:
Display file tree and prompt:
```
Generated files:
  <file list>

Review before verify? (Y/N)
```
- If **N**: skip to Phase 4.
- If **Y**: show brief summary of each file.

---

## Phase 4: VERIFY

**Read before this phase** (Tier 2 — Conditional):
- [loop/build-checklist.md](loop/build-checklist.md) — auto-triggered checklist.

### §3.5 Loop Zone Protocol (Auto-trigger)

`loop/build-checklist.md` runs **automatically** after Phase 3 ends — no user request needed.

**Pass** → proceed to Phase 5 DELIVER.
**Fail** → show violated rules list → prompt: `Fix now? (Retry / Abort)`

- **Retry**: loop back to Phase 3, regenerate violated files only.
- **Abort**: exit skill with partial output.

---

## Phase 5: DELIVER

1. Display final file tree.
2. Confirm all files are in `features/<feature>/<entity>/`.
3. Summary: entity name, filter chips count, card fields count, pagination type.

---

## Anti-Pattern Examples (Hard Rules)

These patterns are **ABSOLUTELY FORBIDDEN**. Code containing them fails verification.

### ❌ G1 Anti-Pattern: UI in `*_page.dart`

`pages/<entity>_page.dart` MUST contain ONLY wiring — `BlocProvider` + `Scaffold` + delegation to `<Entity>ListView`.

```dart
// ❌ WRONG — UI inside *_page.dart
class OrderListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Orders')),
      body: ListView.builder(    // <-- FORBIDDEN
        itemCount: 10,
        itemBuilder: (_, __) => Card(
          child: ListTile(title: Text('Order #1')), // <-- FORBIDDEN
        ),
      ),
    );
  }
}
```

```dart
// ✅ CORRECT — page is pure wiring
class OrderListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => OrderListBloc()..add(const LoadOrderList()),
      child: Scaffold(
        appBar: AppBar(title: Text('Orders')),
        body: const OrderListView(),
      ),
    );
  }
}
```

### ❌ G2 Anti-Pattern: Hard-coded Colors and Fonts

**ALL** color and typography values MUST come from `ColorSkin`, `TypoSkin`, or `Theme.of(context)`. Zero exceptions.

```dart
// ❌ WRONG — hard-coded color
Container(
  decoration: BoxDecoration(
    color: Color(0xFF1A73E8),       // <-- FORBIDDEN
    borderRadius: BorderRadius.circular(8),
  ),
  child: Text(
    'Active',
    style: TextStyle(
      color: Colors.blue,            // <-- FORBIDDEN
      fontWeight: FontWeight.w600,
    ),
  ),
)
```

```dart
// ✅ CORRECT — using shared design tokens
Container(
  decoration: BoxDecoration(
    color: ColorSkin.accentBlue(),
    borderRadius: BorderRadius.circular(8.radius),
  ),
  child: Text(
    'Active',
    style: TypoSkin.caption().copyWith(
      color: ColorSkin.textPrimary(),
      fontWeight: FontWeight.w600,
    ),
  ),
)
```

```dart
// ❌ WRONG — raw Colors reference in widget
Text('Status', style: TextStyle(color: Colors.grey))  // <-- FORBIDDEN

// ✅ CORRECT — token from theme
Text('Status', style: Theme.of(context).textTheme.bodySmall)
```

### ❌ G3 Anti-Pattern: File Over 300 Lines

If a generated file exceeds 300 lines, **split it immediately**:
- Extract sub-widgets into separate `*_widget.dart` files.
- Extract helper methods into `*_helpers.dart`.
- Keep each file under 300 lines.

---

## §3.5 Loop Zone Protocol — Reference

`loop/build-checklist.md` checklist items:

1. All §3 files created
2. `bloc/*_event.dart` + `*_state.dart` import correct (domain + data layers)
3. `pages/*_page.dart` contains ONLY `BlocProvider` + `Scaffold` (no UI widgets)
4. `widgets/*_card.dart` uses shared components — zero `Color(0xFF...)` or `Colors.xxx` literals
5. `constants/*_constants.dart` is pure data (no logic, no imports from bloc/pages/widgets)
6. `widgets/*_card_shimmer.dart` present if loading state is defined
7. No generated file exceeds 300 lines
