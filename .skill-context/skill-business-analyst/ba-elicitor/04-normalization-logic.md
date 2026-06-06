---
extracted_from: "ba-elicitor-analysis.md §4"
source: "file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/ba-elicitor-analysis.md"
purpose: "Input normalization & output generation logic cho ba-elicitor"
---

## 1. Input Normalization

**Nhiệm vụ**: Nhận raw text từ `<user_skill_request>` → bóc tách cấu trúc yêu cầu. [TỪ analysis §4.1]

- Loại bỏ văn cảnh thừa (chào hỏi, giải thích ko cần thiết)
- Phân tách thực thể → ánh xạ vào `input-schema.yaml`
- Đầu ra: normalized fields (skill_name, core_objective, environment)

**Input boundary**: Bọc raw input trong `<user_skill_request>...</user_skill_request>` [TỪ analysis §6.1]

## 2. Proactive Clarification (Phản biện Chủ động)

**Nhiệm vụ**: Phát hiện yêu cầu cảm tính → chuyển thành metrics định lượng. [TỪ analysis §4.2]

**Kỹ thuật**:
- Quét văn bản tìm tính từ mô tả hiệu năng/hành vi [TỪ analysis §4.2]
- Ánh xạ → metrics: latency, throughput, success rate, token usage, security gates
- Nếu ko lượng hóa được → gắn `[CẦN LÀM RÕ]` + sinh câu hỏi

## 3. Structured Output Generation

**Nhiệm vụ**: Tạo `elicitation-report.md` theo template chuẩn. [TỪ analysis §4.3]

**Yêu cầu**:
- Zero information loss — bảo toàn ngữ nghĩa
- Trace tags đầy đủ (`[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`)
- Đúng format: Markdown + YAML frontmatter

## 4. Skills Flow

```
RawInput → 1. Chuẩn hóa → 2. Phân tích Khoảng trống → 3. Sinh 5W1H → 4. Đóng gói Report
```
[TỪ analysis §4 mermaid]
