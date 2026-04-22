# Project Context — Steve Void

> **Usage**: Load in Phase 0 Boot Sequence (mandatory, first file after SKILL.md). Gives AI the project orientation needed before reading any spec or touching any canvas. Read CLAUDE.md and check.list.md for live state — this file gives structural context only.
> **Source**: Synthesized from `CLAUDE.md` + project lifecycle rules

---

## 1. Project Identity

- **Name**: Steve Void — knowledge-sharing social network for Vietnamese tech community
- **Target users**: developers, CS students, tech learners
- **Current phase**: Life-2 (Design & Specification) — completing M4 Engagement + M6 Notifications specs
- **Next phase**: Life-3 (Implementation with Next.js 15 + Payload CMS 3.x)

**Key files to read for live status**:
```
CLAUDE.md              → Full project rules, module map, anti-patterns
Docs/check.list.md     → What phase, what's in progress, what's done
```

---

## 2. Module Map (M1–M6)

| Module | Name | Spec File | Core Screens |
|--------|------|-----------|-------------|
| M1 | Auth & Profile | `Docs/life-2/ui/specs/m1-auth-ui-spec.md` | Login, Register, Profile, Edit Profile, Forgot Password |
| M2 | Content Engine | `Docs/life-2/ui/specs/m2-content-ui-spec.md` | Create Post, Post Detail, Edit Post |
| M3 | Discovery Feed | `Docs/life-2/ui/specs/m3-discovery-ui-spec.md` | News Feed, Trending, Search Results |
| M4 | Engagement | `Docs/life-2/ui/specs/m4-engagement-ui-spec.md` | Likes, Comments thread, Connections |
| M5 | Bookmarking | `Docs/life-2/ui/specs/m5-bookmarking-ui-spec.md` | Collections list, Collection detail, Save to collection |
| M6 | Notifications & Moderation | `Docs/life-2/ui/specs/m6-notifications-ui-spec.md` | Notification bell + tray, Report modal |

**Spec lookup rule**: Given a module code (M1–M6), derive spec path from table above. If spec file not found at that path → escalate with clear error.

---

## 3. Design Aesthetic — Neobrutalism + Pink

**Style**: Neobrutalism with Pink primary color.

| Element | Rule | Example value |
|---------|------|---------------|
| Primary color | Pink | `$--primary` (resolves to strong pink) |
| Borders | Bold black | `border: 2, strokeColor: "$--border-strong"` |
| Shadows | Offset box shadow | `shadow-offset-x: 4, shadow-offset-y: 4, shadow-color: "black"` |
| Background | High contrast | `fill: "$--background"` (white/near-white) |
| Typography | Direct, functional | Bold headings, readable body text |
| Corners | Minimal rounding | `cornerRadius: [4, 4, 4, 4]` or `[0, 0, 0, 0]` |

**In Fluid Zones**: Agent may push whitespace, choose bold typography hierarchy, and use `G()` with "neobrutalism aesthetic, pink accents" prompts.

---

## 4. Frame Naming Convention

All screen frames in STi.pen must follow:

```
{module-code}/{screen-name}

Examples:
  m1/login
  m1/register
  m1/profile
  m2/create-post
  m3/feed
  m4/comment-thread
  m5/collections
  m6/notifications
```

**Lib-Component frame**: Find it via `batch_get({patterns: [{name: "Lib-Component"}]})` — do not assume its frame ID.

---

## 5. File Paths Quick Reference

| Asset | Path |
|-------|------|
| UI spec files | `Docs/life-2/ui/specs/m{N}-*-ui-spec.md` |
| Wireframe blueprints (output) | `Docs/life-2/ui/wireframes/{module}-{screen}-wireframe.md` |
| DB schema | `Docs/life-2/database/schema-design.md` |
| API spec | `Docs/life-2/api/api-spec.md` |
| Main spec (code source) | `Docs/life-2/specs/m{N}-*-spec.md` |
| Activity diagrams | `Docs/life-2/diagrams/activity-diagrams/m{N}-a*.md` |
| Flow diagrams | `Docs/life-2/diagrams/flow/flow-*.md` |
| Sequence diagrams | `Docs/life-2/diagrams/sequence-diagrams/detailed-m{N}-*.md` |
| STi.pen file | Ask user or use `get_editor_state()` to detect |

---

## 7. Diagram Paths — Module-to-Activity Mapping

**Mục đích**: Phase 1 đọc activity diagrams để extract đầy đủ states (error, loading, success, empty) cho mỗi màn hình. Spec file thường chỉ mô tả `default` state — activity diagrams chứa toàn bộ error branches và UI state transitions.

### Activity Diagrams (Primary source for states extraction)

| Module | Files | Extract gì |
|--------|-------|-----------|
| M1 | `m1-a1-registration.md`, `m1-a2-login.md`, `m1-a3-verification.md`, `m1-a4-recovery.md`, `m1-a5-onboarding.md` | Error validation, duplicate email, token expired, success redirect |
| M2 | `m2-a1-editor-pipeline.md`, `m2-a2-media-handler.md`, `m2-a3-post-integrity.md`, `m2-a4-visibility.md` | Draft state, upload error, content violation, publish success |
| M3 | `m3-a1-feed-assembler.md`, `m3-a2-search-engine.md`, `m3-a3-discovery-recommendation.md` | Empty feed, search no results, loading skeleton |
| M4 | `m4-a1-friendship-handshake.md`, `m4-a2-engagement-logic.md`, `m4-a3-connection-privacy.md` | Pending state, blocked state, reaction feedback |
| M5 | `m5-a1-bookmark-persistence.md`, `m5-a2-collection-orchestrator.md` | Empty collection, save success, conflict error |
| M6 | `m6-a1-sse-dispatcher.md`, `m6-a2-report-pipeline.md`, `m6-a3-enforcement-action.md` | Real-time badge, report pending, enforcement result |

### Pattern nhận dạng states từ activity diagram

Khi đọc activity diagram, tìm các node types sau:

| Node Pattern | State Type | Ví dụ |
|---|---|---|
| "Hiển thị lỗi...", "Trả về lỗi..." | `error` | `B3: Hiển thị lỗi Validation` |
| "Đang xử lý...", spinner, `activate` block | `loading` | `C1: Nhận yêu cầu` (processing) |
| "Điều hướng sang...", "Chuyển hướng", redirect | `success` | `B12: Điều hướng sang trang Chờ xác nhận` |
| "Danh sách trống", "Không có kết quả" | `empty` | `S2: Không có kết quả tìm kiếm` |

### State citation format (dùng trong wireframe blueprint)

```
state: error    | source: activity m1-a1 §B3
state: loading  | source: activity m1-a1 §C1
state: success  | source: spec §2.3
state: default  | source: spec §2.1
```

---

## 6. Autonomous Execution Contract

This skill operates in **AGI-oriented autonomous mode**:

- Human provides: `spec_path` + `pen_file_path` (or relies on open file in editor)
- AI handles: context boot → spec parse → blueprint → draw → summary
- AI does NOT ask for phase confirmations
- AI escalates ONLY for hard blockers (pen file not found, component truly missing)
- AI self-corrects: layout issues, overlaps, component fuzzy-match — all handled silently

**Non-escalation examples** (handle internally):
- Minor spec ambiguity → infer from project_context, log inference in blueprint notes
- Component name fuzzy match → use best match from component_map, log in summary
- Screenshot quality marginal → retry batch_design (max 2x) silently
- Overlap detected → recalculate position with `find_empty_space_on_canvas`, larger padding
