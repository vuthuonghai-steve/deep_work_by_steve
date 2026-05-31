# Tính năng Hook Nâng cao (Prompt, Agent & Async Hooks)

Tài liệu này đặc tả các tính năng nâng cao của Claude Code hooks bao gồm Hook dựa trên Prompt (Prompt-based), Hook dựa trên Agent (Agent-based) và chạy Hook chạy ngầm không chặn (Async Hooks).

---

## 1. Hook dựa trên Prompt (Prompt-based Hooks)

Bên cạnh việc thực thi lệnh shell, Claude Code hỗ trợ các hook dựa trên mô hình ngôn ngữ (`type: "prompt"`). Thay vì chạy mã script, loại hook này gửi trực tiếp dữ liệu sự kiện cùng với một prompt chỉ thị tới một mô hình Claude (mặc định là Claude Haiku) để đưa ra đánh giá nhanh.

### Cơ chế hoạt động:
1. Khi sự kiện xảy ra, Claude Code đóng gói dữ liệu đầu vào JSON.
2. Gửi dữ liệu này kèm prompt chỉ thị của bạn tới Claude.
3. Mô hình trả về kết quả dạng JSON có cấu trúc chứa quyết định cho phép (`ok: true`) hoặc chặn (`ok: false`).
4. Claude Code tự động xử lý và áp dụng quyết định này.

### Cấu hình Prompt Hook

Thiết lập `type` thành `"prompt"` và điền nội dung chỉ thị trong trường `prompt`. Sử dụng từ khóa giữ chỗ `$ARGUMENTS` để nhúng toàn bộ dữ liệu đầu vào JSON của sự kiện vào prompt.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Hãy đánh giá xem Claude đã hoàn thành toàn bộ công việc chưa dựa trên ngữ cảnh này: $ARGUMENTS. Trả về quyết định."
          }
        ]
      }
    ]
  }
}
```

### Các trường cấu hình:

| Trường | Bắt buộc | Mô tả |
| :--- | :--- | :--- |
| `type` | **Có** | Phải là `"prompt"`. |
| `prompt` | **Có** | Nội dung prompt chỉ thị gửi tới LLM. Dùng `$ARGUMENTS` để nhúng JSON input. |
| `model` | Không | Tên mô hình Claude sử dụng (mặc định là mô hình nhanh/Haiku). |
| `timeout` | Không | Thời gian chờ tối đa bằng giây (mặc định: 30 giây). |
| `continueOnBlock`| Không | Nếu `ok: false`, nạp lý do ngược lại cho Claude tiếp tục thực hiện lượt thay vì dừng (mặc định: `false`). |

### Schema phản hồi bắt buộc của LLM

Mô hình Claude đánh giá bắt buộc phải trả về JSON đúng cấu trúc sau:

<hook_schema>
```json
{
  "ok": true | false,
  "reason": "Giải thích chi tiết lý do đưa ra quyết định này"
}
```
</hook_schema>

* `ok`: `true` để cho phép tiếp tục; `false` để phát ra lệnh chặn (`decision: "block"`).
* `reason`: Bắt buộc khi `ok: false`. Chuỗi này sẽ được gửi ngược lại cho Claude làm chỉ thị sửa đổi hoặc cảnh báo cho người dùng.

---

## 2. Hook dựa trên Agent (Agent-based Hooks)

> [!WARNING]
> Hook dựa trên Agent là tính năng thử nghiệm (experimental). Cấu trúc và hành vi có thể thay đổi trong các phiên bản tương lai. Đối với quy trình sản xuất ổn định, khuyến khích sử dụng Command Hooks.

Hook dựa trên Agent (`type: "agent"`) hoạt động tương tự như prompt hook nhưng cung cấp cho mô hình khả năng **gọi công cụ đa lượt (multi-turn tool access)**. Thay vì chỉ đánh giá một lượt tĩnh, nó khởi chạy một subagent độc lập có quyền đọc file, tìm kiếm mã nguồn và kiểm tra codebase để tự động xác minh điều kiện.

### Cơ chế hoạt động:
1. Khi sự kiện kích hoạt, Claude Code khởi tạo một subagent kèm theo prompt chỉ thị của bạn và JSON dữ liệu đầu vào.
2. Subagent sử dụng các công cụ như `Read`, `Grep`, và `Glob` để tiến hành phân tích mã nguồn thực tế.
3. Sau tối đa 50 lượt gọi mô hình, subagent đưa ra kết quả cuối cùng dạng `{ "ok": true/false, "reason": "..." }`.
4. Phiên chính của Claude Code xử lý quyết định tương tự như prompt hook.

### Ví dụ cấu hình Agent Hook:
Dưới đây là một hook kiểm tra đảm bảo toàn bộ unit test phải pass trước khi cho phép Claude kết thúc phiên làm việc:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Xác minh xem toàn bộ các bài kiểm thử unit test có vượt qua không. Hãy tự chạy bộ test suite và phân tích kết quả. Ngữ cảnh: $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## 3. Chạy Hook Chạy Ngầm (Async Hooks)

Mặc định, các hook là đồng bộ (synchronous) - chúng sẽ chặn việc thực thi của Claude cho đến khi hoàn thành. Để xử lý các tác vụ tốn thời gian như triển khai ứng dụng (deployment), chạy bộ test suite lớn hoặc gọi API bên ngoài, hãy thiết lập `"async": true`.

<instructions>
must:
  - Chỉ áp dụng `"async": true` cho các hook có `"type": "command"`. Prompt-based và Agent-based hooks không hỗ trợ chạy bất đồng bộ.
must_not:
  - Kỳ vọng Async Hooks có khả năng chặn hoặc thay đổi quyết định tức thời của Claude (như `decision` hoặc `permissionDecision`) vì hành động thực tế đã xảy ra trước khi hook chạy xong.
</instructions>

### Ví dụ cấu hình Async Hook:
Chạy bộ test suite chạy ngầm sau khi Claude ghi đè file (`Write`). Claude tiếp tục làm việc ngay lập tức, script `run-tests.sh` có tối đa 120 giây để hoàn thành ở chế độ nền:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### Cơ chế Gửi phản hồi Ngược (Context Delivery)

Khi tiến trình chạy ngầm kết thúc:
1. Nếu script hook tạo ra một phản hồi JSON chứa trường `additionalContext`, nội dung này sẽ được **nạp làm ngữ cảnh hỗ trợ cho Claude ở lượt hội thoại kế tiếp**.
2. Nếu chứa trường `systemMessage`, thông báo đó sẽ hiển thị trực tiếp cho người dùng trên terminal.
3. Để đánh thức Claude Code ngay lập tức khi đang ở trạng thái chờ (session idle), script hook có thể thoát với mã lỗi `exit 2` (`asyncRewake`).

### Ví dụ kịch bản chạy test ngầm sau khi lưu file (`run-tests-async.sh`):

<examples>
```bash
#!/bin/bash
# .claude/hooks/run-tests-async.sh

# Đọc JSON đầu vào từ stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Chỉ chạy test nếu sửa đổi các file mã nguồn TS/JS
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Chạy test suite thực tế và bắt lại log đầu ra
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  MSG="[Kiểm thử thành công] Bộ test đã PASS sau khi chỉnh sửa file $FILE_PATH"
else
  MSG="[Kiểm thử THẤT BẠI] Lỗi xuất hiện sau khi chỉnh sửa file $FILE_PATH: $RESULT"
fi

# Xuất JSON trả bối cảnh về cho Claude ở turn kế tiếp
jq -nc --arg msg "$MSG" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
```
</examples>
