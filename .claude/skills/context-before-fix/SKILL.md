---
name: context-before-fix
description: 'Skill phân tích scope vấn đề trước khi fix. Trigger khi user/agent có issue, bug, cần sửa, hoặc thêm mới tính năng. Output: scope context document tại docs/context-to-work/{feature-name}/. KHÔNG sửa code — chỉ document findings.'
category: problem-analysis
version: "1.1.0"
author: "Steve Void Team"
tags: [scoping, impact-analysis, context-documentation, vietnamese, codegraph]
---

# Context Before Fix — Problem Scoping Skill

## Mission

Skill này **CHỈ DOCUMENT** — không sửa code. Trước khi fix bất kỳ vấn đề nào, agent phải:

1. Xác định scope thực sự của vấn đề
2. Map impact đầy <instructions>
## Boot Sequence

1. Đọc `SKILL.md` (file này).
2. Kiểm tra tính sẵn sàng của `codegraph` MCP server bằng cách gọi tool `codegraph_status` hoặc tìm kiếm symbol cơ bản với **timeout tối đa là 5 giây (5000ms)**.
   - Nếu thành công và phản hồi hợp lệ: Thiết lập biến/cờ `USE_CODEGRAPH = True`.
   - Nếu lỗi hoặc timeout sau 5 giây (5000ms): Thiết lập `USE_CODEGRAPH = False`, ghi nhận cảnh báo fallback và sử dụng grep.
3. Đọc các tài liệu hướng dẫn nghiệp vụ:
   - `knowledge/output-schema.md` — Cấu trúc Scope Document.
   - `knowledge/scoping-patterns.md` — Quy trình tìm kiếm bằng Codegraph & Fallbacks.
4. Bắt đầu quy trình 4-Step Workflow.

## 4-Step Workflow

### Step 1: INPUT ACCEPTANCE
- Tiếp nhận thông tin issue description (logs, errors, descriptions).
- Xác định entry point (file, component, API endpoint hoặc database model).
- Nếu độ tin cậy khi xác định entry point hoặc ranh giới vấn đề **dưới 60%**, dừng lại ngay lập tức và hỏi làm rõ từ phía người dùng (Clarification Stop Gate).

### Step 2: SCOPE DISCOVERY
- **Nếu `USE_CODEGRAPH == True`**:
  - Dùng `codegraph_search` hoặc `codegraph_context` để tìm các symbol liên quan.
  - Sử dụng `codegraph_callers` để tìm chuỗi gọi upstream (ai gọi entry point) và `codegraph_callees` để tìm chuỗi gọi downstream (entry point gọi ai).
- **Nếu `USE_CODEGRAPH == False` (Fallback)**:
  - Chạy `grep_search` để tìm usages, import references và call sites.
  - Chạy `find_by_name` để liệt kê các file liên quan theo tên.
- Xác định và lập danh sách toàn bộ các tệp tin và symbols có liên quan.

### Step 3: IMPACT ANALYSIS
- **Nếu `USE_CODEGRAPH == True`**:
  - Chạy `codegraph_impact` để phân tích lan truyền ảnh hưởng của các symbol đến các node khác trong đồ thị.
- **Nếu `USE_CODEGRAPH == False` (Fallback)**:
  - Sử dụng LLM reasoning phân tích callers, dependencies và shared services để vẽ bản đồ ảnh hưởng.
- **Xác minh chống stale index (Anti-Stale Index Guardrail)**:
  - Bắt buộc kiểm tra chéo các nút quan trọng trên call chain bằng cách gọi trực tiếp `view_file` để đảm bảo code trên đĩa trùng khớp với kết quả đồ thị.
  - Nếu phát hiện chỉ mục của codegraph bị stale (lỗi thời): **Phải in log cảnh báo lên console/debug output** đồng thời **ghi nhận chi tiết cảnh báo này vào phần "Confidence Assessment"** trong tài liệu Scope Document.
- Phân loại rõ các vùng ảnh hưởng trực tiếp (Direct Impact) và gián tiếp (Indirect Impact).

### Step 4: DOCUMENT GENERATION
- Tổng hợp toàn bộ findings bằng **Tiếng Việt**.
- TUYỆT ĐỐI không đưa ra giải pháp sửa đổi mã nguồn.
- Tạo Scope Context Document dựa trên template mẫu tại `docs/context-to-work/{feature-name}/scope.{YYYY-MM-DD}.md`.
- Chạy self-check tự động dựa trên checklist tại `loop/scoping-checklist.md`.
- Trả về đường dẫn tài liệu và summary ngắn gọn cho caller.
</instructions>

---

## Core Constraints

```yaml
must:
  - check codegraph MCP status with a 5000ms timeout at boot
  - document all findings
  - use Vietnamese language in output
  - write output to docs/context-to-work/{feature-name}/
  - ask user when uncertain (confidence < 60%)
  - trace all findings to specific files/lines
  - cross-verify codegraph outputs with view_file to prevent stale indexes (G3)
  - log stale index warnings to console/debug and scope document (G3)

must_not:
  - edit any project source code files (G1)
  - create branches
  - run tests
  - deploy anything
  - delete files
  - provide fix solutions

priority_order:
  - no_code_changes
  - understanding_scope
  - mapping_impact
  - documenting_findings
```

---

## Confidence Handling

```yaml
confidence_threshold: 60

confidence_levels:
  above_85:
    meaning: "Tin chắc findings chính xác"
    action: "Proceed to generate doc"
  
  60_to_85:
    meaning: "Khá chắc, có một số uncertainties"
    action: "Document with uncertainty flags"
  
  below_60:
    meaning: "Không chắc chắn"
    action: "STOP — Ask user for clarification using clarify tool"
```

---

## Tools

```yaml
primary_tools:
  - codegraph_status      # kiểm tra trạng thái mcp server
  - codegraph_search      # tìm kiếm symbol trong đồ thị
  - codegraph_context     # xem thông tin chi tiết node symbol
  - codegraph_callers     # truy vết caller upstream
  - codegraph_callees     # truy vết callee downstream
  - codegraph_impact      # phân tích lan truyền ảnh hưởng
  - grep_search           # tìm kiếm text/pattern khi fallback
  - find_by_name          # tìm kiếm tệp tin theo tên khi fallback
  - view_file             # xem nội dung tệp tin thực tế để kiểm tra chéo (anti-stale)
  - write_to_file         # ghi file scope document

reasoning:
  - LLM analyze relationships
  - trace logic chains
  - identify patterns
```

---

## Output Contract

```yaml
output_contract:
  path_pattern: "docs/context-to-work/{feature-name}/scope.{YYYY-MM-DD}.md"
  
  sections:
    - Problem Summary
    - Entry Point
    - Scope Definition
    - Impact Analysis (Direct + Indirect)
    - Call Chain
    - Data Flow
    - Affected Components
    - Evidence
    - Confidence Assessment (including codegraph status & stale index warnings)
    - Open Questions
  
  format: Markdown + YAML (theo know.md standards)
  language: Vietnamese
```

---

## Progressive Disclosure

```yaml
Tier_1_Mandatory:
  description: "Load always at boot"
  files:
    - SKILL.md
    - knowledge/output-schema.md

Tier_2_Conditional:
  description: "Load when context requires"
  files:
    - knowledge/scoping-patterns.md
    - templates/scope-doc.template
    - loop/scoping-checklist.md
```

---

## Guardrails

```yaml
guardrails:
  G1_no_code_changes:
    description: "Cấm tuyệt đối sửa đổi mã nguồn ứng dụng chính."
    must_not: [edit_source_code, create_branches, run_tests, deploy]
  
  G2_ask_when_uncertain:
    description: "Clarification Stop Gate - dừng và làm rõ nếu độ tự tin dưới 60%."
    condition: "confidence < 60%"
    action: "STOP → clarify with user"
  
  G3_anti_stale_index:
    description: "Tránh stale index bằng cách đối chiếu với code thực tế."
    must: [cross_verify_with_view_file, log_warnings_to_console, document_warnings_in_scope_doc]
  
  G4_vietnamese_output:
    description: "Đầu ra bắt buộc phải viết hoàn toàn bằng tiếng Việt."
    must: [use_Vietnamese_in_document, use_Vietnamese_in_summary]
```

---

## Stop Conditions

```yaml
stop_conditions:
  - Document written to disk at correct path
  - User receives path to scope document
  - User receives summary of findings
  - Statement: "NO CODE CHANGES — Context ready for fix phase"
```

---

## Large Codebase Fallback

```yaml
large_codebase_strategy:
  when: "grep/search hoặc codegraph query timeout (5000ms) hoặc >50 results"
  action:
    - Ask user to narrow scope
    - Limit search to specific module/feature
    - Use entry point approach (don't full scan)
  max_bounded_search:
    max_files: 20
    max_depth: 3
```

---

## Quality Checklist (self-check trước khi deliver)

```yaml
pre_delivery_check:
  - [ ] Entry point identified và verified
  - [ ] Kiểm tra trạng thái codegraph và xác nhận USE_CODEGRAPH (độ trễ < 5s)
  - [ ] Tất cả related files đã được search qua codegraph/grep
  - [ ] Chạy view_file để kiểm tra chéo (Anti-stale check)
  - [ ] Cảnh báo stale index (nếu có) được log lên console và ghi vào Confidence Assessment
  - [ ] Impact map đầy đủ (direct + indirect)
  - [ ] Evidence ghi nhận cụ thể (file:line)
  - [ ] Confidence assessment đã làm
  - [ ] Document viết bằng tiếng Việt
  - [ ] Document lưu đúng path pattern
  - [ ] NO code changes made
```

---

> **File**: `skills/rebuild/context-before-fix/SKILL.md`
> **Version**: 1.1.0
> **Date**: 2026-06-05sole/debug output** đồng thời **ghi nhận chi tiết cảnh báo này vào phần "Confidence Assessment"** trong tài liệu Scope Document.
- Phân loại rõ các vùng ảnh hưởng trực tiếp (Direct Impact) và gián tiếp (Indirect Impact).

### Step 4: DOCUMENT GENERATION
- Tổng hợp toàn bộ findings bằng **Tiếng Việt**.
- TUYỆT ĐỐI không đưa ra giải pháp sửa đổi mã nguồn.
- Tạo Scope Context Document dựa trên template mẫu tại `docs/context-to-work/{feature-name}/scope.{YYYY-MM-DD}.md`.
- Chạy self-check tự động dựa trên checklist tại `loop/scoping-checklist.md`.
- Trả về đường dẫn tài liệu và summary ngắn gọn cho caller.
</instructions>
