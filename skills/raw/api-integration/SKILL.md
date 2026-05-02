---
name: api-integration
description: Skill tích hợp API backend vào frontend. Sử dụng khi cần (1) nghiên cứu API endpoint, (2) phân tích cấu trúc request/response, (3) ghep API vào frontend, (4) đồng bộ cấu trúc data khi backend thay đổi. Skill này nên được sử dụng khi người dùng cung cấp đường dẫn file API backend hoặc yêu cầu làm việc với API.
category: implementation
pipeline:
  stage_order: 13
  input_contract:
    - type: file
      path: "src/app/api/{module}/route.ts"
      required: true
  output_contract:
    - type: file
      path: "src/lib/api/{module}.ts"
      format: typescript
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


# API Integration

Skill tích hợp API backend vào frontend.
