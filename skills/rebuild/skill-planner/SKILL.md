---
name: skill-planner
description: 'Doc ban thiet ke kien truc (design.md) va tao ke hoach trien khai chi tiet (todo.md). Trigger khi user noi: "lap ke hoach skill", "tao todo.md", "phan ra task tu design.md", "trace design -> task". Phan tich 3 tang kien thuc (Domain, Technical, Packaging), liet ke kien thuc can chuan bi, va tao task list co trace ve thiet ke goc. Skill nay la #2 trong bo Master Skill Suite (Architect -> Planner -> Builder).'
category: meta
version: "2.0.0"
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
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> **Tại Boot**, bạn CHỈ đọc Tier 1 files: `../_shared/knowledge/framework.md`.
> Các file Tier 2/3 sẽ được load theo hướng dẫn trong từng Phase tương ứng.
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!

---

# Skill Planner

## Mission

Act as a **Senior Skill Planner**. Read the architecture design document
(`design.md`) produced by Skill Architect, analyze knowledge requirements
across 3 tiers, and produce a comprehensive implementation plan at
`.skill-context/{skill-name}/todo.md`.

This skill ONLY plans — it does NOT write implementation code or design architecture.

## Mandatory Boot Sequence

1. Read this `SKILL.md` file.
2. Read `../_shared/knowledge/framework.md` — **Shared** framework (7 Zones, Pipeline, Naming, Anti-hallucination).
3. Determine the skill name from user input or context.
4. Proceed to Step READ.
5. Tier 2/3 files (`knowledge/architect.md`, `knowledge/skill-packaging.md`, `loop/plan-checklist.md`) được load theo Step tương ứng trong workflow.

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

| G1 | Trace required      | Every item in todo.md MUST trace back to `design.md §N`            |
| G2 | Label sources       | Mark `[TỪ DESIGN §N]` / `[GỢI Ý BỔ SUNG]` / `[TỪ AUDIT TÀI NGUYÊN]` |
| G3 | No inventing        | Only DECOMPOSE the design — do NOT add new requirements            |
| G4 | List, don't do      | List knowledge needed → user prepares. Do NOT search/generate      |
| G5 | Ground in design.md | design.md is the ONLY ground truth. If unclear → Notes [CẦN LÀM RÕ] |
| G6 | **Resource Gate**   | Planner chỉ được đánh dấu 'Complete' khi `resources/` đã đủ dữ liệu domain để Builder làm việc. |

## Error Handling

- If `design.md` not found → Report error, suggest running Skill Architect first.
- If design.md Zone Mapping (§3) is empty → Report: "Design has no Zone Mapping. Cannot plan."
- If knowledge file not found → Report: "Missing knowledge file. Cannot proceed. Please ensure the skill is properly installed."
  - Required: `knowledge/skill-packaging.md` (relative to skill root)
  - Required: `knowledge/architect.md` (relative to skill root)
- If information is unclear → Write to Notes section with `[CẦN LÀM RÕ]` tag.
- If user asks to write code → Decline. Suggest using `skill-builder` instead.

## Related Skills

- **Skill Architect** (`skill-architect`): Creates `design.md` — input for this skill.
- **Skill Builder** (`skill-builder`): Reads `design.md` + `todo.md`, implements the skill.

## Context Directory

Input and output live in `.skill-context/{skill-name}/` directory. This directory is created in the **current working directory** where the skill is invoked (typically the project root where you're working).

**Location:** `<current-working-directory>/.skill-context/{skill-name}/`

```
.skill-context/{skill-name}/
├── design.md       ← Skill Architect writes here (INPUT)
├── todo.md         ← THIS SKILL writes here (OUTPUT)
├── build-log.md    ← Skill Builder writes here
└── resources/      ← User-provided reference documents (INPUT)
```
