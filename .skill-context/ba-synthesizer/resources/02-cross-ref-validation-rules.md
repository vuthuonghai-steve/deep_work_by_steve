# Quy tắc Kiểm định Chéo — ba-synthesizer

Nguồn: ba-synthesizer-analysis.md §4

## Actor-Entity Matching

1. Quét Sequence Diagram Mermaid → trích Actor + Participant
2. Quét ERD Mermaid → trích Entity list
3. Nếu SD thao tác entity không có trong ERD → `[MAU THUẪN NGHIỆP VỤ: Thực thể CSDL thiếu hụt]`

## MoSCoW-Gherkin Matching

1. Quét bảng MoSCoW → lọc dòng priority=Must
2. Quét Acceptance Criteria → so khớp Scenario name với feature name
3. Nếu Must feature thiếu Gherkin → `[THIẾU KỊCH BẢN KIỂM THỬ: Tính năng cốt lõi chưa có kiểm thử]`

## Warning Tags

| Tag | Trigger |
|---|---|
| `[MAU THUẪN NGHIỆP VỤ]` | Entity SD không khớp ERD |
| `[THIẾU THÔNG TIN]` | Thiếu dữ liệu chéo |
| `[THIẾU KỊCH BẢN KIỂM THỬ]` | Must feature không Gherkin |

## Output Effect

- Nhất quán → quality_gate_status=PASS
- Có mâu thuẫn → quality_gate_status=WARNING
