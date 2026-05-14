## 🔬 Phân tích Bộ 3 Skill Suite: skill-architect / skill-planner / skill-builder

### 1. Kiến trúc Tổng thể (Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Master Framework (7 Zones)                     │
│        _shared/knowledge/framework.md — Single Source of Truth    │
└─────────────────────────────────────────────────────────────────┘
                    ▲           ▲           ▲
        ┌───────────┴───┐ ┌───┴───┐ ┌─────┴─────┐
        │ skill-architect│ │ skill- │ │ skill-    │
        │ v2.0.0        │ │planner │ │ builder   │
        │ Stage: 1      │ │v3.0.0  │ │           │
        │               │ │Stage:2 │ │ Stage: 3  │
        └───────────────┘ └────────┘ └───────────┘
              │                │            │
              ▼                ▼            ▼
         design.md        todo.md      skill files
```

---

### 2. Phân tích theo 3 Tiêu chí Nâng cấp

#### 2.1 AI-First Quality

| Aspect                     | Status        | Issue                                                       |
| -------------------------- | ------------- | ----------------------------------------------------------- |
| **Progressive Disclosure** | ⚠️ Partial    | Có Tier 1/2/3 nhưng load logic không nhất quán giữa 3 skill |
| **Anti-hallucination**     | ⚠️ Partial    | AH1-AH5 rules tốt nhưng thiếu enforcement mechanism cụ thể  |
| **Traceability**           | ⚠️ Weak       | `[TỪ DESIGN §N]` tags tồn tại nhưng thiếu validator tự động |
| **Boot Sequence**          | ✅ Good       | CRITICAL DIRECTIVE block tốt, buộc đọc SKILL.md trước       |
| **Knowledge Depth**        | ❌ Unbalanced | architect.md (skill-planner) = 1.7KB quá mỏng               |

**Vấn đề cốt lõi**: File `knowledge/architect.md` của skill-planner chỉ có **1.7KB** — đây là file bắt buộc đọc ở Boot theo SKILL.md tier1, nhưng nội dung quá mỏng không đủ để Planner thực hiện Multi-Perspective Analysis đúng cách.

```yaml
# skill-planner tier1 reference:
tier1:
  - path: "knowledge/case-system.md" # ❌ FILE KHÔNG TỒN TẠI
  - path: "scripts/check_status.py" # ❌ FILE KHÔNG TỒN TẠI
```

---

#### 2.2 Modularity

| Aspect                | Status       | Issue                                                   |
| --------------------- | ------------ | ------------------------------------------------------- |
| **Zone Separation**   | ✅ Good      | 7 Zones rõ ràng, mỗi skill map đúng zone                |
| **Pipeline Contract** | ⚠️ Partial   | A→P contract (§3 Zone Mapping) tốt, P→B contract yếu    |
| **Dependency**        | ❌ Unclear   | `successor_hints` có nhưng không có `predecessor_hints` |
| **Skill Isolation**   | ❌ Duplicate | 2 bộ skill: `.claude/skills/` và `.hermes/skills/`      |

**Vấn đề nghiêm trọng**: Cùng 1 skill nhưng tồn tại 2 phiên bản. Cái nào là canonical? Khi nào dùng cái nào?

```bash
# Hai bản của cùng 1 skill:
.claude/skills/skill-builder/SKILL.md     # 7.4K
.hermes/skills/skill-builder/SKILL.md     # ???

# skill-planner có thêm file không tồn tại:
.claude/skills/skill-planner/knowledge/case-system.md  # referenced but MISSING
```

---

#### 2.3 Dynamic (LLM-Agnostic)

| Aspect                 | Status          | Issue                                                          |
| ---------------------- | --------------- | -------------------------------------------------------------- |
| **Degrees of Freedom** | ✅ Good         | §5 build-guidelines.md có Low/Medium/High freedom guidelines   |
| **Pattern Examples**   | ⚠️ Limited      | Ví dụ trong framework đủ nhưng thiếu edge case examples        |
| **Error Handling**     | ❌ Inconsistent | Mỗi skill có exit codes khác nhau, không thống nhất            |
| **Model Assumptions**  | ❌ Implicit     | Không có hint gì về model preference (opus vs sonnet vs haiku) |

**Vấn đề**: Skill viết bằng tiếng Việt có dấu cho trigger keywords và trace tags. LLM model có thể không xử lý regex `[CẦN LÀM RÕ]` đúng nếu encoding không consistent.

---

### 3. Root Cause Analysis — Tại sao "Kiến trúc ổn nhưng kết quả không đạt"?

```
┌──────────────────────────────────────────────────────────────────────┐
│                    HYPOTHESIS: 5 ROOT CAUSES                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  H1: KNOWLEDGE STARVATION                                             │
│  ├─ skill-planner knowledge/architect.md = 1.7KB (quá mỏng)          │
│  ├─ case-system.md được reference nhưng không tồn tại                 │
│  └─ Result: Planner không đủ context để phân tích đúng              │
│                                                                       │
│  H2: CONTRACT VIOLATION                                                │
│  ├─ §3 Zone Mapping contract yếu: "Files cần tạo" có placeholder     │
│  ├─ Planner tạo task không đúng spec                                 │
│  └─ Builder nhận input không đủ → hallucinate                        │
│                                                                       │
│  H3: TRACEABILITY BREAK                                               │
│  ├─ Trace tags [TỪ DESIGN §N] không được validate tự động            │
│  ├─ Builder có thể tạo file không có trong §3                        │
│  └─ Không có automated gate giữa các stage                           │
│                                                                       │
│  H4: INCONSISTENT ERROR HANDLING                                        │
│  ├─ skill-architect: Exit codes 0/1/2                                 │
│  ├─ skill-planner: Exit codes 0/1/2 (giống)                           │
│  ├─ skill-builder: Error Policy = Log → Notify → Stop               │
│  └─ Result: LLM không biết khi nào DỪNG                              │
│                                                                       │
│  H5: DUPLICATE ARCHITECTURE                                             │
│  ├─ .claude/skills/ và .hermes/skills/ cùng tồn tại                 │
│  ├─ Không clear đâu là canonical                                     │
│  └─ Result: Confusion khi maintain, upgrade không đồng bộ             │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 4. Gap Analysis vs CLAUDE.md Standards

| CLAUDE.md Principle        | Skill Suite Status | Gap                                             |
| -------------------------- | ------------------ | ----------------------------------------------- |
| **L0 + L1 separation**     | ❌ Không rõ        | Root guide (SKILL.md) chứa quá nhiều L2 content |
| **Token budget awareness** | ❌ Không đề cập    | Không có ngưỡng cho SKILL.md size               |
| **Format selection**       | ⚠️ Partial         | Dùng Markdown + YAML nhưng không nhất quán      |
| **Semantic anchors**       | ⚠️ Inconsistent    | "must", "should" không dùng đúng chỗ            |
| **Output contract**        | ⚠️ Vague           | `output_contract` có nhưng không đủ chi tiết    |
| **Verification**           | ❌ Missing         | Không có section về cách verify output          |

---

### 5. Specific Issues cần fix

#### Issue #1: Missing Critical Files

```
❌ skill-planner/knowledge/case-system.md (referenced in tier1, 1.7KB architect.md gợi là placeholder)
❌ skill-planner/scripts/check_status.py (referenced in tier1, không tồn tại)
❌ skill-builder/knowledge/architect.md = 4.6KB (đọc ở Phase 1 nhưng quá mỏng)
```

#### Issue #2: Duplicate Skills

```
.claude/skills/    ← đây là cái nào? staging? production?
.hermes/skills/    ← hay cái này mới là canonical?
```

#### Issue #3: Workflow Tracker Inconsistency

```
skill-architect:  ✅ Có "Workflow Progress Tracker"
skill-planner:    ❌ KHÔNG CÓ checkpoint tracker (boot sequence hơi mơ)
skill-builder:     ✅ Có "[skill-builder] Progress:" checklist
```

#### Issue #4: Anti-hallucination Without Enforcement

```
skill-planner G1: "Trace required — Every item MUST trace back"
skill-builder G4: "Source Grounding — 100% from design/todo/resources"

Nhưng KHÔNG CÓ script validate trace tags tự động.
```

---

### 6. Recommendations (Priority Order)

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECOMMENDATION MATRIX                         │
├─────────────┬─────────────┬─────────────────────────────────────┤
│ Priority    │ Impact      │ Action                               │
├─────────────┼─────────────┼─────────────────────────────────────┤
│ P0-CRITICAL │ Architecture│ Chọn 1 canonical skill location       │
│             │             │ (.claude/ hoặc .hermes/, không phải  │
│             │             │ cả hai)                              │
├─────────────┼─────────────┼─────────────────────────────────────┤
│ P0-CRITICAL │ Knowledge   │ Tạo case-system.md cho skill-planner  │
│             │             │ (đang reference nhưng missing)         │
├─────────────┼─────────────┼─────────────────────────────────────┤
│ P1-HIGH     │ Validation  │ Thêm validate_skill.py cho trace     │
│             │             │ tags verification                    │
├─────────────┼─────────────┼─────────────────────────────────────┤
│ P1-HIGH     │ Consistency │ Thêm Workflow Tracker vào            │
│             │             │ skill-planner (boot sequence)         │
├─────────────┼─────────────┼─────────────────────────────────────┤
│ P2-MEDIUM   │ Token       │ Thêm size limit reminder vào         │
│             │             │ SKILL.md (300-500 lines guideline)    │
├─────────────┼─────────────┼─────────────────────────────────────┤
│ P2-MEDIUM   │ Documentation│ Bổ sung model preference hints       │
│             │             │ (opus=architecture, sonnet=standard)  │
└─────────────┴─────────────┴─────────────────────────────────────┘
```

---

Bạn muốn tôi tiến hành **nâng cấp** bộ skill như thế nào? Có 2 hướng:

1. **Minimal Fix**: Chỉ fix P0 issues (missing files, duplicate architecture)
2. **Full Upgrade**: Fix toàn bộ theo analysis trên, viết lại các file yếu
