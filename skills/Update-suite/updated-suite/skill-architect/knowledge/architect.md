# Tri Thức Chuyên Sâu Về Kiến Trúc Kỹ Năng (3 Pillars Architecture)

> **Mã số**: STG1-KNW-ARCH
> **Vai trò**: Cung cấp nền tảng tri thức cho Architect để định hình và thiết kế cấu trúc kỹ năng Clean & Solid.

---

## 1. Hệ Thống 3 Pillars Cốt Lõi (The 3 Pillars System)
Mỗi Agent Skill trong hệ thống của Steve không phải là một tập lệnh phẳng đơn thuần, mà là một cấu trúc vững chắc được tựa trên 3 trụ cột vững chãi:

```text
       ┌─────────────────────────────────────────────────────────┐
       │               MASTER PRODUCTION AGENT SKILL             │
       └─────────────────────────────────────────────────────────┘
                    │               │               │
                    ▼               ▼               ▼
             ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
             │  PILLAR 1:  │ │  PILLAR 2:  │ │  PILLAR 3:  │
             │ Core Logic  │ │   Domain    │ │   Quality   │
             │             │ │  Knowledge  │ │    Loop     │
             └─────────────┘ └─────────────┘ └─────────────┘
```

### Pillar 1: Core Logic (Trụ Cột Logic Cốt Lõi)
*   **Định nghĩa**: Các chỉ dẫn điều hành tối cao (L0 Anchor rules) và các quy tắc hành vi bắt buộc mà AI phải tuân thủ khi khởi động kỹ năng.
*   **Thực thể vật lý**: File `SKILL.md` đóng vai trò là L0 Anchor. Nó chứa Persona, Boot Sequence và Routing Map.
*   **Nguyên tắc thiết kế**: Phải cực kỳ tinh gọn (< 600 tokens). Tuyệt đối cấm nhồi nhét tài liệu nghiệp vụ, hướng dẫn dài dòng hoặc code vào `SKILL.md` để bảo vệ Token Economics cho AI.

### Pillar 2: Domain Knowledge (Trụ Cột Tri Thức Nghiệp Vụ)
*   **Định nghĩa**: Các tài liệu chính sách (`policy/`), tri thức nghiệp vụ chuyên biệt (`knowledge/`) và các scripts bổ trợ (`scripts/`) hoặc dữ liệu mẫu (`data/`, `templates/`).
*   **Nguyên tắc thiết kế**: Áp dụng triệt để chính sách **Nạp Tri Thức Động Theo Nhu Cầu (Progressive Disclosure)**. Chỉ nạp các file tri thức này khi AI thực sự đi vào phase nghiệp vụ tương ứng, thông qua liên kết absolute markdown trong Routing Map của `SKILL.md`.

### Pillar 3: Quality Loop (Trụ Cột Vòng Lặp Chất Lượng)
*   **Định nghĩa**: Các chốt chặn kiểm soát chất lượng tĩnh (`loop/checklist.md`) và kịch bản chạy thử tự động trong Sandbox Docker (`verification.json`).
*   **Nguyên tắc thiết kế**: Đảm bảo an toàn thực chất (Fact-Based Confidence Score). Cấm AI tự duyệt pass kết quả của mình mà không qua script chạy thực tế trong Sandbox cô lập.

---

## 2. Bản Đồ Phân Vùng 7 Zones (The 7-Zone Taxonomy)
Kiến trúc 7 Zones phân rã thư mục kỹ năng vật lý thành các vùng có ranh giới trách nhiệm đơn nhất:

1.  **Vùng Core (`core`)**: Chứa tệp `SKILL.md`. Đây là hạt nhân của kỹ năng.
2.  **Vùng Knowledge (`knowledge`)**: Chứa các file markdown lưu trữ tri thức nền tảng, best practices và các ví dụ Good/Bad mẫu.
3.  **Vùng Scripts (`scripts`)**: Chứa mã nguồn thực thi độc lập (Python, Bash) được chạy trong môi trường sandbox cô lập.
4.  **Vùng Templates (`templates`)**: Chứa các file định dạng cấu trúc mẫu cho dữ liệu đầu ra.
5.  **Vùng Data (`data`)**: Chứa các file dữ liệu cấu hình tĩnh (YAML, JSON) hoặc danh sách đen/trắng (blacklist/whitelist).
6.  **Vùng Loop (`loop`)**: Chứa các tệp checklist chất lượng, các quy tắc kiểm soát biên.
7.  **Vùng Assets (`assets`)**: Chứa các tài nguyên đồ họa, hình ảnh tĩnh hoặc sơ đồ thiết kế.
