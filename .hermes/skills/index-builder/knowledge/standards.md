# Tiêu Chuẩn Chỉ Mục llms.txt & Phân Tầng Tri Thức

> **Mã tài nguyên**: KD-STD-INDEX
> **Mục tiêu**: Định nghĩa các tiêu chuẩn kỹ thuật cấu trúc tệp chỉ mục `llms.txt` và mô hình phân tầng tri thức 4 lớp của AI Agent.

---

## 1. Tiêu Chuẩn Cấu Trúc Tệp `llms.txt`

Tệp chỉ mục `llms.txt` hoạt động như một bản đồ tri thức trung tâm đặt tại gốc thư mục hoặc phân vùng của skill. Định dạng bắt buộc là Markdown thuần túy và dễ đọc cho AI.

### Cấu trúc tiêu chuẩn bao gồm các mục chính:

1. **Tiêu đề & Giới thiệu ngắn**:
   - Tiêu đề chính dạng `# [Tên Dự án / Skill] — AI Knowledge Index`
   - Một dòng trích dẫn ngắn (blockquote) mô tả mục đích sử dụng.

2. **Core Guides (L0 & L1)**:
   - Danh sách các file chỉ thị nền tảng (`CLAUDE.md`, `SKILL.md`) và quy ước hành vi, quy tắc gọi công cụ.
   - Định dạng: `- [Tên hiển thị](file:///đường_dẫn_tuyệt_đối_hoặc_tương_đối): Mô tả ngắn gọn về vai trò của tệp tin.`

3. **Domain Knowledge (L2)**:
   - Danh sách các tài liệu nghiệp vụ chuyên sâu, thiết kế kiến trúc, mô hình hóa dữ liệu.

4. **Examples & Checklists (L3)**:
   - Danh sách các đoạn mã ví dụ hoàn chỉnh (exemplars) và checklist nghiệm thu QA.

---

## 2. Mô Hình Phân Tầng 4 Lớp Tri Thức (L0 - L3)

Để tối ưu hóa chi phí token và tránh hiện tượng AI bỏ sót ngữ cảnh quan trọng ở giữa tài liệu (Lost in the Middle), tri thức nghiệp vụ bắt buộc phải được chia làm 4 tầng riêng biệt:

| Lớp Tri Thức | Tên gọi & Ý nghĩa | Ví dụ tệp tin | Ngân sách Token (Khuyến nghị) |
|:---|:---|:---|:---|
| **L0** | **Anchor Rules**: Luật Neo tối thượng, hiến pháp không được vi phạm. | `CLAUDE.md`, System Prompt | **150 - 400 tokens** |
| **L1** | **Working Policy**: Quy ước hành vi, quy tắc viết code, coding conventions. | `loop/checklist.md`, `.claude/rules/` | **400 - 1200 tokens** |
| **L2** | **Domain Context**: Tri thức nghiệp vụ chuyên ngành, kiến trúc hệ thống. | `knowledge/standards.md`, `docs/design.md` | **600 - 2500 tokens** |
| **L3** | **Evidence & Examples**: Code mẫu, dữ liệu đầu vào ví dụ, specs kỹ thuật. | `examples/`, `specs/` | **300 - 2000 tokens** (Chỉ nạp khi cần viết code) |

---

## 3. Quy Định Ngân Sách Token & Thống Kê Chỉ Mục

Khi script `build_index.py` quét và tổng hợp chỉ mục, nó phải:
1. Xác định kích thước tệp tin thực tế trên đĩa (bytes).
2. Ước tính số lượng token bằng cách đếm số từ (words) trong file và nhân với hệ số `1.33` (hoặc chia `0.75`).
3. Ghi nhận thông tin phân tầng rõ ràng để AI Agents khi đọc `llms.txt` có thể tự động ước lượng tổng token cần nạp.
4. Xác thực tất cả các liên kết tương đối để đảm bảo không bị đứt gãy hoặc trỏ tới các tệp tin không tồn tại.
