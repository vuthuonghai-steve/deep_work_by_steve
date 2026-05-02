# Báo cáo xác minh bộ 3 skill `skills/rebuild`

> Cập nhật: 2026-05-02  
> Phạm vi xác minh: `skills/rebuild/` gồm **25 files** hiện có, đối chiếu thêm `skills/raw/_shared/knowledge/framework.md` vì đây là shared framework duy nhất tìm thấy trong repo.  
> Tài liệu xử lý chi tiết: [`docs/rebuild-skill-suite-remediation-guide.md`](docs/rebuild-skill-suite-remediation-guide.md)

---

## 0. Kết luận điều chỉnh so với bản phát hiện ban đầu

Phát hiện ban đầu đúng ở hướng chính: bộ 3 `skill-architect -> skill-planner -> skill-builder` có vấn đề nghiêm trọng về **path boot**, **shared foundation**, **handoff contract**, và **validator**.

Điểm cần chỉnh lại cho chính xác:

1. Không phải toàn repo không có `framework.md`. File có tồn tại tại:
   - `skills/raw/_shared/knowledge/framework.md`
2. Vấn đề thật sự là `skills/rebuild` không có `_shared/`, trong khi 3 skill trong `skills/rebuild` đều bắt đọc shared framework bằng path hiện không resolve được từ layout hiện tại.
3. Một số issue trong bản cũ bị nói quá mức:
   - `data/` zone không hoàn toàn thiếu support: Builder đã có đọc/coverage cho `data/`, nhưng Architect scaffold chưa tạo `data/`, Planner chưa có task template rõ cho `data/`.
   - Templates không hoàn toàn "không dùng": `init_context.py` có dùng 3 templates của Architect; vấn đề là integration giữa Planner/Builder và template contracts chưa đồng bộ.
4. Vì bộ 3 này cần **mạnh, tự do, portable, tái sử dụng nhiều dự án/người dùng**, nhóm vấn đề quan trọng nhất là **dynamic path contract**: không được hardcode `.claude/skills`, `.agent/skills`, hoặc relative path phụ thuộc vị trí repo hiện tại.

---

## 1. Pipeline hiện tại

```text
skill-architect  ->  skill-planner  ->  skill-builder
   design.md             todo.md          skill package
```

Artifacts chính:

| Stage | Skill | Input | Output |
|---|---|---|---|
| 1 | `skill-architect` | user requirements | `.skill-context/{skill-name}/design.md` |
| 2 | `skill-planner` | `design.md` | `.skill-context/{skill-name}/todo.md` |
| 3 | `skill-builder` | `design.md` + `todo.md` + resources | skill folder |

---

## 2. Các vấn đề đã xác minh

### P0-01 — Shared framework path bị gãy

**Trạng thái:** Confirmed  
**Mức độ:** P0  
**Confidence:** High

| Evidence | Ý nghĩa |
|---|---|
| `skills/rebuild/skill-architect/SKILL.md:82` | Boot bắt đọc `../../_shared/knowledge/framework.md` |
| `skills/rebuild/skill-planner/SKILL.md:61` | Boot bắt đọc `../../_shared/knowledge/framework.md` |
| `skills/rebuild/skill-builder/SKILL.md:70` | Phase 1 bắt đọc `../../_shared/knowledge/framework.md` |
| `skills/raw/_shared/knowledge/framework.md` | Shared framework có ở `raw`, nhưng không có ở `rebuild` |

**Vấn đề chính xác:** `framework.md` không tồn tại ở vị trí mà `skills/rebuild` đang reference. Nếu chạy bộ 3 từ `skills/rebuild`, boot có thể fail hoặc agent bỏ qua/hallucinate phần framework.

**Dynamic risk:** Khi copy bộ 3 sang dự án khác, lỗi này càng dễ xảy ra nếu không có layout portable chuẩn.

---

### P0-02 — Path hardcode `.claude/skills/...` không portable

**Trạng thái:** Confirmed  
**Mức độ:** P0/P1  
**Confidence:** High

| Evidence | Ý nghĩa |
|---|---|
| `skills/rebuild/skill-architect/SKILL.md:45` | Reference `@.claude/skills/skill-architect/knowledge/architect.md` |
| `skills/rebuild/skill-planner/SKILL.md:38-39` | Reference `@.claude/skills/skill-planner/...` |
| `skills/rebuild/skill-builder/SKILL.md:37-44` | Reference `@.claude/skills/skill-builder/...` |
| `.claude/` trong repo | Chỉ có `settings.local.json`, không có `.claude/skills/...` |

**Vấn đề:** Skill source nằm ở `skills/rebuild/...`, nhưng SKILL.md lại chỉ dẫn agent đọc từ `.claude/skills/...`. Điều này chỉ đúng nếu đã install vào đúng layout `.claude/skills`; không đúng khi bộ 3 được mang đi như một package source.

**Dynamic requirement:** Tài liệu và skill phải dùng path tương đối theo **skill install root**, không phụ thuộc tên repo, home path, hoặc `.claude` cụ thể.

---

### P1-01 — `knowledge/architect.md` có lặp shared contract và dễ lệch source-of-truth

**Trạng thái:** Confirmed một phần  
**Mức độ:** P1  
**Confidence:** Medium-High

3 file `knowledge/architect.md` là skill-specific, không phải duplicate 1:1:

| File | Nội dung riêng |
|---|---|
| `skill-architect/knowledge/architect.md` | Zone Mapping Contract, Design Output Sections, Architect workflow |
| `skill-planner/knowledge/architect.md` | Planner workflow, 3-tier analysis, anti-hallucination |
| `skill-builder/knowledge/architect.md` | Builder workflow, phase-driven build, context coverage |

**Vấn đề thật:** Các file này cùng nhắc shared framework và contract chung. Khi framework đổi, nhiều nơi phải sửa, dễ lệch.

**Hướng đúng:** Giữ file skill-specific, nhưng đưa contract chung về `_shared/knowledge/framework.md` và chỉ reference lại từ từng skill.

---

### P1-02 — Handoff contract chưa được validate end-to-end

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** High

**Architect -> Planner**

- Architect tạo `design.md` với `§3 Zone Mapping`.
- Planner đọc `Files cần tạo` từ §3.
- Nhưng không có validator bắt buộc kiểm tra schema/table của `design.md` trước khi Planner phân rã task.

**Planner -> Builder**

- Planner tạo `todo.md` với trace tags.
- Builder đọc `todo.md`.
- Nhưng `validate_skill.py` không verify trace tags/dependencies trong `todo.md`.

**Evidence:**

- `skills/rebuild/skill-planner/scripts/validate-todo.py` chỉ nhận `todo.md`, không nhận `design.md`.
- `skills/rebuild/skill-builder/scripts/validate_skill.py` có `--design`, nhưng không có `--todo` và không validate todo trace/dependencies.

---

### P1-03 — Feedback loop có ý tưởng nhưng chưa thành cơ chế

**Trạng thái:** Confirmed một phần  
**Mức độ:** P1  
**Confidence:** Medium-High

**Có tồn tại dấu hiệu feedback:**

- `skill-planner/SKILL.md:152` có `## 6. Builder Feedback Integration`.
- `validate-todo.py:117-122` có check optional section này.

**Thiếu:**

- Không có artifact chuẩn để Builder report ngược lại Planner/Architect.
- Không có status machine như `READY`, `BLOCKED_BY_DESIGN`, `BLOCKED_BY_PLAN`.
- Không có rule rõ: khi Builder thấy design/todo conflict thì dừng ở đâu, ghi gì, ai xử lý.

---

### P1-04 — Trace tag taxonomy không nhất quán

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** High

Các tag/biến thể đang cùng tồn tại:

- `[TỪ DESIGN §N]`
- `[GỢI Ý BỔ SUNG]`
- `[GỢI Ý]`
- `[TỪ AUDIT TÀI NGUYÊN]`
- `[TỪ AUDIT]`
- `[TỪ AUDIT CUSTOM]`
- `[CẦN LÀM RÕ]`

**Evidence:**

- `skill-planner/SKILL.md:172-177` định nghĩa tag chuẩn.
- `skill-planner/SKILL.md:198` lại dùng `[GỢI Ý]` và `[TỪ AUDIT CUSTOM]`.
- `skill-planner/loop/plan-checklist.md:15` dùng `[TỪ DESIGN]`, `[GỢI Ý]`, `[TỪ AUDIT]`.

**Ảnh hưởng:** Validator và Builder có thể bỏ sót/misclassify task, đặc biệt khi bộ skill được dùng bởi nhiều người với nhiều cách viết khác nhau.

---

### P1-05 — Typo khiến Builder bỏ sót clarification blockers

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** High

Planner chuẩn hóa tag:

- `[CẦN LÀM RÕ]`

Nhưng Builder scan:

- `[CẦU LÀM RÕ]`

**Evidence:**

- `skills/rebuild/skill-builder/SKILL.md:85`
- `skills/rebuild/skill-builder/knowledge/architect.md:37`

**Ảnh hưởng:** Builder có thể tiếp tục build dù `todo.md` còn item cần làm rõ.

---

### P1-06 — Planner section contract tự mâu thuẫn

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** High

**Evidence:**

- `skill-planner/SKILL.md:108` nói `todo.md` "MUST contain exactly 5 sections".
- `skill-planner/SKILL.md:152` lại thêm `## 6. Builder Feedback Integration`.
- `validate-todo.py:32-34` coi section 6 optional.

**Ảnh hưởng:** Người/agent dùng skill không biết `section 6` là bắt buộc, optional, hay vi phạm "exactly 5".

---

### P1-07 — Architect output contract lệch template/checklist

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** High

**Evidence:**

- `design-checklist.md:8` ghi "10 Sections".
- `design.md.template` có 10 sections chính.
- Nhưng `skill-architect/SKILL.md` thêm `§10.1`, `§11`, `§12`.

**Ảnh hưởng:** Design output có thể bị đánh giá sai: đủ theo template nhưng thiếu theo SKILL.md, hoặc ngược lại.

---

### P1-08 — Validator logic chưa đủ tin cậy

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** High

#### `validate-todo.py`

Đang check:

- Required section headers.
- Một phần table columns.
- Trace tag dạng string.
- Priority string bằng regex đơn giản.

Chưa check:

- `design.md §3` files đã map đủ thành tasks chưa.
- Dependency IDs hợp lệ.
- Priority column trong bảng thực sự thuộc enum chưa.
- `section 6` là optional hay required.

#### `validate_skill.py`

Vấn đề đã xác minh:

- `check_skill_md_constraints()` bắt keyword `"## Persona"` (`validate_skill.py:96`), trong khi `skill-builder/SKILL.md` chỉ có `## Mission` và `**Persona:**`.
- Regex file mapping tại `validate_skill.py:160` không match extension dài như `.template`; ví dụ `templates/output.template` không được bắt.
- Không có `--todo` để validate todo trace/dependencies.
- `check_error_handling()` chỉ phát hiện string, không chứng minh STOP behavior.

---

### P1-09 — Builder context path không dynamic

**Trạng thái:** Confirmed  
**Mức độ:** P1  
**Confidence:** Medium-High

Builder đọc context bằng:

- `../../.skill-context/{skill-name}/...` tại `skill-builder/SKILL.md:75-79`

Nhưng validator command dùng:

- `../../../.skill-context/{skill-name}/design.md` tại `skill-builder/SKILL.md:110-111`

**Vấn đề:** Relative path phụ thuộc nơi skill được install. Nếu output root không phải `.claude/skills/{skill-name}`, cả hai có thể sai.

**Dynamic requirement:** Luôn resolve context từ **current project root / cwd**, không từ install path của skill.

---

### P2-01 — Progressive disclosure bị front-load quá rộng

**Trạng thái:** Confirmed  
**Mức độ:** P2/P1 nếu dùng rộng rãi  
**Confidence:** High

3 SKILL.md đều có directive yêu cầu quét/đọc trực tiếp nội dung trong `knowledge/`, `templates/`, `scripts/`, `loop/` trước khi bắt đầu.

Điều này mâu thuẫn với chính guideline trong:

- `skill-builder/knowledge/anthropic-skill-standards.md:55-68`, anti-pattern "Context Overloading".

**Ảnh hưởng:** Tốn token, giảm dynamic reuse, dễ làm agent load tài liệu không cần thiết.

---

### P2-02 — `data/` zone support chưa đồng bộ end-to-end

**Trạng thái:** Confirmed một phần  
**Mức độ:** P2  
**Confidence:** Medium-High

**Có support:**

- Architect Zone Mapping có `Data`.
- Builder đọc `.skill-context/{skill-name}/data/` nếu có.
- Builder validator collect critical files trong `data/`.

**Thiếu/mờ:**

- `init_context.py` chỉ tạo `resources/`, không tạo `data/` hoặc `loop/`.
- Planner không có template task riêng cho Data zone.
- `design.md.template` mindmap chưa include `data`.

---

### P2-03 — Template integration chưa đồng bộ

**Trạng thái:** Confirmed một phần  
**Mức độ:** P2  
**Confidence:** Medium

**Đúng:** `init_context.py` dùng:

- `design.md.template`
- `todo.md.template`
- `build-log.md.template`

**Thiếu:**

- Planner không reference rõ `todo.md.template`.
- Builder không reference rõ `build-log.md.template`.
- `resource-document.md.template` không thấy được reference từ Planner.

---

### P2-04 — Output path mismatch `.claude` vs `.agent`

**Trạng thái:** Confirmed  
**Mức độ:** P2  
**Confidence:** High

**Evidence:**

- `skill-builder/SKILL.md:16` output contract: `.claude/skills/{skill-name}`.
- `skill-architect/templates/build-log.md.template:40` ghi `.agent/skills/{skill_name}/`.

**Ảnh hưởng:** Người dùng không biết skill package cuối cùng nằm ở đâu, đặc biệt khi dùng trên nhiều project/tooling khác nhau.

---

### P2-05 — Stale/generated artifacts nằm trong source

**Trạng thái:** Confirmed  
**Mức độ:** P2  
**Confidence:** High

**Evidence:**

- `skills/rebuild/skill-builder/scripts/__pycache__/validate_skill.cpython-314.pyc`
- `skills/rebuild/skill-builder/loop/build-log.md` ghi validation PASS/READY, nhưng chạy validator hiện tại trên `skill-builder` fail vì thiếu `## Persona`.

**Ảnh hưởng:** Dễ gây nhiễu khi đóng gói/copy bộ skill sang nơi khác.

---

## 3. Bảng ưu tiên xử lý

| Ưu tiên | Issue | Lý do |
|---|---|---|
| 1 | P0-01 Shared framework path | Boot foundation; không fix thì 3 skill thiếu nguồn sự thật |
| 2 | P0-02 Path hardcode `.claude/skills` | Điều kiện bắt buộc để portable/dynamic |
| 3 | P1-05 Typo clarification tag | Chặn nguy cơ Builder build khi còn blocker |
| 4 | P1-04 Trace tag taxonomy | Nền cho validator và handoff |
| 5 | P1-06/P1-07 Section contracts | Nền cho artifact schema ổn định |
| 6 | P1-02/P1-08 Validators | Biến rules thành deterministic checks |
| 7 | P1-03 Feedback loop | Cho phép Builder report ngược khi phát hiện design/plan lỗi |
| 8 | P2-01 Progressive disclosure | Tối ưu token và khả năng dùng rộng |
| 9 | P2-02/P2-03 Data/templates | Hoàn thiện end-to-end workflow |
| 10 | P2-04/P2-05 Cleanup packaging | Tránh nhiễu khi phân phối |

---

## 4. Target architecture đề xuất cho bộ 3 portable

Canonical deployable layout:

```text
<skills-root>/
├── _shared/
│   └── knowledge/
│       └── framework.md
├── skill-architect/
│   ├── SKILL.md
│   ├── knowledge/
│   ├── scripts/
│   ├── templates/
│   └── loop/
├── skill-planner/
│   ├── SKILL.md
│   ├── knowledge/
│   ├── scripts/
│   ├── templates/
│   └── loop/
└── skill-builder/
    ├── SKILL.md
    ├── knowledge/
    ├── scripts/
    └── loop/
```

Path rules:

| Từ đâu | Shared framework path nên dùng |
|---|---|
| Từ `skill-*/SKILL.md` | `../_shared/knowledge/framework.md` |
| Từ `skill-*/knowledge/*.md` | `../../_shared/knowledge/framework.md` |
| Từ scripts | Resolve bằng `Path(__file__).parents` hoặc tham số CLI, không hardcode repo |

Context rules:

| Artifact | Resolve từ đâu |
|---|---|
| `.skill-context/{skill-name}` | current project root / cwd, không từ skill install root |
| output skill package | user-configurable `skills_root`, không hardcode `.claude` |

---

## 5. Stop condition cho đợt xử lý

Chưa nên coi bộ 3 là portable-ready cho đến khi đạt tối thiểu:

- Không còn reference hardcode `@.claude/skills/...` trong runtime instructions.
- `framework.md` tồn tại trong deployable `skills-root/_shared/knowledge/framework.md`.
- 3 SKILL.md dùng relative path đúng từ skill root.
- Trace tag taxonomy chỉ còn 1 bộ chuẩn.
- Builder scan đúng `[CẦN LÀM RÕ]`.
- `design.md`, `todo.md`, `build-log.md` contracts đồng bộ giữa SKILL.md, templates, checklists, validators.
- Validators có thể chạy trên fixture tốt/xấu và fail đúng lỗi.
- Copy toàn bộ bộ 3 sang một thư mục tạm khác vẫn resolve được shared/local files.
