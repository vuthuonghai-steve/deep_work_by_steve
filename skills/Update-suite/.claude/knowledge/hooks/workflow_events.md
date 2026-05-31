# Sự kiện Quy trình & Hệ thống (Workflow & System Events)

Tài liệu này đặc tả chi tiết các sự kiện hook liên quan đến quy trình làm việc (Workflow), quản lý tác vụ (Tasks), thư mục/tệp tin, nén bối cảnh (Context Compaction), tương tác với Subagent và các dịch vụ MCP ngoài.

---

## 1. Danh sách Sự kiện Quy trình

```yaml
workflow_events:
  subagent_management:
    - SubagentStart: "Kích hoạt khi một subagent bắt đầu được tạo lập và khởi chạy."
    - SubagentStop: "Kích hoạt khi subagent kết thúc xử lý."
  task_tracking:
    - TaskCreated: "Kích hoạt khi một task mới được tạo ra thông qua công cụ quản lý tác vụ."
    - TaskCompleted: "Kích hoạt khi một task được đánh dấu là hoàn thành."
  environment_reactivity:
    - CwdChanged: "Kích hoạt khi thư mục làm việc hiện tại thay đổi (ví dụ: mô hình gọi lệnh cd)."
    - FileChanged: "Kích hoạt khi các tệp tin đang được theo dõi có sự thay đổi trên đĩa cứng."
    - ConfigChange: "Kích hoạt khi có thay đổi trong file cấu hình dự án của Claude Code."
    - InstructionsLoaded: "Kích hoạt khi hệ thống tải tệp CLAUDE.md hoặc các file .claude/rules/*.md vào bối cảnh."
  git_worktrees:
    - WorktreeCreate: "Kích hoạt khi một git worktree mới được tạo lập để cô lập không gian làm việc."
    - WorktreeRemove: "Kích hoạt khi dọn dẹp và xóa bỏ git worktree."
  context_compaction:
    - PreCompact: "Chạy ngay trước khi kích hoạt quy trình thu gọn bối cảnh (compaction) để giải phóng token."
    - PostCompact: "Chạy sau khi quy trình thu gọn bối cảnh hoàn thành."
  mcp_interaction:
    - Elicitation: "Chạy khi máy chủ MCP gửi yêu cầu thu thập thêm thông tin từ người dùng."
    - ElicitationResult: "Chạy sau khi người dùng nhập câu trả lời, trước khi kết quả gửi lại cho MCP."
  system_alerts:
    - Notification: "Kích hoạt khi Claude Code gửi một thông báo hệ thống ngoài terminal."
```

---

## 2. Nhóm Quản lý Subagent & Đồng đội (Subagents & Teams)

### SubagentStart

Kích hoạt khi tiến trình chính chuẩn bị khởi chạy một subagent (ví dụ: qua lệnh gọi task hoặc tác vụ chuyên biệt).
* **Ứng dụng:** Thiết lập môi trường độc lập cho subagent hoặc kiểm tra chỉ thị trước khi subagent chạy.

<hook_schema>
```json
{
  "session_id": "abc123",
  "cwd": "/project/path",
  "hook_event_name": "SubagentStart",
  "subagent_id": "sub_agent_unique_01",
  "subagent_name": "tên-subagent-kebab-case",
  "subagent_instructions": "Chỉ thị gốc truyền cho subagent"
}
```
</hook_schema>

---

### SubagentStop

Kích hoạt ngay khi subagent hoàn thành toàn bộ công việc và chuẩn bị tắt.
* **Đầu vào:** Nhận trạng thái `status` (`"success"` hoặc `"failure"`) và `summary` (tóm tắt kết quả của subagent).
* **Ứng dụng:** Đồng bộ dữ liệu, thu thập log hoặc kiểm định kết quả do subagent thực hiện.

---

### TeammateIdle

Chạy khi một đồng đội (teammate) trong hệ thống Agent Teams rơi vào trạng thái chờ (nhận lệnh mới từ coordinator).

---

## 3. Nhóm Quản lý Tác vụ (Tasks)

### TaskCreated

Kích hoạt khi công cụ quản lý công việc `TaskCreate` tạo một task mới trong sơ đồ công việc.
* **Khả năng chặn:** Bạn có thể chặn việc tạo các task không hợp lệ bằng cách trả về `exit 2` hoặc JSON chặn:

```json
{
  "decision": "block",
  "reason": "Mô tả tác vụ quá mơ hồ hoặc không chứa trace_tag theo quy định."
}
```

---

### TaskCompleted

Kích hoạt khi mô hình yêu cầu đóng hoặc đánh dấu một tác vụ là hoàn thành (`TaskComplete`).
* **Ứng dụng kiểm soát chất lượng:** Đây là cánh cổng kiểm soát chất lượng (Quality Gate) đắc lực. Bạn có thể tự động chạy test hoặc quét bảo mật tại đây. Nếu phát hiện lỗi chưa sửa, hãy chặn đứng việc hoàn thành task:

```json
{
  "decision": "block",
  "reason": "Test suite cho tính năng này vẫn thất bại. Không được đóng task."
}
```

---

## 4. Phản ứng Môi trường & Hệ thống File (Environment & Files)

### CwdChanged

Chạy ngay sau khi thư mục làm việc hiện tại của Claude thay đổi.
* **Ứng dụng:** Rất hữu ích khi tích hợp với các công cụ tự động hóa môi trường như `direnv`. Bạn có thể tự động nạp cấu hình `.env` cục bộ tương ứng với thư mục mới:

```bash
#!/bin/bash
# .claude/hooks/cwd-changed.sh
INPUT=$(cat)
NEW_CWD=$(echo "$INPUT" | jq -r '.new_cwd')
cd "$NEW_CWD"
if [ -f ".envrc" ]; then
  direnv allow && eval "$(direnv export bash)"
fi
```

---

### FileChanged

Kích hoạt khi một file được chỉ định theo dõi trên ổ đĩa có sự biến động (được tạo, chỉnh sửa hoặc xóa).
* **Cấu hình Matcher:** Phải xác định rõ mẫu đường dẫn file cần watch:
  
```json
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": "src/**/*.ts",
        "hooks": [
          { "type": "command", "command": "npm run build" }
        ]
      }
    ]
  }
}
```

---

### InstructionsLoaded

Kích hoạt khi Claude Code tải file `CLAUDE.md` hoặc các tệp quy tắc `.claude/rules/*.md` vào trong cửa sổ ngữ cảnh.
* **Ứng dụng:** Kiểm tra xem các tệp quy tắc có bị thay đổi trái phép hay không, hoặc chèn thêm luật bảo mật động vào ngữ cảnh của Claude.

---

### ConfigChange

Kích hoạt khi tệp cấu hình của Claude Code (`.claude/settings.json`) bị thay đổi trong quá trình chạy.

---

## 5. Nhóm Quản lý Nhánh Cách ly & Nén ngữ cảnh (Worktrees & Compaction)

### WorktreeCreate & WorktreeRemove

Kích hoạt khi Claude Code sử dụng tính năng tạo Git Worktree độc lập thông qua cờ `--worktree` hoặc tùy chọn `isolation: "worktree"`.
* **Ứng dụng:** Tự động cài đặt dependencies (`npm install` hoặc `pip install -r requirements.txt`) ngay khi worktree được dựng lên, và dọn dẹp các thư mục rác khi worktree bị hủy.

---

### PreCompact & PostCompact

Quy trình thu gọn bối cảnh (Compaction) xảy ra khi lịch sử cuộc gọi đạt tới giới hạn token tối đa của cửa sổ ngữ cảnh. Claude Code sẽ tóm tắt lại hội thoại cũ để giải phóng không gian bộ nhớ.
* **PreCompact:** Cho phép bạn trích xuất các tri thức quan trọng ghi chép lại trước khi chúng bị nén và mất đi chi tiết.
* **PostCompact:** Nhận bối cảnh mới sau khi đã tóm tắt.

---

## 6. Nhóm Sự kiện MCP Elicitation

Khi một máy chủ Model Context Protocol (MCP) cần sự tương tác trực tiếp hoặc xác nhận từ người dùng trong khi đang chạy công cụ (ví dụ: xác thực OAuth 2-Step, chọn một lựa chọn trong danh sách):

* **Elicitation:** Kích hoạt khi yêu cầu từ máy chủ MCP gửi đến, trước khi giao diện terminal hiển thị câu hỏi cho bạn.
* **ElicitationResult:** Kích hoạt ngay sau khi bạn nhập câu trả lời, trước khi Claude Code đóng gói và gửi phản hồi ngược lại cho máy chủ MCP.
