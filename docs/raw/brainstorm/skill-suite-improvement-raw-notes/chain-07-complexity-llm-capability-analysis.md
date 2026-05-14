# Chain 7: Complexity vs LLM Capability — Độ phức tạp có phù hợp với LLM không?

**Date:** 2026-05-12
**Task:** Chain 7 — Complexity vs LLM Capability Analysis
**Workspace:** /home/steve/Work-space/deep_work_by_steve

---

## 1. Core Question

**"Khi nào độ phức tạp của skill design trở thành gánh nặng cho LLM thay vì hỗ trợ?"**

---

## 2. Evidence Base

### 2.1 The DeepSeek Flash Experiment

Từ `skill-suite-llm-execution-analysis.md`:

> **DeepSeek Flash với SINGLE PROMPT mang lại kết quả TỐT cho address audit.**

| Address Audit | Skill Suite |
|---------------|-------------|
| Single clear prompt | 3-stage pipeline with complex gates |
| No state management needed | Session boundary breaks context |
| Single output | Handoff degrades through 3 stages |
| No progressive disclosure | Tier system fails to enforce |
| Direct task execution | Heavy Thinking claimed but not done |

**Kết luận:** Vấn đề không phải ở model mà ở chính skill design.

### 2.2 The 25 Guardrails Problem

Từ `chain-04-guardrails-anti-hallucination-analysis.md`:

> **P1-05: 25 guardrails exceed LLM attention capacity**
> - 3 skills × complex rules
> - Instruction following degrades mid-execution

Design đưa ra 5 AH rules (AH1-AH5), nhiều quality gates, trace tag requirements, progressive disclosure tiers. Nhưng khi LLM phải nhớ và tuân thủ 25+ guardrails cùng lúc, instruction following bắt đầu degrade.

### 2.3 The Self-Paradoxical System

Từ `skill-suite-llm-execution-analysis.md`:

```
┌─────────────────────────────────────────────────────────────────┐
│         SKILL SUITE = "SELF-PARADOXICAL SYSTEM"                  │
│                                                                 │
│  Thiết kế: "Dừng và kiểm tra ở mỗi gate"                     │
│  Thực tế:   Không có mechanism cho gate checkpoint              │
│                                                                 │
│  Thiết kế: "Progressive Disclosure = load when needed"           │
│  Thực tế:   No trigger = no enforcement = no PD                  │
│                                                                 │
│  Thiết kế: "Heavy Thinking K=4 chains"                          │
│  Thực tế:   Sequential analysis ≠ parallel reasoning             │
│                                                                 │
│  Thiết kế: "3-Phase Pipeline = Waterfall"                       │
│  Thực tế:   Waterfall WITHOUT contracts = error cascade         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Handoff Quality Breakdown

Từ `chain-05-handoff-quality-analysis.md`:

```
Contract Design:      7/10
Validator Coverage:   6/10  (missing §3 filename, §7 Tier, §8 count)
Runtime Adherence:    5/10
Overall Handoff:     6/10 — Cần cải thiện validator + runtime enforcement
```

---

## 3. The Complexity Spectrum

### 3.1 What LLMHandles Well

| Pattern | Example | Why It Works |
|---------|---------|--------------|
| **Single clear prompt** | "Audit this address: [input]" | Direct execution, no state management |
| **One-shot output** | Generate complete response | No context accumulation |
| **Flat instruction set** | 5-7 rules max | Within attention capacity |
| **Explicit over implicit** | "Do X then Y" | No inference needed |

### 3.2 What Overloads LLM

| Pattern | Skill Suite Example | Why It Fails |
|---------|---------------------|--------------|
| **Multi-stage pipeline** | Architect → Planner → Builder | Context fragmentation across stages |
| **Implicit Progressive Disclosure** | "load when needed" without triggers | No enforcement = no PD |
| **Claimed Heavy Thinking** | K=4 claimed but sequential only | Parallel ≠ sequential |
| **25+ guardrails** | AH1-AH5 × 3 skills + gates | Attention degradation mid-execution |
| **Relative path dependencies** | `../../_shared/` breaks when relocated | Fragile execution environment |
| **Manual gate checkpoints** | "Dừng và kiểm tra ở mỗi gate" without mechanism | Gates skipped |

### 3.3 The Breaking Point

```
Complexity Level
     │
     │                           ████ Heavy Thinking (K=8)
     │                      ████
     │                 ████
     │            ████      Chain-6: Dead Features (25+ items)
     │       ████
     │  ████
     │                                              Chain-4: 25 guardrails
     │──────────────────────────────────────────────────────────────
     0              LLM Reliable              LLM Degrades      LLM Fails
     
     ▲
     │  DeepSeek Flash (single prompt) — works here
```

**Critical insight:** Skill suite operates ABOVE the LLM reliable threshold on multiple dimensions simultaneously.

---

## 4. Root Cause Analysis

### 4.1 Design Intent vs LLM Reality

| Dimension | Design Intent | LLM Reality |
|-----------|--------------|-------------|
| **Guardrails** | 25 rules ensure quality | 25 rules cause degradation |
| **Progressive Disclosure** | Load when needed | No trigger = no PD |
| **Heavy Thinking** | K=4 parallel chains | Sequential only |
| **Gate Checkpoints** | Stop and verify | No mechanism = skipped |
| **Handoffs** | Markdown contract | 6/10 runtime quality |

### 4.2 The Compound Effect

```
Stage 1: Architect
    ↓ §3 Zone Mapping missing (P0-01)
Stage 2: Planner BLOCKED
    ↓ case-system.md doesn't exist
Stage 3: Builder BLOCKED
    ↓ cascades from original failure
```

Each stage compounds the original error. This is identical to Single-Shot Reasoning failure:
- 1 read → 1 interpret → 1 output → move on
- No self-correction
- Error cascade

---

## 5. The Match Scorecard

### 5.1 Design Complexity vs LLM Capability

| Skill Element | Complexity | LLM Can Execute? | Margin |
|---------------|------------|------------------|--------|
| 5 AH rules | Low | ✅ Yes | Safe |
| 25 guardrails total | High | ❌ No | Overload |
| Single prompt task | Low | ✅ Yes | Safe |
| 3-stage pipeline | High | ⚠️ Partial | Context fragmentation |
| K=4 parallel (true) | High | ⚠️ Partial | Sequential ≠ parallel |
| K=4 claimed only | Medium | ❌ No | Trust damage |
| Explicit PD triggers | Medium | ✅ Yes | With triggers |
| "Load when needed" | Low | ❌ No | No enforcement |
| Gate with validator | Medium | ✅ Yes | Auto-enforced |
| Gate manual only | Low | ⚠️ Partial | Skipped often |
| Specific filename in §3 | Low | ✅ Yes | Clear contract |
| Wildcard in §3 | Medium | ⚠️ Partial | Causes confusion |
| Schema-validated handoff | Medium | ✅ Yes | Machine-checked |
| Markdown-only handoff | Low | ⚠️ Partial | Human-interpreted |

### 5.2 The Threshold Table

```
┌────────────────────────────────────────────────────────────────┐
│                   COMPLEXITY THRESHOLD TABLE                    │
├──────────────────┬───────────────┬─────────────────────────────┤
│ Element          │ Safe Limit    │ Skill Suite Actual          │
├──────────────────┼───────────────┼─────────────────────────────┤
│ Guardrails/skill │ 5-7           │ 8+ (AH1-5 + others)         │
│ Pipeline stages  │ 1-2           │ 3                            │
│ Rules to remember│ 7±2 (Miller)  │ 25+                          │
│ PD tiers         │ 2 max         │ 3 with vague triggers       │
│ Handoff format   │ Schema valid  │ Markdown + partial schema   │
│ Thinking chains   │ Explicit K    │ Claimed K, sequential only  │
└──────────────────┴───────────────┴─────────────────────────────┘
```

---

## 6. When Complexity HELPS vs HURTS

### 6.1 Complexity That Helps

| Type | Example | Why |
|------|---------|-----|
| **Schema validation** | YAML frontmatter with exit codes | Machine-readable, auto-enforced |
| **Explicit triggers** | `load_when: Phase 1 complete` | Clear execution path |
| **Concrete filenames** | `knowledge/architect.md` not `*.md` | No ambiguity |
| **Error recovery** | Validator exit codes (0/1/2) | Know when failed |

### 6.2 Complexity That Hurts

| Type | Example | Why |
|------|---------|-----|
| **Invisible requirements** | "Dừng và kiểm tra" without mechanism | LLM doesn't know when |
| **Implicit rules** | "load when needed" without trigger | No enforcement |
| **Claimed capabilities** | K=4 without parallel execution | Trust paradox |
| **Accumulated state** | 3-stage with context fragmentation | Error cascade |

---

## 7. The Key Insight

**"Complexity that requires LLM to manage itself will fail."**

```
┌──────────────────────────────────────────────────────────────┐
│                    DESIGN PRINCIPLE                            │
│                                                               │
│   If a design element requires LLM to:                        │
│   - Self-regulate instruction adherence                      │
│   - Enforce its own Progressive Disclosure                   │
│   - Remember more than 7±2 rules                             │
│   - Manage cross-stage state without tools                   │
│                                                               │
│   THEN: The design will fail at runtime.                     │
│                                                               │
│   REASON: LLM cannot reliably monitor its own compliance.    │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. The Simplicity Pattern That Works

DeepSeek Flash for address audit:

```
Prompt: "Audit this address: [input]"
         ↓
   Single model
         ↓
   Direct output
         ↓
   Done
```

**What makes it work:**
1. Single clear instruction
2. No tier management
3. Direct execution
4. No state between stages

---

## 9. Recommendations

### 9.1 Reduce to LLM-Reliable Complexity

| Change | Current | Recommended | LLM Impact |
|--------|---------|-------------|-----------|
| Guardrails/skill | 25 total | 5-7 | Attention safe |
| Pipeline stages | 3 | 1-2 | Context preserved |
| PD tiers | 3 vague | 2 explicit | Enforceable |
| Heavy Thinking | Claimed K=4 | Remove claim OR implement | Trust restored |
| Gate checkpoints | Manual | Auto-validator | Reliable |

### 9.2 Make Implicit Explicit

```
IMPLICIT (fails):        EXPLICIT (works):
─────────────────        ─────────────────
"load when needed"   →   "load_when: [PH0_complete]"
"Dừng và kiểm tra"   →   "validator exit code 0 before proceeding"
"Kiểm tra gate"      →   "run validate_gate.py; exit 0 = pass"
```

### 9.3 Enforce What You Claim

| Claim | Reality | Fix |
|-------|---------|-----|
| Heavy Thinking K=4 | Sequential only | Remove claim OR implement K=4 parallel |
| Progressive Disclosure | No triggers | Add explicit `load_when` for each tier |
| Gate checkpoints | Manual, skipped | Auto-run validator before proceeding |

---

## 10. Conclusion

### Câu hỏi: Độ phức tạp có phù hợp với LLM không?

**Có — khi complexity được thiết kế để LLM thực thi, không phải để LLM tự quản lý.**

| Design Pattern | LLM-Friendly? | Reason |
|----------------|----------------|--------|
| Single clear prompt | ✅ Yes | Direct execution |
| 5-7 explicit rules | ✅ Yes | Within attention |
| Auto-validator gates | ✅ Yes | Machine enforced |
| Explicit PD triggers | ✅ Yes | Clear loading path |
| Schema-validated handoff | ✅ Yes | Machine-checkable |
| 25 rules self-managed | ❌ No | Attention overload |
| "Load when needed" | ❌ No | No enforcement |
| Manual gates | ❌ No | Skipped |
| Claimed HT without implementation | ❌ No | Trust paradox |

**The skill suite fails because it was designed for perfect LLM execution (self-regulation, self-enforcement) rather than for what LLM can actually reliably do.**

**The path forward: Make complexity that can be enforced by external mechanisms, not by LLM self-management.**

---

## Files Analyzed

- `/home/steve/Work-space/deep_work_by_steve/docs/skill-suite-llm-execution-analysis.md` — Core evidence
- `/home/steve/Work-space/deep_work_by_steve/docs/chain-04-guardrails-anti-hallucination-analysis.md` — Guardrail analysis
- `/home/steve/Work-space/deep_work_by_steve/docs/chain-05-handoff-quality-analysis.md` — Handoff quality
- `/home/steve/Work-space/deep_work_by_steve/docs/chain-06-dead-features-analysis.md` — Dead features

---

## Related Chains

- Chain 4: Guardrails overload (25 vs 5-7 safe)
- Chain 5: Handoff quality (6/10 runtime)
- Chain 6: Dead features (orphaned complexity)
