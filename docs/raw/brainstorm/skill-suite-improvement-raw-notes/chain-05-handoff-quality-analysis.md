# Chain 5: Handoff Quality — Chất lượng Contract giữa các Skill trong Pipeline

**Date:** 2026-05-12
**Task:** Chain 5 — Handoff Quality Analysis
**Workspace:** /home/steve/Work-space/deep_work_by_steve

---

## 1. Tổng quan

Phân tích chất lượng handoff contract giữa 3 skill trong pipeline: `skill-architect` → `skill-planner` → `skill-builder`.

**Pipeline Flow:**
```
skill-architect  ──→  skill-planner  ──→  skill-builder
    [design.md]            [todo.md]         [skill files]
```

**Kết luận sơ bộ:** Contract có thiết kế rõ ràng với YAML frontmatter + body markdown, nhưng CÓ 5 lỗ hổng critical ảnh hưởng đến handoff quality.

---

## 2. Handoff Contract Specifications

### 2.1 Contract A→P (Architect → Planner)

**Input:** `design.md`
**Output:** `todo.md`

#### Frontmatter Contract (Bắt buộc)

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `skill_schema_version` | string | `"3.0.0"` | Schema version lock |
| `artifact_type` | string | `"design"` | Artifact identification |
| `stage` | string | `"architect"` | Current stage |
| `status` | string | `"ready_for_planner"` | Handoff readiness |
| `zone_mapping` | object | 7 zones | File creation contract |
| `progressive_disclosure` | object | tier1+tier2+tier3 | Boot loading rules |
| `handoff.next_stage` | string | `"planner"` | Next stage directive |

#### Body Contract (10 Sections bắt buộc)

```
§1  Problem Statement      — Pain point, user, lý do
§2  Capability Map        — 3 Pillars analysis
§3  Zone Mapping          — MAIN CONTRACT (xem bảng dưới)
§4  Folder Structure      — Mermaid mindmap
§5  Execution Flow        — Sequence diagram
§6  Interaction Points    — Khi nào dừng hỏi user
§7  Progressive Disclosure — Tier 1/2/3 files
§8  Risks & Blind Spots   — ≥3 risks + mitigation
§9  Open Questions        — Điểm chưa rõ
§10 Metadata              — skill-name, date, author, status
```

#### §3 Zone Mapping Contract (CRITICAL)

Đây là contract chính cho Planner. Format bắt buộc:

```markdown
| Zone         | Files cần tạo              | Nội dung                                | Bắt buộc? |
|--------------|---------------------------|-----------------------------------------|-----------|
| Core (SKILL.md) | `SKILL.md`             | Persona, phases, guardrails             | ✅         |
| Knowledge    | `knowledge/xxx.md`        | Tri thức domain, tiêu chuẩn kỹ thuật   | ✅ / ❌     |
| Scripts      | `scripts/xxx.py`          | Automation tools                        | ✅ / ❌     |
| Templates    | `templates/xxx.template`  | Output format mẫu                       | ✅ / ❌     |
| Data         | `data/xxx.yaml`           | Config tĩnh, schema                     | ✅ / ❌     |
| Loop         | `loop/xxx.md`             | Checklist, verify rules, test cases     | ✅ / ❌     |
| Assets       | N/A                       | Không cần                               | ❌         |
```

**Quy tắc:** Tên file PHẢI cụ thể, không placeholder. Planner dùng cột "Files cần tạo" trực tiếp để tạo task.

#### Handoff Readiness Conditions (design.schema.yaml)

```yaml
handoff:
  next_stage: "planner"
  ready_condition:
    required:
      frontmatter_valid: true
      zone_mapping_complete: true
      required_sections_present: true
      no_blockers: true
```

---

### 2.2 Contract P→B (Planner → Builder)

**Input:** `todo.md` + `design.md`
**Output:** Skill files tại `{skills_root}/{skill-name}/`

#### Frontmatter Contract (Bắt buộc)

| Field | Type | Value | Purpose |
|-------|------|-------|---------|
| `skill_schema_version` | string | `"3.0.0"` | Schema version lock |
| `artifact_type` | string | `"todo"` | Artifact identification |
| `stage` | string | `"planner"` | Current stage |
| `status` | string | `"ready_for_builder"` | Handoff readiness |
| `trace_to_design` | string | `"design.md"` | Source reference |
| `phases` | array | PH0, PH1... | Task breakdown |
| `blockers` | array | empty or all resolved | Blocking issues |
| `prerequisites` | array | all status:"ready" | Resource readiness |
| `handoff.next_stage` | string | `"builder"` | Next stage directive |

#### Phase Task Contract

```yaml
phases:
  - id: "PH0"           # Resource preparation (pre-build)
    name: "PREPARE"
    tasks:
      - id: "T0.1"      # Pattern: T{phase}.{seq}
        title: "..."
        zone: "knowledge"  # Must match a zone from §3
        priority: "critical|high|medium|low"
        trace: "[TỪ DESIGN §3]"  # or [TỪ AUDIT TÀI NGUYÊN]
        depends_on: []    # References other task IDs
        status: "done|skipped"  # PH0 must be done/skipped
        file_target: "resources/xxx.md"  # Output target
```

#### Handoff Readiness Conditions (todo.schema.yaml)

```yaml
handoff:
  next_stage: "builder"
  ready_condition:
    required:
      blockers_empty: true
      phase0_done: true
      prerequisites_ready: true
      schema_valid: true
      design_zones_covered: true
```

---

## 3. Handoff Validator Analysis

### 3.1 handoff_validator.py Coverage

**Stage: design-to-planner (11 checks)**

| Check | What it validates | Quality Rating |
|-------|-------------------|----------------|
| `schema_version` | == "3.0.0" | ✅ Strong |
| `artifact_type` | == "design" | ✅ Strong |
| `stage` | == "architect" | ✅ Strong |
| `status_ready_for_planner` | == "ready_for_planner" | ✅ Strong |
| `all_7_zones_present` | zone_mapping has all 7 zones | ✅ Strong |
| `valid_paths_no_absolute_or_dotdot` | Paths are relative, no ".." | ✅ Strong |
| `tier1_base_field` | tier1 items have base field | ⚠️ Partial |
| `required_10_sections_present` | §1-§10 in body | ✅ Strong |
| `handoff_next_stage_planner` | handoff.next_stage == "planner" | ✅ Strong |
| `trace_tags_valid` | No invalid trace tags | ⚠️ Partial |

**Stage: planner-to-builder (10 checks)**

| Check | What it validates | Quality Rating |
|-------|-------------------|----------------|
| `schema_version` | == "3.0.0" | ✅ Strong |
| `artifact_type` | == "todo" | ✅ Strong |
| `stage` | == "planner" | ✅ Strong |
| `status_ready_for_builder` | == "ready_for_builder" | ✅ Strong |
| `unique_task_ids` | No duplicate IDs | ✅ Strong |
| `depends_on_targets_exist` | All depends_on reference valid IDs | ✅ Strong |
| `no_unresolved_blockers` | blockers all resolved | ✅ Strong |
| `phase0_all_done_or_skipped` | PH0 tasks finished | ✅ Strong |
| `prerequisites_all_ready` | All preqs status=="ready" | ✅ Strong |
| `handoff_next_stage_builder` | handoff.next_stage == "builder" | ✅ Strong |

**Stage: builder-complete (7 checks)**

| Check | What it validates | Quality Rating |
|-------|-------------------|----------------|
| `schema_version` | == "3.0.0" | ✅ Strong |
| `artifact_type` | == "build-log" | ✅ Strong |
| `no_stop_and_report` | No STOP_AND_REPORT in trace | ✅ Strong |
| `failed_actions_have_stop_and_report` | Failed actions logged | ✅ Strong |
| `no_validator_pass_contradiction` | No failed+pass paradox | ✅ Strong |
| `placeholder_ratio_below_0.10` | Placeholder < 10% | ⚠️ Partial |
| `validator_pass_true` | validator_pass == true | ✅ Strong |

### 3.2 Validator Strengths

1. **Machine-readable exit codes**: 0=PASS, 1=FAIL, 2=EMERGENCY
2. **Fix hints**: Every failed check gives actionable fix
3. **Frontmatter parsing**: Validates YAML structure separately from body
4. **Dependency chain validation**: Planner's depends_on validated
5. **Trace tag validation**: Catches malformed tags

### 3.3 Validator Gaps

| Gap | Impact | Severity |
|-----|--------|----------|
| Không validate §3 Zone Mapping có filename cụ thể (không placeholder) | Planner có thể nhận placeholder thay vì filename thật | **P1-Critical** |
| Không validate §7 PD tier1 vs tier2 distinction | Builder có thể load sai tier | P2-High |
| Không validate §8 có ≥3 risks | Risk mitigation có thể thiếu | P2-High |
| Không validate trace tag count/coverage | Task có thể không trace | P3-Medium |
| Không validate §9 Open Questions resolution | Questions có thể bị bỏ qua | P3-Medium |

---

## 4. Contract Quality Issues

### 4.1 CRITICAL: §3 Zone Mapping Filename Contract

**Issue:** Validator KHÔNG kiểm tra §3 Zone Mapping có filename cụ thể hay placeholder.

**Contract requirement:**
```
| Zone         | Files cần tạo              |
|--------------|---------------------------|
| Knowledge    | `knowledge/xxx.md`        |  ← Phải là tên file cụ thể
```

**Problem:** Architect có thể viết:
```
| Knowledge    | `knowledge/domain.md`     |  ← Cụ thể ✅
vs
| Knowledge    | `knowledge/*.md`         |  ← Placeholder ❌
```

**Impact:** Planner không biết chính xác file nào cần tạo → phải hỏi lại hoặc đoán.

**Fix Required:** Thêm check vào handoff_validator.py:
```python
# Kiểm tra §3 Zone Mapping không có wildcard/placeholder trong path
WILDCARD_PATTERN = re.compile(r'[*?[{]')
for zone_name, zone_data in zone_mapping.items():
    for f in zone_data.get("files", []):
        path = f.get("path", "")
        if WILDCARD_PATTERN.search(path):
            bad_paths.append(f"{zone_name}: '{path}' contains wildcard")
```

### 4.2 CRITICAL: Progressive Disclosure Tier Distinction

**Issue:** §7 PD phải phân biệt Tier 1 vs Tier 2, nhưng validator chỉ check `tier1_base_field` (có base hay không), không check Tier 1 vs Tier 2 distinction.

**Contract requirement:**
- **Tier 1**: Files AI PHẢI đọc mỗi khi skill được trigger (base: skill_dir)
- **Tier 2**: Files AI đọc dựa trên context cụ thể (base: skill_dir, load_when: ...)

**Problem:** Architect có thể viết Tier 1 và Tier 2 giống nhau → Builder không biết boot sequence đúng.

**Fix Required:** Thêm check:
```python
# Tier1 must have base="skill_dir" and NO load_when
# Tier2 must have base="skill_dir" AND load_when
# Tier3 must have load_when
```

### 4.3 HIGH: §8 Risk Count Enforcement

**Issue:** SKILL.md yêu cầu §8 có ≥3 risks kèm mitigation, nhưng validator KHÔNG check số lượng.

**Current check:** Không có
**Required check:** `min 3 risks in §8`

### 4.4 MEDIUM: Trace Tag Completeness

**Issue:** Validator check trace_tags_valid (format), nhưng KHÔNG check:
- Mỗi task có trace tag chưa
- Trace tag có đúng nguồn (§N phù hợp với content)

**Impact:** Task có thể gắn "[TỪ DESIGN §3]" nhưng content lại từ §5.

### 4.5 MEDIUM: §9 Open Questions Resolution

**Issue:** SKILL.md yêu cầu §9 phải được làm rõ hoặc flagged, nhưng validator KHÔNG check resolution status.

---

## 5. Pipeline Handoff Flow Analysis

### 5.1 Information Loss Points

```
Architect                          Planner                           Builder
   │                                  │                                 │
   ├─ §1 Problem Statement ──────────→│                                 │
   │                                  │                                 │
   ├─ §2 Capability Map ──────────────→├─ AUDIT ───────────────────────→│
   │                                  │                                 │
   ├─ §3 Zone Mapping ────────────────→├─ DECOMPOSE ───────────────────→│ §3 files
   │                                  │                                 │
   ├─ §7 Progressive Disclosure ──────→├─ AUDIT resources ─────────────→│ PD Plan
   │                                  │                                 │
   ├─ §8 Risks ──────────────────────→├─ CREATE mitigation tasks ─────→│ loop/*
   │                                  │                                 │
   └─ §9 Open Questions ─────────────→├─ FLAGGED as [CẦN LÀM RÕ] ────→│
```

**Information Loss Points:**

| Point | Loss Type | Severity |
|-------|-----------|----------|
| §2 → Planner AUDIT | Planner có thể interpret khác về Domain/Tech/Packaging | P2 |
| §3 Zone Mapping | Planner decomposes thành task - có thể miss nuance | P2 |
| §7 PD → Builder | Tier distinction có thể bị mất | **P1** |
| §8 Risks → loop/* | Builder phải convert risk→checklist - có thể sai | P2 |
| §9 → [CẦN LÀM RÕ] | Flag có thể bị ignore hoặc miss | P3 |

### 5.2 Contract Fidelity Breakdown

| Contract Element | Defined | Validated | Enforcement |
|-----------------|---------|-----------|-------------|
| §3 Zone Mapping (filename specific) | ✅ | ❌ | Weak |
| §7 Tier distinction | ✅ | ❌ | Weak |
| §8 ≥3 risks | ✅ | ❌ | None |
| §9 resolution | ✅ | ❌ | None |
| Trace tags (format) | ✅ | ✅ | Strong |
| Trace tags (coverage) | ✅ | ❌ | None |
| PH0 done/skipped | ✅ | ✅ | Strong |
| Prerequisites ready | ✅ | ✅ | Strong |
| Blockers empty | ✅ | ✅ | Strong |

---

## 6. Specific Contract Violation Scenarios

### Scenario 1: Architect → Planner

**Trigger:** Architect viết §3 Zone Mapping với placeholder path

```
| Knowledge | `knowledge/*.md` |  ← Wildcard
```

**Expected:** Planner tạo task "Tạo knowledge files theo pattern"

**Actual:** Planner không biết file nào → hỏi lại Architect → pipeline stall

**Validator fails to catch:** YES (no wildcard check)

### Scenario 2: Architect → Planner

**Trigger:** §7 PD Tier 1 và Tier 2 giống nhau

```
Tier 1:
  - path: "SKILL.md"
    base: "skill_dir"
Tier 2:
  - path: "SKILL.md"
    base: "skill_dir"
    load_when: "Phase 1"
```

**Expected:** Builder hiểu SKILL.md là boot (Tier 1) + theo phase (Tier 2)

**Actual:** Builder hiểu duplicate → confusion

**Validator fails to catch:** YES (no Tier distinction check)

### Scenario 3: Planner → Builder

**Trigger:** Planner tạo task với trace "[TỪ DESIGN §3]" nhưng content thực tế từ §5

**Expected:** Builder verify trace → content match

**Actual:** Builder trust trace → implement sai

**Validator fails to catch:** PARTIAL (format valid, content mismatch undetected)

---

## 7. Quality Assessment

### 7.1 Contract Design Quality

| Aspect | Rating | Reason |
|-------|--------|--------|
| Completeness | ✅ Strong | 10 sections + frontmatter + validator |
| Clarity | ⚠️ Partial | §3 filename requirement clear, §7 Tier distinction ambiguous |
| Atomicity | ✅ Strong | Mỗi section có purpose rõ ràng |
| Testability | ✅ Strong | handoff_validator.py có 28 checks total |
| Enforceability | ⚠️ Partial | Validator mạnh nhưng missing critical checks |

**Overall Contract Design: 7/10**

### 7.2 Contract Runtime Quality

| Aspect | Rating | Reason |
|-------|--------|--------|
| Execution adherence | ⚠️ Partial | LLM sometimes skip gates |
| Trace tag discipline | ❌ Weak | Format OK, coverage not enforced |
| Zone contract | ⚠️ Partial | File creation OK, naming convention not enforced |
| Gate checkpoints | ⚠️ Partial | Manual gates, not automatic |

**Overall Runtime Quality: 5/10**

### 7.3 Handoff Quality Score

```
Contract Design:      7/10
Validator Coverage:   6/10  (missing §3 filename, §7 Tier, §8 count)
Runtime Adherence:    5/10
Information Loss:     P2-P3 level
Overall Handoff:     6/10 — Cần cải thiện validator + runtime enforcement
```

---

## 8. Recommendations

### 8.1 Priority 1: Fix §3 Zone Mapping Validation

**Add to handoff_validator.py:**

```python
# After line ~224 in validate_design_to_planner
WILDCARD_PATTERN = re.compile(r'[*?[{]')
for zname, zdata in zone_mapping.items():
    for f_entry in zdata.get("files", []):
        p = f_entry.get("path", "")
        if WILDCARD_PATTERN.search(p):
            bad_paths.append(f"{zname}: '{p}' contains wildcard/placeholder")
checks.append(make_check(
    "zone_mapping_no_wildcards",
    len(bad_paths) == 0,
    error=f"Wildcard/placeholder paths found: {bad_paths}" if bad_paths else None,
    fix_hint="Use specific filenames in Zone Mapping, no wildcards",
))
```

### 8.2 Priority 2: Fix §7 Tier Distinction Validation

**Add to validate_design_to_planner:**

```python
# Tier1: must have base, must NOT have load_when
tier1_with_load_when = [item.get("path") for item in tier1 if "load_when" in item]
# Tier2: must have base AND load_when  
tier2_missing_load_when = [item.get("path") for item in tier2 if "load_when" not in item]
# Tier3: must have load_when
tier3_missing_load_when = [item.get("path") for item in tier3 if "load_when" not in item]
```

### 8.3 Priority 3: Add §8 Risk Count Check

```python
risks_section = extract_section(file_path, "8.")
risk_count = len(re.findall(r'- Risk \d+:', risks_section))
checks.append(make_check(
    "min_3_risks",
    risk_count >= 3,
    error=f"Only {risk_count} risks found, need ≥3" if risk_count < 3 else None,
    fix_hint="Add at least 3 risks with mitigation in §8",
))
```

### 8.4 Priority 4: Trace Tag Coverage Validation

**Add new check:**

```python
# Count tasks with trace tags vs total tasks
tasks_with_trace = len(re.findall(r'\[TỪ DESIGN §[0-9]+\]|\[TỪ AUDIT|\[GỢI Ý|\[CẦN', todo_content))
total_task_refs = len(re.findall(r'- \[ \]|\- \[x\]', todo_content))
coverage = tasks_with_trace / max(total_task_refs, 1)
checks.append(make_check(
    "trace_tag_coverage",
    coverage >= 0.95,
    error=f"Trace tag coverage: {coverage:.0%}, need ≥95%" if coverage < 0.95 else None,
))
```

---

## 9. Summary

### What I Did

1. Read and analyzed 3 SKILL.md files (skill-architect, skill-planner, skill-builder)
2. Read _shared/knowledge/framework.md for pipeline context
3. Read handoff_validator.py (28 validation checks across 3 stages)
4. Read design.schema.yaml and todo.schema.yaml for contract specs
5. Read good fixture examples for contract format
6. Read chain-04 analysis for anti-hallucination context

### What I Found

**Contract Design:** Rõ ràng với YAML frontmatter + 10-section body. Schema well-defined.

**Validator Coverage:** 28 checks total, strong on:
- Schema version, artifact type, stage
- Task ID uniqueness, dependency validity
- Blockers resolution, PH0 completion
- Prerequisites readiness

**Validator Gaps (5 critical):**
1. §3 Zone Mapping wildcard/placeholder NOT detected
2. §7 Tier distinction (Tier1 vs Tier2) NOT validated
3. §8 Risk count (≥3) NOT enforced
4. Trace tag coverage NOT validated (only format)
5. §9 Open Questions resolution NOT checked

**Runtime Quality:** 5/10 — LLM instruction following degrades mid-execution (from chain-04).

**Overall Handoff Quality:** 6/10 — Contract design good but validator missing critical checks.

### Files Created

- `/home/steve/Work-space/deep_work_by_steve/docs/chain-05-handoff-quality-analysis.md` — This document

### Recommendations Summary

| Priority | Fix | Impact |
|----------|-----|--------|
| P1 | Add §3 wildcard detection to validator | Prevents placeholder filename |
| P1 | Add §7 Tier distinction validation | Prevents PD loading errors |
| P2 | Add §8 risk count check | Ensures risk coverage |
| P2 | Add trace tag coverage validation | Ensures traceability |
| P3 | Add §9 resolution check | Ensures questions addressed |

---

## 10. Related Files

- `/home/steve/Work-space/deep_work_by_steve/.hermes/skills/_shared/validators/handoff_validator.py` — Validator implementation
- `/home/steve/Work-space/deep_work_by_steve/.hermes/skills/_shared/schemas/design.schema.yaml` — design.md schema
- `/home/steve/Work-space/deep_work_by_steve/.hermes/skills/_shared/schemas/todo.schema.yaml` — todo.md schema
- `/home/steve/Work-space/deep_work_by_steve/.hermes/skills/_shared/knowledge/framework.md` — Pipeline framework
- `/home/steve/Work-space/deep_work_by_steve/docs/chain-04-guardrails-anti-hallucination-analysis.md` — Related chain-04 analysis
