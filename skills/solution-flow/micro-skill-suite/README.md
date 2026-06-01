# Micro Skill Suite — Quản lý micro-skills đã tạo

## 1. Mục đích

Lưu trữ thông tin về các **micro-skills** được tạo ra từ bộ skill-builder-suite.

## 2. Micro-skill là gì?

Micro-skill là skill nhỏ, tập trung vào một nhiệm vụ cụ thể, được phân rã từ skill lớn hơn.

## 3. Cấu trúc thư mục

```
skills/solution-flow/micro-skill-suite/
└── {micro-skill-name}/
    ├── README.md              # Thông tin micro-skill
    ├── trigger-keywords.md    # Từ khóa kích hoạt
    └── related-skills.md       # Skills liên quan
```

## 4. Khi nào tạo micro-skill?

| Điều kiện | Hành động |
|------------|------------|
| SCS score > 3.0 | Phân rã thành micro-skills |
| Có điểm 5 (ngưỡng đỏ) | Bắt buộc phải phân rã |
| Skill quá phức tạp | Chia thành nhiều micro-skills |

## 5. Trigger Keywords

| Từ khóa | Action |
|----------|--------|
| "tao micro-skill" | Tạo micro-skill mới |
| "phan ra skill", "decompose skill" | Phân rã skill |
| "micro-skill" | Truy cập micro-skill |

## 6. Pipeline phân rã

```
Skill lớn (SCS > 3.0)
        ↓
┌───────────────────┐
│ skill-explorer     │ ← Đánh giá độ phức tạp
└────────┬──────────┘
         ↓
┌───────────────────┐
│ skill-architect    │ ← Thiết kế micro-skills
└────────┬──────────┘
         ↓
┌───────────────────┐
│ skill-planner      │ ← Lập kế hoạch
└────────┬──────────┘
         ↓
┌───────────────────┐
│ skill-builder      │ ← Tạo micro-skills
└────────┬──────────┘
         ↓
micro-skill-suite/
```

## 7. Tiêu chuẩn micro-skill

| Tiêu chí | Yêu cầu |
|-----------|----------|
| Đơn nhiệm | Mỗi micro-skill làm một việc |
| Tái sử dụng | Có thể dùng trong nhiều pipeline |
| Kích hoạt | Có trigger keywords riêng |
| Giao diện | Có input/output contract rõ ràng |

## 8. Liên quan

- **Skill Builder Suite:** `skills/solution-flow/skill-builder-suite/README.md`
- **Root Guide:** `skills/rebuild/AGENT.md`
