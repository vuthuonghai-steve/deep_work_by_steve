---
name: skill-planner
description: 'Doc ban thiet ke kien truc (design.md) va tao ke hoach trien khai chi tiet (todo.md). Trigger khi user noi: "lap ke hoach skill", "tao todo.md", "phan ra task tu design.md", "trace design -> task". Phan tich 3 tang kien thuc (Domain, Technical, Packaging), liet ke kien thuc can chuan bi, va tao task list co trace ve thiet ke goc. Skill nay la #2 trong bo Master Skill Suite (Architect -> Planner -> Builder).'
category: meta
version: "3.0.0"
case_system: true
pipeline:
  stage_order: 2
  input_contract:
    - type: file
      path: ".skill-context/{skill-name}/design.md"
      required: true
  output_contract:
    - type: file
      path: ".skill-context/{skill-name}/todo.md"
      format: markdown
  dependencies:
    - skill-architect
  successor_hints:
    - skill: skill-builder
      needs: [design.md, todo.md]
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "../_shared/knowledge/framework.md"
      base: "skill_dir"
    - path: "knowledge/case-system.md"
      base: "skill_dir"
      triggers: [boot_sequence, entering_planning]
    - path: "scripts/check_status.py"
      base: "skill_dir"
      triggers: [boot_sequence]
    - path: "references/format-standards.md"
      base: "skill_dir"
      load_when: "Boot — REQUIRED for AI-first format knowledge"
  tier2:
    - path: "knowledge/architect.md"
      base: "skill_dir"
      load_when: "Step READ (audit design.md)"
    - path: "knowledge/skill-packaging.md"
      base: "skill_dir"
      load_when: "Step ANALYZE (3-tier breakdown)"
  tier3:
    - path: "loop/plan-checklist.md"
      base: "skill_dir"
      load_when: "Before deliver (Quality Gate)"
    - path: "loop/resume_checklist.md"
      base: "skill_dir"
      triggers: [resuming_from_checkpoint]
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> **Tại Boot**, bạn CHỈ đọc Tier 1 files.
> Các file Tier 2/3 sẽ được load theo hướng dẫn trong từng Phase tương ứng.
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!

---

# Skill Planner — Multi-Perspective Design-to-Plan Converter

## 🚀 Boot Sequence (MANDATORY — Thực hiện ĐÚNG THỨ TỰ)

### Step 1: Read SKILL.md

- [ ] Đọc `SKILL.md` này toàn bộ
- [ ] Nắm workflow và guardrails

### Step 2: Check design.md exists

- [ ] Verify `.skill-context/{skill-name}/design.md` tồn tại
- [ ] Nếu không có → báo lỗi: cần chạy skill-architect trước

### Step 3: Determine Position

| phase | Position         | Action                                               |
| ----- | ---------------- | ---------------------------------------------------- |
| 0     | Fresh start      | Proceed to Step READ                                 |
| 1-3   | Resume available | Ask user: resume or restart?                         |
| 4     | Complete         | Report: "Todo.md already exists. Use skill-builder." |

### Step 4: Proceed to Step READ

---

# Skill Planner

## Mission

Act as a **Senior Skill Planner**. Read the architecture design document
(`design.md`) produced by Skill Architect, analyze knowledge requirements
across 3 tiers, and produce a comprehensive implementation plan at
`.skill-context/{skill-name}/todo.md`.

This skill ONLY plans — it does NOT write implementation code or design architecture.

## Multi-Perspective Analysis

Planner sử dụng **Multi-Perspective Analysis** để phân tích design.md toàn diện:

### 4 Analysis Perspectives

| Perspective   | Focus Area             | Purpose                                     |
| ------------- | ---------------------- | ------------------------------------------- |
| Perspective 1 | Domain Knowledge Audit | Đánh giá resources/ có đủ domain knowledge? |
| Perspective 2 | Technical Requirements | Phân tích tool, syntax, dependencies        |
| Perspective 3 | Task Complexity        | Ước lượng effort, phát hiện risks           |
| Perspective 4 | Traceability           | Đảm bảo every task → design section         |

### Synthesis Step

Sau khi phân tích từ 4 góc nhìn:

1. **Synthesize**: Tổng hợp 4 perspectives thành unified plan
2. **Cross-validate**: Kiểm tra tasks không conflict
3. **Final output**: todo.md với đầy đủ trace tags

---

## Step READ — Đọc Input & Audit Tài nguyên

Read all available input sources and audit current state:

1. **Master Design** (REQUIRED): Refer to `knowledge/architect.md` (the 7-Zone framework reference) and read `.skill-context/{skill-name}/design.md` to understand the overarching standards.
2. **design.md** (REQUIRED): Read `.skill-context/{skill-name}/design.md`.
   - Extract Zone Mapping (§3) and Capability Map (§2) as the primary analysis targets.

3. **Audit resources/** (IF EXISTS): List all files in `.skill-context/{skill-name}/resources/`.
   - For each file: Read filename and content.
   - **Evaluative Audit**: Planner must judge if the content is "Thin" (lack of detail) or "Rich" (ready for Builder implementation).

4. **Context prompt** (IF EXISTS): Integrate user specific instructions.

## Step ANALYZE — Phân tích 3 Tầng & Audit Kiến thức

Apply the 3-tier knowledge model from `knowledge/skill-packaging.md`.

For EACH Zone that has content in **design.md §3 Zone Mapping** (specifically reading the `Files cần tạo` column):

1. **Tier 1 — Domain (THE AUDIT)**: What domain knowledge is needed?
   - **Audit Logic**: Đối chiếu kiến thức cần thiết với "Danh sách tài nguyên hiện có" (từ Step READ).
   - **Case 1: Đã có đủ** → Ghi Status: `✅`, Tier: `Domain` trong Pre-requisites table.
   - **Case 2: Chưa có hoặc Sơ sài** → Ghi Status: `⬜` trong Pre-requisites table **VÀ** sinh một **TASK** trong Phase 0: "Chuẩn bị/Soạn thảo tài liệu domain cho {Topic} tại resources/{topic}.md". [TỪ AUDIT TÀI NGUYÊN]

2. **Tier 2 — Technical**: What tools, syntax, or technical skills are needed to implement this zone?
   - If documentation for these tools is missing → sinh pre-requisite entry (Tier: `Technical`).

3. **Tier 3 — Packaging**: How to map this into the specific zone of the agent skill?
   - Read `Files cần tạo` from §3. Generate explicit Tasks for Builder to create exactly these files.
   - **Data Zone**: If §3 lists files under `data/` zone (e.g., `data/config.yaml`, `data/schema.json`), create a Task for Builder to create `data/` directory and populate these files per design specification.

Apply the **Conversion Checklist** for specific design sections:

- **§6 Interaction Points**: Create Tasks to implement templates or prompts for user interaction points.
- **§7 Progressive Disclosure Plan**: For files listed as Tier 1 (Mandatory) vs Tier 2 (Conditional), create a Task for Builder to document this boot sequence in `SKILL.md`.
- **§8 Risks & Blind Spots**: Create a Task to build strict `loop/` checklists to mitigate these exact risks.

## Step WRITE — Ghi todo.md

Write the analysis results to `.skill-context/{skill-name}/todo.md`.

The file MUST contain exactly 6 sections:

```
## 1. Pre-requisites
  Table with columns: #, Tài liệu / Kiến thức, Tier (Domain/Technical/Packaging), Mục đích, Trace, Status

## 2. Phase Breakdown
  Tasks grouped by execution phase, each with checkbox, priority, and trace tag.
  MUST include `Phase 0: Resource Preparation` for missing domain documents.

  **Table columns**: #, Task, Priority (Critical/High/Medium/Low), Est. Hours, Dependencies, Trace

## 3. Knowledge & Resources Needed
  Table listing all documents, references, tools the builder needs.

## 4. Definition of Done
  Checklist of completion criteria. Must include checking that all files specified in §3 are created.

## 5. Notes
  Open questions, things to clarify, supplementary suggestions.
  Items from design.md §9 (Open Questions) → migrate here, mark [CẦN LÀM RÕ].

## 6. Builder Feedback Integration
  (Required only if there is upstream feedback to address)

  Each task:
```

- [ ] Task description [TỪ DESIGN §N] hoặc [TỪ AUDIT TÀI NGUYÊN]

```

**Priority Guidelines**:
- **Critical**: Tasks that block other tasks or are core to skill functionality
- **High**: Important tasks that should be done early
- **Medium**: Standard tasks
- **Low**: Nice-to-have tasks, can be done later

**Est. Hours Guidelines**:
- 1-2 hours: Simple file creation
- 4-8 hours: Complex knowledge documents
- 8-16 hours: Full zone implementation

**Dependency Detection**:
- Task A depends on Task B when:
- Task A needs output of Task B
- Task A references file created by Task B
- Task A must happen after Task B temporally

## Step VERIFY
Every item MUST end with a trace tag:
- `[TỪ DESIGN §N]` — derived directly from design.md section N
- `[GỢI Ý BỔ SUNG]` — suggested by Planner, not in design.md
- `[TỪ AUDIT TÀI NGUYÊN]` — generated because a required resource was missing
- `[CẦN LÀM RÕ]` — needs user clarification

## Step VERIFY — Kiểm chứng & Đóng băng Kế hoạch

Sau khi viết `todo.md`, Planner thực hiện bước tự kiểm tra cuối cùng:

1. **Resource Integrity Check**: Đối chiếu bảng Pre-requisites với thực tế `resources/`.
 - Nếu bất kỳ tài nguyên Sống còn (Crucial) nào ghi `Status: ⬜`, Planner PHẢI thông báo: "Kế hoạch sẽ bắt đầu từ Phase 0 để chuẩn bị tài nguyên. Xin mời bổ sung."
2. **Contract Traceability**: Kiểm tra xem tất cả các file trong §3 "Files cần tạo" đã được ánh xạ thành Task cụ thể chắp nối với `todo.md` chưa.
3. **DoD Verification**: Đảm bảo bảng Definition of Done có bao hàm việc tạo tất cả các file thiết yếu.

## Confirm

Present the completed todo.md to the user for review.

- If user confirms → mark planning as complete.
- If user requests changes → update todo.md accordingly and present again.

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | Trace required      | Every item in todo.md MUST trace back to `design.md §N`            |
| G2 | Label sources       | Mark `[TỪ DESIGN §N]` / `[GỢI Ý BỔ SUNG]` / `[TỪ AUDIT TÀI NGUYÊN]` |
| G3 | No inventing        | Only DECOMPOSE the design — do NOT add new requirements            |
| G4 | Ground in design.md | design.md is the ONLY ground truth. If unclear → Notes [CẦN LÀM RÕ] |
| G5 | Resource Gate       | Planner chỉ đánh dấu 'Complete' khi `resources/` đã đủ cho Builder |

## 📐 Format Standards (Output Contract)

Todo documents MUST use hybrid XML+YAML+Markdown format:

```xml
<task>Implementation goal summary</task>
<constraints>
```yaml
must:
  - requirement 1
  - requirement 2
must_not:
  - prohibition 1
priority_order:
  - critical_first
  - high_second
```
</constraints>
<examples>Phase breakdown examples with trace tags</examples>
```

- **YAML frontmatter**: Required for artifact_type, skill_name, stage, status
- **XML tags**: Use `<task>`, `<context>`, `<constraints>`, `<examples>` for semantic boundaries
- **YAML blocks**: For priority_order, must/must_not constraints, pre-requisite tiering
- **Trace tags**: REQUIRED — `[TỪ DESIGN §N]`, `[TỪ AUDIT TÀI NGUYÊN]`, `[GỢI Ý BỔ SUNG]`, `[CẦN LÀM RÕ]`

> ⚠️ **Non-negotiable**: todo.md output from this skill MUST follow this format with proper trace tags.

## Error Handling

### Exit Codes (Machine-Readable)

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | PASS/Success | Continue to next step |
| 1 | FAIL | Fix issue, retry, or report |
| 2 | EMERGENCY | Stop immediately, report error |

### Error Scenarios

- If `design.md` not found → Report error, suggest running Skill Architect first.
- If design.md Zone Mapping (§3) is empty → Report: "Design has no Zone Mapping. Cannot plan."
- If knowledge file not found → Report: "Missing knowledge file. Cannot proceed. Please ensure the skill is properly installed."
- Required: `knowledge/skill-packaging.md` (relative to skill root)
- Required: `knowledge/architect.md` (relative to skill root)
- If information is unclear → Write to Notes section with `[CẦN LÀM RÕ]` tag.
- If user asks to write code → Decline. Suggest using `skill-builder` instead.
- If checkpoint is stale (> 7 days) → Warn user, require explicit confirmation to proceed.

## Related Skills

- **Skill Architect** (`skill-architect`): Creates `design.md` — input for this skill.
- **Skill Builder** (`skill-builder`): Reads `design.md` + `todo.md`, implements the skill.

## Context Directory

Input and output live in `.skill-context/{skill-name}/` directory. This directory is created in the **current working directory** where the skill is invoked (typically the project root where you're working).

**Location:** `<current-working-directory>/.skill-context/{skill-name}/`

```

.skill-context/{skill-name}/
├── design.md ← Skill Architect writes here (INPUT)
├── todo.md ← THIS SKILL writes here (OUTPUT)
├── build-log.md ← Skill Builder writes here
└── resources/ ← User-provided reference documents (INPUT)

```

```
