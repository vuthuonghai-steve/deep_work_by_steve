---
name: screen-structure-checker
description: Skill kiểm tra cấu trúc thư mục screens theo kiến trúc quản lý tập trung. Sử dụng khi cần (1) audit cấu trúc screen mới tạo, (2) kiểm tra toàn bộ screens trong dự án, (3) tìm các vi phạm naming convention, (4) phát hiện file cần refactor do quá lớn.
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
- [references/architecture-rules.md](references/architecture-rules.md) - Quy tắc kiến trúc screens

### Tier 3: Optional (load when needed)
- @.claude/skills/screen-structure-checker/scripts/check_structure.py - Script kiểm tra cấu trúc

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào. 
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!


# Screen Structure Checker

Skill này kiểm tra cấu trúc thư mục của các screen components để đảm bảo tuân thủ kiến trúc quản lý tập trung.

## Mục Đích

- **Audit cấu trúc**: Quét và đánh giá cấu trúc thư mục screens
- **Phát hiện vi phạm**: Tìm các screen không tuân theo kiến trúc chuẩn
- **Đề xuất cải thiện**: Gợi ý cách sửa cho từng vi phạm
- **Báo cáo chi tiết**: Xuất kết quả dạng dễ đọc

## Khi Nào Sử Dụng

Skill này nên được trigger khi:
- Người dùng hỏi về "kiểm tra cấu trúc screen"
- Người dùng yêu cầu "audit screens" hoặc "validate structure"
- Cần review code quality của screens
- Tạo screen mới và muốn kiểm tra đúng convention

## Cách Sử Dụng

### 1. Kiểm Tra Một Screen Cụ Thể

Chạy script với đường dẫn đến thư mục screen:

```bash
python3 scripts/check_structure.py /path/to/screens/ScreenName
```

**Output mẫu:**
```
📊 Screen Structure Report: home-screen
========================================

✅ PASSED (4/6 rules)
├─ ✅ Has index.tsx or main component
├─ ✅ Has components/ directory
├─ ✅ Has hooks/ directory
├─ ⚠️ Missing types/ directory
├─ ✅ Correct naming convention
└─ ⚠️ 2 files exceed 200 lines

🔧 Recommendations:
1. Create types/ directory for TypeScript interfaces
2. Refactor index.tsx (476 lines) - consider splitting
```

### 2. Kiểm Tra Toàn Bộ Screens

```bash
python3 scripts/check_structure.py /path/to/screens --all
```

### 3. Xuất Báo Cáo JSON

```bash
python3 scripts/check_structure.py /path/to/screens/ScreenName --json
```

## Các Rules Kiểm Tra

| Rule | Mô tả | Severity |
|------|-------|----------|
| `has_main_component` | Có `index.tsx` hoặc `{ScreenName}.tsx` | ❌ Error |
| `has_components_dir` | Có thư mục `components/` | ⚠️ Warning |
| `has_hooks_dir` | Có thư mục `hooks/` | ⚠️ Warning |
| `has_types_dir` | Có thư mục `types/` | 💡 Info |
| `naming_convention` | File/folder đúng convention | ❌ Error |
| `file_size_limit` | Không có file > 200 lines | ⚠️ Warning |
| `barrel_exports` | Có `index.ts` trong sub-dirs | 💡 Info |

## Kiến Trúc Chuẩn

Tham khảo chi tiết tại `references/architecture-rules.md`.

```text
{ScreenName}/
├── index.tsx              # Component chính (BẮT BUỘC)
├── components/            # Sub-components
│   ├── cards/
│   ├── sections/
│   └── index.ts           # Barrel export
├── hooks/                 # Custom hooks
│   ├── useScreenData.ts
│   └── index.ts
├── types/                 # TypeScript types
├── utils/                 # Helper functions
├── constants/             # Constants
└── README.md              # Documentation
```

## Tích Hợp Với Workflow

Skill này hoạt động tốt với:
- `/implement-workflow`: Verify screen mới tạo đúng cấu trúc
- `/ultra-think`: Phân tích chi tiết các vi phạm
- `/ui-ux-pro-max`: Đảm bảo components được tổ chức đúng
