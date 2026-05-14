# Agentic Harnesses — Tổng quan

## Bối cảnh

**Nguồn:** Bài post Codex VN, tháng 5/2026  
**Liên quan:** HeavySkill paper (arXiv:2605.02396)

---

## Vấn đề

Cả ngành đua nhau xếp lego — mỗi harness tự xây orchestration framework riêng:

- **Claude Code** — chia kỹ năng thành file, gọi sub-agents
- **CodeX** — gọi sub-agents có chiến lược
- **Hermes** — nhồi memory phức tạp, nhiều tầng

Câu hỏi không ai trả lời thẳng: **Phần nào thực sự đẩy hiệu năng?**

---

## Phân tích qua lăng kính HeavySkill

HeavySkill paper bóc tách sự thật: tất cả các harness đắt tiền đang bí mật dựa vào **cùng một kỹ năng nội tại** — Heavy Thinking.

```
┌─────────────────────────────────────────────────┐
│              Agentic Harness                     │
│  ┌─────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Skills  │  │  Memory   │  │  Sub-agents    │  │
│  └────┬────┘  └────┬─────┘  └───────┬────────┘  │
│       │             │                │           │
│       └──────────┬──┴────────────────┘           │
│                    ▼                              │
│            ┌───────────────┐                      │
│            │ Heavy Thinking │  ← INNER SKILL    │
│            │  (2-stage)     │                    │
│            └───────────────┘                      │
└─────────────────────────────────────────────────┘
```

---

## So sánh các Harness

### Claude Code

- **Đặc điểm:** Skills chia thành file, mỗi skill là đơn vị nhỏ
- **Điểm mạnh:** Tái sử dụng tốt, portable
- **Liên quan Heavy Thinking:** Load được HeavySkill file

### CodeX

- **Đặc điểm:** Gọi sub-agents có chiến lược, parallel execution
- **Điểm mạnh:** Multi-agent orchestration
- **Liên quan Heavy Thinking:** Parallel reasoning stage

### Hermes

- **Đặc điểm:** Memory phức tạp, nhiều tầng
- **Điểm mạnh:** Contextual memory, cross-session
- **Liên quan Heavy Thinking:** Serialized memory cache (stage 2 input)

---

## Chiến lược để performance

| Strategy | Mô tả | Hạn chế |
|----------|--------|----------|
| Single-shot | 1 lần suy luận | Yếu trên bài khó |
| Best-of-N (BoN) | Chọn best từ N samples | Không tổng hợp |
| Voting | Majority vote từ N samples | Không có reasoning |
| **Heavy Thinking** | Parallel + Deliberation | 8-16x cost |

---

## Lý thuyết nền

### Inner Skill vs Orchestration

**Orchestration layer** (skills, memory, sub-agents) là vỏ bọc bên ngoài.

**Inner skill** (Heavy Thinking) là cơ chế thực sự đẩy performance.

> Orchestration giúp quản lý complexity, nhưng **performance gain đến từ inner skill**.

### Tại sao harness phức tạp?

1. **Tính reusable** — skills có thể share giữa các task
2. **Maintainability** — modular, dễ debug
3. **User experience** — developer quen với paradigm này
4. **Marketing** — "nhiều tầng" nghe có vẻ mạnh

Nhưng về mặt performance, heavy thinking có thể đứng **bên dưới bất kỳ harness nào**.

---

## Khi nào dùng Heavy Thinking

### Nên dùng (bài khó)

- Math olympiad (AIME, HMMT)
- Hard coding (competitive programming)
- Exam-style HLE (Humanity's Last Exam)
- Tasks mà single-shot thường rớt

### Không cần (bài dễ)

- Simple QA
- Basic generation
- Tasks mà single-shot đã đạt >95%

---

## Chi phí

| Strategy | Inference cost | Quality gain |
|----------|---------------|--------------|
| Single-shot | 1x | baseline |
| Voting (N=8) | 8x | modest |
| Heavy (K=8) | 8x | significant |
| Heavy (K=16) | 16x | near-ceiling |

**Đường cong saturate:** K > 20 chỉ thêm ~0.2%

---

## Tham khảo

- [Heavy Thinking](./heavy-thinking.md) — chi tiết inner skill
- [Agentic Memory](../agentic-memory.md) — memory trong các harness
