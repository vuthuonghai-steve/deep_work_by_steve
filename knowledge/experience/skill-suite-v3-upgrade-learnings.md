# Skill Suite v3.0 Upgrade — Key Learnings

**Extracted from:** skill-suite-upgrade-session
**Date:** 2026-05-09
**Category:** experience

---

## Overview

Upgrade skill suite (skill-architect, skill-planner, skill-builder) từ v2.x lên v3.0 để trở thành Hermes-native, hỗ trợ multi-operation types, và YAML-first contracts.

---

## Key Insights

### Insight 1: Parallel Delegation Pattern
**What:** Orchestrator spawns 3 agents working simultaneously for brainstorming
**Why:** Reduces total session time, different perspectives captured
**Context:** Vòng 1 của upgrade session — Claude Code, Codex + subagent được delegate song song

### Insight 2: YAML-First Validation
**What:** Frontmatter YAML là canonical contract giữa các stage
**Why:** Machine-readable, validated, consistent across platforms
**Context:** Thay thế Markdown table contracts từ v2.x

### Insight 3: Hermes-Native Path Conventions
**What:** `~/.hermes/skills/` vs `~/.claude/skills/`
**Why:** Platform detection tự động, Hermes là default
**Context:** v3.0 architecture design

### Insight 4: Operation Type Enum (6 types)
**What:** `create_new`, `patch_existing`, `refactor_existing`, `migrate_platform`, `consolidate_skills`, `deprecate_skill`
**Why:** Xác định workflow và gates phù hợp với từng loại operation
**Context:** Core enhancement trong v3.0 upgrade

### Insight 5: Execution Mode (3 modes)
**What:** `lightweight` (fast, minimal gates), `standard` (balanced), `strict` (full validation)
**Why:** Adaptive workflow — không overhead khi không cần
**Context:** Cho phép patch nhỏ không phải qua full pipeline

### Insight 6: Install Target Resolution (4 priority levels)
**What:** Explicit CLI flag → Frontmatter → Platform detection → Default fallback
**Why:** Flexibility trong deployment target
**Context:** v3.0 architecture

### Insight 7: Refinement Loop (6-step)
**What:** `Observe → Identify → Decide → Apply → Document → Verify`
**Why:** Continuous improvement cho skill sau deployment
**Context:** Giải quyết issue #9.5 — vòng học từ feedback

### Insight 8: Progressive Disclosure Tiering (3-tier)
**What:** Tier 1 (skills_list), Tier 2 (skill_view), Tier 3 (specific path)
**Why:** Token-efficient loading — chỉ load khi cần
**Context:** Hermes native skill loading pattern

---

## Lessons Learned

### Lesson 1: Parallel Agent Delegation
**Situation:** Muốn brainstorm upgrade proposals từ nhiều góc nhìn
**Learning:** Spawn 3 agents song song thay vì sequential — hiệu quả hơn nhiều
**Action:** Sử dụng orchestrator pattern cho các session tương lai

### Lesson 2: Raw Files Are Input, Knowledge Is Output
**Situation:** Có 15+ raw documents từ session
**Learning:** Raw files chỉ là nguồn tham khảo — cần extract và consolidate thành knowledge entries
**Action:** Luôn chạy session-learner sau khi tạo raw documents

### Lesson 3: 3-Phase Pipeline Validated
**Situation:** Thiết kế skill suite với 3 stage (Architect → Planner → Builder)
**Learning:** Pipeline separation rõ ràng, contract giữa các stage là YAML frontmatter
**Action:** Giữ nguyên 3-phase structure cho skill suite v3.0

---

## Related

- [[skill-architect]] — Stage 1 của pipeline
- [[skill-planner]] — Stage 2 của pipeline
- [[skill-builder]] — Stage 3 của pipeline
- [[Hermes skill v3.0 architecture]] — Design document
- [[Operation types & execution modes]] — Proposal document

---

## Source

Session: skill-suite-upgrade-session
Messages: Session chứa 2 vòng delegate (vòng 1: brainstorm, vòng 2: research/design/brainstorm)
Files created: 15 raw documents trong docs/raw/{category}/