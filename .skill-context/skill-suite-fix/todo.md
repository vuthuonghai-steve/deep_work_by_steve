# Todo.md - Skill Suite Fix Plan

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | CLAUDE.md format standards (sections 3,4,10,11,12) | Technical | Source for format knowledge | [TỪ DESIGN §3] | ✅ |
| 2 | Existing validate_skill.py | Technical | Reference for validator pattern | [TỪ DESIGN §3] | ✅ |
| 3 | build-checklist.yaml (existing) | Technical | Reference for checklist format | [TỪ DESIGN §3] | ✅ |

---

## 2. Phase Breakdown

### Phase 1: Embed Format Knowledge (Shared + Per-Skill)

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 1.1 | Create `_shared/knowledge/format-standards.md` - single source of truth for format knowledge | Critical | 2 | None | [TỪ DESIGN §3] |
| 1.2 | Create `skill-architect/knowledge/format-standards.md` - reference _shared + architect-specific | Critical | 1 | 1.1 | [TỪ DESIGN §3] |
| 1.3 | Create `skill-planner/knowledge/format-standards.md` - reference _shared + planner-specific | Critical | 1 | 1.1 | [TỪ DESIGN §3] |
| 1.4 | Create `skill-builder/knowledge/format-standards.md` - reference _shared + builder-specific | Critical | 1 | 1.1 | [TỪ DESIGN §3] |
| 1.5 | Update SKILL.md of each skill to reference new format-standards.md in Tier 1 boot sequence | High | 1 | 1.2, 1.3, 1.4 | [TỪ DESIGN §3] |

### Phase 2: Create Format Validator

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 2.1 | Create `skill-builder/scripts/validate_format.py` - core validator | Critical | 4 | None | [TỪ DESIGN §3] |
| 2.2 | Add XML tag validation (<instructions>, <context>, <examples>, <output_contract>) | Critical | 1 | 2.1 | [TỪ DESIGN §3] |
| 2.3 | Add YAML block validation (must:, must_not:, priority_order:) | Critical | 1 | 2.1 | [TỪ DESIGN §3] |
| 2.4 | Add trace tag validation ([TỪ DESIGN §N], [GỢI Ý BỔ SUNG], etc.) | Critical | 1 | 2.1 | [TỪ DESIGN §3] |
| 2.5 | Add token budget check (SKILL.md <500 lines, knowledge <200 lines) | High | 1 | 2.1 | [TỪ DESIGN §3] |
| 2.6 | Add Progressive Disclosure tier validation | Medium | 2 | 2.1 | [TỪ DESIGN §3] |

### Phase 3: Update Checklists

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 3.1 | Update `skill-architect/loop/design-checklist.yaml` - add format compliance items | High | 1 | 1.2, 2.1 | [TỪ DESIGN §3] |
| 3.2 | Update `skill-planner/loop/plan-checklist.yaml` - add trace tag validation | High | 1 | 1.3, 2.4 | [TỪ DESIGN §3] |
| 3.3 | Update `skill-builder/loop/build-checklist.yaml` - add format compliance items | High | 1 | 1.4, 2.1 | [TỪ DESIGN §3] |
| 3.4 | Add checklist item: verify XML tags in SKILL.md output | High | 0.5 | 3.3 | [TỪ DESIGN §3] |
| 3.5 | Add checklist item: verify YAML blocks in constraints/output_contract | High | 0.5 | 3.3 | [TỪ DESIGN §3] |

### Phase 4: Add Reference Examples

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 4.1 | Create `skill-architect/references/examples/design-example.md` - full format design.md | Medium | 2 | 1.2 | [TỪ DESIGN §3] |
| 4.2 | Create `skill-planner/references/examples/todo-example.md` - full format todo.md | Medium | 2 | 1.3 | [TỪ DESIGN §3] |
| 4.3 | Create `skill-builder/references/examples/skill-example.md` - full format SKILL.md | Medium | 2 | 1.4 | [TỪ DESIGN §3] |
| 4.4 | Verify all examples match format-standards.md | Medium | 1 | 4.1, 4.2, 4.3 | [TỪ DESIGN §3] |

### Phase 5: Enforce Progressive Disclosure

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 5.1 | Add tier loading validation to validate_format.py | Medium | 2 | 2.6 | [TỪ DESIGN §3] |
| 5.2 | Add check: Tier 1 boot should load ≤3 files | Medium | 1 | 5.1 | [TỪ DESIGN §3] |
| 5.3 | Add check: Tier 2 files only loaded from correct phase | Medium | 1 | 5.1 | [TỪ DESIGN §3] |
| 5.4 | Document tier loading rules in format-standards.md | Medium | 1 | 5.1 | [TỪ DESIGN §3] |

---

## 3. Knowledge & Resources Needed

| Resource | Purpose | Source |
|----------|---------|--------|
| CLAUDE.md sections 3,4,10,11,12 | Format standards source | `/home/steve/Work-space/deep_work_by_steve/CLAUDE.md` |
| validate_skill.py | Validator pattern reference | `/skills/rebuild/skill-builder/scripts/` |
| build-checklist.yaml | Checklist format reference | `/skills/rebuild/skill-builder/loop/` |
| framework.md | Zone structure reference | `/skills/rebuild/_shared/knowledge/` |

---

## 4. Definition of Done

- [ ] `_shared/knowledge/format-standards.md` created and contains all format standards
- [ ] Each skill has `knowledge/format-standards.md` referencing shared
- [ ] SKILL.md of each skill references format-standards in Tier 1
- [ ] `validate_format.py` exists and validates:
  - [ ] XML tags presence
  - [ ] YAML block format
  - [ ] Trace tag format
  - [ ] Token budget compliance
- [ ] All 3 checklists updated with format compliance items
- [ ] Reference examples created for all 3 skills
- [ ] Progressive Disclosure tier validation functional

---

## 5. Notes

### Format Standards cần embed (từ CLAUDE.md):
1. **Section 3**: Format Selection Rules (Markdown vs YAML vs XML)
2. **Section 4**: Token Budget Guidelines (L0 <400, L1 <1000, L2 <2500)
3. **Section 10**: Semantic Activation Anchors (must, must_not, should)
4. **Section 11**: Token Budget by Format
5. **Section 12**: Definition of Done

### Validation priorities:
1. **Critical**: XML tags, YAML blocks, trace tags
2. **High**: Token budget, file structure
3. **Medium**: Progressive Disclosure enforcement

---

## 6. Builder Feedback Integration

### Success Criteria
- [ ] skill-builder có thể start ngay sau khi nhận design.md + todo.md
- [ ] Tất cả files trong §3 Zone Mapping đã được ánh xạ thành task cụ thể
- [ ] Resources đủ "rich" để Builder không cần hỏi thêm domain knowledge

### Known Gaps (for Builder)
- [ ] Token budget per file type chưa được define cụ thể
- [ ] Legacy trace tags ([GỢI Ý], [TỪ AUDIT]) support cần xác nhận

### Pre-implementation Checklist
Trước khi bàn giao cho Builder, đảm bảo:
- [ ] Todo.md có đủ thông tin để Builder bắt đầu
- [ ] Tất cả Priority/Critical tasks đã được đánh dấu rõ
- [ ] Dependencies giữa các task đã được xác định
- [ ] Resources trong resources/ đã được audit là "Rich"
