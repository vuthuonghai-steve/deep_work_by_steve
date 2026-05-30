# 🔍 Báo cáo Khảo sát Nghiệp vụ (Stage 0): production-code-reviewer

> **Tên Skill**: `production-code-reviewer`
> **Mục tiêu**: Thiết lập bộ máy đánh giá và phản biện mã nguồn (Code Reviewer) đạt chuẩn Production-grade, tuân thủ tuyệt đối các quy định và triết lý duyệt code chính thức của Google (Google Code Review Standards).
> **Trạng thái**: Hoàn thành Stage 0 (Exploration)

---

## 1. Phân tích Nỗi đau & Nhu cầu (Pain Point & Needs)

* **Vấn đề cốt lõi**:
  1. **Duyệt code qua loa**: AI Agent thường duyệt code ở mức cú pháp đơn giản, không phát hiện được lỗi thiết kế hệ thống, SOLID, bảo mật song song (concurrency safety) hoặc xử lý biên.
  2. **Viết comment thiếu tính xây dựng**: Nhận xét review của AI thường mơ hồ, không chỉ rõ nguyên nhân (WHY) hoặc phân cấp mức độ kỳ vọng (Must fix vs Nitpick).
  3. **Không tuân thủ Google Standards**: Thiếu các triết lý vàng của Google như: Duyệt code để cải thiện codebase health thay vì ép hoàn hảo vô ích, thời gian phản hồi dưới 1 business day, khuyên khích CL nhỏ, và tách biệt refactoring khỏi functional change.
* **Giải pháp**: 
  - Skill này sẽ đóng vai trò là một **Senior Google Code Reviewer**, tự động hóa quá trình quét tệp nguồn/diff, phát hiện các lỗi nghiêm trọng về thiết kế, thuật toán, exception, bảo mật, và style.
  - Sinh báo cáo review có tính cấu trúc cao, lịch sự, chỉ ra rõ lý do tại sao (WHY) kèm hướng dẫn sửa chi tiết, phân cấp các nhận xét rõ ràng bằng nhãn `Nit:`, `Optional:`, `FYI:`.

---

## 2. Đánh giá 7 Tiêu chuẩn Vàng (7 Golden Standards Assessment)

1. **Reusability (Tái sử dụng)**: Cực kỳ cao. Bất kỳ CL/PR nào trước khi merge vào codebase chung đều có thể sử dụng skill này để tự kiểm định.
2. **Composability (Khả năng cấu thành)**: Có thể tích hợp trực tiếp vào pre-commit hooks hoặc CI/CD pipeline.
3. **Maintainability (Khả năng bảo trì)**: Lưu trữ các luật review tĩnh trong `data/review-rules.yaml` để dễ dàng mở rộng.
4. **Security (Bảo mật)**: Phải cảnh giác cao độ khi rà soát mã nguồn chứa thông tin nhạy cảm.
5. **Context Economics (Kinh tế ngữ cảnh)**: Nạp tài liệu tri thức `google-standards.md` một cách chọn lọc bằng progressive disclosure.
6. **Portability (Tính di động)**: Chạy độc lập bằng Prompt Markdown (`SKILL.md`) kết hợp với script phân tích tĩnh bằng Python (`scripts/code_auditor.py`).
7. **Reliability (Độ tin cậy)**: Áp dụng cơ chế chấm điểm và tự động hóa qua `loop_refiner.py` của `production-quality-gatekeeper` để đảm bảo output của chính reviewer đạt chuẩn.

---

## 3. Bản đồ Phân rã Nghiệp vụ & Đánh giá Quy mô (SCS Score)

Chúng ta tiến hành chấm điểm độ phức tạp SCS (Skill Complexity Score):
* **Số bước quy trình (Process steps)**: 4 (Quét file ➔ Chạy script auditor ➔ Chấm điểm phân loại ➔ Biên soạn báo cáo). Điểm: 3.
* **Số công cụ/API khác biệt**: 3 (Đọc file, regex, linter/auditor). Điểm: 2.
* **Kích thước chỉ dẫn**: Trung bình (khoảng 350 lines). Điểm: 3.
* **Rủi ro bảo mật**: Thấp (chỉ đọc code và đưa nhận xét). Điểm: 2.
* **Kết quả SCS**: **2.5** (Độ phức tạp vừa phải, có thể tích hợp trong một skill duy nhất mà không cần phân rã sâu thêm).

---

## 4. Kế hoạch Zones của Skill

Chúng ta sẽ quy hoạch cấu trúc 7 Zones cho kỹ năng `production-code-reviewer` như sau:
* **Core**: `SKILL.md` (Định hướng Persona, chỉ dẫn từng bước duyệt code và progressive disclosure).
* **Knowledge**: `knowledge/google-standards.md` (Tài liệu tổng hợp Google Code Review Guidelines tiếng Việt do Subagent khai thác được).
* **Scripts**: `scripts/code_auditor.py` (Script Python tự động quét file code để tính toán độ phức tạp, Exception swallowing, docstring và style).
* **Data**: `data/review-rules.yaml` (Bảng tra cứu quy tắc thiết kế và mức độ vi phạm).
* **Templates**: `templates/review-report.md.template` (Mẫu xuất báo cáo review chuẩn Google).
* **Loop**: `loop/gate-checklist.yaml` (Checklist đánh giá độ sẵn sàng bàn giao của báo cáo review).

---
**STAGE 0 COMPLETE — Resources and standards ready for Architect stage**
