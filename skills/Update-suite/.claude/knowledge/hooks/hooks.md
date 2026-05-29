# Cẩm nang Cấu hình Hook trong Claude Code (L0 Root Guide)

Tài liệu này đóng vai trò là L0 Anchor - Bản đồ chỉ hướng và Quy tắc cứng cho việc cấu hình, kiểm tra và vận hành các hook tự động hóa trong Claude Code.

---

## 1. Metadata

```yaml
version: "1.0.0"
updated_at: "2026-05-28"
tags: [hooks, configuration, lifecycle, automation]
description: "Cẩm nang root guide định tuyến và chuẩn hóa việc phát triển hook cho Claude Code."
```

---

## 2. Mục tiêu & Định nghĩa Thành công (Purpose)

Tự động hóa các luồng công việc phức tạp, xây dựng tường lửa bảo mật cục bộ, tích hợp CI/CD và tối ưu hóa token bằng cách can thiệp vào các điểm then chốt trong vòng đời thực thi của Claude Code.

<instructions>
must:
  - **Dùng đường dẫn biến số:** Luôn sử dụng biến môi trường `${CLAUDE_PROJECT_DIR}` trong cấu hình JSON thay vì dùng đường dẫn cứng (hardcoded paths) như `/home/user/`.
  - **Quyền chạy script:** Đảm bảo tất cả các script hook dạng Command được phân quyền thực thi bằng lệnh `chmod +x` trước khi khai báo.
  - **Kiểm soát mã lỗi:** Hiểu rõ các mã lỗi thoát (exit codes) của hook. Trả về `exit 2` khi muốn chặn hành động của Claude và xuất thông báo lỗi qua `stderr`.
must_not:
  - **Không chặn vô hạn:** Tránh tạo các hook sự kiện `Stop` hoặc `SubagentStop` có nguy cơ rơi vào vòng lặp chặn vô hạn (`decision: "block"` liên tục), khiến Claude không thể dừng turn.
  - **Không nhúng thông tin nhạy cảm:** Không commit các file script hook chứa thông tin bí mật (token, API keys, credentials) lên Git.
</instructions>

---

## 3. Bản đồ Nạp Ngữ cảnh (Working Map)

Dưới đây là sơ đồ phân vùng kiến thức của hệ thống Hook. Khi cần thực hiện các tác vụ liên quan đến phân vùng nào, hãy nạp tệp tài liệu tương ứng để có đầy đủ tri thức chuyên sâu.

```yaml
load_when_needed:
  core_architecture:
    file: "types_and_architecture.md"
    desc: "Kiến trúc nền tảng, cơ chế hoạt động, 5 loại hook hỗ trợ và cách truyền nhận dữ liệu."
  
  core_lifecycle_events:
    file: "core_events.md"
    desc: "Chi tiết schema và logic kiểm soát của các sự kiện cốt lõi (SessionStart, PreToolUse, PostToolUse, Stop, v.v.)."
    
  workflow_system_events:
    file: "workflow_events.md"
    desc: "Chi tiết schema của các sự kiện hệ thống và quy trình (SubagentStart, TaskCreated, CwdChanged, FileChanged, v.v.)."
    
  advanced_hook_capabilities:
    file: "advanced_hooks.md"
    desc: "Cách cấu hình và ví dụ thực tế cho Hook dựa trên Prompt, Hook dựa trên Agent và chạy ngầm bất đồng bộ (Async)."
    
  security_and_debugging:
    file: "security_and_debugging.md"
    desc: "Quy tắc an toàn bảo mật, cấu hình PowerShell trên Windows và cách đọc file nhật ký gỡ lỗi (debug log)."

  xml_tagging_standards:
    file: "xml_tags_standards.yaml"
    desc: "Các thẻ XML chuẩn hóa phục vụ cho việc kích hoạt tri thức của LLM đối với tài liệu Hook."
```

---

## 4. Giao thức Tương tác của Agent (Interaction Protocol)

Khi làm việc với các file cấu hình hoặc viết script hook trong dự án, Agent bắt buộc phải tuân thủ quy trình 3 bước sau:

```yaml
agent_protocol:
  before_editing:
    - "Đọc file `xml_tags_standards.yaml` trong thư mục này để hiểu rõ các thẻ XML sử dụng."
    - "Xác định rõ sự kiện hook cần can thiệp thuộc file tài liệu con nào (core_events.md hay workflow_events.md) và tải file đó."
    - "Kiểm tra kỹ xem hook cần viết là đồng bộ hay bất đồng bộ để áp dụng đúng giới hạn thiết kế."

  during_editing:
    - "Viết mã nguồn script hook rõ ràng, tránh sử dụng placeholder (TODO, pass, mock)."
    - "Luôn bọc các biến shell trong dấu ngoặc kép và kiểm tra lỗi cú pháp (linter) của script."
    - "Đảm bảo cấu hình JSON trong `.claude/settings.json` được định dạng chuẩn xác."

  before_final_response:
    - "Xác nhận các file script mới tạo đã được cấp quyền chạy (+x)."
    - "Hướng dẫn người dùng cách chạy kiểm thử hoặc kiểm tra hoạt động của hook thông qua log debug."
    - "Báo cáo rõ: Sự kiện đã can thiệp, File thay đổi, và Đánh giá rủi ro an toàn."
```
