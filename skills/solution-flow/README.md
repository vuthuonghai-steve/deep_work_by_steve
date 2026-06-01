# Solution Flow — Quản lý Hướng dẫn Skill cho Agent

## 1. Mục đích

Thư mục này quản lý các **hướng dẫn** cho từng bộ skill hoặc nhóm skill phục vụ một mục đích/quy trình cụ thể.

## 2. Cấu trúc

```
skills/solution-flow/
├── README.md                      # File này — chỉ mục tổng
├── skill-builder-suite/           # Bộ 4 skill xây dựng agent skill
│   └── README.md
├── knowledge-extraction/          # Trích xuất kiến thức từ repo/document
│   └── README.md
├── context-to-work/              # Phân tích scope trước khi fix
│   └── README.md
└── micro-skill-suite/            # Micro-skills được tạo từ skill-builder
    └── README.md
```

## 3. Danh sách Solution Flows

| Thư mục | Mục đích | Skills liên quan |
|----------|-----------|-----------------|
| skill-builder-suite | Xây dựng agent skill mới | explorer, architect, planner, builder |
| knowledge-extraction | Trích xuất kiến thức từ repo/document | source-gatherer, format-converter |
| context-to-work | Phân tích scope trước khi fix | context-before-fix |
| micro-skill-suite | Quản lý micro-skills đã tạo | skill-builder |

## 4. Nguyên tắc

1. **Mỗi solution flow** có README.md mô tả:
   - Mục đích
   - Skills liên quan
   - Pipeline/workflow
   - Trigger keywords
   - Vị trí skills

2. **Khi tạo skill mới** qua skill-builder:
   - Tạo thư mục mới trong `solution-flow/`
   - Viết README.md theo mẫu
   - Cập nhật file này

3. **Khi quên** — Đọc file này để biết:
   - Có những solution flows nào
   - Mỗi flow làm gì
   - Dùng keywords nào để kích hoạt

## 5. Trigger Keywords Map

| Từ khóa | Solution Flow |
|----------|---------------|
| "tao skill", "xay dung skill", "bo skill" | skill-builder-suite |
| "thiet ke skill", "design", "mermaid" | skill-builder-suite |
| "trich xuat kien thuc", "knowledge extraction" | knowledge-extraction |
| "clone repo", "doc pdf", "markdown chuan" | knowledge-extraction |
| "phan tich scope", "truoc khi fix" | context-to-work |
| "debug", "bug", "issue" | context-to-work |
| "micro-skill", "skill con" | micro-skill-suite |

## 6. Mở rộng

Khi bổ sung solution flow mới:
1. Tạo thư mục tại `skills/solution-flow/{new-flow}/`
2. Viết README.md theo cấu trúc chuẩn
3. Cập nhật bảng tại mục 3

## 7. Liên quan

- **Root Agent Guide:** `skills/rebuild/AGENT.md`
- **Skills Source:** `skills/rebuild/`
- **Shared Framework:** `skills/rebuild/_shared/knowledge/framework.md`
