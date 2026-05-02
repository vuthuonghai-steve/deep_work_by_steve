---
name: sequence-design-analyst
description: Chuyên gia phân tích và thiết kế Sequence Diagram (UML) chuẩn Mermaid. Kích hoạt khi user yêu cầu vẽ sơ đồ tuần tự, phân tích luồng tương tác, hoặc thiết kế message flow cho chức năng. Tự động nghiên cứu codebase để đảm bảo tính thực tế.
category: uml
pipeline:
  stage_order: 2
  input_contract:
    - type: directory
      path: "Docs/life-2/normalization"
      description: "Normalized FR/US/UC from input-normalizer"
      required: false
    - type: file
      path: "Docs/life-2/diagrams/flow/{module}-flow.md"
      description: "Flow diagram from flow-design-analyst"
      required: false
    - type: file
      path: "Docs/life-2/api/api-spec.md"
      description: "API specification"
      required: false
  output_contract:
    - type: file
      path: "Docs/life-2/diagrams/sequence/{module}-sequence.md"
      format: markdown
  dependencies:
    - flow-design-analyst
  successor_hints:
    - skill: class-diagram-analyst
      needs: [sequence.md]
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
>
> **TRƯỚC KHI BẮT ĐẦU BẤT KỲ TASK NÀO, BẠN PHẢI:**
> 1. Sử dụng tool `Glob` để QUÉT thư mục `knowledge/` và liệt kê tất cả files
> 2. Sử dụng @import để LOAD các file sau VÀO CONTEXT:
>    - @.claude/skills/sequence-design-analyst/knowledge/uml-rules.md
>    - @.claude/skills/sequence-design-analyst/knowledge/sequence-preparation.md
> 3. CHỈ SAU KHI ĐỌC xong mới được phép tiếp tục với task chính
>
> **NẾU KHÔNG DÙNG @IMPORT → AGENT SẼ LÀM VIỆC THIẾU CONTEXT VÀ SAI!**


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

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc - dùng @import)
- @.claude/skills/sequence-design-analyst/knowledge/uml-rules.md
- @.claude/skills/sequence-design-analyst/knowledge/sequence-preparation.md
- @.claude/skills/sequence-design-analyst/knowledge/project-patterns.md

### Tier 3: Optional (load when needed - dùng @import)
- @.claude/skills/sequence-design-analyst/loop/checklist.md
- @.claude/skills/sequence-design-analyst/templates/auth-flow.mmd
- @.claude/skills/sequence-design-analyst/templates/crud-flow.mmd
- @.claude/skills/sequence-design-analyst/templates/logic-flow.mmd

