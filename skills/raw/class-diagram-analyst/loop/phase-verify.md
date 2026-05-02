# class-diagram-analyst — Phase Verification Checklist

> **Usage**: Builder tự điền sau mỗi phase hoàn thành. Theo dõi tiến độ toàn bộ workflow.
> **Source**: design.md §2.2, §5.1, §5.2, §6

---

## Phase 0 — Input Resolution

- [ ] Input type đã được phân loại (module rõ / chức năng / file context / mơ hồ)
- [ ] Nếu mơ hồ: IP0 đã được kích hoạt và user đã confirm scope
- [ ] Module ID đã xác định (VD: M1, M2...)
- [ ] Entity list dự kiến đã được đề xuất

**Trạng thái**: ⬜ Pending / ✅ Done
**Ghi chú**: ___

---

## Phase A — Extract Entities

- [ ] `data/module-map.yaml` đã được đọc
- [ ] Entity slugs cho module đã được lấy
- [ ] `er-diagram.md` đã được parse cho mỗi entity
- [ ] Field dict đầy đủ (tên, raw type, constraints từ ER)
- [ ] Không có entity nào bị bỏ sót so với module-map

**Trạng thái**: ⬜ Pending / ✅ Done
**Entities extracted**: ___
**Ghi chú**: ___

---

## Phase B — Cross-Reference

- [ ] `activity-diagrams/mX-a*.md` đã được scan
- [ ] Behaviors/hooks đã được extract cho mỗi entity
- [ ] `UseCase/use-case-mX-*.md` đã được scan
- [ ] Access rules (actor → CRUD) đã được extract
- [ ] Behaviors[] và access_control[] đã được gắn vào entity dict

**Trạng thái**: ⬜ Pending / ✅ Done
**Behaviors found**: ___
**Access rules found**: ___
**Ghi chú**: ___

---

## Phase C — Classify

- [ ] Decision Tree đã được chạy cho mỗi entity (Q1 → Q4)
- [ ] Stereotype labels đã gán: `<<Collection>>`, `<<EmbeddedDoc>>`, `<<ValueObject>>`
- [ ] `post_tags`, `post_media` đánh dấu `embed_in: posts` (nếu M2)
- [ ] M3 FeedQuery đánh dấu `<<ValueObject>>` (nếu M3)
- [ ] `shares` đánh dấu `[ASSUMPTION]` (nếu M4)
- [ ] Classification khớp với `module-map.yaml`

**Trạng thái**: ⬜ Pending / ✅ Done
**Root entities**: ___
**Embedded entities**: ___
**Assumptions**: ___
**Ghi chú**: ___

---

## [IP1] — Confirm Entity List

- [ ] Entity list + classification đã được trình bày cho user
- [ ] Behaviors tóm tắt đã được hiển thị
- [ ] Assumptions đã được báo cáo
- [ ] **User đã xác nhận** (ghi thời điểm confirm): ___
- [ ] Mọi adjustment đã được apply vào Phase C

**Trạng thái**: ⬜ Pending → Waiting → ✅ Confirmed
**Ghi chú user**: ___

---

## Phase D — Generate Markdown

- [ ] `templates/class-module.md.template` đã được đọc
- [ ] Mermaid `classDiagram` block đã được sinh
- [ ] Visibility modifiers đúng (`+` public, `-` passwordHash)
- [ ] Field format đúng (`+TypeName fieldName`, không có colon)
- [ ] Relationship arrows đúng (`User "1" --o "many" Post : authors`)
- [ ] Traceability Table đã được điền đầy đủ
- [ ] Assumption Register đã được tạo
- [ ] File ghi tại: `Docs/life-2/diagrams/class-diagrams/mX-name/class-mX.md`

**Trạng thái**: ⬜ Pending / ✅ Done
**File path**: ___
**Ghi chú**: ___

---

## [IP2] — Review Markdown

- [ ] `class-mX.md` đã được trình bày cho user
- [ ] Summary (entities, fields, relationships, assumptions) đã được hiển thị
- [ ] **User đã approve** (ghi thời điểm approve): ___
- [ ] Mọi changes requested đã được apply và user đã re-approve

**Trạng thái**: ⬜ Pending → Waiting → ✅ Approved
**Ghi chú user**: ___

---

## Phase E — Generate YAML

- [ ] `templates/contract.yaml.template` đã được đọc
- [ ] `scripts/generate_yaml.py` đã được chạy (hoặc YAML được tạo thủ công theo template)
- [ ] LOCKED header comment tồn tại ở đầu file
- [ ] `meta` section đầy đủ: module, skill_version, generated_at, sources_consumed
- [ ] Mọi entity có: slug, aggregate_root, fields[], behaviors[], access_control, assumptions[]
- [ ] `validation_report` có: total_fields, fields_with_source, fields_as_assumption
- [ ] File ghi tại: `Docs/life-2/diagrams/class-diagrams/mX-name/class-mX.yaml`

**Trạng thái**: ⬜ Pending / ✅ Done
**File path**: ___
**Ghi chú**: ___

---

## Phase F — Self-Validate

- [ ] `scripts/validate_contract.py class-mX.yaml` đã được chạy
- [ ] [G1] Citation check: Mọi field có source — KQ: ___ violations
- [ ] [G2] Type check: Mọi type trong whitelist — KQ: ___ violations
- [ ] [G3] Slug unique check: Không có duplicate — KQ: ___ violations
- [ ] [G4] Root classification check: KQ: ___ warnings
- [ ] [G5] LOCKED header check: KQ: ___ warnings
- [ ] Tổng violations: ___ | Tổng warnings: ___
- [ ] KQ cuối: ✅ PASS / ❌ FAIL

**Trạng thái**: ⬜ Pending / ✅ Done
**Validate output**: ___
**Ghi chú**: ___

---

## [IP3] — Validation Report

- [ ] Kết quả validation đã được trình bày cho user
- [ ] Nếu PASS: **User đã acknowledge** (ghi thời điểm): ___
- [ ] Nếu FAIL: violations đã được trình bày, đã quay về Phase E để fix
- [ ] `index.md` đã được cập nhật → Status: ✅ Ready (CHỈ khi PASS + user acknowledge)

**Trạng thái**: ⬜ Pending → Waiting → ✅ Done (PASS) / 🔴 BLOCKED (FAIL)
**Ghi chú user**: ___

---

## Session Summary

| Phase | Status | Key Output |
|-------|--------|-----------|
| Phase 0 — Input Resolution | ⬜ | Module: ___ |
| Phase A — Extract | ⬜ | ___ entities |
| Phase B — CrossRef | ⬜ | ___ behaviors, ___ access rules |
| Phase C — Classify | ⬜ | ___ Root, ___ Embedded |
| [IP1] — Entity Confirm | ⬜ | User: ___ |
| Phase D — Gen .md | ⬜ | class-mX.md |
| [IP2] — .md Review | ⬜ | User: ___ |
| Phase E — Gen .yaml | ⬜ | class-mX.yaml |
| Phase F — Validate | ⬜ | PASS/FAIL |
| [IP3] — Report | ⬜ | User: ___ |
