# todo.md — session-learner

**Skill Name:** `session-learner`
**Planner:** skill-planner
**Date:** 2026-05-08

---

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|------------------------|------|----------|-------|--------|
| 1 | Session structure (Hermes) | Technical | Hiểu cách đọc session data | [TỪ DESIGN §5] | ⬜ Cần research |
| 2 | Markdown best practices | Domain | Viết markdown đúng chuẩn | [GỢI Ý BỔ SUNG] | ✅ Có sẵn |
| 3 | Knowledge folder structure | Domain | Biết ghi vào đâu | [TỪ DESIGN §1] | ⬜ Cần xác nhận |

---

## 2. Phase Breakdown

### Phase 1: Core Skill Files

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 1.1 | Tạo `SKILL.md` với persona session-learner | Critical | 1 | None | [TỪ DESIGN §3] |
| 1.2 | Viết workflow 2-phase trong SKILL.md | Critical | 1 | 1.1 | [TỪ DESIGN §7] |

### Phase 2: Knowledge & Templates

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 2.1 | Viết `knowledge/session-extraction.md` | High | 2 | Phase 1 | [TỪ DESIGN §3] |
| 2.2 | Tạo `templates/knowledge-entry.template` | High | 1 | 2.1 | [TỪ DESIGN §3] |

### Phase 3: Quality & Guardrails

| # | Task | Priority | Est. Hours | Dependencies | Trace |
|---|------|----------|------------|--------------|-------|
| 3.1 | Viết `loop/learn-checklist.md` | Medium | 1 | Phase 2 | [TỪ DESIGN §8] |

---

## 3. Knowledge & Resources Needed

| Resource | Purpose | Source |
|----------|---------|--------|
| Hermes session format | Cách đọc session data | Cần research |
| Markdown standard | Viết markdown đúng chuẩn | Có sẵn |

---

## 4. Definition of Done

- [ ] `SKILL.md` có đầy đủ persona, 2-phase workflow, guardrails
- [ ] `knowledge/session-extraction.md` hướng dẫn extract từ session
- [ ] `templates/knowledge-entry.template` đúng format markdown
- [ ] `loop/learn-checklist.md` có checklist quality gate
- [ ] Skill output vào đúng folder: `skills/rebuild/session-learner/`

---

## 5. Notes

- Hardcoded path `/home/steve/Work-space/deep_work_by_steve/knowledge/` — user đã confirm
- Skill này standalone, không thuộc pipeline 3-stage chính

---

## 6. Builder Feedback Integration

### Success Criteria
- [ ] skill-builder có thể bắt đầu ngay với design.md + todo.md này
- [ ] Tất cả files trong §3 Zone Mapping đã được ánh xạ thành task

### Known Gaps (for Builder)
- [ ] Session format cụ thể của Hermes — cần tự research thêm

### Pre-implementation Checklist
- [ ] Todo.md đủ thông tin để Builder bắt đầu
- [ ] Priority/Critical tasks đã rõ
- [ ] Dependencies giữa tasks đã xác định
