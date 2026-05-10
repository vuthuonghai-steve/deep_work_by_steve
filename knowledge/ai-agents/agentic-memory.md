# Agentic Memory — So sánh cách các Harness xử lý Memory

## Bối cảnh

**Liên quan:** HeavySkill paper (arXiv:2605.02396) — phần serialized memory cache

Memory là một trong những thành phần cốt lõi của agentic harness. HeavySkill chỉ ra rằng memory cache chỉ là **input cho deliberation stage**, không phải cơ chế đẩy performance chính.

---

## Memory trong các Harness

### Hermes — Persistent Memory

**Đặc điểm:**
- Memory persisitent qua sessions
- Lưu user preferences, facts, conventions
- Dùng `memory` tool để add/replace/remove
- Injection vào system prompt mỗi turn

**Ưu điểm:**
- Contextual understanding qua thời gian
- Giảm repeated corrections
- Personalization theo user

**Hạn chế:**
- Memory size growth → context pollution
- Entropy tăng theo thời gian
- Không rõ mechanism nào thực sự drive performance

### Claude Code — Skills-based Memory

**Đặc điểm:**
- Knowledge nằm trong skill files
- Declarative facts, không phải episodic memory
- Skills được load khi cần

**Ưu điểm:**
- Modular, có thể share
- Declarative → dễ debug
- No context pollution

**Hạn chế:**
- Static — không adapt theo session

### CodeX — Sub-agent Memory

**Đặc điểm:**
- Mỗi sub-agent có memory riêng
- Inter-agent memory sharing qua shared context

**Ưu điểm:**
- Parallelism
- Specialization

**Hạn chế:**
- Memory fragmentation
- Coordination overhead

---

## HeavySkill Perspective

HeavySkill bóc tách:

```
Memory trong orchestration ≠ Memory trong Heavy Thinking
```

### Serialized Memory Cache (HeavySkill)

Trong HeavySkill, **memory cache** là output của Stage 1 (Parallel Reasoning):

```
Stage 1 Output = K independent chains of thought
                     ↓
              Serialized into
              Memory Cache
                     ↓
              Stage 2 Input
```

**Đặc điểm:**
- Memory là **structured input**, không phải persistent storage
- K luồng được gói tuần tự vào cache
- Deliberator đọc cache như một document

**Khác biệt cốt lõi:**

| Aspect | Orchestration Memory | HeavySkill Cache |
|--------|---------------------|------------------|
| Purpose | Store facts, preferences | Bundle reasoning traces |
| Lifetime | Cross-session | Per-query |
| Content | Facts, conventions | K chains of thought |
| Reader | Same agent | Deliberator model |

---

## Key Insight

> Memory phức tạp trong Hermes/Claude Code/CodeX giúp **orchestration** và **user experience**, nhưng **performance gain thực sự** đến từ Heavy Thinking — parallel reasoning → deliberation.

Nghĩa là:
1. Memory tốt = orchestration tốt hơn
2. Nhưng orchestration tốt ≠ reasoning tốt hơn
3. Reasoning tốt hơn cần **Heavy Thinking mechanism**

---

## Tham khảo

- [Heavy Thinking](./ai-agents/heavy-thinking.md) — chi tiết 2-stage pipeline
- [Agentic Harnesses](./ai-agents/agent-harnesses.md) — so sánh các harness
