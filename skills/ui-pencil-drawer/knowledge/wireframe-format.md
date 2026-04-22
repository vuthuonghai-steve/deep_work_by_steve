# Wireframe Blueprint Format Standard

> **Usage**: Load in Phase 0 boot. Required before Phase 2 (generate blueprints) and Phase 3 (interpret blueprints for drawing). Defines the DOM Tree format for single-screen wireframe files.
> **Source**: `resources/wireframe-format-draft.md` (100% transform — Parity: 8 sections → 8 sections)

---

## Table of Contents
- [Wireframe Blueprint Format Standard](#wireframe-blueprint-format-standard)
  - [Table of Contents](#table-of-contents)
  - [1. Overview](#1-overview)
  - [2. DOM Tree Hierarchy — 4 Levels](#2-dom-tree-hierarchy--4-levels)
    - [Level 0 — Screen Root Frame](#level-0--screen-root-frame)
    - [Level 1 — Composition Pattern](#level-1--composition-pattern)
    - [Level 2 — Component Slot](#level-2--component-slot)
    - [Level 3 — Text Override Notation](#level-3--text-override-notation)
  - [3. Source Citation Format](#3-source-citation-format)
  - [4. States](#4-states)
  - [5. Design Freedom \& Tagging Injection](#5-design-freedom--tagging-injection)
  - [6. Notation Summary Table](#6-notation-summary-table)
  - [7. Complete Example — Login Screen (M1)](#7-complete-example--login-screen-m1)
  - [8. Blueprint Validation Rules](#8-blueprint-validation-rules)

---

## 1. Overview

A Wireframe Blueprint is a markdown file describing the **DOM structure of 1 screen** as a hierarchical tree. One file = one screen. AI uses this file as a technical drawing spec to execute `batch_design` operations in Phase 3.

**Core Principles**:
- Each DOM Tree node maps **1:1** to one operation in `batch_design`
- Every component must have a `ref` pointing to a real node ID from Lib-Component (obtained in Phase 0 via `batch_get`). Never hardcode or invent IDs.
- Every component must have `spec-cite` tracing back to a specific spec file section
- Never add components not mentioned in the spec file

---

## 2. DOM Tree Hierarchy — 4 Levels

```
Level 0 — Screen Root Frame
  └── Level 1 — Composition Pattern (defines semantic grouping & high-level visual pattern)
        └── Level 2 — Component Slot (data binding with tag injection)
              └── Level 3 — Text/Override (specific content values)
```

### Level 0 — Screen Root Frame

Outermost frame for the entire screen. Maps to: `I(document, {type: "frame", name: "...", layout: "...", ...})`

```
# Screen: {screen-name}
> module: {M1|M2|M3|M4|M5|M6}
> spec: {spec-file-path} §{section-number}
> layout: vertical | horizontal
> width: 375 | 768 | 1440
> height: fit_content | {number}
> state: default | loading | error | empty
```

### Level 1 — Composition Pattern

Defines the creative visual structure. The AI is free to implement this pattern logically (e.g., using Grid/Flexbox with large paddings, Neo-brutalism borders, Background AI Images).
Maps to: `I(screenFrame, {type: "frame", layout: "...", fill: "...", ...})` + `G()` for immersive backgrounds.

```
## Section: {section-name}
> composition: split-screen | immersive-card | sidebar-layout | stacked
> styling: neo-brutalism | glassmorphism | minimal
> layout: vertical | horizontal
> width: fill_container | {px} | fit_content
> height: fit_content | fill_container
> gap: {number}          (default from layout-rules.yaml if omitted)
> padding: {number}      (or: {top} {right} {bottom} {left})
```

### Level 2 — Component Slot

Instance of a Lib-Component component. Maps to: `I(sectionFrame, {type: "ref", ref: nodeId, ...})` or `C(nodeId, sectionFrame, {...})`

```
- comp: {human-readable-name}
  ref: {NODE_ID}              # Real ID from Phase 0 component_map — NEVER hardcode or guess
  width: fill_container | {px} | fit_content
  height: fit_content | {px}
  spec-cite: [spec §{N}.{M}]  # MANDATORY — every component slot
  zone: strict | fluid         # strict = Lib only; fluid = creative allowed
  overrides:                   # Descendant property overrides (passed via C() descendants param)
    {child-field-id}: {value}  # Only real field IDs from component structure
```

### Level 3 — Text Override Notation

Override specific text content within a component. Uses special syntax to distinguish from layout properties:

```
  text@{field-id}: "Display content here"
```

**Example**:
```
- comp: primary-button
  ref: BTN_PRIMARY_ID
  width: fill_container
  spec-cite: [spec §2.1]
  zone: strict
  text@label: "Đăng nhập"
```

---

## 3. Source Citation Format

Every component slot **MUST** have `spec-cite`. Missing citation = component treated as hallucination by self-verify.

```
spec-cite: [spec §{section}]
spec-cite: [spec §{section}.{subsection}]
spec-cite: [spec §{section} — {short description}]
```

**Examples**:
```
spec-cite: [spec §3.1 — Login form fields]
spec-cite: [spec §5.2.1]
spec-cite: [spec §7 — Navigation bar]
```

---

## 4. States

Each screen can have multiple states. **Default: draw only `default` state.** Draw additional states only when spec explicitly mentions them.

```
## States
- default: Standard visible state (always draw)
- loading?: Loading/fetching data state (draw only if spec §N mentions it)
- error?: Validation or network error state (draw only if spec §N mentions it)
- empty?: No data / empty collection state (draw only if spec §N mentions it)
```

The `?` suffix = optional/conditional (depends on spec mention).

---

## 5. Design Freedom & Tagging Injection

**1. Creative Presentation Contract (The Freedom)**
The AI is encouraged to use bold Composition Patterns (e.g., dividing screen 50/50, applying full-bleed AI images `G()`, adding thick borders, hard shadows). The visual presentation boundaries are wide open as long as it aligns with the project's Neo-brutalism or modern aesthetic.

**2. Semantic Data Contract (The Restriction)**
While layout and styling are fluid, **the data logic is 100% strict**.
Every Component Slot defined in the UI Spec MUST be drawn, and NO extra functional fields may be invented.

**3. Tagging Injection (The Verification Anchor)**
When drawing nodes in Phase 3, you **MUST** inject the `spec-cite` into the drawn node's properties (e.g., in the `name` field or `context.cite`) to allow Reverse Verification later. 
Example: `I(form, {type: "frame", name: "input-email [spec §2.1]"})`

---

## 6. Notation Summary Table

| Symbol | Meaning | Example |
|--------|---------|---------|
| `# Screen:` | Level 0 — screen root frame | `# Screen: m1/login` |
| `## Section:` | Level 1 — layout area | `## Section: form-area` |
| `- comp:` | Level 2 — component instance | `- comp: input-email` |
| `ref:` | Node ID from Lib-Component | `ref: INP_TEXT_001` |
| `text@{id}:` | Level 3 text override | `text@label: "Email"` |
| `spec-cite:` | Mandatory source citation | `spec-cite: [spec §3.1]` |
| `zone:` | strict or fluid | `zone: strict` |
| `overrides:` | Descendant property map | `overrides: {child_id: value}` |
| `?` after state name | Optional state | `error?:` |
| `CAPS_UNDERSCORE` ID | Placeholder — replace with real ID from batch_get | `ref: BTN_PRIMARY_ID` |
| `FEkTl`-style ID | Real Pencil node ID — use directly | `ref: FEkTl` |

**ID Rule**: Uppercase + underscore IDs (e.g., `BTN_PRIMARY_ID`) are placeholders Phase 0 must resolve. Short alphanumeric IDs (e.g., `FEkTl`, `Njux9`) are real Pencil node IDs obtained from `batch_get`.

---

## 7. Complete Example — Login Screen (M1)

```markdown
# Screen: m1/login
> module: M1
> spec: Docs/life-2/ui/specs/m1-auth-ui-spec.md §3
> state: default

## Section: hero-area
> composition: split-screen
> styling: neo-brutalism

- comp: heading-text
  ref: TEXT_H1_ID
  width: fill_container
  spec-cite: [spec §3.2 — Login heading]
  text@content: "Chào mừng trở lại"

## Section: form-area
> composition: stacked
> styling: neo-brutalism

- comp: input-email
  ref: INPUT_TEXT_ID
  width: fill_container
  spec-cite: [spec §3.3 — Email field]
  text@label: "Email"

- comp: input-password
  ref: INPUT_PASSWORD_ID
  width: fill_container
  spec-cite: [spec §3.3 — Password field]
  text@label: "Mật khẩu"

## Section: cta-area
> composition: stacked
> styling: neo-brutalism

- comp: button-primary
  ref: BTN_PRIMARY_ID
  width: fill_container
  spec-cite: [spec §3.4 — Login CTA button]
  text@label: "Đăng nhập"

## States
- default: Empty form, button enabled, no error messages
- error?: Inline error below invalid field — spec §3.5
- loading?: Button disabled + spinner while submitting — spec §3.4
```

---

## 8. Blueprint Validation Rules

Before using a blueprint in Phase 3, self-verify:

```
□ Every `# Screen:` has: module, spec, layout, width, state?
□ Every `- comp:` has: ref, spec-cite, zone?
□ No `ref:` is empty, "?", or "undefined"?
□ All text overrides use correct `text@{id}:` notation?
□ States section exists with at least `default`?
□ Total components in 1 screen ≤ 20? (if > 20, split into sub-sections)
□ All CAPS_UNDERSCORE IDs resolved to real nodeIds from Phase 0 component_map?
```
