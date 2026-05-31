# 🔍 Báo cáo Khảo sát Nghiệp vụ (Stage 0): production-quality-gatekeeper

> **Tên Skill**: `production-quality-gatekeeper`
> **Mục tiêu**: Tự động khai thác ngữ cảnh để lập ra bộ tiêu chí đánh giá chất lượng cực kỳ chi tiết, nhiều lớp (layered) và chặt chẽ; thiết lập vòng lặp tự phản biện và hoàn thiện (self-refining loop) cho AI Agent cho đến khi đạt chất lượng Production-grade trong các lĩnh vực: Sáng tạo (Creative), Lập trình (Dev) và Đánh giá LLM.
> **Trạng thái**: Hoàn thành Stage 0 (Exploration)

---

## 1. Phân tích Nỗi đau & Nhu cầu (Pain Point & Needs)

* **Vấn đề cốt lõi**:
  1. **Thiếu tiêu chuẩn sản xuất (Production-grade)**: Các AI Agent hiện tại thường đưa ra câu trả lời chung chung, thiếu chiều sâu, không đạt chuẩn vận hành thực tế.
  2. **Human Criteria Limit**: Con người không đủ kiến thức chuyên sâu trong mọi lĩnh vực để đưa ra tất cả các tiêu chí đánh giá cần thiết.
  3. **Vòng lặp thủ công quá dài**: Cần trung bình hơn 10 lần chỉnh sửa thủ công (vòng lặp prompt) giữa người dùng và AI mới đạt được chất lượng tương đối chấp nhận được.
* **Giải pháp**: 
  - Skill này phải tự động hóa quá trình sinh ra **bộ tiêu chí đánh giá đa tầng cực kỳ nghiêm ngặt** (Multi-layered Quality Matrix) dựa trên đầu vào mỏng hoặc dày.
  - Sử dụng chính bộ tiêu chí này để kích hoạt một **Vòng lặp tự sửa đổi tự động (Automatic Self-Refining Loop)**. Mô hình sẽ đóng vai trò kép: vừa là Kỹ sư triển khai vừa là Chuyên gia đánh giá nghiêm khắc (Quality Critic), tự động chấm điểm và sửa đổi liên tục trong nội bộ cho đến khi đáp ứng 100% tiêu chí mới xuất kết quả cuối cùng.

---

## 2. Đánh giá 7 Tiêu chuẩn Vàng (7 Golden Standards Assessment)

1. **Reusability (Tái sử dụng)**: Cực kỳ cao. Lắp ghép được vào bất kỳ Agent nào cần xuất output chất lượng cao (làm báo cáo, viết code, viết prompt).
2. **Composability (Khả năng cấu thành)**: Hoạt động như một "Quality Gate" ở cuối pipeline của các skill khác.
3. **Maintainability (Khả năng bảo trì)**: Lưu trữ các ma trận tiêu chí (Quality Matrix) dưới dạng YAML tĩnh trong zone `data/` giúp dễ dàng cập nhật mà không cần sửa code.
4. **Security (Bảo mật)**: Phải lọc các token nhạy cảm trước khi gửi qua các vòng lặp phản biện LLM, tránh rò rỉ prompt gốc (System Prompt Leakage).
5. **Context Economics (Kinh tế ngữ cảnh)**: Sử dụng mô hình Tiết lộ lũy tiến (Progressive Disclosure). Chỉ nạp bộ tiêu chí cụ thể của lĩnh vực được yêu cầu (Creative, Dev hoặc LLM), tránh nạp toàn bộ gây tràn ngữ cảnh.
6. **Portability (Tính di động)**: Chạy thuần bằng Prompt Markdown (`SKILL.md`) kết hợp với script Python hỗ trợ chạy thử nghiệm (`scripts/loop_refiner.py`).
7. **Reliability (Độ tin cậy)**: Sử dụng chấm điểm nhị phân (Binary Scoring: Đạt/Không đạt) cho từng tiêu chí để loại bỏ sự mơ hồ của LLM.

---

## 3. Bản đồ Nghiệp vụ 3 Lĩnh vực Mục tiêu (The Triple-Domain Matrix)

Bộ tiêu chí sẽ được phân cấp thành **3 Layers (Tầng)** chặt chẽ:
* **Tầng 1: Kiến trúc & Nền tảng (Foundation & Architecture)**
* **Tầng 2: Vận hành & Hiệu năng (Operational & Efficiency)**
* **Tầng 3: Tinh tế & Trải nghiệm (Sophistication & Polish)**

### A. Lĩnh vực Sáng tạo (Creative Domain)
*   **Tầng 1**: Cấu trúc mạch truyện, tính nhất quán của nhân vật/giọng văn, mạch logic (Narrative Arc).
*   **Tầng 2**: Nhịp điệu câu từ (Pacing), tính nhạc (Cadence), tránh sử dụng các sáo ngữ AI (AI clichés như "tapestry", "delve", "testament").
*   **Tầng 3**: Chiều sâu cảm xúc (Emotional Resonance), ẩn dụ đa tầng, khả năng gợi hình không cần tả (Show, Don't Tell).

### B. Lĩnh vực Lập trình (Dev Domain)
*   **Tầng 1**: Đúng logic nghiệp vụ, xử lý lỗi (Exception Handling) toàn diện, kiểm soát điều kiện biên (Edge cases).
*   **Tầng 2**: Độ phức tạp thuật toán (Time/Space Complexity), tối ưu bộ nhớ, tính module hóa và Clean Code (SOLID).
*   **Tầng 3**: Idempotency (tính đơn trị), tính bảo mật (SQL Injection, CSRF, XSS), hiệu năng concurrency/race condition, và khả năng tự kiểm thử (Self-testability).

### C. Lĩnh vực LLM / Prompt Engineering (LLM Eval Domain)
*   **Tầng 1**: Khả năng định hướng hành vi tuyệt đối (Rule Enforcement), ranh giới XML cô lập đầu vào thô.
*   **Tầng 2**: Tối ưu hóa token (Token Economics), tránh redundency, tỷ lệ nạp Progressive Disclosure.
*   **Tầng 3**: Cơ chế tự động phát hiện lỗi và cảnh báo sớm (Alert/Recovery), chống Prompt Injection nâng cao.

---

## 4. Thiết kế Luồng Vòng lặp tự hoàn thiện (Self-Refining Loop)

Hệ thống sẽ chạy qua tối đa **10 vòng lặp** nội bộ không cần sự can thiệp của con người:

```
[Khởi tạo Output nháp]
         │
         ▼
┌──────────────────────────────────────────┐
│  Hệ thống chạy Validator (loop_refiner)  │ ◄─────────────────┐
│  - Chấm điểm Binary đạt/không đạt        │                   │
│  - Tổng hợp danh sách tiêu chí thất bại   │                   │
└────────────────────┬─────────────────────┘                   │
                     │                                         │
            [Kiểm tra kết quả]                                 │
                     │                                         │
        Có tiêu chí thất bại? ───(YES: Vòng lặp < 10) ───► [Refine Output]
                     │                                    - Chỉ sửa vùng lỗi
                     │                                    - Giữ nguyên vùng đạt
            (NO hoặc Vòng lặp >= 10)
                     │
                     ▼
             [Xuất Output Đạt chuẩn]
```

## 5. Kết luận Stage 0
Nghiệp vụ đã được xác định rất rõ ràng. Skill `production-quality-gatekeeper` sẽ là giải pháp tối ưu giúp chấm dứt trạng thái output AI chất lượng thấp. Chúng ta sẽ chuyển sang Stage 1: Thiết kế kiến trúc tệp `design.md`.

---
**STAGE 0 COMPLETE — Resources and standards ready for Architect stage**
