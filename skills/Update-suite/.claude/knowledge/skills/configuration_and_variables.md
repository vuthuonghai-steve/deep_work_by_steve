# ⚙️ Cấu hình & Biến Thay thế trong Skill

> **Cấp độ tài liệu:** L1 Core Reference & Technical Specification

Skill được cấu hình thông qua phần YAML frontmatter ở đầu tệp `SKILL.md` và phần nội dung Markdown đi kèm sau đó.

---

## 1. Phân loại Nội dung của Skill

Dựa trên cách thức bạn muốn kích hoạt, nội dung skill thường được chia làm hai loại:

### Tài liệu Tham chiếu (Reference Content)
Cung cấp kiến thức nền, quy ước dự án, style guide hoặc domain knowledge giúp Claude áp dụng xuyên suốt phiên làm việc. Nội dung này nạp inline để mô hình dễ dàng phối hợp cùng ngữ cảnh hội thoại.
```yaml
---
name: api-conventions
description: Các mẫu thiết kế API dành riêng cho dự án này
---
Khi viết các API endpoint:
- Luôn tuân thủ quy tắc đặt tên RESTful.
- Trả về mã lỗi định dạng nhất quán.
```

### Hướng dẫn Nhiệm vụ (Task Content)
Đưa ra chỉ dẫn chi tiết từng bước cho các tác vụ cụ thể như deploy, commit, chạy test. Những skill này thường được gọi thủ công bằng `/tên-skill` thay vì để tự động. Bạn nên đặt `disable-model-invocation: true` để tránh Claude tự chạy ngoài ý muốn.
```yaml
---
name: deploy
description: Thực hiện triển khai ứng dụng lên production
disable-model-invocation: true
---
Quy trình triển khai:
1. Chạy toàn bộ test suite.
2. Build ứng dụng.
3. Push bản build lên server.
```

---

## 2. Đặc tả YAML Frontmatter

Dưới đây là các trường cấu hình nâng cao trong phần frontmatter nằm giữa hai dấu `---` ở đầu `SKILL.md`:

| Trường | Bắt buộc | Mô tả |
| :--- | :--- | :--- |
| **`name`** | Không | Tên hiển thị của skill trên menu. Mặc định lấy tên thư mục. |
| **`description`** | Khuyên dùng | Mô tả tính năng và hoàn cảnh sử dụng. Claude dùng trường này để quyết định kích hoạt tự động. Giới hạn độ dài kết hợp với `when_to_use` là **1,536 ký tự**. |
| **`when_to_use`** | Không | Bổ sung ngữ cảnh kích hoạt (ví dụ: các cụm từ kích hoạt mẫu). Sẽ được nối tiếp vào sau `description`. |
| **`argument-hint`** | Không | Gợi ý tham số hiển thị khi gõ autocomplete trên dòng lệnh. Ví dụ: `[số-issue]` hoặc `[tên-file]`. |
| **`arguments`** | Không | Danh sách khai báo tên tham số để thay thế động thông qua biến `$tên_tham_số`. |
| **`disable-model-invocation`** | Không | Đặt thành `true` để ngăn Claude tự động kích hoạt skill này. Hữu ích cho các tác vụ thay đổi hệ thống hoặc chạy deploy. |
| **`user-invocable`** | Không | Đặt thành `false` để ẩn skill này khỏi menu `/` của người dùng. Dành cho các skill kiến thức chạy ngầm. |
| **`allowed-tools`** | Không | Danh sách các tool hệ thống mà Claude được quyền chạy tự động không cần xin phép khi skill này đang active. |
| **`disallowed-tools`** | Không | Các tool bị cấm sử dụng hoàn toàn trong thời gian skill hoạt động (ví dụ: cấm `AskUserQuestion`). |
| **`model`** | Không | Chỉ định model chạy riêng khi skill này hoạt động. |
| **`effort`** | Không | Mức độ nỗ lực suy nghĩ (`effort level`) của mô hình: `low`, `medium`, `high`, `xhigh`, `max`. |
| **`context`** | Không | Đặt thành `fork` để chạy cô lập trong một subagent riêng biệt. |
| **`agent`** | Không | Loại subagent sẽ thực thi khi sử dụng `context: fork` (ví dụ: `Explore`, `Plan`). |
| **`hooks`** | Không | Định nghĩa các hook cục bộ gắn với vòng đời của skill. |
| **`paths`** | Không | Danh sách các mẫu đường dẫn file (glob pattern) giới hạn phạm vi kích hoạt tự động của skill. |
| **`shell`** | Không | Chỉ định shell thực thi cho lệnh động: `bash` (mặc định) hoặc `powershell`. |

---

## 3. Quy tắc Đặt tên Lệnh Gọi Skill

Lệnh `/tên-lệnh` dùng để gọi thủ công một skill được quyết định bởi **vị trí lưu trữ** của skill đó chứ không phải trường `name` trong frontmatter:

*   **Dưới thư mục skill:** Lấy tên của thư mục chứa tệp `SKILL.md`.
    *   Ví dụ: `.claude/skills/deploy-staging/SKILL.md` → Gọi bằng `/deploy-staging`.
*   **Dưới thư mục commands cũ:** Lấy tên tệp bỏ phần mở rộng.
    *   Ví dụ: `.claude/commands/deploy.md` → Gọi bằng `/deploy`.
*   **Plugin skills:** Tên thư mục con và được namespaced bởi tên plugin.
    *   Ví dụ: `my-plugin/skills/review/SKILL.md` → Gọi bằng `/my-plugin:review`.

---

## 4. Các Biến Thay thế chuỗi Động (String Substitutions)

Skill hỗ trợ thay thế các giá trị động ngay tại thời điểm thực thi thông qua các biến hệ thống sau:

| Biến số | Mô tả chi tiết |
| :--- | :--- |
| **`$ARGUMENTS`** | Toàn bộ chuỗi tham số mà người dùng nhập vào sau lệnh gọi skill. |
| **`$ARGUMENTS[N]`** | Truy cập tham số cụ thể theo chỉ mục (0-indexed). Ví dụ: `$ARGUMENTS[0]` là tham số thứ nhất. |
| **`$N`** | Cú pháp viết tắt của `$ARGUMENTS[N]`. Ví dụ: `$0`, `$1`. |
| **`$tên_biến`** | Thay thế tham số theo tên đã được định nghĩa trong mảng `arguments` ở frontmatter. |
| **`${CLAUDE_SESSION_ID}`** | Mã định danh duy nhất của phiên làm việc hiện tại, rất tốt để tạo log hoặc file tạm độc lập. |
| **`${CLAUDE_EFFORT}`** | Mức độ suy nghĩ hiện tại của phiên (`low`, `medium`, `high`, `xhigh`, `max`). |
| **`${CLAUDE_SKILL_DIR}`** | Đường dẫn tuyệt đối dẫn đến thư mục chứa tệp `SKILL.md` của skill này. Cực kỳ quan trọng để chạy các script bổ trợ nằm trong cùng thư mục mà không lo ngại về thư mục làm việc hiện hành (`cwd`). |

<instructions>
must:
  - Nếu tham số chứa nhiều từ hoặc khoảng trắng, người dùng phải bọc giá trị bằng dấu nháy kép (ví dụ: `/my-skill "tham so 1" thamso2`) để mô hình phân tách chính xác giữa `$0` và `$1`.
  - Luôn sử dụng `${CLAUDE_SKILL_DIR}` thay vì đường dẫn tương đối khi gọi các script Python/Bash đi kèm trong thư mục skill.
</instructions>
