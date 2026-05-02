# Design Checklist — Self-Verification Before Writing Output

> Source: design.md §3 (Loop row), §8 (Risks R1–R5)
> Run this checklist in Phase 5 before writing any file. All 5 questions must PASS.
> If any FAIL → return to Phase 3 (Data Mapping) to fix, then re-run checklist.

---

## The 5 Anti-Hallucination Questions

### Q1 — Source Field Verification (Mitigates: R2 Field Hallucination)

**Question**: "Mọi UI element trong bảng Data-Component Binding (§2A) đều có Source Field trong Schema không?"

**Check**:
- [ ] Mở schema file của module này (`Docs/life-2/database/schema-design/m[X]-*-schema.yaml`)
- [ ] Với mỗi row trong bảng §2A: xác nhận tên field tồn tại trong schema (exact match, không đoán)
- [ ] Nếu có bất kỳ UI element nào có Source Field = `[SOURCE MISSING]` → **FLAG** và report to user

**PASS condition**: Mọi Source Field đều là tên field thực tế trong schema, hoặc được đánh dấu rõ `[SOURCE MISSING]` (không có field ẩn hoặc field tự bịa).

**FAIL action**: Xóa hoặc đánh dấu `[SOURCE MISSING]` cho mọi field không verify được. Return to Phase 3.

---

### Q2 — Interaction Flow Verification (Mitigates: R4 Missing Diagram Gap)

**Question**: "Mọi Interaction Flow (Pre/Post/Error trong §2B) đều có nguồn từ diagram không?"

**Check**:
- [ ] Mở diagram files từ Phase 1 (activity diagram, sequence diagram, flow diagram)
- [ ] Với mỗi flow statement trong §2B: xác nhận có thể trace về ít nhất 1 diagram cụ thể
- [ ] Nếu diagram bị stub/empty → đã kích hoạt IP-3 ở Phase 1 chưa?
- [ ] Không có flow statement nào được viết chỉ dựa trên "common sense" hoặc suy đoán

**PASS condition**: Mọi Pre-condition, Main Action, Post-condition, Error State đều traceable về diagram đã đọc.

**FAIL action**: Remove hoặc annotate unverified flows với `[DIAGRAM MISSING]`. Kích hoạt IP-3 để report gap.

---

### Q3 — Merge Safety Check (Mitigates: R3 Overwrite Data Loss)

**Question**: "Nếu file spec cũ đã tồn tại, đã thực hiện Merge (không phải Overwrite) chưa?"

**Check**:
- [ ] Đã check xem `Docs/life-2/ui/specs/m[X]-*-ui-spec.md` tồn tại chưa (Phase 4)
- [ ] Nếu tồn tại: đã kích hoạt IP-2 và có confirm từ user chưa?
- [ ] Sections cũ có nội dung → preserved (không bị overwrite)?
- [ ] Chỉ sections trống/missing → generated?
- [ ] Không sử dụng "write entire file" nếu file cũ có sections với human-written content

**PASS condition**: Một trong hai:
- (a) File chưa tồn tại → write fresh từ template (PASS)
- (b) File đã tồn tại → đã IP-2, đã confirm merge plan, preserved existing sections (PASS)

**FAIL action**: Dừng write. Quay về Phase 4, thực hiện merge đúng quy trình.

---

### Q4 — Screen ID Convention Check (Mitigates: R2 Field Hallucination / naming)

**Question**: "Tất cả Screen ID trong §1 (Screen Inventory) đúng convention `SC-M[X]-NN` không?"

**Check**:
- [ ] Prefix là `SC-` (uppercase)
- [ ] Module segment là `M[X]` với X ∈ {1,2,3,4,5,6} và đúng module đang xử lý
- [ ] Number segment là 2-digit zero-padded: `01`, `02`, `10` (không phải `1`, `2`, `10` thiếu số 0)
- [ ] Số thứ tự sequential, không skip (01, 02, 03 — không phải 01, 03)
- [ ] Element IDs trong §2A đúng naming convention (prefix + kebab-case semantic name)

**PASS condition**: Mọi SC-ID đều pass format check. Mọi element ID đều có prefix đúng từ `knowledge/ui-component-rules.md`.

**FAIL action**: Rename sai IDs trước khi write. Update §3 UI Contract để match.

---

### Q5 — Cross-Module Component Check (Mitigates: Q1 policy violation)

**Question**: "Có component cross-module nào bị lặp lại trong spec này không?"

**Check**:
- [ ] Scan §2A (Data-Component Binding tables) tìm: `<Header>`, `<Sidebar>`, `<BottomNav>`, `<Toast>`, `<NotificationBanner>`, `<SearchBar>`, `<UserAvatar>` ở level "full specification"
- [ ] Nếu có → đã thay bằng reference đến `index.md` chưa?
- [ ] Check section đầu file có dòng: `> Cross-module components — see Docs/life-2/ui/specs/index.md.`?

**PASS condition**: Cross-module components chỉ được reference, không được spec lại từ đầu trong module spec này.

**FAIL action**: Replace full spec của cross-module component bằng reference: `> See index.md: [ComponentName]`.

---

## Severity Reference (từ design.md §8)

| Risk ID | Severity | Description | Checklist Question |
|---------|----------|-------------|-------------------|
| R1 — Context Overflow | P1 | Đọc quá nhiều files, tràn context | (Preventive: resource_scanner.py) |
| R2 — Field Hallucination | **P0** | UI field không có trong Schema | Q1, Q4 |
| R3 — Overwrite Data Loss | P1 | Ghi đè file cũ mất nội dung human | Q3 |
| R4 — Missing Diagram Gap | P1 | Diagram trống → AI đoán mò flow | Q2 |
| R5 — Component Misidentification | P2 | Nhầm component type (Input thay Select) | Q1 (verify Source Field type) |

> **P0** = Critical, fail immediately | **P1** = High, must fix before write | **P2** = Medium, note and continue

---

## Checklist Summary (Quick Run)

```
[ ] Q1 — PASS: All Source Fields verified against schema (no invented fields)
[ ] Q2 — PASS: All Interaction Flows traceable to specific diagrams
[ ] Q3 — PASS: Merge/fresh-write decision made correctly (IP-2 honored if file exists)
[ ] Q4 — PASS: All Screen IDs and Element IDs follow naming conventions
[ ] Q5 — PASS: No cross-module component fully re-specified (only referenced)

ALL 5 PASS → Proceed to write file
ANY FAIL  → Fix issue, re-run checklist
```
