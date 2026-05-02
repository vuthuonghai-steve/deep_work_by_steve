# Pencil MCP Tools Reference

> **Usage**: Load in Phase 0 boot. Required before any Pencil canvas operation. Contains tool API syntax, layout rules, script patterns, creativity zones, and trigger flags.
> **Source**: `resources/pencil-mcp-agent-rules.md` (100% transform — Parity: 6 sections → 6 sections)

---

## Table of Contents
- [I. Pencil vs Figma — Working Mode](#i-pencil-vs-figma)
- [II. Agent Workflow Rules](#ii-agent-workflow-rules)
- [III. Structural & Layout Rules](#iii-structural--layout-rules)
- [IV. Code Syntax Rules (batch_design)](#iv-code-syntax-rules)
- [V. Bounded Creativity](#v-bounded-creativity)
- [VI. User Trigger Flags](#vi-user-trigger-flags)

---

## I. Pencil vs Figma — Working Mode

| Feature | Figma | Pencil + AI Agent |
|---------|-------|------------------|
| **Context** | Depends on layer/group names (often vague) | Integrated directly in node `context` property. AI reads business logic and function directly. |
| **Data structure** | Complex, proprietary metadata | Pure JSON/Schema. AI uses CRUD (I, U, R, M, D, C) via `batch_design` like a Database query. |
| **Reusability** | Main Component → Instance. Hard-to-query overrides. | Node with `reusable: true` flag. Use `ref` type with `descendants` mapping for precise overrides. |
| **Layout Engine** | Auto Layout (Frame) | Pure Flexbox (vertical/horizontal, gap, padding, justifyContent). Easily reasoned with frontend code logic. |

---

## II. Agent Workflow Rules

### Rule 1: "Discover Before Draw" (Mandatory)

NEVER create a new component without first surveying `Lib-Component`.

```
Action 1: get_editor_state(include_schema: false)
  → Get list of reusable components from editor state

Action 2: Extract IDs of needed components from the reusable list

Action 3: batch_get(nodeIds: [...], readDepth: 3)
  → Understand component structure (especially child IDs for override path)

Action 4: If required component NOT in library:
  → Ask user to add it, OR create new with reusable: true + clear context property
```

### Rule 2: "Slot Replacement" (Component Composition)

Instead of building discrete UI fragments, use the component **Slot** system:

```javascript
// Step 1: Insert parent component
parent = I(screenFrame, {type: "ref", ref: "parentComponentId"})

// Step 2: Replace a child slot with new content
R(parent+"/slotId", {type: "frame", layout: "vertical", ...children})
```

This preserves component structure while allowing deep customization.

### Rule 3: "25-Ops Safety" (Batch Size Limit)

- **Hard limit**: Maximum **25 operations** per `batch_design` call
- **For large screens** (Dashboard, Feed): split into multiple batches:
  - *Batch 1*: Container structure, layout columns, background, navbar frame
  - *Batch 2*: Populate sidebar and header content
  - *Batch 3*: Populate main content (cards, tables, lists)

---

## III. Structural & Layout Rules

### Rule 1: Flexbox Absolute

**Default**: Always initialize frames with `layout: "vertical"` or `layout: "horizontal"`. Set `layout: "none"` ONLY for overlapping graphic effects (e.g., Neobrutalism button shadow).

**X/Y coordinates**: **DISABLED** inside Flexbox. Never assign `x`, `y` inside a flex container. Use `padding`, `gap`, or intermediate wrapper frames for spacing.

**Sizing Engine**:
```javascript
width: "fill_container"   // Expand to fill parent (like Figma "Fill Container")
height: "fit_content"     // Shrink-wrap children (like Figma "Hug Contents")
height: "fit_content(200)" // Hug contents with 200px minimum fallback
```

**Critical Anti-Pattern — Circular Dependency**:
```javascript
// ❌ NEVER DO THIS — causes layout collapse to 0
parent: { height: "fit_content" }
  child: { height: "fill_container" }  // Circular! Parent height = child, child = parent
```

### Rule 2: Text & Wrapping

Default `textGrowth: "auto"` = NEVER wraps, expands infinitely in width direction. Does NOT respond to width/height.

**To enable text wrapping**:
```javascript
// ✅ REQUIRED for wrapping text
{
  type: "text",
  content: "Long text that needs wrapping",
  textGrowth: "fixed-width",   // MUST set this
  width: "fill_container",     // OR specific pixel value — MUST provide width
  textAlign: "left",           // Only works with fixed-width
  textAlignVertical: "top"     // Only works with fixed-width or fixed-width-height
}
```

### Rule 3: Design Token Variables (Mandatory)

**NEVER use static hex colors** outside token declarations.

```javascript
// ❌ WRONG
fill: "#FF4500"

// ✅ CORRECT — call get_variables() first, then use token names with $ prefix
fill: "$--primary"
fill: "$--background"
fill: "$--surface"
gap: "$--spacing-md"
```

Workflow:
1. Call `get_variables()` → see available design tokens in project
2. Use `$--token-name` syntax in all fill, stroke, gap, padding properties
3. Enables global theme switching without touching individual components

---

## IV. Code Syntax Rules

### Pattern 1: Binding & Reference (Variable Assignment)

After every `I()`, `C()`, or `R()` operation, save result to binding variable for subsequent operations in the same call:

```javascript
// ✅ CORRECT — Binding enables chaining
card = I(container, {type: "ref", ref: "FEkTl", width: "fill_container"})
U(card+"/xdCvx_n", {content: "New static title"})
U(card+"/subtitle", {content: "Subtitle text", textColor: "$--text-secondary"})
```

### Pattern 2: The "C" (Copy) Trap — CRITICAL

When using `C` (Copy) to duplicate a node group:
- `C` creates **completely new IDs** for ALL child nodes inside the copy
- **FORBIDDEN**: `U(copiedNode+"/oldChildId", ...)` — will FAIL because `oldChildId` no longer exists in the copy

**Correct approach — use `descendants` parameter**:
```javascript
// ✅ CORRECT — Pass updates via descendants at copy time
btn = C("wWUxj", container, {
  descendants: {
    "Njux9": {content: "SAVE CHANGES", fill: "$--secondary"}
  }
})

// ❌ WRONG — Update after copy with old child IDs
btn = C("wWUxj", container, {})
U(btn+"/Njux9", {content: "SAVE CHANGES"})  // FAILS — Njux9 is a new ID now
```

### Pattern 3: Placeholder Container

When beginning a screen draw:
1. Insert a root container and mark `placeholder: true`
2. This signals to user that content is being constructed
3. After final batch completes, call `U("rootFrameId", {placeholder: false})` to hand off

```javascript
// Start
screen = I(document, {type: "frame", name: "m1/login", placeholder: true, layout: "vertical", width: 375})

// ... all design operations ...

// Finish
U(screen, {placeholder: false})
```

---

## V. Bounded Creativity

### Zone Classification

| Zone Type | Applies To | AI Behavior |
|-----------|-----------|-------------|
| **Strict Zone** | Forms, Tables, Navigation, Data Cards | Assemble 100% from Lib-Component. No invented UI elements. No omission of spec fields. No layout/color overrides beyond text content. |
| **Fluid Zone** | Hero banners, Empty states, Onboarding, Marketing sections | Free to define Flexbox sizing, control whitespace, write persuasive copywriting based on Persona, use `G()` for AI images. |

### G() — AI Image Operation

Never draw complex Vector/Path manually (generates junk nodes). Use `G()` to fill frame containers with images:

```javascript
// Step 1: Create a frame container
heroImg = I(section, {type: "frame", width: "fill_container", height: 240})

// Step 2: Apply AI-generated image as fill
G(heroImg, "ai", "abstract glassmorphism shapes floating, soft pink neobrutalism aesthetic")

// Stock photo alternative
G(profilePic, "stock", "professional developer portrait workspace")
```

**Result**: Professional visual output without fragile vector nodes.

### Self-Critique via get_screenshot

After each `batch_design` call, call `get_screenshot` and check:

```
□ Typography (Visual Hierarchy) — is text hierarchy clear? headings vs body vs captions?
□ White space — is spacing breathable? Not cramped?
□ Orphan elements — any rogue/misplaced nodes not belonging to screen?
□ Color tokens — all fills using $--variables, not hardcoded hex?
□ Layout integrity — no elements spilling outside parent frame?
```

If any check fails: self-correct (adjust gap/padding, reorder nodes) silently before reporting to user.

---

## VI. User Trigger Flags

User may append these to their prompt to adjust agent behavior:

| Flag | Effect |
|------|--------|
| `--use-lib [nodeId]` | Force agent to use ONLY the component at this specific nodeId |
| `--wireframe` | Draw gray placeholder boxes at correct sizes only. No real content, no images. Focus on layout/flow validation. |
| `--strict-layout` | Call `snapshot_layout()` after EVERY `batch_design` call (not only on failure) |
| `--component-mode` | Agent is designing library components. Auto-set `reusable: true`. Prompt user for `context` description before saving. |
| `--creative` | Enable maximum Fluid Zone freedom. Auto-generate `G()` AI images for empty/hero/banner areas. |
