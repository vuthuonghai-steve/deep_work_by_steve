# An toàn Bảo mật & Gỡ lỗi Hook (Security & Debugging)

Tài liệu này đặc tả các nguyên tắc an toàn bảo mật khi vận hành hook, cách thiết lập hook chạy trên môi trường Windows PowerShell và quy trình gỡ lỗi (debugging) khi viết hook cho Claude Code.

---

## 1. Vấn đề An toàn & Bảo mật (Security Considerations)

<context>
**Tuyên bố miễn trừ trách nhiệm quan trọng:**
Các Command hook chạy trực tiếp trên hệ thống của bạn dưới quyền sở hữu của tài khoản người dùng hiện tại (system user). Chúng có toàn quyền đọc, sửa đổi, xóa hoặc truy cập bất kỳ tài nguyên nào mà tài khoản của bạn được phép truy cập trên hệ điều hành.
</context>

> [!WARNING]
> Luôn luôn kiểm tra kỹ lưỡng mã nguồn của bất kỳ script hook nào trước khi đưa vào cấu hình. Không bao giờ chạy các script tải từ nguồn lạ mà chưa qua rà soát bảo mật.

### Nguyên tắc bảo mật khuyến nghị (Security Best Practices):

<instructions>
must:
  - **Làm sạch dữ liệu đầu vào (Sanitize Input):** Không bao giờ tin tưởng tuyệt đối vào các tham số lấy ra từ payload JSON của Claude Code. Hãy kiểm tra tính hợp lệ trước khi đưa vào các hàm thực thi shell.
  - **Luôn bao bọc biến Shell trong dấu ngoặc kép:** Sử dụng `"$VAR"` thay vì `$VAR` để ngăn chặn các cuộc tấn công chèn lệnh (Command Injection) thông qua khoảng trắng hoặc ký tự đặc biệt.
  - **Chặn tấn công duyệt thư mục (Path Traversal):** Nếu script xử lý đường dẫn file do Claude truyền vào, hãy kiểm tra và từ chối các đường dẫn chứa ký tự đi ngược thư mục cha như `..`.
  - **Sử dụng đường dẫn tuyệt đối:** Sử dụng biến môi trường hệ thống `${CLAUDE_PROJECT_DIR}` trong cấu hình JSON để luôn trỏ tới đúng thư mục gốc dự án.
must_not:
  - Thực thi trực tiếp các lệnh dạng `eval "$COMMAND"` hoặc truyền trực tiếp các chuỗi chưa được làm sạch vào shell.
  - Cho phép hook truy cập, đọc hoặc xuất bản thông tin các tệp tin nhạy cảm chứa khóa bí mật như `.env`, `.git/`, `.ssh/` hay các file private keys.
</instructions>

---

## 2. Cấu hình chạy trên môi trường Windows PowerShell

Trên hệ điều hành Windows, bạn có thể chỉ định cụ thể một hook chạy bằng PowerShell bằng cách thiết lập thuộc tính `"shell": "powershell"` bên trong cấu hình của Command hook.

* **Cơ chế tự động:** Claude Code sẽ tự động dò tìm phiên bản PowerShell 7 trở lên (`pwsh.exe`) trên hệ thống, nếu không thấy sẽ tự động lùi về PowerShell mặc định (`powershell.exe` phiên bản 5.1).
* **Độc lập môi trường:** Tính năng này hoạt động độc lập với việc bạn có thiết lập biến môi trường toàn cục `CLAUDE_CODE_USE_POWERSHELL_TOOL` hay không.

### Ví dụ cấu hình PowerShell Hook:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'Tệp tin đã được ghi đè thành công!'"
          }
        ]
      }
    ]
  }
}
```

---

## 3. Gỡ lỗi Hook (Debugging Hooks)

Toàn bộ chi tiết quá trình thực thi hook bao gồm: các hook nào khớp matcher, mã thoát (exit code), dữ liệu đầu ra tiêu chuẩn (stdout) và đầu ra lỗi (stderr) đều được ghi nhận chi tiết trong tệp nhật ký gỡ lỗi (debug log).

### Cách lấy tệp nhật ký gỡ lỗi:

1. **Ghi vào tệp chỉ định:** Khởi động Claude Code với tham số đường dẫn cụ thể:
   `claude --debug-file /đường_dẫn_tới/log_file.txt`
2. **Đọc tệp mặc định của hệ thống:** Khởi động bằng lệnh `claude --debug` và tìm tệp log được sinh ra tại thư mục:
   `~/.claude/debug/<session-id>.txt`

> [!NOTE]
> Cờ `--debug` sẽ ghi log ra file chạy ngầm chứ không in trực tiếp các thông tin debug này lên màn hình terminal tương tác của bạn.

### Mẫu log debug tiêu chuẩn của Hook:
```text
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: /project/scripts/validate.sh with timeout 600000ms
[DEBUG] Hook command completed with status 0: Output validation successful.
```

### Bật chế độ log chi tiết (Verbose Debug):
Để phân tích sâu hơn về số lượng so khớp matcher hoặc chi tiết truy vấn bộ lọc, hãy thiết lập biến môi trường trước khi khởi động Claude Code:

```bash
export CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose
claude
```

---

## 4. Xử lý các sự cố thường gặp (Troubleshooting)

```yaml
common_issues_and_solutions:
  hooks_not_firing:
    cause: "Bộ lọc 'matcher' viết sai chính tả hoặc không khớp với tên công cụ thực tế."
    solution: "Kiểm tra kỹ tên công cụ trong log debug hoặc danh sách sự kiện chuẩn."
  
  stop_hooks_blocking_forever:
    cause: "Hook Stop liên tục trả về ok: false hoặc exit 2 do logic kiểm tra test/linter bị lỗi vòng lặp."
    solution: "Sử dụng chế độ chạy an toàn không nạp cấu hình (claude -p dontAsk) để sửa đổi lại cấu hình hook."
  
  permission_errors_on_scripts:
    cause: "File script xử lý hook chưa được cấp quyền thực thi trên hệ thống Unix/Linux."
    solution: "Chạy lệnh chmod +x cho tệp tin script (ví dụ: chmod +x .claude/hooks/my-script.sh)."
```
