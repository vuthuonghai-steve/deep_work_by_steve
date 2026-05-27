# Quy Trình Vận Hành 3 Phase Chi Tiết (Architect Workflow)

> **Mã số**: STG1-POL-WORKFLOW
> **Vai trò**: Chỉ dẫn Architect thực hiện phân tích và thiết kế kiến trúc kỹ năng theo quy trình có kiểm soát chặt chẽ.

---

## Phase 1: Collect & Context Alignment (Thu Thập & Đồng Bộ Ngữ Cảnh)
*   **Mục tiêu**: Nạp và đồng bộ toàn bộ bối cảnh nghiệp vụ từ Stage 0.
*   **Hành động bắt buộc**:
    1.  Đọc hai tệp Sổ cái Bối cảnh `exploration.json` và `criteria.json` tại `.skill-context/{skill-name}/`.
    2.  Tổng hợp các mục sau từ `exploration.json`:
        -   `problem_statement` → làm căn cứ cho static_structure
        -   `technical_risks[]` → danh sách threats cần mitigation
        -   `security_risks[]` → **bắt buộc phải có entry trong `mitigation_map`**
        -   `dependencies[]` → xác định scripts/ và data/ zones cần có
    3.  Tổng hợp các mục sau từ `criteria.json`:
        -   `acceptance_criteria[]` → làm căn cứ xác định loop/checklist cần gì
        -   `test_cases[]` → xác định templates và scripts cần cho Stage 4 Tester

> **⏸️ IP-01 Gate**: Báo cáo bằng tiếng Việt danh sách files đề xuất (draft static_structure) và chờ xác nhận từ Steve trước khi sang Phase 2.

---

## Phase 2: Analyze & Structural Mapping (Phân Tích & Quy Hoạch Cấu Trúc)
*   **Mục tiêu**: Xây dựng cấu trúc hệ thống tĩnh và sequence logic động cho kỹ năng đích.
*   **Hành động bắt buộc**:

    **2.1 Thiết kế Static Structure (folder_structure)**
    *   Quy hoạch tất cả tệp vật lý cần có cho kỹ năng.
    *   Phân vùng từng tệp vào **đúng 1 trong 7 Zones** (`core`, `knowledge`, `scripts`, `templates`, `data`, `loop`, `assets`).
    *   Áp dụng Zone Decision Table từ `knowledge/design-exemplars.md §5`.
    *   **Cấm tuyệt đối**: tên file placeholder (`file1.py`, `temp.sh`, `xxx.md`).
    *   Viết `role_description` ≥ 10 ký tự thực chất cho từng tệp.

    **2.2 Thiết kế Dynamic Behavior (sequence_steps)**
    *   Định nghĩa ít nhất 1 main flow với ≥ 4 steps tuyến tính.
    *   Mỗi step có đủ: `step_number` (tăng dần từ 1), `actor`, `action` (≥5 chars), `expected_result` (≥5 chars).
    *   Tham chiếu `knowledge/visualization-guidelines.md` để vẽ sequence diagram đúng cú pháp.

    **2.3 Lập Mitigation Map (mitigation_map)**
    *   Với **mỗi** `security_risks[]` trong `exploration.json`: tạo một entry trong `mitigation_map`.
    *   Chỉ định `implemented_in_zone` — zone nào của Stage 3 Builder sẽ triển khai.
    *   Viết `implementation_strategy` ≥ 15 ký tự mô tả chiến lược kỹ thuật cụ thể.
    *   Tham chiếu `knowledge/design-exemplars.md §3` để tránh lỗi Bad Design.

---

## Phase 3: Synthesis, Validation & Publish (Tổng Hợp, Xác Thực & Xuất Bản)
*   **Mục tiêu**: Xuất bản tệp bản vẽ `blueprint.json` hợp lệ và bàn giao sạch sẽ.
*   **Hành động bắt buộc** (theo đúng thứ tự):

    1.  **Nạp template**: Đọc `templates/blueprint.json.template` để đảm bảo cấu trúc đầy đủ.
    2.  **Biên soạn blueprint.json**: Điền đầy đủ 4 sections chính:
        -   `metadata` (skill_name, version, architect_timestamp)
        -   `static_structure.folder_structure[]`
        -   `dynamic_behavior[]`
        -   `interaction_points[]` (IP-01, IP-02 bắt buộc)
        -   `mitigation_map[]`
    3.  **Chạy Checklist tự kiểm định**: Nạp `loop/design-checklist.json` và xác nhận tất cả MUST-level checks đều PASS.
    4.  **Chạy Schema Validator**:
        ```bash
        python3 skills/Update-suite/updated-suite/_shared/validators/schema_validator.py \
          --schema skills/Update-suite/updated-suite/_shared/schemas/blueprint.json \
          .skill-context/{skill-name}/blueprint.json
        ```
    5.  **Báo cáo tiếng Việt** bao gồm:
        -   Sơ đồ phân vùng 7 Zones (danh sách files theo zone)
        -   Sequence flow chính tóm tắt
        -   Kết quả validation PASS/FAIL

> **⏸️ IP-02 Gate**: Trình bày kết quả blueprint.json và validation report. Chờ nghiệm thu từ Steve trước khi bàn giao cho Stage 2 Planner.

---

## Progressive Writing Contract

> **⚠️ CRITICAL**: Ghi vào `blueprint.json` **từng phần ngay sau khi Gate confirm** — không tích lũy.

| Sau Gate | Ghi vào blueprint.json |
|----------|----------------------|
| IP-01 confirm | `metadata` + `static_structure.folder_structure[]` (draft) |
| Phase 2 hoàn tất | `dynamic_behavior[]` + `mitigation_map[]` |
| IP-02 confirm | `interaction_points[]` + finalize toàn bộ |

---

## Kết Thúc Stage 1

Sau khi IP-02 được nghiệm thu, phát biểu statement kết thúc:

```
✅ STAGE 1 COMPLETE — Blueprint validated and ready for Planner
📍 Blueprint: .skill-context/{skill-name}/blueprint.json
📊 Validation: PASS (100% schema compliant)
➡️  Next: skill-planner reads blueprint.json → generates dag_plan.json
```
