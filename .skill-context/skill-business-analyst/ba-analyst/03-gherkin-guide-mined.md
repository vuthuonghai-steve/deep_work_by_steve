# Gherkin Acceptance Criteria Standards — BA Analyst

> Nguồn: [`thong-tin-mau.md` — Skills Layer: Acceptance Criteria](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/thong-tin-mau.md) + [`raw2.md` — Knowledge Layer](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/raw2.md)

---

## 1. Cấu Trúc Given-When-Then

Định dạng bắt buộc từ Master Prompt (thong-tin-mau.md):

```gherkin
Feature: [Tên tính năng]
  Scenario: [Tên kịch bản]
    Given [Trạng thái tiền đề]
    When [Hành động xảy ra]
    Then [Kết quả mong đợi]
```

## 2. Số Lượng Scenario Tối Thiểu

Mỗi feature bắt buộc ≥3 kịch bản:

```yaml
minimum_scenarios: 3
scenarios:
  - type: "Happy Path"
    desc: "Luồng chuẩn — mọi điều kiện đều đúng"
    count_min: 1
  - type: "Alternative Path"
    desc: "Luồng thay thế — xử lý rẽ nhánh hợp lệ"
    count_min: 1
  - type: "Exception Path"
    desc: "Luồng lỗi — validation fail, ngoại lệ"
    count_min: 1
source: "thong-tin-mau.md — Skills Layer: Acceptance Criteria + raw2.md: User Story template"
```

## 3. Format Yêu Cầu

```yaml
format_rules:
  - "Testable — Given/When/Then phải đo lường được, không mơ hồ"
  - "User Story template đi kèm: As a... I want... So that..."
  - "Zero placeholder: không TODO, TBD"
  - "Đồng bộ Markdown: ##, ###, tables — sẵn sàng cho Git/Notion"
source: "thong-tin-mau.md — Acceptance Criteria + raw2.md — User Story template"
```

## 4. Ví dụ Áp Dụng

Trích từ luồng xuất bản Markdown chuẩn (thong-tin-mau.md):

```gherkin
Feature: Xử lý giao dịch thanh toán
  Scenario: Happy Path — Thanh toán thành công
    Given Người dùng đã đăng nhập và có giỏ hàng hợp lệ
    When Người dùng xác nhận thanh toán
    Then Hệ thống ghi nhận giao dịch và gửi email xác nhận

  Scenario: Exception Path — Thẻ hết hạn
    Given Người dùng nhập thẻ tín dụng đã hết hạn
    When Hệ thống xác thực thẻ
    Then Hệ thống báo lỗi "Thẻ đã hết hạn" và yêu cầu nhập thẻ khác
```
