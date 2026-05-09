# Session Extraction Guide

Hướng dẫn cách trích xuất kiến thức từ session chat.

---

## Extraction Principles

1. **Chỉ trích xuất giá trị** — Không phải mọi thứ đều worth saving
2. **Ngữ cảnh quan trọng** — Ghi lại WHY, không chỉ WHAT
3. **Actionable** — Kiến thức phải useful, không chỉ interesting
4. **Unique** — Ưu tiên insights không có sẵn ở nơi khác

---

## Categories & What to Extract

### `experience/` — Personal Lessons

| Extract | Ví dụ |
|---------|-------|
| Mistake + Fix | "Tôi đã sai ở chỗ X, cách sửa là Y" |
| Discovery | "Tôi phát hiện ra rằng X" |
| Insight | "X có vẻ đúng, nhưng thực ra Y mới đúng" |
| Workflow improvement | "Cách cũ X không tốt, cách mới Y hiệu quả hơn" |

### `projects/` — Project Knowledge

| Extract | Ví dụ |
|---------|-------|
| Architecture decision | "Chọn X thay vì Y vì Z" |
| Technical approach | "Cách implement feature này là..." |
| Gotchas | "Cẩn thận X — nó gây ra Y" |
| Dependencies | "Cần X trước khi làm Y" |

### `notes/` — Quick Notes

| Extract | Ví dụ |
|---------|-------|
| TODO items | "Cần làm X" |
| Questions | "Tại sao X lại hoạt động như vậy?" |
| Ideas | "Thử X xem sao" |
| Reminders | "X — đừng quên" |

### `programming/` — Technical Patterns

| Extract | Ví dụ |
|---------|-------|
| Command | "Lệnh `X` làm Y" |
| Pattern | "Pattern X giải quyết vấn đề Y" |
| Tool usage | "Cách dùng tool X hiệu quả" |
| Code snippet | "Đoạn code này làm X" |

### `resources/` — References

| Extract | Ví dụ |
|---------|-------|
| URL | "Link này hữu ích cho X" |
| Documentation | "Doc của X có section về Y" |
| Tool | "Tool X hữu ích cho Y" |

---

## Extraction Process

### Step 1: Identify Candidates

Scan messages for:

- 🔍 Problem-solving exchanges
- 💡 Lightbulb moments ("aha!", "tôi hiểu rồi")
- ⚠️ Warnings or cautions
- ✅ Confirmations of approach
- 🔧 Tool or command usage
- 📚 Explanations or teaching moments

### Step 2: Evaluate Value

Ask:

- Đây có phải knowledge mới không?
- Nó sẽ hữu ích trong tương lai không?
- Có thể action được không?

### Step 3: Capture Context

For each valid extraction:

- **What**: Nội dung chính
- **Why**: Tại sao nó quan trọng
- **When**: Trong bối cảnh nào
- **Source**: Message nào trong session

### Step 4: Structure

Apply template từ `templates/knowledge-entry.template`

---

## Anti-Patterns

| ❌ Don't Extract | ✅ Do Instead |
|-----------------|--------------|
| Generic info có sẵn ở docs | Chỉ extract nếu có context cụ thể |
| Nội dung quá dài (>500 words) | Tóm tắt, giữ essence |
| Duplicate kiến thức đã có | Check trước, skip nếu trùng |
| Opinion mà không có basis | Ghi rõ đây là opinion, không phải fact |

---

## Quality Checklist

- [ ] Mỗi entry có ngữ cảnh đầy đủ
- [ ] Không trùng lặp với file có sẵn
- [ ] Markdown syntax đúng
- [ ] File size <100KB
- [ ] Tiêu đề mô tả rõ nội dung
