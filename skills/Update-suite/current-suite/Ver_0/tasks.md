# CỘT MỐC NGHIỆM THU KIẾN TRÚC: MASTER SKILL SUITE (VER_2.0.0)

Tài liệu này quản lý chi tiết các cột mốc lớn để thực hiện nghiệm thu cấu trúc thiết kế Clean & Solid của Ver_2.0.0 dựa trên tệp [architecture.md](file:///home/stveve/Documents/workspace/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/architecture.md).

---

## 🗺️ KÝ HIỆU TIẾN ĐỘ
- `[ ]` Chưa thực hiện
- `[/]` Đang thực hiện
- `[x]` Đã hoàn thành

---

## 📋 CÁC CỘT MỐC LỚN VÀ TIÊU CHÍ NGHIỆM THU ĐỊNH LƯỢNG

### MỐC 0: DUYỆT THIẾT KẾ KIẾN TRÚC TỐI ƯU (HITL GATE 0) [x]
- [x] Phân tích điểm thắt và đề xuất giải pháp kiến trúc Ver_2.0.0
- [x] Cập nhật bản vẽ kiến trúc gốc [architecture.md](file:///home/stveve/Documents/workspace/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/architecture.md) theo hướng Clean, Solid, Modular, Dynamic và có Post-Build Lifecycle
- [x] Nhận phản hồi phê duyệt thiết kế từ Steve tại Chat UI

---

### MỐC 1: HIỆN THỰC HÓA RANH GIỚI DỮ LIỆU (STRUCTURED CONTRACTS) [/]
Mục tiêu: Đảm bảo tính phi trạng thái (Statelessness) và khả năng parse tự động chính xác 100% của AI thông qua JSON có cấu trúc.
- [x] Xây dựng bộ Schemas JSON (`.schema.json`) chuẩn hóa cho các tệp trung gian của Sổ cái Bối cảnh tại `_shared/schemas/`:
  - [x] `exploration.schema.json` (Tích hợp phân tích rủi ro Prompt Injection định lượng)
  - [x] `criteria.schema.json` (Định hình rõ cấu trúc test cases định lượng mẫu)
  - [x] `blueprint.json` (Thiết lập cấu trúc 7 Zones vật lý và Mitigation Map)
  - [x] `dag_plan.json` (Ma trận phụ thuộc công việc DAG và trace tags)
  - [x] `verification.json` (Định dạng kết quả Sandbox và điểm số toán học)
  - [x] `diagnostic.json` (Cấu trúc chẩn đoán lỗi rollback chi tiết)
- [/] Xác minh 100% việc truyền nhận dữ liệu giữa các Stage đi qua Sổ cái JSON thành công, không dùng Markdown phẳng làm trung gian.

---

### MỐC 2: THIẾT LẬP KIẾN TRÚC MULTI-AGENT & CÔ LẬP SUBAGENTS [ ]
Mục tiêu: Spawn subagent cô lập để thực thi sandbox an toàn, tránh tràn log và chống Prompt Injection.
- [ ] Xây dựng **Giao thức Đóng gói Ngữ cảnh (Context Packaging)** tinh giản cho Subagents:
  - [ ] Triệt tiêu thông tin thừa, chỉ nạp L0 Anchor + Structured JSON cần thiết.
- [ ] Triển khai `skill-tester/scripts/spawn_tester.py` tại Stage 4:
  - [ ] Tự động spawn một `Tester Subagent` cô lập.
  - [ ] Truyền gói ngữ cảnh tối giản qua `invoke_subagent`.
- [ ] Xác minh Tester Subagent chạy Sandbox độc lập, không làm tràn log rác về session chính và trả kết quả chắt lọc về thành công.

---

### MỐC 3: HOÀN THIỆN VÒNG LẶP PHỤC HỒI KHÉP KÍN (CASE RECOVERY @ 85%) [ ]
Mục tiêu: Đạt tỷ lệ tự động sửa lỗi thành công (SCR) >= 80% dựa trên chỉ số tự tin tính toán thực tế.
- [ ] Cài đặt thuật toán phát hiện Semantic Placeholders thực chất (chặn đứng mock logic rỗng, hàm return mock cứng).
- [ ] Cài đặt công thức tính toán **Fact-Based Confidence Score** tại Stage 4:
  - [ ] Chỉ số tự tin = $0.4 \times (\text{Pass Rate}) + 0.3 \times (1 - \text{Semantic Placeholders}) + 0.3 \times (\text{Static Analysis})$.
- [ ] Cài đặt cơ chế sinh tệp `diagnostic.json` khi chỉ số tự tin < 85%.
- [ ] Xác minh vòng lặp tự sửa lỗi (Closed-Loop Diagnostic) tự động re-route về Stage 1 hoặc Stage 2 thành công, sửa lỗi thành công trong tối đa 3 vòng lặp mà không cần Steve can thiệp.

---

### MỐC 4: QUẢN LÝ VÒNG ĐỜI VÀ GIAO THỨC ĐỒNG BỘ RUNTIME AN TOÀN [ ]
Mục tiêu: Đăng ký vòng đời tự động và cài đặt runtime nguyên tử (Atomic Swap) để tránh làm crash agent đang chạy.
- [ ] Triển khai Giao thức Đăng ký Vòng đời Tự động tại Stage 5 (Indexer):
  - [ ] Tự động đăng ký Metadata (Version, Confidence Score, Capability Map) vào `.skill-context/registry/README.md` và `llms.txt`.
- [ ] Triển khai **Giao thức Hoán đổi Nguyên tử (Atomic Staging Swap)** tại `skill-sync`:
  - [ ] Tạo thư mục tạm thời `.hermes/skills/.staging/{skill-name}/`.
  - [ ] Chạy dry-run test tại staging.
  - [ ] Thực hiện hoán đổi nguyên tử (atomic swap/mv) thư mục staging thành production runtime an toàn tuyệt đối.

---

### MỐC 5: XÁC MINH KIẾN TRÚC TOÀN PHẦN (DRY-RUN) & TỰ HỌC [ ]
Mục tiêu: Kiểm chứng hệ thống tự học từ các sự cố sandbox sang chuẩn standards.md.
- [ ] Cài đặt **Module Tự động Trích xuất Tri thức (Knowledge Distiller)** tại Stage 5:
  - [ ] Trích xuất tự động bài học kinh nghiệm từ sandbox thành cấu trúc chuẩn standards.md (Constraints dạng YAML, Explanation dạng Markdown, Examples dạng XML tags) ghi vào `knowledge/experience/`.
- [ ] Thực hiện dry-run toàn phần xây dựng micro-skill `path-distiller` từ đầu vào Gate 0.
- [ ] Nghiệm thu toàn bộ 5 chỉ số thành công của bản thiết kế:
  - [ ] **ZPI:** Mật độ placeholder = 0% thực chất.
  - [ ] **SCR:** Tỷ lệ tự sửa lỗi thành công >= 80%.
  - [ ] **SAA:** Tỷ lệ độc lập của Tester Subagent = 100%.
  - [ ] **ECC:** Tester sinh thành công 2 Edge Cases độc lập.
  - [ ] **KRL:** Số lượng tool calls nạp skill của AI giảm xuống dưới 3 cuộc gọi.
