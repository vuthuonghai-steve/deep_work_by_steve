# Heavy Thinking Manual — Implementation Plan

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | Heavy Thinking K=8 chains methodology | Domain | Framework cho 8 lens | §2 P1 | ✅ |
| 2 | Hermes memory/session tools | Domain | Context loading sources | §2 P1 | ✅ |
| 3 | delegate_task subagent spawning | Technical | Spawn chains as subagents | §2 P1 | ✅ |
| 4 | YAML/JSON Schema syntax | Technical | Viết schemas cho output | §2 P1 | ✅ |
| 5 | Mermaid diagram syntax | Technical | diagrams.mmd output | §2 P1 | ✅ |
| 6 | K-chain lens taxonomy chi tiết | Domain | 8 lens definitions | §3 Zone | ⬜ |
| 7 | Context sources mapping chi tiết | Domain | Memory/Session/Project loading | §3 Zone | ⬜ |
| 8 | Deliberation process chi tiết | Domain | Synthesis methodology | §3 Zone | ⬜ |
| 9 | Chain isolation rules | Domain | Anti-contamination enforcement | §3 Zone | ⬜ |

**Legend**: ✅ = Có đủ | ⬜ = Cần tạo

---

## 2. Phase Breakdown

### Phase 0: Resource Preparation (Knowledge Domain)

```
Priority: Critical
Dependencies: None
```

- [x] Tạo `knowledge/k-chains-lens.md` — Chi tiết 8 lens taxonomy [TỪ DESIGN §3]
- [x] Tạo `knowledge/context-sources.md` — Chi tiết cách load Memory/Session/Project [TỪ DESIGN §3]
- [x] Tạo `knowledge/deliberation-process.md` — Synthesis methodology chi tiết [TỪ DESIGN §3]
- [x] Tạo `knowledge/chain-isolation-rules.md` — Anti-contamination rules [TỪ DESIGN §3]

### Phase 1: Core Skill Definition

```
Priority: Critical
Dependencies: Phase 0
Est: 4-6 hours
```

- [x] Tạo `SKILL.md` — Heavy thinking manual skill definition [TỪ DESIGN §3]

### Phase 2: Templates & Schemas

```
Priority: High
Dependencies: Phase 0
Est: 4-6 hours
```

- [x] Tạo `templates/task-meta.schema.yaml` — Task metadata YAML schema [TỪ DESIGN §3]
- [x] Tạo `templates/context-sources.schema.json` — Context sources JSON schema [TỪ DESIGN §3]
- [x] Tạo `templates/prepared-context.schema.json` — Enriched context JSON schema [TỪ DESIGN §3]
- [x] Tạo `templates/checklist.schema.yaml` — Verification checklist YAML schema [TỪ DESIGN §3]

### Phase 3: Scripts

```
Priority: High
Dependencies: Phase 1, Phase 2
Est: 6-8 hours
```

- [x] Tạo `scripts/load-context.py` — Context loading automation [TỪ DESIGN §3]
- [x] Tạo `scripts/spawn-chains.py` — Subagent spawning logic [TỪ DESIGN §3]

### Phase 4: Loops & Data

```
Priority: Medium
Dependencies: Phase 1
Est: 3-4 hours
```

- [x] Tạo `loop/quality-gate.md` — Pre-implementation checklist [TỪ DESIGN §3, §8]
- [x] Tạo `loop/chain-isolation-enforcer.md` — Anti-contamination rules [TỪ DESIGN §3, §8]
- [x] Tạo `data/trigger-keywords.md` — Trigger keywords config [TỪ DESIGN §3]
- [x] Tạo `data/chain-lens-taxonomy.yaml` — 8 lens definitions structured [TỪ DESIGN §3]

### Phase 5: References & Examples

```
Priority: Medium
Dependencies: Phase 1
Est: 2-3 hours
```

- [x] Tạo `references/examples/analysis-example.md` — Example output [TỪ DESIGN §3]

---

## 3. Knowledge & Resources Needed

| # | Resource | Type | Purpose |
|---|----------|------|---------|
| 1 | Hermes memory tool docs | Internal | Memory loading patterns |
| 2 | session_search tool | Internal | Session history extraction |
| 3 | delegate_task API | Internal | Subagent spawning |
| 4 | opencode-go model | External | DeepSeek V4 Flash cho chains |
| 5 | YAML Schema reference | External | Viết task-meta.schema.yaml |
| 6 | JSON Schema draft-07 | External | Viết context-sources.schema.json |
| 7 | Mermaid syntax guide | External | diagrams.mmd output |

---

## 4. Definition of Done

Trước khi đánh dấu hoàn thành, đảm bảo:

- [ ] Tất cả 14 files trong §3 Zone Mapping đã được tạo
- [ ] SKILL.md có đầy đủ: boot sequence, workflow phases, guardrails, triggers
- [ ] Tất cả 8 templates/schemas validate được (dùng schema validator)
- [ ] scripts/load-context.py chạy được và load đủ 3 nguồn
- [ ] scripts/spawn-chains.py spawn được K=8 chains
- [ ] loop/quality-gate.md có checklist đầy đủ
- [ ] loop/chain-isolation-enforcer.md có rules chống contamination
- [ ] data/trigger-keywords.yaml match được tất cả keywords đã liệt kê
- [ ] references/examples/analysis-example.md có output mẫu

---

## 5. Notes

### Từ design.md §9 Open Questions

1. **Task ID naming**: `{date}-{keyword}-{counter}` → Dùng pattern: `{date}-{trigger-keyword}-{uuid-short}` [CẦN LÀM RÕ: user preference?]
2. **Max context size**: 50KB per source → Đặt limit trong load-context.py [GỢI Ý BỔ SUNG]
3. **Chain timeout**: 5 min per chain → Đặt trong spawn-chains.py [GỢI Ý BỔ SUNG]
4. **Subagent vs inline**: Complex task = subagent → Đặt heuristic trong spawn-chains.py [GỢI Ý BỔ SUNG]
5. **OpenCode integration**: Dùng opencode-go/deepseek-v4-flash cho all chains → Support cả delegate_task [CẦN LÀM RÕ: preference?]

### Suggestions

- Nên tách `knowledge/chain-isolation-rules.md` riêng để dễ maintain [GỢI Ý BỔ SUNG]
- Thêm `scripts/validate-output.py` để validate output schemas [GỢI Ý BỔ SUNG]
- Nên có `data/task-complexity-matrix.yaml` để classify task type [GỢI Ý BỔ SUNG]

---

## 6. Builder Feedback Integration

### Success Criteria

- [ ] skill-builder có thể bắt đầu ngay sau khi nhận design.md + todo.md
- [ ] Tất cả 14 files trong §3 Zone Mapping đã được ánh xạ thành task cụ thể
- [ ] Phase 0 (Resource Preparation) đã hoàn thành — domain knowledge đủ cho Builder

### Known Gaps (for Builder)

- [ ] OpenCode integration details — khi nào dùng opencode vs delegate_task?
- [ ] Task complexity heuristics — phân biệt "complex" vs "simple" task?
- [ ] Output validation threshold — pass/fail criteria cho schema validation?

### Pre-implementation Checklist

- [ ] todo.md đã đủ thông tin để Builder bắt đầu
- [ ] Tất cả Critical/High priority tasks đã được đánh dấu
- [ ] Dependencies giữa các task đã được xác định rõ
- [ ] Phase 0 resources đã được tạo (4 knowledge files)
- [ ] Definition of Done đã đầy đủ

---

## Task Summary

| Phase | Tasks | Priority | Est. Hours |
|-------|-------|----------|------------|
| Phase 0 | 4 | Critical | 4-6 |
| Phase 1 | 1 | Critical | 4-6 |
| Phase 2 | 4 | High | 4-6 |
| Phase 3 | 2 | High | 6-8 |
| Phase 4 | 4 | Medium | 3-4 |
| Phase 5 | 1 | Medium | 2-3 |
| **Total** | **16** | - | **23-33** |

---

## Trace Summary

| Source | Items |
|--------|-------|
| [TỪ DESIGN §3] | 14 files |
| [TỪ DESIGN §8] | 2 loop files |
| [GỢI Ý BỔ SUNG] | 3 items |
| [CẦN LÀM RÕ] | 2 items |

---

**Planner**: Hermes Agent  
**Date**: 2026-05-11  
**Status**: COMPLETE
