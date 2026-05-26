# Sourced: skill-explorer/knowledge/exploration-standards.md

## Thông tin nguồn
- **Path**: `skills/rebuild/skill-explorer/knowledge/exploration-standards.md`
- **Mã số**: STG0-KNOW-01
- **Mục đích**: Xác định tiêu chí định lượng và thực hành tốt nhất cho đánh giá Agent Skills

## Tri thức trích xuất

### 7 Golden Standards

#### A. Reusability
- **Rich**: Skill thiết kế các file tri thức độc lập tại `knowledge/` để nạp động
- **Thin**: Skill chỉ giải quyết một case hẹp và cụ thể

#### B. Composability
- Input/Output Contract rõ ràng
- Tương tác qua `.skill-context/`
- **Prompt Hierarchy** khi có mâu thuẫn giữa skills

#### C. Maintainability (Goldilocks Zone)
- SKILL.md < 1800 tokens
- 4-layer knowledge model:
  - L0: Core Constitution
  - L1: Operating Policies
  - L2: Domain Knowledge
  - L3: Contextual Examples

#### D. Security
- Chống Prompt Injection qua XML delimiters
- Sandbox biệt lập cho scripts

#### E. Context Efficiency (Progressive Disclosure)
- Tier 1: Boot (always)
- Tier 2: Phase-specific (when needed)
- Tier 3: Task-specific (on-demand)

#### F. Portability
- Không trói buộc vào model-specific API
- Tool-agnostic core

#### G. Reliability & Fallback
- Execution logging
- Fallback mechanism
- Human-in-the-loop (HITL) khi cần

### Rich vs Thin Resources
| Chỉ số | Thin | Rich |
|--------|------|------|
| Độ phủ tri thức | Thiếu tài liệu cơ bản | Đầy đủ domain docs |
| Mẫu mã/Schema | Không có | Có code + API schemas |
| Ranh giới bảo mật | Không phân tách | XML boundaries rõ ràng |
| Sẵn sàng cho Builder | Cần Phase 0 bổ sung | Trực tiếp deploy |

### SCS Complexity Score
| Tiêu chí | Ngưỡng | Điểm SCS |
|----------|--------|----------|
| Số bước quy trình | ≤3:1, 4-5:3, >5:5 | 30% |
| Số công cụ/API | ≤2:1, 3-4:3, >4:5 | 30% |
| Kích thước SKILL.md | <800:1, 800-1500:3, >1500:5 | 20% |
| Security Risk | none:1, read:3, write/API:5 | 20% |

**Luật Neo cứng**: SCS > 3.0 HOẶC bất kỳ tiêu chí nào = 5 → PHẢI phân rã

### Micro-skills Orchestration Patterns
1. **Sequential Pipeline**: A→B→C (output A = input B)
2. **Condition Router**: Central skill điều hướng đến specialized skills
3. **Meta-Orchestrator**: "Nhạc trưởng" quản lý subagent lifecycle

---

## Áp dụng cho knowledge-processor

**Đã tuân thủ**:
- ✅ SCS score = 3.4 → phân rã bắt buộc
- ✅ 4 micro-skills đề xuất: pdf-extractor, html-cleaner, text-normalizer, markdown-fixer
- ✅ Sequential Pipeline + Condition Router pattern
- ✅ Security measures đầy đủ
