# Chain 4: Guardrails & Anti-Hallucination — Các biện pháp chống hallucination có hiệu quả không?

**Date:** 2026-05-12  
**Task:** Chain 4 — Guardrails & Anti-Hallucination Analysis  
**Workspace:** /home/steve/Work-space/deep_work_by_steve

---

## 1. Tổng quan

Phân tích hiệu quả của các biện pháp chống hallucination trong skill suite (skill-architect, skill-planner, skill-builder).

**Kết luận sơ bộ:** Thiết kế mạnh về ý tưởng (AH1-AH5, trace tags, zone contract), NHƯNG runtime không hiệu quả do quá tải — 25 guardrails vượt quá khả năng chú ý của LLM.

---

## 2. Các biện pháp hiện có

### 2.1 Anti-Hallucination Rules (AH1-AH5)

Từ `_shared/knowledge/framework.md` §7:

| Rule | Mô tả | Violation |
|------|-------|-----------|
| **AH1** | Every task MUST trace to source | Task without `[TỪ DESIGN §N]` |
| **AH2** | Only decompose, don't add requirements | New requirement not in design.md |
| **AH3** | Don't guess domain knowledge | Writing domain content without resources |
| **AH4** | Always label sources | No `[TỪ DESIGN]` / `[GỢI Ý]` distinction |
| **AH5** | Verify resources before completion | Planning complete with missing critical resources |

### 2.2 Trace Tags Standard

```
[TỪ DESIGN §N]      — Derived directly from design.md section N
[GỢI Ý BỔ SUNG]     — Suggested by skill, not in design.md
[TỪ AUDIT TÀI NGUYÊN] — Generated because resource was missing
[CẦN LÀM RÕ]        — Needs user clarification
```

### 2.3 Zone Contract

Builder chỉ được tạo file trong `design.md §3` (Zone Mapping). Không được thêm file ngoài contract.

### 2.4 Quality Gates

3 gate checks:
- Architect → Planner: §3 Zone Mapping, §7 PD, §8 Risks, §9 Open Questions
- Planner → Builder: task mapping, pre-req table, resource audit, phase breakdown
- Builder → Complete: placeholder density <5, all §3 files created, build-log evidence

---

## 3. Vấn đề: Thiết kế tốt nhưng Execution yếu

### 3.1 Quá tải Guardrails (P1-05)

Từ `skill-suite-llm-execution-analysis.md`:

> **P1-05: 25 guardrails exceed LLM attention capacity**
> - 3 skills × complex rules
> - Instruction following degrades mid-execution

**Thiết kế đưa ra:**
- 5 AH rules (AH1-AH5)
- Nhiều quality gates
- Trace tag requirements
- Progressive disclosure tiers

**Thực tế:** Khi LLM phải nhớ và tuân thủ 25+ guardrails cùng lúc, instruction following bắt đầu degrade ở giữa execution.

### 3.2 Self-Paradoxical System

```
┌─────────────────────────────────────────────────────────┐
│ Thiết kế: "Dừng và kiểm tra ở mỗi gate"              │
│ Thực tế:   Không có mechanism cho gate checkpoint      │
│                                                         │
│ Thiết kế: "Progressive Disclosure = load when needed"  │
│ Thực tế:   No trigger = no enforcement = no PD         │
│                                                         │
│ Thiết kế: "Heavy Thinking K=4 chains"                  │
│ Thực tế:   Sequential analysis ≠ parallel reasoning    │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Không có Automatic Enforcement

Các biện pháp hiện tại phụ thuộc vào:
1. LLM tuân thủ rule trong SKILL.md (dựa vào system prompt)
2. Checklist thủ công (không tự động)
3. Không có validator chạy tự động trước mỗi gate

---

## 4. Đánh giá Hiệu quả

### 4.1 Điểm mạnh

| Measure | Intent | Effect |
|---------|--------|--------|
| AH1 Traceability | Mạnh | Task có nguồn gốc rõ ràng |
| AH2 No new requirements | Mạnh | Ngăn builder tự thêm spec |
| AH3 No domain guessing | Mạnh | Buộc audit tài nguyên |
| Zone Contract | Mạnh | Giới hạn file creation |
| Trace Tags | Mạnh | Phân biệt nguồn gốc |

**Tư duy chống hallucination được đánh giá là "mạnh" trong research evaluation.**

### 4.2 Điểm yếu

| Measure | Problem | Impact |
|---------|---------|--------|
| 25 guardrails total | Quá tải LLM attention | Instruction degradation |
| No enforcement mechanism | Phụ thuộc vào system prompt | Không đáng tin cậy |
| Gate checkpoints manual | Không có auto-validate | LLM skip verification |
| P0-01: case-system.md missing | Boot fails → hallucinate | Architect fails at boot |

### 4.3 Specific Failures

**P0-01:** `case-system.md` referenced by skill-planner but DOES NOT EXIST
- Boot fails or hallucinates content
- Triggers when: skill-planner SKILL.md line 29 references it

**P0-02:** `knowledge/architect.md` in skill-builder doesn't exist
- Builder cannot read domain knowledge
- Triggers when: skill-builder SKILL.md line 78 references it

---

## 5. So sánh: Design vs Runtime

| Aspect | Design | Runtime |
|--------|--------|---------|
| AH Rules | 5 rules, clear | 25+ total, overwhelming |
| Trace Tags | Required, explicit | Often missing |
| Zone Contract | Strict | Frequently violated |
| Gate Checks | Defined | Manual, skipped |
| PD System | Tier 1/2/3 | No triggers = no enforcement |

---

## 6. Recommendations

### 6.1 Rút gọn Guardrails (Recommended)

Từ `skill-suite-llm-execution-analysis.md`:

| Change | Current | Recommended |
|--------|---------|-------------|
| Guardrails | 25 total | 5-7 per skill |
| Heavy Thinking | Claimed K=4 | Remove claim OR implement correctly |
| Progressive Disclosure | "load when needed" | Explicit triggers per phase |

**Target: 5-7 guardrails per skill maximum.**

### 6.2 Implement Automatic Enforcement

Thay vì dựa vào system prompt:
- Validator script chạy trước mỗi gate
- Exit code 0/1/2 cho pass/warn/fail
- LLM phải pass validator trước khi proceed

### 6.3 Essential Anti-Hallucination Core (5 rules)

```
1. [TỪ DESIGN §N] — Every task must trace
2. Không tạo file ngoài §3 Zone Mapping  
3. Không viết domain knowledge không có tài nguyên
4. Placeholder density < 5 (warning at 5-9, fail at 10+)
5. Stop and ask when blocked — don't guess
```

---

## 7. Kết luận

### Câu hỏi: Các biện pháp chống hallucination có hiệu quả không?

**Có — về thiết kế. Không — về execution.**

| Dimension | Rating | Reason |
|-----------|--------|--------|
| Design Intent | ✅ Mạnh | AH1-AH5, trace tags, zone contract đúng hướng |
| Coverage | ⚠️ Đủ | Đủ rules nhưng không enforced |
| Enforceability | ❌ Yếu | 25 guardrails quá tải, manual gates |
| Runtime Reliability | ❌ Thấp | LLM skip verification, hallucinate when blocked |

**Root Cause:** Thiết kế tốt nhưng "self-paradoxical" — đòi hỏi LLM tự kiểm soát mà không có enforcement mechanism.

**Để cải thiện:** Giảm guardrails xuống 5-7, thêm automatic validator, và implement explicit trigger cho progressive disclosure.

---

## Files Analyzed

- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/_shared/knowledge/framework.md` — AH1-AH5 rules
- `/home/steve/Work-space/deep_work_by_steve/docs/skill-suite-llm-execution-analysis.md` — P1-05 analysis
- `/home/steve/Work-space/deep_work_by_steve/docs/raw/ideas/skill-suite-improvement-raw-notes/2026-05-09-research-master-skill-suite-evaluation.vi.md` — Evaluation scoring
- `/home/steve/Work-space/deep_work_by_steve/knowledge/experience/skill-suite-pipeline-workflow.md` — Anti-hallucination rule documentation
