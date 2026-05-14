# **BUILD GUIDELINES (Usage: Quy chuẩn viết nội dung)**

> **Usage**: Hướng dẫn Kỹ sư cách viết và tổ chức nội dung cho từng Zone. Dùng trong Step BUILD.

---

## 0. CHUẨN ANTHROPIC — BẮT BUỘC ĐỌC KHI VIẾT SKILL.MD

Trước khi viết `SKILL.md`, đọc [anthropic-skill-standards.md](anthropic-skill-standards.md).
File này chứa các yêu cầu bắt buộc từ Anthropic về cấu trúc, discovery, và hiệu quả của skill.

**Checklist nhanh (từ anthropic-skill-standards.md §9)**:
- YAML frontmatter dòng đầu (name + description ngôi thứ 3)
- name: lowercase-kebab-case, ≤ 64 chars, gerund form ưu tiên
- description: WHAT + WHEN trigger, ≤ 1024 chars
- Progressive Disclosure: files load đúng phase (không front-load)
- Workflow Tracker Checklist nếu có 3+ phases hoặc Interaction Points
- Examples file nếu có mapping trừu tượng
- SKILL.md body ≤ 500 lines

---

## 1. NGUYÊN TẮC VIẾT SKILL.MD (CORE)

- **Ngôn ngữ**: Tuyệt đối dùng thể mệnh lệnh (Imperative).
- **Anthropic Standards**: Tuân thủ 100% `anthropic-skill-standards.md` — YAML frontmatter, Progressive Disclosure, Checklist Tracker, Examples Pattern.
- **Phân tầng (PD)**: Mọi file trong `knowledge/`, `scripts/`, `loop/` phải có ít nhất 1 link tham chiếu từ `SKILL.md` tại đúng phase cần dùng (không phải ở Boot Sequence nếu không cần ngay).
- **Phases**: Chia workflow thành các Phase có thể đánh dấu hoàn thành.

## 2. NGUYÊN TẮC VIẾT KNOWLEDGE
 
 - Mỗi file phải có header **Usage** mô tả mục đích và thời điểm sử dụng.
 - Ưu tiên bảng và sơ đồ Mermaid.
 - Nội dung domain phải dẫn nguồn từ `resources/`.
 - **Fidelity Standard**: Tuyệt đối không tóm tắt tài nguyên `Critical`. Mọi định nghĩa, mã định danh (Rule IDs, Error codes) phải được chuyển hóa chính xác. Nếu resource có danh sách chi tiết, kết quả build phải có danh sách tương ứng.
 - **Kỹ thuật Parity Check**: Trước khi lưu file knowledge, hãy đếm số lượng mục/đoạn (headers) trong resource và đảm bảo file knowledge có số lượng tương đương. Nếu file knowledge ngắn hơn >30% so với tài liệu gốc dày đặc thông tin, hãy thực hiện lượt truyền dẫn thứ hai (Second Pass) để bổ sung chi tiết.

## 3. NGUYÊN TẮC VIẾT LOOP (CHECKLIST & LOG)

- **Checklist**: Phải ghi rõ tiêu chí có thể đo lường (measurable).
- **Build-log**: Phải phản ánh trung thực thực tế:
  * Số lượng Placeholder thực tế.
  * Tick checkbox `[x]` chỉ khi task ĐÃ hoàn thành thực sự.
  * Ghi rõ lý do nếu dừng build (Error Policy).

## 4. QUY TẮC ĐẶT TÊN (Naming)

- **Skill Name**: kebab-case (ví dụ: `skill-builder`).
- **Files trong Knowledge**: kebab-case.
- **Scripts**: snake_case hoặc kebab-case.
- **Checklist/Log**: kebab-case.

## 5. CONTEXT DIRECTORY COVERAGE (BAT BUOC)

Muc tieu: Dam bao Builder khong bo sot tai nguyen trong `.skill-context/{skill-name}/`.

### 5.1 Cau truc sub-skill context can hieu ro

```
.skill-context/{skill-name}/
├── design.md        # Architecture source of truth
├── todo.md          # Execution plan source of truth
├── build-log.md     # Evidence + usage matrix + validation log
├── resources/       # Domain references (business/uml/analysis docs)
├── data/            # Rule configs (yaml/json), scoring matrix
└── loop/            # Prior checks, proofs, phase logs (supportive)
```

### 5.2 Phan loai muc do uu tien tai nguyen

- `Critical`:
  - `design.md`
  - `todo.md`
  - Tat ca file trong `resources/`
  - Tat ca file trong `data/`
- `Supportive`:
  - Tat ca file trong `loop/`
  - Tai lieu proof/snapshot

### 5.3 Resource Usage Matrix (bat buoc trong build-log.md)

Builder phai co bang sau trong `.skill-context/{skill-name}/build-log.md`:

| Resource File | Priority | Used In Task | Output File(s) | Notes |
|---|---|---|---|---|
| `resources/...` | Critical | `Task x.y` | `knowledge/...` | rationale |

Quy tac:
- Moi file `Critical` phai xuat hien it nhat 1 dong.
- Moi dong phai co duong dan resource trong backticks.
- Khong duoc danh dau task done neu chua co dong trace tuong ung.
