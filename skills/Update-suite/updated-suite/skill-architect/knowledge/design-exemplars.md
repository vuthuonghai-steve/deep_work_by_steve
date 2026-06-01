# Danh Mục Ví Dụ Thiết Kế Chuẩn (Design Exemplars v2.0)

> **Mã số**: STG1-KNW-EXEMPLAR
> **Vai trò**: Cung cấp các ví dụ Good/Bad thực tế để Architect tránh lỗi khi tạo `blueprint.json`. Kèm Quick Reference và Token Budget guidance.

---

## 1. Ví Dụ Về Cấu Trúc Tĩnh (Static Structure)

### ❌ Thiết Kế Tồi (BAD — Placeholder Names)
*   **Đặc điểm**: Tên file placeholder chung chung, phân bổ sai zone, `role_description` rỗng tuếch.
```json
{
  "static_structure": {
    "folder_structure": [
      { "file_path": "file1.py",       "zone": "core",    "role_description": "Code chính." },
      { "file_path": "temp_script.sh", "zone": "scripts", "role_description": "Chạy thử." },
      { "file_path": "todo.txt",       "zone": "loop",    "role_description": "Việc cần làm." }
    ]
  }
}
```
*   **Lỗi**: `file1.py` ở zone `core` sai (chỉ SKILL.md mới ở `core`). Tên file ảo, mô tả < 10 ký tự thực chất.

### ✅ Thiết Kế Tốt (GOOD — Physical filenames + correct zones)
```json
{
  "static_structure": {
    "folder_structure": [
      {
        "file_path": "SKILL.md",
        "zone": "core",
        "role_description": "File L0 Anchor tối cao điều hướng, chứa boot sequence và metadata của kỹ năng."
      },
      {
        "file_path": "knowledge/exploration-standards.md",
        "zone": "knowledge",
        "role_description": "Tài liệu 7 Tiêu chuẩn Vàng và thang SCS đánh giá độ phức tạp skill."
      },
      {
        "file_path": "scripts/init_context.py",
        "zone": "scripts",
        "role_description": "Script Python khởi tạo thư mục bối cảnh và tạo JSON ledgers mẫu hợp lệ."
      },
      {
        "file_path": "loop/exploration-checklist.md",
        "zone": "loop",
        "role_description": "Chốt chặn chất lượng Stage 0 — tự kiểm định trước khi hoàn thành."
      }
    ]
  }
}
```

---

## 2. Ví Dụ Về Dynamic Behavior (Sequence Steps)

### ❌ Thiết Kế Tồi (BAD — Thiếu steps, mô tả mơ hồ)
```json
{
  "dynamic_behavior": [
    {
      "flow_name": "main",
      "description": "Luồng chính.",
      "sequence_steps": [
        { "step_number": 1, "actor": "AI", "action": "Làm gì đó.", "expected_result": "Xong." }
      ]
    }
  ]
}
```
*   **Lỗi**: Chỉ có 1 step (cần ≥ 2). `action` và `expected_result` < 5 ký tự thực chất.

### ✅ Thiết Kế Tốt (GOOD — Rõ ràng từng bước)
```json
{
  "dynamic_behavior": [
    {
      "flow_name": "Context Initialization Flow",
      "description": "Luồng khởi tạo bối cảnh và thiết lập JSON ledgers cho skill mới.",
      "sequence_steps": [
        {
          "step_number": 1,
          "actor": "User",
          "action": "Gửi yêu cầu tạo skill mới kèm mô tả nghiệp vụ.",
          "expected_result": "Agent nhận yêu cầu và bắt đầu Phase 1 boot sequence."
        },
        {
          "step_number": 2,
          "actor": "Explorer Agent",
          "action": "Chạy scripts/init_context.py để khởi tạo thư mục .skill-context/{name}/.",
          "expected_result": "Thư mục bối cảnh và 2 JSON ledgers mẫu được tạo thành công."
        },
        {
          "step_number": 3,
          "actor": "Explorer Agent",
          "action": "Quét codebase và web để thu thập tri thức nghiệp vụ vào resources/.",
          "expected_result": "Tài nguyên được phân loại và lưu vào thư mục resources/."
        },
        {
          "step_number": 4,
          "actor": "Explorer Agent",
          "action": "Điền đầy đủ exploration.json và criteria.json rồi chạy schema validation.",
          "expected_result": "Cả hai JSON ledgers vượt qua 100% schema validation, sẵn sàng cho Architect."
        }
      ]
    }
  ]
}
```

---

## 3. Ví Dụ Về Mitigation Map (Bản Đồ Phòng Thủ)

### ❌ Thiết Kế Tồi (BAD — Vague strategy, sai zone)
```json
{
  "mitigation_map": [
    {
      "threat_id": "Prompt Injection",
      "implemented_in_zone": "knowledge",
      "implementation_strategy": "Viết tài liệu khuyên AI tránh bị hack."
    }
  ]
}
```
*   **Lỗi**: Viết tài liệu ở `knowledge` không thể giải quyết Prompt Injection. Phải phòng ngự ở `core` và `scripts`.

### ✅ Thiết Kế Tốt (GOOD — Specific zone + concrete strategy)
```json
{
  "mitigation_map": [
    {
      "threat_id": "Prompt Injection",
      "implemented_in_zone": "core",
      "implementation_strategy": "Bọc toàn bộ dữ liệu thô từ web hoặc file ngoài vào thẻ XML <external_input> trong SKILL.md và thiết lập Directive Separation cứng."
    },
    {
      "threat_id": "JSON Parsing and Validation Failures",
      "implemented_in_zone": "scripts",
      "implementation_strategy": "Tích hợp thư viện jsonschema Python vào init_context.py để tự động validate ngay khi tạo file, reject và log lỗi nếu không khớp schema."
    }
  ]
}
```

---

## 4. Ví Dụ Về Interaction Points

### ✅ Chuẩn (IP-01 và IP-02 bắt buộc)
```json
{
  "interaction_points": [
    {
      "point_id": "IP-01",
      "stage": "architect",
      "description": "Dừng lại báo cáo phân vùng 7 Zones tĩnh (folder_structure) và chờ xác nhận từ Steve trước khi thiết kế sequence steps.",
      "require_user_approval": true
    },
    {
      "point_id": "IP-02",
      "stage": "architect",
      "description": "Dừng lại báo cáo toàn bộ blueprint.json và chờ nghiệm thu từ Steve trước khi bàn giao cho Planner.",
      "require_user_approval": true
    }
  ]
}
```

---

## 5. Zone Decision Table — Khi nào dùng Zone nào

| Zone | Required khi | File ví dụ thực tế |
|------|-------------|-------------------|
| `core` | **Luôn luôn** | `SKILL.md`, `policy/guardrails.md`, `policy/workflow.md` |
| `knowledge` | Skill cần domain knowledge | `knowledge/standards.md`, `knowledge/concepts.md` |
| `scripts` | Cần automation hoặc validation | `scripts/init_context.py`, `scripts/validator.py` |
| `templates` | Cần output format chuẩn | `templates/blueprint.json.template` |
| `data` | Cần config tĩnh hoặc blacklist | `data/search-blacklist.yaml`, `data/config.json` |
| `loop` | Cần self-verification | `loop/checklist.md`, `loop/checklist.json` |
| `assets` | Hiếm — chỉ khi có hình ảnh/đồ họa | `assets/diagram.png` |

---

## 6. Quick Reference — Field Validation Rules

| Field | Rule | Ví dụ sai | Ví dụ đúng |
|-------|------|-----------|-----------|
| `file_path` | Tên vật lý, không placeholder | `file1.py`, `xxx.md` | `scripts/init_context.py` |
| `zone` | Thuộc enum 7 Zones | `"main"`, `"utility"` | `"scripts"`, `"knowledge"` |
| `role_description` | ≥ 10 ký tự thực chất | `"Code chính."` | `"Script Python khởi tạo thư mục bối cảnh..."` |
| `step_number` | Tăng dần từ 1 | `0`, random | `1, 2, 3, 4` |
| `action` | ≥ 5 ký tự thực chất | `"Do X."` | `"Chạy script init_context.py để..."` |
| `point_id` | Pattern `^IP-[0-9]+$` | `"IP_01"`, `"ip01"` | `"IP-01"`, `"IP-02"` |
| `implementation_strategy` | ≥ 15 ký tự thực chất | `"Dùng sandbox."` | `"Tích hợp jsonschema vào script để validate..."` |

---

## 7. Token Budget cho blueprint.json

```yaml
blueprint_json_budget:
  excellent: "2KB - 5KB"
  acceptable: "5KB - 8KB"
  warning: "8KB - 10KB (gần ngưỡng max)"
  overloaded: "> 10KB — Hard Rejection bởi guardrails.md"

section_guidance:
  static_structure: "Khoảng 1-3KB tùy số lượng tệp đề xuất"
  dynamic_behavior: "Khoảng 1-2KB — chỉ cần main flow + 1 alternative nếu có"
  interaction_points: "< 500 bytes — 2 IP là đủ"
  mitigation_map: "Khoảng 500B-1KB tùy số lượng threats từ exploration.json"
```

> **Nếu vượt 10KB**: Rút gọn `role_description` — giữ tối thiểu 10 ký tự. Thu gọn `sequence_steps` — chỉ giữ các bước có sự thay đổi trạng thái quan trọng.
