# Learn Checklist v2.0 — Automated Quality Gate

Cho session-learner v2.0 — verify tự động, không cần user confirm.

---

## Pre-Write Checks (Automated)

- [ ] Session có nội dung để extract
- [ ] Đã detect category phù hợp từ content
- [ ] Filename đúng format `YYYY-MM-DD.{session-name}.md`
- [ ] Knowledge folder tồn tại (auto-create nếu không)

---

## Content Checks (Automated)

- [ ] File chưa tồn tại (nếu trùng → append `_v2`)
- [ ] Markdown syntax đúng
- [ ] Không có placeholder chưa fill (`{...}`)
- [ ] File size <100KB
- [ ] Tiêu đề mô tả rõ nội dung
- [ ] Ngữ cảnh đầy đủ để hiểu sau này

---

## Safety Checks (Automated)

- [ ] Không ghi đè file có sẵn (auto-rename)
- [ ] Không chứa sensitive data (API keys, tokens đã redact)
- [ ] Ngữ cảnh đầy đủ để hiểu sau này

---

## Deliver (Auto)

Tự động output confirmation:

```
✅ Đã ghi: knowledge/{category}/{filename}.md
📊 Stats: N insights, M lessons, K patterns
📁 Related: {other files created in same session}
```

---

## Version History

- v2.0: 2026-05-09 — Simplified for 1-PASS execution, automated checks
- v1.0: 2025 — Original multi-gate design with user interactions