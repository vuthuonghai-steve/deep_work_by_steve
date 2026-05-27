# Đặc Tả Kỹ Thuật Đầu Ra (Architect Output Spec)

> **Mã số**: STG1-POL-OUTSPEC
> **Vai trò**: Định hình cấu trúc JSON bắt buộc của tệp bản vẽ thiết kế `blueprint.json` tại đầu ra của Stage 1.

---

## 1. Cấu Trúc Tổng Thể (Overall Structure)
Tệp đầu ra bắt buộc phải ghi vào đường dẫn `.skill-context/{skill-name}/blueprint.json` có cấu trúc phân cấp như sau:

```json
{
  "$schema": "../_shared/schemas/blueprint.json",
  "metadata": {
    "skill_name": "tên-kỹ-năng-kebab-case",
    "version": "1.0.0",
    "architect_timestamp": "ISO-8601-DateTime"
  },
  "static_structure": {
    "folder_structure": [
      {
        "file_path": "đường-dẫn-tập-tin-vật-lý",
        "zone": "core | knowledge | scripts | templates | data | loop | assets | _shared",
        "role_description": "Mô tả vai trò của tệp vật lý này trong kỹ năng."
      }
    ]
  },
  "dynamic_behavior": [
    {
      "flow_name": "Tên luồng hoạt động chính",
      "description": "Mô tả vai trò và chức năng của luồng này.",
      "sequence_steps": [
        {
          "step_number": 1,
          "actor": "Tác nhân (ví dụ: User, Architect, Builder)",
          "action": "Hành động thực hiện trong bước này.",
          "expected_result": "Kết quả mong đợi sau khi thực hiện hành động."
        }
      ]
    }
  ],
  "interaction_points": [
    {
      "point_id": "IP-01",
      "stage": "architect",
      "description": "Mô tả điểm dừng phê duyệt.",
      "require_user_approval": true
    }
  ],
  "mitigation_map": [
    {
      "threat_id": "Tên mối đe dọa từ exploration.json",
      "implemented_in_zone": "core | knowledge | scripts | templates | data | loop | assets",
      "implementation_strategy": "Chiến lược cụ thể để Builder lập trình khắc phục mối đe dọa."
    }
  ]
}
```

---

## 2. Quy Định Định Dạng & Xác Thực Trường (Field Specifications)

### A. Trường Metadata
*   `skill_name`: Bắt buộc viết ở dạng kebab-case chuẩn (ví dụ: `prompt-cleaner`, `skill-sync`).
*   `version`: Chuỗi định dạng Semantic Versioning `X.Y.Z`.
*   `architect_timestamp`: Chuỗi thời gian chuẩn ISO 8601 UTC.

### B. Phân Vùng folder_structure (Static Structure)
*   Mỗi tệp vật lý được đề xuất phải thuộc chính xác 1 trong 8 vùng thuộc enum `zone`.
*   Trường `role_description` của mỗi tệp phải có độ dài **tối thiểu 10 ký tự** để đảm bảo mô tả thực chất, không viết chung chung.
*   Cấu trúc tĩnh bắt buộc phải có **tối thiểu 3 tệp vật lý** được quy hoạch.

### C. Luồng Sequence Steps (Dynamic Behavior)
*   Trường `sequence_steps` trong mỗi behavior phải chứa **tối thiểu 2 bước** sequence logic.
*   Mỗi step phải có đầy đủ: `step_number` dạng số nguyên tăng dần từ 1, `actor` là danh từ chỉ tác nhân, `action` và `expected_result` có độ dài **tối thiểu 5 ký tự**.

### D. Interaction Points (IP)
*   `point_id` phải khớp với pattern định dạng `^IP-[0-9]+$` (ví dụ: `IP-01`, `IP-02`).
*   `description` có độ dài **tối thiểu 10 ký tự**.

### E. Mitigation Map
*   `threat_id` phải khớp hoàn toàn với các rủi ro bảo mật (`security_risks.threat_type`) khai báo ở `exploration.json`.
*   `implementation_strategy` có độ dài **tối thiểu 15 ký tự** mô tả chi tiết chiến thuật thực tế.
