# Responsive Layout Rules

> **Mục tiêu**: Ngăn chặn lỗi "RenderFlex overflow" kinh điển và đảm bảo UI hiển thị tốt trên mọi kích thước màn hình thiết bị di động.

## 1. Tránh Hardcode Kích thước Tuyệt đối

- Bản prototype Source (`tranphueco-redo-AI`) thường được vẽ cho một kích thước màn hình cụ thể (ví dụ: iPhone 14 Pro) và hay sử dụng kích thước cứng (e.g., `height: 800`, `width: 390`).
- Khi mang sang Target, Agent **TUYỆT ĐỐI KHÔNG** sao chép các con số fixed width/height này cho màn hình hoặc các container chiếm diện tích lớn.
- **Giải pháp**: 
  - Sử dụng `MediaQuery.of(context).size` khi cần tính toán tỷ lệ.
  - Ưu tiên dùng `Expanded`, `Flexible` bên trong `Column` và `Row`.
  - Nếu bắt buộc dùng chiều cao/rộng, hãy thiết lập `constraints` (minHeight, maxHeight) thay vì fixed height.

## 2. Ngăn ngừa RenderFlex Overflow

**Lỗi thường gặp:** Màn hình nhỏ gọn trên bản thiết kế, nhưng khi chạy trên thiết bị có bàn phím ảo bật lên hoặc font chữ hệ thống to, màn hình bị báo sọc vàng đen (RenderFlex overflow).

**Quy tắc phòng tránh cho Agent:**
- Luôn cân nhắc bọc phần nội dung chính của màn hình (trừ phần Header/BottomBar cố định) bằng `SingleChildScrollView` + `SafeArea`.
- Chú ý khi dùng `ListView` bên trong `Column`: Luôn bọc `ListView` bằng `Expanded` hoặc thêm thuộc tính `shrinkWrap: true, physics: NeverScrollableScrollPhysics()` nếu nó nằm trong một `SingleChildScrollView`.
- Với các đoạn Text dài, không bọc trong `Row` mà thiếu `Expanded`. Ví dụ:
  *(Sai)*: `Row(children: [Icon(Icons.info), Text("Rất dài...")])`
  *(Đúng)*: `Row(children: [Icon(Icons.info), Expanded(child: Text("Rất dài..."))])`

## 3. Padding và Insets Tương thích

- Luôn dùng `SafeArea` ở cấp độ ngoài cùng của Screen (nếu không dùng Scaffold có AppBar) để tránh UI bị đè bởi "tai thỏ" (notch) hoặc thanh điều hướng.
- Sử dụng các hằng số khoảng cách (Spacing constants) của dự án thay vì nhập số tự do nếu dự án có định nghĩa (ví dụ `padding: EdgeInsets.all(AppDimens.padding16)`).

---

## Reference Data

- **Related knowledge**: `flutter-ui-patterns.md` — widget tree structure basics
- **Related knowledge**: `conversion-rules.md` — UI-only constraints
- **Forbidden patterns**: `data/forbidden-patterns.yaml` — anti-patterns to avoid
