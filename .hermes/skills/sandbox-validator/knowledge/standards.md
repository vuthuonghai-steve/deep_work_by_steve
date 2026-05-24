# Quy Chuẩn An Toàn Sandbox & Kiểm Định Schema YAML

Tài liệu này định nghĩa các quy chuẩn kỹ thuật áp dụng cho micro-skill `sandbox-validator` nhằm đảm bảo môi trường thực thi biệt lập hoàn toàn và kiểm định cấu trúc tri thức AI chuẩn xác.

---

## 1. Tiêu Chuẩn An Toàn Docker Sandbox (gVisor & Egress Block)

Khi thực thi mã nguồn kiểm thử (unit tests) hoặc chạy thử mã nguồn ví dụ (L3: Examples) từ tài liệu thô, bắt buộc phải cách ly hoàn toàn tiến trình với hệ điều hành máy host.

### A. Thiết lập gVisor Runtime (`runsc`)
gVisor là một nhân (kernel) bảo mật do Google phát triển, hoạt động như một lớp ảo hóa mỏng chặn đứng các lời gọi hệ thống (system calls) trực tiếp từ container xuống kernel của máy host.
- **Tham số kích hoạt**: Bắt buộc cấu hình `--runtime=runsc` khi khởi chạy container Docker.
- **Hành vi**: gVisor chặn các lỗ hổng escape-container bảo vệ nhân Linux máy host khỏi bị khai thác.
- **Cơ chế Fallback**: Trong trường hợp máy host chưa cấu hình gVisor runtime (`runsc`), tiến trình điều khiển sẽ tự động chuyển hướng sử dụng runtime mặc định (`runc`) nhưng phải ghi nhận cảnh báo mức Vàng (Warning) kèm theo các chỉ thị kiểm soát tài nguyên nghiêm ngặt khác.

### B. Ngắt Kết Nối Mạng Ngoài (Egress Isolation)
Để triệt tiêu nguy cơ rò rỉ hoặc gửi dữ liệu nhạy cảm ra ngoài (Data Exfiltration):
- **Tham số cấu hình**: Bắt buộc gắn cờ `--network none` khi chạy container Docker.
- **Tác động**: Mọi hành vi mở socket kết nối HTTP/TCP từ bên trong container ra internet hoặc mạng nội bộ sẽ bị chặn đứng lập tức ở tầng kernel.

### C. Giới Hạn Tài Nguyên & Tự Hủy
- **Giới hạn thời gian**: Thiết lập timeout thực thi tối đa là 60 giây. Nếu vượt quá, tiến trình cha sẽ gửi tín hiệu `SIGKILL` cưỡng bức dừng container.
- **Hạn chế tài nguyên**: Giới hạn RAM tối đa 512MB (`-m 512m`) và CPU tối đa 0.5 core (`--cpus="0.5"`) để tránh tấn công từ chối dịch vụ (DoS) tài nguyên máy host.
- **Tự dọn dẹp**: Luôn sử dụng cờ `--rm` để Docker tự động xóa bỏ container và bộ nhớ tạm ngay sau khi dừng.

---

## 2. Phòng Chống Tấn Công Prompt & Shell Injection

Dữ liệu thô từ nguồn cào quét (web hoặc codebase) có thể chứa mã độc hại được chèn tinh vi.

### A. Nhận diện các mẫu lệnh nguy hại
Script kiểm định phải chủ động quét chuỗi thô (static analysis) để nhận diện các ký tự đặc biệt hoặc các từ khóa hệ thống nguy hiểm:
- Các ký tự nối lệnh shell: `;`, `&&`, `|`, `` ` ``, `$()`.
- Các câu lệnh hệ thống nhạy cảm: `rm -rf`, `wget`, `curl`, `chmod`, `chown`, `env`, `printenv`, `ssh`, `aws`.
- Các đường dẫn tệp tin hệ thống nhạy cảm: `/etc/passwd`, `/etc/shadow`, `~/.ssh/`, `~/.aws/`, `~/.bashrc`.

### B. Biện pháp cô lập mount
- **CẤM TUYỆT ĐỐI**: Không mount socket Docker `/var/run/docker.sock` vào container (tránh tấn công Docker-in-Docker để kiểm soát máy host).
- **CẤM TUYỆT ĐỐI**: Không mount các thư mục chứa thông tin nhạy cảm của người phát triển (`~/.ssh`, `~/.aws`, `~/.gemini`).
- **CHỈ PHÉP**: Mount thư mục tạm thời dạng Read-Only (`:ro`) chứa mã nguồn cần kiểm thử.

---

## 3. Quy Chuẩn Kiểm Định Cấu Trúc Schema YAML

Tài liệu tri thức chắt lọc chuyển giao từ `format-converter` phải tuân thủ nghiêm ngặt mô hình cấu trúc phân tầng tri thức.

### A. Cấu trúc Schema bắt buộc cho `distilled_draft.yaml`
Mỗi thực thể tri thức chắt lọc phải chứa đầy đủ các trường sau:
```yaml
knowledge_id: "Tên định danh dạng kebab-case"
layer: "L0" | "L1" | "L2" | "L3"
format: "markdown" | "yaml" | "xml"
content: "Nội dung chi tiết của tri thức"
confidence_score: float (0.0 đến 1.0)
```

### B. Quy tắc Schema Validation
1. **Định dạng lớp L0 (Anchor)**:
   - `format` bắt buộc phải là `markdown`.
   - Token budget thực tế của `content` không được vượt quá 400 tokens.
2. **Định dạng lớp L1 (Policy)**:
   - `format` bắt buộc phải là `yaml` (chứa các quy định hành vi dạng must/must_not).
   - Token budget không được vượt quá 1200 tokens.
3. **Định dạng lớp L2 (Domain)**:
   - `format` có thể là `markdown` hoặc `yaml`.
   - Token budget không được vượt quá 2500 tokens.
4. **Định dạng lớp L3 (Examples)**:
   - `format` bắt buộc phải là `xml` (chứa các đoạn mã mẫu thực tế được bao bọc an toàn).
