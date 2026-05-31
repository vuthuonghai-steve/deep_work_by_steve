# Sự kiện Hook Cốt lõi (Core Session & Tool Events)

Tài liệu này đặc tả chi tiết các sự kiện hook cốt lõi liên quan đến quản lý phiên làm việc (Session) và quá trình thực thi công cụ (Tool Execution) trong Claude Code.

---

## 1. Mục lục Sự kiện

```yaml
core_events:
  session_lifecycle:
    - SessionStart: "Kích hoạt khi bắt đầu hoặc khôi phục một phiên làm việc."
    - Setup: "Kích hoạt một lần khi khởi tạo môi trường (ví dụ trong CI)."
    - SessionEnd: "Kích hoạt khi phiên làm việc kết thúc."
  user_interaction:
    - UserPromptSubmit: "Chạy ngay sau khi người dùng gửi prompt, trước khi mô hình xử lý."
    - UserPromptExpansion: "Chạy trước khi các lệnh mở rộng (như lệnh /) được phân giải."
  tool_execution_loop:
    - PreToolUse: "Chạy trước khi một công cụ được thực thi. Có quyền chặn lệnh."
    - PermissionRequest: "Chạy khi hộp thoại yêu cầu cấp quyền xuất hiện."
    - PermissionDenied: "Chạy khi hệ thống tự động từ chối quyền gọi công cụ trong chế độ auto."
    - PostToolUse: "Chạy sau khi cuộc gọi công cụ thành công."
    - PostToolUseFailure: "Chạy sau khi cuộc gọi công cụ gặp thất bại."
    - PostToolBatch: "Chạy sau khi toàn bộ một loạt công cụ chạy song song hoàn tất."
  assistant_response:
    - Stop: "Chạy khi Claude hoàn thành phản hồi và chuẩn bị trả quyền điều khiển."
    - StopFailure: "Chạy thay cho Stop khi lượt tương tác kết thúc do lỗi API."
```

---

## 2. Chi tiết Nhóm Phiên & Tương tác (Session & Prompt Events)

### SessionStart

Chạy khi phiên Claude Code mới bắt đầu hoặc được khôi phục.
* **Đặc điểm:** Tốt nhất để nạp các khóa API, cấu hình biến môi trường hoặc chạy các script kiểm tra khởi động.
* **Ghi nhận môi trường:** Có thể sử dụng file `$CLAUDE_ENV_FILE` để truyền biến môi trường vào phiên làm việc.

<hook_schema>
Payload dữ liệu đầu vào (JSON) của `SessionStart`:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/project/path",
  "permission_mode": "default",
  "hook_event_name": "SessionStart"
}
```
</hook_schema>

---

### Setup

Chạy khi khởi động Claude Code với các tham số đặc biệt cho việc cấu hình tự động như `--init-only`, `--init` hoặc `--maintenance` ở chế độ `-p`.
* **Đặc điểm:** Thường dùng để cài đặt môi trường tự động một lần trong CI hoặc các script triển khai dự án.

---

### UserPromptSubmit

Chạy ngay sau khi bạn nhấn Enter gửi prompt, trước khi Claude nhận được dữ liệu.
* **Đặc điểm:** Có thể chặn đứng yêu cầu của người dùng hoặc chỉnh sửa nội dung prompt trước khi gửi đi.
* **Khả năng chặn:** Trả về mã thoát `exit 2` hoặc JSON `{"decision": "block", "reason": "lý do chặn"}` sẽ chặn đứng turn tương tác.

<hook_schema>
```json
{
  "session_id": "abc123",
  "cwd": "/project/path",
  "hook_event_name": "UserPromptSubmit",
  "user_prompt": "Nội dung câu hỏi thực tế của người dùng"
}
```
</hook_schema>

---

### UserPromptExpansion

Chạy khi một lệnh tắt (như `/explain`) chuẩn bị được mở rộng thành prompt đầy đủ. Cho phép chặn hoặc điều chỉnh kết quả mở rộng.

---

## 3. Chi tiết Nhóm Thực thi Công cụ (Tool Execution Events)

### PreToolUse

Chạy ngay trước khi một công cụ (Bash, Read, Write...) được thực thi.
* **Khả năng đặc biệt:** Đây là sự kiện quan trọng nhất để xây dựng tường lửa bảo mật, lọc lệnh shell nguy hiểm.
* **Matcher:** Lọc theo tên công cụ (ví dụ: `Bash`, `Write`).

<hook_schema>
Dữ liệu đầu vào:
```json
{
  "session_id": "abc123",
  "cwd": "/project/path",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf build/",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_unique_id"
}
```
</hook_schema>

Để kiểm soát quyền chạy công cụ, hook có thể trả về JSON chỉ định cụ thể quyết định phân quyền (`permissionDecision`):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Từ chối thực thi do lệnh không an toàn."
  }
}
```

Các giá trị hợp lệ của `permissionDecision`:
- `"allow"`: Tự động cho phép chạy công cụ (bỏ qua hỏi ý kiến người dùng).
- `"deny"`: Chặn đứng công cụ và báo lỗi về cho Claude.
- `"default"`: Tiếp tục quy trình kiểm tra quyền mặc định của phiên.

---

### PermissionRequest

Chạy khi một hộp thoại yêu cầu cấp quyền hiển thị cho người dùng. Cho phép tự động hóa câu trả lời dựa trên logic tùy biến.

---

### PermissionDenied

Chạy khi công cụ bị hệ thống phân loại bảo mật (Auto Mode Classifier) chặn trong chế độ chạy tự động (`auto`).

* **Khả năng xử lý:** Cho phép hướng dẫn Claude thử lại nếu phù hợp bằng cách trả về đầu ra JSON:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

---

### PostToolUse

Chạy sau khi một công cụ thực thi thành công và trả về kết quả.
* **Đặc điểm:** Thích hợp để tự động kiểm tra cú pháp (linting) sau khi file được ghi, hoặc phân tích kết quả test.
* **Đầu vào bổ sung:** Nhận thêm trường `tool_output` chứa dữ liệu phản hồi của công cụ.

---

### PostToolUseFailure

Chạy khi công cụ thất bại (lỗi lệnh Bash, file không tồn tại...).
* **Đặc điểm:** Nhận trường `error` mô tả lỗi và `is_interrupt` (nếu người dùng bấm Ctrl+C để ngắt).
* **Đầu ra hỗ trợ:** Có thể trả về `additionalContext` để giải thích thêm cho Claude về nguyên nhân lỗi nhằm giúp nó tự sửa sai tốt hơn.

---

### PostToolBatch

Chạy duy nhất một lần sau khi toàn bộ một loạt công cụ chạy song song (Parallel Tool Calls) hoàn tất, trước khi Claude đưa lời gọi tiếp theo lên mô hình.
* **Đầu vào:** Nhận danh sách mảng `tool_calls` chứa thông tin của tất cả các công cụ trong batch.

---

## 4. Nhóm Kết thúc Hội thoại & Session

### Stop

Chạy khi Claude đã hoàn thành phản hồi toàn bộ và chuẩn bị nhường quyền tương tác lại cho người dùng.

* **Kiểm soát Quyết định (Stop Loop):** Đây là nơi bạn có thể kiểm tra xem nhiệm vụ thực sự đã hoàn thành chưa (ví dụ: chạy test suite). Nếu chưa đạt tiêu chí, bạn có thể **chặn dừng** và ép Claude tiếp tục làm việc:
  
```json
{
  "decision": "block",
  "reason": "Bộ kiểm thử vẫn đang báo lỗi. Hãy đọc log lỗi và sửa tiếp."
}
```

* **Dữ liệu đầu vào đặc biệt:** Nhận `last_assistant_message` (nội dung câu trả lời cuối của Claude), `background_tasks` (các tác vụ nền đang chạy) và `session_crons` (các lịch trình cron đã lên lịch).

---

### StopFailure

Chạy thay cho sự kiện `Stop` khi lượt tương tác bị dừng đột ngột do lỗi API hệ thống (hết hạn token, lỗi máy chủ, vượt giới hạn rate limit).
* **Đặc điểm:** Được dùng chủ yếu cho việc ghi log giám sát và thông báo sự cố ra bên ngoài. Không thể can thiệp luồng quyết định của Claude.

---

### SessionEnd

Chạy khi phiên làm việc Claude Code kết thúc.
* **Đầu vào:** Trường `reason` ghi rõ nguyên nhân kết thúc:
  - `clear`: Dọn dẹp phiên bằng lệnh `/clear`.
  - `resume`: Chuyển đổi phiên thông qua `/resume`.
  - `logout`: Đăng xuất tài khoản.
  - `prompt_input_exit`: Người dùng thoát bằng cách bấm Ctrl+D/Ctrl+C tại dòng nhập prompt.
  - `bypass_permissions_disabled`: Chế độ bỏ qua phân quyền bị tắt.
  - `other`: Các nguyên nhân khác.
* **Thời gian giới hạn (Timeout):** Mặc định có 1.5 giây để thực thi dọn dẹp. Có thể nâng lên tối đa 60 giây bằng cấu hình `timeout` trong settings.
