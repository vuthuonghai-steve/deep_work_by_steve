# Heavy Thinking — The Inner Skill in Agentic Harnesses

## Nguồn gốc

**Paper:** HeavySkill: Heavy Thinking as the Inner Skill in Agentic Harness  
**arXiv:** [2605.02396](https://arxiv.org/abs/2605.02396) (4 May 2026)  
**Tác giả:** Jianing Wang, Linsen Guo, Zhengyu Chen et al. — Meituan LongCat  
**Repo:** [github.com/wjn1996/HeavySkill](https://github.com/wjn1996/HeavySkill) (Apache-2.0)

---

## Tóm tắt

Mọi agentic harness phức tạp (Claude Code, CodeX, Hermes, ...) thực ra đang che giấu **một kỹ năng nội tại đơn giản** gọi là **Heavy Thinking** — tư duy nặng.

Cơ chế cốt lõi chỉ có **2 giai đoạn**:

```
Input → [Stage 1: Parallel Reasoning] → [Stage 2: Deliberation] → Output
              K independent chains           Synthesize into
              of thought (K=8/16)            final answer
```

### Stage 1: Parallel Reasoning
- Model nhận bài toán q
- Sinh K luồng suy nghĩ độc lập (K = 8 hoặc 16)
- Mỗi luồng là một chain of thought riêng biệt

### Stage 2: Sequential Deliberation
- Tất cả K luồng được gói vào một **serialized memory cache**
- Model thứ 2 ("deliberator") đọc cache
- Deliberator tổng hợp và sinh đáp án cuối cùng

---

## Kết quả nổi bật

### Benchmarks

| Model | K | Benchmark | Single-shot | Heavy Mean |
|-------|---|-----------|-------------|------------|
| Kimi K2 Thinking | K=8 | AIME25 | ~80-90 | **100** |
| GLM 4.6 | K=8 | HMMT25-Feb | ~80-90 | **100** |
| DeepSeek V3.2 Thinking | K=16 | AIME25 | ~80-90 | **100** |
| Gemini 3 Pro Preview | K=8 | HMMT25-Feb | ~80-90 | **95.4** |

> Single-shot gốc của các model này chỉ đạt 80–90, Heavy Thinking đẩy lên **trần hoàn hảo**.

### Heavy Mean vs các chiến lược khác

- **Best-of-N (BoN):** chọn best từ N samples
- **Pass@N:** đạt được nếu bất kỳ sample nào đúng
- **Heavy Mean / Heavy Pass:** metric riêng của paper

Key finding: **stronger LLMs can even approach Pass@N performance** khi dùng Heavy Thinking.

---

## Phát hiện quan trọng (§4.2)

### Deliberator KHÔNG cần là model mạnh nhất

Thí nghiệm cố định parallel-stage là `R1-Distill-Qwen-7B`, rồi xoay vòng deliberation qua:

- R1-Distill-Qwen-7B
- R1-Distill-Qwen3-8B
- Qwen2.5-32B-Instruct

**Kết quả:** Qwen2.5-32B-Instruct (nổi tiếng yếu về tự suy luận) vẫn nâng Heavy Mean đáng kể khi đứng làm phase 2.

**Ý nghĩa:** Deliberator cần **khả năng tổng hợp và bám hướng dẫn**, không cần khả năng tự suy luận mạnh.

> ⚡️ Đảo ngược trực giác: "lấy model mạnh nhất làm model cuối" là sai.

---

## RLVR Scaling

**Reinforcement Learning with Verifiable Rewards** — học tăng cường có phần thưởng kiểm chứng được.

- Backbone: R1-Distill-Qwen-7B
- Heavy Mean cải thiện ~**10% chỉ trong 100 step đầu**

### Cảnh báo

| K | Stability | Notes |
|---|-----------|-------|
| K=8 | ✅ Ổn định | GRPO/GSPO hoạt động tốt |
| K=16 | ⚠️ Entropy collapse sau 100 step | Tín hiệu loãng đi |

> Càng song song không có nghĩa càng dễ huấn luyện — phần tín hiệu loãng đi.

---

## Production

### Đã ship

| System | Improvement | Notes |
|--------|-------------|-------|
| Kimi K2 Thinking — Heavy Mode | HLE: 44.9 → 51.0% | Live production |
| LongCat-Flash-Thinking-2601 | Same principle | Meituan internal |

### Chi phí

- **8–16x inference** cho mỗi câu trả lời
- Đường cong saturate nhanh: K > 20 chỉ thêm ~0.2%
- **Khuyến nghị:** chỉ bật Heavy Mode cho bài **cực khó** (math olympiad, hard code, HLE exam-style)
- Bài thường: **voting đơn giản đã hòa vốn**

---

## Skill Format

Toàn bộ workflow nén vào **1 file skill duy nhất** với 4 mục:

```yaml
# HeavySkill — 4-section skill
activation_conditions:  # Khi nào kích hoạt
parallel_reasoning_protocol:  # Cách sinh K luồng
deliberation_prompt:  # Cách model thứ 2 tổng hợp
output_constraints:  # Ràng buộc đầu ra
```

**Tương thích:** Claude Code, CodeX, Hermes, bất kỳ harness nào hỗ trợ skill — **không cần sửa code**.

---

## Supporting Models

- vLLM
- DeepSeek API
- Together AI
- OpenRouter
- Ollama

---

## Key Takeaways

1. **Heavy Thinking là inner skill** nội tại bên trong mọi agentic harness đắt tiền
2. **2-stage pipeline:** parallel reasoning → sequential deliberation
3. **Deliberator không cần mạnh** — cần khả năng tổng hợp
4. **RLVR scaling được** — nhưng K=8 bền hơn K=16
5. **Cost/benefit:** chỉ dùng cho bài khó, bài dễ dùng voting

---

## Liên quan

- [Agentic Harnesses](./agent-harnesses.md) — tổng quan các framework đang cạnh tranh
- [Agentic Memory](../agentic-memory.md) — so sánh cách các harness xử lý memory
