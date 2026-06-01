# Hướng Dẫn Vẽ Sơ Đồ & Thiết Kế Trực Quan (Visualization Guidelines)

> **Mã số**: STG1-KNW-VISUAL
> **Vai trò**: Hướng dẫn Architect vẽ sơ đồ và biểu diễn trực quan cấu trúc kỹ năng một cách sạch sẽ và dễ hiểu.

---

## 1. Tiêu Chuẩn Sơ Đồ Mermaid (Mermaid Standards)
Sơ đồ Mermaid là công cụ mạnh mẽ để AI và Steve hiểu nhanh luồng tuần tự động của hệ thống. Để tránh lỗi cú pháp, Architect phải tuân thủ các quy tắc sau:

*   **Tránh dùng HTML**: Tuyệt đối không dùng các thẻ HTML (`<br>`, `<b>`, `<i>`) bên trong nhãn (labels) của Mermaid.
*   **Tránh ký tự đặc biệt trong nhãn**: Nếu nhãn chứa dấu ngoặc đơn `()`, ngoặc vuông `[]`, hoặc dấu ngoặc nhọn `{}`, bắt buộc phải bọc nhãn đó trong dấu nháy kép `""`.
    *   *Sai*: `id[Hàm main(arg)]`
    *   *Đúng*: `id["Hàm main(arg)"]`
*   **Cấu trúc Sequence Diagram chuẩn**:
    ```mermaid
    sequenceDiagram
        autonumber
        actor User as Steve
        participant Explorer as Stage 0: Explorer
        participant Architect as Stage 1: Architect

        User->>Explorer: Gửi Prompt yêu cầu
        Explorer->>Explorer: Khảo sát rủi ro bảo mật
        Explorer->>Architect: Bàn giao exploration.json & criteria.json
        Architect->>Architect: Phân tích & thiết kế 7 Zones
        Architect->>User: Xuất bản vẽ blueprint.json
    ```

---

## 2. Quy Tắc Ánh Xạ Phân Vùng 7 Zones (Taxonomy Mapping Rules)
Khi Architect quy hoạch cấu trúc tĩnh cho một kỹ năng, việc phân bổ tệp vật lý vào các Zones phải tuân theo sơ đồ quan hệ logic:

```text
       ┌───────────┐
       │   core    │  ◄── (Hạt nhân: SKILL.md)
       └─────┬─────┘
             │
      ┌──────┴──────┐
      ▼             ▼
┌───────────┐ ┌───────────┐
│ knowledge │ │   loop    │  ◄── (Các chốt kiểm soát chất lượng)
└─────┬─────┘ └─────┬─────┘
      │             │
      ├─────────────┼─────────────┐
      ▼             ▼             ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  scripts  │ │ templates │ │   data    │  ◄── (Thực thi & cấu hình)
└───────────┘ └───────────┘ └───────────┘
```

*   **SKILL.md** nằm tại gốc của kỹ năng, thuộc zone `core`.
*   Các tài liệu tri thức nằm trong `knowledge/`, thuộc zone `knowledge`.
*   Các chính sách nằm trong `policy/`, thuộc zone `knowledge`.
*   Các kịch bản kiểm thử tĩnh hoặc động nằm trong `loop/`, thuộc zone `loop`.
*   Mã nguồn thực thi nằm trong `scripts/`, thuộc zone `scripts`.
*   Các tệp mẫu đầu ra nằm trong `templates/`, thuộc zone `templates`.
*   Cấu hình tĩnh nằm trong `data/`, thuộc zone `data`.
