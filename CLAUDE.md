# AGENTS.md — Deep Work by Steve

> **Version:** 2.1 | **Updated:** 2026-05-27
> **Scope:** Root agent guide — L0 anchor rules + L1 working policy.
> Đọc file này đầu tiên. Tra cứu chi tiết tại Working Map bên dưới.

<instructions>
Luôn ưu tiên thay đổi an toàn. Workspace này là Personal AI Skill Lab — không phải production runtime codebase.
KHÔNG sửa trực tiếp `.hermes/skills/` — edit ở `skills/rebuild/` rồi sync qua skill-sync.
KHÔNG xóa skill context artifacts mà không archive.
KHÔNG di chuyển file mà không cập nhật routing maps.
</instructions>

---

## 1. Project Overview

**Đây là gì:** Personal AI Skill Lab + Knowledge Base để xây dựng và duy trì **Master Skill Suite** — bộ công cụ tạo, nâng cấp, quản lý và bảo trì Agent Skills cho Claude Code / AI agents.

**Mục tiêu:**
1. Tích lũy tri thức cá nhân → chuyển hóa thành Agent Skill chất lượng cao, reusable, production-ready
2. Phát triển 6-Stage pipeline: Explorer → Architect → Planner → Builder → Tester → Indexer
3. Quản lý vòng đời skill: `raw → designed → planned → built → verified → installed`
4. Áp dụng CASE System (Confidence-Aware Skill Execution) để kiểm soát chất lượng

**Người dùng:** Steve (Steve-claw#7410) + AI coding agents (Claude Code, Codex, Hermes, Antigravity)

---

## 2. Tech Stack

```yaml
tech_stack:
  primary_languages: [Markdown, YAML, Python, Bash]
  agent_runtimes:
    - Claude Code (.calude/skills)
    - Antigravity (.agents.skills)
    - Hermes agent (.hermes/skills/)
    - OMC/OMX agents (.omc/, .omx/)
  documentation_format: "Hybrid Markdown + YAML + XML-like tags (per standards.md)"
  knowledge_format: "LLM Knowledge Activation Standard (standards.md)"
  skill_format: "7-Zone structure (SKILL.md + knowledge/ + scripts/ + templates/ + data/ + loop/ + assets/)"
  versioning: "Semantic versioning per skill (YAML frontmatter)"
  validation: "schema_validator.py + Docker/gVisor sandbox"
```

---

## 3. Folder Structure

```text
deep_work_by_steve/          ← Root workspace
├── AGENTS.md                ← [L0] Root agent guide (file này)
├── workspce_tree.md         ← Workspace map + Zone taxonomy (L0 routing)
├── architecture.md          ← Master Skill Suite architecture — 6 stages, CASE system
├── standards.md             ← LLM Knowledge Activation Standard — format rules
├── hermes.md                ← Hermes agent config/notes
│
├── knowledge/               ← [L1] Curated knowledge (ai-agents, programming, experience, projects)
├── .skill-context/          ← [L2] Design & planning state per skill (design.md, todo.md, criteria.md)
├── skills/
│   ├── rebuild/             ← [L3] Canonical skill factory — nơi build production skills
│   │   ├── _shared/         ← Shared schemas, validators, templates, fixtures
│   │   ├── skill-architect/ ← Stage 1: Architect skill
│   │   ├── skill-planner/   ← Stage 2: Planner skill
│   │   ├── skill-builder/   ← Stage 3: Builder skill
│   │   ├── skill-sync/      ← Sync rebuild → runtime
│   │   └── ...              ← Other rebuilt skills
│   ├── raw/                 ← [L4] Imported/legacy skills — chưa qua rebuild
│   ├── Update-suite/        ← Suite upgrade workspace (current-suite, updated-suite, lifecycle-docs)
│   └── solution-flow/       ← Micro-skills cho specific problem flows
│
├── .agents/skills/          ← Active project-level skills (read by Antigravity)
├── .hermes/skills/          ← [L6] Installed runtime skills — KHÔNG sửa trực tiếp
├── agents/                  ← Agent role prompts (architect.md, planner.md, executor.md...)
├── .skill-context/          ← Per-skill design state (design.md, todo.md, criteria.md, build-log.md)
├── docs/                    ← Documentation, session summaries, raw drafts
├── knowledge/               ← Curated knowledge base
├── info_temp/               ← [L7] Raw inbox — ideas, drafts, scratch (không permanent)
└── scripts/                 ← Utility scripts (sync-skills.sh, ...)
```

> **Routing nhanh:** Xem `workspce_tree.md` → Routing Quick Reference table.

---

## 4. Commands

```yaml
commands:
  sync_skill:
    run: "bash scripts/sync-skills.sh"
    desc: "Sync rebuilt skill từ skills/rebuild/ vào .hermes/skills/"

  validate_skill:
    run: "python skills/rebuild/_shared/validators/schema_validator.py <skill-path>"
    desc: "Validate SKILL.md structure và YAML frontmatter"

  check_workspace:
    run: "cat workspce_tree.md"
    desc: "Xem workspace map đầy đủ + routing guide"

  view_architecture:
    run: "cat architecture.md"
    desc: "Xem 6-stage pipeline + CASE recovery + Acceptance Matrix"

  view_standards:
    run: "cat standards.md"
    desc: "Xem LLM Knowledge Activation format rules"
```

---

## 5. Code Style & Conventions

```yaml
conventions:
  skill_naming: "kebab-case (ví dụ: skill-architect, prompt-cleaner)"
  frontmatter: "YAML frontmatter bắt buộc: name, description, version, tags, when_to_use"
  language_in_instructions: "Imperative (Do X, Never Y — không dùng passive voice)"
  skill_file_limit: "SKILL.md tối đa 700 tokens (L0 anchor) — chi tiết chuyển sang knowledge/ hoặc policy/"
  format_rules:
    markdown: "Dùng cho explanation, architecture, rationale, onboarding"
    yaml: "Dùng cho constraints, policies, checklists, output_contract"
    xml_tags: "Dùng cho semantic boundaries (instructions, context, examples)"
  trace_tags: "Mọi task trong todo.md phải có trace: [TỪ DESIGN §N] hoặc [TỪ AUDIT TÀI NGUYÊN]"
  placeholder_rule: "ZERO placeholder trong production code (// TODO, pass, mock() = FAIL)"
```

---

## 6. Do's & Don'ts

```yaml
must:
  - Đọc workspce_tree.md trước khi làm bất kỳ task nào để xác định đúng zone
  - Edit skill ở skills/rebuild/ — KHÔNG sửa .hermes/skills/ trực tiếp
  - Viết YAML frontmatter đầy đủ cho mọi SKILL.md mới
  - Archive context artifacts trước khi xóa hoặc overwrite
  - Update routing map (workspce_tree.md) khi thay đổi structure
  - Báo cáo summary_of_changes + zones_affected sau mỗi task

must_not:
  - Sửa trực tiếp .hermes/skills/ — dùng rebuild + sync workflow
  - Nhồi domain context vào AGENTS.md (file này) — chuyển sang docs/ hoặc knowledge/
  - Dùng placeholder (TODO, mock, pass) trong production skill code
  - Di chuyển file mà không cập nhật routing maps
  - Xóa .skill-context/ artifacts mà không archive evidence
  - Tạo skill mới mà không có design.md và criteria.md trước
```

---

## 7. Architecture Notes

> Chi tiết đầy đủ tại `architecture.md`. Dưới đây là quyết định cốt lõi đã được confirm — KHÔNG tranh luận lại.

**6-Stage Pipeline (Master Skill Suite v1.0.0):**

```text
Stage 0 Explorer  → sinh exploration.md + criteria.md
Stage 1 Architect → sinh design.md (7-Zone mapping, Mermaid diagrams)
Stage 2 Planner   → sinh todo.md (trace tags, DAG blocker map)
Stage 3 Builder   → build SKILL.md + src code (zero placeholder)
Stage 4 Tester    → chạy sandbox Docker/gVisor → sinh verification.md (PASS/FAIL)
Stage 5 Indexer   → sinh README.md + đăng ký vào llms.txt
```

**State Ledger:** `.skill-context/{skill-name}/` là persistent state giữa các stage stateless.

**CASE System:** Rollback tự động khi confidence < 70% hoặc validation FAIL → tạo `rollback_request.yaml`, archive state, notify developer.

**Staleness Policy:**
- < 7 ngày: tiếp tục từ checkpoint
- 7-30 ngày: cảnh báo, review todo.md trước
- > 30 ngày: force restart từ Stage 0

---

## 8. Testing Standards

```yaml
testing:
  framework: "Docker/gVisor sandbox (Stage 4 Tester)"
  minimum_test_cases: 2 kịch bản test cụ thể trong criteria.md
  placeholder_density: "Phải = 0 để PASS"
  validator: "schema_validator.py đối chiếu exploration.schema.yaml"
  evidence: "verification.md với kết quả PASS/FAIL rõ ràng"
  sandbox_isolation: "Mọi script kiểm thử chạy trong Docker biệt lập — KHÔNG chạy trực tiếp trên host"
  acceptance_gate:
    bad: "AI tự xác nhận Pass mà không chạy script thực tế"
    good: "100% kịch bản test từ criteria.md pass trong sandbox"
    premium: "Tích hợp kiểm thử hiệu năng + prompt injection defense"
```

---

## 9. Known Constraints & Limitations

```yaml
constraints:
  runtime_is_readonly:
    desc: ".hermes/skills/ là installed runtime — KHÔNG edit trực tiếp"
    workaround: "Edit skills/rebuild/ → chạy skill-sync"

  stateless_sessions:
    desc: "Mỗi agent stage là một session độc lập (stateless)"
    workaround: "Dùng .skill-context/{name}/ làm persistent state ledger"

  token_budget_l0:
    desc: "SKILL.md không được vượt 700 tokens (L0 anchor rule)"
    workaround: "Tách chi tiết sang knowledge/, policy/, scripts/"

  architure_typo:
    desc: "File architure.md bị typo (thiếu 'c') — đây là tên file thực tế, chưa rename"
    note: "Khi reference file này, dùng đúng tên: architure.md (không phải architecture.md)"
    status: "Open — chờ Steve confirm rename"

  raw_skills_unverified:
    desc: "skills/raw/ chứa ~40 skill chưa kiểm chứng — chỉ dùng để tham khảo"
    workaround: "Copy vào skills/rebuild/ và qua pipeline trước khi dùng"

  omx_unclear:
    desc: ".omx/ directory purpose chưa được document đầy đủ"
    status: "Open — chờ Steve clarify"
```

---

## 10. Quality Gates

```yaml
quality_gates:
  skill_production_checklist:
    - "YAML frontmatter đầy đủ: name, description, version, tags, when_to_use"
    - "SKILL.md ≤ 700 tokens (L0 anchor)"
    - "Có sections: Limitations + When not to use"
    - "Zero placeholders trong code/scripts"
    - "criteria.md có ≥ 5 tiêu chí nghiệm thu + ≥ 2 kịch bản test case"
    - "verification.md PASS từ sandbox"
    - "Đăng ký vào llms.txt sau khi verified"
    - "Update .skill-context/registry/README.md với lifecycle status"

  progressive_disclosure:
    - "SKILL.md chỉ chứa L0 anchor (instructions + routing map)"
    - "Chi tiết ở knowledge/, policy/, scripts/ — nạp on-demand"
    - "Root guide không làm kho tri thức"

  modularity:
    - "Mỗi skill có cấu trúc 7 Zones: core, knowledge, scripts, templates, data, loop, assets"
    - "Skill phải reusable độc lập với project cụ thể"

  versioning:
    - "Mọi skill có version + changelog trong YAML frontmatter"
    - "Breaking changes phải có migration notes"
```

---

## Working Map

```yaml
load_when_needed:
  workspace_routing: "workspce_tree.md"
  skill_framework_architecture: "architecture.md"
  documentation_format_standard: "standards.md"
  skill_lifecycle_status: ".skill-context/registry/README.md"
  shared_schemas_validators: "skills/rebuild/_shared/"
  agent_role_catalog: "agents/README.md"
  knowledge_base_index: "knowledge/README.md"
  hermes_config: "hermes.md"
```

---

## Interaction Protocol

```yaml
agent_protocol:
  before_any_task:
    - Đọc workspce_tree.md để xác định đúng Zone cần làm việc
    - Xác định skill đang ở lifecycle phase nào (raw / designed / planned / built / verified / installed)
  before_editing_skill:
    - Nếu runtime (.hermes/skills/): edit rebuild → sync
    - Nếu raw (skills/raw/): copy vào rebuild trước
    - Nếu new: tạo design.md + criteria.md trong .skill-context/{name}/
  during_editing:
    - Preserve SKILL.md contract (frontmatter, sections, 7 Zones structure)
    - Document build evidence trong build-log.md
    - Zero placeholder — nếu chưa implement được, dừng và notify
  before_final_response:
    - Verify routing map updated nếu có thay đổi structure
    - Report: summary_of_changes + zones_affected + lifecycle_phase_changed
```
