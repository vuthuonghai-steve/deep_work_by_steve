# Sourced: CLAUDE.md

## Thông tin nguồn
- **Path**: `/home/steve/Work-space/deep_work_by_steve/CLAUDE.md`
- **Mục đích**: LLM Knowledge Activation Documentation Standard — chuẩn hóa cách biến tri thức thô thành tài liệu cho LLM

## Tri thức trích xuất

### Semantic Questions (câu hỏi ngữ nghĩa)
```yaml
semantic_questions:
  - đây là mệnh lệnh hay dữ liệu tham chiếu?
  - đây là luật bắt buộc hay gợi ý mềm?
  - thông tin này luôn cần dùng hay chỉ dùng theo ngữ cảnh?
  - phần nào là ví dụ, phần nào là tiêu chí chấp nhận?
  - khi có xung đột, ưu tiên nào cao hơn?
```

### Design Principles
```yaml
principles:
  encode_intent_over_decoration: true
  separate_rules_from_context: true
  separate_examples_from_instructions: true
  keep_root_guide_compact: true
  load_domain_context_on_demand: true
  prefer_named_schema_over_implicit_notes: true
  avoid_large_flat_markdown: true
```

### 4-Layer Knowledge Model
```yaml
L0_anchor_rules:
  purpose: "Luật nền, mục tiêu, giới hạn tuyệt đối, anti-goals"
  load_policy: "always"
  location: "root guide: CLAUDE.md, AGENT.md, SYSTEM.md"
  token_budget: 150-400 good, 500-700 warning, >700 split

L1_working_policy:
  purpose: "Quy ước làm việc, coding rules, review rules"
  load_policy: "frequent_or_scoped"
  token_budget: 400-1200 good, 1200-2000 warning, >2000 split

L2_domain_context:
  purpose: "Kiến trúc, domain glossary, data flow"
  load_policy: "on_demand"
  token_budget: 600-2500 good, 2500-5000 warning, >5000 split

L3_evidence_examples:
  purpose: "Spec, ticket, logs, examples, fixtures"
  load_policy: "task_specific_only"
  token_budget: 300-2000 good, 2000-6000 warning, >6000 split
```

### Format Selection Rules
| Format | Use For | Avoid For |
|--------|---------|-----------|
| Markdown | explanation, architecture, rationale, onboarding | hard_rules_without_schema, long_mixed_policy |
| YAML | constraints, policies, checklists, routing | long_prose, deeply_nested |
| XML-like tags | semantic boundaries, separating context from instruction | excessive_micro_tagging, replacing_all_markdown |

### Token Budget
| Layer | Excellent | Good | Warning | Heavy |
|-------|-----------|------|---------|-------|
| L0 | 300-900 | 900-1800 | 1800-3000 | 3000-5000 |
| L1 | 400-1200 | 1200-2000 | — | — |

### Semantic Activation Anchors
```yaml
high_priority_rules:
  - instructions, non_negotiables, hard_rules, constraints, must, must_not, priority_order

task_execution:
  - task, scope, assumptions, plan, steps, stop_conditions, validation

quality_control:
  - acceptance_criteria, review_checklist, test_policy, definition_of_done

context_boundaries:
  - context, reference, examples, evidence, input, retrieved_docs
```

---

## Áp dụng cho knowledge-processor

**Đã tuân thủ**:
- ✅ Semantic questions framework
- ✅ 4-layer knowledge model được áp dụng
- ✅ YAML cho contracts và constraints
- ✅ XML delimiters cho raw input wrapping
- ✅ Token budget được kiểm soát
