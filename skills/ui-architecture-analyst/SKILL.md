---
name: ui-architecture-analyst
description: Extracts UI Screen Specs by analyzing Schema and Diagrams. Use when you need to bridge database logic and flow diagrams into intermediate UI component specifications for a given module. Trigger when user says "analyze UI for module X", "generate ui spec", "phân tích UI module", or invokes "ui-architecture-analyst --module M[X]".
category: ui
pipeline:
  stage_order: 6
  input_contract:
    - type: file
      path: "Docs/life-2/database/schema-{module}.yaml"
      required: false
    - type: file
      path: "Docs/life-2/diagrams/sequence/{module}-sequence.md"
      required: false
  output_contract:
    - type: file
      path: "Docs/life-2/ui/specs/{module}-ui-spec.md"
      format: markdown
  dependencies:
    - schema-design-analyst
  successor_hints:
    - skill: ui-pencil-drawer
      needs: [ui-spec.md]
---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file) - luôn được load

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
Liệt kê các file trong knowledge/ mà skill cần:
- @.claude/skills/ui-architecture-analyst/knowledge/ui-component-rules.md - UI component rules
- @.claude/skills/ui-architecture-analyst/knowledge/mapping-rules.md - Schema to UI mapping rules

### Tier 3: Optional (load when needed)
Các file trong loop/, templates/, scripts/:
- @.claude/skills/ui-architecture-analyst/loop/design-checklist.md - Quality checklist
- @.claude/skills/ui-architecture-analyst/templates/screen-spec.md.template - Screen spec template

---

> ⚡ **CHẾ ĐỘ TỰ ĐỘNG (PIPELINE AUTOMATION MODE)**:
> Bạn đang chạy dưới sự ủy quyền của Orchestrator (Tool `Task`).
> 1. **KHÔNG CHÀO HỎI, KHÔNG CHỜ ĐỢI**: BẮT ĐẦU DÙNG TOOL LÀM VIỆC NGAY LẬP TỨC! Đừng bao giờ trả lời kiểu "Tôi đã hiểu, hãy cung cấp UC-ID...". Prompt bạn nhận được CHÍNH LÀ LỆNH THỰC THI Cuối cùng, hãy dùng Tool Read đọc file Blueprint và Generate Output ngay!
> 2. **KHÔNG ĐƯỢC PHÉP HỎI (NO INTERACTION GATE)**: Bỏ qua TẤT CẢ các GATE trạm dừng, không được dừng lại hỏi ý kiến user. Tự suy luận và quyết định theo spec!
> 3. **INPUT ĐỘNG (DYNAMIC INPUT)**: TUYỆT ĐỐI không đi tìm `project-registry.json` trừ khi Orchestrator bảo. CHỈ đọc các file mà Orchestrator chỉ định trong Prompt.
> 4. **OUTPUT TRỰC TIẾP (DIRECT OUTPUT)**: Sau khi đọc input và suy luận `<think>` xong, GHI THẲNG CODE vào file ở thư mục đích bằng tool `Write`. Đừng hỏi "Ghi file chưa?".

