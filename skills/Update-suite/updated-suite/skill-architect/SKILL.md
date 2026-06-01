---
name: skill-architect
description: "Senior Architect thiết kế kiến trúc Agent Skill mới. Nhận đầu vào là exploration.json và criteria.json để tự động hóa xây dựng bản vẽ blueprint.json hợp lệ 100% schema."
category: meta
tags: [architecture, design, blueprint, case-control]
version: "2.0.0"
author: "Steve Void Team"
when_to_use:
  - "Khi người dùng yêu cầu thiết kế kỹ năng hoặc skill mới"
  - "Khi đã hoàn thành Stage 0 Explorer và có exploration.json + criteria.json"
  - "Khi cần xây dựng bản vẽ cấu trúc 7 Zones và sơ đồ sequence cho skill"
---

# === BOOT CONFIGURATION (L0 — Anchor Rules) ===

```yaml
token_budget:
  SKILL_md: 500 tokens max
  enforcement: hard

priority_order:
  - schema_compliance
  - zero_placeholders
  - minimal_context_drift
  - safety_boundaries
```

---

<instructions>
## BOOT SEQUENCE — Execute in order

1. Đọc tệp `SKILL.md` này (done).
2. Nạp chính sách an toàn từ `policy/guardrails.md` (Tier 1).
3. Đọc quy trình thiết kế 3 Phase từ `policy/workflow.md` (Tier 1).
4. Kiểm tra sự tồn tại của Sổ cái bối cảnh `.skill-context/{skill-name}/`:
   - CHƯA CÓ: Báo lỗi và yêu cầu chạy Stage 0 Explorer trước.
   - ĐÃ CÓ: Đọc `exploration.json` và `criteria.json` làm cơ sở thiết kế.
5. Tiến hành thiết kế static structure, dynamic behavior và mitigation map theo đúng `policy/output-spec.md`.

## Core Constraints

```yaml
must:
  - write output strictly to .skill-context/{skill-name}/blueprint.json
  - ensure output complies 100% with _shared/schemas/blueprint.json
  - map 100% proposed files into standard 7 Zones enum
  - wrap all raw external references in XML boundaries (<external_input>)
  - implement mitigation strategy for every threat defined in Stage 0
  - include at least 2 interaction points (IP-01, IP-02)

must_not:
  - edit or modify any source code files directly in Stage 1
  - use placeholder names (file1.py, temp.sh) in static structure
  - introduce circular dependency in dynamic sequence steps
```

## Stop Conditions

```yaml
stop_conditions:
  - File written: .skill-context/{skill-name}/blueprint.json
  - Validation pass: blueprint.json validated 100% against its schema
  - Vietnamese summary and structural diagram delivered to user
  - Statement: "STAGE 1 COMPLETE — Blueprint validated and ready for Planner"
```
</instructions>

<context>
## ROUTING MAP — Load on demand

| File | Content | Load when |
|------|---------|-----------|
| `policy/guardrails.md` | Ràng buộc an toàn & Chống Shortcut | Boot Phase (Luôn nạp) |
| `policy/workflow.md` | Quy trình 3 Phase + Progressive Writing Contract | Boot Phase (Luôn nạp) |
| `policy/output-spec.md` | Đặc tả kỹ thuật blueprint.json với field validation | Phase 3 (Khi xuất file) |
| `knowledge/architect.md` | Tri thức chuyên sâu 3 Pillars & 7 Zones taxonomy | Phase 2 (Phân tích cấu trúc) |
| `knowledge/visualization-guidelines.md` | Hướng dẫn vẽ sơ đồ sequence & mapping 7 Zones | Phase 2 (Thiết kế flow) |
| `knowledge/design-exemplars.md` | Good/Bad JSON examples + Zone table + Token Budget | Phase 2 (Trước khi thiết kế) |
| `templates/blueprint.json.template` | Template JSON mẫu cho blueprint.json | Phase 3 (Khi viết output) |
| `loop/design-checklist.json` | Machine-readable quality gate MUST/SHOULD | Phase 3 (Trước khi hoàn thành) |
</context>