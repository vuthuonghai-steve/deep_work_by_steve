---
name: prompt-improver
description: Skill cải thiện và tối ưu hóa prompt cho AI Agent. Phân tích prompt hiện tại, xác định vấn đề, đề xuất cải thiện, cung cấp templates. Sử dụng khi: (1) prompt không rõ ràng, (2) AI hiểu sai yêu cầu, (3) cần tối ưu prompt phức tạp, (4) cần tạo prompt mới chất lượng cao. Trigger: /prompt, improve prompt, fix prompt, optimize prompt, prompt không hiệu quả.
category: utility
pipeline:
  stage_order: 0
  input_contract: []
  output_contract: []
  dependencies: []
---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file)

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
- (skill chưa có knowledge files - cần xem xét tạo thêm)

### Tier 3: Optional (load when needed)
- (không có folder bổ sung)

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào. 
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!


# Prompt Improver

Skill cải thiện và tối ưu hóa prompt cho AI Agent.

## Features

- Phân tích prompt hiện tại
- Xác định vấn đề
- Đề xuất cải thiện
- Cung cấp templates
