# Data Schema & Quality Gates — ba-analyst

> Trích xuất từ `ba-analyst-analysis.md`.

## 1. 7 Deliverables Bắt Buộc [TỪ analysis §6.2] [TỪ analysis §8.1 QG-BA-02]

1. YAML Frontmatter (skill_name, analyzed_by, analyzed_at, status)
2. Requirements Classification & MoSCoW (Markdown table: ID, Loại, Phân loại, Mô tả, Độ ưu tiên, Lý do)
3. System Diagrams (3 Mermaid diagrams: Sequence + Flowchart + ERD)
4. Data Schema Design (Markdown tables / JSON Schema)
5. Acceptance Criteria — Gherkin (≥ 3 scenarios)
6. Risk & Impact Assessment Matrix (Markdown table: Mã RR, Mô tả, Xác suất L/M/H, Tác động L/M/H, Giải pháp)
7. Traceability Mapping (Markdown list với trace tags)

## 2. Output Contract Schema (FULL) [TỪ analysis §6.2]

```yaml
output_contract:
  target_file: ".skill-context/skill-business-analyst/resources/analysis-report.md"
  required_format: "Hybrid Markdown + YAML"
  sections:
    - name: "YAML Frontmatter"
      keys: [skill_name, analyzed_by, analyzed_at, status]
    - name: "Requirements Classification & MoSCoW"
      format: "Markdown Table"
      columns: [ID, Loại yêu cầu, Phân loại cụ thể, Mô tả đặc tả kỹ thuật, Độ ưu tiên MoSCoW, Lý do kỹ thuật]
    - name: "System Diagrams"
      format: "Mermaid.js"
      diagrams: [Sequence Diagram, Flowchart, ERD]
    - name: "Data Schema Design"
      format: "Markdown Tables / JSON Schema"
    - name: "Acceptance Criteria (Gherkin)"
      format: "Gherkin Code Blocks"
    - name: "Risk & Impact Assessment Matrix"
      format: "Markdown Table"
      columns: [Mã Rủi ro, Mô tả, Xác suất (L/M/H), Tác động (L/M/H), Giải pháp]
    - name: "Traceability Mapping"
      format: "Markdown List"
      trace_tags: ["[TỪ INPUT]", "[SUY LUẬN]", "[CẦN LÀM RÕ]"]
```

## 3. Quality Gates [TỪ analysis §8.1]

| ID | Tiêu chí | Verification | Target |
|----|----------|-------------|--------|
| QG-BA-01 | Tuân thủ XML/YAML contract | Kiểm tra frontmatter + XML tags | 100% đạt chuẩn |
| QG-BA-02 | 7 deliverables đầy đủ | Đối chiếu output | 7/7, zero placeholder |
| QG-BA-03 | Mermaid syntax chính xác | Render test / parser | Không lỗi render |
| QG-BA-04 | Gherkin coverage ≥ 3 | Đếm scenarios | ≥3, Given-When-Then chuẩn |
| QG-BA-05 | Traceability | Quét trace tags | Mọi entity gán đúng tag |

## 4. Validation Algorithms [TỪ analysis §7]

- **R-1 mitigation:** `syntax_validator.py` kiểm tra Mermaid syntax
- **R-3 mitigation:** trace tag enforcement — mọi phát biểu gán [TỪ INPUT]/[SUY LUẬN]/[CẦN LÀM RÕ]
- **R-4 mitigation:** Progressive Disclosure — chỉ nạp knowledge file khi cần
