# 🚀 Hướng dẫn Bắt đầu & Vòng đời của Skill

> **Cấp độ tài liệu:** L1 Working Policy & Walkthrough

Skill giúp bạn mở rộng năng lực của Claude. Bằng cách viết một tệp `SKILL.md` với các hướng dẫn chuyên biệt, Claude sẽ nạp nó vào hộp công cụ của mình và kích hoạt tự động khi cần thiết, hoặc bạn có thể gọi thủ công bằng `/tên-skill`.

---

## 1. Xây dựng Skill Đầu tiên của Bạn

Chúng ta sẽ tạo một skill tên là `summarize-changes` nhằm tự động tóm tắt các thay đổi chưa commit trong Git repo, chỉ ra các rủi ro kỹ thuật. Skill này sẽ kéo trực tiếp output của `git diff` vào prompt của Claude trước khi mô hình đọc, giúp câu trả lời cực kỳ chính xác.

### Các Bước Thực hiện

<context>
#### Bước 1: Tạo thư mục chứa skill
Tạo thư mục cho skill trong thư mục cá nhân (Personal Skills). Thư mục này giúp skill khả dụng trên tất cả các dự án của bạn:
```bash
mkdir -p ~/.claude/skills/summarize-changes
```

#### Bước 2: Viết tệp SKILL.md
Mỗi skill yêu cầu một tệp `SKILL.md` gồm hai phần: YAML frontmatter (nằm giữa hai dấu `---`) định nghĩa khi nào tự động chạy, và nội dung Markdown chứa hướng dẫn mà Claude sẽ thực hiện.

Lưu nội dung sau vào `~/.claude/skills/summarize-changes/SKILL.md`:
```yaml
---
description: Tóm tắt các thay đổi chưa committed trong Git và gắn cờ cảnh báo rủi ro. Kích hoạt khi người dùng hỏi có gì thay đổi, muốn tạo commit message, hoặc yêu cầu xem diff của họ.
---

## Các thay đổi hiện tại

!`git diff HEAD`

## Hướng dẫn

Hãy tóm tắt các thay đổi ở trên thành 2 hoặc 3 gạch đầu dòng ngắn gọn. Sau đó, liệt kê bất kỳ rủi ro nào bạn phát hiện (ví dụ: thiếu xử lý lỗi, giá trị hardcoded, hoặc các file test cần được cập nhật). Nếu diff trống, thông báo rằng không có thay đổi nào chưa commit.
```

> **Lưu ý cú pháp:** Dòng `` !`git diff HEAD` `` sử dụng [Cơ chế Nhúng ngữ cảnh Động (Dynamic Context Injection)](./advanced_patterns.md). Claude Code sẽ thực thi lệnh này và thay thế bằng output thực tế trước khi gửi nội dung cho mô hình.
</context>

---

## 2. Nơi Lưu trữ Skill & Thứ tự Ưu tiên

Vị trí lưu trữ quyết định phạm vi áp dụng và đối tượng có quyền sử dụng:

| Phạm vi | Đường dẫn lưu trữ | Áp dụng cho | Thứ tự ưu tiên |
| :--- | :--- | :--- | :--- |
| **Enterprise** | Khai báo qua cài đặt hệ thống | Toàn bộ lập trình viên trong tổ chức. | Cao nhất (Ghi đè tất cả) |
| **Personal** | `~/.claude/skills/<tên-skill>/SKILL.md` | Mọi dự án cục bộ của bạn. | Trung bình (Ghi đè Project) |
| **Project** | `.claude/skills/<tên-skill>/SKILL.md` | Chỉ dự án hiện tại. | Thấp (Bị Personal ghi đè) |
| **Plugin** | `<plugin>/skills/<tên-skill>/SKILL.md` | Nơi plugin được kích hoạt. | Namespaced dạng `plugin:skill` |

---

## 3. Cơ chế Khám phá Động & Phát hiện Thay đổi thời gian thực

### Phát hiện Thay đổi Nóng (Live Change Detection)
Claude Code theo dõi (watch) các thư mục chứa skill theo thời gian thực. Khi bạn thêm mới, sửa đổi hoặc xóa bất kỳ skill nào dưới thư mục `~/.claude/skills/` hoặc `.claude/skills/` của project, thay đổi sẽ **có hiệu lực ngay lập tức** trong phiên chat hiện tại mà không cần khởi động lại.

> [!WARNING]
> Nếu tại thời điểm khởi động phiên làm việc, thư mục chứa skill chưa hề tồn tại trên hệ thống, bạn cần tắt và khởi động lại Claude Code sau khi tạo thư mục để hệ thống kích hoạt bộ lắng nghe thay đổi (watcher).

### Tự động Khám phá trong Monorepo
Đối với các dự án lớn dạng Monorepo, Claude Code sở hữu cơ chế khám phá phân tầng thông minh:
*   **Đi từ dưới lên (Bottom-up):** Skill sẽ được nạp từ `.claude/skills/` tại thư mục bạn đang đứng, đồng thời quét ngược lên các thư mục cha cho đến gốc repository.
*   **Nạp theo yêu cầu (On-demand nested):** Khi bạn mở và chỉnh sửa một tệp tin nằm sâu trong cấu trúc Monorepo (ví dụ: `packages/frontend/src/App.tsx`), Claude Code sẽ tự động khám phá và nạp các skill nằm trong `packages/frontend/.claude/skills/` để áp dụng riêng cho ngữ cảnh của package đó.

---

## 4. Cấu trúc Chuẩn của một Skill Package

Mỗi skill là một thư mục tự chứa (Self-contained) với tệp `SKILL.md` đóng vai trò là điểm vào (entrypoint) chính:

```text
my-skill/
├── SKILL.md           # Hướng dẫn chính & Frontmatter (Bắt buộc)
├── template.md        # Tệp mẫu để Claude điền thông tin (Tùy chọn)
├── examples/
│   └── sample.md      # Output mẫu để làm tiêu chuẩn định dạng (Tùy chọn)
└── scripts/
    └── validate.sh    # Script chạy kiểm định mà Claude có thể thực thi (Tùy chọn)
```

<instructions>
must:
  - Tệp `SKILL.md` phải là L0 anchor và bắt buộc phải có.
  - Phải tách các tài liệu tham khảo cồng kềnh, API spec hoặc script kiểm định sang các file bổ trợ riêng biệt trong package để tránh phình token.
</instructions>
