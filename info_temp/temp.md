## 📋 DANH SÁCH VẤN ĐỀ CHI TIẾT

### 🔴 VẤN ĐỀ CẤP ĐỘ 1 (ROOT CAUSES) 

| # | Vấn đề | Bằng chứng | Tác động |
|---|---------|-------------|-----------|
| **R1** | **CLAUDE.md (format knowledge source) KHÔNG được reference trong bất kỳ skill nào** | `grep -r "CLAUDE.md"` trong cả 3 skill đều return 0 results | Agent không biết về các format chuẩn YAML/XML/Token budget |
| **R2** | **Format knowledge bị CÔ LẬP** - chỉ tồn tại trong CLAUDE.md thay vì được nhúng vào skill files | CLAUDE.md chứa đầy đủ semantic_questions, format_selection_rules, token_budget nhưng KHÔNG ai dùng | Khi invoke skill, agent không load được format knowledge |
| **R3** | **Progressive Disclosure chỉ là DECLARATION không có ENFORCEMENT** | skill-builder có `progressive_disclosure:` trong frontmatter nhưng KHÔNG có cơ chế từ chối nếu agent load sai tier | Agent vẫn load tất cả context một lần |

---

### 🟠 VẤN ĐỀ CẤP ĐỘ 2 (SKILL SPECIFIC)

#### **skill-architect**

| # | Vấn đề | Chi tiết |
|---|---------|----------|
| **A1** | **Thiếu format knowledge trong knowledge/architect.md** | File này chỉ mô tả workflow, KHÔNG chứa YAML/XML format standards |
| **A2** | **Thiếu ví dụ (examples) cho design.md output** | Không có reference implementation cho thấy design.md nên trông như thế nào với đầy đủ format |
| **A3** | **Zone Mapping template thiếu format specification** | §3 Zone Mapping Contract định nghĩa cấu trúc nhưng không enforce YAML format trong actual output |
| **A4** | **Thiếu enforcement cho §1-§10 format** | design.md checklist chỉ kiểm tra sự tồn tại, không kiểm tra format compliance |

#### **skill-planner**

| # | Vấn đề | Chi tiết |
|---|---------|----------|
| **P1** | **Không reference format knowledge từ CLAUDE.md** | Todo.md output không bao giờ sử dụng YAML blocks hay XML tags dù CLAUDE.md yêu cầu |
| **P2** | **Thiếu Examples cho trace tag validation** | `[TỪ DESIGN §N]` được dùng nhưng không có validator script để reject missing/wrong tags |
| **P3** | **3-Tier Analysis không đầy đủ** | Tier 1/2/3 chỉ là tên gọi, không có hướng dẫn cụ thể về token budget hay format per tier |
| **P4** | **Phase 0 (Resource Preparation) không có success criteria** | Sinh task nhưng không define khi nào resource được coi là "Rich" vs "Thin" |

#### **skill-builder**

| # | Vấn đề | Chi tiết |
|---|---------|----------|
| **B1** | **Không reference CLAUDE.md format knowledge** | Anthropic standards được dùng nhưng YAML/XML/Token budget guidelines bị bỏ qua |
| **B2** | **validate_skill.py không validate FORMAT COMPLIANCE** | Script chỉ kiểm tra orphan files và placeholder density, KHÔNG kiểm tra XML/YAML format usage |
| **B3** | **SKILL.md output không enforce XML tags** | Dù CLAUDE.md yêu cầu `<instructions>`, `<context>`, skill output không tạo ra chúng |
| **B4** | **Không có token budget enforcement** | Không script/checklist để đảm bảo SKILL.md <500 lines, knowledge files có ToC khi >200 lines |

---

### 🟡 VẤN ĐỀ CẤP ĐỘ 3 (EXECUTION)

| # | Vấn đề | Chi tiết |
|---|---------|----------|
| **E1** | **Boot Sequence directive bị IGNORED** | Mệnh lệnh "CHỈ ĐỌC Tier 1" bị agent bỏ qua khi context quá nhỏ |
| **E2** | **No auto-discovery of missing references** | Agent KHÔNG phát hiện khi nó thiếu kiến thức - nó chỉ hallucinate |
| **E3** | **Gates không verify FORMAT** | Phase gates chỉ dừng cho user confirm, không verify format compliance |
| **E4** | **Build checklist không check FORMAT** | build-checklist.md chỉ verify structure, không verify format standards |

---

## 🔍 TEST EVIDENCE

Subagent test cho thấy:

```
Expected Format              | Found | Notes
─────────────────────────────────────────────────────
XML tags (<instructions>)   | ❌    | Skills use plain markdown
YAML constraint blocks       | ❌    | Only YAML frontmatter
Trace tags [TỪ DESIGN §N]   | ⚠️    | Planner uses, Architect didn't embed
Token budget guidance         | ❌    | Not specified anywhere
Progressive disclosure YAML   | ⚠️    | In frontmatter but not enforced
```

---

## 🛠️ GỢI Ý KHẮC PHỤC (PRIORITY ORDER)

### 1. **THÊM format knowledge vào skill suite** (Critical)
- Tạo `knowledge/format-standards.md` trong mỗi skill chứa nội dung từ CLAUDE.md section 3, 4, 10, 11, 12
- Hoặc: Add CLAUDE.md vào Tier 1 boot sequence của cả 3 skill

### 2. **TẠO format validator script** (High)
- `validate_format.py` - kiểm tra SKILL.md output có:
  - XML tags (`<instructions>`, `<context>`, `<examples>`, `<output_contract>`)
  - YAML blocks (`must:`, `must_not:`)
  - Token budget comments
  - Trace tags presence

### 3. **CẬP NHẬT build-checklist.md** (High)
- Thêm checklist items cho format compliance
- Thêm checklist items cho XML/YAML usage

### 4. **THÊM examples vào references/** (Medium)
- Tạo `references/examples/good-design.md` với đầy đủ format
- Tạo `references/examples/good-skill.md` với XML tags + YAML blocks
- Tạo `references/examples/good-todo.md` với proper trace tags

### 5. **ENFORCE Progressive Disclosure** (Medium)
- Thêm vào validate script: check rằng Tier 2 files CHỈ được reference từ đúng phase
- Reject SKILL.md nếu Tier 1 load >3 files

---

Anh yêu ơi, đây là phân tích toàn diện. Vấn đề cốt lõi là **format knowledge bị cô lập trong CLAUDE.md** mà KHÔNG được nhúng vào bộ 3 skill, dẫn đến agent không biết phải tạo ra format như thế nào. Có muốn em tạo task list để fix không?