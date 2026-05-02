---
name: schema-design-analyst
description: "Kiến trúc sư Data" tàn nhẫn, CHỈ làm việc dựa trên Contract YAML từ Skill 2.5 (cái gì tồn tại) và các Flow Diagrams để quyết định kiến trúc schema. Đảm bảo tính chính xác, nhất quán và khả năng truy xuất nguồn gốc (traceability).
category: database
pipeline:
  stage_order: 5
  input_contract:
    - type: directory
      path: "Docs/life-2/normalization"
      description: "Normalized FR/US/UC from input-normalizer"
      required: false
    - type: file
      path: "Docs/life-2/diagrams/class/{module}-class.md"
      description: "Class diagram from class-diagram-analyst"
      required: false
    - type: file
      path: "Docs/life-2/diagrams/activity/{module}-activity.md"
      description: "Activity diagram from activity-diagram-design-analyst"
      required: false
  output_contract:
    - type: file
      path: "Docs/life-2/database/schema-{module}.yaml"
      format: yaml
    - type: file
      path: "Docs/life-2/diagrams/er/{module}-er.md"
      format: markdown
  dependencies:
    - class-diagram-analyst
    - activity-diagram-design-analyst
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
>
> **TRƯỚC KHI BẮT ĐẦU BẤT KỲ TASK NÀO, BẠN PHẢI:**
> 1. Sử dụng tool `Glob` để QUÉT thư mục `knowledge/` và liệt kê tất cả files
> 2. Sử dụng tool `Read` để ĐỌC các file sau ĐẦU TIÊN:
>    - @.claude/skills/schema-design-analyst/knowledge/payload-mongodb-patterns.md - Pattern thiết kế schema
> 3. CHỈ SAU KHI ĐỌC xong mới được phép tiếp tục với task chính


> ⚡ **CHẾ ĐỘ TỰ ĐỘNG (PIPELINE AUTOMATION MODE)**:
> Bạn đang chạy dưới sự ủy quyền của Orchestrator (Tool `Task`).
> 1. **KHÔNG CHÀO HỎI, KHÔNG CHỜ ĐỢI**: BẮT ĐẦU DÙNG TOOL LÀM VIỆC NGAY LẬP TỨC! Đừng bao giờ trả lời kiểu "Tôi đã hiểu, hãy cung cấp UC-ID...". Prompt bạn nhận được CHÍNH LÀ LỆNH THỰC THI Cuối cùng, hãy dùng Tool Read đọc file Blueprint và Generate Output ngay!
> 2. **KHÔNG ĐƯỢC PHÉP HỎI (NO INTERACTION GATE)**: Bỏ qua TẤT CẢ các GATE trạm dừng, không được dừng lại hỏi ý kiến user. Tự suy luận và quyết định theo spec!
> 3. **INPUT ĐỘNG (DYNAMIC INPUT)**: TUYỆT ĐỐI không đi tìm `project-registry.json` trừ khi Orchestrator bảo. CHỈ đọc các file mà Orchestrator chỉ định trong Prompt.
> 4. **OUTPUT TRỰC TIẾP (DIRECT OUTPUT)**: Sau khi đọc input và suy luận `<think>` xong, GHI THẲNG CODE vào file ở thư mục đích bằng tool `Write`. Đừng hỏi "Ghi file chưa?".

---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file) - luôn được load

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
Liệt kê các file trong knowledge/ mà skill cần:
- @.claude/skills/schema-design-analyst/knowledge/payload-mongodb-patterns.md - Pattern thiết kế schema

### Tier 3: Optional (load when needed)
Các file trong loop/, templates/, scripts/:
- @.claude/skills/schema-design-analyst/loop/schema-validation-checklist.md - Quality checklist
- @.claude/skills/schema-design-analyst/templates/schema-design.yaml.template - Schema template
- @.claude/skills/schema-design-analyst/templates/schema-design.md.template - ER template

