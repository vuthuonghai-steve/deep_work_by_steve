# MASTER FRAMEWORK — Shared Knowledge Base

> **Purpose**: Single source of truth for all 3 meta-skills
> **Location**: `_shared/knowledge/framework.md` (portable, resolved relative to skills-root)
> **Path from SKILL.md**: `../_shared/knowledge/framework.md` (1 level up)
> **Path from knowledge/*.md**: `../../_shared/knowledge/framework.md` (2 levels up)
> **Usage**: Read this FIRST when working with skill-architect, skill-planner, or skill-builder

---

## 1. SEVEN ZONES STRUCTURE

Every skill package MUST follow this directory structure:

| Zone | Folder | Purpose | Required |
|------|--------|---------|----------|
| **Core** | `SKILL.md` | Orchestration, persona, workflow, guardrails | ✅ Always |
| **Knowledge** | `knowledge/` | References, standards, guidelines | ✅ Usually |
| **Scripts** | `scripts/` | Executable automation (Python, Bash) | As needed |
| **Templates** | `templates/` | Output format templates | As needed |
| **Data** | `data/` | Config, static data, schemas | As needed |
| **Loop** | `loop/` | Checklists, logs, test cases | ✅ Usually |
| **Assets** | `assets/` | Images, icons, static files | Rarely |

---

## 2. PIPELINE FLOW

```
skill-explorer           skill-architect          skill-planner           skill-builder
     │                        │                        │                        │
     ▼                        ▼                        ▼                        ▼
exploration.md §6   →    design.md §3       →    todo.md tasks      →   <skills-root>/{name}/
(Arch Recommendations)  (Zone Mapping)         (phase breakdown)          (skill package)
     │                        │                        │
     ▼                        ▼                        ▼
exploration.md §3   →    design.md §7       →    Pre-req table
(7 Golden Standards)    (PD Plan)               (resources audit)
```

### Handoff Contracts

**Explorer → Architect** (exploration.md sections):
- §3 Seven Golden Standards Assessment → Architect designs Capability Map (§2) and Risks (§8)
- §4 AI Instruction Standards & Rules → Architect guides loop checklists (§3.loop)
- §6 Architectural Recommendations → Architect defines Zone Mapping (§3) and Progressive Disclosure Plan (§7)

**Architect → Planner** (design.md sections):
- §3 Zone Mapping → Planner creates task breakdown
- §7 Progressive Disclosure → Planner audit resources
- §8 Risks → Planner creates mitigation tasks

**Planner → Builder** (todo.md):
- Phase tasks with priorities
- Pre-requisites table
- Resource readiness status

---

## 3. ZONE MAPPING CONTRACT

When reading `design.md §3`, all skills must follow this format:

| Zone | Files cần tạo | Nội dung | Bắt buộc? |
|------|--------------|----------|-----------|
| Core | `SKILL.md` | Persona, phases, guardrails | ✅ |
| Knowledge | `knowledge/xxx.md` | Domain, standards | ✅/❌ |
| Scripts | `scripts/xxx.py` | Automation tools | ✅/❌ |
| Templates | `templates/xxx.template` | Output formats | ✅/❌ |
| Data | `data/xxx.yaml` | Config, schema | ✅/❌ |
| Loop | `loop/xxx.md` | Checklists, verify rules | ✅/❌ |
| Assets | N/A | Not needed | ❌ |

**Rules**:
- "Files cần tạo" column → direct input for task creation
- "Không cần" → skip that zone
- Builder MUST NOT add files not in §3 (except with documented rationale)

---

## 4. PROGRESSIVE DISCLOSURE (PD)

Three-tier loading system:

| Tier | Name | When to Load | Examples |
|------|------|--------------|----------|
| **Tier 1** | Mandatory | Always, at boot | `SKILL.md`, core knowledge |
| **Tier 2** | Conditional | When context requires | Domain docs, templates |
| **Tier 3** | Optional | On-demand | Assets, edge-case references |

**PD in SKILL.md**:
- Boot Sequence → Tier 1 files only
- Each Phase → Reference Tier 2 files as needed

---

## 5. PIPELINE STAGE DEFINITIONS

| Stage | Skill | Input | Output | Key Sections |
|-------|-------|-------|--------|--------------|
| **0** | skill-explorer | User idea + raw resources | `exploration.md` | §1-§8 |
| **1** | skill-architect | `exploration.md` + Requirements | `design.md` | §1-§10 |
| **2** | skill-planner | `design.md` | `todo.md` | Pre-reqs, Phase Breakdown |
| **3** | skill-builder | `design.md` + `todo.md` | Skill files | SKILL.md, knowledge/*, loop/* |

---

## 6. NAMING CONVENTIONS

### Skill Names
- **Pattern**: `kebab-case` (lowercase, hyphen-separated)
- ✅ `skill-planner`, `api-integrator`, `flow-design-analyst`
- ❌ `SkillPlanner`, `skill_planner`, `skill planner`

### File Names in Zones
| Zone | Pattern | Example |
|------|---------|---------|
| knowledge/ | `domain-topic.md` | `uml-rules.md`, `api-standards.md` |
| scripts/ | `action-target.py` | `init-context.py`, `validate-skill.py` |
| templates/ | `output-format.template` | `design-md.template` |
| loop/ | `purpose-checklist.md` | `design-checklist.md`, `plan-checklist.md` |
| data/ | `config-name.yaml` | `skill-config.yaml` |

---

## 7. ANTI-HALLUCINATION RULES

| Rule | Description | Violation |
|------|-------------|-----------|
| **AH1** | Every task MUST trace to source | Task without `[TỪ DESIGN §N]` |
| **AH2** | Only decompose, don't add requirements | New requirement not in design.md |
| **AH3** | Don't guess domain knowledge | Writing domain content without resources |
| **AH4** | Always label sources | No `[TỪ DESIGN]` / `[GỢI Ý]` distinction |
| **AH5** | Verify resources before completion | Planning complete with missing critical resources |

### Trace Tags Standard

```
[TỪ DESIGN §N]      — Derived directly from design.md section N (regex: ^\[TỪ DESIGN §[0-9]+(\.[0-9]+)?\]$)
[GỢI Ý BỔ SUNG]     — Suggested by skill, not in design.md
[TỪ AUDIT TÀI NGUYÊN] — Generated because resource was missing
[CẦN LÀM RÕ]        — Needs user clarification
```

---

## 8. VERSION MANAGEMENT

All skills use Semantic Versioning:

```
MAJOR.MINOR.PATCH
- MAJOR: Breaking changes (output format, workflow)
- MINOR: Backward-compatible (new features)
- PATCH: Bug fixes, documentation
```

**Version update rules**:
- New section (§11, §12) → MINOR
- Zone Mapping format change → MAJOR
- Typo fix, add example → PATCH

---

## 9. CONTEXT DIRECTORY STRUCTURE

```
.skill-context/{skill-name}/
├── design.md        # Architect's output (INPUT)
├── todo.md          # Planner's output (INPUT)
├── build-log.md     # Builder's output (EVIDENCE)
├── resources/       # User-provided domain docs (INPUT)
├── data/            # Rule configs, scoring matrix (INPUT)
└── loop/            # Prior checks, phase logs (SUPPORTIVE)
```

### Resource Priority Classification

| Priority | Contents | Must Appear In |
|----------|----------|----------------|
| **Critical** | design.md, todo.md, resources/*, data/* | Resource Usage Matrix |
| **Supportive** | loop/*, proof/snapshots | Optional |

---

## 10. 50-POINT MASTER QUALITY GATES SPECIFICATION (ĐẶC TẢ CỔNG CHẤT LƯỢNG CHỦ THỂ)

Để bảo đảm mọi Kỹ năng (Skill) được tạo ra đạt chất lượng Production-grade tuyệt đối và triệt tiêu tính cẩu thả, hời hợt của AI Agent, bộ suite áp dụng **Hệ thống Cổng chất lượng 50 Tiêu chí nghiêm ngặt** chia đều cho 5 Phân lớp:

### A. Stage 0: Explorer (Khai phá Nghiệp vụ) — 10 Tiêu chí
*   **[EXP-01] Business Intent**: Làm rõ nỗi đau nghiệp vụ cốt lõi, người dùng mục tiêu và hành vi kỳ vọng của Kỹ năng.
*   **[EXP-02] Golden Standards Assessment**: Đánh giá Kỹ năng trên tất cả 7 Tiêu chuẩn Vàng (Reusability, Composability, Maintainability, Security, Context Economics, Portability, Reliability).
*   **[EXP-03] SCS Score Calculation**: Đo lường định lượng SCS (Skill Complexity Score) dựa trên 4 biến số thực tế, có giải trình số liệu rõ ràng.
*   **[EXP-04] Decomposed Pivot**: Nếu điểm SCS > 3.0, bắt buộc phải có phương án phân rã Kỹ năng thành các Micro-skills và vẽ sơ đồ phối hợp.
*   **[EXP-05] Security Script Sandbox**: Quy định môi trường thực thi biệt lập (Docker/gVisor) cho các script đi kèm.
*   **[EXP-06] Injection Defense**: Thiết lập luật ranh giới XML để cô lập đầu vào thô và chống Prompt Injection.
*   **[EXP-07] Active Resource Mining**: Phải tra cứu mã nguồn thực tế vàbest practices bên ngoài để thu thập mã mẫu, không tự bịa ra tri thức.
*   **[EXP-08] Grouped Resources**: Phân loại và lưu trữ tài nguyên thu thập được vào các thư mục con có cấu trúc dưới `.skill-context/{name}/resources/`.
*   **[EXP-09] Exploration Schema Pass**: Chạy `schema_validator.py` trên `exploration.md` đạt 100% PASS đối chiếu với `exploration.schema.yaml`.
*   **[EXP-10] Vietnamese Translation**: Dịch toàn bộ thuật ngữ chuyên môn và tóm tắt sang tiếng Việt chuẩn kỹ thuật.

### B. Stage 1: Architect (Thiết kế Kiến trúc) — 10 Tiêu chí
*   **[ARC-01] Problem Statement (§1)**: Mô tả rõ ràng ngữ cảnh, nỗi đau kỹ thuật, giải pháp cụ thể và phạm vi thiết kế.
*   **[ARC-02] 3 Pillars Map (§2)**: Mô tả đầy đủ 3 Trụ cột (Knowledge, Process, Guardrails) của Kỹ năng.
*   **[ARC-03] Specific Zone Mapping (§3)**: Bảng Zone Mapping phải định nghĩa tên file cụ thể, tuyệt đối cấm dùng placeholder như "...", "xxx", "tùy chọn".
*   **[ARC-04] Folder Mindmap (§4)**: Sơ đồ Mermaid mindmap biểu diễn trực quan cấu trúc thư mục của Kỹ năng đúng cú pháp.
*   **[ARC-05] Sequence Flow (§5)**: Sơ đồ Mermaid sequence biểu diễn chính xác luồng chạy nghiệp vụ, các bước kiểm tra và các điểm quyết định.
*   **[ARC-06] Interaction Points (§6)**: Đặc tả các lệnh gọi, đối số truyền vào và kết quả đầu ra mong đợi.
*   **[ARC-07] Progressive Disclosure (§7)**: Định nghĩa rõ ràng 3 Tiers load tài nguyên tĩnh (Tier 1: Mandatory, Tier 2: Conditional, Tier 3: On-Demand).
*   **[ARC-08] Risk Matrix (§8)**: Chỉ ra ít nhất 3 rủi ro kỹ thuật nghiêm trọng kèm theo giải pháp giảm thiểu (Mitigation) cụ thể.
*   **[ARC-09] Open Questions (§9)**: Liệt kê các điểm chưa rõ cần khảo sát thêm và kế hoạch giải quyết.
*   **[ARC-10] Design Schema Pass**: Chạy `schema_validator.py` trên `design.md` đạt 100% PASS đối chiếu với `design.schema.yaml`.

### C. Stage 2: Planner (Lập kế hoạch Triển khai) — 10 Tiêu chí
*   **[PLN-01] Resource Readiness Audit**: Bảng đánh giá tính sẵn sàng của các tài nguyên gốc trước khi lập kế hoạch (Rich vs Thin).
*   **[PLN-02] Context Integrity Check**: Cấm lập kế hoạch khi tài nguyên ở trạng thái "Thin" hoặc thiếu tài liệu critical mà không có task bổ sung tài nguyên.
*   **[PLN-03] Phased Roadmap**: Phân rã kế hoạch thành ít nhất 3-5 Phase độc lập theo trình tự logic.
*   **[PLN-04] Traceability Compliance**: Mọi task lập ra bắt buộc phải có Trace Tag trỏ ngược về mục thiết kế tương ứng (ví dụ: `[TỪ DESIGN §3]`).
*   **[PLN-05] Extra Suggestion Label**: Các task do Agent đề xuất thêm không có trong thiết kế phải dán nhãn `[GỢI Ý BỔ SUNG]`.
*   **[PLN-06] Blocker Flags**: Đánh dấu các rủi ro hoặc điểm nghẽn bằng thẻ `[CẦN LÀM RÕ]`.
*   **[PLN-07] Step-by-Step DoD**: Mỗi Phase phải có tiêu chí Definition of Done (DoD) riêng biệt và đo lường được.
*   **[PLN-08] Dependency Mapping**: Xác định rõ ràng sự phụ thuộc giữa các task, task nào chạy trước, task nào chạy sau.
*   **[PLN-09] Clean Todo Structure**: Trình bày `todo.md` theo đúng cấu trúc Markdown chuẩn hóa.
*   **[PLN-10] Todo Schema Pass**: Chạy `schema_validator.py` trên `todo.md` đạt 100% PASS đối chiếu với `todo.schema.yaml`.

### D. Stage 3: Builder (Xây dựng & Đóng gói) — 10 Tiêu chí
*   **[BLD-01] Zone Completeness**: Tất cả các tệp tin được định nghĩa trong §3 Zone Mapping của thiết kế phải được tạo ra đầy đủ.
*   **[BLD-02] SKILL.md Frontmatter Rules**: YAML Frontmatter của `SKILL.md` chỉ chứa các metadata chuẩn của hệ thống, cấm nhồi nhét cấu hình tùy biến.
*   **[BLD-03] XML Anchor Boundaries**: Toàn bộ chỉ thị hành vi, ngữ cảnh phải bọc trong các thẻ XML L0 thống nhất (`<instructions>`, `<context>`, `<output_contract>`).
*   **[BLD-04] YAML Instructions Block**: Nội dung trong `<instructions>` phải định dạng dưới dạng YAML block với các phân cấp `must`, `must_not` rõ ràng.
*   **[BLD-05] Path Substitution**: Luôn sử dụng biến môi trường `${CLAUDE_SKILL_DIR}` để gọi các script bổ trợ đi kèm, tuyệt đối cấm hardcode đường dẫn tuyệt đối cá nhân.
*   **[BLD-06] Exception Boundary**: Mọi tác vụ I/O, gọi file/mạng trong scripts phải bọc try/except an toàn, cấm nuốt lỗi bằng `except: pass`.
*   **[BLD-07] Context Managers**: Sử dụng cú pháp `with open(...)` khi làm việc với file trong scripts để chống rò rỉ tài nguyên.
*   **[BLD-08] Docstring & Hygiene**: Mọi class và hàm public phải có docstring giải thích chi tiết, đặt tên đúng chuẩn PEP 8.
*   **[BLD-09] Placeholder Density**: Mật độ placeholder (như "...", "todo", "xxx") trong toàn bộ gói Kỹ năng phải < 5 (độ phủ tuyệt đối).
*   **[BLD-10] Unit Test Coverage**: Kỹ năng đi kèm mã nguồn tự động hóa bắt buộc phải có file unit test đi kèm phủ > 90% kịch bản thành công/thất bại.

### E. CASE System & Quality Integration — 10 Tiêu chí
*   **[INT-01] State-Aware Boot**: Mỗi Kỹ năng bắt đầu chạy bắt buộc phải thực thi `check_status.py` để xác định chính xác checkpoint/phase hiện tại.
*   **[INT-02] Checkpoint Staleness Guard**: Phát hiện và cảnh báo người dùng nếu checkpoint thiết kế đã bị bỏ quên quá 7 ngày hoặc sửa đổi ngoài luồng.
*   **[INT-03] Automated Handoff Gate**: Chạy `handoff_validator.py` sau mỗi Stage để kiểm tra tự động bằng máy trước khi gửi câu hỏi tương tác cho người dùng.
*   **[INT-04] Exit Code Compliance**: Tôn trọng tuyệt đối exit codes của validator (0=Pass, 1=Fail, 2=Emergency). Cấm tự ý vượt cổng khi exit 1.
*   **[INT-05] Reverse Trace Integrity**: Sử dụng `trace_validator.py` để quét sạch các lỗi chính tả Trace Tag tiếng Việt (như `[CẦU LÀM RÕ]`, `[TỪ ĐESIGN]`).
*   **[INT-06] Programmatic Rollback Engine**: Tích hợp `rollback_engine.py` để tự động sao lưu bối cảnh và revert về checkpoint an toàn khi Gate validation thất bại 3 lần liên tiếp.
*   **[INT-07] Targeted Refinement Loops**: Vòng lặp sửa lỗi chỉ được phép sửa đổi có mục tiêu tại các dòng/hàm bị báo lỗi, cấm sửa đổi lan man làm phát sinh lỗi thoái lui (regression).
*   **[INT-08] Quality Gatekeeper Integration**: Sử dụng chính Kỹ năng `production-quality-gatekeeper` để quét và chấm điểm chéo các Kỹ năng mới tạo đạt tối thiểu 90% điểm số chất lượng.
*   **[INT-09] Build Log Completeness**: File `build-log.md` ghi nhận đầy đủ, trung thực từng bước quyết định kỹ thuật và bằng chứng chạy test thành công.
*   **[INT-10] Sync & Deployment Verification**: Xác minh sự hoạt động ổn định của Kỹ năng sau khi đồng bộ lên không gian làm việc chính thức.

---

> **Last Updated**: 2026-05-03
> **Maintained By**: Meta-Skill Suite
