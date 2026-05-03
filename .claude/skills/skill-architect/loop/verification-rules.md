# Verification Rules — Self-Check Before Delivery

> Skill Architect PHAI chay qua checklist nay truoc khi declare hoan thanh.
> Neu bat ky item nao [ ] → fix truoc khi deliver.

---

## Structure Verification

- [ ] §1 problem_statement: ro rang (Pain Point + Nguoi dung + Ly do)
- [ ] §2 capability_map: du 3 Pillars (Knowledge / Process / Guardrails)
- [ ] §3 zone_mapping: dung format chuan (co cot "Files can tao" voi ten file thuc)
- [ ] §4 folder_structure: co Mermaid mindmap, phan anh dung §3
- [ ] §5 execution_flow: co Mermaid sequence hoac flowchart
- [ ] §6 interaction_points: it nhat 1 diem tuong tac bat buoc
- [ ] §7 progressive_disclosure: phan biet ro Tier 1/2/3
- [ ] §8 risks: it nhat 3 risks kem mitigation cu the
- [ ] §9 open_questions: khong de trong (ghi "Khong co" neu da giai quyet het)
- [ ] §10 metadata: co skill-name, date, status
- [ ] §11 context_management: co token budget va compression strategy
- [ ] §12 verification_loop: co self-check procedure
- [ ] §13 error_recovery: co recovery procedures
- [ ] §14 agent_strength: co confidence scoring va CoT enforcement

---

## Diagram Verification

- [ ] D1 — Folder Structure (mindmap): co
- [ ] D2 — Execution Flow (sequenceDiagram): co
- [ ] D3 — Workflow Phases (flowchart LR): co
- [ ] Mermaid syntax hop le (khong loi render)
- [ ] Tat ca participant/node labels ngan gon, de doc
- [ ] Interaction points voi user duoc danh dau ro trong diagram

---

## Zone Mapping Contract Verification

- [ ] Moi Zone deu co gia tri trong cot "Files can tao" (khong de trong, khong placeholder)
- [ ] Zone khong dung → ghi "Khong can" (khong bo dong)
- [ ] Ten file cu the (vi du: `knowledge/uml-rules.md`, khong phai `knowledge/...`)
- [ ] Cot "Bat buoc?" dien dung ✅ hoac ❌

---

## AI Strength Verification (NEW v2.1)

- [ ] Confidence Score duoc tinh va >= 70
- [ ] Moi design decision co reasoning (Chain-of-Thought)
- [ ] Source trace cho moi claim trong knowledge
- [ ] Progressive Disclosure Plan co 3 tiers ro rang
- [ ] Token budget duoc specify
- [ ] Error recovery procedures duoc define
- [ ] Handoff contract day du cho Planner + Builder

---

## Handoff Readiness — Architect → Planner

- [ ] §3 Zone Mapping du thong tin de Planner decompose thanh Tasks
- [ ] §7 Progressive Disclosure Plan du de Builder biet files Tier 1/2/3
- [ ] §8 Risks du de Builder thiet lap Guardrails
- [ ] §9 Open Questions: items [CAN LAM RO] da duoc lam ro hoac ghi chu ro rang
- [ ] §12 Verification Rules du de Planner biet quality standards
- [ ] §13 Error Recovery du de Builder biet failure handling

---

## Process Gate Verification

- [ ] Phase 1 Gate: user da xac nhan §1 Problem Statement
- [ ] Phase 2 Gate: user da xac nhan §2+§3+§8 Analysis
- [ ] Phase 3 Gate: user da xac nhan toan bo design
- [ ] `init_context.py` da chay va tao `.skill-context/{skill-name}/`
- [ ] design.md da duoc ghi day du (khong con comment placeholder `<!-- -->`)

---

## Final Deliver Verification

- [ ] Khong co section nao con HTML comment `<!-- -->` chua duoc dien
- [ ] Tat ca ten file trong §3 khop voi §4 Folder Structure
- [ ] User da nhan thong bao "Buoc tiep theo: skill-planner"
- [ ] validate_design.py chay PASS (neu available)
