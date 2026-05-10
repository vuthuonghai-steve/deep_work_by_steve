# Báo cáo nghiên cứu: Những gì em hiểu từ Master Skill Suite và ghi chú cải thiện

> Ngày: 2026-05-09
> Tác giả: Hermes Agent, viết từ góc nhìn vận hành của trợ lý
> Trạng thái: Báo cáo raw phục vụ cải thiện
> Thư mục nguồn: `docs/raw/ideas/skill-suite-improvement-raw-notes/`
> Mục đích: Ghi lại những gì trợ lý đã hiểu và tiếp nhận từ bộ `skill-architect`, `skill-planner`, `skill-builder`, đồng thời đề xuất hướng cải thiện cho vòng tiếp theo.

---

## 1. Bối cảnh

Báo cáo này ghi lại hiểu biết của em sau khi đọc và đánh giá bộ 3 skill phát triển kỹ năng mà anh Steve yêu cầu:

1. `skill-architect`
2. `skill-planner`
3. `skill-builder`

Quá trình đánh giá cũng sử dụng tài liệu kiến trúc raw:

- `/home/steve/Work-space/deep_work_by_steve/docs/raw/AGENTS.md`

Và các file skill chính đã được đọc trước đó:

- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-architect/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-planner/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/_shared/knowledge/framework.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-planner/knowledge/skill-packaging.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/knowledge/build-guidelines.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/knowledge/anthropic-skill-standards.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/scripts/validate_skill.py`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/loop/build-checklist.md`

Đây là một báo cáo raw, chưa phải bản đặc tả triển khai cuối cùng. Nên xem tài liệu này như nguyên liệu đầu vào để tiếp tục cải thiện bộ skill suite.

---

## 2. Những gì em hiểu từ `AGENTS.md`

`AGENTS.md` mô tả một kiến trúc agent rộng hơn, trong đó bộ skill suite là một phần của hệ thống agent lớn.

### 2.1 Hệ thống orchestrator nhiều lớp

Project có pattern orchestrator tên là `pipeline-steve`. Pattern này điều phối một pipeline thực thi gồm 4 lớp:

1. Explore
2. Implement
3. Verify Rule
4. Simplify

Tài liệu ghi rõ một ràng buộc nền tảng rất quan trọng:

> Subagents cannot spawn other subagents.

Nghĩa là: subagent không thể spawn subagent khác.

Vì vậy, orchestrator cấp cao nhất phải trực tiếp spawn toàn bộ worker subagents. Điều này ảnh hưởng trực tiếp đến cách thiết kế automation cho việc build skill trong tương lai. Nếu sau này bộ skill suite sử dụng subagents, nó không nên giả định rằng có thể delegate lồng nhau, trừ khi runtime hỗ trợ rõ ràng.

### 2.2 Pipeline phát triển skill

`AGENTS.md` định nghĩa Master Skill Suite như một pipeline 3 stage:

```text
Yêu cầu người dùng
  -> skill-architect -> design.md
  -> skill-planner   -> todo.md
  -> skill-builder   -> skill package hoàn chỉnh
```

Mỗi stage có trách nhiệm riêng:

| Stage | Skill | Vai trò chính | Output |
|---|---|---|---|
| 1 | `skill-architect` | Phân tích yêu cầu và thiết kế kiến trúc skill | `design.md` |
| 2 | `skill-planner` | Chuyển design thành các task triển khai | `todo.md` |
| 3 | `skill-builder` | Build và kiểm chứng skill package thật | skill files + build log |

Bộ suite này không chỉ là công cụ viết nội dung. Mục tiêu của nó là trở thành một meta-system có thể tái sử dụng để biến các pattern hợp tác giữa người dùng và agent thành những kỹ năng bền vững.

### 2.3 Cấu trúc skill package 7 vùng

Skill package mong muốn đi theo cấu trúc 7 vùng:

```text
{skill-name}/
├── SKILL.md
├── knowledge/
├── scripts/
├── templates/
├── data/
├── loop/
└── assets/   # đôi khi bị bỏ qua trong ví dụ, nhưng vẫn thuộc mô hình 7 vùng
```

Mỗi vùng đại diện cho một loại năng lực có thể tái sử dụng:

- `SKILL.md`: điều phối, persona, workflow, guardrails
- `knowledge/`: tri thức domain, tiêu chuẩn, tài liệu tham chiếu
- `scripts/`: công cụ automation và validator
- `templates/`: định dạng output mẫu
- `data/`: config, schema, dữ liệu tĩnh
- `loop/`: checklist, log, luật kiểm chứng
- `assets/`: hình ảnh hoặc tài nguyên tĩnh hỗ trợ khác

### 2.4 Quy trình ghi raw ideas

`AGENTS.md` cũng quy định rằng các ý tưởng raw nên được ghi vào `docs/raw/ideas/`, với cách đặt tên như:

- `YYYY-MM-DD-idea-name.md`
- `YYYY-MM-DD-research-name.md`
- `YYYY-MM-DD-design-name.md`
- `YYYY-MM-DD-brainstorm-name.md`

Báo cáo này tuân theo quy ước đó bằng cách được đặt trong một thư mục ý tưởng có tên tiếng Anh và dùng tiền tố `research-`.

---

## 3. Những gì em nhận được từ bộ 3 skill

Từ góc nhìn vận hành của em, bộ 3 skill này cho em một cách có cấu trúc để biến quá trình hợp tác lặp lại giữa anh và em thành các agent skills có thể tái sử dụng.

Điều quan trọng nhất em nhận được không chỉ là hướng dẫn viết một skill. Em nhận được một vòng đời đầy đủ:

1. Hiểu pain point.
2. Thiết kế kiến trúc skill.
3. Chuyển kiến trúc thành task triển khai.
4. Build các file.
5. Kiểm chứng output.
6. Ghi lại bằng chứng và bài học.

Điều này có giá trị vì nó ngăn việc tạo skill trở thành một hoạt động viết prompt một lần rồi bỏ đó. Nó biến việc tạo skill thành một quy trình kỹ thuật.

---

## 4. Hiểu biết về `skill-architect`

### 4.1 Vai trò

`skill-architect` đóng vai trò Senior Skill Architect. Nhiệm vụ của nó chỉ là thiết kế.

Nó không nên trực tiếp implement file và không nên tạo task list. Output của nó là `design.md`.

### 4.2 Workflow

Architect có 3 phase chính:

1. Collect
   - Xác định tên skill.
   - Hiểu pain point.
   - Xác định người dùng và ngữ cảnh.
   - Làm rõ output mong đợi.

2. Analyze
   - Map yêu cầu vào 3 Pillars:
     - Knowledge
     - Process
     - Guardrails
   - Map skill vào 7 Zones.
   - Xác định rủi ro và blind spots.

3. Design and output
   - Tạo sơ đồ Mermaid.
   - Định nghĩa cấu trúc thư mục.
   - Định nghĩa execution flow.
   - Định nghĩa interaction points.
   - Định nghĩa progressive disclosure tiers.
   - Viết `design.md`.

### 4.3 Giá trị nhận được

Architect giúp em tránh build skill quá sớm. Nó buộc hệ thống phải hỏi:

- Vấn đề thật sự là gì?
- Tri thức nào phải được viết rõ ra?
- Quy trình nào cần được mã hóa?
- Model có khả năng sai ở đâu?
- Thật sự cần những file nào?

Điều này hữu ích vì nhiều skill yếu không thất bại do câu chữ kém, mà thất bại do kiến trúc không rõ.

---

## 5. Hiểu biết về `skill-planner`

### 5.1 Vai trò

`skill-planner` đọc `design.md` và tạo ra `todo.md`.

Mục đích của nó là phân rã kế hoạch, không phải implement.

### 5.2 Workflow

Planner thực hiện:

1. Đọc input và audit tài nguyên.
2. Phân tích tri thức cần thiết bằng mô hình 3 tầng:
   - Domain
   - Technical
   - Packaging
3. Sinh task kèm trace tags.
4. Kiểm tra task có bao phủ design hay không.
5. Chuẩn bị handoff cho builder.

### 5.3 Giá trị nhận được

Planner quan trọng vì nó tạo cây cầu giữa kiến trúc và triển khai.

Ý tưởng mạnh nhất trong planner là traceability. Mỗi task nên liên kết ngược về một nguồn:

- `[TỪ DESIGN §N]`
- `[GỢI Ý BỔ SUNG]`
- `[TỪ AUDIT TÀI NGUYÊN]`
- `[CẦN LÀM RÕ]`

Điều này giúp giảm hallucination vì builder không nên tạo file hoặc requirement nếu không có lý do có thể truy vết.

---

## 6. Hiểu biết về `skill-builder`

### 6.1 Vai trò

`skill-builder` là implementation engineer.

Nó đọc:

- `design.md`
- `todo.md`
- `resources/`
- `data/` nếu có
- các file loop/proof trước đó nếu có

Sau đó nó build skill package.

### 6.2 Workflow

Builder có 5 phase:

1. PREPARE and evaluate
2. CLARIFY unresolved issues
3. BUILD phase-by-phase
4. VERIFY using quality gates
5. DELIVER with build log

### 6.3 Giá trị nhận được

Builder đóng góp nhiều thực hành kỹ thuật mạnh:

- Nó nên phản biện design không nhất quán.
- Nó không nên âm thầm tiếp tục khi có lỗi nghiêm trọng.
- Nó nên dùng build log làm bằng chứng.
- Nó nên kiểm tra mật độ placeholder.
- Nó nên giữ fidelity từ các tài nguyên nguồn critical.
- Nó nên tránh bịa thêm file ngoài zone contract.

Điều này giúp stage cuối có tư duy kiểm soát chất lượng, thay vì chỉ sinh file đơn thuần.

---

## 7. Đánh giá chất lượng tổng thể

Đánh giá tổng thể của em là:

```text
Ý tưởng kiến trúc:              mạnh
Tách pipeline theo trách nhiệm: mạnh
Ý định chống hallucination:     mạnh
Độ nhất quán runtime:           trung bình
Tương thích Hermes:             trung bình-thấp
Độ chắc của validator:          trung bình-thấp
Vòng học từ feedback:           chưa hoàn chỉnh
```

Về mặt ý tưởng, bộ suite này mạnh. Nó đã đi đúng hướng: thiết kế trước, lập kế hoạch sau, build cuối cùng.

Tuy nhiên, nó chưa hoàn toàn ổn định như một workflow build Hermes skill ở cấp production. Một số contract vẫn còn mơ hồ, phụ thuộc nhiều vào Markdown, hoặc kế thừa assumption từ môi trường Claude.

---

## 8. Điểm mạnh chính

### 8.1 Tách trách nhiệm rõ ràng

Việc chia thành 3 stage là điểm mạnh nhất:

- Architect thiết kế.
- Planner phân rã.
- Builder triển khai.

Điều này ngăn một skill cố làm tất cả mọi thứ cùng lúc.

### 8.2 Tư duy chống hallucination tốt

Bộ suite nhiều lần nhấn mạnh:

- Không bịa tri thức domain.
- Trace task về section nguồn.
- Audit tài nguyên trước khi tuyên bố sẵn sàng.
- Dùng checklist và validator.
- Dừng lại khi bị block.

Đây chính xác là tư duy cần có để xây dựng skill đáng tin cậy.

### 8.3 Mô hình skill package tốt

Mô hình 7-zone hữu ích vì nó tách instruction, knowledge, automation, template, dữ liệu tĩnh, feedback loop và assets.

Nhờ vậy skill dễ bảo trì và mở rộng hơn.

### 8.4 Có ý thức về progressive disclosure

Bộ suite hiểu rằng skill không nên load mọi thứ ngay từ boot. Nó cố định nghĩa Tier 1, Tier 2 và Tier 3.

Điều này tốt cho hiệu quả token và giảm quá tải nhận thức cho model.

### 8.5 Có bằng chứng build và validation

Yêu cầu của builder về build logs, resource usage matrix, placeholder checks và validation scripts rất có giá trị.

Nó khuyến khích builder chứng minh những gì đã làm, thay vì chỉ tuyên bố là đã hoàn thành.

---

## 9. Vấn đề và khoảng trống chính

### 9.1 Path còn thiên về Claude thay vì Hermes-native

Builder hiện vẫn dùng `.claude/skills/{skill-name}` làm output contract ở một số chỗ.

Với Hermes, điều này chưa phù hợp. Hermes skills thường nằm ở:

```text
~/.hermes/skills/{category}/{skill-name}/
```

hoặc trong một repository:

```text
skills/{category}/{skill-name}/SKILL.md
```

Bộ suite nên hỗ trợ target cài đặt động thay vì hardcode `.claude/skills`.

Contract được đề xuất:

```yaml
install_target:
  platform: hermes
  scope: user-local
  path: ~/.hermes/skills/{category}/{skill-name}/
```

Các giá trị khả dĩ:

```yaml
platform: hermes | claude | both
scope: user-local | repo | project-local
```

### 9.2 Markdown table vẫn đang bị xem là source of truth

Bộ suite muốn hướng đến contract có cấu trúc theo kiểu AI-first, nhưng phần handoff thực tế vẫn phụ thuộc nhiều vào Markdown table.

Điều này mong manh. Validator hoặc agent có thể đọc sai Markdown table nếu:

- heading thay đổi
- format table thay đổi
- file path xuất hiện trong ví dụ
- một zone được viết bằng prose thay vì table
- filename có extension không thường gặp

Cách tốt hơn là dùng artifact YAML-first:

- frontmatter của `design.md` chứa `zone_mapping` chính thức
- frontmatter của `todo.md` chứa `phases`, `tasks`, `blockers`, `prerequisites` chính thức
- frontmatter của `build-log.md` chứa `execution_trace`, `quality_metrics`, `resource_usage` chính thức

Markdown body vẫn nên giữ lại để giải thích cho con người, nhưng không nên là machine contract.

### 9.3 Contract nội bộ chưa nhất quán

Một số hướng dẫn đang mâu thuẫn với nhau.

Ví dụ:

1. `skill-planner` nói `todo.md` phải có chính xác 5 section, nhưng sau đó lại định nghĩa section thứ 6: Builder Feedback Integration.
2. `skill-architect` có tín hiệu mâu thuẫn về việc `knowledge/architect.md` là Tier 1 hay Tier 2.
3. Shared framework xem scripts là optional, trong khi một số câu chữ ở builder checklist lại khiến scripts giống như bắt buộc.
4. Hệ thống đôi khi nói 7 zones, nhưng một số validator/checklist chỉ tập trung vào 4 zones.
5. Vị trí build log chưa hoàn toàn nhất quán: đôi khi ở trong skill package được sinh ra, đôi khi ở `.skill-context/{skill-name}/build-log.md`.

Những mâu thuẫn này có thể khiến em chọn sai rule trong lúc thực thi.

### 9.4 Validator phụ thuộc quá nhiều vào regex

`validate_skill.py` hữu ích, nhưng hiện tại phụ thuộc quá nhiều vào pattern matching.

Những điểm mong manh quan sát được:

- Nó parse Zone Mapping của `design.md` bằng heading và backtick regex.
- Nó kỳ vọng một số section keyword như `## Persona`, `Workflow`, `Guardrails`.
- Nó kiểm tra progressive disclosure chủ yếu qua Markdown links.
- Nó hardcode danh sách extra files được ignore.
- Nó chỉ đếm `[MISSING_DOMAIN_DATA]` như bằng chứng placeholder.

Validator mạnh hơn nên đọc YAML frontmatter có schema trước, sau đó mới dùng Markdown như nội dung phụ phục vụ người đọc.

### 9.5 Vòng học từ feedback chưa hoàn chỉnh

Bộ suite có build logs và một số feedback fields, nhưng workflow học từ việc sử dụng thật vẫn chưa đủ mạnh.

Mục tiêu không chỉ là tạo skill một lần. Mục tiêu là:

> Steve và trợ lý làm việc cùng nhau, phát hiện pattern, rồi liên tục cải thiện hệ thống skill.

Để làm được điều đó, suite cần một refinement loop chính thức:

1. Quan sát một session thật.
2. Xác định pain point lặp lại hoặc pattern thành công.
3. Quyết định nên lưu memory, patch skill, tạo skill mới, hay refactor skill hiện có.
4. Áp dụng bản patch nhỏ nhất và an toàn nhất.
5. Ghi lại lý do thay đổi.
6. Kiểm tra skill vẫn load được và vẫn đủ gọn.

### 9.6 Quá nhiều gate cho task nhỏ

Architect hiện yêu cầu nhiều confirmation gates. Điều này tốt cho workflow strict, nhưng quá nặng với các cải thiện skill nhỏ.

Bộ suite nên hỗ trợ execution modes:

```yaml
mode: lightweight | standard | strict
```

Hành vi gợi ý:

- `lightweight`: hỏi ít nhất có thể, output thiên về patch nhỏ
- `standard`: workflow 3-stage bình thường
- `strict`: đầy đủ gates, schemas, validators, build logs và handoff checks

### 9.7 Workflow tạo mới đang lấn át workflow patch/refactor

Bộ suite hiện mạnh nhất khi tạo skill mới từ đầu.

Nhưng trong công việc thật, các thao tác phổ biến thường là:

- patch một skill hiện có
- thêm pitfall
- thêm command còn thiếu
- tách một skill quá lớn
- merge các skill trùng lặp
- migrate skill tương thích Claude sang skill tương thích Hermes
- cải thiện validator sau khi gặp bug

Bộ suite nên hỗ trợ rõ ràng:

```yaml
operation_type:
  - create_new
  - patch_existing
  - refactor_existing
  - migrate_platform
  - consolidate_skills
  - deprecate_skill
```

Nếu không có phần này, builder có thể overbuild thay vì tạo một patch tập trung.

---

## 10. Các cải thiện Hermes-native cần có

Vì công việc này hiện đang được sử dụng qua Hermes Agent, bộ suite nên encode các quy tắc riêng của Hermes.

Đề xuất thêm file knowledge mới:

```text
skill-builder/knowledge/hermes-skill-standards.md
```

File này nên bao gồm:

1. User-local skills nằm trong `~/.hermes/skills/`.
2. Tạo skill bằng `skill_manage(action='create')` sẽ ghi vào cây user-local.
3. In-repo skills cần được ghi trực tiếp vào cây `skills/` trong repo.
4. Session hiện tại có thể chưa thấy skill mới tạo vì loader có thể được cache.
5. Frontmatter chuẩn cho Hermes nên gồm:
   - `name`
   - `description`
   - `version`
   - `author`
   - `license`
   - `metadata.hermes.tags`
   - `metadata.hermes.related_skills`
6. Supporting files nên dùng các thư mục được phép như:
   - `references/`
   - `templates/`
   - `scripts/`
   - `assets/`
7. Sửa nhỏ nên ưu tiên targeted patch thay vì rewrite toàn bộ.
8. Không giả định `.claude/skills` trừ khi platform được khai báo rõ là Claude.

Điều này sẽ giúp builder an toàn hơn trong môi trường hiện tại.

---

## 11. Kế hoạch cải thiện tiếp theo được đề xuất

### Phase 1: Sửa contract và mâu thuẫn

Patch các skill file hiện có để loại bỏ mâu thuẫn nội bộ:

- Sửa số lượng section của `todo.md`: 5 vs 6 sections.
- Làm rõ `knowledge/architect.md` là Tier 1 hay Tier 2 một cách nhất quán.
- Làm rõ scripts/templates/data/assets là optional trừ khi được khai báo trong `zone_mapping`.
- Làm rõ vị trí build-log.
- Thay hardcode `.claude/skills` bằng `install_target` động.

### Phase 2: Giới thiệu YAML-first artifacts

Thêm YAML frontmatter templates cho:

- `design.md`
- `todo.md`
- `build-log.md`

Biến YAML frontmatter thành canonical source of truth. Các section Markdown vẫn giữ lại để giải thích cho con người.

### Phase 3: Thêm schemas và validators

Tạo hoặc hoàn thiện:

```text
_shared/schemas/design.schema.yaml
_shared/schemas/todo.schema.yaml
_shared/schemas/build-log.schema.yaml
_shared/validators/handoff_validator.py
_shared/validators/schema_validator.py
_shared/validators/trace_validator.py
```

Validators nên đọc YAML contracts thay vì parse Markdown tables.

### Phase 4: Thêm Hermes skill standards

Thêm knowledge riêng cho Hermes và cho builder load file này khi target platform là Hermes.

Path đề xuất:

```text
skill-builder/knowledge/hermes-skill-standards.md
```

### Phase 5: Thêm operation modes

Thêm:

```yaml
mode: lightweight | standard | strict
operation_type: create_new | patch_existing | refactor_existing | migrate_platform | consolidate_skills | deprecate_skill
```

Điều này cho phép trợ lý chọn mức độ quy trình phù hợp.

### Phase 6: Thêm feedback/refinement loop

Tạo cơ chế feedback chính thức sau khi sử dụng.

Stage mới khả dĩ:

```text
skill-refiner
```

hoặc tích hợp vào builder dưới dạng:

```text
Phase 6: LEARN AND PATCH
```

Trách nhiệm:

- phân tích kết quả session
- ghi nhận pitfalls
- xác định workflow step còn thiếu
- đề xuất patch skill
- cập nhật skill ở mức tối thiểu
- ghi lại lý do thay đổi

---

## 12. Kiến trúc mục tiêu được đề xuất

Bộ suite tương lai nên có hình dạng như sau:

```text
Insight từ user/session
  -> skill-architect
       xuất design.md với YAML contract
  -> skill-planner
       xuất todo.md với YAML tasks và blockers
  -> skill-builder
       xuất Hermes-compatible skill package
       xuất build-log.md với evidence
  -> skill-refiner hoặc feedback loop
       patch skill hiện có dựa trên việc sử dụng thật
```

Artifacts:

```text
.skill-context/{skill-name}/
├── design.md       # YAML contract + giải thích cho con người
├── todo.md         # YAML task graph + human checklist
├── build-log.md    # YAML execution trace + validation evidence
├── resources/      # tài liệu nguồn domain
├── data/           # configs/schemas optional
└── loop/           # review notes, proofs, feedback trước đó
```

Target output của skill:

```text
~/.hermes/skills/{category}/{skill-name}/
```

hoặc, khi build cho repo:

```text
{repo}/skills/{category}/{skill-name}/
```

---

## 13. Kết luận thực tế

Bộ 3 skill đã có nền tảng mạnh. Nó cho em một mental model có giá trị để chuyển các pattern hợp tác lặp lại thành skill có thể tái sử dụng và bảo trì.

Những gì em đã nhận được từ nó:

1. Một quy trình theo stage để tạo skill.
2. Một mô hình package 7-zone.
3. Một phương pháp planning ưu tiên traceability.
4. Một tư duy builder có validation và evidence.
5. Một triết lý quality gate.
6. Một hướng đi rõ ràng tới structured contracts theo kiểu AI-first.

Những gì vẫn cần cải thiện:

1. Làm cho nó Hermes-native.
2. Thay Markdown-as-contract bằng YAML-first contracts.
3. Loại bỏ mâu thuẫn nội bộ.
4. Nâng cấp validators từ regex parsing sang schema validation.
5. Thêm execution modes cho lightweight vs strict work.
6. Thêm workflow patch/refactor, không chỉ workflow tạo mới.
7. Thêm vòng học thật để suite cải thiện qua quá trình Steve-trợ lý làm việc cùng nhau.

Đánh giá cuối:

> Bộ suite là một bản design draft mạnh với kiến trúc đúng hướng. Bước tiếp theo nên là làm nó cứng cáp hơn thành một hệ thống cải thiện skill theo hướng Hermes-native, schema-backed và feedback-driven.

---

## 14. Checklist hành động ngắn

- [ ] Patch output target từ `.claude/skills` sang `install_target` động.
- [ ] Thêm file Hermes Skill Standards.
- [ ] Chuyển `design.md`, `todo.md`, và `build-log.md` thành YAML-first artifacts.
- [ ] Thêm schema validators.
- [ ] Sửa mâu thuẫn về số lượng section trong planner.
- [ ] Sửa mâu thuẫn Tier 1/Tier 2.
- [ ] Làm rõ zone nào optional và zone nào mandatory.
- [ ] Thêm `mode` và `operation_type`.
- [ ] Thêm feedback/refinement loop.
- [ ] Dùng báo cáo này như nguyên liệu raw cho spec tiếp theo trong `docs/specs/`.
