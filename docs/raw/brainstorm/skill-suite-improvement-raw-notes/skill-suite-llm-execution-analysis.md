# Skill Suite LLM Execution Analysis
## Why Well-Designed Skills Don't Translate to Quality LLM Execution

**Date:** 2026-05-10  
**Analysis Method:** Heavy Thinking K=8 (Steve's Manual)  
**Workspace:** /home/steve/Work-space/deep_work_by_steve

---

## Executive Summary

**Problem:** Bộ 3 skill (skill-architect, skill-planner, skill-builder) có thiết kế tốt NHƯNG khi được LLM sử dụng thì KHÔNG phát huy toàn bộ thiết kế.

**Root Cause:** Skill suite suffers from **"SPECIFICATION HYGIENE FAILURE"** - thiết kế promises rigorous workflow nhưng implementation tự tạo ra cái bẫy cho chính nó.

**Key Insight:** DeepSeek Flash với SINGLE PROMPT mang lại kết quả TỐT cho address audit. Điều này chứng tỏ: vấn đề không phải ở model mà ở chính skill design.

---

## Root Causes (Priority Order)

### P0 — EMERGENCY (Skill doesn't work at all)

| # | Root Cause | Evidence | Impact |
|---|------------|----------|--------|
| P0-01 | `case-system.md` referenced by skill-planner but DOES NOT EXIST | skill-planner SKILL.md line 29 references it, file missing | Boot fails or hallucinates content |
| P0-02 | `knowledge/architect.md` in skill-builder doesn't exist | skill-builder SKILL.md line 78 references it, directory missing | Builder cannot read domain knowledge |
| P0-03 | `skills/rebuild/skill-suite-upgrade/scripts/check_status.py` hardcoded path | skill-planner SKILL.md line 88-89 | Boot sequence fails when CWD differs |

### P1 — CRITICAL (Skill works but quality degraded)

| # | Root Cause | Evidence | Impact |
|---|------------|----------|--------|
| P1-01 | Progressive Disclosure contradictions | YAML tier1 says 2 files, Contributing Components table says 2+ mandatory at boot | LLM confused, front-loads instead of lazy loading |
| P1-02 | Heavy Thinking claimed but NOT implemented | skill-planner says K=4 but no delegate_task spawning | Sequential analysis ≠ parallel reasoning |
| P1-03 | §3 Zone Mapping regex matches ALL backtick text | validate_skill.py extracts `xxx` from any backtick, not just table cells | False positives, wrong files expected |
| P1-04 | Tier 2 triggers are vague event names | "load_when: Step READ" - LLM must guess when that is | No automatic PD enforcement |
| P1-05 | 25 guardrails exceed LLM attention capacity | 3 skills × complex rules | Instruction following degrades mid-execution |

### P2 — IMPORTANT (Tech debt)

| # | Root Cause | Evidence | Impact |
|---|------------|----------|--------|
| P2-01 | `../_shared/` path breaks when skill relocated | Relative path only works at `skills/rebuild/` | Not portable |
| P2-02 | Validator exit codes inconsistent | case-system.md says 0/1/2, validate_gate.py only uses 0/1 | EMERGENCY handling missing |
| P2-03 | Version numbers inconsistent | skill-architect: 2.0.0, skill-planner: 3.0.0, skill-builder: none | Can't track which version deployed |

---

## The Self-Paradoxical Loop

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

**This is identical to Single-Shot Reasoning failure (per HeavySkill paper):**
- 1 read → 1 interpret → 1 output → move on
- No self-correction
- Error cascade

Applied to skill suite:
- Architect designs based on 1 read
- Planner interprets design based on 1 read  
- Builder builds based on 1 read
- All 3 stages compound the original misinterpretation

---

## Why DeepSeek Flash Works for Address Audit

**Single prompt, single response, good quality output.**

**Why skill suite fails:**

| Address Audit | Skill Suite |
|---------------|-------------|
| Single clear prompt | 3-stage pipeline with complex gates |
| No state management needed | Session boundary breaks context |
| Single output | Handoff degrades through 3 stages |
| No progressive disclosure | Tier system fails to enforce |
| Direct task execution | Heavy Thinking claimed but not done |

**Conclusion:** Problem is NOT model capability. Problem is skill design complexity exceeding what LLM can reliably execute.

---

## Impact Cascade

```
skill-architect fails → skill-planner BLOCKED → skill-builder BLOCKED
     ↓                       ↓                       ↓
§3 Zone Mapping      todo.md missing         No skill output
missing
```

**Shared framework failure affects ALL 3 skills simultaneously:**
- `../_shared/knowledge/framework.md` is Tier 1 mandatory for all
- If missing → all 3 skills fail at boot

---

## Solution Recommendations

### Option A: True Heavy Thinking Implementation

Implement HT correctly per paper:
- K=8 parallel chains at each phase
- Deliberation checkpoint before phase gates
- Serialized memory cache between stages

**Cost:** 8x inference per phase  
**Benefit:** Follows the science  
**Risk:** Expensive, may not be needed for structured tasks

### Option B: Honest Simpler Design (RECOMMENDED)

Remove complexity that exceeds LLM capacity:

| Change | Current | Recommended |
|--------|---------|-------------|
| Guardrails | 25 total | 5-7 per skill |
| Heavy Thinking | Claimed K=4 | Remove claim OR implement correctly |
| Progressive Disclosure | "load when needed" | Explicit triggers per phase |
| Handoffs | Markdown text | Add schema validation |
| Path resolution | Relative fragile | Absolute or documented requirement |

**This is what DeepSeek Flash does naturally:**
- Single clear instruction
- No tier management
- Direct execution

---

## Files Analyzed

- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-architect/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-planner/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-builder/SKILL.md`
- `/home/steve/Work-space/deep_work_by_steve/skills/rebuild/skill-suite-upgrade/*`
- `/home/steve/Work-space/deep_work_by_steve/knowledge/ai-agents/*`
- `/home/steve/Work-space/deep_work_by_steve/docs/rebuild-skill-suite-*.md`

---

## Related Documents

- `/home/steve/Work-space/deep_work_by_steve/docs/rebuild-skill-suite-risk-analysis.md` - 35+ risks identified
- `/home/steve/Work-space/deep_work_by_steve/docs/raw/ideas/skill-suite-improvement-raw-notes/2026-05-09-alternative-design-patterns.vi.md` - Alternative patterns
