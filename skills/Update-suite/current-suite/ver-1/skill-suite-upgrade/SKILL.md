---
name: skill-suite-upgrade
description: "Kỹ sư nâng cấp bộ skill (Architect/Planner/Builder) với CASE System và các validator."
disable-model-invocation: true
user-invocable: true
---

# === BOOT CONFIGURATION (L0 — Anchor Rules) ===

<instructions>
must:
  - run the core_case.py status check at startup before taking any actions
  - analyze skill issues using Heavy Thinking K=4 chains
  - design upgrades according to the CASE System (PREVENT/DETECT/RECOVER)
  - run rollback checks using the rollback_engine.py if verification fails
must_not:
  - skip boot sequence or ignore check status codes
  - modify actual production skill files without user confirmation
</instructions>

<context>
### Boot Sequence
1. Read `SKILL.md` (this file) — done
2. Read `../_shared/knowledge/framework.md` — Stage boundaries and conventions
3. Read `../_shared/knowledge/case-system.md` — CASE System specifications
4. Run `python3 ../_shared/validators/check_status.py .skill-context/{skill-name}/design.md` to verify current status.
   - If checkpoint stale (> 7 days), alert user.
5. Determine Position:
   - phase = 0 → Fresh start (Phase 1)
   - phase > 0 → Ask user: resume or restart?
6. Proceed to Phase 1: Analyze

### Pipeline Specification
- Stage Order: 4 (Meta-Stage)
- Input Contract: `.skill-context/{skill-name}` (optional)
- Output Contract: Upgraded Skill files under `skills/rebuild/{skill-name}`
- Dependencies: None

### Routing Map (Progressive Disclosure)
- **Tier 1 (Boot)**:
  - `../_shared/knowledge/framework.md` (Stage boundaries & conventions)
  - `../_shared/knowledge/case-system.md` (CASE System specifications)
  - `../_shared/validators/check_status.py` (Boot status checker)
- **Tier 2 (Conditional)**:
  - `knowledge/state-management.md` (Load when: Resuming checkpoint)
  - `../_shared/validators/handoff_validator.py` (Load when: Gate checking)
  - `../_shared/validators/rollback_engine.py` (Load when: Rollback needed)
- **Tier 3 (On-Demand)**:
  - `loop/resume_checklist.md` (When resuming checkpoint)
</context>

## 📋 Workflow Phases

### Phase 1: Analyze — Heavy Thinking Problem Identification

**Mục tiêu**: Áp dụng Heavy Thinking để phân tích vấn đề của bộ skill hiện tại.

**Thực hiện**:
1. Đọc 3 skill files hiện tại (skill-architect, skill-planner, skill-builder)
2. Áp dụng Heavy Thinking K=4 chains:
   - Chain 1: Context & State Management
   - Chain 2: Handoff & Contract Integrity
   - Chain 3: Progressive Disclosure Enforcement
   - Chain 4: Error Detection & Recovery
3. Tổng hợp thành danh sách vấn đề cốt lõi
4. Đề xuất giải pháp theo CASE System

**Output**: §1 Problem Statement với:
- Danh sách vấn đề được identify
- Giải pháp đề xuất (PREVENT/DETECT/RECOVER)
- Priority ranking

> ⏸️ **Gate 1**: Trình bày problems + solutions. Chờ user confirm.

---

### Phase 2: Design — CASE System Architecture

**Mục tiêu**: Thiết kế kiến trúc nâng cấp dựa trên CASE System.

**Thực hiện**:
1. **3 Pillars Analysis**:
   - Pillar 1 – Knowledge: Case system framework, state management
   - Pillar 2 – Process: State-aware boot, 3-gate system
   - Pillar 3 – Guardrails: Explicit triggers, validators

2. **Zone Mapping**: Xác định files cần tạo/sửa

3. **Design Output** (§2, §3, §8):
   - §2: Capability Map
   - §3: Zone Mapping
   - §8: Risks & Blind Spots

> ⏸️ **Gate 2**: Trình bày architecture design. Chờ user confirm.

---

### Phase 3: Implement — Build & Verify

**Mục tiêu**: Implement nâng cấp theo design.

**Thực hiện**:
1. Tạo scripts (check_status.py, validate_gate.py, validate_zone_mapping.py)
2. Tạo knowledge files (case-system.md, state-management.md)
3. Tạo loop files (boot_checklist.md, gate_checklist.md, resume_checklist.md)
4. Cập nhật SKILL.md cho từng skill

> ⏸️ **Gate 3**: Validate tất cả gates. Chờ user confirm.

---

## 🔧 CASE System Components

### 1. PREVENT — Chặn lỗi trước

```
A. State-aware Boot:
   - check_status.py đọc design.md status TRƯỚC KHI làm gì
   - Xác định phase hiện tại (fresh/resume)
   
B. Explicit PD triggers:
   - Tier 2 files có CONCRETE triggers
   - Không "load when needed" — cụ thể khi nào
   
C. Contract validation:
   - validate_zone_mapping.py check §3 schema
   - validate_gate.py check gate checklists
```

### 2. DETECT — Phát hiện sớm

```
A. Gate Validators:
   - Gate 1: §1 Problem Statement
   - Gate 2: §2 + §3 + §8
   - Gate 3: §4-§9 + diagrams
   
B. Reverse Trace:
   - §3 Zone Mapping → trace về §1 Pain Point
   - Phát hiện drift sớm
   
C. Exit Codes:
   - 0 = PASS
   - 1 = FAIL (fix and retry)
   - 2 = EMERGENCY (stop)
```

### 3. RECOVER — Khôi phục

```
A. Rollback Procedures:
   - Mỗi phase có rollback steps
   - Archive before rollback
   
B. Checkpoint Resume:
   - Status block có phase, gates_passed, timestamp
   - Resume từ checkpoint
   
C. Staleness Check:
   - < 7 days: normal
   - 7-30 days: warning
   - > 30 days: force fresh
```

---

## 📁 Output Specification

**Output Directory**: `skills/rebuild/skill-suite-upgrade/`

```
skill-suite-upgrade/
├── SKILL.md                       # CASE-aware skill definition
├── knowledge/
│   ├── case-system.md            # CASE framework
│   └── state-management.md       # State protocol
├── scripts/
│   ├── check_status.py           # Status reader
│   ├── validate_gate.py          # Gate validator
│   └── validate_zone_mapping.py  # Contract validator
├── data/
│   └── skill-schema.yaml         # YAML schema
└── loop/
    ├── boot_checklist.md         # Boot verification
    ├── gate_checklist.md         # Gate criteria
    └── resume_checklist.md       # Resume procedure
```

---

## ✅ Quality Gate

Trước khi declare hoàn thành:

1. **Self-validate all gates**:
   ```bash
   python scripts/validate_gate.py .skill-context/skill-suite-upgrade/design.md --all
   ```

2. **Run check_status.py** to verify status block

3. **Verify all files exist** per Zone Mapping

---

## 🛡️ Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | **CASE System First** | Hiểu CASE trước khi design |
| G2 | **Boot Mandatory** | KHÔNG ĐƯỢC skip boot sequence |
| G3 | **3 Gates** | Mỗi phase phải qua gate confirmation |
| G4 | **Exit Codes** | validate scripts exit 0/1/2 phải được respect |
| G5 | **State Block** | Status phải update sau mỗi gate |
| G6 | **Heavy Thinking** | Dùng K=4 chains để analyze vấn đề |

---

## 📊 Triggers

- "upgrade skill suite"
- "nâng cấp bộ skill"
- "cải thiện skill-architect/planner/builder"
- "apply CASE System"
- "Heavy Thinking cho skill"
