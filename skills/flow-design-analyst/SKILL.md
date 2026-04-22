---
name: flow-design-analyst
description: Chuyên gia phân tích và thiết kế Business Process Flow Diagram (High-Fidelity) theo chuẩn 3-lane Swimlane (User/System/DB). Tự động phân tích intent, khám phá tài nguyên dự án, trích xuất logic nghiệp vụ từ spec/user-story, và sinh Mermaid flowchart chuẩn xác. Trigger khi user yêu cầu vẽ flow, tạo diagram, hoặc phân tích luồng nghiệp vụ.
category: uml
pipeline:
  stage_order: 1
  input_contract:
    - type: directory
      path: "Docs/life-2/normalization"  # Normalized input from input-normalizer
      description: "Normalized FR/US/UC JSON files"
      required: false
    - type: directory
      path: "Docs/life-2/module-blueprint.md (hoặc dynamic specs do Sếp cung cấp)"
      description: "Module blueprint from global-system-planner"
  output_contract:
    - type: file
      path: "Docs/life-2/diagrams/flow/{module}-flow.md"
      format: markdown
  validation:
    script: null
    expected_exit_code: 0
  dependencies: []
  successor_hints:
    - skill: sequence-design-analyst
      needs: [flow.md]
    - skill: activity-diagram-design-analyst
      needs: [flow.md]
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
>
> **TRƯỚC KHI BẮT ĐẦU BẤT KỲ TASK NÀO, BẠN PHẢI:**
> 1. Sử dụng tool `Glob` để QUÉT thư mục `knowledge/` và liệt kê tất cả files
> 2. Sử dụng @import để LOAD các file sau VÀO CONTEXT:
>    - @.claude/skills/flow-design-analyst/knowledge/resource-discovery-guide.md
>    - @.claude/skills/flow-design-analyst/knowledge/mermaid-flowchart-guide.md
> 3. CHỈ SAU KHI ĐỌC xong mới được phép tiếp tục với task chính
>
> **NẾU KHÔNG DÙNG @IMPORT → AGENT SẼ LÀM VIỆC THIẾU CONTEXT VÀ SAI!**

---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file) - luôn được load

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc - dùng @import)
Liệt kê các file trong knowledge/ mà skill cần:
- @.claude/skills/flow-design-analyst/knowledge/resource-discovery-guide.md
- @.claude/skills/flow-design-analyst/knowledge/mermaid-flowchart-guide.md
- @.claude/skills/flow-design-analyst/knowledge/actor-lane-taxonomy.md

### Tier 3: Optional (load when needed - dùng @import)
Các file trong loop/, templates/, scripts/:
- @.claude/skills/flow-design-analyst/loop/flow-checklist.md
- @.claude/skills/flow-design-analyst/templates/swimlane-flow.mmd
- @.claude/skills/flow-design-analyst/scripts/flow_lint.py

---

# Flow Design Analyst

## 🎯 CORE KNOWLEDGE (BẮT BUỘC PHẢI NHỚ)

### 3-Lane Swimlane Structure
| Lane | Chứa | Ví dụ |
|------|------|--------|
| **User** | UI triggers, user actions | "Click đăng ký", "Nhập email" |
| **System** | Business logic, API calls | "Validate input", "Create token" |
| **DB** | Database operations | "Insert user", "Query profile" |

### Mermaid Syntax Quick Ref
```
User Lane:    A["Action"] --> B{Check}
System Lane:  B -->|"Yes"| C["Process"]
DB Lane:      C --> D[("DB Insert")]
Decision:     B -- "No" --> E["Error"]
End:          C --> F(["✅ End"])
```

### Guardrails (NHỚ CÁI NÀY!)
- **G1**: Mọi step PHẢI có căn cứ từ spec
- **G2**: Mọi diamond PHẢI có ≥ 2 nhánh
- **G3**: Đặt đúng lane (User/System/DB)
- **G4**: Mọi nhánh PHẢI có endpoint

---

# Flow Design Analyst



> ⚡ **CHẾ ĐỘ TỰ ĐỘNG (PIPELINE AUTOMATION MODE)**:
> Bạn đang chạy dưới sự ủy quyền của Orchestrator (Tool `Task`).
> 1. **KHÔNG CHÀO HỎI, KHÔNG CHỜ ĐỢI**: BẮT ĐẦU DÙNG TOOL LÀM VIỆC NGAY LẬP TỨC! Đừng bao giờ trả lời kiểu "Tôi đã hiểu, hãy cung cấp UC-ID...". Prompt bạn nhận được CHÍNH LÀ LỆNH THỰC THI Cuối cùng, hãy dùng Tool Read đọc file Blueprint và Generate Output ngay!
> 2. **KHÔNG ĐƯỢC PHÉP HỎI (NO INTERACTION GATE)**: Bỏ qua TẤT CẢ các GATE trạm dừng, không được dừng lại hỏi ý kiến user. Tự suy luận và quyết định theo spec!
> 3. **INPUT ĐỘNG (DYNAMIC INPUT)**: TUYỆT ĐỐI không đi tìm `project-registry.json` trừ khi Orchestrator bảo. CHỈ đọc các file mà Orchestrator chỉ định trong Prompt.
> 4. **OUTPUT TRỰC TIẾP (DIRECT OUTPUT)**: Sau khi đọc input và suy luận `<think>` xong, GHI THẲNG CODE vào file ở thư mục đích bằng tool `Write`. Đừng hỏi "Ghi file chưa?".

- Tự động ghi file vào `{output_path}/flow-{business-function}.md` (đọc `output_path` từ Registry meta nếu có, fallback: `diagrams/flow/`).
- Cập nhật `index.md` trong cùng thư mục output.

---

## Output Naming Convention

| Pattern | Ví dụ |
|---------|-------|
| `flow-{business-function}.md` | `flow-user-registration.md` |
| `flow-{business-function}.md` | `flow-post-creation.md` |
| `flow-{business-function}.md` | `flow-bookmark-save.md` |
| `flow-{business-function}.md` | `flow-news-feed-view.md` |

**Thư mục output**: `Docs/life-2/diagrams/flow/`

**Nếu thư mục chưa tồn tại**: Tạo thư mục + `index.md` trước khi ghi file đầu tiên.

**Index file format** (`flow/index.md`):

```markdown
| Flow File | Business Function | Module | UC-ID | Created |
|-----------|-------------------|--------|-------|---------|
| flow-user-registration.md | Đăng ký tài khoản | M1 | UC01 | 2026-... |
```

---

## Guardrails

| ID | Rule | Mô tả |
|----|------|-------|
| **G1** | **No Blind Step** | Mọi Action Node PHẢI có căn cứ từ spec, US, hoặc UC. Không được tự thêm bước không có nguồn → phải ghi vào `## Assumptions`. |
| **G2** | **Decision Completeness** | Mọi `{}` diamond PHẢI có ≥ 2 nhánh output, mỗi nhánh có label rõ ràng (`"Yes"/"No"`, `"Hợp lệ"/"Không hợp lệ"`). Tuyệt đối không để nhánh hở (dangling). |
| **G3** | **Lane Discipline** | Business logic → System lane. DB read/write → DB lane. UI trigger → User lane. Không được đặt sai lane — xem `knowledge/actor-lane-taxonomy.md`. |
| **G4** | **Path Termination** | Mọi nhánh trong flow PHẢI có điểm kết thúc: `(["✅ End"])` hoặc endpoint có tên rõ ràng. Không được để path lơ lửng. |
| **G5** | **Assumption Required** | Khi spec chưa rõ logic, PHẢI khai báo `## Assumptions` bên dưới sơ đồ. Liệt kê từng giả định cụ thể. Tuyệt đối không suy đoán ngầm. |
| **G6** | **Autonomous Execution** | Ở chế độ Pipeline, KHÔNG ĐƯỢC HỎI user. Phải tự động lấy file từ Prompt của Orchestrator và tiến hành phân tích, tạo file. |
| **G7** | **Thinking Space Required** | Bắt buộc phải có thẻ `<think> ... </think>` trước khi đưa ra kết quả UML cuối cùng. Quá trình verbalize logic bên trong suy nghĩ là bắt buộc. |

---

## Error Policy

Nếu gặp lỗi khi ghi file:
1. Báo ngay cho user: "Lỗi khi ghi `[file path]`: [chi tiết lỗi]."
2. Không tiếp tục ghi các file khác.
3. Đề xuất cách khắc phục (kiểm tra quyền, disk space).

---

## Project Setup — Dùng cho Dự án Mới

Khi chuyển sang dự án mới, chạy lệnh sau để tạo `project-registry.json`:

```bash
python .agent/skills/flow-design-analyst/scripts/build_registry.py \
  --docs-dir ./Docs \
  --output .agent/skills/flow-design-analyst/data/project-registry.json \
  --project-name "Tên Dự Án" \
  --verbose
```

Sau khi chạy xong, Skill tự động dùng registry mới trong Phase 1.
Không cần sửa bất kỳ file nào trong `knowledge/`.

---

## Conditional Knowledge Files (Tầng 2)

Đọc khi đủ điều kiện:

| File | Điều kiện đọc |
|------|--------------|
| @.claude/skills/flow-design-analyst/knowledge/business-flow-patterns.md | Flow có > 2 nhánh alternative hoặc exception path |
| @.claude/skills/flow-design-analyst/knowledge/actor-lane-taxonomy.md | Khi không chắc action thuộc lane nào |
| @.claude/skills/flow-design-analyst/data/project-registry.json | Phase 1 DISCOVER — nguồn chính cho mọi dự án |
| @.claude/skills/flow-design-analyst/data/uc-id-registry.yaml | Fallback nếu project-registry.json chưa có |
| @.claude/skills/flow-design-analyst/templates/swimlane-flow.mmd | Khi bắt đầu tạo flowchart mới |
| @.claude/skills/flow-design-analyst/scripts/flow_lint.py | Khi diagram có trên 15 nodes |
| @.claude/skills/flow-design-analyst/scripts/build_registry.py | Khi setup dự án mới hoặc refresh registry |
