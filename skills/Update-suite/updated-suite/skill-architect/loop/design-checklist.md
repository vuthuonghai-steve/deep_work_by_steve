# Chốt Chặn Chất Lượng Thiết Kế (Design Quality Checklist)

> **Mã số**: STG1-LOP-CHECK
> **Vai trò**: Cung cấp bộ câu hỏi tự kiểm định chất lượng để Architect rà soát bản vẽ blueprint.json trước khi kết thúc Stage 1.

---

## 📋 Bộ Câu Hỏi Rà Soát Chất Lượng (Quality Gates)

### 1. Tính Tuân Thủ Hợp Đồng Dữ Liệu (Schema Compliance)
- [ ] Tệp JSON đầu ra có được đặt chính xác tại đường dẫn `.skill-context/{skill-name}/blueprint.json` không?
- [ ] Tệp `blueprint.json` có vượt qua validation schema `blueprint.json` thành công 100% không?
- [ ] Metadata của bản vẽ có chứa đầy đủ: `skill_name`, `version`, và `architect_timestamp` hợp lệ không?

### 2. Sự Thực Chất Của Cấu Trúc Tĩnh (Static Structure Integrity)
- [ ] 100% các tệp vật lý đề xuất có được phân bổ khớp hoàn hảo vào enum 7 Zones không?
- [ ] Có tồn tại tệp tin ảo, tệp tin placeholder rỗng nào trong danh sách đề xuất không? (Bắt buộc PHẢI KHÔNG)
- [ ] Trường `role_description` của từng tệp đề xuất có đạt độ dài tối thiểu 10 ký tự và mô tả thực chất ranh giới trách nhiệm của tệp không?
- [ ] Bản vẽ static có chứa tối thiểu 3 tệp vật lý được quy hoạch rõ ràng không?

### 3. Logic Vận Hành Động (Dynamic Flow & Steps)
- [ ] 100% các flow được định nghĩa trong `dynamic_behavior` có chứa đầy đủ `flow_name`, `description`, và `sequence_steps` không?
- [ ] Mỗi flow có chứa tối thiểu 2 sequence steps logic không?
- [ ] Các bước sequence có được đánh số thứ tự tăng dần liên tục và có đầy đủ: `step_number`, `actor`, `action`, và `expected_result` không?

### 4. Ranh Giới Bảo Mật & Phòng Thủ (Mitigation Map Gate)
- [ ] 100% các rủi ro bảo mật phát hiện được ở Stage 0 (exploration.json) đã được ánh xạ vào `mitigation_map` chưa?
- [ ] Zone chịu trách nhiệm khắc phục ở Stage 3 có được chỉ định chính xác không?
- [ ] Chiến lược phòng thủ `implementation_strategy` có đạt độ dài tối thiểu 15 ký tự và mang tính khả thi lập trình thực tế không?
