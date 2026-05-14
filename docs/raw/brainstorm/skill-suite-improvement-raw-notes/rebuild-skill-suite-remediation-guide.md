# Hướng xử lý bộ 3 skill `skills/rebuild`

> Mục tiêu: biến `skill-architect`, `skill-planner`, `skill-builder` thành bộ 3 **mạnh, tự do, dynamic, portable**, có thể copy/install vào nhiều dự án, nhiều máy, nhiều người dùng mà vẫn resolve đúng kiến thức, context, validators, và handoff contracts.

---

## 1. Nguyên tắc thiết kế bắt buộc

### 1.1 Portable by default

Bộ 3 không được phụ thuộc vào path cụ thể như:

- `/home/...`
- repo hiện tại `deep_work_by_steve`
- `.claude/skills`
- `.agent/skills`
- `skills/rebuild`

Thay vào đó phải dùng 2 root động:

| Root | Ý nghĩa | Cách xác định |
|---|---|---|
| `skills_root` | nơi install/copy bộ skills | parent của `skill-architect/`, `skill-planner/`, `skill-builder/` |
| `project_root` | dự án mà user đang dùng skill để tạo skill mới | cwd hoặc thư mục tìm thấy `.skill-context/` |

### 1.2 Shared foundation là sibling package

Layout portable chuẩn:

```text
<skills-root>/
├── _shared/knowledge/framework.md
├── skill-architect/SKILL.md
├── skill-planner/SKILL.md
└── skill-builder/SKILL.md
```

Path chuẩn:

| File đang đọc | Path tới shared framework |
|---|---|
| `skill-*/SKILL.md` | `../_shared/knowledge/framework.md` |
| `skill-*/knowledge/*.md` | `../../_shared/knowledge/framework.md` |
| `skill-*/scripts/*.py` | resolve bằng `Path(__file__)`, không hardcode |

### 1.3 Context project tách khỏi install path

`.skill-context/{skill-name}` là artifact của **project đang làm việc**, không phải artifact của thư mục install skill.

Quy tắc:

```text
project_root/.skill-context/{skill-name}/
├── design.md
├── todo.md
├── build-log.md
├── resources/
├── data/
└── loop/
```

Không dùng `../../.skill-context` từ skill install path để suy ra context.

### 1.4 Tự do nhưng có contract

Bộ 3 có thể tự do phản biện, hỏi lại, hoặc đề xuất bổ sung, nhưng mọi tự do phải được đánh dấu bằng nguồn:

| Tag chuẩn | Nghĩa | Ai dùng |
|---|---|---|
| `[TỪ DESIGN §N]` | lấy trực tiếp từ `design.md` section N | Planner, Builder |
| `[TỪ AUDIT TÀI NGUYÊN]` | sinh từ audit `resources/`/`data/` thiếu hoặc mỏng | Planner |
| `[GỢI Ý BỔ SUNG]` | đề xuất hữu ích nhưng không có trong design | Planner, Builder |
| `[CẦN LÀM RÕ]` | blocker cần user/Architect/Planner làm rõ | Planner, Builder |

Không dùng biến thể khác.

---

## 2. Hướng xử lý theo issue

### P0-01 — Sửa shared framework path

**Xử lý vấn đề gì:** 3 skill boot fail vì reference shared framework ở path không tồn tại trong `skills/rebuild`.

**Lý do:** Shared framework là nguồn sự thật cho 7 Zones, pipeline, naming, anti-hallucination. Nếu boot không đọc được file này thì bộ 3 mất nền chung.

**Cách xử lý:**

1. Thêm shared package vào bản rebuild:

   ```text
   skills/rebuild/_shared/knowledge/framework.md
   ```

   Nguồn ban đầu có thể copy từ:

   ```text
   skills/raw/_shared/knowledge/framework.md
   ```

2. Đổi references trong 3 `SKILL.md`:

   ```text
   ../../_shared/knowledge/framework.md
   ```

   thành:

   ```text
   ../_shared/knowledge/framework.md
   ```

3. Giữ references trong `knowledge/*.md` là:

   ```text
   ../../_shared/knowledge/framework.md
   ```

   vì các file này nằm sâu thêm 1 cấp.

**Tiêu chí đạt:**

- Từ mỗi `skill-*/SKILL.md`, path `../_shared/knowledge/framework.md` tồn tại.
- Từ mỗi `skill-*/knowledge/architect.md`, path `../../_shared/knowledge/framework.md` tồn tại.
- Copy toàn bộ `skills/rebuild` sang thư mục tạm bất kỳ vẫn resolve được shared framework.

---

### P0-02 — Gỡ hardcode `.claude/skills` khỏi runtime instructions

**Xử lý vấn đề gì:** SKILL.md đang hướng agent đọc file từ `.claude/skills/...`, nhưng package source có thể nằm ở bất kỳ `skills_root` nào.

**Lý do:** Bộ 3 cần mang đi dùng nhiều nơi; `.claude/skills` chỉ là một install target, không phải contract runtime.

**Cách xử lý:**

1. Trong 3 `SKILL.md`, thay các dòng dạng:

   ```text
   @.claude/skills/skill-builder/knowledge/build-guidelines.md
   ```

   bằng path tương đối từ skill root:

   ```markdown
   [knowledge/build-guidelines.md](knowledge/build-guidelines.md)
   ```

2. Với shared file, dùng:

   ```markdown
   [../_shared/knowledge/framework.md](../_shared/knowledge/framework.md)
   ```

3. Nếu cần nói về install target, chuyển sang section riêng kiểu:

   ```text
   Install target examples: .claude/skills, ~/.codex/skills, or any custom skills_root.
   Runtime instructions must not depend on a specific target.
   ```

**Tiêu chí đạt:**

- Không còn `@.claude/skills` trong runtime boot/progressive disclosure instructions.
- Không còn `.agent/skills` trong artifact contracts.
- Chỉ còn nhắc `.claude/skills` như ví dụ install, không phải path bắt buộc.

---

### P1-01 — Tách shared contract và skill-specific knowledge

**Xử lý vấn đề gì:** 3 `knowledge/architect.md` lặp lại framework chung và có nguy cơ lệch.

**Lý do:** Shared rule chỉ nên có một nguồn. Skill-specific file chỉ nên chứa workflow riêng của từng stage.

**Cách xử lý:**

1. Trong `_shared/knowledge/framework.md`, giữ các nội dung chung:
   - 7 Zones.
   - Pipeline flow.
   - Zone Mapping Contract.
   - Trace tag standard.
   - Context directory contract.
   - Handoff quality gates.
2. Trong từng `knowledge/architect.md`, chỉ giữ:
   - Architect workflow riêng.
   - Planner workflow riêng.
   - Builder workflow riêng.
3. Nếu cần nhắc lại bảng chung, chỉ tóm tắt và link shared file.

**Tiêu chí đạt:**

- Khi Zone Mapping format đổi, chỉ cần sửa `_shared/knowledge/framework.md` và templates/validators liên quan.
- `knowledge/architect.md` không tự định nghĩa lại bảng chung theo cách khác.

---

### P1-02 — Thêm handoff validators

**Xử lý vấn đề gì:** Architect -> Planner và Planner -> Builder chưa có kiểm chứng deterministic.

**Lý do:** Bộ skill tự do cần guardrail mạnh để không hallucinate hoặc bỏ sót file/task khi handoff.

**Cách xử lý:**

1. Tạo/sửa validator cho `design.md`:
   - Check section bắt buộc.
   - Parse `§3 Zone Mapping`.
   - Validate cột: `Zone`, `Files cần tạo`, `Nội dung`, `Bắt buộc?`.
   - Fail nếu file placeholder như `knowledge/xxx.md` còn tồn tại trong final design.
2. Nâng cấp `validate-todo.py`:
   - Nhận thêm `--design <design.md>`.
   - Parse expected files từ `design.md §3`.
   - Check mỗi expected file có ít nhất một task trace `[TỪ DESIGN §3]`.
   - Check dependencies trỏ tới task IDs hợp lệ.
3. Nâng cấp `validate_skill.py`:
   - Nhận thêm `--todo <todo.md>`.
   - Check task done/trace với file thực tế.
   - Check `[CẦN LÀM RÕ]` không còn blocker unresolved.

**Tiêu chí đạt:**

- Bad `design.md` fail trước khi Planner viết plan.
- Bad `todo.md` fail trước khi Builder build.
- Skill package thiếu file trong §3 fail validation.
- Có fixture tốt/xấu cho từng validator.

---

### P1-03 — Chuẩn hóa feedback loop

**Xử lý vấn đề gì:** Builder phát hiện lỗi design/todo nhưng không có đường report ngược chính thức.

**Lý do:** Bộ 3 cần tự do phản biện nhưng phải biết dừng đúng nơi và trả lỗi đúng upstream stage.

**Cách xử lý:**

1. Chuẩn hóa section trong `build-log.md`:

   ```markdown
   ## Upstream Feedback

   | ID | Type | Blocks Build? | Source | Issue | Required Upstream Action | Status |
   |---|---|---|---|---|---|---|
   | FB-001 | DESIGN | yes | design.md §3 | ... | Architect revise §3 | OPEN |
   ```

2. Chuẩn hóa status:
   - `READY_FOR_BUILD`
   - `BLOCKED_BY_DESIGN`
   - `BLOCKED_BY_PLAN`
   - `BLOCKED_BY_RESOURCES`
   - `BUILT_WITH_WARNINGS`
   - `COMPLETE`
3. Builder rule:
   - Nếu `Blocks Build? = yes`, stop build, ghi feedback, không tự ý sửa upstream artifact trừ khi được giao rõ.
4. Planner rule:
   - Section `## 6. Builder Feedback Integration` là required nếu có feedback, và phải ghi cách resolve.

**Tiêu chí đạt:**

- Builder có thể report ngược mà không freelancing.
- Planner/Architect biết chính xác section nào cần sửa.
- Validator fail nếu feedback blocker còn `OPEN` mà status lại `COMPLETE`.

---

### P1-04 — Chuẩn hóa trace tags

**Xử lý vấn đề gì:** Nhiều biến thể tag gây validator/agent hiểu khác nhau.

**Lý do:** Trace tag là xương sống chống hallucination. Dynamic user càng nhiều thì tag càng phải ít và rõ.

**Cách xử lý:**

1. Đưa 4 tag chuẩn vào `_shared/knowledge/framework.md`.
2. Sửa toàn bộ SKILL.md, templates, checklists, validators chỉ dùng 4 tag này:
   - `[TỪ DESIGN §N]`
   - `[TỪ AUDIT TÀI NGUYÊN]`
   - `[GỢI Ý BỔ SUNG]`
   - `[CẦN LÀM RÕ]`
3. Validator warning/fail khi gặp tag legacy:
   - `[GỢI Ý]`
   - `[TỪ AUDIT]`
   - `[TỪ AUDIT CUSTOM]`
   - `[CẦU LÀM RÕ]`

**Tiêu chí đạt:**

- Repo search không còn tag legacy trong runtime files.
- `validate-todo.py` fail với unknown tag.
- Builder scan đúng `[CẦN LÀM RÕ]`.

---

### P1-05 — Sửa typo clarification blocker

**Xử lý vấn đề gì:** Builder scan sai `[CẦU LÀM RÕ]` thay vì `[CẦN LÀM RÕ]`.

**Lý do:** Đây là lỗi nhỏ nhưng nguy hiểm vì có thể làm Builder bỏ qua blocker.

**Cách xử lý:**

1. Replace trong:
   - `skill-builder/SKILL.md`
   - `skill-builder/knowledge/architect.md`
2. Thêm validator check legacy typo.

**Tiêu chí đạt:**

- Không còn `[CẦU LÀM RÕ]`.
- Nếu `todo.md` có `[CẦN LÀM RÕ]`, Builder phải dừng ở Phase 2 CLARIFY.

---

### P1-06 — Đồng bộ section contracts

**Xử lý vấn đề gì:** Planner nói exactly 5 sections nhưng lại có section 6; Architect nói 10 sections nhưng có §10.1/§11/§12.

**Lý do:** Artifact schema không ổn định thì validator và handoff không đáng tin.

**Cách xử lý:**

1. Chọn contract rõ:
   - `design.md` dùng 12 top-level sections, hoặc 10 top-level + optional appendix. Khuyến nghị: **12 top-level sections** nếu §11/§12 thật sự bắt buộc.
   - `todo.md` dùng **6 sections**, trong đó section 6 là feedback integration.
2. Cập nhật đồng bộ:
   - SKILL.md.
   - templates.
   - checklists.
   - validators.
3. Không dùng cụm "exactly" nếu còn extension optional. Dùng "must contain these sections at minimum" hoặc định nghĩa rõ optional.

**Tiêu chí đạt:**

- `design.md.template`, `design-checklist.md`, `skill-architect/SKILL.md` thống nhất số section.
- `todo.md.template`, `validate-todo.py`, `skill-planner/SKILL.md` thống nhất số section.

---

### P1-07 — Sửa validators để đáng tin

**Xử lý vấn đề gì:** Validator hiện tại có false positive/false negative.

**Lý do:** Bộ 3 càng tự do thì validation càng phải chắc.

**Cách xử lý:**

1. `validate_skill.py`:
   - Không bắt cứng `## Persona`; check `Persona` có thể là heading hoặc field rõ trong Mission.
   - Regex file path phải match extension dài và multi-extension:

     ```python
     r"`([^`]+)`"
     ```

     rồi filter path hợp lệ bằng parser riêng.
   - Bỏ scan `__pycache__` và generated files.
   - Thêm `--todo`.
2. `validate-todo.py`:
   - Parse markdown table thật thay vì chỉ regex toàn file.
   - Validate enum Priority trong cột table.
   - Validate dependencies.
   - Validate trace tags.
3. Thêm fixtures:

   ```text
   tests/fixtures/valid-design.md
   tests/fixtures/invalid-design-missing-zone-column.md
   tests/fixtures/valid-todo.md
   tests/fixtures/invalid-todo-bad-dependency.md
   ```

**Tiêu chí đạt:**

- Validator pass fixture tốt.
- Validator fail fixture xấu với message rõ.
- Validator không fail chính skill-builder vì `## Persona` giả định sai.

---

### P1-08 — Dynamic context/output resolution

**Xử lý vấn đề gì:** Builder dùng relative path không ổn định cho `.skill-context` và output skill package.

**Lý do:** Khi mang skill sang project khác, install path và project path là hai khái niệm khác nhau.

**Cách xử lý:**

1. Scripts nhận tham số rõ:

   ```text
   --project-root <path>
   --context-dir <path>
   --skills-root <path>
   ```

2. Default:
   - `project_root = cwd` hoặc ancestor có `.skill-context/`.
   - `context_dir = project_root/.skill-context/{skill-name}`.
   - `skills_root = parent(current_skill_dir)` hoặc user-provided.
3. SKILL.md hướng dẫn agent:
   - Nếu user không chỉ định output root, hỏi hoặc dùng current `skills_root` của bộ 3.
   - Không hardcode `.claude/skills`.

**Tiêu chí đạt:**

- Chạy từ project A vẫn đọc `.skill-context` của project A.
- Install bộ skill ở project B không ảnh hưởng context project A.
- Có smoke test copy package sang `/tmp/...` và vẫn resolve đúng.

---

### P2-01 — Giảm front-load, giữ progressive disclosure

**Xử lý vấn đề gì:** 3 SKILL.md yêu cầu đọc quá nhiều thư mục trước khi làm việc.

**Lý do:** Portable skill cho nhiều người cần nhanh, tiết kiệm context, và không ép load file không cần.

**Cách xử lý:**

1. Boot chỉ đọc:
   - shared framework.
   - `knowledge/architect.md` riêng của skill.
2. Templates/checklists chỉ đọc ở phase cần:
   - Architect đọc `templates/design.md.template` khi ghi design.
   - Planner đọc `templates/resource-document.md.template` khi cần tạo nháp resource docs.
   - Builder đọc `loop/build-checklist.md` ở verify phase.
3. SKILL.md dùng one-level links trực tiếp tới file cần đọc.

**Tiêu chí đạt:**

- Không còn directive "đọc toàn bộ knowledge/templates/scripts/loop trước khi bắt đầu".
- Mọi bundled resource có link trực tiếp từ SKILL.md ở phase cần dùng.
- `SKILL.md` vẫn dưới 500 lines.

---

### P2-02 — Hoàn thiện `data/` zone end-to-end

**Xử lý vấn đề gì:** `data/` được định nghĩa nhưng chưa đồng bộ từ Architect -> Planner -> Builder.

**Lý do:** Dynamic skills thường cần config/schema/rules tĩnh; `data/` là zone quan trọng cho portability.

**Cách xử lý:**

1. `init_context.py` tạo optional directories:
   - `resources/`
   - `data/`
   - `loop/`
2. `design.md.template` mindmap thêm `data`.
3. Planner có task template cho `Data` zone:
   - tạo `data/*.yaml/json` theo §3.
   - audit data resources nếu cần.
4. Builder validator parse và check `data/*` expected files.

**Tiêu chí đạt:**

- Nếu design §3 có `data/schema.json`, Planner tạo task tương ứng.
- Builder tạo/check file `data/schema.json`.
- Build-log Resource Usage Matrix có trace cho data critical files.

---

### P2-03 — Đồng bộ templates

**Xử lý vấn đề gì:** Templates có nhưng chưa được tích hợp đều vào workflow.

**Lý do:** Templates giúp output ổn định giữa nhiều người dùng và nhiều dự án.

**Cách xử lý:**

1. Architect:
   - Reference `templates/design.md.template` tại phase ghi design.
2. Planner:
   - Dùng `todo.md.template` hoặc có own `templates/todo.md.template`.
   - Reference `resource-document.md.template` khi tạo/đề xuất resource docs.
3. Builder:
   - Dùng `build-log.md.template` để tạo/hoàn thiện build-log.
4. Xóa hoặc di chuyển template không dùng khỏi deployable package.

**Tiêu chí đạt:**

- Mỗi template có ít nhất một runtime reference từ SKILL.md.
- Không có template mồ côi trừ khi ghi rõ là example/non-runtime.

---

### P2-04 — Dọn package artifacts

**Xử lý vấn đề gì:** Source chứa pycache và stale build-log.

**Lý do:** Bộ skill mang đi nhiều nơi phải sạch, không chứa artifact cục bộ gây hiểu nhầm.

**Cách xử lý:**

1. Remove `__pycache__/` khỏi source package.
2. Chuyển stale `loop/build-log.md` thành template hoặc xóa khỏi runtime package nếu chỉ là historical log.
3. Thêm ignore/package rule cho generated artifacts.

**Tiêu chí đạt:**

- Không có `.pyc`, `__pycache__` trong deployable package.
- Build-log runtime không claim PASS stale.
- Validator không scan generated caches.

---

## 3. Thứ tự xử lý đề xuất

| Step | Việc làm | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo `_shared` trong `skills/rebuild` và sửa shared path | Boot đọc được framework |
| 2 | Gỡ hardcode `.claude/.agent` | Package portable |
| 3 | Sửa trace tags + typo clarification | Handoff không bỏ sót blocker |
| 4 | Đồng bộ section contracts/templates/checklists | Artifact schema ổn định |
| 5 | Nâng cấp validators + fixtures | Guardrails deterministic |
| 6 | Chuẩn hóa feedback loop | Builder report upstream rõ ràng |
| 7 | Dynamic context/output resolution | Dùng được nhiều project/install root |
| 8 | PD cleanup + data/template support | Token-efficient và full 7-zone |
| 9 | Dọn generated/stale artifacts | Package sạch để phân phối |
| 10 | Smoke test portable copy | Xác nhận mang đi tái sử dụng được |

---

## 4. Bộ tiêu chí nghiệm thu tổng thể

### 4.1 Static checks

- Không còn `@.claude/skills` trong runtime instructions.
- Không còn `.agent/skills` trong contracts/templates.
- Không còn `[CẦU LÀM RÕ]`, `[GỢI Ý]`, `[TỪ AUDIT]`, `[TỪ AUDIT CUSTOM]` trong runtime files.
- Không có `__pycache__`/`.pyc` trong deployable package.

### 4.2 Contract checks

- `design.md` template/checklist/SKILL.md cùng một schema.
- `todo.md` template/validator/SKILL.md cùng một schema.
- `build-log.md` template/validator/SKILL.md cùng một schema.
- Zone Mapping parse được và không chứa placeholder trong final artifact.

### 4.3 Dynamic portability checks

Thực hiện smoke test:

```text
1. Copy skills/rebuild -> /tmp/portable-skills
2. Invoke/read each SKILL.md from /tmp/portable-skills/<skill>
3. Verify each skill resolves ../_shared/knowledge/framework.md
4. Use a separate project cwd with .skill-context/demo-skill/
5. Run validators using explicit --project-root / --context-dir
6. Confirm no path points back to original repo
```

### 4.4 Behavioral checks

- Architect không deliver nếu Zone Mapping còn placeholder.
- Planner không mark complete nếu resources critical còn missing/thin.
- Builder dừng nếu todo còn `[CẦN LÀM RÕ]`.
- Builder không tạo file ngoài `design.md §3` nếu không có feedback/rationale rõ.
- Builder ghi `Upstream Feedback` khi design/todo conflict.

---

## 5. Definition of Done cho remediation

Remediation hoàn tất khi:

1. Bộ 3 có shared framework portable tại `_shared/knowledge/framework.md`.
2. Tất cả runtime path là relative/dynamic.
3. Handoff artifacts có schema thống nhất.
4. Validators pass/fail đúng trên fixtures.
5. Copy package sang một folder khác vẫn chạy smoke test thành công.
6. Không còn artifact cục bộ/stale trong package.
7. Tài liệu trong `temp.md` và guide này phản ánh đúng trạng thái cuối cùng sau sửa.
