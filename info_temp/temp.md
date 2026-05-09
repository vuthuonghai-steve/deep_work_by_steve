# Skill Suite v3.0 Upgrade — Project Spec & Task Breakdown

**Ngày:** 2026-05-09
**Version:** 1.0.0
**Status:** draft
**Author:** Steve Void Team
**Language:** vi

---

## MỤC ĐÍCH

Tài liệu này định nghĩa **SPEC** đầy đủ và **TASK BREAKDOWN** cho việc nâng cấp bộ 3 skill (skill-architect, skill-planner, skill-builder) từ v2.x lên v3.0 — Hermes-native, portable, multi-operation.

---

## TỔNG QUAN DỰ ÁN

### Mục tiêu

1. Hoạt động trên cả Hermes và Claude platforms
2. Hỗ trợ 6 operation types: create_new, patch_existing, refactor_existing, migrate_platform, consolidate_skills, deprecate_skill
3. Sử dụng YAML frontmatter làm contract chính thức
4. Portable — có thể copy sang bất kỳ thư mục nào mà không hardcode path
5. Có refinement loop chính thức với feedback mechanism

### Phạm vi

**Trong phạm vi:**
- Bộ 3 skill tại `skills/rebuild/`: skill-architect, skill-planner, skill-builder
- `_shared/knowledge/framework.md` — shared foundation
- Validators tại `_shared/validators/`
- Templates tại `_shared/templates/`
- Fixtures tại `_shared/fixtures/`

**Ngoài phạm vi:**
- skill-learner, spec-generator (khác pipeline)
- Skills Hub integration (P2)

### Nguồn tài liệu tham khảo

| Thư mục | Nội dung | Key takeaways |
|---------|----------|---------------|
| `docs/raw/ideas/` | SPEC chính, proposals từ Claude Code/Codex | 7 vấn đề cốt lõi, hướng upgrade v3.0 |
| `docs/raw/research/` | Validation patterns, YAML conventions, refinement loop | Hermes validator system, frontmatter schema |
| `docs/raw/designs/` | Architecture design, install target resolution, state machine | Hermes-native conventions, 6 operation workflows |
| `docs/raw/brainstorm/` | Migration strategy, testing strategy, future extensions | Rollback plan, test pyramid, roadmap |
| `docs/rebuild-skill-suite-remediation-guide.md` | Checklist P0/P1/P2 issues | Cách xử lý chi tiết từng vấn đề |
| `skills/raw/prompt-cleaner/` | Prompt patterns cho Claude Code/Codex | Cách giao tiếp với external agents |

---

## CÁC VẤN ĐỀ CẦN XỬ LÝ

### P0 — CRITICAL

#### P0-01: Shared Framework Path Resolution

**Vấn đề:** 3 skill boot fail vì reference `../_shared/knowledge/framework.md` không resolve đúng từ skill install path.

**Hướng xử lý:**
1. Kiểm tra _shared/knowledge/framework.md tồn tại
2. Nếu không → trigger init_context.py để extract từ references/_shared.zip
3. Đổi references trong SKILL.md (Tier 1) thành: `../_shared/knowledge/framework.md`
4. Đổi references trong knowledge/*.md (Tier 2) thành: `../../_shared/knowledge/framework.md`

**Tiêu chí đạt:**
- Từ skill-architect/SKILL.md, path `../_shared/knowledge/framework.md` tồn tại
- Từ skill-planner/knowledge/architect.md, path `../../_shared/knowledge/framework.md` tồn tại
- Copy toàn bộ package sang /tmp/test-skill/ vẫn resolve đúng

**Source:** rebuild-skill-suite-remediation-guide.md Section P0-01

---

#### P0-02: Hardcode `.claude/skills` trong Runtime Instructions

**Vấn đề:** SKILL.md đang hướng agent đọc file từ `.claude/skills/...`, nhưng package có thể nằm ở bất kỳ `skills_root` nào.

**Hướng xử lý:**
1. Thay tất cả `@.claude/skills/...` bằng relative path từ skill root
2. Ví dụ: `@.claude/skills/skill-builder/knowledge/build-guidelines.md` → `knowledge/build-guidelines.md`
3. Với shared files: `../_shared/knowledge/framework.md`
4. Section install target examples chỉ để minh họa, không phải runtime contract

**Tiêu chí đạt:**
- Không còn `@.claude/skills` trong runtime boot instructions
- Không còn `.agent/skills` trong artifact contracts
- Chỉ còn `.claude/skills` như ví dụ install, không phải path bắt buộc

**Source:** rebuild-skill-suite-remediation-guide.md Section P0-02

---

### P1 — HIGH PRIORITY

#### P1-01: Tách Shared Contract vs Skill-Specific Knowledge

**Vấn đề:** 3 skill có `knowledge/architect.md` lặp lại framework chung → nguy cơ lệch version.

**Hướng xử lý:**
1. `_shared/knowledge/framework.md` giữ: 7 Zones, Pipeline flow, Zone Mapping Contract, Trace tag standard, Handoff quality gates
2. skill-*/knowledge/architect.md chỉ giữ: Skill-specific workflow, link đến framework.md khi cần

**Tiêu chí đạt:**
- Khi Zone Mapping format đổi, chỉ sửa framework.md + validators liên quan
- knowledge/architect.md không tự định nghĩa bảng chung theo cách khác

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-01

---

#### P1-02: Handoff Validators

**Vấn đề:** Architect → Planner và Planner → Builder chưa có kiểm chứng deterministic.

**Hướng xử lý:**
1. validate_skill.py (Builder validator):
   - Nhận thêm `--design` flag
   - Parse expected files từ design.md §3 Zone Mapping
   - Check mỗi expected file có ít nhất một task trace [TỪ DESIGN §3]
   - Check [CẦN LÀM RÕ] không còn blocker unresolved

2. validate-todo.py (Planner validator):
   - Nhận thêm `--design` flag
   - Parse expected files từ design.md §3
   - Check dependencies trỏ tới task IDs hợp lệ
   - Validate trace tags: chỉ 4 tags chuẩn được dùng

3. handoff_validator.py (mới - shared):
   - Check design.md frontmatter tồn tại và valid
   - Check §3 Zone Mapping có files cụ thể (không placeholder)
   - Check §7 phân biệt Tier 1 và Tier 2

**Tiêu chí đạt:**
- Bad design.md fail trước khi Planner viết plan
- Bad todo.md fail trước khi Builder build
- Có fixtures tốt/xấu cho từng validator

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-02

---

#### P1-03: Chuẩn hóa Feedback Loop

**Vấn đề:** Builder phát hiện lỗi design/todo nhưng không có đường report ngược chính thức.

**Hướng xử lý:**
1. Chuẩn hóa section trong build-log.md:

```
## Upstream Feedback
| ID | Type | Blocks Build? | Source | Issue | Required Upstream Action | Status |
|---|---|---|---|---|---|---|
| FB-001 | DESIGN | yes | design.md §3 | ... | Architect revise §3 | OPEN |
```

2. Chuẩn hóa status enum:
   - READY_FOR_BUILD
   - BLOCKED_BY_DESIGN
   - BLOCKED_BY_PLAN
   - BLOCKED_BY_RESOURCES
   - BUILT_WITH_WARNINGS
   - COMPLETE

3. Builder rule: Nếu Blocks Build? = yes → stop build, ghi feedback

4. Planner rule: Section "## 6. Builder Feedback Integration" là required nếu có feedback

**Tiêu chí đạt:**
- Builder có thể report ngược mà không freelancing
- Planner/Architect biết chính xác section nào cần sửa
- Validator fail nếu feedback blocker còn OPEN mà status COMPLETE

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-03

---

#### P1-04: Chuẩn hóa Trace Tags

**Vấn đề:** Nhiều biến thể tag → validator/agent hiểu khác nhau.

**Hướng xử lý:**
1. 4 tags CHUẨN (bắt buộc):
   - [TỪ DESIGN §N] — derived từ design.md section N
   - [TỪ AUDIT TÀI NGUYÊN] — generated vì resource thiếu
   - [GỢI Ý BỔ SUNG] — Planner suggest, không trong design
   - [CẦN LÀM RÕ] — cần user/Architect/Planner làm rõ

2. Legacy tags → warning/fail:
   - [GỢI Ý] → fail
   - [TỪ AUDIT] → fail
   - [TỪ AUDIT CUSTOM] → fail
   - [CẦU LÀM RÕ] → fail (typo)

3. Validator check: trace_validator.py parse và validate tags, unknown tag → warning + reject

**Tiêu chí đạt:**
- Repo search không còn tag legacy trong runtime files
- validate-todo.py fail với unknown tag
- Builder scan đúng [CẦN LÀM RÕ]

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-04

---

#### P1-05: Sửa Typo Clarification Blocker

**Vấn đề:** Builder scan sai `[CẦN LÀM RÕ]` thay vì `[CẦN LÀM RÕ]`.

**Hướng xử lý:**
1. Replace trong: skill-builder/SKILL.md, skill-builder/knowledge/architect.md
2. Thêm validator check legacy typo

**Tiêu chí đạt:**
- Không còn [CẦU LÀM RÕ]
- Nếu todo.md có [CẦN LÀM RÕ], Builder phải dừng ở Phase 2 CLARIFY

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-05

---

#### P1-06: Đồng bộ Section Contracts

**Vấn đề:** Planner SKILL.md dòng 109 nói "exactly 5 sections" nhưng dòng 153-171 định nghĩa 6 sections.

**Hướng xử lý:**
1. design.md: 12 top-level sections (§1-§12)
2. todo.md: 6 sections chính thức:
   - ## 1. Pre-requisites
   - ## 2. Phase Breakdown
   - ## 3. Knowledge & Resources Needed
   - ## 4. Definition of Done
   - ## 5. Notes
   - ## 6. Builder Feedback Integration

3. Cập nhật đồng bộ: SKILL.md, templates/todo.md.template, loop/plan-checklist.md, scripts/validate-todo.py

**Tiêu chí đạt:**
- design.md.template, design-checklist.md, skill-architect/SKILL.md thống nhất số section
- todo.md.template, validate-todo.py, skill-planner/SKILL.md thống nhất 6 sections

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-06

---

#### P1-07: Sửa Validators Đáng Tin

**Vấn đề:** Validator hiện tại có false positive/false negative.

**Hướng xử lý:**
1. validate_skill.py:
   - Không bắt cứng ## Persona; check "Persona" có thể là heading hoặc field
   - Regex file path phải match multi-extension: `([^`]+)`
   - Bỏ scan __pycache__ và generated files
   - Thêm --todo flag để cross-reference

2. validate-todo.py:
   - Parse markdown table thật (không chỉ regex toàn file)
   - Validate Priority enum trong cột table
   - Validate dependencies trỏ tới task IDs hợp lệ
   - Validate trace tags: chỉ 4 tags chuẩn

3. Thêm fixtures:
   - tests/fixtures/valid-design.md
   - tests/fixtures/invalid-design-missing-zone-column.md
   - tests/fixtures/valid-todo.md
   - tests/fixtures/invalid-todo-bad-dependency.md

**Tiêu chí đạt:**
- Validator pass fixture tốt
- Validator fail fixture xấu với message rõ
- Validator không fail skill-builder vì "## Persona" giả định sai

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-07

---

#### P1-08: Dynamic Context/Output Resolution

**Vấn đề:** Builder dùng relative path không ổn định cho .skill-context và output skill package.

**Hướng xử lý:**
1. Scripts nhận tham số rõ:
   - `--project-root <path>`
   - `--context-dir <path>`
   - `--skills-root <path>`

2. Default resolution:
   - project_root = cwd hoặc ancestor có .skill-context/
   - context_dir = project_root/.skill-context/{skill-name}
   - skills_root = parent(current_skill_dir) hoặc user-provided

3. SKILL.md hướng dẫn agent: Nếu user không chỉ định output root → hỏi hoặc dùng skills_root của bộ 3

**Tiêu chí đạt:**
- Chạy từ project A vẫn đọc .skill-context của project A
- Install bộ skill ở project B không ảnh hưởng context project A
- Có smoke test copy package sang /tmp/... và vẫn resolve đúng

**Source:** rebuild-skill-suite-remediation-guide.md Section P1-08

---

### P2 — MEDIUM PRIORITY

#### P2-01: Giảm Front-Load, Giữ Progressive Disclosure

**Vấn đề:** 3 SKILL.md yêu cầu đọc quá nhiều thư mục trước khi làm việc.

**Hướng xử lý:**
1. Boot chỉ đọc: SKILL.md + ../_shared/knowledge/framework.md (Tier 1 mandatory)
2. Templates/checklists chỉ đọc ở phase cần
3. SKILL.md dùng one-level links trực tiếp tới file cần đọc

**Tiêu chí đạt:**
- Không còn directive "đọc toàn bộ knowledge/templates/scripts/loop trước khi bắt đầu"
- Mọi bundled resource có link trực tiếp từ SKILL.md ở phase cần dùng
- SKILL.md vẫn dưới 500 lines

**Source:** rebuild-skill-suite-remediation-guide.md Section P2-01

---

#### P2-02: Hoàn thiện data/ Zone End-to-End

**Vấn đề:** data/ được định nghĩa nhưng chưa đồng bộ từ Architect → Planner → Builder.

**Hướng xử lý:**
1. init_context.py tạo optional directories: resources/, data/, loop/
2. design.md.template mindmap thêm data
3. Planner có task template cho Data zone: tạo data/*.yaml/json theo §3
4. Builder validator parse và check data/* expected files

**Tiêu chí đạt:**
- Nếu design §3 có data/schema.json → Planner tạo task tương ứng
- Builder tạo/check file data/schema.json
- Build-log Resource Usage Matrix có trace cho data critical files

**Source:** rebuild-skill-suite-remediation-guide.md Section P2-02

---

#### P2-03: Đồng bộ Templates

**Vấn đề:** Templates có nhưng chưa được tích hợp đều vào workflow.

**Hướng xử lý:**
1. Architect: Reference templates/design.md.template tại phase ghi design
2. Planner: Dùng templates/todo.md.template + resource-document.md.template
3. Builder: Dùng loop/build-log.md.template để tạo/hoàn thiện build-log
4. Xóa hoặc di chuyển template không dùng khỏi deployable package

**Tiêu chí đạt:**
- Mỗi template có ít nhất một runtime reference từ SKILL.md
- Không có template mồ côi trừ khi ghi rõ là example/non-runtime

**Source:** rebuild-skill-suite-remediation-guide.md Section P2-03

---

#### P2-04: Dọn Package Artifacts

**Vấn đề:** Source chứa __pycache__ và stale build-log.

**Hướng xử lý:**
1. Remove __pycache__/ khỏi source package
2. Chuyển stale loop/build-log.md thành template hoặc xóa khỏi runtime
3. Thêm ignore/package rule cho generated artifacts

**Tiêu chí đạt:**
- Package sạch, không có __pycache__
- Không stale artifacts

**Source:** rebuild-skill-suite-remediation-guide.md Section P2-04

---

## PHASE BREAKDOWN

### Phase 1: Foundation (P0 Fixes)

**Mục tiêu:** Fix critical path issues để bộ 3 skill có thể boot và resolve đúng.

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 1.1 | Verify _shared/knowledge/framework.md tồn tại | Tại skills/rebuild/_shared/ |
| 1.2 | Update skill-architect/SKILL.md: ../_shared/knowledge/framework.md | Path resolve đúng |
| 1.3 | Update skill-planner/SKILL.md: ../_shared/knowledge/framework.md | Path resolve đúng |
| 1.4 | Update skill-builder/SKILL.md: ../_shared/knowledge/framework.md | Path resolve đúng |
| 1.5 | Update skill-*/knowledge/*.md: ../../_shared/knowledge/framework.md | Path resolve đúng |
| 1.6 | Search toàn bộ SKILL.md cho @.claude/skills, .claude/skills | Không còn hardcode |
| 1.7 | Replace bằng relative paths | Runtime instructions sạch |
| 1.8 | Test: copy package sang /tmp/test/, resolve vẫn đúng | Portable verified |

---

### Phase 2: Contract & Validation (P1 Fixes)

**Mục tiêu:** Chuẩn hóa contracts giữa các stage và improve validators.

#### P1-01: Shared vs Specific

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 2.1 | Verify _shared/knowledge/framework.md giữ: 7 Zones, Pipeline, Naming, Anti-hallucination, Quality Gates | Không lặp trong skill-specific |
| 2.2 | Update skill-*/knowledge/architect.md: chỉ giữ workflow riêng, link đến framework.md | Skill-specific rõ ràng |

#### P1-02: Handoff Validators

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 2.3 | Update validate-todo.py: nhận --design flag | Parse §3 Zone Mapping |
| 2.4 | Update validate_skill.py: nhận --todo flag | Cross-reference check |
| 2.5 | Create handoff_validator.py (shared) | Check frontmatter + §3 |
| 2.6 | Parse markdown table thật (không regex toàn file) | Validate dependencies |
| 2.7 | Add fixtures: valid-design.md, invalid-design-missing-zone.md, valid-todo.md, invalid-todo-bad-dependency.md | Test coverage |

#### P1-03: Feedback Loop

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 2.8 | Update build-log.md.template: Upstream Feedback section format | FB-001 format |
| 2.9 | Define status enum | Enum complete |
| 2.10 | Update skill-builder/SKILL.md: Builder feedback reporting rules | Stop if blocks build |
| 2.11 | Update skill-planner/SKILL.md: Section 6 Builder Feedback Integration required | Required section |

#### P1-04: Trace Tags

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 2.12 | Update _shared/knowledge/framework.md: ghi rõ 4 tags chuẩn | Documented |
| 2.13 | Update skill-planner/SKILL.md: trace tag rules | Enforce |
| 2.14 | Update skill-builder/SKILL.md: scan tags rules | Scan correct |
| 2.15 | Fix typo [CẦU LÀM RÕ] → [CẦN LÀM RÕ] | Fixed everywhere |
| 2.16 | Update trace_validator.py: fail unknown/legacy tags | Reject |

#### P1-06: Section Contracts

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 2.17 | Confirm design.md = 12 sections (§1-§12) | Spec aligned |
| 2.18 | Confirm todo.md = 6 sections (Section 1-6) | Spec aligned |
| 2.19 | Update skill-architect/SKILL.md output spec | 12 sections |
| 2.20 | Update skill-planner/SKILL.md output spec (fix 5 vs 6 sections) | 6 sections |
| 2.21 | Sync templates: design.md.template, todo.md.template | Match specs |
| 2.22 | Sync loop checklists: design-checklist.md, plan-checklist.md | Match specs |

#### P1-07: Validator Accuracy

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 2.23 | Fix validate_skill.py: parse markdown table thật | No regex toàn file |
| 2.24 | Fix validate_skill.py: don't assume ## Persona | Check field content |
| 2.25 | Fix validate_skill.py: bỏ scan __pycache__ | Clean scan |
| 2.26 | Fix validate-todo.py: validate Priority enum | Enum check |
| 2.27 | Fix validate-todo.py: validate trace tags | 4 tags only |

---

### Phase 3: Portability & Dynamic Resolution

**Mục tiêu:** Bộ 3 skill portable và dynamic context resolution.

#### P1-08: Dynamic Resolution

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 3.1 | Update init_context.py: nhận --project-root, --context-dir, --skills-root | All flags present |
| 3.2 | Update validate_skill.py: dynamic path resolution | From any cwd |
| 3.3 | Update validate-todo.py: dynamic path resolution | From any cwd |
| 3.4 | Update SKILL.md boot: cwd detection, skills_root detection | Auto-detect |

#### P2-01: Reduce Front-Load

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 3.5 | Audit SKILL.md boot: đọc bao nhiêu files trước khi làm việc | Under 5 files |
| 3.6 | Move non-essential references sang Tier 2 | Tiered loading |
| 3.7 | Verify SKILL.md vẫn dưới 500 lines | Under 500 |

#### P2-02: Data Zone End-to-End

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 3.8 | Update init_context.py: tạo data/ directory | Created |
| 3.9 | Update design.md.template: mindmap data zone | Documented |
| 3.10 | Update skill-planner: task template cho Data zone | Task created |
| 3.11 | Update Builder validator: check data/* files | Validated |

#### P2-03: Template Integration

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 3.12 | Audit templates: mỗi template có runtime reference? | All referenced |
| 3.13 | Remove orphan templates hoặc đánh dấu non-runtime | Clean package |
| 3.14 | Update SKILL.md references | References sync |

#### P2-04: Clean Artifacts

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 3.15 | Remove __pycache__/ | Zero __pycache__ |
| 3.16 | Remove stale build-log.md (nếu historical log) | Clean |
| 3.17 | Add .gitignore cho generated artifacts | Generated ignored |

---

### Phase 4: Testing & Validation

**Mục tiêu:** Verify toàn bộ system hoạt động đúng.

#### Unit Tests

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 4.1 | validate_design_schema.py: section count, frontmatter valid | Pass/fail correct |
| 4.2 | validate_todo_schema.py: 6 sections, trace tags | Pass/fail correct |
| 4.3 | trace_validator.py: 4 tags chuẩn, legacy fail | Reject legacy |
| 4.4 | Run: pytest tests/unit/ -v | 90% coverage |

#### Integration Tests

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 4.5 | architect_to_planner.py: design.md → todo.md handoff | Contract valid |
| 4.6 | planner_to_builder.py: todo.md → skill-package handoff | Contract valid |
| 4.7 | Run: pytest tests/integration/ -v | 100% happy path |

#### Smoke Tests

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 4.8 | test_architect_analyze: sample requirement → design.md | Output correct |
| 4.9 | test_planner_plan: design.md → todo.md | Output correct |
| 4.10 | test_builder_build: design.md + todo.md → skill package | Output correct |
| 4.11 | Run: pytest tests/smoke/ -v | All pass |

#### Portable Test

| # | Task | Tiêu chí đạt |
|---|------|-------------|
| 4.12 | Copy package sang /tmp/portable-test/ | Copied |
| 4.13 | Run smoke tests từ /tmp/ | Pass |
| 4.14 | Verify shared framework resolve đúng | Resolve OK |

---

## DELEGATION PLAN

### Claude Code Tasks (skill-architect + skill-planner focus)

| # | Task | P0/P1/P2 | Input Files |
|---|------|----------|-------------|
| C1 | Fix P0-01, P0-02 (Foundation) | P0 | skill-architect/SKILL.md, skill-planner/SKILL.md, _shared/knowledge/framework.md |
| C2 | Fix P1-01, P1-06 (Section Contracts) | P1 | skill-architect/SKILL.md, skill-planner/SKILL.md, templates/ |
| C3 | Phase 3.1 + 3.2 (Portability + Front-Load) | P1-08, P2-01 | init_context.py, SKILL.md boot sequence |
| C4 | Phase 3.3 (Data Zone) | P2-02 | init_context.py, design.md.template, skill-planner/ |

### Codex Tasks (skill-builder + validators focus)

| # | Task | P0/P1/P2 | Input Files |
|---|------|----------|-------------|
| X1 | Fix P1-02 (Handoff Validators) | P1-02 | validate-todo.py, validate_skill.py, handoff_validator.py, fixtures/ |
| X2 | Fix P1-03 + P1-04 (Feedback + Trace Tags) | P1-03, P1-04 | skill-builder/SKILL.md, build-log.md.template, trace_validator.py |
| X3 | Phase 3.3 (Data Zone - Builder) | P2-02 | Builder validator, data/* handling |
| X4 | P2-04 (Clean Artifacts) | P2-04 | __pycache__ removal |

---

## FILE REFERENCE MAP

| File | Role | Key Changes |
|------|------|-------------|
| skill-architect/SKILL.md | Architect skill | P0-01, P0-02, P1-06, P2-01 |
| skill-planner/SKILL.md | Planner skill | P0-01, P0-02, P1-06, P2-01 |
| skill-builder/SKILL.md | Builder skill | P0-01, P0-02, P1-03, P1-04, P1-05 |
| _shared/knowledge/framework.md | Shared foundation | P1-01, P1-04 |
| _shared/validators/validate_skill.py | Builder validator | P1-02, P1-07 |
| skill-planner/scripts/validate-todo.py | Planner validator | P1-02, P1-07 |
| _shared/validators/handoff_validator.py | Handoff validator (NEW) | P1-02 |
| _shared/validators/trace_validator.py | Trace tag validator | P1-04 |
| _shared/schemas/design.schema.yaml | Design schema | P1-02, P1-06 |
| _shared/schemas/todo.schema.yaml | Todo schema | P1-02, P1-06 |
| _shared/templates/feedback.yaml.template | Feedback template | P1-03 |
| _shared/fixtures/good/*.md | Good fixtures | P1-02, P1-07 |
| _shared/fixtures/bad/*.md | Bad fixtures | P1-02, P1-07 |
| skill-architect/scripts/init_context.py | Context init | P1-08, P2-02 |
| skill-architect/templates/design.md.template | Design template | P1-06, P2-03 |
| skill-planner/templates/todo.md.template | Todo template | P1-06, P2-03 |
| skill-builder/loop/build-log.md.template | Build log template | P1-03 |

---

## DEPENDENCY GRAPH

```
P0-01, P0-02 (Foundation)
     ↓
P1-01, P1-06 (Section Contracts)
     ↓
P1-02, P1-03, P1-04, P1-05, P1-07 (Validation & Feedback)
     ↓
P1-08, P2-01, P2-02, P2-03, P2-04 (Portability & Polish)
     ↓
Phase 4: Testing & Validation
```

---

## CHECKLIST HOÀN THÀNH

### P0 Completion

- [ ] P0-01: Shared framework path resolve đúng từ mọi skill
- [ ] P0-02: Không còn .claude/skills hardcode trong runtime

### P1 Completion

- [ ] P1-01: Shared framework giữ 7 Zones + Pipeline, không lặp trong skill-specific
- [ ] P1-02: Validators nhận --design flag, pass/fail đúng fixtures
- [ ] P1-03: Feedback loop chuẩn hóa với FB-001 format và status enum
- [ ] P1-04: 4 trace tags chuẩn, legacy fail, typo fixed
- [ ] P1-05: [CẦU LÀM RÕ] → [CẦN LÀM RÕ] đã fix
- [ ] P1-06: design.md = 12 sections, todo.md = 6 sections, synced
- [ ] P1-07: Validators accurate, không false positive/negative
- [ ] P1-08: Dynamic resolution, copy sang /tmp/ vẫn đúng

### P2 Completion

- [ ] P2-01: Boot chỉ đọc Tier 1, SKILL.md < 500 lines
- [ ] P2-02: data/ zone sync Architect → Planner → Builder
- [ ] P2-03: Mỗi template có runtime reference từ SKILL.md
- [ ] P2-04: Package sạch, không __pycache__, không stale artifacts

### Testing Completion

- [ ] Unit tests: 90% coverage
- [ ] Integration tests: happy path 100%
- [ ] Smoke tests: all operation types pass
- [ ] Portable test: copy sang /tmp/ vẫn resolve đúng