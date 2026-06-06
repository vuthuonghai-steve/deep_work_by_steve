# FR/NFR Classification + MoSCoW Priority — BA Analyst

> Nguồn: [`thong-tin-mau.md` — Skills Layer](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/thong-tin-mau.md) + [`raw2.md` — LĨNH VỰC 2](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/raw2.md)

---

## 1. Phân Loại Yêu Cầu: FR / NFR

Agent tự động tách câu lệnh tự nhiên thành hai nhóm:

```yaml
functional_requirements:
  desc: "Yêu cầu chức năng — tính năng hệ thống phải làm"
  trigger: "Mô tả hành động, CRUD, quy trình"
  source: "thong-tin-mau.md — kỹ năng Specification & Classification"

non_functional_requirements:
  desc: "Yêu cầu phi chức năng — hiệu năng, bảo mật, mở rộng"
  trigger: "Mô tả cảm tính → Agent buộc user lượng hóa"
  examples:
    - "Throughput: 1000 req/s"
    - "Latency: < 200ms"
    - "Availability: 99.9%"
  source: "thong-tin-mau.md — case study 'chạy rất nhanh'"
```

## 2. Ma Trận MoSCoW

> Agent áp dụng ma trận MoSCoW để tự động phân bổ độ quan trọng cho từng tính năng.
> Nguồn: `thong-tin-mau.md` — kỹ năng Specification & Classification

```yaml
moscow_matrix:
  must_have:
    label: "P0"
    desc: "Bắt buộc — MVP, không thể release nếu thiếu"
  should_have:
    label: "P1"
    desc: "Quan trọng — có workaround nhưng nên có"
  could_have:
    label: "P2"
    desc: "Có thì tốt — nice to have, low risk"
  wont_have:
    label: "P3"
    desc: "Không làm — xác định rõ scope out"
```

## 3. Knowledge Layer — Chuẩn Kiến Thức

> Nguồn: `raw2.md` — LĨNH VỰC 2: KIẾN THỨC (KNOWLEDGE BASE)

```yaml
knowledge_layer:
  mindset: "Tư duy Chuẩn hóa và Tuân thủ (Compliance Mindset)"
  rules:
    - "Sử dụng thuật ngữ chuẩn quốc tế (BABOK, Agile/Scrum)"
    - "Đảm bảo nhất quán từ Business → System"
  knowledge_sources:
    - "SRS — Software Requirement Specification"
    - "Wireframe Specs"
    - "User Story template: As a... I want... So that..."
    - "Gherkin Acceptance Criteria (Given-When-Then)"
    - "Mermaid.js syntax (Sequence, Activity, Use Case, ERD)"
    - "Data Schema / ERD / API"
  skills:
    - "Phân loại FR/NFR tự động"
    - "Áp dụng MoSCoW để đề xuất độ ưu tiên"
```
