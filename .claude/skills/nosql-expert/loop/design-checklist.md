# MongoDB Design Validation Checklist

<trace>[TỪ DESIGN §8]</trace>

Sử dụng checklist này để rà soát thiết kế Document Model và Indexing trước khi trình bày cho người dùng.

## 1. Document Model Boundaries
- [ ] **No 3NF Check**: Thiết kế đã từ bỏ tư duy chuẩn hóa của SQL (3NF) chưa? Việc phân tách collections phải dựa trên Access Patterns chứ không phải để tránh lặp dữ liệu.
- [ ] **Unbounded Arrays Warning**: Có mảng nào (Array) có khả năng phát triển vô hạn (ví dụ: danh sách logs, comments của một bài viết nổi tiếng) không? Nếu có, hãy chuyển sang Bucket Pattern hoặc Referencing.
- [ ] **16MB Limit Estimation**: Tổng kích thước lớn nhất dự kiến của một Document có nguy cơ vượt qua 16MB không?
- [ ] **Extended Reference Check**: Nếu sử dụng Referencing, đã áp dụng Extended Reference Pattern để tối ưu (tránh N+1 queries) cho các thuộc tính thường xuyên truy xuất chưa?

## 2. Indexing Rules (ESR)
- [ ] **Equality First**: Các trường Equality (`=`) đã được đặt ở vị trí đầu tiên trong Compound Index chưa?
- [ ] **Sort Second**: Các trường dùng cho việc sắp xếp (Sort) có được đặt ngay sau Equality không?
- [ ] **Range Last**: Các truy vấn khoảng (`$gt`, `$lt`) đã được đặt ở cuối cùng của Index chưa?
- [ ] **Covered Query**: Liệu Index này có thỏa mãn Covered Query (chứa đủ các trường cần trả về) để MongoDB không cần Fetch Document chưa?

## 3. Tool & Implementation Check
- [ ] Đã chốt được framework/driver (ví dụ: Mongoose, MongoDB Native Driver) với người dùng chưa?
- [ ] Cấu trúc JSON Schema đã được viết hoàn chỉnh, không dùng placeholder (`// TODO`, `pass`) chưa?
- [ ] Script kiểm tra `schema_validator.py` đã báo kết quả hợp lệ (Pass) chưa?
