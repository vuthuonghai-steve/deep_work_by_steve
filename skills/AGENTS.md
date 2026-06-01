# Hướng dẫn Cấu trúc Thư mục Skills

Tài liệu này hướng dẫn chi tiết về cấu trúc và vai trò của các thư mục bên trong `/home/steve/Work-space/deep_work_by_steve/skills/` nhằm giúp các Agents và Nhà phát triển dễ dàng nắm bắt, bảo trì, nâng cấp hệ thống kỹ năng (Skills).

---

## 📂 Sơ đồ Cấu trúc Thư mục

```text
skills/
├── AGENTS.md              # Tài liệu hướng dẫn cấu trúc thư mục (Tệp này)
├── raw/                   # Chứa các tài liệu, kịch bản, tri thức thô chưa nâng cấp
├── rebuild/               # Vị trí chứa các Skill thông thường được Rebuild và Đồng bộ
├── solution-flow/         # Tài liệu & Micro-skills chuyên biệt cho từng Flow giải quyết vấn đề
└── Update-suite/          # Khu vực riêng để phát triển và cập nhật bộ Skill Suite
```

---

## 🔍 Chi tiết Vai trò & Quy định sử dụng từng Thư mục

### 1. 📥 `skills/raw/`
* **Mô tả:** Nơi lưu trữ tài nguyên thô, các ý tưởng thiết kế, hoặc các tệp cấu hình Skill cũ chưa được tối ưu hóa.
* **Vai trò:**
  * Lưu trữ dữ liệu đầu vào trước khi thực hiện quy trình nâng cấp hoặc tái cấu trúc.
  * Là nguồn tham khảo lịch sử để nâng cấp các Skill khi có yêu cầu hoặc khi phát hiện lỗi/điểm chưa tối ưu.
* **Quy trình:** Khi cần nâng cấp một Skill cũ, tài nguyên từ thư mục `raw` sẽ được phân tích, cấu trúc lại và chuyển sang dạng chuẩn hóa tại `rebuild` hoặc `solution-flow`.

### 2. 🔨 `skills/rebuild/`
* **Mô tả:** Khu vực lưu trữ và quản lý các Skill thông thường đã được tối ưu hóa, cấu trúc lại (rebuilt) theo chuẩn thiết kế mới.
* **Vai trò:**
  * Chứa các Skill dùng chung (General Skills) đã sẵn sàng để đồng bộ với môi trường làm việc thông qua công cụ đồng bộ (ví dụ: `skill-sync`).
  * Đảm bảo tính nhất quán của mã nguồn, tài liệu hướng dẫn (`SKILL.md`), và các script bổ trợ cho từng Skill.

### 3. 🎯 `skills/solution-flow/`
* **Mô tả:** Thư mục lưu trữ các tài liệu kiến trúc, hướng dẫn và các **Micro-skills** được thiết kế riêng biệt để giải quyết các Flow công việc cụ thể hoặc các bài toán chuyên sâu.
* **Vai trò:**
  * Tổ chức tri thức và kỹ năng theo từng luồng giải quyết vấn đề riêng biệt.
  * Tránh làm loãng các Skill chung bằng cách cô lập các giải pháp đặc thù vào các thư mục luồng tương ứng.

### 4. 🚀 `skills/Update-suite/`
* **Mô tả:** Vùng không gian chuyên biệt được thiết lập riêng cho việc nghiên cứu, phát triển và cập nhật phiên bản mới của bộ **Skill Suite** (Hệ thống Master Skills: Architect -> Planner -> Builder).
* **Liên kết tài liệu quan trọng:**
  * Mọi hoạt động nâng cấp, điều chỉnh và cập nhật luồng cho bộ Master Skill Suite được mô tả và theo dõi chi tiết tại: [skill-builder-suite/README.md](file:///home/steve/Work-space/deep_work_by_steve/skills/solution-flow/skill-builder-suite/README.md).
* **Cấu trúc bên trong:**
  * 🛡️ [current-suite/](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/AGENTS.md): Bản sao đóng băng (frozen baseline) của bộ skill suite hiện tại đang chạy ổn định.
  * 📜 [lifecycle-docs/](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/lifecycle-docs/AGENTS.md): Nhật ký vòng đời nâng cấp, ghi nhận lịch sử thay đổi, ADRs (Quyết định thiết kế), và migration paths qua các version.
  * 🚀 [updated-suite/](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/updated-suite/AGENTS.md): Không gian phát triển tích cực (active workspace) để cải tiến, kiểm thử sandbox và chuẩn bị đồng bộ (staging zone) cho phiên bản mới.
* **Quy định:** Tránh can thiệp trực tiếp vào bộ core suite khi chưa được thử nghiệm và phê duyệt cấu trúc tại đây.

---

> [!NOTE]
> Mọi thay đổi về cấu trúc thư mục hoặc cơ chế hoạt động của các Skill cần được cập nhật đồng bộ vào tệp chỉ mục định vị và đồng bộ hóa ngữ cảnh chung. Đảm bảo tuân thủ nghiêm ngặt chuẩn định dạng tài liệu để các Agent AI có thể đọc hiểu và vận dụng chính xác nhất.
