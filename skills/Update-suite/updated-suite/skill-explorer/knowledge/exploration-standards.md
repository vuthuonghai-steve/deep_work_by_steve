# Tiêu Chuẩn Khảo Sát Nghiệp Vụ & Thang SCS (Exploration Standards)

> **Mã số**: STG0-KNOW-STANDARDS
> **Vai trò**: Định hình các tiêu chuẩn đánh giá chất lượng và quy mô của Agent Skills.

---

## 1. Khung 7 Tiêu Chuẩn Vàng Tiếng Việt

Khi Explorer Agent khảo sát và chuẩn bị thiết kế một kỹ năng, bắt buộc phải đánh giá khả năng của kỹ năng đích trên 7 khía cạnh sau:

### A. Khả năng tái sử dụng (Reusability)
*   **Tiêu chuẩn**: Không được mã hóa cứng (hardcode) các bối cảnh, đường dẫn cục bộ, hoặc logic nghiệp vụ rườm rà. Skill chỉ đóng vai trò là "chương trình điều khiển hành vi", còn dữ liệu tĩnh phải nằm ngoài.
*   **Tiêu chí đánh giá**:
    *   `Rich (Đạt)`: Skill thiết kế các file tri thức độc lập tại `knowledge/` để nạp động, cho phép áp dụng cho nhiều tệp dữ liệu khác nhau.
    *   `Thin (Mơ hồ)`: Skill chỉ giải quyết một case hẹp và cụ thể (Ví dụ: "Viết kịch bản kiểm tra cho hàm checkout.ts" thay vì "Quy chuẩn viết unit test chung cho dự án").

### B. Khả năng kết hợp (Composability)
*   **Tiêu chuẩn**: Kỹ năng phải có Input/Output Contract rõ ràng, tương tác mượt mà thông qua thư mục `.skill-context/` làm kho lưu trữ trạng thái.
*   **Quy tắc giải quyết xung đột**:
    *   Khi hai kỹ năng có hướng dẫn mâu thuẫn (Ví dụ: Một bên yêu cầu cài đặt mọi gói để test nhanh, một bên yêu cầu bảo mật nghiêm ngặt chặn cài đặt), Agent bắt buộc phải thiết lập **Cơ chế Phân cấp quyền ưu tiên (Prompt Hierarchy)** trong `SKILL.md` để xác định rõ kỹ năng nào giữ vai trò neo chính.

### C. Khả năng bảo trì (Maintainability - Goldilocks Prompting Zone)
*   **Tiêu chuẩn**: Prompt của skill phải ở trong vùng "Goldilocks" - không quá dài để tránh tốn token và nhiễu ngữ cảnh, không quá ngắn dẫn đến thiếu logic chỉ dẫn.
*   **Cấu trúc 4 lớp tri thức**:
    *   `L0`: Core Constitution (`SKILL.md` dưới 700 tokens).
    *   `L1`: Operating Policies (`policy/*.md`).
    *   `L2`: Domain Knowledge (`knowledge/*.md`).
    *   `L3`: Contextual examples (`examples/*.md` hoặc `templates/`).

### D. Độ an toàn và bảo mật (Security)
*   Xem chi tiết tại `knowledge/security-standards.md`.
*   **Ranh giới an toàn**: Chống Prompt Injection thông qua thẻ XML bọc dữ liệu và Structured tool calling; chạy sandbox biệt lập cho scripts.

### E. Hiệu suất ngữ cảnh (Context Efficiency)
*   **Tiêu chuẩn**: Áp dụng triệt để mô hình **Bộc lộ lũy tiến (Progressive Disclosure)**:
    *   Only boot neo cứng Tier 1 lúc khởi động (`SKILL.md`, `guardrails.md`).
    *   Chỉ nạp tri thức domain nghiệp vụ Tier 2 khi thực hiện phase cụ thể (`workflow.md`, `exploration-standards.md`).
    *   Chỉ nạp ví dụ chi tiết Tier 3 khi chuẩn bị ghi file (`templates/*`).

### F. Tính di động (Portability)
*   **Tiêu chuẩn**: Không được trói buộc ngầm vào API đặc thù của một mô hình cụ thể, ngoại trừ các trường hợp bắt buộc. Hướng tới viết prompt độc lập, dùng ngôn ngữ tự nhiên chuẩn hóa.

### G. Khả năng phục hồi và dự phòng (Reliability & Fallback)
*   **Tiêu chuẩn**: Khi hệ thống xảy ra lỗi (API sập, sai định dạng đầu vào), Agent không được phép đoán mò (hallucinate).
*   **Hành vi bắt buộc**:
    *   Ghi nhận nhật ký (execution logging) các bước thực hiện.
    *   Kích hoạt phương án dự phòng (fallback) hoặc kích hoạt kênh Human-in-the-loop (HITL) thông qua các Stop Conditions để hỏi ý kiến người dùng.

---

## 2. Thang Đo Điểm Phức Tạp SCS (Skill Complexity Score)

Sử dụng thang đo định lượng dưới đây để tính toán **Điểm Phức tạp của Kỹ năng (Skill Complexity Score - SCS)**:

| Tiêu chí | Ngưỡng định lượng | Trọng số điểm | Điểm SCS |
|----------|-------------------|---------------|----------|
| **Số bước quy trình** | • ≤ 3 bước: 1 điểm<br/>• 4 - 5 bước: 3 điểm<br/>• > 5 bước: **5 điểm (Phải phân rã)** | 30% | |
| **Số công cụ / API tương tác** | • ≤ 2 công cụ: 1 điểm<br/>• 3 - 4 công cụ: 3 điểm<br/>• > 4 công cụ: **5 điểm (Phải phân rã)** | 30% | |
| **Kích thước chỉ dẫn SKILL.md dự kiến** | • < 800 tokens: 1 điểm<br/>• 800 - 1500 tokens: 3 điểm<br/>• > 1500 tokens: **5 điểm (Phải phân rã)** | 20% | |
| **Độ nhạy cảm an ninh (Security Risk)** | • Không chạy scripts/shell: 1 điểm<br/>• Chạy scripts đọc/quét: 3 điểm<br/>• Chạy scripts ghi/biên dịch hoặc gọi API bên thứ ba không tin cậy: **5 điểm (Phải phân rã)** | 20% | |

*   **Luật Neo cứng**:
    *   Nếu **Điểm trung bình SCS > 3.0** HOẶC **có bất kỳ tiêu chí nào đạt 5 điểm (ngưỡng đỏ)**: Explorer Agent bắt buộc phải **phủ quyết giải pháp Monolithic** và đề xuất **Hệ thống Micro-skills phối hợp**.

---

## 3. Các Mẫu Thiết Kế Phối Hợp Micro-skills

Khi phân rã kỹ năng, AI phải định hình luồng phối hợp theo các mẫu chuẩn sau:
1.  **Sequential Pipeline (Chuỗi tuần tự)**: Đầu ra của Micro-skill A là đầu vào trực tiếp của Micro-skill B thông qua tệp tin JSON bối cảnh tại `.skill-context/`.
2.  **Condition Router (Phân nhánh rẽ hướng)**: Một Micro-skill trung tâm phân tích kết quả đầu ra và điều hướng sang các Micro-skills chuyên biệt khác dựa trên điều kiện thực tế.
3.  **Meta-Orchestrator (Điều phối trung tâm)**: Sử dụng một Micro-skill chính đóng vai trò "nhạc trưởng" gọi và quản lý vòng đời của các Micro-skills phụ thuộc thông qua Subagent calls.
