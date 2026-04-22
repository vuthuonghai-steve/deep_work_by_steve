# Sequence Diagram Preparation Guide

> **Usage**: Hướng dẫn chuẩn bị và phân tích trước khi vẽ sơ đồ tuần tự. Đảm bảo đầy đủ thông tin đầu vào để sơ đồ chính xác về mặt nghiệp vụ và kỹ thuật.

---

## 1. Xác định rõ kịch bản (scenario) / use case

Sequence Diagram luôn vẽ **cho một kịch bản cụ thể** (main flow hoặc 1 nhánh ngoại lệ) chứ không vẽ chung chung.

**Cần có:**
* Tên use case hoặc chức năng: ví dụ “Đăng nhập hệ thống”, “Đặt hàng online”, “Rút tiền ATM”…
* Mục tiêu của use case: người dùng / hệ thống muốn đạt được điều gì sau khi kết thúc kịch bản.
* Kịch bản mô tả bằng lời (text) từng bước.

---

## 2. Danh sách các “người chơi”: Actor và đối tượng / lớp tham gia

Trước khi vẽ, phải liệt kê được **những thành phần nào tương tác với nhau** trong kịch bản:

* Các **actor** (tác nhân bên ngoài): Người dùng (User, Admin...), hệ thống bên ngoài (Payment Gateway, Email Service...).
* Các **đối tượng / lớp / thành phần hệ thống**: Màn hình / UI, Controller, Service, Repository/DAO, CSDL.

**Thông tin cần có:**
* Tên rõ ràng cho từng actor và đối tượng.
* Vai trò / trách nhiệm chính của từng thành phần trong kịch bản (Lifelines).

---

## 3. Thứ tự các bước tương tác (message flow)

Đây là phần quan trọng nhất: **ai gọi ai, gọi cái gì, theo thứ tự nào**.

**Cần làm rõ:**
* Bắt đầu từ actor nào gửi request đầu tiên cho hệ thống?
* Chuỗi gọi liên tầng (A -> B -> C).
* Nội dung message: Tên hàm / phương thức, tham số quan trọng.
* Phân biệt gửi request và trả về kết quả (return).

---

## 4. Điều kiện rẽ nhánh, lặp, luồng thay thế

* Các **điều kiện** có thể xảy ra: “Nếu mật khẩu sai”, “Nếu số dư không đủ”...
* Các **nhánh xử lý tương ứng**: Dùng `alt`, `opt`.
* Các **vòng lặp** (loop): Duyệt danh sách, gửi thông báo hàng loạt.

---

## 5. Thời điểm tạo / hủy đối tượng

* Đối tượng được **tạo mới** (ví dụ tạo `Order`, `Session`).
* Đối tượng bị **hủy / kết thúc**.
* Thể hiện bằng mũi tên tạo đối tượng và dấu “X” hủy lifeline.

---

## 6. Ranh giới hệ thống và mức độ chi tiết

Xác định mức độ chi tiết:
* **System Sequence Diagram (SSD)**: Chỉ giữa Actor ↔ Hệ thống như một khối.
* **Design-level Sequence Diagram**: Chi tiết đến UI, Controller, Service, Repository...

---

## 7. Checklist chuẩn bị (Summary)

Trước khi vẽ, hãy đảm bảo đã có:
1. Use case / kịch bản mô tả bằng lời.
2. Danh sách actor và đối tượng tham gia.
3. Thứ tự tương tác các bước.
4. Các điều kiện rẽ nhánh và lặp.
5. (Tùy chọn) Thời điểm tạo/hủy đối tượng.

---
*Fidelity Source: resources/context1.md (Transformed 100%)*
