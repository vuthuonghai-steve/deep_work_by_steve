---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "source-gatherer"
generated_by: "skill-planner"
generated_at: "2026-05-25T03:05:00+07:00"
stage: "planner"
status: "ready_for_builder"
trace_to_design: "design.md"
phases:
  - id: "PH0"
    name: "Resource Preparation"
    tasks:
      - id: "T0.1"
        title: "Đọc hiểu tài liệu thiết kế design.md và master exploration."
        zone: "knowledge"
        priority: "critical"
        trace: "[TỪ DESIGN §1]"
        status: "done"
        acceptance_criteria:
          - "Đọc và hiểu rõ kiến trúc 7 zones và 12 chương mục của source-gatherer."
      - id: "T0.2"
        title: "Khảo sát tài nguyên CLAUDE.md và các tiêu chuẩn bảo mật XML."
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        status: "done"
        acceptance_criteria:
          - "Nắm vững nguyên lý bọc XML và chống Prompt Injection."
  - id: "PH1"
    name: "Core & Supporting Implementation"
    tasks:
      - id: "T1.1"
        title: "Triển khai tệp SKILL.md (Persona cào quét, lọc và đóng gói XML boundaries)."
        zone: "core"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        status: "pending"
        file_target: "skills/rebuild/source-gatherer/SKILL.md"
        acceptance_criteria:
          - "Chỉ thị AI cực kỳ gọn gàng < 600 tokens."
          - "Quy định rõ Persona quét và đóng gói XML boundaries."
      - id: "T1.2"
        title: "Triển khai tệp knowledge/standards.md (Tiêu chuẩn kỹ thuật bọc XML, chống Prompt Injection)."
        zone: "knowledge"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        status: "pending"
        file_target: "skills/rebuild/source-gatherer/knowledge/standards.md"
        acceptance_criteria:
          - "Nêu rõ tiêu chuẩn bọc XML boundary."
          - "Các biện pháp chống Prompt Injection chi tiết."
      - id: "T1.3"
        title: "Triển khai cấu hình loại trừ data/search-blacklist.yaml."
        zone: "data"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        status: "pending"
        file_target: "skills/rebuild/source-gatherer/data/search-blacklist.yaml"
        acceptance_criteria:
          - "Chứa danh sách glob patterns loại trừ file rác và dependencies."
  - id: "PH2"
    name: "Automation Scripts & QA Validation"
    tasks:
      - id: "T2.1"
        title: "Triển khai mã nguồn Python scripts/gather.py."
        zone: "scripts"
        priority: "critical"
        trace: "[TỪ DESIGN §3]"
        status: "pending"
        depends_on:
          - "T1.3"
        file_target: "skills/rebuild/source-gatherer/scripts/gather.py"
        acceptance_criteria:
          - "Quét thư mục recursively."
          - "Lọc các tệp khớp blacklist globs từ data/search-blacklist.yaml."
          - "Bọc nội dung thô trong cặp thẻ XML <external_input>..."
          - "Mã nguồn Python thực tế, hoạt động tốt."
      - id: "T2.2"
        title: "Triển khai tệp QA loop/checklist.md."
        zone: "loop"
        priority: "high"
        trace: "[TỪ DESIGN §3]"
        status: "pending"
        file_target: "skills/rebuild/source-gatherer/loop/checklist.md"
        acceptance_criteria:
          - "Bản checklist QA kiểm soát chất lượng E2E."
blockers: []
prerequisites:
  - item: "Domain knowledge about source-gatherer"
    tier: "domain"
    status: "ready"
    resource_file: "knowledge/standards.md"
  - item: "Technical standards for XML wrapping"
    tier: "technical"
    status: "ready"
    resource_file: "knowledge/standards.md"
  - item: "Skill directory and files layout conventions"
    tier: "packaging"
    status: "ready"
    resource_file: "CLAUDE.md"
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
# source-gatherer — Kế Hoạch Triển Khai (Implementation Plan)

> **Khởi tạo**: 2026-05-25 | Bởi `skill-planner`
> **Trạng thái**: `ready_for_builder`
> **Bản thiết kế nguồn**: [design.md](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/knowledge-distiller/source-gatherer/design.md)

---

## 1. Yêu cầu Tiền đề (Pre-requisites)

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|---|---|---|---|---|
| 1 | Domain knowledge about source-gatherer | Domain | Hiểu sâu về thu thập và bọc dữ liệu XML | [TỪ DESIGN §2] | ✅ Ready |
| 2 | Technical standards | Technical | Quy tắc chống Prompt Injection qua XML boundaries | [TỪ DESIGN §3] | ✅ Ready |
| 3 | Output packaging format | Packaging | Tuân thủ cấu trúc thư mục của dự án | [TỪ DESIGN §3] | ✅ Ready |

---

## 2. Phân Rã Các Giai Đoạn (Phase Breakdown)

### Phase 0: Chuẩn bị tài nguyên (Resource Preparation)

| # | Nhiệm vụ (Task) | Phân vùng (Zone) | Độ ưu tiên | Phụ thuộc | Trace | Trạng thái |
|---|------|-----------|------------|-----------|-------|---|
| T0.1 | Đọc hiểu tài liệu thiết kế design.md và master exploration | `knowledge` | Critical | — | [TỪ DESIGN §1] | ✅ done |
| T0.2 | Khảo sát tài nguyên CLAUDE.md và các tiêu chuẩn bảo mật XML | `knowledge` | High | — | [TỪ AUDIT TÀI NGUYÊN] | ✅ done |

### Phase 1: Triển khai Cốt lõi & Tri thức (Build Core & Knowledge)

| # | Nhiệm vụ (Task) | Phân vùng (Zone) | Độ ưu tiên | Phụ thuộc | Trace | Trạng thái |
|---|------|-----------|------------|-----------|-------|---|
| T1.1 | Triển khai tệp `SKILL.md` (AI instructions) | `core` | Critical | — | [TỪ DESIGN §3] | ⬜ pending |
| T1.2 | Triển khai tệp `knowledge/standards.md` (Tiêu chuẩn kỹ thuật bọc XML, chống Prompt Injection) | `knowledge` | High | — | [TỪ DESIGN §3] | ⬜ pending |
| T1.3 | Triển khai cấu hình loại trừ `data/search-blacklist.yaml` | `data` | High | — | [TỪ DESIGN §3] | ⬜ pending |

### Phase 2: Triển khai Scripts Tự động & QA (Automation Scripts & QA)

| # | Nhiệm vụ (Task) | Phân vùng (Zone) | Độ ưu tiên | Phụ thuộc | Trace | Trạng thái |
|---|------|-----------|------------|-----------|-------|---|
| T2.1 | Triển khai mã nguồn Python `scripts/gather.py` | `scripts` | Critical | T1.3 | [TỪ DESIGN §3] | ⬜ pending |
| T2.2 | Triển khai tệp QA `loop/checklist.md` | `loop` | High | — | [TỪ DESIGN §3] | ⬜ pending |

---

## 3. Tri thức & Tài nguyên cần thiết (Knowledge & Resources Needed)

| # | Tài nguyên | Loại | Vị trí | Trạng thái |
|---|----------|------|----------|--------|
| 1 | [design.md](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/knowledge-distiller/source-gatherer/design.md) | Quyết định | `.skill-context/knowledge-distiller/source-gatherer/design.md` | ✅ Sẵn có |
| 2 | [exploration.md](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/knowledge-distiller/exploration.md) | Tham chiếu | `.skill-context/knowledge-distiller/exploration.md` | ✅ Sẵn có |

---

## 4. Tiêu chí hoàn thành (Definition of Done)

- [ ] Tệp `SKILL.md` được sinh và tối ưu hóa ngân sách token (< 600 tokens).
- [ ] Tệp `knowledge/standards.md` mô tả chi tiết tiêu chuẩn bọc XML và an toàn bảo mật.
- [ ] Tệp `data/search-blacklist.yaml` định nghĩa đầy đủ các glob patterns loại trừ file rác.
- [ ] Script Python `scripts/gather.py` hoạt động hoàn chỉnh, chạy thành công việc quét và tạo ra tệp `data/raw_source.xml` bọc XML an toàn.
- [ ] Tệp `loop/checklist.md` được triển khai đầy đủ và tất cả các mục QA đều đạt yêu cầu.
- [ ] Toàn bộ các task trong Phase Breakdown được đánh dấu là hoàn tất (`done`).

---

## 5. Ghi chú (Notes)

- Các câu hỏi mở được ghi nhận từ [design.md](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/knowledge-distiller/source-gatherer/design.md) §9:
  - *Có nên hỗ trợ cào quét trực tiếp các URL trên Web trong phiên bản này không?* -> [CẦN LÀM RÕ] Hiện tại ưu tiên quét codebase nội bộ, tích hợp web-scraper trong tương lai.
