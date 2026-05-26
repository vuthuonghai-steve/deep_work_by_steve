# Sổ Kiểm Định Chất Lượng Khảo Sát (Exploration Checklist)

> **Mã số**: STG0-LOOP-CHECKLIST
> **Vai trò**: Chốt chặn chất lượng cuối cùng để Explorer Agent tự đánh giá trước khi kết thúc Stage 0.

---

## 📋 TIÊU CHÍ NGHIỆM THU ĐỊNH LƯỢNG

Explorer Agent bắt buộc phải tích dấu `[x]` vào toàn bộ các tiêu chí dưới đây để tự nghiệm thu đạt cổng chất lượng:

### 1. Ranh giới Sổ cái JSON có cấu trúc
- [ ] Đã chạy script `scripts/init_context.py` để khởi tạo thư mục bối cảnh thành công.
- [ ] Tệp `exploration.json` đã được tạo đầy đủ các trường và không có bất kỳ placeholder rỗng nào.
- [ ] Tệp `criteria.json` đã được tạo đầy đủ ít nhất 5 tiêu chí AC và 2 test cases định lượng cụ thể.
- [ ] Cả hai tệp JSON đều đã **vượt qua 100% xác thực schema** tại `_shared/schemas/` thông qua schema validator.

### 2. Thu thập tri thức và tài nguyên thực tế (Rich status)
- [ ] Đã quét codebase và thu thập tối thiểu 2 mã nguồn mẫu, helper functions hoặc API schema có liên quan và lưu vào `.skill-context/{skill-name}/resources/`.
- [ ] Đã quét và chắt lọc các best practices bên ngoài từ Web (nếu cần thiết) và lưu lại dưới dạng tài liệu tri thức thô bọc trong XML boundaries.
- [ ] Không có file tài nguyên nào dạng Markdown phẳng rỗng, tất cả phải được phân chủ đề rõ ràng.

### 3. Đánh giá quy mô & Phân rã Micro-skills
- [ ] Đã thực hiện thang đo điểm phức tạp **SCS (Skill Complexity Score)** đầy đủ.
- [ ] Nếu điểm SCS > 3.0 hoặc có điểm 5 (ngưỡng đỏ), đã kích hoạt Smart Context Splitter (`--split`) để phân rã bối cảnh.
- [ ] Sơ đồ Mermaid của luồng điều phối micro-skills được vẽ đầy đủ và lưu vào bối cảnh con.

### 4. Ranh giới Bảo mật & An toàn
- [ ] Đã kiểm tra và bọc toàn bộ đầu vào từ bên ngoài vào trong các thẻ XML `<external_input>` an toàn.
- [ ] Đã thiết lập các khuyến nghị bảo mật và sandbox isolation cụ thể đối với các scripts thực thi của skill đích.
- [ ] Đã dịch toàn bộ tóm tắt kỹ thuật và giải trình nghiệp vụ sang **Tiếng Việt** chất lượng cao cho người dùng.
