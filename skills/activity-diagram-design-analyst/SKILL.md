---
name: activity-diagram-design-analyst
description: Chuyên gia phân tích và thiết kế sơ đồ Activity Diagram (High-Fidelity) theo tư duy Clean Architecture (B-U-E). Phản biện logic, phát hiện Deadlocks và đảm bảo tính nhất quán giữa nghiệp vụ và thiết kế.
category: uml
pipeline:
  stage_order: 4
  input_contract:
    - type: file
      path: "Docs/life-2/diagrams/flow/{module}-flow.md"
      required: false
  output_contract:
    - type: file
      path: "Docs/life-2/diagrams/activity/{module}-activity.md"
      format: markdown
  dependencies:
    - flow-design-analyst
  successor_hints:
    - skill: schema-design-analyst
      needs: [activity.md]
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào.
> Tuyệ không được đoán ngữ cảnh hoặc tự bt đốiịa ra kiến thức nếu chưa tự mình gọi tool đọc file!


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
- @.claude/skills/activity-diagram-design-analyst/knowledge/clean-architecture-lens.md - Clean Architecture B-U-E
- @.claude/skills/activity-diagram-design-analyst/knowledge/activity-uml-rules.md - Activity diagram rules
- @.claude/skills/activity-diagram-design-analyst/knowledge/refactor-risk-patterns.md - Refactor risk patterns

### Tier 3: Optional (load when needed)
Các file trong loop/, templates/, scripts/:
- @.claude/skills/activity-diagram-design-analyst/loop/checklist.md - Quality checklist
- @.claude/skills/activity-diagram-design-analyst/templates/activity-mode-a.template.md - Activity mode A template
- @.claude/skills/activity-diagram-design-analyst/templates/activity-mode-b.template.md - Activity mode B template

