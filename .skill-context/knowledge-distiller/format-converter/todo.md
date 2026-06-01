# format-converter — Implementation Plan

> **Khởi tạo**: 2026-05-25
> **Nguồn gốc**: design.md (Architecture Design)
> **Trạng thái**: 🔵 IN PROGRESS

---

## 1. Pre-requisites

| # | Tài liệu / Kiến thức | Tier | Mục đích | Trace | Status |
|---|----------------------|------|----------|-------|--------|
| 1 | CLAUDE.md format rules | Domain | Hiểu nguyên tắc chọn Markdown/YAML/XML tối ưu cho AI | [TỪ AUDIT TÀI NGUYÊN] [TỪ DESIGN §1] | ✅ Sẵn có |
| 2 | exploration.md | Domain | Báo cáo khảo sát nghiệp vụ và phân rã 4 micro-skills | [TỪ AUDIT TÀI NGUYÊN] [TỪ DESIGN §1] | ✅ Sẵn có |
| 3 | resources/01-optimal-formats.md | Domain | Hướng dẫn chi tiết cách phối hợp các định dạng lai | [TỪ AUDIT TÀI NGUYÊN] [TỪ DESIGN §2] | ✅ Sẵn có |
| 4 | resources/02-knowledge-chunking-layers.md | Domain | Mô hình 4 lớp tri thức và Progressive Disclosure | [TỪ AUDIT TÀI NGUYÊN] [TỪ DESIGN §2] | ✅ Sẵn có |
| 5 | resources/03-security-and-anti-injection.md | Domain | Biện pháp chống Prompt Injection bằng XML boundaries | [TỪ AUDIT TÀI NGUYÊN] [TỪ DESIGN §2] | ✅ Sẵn có |

---

## 2. Phase Breakdown

### Phase 1: Core Zone (Core AI Instructions)

| # | Task | Priority | Est. Hours | Dependencies | Trace | Status |
|---|------|----------|------------|--------------|-------|--------|
| 1.1 | Tạo `SKILL.md` dưới thư mục `skills/rebuild/format-converter/` — Định nghĩa persona "Format Converter Specialist", quy định 4 phases xử lý (Collect, Analyze, Restructure, Output), áp dụng các Guardrails an toàn bảo mật, cấm command line execution, đảm bảo budget < 600 tokens. -> `SKILL.md` | Critical | 3-4 | None | [TỪ DESIGN §3] | ⬜ TODO |

---

### Phase 2: Knowledge Zone (Domain Standards)

| # | Task | Priority | Est. Hours | Dependencies | Trace | Status |
|---|------|----------|------------|--------------|-------|--------|
| 2.1 | Tạo `knowledge/standards.md` dưới thư mục `skills/rebuild/format-converter/` — Đặc tả quy chuẩn định dạng lai YAML/XML/MD dựa trên CLAUDE.md và exploration resources. Làm rõ vai trò từng định dạng, mô hình 4 lớp tri thức (L0-L3) và ngân sách Token Budget tương ứng. -> `knowledge/standards.md` | High | 2-3 | None | [TỪ DESIGN §3] | ⬜ TODO |

---

### Phase 3: Data & Loop Zone (Artifacts & Quality Gate)

| # | Task | Priority | Est. Hours | Dependencies | Trace | Status |
|---|------|----------|------------|--------------|-------|--------|
| 3.1 | Tạo `loop/checklist.md` dưới thư mục `skills/rebuild/format-converter/` — Bảng checklist tự kiểm soát chất lượng (QA) gồm các hạng mục đánh giá tỷ lệ phân tách, an toàn bảo mật, và tính Goldilocks zone. Quy định rõ cơ chế chấm điểm và xử lý dừng khi Confidence Score < 70%. -> `loop/checklist.md` | Critical | 2 | 1.1 | [TỪ DESIGN §3] | ⬜ TODO |
| 3.2 | Tạo tệp tin nháp trung gian rỗng `data/distilled_draft.yaml` dưới thư mục `skills/rebuild/format-converter/` — Làm tệp lưu trữ kết quả đầu ra nháp của quá trình chắt lọc. -> `data/distilled_draft.yaml` | Medium | 0.5 | None | [TỪ DESIGN §3] | ⬜ TODO |

---

## 3. Knowledge & Resources Needed

### Internal Resources
| Resource | Format | Purpose | Status |
|----------|--------|---------|--------|
| CLAUDE.md | Markdown | Hệ tiêu chuẩn và nguyên lý chọn định dạng | ✅ Sẵn có [TỪ AUDIT TÀI NGUYÊN] |
| `.skill-context/knowledge-distiller/resources/01-optimal-formats.md` | Markdown | Hướng dẫn chi tiết cách phối hợp các định dạng lai | ✅ Sẵn có [TỪ AUDIT TÀI NGUYÊN] |
| `.skill-context/knowledge-distiller/resources/02-knowledge-chunking-layers.md` | Markdown | Đặc tả mô hình 4 lớp tri thức và chuẩn llms.txt | ✅ Sẵn có [TỪ AUDIT TÀI NGUYÊN] |
| `.skill-context/knowledge-distiller/resources/03-security-and-anti-injection.md` | Markdown | Hướng dẫn phòng chống Prompt Injection | ✅ Sẵn có [TỪ AUDIT TÀI NGUYÊN] |

### Tool Knowledge
| Tool | Purpose | Required |
|------|---------|----------|
| YAML | Cấu trúc dữ liệu trung gian và config | Yes |
| Markdown | Tài liệu giải thích tự nhiên | Yes |
| XML tags | Phân tách ngữ nghĩa và boundaries | Yes |

---

## 4. Ghi Chú & Hướng Dẫn Vận Hành

- **[CẦN LÀM RÕ]**: Cần làm rõ với người sử dụng nếu cấu trúc `raw_source.xml` bị lỗi định dạng XML trước khi Agent thực thi chuyển đổi.
- **[GỢI Ý BỔ SUNG]**: Gợi ý bổ sung một script tự động kiểm tra token thực tế của các khối tri thức đầu ra bằng thư viện `tiktoken` trong tương lai để thay thế việc ước lượng ký tự thủ công.

---

## 5. Definition of Done

### Checklist — Toàn bộ các hạng mục phải được tích dấu hoàn thành:

- [ ] **Core `SKILL.md` hoàn chỉnh**:
  - [ ] Persona định nghĩa rõ ràng: Chuyên gia chuyển đổi và bóc tách cấu trúc tri thức.
  - [ ] Kích thước file cực kỳ nhỏ gọn (< 600 tokens) để tiết kiệm ngữ cảnh.
  - [ ] Quy định rõ 4 Phase xử lý nghiệp vụ.
  - [ ] Tích hợp đầy đủ các Guardrails an toàn bảo mật (cấm shell command, bọc XML).

- [ ] **`knowledge/standards.md` đạt chuẩn**:
  - [ ] Phản ánh chính xác tri thức từ CLAUDE.md và các tài liệu tài nguyên KD-RES.
  - [ ] Phân tích chi tiết vai trò của 3 định dạng MD, YAML, XML.
  - [ ] Định nghĩa rõ ràng mô hình 4 lớp tri thức L0-L3 và Token Budget.

- [ ] **`loop/checklist.md` nghiêm ngặt**:
  - [ ] Chứa ít nhất 5 tiêu chí tự kiểm duyệt chất lượng quan trọng.
  - [ ] Quy định rõ Confidence Score Gate (PASS >= 70%, dừng và báo cáo khi < 70%).

- [ ] **Tệp trung gian `data/distilled_draft.yaml`**:
  - [ ] Được khởi tạo chính xác tại đường dẫn zone mapping.
