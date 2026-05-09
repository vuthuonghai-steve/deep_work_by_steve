# Clean Checklist — Validate Cleaned Prompts

> **Usage**: Run this checklist BEFORE outputting cleaned prompt to user.
> Reference: design.md §8 R5 + todo.md Phase 1.5

---

## 6-Item Validation Checklist

| # | Tiêu chí | Pass Condition | Fail → Action |
|---|----------|----------------|---------------|
| **1** | Goal rõ ràng? | Có `<goal>` 1-3 dòng, mục tiêu rõ ràng | Thêm/revise `<goal>` |
| **2** | Context đầy đủ? | Vừa đủ — không thừa, không thiếu. Nếu bổ sung phải cite source:line | Bổ sung hoặc cắt bớt context |
| **3** | Constraints đủ? | Có `<constraints>` với `<must_do>`/`<never_do>`/`<prefer>` nếu prompt có rules | Thêm constraints block |
| **4** | Output format rõ? | Có `<output_format>` nếu user yêu cầu format cụ thể | Thêm output_format block |
| **5** | Length acceptable? | Cleaned prompt **≤ 3x** prompt gốc | Rút gọn, bỏ redundant info |
| **6** | Tags đúng chuẩn? | Chỉ dùng tags từ `data/tag-reference.yaml`. Không tag tự phát minh | Thay bằng tag chuẩn |

---

## Pass Threshold

| Điểm | Result | Action |
|------|--------|--------|
| **≥ 5/6** | ✅ **ACCEPT** | Output cleaned prompt |
| **3–4/6** | ⚠️ **CONDITIONAL** | Output + note các items chưa đạt |
| **< 3/6** | ❌ **REJECT** | Quay lại restructure, sửa các fail items |

---

## Quick Scan

```
[ ] Item 1: Goal rõ ràng?
[ ] Item 2: Context đầy đủ?
[ ] Item 3: Constraints đủ?
[ ] Item 4: Output format rõ?
[ ] Item 5: Length ≤ 3x original?
[ ] Item 6: Tags đúng chuẩn?

Score: ___/6 → [ACCEPT / CONDITIONAL / REJECT]
```

---

## Anti-Pattern Detection

| ❌ Phát hiện | ✅ Sửa |
|-------------|--------|
| Không có `<goal>` | Thêm `<goal>` đầu tiên |
| Context quá dài (≥ 3x original) | Cắt redundant info |
| Tag không có trong tag-reference.yaml | Thay bằng tag chuẩn |
| Hardcoded path thay vì `${VAR}` | Đổi thành `${VAR}` syntax |
| NEVER rule không rõ ràng | Viết cụ thể: `NEVER [action]` |
