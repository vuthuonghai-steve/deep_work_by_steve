# Risk Assessment Framework — BA Analyst

> Nguồn: [`thong-tin-mau.md` — Impact Analysis keyword](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/thong-tin-mau.md)

---

## Ma Trận Rủi Ro: Xác suất x Mức ảnh hưởng

```yaml
matrix:
  probability: ["Thấp (Low)", "Trung bình (Medium)", "Cao (High)"]
  impact: ["Thấp (Low)", "Trung bình (Medium)", "Cao (High)"]

scoring:
  - probability: "Thấp"
    impact: "Thấp"
    level: "Chấp nhận được"
  - probability: "Cao"
    impact: "Cao"
    level: "Không thể chấp nhận — cần mitigation ngay"
  - probability: "Trung bình"
    impact: "Cao"
    level: "Cần kế hoạch giảm thiểu"

actions:
  - "Agent tự động khoanh vùng phạm vi ảnh hưởng kỹ thuật"
  - "Ước lượng rủi ro trước khi thay đổi hệ thống"
  - "Đề xuất mitigation path cho mỗi rủi ro được xác định"

vector_anchors:
  - change impact vector
  - scope boundary detection
  - risk mitigation path
  - dependency analysis
```

## Kích Hoạt

```yaml
trigger: "Bất kỳ yêu cầu thay đổi nào → tự động đánh giá risk + scope + constraint"
source: "thong-tin-mau.md — Impact Analysis: 'Tự động đánh giá rủi ro, ràng buộc và phạm vi ảnh hưởng'"
```

## Tích Hợp với MoSCoW

```yaml
integration:
  - "Rủi ro cao + Must Have → ưu tiên mitigation planning"
  - "Rủi ro cao + Wont Have → đánh giá lại scope"
  - "Rủi ro thấp + Could Have → chấp nhận, theo dõi"
```
