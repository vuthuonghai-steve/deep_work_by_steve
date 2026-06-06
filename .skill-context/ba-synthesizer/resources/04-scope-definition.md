# Phạm vi & Nghiệm thu — ba-synthesizer

Nguồn: ba-synthesizer-analysis.md

## Vị trí Pipeline (§1.1)

ba-elicitor → elicitation-report.md → ba-analyst → analysis-report.md → **ba-synthesizer** → business-analysis.md → Explorer (Stage 0)

## Input/Output (§6)

| Hướng | File | Từ |
|---|---|---|
| Input | elicitation-report.md | ba-elicitor |
| Input | analysis-report.md | ba-analyst |
| Output | business-analysis.md | → Explorer |

Cross-ref: ba-analyst đủ 7 deliverables ✅; ba-elicitor format khớp input contract ✅

## Rủi ro & Mitigation (§7)

| # | Rủi ro | Mức | Mitigation |
|---|---|---|---|
| 1 | Mất thông tin hợp nhất | TB | Template cứng + checklist |
| 2 | Mermaid lỗi cú pháp | Cao | Parser regex/sandbox |
| 3 | Mâu thuẫn ERD-SD | Cao | Mapping rules |
| 4 | Tràn context window | TB | Progressive disclosure |

## Acceptance Criteria (§8.1)

| ID | Mô tả | Validation |
|---|---|---|
| AC_1 | YAML frontmatter đủ | Schema match 100% |
| AC_2 | Mermaid hợp lệ | Đúng thẻ, zero syntax error |
| AC_3 | Cross-ref có kết quả | Section "Kiểm định nhất quán chéo" |
| AC_4 | Zero placeholder | Regex TBD/TODO/mock = từ chối |
| AC_5 | Tiếng Việt chuẩn | Trừ thuật ngữ kỹ thuật + Gherkin |

## Gherkin Scenarios (§8.2)

**Scenario 1**: Đầu vào hợp lệ, 100% nhất quán. → Merge 7 deliverables, quality >= 80%, quality_gate_status=PASS, zero placeholder.

**Scenario 2**: SD có PaymentGateway nhưng ERD thiếu Transactions/Payments. → Merge nhưng inject [MAU THUẪN NGHIỆP VỤ], quality score giảm, quality_gate_status=WARNING, zero placeholder.

## Confidence

- Design: completed v1.0.0
- Cross-ref OK: 7 deliverables khớp, input format khớp
- Rủi ro mở: Chưa có sandbox Mermaid parser (Rủi ro #2)
