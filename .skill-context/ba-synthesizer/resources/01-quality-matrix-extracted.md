# Ma trận Chất lượng — ba-synthesizer

Nguồn: ba-synthesizer-analysis.md §3.2

## 7 Deliverables

| Deliverable | Weight | Min Criteria |
|---|---|---|
| elicitation_report | 0.15 | Normalize mô tả; Pain Points; Giả định hệ thống |
| requirements_classification | 0.15 | Phân biệt FR/NFR; MoSCoW đầy đủ |
| sequence_diagram | 0.15 | Mermaid hợp lệ; >=3 tác nhân (User/Agent/Tool) |
| flowchart_activity | 0.15 | 3 luồng: Happy/Alternative/Exception |
| erd_schema | 0.15 | PK+FK; Kiểu dữ liệu rõ |
| acceptance_criteria | 0.15 | Gherkin Given-When-Then; >=3 kịch bản |
| risk_matrix | 0.10 | >=3 rủi ro kèm mitigation |

## Evaluation Rules

- pass_threshold: 0.80
- calculation_method: weighted_sum
- Σ(weight_i × score_i) >= 0.80 → PASS; < 0.80 → WARNING
