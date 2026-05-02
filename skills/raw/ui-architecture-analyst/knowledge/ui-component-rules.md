# UI Component Rules: Naming, Catalogue & Policies

> Source: design.md §3 (Knowledge Zone), §9 Q1 (Cross-module policy), §9 Q2 (Error/Empty States policy)
> Resources: design-research.md (shadcn/ui component context)
> Fidelity: 4 sections — Screen ID naming, Element ID naming, Component catalogue, Cross-module policy

---

## Section 1 — Screen ID Convention

### Format
```
SC-M[X]-[NN]
```

| Segment | Description | Example |
|---------|-------------|---------|
| `SC` | Screen prefix (fixed) | SC |
| `M[X]` | Module number (1–6) | M1, M2, M6 |
| `[NN]` | 2-digit sequential number (01, 02, ...) | 01, 02, 10 |

### Examples
```
SC-M1-01   → Register Screen (Module 1)
SC-M1-02   → Login Screen (Module 1)
SC-M2-01   → Create Post Screen (Module 2)
SC-M3-01   → News Feed Screen (Module 3)
SC-M6-03   → Notification List Screen (Module 6)
```

### Rules
- Numbers are sequential within a module, starting from `01`
- Never skip numbers (no `SC-M1-01`, then `SC-M1-03`)
- If a screen is removed, do not reuse its number
- Screens are **UI states** (what a user sees at a given moment), not routes alone
  - Login page = `SC-M1-02`
  - Login page in "loading" state = **NOT a separate SC** (use §2C States sub-section)
  - Login page in "OTP step" = **separate SC** `SC-M1-03` if layout fundamentally changes

---

## Section 2 — Element ID Naming Convention

### Prefixes by Component Type

| Component Category | Prefix | Example |
|-------------------|--------|---------|
| Text input (text, email, password, number) | `input-` | `input-email`, `input-password` |
| Textarea / Rich text | `textarea-` | `textarea-bio`, `editor-content` |
| Rich text editor | `editor-` | `editor-content` |
| Select dropdown (single) | `select-` | `select-role`, `select-category` |
| Multi-select | `multi-select-` | `multi-select-tags` |
| Checkbox | `checkbox-` | `checkbox-agree-terms` |
| Radio group | `radio-` | `radio-visibility` |
| Date picker | `date-` | `date-birthday` |
| File / image upload | `upload-` | `upload-avatar`, `upload-cover` |
| Relationship picker | `relation-` | `relation-author` |
| Multi-relation picker | `relation-multi-` | `relation-multi-tags` |
| Button (action) | `btn-` | `btn-submit`, `btn-cancel`, `btn-delete` |
| Link (navigation) | `link-` | `link-forgot-password`, `link-register` |
| Badge / status indicator | `badge-` | `badge-status`, `badge-role` |
| Avatar | `avatar-` | `avatar-user` |
| Card (container) | `card-` | `card-post`, `card-profile` |
| Label | `label-` | `label-email`, `label-bio` |
| Section container | `section-` | `section-personal-info` |
| List item | `item-` | `item-notification`, `item-post` |
| Search input | `search-` | `search-query` |
| Toggle / Switch | `toggle-` | `toggle-dark-mode` |
| Dialog / Modal | `dialog-` | `dialog-confirm-delete` |
| Toast / Alert | `toast-` | `toast-success`, `toast-error` |

### Element ID Format
```
[prefix][semantic-name]
```

**Rules**:
- Use **kebab-case** (lowercase, hyphens)
- Name must be semantic (describes content, not style): `input-email` not `input-blue-field`
- No spaces, no underscores
- If multiple instances: append context: `btn-submit-login`, `btn-submit-register`

### data-testid Mapping
Element IDs directly become `data-testid` attributes in implementation:
```html
<input id="input-email" data-testid="input-email" ... />
<button id="btn-submit" data-testid="btn-submit" ... />
```

---

## Section 3 — UI Component Catalogue (Tailwind v4 + Radix UI)

> **CRITICAL**: This project uses **Tailwind CSS v4 + Radix UI ONLY**.
> shadcn/ui, antd, @mui, @chakra-ui are **FORBIDDEN**.
> When specifying components, reference Radix UI primitives.

### Core Radix UI Primitives Available

| Component Name | Radix Package | Usage |
|---------------|--------------|-------|
| **Button** | `@radix-ui/react-button` (or native `<button>`) | Primary actions, form submit |
| **Checkbox** | `@radix-ui/react-checkbox` | Boolean fields |
| **Dialog** | `@radix-ui/react-dialog` | Modals, confirmations |
| **DropdownMenu** | `@radix-ui/react-dropdown-menu` | Action menus, kebab menus |
| **Form** | `@radix-ui/react-form` | Form validation |
| **Label** | `@radix-ui/react-label` | Field labels |
| **Popover** | `@radix-ui/react-popover` | Tooltips, small overlays |
| **RadioGroup** | `@radix-ui/react-radio-group` | Single-choice options |
| **ScrollArea** | `@radix-ui/react-scroll-area` | Scrollable containers |
| **Select** | `@radix-ui/react-select` | Single dropdown select |
| **Separator** | `@radix-ui/react-separator` | Visual dividers |
| **Slider** | `@radix-ui/react-slider` | Range inputs |
| **Switch** | `@radix-ui/react-switch` | Toggle on/off |
| **Tabs** | `@radix-ui/react-tabs` | Tabbed navigation within a screen |
| **Toast** | `@radix-ui/react-toast` | Notification toasts |
| **Tooltip** | `@radix-ui/react-tooltip` | Hover hints |
| **Avatar** | `@radix-ui/react-avatar` | User avatars with fallback |
| **Progress** | `@radix-ui/react-progress` | Upload progress, step indicators |
| **Accordion** | `@radix-ui/react-accordion` | Collapsible sections |
| **AlertDialog** | `@radix-ui/react-alert-dialog` | Destructive action confirmations |
| **Collapsible** | `@radix-ui/react-collapsible` | Expandable content |
| **HoverCard** | `@radix-ui/react-hover-card` | Rich preview on hover |
| **NavigationMenu** | `@radix-ui/react-navigation-menu` | Top-level nav links |
| **ContextMenu** | `@radix-ui/react-context-menu` | Right-click menus |

### Custom Components (Project-specific, non-Radix)

| Component Name | Category | Usage |
|---------------|----------|-------|
| `<Input>` | Atom | Styled text/email/password/number input (Tailwind v4) |
| `<Textarea>` | Atom | Styled multi-line text input |
| `<ImageUpload>` | Atom | Drag-and-drop image upload with preview |
| `<FileUpload>` | Atom | Generic file upload |
| `<RichTextEditor>` | Molecule | Lexical/Slate-based rich text editor |
| `<RelationPicker>` | Molecule | Async search-select for related entities |
| `<RelationMultiPicker>` | Molecule | Multi-select for relationships |
| `<MultiSelect>` | Molecule | Tag-based multi option select |
| `<DatePicker>` | Atom | Calendar date picker |
| `<BlockEditor>` | Organism | Content block editor (Payload blocks field) |
| `<ArrayField>` | Molecule | Repeater for array fields |
| `<PostCard>` | Molecule | Card displaying a post summary |
| `<UserAvatar>` | Atom | Avatar + display name |
| `<NotificationItem>` | Molecule | Single notification row |
| `<CommentThread>` | Organism | Nested comment display |
| `<TagBadge>` | Atom | Small badge for category/tag |

### Atomic Design Hierarchy

```
Atoms       → ui/          (Input, Button, Checkbox, Label, Badge, Avatar)
Molecules   → shared/      (PostCard, FormField, RelationPicker, CommentThread)
Organisms   → layout/      (Header, Sidebar, FeedList, ProfileSection)
Pages       → screens/     (Full screen compositions)
```

### Design Aesthetic — Neobrutalism

All components follow the project's Neobrutalism style:
- **Borders**: `border-2 border-black`
- **Shadows**: `shadow-[4px_4px_0px_black]` (offset box shadow)
- **Primary color**: Pink / Rose (`#FF69B4` range)
- **Background**: High contrast (white or soft off-white)
- **Typography**: Bold, direct, functional (no decorative fonts)

---

## Section 4 — Cross-Module Component Policy

> Source: design.md §9 Q1 — Confirmed policy

### Rule
**Cross-module shared components** (appearing across multiple screens) are:
- ✅ Documented **once** in `Docs/life-2/ui/specs/index.md`
- ✅ Referenced in module specs by name only (do not repeat specs)
- ❌ NOT re-specified in each individual module spec

### Cross-Module Component List (Core)

| Component | Appears In | Document In |
|-----------|-----------|-------------|
| `<Header>` / `<Navbar>` | All screens | `index.md` |
| `<Sidebar>` | Dashboard/feed screens | `index.md` |
| `<BottomNav>` (mobile) | All mobile screens | `index.md` |
| `<NotificationBanner>` | All screens (SSE) | `index.md` |
| `<Toast>` system | All screens | `index.md` |
| `<SearchBar>` | Header / M3 screens | `index.md` |
| `<UserAvatar>` | Posts, comments, profiles | `index.md` |

### How to Reference in Module Spec
In a module spec, do not detail these components. Instead, write:

```markdown
> Header, Sidebar, Toast — see `Docs/life-2/ui/specs/index.md` for spec.
> This screen uses standard layout: [Header] + [Sidebar] + [Main Content Area]
```

### Exception
If a cross-module component has **module-specific behavior** (e.g., a filter SearchBar only in M3), document that specific behavior as a **sub-note** in the module spec's screen detail, but still reference the base spec from `index.md`.
