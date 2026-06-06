# 5W1H Elicitation Question Framework — BA Elicitor

> Nguồn: [`raw2.md` — LĨNH VỰC 1: TƯ DUY (MINDSET), Kiến thức cấp cho Agent](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/skill-business-analyst/resources/raw2.md)

## Cấu trúc Bộ Câu Hỏi Chuẩn Hóa

Agent sử dụng bộ câu hỏi 5W1H để khơi gợi (elicit) thông tin từ người dùng khi yêu cầu còn mơ hồ hoặc thiếu:

```yaml
question_types:
  who:
    label: "Tác nhân (Actor)"
    sub_questions:
      - "Ai thực hiện thao tác này? (Người dùng / Hệ thống / Hệ thống thứ ba)"
      - "Ai là người hưởng lợi từ kết quả?"
      - "Ai chịu trách nhiệm phê duyệt?"
  
  what:
    label: "Hành động / Đối tượng"
    sub_questions:
      - "Thao tác cụ thể là gì? (CRUD? Báo cáo? Phê duyệt?)"
      - "Dữ liệu nào được tạo ra / thay đổi?"
      - "Sản phẩm đầu ra là gì?"
  
  why:
    label: "Mục đích / Lý do"
    sub_questions:
      - "Tại sao cần tính năng này? (Mục tiêu kinh doanh?)"
      - "Nếu không có, điều gì xảy ra?"
      - "Giá trị mang lại là gì?"
  
  how:
    label: "Phương thức"
    sub_questions:
      - "Quy trình thực hiện ra sao? (Có bao nhiêu bước?)"
      - "Dữ liệu đầu vào từ đâu? / Đầu ra đi đâu?"
      - "Xử lý đồng bộ hay bất đồng bộ?"
  
  when:
    label: "Thời điểm / Tần suất"
    sub_questions:
      - "Khi nào sự kiện được kích hoạt? (Theo lịch / Sự kiện / Thủ công)"
      - "Tần suất xử lý? (Real-time / Batch / Theo ca)"
  
  where:
    label: "Vị trí / Kênh"
    sub_questions:
      - "Tính năng hoạt động ở đâu? (Web / Mobile / API / Internal)"
      - "Dữ liệu được lưu ở đâu? (DB / Cache / File / External Service)"
```

## Cơ chế Phân tách Luồng (Path Decomposition)

Mỗi yêu cầu được phân tách thành 3 luồng bắt buộc:

```yaml
path_types:
  - path: "Happy Path"
    desc: "Luồng chuẩn — mọi điều kiện đều đúng"
    min_scenarios: 1
  - path: "Alternative Path"
    desc: "Luồng thay thế — điều kiện khác nhưng vẫn thành công"
    min_scenarios: 1
  - path: "Exception Path"
    desc: "Luồng lỗi — xử lý ngoại lệ, validation fail"
    min_scenarios: 1
```

## Format Multiple-choice cho Người dùng

Khi phát hiện vùng thiếu thông tin, Agent trình bày dưới dạng:

```yaml
response_format: "Multiple-choice hoặc Bullet points để người dùng chọn/làm rõ"
source: "raw2.md — Kỹ năng Agent sử dụng: Proactive Clarification"
```
