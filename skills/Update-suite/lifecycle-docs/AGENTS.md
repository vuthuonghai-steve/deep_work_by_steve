# 📂 /skills/Update-suite/lifecycle-docs/
## 📜 NHẬT KÝ VÒNG ĐỜI VÀ TIẾN TRÌNH NÂNG CẤP (LIFECYCLE & UPDATE DOCS)

Tài liệu này cung cấp hướng dẫn và quy định cho thư mục `lifecycle-docs/`, nơi lưu trữ toàn bộ lịch sử, quyết định kiến trúc, và dấu chân kỹ thuật của bộ Skill Suite qua từng phiên bản nâng cấp.

---

## 🗺️ Tổng quan Vai trò & Tầm quan trọng
Trong vòng đời của một hệ thống Agent AI, tri thức không chỉ nằm ở mã nguồn mà còn ở **lý do tại sao mã nguồn đó được thay đổi (Rationale)**. Thư mục `lifecycle-docs/` là **"Trí nhớ dài hạn"** ghi lại:
* Các quyết định thay đổi cấu trúc cốt lõi.
* Các tài liệu di chuyển (migration paths) giữa các phiên bản.
* Nhật ký phân tích rủi ro và các bài học rút ra (post-mortems).

```
 ┌─────────────────────────────────────────────────────────────┐
 │                         lifecycle-docs/                     │
 │                                                             │
 │   - ADRs (Architecture Decision Records)                    │
 │   - Changelogs & RFCs cho các thay đổi lớn                  │
 │   - Checkpoint reports & post-mortems                       │
 └─────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **QUY TẮC BẤT BIẾN:**
> Tất cả các Agent khi tham gia vào quy trình nâng cấp **bắt buộc phải cập nhật** tài liệu tại đây trước khi kết thúc chu kỳ nâng cấp. Việc này đảm bảo tính nhất quán (traceability) và ngăn ngừa hiện tượng trôi lệch logic (knowledge drift).

---

## 🏗️ Cấu trúc Thư mục Đề xuất

```text
lifecycle-docs/
├── AGENTS.md                   # Tài liệu hướng dẫn này
├── CHANGELOG.md                # Nhật ký thay đổi tổng hợp qua các phiên bản
├── ADRs/                       # Architecture Decision Records (Quyết định thiết kế)
│   ├── 0001-init-lifecycle.md
│   └── 0002-apply-case-system.md
├── RFCs/                       # Request for Comments cho các cải tiến lớn
│   └── RFC-001-dynamic-state.md
└── migration-paths/            # Hướng dẫn di chuyển và chuyển đổi trạng thái
    └── v1.0.0-to-v2.0.0.md
```

---

## 🛡️ Tích hợp CASE System (PREVENT -> DETECT -> RECOVER)

Thư mục này là trung tâm của cả 3 cơ chế trong CASE System:

### 1. PREVENT (Ngăn ngừa lỗi)
* **ADR (Architecture Decision Records):** Ghi chép lý do cụ thể vì sao một kiến trúc được chọn để các Agent sau này không lặp lại các sai lầm cũ.
* **Migration Paths:** Cung cấp tài liệu rõ ràng về sự tương thích ngược, ngăn chặn lỗi biên dịch hoặc runtime khi nâng cấp.

### 2. DETECT (Phát hiện lỗi)
* **Checkpoint Reports:** Lưu trữ kết quả của các script kiểm tra tự động (`validate_gate.py`, `check_status.py`) qua mỗi đợt tích hợp, giúp nhanh chóng khoanh vùng phiên bản gây ra lỗi.

### 3. RECOVER (Khôi phục)
* **Version History:** Nhờ nhật ký chi tiết và cấu trúc phân mảnh theo phiên bản, Agent có thể dễ dàng xác định điểm khôi phục (restore point) tối ưu nhất khi gặp thảm họa hệ thống.

---

## 📝 Quy trình đóng góp tài liệu dành cho Agent

1. **Khi đề xuất kiến trúc mới:** Tạo một file ADR mới dạng `ADRs/NNNN-descriptive-name.md` để ghi nhận bối cảnh, các giải pháp cân nhắc, và giải pháp được chọn.
2. **Khi hoàn thành một chu kỳ nâng cấp:** Cập nhật ngay `CHANGELOG.md` dưới định dạng chuẩn [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
3. **Khi thay đổi Database Schema / Agent Contract:** Viết hướng dẫn chi tiết trong thư mục `migration-paths/`.

---

> [!TIP]
> Việc ghi chép tài liệu rõ ràng tại đây giúp tăng điểm **Confidence Score (Mức độ tin cậy)** của Agent lên trên 90%, giảm thiểu thời gian debug và nâng cao đáng kể chất lượng sản phẩm đầu ra!
