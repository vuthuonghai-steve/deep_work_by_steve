# AI Agents — AI-First Knowledge Base

> **Source:** HeavySkill Paper — arXiv:2605.02396 (Meituan LongCat, May 2026)

---

## CORE: LLM Xử Lý Thông Tin Như Thế Nào

```
USER INPUT
    │
    ▼
[1] PARALLEL REASONING — K chains độc lập
    │   Mỗi chain = 1 cách tiếp cận khác nhau
    │
    ▼
[2] MEMORY CACHE — Kết hợp K chains
    │   Đóng gói thành input cho stage tiếp
    │
    ▼
[3] DELIBERATION — Model thứ 2 tổng hợp
    │   Phân tích, chọn lọc, tạo output cuối
    │
    ▼
FINAL OUTPUT
```

---

## 1. SINGLE-SHOT THẤT BẠI — TẠI SAO

| Vấn đề | Giải thích |
|---------|------------|
| Confirmation Bias | Đi theo hướng đầu, bám vào đó dù sai |
| Error Cascade | Sai step 1 → sai tất cả steps sau |
| Local Optimum | Mắc kẹt ở một hướng, không thấy hướng khác |
| No Self-Correction | Không có bước review lại |

---

## 2. HEAVY THINKING = "NGHĩ NHIỀU LẦN, THEO NHIỀU HƯỚNG"

**2-Stage Pipeline:**

```
Stage 1: PARALLEL REASONING
├── Sinh K chains độc lập (K = 8 hoặc 16)
├── Mỗi chain = 1 method khác nhau
└── Không thấy output của chain khác

Stage 2: DELIBERATION
├── Model thứ 2 đọc tất cả K chains
├── Phân tích reasoning quality
├── Tổng hợp → Final Answer
```

---

## 3. DELIBERATION ≠ VOTING

**Voting:** Đếm số lần xuất hiện → chọn majority
**Deliberation:** Phân tích CHẤT LƯỢNG reasoning → chọn đúng

```
Ví dụ:
Chain 1: X (step 3 có lỗi)
Chain 2: X (confirmed)
Chain 3: Y (logic đúng)

Voting → X (2/3)
Deliberation → Y (vì X có lỗi ở step 3)
```

**Majority ≠ Correct**

---

## 4. K INDEPENDENT CHAINS > 1 LONG CHAIN

| 1 Long Chain | K Independent Chains |
|-------------|---------------------|
| Confirmation bias escalation | Independence |
| Single starting point | K starting points |
| Error cascade | Error isolation |
| Path stagnation | Multiple paths |

---

## 5. DELIBERATOR KHÔNG CẦN MẠNH NHẤT

**Cần:** Tổng hợp + Bám hướng dẫn + Phân tích phê bình

**Không cần:** Tự suy luận mạnh (job của parallel stage)

> ⚡ "Lấy model mạnh nhất làm cuối" = SAI

---

## 6. K=8 LÀ SWEET SPOT

| K | Cost | Quality | RLVR Stability |
|---|------|---------|----------------|
| 8 | 8x | ~95-100% | ✅ Stable |
| 16 | 16x | ~100% | ❌ Entropy collapse |

K > 20 → chỉ thêm ~0.2%

---

## 7. KHI NÀO DÙNG

| Task | Approach |
|------|----------|
| Easy (>95% single-shot) | Single-shot |
| Medium (85-95%) | Voting |
| Hard (<85%) | Heavy Thinking |
| Extreme (<50%) | Heavy (K=8+) |

---

## 8. KEY INSIGHTS

1. **Heavy Thinking là inner skill** — bên trong mọi agentic harness
2. **Orchestration ≠ Performance** — skills/memory/sub-agents chỉ quản lý complexity
3. **Parallel + Deliberation** — cơ chế thực sự đẩy LLM output
4. **Partial correctness** — super power của deliberation: tạo answer hoàn chỉnh từ K chains đều sai một phần
5. **Diversity > Length** — nhiều chains độc lập tốt hơn 1 chain dài

---

## LIÊN QUAN

- **Paper:** arXiv:2605.02396
- **Repo:** github.com/wjn1996/HeavySkill
