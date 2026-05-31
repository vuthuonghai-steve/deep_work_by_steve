# Kiến trúc & Các loại Hook trong Claude Code

Tài liệu này đặc tả kiến trúc cốt lõi, vòng đời hoạt động và các hình thức triển khai hook (Command, HTTP, MCP, Prompt, Agent) trong hệ sinh thái Claude Code.

---

## 1. Tổng quan & Vòng đời Hook

Hook là các đoạn kịch bản shell do người dùng định nghĩa, các điểm cuối HTTP hoặc prompt LLM tự động thực thi tại các thời điểm cụ thể trong vòng đời hoạt động của Claude Code. 

### Phân nhóm tần suất thực thi (Cadence)

<context>
Các sự kiện hook được chia làm 3 nhóm tần suất chính:
1. **Một lần mỗi Session (Once per Session):** Chạy khi khởi động hoặc kết thúc phiên (ví dụ: `SessionStart`, `SessionEnd`, `Setup`).
2. **Một lần mỗi Lượt tương tác (Once per Turn):** Chạy trước khi gửi yêu cầu lên mô hình hoặc sau khi nhận phản hồi hoàn tất (ví dụ: `UserPromptSubmit`, `Stop`, `StopFailure`).
3. **Mỗi bước gọi công cụ (On every Tool Call):** Chạy bên trong vòng lặp agentic loop cho từng lệnh gọi công cụ riêng lẻ (ví dụ: `PreToolUse`, `PostToolUse`).
</context>

### Luồng phân giải Hook (How a Hook Resolves)

Khi một sự kiện xảy ra, Claude Code sẽ quét cấu hình để tìm bộ lọc khớp (`matcher`). Nếu khớp, nó sẽ chuyển bối cảnh sự kiện dạng JSON vào kịch bản xử lý của bạn:
- **Command hooks:** Dữ liệu đầu vào truyền qua `stdin` và đầu ra được đọc từ `stdout`/`stderr`.
- **HTTP hooks:** Dữ liệu truyền qua body của yêu cầu `POST` và đầu ra trả về qua HTTP response JSON.

---

## 2. Các loại Hook Hỗ trợ

Claude Code hỗ trợ 5 loại hook linh hoạt tùy thuộc vào nhu cầu bảo mật và khả năng thực thi:

```yaml
supported_hook_types:
  command:
    desc: "Chạy một lệnh shell hoặc script cục bộ."
    input_via: "stdin"
    output_via: "stdout / stderr / exit codes"
    suitability: "Tốt nhất cho các tác vụ kiểm tra cục bộ, chạy linter, git hooks hoặc xác thực nhanh."
  
  http:
    desc: "Gửi yêu cầu POST tới một URL dịch vụ bên ngoài."
    input_via: "POST request body JSON"
    output_via: "HTTP response JSON"
    suitability: "Lý tưởng để tích hợp với CI/CD, webhook Slack, hoặc hệ thống giám sát tập trung."
    
  mcp_tool:
    desc: "Kích hoạt trực tiếp một công cụ từ máy chủ Model Context Protocol (MCP) đã kết nối."
    suitability: "Được dùng khi muốn tận dụng các tài nguyên/máy chủ MCP có sẵn để xử lý logic."

  prompt:
    desc: "Sử dụng một mô hình Claude (mặc định là Haiku) để đánh giá hành động dựa trên prompt."
    suitability: "Tự động hóa việc phân tích ngữ nghĩa, duyệt nhanh các quyết định phi kỹ thuật."

  agent:
    desc: "Khởi chạy một subagent chuyên biệt có quyền truy cập công cụ để điều tra chi tiết trước khi quyết định."
    suitability: "Phù hợp để thực hiện các cuộc kiểm tra sâu như chạy kiểm thử tự động rồi phân tích lỗi."
```

---

## 3. Cấu trúc Dữ liệu Chung (Common Payload Schema)

Mọi sự kiện hook khi kích hoạt đều nhận được một payload JSON chứa các thông tin ngữ cảnh chung sau:

<hook_schema>
```json
{
  "session_id": "chuỗi_định_danh_session_duy_nhất",
  "transcript_path": "/đường_dẫn_tuyệt_đối/tới/transcript.jsonl",
  "cwd": "/thư_mục/làm_việc/hiện_tại",
  "permission_mode": "default | auto | dontAsk | bypassPermissions | plan",
  "hook_event_name": "TênSựKiệnHook"
}
```
</hook_schema>

### Chi tiết các trường chung:
* `session_id`: ID phiên duy nhất giúp phân biệt các luồng chạy độc lập.
* `transcript_path`: File ghi nhật ký toàn bộ tương tác của phiên hiện tại dưới định dạng JSONL.
* `cwd`: Thư mục làm việc hiện thời của Claude Code.
* `permission_mode`: Chế độ phân quyền đang hoạt động của phiên chính.
* `hook_event_name`: Tên chính xác của sự kiện đang kích hoạt.

---

## 4. Cơ chế Kiểm soát Quyết định (Decision Control)

Một số sự kiện hook cho phép chặn đứng (`block`), thay đổi quyết định phân quyền (`deny`/`allow`) hoặc đưa thêm chỉ thị để Claude Code tiếp tục thực thi.

```yaml
decision_flow_rules:
  exit_codes:
    exit_0: "Chấp thuận hành động mà không đưa ra quyết định đặc biệt nào khác. Luồng phân quyền mặc định tiếp tục áp dụng."
    exit_2: "Từ chối/chặn hành động. Đưa thông báo từ stderr phản hồi lại cho mô hình (đối với PreToolUse, TaskCreated, v.v.)."
    exit_other: "Lỗi thực thi hook. Coi như không chặn hoặc chặn tùy thuộc vào cấu hình an toàn."

  json_output_fields:
    systemMessage:
      type: "string"
      target: "User"
      desc: "Thông báo hiển thị trực tiếp cho người dùng trên giao diện terminal. Không gửi cho Claude."
    assistantMessage:
      type: "string"
      target: "Claude"
      desc: "Thay thế hoặc chèn thêm nội dung vào lượt hội thoại tiếp theo của Claude."
    additionalContext:
      type: "string"
      target: "Claude Context"
      desc: "Bổ sung tri thức/ngữ cảnh dưới dạng tài liệu hỗ trợ mà không làm loãng transcript."
```

---

## 5. Duy trì Biến Môi trường (Environment Persistence)

Các sự kiện như `SessionStart`, `CwdChanged` và `FileChanged` có quyền truy cập vào biến môi trường đặc biệt `CLAUDE_ENV_FILE`.

<instructions>
must:
  - Khi muốn ghi nhận các biến môi trường để sử dụng cho các lệnh Bash tiếp theo của Claude, hãy viết chúng vào file nằm trong biến `$CLAUDE_ENV_FILE`.
  - Định dạng ghi nhận phải tuân thủ chuẩn: `KEY=VALUE` (mỗi dòng một biến).
must_not:
  - Xuất trực tiếp bằng lệnh `export KEY=VALUE` bên trong script hook vì tiến trình con sẽ bị hủy ngay khi hook kết thúc, khiến biến bị mất.
</instructions>

### Ví dụ cơ chế ghi nhận biến môi trường:
```bash
#!/bin/bash
# Nạp cấu hình từ tệp cục bộ và truyền cho phiên Claude Code
if [ -f ".env.local" ]; then
  cat .env.local >> "$CLAUDE_ENV_FILE"
fi
```
