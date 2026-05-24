---
skill_schema_version: "3.0.0"
artifact_type: "todo"
skill_name: "index-builder"
generated_by: "skill-planner"
generated_at: "2026-05-25T03:05:00.000000+00:00"
stage: "planner"
status: "completed"
---

# index-builder — Kế Hoạch Triển Khai Chi Tiết

> **Khởi tạo**: 2026-05-25
> **Trạng thái**: ✅ COMPLETED
> **Bản đồ chỉ dẫn thiết kế**: [design.md](file:///home/steve/Work-space/deep_work_by_steve/.skill-context/knowledge-distiller/index-builder/design.md)

---

## 1. Pre-requisites (Điều kiện tiên quyết)

| # | Tài liệu / Kiến thức | Loại kiến thức | Mục đích | Trace | Trạng thái |
|---|---------------------|------|----------|-------|--------|
| 1 | Cấu trúc tiêu chuẩn của tệp chỉ mục `llms.txt` | Domain | Hiểu các mục cần phân nhóm (Core, Domain, Examples) | [TỪ DESIGN §2.1] | ✅ |
| 2 | Kỹ thuật quét thư mục đệ quy và loại trừ file rác trong Python | Technical | Tránh quét các file ẩn, file hệ thống và symlinks | [TỪ DESIGN §2.2] | ✅ |
| 3 | Cách tính toán và ước lượng Token bằng thư viện Python (tiktoken hoặc tương đương, hoặc thuật toán heuristics xấp xỉ) | Technical | Thống kê chính xác ngân sách token của từng tệp tri thức | [TỪ DESIGN §2.1] | ✅ |
| 4 | Kỹ thuật kiểm định liên kết (link checker) cho các liên kết tương đối | Technical | Đảm bảo không xảy ra liên kết đứt gãy trong tệp chỉ mục | [TỪ DESIGN §2.3] | ✅ |
| 5 | Các tài nguyên của master-skill `knowledge-distiller` đã audit | Domain | Kế thừa các tiêu chuẩn tri thức sẵn có từ explore | [TỪ EXPLORATION §2] | ✅ |

---

## 2. Phase Breakdown (Phân rã các giai đoạn)

### Phase 0: Resource Preparation (Chuẩn bị Tài nguyên Tri thức)

| # | Nhiệm vụ (Task) | Mức độ ưu tiên | Thời gian (giờ) | Phụ thuộc | Trace |
|---|-----------------|----------------|-----------------|-----------|-------|
| 1 | Biên soạn tệp tri thức `knowledge/standards.md` chứa tiêu chuẩn định dạng `llms.txt`, quy định phân tầng tri thức và ngân sách token chi tiết | Critical | 1 | Không | [TỪ DESIGN §3] |

### Phase 1: Core Implementation (Lập trình mã nguồn lõi)

| # | Nhiệm vụ (Task) | Mức độ ưu tiên | Thời gian (giờ) | Phụ thuộc | Trace |
|---|-----------------|----------------|-----------------|-----------|-------|
| 1 | Tạo tệp chỉ thị AI `SKILL.md` (Persona chuyên gia tổng hợp, quy trình 3 phases hoạt động, guardrails và cơ chế bộc lộ lũy tiến) | Critical | 1 | Phase 0 | [TỪ DESIGN §3] |
| 2 | Viết mã nguồn Python `scripts/build_index.py` thực hiện: quét thư mục đệ quy, loại trừ blacklist, phân loại tri thức L0-L3, tính toán token, tạo/cập nhật `data/llms.txt` và tự động kiểm định link | Critical | 3 | Task 1 | [TỪ DESIGN §3, §2.2] |
| 3 | Tạo tệp tự kiểm soát chất lượng `loop/checklist.md` cho các bước biên dịch, cập nhật index và đồng bộ ngữ cảnh | Critical | 0.5 | Task 1 | [TỪ DESIGN §3] |

### Phase 2: Knowledge & Documentation (Hoàn thiện tài liệu)

| # | Nhiệm vụ (Task) | Mức độ ưu tiên | Thời gian (giờ) | Phụ thuộc | Trace |
|---|-----------------|----------------|-----------------|-----------|-------|
| 1 | Rà soát và hoàn thiện tệp `knowledge/standards.md` đảm bảo tương thích 100% với logic code của script | High | 0.5 | Phase 0, Phase 1 | [TỪ DESIGN §3] |

### Phase 3: Verification & Packaging (Xác minh & Đóng gói)

| # | Nhiệm vụ (Task) | Mức độ ưu tiên | Thời gian (giờ) | Phụ thuộc | Trace |
|---|-----------------|----------------|-----------------|-----------|-------|
| 1 | Chạy thử nghiệm script `build_index.py` trên môi trường thực tế, kiểm định tệp `data/llms.txt` được sinh ra | Critical | 1 | Phase 1 | [TỪ DESIGN §5] |
| 2 | Thực hiện tự kiểm soát chất lượng QA qua `loop/checklist.md`, đảm bảo tất cả files trong Zone Mapping tồn tại | Critical | 0.5 | Phase 1, Phase 2 | [TỪ DESIGN §3, §10] |

---

## 3. Knowledge & Resources Needed (Tri thức & Tài nguyên cần có)

| Tài nguyên (Resource) | Phân loại | Mục đích sử dụng | Trạng thái |
|-----------------------|-----------|------------------|------------|
| `SKILL.md` | Core | Persona và chỉ đạo luồng công việc của AI | ⬜ Cần tạo |
| `knowledge/standards.md` | Knowledge | Quy định và chuẩn hóa cấu trúc tệp `llms.txt` | ⬜ Cần tạo |
| `scripts/build_index.py` | Scripts | Logic tự động hóa sinh tệp chỉ mục và xác thực link | ⬜ Cần tạo |
| `data/llms.txt` | Data | Chỉ mục được biên dịch thành công | ⬜ Sẽ được sinh tự động |
| `loop/checklist.md` | Loop | Checklist QA cho luồng phát triển | ⬜ Cần tạo |

---

## 4. Definition of Done (Định nghĩa Hoàn thành)

### Core Files Verification (Xác minh tệp tin cốt lõi)
- [ ] `SKILL.md` tồn tại đầy đủ Persona, workflow 3 phases, guardrails và nhỏ hơn 800 tokens.
- [ ] `knowledge/standards.md` mô tả chi tiết tiêu chuẩn `llms.txt`, token budget.
- [ ] `scripts/build_index.py` chạy thành công không có lỗi runtime, tự động sinh `data/llms.txt`.
- [ ] `data/llms.txt` được sinh thành công đúng định dạng chuẩn.
- [ ] `loop/checklist.md` định nghĩa đầy đủ các tiêu chí tự kiểm soát chất lượng QA.

### Quality Checks (Kiểm định Chất lượng)
- [ ] Tất cả tệp tin được định nghĩa trong `design.md` §3 Zone Mapping phải tồn tại đầy đủ dưới thư mục `skills/rebuild/index-builder/`.
- [ ] Mọi task trong todo đều có Trace tag hợp lệ ngược về `design.md`.
- [ ] Không chứa bất kỳ nội dung placeholder rỗng nào.
- [ ] Chạy thành công link-checker tích hợp sẵn mà không phát hiện liên kết chết.

### Handoff Readiness (Sẵn sàng bàn giao)
- [ ] Báo cáo kết quả và đường dẫn đầy đủ các tệp tin cho caller agent (main agent).
- [ ] Tạo tệp nhật ký `build-log.md` nếu cần ghi nhận lịch sử xây dựng.

---

## 5. Notes (Ghi chú nghiệp vụ)

### Open Questions từ design.md §9
- **Q1**: Có cần sinh file phụ `llms-full.txt` (chứa nội dung gộp) không?
  - *Phương án giải quyết*: Hiện tại chỉ tập trung sinh file chỉ mục liên kết `llms.txt`. Nếu có nhu cầu mở rộng sẽ phát triển sau. [CẦN LÀM RÕ]
- **Q2**: Thư mục quét của script có nên hỗ trợ cấu hình động từ CLI không?
  - *Phương án giải quyết*: Rất cần. Thêm đối số `--target-dir` vào script để linh hoạt quét bất kỳ thư mục nào. [CẦN LÀM RÕ]

### Gợi ý bổ sung
- [GỢI Ý BỔ SUNG]: Script Python nên sử dụng thuật toán xấp xỉ số lượng token bằng cách tính số từ (words) chia cho `0.75` nếu không muốn phụ thuộc vào thư viện bên ngoài như `tiktoken` để tăng tính portability (không cần cài thêm pip packages).
- [GỢI Ý BỔ SUNG]: Thiết lập một cơ chế tự động giữ lại (preserve) các dòng mô tả do người dùng viết thủ công trong `llms.txt` cũ bằng cách parse và merge thông minh.

---

## 6. Builder Feedback Integration (Phản hồi từ Builder)

*(Hiện tại chưa có phản hồi nào từ kỹ sư triển khai)*

---

## Trace Tags Summary (Thống kê Trace Tags)

| Loại Tag (Tag Type) | Số lượng | Ví dụ cụ thể |
|-------------------|----------|--------------|
| [TỪ DESIGN §N] | 9 | §2.1, §2.2, §2.3, §3, §5, §10 |
| [TỪ EXPLORATION §N] | 1 | §2 |
| [GỢI Ý BỔ SUNG] | 2 | Notes section |
| [CẦN LÀM RÕ] | 2 | Open questions section |

---

> **Bước tiếp theo**: Thực hiện Stage 3 (Builder) để triển khai lập trình mã nguồn hoàn chỉnh theo todo.md dưới thư mục `skills/rebuild/index-builder/`.
