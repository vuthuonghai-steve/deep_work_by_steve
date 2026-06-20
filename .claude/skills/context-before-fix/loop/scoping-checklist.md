# Scoping Checklist — Quality Gates

> **Purpose**: Self-check trước khi deliver scope document tích hợp Codegraph & Fallback.
> **Skill**: context-before-fix v1.1.0
> **Language**: Tiếng Việt
> **Date**: 2026-06-05

---

## Pre-Scoping Checks

```yaml
pre_scoping:
  - [ ] Issue description rõ ràng
  - [ ] Kiểm tra trạng thái Codegraph MCP với timeout tối đa 5000ms
  - [ ] Cờ USE_CODEGRAPH được thiết lập tương ứng (True nếu sẵn sàng, False nếu timeout/lỗi)
  - [ ] Entry point đã được xác định sơ bộ
  - [ ] Feature area đã được xác định
  - [ ] User đã confirm scope (nếu cần)
```

---

## Discovery Phase Checks

```yaml
discovery_checks:
  codegraph_status:
    - [ ] Đã chạy codegraph_status hoặc query test trước khi bắt đầu
    - [ ] Phản hồi từ codegraph MCP dưới 5000ms
  
  entry_point_verified:
    - [ ] Entry point đã được read/view bằng view_file để đối chiếu thực tế
    - [ ] Entry point line(s) và symbol name đã được ghi nhận chính xác
  
  scoping_pathway:
    - [ ] Nếu USE_CODEGRAPH == True:
        - [ ] Sử dụng codegraph_search / codegraph_context để tra cứu symbol
        - [ ] Sử dụng codegraph_callers để truy vết upstream callers
        - [ ] Sử dụng codegraph_callees để truy vết downstream callees
    - [ ] Nếu USE_CODEGRAPH == False (Fallback):
        - [ ] Sử dụng grep_search tìm usages và import reference
        - [ ] Sử dụng find_by_name để tìm file theo mẫu đặt tên
  
  related_files_found:
    - [ ] Kết quả tìm kiếm đã được review kỹ lưỡng
    - [ ] ≥1 related files đã được xác định
```

---

## Analysis Phase Checks

```yaml
analysis_checks:
  impact_mapping_complete:
    direct_impact:
      - [ ] Tất cả directly affected files đã được list
      - [ ] Specific line(s) đã được ghi nhận
      - [ ] Bản chất vấn đề và logic cần sửa đã được mô tả
    
    indirect_impact:
      - [ ] Sử dụng codegraph_impact (nếu dùng graph) hoặc LLM reasoning để map lan truyền
      - [ ] Callers và Callees gián tiếp đã được xác định
      - [ ] Shared dependencies đã được ghi nhận
    
    api_contracts:
      - [ ] Affected endpoints đã được xác định
      - [ ] Các thay đổi tiềm ẩn đối với API contract đã được ghi chú
  
  anti_stale_checks:
    - [ ] Đã chạy view_file kiểm tra chéo các nút quan trọng trên call chain
    - [ ] Không có sự sai lệch giữa đồ thị AST của Codegraph và code thực tế trên đĩa
    - [ ] Nếu phát hiện stale index:
        - [ ] Đã in log cảnh báo ra console/debug output
        - [ ] Đã ghi nhận cảnh báo chi tiết trong phần "Confidence Assessment" của Scope Document
  
  data_flow_traced:
    - [ ] Input data sources đã được xác định
    - [ ] Output destinations đã được xác định
    - [ ] Các bước biến đổi dữ liệu (Data transformation) đã được ghi nhận
  
  evidence_collected:
    - [ ] Mỗi bằng chứng (evidence) có file:line:method cụ thể
    - [ ] Tag method được ghi nhận chính xác (codegraph_ast | classic_grep)
    - [ ] Không giả định hoặc suy đoán thiếu căn cứ thực tế
```

---

## Confidence Assessment Checks

```yaml
confidence_checks:
  overall:
    - [ ] Confidence score đã được tính toán dựa trên độ chắc chắn
    - [ ] Score ≥ 60% → proceed
    - [ ] Score < 60% → Kích hoạt Clarification Stop Gate (Dừng lại và hỏi làm rõ từ người dùng)
  
  breakdown_review:
    - [ ] entry_point_identification: đã verify bằng view_file
    - [ ] impact_mapping: đã verify bằng codegraph_impact / grep + view_file
    - [ ] call_chain_trace: đã verify bằng callers/callees hoặc grep passes
    - [ ] evidence_verification: đã verify bằng view_file nội dung thực tế trên disk
  
  uncertainty_flags:
    - [ ] Tất cả các điểm chưa chắc chắn và cảnh báo stale index được flag đầy đủ
    - [ ] Gửi cảnh báo stale index (nếu có) vào Scope Document
```

---

## Output Quality Gates

```yaml
output_checks:
  document_structure:
    - [ ] Cập nhật mẫu template v1.1.0
    - [ ] Điền đầy đủ thông tin vào tất cả các mục (§1 đến §11)
    - [ ] Không còn giá trị placeholder nào ({...})
  
  language_compliance:
    - [ ] Toàn bộ nội dung tài liệu viết bằng tiếng Việt
    - [ ] Tóm tắt phản hồi viết bằng tiếng Việt
  
  path_compliance:
    - [ ] Đường dẫn lưu tài liệu dạng: `docs/context-to-work/{feature-name}/scope.{YYYY-MM-DD}.md`
    - [ ] Thư mục lưu trữ đã được tạo tự động
    - [ ] Định dạng tệp tin là Markdown (.md)
  
  file_quality:
    - [ ] KHÔNG sửa đổi bất kỳ tệp nguồn (source code) nào của dự án chính
    - [ ] KHÔNG đưa ra giải pháp sửa đổi cụ thể cho mã nguồn (chỉ dừng ở mô tả phạm vi)
    - [ ] Chỉ ghi nhận findings khách quan
```

---

## Final Declaration

```yaml
final_checks:
  before_deliver:
    - [ ] Tuyên bố "NO CODE CHANGES" xuất hiện ở Stop Conditions và Next Steps
    - [ ] Trả về đường dẫn tuyệt đối của Scope Document cho user/caller
    - [ ] Summary ngắn gọn (≤5 gạch đầu dòng) viết bằng tiếng Việt được gửi đi
    - [ ] Định nghĩa Next Steps rõ ràng cho phase fix tiếp theo
```

---

## Gating Rules

```yaml
gate_rules:
  pass_all:
    - Mục "Pre-Scoping" bắt buộc phải pass
    - Mục "Discovery Phase" bắt buộc phải pass
    - Mục "Analysis Phase" bắt buộc phải pass (bao gồm anti-stale check)
    - Mục "Confidence" bắt buộc phải pass và ≥ 60%
    - Mục "Output" bắt buộc phải pass (tiếng Việt, đúng đường dẫn, không sửa code)
  
  fail_any_action:
    - "Confidence below 60% hoặc Entry point mơ hồ" → STOP SEQUENCE → Clarification Stop Gate (Dừng lại hỏi user)
    - "Không có bằng chứng thực tế (evidence)" → STOP → quay lại bước thu thập bằng chứng
    - "Phát hiện thay đổi file nguồn" → ROLLBACK → khôi phục mã nguồn và hủy bỏ tài liệu
    - "Sai đường dẫn hoặc định dạng" → FIX PATH → điều chỉnh đường dẫn lưu trữ trước khi bàn giao
```

---

## Quick Reference

| Check | When | Gate | Action |
|-------|-------|------|--------|
| Codegraph status check | Boot Sequence | Must check | Timeout 5s fallback to grep |
| Entry point verified | After discovery | Must pass | view_file to verify |
| Anti-stale cross check | After analysis | Must pass | Compare AST vs Disk, log warnings |
| Confidence ≥ 60% | After assessment | Must pass | If < 60%, Clarification Stop Gate |
| No source code edits | Always (G1) | Critical Gate | Fail if any code changes made |
| Vietnamese language | Before deliver | Must pass | Output strictly in Vietnamese |

---

> **File**: `skills/rebuild/context-before-fix/loop/scoping-checklist.md`
> **Version**: 1.1.0
> **Date**: 2026-06-05
