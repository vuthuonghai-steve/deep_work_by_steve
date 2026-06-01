---
# Context Management Strategy for skill-builder
# Usage: Load when token pressure > 50% or at Phase 1 boot
---

# Context Management — Token Budget Strategy

> **Usage**: Kỹ thuật tối ưu context window cho Builder. Load khi token pressure > 50% hoặc Phase 1 boot.

---

## Token Budget Levels

| Level | Threshold | Action | Loading Strategy |
|-------|-----------|--------|-----------------|
| **Green** | < 50% | Normal operation | Load Tier 2 theo load_when conditions |
| **Yellow** | 50-80% | Cautious | Chỉ load Tier 1 + Tier 2 cho phase hiện tại |
| **Red** | > 80% | Emergency | Compress completed phases, skip Tier 3 |

---

## Compression Techniques

### 1. Phase Completion Compression
Khi một phase hoàn thành, summarize thay vì giữ full content:
```
Phase 1 PREPARE: COMPLETED — Inputs read, inventory classified, confidence assessed.
Phase 3 BUILD: IN PROGRESS — Currently writing knowledge files.
```

### 2. Tier 3 Lazy Loading
- `templates/build-log.md.template` chỉ load ở Phase 5 DELIVER
- Nếu Red budget → tạo build-log từ memory thay vì load template

### 3. Knowledge Deduplication
- KHÔNG duplicate nội dung từ `../_shared/knowledge/framework.md`
- Dùng reference: "See framework.md §N" thay vì copy content

### 4. HTML Comment Removal
Khi build template files, xóa HTML comments (`<!-- -->`) ngay sau khi điền content.

---

## Monitoring Points

Builder PHẢI check token pressure tại:

| Checkpoint | Action if Red |
|-----------|--------------|
| Boot (after Tier 1) | Load context-management.md, reduce boot reads |
| Phase 3 start | Skip non-essential Tier 2, load only current phase needs |
| Phase 3 per-phase | Compress completed phases before loading next |
| Phase 4 start | Skip Tier 3 templates, use memory for checklist |
| Phase 5 start | Create build-log from summary, not template |

---

## Decision Tree

```
Token Pressure Check
├── < 50% (Green)
│   └── Load all Tier 2 as specified in load_when
├── 50-80% (Yellow)
│   └── Load Tier 1 + current phase Tier 2 only
│       └── Skip "nice to have" Tier 2 (error-recovery.md)
└── > 80% (Red)
    └── Compress completed phases to 1-line summaries
        └── Skip all non-essential Tier 2/3
            └── Build with minimal context, accept lower confidence
```

---

## Anti-Pattern: Context Overloading

❌ **KHÔNG làm**: Load tất cả Tier 2 files tại Boot Sequence.
✅ **LÀM ĐÚNG**: Mỗi phase chỉ load file mình cần theo `load_when`.
