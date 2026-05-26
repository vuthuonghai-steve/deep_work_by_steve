# 📂 /skills/Update-suite/current-suite/
## 🛡️ BẢN ĐỒNG BỘ NGUỒN (CURRENT BASELINE) - HƯỚNG DẪN DÀNH CHO AGENT

Tài liệu này cung cấp hướng dẫn và quy định cho thư mục `current-suite/`, nơi đóng vai trò làm **điểm tựa đóng băng (frozen baseline)** cho toàn bộ quy trình nâng cấp bộ Master Skill Suite.

---

## 🗺️ Tổng quan Vai trò & Tầm quan trọng
Trong vòng đời bảo trì và nâng cấp, thư mục `current-suite/` là **"Hộp đen lưu trữ"** chứa bản sao chính xác của bộ Skill Suite hiện tại đang chạy ổn định trên hệ thống (bao gồm *skill-explorer*, *skill-architect*, *skill-planner*, và *skill-builder*).

```
 ┌─────────────────────────────────────────────────────────────┐
 │                         current-suite/                      │
 │                                                             │
 │   - Bản sao đông băng của hệ thống đang chạy                │
 │   - Điểm đối sánh (Diff baseline) để đo lường cải tiến      │
 │   - Điểm khôi phục (Rollback target) khi xảy ra sự cố       │
 └─────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **QUY TẮC BẤT BIẾN:**
> Thư mục này hoàn toàn là **ĐỌC-GHI CÓ KIỂM SOÁT (HOẶC CHỈ ĐỌC)** trong suốt quá trình nâng cấp. Các Agent **tuyệt đối không được chỉnh sửa trực tiếp** bất kỳ tệp nào ở đây trừ khi cần thiết lập cấu trúc ban đầu hoặc đồng bộ hóa trạng thái ổn định mới từ hệ thống chính trước khi bắt đầu một chu kỳ nâng cấp mới.

---

## 🏗️ Cấu trúc Thư mục Đề xuất

Khi bắt đầu chu kỳ nâng cấp, bộ skill hiện tại từ `skills/rebuild/` hoặc `skills/solution-flow/skill-builder-suite/` sẽ được copy nguyên bản vào đây:

```text
current-suite/
├── AGENTS.md                   # Tài liệu hướng dẫn này
├── skill-explorer/             # Bản frozen của Skill Explorer
│   └── SKILL.md
├── skill-architect/            # Bản frozen của Skill Architect
│   └── SKILL.md
├── skill-planner/              # Bản frozen của Skill Planner
│   └── SKILL.md
├── skill-builder/              # Bản frozen của Skill Builder
│   └── SKILL.md
└── _shared/                    # Shared resources hiện tại
    └── knowledge/
```

---

## 📝 Quy định dành cho Agent (Operational Guidelines)

| Hành động | Được phép? | Chi tiết & Hướng dẫn |
| :--- | :--- | :--- |
| **Đọc Code** |  **Có** | Đọc thoải mái để phân tích cấu trúc, logic hiện tại và phát hiện các điểm nghẽn (pain points). |
| **So sánh Diff** |  **Có** | Sử dụng làm gốc để chạy `diff` nhằm so sánh sự khác biệt và tối ưu hóa ở bộ skill mới. |
| **Chỉnh sửa File** | ❌ **Không** | Không được sửa đổi logic, sửa comment hay tối ưu trực tiếp trên thư mục này. |
| **Đồng bộ hóa** | 🔄 **Chỉ khi bắt đầu** | Chỉ copy đè từ bộ skill đang chạy trên hệ thống vào đây tại thời điểm khởi tạo chu kỳ nâng cấp. |

---

## 🛡️ Tích hợp CASE System (PREVENT -> DETECT -> RECOVER)

Thư mục này đóng vai trò quan trọng trong việc hiện thực hóa cột trụ **RECOVER (Khôi phục)** của CASE System:
* **Hỗ trợ Rollback:** Nếu phiên bản đang phát triển tại `updated-suite/` gặp lỗi nghiêm trọng trong quá trình tích hợp hoặc kiểm thử sandbox, Agent sẽ dùng mã nguồn tại `current-suite/` để rollback lại trạng thái an toàn.
* **Đối chiếu Regression:** Đảm bảo các tính năng cũ không bị mất đi (Backward Compatibility) sau khi nâng cấp bằng cách so sánh hành vi input/output.

---

> [!TIP]
> Trước khi bắt đầu bất kỳ hành động viết mã nào trong `updated-suite/`, hãy chạy công cụ thu thập tài nguyên hoặc xem chi tiết cấu trúc `current-suite/` để có cái nhìn toàn cảnh về những gì đang hoạt động tốt.
