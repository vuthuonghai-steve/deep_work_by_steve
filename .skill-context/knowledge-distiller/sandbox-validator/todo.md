---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "sandbox-validator"
generated_by: "skill-planner"
generated_at: "2026-05-25T03:01:58+07:00"
stage: "planner"
status: "ready_for_builder"
trace_to_design: "design.md"
prerequisites:
  - item: "Docker daemon available on host"
    tier: "technical"
    status: "ready"
  - item: "distilled_draft.yaml schema definition"
    tier: "domain"
    status: "ready"
phases:
  - id: "PH1"
    name: "Chuẩn bị Tài nguyên & Thiết lập Kiến thức"
    tasks:
      - id: "T1.1"
        title: "Tạo knowledge/standards.md định nghĩa quy chuẩn an toàn gVisor và YAML schema"
        zone: "knowledge"
        priority: "high"
        trace: "design.md#3-zone-mapping"
        status: "done"
        file_target: "knowledge/standards.md"
        acceptance_criteria:
          - "Có đặc tả chi tiết về an toàn gVisor"
          - "Có hướng dẫn cấu trúc schema YAML và phòng ngừa Prompt Injection"
  - id: "PH2"
    name: "Xây dựng Scripts Thực thi Kiểm định Sandbox"
    tasks:
      - id: "T2.1"
        title: "Tạo scripts/validate.py thực thi Docker sandbox và schema validation"
        zone: "scripts"
        priority: "critical"
        trace: "design.md#3-zone-mapping"
        status: "done"
        file_target: "scripts/validate.py"
        acceptance_criteria:
          - "Kiểm tra cú pháp YAML, Markdown của tệp tin draft"
          - "Thực thi Docker container biệt lập với --network none và --runtime=runsc (hoặc fallback)"
          - "Xuất file validated_artifacts.yaml hợp lệ"
  - id: "PH3"
    name: "Xây dựng Chỉ thị Core Persona và Loop Checklist QA"
    tasks:
      - id: "T3.1"
        title: "Tạo SKILL.md định nghĩa Persona Sandbox Validator và Core Workflow"
        zone: "core"
        priority: "critical"
        trace: "design.md#3-zone-mapping"
        status: "done"
        file_target: "SKILL.md"
        acceptance_criteria:
          - "Định nghĩa rõ vai trò Sandbox Validator"
          - "Quy định chạy Docker Sandbox cô lập bảo mật"
          - "Có hướng dẫn Progressive Disclosure nạp Tier 1-3 files"
      - id: "T3.2"
        title: "Tạo loop/checklist.md chứa 6 chỉ tiêu Quality Gate kiểm định"
        zone: "loop"
        priority: "high"
        trace: "design.md#3-zone-mapping"
        status: "done"
        file_target: "loop/checklist.md"
        acceptance_criteria:
          - "Có đủ 6 chỉ tiêu QA chi tiết"
          - "Xác định rõ ngưỡng Pass/Fail"
  - id: "PH4"
    name: "Tự kiểm định E2E & Bàn giao"
    tasks:
      - id: "T4.1"
        title: "Chạy thử nghiệm E2E pipeline sandbox-validator với file mock draft"
        zone: "loop"
        priority: "high"
        trace: "design.md#5-execution-flow"
        status: "done"
        file_target: "data/validated_artifacts.yaml"
        acceptance_criteria:
          - "Thực thi thành công script validate.py"
          - "Tạo file data/validated_artifacts.yaml hợp lệ"
          - "Pass toàn bộ checklist chất lượng của micro-skill"
blockers: []
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

# sandbox-validator — Kế Hoạch Triển Khai Chi Tiết (ĐÃ HOÀN THÀNH)

> **Khởi tạo**: 2026-05-25
> **Nguồn gốc**: design.md (skill-architect output)
> **Trạng thái**: Đã hoàn thành triển khai (`completed`)

---

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | Docker Daemon | Technical | Thực thi container cô lập, bảo mật | [DESIGN §6, §12] | ✅ Sẵn sàng |
| 2 | distilled_draft.yaml schema | Domain | Định dạng YAML đầu vào từ format-converter | [DESIGN §1, §2] | ✅ Sẵn sàng |

---

## 2. Phase Breakdown

### Phase 1: Chuẩn bị Tài nguyên & Thiết lập Kiến thức

| # | Task | Priority | Zone | Trace | Status |
|---|------|----------|------|-------|--------|
| T1.1 | Tạo `knowledge/standards.md` định nghĩa quy chuẩn an toàn gVisor và YAML schema | High | knowledge | [DESIGN §3] | ✅ DONE |

---

### Phase 2: Xây dựng Scripts Thực thi Kiểm định Sandbox

| # | Task | Priority | Zone | Trace | Status |
|---|------|----------|------|-------|--------|
| T2.1 | Tạo `scripts/validate.py` thực thi Docker sandbox và schema validation | Critical | scripts | [DESIGN §3] | ✅ DONE |

---

### Phase 3: Xây dựng Chỉ thị Core Persona và Loop Checklist QA

| # | Task | Priority | Zone | Trace | Status |
|---|------|----------|------|-------|--------|
| T3.1 | Tạo `SKILL.md` định nghĩa Persona Sandbox Validator và Core Workflow | Critical | core | [DESIGN §3] | ✅ DONE |
| T3.2 | Tạo `loop/checklist.md` chứa 6 chỉ tiêu Quality Gate kiểm định | High | loop | [DESIGN §3] | ✅ DONE |

---

### Phase 4: Tự kiểm định E2E & Bàn giao

| # | Task | Priority | Zone | Trace | Status |
|---|------|----------|------|-------|--------|
| T4.1 | Chạy thử nghiệm E2E pipeline sandbox-validator với file mock draft | High | loop | [DESIGN §5] | ✅ DONE |

---

## 3. Knowledge & Resources Needed

### External References
- Docker CLI Command Reference.
- gVisor Security Architecture Guide.

### Internal Resources
- `.skill-context/knowledge-distiller/exploration.md`
- `.skill-context/knowledge-distiller/sandbox-validator/design.md`

---

## 4. Definition of Done

### Checklist — Tất cả các mục phải vượt qua
- [x] `knowledge/standards.md` được tạo với đặc tả đầy đủ về gVisor và schema YAML.
- [x] `scripts/validate.py` được triển khai hoàn chỉnh bằng Python, chạy Docker `--network none` để validate.
- [x] `SKILL.md` định nghĩa Persona và workflow chặt chẽ (< 800 tokens).
- [x] `loop/checklist.md` có đủ 6 tiêu chuẩn chất lượng.
- [x] Tự kiểm thử chạy thành công và xuất ra `data/validated_artifacts.yaml`.
- [x] Mật độ placeholders trong tất cả các tệp tin < 5%.

---

## 5. Notes
- Môi trường chạy Docker đã được kiểm chứng và hoạt động hoàn hảo. Pipeline tự động tạo ra file an toàn `data/validated_artifacts.yaml` sau khi hoàn thành.
