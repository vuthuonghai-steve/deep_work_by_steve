# Heavy Thinking — Binary Tree Q&A
## 5 Layers · 31 Nodes · Hiểu sâu bản chất qua cấu trúc cây nhị phân

> **Nguồn:** HeavySkill Paper — arXiv:2605.02396 (Meituan LongCat, 4 May 2026)  
> **Repo:** [github.com/wjn1996/HeavySkill](https://github.com/wjn1996/HeavySkill)

---

```
TREE STRUCTURE — 5 LAYERS, 31 NODES

Layer 0 (Root)                    ── NODE #1
        │
        ├── NODE #2 ── NODE #3    ── Layer 1 (2 nodes)
        │           │
        │    ┌──────┴──────┐
        │    │             │
      NODE #4 ── NODE #5  NODE #6 ── NODE #7    ── Layer 2 (4 nodes)
        │        │            │          │
     ┌──┴──┐  ┌──┴──┐     ┌──┴──┐   ┌──┴──┐
   NODE#8 #9 #10  #11    #12  #13  #14  #15    ── Layer 3 (8 nodes)
     │ │   │ │   │  │     │   │    │   │
   ┌┬┐┌┴┐┌┐┌┴┐┌┐┌┐   ┌┴┐┌┐┌┐┌┐┌┐
  #16#17#18#19#20#21#22  #23#24#25#26#27#28#29#30#31  ── Layer 4 (16 leaf nodes)
```

---

# LAYER 0 — ROOT NODE #1

## ⚡ NODE #1 — ROOT

### ❓ Q: Heavy Thinking LÀ GÌ?

### ✅ A:

**Heavy Thinking** là một **inner skill** (kỹ năng nội tại) trong LLMs, được định nghĩa trong paper HeavySkill như sau:

> *"HeavySkill views heavy thinking not only as a minimal execution unit in orchestration harness but also as an inner skill internalized within the model's parameters."*

Nói đơn giản: Heavy Thinking = **nghĩ nhiều lần, theo nhiều hướng, rồi tổng hợp lại**.

### Cơ chế cốt lõi: **2-stage pipeline**

```
Input (Problem q)
        │
        ▼
┌─────────────────────────────────┐
│  STAGE 1: PARALLEL REASONING    │
│  Sinh K luồng suy nghĩ ĐỘC LẬP│
│  (K = 8 hoặc 16)              │
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│  SERIALIZED MEMORY CACHE        │
│  K luồng được gói tuần tự      │
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│  STAGE 2: SEQUENTIAL            │
│  DELIBERATION                   │
│  Model thứ 2 đọc cache         │
│  → Tổng hợp → Đáp án CUỐI   │
└─────────────────────────────────┘
```

### Đặc điểm quan trọng

| Đặc điểm | Giải thích |
|-----------|-----------|
| **Inner skill** | Không phải orchestration bên ngoài, mà nằm trong mechanism |
| **2-stage** | Stage 1: parallel K chains → Stage 2: deliberation |
| **No extra training** | Hoạt động với bất kỳ LLM nào, không cần fine-tune |
| **Heavy** | Nặng về computation (8-16x) nhưng đáng giá |

---

# LAYER 1 — NODES #2 & #3

## ⚡ NODE #2

### ❓ Q: **PARALLEL REASONING** là gì? Tại sao nó cần thiết?

### ✅ A:

**Parallel Reasoning** là Stage 1 của Heavy Thinking — sinh **K independent reasoning trajectories** cho cùng một bài toán.

### Cách hoạt động

```
Bài toán q
    │
    ▼
┌──────────────────────────────────────────┐
│  Spawn K = 8 (hoặc 16) agents           │
│                                          │
│  Agent 1: "Solve q step by step" ──→ T₁│
│  Agent 2: "Solve q step by step" ──→ T₂│
│  Agent 3: "Solve q step by step" ──→ T₃│
│  ...                                     │
│  Agent K: "Solve q step by step" ──→ Tₖ│
│                                          │
│  Mỗi agent suy nghĩ ĐỘC LẬP            │
│  Không thấy output của agent khác        │
└──────────────────────────────────────────┘
```

### Tại sao cần thiết?

**1. Giải quyết Confirmation Bias**

Single-shot đi theo hướng đầu và bám vào đó. Nếu sai → cả đường sai.

K chains độc lập → Chain 1 sai ≠ Chain 2 sai.

**2. Tránh Local Optimum Trap**

Single-shot dễ bị mắc kẹt ở một optimum cục bộ.

K chains đồng thời tìm kiếm nhiều optimum → deliberator chọn global optimum.

**3. Diversity of Approaches**

Một bài toán có thể giải bằng nhiều cách: algebraic, geometric, brute force, elegant proof.

K chains thử K cách đồng thời.

**4. Isolation prevents Error Cascade**

Trong single-shot: sai ở step 1 → sai ở step 2 → ... → sai cuối.

K chains: Chain 1 sai ở step 2 → Chain 2 không bị ảnh hưởng.

---

## ⚡ NODE #3

### ❓ Q: **DELIBERATION** là gì? Nó khác Voting chỗ nào?

### ✅ A:

**Deliberation** là Stage 2 của Heavy Thinking — model thứ 2 ("deliberator") đọc K trajectories và **tổng hợp** thành đáp án cuối cùng.

### Cách hoạt động

```
Serialized Memory Cache (K trajectories)
    │
    │ T₁: "Method A → Answer X"
    │ T₂: "Method B → Answer Y"
    │ T₃: "Method A again → Answer X"
    │ ...
    │ Tₖ: "Method C → Answer Z"
    ▼
┌──────────────────────────────────────────┐
│  DELIBERATOR MODEL                       │
│                                          │
│  1. Identify answer distribution         │
│  2. Analyze reasoning quality            │
│  3. Cross-validate approaches           │
│  4. Critical evaluation (majority≠right) │
│  5. Synthesize final answer              │
└──────────────────────────────────────────┘
    │
    ▼
Final Answer
```

### Deliberation ≠ Voting — Sự khác biệt cốt lõi

**Voting:**
```
Chain 1: X
Chain 2: X
Chain 3: Y
Chain 4: X
→ Majority = X
→ Output: X
→ Chỉ ĐẾM, không PHÂN TÍCH
```

**Deliberation:**
```
Chain 1: X (method A, step 3 có vấn đề)
Chain 2: X (method A, confirmed)
Chain 3: Y (method B, logic sound)
Chain 4: X (method A, nhưng step 2 uncertain)

Deliberator:
→ Chains 1,2,4 cùng method A nhưng step 3 có lỗi nghiêm trọng
→ Chain 3 (Y) tuy minority nhưng logic đúng
→ Output: Y (minority nhưng đúng)
```

### Tại sao Majority không đồng nghĩa đúng?

| Trường hợp | Vấn đề |
|------------|--------|
| Systematic bias | Cả K chains dùng cùng method sai |
| Confidence ≠ Correctness | Tự tin ≠ Đúng |
| Partial correctness | Mỗi chain đúng một phần |

---

# LAYER 2 — NODES #4, #5, #6, #7

## ⚡ NODE #4

### ❓ Q: Tại sao cần **K INDEPENDENT CHAINS**? Không phải 1 long chain?

### ✅ A:

**K independent chains** không phải "nhiều hơn" mà là "đa dạng hơn" — và đa dạng là cốt lõi.

### 1 Long Chain vs K Independent Chains

**Giả thuyết sai:** "Tăng độ dài single-shot = same effect"

**Thực tế:** KHÔNG. Extending 1 chain ≠ K parallel chains.

### Tại sao K chains > 1 Long Chain?

| Vấn đề của 1 Long Chain | K Chains giải quyết |
|-------------------------|---------------------|
| Confirmation bias escalation | Independence — không build trên sai |
| Single starting point | K starting points — đa dạng |
| Error accumulation | Error isolation — chain sai ≠ khác sai |
| Path stagnation | Multiple paths — không bị stuck |

### Cụ thể

```
1 Long Chain:
A → B → C → D → E → F → G → H (sai ở B)

K Independent Chains:
Chain 1: A₁ → B₁ → ... → Answer₁ (sai ở B₁)
Chain 2: A₂ → B₂ → ... → Answer₂ (đúng!)
Chain 3: A₃ → B₃ → ... → Answer₃ (đúng, cách khác)

→ Deliberator thấy có chain đúng → chọn Answer₂ hoặc Answer₃
```

---

## ⚡ NODE #5

### ❓ Q: **SERIALIZED MEMORY CACHE** là gì? Nó hoạt động thế nào?

### ✅ A:

**Memory Cache** = cách đóng gói K trajectories từ Stage 1 để input vào Stage 2.

### Bản chất

Memory Cache trong HeavySkill **KHÔNG phải** sophisticated memory system (như Hermes persistent memory). Nó đơn giản là **concatenation of all K trajectories**.

### Cấu trúc

```
Thinker #1: {trajectory_1}
---
Thinker #2: {trajectory_2}
---
...
Thinker #K: {trajectory_K}
```

### Ví dụ

**Problem:** Tính tổng 1 đến 100

```
Serialized Memory Cache:

Thinker #1: Using formula: n(n+1)/2 = 100(101)/2 = 5050
---
Thinker #2: 1+2+3+...+100 = 5050 (calculated step by step)
---
Thinker #3: Using Python: sum(range(1,101)) = 5050
```

### Implementation (từ repo)

```python
# memory_cache.py (HeavySkill repo)
class MemoryCache:
    def serialize(self, trajectories: List[str]) -> str:
        cache = ""
        for i, traj in enumerate(trajectories, 1):
            cache += f"Thinker #{i}: {traj}\n"
            cache += "---\n"
        return cache
```

### Tại sao không dùng fancy memory?

| Aspetto | HeavySkill Cache | Hermes Memory |
|---------|-----------------|---------------|
| Purpose | Bundle K reasoning traces | Store facts across sessions |
| Lifetime | Per-query | Cross-session |
| Complexity | Simple concatenation | Complex structured storage |

**Key:** Memory cache chỉ là **passing mechanism** — cách đưa K outputs từ Stage 1 vào Stage 2.

---

## ⚡ NODE #6

### ❓ Q: **GRPO và GSPO** là gì? Cách chúng hoạt động trong Heavy Thinking RLVR?

### ✅ A:

**GRPO** = Group Relative Policy Optimization  
**GSPO** = Group Sampling Policy Optimization

Đây là các **RL algorithms** được dùng để train Heavy Thinking qua RLVR.

### GRPO — Chi tiết

**Đặc điểm chính:**
- Không cần critic/value network (như PPO)
- So sánh tương đối trong group
- Dùng cho tasks với verifiable rewards (đúng/sai)

### GRPO trong Heavy Thinking RLVR

```
Problem q
    │
    ▼
Generate K=8 trajectories (policy πθ)
    │
    ▼
Deliberation → Final answer
    │
    ▼
Reward: r = 1 if correct, 0 if incorrect
    │
    ▼
Update policy dựa trên relative ranking trong K
```

### Advantage Calculation

```
A_i (advantage của trajectory i) = r_i - mean(r)

Hoặc dùng relative ranking:
A_i = rank(reward_i) / K
```

### Tại sao K=8 tốt cho GRPO?

| K | Group homogeneity | Advantage estimation | Training |
|---|-----------------|---------------------|----------|
| K=8 | ~Optimal | Reliable | ✅ Stable |
| K=16 | Too heterogeneous | Noisy | ❌ Collapse |

K=16 → group quá đa dạng → advantage estimation noisy → unstable.

### RLVR Training Loop

```
1. Sample K=8 trajectories cho batch of problems
2. Each problem: deliberation → reward r ∈ {0,1}
3. Compute advantage: A_i = r_i - mean(r)
4. GRPO update: L = -Σ log π(a_i) × A_i
5. Repeat

→ After ~100 steps: Heavy Mean improves ~10%
```

---

## ⚡ NODE #7

### ❓ Q: **ENTROPY** trong reasoning chains là gì? Tại sao nó quan trọng?

### ✅ A:

**Entropy** = mức độ **đa dạng/không chắc chắn** của các reasoning traces.

```
HIGH Entropy = K chains rất khác nhau, nhiều cách tiếp cận
LOW Entropy  = K chains giống nhau, cùng kết quả
```

### Entropy trong Heavy Thinking

```
Parallel Reasoning Output (HIGH Entropy):
Chain 1: "Method A → Answer X"
Chain 2: "Method B → Answer Y"
Chain 3: "Method C → Answer Z"
→ 3 methods, 3 answers
→ ENTROPY: HIGH

After Deliberation (LOW Entropy):
Final Answer: Y
→ ENTROPY: LOW (converged)
```

### Tại sao Entropy quan trọng?

**RLVR cần entropy để học:**
- K chains cùng answer → không diversity → không có gì để học
- K chains khác nhau → học được pattern nào đúng/sai

### Entropy Collapse — K=16

```
Initial (K=16):
- Chains 1-5: method A
- Chains 6-10: method B
- Chains 11-16: method C
→ Entropy: HIGH

After 100 RLVR steps:
- ALL chains converge to method A
→ Entropy: LOW (collapse!)
→ RLVR loses learning signal
```

### K=8 vs K=16

| K | Initial Entropy | After 100 RL | Stability |
|---|----------------|--------------|-----------|
| K=8 | Medium-High | Stable | ✅ |
| K=16 | Very High | COLLAPSE | ❌ |

**Đây là lý do K=8 được khuyến nghị cho RLVR training.**

---

# LAYER 3 — NODES #8–#15

## ⚡ NODE #8

### ❓ Q: **K=8 HAY K=16**? Khi nào chọn con số nào?

### ✅ A:

**K=8** là sweet spot cho hầu hết cases. **K=16** chỉ cho extreme cases.

### So sánh

| Metric | K=8 | K=16 |
|--------|-----|------|
| **Heavy Mean** | ~95-100 | ~100 (ceiling) |
| **Cost** | 8x | 16x |
| **RLVR Stability** | ✅ Ổn định | ❌ Collapse sau 100 steps |
| **Entropy** | Optimal | Quá cao → collapse |
| **Saturation** | Chưa saturate | Gần saturate |

### Khi nào dùng K=8

1. **Production deployment** — cost-effective
2. **RLVR training** — stable, entropy optimal
3. **Standard hard problems** — đủ để đạt 99%+ performance

### Khi nào dùng K=16

1. **Extreme benchmarks** — AIME level hoặc cao hơn
2. **Không huấn luyện** — inference-only
3. **Cost không là vấn đề** — cần squeeze ra 0.5-1% cuối

### Saturation

> **K > 20 chỉ thêm ~0.2%**

```
Heavy Mean
    ↑
100%│●───────────────────────── (ceiling)
    │     ●
 95% │        ●
    │           ●        ●
 90% │               ●
    │
    └────┬────┬────┬────┬────→ K
         4    8    12   16   20+
              ↑
         Sweet spot: K=8
```

---

## ⚡ NODE #9

### ❓ Q: **Heavy Mean vs Heavy Pass vs Pass@N** — Khác nhau thế nào?

### ✅ A:

### Pass@N

**Định nghĩa:** Probability **at least 1** of N samples is correct.

```
Pass@N = 1 - (1-p)ⁿ

p = single sample accuracy
```

### Heavy Pass

**Định nghĩa:** After deliberation, **final synthesized answer** is correct.

```
Heavy Pass = 1 if deliberation_final == correct
           = 0 otherwise
```

### Heavy Mean

**Định nghĩa:** Mean of Heavy Pass across M problems.

```
Heavy Mean = (1/M) × Σ Heavy_Pass_i
```

### So sánh

| Metric | Khi nào = 1? | Yêu cầu |
|--------|-------------|---------|
| **Pass@N** | Any of N samples correct | Just 1 correct |
| **Heavy Pass** | Deliberation synthesis correct | Synthesis must be right |
| **Heavy Mean** | Average Heavy Pass | Consistent across dataset |

### Tại sao Heavy Pass khó hơn Pass@N?

```
Pass@N scenario:
Chain 1: Wrong
Chain 2: Wrong
Chain 3: Correct ← Pass@N = 1

Heavy Pass scenario:
Chains 1,2,3 đều cho answers nhưng deliberation có thể:
→ Pick chain 3 → Wrong (deliberation made wrong synthesis)
→ OR: Catch error in chain 3 → Correct
→ Heavy Pass requires deliberation to be correct
```

---

## ⚡ NODE #10

### ❓ Q: Tại sao **DELIVERATOR** không cần là model mạnh nhất?

### ✅ A:

**Phát hiện ngược chiều từ §4.2:**

Experiment cố định parallel-stage (R1-Distill-Qwen-7B), xoay vòng deliberation qua 3 models:

| Deliberator Model | Heavy Mean Improvement |
|-------------------|----------------------|
| R1-Distill-Qwen-7B (7B) | Baseline |
| R1-Distill-Qwen3-8B (8B) | Improved |
| Qwen2.5-32B-Instruct (32B) | **Significant** |

**Bất ngờ:** Qwen2.5-32B-Instruct nổi tiếng **yếu về tự suy luận** nhưng tốt về tổng hợp.

### Tại sao?

**Deliberator cần:**
- ✅ Khả năng **tổng hợp** — kết hợp nhiều luồng
- ✅ Khả năng **bám hướng dẫn** — làm theo protocol
- ✅ Khả năng **phân tích phê bình** — tìm lỗi logic

**Deliberator KHÔNG cần:**
- ❌ Khả năng tự suy luận mạnh (job của parallel stage)
- ❌ Creative reasoning (đã có K chains)
- ❌ State-of-the-art reasoning

> **Đảo ngược trực giác:** "Lấy model mạnh nhất làm cuối" là SAI.

---

## ⚡ NODE #11

### ❓ Q: **Khi nào** Heavy Thinking THẤT BẠI?

### ✅ A:

Heavy Thinking không phải silver bullet. Có những cases nó không hoạt động.

### Limitations

| Hạn chế | Mô tả |
|---------|-------|
| **Cost** | 8-16x inference — đắt cho bài dễ |
| **Latency** | Sequential bottleneck |
| **Saturate** | K > 20 marginal ~0% |
| **Deliberator quality** | Có baseline floor |

### Failure Cases

| Scenario | Lý do | Mitigation |
|----------|-------|-----------|
| **All K chains wrong** | Diversity đủ nhưng tất cả sai | Cần better model |
| **Deliberator bias** | Deliberator cũng có bias | Multi-deliberator? |
| **Problem not decomposable** | Cần sequential, không parallel | Không phù hợp |
| **Domain shift** | Train math, test code | Fine-tune riêng |
| **K chains too similar** | Lack of diversity | Increase diversity |

### Khi nào KHÔNG nên dùng

```
✅ NÊN dùng:
- Math Olympiad (AIME, HMMT)
- Competitive programming
- HLE (Humanity's Last Exam)
- Complex logical deduction

❌ KHÔNG nên:
- Simple QA
- Factual retrieval
- Casual conversation
- Tasks single-shot đã đạt >95%
```

---

## ⚡ NODE #12

### ❓ Q: **RLVR** (Reinforcement Learning with Verifiable Rewards) hoạt động thế nào?

### ✅ A:

**RLVR** = RL with Verifiable Rewards — phần thưởng có thể kiểm chứng được (đúng/sai).

### Đặc điểm

- Không cần reward model (như RLHF)
- Áp dụng cho reasoning tasks: math, code, logic
- Reward: correct (1) or incorrect (0)

### RLVR trong Heavy Thinking

```
1. Sample K=8 trajectories cho problem q
2. Deliberation → final answer
3. Compute reward: r = 1 if correct, 0 if incorrect
4. GRPO/GSPO update policy
5. Repeat

→ Heavy Mean improves ~10% in first 100 steps
```

### Tại sao cải thiện?

```
Initial: K chains có diversity ngẫu nhiên
After RLVR: Policy học được:
  - Reasoning patterns nào dẫn đến đúng
  - Khi nào thử method A vs method B
  - Cách tổng hợp hiệu quả

→ Heavy Mean tăng vì policy "thông minh hơn"
```

---

## ⚡ NODE #13

### ❓ Q: **Voting đơn giản** vs **Heavy Thinking** — Khi nào dùng cái nào?

### ✅ A:

**Voting:** Chọn majority answer từ N samples  
**Heavy Thinking:** Phân tích reasoning rồi tổng hợp

### Decision Framework

| Task | Single-shot | Voting | Heavy |
|------|-------------|--------|-------|
| **Easy (>95%)** | ✅ | ❌ Overkill | ❌ Overkill |
| **Medium (85-95%)** | ✅ | OK | ✅ |
| **Hard (<85%)** | ❌ | Insufficient | ✅ |
| **Extreme (<50%)** | ❌ | ❌ | ✅ Required |

### Cost/Benefit

```
Single-shot: 1x cost, baseline quality
Voting (N=8): 8x cost, +5-10% quality
Heavy (K=8): 8x cost, +10-20% quality (on hard tasks)
```

### Khi nào Voting đủ?

1. Bài toán không quá khó (single-shot > 85%)
2. Có external tool verify được
3. Latency quan trọng hơn accuracy
4. Cost-sensitive

### Khi nào cần Heavy?

1. Bài toán khó (single-shot < 85%)
2. Không có ground truth verify
3. Reasoning process quan trọng
4. Quality > cost

---

## ⚡ NODE #14

### ❓ Q: **4-SECTION SKILL FORMAT** — HeavySkill được đóng gói thế nào?

### ✅ A:

HeavySkill được đóng gói thành **1 portable skill file** với 4 sections.

### 4 Sections

```yaml
# Section 1: WHEN TO ACTIVATE
---
ACTIVATION_CONDITIONS:
  - Mathematical reasoning
  - Complex logical deduction
  - Tasks where correctness is critical
  - Problems where single attempt may fail

DO_NOT_ACTIVATE_FOR:
  - Simple factual questions
  - Casual conversation

# Section 2: PARALLEL REASONING PROTOCOL
---
PARALLEL_REASONING_PROTOCOL:
  spawn: K agents (K=3~5 harness, K=8+ workflow)
  instructions:
    - Solve independently from scratch
    - Show complete reasoning
    - Use different approaches

# Section 3: DELIBERATION PROMPT
---
DELIBERATION_PROMPT:
  - Analyze all trajectories
  - Identify errors/gaps
  - Synthesize final answer

# Section 4: OUTPUT CONSTRAINTS
---
OUTPUT_CONSTRAINTS:
  - Match domain format (boxed for math)
  - Match query language
```

### Tại sao quan trọng?

| Lợi ích | Giải thích |
|---------|-----------|
| **Portable** | Load được Claude Code, CodeX, Hermes, OpenAI Agents, LangChain |
| **No code changes** | Không cần implement, chỉ load skill |
| **Standardized** | Mọi người dùng cùng protocol |

### Supported Engines

| Engine | Status |
|--------|--------|
| **vLLM** | ✅ Recommended |
| **DeepSeek API** | ✅ |
| **Together AI** | ✅ |
| **OpenRouter** | ✅ |
| **Ollama** | ✅ |

---

## ⚡ NODE #15

### ❓ Q: **Single-shot** thất bại NHƯ THẾ NÀO trên bài toán khó?

### ✅ A:

### Cơ chế thất bại

**1. Confirmation Bias**
```
Step 1: "I'll try method A"
Step 2: "Method A is working..."
Step 3: "Wait, this isn't right... but I've committed"
Step 4: "Let me push through anyway"
→ NO OPPORTUNITY TO TRY METHOD B
```

**2. Error Propagation**
```
Step 1 (95%) → Step 2 (95%|S1) → Step 3 (95%|S2) → Final
Probability correct: 0.95³ ≈ 86%

Với 10 steps: 0.95¹⁰ ≈ 60%
→ Càng nhiều steps → càng dễ sai
```

**3. Local Optimum Trap**
```
Single-shot: Stuck at local optimum A
            ↙
Start → A(optimum) → B(worse)
         ↓
    Không thấy global optimum C

Heavy: Chains explore A, B, C simultaneously
      → Deliberator picks C (global optimum)
```

### Tóm tắt

| Vấn đề | Heavy Thinking giải quyết bằng |
|--------|-------------------------------|
| Confirmation bias | Independence — chains không thấy nhau |
| No self-correction | Deliberation — review tất cả |
| Limited exploration | K parallel paths |
| Error propagation | K independent chains |
| No failure diversity | Diversity of approaches |

---

# LAYER 4 — LEAF NODES #16–#31

*(16 câu hỏi chi tiết nhất, mở rộng từ các parent nodes)*

---

## NODE #16 — từ NODE #8

### ❓ Q: Tại sao **K > 20** không cải thiện thêm?

### ✅ A:

Đường cong saturate rất nhanh sau K=8-12.

```
K=0 → K=4:  Steep improvement
K=4 → K=8:  Significant improvement  
K=8 → K=12: Moderate improvement
K=12 → K=16: Small improvement
K=16 → K=20: ~0.5% improvement
K=20+ → ~0.2% improvement
```

**Nguyên nhân:**
- K đủ lớn → hầu hết approaches đã được explore
- Thêm K chỉ thêm marginal diversity
- Cost tăng tuyến tính, gain giảm dần

---

## NODE #17 — từ NODE #8

### ❓ Q: **K=3-5** trong Claude Code harness — tại sao không phải K=8?

### ✅ A:

Trong Claude Code (skill mode), K được khuyến nghị K=3-5 vì:

| Lý do | Giải thích |
|-------|-----------|
| **Context limit** | Claude Code context window nhỏ hơn |
| **Cost** | 8x có thể quá đắt cho typical tasks |
| **Skill mode** | Lightweight version, không phải full pipeline |
| **Use case** | Harness đơn giản, không phải batch evaluation |

**Khi nào dùng K=8 trong Claude Code:**
- Task cực khó
- Cost không là vấn đề
- Muốn maximum quality

---

## NODE #18 — từ NODE #9

### ❓ Q: **Pass@N = 99%** nhưng Heavy Mean chỉ 95% — có nghĩa gì?

### ✅ A:

Pass@N cao nhưng Heavy Mean thấp hơn có thể xảy ra.

**Giải thích:**
- Pass@N: "có ít nhất 1 chain đúng"
- Heavy Mean: "deliberation synthesis đúng"

**Nghĩa:**
- K chains có chain đúng, nhưng deliberator **không nhận ra** nó đúng
- Hoặc deliberator bị **bias** làm sai synthesis

**Đây là weakness của Heavy Thinking:**
- Cần better deliberator để match Pass@N
- Paper claim: "stronger LLMs can approach Pass@N"

---

## NODE #19 — từ NODE #9

### ❓ Q: Tại sao **Heavy Mean 100%** nhưng **Pass@N 99%**?

### ✅ A:

Heavy Mean > Pass@N có thể xảy ra!

**Giải thích:**
- Pass@N: có ít nhất 1 chain đúng
- Heavy Mean: deliberation synthesis **tạo ra** đáp án đúng từ K chains

**Ví dụ:**
```
Chain 1: Wrong (method A sai ở step 2)
Chain 2: Wrong (method B đúng nhưng computing sai)
Chain 3: Wrong (method C gần đúng)

Pass@N = 0 (không có chain nào hoàn toàn đúng)

Heavy:
Deliberator nhận ra:
- Chain 1: Method A đúng direction nhưng step 2 sai
- Chain 2: Method B đúng, chỉ computing sai → có thể fix
- Chain 3: Method C có partial insight

Deliberation: "Method B là đúng, chỉ cần recalculate step 3"
→ Final Answer: CORRECT

Heavy Mean = 100%
```

**Đây là sức mạnh của Deliberation:** tạo ra đáp án mới từ K chains, không chỉ chọn.

---

## NODE #20 — từ NODE #10

### ❓ Q: **Qwen2.5-32B-Instruct** — tại sao yếu về suy luận nhưng tốt về tổng hợp?

### ✅ A:

Đây là hiện tượng thú vị về **specialization of LLMs**.

**Yếu về tự suy luận:**
- Single-chain reasoning không tốt
- Thường miss steps, logical gaps
- Confidence không correlated với correctness

**Tốt về tổng hợp:**
- Đọc và phân tích nhiều inputs tốt
- So sánh và contrast different approaches
- Identify patterns và inconsistencies

**Giả thuyết:**
- Training data emphasis on "analysis/summary" tasks
- Ít emphasis on "generate new reasoning from scratch"
- Có xu hướng "follow instructions" tốt

---

## NODE #21 — từ NODE #10

### ❓ Q: Có nên dùng **Multi-deliberator** không?

### ✅ A:

**Ý tưởng:** Thay vì 1 deliberator, dùng K deliberators để reduce bias.

**Potential benefits:**
- Reduce single deliberator bias
- Multiple perspectives on synthesis
- More robust final answer

**Problems:**
- 2x cost (hoặc K+1x)
- Additional coordination overhead
- Diminishing returns

**Recommendation:**
- Single deliberator đủ cho hầu hết cases
- Multi-deliberator chỉ cho extreme reliability requirements
- Đơn giản hơn: dùng better single deliberator

---

## NODE #22 — từ NODE #11

### ❓ Q: **Domain shift** — train trên math, test trên code?

### ✅ A:

Heavy Thinking được train/test chủ yếu trên math reasoning.

**Transfer sang code:**
- Math: verifiable reward (đáp án đúng/sai)
- Code: verifiable reward (compiles, passes tests)

**Khả năng transfer:**
- Parallel reasoning: TỐT (code cũng cần nhiều approaches)
- Deliberation: TỐT (synthesis skills transferable)
- RLVR training: CẦN domain-specific training

**Cần confirm:**
- Benchmark trên code tasks
- Training recipes cho code domain
- Verifiable reward setup cho code

---

## NODE #23 — từ NODE #12

### ❓ Q: **Reward shaping** trong Heavy Thinking RLVR?

### ✅ A:

**Current:** Binary reward (correct = 1, incorrect = 0)

**Potential improvements:**
- Partial credit: partially correct approach gets partial reward
- Step-level reward: reward based on which steps are correct
- Style reward: reward for elegant/efficient reasoning

**Trade-offs:**
- More complex reward → more complex to implement
- Shaped reward → potential for reward hacking
- Binary reward → simple, hard to game

**Paper focus:** Binary verifiable reward là đủ cho math/code.

---

## NODE #24 — từ NODE #12

### ❓ Q: **Curriculum learning** với Heavy Thinking?

### ✅ A:

**Ý tưởng:** Train từ easy → hard problems.

```
Stage 1: Easy problems (K=4)
Stage 2: Medium problems (K=6)  
Stage 3: Hard problems (K=8)
```

**Benefits:**
- Start with high success rate → stable RL
- Gradually increase difficulty → better final performance
- K escalation matches problem difficulty

**Implementation:**
- Problem difficulty classifier needed
- Staged training setup
- May require custom RL infrastructure

---

## NODE #25 — từ NODE #13

### ❓ Q: **Hybrid approach** — Heavy Thinking + Voting?

### ✅ A:

**Ý tưởng:** Dùng voting cho easy, Heavy cho hard.

```
if problem_difficulty == "easy":
    use Voting (N=8)
elif problem_difficulty == "hard":
    use Heavy (K=8)
```

**Implementation:**
- Difficulty classifier: single-shot confidence, problem type, etc.
- Route accordingly
- Cost: average between Voting and Heavy

**Benefits:**
- Cost savings on easy problems
- Quality maintained on hard problems
- Best of both worlds

**Best classifier:**
- Single-shot confidence < threshold → use Heavy
- Problem type (math/code) → heuristic routing

---

## NODE #26 — từ NODE #13

### ❓ Q: **Iterative Heavy Thinking** — chạy nhiều lần?

### ✅ A:

**Ý tưởng:** Sau deliberation, feed kết quả lại thành "expert thinker" và chạy lại.

```
Iteration 1:
  K chains → Deliberation → Answer₁

Iteration 2:
  K chains + Answer₁ (as "expert trajectory") → Deliberation → Answer₂

Iteration 3:
  K chains + Answer₂ → Deliberation → Answer₃
```

**When useful:**
- Extremely hard problems (2-3 iterations max)
- Convergence check
- Verification

**Diminishing returns:**
- 2 iterations thường đủ
- 3 iterations: marginal gain
- More: almost no improvement

---

## NODE #27 — từ NODE #14

### ❓ Q: **Custom skill** — tạo HeavySkill variant cho domain riêng?

### ✅ A:

**Có thể customize 4 sections:**

```yaml
ACTIVATION_CONDITIONS:
  # Thay đổi: chỉ activate cho domain cụ thể
  - "Legal case analysis"
  - "Financial document review"

PARALLEL_REASONING_PROTOCOL:
  # Thay đổi: spawn specialized agents
  - "Use legal reasoning framework"
  - "Apply different precedent searches"

DELIBERATION_PROMPT:
  # Thay đổi: domain-specific analysis
  - "Evaluate legal arguments"
  - "Compare precedent strength"

OUTPUT_CONSTRAINTS:
  # Thay đổi: output format cho domain
  - "Format: legal brief"
  - "Citations required"
```

**Examples:**
- Legal: K chains = different legal theories
- Medical: K chains = different diagnostic frameworks
- Financial: K chains = different analysis models

---

## NODE #28 — từ NODE #14

### ❓ Q: **vs Chain-of-Thought** — Heavy Thinking khác gì?

### ✅ A:

| Aspect | CoT | Heavy Thinking |
|--------|-----|---------------|
| **Chains** | 1 chain | K chains (8 hoặc 16) |
| **Self-correction** | Limited | Deliberation stage |
| **Diversity** | None | High |
| **Cost** | 1x | 8-16x |
| **Training** | None | RLVR possible |

**CoT** = single chain of thought (prompt "think step by step")

**Heavy Thinking** = multiple chains + deliberation synthesis

**Relationship:** CoT là predecessor, Heavy Thinking là advanced version.

---

## NODE #29 — từ NODE #15

### ❓ Q: **Systematic bias** trong single-shot?

### ✅ A:

**Systematic bias** = tất cả chains đi theo cùng một hướng sai vì shared assumptions.

```
Shared assumption: "Problem is about X"
Chain 1: A → B → C → X (sai vì X không đúng)
Chain 2: A → B → C → X (sai vì X không đúng)
Chain 3: A → B → C → X (sai vì X không đúng)

Voting: 3/3 = X (sai nhưng unanimous)
Heavy: Deliberator CÓ THỂ catch nếu phân tích được assumption sai
```

**Heavy Thinking advantage:** Deliberator có thể question shared assumptions mà không có chain nào question.

---

## NODE #30 — từ NODE #15

### ❓ Q: **Error cascade** trong reasoning chains?

### ✅ A:

**Error cascade** = lỗi ở step N lan truyền đến tất cả steps sau.

```
Single-shot:
Step 1 (95%) → Step 2 (95%|S1) → Step 3 (95%|S2) → Step 4 (95%|S3) → Final

Probability: 0.95 × 0.95 × 0.95 × 0.95 = ~81%

Heavy:
Chain 1: S1 → S2 → S3 → S4 → E1 (cascade error)
Chain 2: S1' → S2' → S3' → S4' → E2 (cascade error)
Chain 3: S1'' → S2'' → S3'' → S4'' → E3 (NO cascade — different path)

Deliberator: E1 và E2 cùng sai, E3 đúng → pick E3
```

**Key:** Chains độc lập → cascade errors không lan truyền giữa các chains.

---

## NODE #31 — từ NODE #15

### ❓ Q: **Partial correctness** — K chains đúng một phần?

### ✅ A:

**Partial correctness** = mỗi chain đúng một phần, không chain nào hoàn toàn đúng.

```
Chain 1: Step A ✓ → Step B ✓ → Step C ✗ → Answer X (wrong)
Chain 2: Step A ✗ → Step B ✓ → Step C ✓ → Answer Y (wrong)
Chain 3: Step A ✓ → Step B ✗ → Step C ✓ → Answer Z (wrong)

All 3 wrong individually

Heavy Deliberation:
→ Chain 1: A, B đúng, C sai
→ Chain 2: B, C đúng, A sai
→ Chain 3: A, C đúng, B sai

Deliberator: "A, B, C đều có trong ít nhất 1 chain đúng"
→ "Hãy kết hợp: A từ chain 1, B từ chain 2, C từ chain 3"
→ Final Answer: A + B + C = CORRECT

Heavy Mean = 100% (mặc dù không chain nào đúng 100%)
```

**Đây là superpower của Heavy Thinking:** synthesis tạo ra đáp án tốt hơn bất kỳ chain nào đơn lẻ.

---

# KEY TAKEAWAYS

## Từ Root (Node #1)
1. Heavy Thinking = **2-stage pipeline**: Parallel K chains → Deliberation → Synthesis

## Từ Layer 1 (Nodes #2, #3)
2. **Parallel Reasoning** cần thiết vì confirmation bias, local optimum, error cascade
3. **Deliberation ≠ Voting** — phân tích reasoning quality, không chỉ đếm votes

## Từ Layer 2 (Nodes #4–#7)
4. **K independent chains** tốt hơn 1 long chain vì diversity và isolation
5. **Memory Cache** = simple concatenation, không phải fancy memory system
6. **GRPO/GSPO** enable RLVR training với relative ranking
7. **Entropy** cần balance — K=8 optimal, K=16 entropy collapse

## Từ Layer 3 (Nodes #8–#15)
8. **K=8** là sweet spot, K=16 chỉ cho extreme cases
9. **Heavy Mean** đo deliberation quality, khác với Pass@N
10. **Deliberator** không cần mạnh, cần tổng hợp tốt
11. **Heavy Thinking** không dùng cho easy tasks, chỉ cho hard tasks
12. **RLVR** cải thiện ~10% trong 100 steps đầu
13. **Voting** đủ cho easy, Heavy cho hard
14. **4-section skill format** = portable, no code changes
15. **Single-shot** thất bại vì confirmation bias, error cascade, local optimum

## Từ Leaf Nodes (#16–#31)
16. **K > 20** saturate, chỉ thêm ~0.2%
17. **K=3-5** trong Claude Code harness vì context/cost limits
18. **Pass@N ≠ Heavy Mean** — có thể Heavy Mean thấp hơn
19. **Heavy Mean > Pass@N** có thể xảy ra khi deliberation tạo ra answer mới
20. **Specialization** — deliberator cần tổng hợp, không cần suy luận
21. **Multi-deliberator** không đáng vì diminishing returns
22. **Domain shift** cần domain-specific training
23. **Reward shaping** phức tạp, binary reward đủ
24. **Curriculum learning** từ easy → hard có thể giúp
25. **Hybrid** approach tối ưu cost/quality
26. **Iterative** Heavy Thinking có diminishing returns
27. **Custom skill** có thể tạo cho domain riêng
28. **vs CoT** — Heavy là advanced version với K chains
29. **Systematic bias** = all chains same wrong assumption
30. **Error cascade** không lan truyền giữa independent chains
31. **Partial correctness** = super power của Heavy — synthesis tạo answer hoàn chỉnh

---

# APPENDIX

## Source Files

| File | Link |
|------|------|
| Paper | [arXiv:2605.02396](https://arxiv.org/abs/2605.02396) |
| Repo | [github.com/wjn1996/HeavySkill](https://github.com/wjn1996/HeavySkill) |
| Skill file | [skill/heavyskill.md](https://raw.githubusercontent.com/wjn1996/HeavySkill/main/skill/heavyskill.md) |

## Tree Stats

| Stat | Value |
|------|-------|
| **Total Nodes** | 31 |
| **Layers** | 5 |
| **Root** | Node #1 |
| **Leaf Nodes** | 16 (Nodes #16–#31) |
| **Internal Nodes** | 15 |
