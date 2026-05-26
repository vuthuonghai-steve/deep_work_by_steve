# BẢN ĐỒ CÔNG VIỆC CHI TIẾT (TASK.MD): MASTER SKILL SUITE VER_1.0.0

Tài liệu này phân tách và quản lý chi tiết các công việc cần triển khai dựa trên thiết kế kiến trúc chuẩn mực của [architecture.md](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/architecture.md) (Ver_3.0).

---

## 🗺️ KÝ HIỆU TIẾN ĐỘ
- `[ ]` Chưa thực hiện
- `[/]` Đang thực hiện
- `[x]` Đã hoàn thành

---

## 📋 CHI TIẾT CÁC GIAI ĐOẠN VÀ NHIỆM VỤ THỰC THI

### PHASE 0: HỒ SƠ KHẢO SÁT & SCOPING ĐẦU VÀO
- [x] Chạy khảo sát nghiệp vụ Ver_0 bằng công cụ `context-before-fix`.
- [x] Xuất bản báo cáo Scoping chuẩn tại [scope.2026-05-26.md](file:///home/steve/Work-space/deep_work_by_steve/docs/context-to-work/restructure-master-suite/scope.2026-05-26.md).
- [x] Di chuyển và đồng bộ hóa tuyệt đối bản thiết kế kiến trúc [architecture.md](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/architecture.md) (đã sửa sơ đồ Mermaid đa hướng nhất quán).

---

### PHASE 1: THIẾT LẬP PHÂN VÙNG DÙNG CHUNG (SHARED FRAMEWORK)
Mục tiêu: Đảm bảo nguyên lý DRY, loại bỏ trùng lặp file kiến thức `architect.md` cũ.
- [ ] Xây dựng tài liệu hướng dẫn khung vòng đời 6 giai đoạn chung tại `updated-suite/_shared/knowledge/framework.md`.
- [ ] Thiết lập schemas xác thực dữ liệu đầu ra:
  - [ ] `_shared/schemas/exploration.schema.yaml`
  - [ ] `_shared/schemas/criteria.schema.yaml`
  - [ ] `_shared/schemas/design.schema.yaml`
  - [ ] `_shared/schemas/todo.schema.yaml`
  - [ ] `_shared/schemas/verification.schema.yaml`

---

### PHASE 2: CẢI TỔ VÀ XÂY DỰNG 6 STAGES CHUYÊN BIỆT

#### 1. STAGE 0: skill-explorer (Cải tiến)
*Trọng tâm: Nghiên cứu domain và sinh bộ tiêu chí định lượng `criteria.md`.*
- [ ] Triển khai `skill-explorer/SKILL.md` (L0 Anchor dưới 400 tokens).
- [ ] Trích xuất logic phân tích rủi ro sang `skill-explorer/policy/guardrails.md`.
- [ ] Viết script `skill-explorer/scripts/generate_criteria.py` tự động sinh tệp `criteria.md` chứa tối thiểu 5 tiêu chí định lượng và 2 test cases.
- [ ] Xây dựng validator `skill-explorer/scripts/validate_explorer.py` để chạy chốt chặn chất lượng:
  - [ ] **❌ BAD**: Không có rủi ro kỹ thuật, thiếu test case mẫu.
  - [ ] **✅ GOOD**: Vượt qua Frontmatter Schema, có đủ 5 tiêu chí.
  - [ ] **💎 SPECIFIC ACCEPTANCE**: Có sẵn dữ liệu mock input/output chất lượng cao.

#### 2. STAGE 1: skill-architect (Cải tiến)
*Trọng tâm: Chuyển hóa criteria thành bản vẽ kiến trúc 7 Zones chuyên sâu.*
- [ ] Triển khai `skill-architect/SKILL.md` (L0 Anchor dưới 500 tokens).
- [ ] Cập nhật chỉ dẫn nạp dữ liệu: Rút quyền phân rã Micro-skills từ Explorer sang Architect.
- [ ] Xây dựng validator `skill-architect/scripts/validate_architect.py` để chạy chốt chặn chất lượng:
  - [ ] **❌ BAD**: Dùng tên file giả định, thiếu sơ đồ, thiếu Interaction Points.
  - [ ] **✅ GOOD**: 100% file mapping vật lý chính xác, có sequence flow.
  - [ ] **💎 SPECIFIC ACCEPTANCE**: Có sẵn cơ chế Rollback bối cảnh và bảng mitigation map.

#### 3. STAGE 3: skill-planner (Stage 2 - Cải tiến)
*Trọng tâm: Phân rã design thành checklist todo có trace tags đầy đủ.*
- [ ] Triển khai `skill-planner/SKILL.md` (Rút gọn từ 3000 tokens cũ về dưới 500 tokens).
- [ ] Tách logic dài dòng sang `skill-planner/policy/workflow.yaml` và `skill-planner/knowledge/standards.yaml`.
- [ ] Cập nhật script `skill-planner/scripts/validate-todo.py` để quét trace tags:
  - [ ] **❌ BAD**: Task mơ hồ, sai định dạng trace tag, sắp xếp phi logic.
  - [ ] **✅ GOOD**: 100% trace tags hợp lệ, có Phase 0 cho tài nguyên bị mỏng.
  - [ ] **💎 SPECIFIC ACCEPTANCE**: Có blocker matrix chi tiết, ước lượng Est. Hours tự động.

#### 4. STAGE 4: skill-builder (Stage 3 - Cải tiến)
*Trọng tâm: Thực thi todo checklist viết code chất lượng cao.*
- [ ] Triển khai `skill-builder/SKILL.md` (Rút gọn từ 2500 tokens cũ về dưới 500 tokens).
- [ ] Tách logic hướng dẫn Anthropic và CLAUDE.md sang `skill-builder/policy/build-guidelines.yaml`.
- [ ] Cấm Builder sửa đè ngược lên `design.md`.
- [ ] Cập nhật validator `skill-builder/scripts/validate_skill.py`:
  - [ ] **❌ BAD**: Chứa code giả/placeholder, SKILL.md mới > 700 tokens.
  - [ ] **✅ GOOD**: Code chạy thật, SKILL.md mới có frontmatter chuẩn và < 700 tokens.
  - [ ] **💎 SPECIFIC ACCEPTANCE**: Kỹ năng module hóa cực tinh gọn, có sẵn unit tests đi kèm.

#### 5. STAGE 5: skill-tester (Stage 4 - MỚI)
*Trọng tâm: Độc lập kiểm thử Sandbox và đối chiếu với criteria.md.*
- [ ] Khởi tạo thư mục `skill-tester/` và file `skill-tester/SKILL.md`.
- [ ] Viết script `skill-tester/scripts/run_sandbox_tests.py` để tự động hóa:
  - [ ] Tạo container Docker Sandbox gVisor cô lập an toàn.
  - [ ] Thực thi các test cases lấy từ `criteria.md` của Stage 0.
  - [ ] Chấm điểm Placeholder Density (Density > 5 ➔ WARNING, 10 ➔ FAIL).
- [ ] Tự động sinh báo cáo nghiệm thu `.skill-context/{skill-name}/verification.md`:
  - [ ] **❌ BAD**: Tự nghiệm thu bằng mắt không chạy sandbox, placeholder > 5.
  - [ ] **✅ GOOD**: Vượt qua 100% test cases trong Sandbox, placeholder = 0.
  - [ ] **💎 SPECIFIC ACCEPTANCE**: Tích hợp kiểm thử bảo mật chống Prompt Injection, tự động rollback khi phát hiện lỗi.

#### 6. STAGE 6: skill-indexer (Stage 5 - MỚI)
*Trọng tâm: Đóng gói, viết hướng dẫn và cập nhật llms.txt.*
- [ ] Khởi tạo thư mục `skill-indexer/` và file `skill-indexer/SKILL.md`.
- [ ] Viết script `skill-indexer/scripts/sync_catalog.py` để:
  - [ ] Tự động sinh Quick Start Guide (`README.md` tại thư mục kỹ năng).
  - [ ] Đọc và đồng bộ hóa kỹ năng mới vào chỉ mục `llms.txt`.
- [ ] Cài đặt cổng kiểm soát:
  - [ ] **❌ BAD**: Không viết tài liệu hoặc tài liệu sơ sài, quên cập nhật llms.txt.
  - [ ] **✅ GOOD**: README đầy đủ, có Good/Bad exemplars, đăng ký llms.txt thành công.
  - [ ] **💎 SPECIFIC ACCEPTANCE**: Tài liệu có Mermaid flowchart sinh động, tự động gửi thông báo deployment.

---

### PHASE 3: KIỂM THỬ KHÉP KÍN SUITE MỚI (VERIFICATION DRY-RUN)
- [ ] Kích hoạt bộ suite Ver_1.0.0 chạy thử nghiệm tạo lập một micro-skill thực tế (Ví dụ: `path-distiller`).
- [ ] Chạy độc lập từng stage trên các session LLM chat biệt lập để kiểm chứng khả năng truyền nhận bối cảnh qua Sổ cái `.skill-context/`.
- [ ] Nghiệm thu toàn bộ test cases đạt trạng thái **PASS** trong Sandbox.

---

### PHASE 4: ĐÓNG GÓI & ĐỒNG BỘ PRODUCTION DEPLOYMENT
- [ ] Ghi nhận toàn bộ quyết định thiết kế (ADRs) và nhật ký nâng cấp vào `lifecycle-docs/`.
- [ ] Kích hoạt `sync_skills.py` để đẩy toàn bộ code mới từ `updated-suite/` vào hệ thống chạy chính thức.
- [ ] Đồng bộ hóa chỉ mục toàn dự án `llms.txt` để AI có thể tự khám phá bộ suite mới.
