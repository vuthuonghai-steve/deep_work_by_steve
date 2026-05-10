# Proposal: Upgrade skill-architect cho Hermes-native

## 1. Phase 1 Collect — Thêm Fields cho Platform Targeting

Ở Phase 1 Collect, Architect cần hỏi user 3 trường mới:

```yaml
platform_target:
  type: enum
  options: [hermes, claude, both]
  default: both
  prompt: "Skill nhắm đến nền tảng nào?"

operation_type:
  type: enum
  options: [single_shot, streaming, long_running, agentic]
  default: single_shot
  prompt: "Loại operation chính là gì?"

execution_mode:
  type: enum
  options: [sync, async, background, daemon]
  default: sync
  prompt: "Chế độ thực thi ưu tiên?"
```

**Lý do**: 3 trường này quyết định toàn bộ pipeline phía sau — từ zone structure, contract schema, đến cách Designer suggest implementation.

---

## 2. Zone Structure theo Platform Target

| Target | Zone Structure | Ghi chú |
|--------|---------------|---------|
| **Hermes** | `core/`, `tools/`, `manifest/`, `runtime/` | Nhẹ, embeddable, tập trung tool execution |
| **Claude** | `core/`, `skills/`, `context/`, `capabilities/` | Mở rộng, multi-skill orchestration |
| **Both** | `core/`, `tools/`, `skills/`, `manifest/`, `runtime/`, `context/` | Union của 2 bên, phức tạp hơn |

**Zone khác biệt cốt lõi**:
- **Hermes** zone gọn hơn, thiên vị `tools/` — skill như một tool có manifest riêng
- **Claude** zone phong phú hơn, có `capabilities/` — skill như một agent với system prompt
- **Both** cần bridge layer ở `core/` để hai hệ thống giao tiếp được

---

## 3. Frontmatter Schema cho design.md

```yaml
---
name: skill_name
platform: hermes | claude | both        # từ platform_target
operation:
  type: single_shot | streaming | long_running | agentic
  mode: sync | async | background | daemon
  timeout: <seconds>                    # optional, cho long_running
  streaming_output: boolean             # true nếu type=streaming
contract:
  input:
    - name: <param>
      type: <string|number|object|array>
      required: boolean
      default: <value>
  output:
    - name: <param>
      type: <type>
zones:
  hermes:
    - core/
    - tools/
    - manifest/
  claude:
    - core/
    - skills/
    - context/
  both:
    - core/
    - tools/
    - skills/
    - manifest/
    - runtime/
    - context/
depends_on:
  - skill_name
  - tool_name
version: "1.0"
---
```

---

## 4. Tóm tắt Action Items

| # | Action | Priority |
|---|--------|----------|
| 1 | Thêm 3 field vào Phase 1 Collect prompt | P0 |
| 2 | Viết zone suggestion logic dựa trên platform_target | P0 |
| 3 | Cập nhật Designer template để include frontmatter schema | P1 |
| 4 | Thêm validation ở Phase 2 (Contract) cho operation_type/execution_mode consistency | P1 |
| 5 | Refinement loop cần re-validate platform_target nếu user thay đổi zone structure thủ công | P2 |
