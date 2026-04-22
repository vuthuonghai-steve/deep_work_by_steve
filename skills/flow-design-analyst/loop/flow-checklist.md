# Flow Diagram Checklist — 6 Điểm Kiểm Tra Bắt Buộc

> **Usage**: Đọc bắt buộc (Tầng 1) tại Phase 5 VALIDATE. Thực hiện 6-point check TRƯỚC khi trình bày diagram cho user (Gate 3).
> **Rule**: Nếu fail bất kỳ điểm nào → quay lại Phase 3 hoặc 4 tương ứng để sửa, KHÔNG được output diagram chưa pass.

---

## Hướng dẫn sử dụng

Với mỗi diagram đã sinh xong:
1. Đọc qua toàn bộ Mermaid code.
2. Check từng điểm C1–C6 theo thứ tự.
3. Tick `[x]` chỉ khi điểm đó **thực sự PASS** — không được tick trước khi kiểm tra.
4. Nếu bất kỳ điểm nào chưa pass → đọc cột "Hành động khi Fail" và sửa ngay.
5. Khi đủ 6/6 → tiến hành Gate 3.

---

## Checklist

### C1 — Lane Discipline ✅ / ❌

**Tiêu chí**: Mọi node đặt đúng lane theo `knowledge/actor-lane-taxonomy.md`.

| Câu hỏi kiểm tra | Trả lời |
|-----------------|---------|
| Tất cả thao tác UI của user nằm trong `subgraph User`? | Yes / No |
| Tất cả business logic, validation, external API call nằm trong `subgraph System`? | Yes / No |
| Tất cả SELECT/INSERT/UPDATE/DELETE nằm trong `subgraph DB`? | Yes / No |
| Không có DB operation nào trong System Lane? | Yes / No |
| Không có System logic nào trong User Lane? | Yes / No |

**Hành động khi Fail**:
- Mở `knowledge/actor-lane-taxonomy.md` §2 (Decision Table).
- Xác định node nào đặt sai lane.
- Di chuyển node sang đúng subgraph.
- Cập nhật connections tương ứng.

---

### C2 — Decision Completeness ✅ / ❌

**Tiêu chí**: Mọi `{}` diamond có ≥ 2 nhánh output, mỗi nhánh có label rõ ràng.

| Câu hỏi kiểm tra | Trả lời |
|-----------------|---------|
| Tất cả node `{}` có ít nhất 2 mũi tên ra không? | Yes / No |
| Mỗi mũi tên ra từ `{}` có label (dùng `-- "label" -->`)? | Yes / No |
| Không có `{}` node nào chỉ có 1 nhánh output (dangling decision)? | Yes / No |
| Label nhánh đủ rõ để hiểu logic? (e.g., "Hợp lệ"/"Không hợp lệ", "Tìm thấy"/"Không tìm thấy") | Yes / No |

**Hành động khi Fail**:
- Tìm diamond `{}` có ít hơn 2 mũi tên ra.
- Thêm nhánh còn thiếu (exception path nếu chưa có).
- Đặt label rõ ràng cho mỗi nhánh.
- Tham khảo `knowledge/business-flow-patterns.md §3` (Exception Path patterns).

---

### C3 — Path Termination ✅ / ❌

**Tiêu chí**: Mọi nhánh trong flow kết thúc bằng `(["✅ End"])` hoặc endpoint có tên rõ ràng.

| Câu hỏi kiểm tra | Trả lời |
|-----------------|---------|
| Mọi success path kết thúc bằng success endpoint rõ ràng? | Yes / No |
| Mọi exception/error path kết thúc bằng error endpoint rõ ràng? | Yes / No |
| Không có node nào là "dead end" (không có mũi tên ra VÀ không phải terminal node)? | Yes / No |
| Stadium node `(["..."])` được dùng cho Start/End nodes? | Yes / No |

**Hành động khi Fail**:
- Trace từng nhánh Diamond node đến cuối.
- Tìm nhánh không có terminal node.
- Thêm End node: `U_end(["✅ [Mô tả kết quả]"])` hoặc `U_err(["❌ [Mô tả lỗi"])`
- Kết nối nhánh thiếu vào End node tương ứng.

---

### C4 — Traceability ✅ / ❌

**Tiêu chí**: Mọi Action Node chính có comment `%% UC-ID %%` hoặc ghi rõ nguồn trong metadata.

| Câu hỏi kiểm tra | Trả lời |
|-----------------|---------|
| Comment `%% UC-ID: [ID] %%` có ở đầu diagram? | Yes / No |
| Comment `%% Business Function: [name] %%` có ở đầu diagram? | Yes / No |
| Tên file output dùng đúng pattern `flow-{business-function}.md`? | Yes / No |
| Có thể truy vết ngược từ diagram về UC trong `data/uc-id-registry.yaml`? | Yes / No |

**Hành động khi Fail**:
- Mở `data/uc-id-registry.yaml`.
- Tìm UC-ID tương ứng với flow đang vẽ.
- Thêm metadata comments vào đầu diagram:
  ```
  %% UC-ID: UC01
  %% Business Function: user-registration
  %% Generated: 2026-02-XX
  ```

---

### C5 — Assumptions Documented ✅ / ❌

**Tiêu chí**: Nếu có logic suy luận (không có trong spec/US) → có section `## Assumptions` bên dưới sơ đồ.

| Câu hỏi kiểm tra | Trả lời |
|-----------------|---------|
| Flow có bất kỳ bước nào không có trong spec hoặc US không? | Yes / No |
| Nếu Yes ở trên: có section `## ⚠️ Assumptions` bên dưới diagram? | Yes / No (N/A nếu No ở trên) |
| Mỗi assumption được liệt kê cụ thể (không phải chung chung)? | Yes / No (N/A) |
| Assumptions được đánh số và có giải thích ngắn? | Yes / No (N/A) |

**Hành động khi Fail**:
- Review lại từng step trong diagram.
- Với bước nào không có nguồn rõ ràng trong spec → ghi vào Assumptions.
- Format chuẩn:

```markdown
## ⚠️ Assumptions (Thông tin suy luận — chưa có trong spec)

1. **Trigger**: Spec chưa mô tả rõ. Giả định: "Member nhấn icon Bookmark trên PostCard."
2. **Precondition**: Giả định: "Member đã đăng nhập (JWT hợp lệ)."
3. **Error handling**: Giả định server trả 500 khi DB fail — spec chưa mô tả.

> ⚠️ Cần Steve review và xác nhận trước khi finalize.
```

---

### C6 — Mermaid Syntax Valid ✅ / ❌

**Tiêu chí**: Không có ký tự unsafe, label dùng `""`, không dùng `\n`, không có dangling node.

| Câu hỏi kiểm tra | Trả lời |
|-----------------|---------|
| Tất cả label > 1 từ được wrap trong `""`? | Yes / No |
| Không có `\n` trong bất kỳ label nào (dùng `<br/>` thay thế)? | Yes / No |
| Tất cả Node ID chỉ dùng `a-z, A-Z, 0-9, _`? | Yes / No |
| Tất cả subgraph label được wrap trong `""`? (e.g., `subgraph User ["👤 User"]`) | Yes / No |
| Từ `end` trong label được wrap trong `""`? | Yes / No |
| Không có node nào khai báo nhưng không có edge (orphan node)? | Yes / No |
| Ký tự đặc biệt (`(`, `)`, `{`, `}`, `:`, `/`, `?`) trong label đều trong `""`? | Yes / No |

**Hành động khi Fail**:
- Scan qua toàn bộ Mermaid code.
- Fix từng vi phạm:
  - Label chưa quote → thêm `""`
  - `\n` → thay bằng `<br/>`
  - Node ID có dấu `-` → thay bằng `_`
  - Subgraph label chưa quote → thêm `""`
- Tham khảo `knowledge/mermaid-flowchart-guide.md §4` (Safe Label Rules).
- Nếu diagram > 15 nodes: chạy `scripts/flow_lint.py` để tự động detect.

---

## Tóm tắt — Quick Reference

| # | Check | Nếu Fail → Goto |
|---|-------|-----------------|
| **C1** | Lane Discipline | actor-lane-taxonomy.md §2 → Phase 3 STRUCTURE |
| **C2** | Decision Completeness | business-flow-patterns.md §3 → Phase 4 GENERATE |
| **C3** | Path Termination | Thêm End nodes → Phase 4 GENERATE |
| **C4** | Traceability | uc-id-registry.yaml → Phase 4 GENERATE (metadata) |
| **C5** | Assumptions |  Viết `## Assumptions` section → Phase 4 GENERATE |
| **C6** | Mermaid Syntax | mermaid-flowchart-guide.md §4 → Phase 4 GENERATE |

**Pass 6/6** → Tiến hành **Gate 3**: Trình bày bản nháp cho user review.
