---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "skill-explorer"
generated_by: "skill-planner"
generated_at: "2026-05-24T18:50:00Z"
stage: "planner"
status: "ready_for_builder"
trace_to_design: "design.md"
phases:
  - id: "PH0"
    name: "Chuẩn bị Tài nguyên"
    tasks:
      - id: "T0.1"
        title: "Xem xét báo cáo khảo sát của scout và cấu trúc framework"
        zone: "knowledge"
        priority: "critical"
        trace: "design.§1"
        depends_on: []
        status: "done"
        file_target: "resources/skill-explorer-scout-report.md"
        acceptance_criteria:
          - "Báo cáo của Scout đã được sao chép vào thư mục resources và được duyệt"
  - id: "PH1"
    name: "Dựng Core & Cổng Chất lượng (Quality Gate)"
    tasks:
      - id: "T1.1"
        title: "Tạo SKILL.md với 4-Phase Workflow và Core Constraints"
        zone: "core"
        priority: "critical"
        trace: "design.§3.core"
        depends_on: ["T0.1"]
        status: "pending"
        file_target: "SKILL.md"
        acceptance_criteria:
          - "SKILL.md chứa đầy đủ Boot Sequence và routing map định tuyến"
          - "Quy định rõ ràng must/must_not trong YAML để AI tuân thủ"
          - "Định nghĩa quy trình 4 Phase khảo sát tri thức"
      - id: "T1.2"
        title: "Tạo loop/exploration-checklist.md làm cổng chất lượng tự đánh giá"
        zone: "loop"
        priority: "high"
        trace: "design.§3.loop"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: "loop/exploration-checklist.md"
        acceptance_criteria:
          - "Checklist tự kiểm tra bao phủ trọn vẹn 7 Tiêu chuẩn Vàng"
          - "Kiểm tra ranh giới thẻ XML và tối ưu hóa proxy rtk"
  - id: "PH2"
    name: "Xây dựng Cơ sở Tri thức & Luật (Knowledge & Rules)"
    tasks:
      - id: "T2.1"
        title: "Tạo knowledge/security-standards.md chi tiết bảo mật"
        zone: "knowledge"
        priority: "critical"
        trace: "design.§3.knowledge"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: "knowledge/security-standards.md"
        acceptance_criteria:
          - "Chi tiết kỹ thuật bọc thẻ XML chống Prompt Injection"
          - "Quy chuẩn môi trường chạy mã biệt lập Docker Sandboxing"
      - id: "T2.2"
        title: "Tạo knowledge/exploration-standards.md đặc tả 7 tiêu chí vàng"
        zone: "knowledge"
        priority: "high"
        trace: "design.§3.knowledge"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: "knowledge/exploration-standards.md"
        acceptance_criteria:
          - "Đặc tả chi tiết cách đánh giá và tối ưu 7 Tiêu chuẩn Vàng"
          - "Định nghĩa cụ thể chuẩn đánh giá tài nguyên Rich vs Thin"
      - id: "T2.3"
        title: "Tạo data/search-blacklist.yaml để lọc bỏ file rác khi quét"
        zone: "data"
        priority: "medium"
        trace: "design.§3.data"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: "data/search-blacklist.yaml"
        acceptance_criteria:
          - "Cấu trúc YAML liệt kê các thư mục/tệp hệ thống cần loại bỏ"
  - id: "PH3"
    name: "Triển khai Tự động hóa & Mẫu Templates"
    tasks:
      - id: "T3.1"
        title: "Tạo templates/exploration.md.template cấu trúc 8 chương nghiệp vụ"
        zone: "templates"
        priority: "high"
        trace: "design.§3.templates"
        depends_on: ["T1.1"]
        status: "pending"
        file_target: "templates/exploration.md.template"
        acceptance_criteria:
          - "Cấu trúc sẵn 8 chương mục khảo sát chuẩn hóa"
      - id: "T3.2"
        title: "Viết scripts/init_context.py tự động khởi tạo"
        zone: "scripts"
        priority: "high"
        trace: "design.§3.scripts"
        depends_on: ["T3.1"]
        status: "pending"
        file_target: "scripts/init_context.py"
        acceptance_criteria:
          - "Khởi tạo thư mục và ghi chép tệp tin mẫu thành công"
blockers: []
prerequisites:
  - item: "Báo cáo nghiên cứu nghiệp vụ của Scout"
    tier: "domain"
    status: "ready"
    resource_file: "resources/skill-explorer-scout-report.md"
  - item: "Quy ước thiết kế framework 7 Zones"
    tier: "technical"
    status: "ready"
    resource_file: "_shared/knowledge/framework.md"
handoff:
  next_stage: "builder"
  ready_condition:
    required:
      blockers_empty: true
      phase0_done: true
      prerequisites_ready: true
      schema_valid: true
      design_zones_covered: true
---

# skill-explorer — Kế Hoạch Triển Khai Chi Tiết (todo.md)

> **Tệp thiết kế tham chiếu**: [design.md](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-explorer/design.md)
> **Trạng thái kế hoạch**: Sẵn sàng lập trình (`ready_for_builder`)

---

## 1. Pre-requisites

Bảng kiểm tra tính sẵn sàng của tài nguyên và tri thức trước khi chuyển giao cho Builder:

| # | Tài liệu / Kiến thức | Tier | Mục đích | Nguồn truy vết | Trạng thái |
|---|----------------------|------|----------|----------------|------------|
| 1 | Báo cáo nghiên cứu nghiệp vụ của Scout | Domain | Cung cấp tri thức nghiệp vụ về 7 Tiêu chuẩn Vàng và bảo mật | [Scout Report](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-explorer/resources/skill-explorer-scout-report.md) | ✅ Sẵn sàng |
| 2 | Quy chuẩn Master Framework 7 Zones | Technical | Đảm bảo đóng gói skill đúng tiêu chuẩn chung | [framework.md](file:///home/steve/Work-space/deep_work_by_steve/.agents/skills/_shared/knowledge/framework.md) | ✅ Sẵn sàng |
| 3 | Quy tắc định dạng cú pháp AI-First | Technical | Đảm bảo tính tuân thủ XML, YAML và Trace tags | [CLAUDE.md](file:///home/steve/Work-space/deep_work_by_steve/CLAUDE.md) | ✅ Sẵn sàng |

---

## 2. Phase Breakdown

Quy trình triển khai chia nhỏ thành các nhiệm vụ độc lập, có mối quan hệ phụ thuộc rõ ràng:

| # | Nhiệm vụ phát triển | Độ ưu tiên | Ước lượng | Nhiệm vụ phụ thuộc | Truy vết (Trace) | Trạng thái |
|---|----------------------|------------|------------|---------------------|------------------|------------|
| **PH0** | **Chuẩn bị** | | | | | |
| T0.1 | Phân tích sâu sắc báo cáo của Scout | Critical | 1h | Không có | `[TỪ DESIGN §1]` | ✅ Xong |
| **PH1** | **Dựng Core & Loop** | | | | | |
| T1.1 | Tạo cấu trúc tệp lõi `SKILL.md` | Critical | 2h | T0.1 | `[TỪ DESIGN §3.core]` | ⬜ Chờ |
| T1.2 | Tạo checklist kiểm định `loop/exploration-checklist.md` | High | 1h | T1.1 | `[TỪ DESIGN §3.loop]` | ⬜ Chờ |
| **PH2** | **Xây dựng Tri thức & Cấu hình** | | | | | |
| T2.1 | Tạo hướng dẫn an toàn `knowledge/security-standards.md` | Critical | 2h | T1.1 | `[TỪ DESIGN §3.knowledge]` | ⬜ Chờ |
| T2.2 | Tạo quy chuẩn `knowledge/exploration-standards.md` | High | 1.5h | T1.1 | `[TỪ DESIGN §3.knowledge]` | ⬜ Chờ |
| T2.3 | Tạo tệp bỏ qua tìm kiếm `data/search-blacklist.yaml` | Medium | 0.5h | T1.1 | `[TỪ DESIGN §3.data]` | ⬜ Chờ |
| **PH3** | **Tự động hóa & Bản mẫu** | | | | | |
| T3.1 | Dựng mẫu báo cáo `templates/exploration.md.template` | High | 1.5h | T1.1 | `[TỪ DESIGN §3.templates]` | ⬜ Chờ |
| T3.2 | Lập trình Python script `scripts/init_context.py` | High | 2h | T3.1 | `[TỪ DESIGN §3.scripts]` | ⬜ Chờ |

---

## 3. Knowledge & Resources Needed

Các công cụ và tài liệu bổ trợ mà Builder cần để hoàn thành tác vụ:

| Tên tài liệu / Công cụ | Vai trò bổ trợ | Hướng dẫn nạp ngữ cảnh |
|------------------------|----------------|-------------------------|
| `schema_validator.py` | Tự động kiểm tra tính hợp lệ của frontmatter | Gọi khi chạy test cục bộ |
| `handoff_validator.py` | Xác thực cổng bàn giao sang Stage 1 | Gọi trước khi đóng cổng |
| `rtk` (Rust Token Killer) | Tối ưu hóa token ngữ cảnh khi chạy CLI | Gọi proxy tự động |

---

## 4. Definition of Done

Checklist tiêu chuẩn nghiệm thu cuối cùng của sản phẩm:

- [ ] Tạo thành công toàn bộ **6 tệp tin** đã quy hoạch trong §3 Zone Mapping.
- [ ] Frontmatter của tất cả các file cấu trúc đạt chuẩn schema của validator.
- [ ] Đạt chuẩn Quality Gate: Tỷ lệ placeholder < 5% trên toàn bộ gói skill.
- [ ] Thử nghiệm thực tế chạy kịch bản khởi tạo context của Explorer Agent đạt kết quả mỹ mãn.
- [ ] Chạy thành công bộ đồng bộ hóa `skill-sync` lên hệ thống.

---

## 5. Notes

- **Ranh giới thực thi**: Builder tuyệt đối không tự ý chèn thêm file ngoài phân vùng §3 trừ khi có giải trình cụ thể.
- **Xác thực tự động**: Ưu tiên chạy xác thực handoff validator ở từng bước chuyển phase để phát hiện lỗi sớm.
