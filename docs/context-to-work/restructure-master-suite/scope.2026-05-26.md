# PROBLEM SCOPING: RESTRUCTURE MASTER SKILL SUITE TO VER_1.0.0

Tài liệu này xác định phạm vi ảnh hưởng, hiện trạng hệ thống và các vấn đề của bộ Master Skill Suite hiện tại (`Ver_0`) trước khi tiến hành nâng cấp. Thiết kế tuân thủ nghiêm ngặt kỹ năng `context-before-fix` và tích hợp sâu báo cáo phân tích từ Subagent Nghiên cứu.

---

## 1. Problem Summary (Tóm tắt vấn đề)
Bộ kỹ năng Master Skill Suite phiên bản hiện tại (`Ver_0`) gặp nhiều lỗi nghiêm trọng, chưa sẵn sàng cho môi trường thương mại (production-ready). Qua phân tích chi tiết, chúng tôi xác định các điểm nghẽn cốt lõi sau:
- **Vai trò chồng chéo & Quá tải**:
  - `skill-explorer` (Stage 0) bị quá tải vai trò thiết kế khi phải tự tính toán điểm phức tạp SCS, tự phân rã Micro-skills và vẽ sơ đồ phối hợp Mermaid. Lẽ ra đây phải là vai trò của `skill-architect` (Stage 1).
  - `skill-planner` (Stage 2) bị chồng chéo khi phải tự đánh giá tài nguyên `resources/` là "Thin" hay "Rich" và lập kế hoạch bù đắp (đây thuộc về khâu Khảo sát đầu vào).
  - `skill-builder` (Stage 3) bị quá tải khi vừa coding vừa kiểm soát placeholder, vừa phải ghi log chi tiết. Đồng thời, vòng lặp làm rõ (Clarify Loop) bị lỗi luồng một chiều khi Builder sửa đổi ngược tệp `design.md` của Architect, gây rủi ro mất đồng bộ nghiêm trọng.
- **Vi phạm Token Budget chuẩn CLAUDE.md**:
  - Tệp `SKILL.md` (L0) của Planner dài **360 dòng (~14.6KB, ~2,800 tokens)** và Builder dài **330 dòng (~12KB, ~2,300 tokens)**, vượt xa ngưỡng khuyến nghị cực đại là **700 tokens**. Điều này làm cạn kiệt Token budget của AI Agent ngay khi vừa khởi động.
- **Vi phạm Nguyên tắc DRY (Don't Repeat Yourself)**:
  - Bản sao vật lý của `knowledge/architect.md` bị lặp lại ở 3 nơi (explorer, planner, builder) thay vì dùng đường dẫn tham chiếu tương đối trỏ về `_shared/knowledge/framework.md`.
- **Thiếu sót Vùng Loop & Tệp rác**:
  - `skill-explorer` thiếu hoàn toàn tệp cấu trúc `.yaml` và script validator chuyên biệt cho Stage 0.
  - Tồn tại tệp nén rác `skill-architect/references/_shared.zip` trong git-tree làm nặng bộ nhớ AI.
- **Mất bối cảnh giữa các Session độc lập (Stateless Desynchronization)**:
  - Không có cơ chế lưu trữ lập luận ẩn (hidden reasoning) giữa các phiên chạy, các tệp trung gian chỉ chứa văn bản thô. Lỗi chính tả nhỏ của trace tags (như `[CẦU LÀM RÕ]`) lập tức làm treo hệ thống handoff validator.

---

## 2. Entry Point (Điểm bắt đầu)
- Thư mục nguồn: `/home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/`
  - [skill-explorer](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/skill-explorer/SKILL.md)
  - [skill-architect](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/skill-architect/SKILL.md)
  - [skill-planner](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/skill-planner/SKILL.md)
  - [skill-builder](file:///home/steve/Work-space/deep_work_by_steve/skills/Update-suite/current-suite/Ver_0/skill-builder/SKILL.md)

---

## 3. Scope Definition (Phạm vi xác định)
Phạm vi nâng cấp sẽ diễn ra hoàn toàn bên trong không gian phát triển tích cực:
`/home/steve/Work-space/deep_work_by_steve/skills/Update-suite/updated-suite/`

Các thành phần cần xây dựng và cấu trúc lại bao gồm:
1. `_shared/knowledge/framework.md`: Định nghĩa lại vòng đời 6 giai đoạn và luật giao tiếp bối cảnh chung, loại bỏ trùng lặp tri thức.
2. `skill-explorer/` (Stage 0): Rút gọn nghiệp vụ khảo sát, bổ sung đầu ra là danh sách tiêu chí kiểm định chất lượng (`criteria.md`), bổ sung loop validator.
3. `skill-architect/` (Stage 1): Chuyển giao quyền lực phân rã Micro-skills từ Explorer sang Architect, thiết kế cấu trúc dựa trên 3 Pillars và 7 Zones (`design.md`).
4. `skill-planner/` (Stage 2): Tái cấu trúc tệp `SKILL.md` để đưa token budget về dưới 700 tokens, chuyển logic dài sang `policy/` và `knowledge/`.
5. `skill-builder/` (Stage 3): Tái cấu trúc tệp `SKILL.md` tương tự Planner, cấm Builder ghi đè ngược lên `design.md`.
6. `skill-tester/` (Stage 4 - MỚI): Chạy kịch bản kiểm thử trong Docker Sandbox và xuất báo cáo nghiệm thu (`verification.md`).
7. `skill-indexer/` (Stage 5 - MỚI): Đồng bộ hóa danh mục, sinh tài liệu hướng dẫn nhanh (User Guide).

---

## 4. Impact Analysis (Phân tích ảnh hưởng)
### Ảnh hưởng trực tiếp (Direct Impact):
- Các micro-skills được sinh ra theo quy trình cũ bị loãng chất lượng, thiếu các chốt chặn an toàn (validation gates), dễ bị lỗi cú pháp khi đưa vào chạy thực tế.
- Khả năng quản trị hệ thống kém do số lượng kỹ năng tăng lên nhưng không được lập chỉ mục đồng bộ.

### Ảnh hưởng gián tiếp (Indirect Impact):
- Khi chạy trên các nền tảng AI Agent stateless (mỗi bước là một session độc lập), quy trình bị gãy do thiếu Sổ cái bối cảnh (Context Ledger) để truyền tải lập luận ẩn và trạng thái đồng bộ giữa các stage.

---

## 5. Call Chain (Chuỗi gọi)
```text
User Request 
   │
   ▼
[Stage 0: Explorer] ──(exploration.md, criteria.md)──► [Stage 1: Architect]
                                                               │
                                                          (design.md)
                                                               │
                                                               ▼
[Stage 3: Builder] ◄──(todo.md)── [Stage 2: Planner] ◄─────────┘
   │
 (Code)
   │
   ▼
[Stage 4: Tester] ──(verification.md)──► [Stage 5: Indexer] ──► Production Ready
```

---

## 6. Data Flow (Luồng dữ liệu)
- Đầu ra của Stage trước đóng vai trò là "Sự thật duy nhất" (Ground Truth) và là đầu vào bắt buộc của Stage sau thông qua thư mục `.skill-context/{skill-name}/`.
- Bảng tiêu chí chất lượng `criteria.md` do Stage 0 tạo ra sẽ đi xuyên suốt pipeline và được Stage 4 (Tester) sử dụng làm kịch bản kiểm thử chính xác để nghiệm thu.

---

## 7. Evidence (Minh chứng lỗi ở Ver_0)
- **Tập tin `skill-explorer/SKILL.md`**: Gánh vác quá nhiều chức năng từ Phase 1 tới Phase 4, bao gồm cả phân tích Prompt Injection và SCS, dẫn đến cạn kiệt Token Budget (>1200 tokens chỉ riêng file hướng dẫn).
- **Tập tin `skill-planner/SKILL.md` và `skill-builder/SKILL.md`**: Thiếu các bước kiểm tra chất lượng tự động hóa, chủ yếu dựa trên checklist thủ công mà AI tự đọc tự phê duyệt.

---
## 8. Confidence Assessment (Đánh giá mức tin cậy)
- Mức độ tin cậy: **98%** (Đã kiểm chứng trực tiếp và chạy quét codebase chuyên sâu thông qua Subagent Nghiên cứu).

---

## 9. Open Questions (Các câu hỏi mở)
- Làm thế nào để tự động hóa khâu chuyển giao "Lập luận ẩn" (hidden reasoning) của LLM qua từng stage mà không làm phình to token budget của các tệp trung gian?
- Cơ chế kiểm thử tự động của `skill-tester` nên dựa trên unit tests (pytest) hay thực thi bằng schema validator thông qua công cụ `rtk`?

---

> [!NOTE]
> NO CODE CHANGES — Context ready for design and upgrade phase.

