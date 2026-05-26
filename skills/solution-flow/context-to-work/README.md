# Context to Work — Quản lý ngữ cảnh trước khi fix

## 1. Mục đích

Lưu trữ ngữ cảnh (scope context document) cho các issue, bug, hoặc tính năng cần phân tích trước khi fix.

## 2. Cấu trúc thư mục

```
skills/solution-flow/context-to-work/
└── {feature-name}/
    └── README.md          # Scope context document
```

## 3. Khi nào sử dụng

| Trigger | Mục đích |
|---------|----------|
| Issue bug | Phân tích scope trước khi fix |
| Tính năng mới | Hiểu rõ yêu cầu trước khi code |
| Refactor | Đánh giá impact trước khi thay đổi |

## 4. Skill liên quan

| Skill | Chức năng |
|-------|-----------|
| context-before-fix | Phân tích scope, tạo context document |

## 5. Quy tắc

- **KHÔNG sửa code** — chỉ document findings
- Output: `docs/context-to-work/{feature-name}/`
- Bắt buộc phải có scope, constraints, acceptance criteria

## 6. Trigger Keywords

| Từ khóa | Action |
|----------|--------|
| "phan tich scope", "scope context" | Tạo context document |
| "trước khi fix", "trước khi code" | Phân tích trước |
| "debug", "bug", "issue" | Tạo context |

## 7. Liên quan

- **Skill:** `skills/rebuild/context-before-fix/SKILL.md`
- **Output location:** `docs/context-to-work/{feature-name}/`
