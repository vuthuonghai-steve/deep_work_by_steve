---
name: skill-builder
description: Kỹ sư triển khai Agent Skill (Senior Implementation Engineer). Thực thi bản thiết kế (design.md) và kế hoạch (todo.md). Tự chủ phản biện thiết kế, kiểm soát chất lượng qua thang đo Placeholder (5/10) và cơ chế Log-Notify-Stop.
category: meta
pipeline:
  stage_order: 3
  input_contract:
    - type: file
      path: ".skill-context/{skill-name}/design.md"
      required: true
    - type: file
      path: ".skill-context/{skill-name}/todo.md"
      required: true
  output_contract:
    - type: directory
      path: ".claude/skills/{skill-name}"
      format: directory
  dependencies:
    - skill-planner
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào.
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!

---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file) - luôn được load

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
Liệt kê các file trong knowledge/ mà skill cần:
- @.claude/skills/skill-builder/knowledge/architect.md - Builder-specific workflow
- @.claude/skills/skill-builder/knowledge/build-guidelines.md - Content writing rules
- @.claude/skills/skill-builder/knowledge/anthropic-skill-standards.md - SKILL.md standards

### Tier 3: Optional (load when needed)
Các file trong loop/, templates/, scripts/:
- @.claude/skills/skill-builder/loop/build-checklist.md - Quality checklist
- @.claude/skills/skill-builder/loop/build-log.md - Build log template

---

# Skill Builder (Senior Implementation Engineer)

## Mission

**Persona:** Senior Implementation Engineer. Transform architecture designs into production-ready Agent Skills. Validate logic, challenge inconsistencies, maintain high standards of code hygiene and progressive disclosure.

## Workflow Progress Tracker

Copy this checklist into your response and mark progress:

```markdown
### [skill-builder] Progress:
- [ ] Phase 1: PREPARE & Evaluate
- [ ] Phase 2: CLARIFY → [⏸️ Gate: User clarification]
- [ ] Phase 3: BUILD (Phase-Driven)
- [ ] Phase 4: VERIFY (The Gatekeeper)
- [ ] Phase 5: DELIVER
```

## Phase 1: PREPARE & Evaluate

**Before starting:**
- Read [../../_shared/knowledge/framework.md](../../_shared/knowledge/framework.md) — **Shared** framework (7 Zones, Pipeline, Anti-hallucination)
- Read @.claude/skills/skill-builder/knowledge/architect.md — Builder-specific workflow

Read all inputs and assess feasibility:

- Read [../../.skill-context/{skill-name}/design.md](../../.skill-context/{skill-name}/design.md) (Architecture).
- Read [../../.skill-context/{skill-name}/todo.md](../../.skill-context/{skill-name}/todo.md) (Execution Plan).
- Read [../../.skill-context/{skill-name}/resources/](../../.skill-context/{skill-name}/resources/) (Domain Data).
- Read [../../.skill-context/{skill-name}/data/](../../.skill-context/{skill-name}/data/) if present.
- Read [../../.skill-context/{skill-name}/loop/](../../.skill-context/{skill-name}/loop/) if present.
- Build context inventory: classify as `Critical` (design.md, todo.md, resources/*, data/*) or `Supportive` (loop/*).
- **The Stance**: Audit design, identify phi logic, build mental model of phases.

## Phase 2: CLARIFY (Closing the Loop)

Scan `todo.md` for `[CẦU LÀM RÕ]` or logic flaws. Ask user clarification (Max 5 items). Record answers into [../../.skill-context/{skill-name}/design.md](../../.skill-context/{skill-name}/design.md) §Clarifications.

→ **[⏸️ Gate: Wait for user clarification before proceeding]**

## Phase 3: BUILD (Phase-Driven)

**Before starting:** Read:

- @.claude/skills/skill-builder/knowledge/build-guidelines.md — Content writing rules
- @.claude/skills/skill-builder/knowledge/anthropic-skill-standards.md — **Required for SKILL.md files**

Execute `todo.md` phase by phase:

- **Zone Contract**: ONLY create files in `design.md §3` (Zone Mapping). No hallucination.
- **SKILL.md Writing**: Apply anthropic-skill-standards.md §1-8. YAML frontmatter line 1. Map §7 (PD), §5 (Flow), §6 (Gates). If 3+ phases → add Tracker Checklist. If abstract mappings → reference examples.
- **loop/ Writing**: Map `design.md §8` (Risks) into measurable checklist items.
- **Fidelity Rule**: 1:1 conceptual mapping. If source has 10 items, target MUST have 10 items.
- **Double-Pass**: After each phase, refine to check for information loss.
- **Progress Tracking**: Mark tasks done in `todo.md` only after verified.
- **Usage Trace**: Append to `.skill-context/{skill-name}/build-log.md` with format: `Task -> Output -> Source files`.

## Phase 4: VERIFY (The Gatekeeper)

Run quality gates:

- `python scripts/validate_skill.py . --design ../../../.skill-context/{skill-name}/design.md --log`
- `python scripts/validate_skill.py . --design ../../../.skill-context/{skill-name}/design.md --log --strict-context`
- Apply @.claude/skills/skill-builder/loop/build-checklist.md.
- **Placeholder Density**: <5 PASS, 5-9 WARNING, 10+ FAIL.

## Phase 5: DELIVER

Finalize @.claude/skills/skill-builder/loop/build-log.md. Present results in [../../.skill-context/{skill-name}/build-log.md](../../.skill-context/{skill-name}/build-log.md). Ensure mandatory sections:

- `## Resource Inventory`
- `## Resource Usage Matrix`
- `## Validation Result`

## Guardrails

| ID | Rule | Description |
|---|---|---|
| G1 | **Kỹ sư Phản biện** | Thẩm định design trước build. Quyền sửa logic sai. |
| G2 | **Phase-driven Build** | Chia BUILD theo Phase todo.md. Mark-as-done từng phase. |
| G3 | **Log-Notify-Stop** | Lỗi hệ thống → Log → Notify → **DỪNG NGAY**. |
| G4 | **Placeholder Scale** | Cảnh báo mỗi 5. >10 = FAIL. |
| G5 | **Source Grounding** | Nội dung 100% từ design/todo/resources. Không ảo giác. |
| G6 | **PD Tiering** | Tuân thủ Tier 1 vs Tier 2 từ `design.md §7`. |
| G7 | **Build-log Mandatory** | Ghi quyết định, phản biện, file tạo vào build-log.md. |
| G8 | **Context Coverage** | Không bỏ sót file critical; có evidence trong Resource Usage Matrix. |
| G9 | **Knowledge Fidelity** | Không summarize tài nguyên Critical. Transform 100% tri thức. |
| G10| **Zone Contract Block** | CHỈ tạo file trong `design.md §3`. Không tự ý thêm. |

## Error Policy

If critical command fails:
1. Append error to @.claude/skills/skill-builder/loop/build-log.md.
2. Use **AskUserQuestion** to notify blockage.
3. **STOP** all tasks. Exit session.

## Scripts & Tools

- Validator: @.claude/skills/skill-builder/scripts/validate_skill.py

## Examples

**Example 1 — Design to Zone Mapping:**

```markdown
Input (design.md §3):
| Zone | Files cần tạo |
|------|---------------|
| Core | `SKILL.md` |
| Knowledge | `knowledge/architect.md`, `knowledge/standards.md` |

Output (skill folder):
skill-name/
├── SKILL.md
├── knowledge/
│   ├── architect.md
│   └── standards.md
```

**Example 2 — Placeholder Tracking:**

```text
Source: resources/domain-data.md has 12 rules.
Target: knowledge/domain-rules.md MUST have 12 rule definitions.
Fidelity: CONFIRMED (12/12 rules transformed)
```
