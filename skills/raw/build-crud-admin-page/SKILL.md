---
name: build-crud-admin-page
description: Xây dựng trang quản lý CRUD cho PayloadCMS collection. List view với filter, pagination. Form view với create, view, edit modes. Triggers: tạo trang admin, build CRUD page, tạo màn hình quản lý, new admin screen.
category: implementation
pipeline:
  stage_order: 10
  input_contract:
    - type: file
      path: "src/collections/{collection}.ts"
      required: false
  output_contract:
    - type: directory
      path: "src/components/screens/{collection}"
      format: directory
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


# Build CRUD Admin Page

Skill xây dựng trang quản lý CRUD cho PayloadCMS collection theo pattern BouquetScreen.

## Features

- List view với filter, pagination
- Form view với create, view, edit modes
- Tự động generate từ Payload collection config
