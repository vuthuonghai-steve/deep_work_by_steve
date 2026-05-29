# 🔍 Chẩn đoán & Khắc phục Sự cố của Skill

> **Cấp độ tài liệu:** L2 Playbook & Troubleshooting

Tài liệu này cung cấp các bước xử lý thực tế và các tham số tinh chỉnh cấu hình khi hệ thống skill hoạt động không như kỳ vọng.

---

## 1. Các Vấn đề Kích hoạt Thường gặp

### Sự cố 1: Skill không được kích hoạt (Skill not triggering)
Nếu Claude Code không tự động sử dụng skill khi bạn đưa ra yêu cầu:
1.  **Kiểm tra từ khóa trong mô tả:** Xác minh phần `description` trong frontmatter của skill có chứa các từ khóa tự nhiên mà người dùng thường dùng khi trò chuyện hay không.
2.  **Xác minh danh sách khả dụng:** Kiểm tra xem skill có xuất hiện trong danh sách khi hỏi *"Những skill nào đang khả dụng?"* không.
3.  **Diễn đạt lại yêu cầu:** Thử diễn đạt lại câu lệnh trò chuyện để sát với mô tả kích hoạt trong frontmatter hơn.
4.  **Gọi lệnh trực tiếp:** Nếu skill hỗ trợ gọi thủ công, hãy gõ trực tiếp `/tên-skill` trên dòng lệnh để force kích hoạt.

### Sự cố 2: Skill kích hoạt quá thường xuyên (Skill triggers too often)
Nếu Claude tự động nạp và thực thi skill trong những ngữ cảnh không liên quan:
1.  **Thu hẹp mô tả:** Viết lại mô tả `description` chi tiết và cụ thể hơn, giới hạn rõ ràng hoàn cảnh áp dụng.
2.  **Chuyển sang chế độ thủ công:** Khai báo khóa `disable-model-invocation: true` ở frontmatter để chặn hoàn toàn việc tự động kích hoạt của mô hình, bắt buộc phải gọi bằng lệnh `/tên-skill`.

---

## 2. Sự cố Mô tả Skill bị Cắt ngắn (Truncated Descriptions)

### Nguyên nhân hoạt động
Mô tả sơ lược của toàn bộ các skill được nạp sẵn vào context của Claude để mô hình biết những công cụ nào đang khả dụng.
*   **Char budget giới hạn:** Để tránh lãng phí token, mặc định tổng character budget cho toàn bộ mô tả skill được giới hạn ở mức **1%** cửa sổ ngữ cảnh của model.
*   **Cơ chế cắt tỉa (Trimming):** Khi số lượng skill quá nhiều vượt quá budget, hệ thống sẽ tự động cắt ngắn mô tả của các skill ít được sử dụng nhất về dạng chỉ hiển thị tên (`"name-only"`).

Để kiểm tra xem hệ thống có đang bị tràn budget skill và ảnh hưởng đến những skill nào, hãy chạy lệnh:
```text
/doctor
```

### Kỹ thuật Giải quyết & Tinh chỉnh

<instructions>
must:
  - Để giải phóng character budget cho các skill quan trọng, hãy chuyển các skill ít dùng sang chế độ hiển thị chỉ tên bằng cách khai báo trong cấu hình `skillOverrides` là `"name-only"`.
  - Luôn viết phần use case cốt lõi ở đầu chuỗi mô tả, vì tổng độ dài kết hợp của `description` và `when_to_use` của mỗi skill bị giới hạn cứng ở mức **1,536 ký tự** tại nguồn, bất kể budget của phiên là bao nhiêu.
</instructions>

Để mở rộng Character Budget dành cho skill, bạn có thể áp dụng các tùy chọn sau trong cấu hình:

*   **Tăng tỷ lệ phần trăm budget trong settings:** Cấu hình thuộc tính `skillListingBudgetFraction` (ví dụ: đặt `0.02` tương đương với 2% cửa sổ ngữ cảnh).
*   **Đặt số lượng ký tự cứng bằng biến môi trường:** Khai báo biến môi trường `SLASH_COMMAND_TOOL_CHAR_BUDGET` bằng một số nguyên cụ thể đại diện cho số ký tự tối đa được cấp phát.
*   **Điều chỉnh giới hạn cứng của từng tệp:** Cấu hình biến `maxSkillDescriptionChars` để thay đổi ngưỡng giới hạn 1,536 ký tự mặc định của mỗi mô tả skill.
