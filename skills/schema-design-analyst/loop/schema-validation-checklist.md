# Schema Validation Checklist

Sử dụng checklist này Ở BƯỚC CUỐI (Phase 3) để đảm bảo chất lượng Schema trước khi hoàn tất.

## 1. Zero Hallucination (Chống rác dữ liệu)
- [ ] 100% các Field quy định trong `mX-schema.yaml` CÓ TỒN TẠI ở `class-mX.yaml` gốc (Contract từ UML). 
- [ ] KHÔNG CÓ trường dữ liệu nào tự phân bổ do "thuận mồm", "nguồn ngoài", hay tự nghĩ thêm rác rưởi của AI.

## 2. Limits & NoSQL Data Size (MongoDB)
- [ ] Những collection sử dụng `array` hay `group` nhúng, đặc biệt `array` có được lý luận giới hạn tăng trưởng không?
- [ ] Array nào có khả năng lưu log theo thời gian (ví dụ: `notifications`, `comments`, `history`) bắt buộc phải TÁCH ra làm collection độc lập bằng `reference`, tuyệt đối không lưu Embed tránh giới hạn 16MB document của Mongo.

## 3. Query Efficiency (Indexing & Computed)
- [ ] Những fields hay được Filter / Sort (createdAt, user_id, status...) có khai báo chỉ thị `{ index: true }` hay không?
- [ ] Những biến thống kê `số lượng` (như counter_likes, total_spending) có được chỉ định `Computed Pattern` đi kèm Hook description thay vì tính real-time không?

## 4. Documentation Fidelity 
- [ ] Output Markdown (`mX-schema.md`) có chứa các mục `Reason` hay `Justification` cho những field Embed/Reference mang tính chất rủi ro?
- [ ] Script `validate_schema.py` đã thực hiện gọi chạy thành công để chốt hạ Field count chưa?
