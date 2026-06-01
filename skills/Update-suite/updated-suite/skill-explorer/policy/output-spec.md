# Đặc Tả Kỹ Thuật JSON Đầu Ra (Output Specification)

> **Mã số**: STG0-POL-OUTPUT
> **Vai trò**: Cung cấp cấu trúc chính xác và các ví dụ Good/Bad của các file JSON để AI sinh dữ liệu chuẩn xác, tránh lỗi schema.

---

## 1. Cấu trúc đặc tả của `exploration.json`

Tệp `exploration.json` khảo sát nghiệp vụ và phân tích rủi ro bắt buộc phải chứa các trường thông tin sau:

```json
{
  "$schema": " đường dẫn đến schema exploration.schema.json",
  "metadata": {
    "skill_name": "tên kỹ năng dạng kebab-case",
    "version": "phiên bản dạng X.Y.Z",
    "created_at": "ISO timestamp dạng date-time",
    "lifecycle_status": "trạng thái vòng đời (raw / designed / planned / built / verified / installed)"
  },
  "problem_statement": {
    "summary": "Mô tả tóm tắt vấn đề thực tế (tối thiểu 10 ký tự)",
    "context": "Bối cảnh nghiệp vụ chi tiết của dự án (tối thiểu 20 ký tự)",
    "target_audience": "Đối tượng đích sử dụng (AI agent only / Human only / Hybrid (Human & AI))"
  },
  "technical_risks": [
    {
      "risk_name": "Tên rủi ro kỹ thuật (tối thiểu 5 ký tự)",
      "severity": "mức độ nghiêm trọng (low / medium / high / critical)",
      "description": "Mô tả chi tiết rủi ro (tối thiểu 15 ký tự)",
      "mitigation_strategy": "Phương án khắc phục chi tiết (tối thiểu 15 ký tự)"
    }
  ],
  "security_risks": [
    {
      "threat_type": "Loại đe dọa (Prompt Injection / Data Leakage / Insecure Tool Call / Arbitrary Code Execution / Other)",
      "attack_vector": "Mô tả vector tấn công (tối thiểu 15 ký tự)",
      "potential_impact": "Mô tả tác động tiềm ẩn (tối thiểu 15 ký tự)",
      "defense_mechanism": "Cơ chế phòng vệ chi tiết (tối thiểu 15 ký tự)"
    }
  ],
  "dependencies": [
    {
      "name": "tên phụ thuộc",
      "type": "loại phụ thuộc (skill / python_library / system_tool / other)",
      "version_constraint": "ràng buộc phiên bản"
    }
  ],
  "decomposed": false,
  "micro_skills": []
}
```

*Lưu ý về decomposed và micro_skills*:
Nếu kỹ năng bị phân rã, trường `decomposed` phải là `true`, và `micro_skills` chứa danh sách các micro-skills dạng:
```json
  "decomposed": true,
  "micro_skills": [
    {
      "name": "tên-micro-skill-1",
      "description": "nhiệm vụ chuyên biệt của micro-skill 1",
      "zone_recommendations": "các phân vùng zones khuyến nghị cho micro-skill 1"
    }
  ]
```

---

## 2. Cấu trúc đặc tả của `criteria.json`

Tệp `criteria.json` xác định tiêu chí nghiệm thu định lượng và các test cases mẫu:

```json
{
  "$schema": "đường dẫn đến schema criteria.schema.json",
  "metadata": {
    "skill_name": "tên kỹ năng dạng kebab-case",
    "version": "phiên bản dạng X.Y.Z",
    "updated_at": "ISO timestamp dạng date-time"
  },
  "acceptance_criteria": [
    {
      "criterion_id": "AC-01",
      "description": "Mô tả chi tiết tiêu chí (tối thiểu 10 ký tự)",
      "metric": "Chỉ số đo lường định lượng cụ thể (tối thiểu 5 ký tự)",
      "validation_method": "Phương pháp kiểm thử (sandbox_test / unit_test / static_analysis / prompt_injection_defense_test / manual_verification)"
    }
  ],
  "test_cases": [
    {
      "test_case_id": "TC-01",
      "name": "Tên test case (tối thiểu 5 ký tự)",
      "description": "Mô tả chi tiết kịch bản test (tối thiểu 15 ký tự)",
      "mock_input": {
        "mô tả cấu trúc đầu vào giả lập để chạy thử"
      },
      "expected_output": {
        "mô tả cấu trúc đầu ra mong đợi để so khớp"
      }
    }
  ]
}
```

---

## 3. Quy tắc chất lượng (Quality Enforcement)
*   **Không chứa placeholder**: Tuyệt đối không dùng các giá trị rỗng hoặc mang tính mô tả chung chung (`"TODO"`, `"pass"`, `"N/A"`, `"..."`). Mọi chuỗi ký tự phải mô tả thực tế, chi tiết.
*   **AC-ID và TC-ID chuẩn hóa**:
    *   Mã tiêu chí nghiệm thu bắt buộc tuân thủ regex `^AC-[0-9]+$` (ví dụ: `AC-01`, `AC-02`).
    *   Mã kịch bản test bắt buộc tuân thủ regex `^TC-[0-9]+$` (ví dụ: `TC-01`, `TC-02`).
*   **Mức độ bao phủ**:
    *   Có tối thiểu **5 tiêu chí nghiệm thu** rõ ràng.
    *   Có tối thiểu **2 kịch bản test-case** định lượng cụ thể.
