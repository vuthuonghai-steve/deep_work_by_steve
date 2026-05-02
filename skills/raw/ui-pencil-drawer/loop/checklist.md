# Autonomous Self-Verify Checklist

> **Usage**: Load at end of each Phase for self-verification before auto-proceeding.
> AI runs this checklist internally. Pass/fail thresholds determine proceed / self-fix / escalate.
> Source: design.md §3 (Loop Zone) + §8 (Risks & Blind Spots)

---

## §P0 — Phase 0: Context Boot Checklist

Run after completing all Phase 0 actions. Required before Phase 1.

```
□ P0.1  get_editor_state() returned a valid .pen file (not null, not error)?
□ P0.2  project_context.module_scope is populated (M1-M6 map confirmed)?
□ P0.3  batch_get Lib-Component returned ≥ 1 node with reusable: true?
□ P0.4  component_map has been built ({name → nodeId} entries present)?
□ P0.5  Design aesthetic confirmed: Neobrutalism + Pink primary?
```

**Threshold**:
- ALL 5 pass → ✅ auto-proceed to Phase 1
- P0.1 fail → ⚠️ ESCALATE: "STi.pen not found. Please open the file or provide path."
- P0.3 or P0.4 fail → ⚠️ ESCALATE: "Lib-Component frame not found or empty. Please check STi.pen structure."
- P0.2 or P0.5 fail → Self-fix: re-read CLAUDE.md and retry. Max 1 retry.

---

## §P1 — Phase 1: Spec Analyzer Checklist

Run after parsing spec file + activity diagrams. Required before Phase 2.

```
□ P1.1  screens[] is non-empty (at least 1 screen extracted)?
□ P1.2  Each screen in screens[] has: name, layout direction, width?
□ P1.3  Each screen has at least 1 component mapping entry?
□ P1.4  Every component mapping entry has a corresponding name in component_map (or marked MISSING_)?
□ P1.5  No field names were invented — all entries traceable to spec or activity diagram sections?
□ P1.6  Spec file was readable and existed at provided path?
□ P1.7  Activity diagrams for the module were found and read (or absence was logged)?
□ P1.8  states[] for each screen contains more than just "default" (error/loading/success extracted from diagrams)?
```

**Threshold**:
- ALL pass → ✅ auto-proceed to Phase 2
- P1.6 fail → ⚠️ ESCALATE: "Spec file not found at {path}. Please verify the path."
- P1.1 fail → ⚠️ ESCALATE: "Could not extract any screens from spec. Format may be unrecognized."
- P1.2 or P1.3 fail → Self-fix: re-parse spec with wider pattern matching. Max 1 retry.
- P1.4 fail (MISSING_ entries exist) → Log missing components. Continue. Note in Phase 3 as `zone: blocked`.
- P1.5 fail → Self-correct: remove invented entries, re-extract from spec or diagrams only.
- P1.7 fail (diagrams not found) → Log "activity diagrams not found for M{N}". Continue with spec states only. Do NOT escalate.
- P1.8 fail (only default state) → Self-fix: re-read activity diagrams with wider pattern scan. If still only default → log warning, continue.

---

## §P2 — Phase 2: Wireframe Blueprint Checklist

Run after generating all screen blueprints. Required before Phase 3.

```
□ P2.1  Blueprint file exists for every screen in screens[]?
□ P2.2  Every blueprint has a valid # Screen: header (module, spec, layout, width, state)?
□ P2.3  Every `- comp:` entry has spec-cite (no missing citations)?
□ P2.4  No `ref:` value is empty, "?", "undefined", or blank?
□ P2.5  No component was added that has no equivalent in spec (hallucination check)?
□ P2.6  MISSING_ placeholder entries are correctly flagged (not silently dropped)?
□ P2.7  All ## Section: blocks have layout direction specified?
```

**Threshold**:
- ALL pass → ✅ auto-proceed to Phase 3
- P2.3 fail → Self-correct: add spec-cite to uncited entries using spec content. Re-run checklist.
- P2.4 fail → Self-correct: trace back to component_map, replace empty refs with MISSING_ pattern.
- P2.5 fail → Self-correct: remove hallucinated components. No tolerance for invented elements.
- P2.1 fail (missing blueprint for a screen) → Self-fix: generate missing blueprint. Max 1 retry.
- P2.2 or P2.7 fail → Self-fix: add missing header fields from spec context.
- P2.6 fail → Self-correct: ensure MISSING_ entries are explicit in blueprint for Phase 3 skipping.

---

## §P3 — Phase 3: Per-Screen Draw Checklist

Run after each `batch_design` + `get_screenshot` for 1 screen. Score 0–7.

```
□ P3.1  Screenshot renders (not blank/white/error)?              [critical]
□ P3.2  No overlap with Lib-Component frame (snapshot_layout confirms)?  [critical]
□ P3.3  All component node IDs used were from component_map (not hardcoded)?  [critical]
□ P3.4  Number of drawn components matches blueprint slot count?
□ P3.5  Typography hierarchy is clear (headings vs body vs captions visible)?
□ P3.6  White space is adequate (not cramped — minimum gap_default: 24px)?
□ P3.7  No orphan/rogue elements outside the screen frame?
```

**Threshold**:
- 7/7 pass → ✅ Screen complete. Auto-proceed to next screen.
- 5–6/7 pass (non-critical failures only) → ✅ Proceed. Log minor issue in summary.
- Any critical (P3.1, P3.2, P3.3) fail → Self-fix:
  - P3.1 fail: check operations for errors, retry batch_design. Max 2 retries.
  - P3.2 fail: call find_empty_space_on_canvas with larger padding (padding * 2). Redraw.
  - P3.3 fail: revert batch, re-check component_map, redraw with correct IDs.
- < 5/7 pass AND non-fixable → Count as **failure**. Track consecutive failures.

**Consecutive Failure Rule (G-Fail-Fast)**:
```
consecutive_failures = 0

Per screen:
  if screen passes threshold:
    consecutive_failures = 0
  elif self-fix succeeds:
    consecutive_failures = 0
  else:
    consecutive_failures += 1
    if consecutive_failures >= 2:
      ⚠️ ESCALATE — "2 consecutive screen failures. Reporting blocker."
```

---

## §FINAL — Post-Build Summary Checklist

Run after all screens are drawn.

```
□ FINAL.1  All screens in screens[] attempted (drawn OR skipped with reason)?
□ FINAL.2  Wireframe blueprint files saved for all screens?
□ FINAL.3  placeholder: false set on all completed screen frames?
□ FINAL.4  Summary report output with: screen count, skip count, warning list?
□ FINAL.5  No unresolved MISSING_ refs silently ignored (all documented in summary)?
```

**Threshold**: ALL pass → Output summary to user. Session complete.

---

## Risk Coverage Map

Checklist items map to design.md §8 Risks:

| Risk (design.md §8) | Checklist Item | Enforcement |
|---------------------|---------------|-------------|
| R1 — AI bịa component IDs (P0) | P0.3, P0.4, P3.3 | batch_get first; no hardcoding |
| R2 — Vẽ đè canvas (P0) | P3.2 | find_empty_space + snapshot_layout |
| R3 — Thêm elements không có trong spec (P1) | P1.5, P2.3, P2.5 | spec-cite required; hallucination check |
| R7 — Bỏ sót error/loading states (chỉ vẽ default) | P1.7, P1.8 | Đọc activity diagrams M{N}; states[] phải > default |
| R4 — batch_design quá nhiều ops (P1) | (data/layout-rules.yaml limits.batch_ops_max) | 25-op hard cap per call |
| R5 — G-Fail-Fast: accumulate errors (P1) | P3 consecutive failure rule | Escalate after 2 consecutive |
| R6 — Wireframe phức tạp, AI lost (P2) | P2.1, max_components_per_screen | 1 file = 1 screen; max 20 components |
