# clean-architecture-rules — Flutter Clean Architecture Rules for List Pages

> **Usage**: Read at Boot Sequence (Tier 1). Enforced by `loop/build-checklist.md`. These rules are cross-project reusable.

---

## 1. Layer Structure

```
lib/
├── app/           # Bootstrap: app root, theme, router, DI
├── core/          # Shared utilities, network, errors
├── domain/        # Entities, repository interfaces (abstract)
├── data/          # Repository implementations, models, datasources
├── features/      # Feature modules (each self-contained)
│   └── role_admin/
│       └── <entity>/
│           ├── bloc/
│           ├── domain/        ← repository interface
│           ├── data/          ← repository impl, models
│           ├── pages/
│           ├── widgets/
│           └── constants/
└── shared/        # Reusable UI + cross-feature helpers only
```

**Dependency direction**: `features → domain ← data`
- Features MAY import domain.
- Features MUST NOT import data directly.
- Shared components are allowed from `lib/shared/`.

---

## 2. File Size Limit: 300 Lines

### Rule R1 — Hard Limit

> Any file exceeding **300 lines** MUST be split.

**How to split**:
- Extract reusable sub-widgets → new `*_sub_widget.dart` in `widgets/`
- Extract helper logic → new `*_helpers.dart` in same folder
- Extract constants → move to `constants/*_constants.dart`

**Enforcement**: `loop/build-checklist.md` item #7 checks line count.

---

## 3. Shared Components — Single Source of Truth

### Rule R2 — Color

> **NEVER** use raw `Color(0xFF...)`, `Colors.xxx`, `Color.fromRGBO(...)` in feature code.

**Correct usage** — always from `ColorSkin`:
```dart
ColorSkin.accentBlue()          // primary accent
ColorSkin.accentBlue(alpha: 0.15) // with opacity
ColorSkin.textPrimary()         // main text
ColorSkin.textSecondary()       // secondary text
ColorSkin.border()              // border color
ColorSkin.surface()             // card/surface background
ColorSkin.background()          // scaffold background
ColorSkin.error()                // error state
ColorSkin.success()              // success state
ColorSkin.warning()              // warning state
```

**Wrong** (❌ Forbidden):
```dart
Color(0xFF1A73E8)       // hard-coded hex
Colors.blue
Colors.grey.shade300
Color.fromRGBO(26, 115, 232, 1.0)
```

### Rule R3 — Typography

> **NEVER** use raw `TextStyle(...)`, `FontWeight.w600` in feature code.

**Correct usage** — always from `TypoSkin` or `Theme.of(context)`:
```dart
TypoSkin.heading()        // h1 heading
TypoSkin.subheading()     // h2 heading
TypoSkin.body()           // body text
TypoSkin.caption()        // caption/small text
TypoSkin.button()         // button label

// With overrides
TypoSkin.body().copyWith(
  color: ColorSkin.textPrimary(),
  fontWeight: FontWeight.w600,
)
```

**Wrong** (❌ Forbidden):
```dart
TextStyle(color: Colors.blue, fontSize: 14, fontWeight: FontWeight.w600)
Text('Label', style: TextStyle(fontSize: 12))
```

### Rule R4 — Theme

> Prefer `Theme.of(context)` for theme-aware values when in a `build(BuildContext context)` method.

```dart
// ✅ Good
Widget build(BuildContext context) {
  return Text(
    'Title',
    style: Theme.of(context).textTheme.titleMedium,
  );
}
```

### Rule R5 — Spacing & Radius

> Use shared spacing/radius tokens, not raw `EdgeInsets.all(16)` or `BorderRadius.circular(8)`.

```dart
// ✅ Good
Padding(
  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
)
// ✅ Better: if shared spacing constants exist
context.spacePadding()

// ✅ Good radius
BorderRadius.circular(12.radius)
// ✅ Better: if shared radius constants exist
RadiusSkin.card(),
```

---

## 4. Dependency Direction Rules

### Rule D1 — Features Must Not Import Data Layer

```dart
// ❌ WRONG — feature importing data layer directly
import '../../data/repositories/order_repository_impl.dart';

// ✅ CORRECT — feature imports domain (abstract) only
import '../../domain/repositories/order_repository.dart';
```

### Rule D2 — BLoC Is the Sole Mediator

- UI (`widgets/`) MUST NOT import data models directly.
- UI receives data through BLoC state.
- All data transformations happen in BLoC or below (repository/datasource).

---

## 5. `*_page.dart` Rules

### Rule P1 — Page Is Wiring ONLY

`pages/*_page.dart` is the **thin layer** between the router and the UI.

**Permitted contents**:
- `BlocProvider` or `MultiBlocProvider`
- `Scaffold` with `appBar`, `body`, `floatingActionButton`
- `Navigation` calls
- Delegation to a single widget (`const <Entity>ListView()`)

**Forbidden contents**:
- `ListView.builder`, `Column`, `Row` inside `body`
- `Card`, `Container` with children
- Any business logic
- Any conditional rendering based on data

```dart
// ❌ WRONG — body contains a ListView
Scaffold(
  appBar: AppBar(),
  body: ListView.builder(...)  // ❌ FORBIDDEN
)

// ✅ CORRECT — body is a single widget
Scaffold(
  appBar: AppBar(),
  body: const OrderListView(),  // ✅ OK
)
```

### Rule P2 — Page Max 30 Lines

A correctly written `*_page.dart` should never exceed 30 lines. If it does, you are likely putting UI in it.

---

## 6. `constants/*.dart` Rules

### Rule C1 — Pure Data, No Logic

`constants/*_constants.dart` files must contain **only**:
- `const` or `static const` declarations
- `List<String>` for filter options
- `int` for pagination sizes
- `String` for date formats, label texts

**Forbidden**:
- `if/else`, `switch` statements
- Function bodies
- Imports from `bloc/`, `pages/`, `widgets/`
- Non-const variables

---

## 7. Anti-Pattern Gallery

### AP1 — Hard-coded Color (G2)
```dart
// ❌ WRONG
Container(color: Color(0xFF123456))
Text('Label', style: TextStyle(color: Colors.blue))

// ✅ FIX
Container(color: ColorSkin.accentBlue())
Text('Label', style: TypoSkin.body().copyWith(color: ColorSkin.textPrimary()))
```

### AP2 — UI in Page (G1)
```dart
// ❌ WRONG — Scaffold body contains a Column with children
body: Column(children: [
  Text('Header'),
  ListView.builder(...),
  Text('Footer'),
]),

// ✅ FIX — extract to a widget
body: const OrderListView(),
```

### AP3 — Feature Importing Data Directly
```dart
// ❌ WRONG
import 'package:ktx_app/features/role_admin/order/data/repositories/order_repository_impl.dart';

// ✅ FIX — use domain interface
import 'package:ktx_app/features/role_admin/order/domain/repositories/order_repository.dart';
```

### AP4 — Logic in Constants
```dart
// ❌ WRONG
const String getStatusLabel => status == 'active' ? 'Active' : 'Inactive';

// ✅ FIX — constants are pure data
const List<String> orderStatusOptions = ['All', 'Pending', 'Active', 'Completed'];
```

---

## 8. Project Overlay

> This section allows temporary project-specific overrides when local rules conflict.

**When to use**: If the current project has a shared component with a slightly different API than described here, the local project override takes precedence for that specific project only.

**How**: Before generating, check if the project has:
- Custom `ColorSkin` values not listed above → use project's version
- Custom `TypoSkin` keys not listed above → use project's version
- Custom `radius` or `spacing` tokens → use project's version

**When NOT to use**: Never use this to bypass G1 (UI in page) or G2 (hard-coded colors). Those rules are absolute.

---

## 9. Verification Checklist

| Rule | What to Check | How to Verify |
|------|---------------|---------------|
| R1 | No file > 300 lines | Count lines in each generated file |
| R2 | No raw Color/Colors in widgets | Grep for `Color(0xFF`, `Colors.` in `widgets/` |
| R3 | No raw TextStyle in widgets | Grep for `TextStyle(` in `widgets/` |
| D1 | Domain import only in features | Grep for `data/repositories` imports in features |
| P1 | Page has no ListView/Column in body | Read `pages/*_page.dart` |
| P2 | Page ≤ 30 lines | Count lines |
| C1 | Constants file has no logic | Read `constants/*_constants.dart` |
