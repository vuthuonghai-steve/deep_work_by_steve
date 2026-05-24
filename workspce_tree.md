# Workspace Tree — deep_work_by_steve

> **Ngày cập nhật:** 2026-05-29
> **Version:** 2.0 — viết lại theo chuẩn CLAUDE.md
> **Mục đích:** Bản đồ tổng quan + routing guide cho AI agent khi làm việc trong workspace này

---

## Purpose

**Đây là gì:** Personal AI Skill Lab + Knowledge Base — không phải app/runtime codebase truyền thống.

**Mục tiêu:**
1. Tích lũy tri thức cá nhân (kinh nghiệm, notes, project knowledge, resources, templates)
2. Chuyển hóa knowledge thành Agent Skill (rebuild skill cũ hoặc thiết kế skill mới)
3. Quản lý hệ sinh thái AI agent/prompt/skill đã được thiết kế hoặc import
4. Tạo cấu trúc dễ duy trì theo lifecycle: raw → curated → designed → built → installed

**Ai dùng:** Steve (Steve-claw#7410) + AI coding agents (Claude Code, Codex, Hermes)

<instructions>
Luôn ưu tiên thay đổi an toàn. Đây là workspace quản lý skill/knowledge — không phải production codebase. Các file trong `.hermes/skills/` là installed runtime, không sửa trực tiếp tại đây khi muốn thay đổi skill — hãy edit ở `skills/rebuild/` rồi sync.
</instructions>

---

## Core Policy

```yaml
priority_order:
  - user_task
  - source_fidelity
  - knowledge_integrity
  - minimal_change

constraints:
  must:
    - preserve existing skill contracts (SKILL.md format, folder structure)
    - document any change to skill lifecycle status
    - keep workspace self-documenting (README/index in every major zone)
  must_not:
    - edit installed runtime skills directly (use rebuild + sync workflow)
    - delete skill context artifacts without archiving evidence
    - move files without updating routing maps

output_contract:
  include:
    - summary_of_changes
    - zones_affected
    - lifecycle_phase_changed
    - routing_updated
```

---

## Workspace Zones

### Zone Taxonomy

```yaml
zones:
  L0_root:
    path: "./"
    role: "Entry point — CLAUDE.md, workspce_tree.md, architure.md"
    contains:
      - CLAUDE.md              # LLM standard — format/structure guide
      - workspce_tree.md      # This file — workspace map
      - architure.md          # Skill framework architecture (3 Pillars, 7 Zones)
      - hermes.md             # Hermes agent config/notes

  L1_knowledge:
    path: "./knowledge/"
    role: "Curated source of truth — đã qua chọn lọc"
    contains:
      - ai-agents/            # AI agent research & patterns
      - programming/          # Programming notes & patterns
      - experience/           # Learnings từ thực tế (skill-suite-pipeline-workflow, etc.)
      - projects/            # Project-specific knowledge
      - notes/                # Quick notes
      - resources/            # Curated external resources
      - templates/            # Note templates
      - map/                  # Knowledge maps / indices
    load_policy: "on_demand"
    note: "knowledge/ cần giữ sạch — chỉ content đã curate, không phải raw intake"

  L2_skill_context:
    path: "./.skill-context/"
    role: "Design/planning state cho từng skill đang thiết kế"
    contains_format:
      - "{skill-name}/design.md"
      - "{skill-name}/todo.md"
      - "{skill-name}/build-log.md"
      - "{skill-name}/resources/"
    current_skills:
      - hello-world-writer
      - session-learner
      - skill-suite-upgrade
      - prompt-cleaner
      - heavy-thinking-manual
      - skill-architect-v21
      - skill-planner-v21
      - spec-generator-redesign
      - build-crud-admin-page
    load_policy: "on_demand"
    note: "Đây là design state — không phải nơi đặt skill package hoàn chỉnh"

  L3_skill_factory:
    path: "./skills/rebuild/"
    role: "Canonical skill factory — rebuild skill sau khi có design/todo"
    contains:
      - _shared/              # Shared schemas, templates, validators, fixtures
      - skill-architect/      # OMC skill factory — Architect phase
      - skill-planner/        # OMC skill factory — Planner phase
      - skill-builder/        # OMC skill factory — Builder phase
      - context-before-fix/   # Siinstore-api scoped fix workflow
      - prompt-cleaner/       # Rebuild complete
      - session-learner/      # Rebuild complete
      - spec-generator/       # Rebuild complete
      - skill-suite-upgrade/ # Upgrade workflow
      - skill-sync/          # Sync workflow (rebuild → installed)
      - vercel-agent-skills/ # Vercel agent skills suite
      - tests/               # Unit/integration/e2e tests
    load_policy: "on_demand"
    note: "Output canonical — đây là nơi build skill sau design phase"

  L4_skill_raw:
    path: "./skills/raw/"
    role: "Imported/legacy/reference skills — chưa qua rebuild"
    contains: ~40 raw skills (flutter-*, react-*, ui-*, mermaid-*, etc.)
    load_policy: "task_specific_only"
    note: "Dùng để tham khảo hoặc import nguyên mẫu — không sửa trực tiếp"

  L5_agent_prompts:
    path: "./agents/"
    role: "Agent role prompts — orchestrator/subagent role definitions"
    contains: architect.md, planner.md, executor.md, verifier.md, critic.md, etc.
    load_policy: "on_demand"
    note: "Đây là role prompts, KHÁC với skill packages trong skills/"

  L6_runtime:
    path: "./.hermes/skills/"
    role: "Installed/active skills — Hermes agent runtime"
    contains:
      - skill-architect/      # Active installed
      - skill-planner/        # Active installed
      - skill-builder/        # Active installed
      - spec-generator-has-api/
      - deep-session-learner/
      - prompt-cleaner/
      - hello-world-writer/
      - skill-sync/
      - _shared/
      - achive/               # Archived (older versions)
    load_policy: "task_specific"
    note: "ĐÂY LÀ RUNTIME — edit ở skills/rebuild/ rồi sync, KHÔNG sửa trực tiếp"

  L7_inbox:
    path: "./info_temp/, ./docs/raw/"
    role: "Raw intake — ý tưởng/session/draft chưa xử lý"
    contains:
      - info_temp/           # Scratch, temp files
      - docs/raw/            # Raw ideas, brainstorm, research drafts
    load_policy: "task_specific_only"
    note: "Coi như inbox — định kỳ curate hoặc archive, không giữ permanent"

  L8_runtime_state:
    path: "./.omc/, ./.omx/, ./.task-context/"
    role: "Runtime state — session data, plans, task context"
    contains:
      - .omc/sessions/      # Session history
      - .omc/plans/         # Plan documents
      - .omc/state/         # Mission state
      - .omx/               # OMX runtime state
      - .task-context/      # Task-specific context
    load_policy: "task_specific"
    note: "Đây là runtime artifacts — không phải source of truth cho knowledge"

  L9_docs:
    path: "./docs/"
    role: "Documentation — remediation guides, architecture docs"
    contains:
      - docs/raw/           # Raw documentation drafts
      - docs/sessions/      # Session summaries
    note: "Thường là temporary hoặc reference — không phải curated knowledge"
```

---

## Operating Model

```yaml
knowledge_lifecycle:
  flow:
    - Raw intake (docs/raw, info_temp, sessions)
    - Curate (knowledge/)
    - Design context (.skill-context/{name}/design.md)
    - Plan (.skill-context/{name}/todo.md)
    - Build (skills/rebuild/{name}/)
    - Verify (build-log.md + validators)
    - Install (.hermes/skills/ or target runtime)
    - Feedback (knowledge/experience/)

skill_lifecycle:
  L0_raw:       "Imported/legacy skill, chưa kiểm chứng"
  L1_designed:  "Có design.md"
  L2_planned:   "Có todo.md trace về design"
  L3_built:     "Có package theo 7 Zones structure"
  L4_verified:  "Có build-log/validator evidence"
  L5_installed: "Đã copy vào runtime .hermes/skills/"
```

---

## Working Map

```yaml
load_when_needed:
  skill_framework: "architure.md"
  knowledge_base: "knowledge/README.md"
  skill_context_convention: ".skill-context/registry/README.md"
  rebuild_pipeline: "skills/rebuild/_shared/knowledge/framework.md"
  agent_role_catalog: "agents/README.md"
  current_skill_status: ".skill-context/registry/README.md"
```

---

## Routing Quick Reference

| Task | Zone | Path |
|---|---|---|
| Tạo skill mới | .skill-context + skills/rebuild | `.skill-context/{name}/` → `skills/rebuild/{name}/` |
| Sửa skill đang chạy | skills/rebuild/ rồi sync | `skills/rebuild/{name}/` → sync qua `skill-sync/` |
| Đọc hiểu skill hiện tại | .hermes/skills/ | `.hermes/skills/{name}/` |
| Thêm knowledge mới | knowledge/ | `knowledge/{category}/` |
| Raw ideas/scratch | info_temp/, docs/raw/ | inbox — chưa curate |
| Xem agent role | agents/ | `agents/*.md` |
| Lưu session/sự cố | .omc/sessions/ | runtime artifacts |
| Đọc architecture | architure.md | root hoặc docs/ nếu đã chuẩn hóa |

---

## Key Files

```yaml
critical_files:
  root_constitution:
    - CLAUDE.md              # LLM format standard
    - workspce_tree.md       # Workspace map (this file)
    - architure.md          # 3 Pillars, 7 Zones skill framework

  skill_factory_contracts:
    - skills/rebuild/_shared/knowledge/framework.md
    - skills/rebuild/_shared/schemas/
    - skills/rebuild/_shared/validators/

  active_skill_contexts:
    - .skill-context/skill-suite-upgrade/
    - .skill-context/skill-architect-v21/
    - .skill-context/skill-planner-v21/
    - .skill-context/prompt-cleaner/
    - .skill-context/session-learner/

  registry:
    - .skill-context/registry/README.md  # Skill status tracker
```

---

## Interaction Protocol

```yaml
agent_protocol:
  before_editing_skill:
    - Xác định skill đang ở zone nào (rebuild vs runtime vs raw)
    - Nếu là runtime (.hermes/skills/): edit ở rebuild rồi sync
    - Nếu là raw import: copy vào rebuild trước khi sửa
  before_creating_skill:
    - Tạo design.md trong .skill-context/{name}/
    - Tạo todo.md với task breakdown
    - Build vào skills/rebuild/{name}/
    - Sync vào .hermes/skills/ khi verified
  during_editing:
    - Preserve SKILL.md contract (frontmatter, sections)
    - Document build evidence trong build-log.md
    - Update registry khi status thay đổi
  before_final_response:
    - Verify routing map updated nếu có thay đổi structure
    - State what changed trong summary
```

---

## Confidence Assessment

```yaml
confidence: "95%"

basis:
  - Đã verify toàn bộ top-level directories
  - Đã verify skills/rebuild structure (canonical factory)
  - Đã verify .hermes/skills structure (installed runtime)
  - Đã verify .skill-context active contexts
  - Đã verify knowledge/ structure

uncertainties:
  - some raw skills in skills/raw/ may be duplicates or outdated
  - architure.md bị typo (nên rename later)
  - info_temp/ content chưa verified chi tiết
  - .omx/ state chưa explore đầy đủ

notes:
  - repos/ directory trống (placeholder?)
  - scripts/ chỉ có sync-skills.sh
```

---

## Open Questions

```yaml
open:
  - Steve cần confirm: runtime chính là Codex skills, Claude skills, hay cả hai?
  - architure.md nên rename → docs/architecture/skill-framework.md?
  - info_temp/ nên có rule cụ thể hơn (TTL, auto-cleanup)?
  - .omx/ directory purpose chưa rõ — cần Steve clarify
```

---

**Document status:** NO CODE CHANGES — Chỉ cập nhật workspace map
