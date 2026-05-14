# Heavy Thinking Tree — 5 Layers Plan

## Layer 0: Gốc — What / How / Why
- Q0.1: Heavy Thinking là gì?
- Q0.2: Nó giải quyết bài toán nào? (tại sao single-shot không đủ)
- Q0.3: Nó giải quyết như thế nào? (2-stage pipeline)
- Q0.4: Tại sao nó lại giải quyết được? (tại sao parallel + deliberation hiệu quả)

## Layer 1: Đào sâu từ Layer 0
### Từ Q0.1 (What is it)
- Q1.1a: Parallel Reasoning là gì chính xác?
- Q1.1b: Deliberation là gì chính xác?

### Từ Q0.2 (What problem)
- Q1.2a: Tại sao single-shot reasoning thất bại trên bài khó?
- Q1.2b: Best-of-N và Voting khác Heavy Thinking chỗ nào?

### Từ Q0.3 (How)
- Q1.3a: K=8 hay K=16? Khác nhau thế nào?
- Q1.3b: Serialized memory cache là gì?

### Từ Q0.4 (Why)
- Q1.4a: Tại sao deliberator không cần là model mạnh nhất?
- Q1.4b: Tại sao cần K luồng độc lập, không phải 1 luồng dài?

## Layer 2: Cơ chế chi tiết
- Q2.1: Entropy trong reasoning chains là gì?
- Q2.2: Tại sao K=16 bị entropy collapse sau 100 step RL?
- Q2.3: GRPO/GSPO là gì trong ngữ cảnh RLVR?
- Q2.4: Heavy Mean vs Heavy Pass vs Pass@N khác nhau thế nào?

## Layer 3: RLVR và Training
- Q3.1: RLVR (Reinforcement Learning with Verifiable Rewards) hoạt động thế nào?
- Q3.2: Tại sao K=8 ổn định hơn K=16 trong RLVR?
- Q3.3: Skill format 4 phần là gì? (Activation Conditions, Parallel Reasoning Protocol, Deliberation Prompt, Output Constraints)

## Layer 4: Production & Limitations
- Q4.1: Khi nào nên dùng Heavy Thinking, khi nào dùng voting đơn giản?
- Q4.2: Đường cong saturate của K là gì? Tại sao K>20 chỉ thêm 0.2%?
- Q4.3: Chi phí 8-16x inference có đáng không?
- Q4.4: HeavySkill repo hỗ trợ những engine nào?

---

## Research với Codex
Mỗi tầng cần research web để lấy thông tin bổ sung từ:
- Paper gốc arXiv:2605.02396
- github.com/wjn1996/HeavySkill
- Các blog posts, explanations về heavy thinking
