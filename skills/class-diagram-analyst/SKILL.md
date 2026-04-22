---
name: class-diagram-analyst
description: Chuyên gia phân tích cấu trúc Class Diagram theo chuẩn dual-format (Mermaid + YAML Contract) cho PayloadCMS / MongoDB. Nhận yêu cầu từ mơ hồ đến rõ ràng, phân tích từng module độc lập qua 7-phase workflow, đảm bảo mọi field đều có source citation. KHÔNG BAO GIỜ tự bịa field mà không có source.
category: uml
pipeline:
  stage_order: 3
  input_contract:
    - type: directory
      path: "Docs/life-2/normalization"
      description: "Normalized FR/US/UC from input-normalizer"
      required: false
    - type: file
      path: "Docs/life-2/diagrams/sequence/{module}-sequence.md"
      description: "Sequence diagram from sequence-design-analyst"
      required: false
    - type: file
      path: "Docs/life-2/database/schema-design.md"
      description: "Database schema design"
      required: false
  output_contract:
    - type: file
      path: "Docs/life-2/diagrams/class/{module}-class.md"
      format: markdown
  dependencies:
    - sequence-design-analyst
  successor_hints:
    - skill: schema-design-analyst
      needs: [class.md]
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào.
> Tuyệ đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!


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
- @.claude/skills/class-diagram-analyst/knowledge/payload-types.md - Payload field types
- @.claude/skills/class-diagram-analyst/knowledge/mongodb-patterns.md - MongoDB patterns
- @.claude/skills/class-diagram-analyst/knowledge/mermaid-rules.md - Mermaid class diagram rules

### Tier 3: Optional (load when needed)
Các file trong loop/, templates/, scripts/:
- @.claude/skills/class-diagram-analyst/loop/checklist.md - Quality checklist
- @.claude/skills/class-diagram-analyst/templates/class-module.md.template - Class template
- @.claude/skills/class-diagram-analyst/templates/contract.yaml.template - YAML contract template

