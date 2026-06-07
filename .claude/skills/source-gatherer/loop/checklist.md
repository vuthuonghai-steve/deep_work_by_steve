# Danh Sách QA Kiểm Soát Chất Lượng (Quality Gate Checklist)

Bản checklist này được sử dụng bởi `source-gatherer` Agent để tự kiểm định chất lượng và an toàn trước khi bàn giao kết quả (handoff) cho giai đoạn tiếp theo.

---

## 1. Xác Minh Cấu Trúc File & Phân Vùng (Zone Mapping Verification)

- [ ] Tệp `SKILL.md` tồn tại ở thư mục gốc của skill.
- [ ] Tệp `knowledge/standards.md` tồn tại và ghi nhận đầy đủ tiêu chuẩn bọc XML.
- [ ] Script Python `scripts/gather.py` tồn tại và có quyền thực thi.
- [ ] Tệp cấu hình `data/search-blacklist.yaml` tồn tại và định nghĩa đầy đủ patterns loại trừ.
- [ ] Tệp `loop/checklist.md` (chính là file này) tồn tại đầy đủ.

---

## 2. Kiểm Soát Chỉ Thị AI & Token Budget (AI Instruction & Token Budget)

- [ ] Tệp `SKILL.md` có kích thước cực kỳ tối ưu, **dưới 600 tokens** để duy trì hiệu năng nạp ngữ cảnh Tier 1.
- [ ] Persona định nghĩa rõ ràng vai trò của một chuyên gia cào quét, làm sạch và đóng gói dữ liệu an toàn.
- [ ] Không chứa mã nguồn (no monolithic code) bên trong `SKILL.md` — tất cả logic tự động hóa được chuyển sang `scripts/gather.py`.

---

## 3. Kiểm Định Tính Năng Script Quét (Script Functionality & Guardrails)

- [ ] Script `scripts/gather.py` quét đệ quy thành công thư mục đích được chỉ định.
- [ ] Lọc bỏ 100% các tệp tin và thư mục rác nằm trong danh sách `data/search-blacklist.yaml`.
- [ ] Bỏ qua các tệp tin nhị phân và các tệp tin đơn lẻ vượt quá kích thước giới hạn (500KB).
- [ ] Ranh giới XML được bọc đúng chuẩn thẻ `<external_input>` và nội dung thô được bọc an toàn trong `<![CDATA[ ... ]]>`.
- [ ] Script xử lý và escape an toàn chuỗi `]]>` nếu xuất hiện trong nội dung file thô để tránh vỡ CDATA.
- [ ] Tệp đầu ra `data/raw_source.xml` được tạo lập thành công và đúng định dạng XML hợp lệ.

---

## 4. Bảo Mật & Phòng Chống Directory Traversal

- [ ] Script quét sử dụng đường dẫn chuẩn hóa (`os.path.abspath` hoặc `pathlib.Path.resolve()`) để ngăn chặn Directory Traversal.
- [ ] Không ghép chuỗi thô của người dùng vào các câu lệnh hệ thống (Shell Execution) để phòng ngừa Shell Injection.
