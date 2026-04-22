# Design Quality Checklist

> Skill Architect PHẢI chạy qua checklist này trước khi thông báo hoàn thành.
> Nếu bất kỳ item nào `[ ]` → sửa trước khi deliver.

---

## ✅ Structure Check — 10 Sections

- [ ] §1 Problem Statement: rõ ràng (Pain Point + Người dùng + Lý do)
- [ ] §2 Capability Map: đủ 3 Pillars (Knowledge / Process / Guardrails)
- [ ] §3 Zone Mapping: đúng format chuẩn (có cột "Files cần tạo" với tên file thực)
- [ ] §4 Folder Structure: có Mermaid mindmap, phản ánh đúng §3
- [ ] §5 Execution Flow: có Mermaid sequence hoặc flowchart
- [ ] §6 Interaction Points: ít nhất 1 điểm tương tác bắt buộc
- [ ] §7 Progressive Disclosure Plan: phân biệt rõ Tier 1 (mandatory) và Tier 2 (conditional)
- [ ] §8 Risks & Blind Spots: ít nhất 3 risks kèm mitigation cụ thể
- [ ] §9 Open Questions: không để trống (ghi "Không có" nếu đã giải quyết hết)
- [ ] §10 Metadata: có skill-name, date, status

---

## ✅ Diagram Check — Tối thiểu 3 sơ đồ Mermaid

- [ ] D1 — Folder Structure (mindmap): có
- [ ] D2 — Execution Flow (sequenceDiagram): có
- [ ] D3 — Workflow Phases (flowchart LR): có
- [ ] Mermaid syntax hợp lệ (không lỗi render — kiểm tra bằng mắt)
- [ ] Tất cả participant/node labels ngắn gọn, dễ đọc
- [ ] Interaction points với user được đánh dấu rõ trong diagram

---

## ✅ Zone Mapping Contract Check (§3)

- [ ] Mọi Zone đều có giá trị trong cột "Files cần tạo" (không để trống, không placeholder)
- [ ] Zone không dùng → ghi "Không cần" (không bỏ dòng)
- [ ] Tên file cụ thể (ví dụ: `knowledge/uml-rules.md`, không phải `knowledge/...`)
- [ ] Cột "Bắt buộc?" điền đúng ✅ hoặc ❌

---

## ✅ Handoff Readiness — Architect → Planner

- [ ] §3 Zone Mapping đủ thông tin để Planner decompose thành Tasks
- [ ] §7 Progressive Disclosure Plan đủ để Builder biết files Tier 1/2
- [ ] §8 Risks đủ để Builder thiết lập Guardrails
- [ ] §9 Open Questions: items `[CẦN LÀM RÕ]` đã được làm rõ hoặc ghi chú rõ ràng

---

## ✅ Process Gate Check

- [ ] Phase 1 Gate: user đã xác nhận §1 Problem Statement
- [ ] Phase 2 Gate: user đã xác nhận §2+§3+§8 Analysis
- [ ] Phase 3 Gate: user đã xác nhận toàn bộ design
- [ ] `init_context.py` đã chạy và tạo `.skill-context/{skill-name}/`
- [ ] design.md đã được ghi đầy đủ (không còn comment placeholder `<!-- -->`)

---

## ✅ Final Deliver Check

- [ ] Không có section nào còn HTML comment `<!-- -->` chưa được điền
- [ ] Tất cả tên file trong §3 khớp với §4 Folder Structure
- [ ] User đã nhận thông báo "Bước tiếp theo: skill-planner"
