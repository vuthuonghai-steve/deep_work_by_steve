# Quy Trình Vận Hành 4 Phase Chi Tiết (Exploration Workflow)

> **Mã số**: STG0-POL-WORKFLOW
> **Vai trò**: Chỉ dẫn AI thực thi khảo sát theo chuỗi tuần tự có kiểm soát chất lượng chặt chẽ.

---

## Phase 1: Input Acceptance & Intent Analysis (Nhận Diện Ý Định)
*   **Mục tiêu**: Nhận diện yêu cầu ban đầu của người dùng về skill cần xây dựng. Phân tích bối cảnh, đối tượng sử dụng và các class/hàm nghiệp vụ chính.
*   **Hành động bắt buộc**:
    1.  Khởi tạo thư mục bối cảnh `.skill-context/{skill-name}/` và thư mục tài nguyên con `resources/`.
    2.  Chạy script `python3 scripts/init_context.py {skill-name}` để tự động sinh cấu trúc và các tệp JSON ledgers mẫu (`exploration.json`, `criteria.json`).
    3.  Phân tích mục tiêu cốt lõi: Skill đích giải quyết nỗi đau gì, đối tượng người dùng là ai, và hệ thống cần những luồng nghiệp vụ cơ bản nào.

---

## Phase 2: Golden Standards & Security Assessment (Đánh Giá Tiêu Chuẩn & An Toàn)
*   **Mục tiêu**: Đánh giá tính khả thi, độ an toàn và quy mô của skill đích.
*   **Hành động bắt buộc**:
    1.  Nạp tài liệu `knowledge/exploration-standards.md` để tự kiểm định skill đích dựa trên **7 Tiêu chuẩn Vàng** (Reusability, Composability, Maintainability, Security, Context Economics, Portability, Reliability).
    2.  **Đánh giá quy mô & Phân rã Micro-skills (SCS Thang đo)**:
        *   Tự đánh giá điểm số SCS dựa trên: Số bước quy trình, Số công cụ, Kích thước SKILL.md dự kiến, và Rủi ro an ninh.
        *   Nếu SCS trung bình > 3.0 hoặc có điểm 5 (ngưỡng đỏ), bắt buộc phải đề xuất phương án phân rã thành các Micro-skills chuyên biệt và vẽ sơ đồ phối hợp (Mermaid Diagram) trong `exploration.json`.
    3.  **Lập kịch bản bảo mật**:
        *   Phòng vệ Prompt Injection: Thiết lập strict XML boundaries cho dữ liệu external.
        *   Cô lập Sandbox: Thiết lập môi trường Docker chạy mã biệt lập nếu skill đích có đi kèm thực thi scripts.

---

## Phase 3: Codebase Resource Gathering & Mining (Khai Thác Mã Mẫu & API)
*   **Mục tiêu**: Lục lọi codebase hiện tại để thu hoạch các API hiện có, các mã nguồn mẫu có thể tái sử dụng, giúp skill mới khớp nối hoàn hảo với hệ thống.
*   **Hành động bắt buộc**:
    1.  Tra cứu mã nguồn hiện có trong codebase của dự án (LSP, grep_search) sử dụng `data/search-blacklist.yaml` để loại bỏ các file/thư mục rác.
    2.  Thu thập mã mẫu (code exemplars), API schemas, helper functions có sẵn để tái sử dụng.
    3.  Khảo sát tri thức bên ngoài qua web (`search_web`, `read_url_content`) để tìm các best practices của các thư viện mã nguồn mở.
    4.  Lưu trữ tri thức nghiệp vụ thô thu thập được vào các tệp tin có cấu trúc bên dưới thư mục `.skill-context/{skill-name}/resources/`.

---

## Phase 4: Synthesis, Validation & Deliver (Tổng Hợp, Xác Thực & Bàn Giao)
*   **Mục tiêu**: Đóng gói toàn bộ thông tin khảo sát nghiệp vụ và bàn giao sạch sẽ.
*   **Hành động bắt buộc**:
    1.  Nạp tệp mẫu `templates/exploration.json.template` và `templates/criteria.json.template`.
    2.  Biên soạn đầy đủ nội dung cho `exploration.json` và `criteria.json` đảm bảo không chứa bất kỳ placeholder nào.
    3.  **Tự chạy kiểm tra chốt chặn chất lượng**: Nạp checklist `loop/exploration-checklist.md` để tự kiểm định.
    4.  **Xác thực Schema**: Chạy validation:
        `python3 skills/rebuild/_shared/validators/schema_validator.py --schema skills/rebuild/_shared/schemas/exploration.schema.json .skill-context/{skill-name}/exploration.json`
        `python3 skills/rebuild/_shared/validators/schema_validator.py --schema skills/rebuild/_shared/schemas/criteria.schema.json .skill-context/{skill-name}/criteria.json`
    5.  Báo cáo tóm tắt bằng tiếng Việt đường dẫn file và bàn giao kết quả. Nếu quyết định phân rã micro-skills được kích hoạt ở Phase 2, hướng dẫn người dùng chạy lệnh chia bối cảnh hạ nguồn để khởi dựng đồng loạt các micro-skills con sẵn sàng cho Stage 1:
        `python3 scripts/init_context.py --split .skill-context/{skill-name}/exploration.json`
