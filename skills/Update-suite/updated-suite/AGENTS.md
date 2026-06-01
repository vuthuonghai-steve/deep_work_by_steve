# 📂 /skills/Update-suite/updated-suite/
## 🚀 BỘ SKILL SAU KHI ĐƯỢC UPDATE (STAGING & TESTBED) - HƯỚNG DẪN DÀNH CHO AGENT

Tài liệu này cung cấp hướng dẫn và quy định cho thư mục `updated-suite/`, nơi đóng vai trò làm **không gian phát triển tích cực (active workspace/testbed)** và **bệ phóng đồng bộ (staging zone)** cho phiên bản mới của bộ Skill Suite.

---

## 🗺️ Tổng quan Vai trò & Tầm quan trọng
Thư mục `updated-suite/` là **"Phòng thí nghiệm công nghệ cao"** nơi Agent trực tiếp viết code, thiết kế lại cấu trúc, và triển khai các cải tiến cho bộ Master Skill Suite.

```
 ┌─────────────────────────────────────────────────────────────┐
 │                         updated-suite/                      │
 │                                                             │
 │   - Không gian phát triển tích cực (Staging)                │
 │   - Nơi áp dụng các cải tiến mới của CASE System            │
 │   - Cổng kiểm định Sandbox trước khi Deploy lên Main        │
 └─────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **QUY TẮC BẤT BIẾN:**
> Tất cả các chỉnh sửa logic, cập nhật `SKILL.md`, cải tiến script đều phải diễn ra tại đây. Code trong thư mục này chỉ được coi là **"Sẵn sàng Deploy" (Production-ready)** sau khi đã vượt qua toàn bộ các bài kiểm tra tự động tại sandbox và được ký duyệt (signed-off).

---

## 🏗️ Cấu trúc Thư mục Đề xuất

```text
updated-suite/
├── AGENTS.md                   # Tài liệu hướng dẫn này
├── skill-explorer/             # Bộ Skill Explorer đã nâng cấp
│   └── SKILL.md
├── skill-architect/            # Bộ Skill Architect đã nâng cấp
│   └── SKILL.md
├── skill-planner/              # Bộ Skill Planner đã nâng cấp
│   └── SKILL.md
├── skill-builder/              # Bộ Skill Builder đã nâng cấp
│   └── SKILL.md
├── _shared/                    # Shared resources phiên bản mới
│   └── knowledge/
└── tests/                      # Bộ kiểm thử tích hợp tự động cho Skills
```

---

## 🛡️ Tích hợp CASE System & Quy trình Phát triển (Boot -> Verify -> Deploy)

Quy trình phát triển tại `updated-suite/` tuân thủ nghiêm ngặt 3 cơ chế an toàn:

### 1. 🚀 PREVENT (Ngăn ngừa lỗi sớm)
* **Khởi động An toàn (Boot Sequence):** Trước khi viết code, Agent phải chạy công cụ phân tích để nắm rõ phạm vi nâng cấp.
* **Cấu hình chặt chẽ:** Sử dụng schema validation cho file `SKILL.md` để phát hiện lỗi định dạng ngay khi viết.

### 2. 🔍 DETECT (Phát hiện & Sửa lỗi)
* **Sandbox Verification:** Chạy kiểm thử code trong Docker Sandbox cô lập (sử dụng skill `sandbox-validator` hoặc chạy pytest cục bộ nếu an toàn).
* **Gate Validation:** Sử dụng các validator script để xác minh sự khớp nối giữa `design.md` và mã nguồn thực tế.

### 3. 🔄 RECOVER & DEPLOY (Đồng bộ hóa an toàn)
Khi phiên bản mới đã vượt qua 100% các bài test và đáp ứng đầy đủ tiêu chí chất lượng:
1. Thực hiện sao lưu phiên bản hiện tại từ hệ thống chính vào `current-suite/` (nếu chưa làm).
2. Kích hoạt script đồng bộ hóa để đẩy code từ `updated-suite/` sang hệ thống chạy thực:
   ```bash
   python3 skills/rebuild/skill-sync/scripts/sync_skills.py
   ```
3. Lưu trữ tài liệu chuyển đổi vào `lifecycle-docs/`.

---

## 📝 Quy định Kiểm soát Chất lượng (Quality Gate Checklist)

Trước khi kích hoạt lệnh Deploy, Agent phải đảm bảo:
- [ ] Tất cả các file `SKILL.md` đều có mô tả, version rõ ràng, và khớp schema.
- [ ] Không chứa code placeholder (`// TODO`, `pass`, `// mock`).
- [ ] Đã chạy linting và format toàn bộ code mới.
- [ ] Chạy thành công suite tests mà không có lỗi biên dịch hay runtime lỗi.

---

> [!TIP]
> Hãy tận dụng tối đa sức mạnh của **Heavy Thinking** tại đây để kiến tạo nên những Skill có độ tự chủ cao, xử lý lỗi thông minh và mang lại trải nghiệm tối ưu nhất cho người dùng!
