# Deep Work by Steve

## Project Purpose

Triển khai Hermes như **AI-first productivity platform** — không phải chatbot, mà là **AI agent skill suite** giúp khai thác và nâng cao khả năng của LLM.

**Định hướng:** Hướng tới câu hỏi — *Làm thế nào để sử dụng AI hiệu quả?*

**Con đường:** Cung cấp hệ thống **skill + knowledge + workflow** để điều hướng và giải quyết vấn đề.

### Core Principle: Heavy Thinking

Mọi agentic harness (Claude Code, CodeX, Hermes) đều dựa vào **một inner skill** — **Heavy Thinking** (arXiv:2605.02396):

```
Input → [Stage 1: Parallel Reasoning] → [Stage 2: Deliberation] → Output
              K independent chains            Synthesize
              (K = 8 hoặc 16)                 final answer
```

**Insight:** Orchestration layer (skills, memory, sub-agents) chỉ quản lý complexity. Performance gain thực sự đến từ **inner skill** — Heavy Thinking.

**Deliberator không cần mạnh nhất** — chỉ cần khả năng tổng hợp và bám hướng dẫn.

### Áp Dụng Trong Dự Án

Khi thiết kế skill mới:
1. **Skill architect** → design rõ input/output
2. **Skill planner** → chia thành task nhỏ
3. **Skill builder** → implement + validate
4. **Deep session learner** → capture durable lessons

Kiến thức nền tảng: `/home/steve/Work-space/deep_work_by_steve/knowledge/ai-agents/ai-agents.md`

## Local Hermes Skills

Project-local skills live at:

`/home/steve/Work-space/deep_work_by_steve/.hermes/skills`

Registered in global Hermes config via:

```yaml
skills:
  external_dirs:
    - /home/steve/Work-space/deep_work_by_steve/.hermes/skills
```

Primary skills:

- `prompt-cleaner` — clean raw Vietnamese/English prompts into structured Claude Code XML prompts.
- `deep-session-learner` — extract durable knowledge from the current session into a project knowledge base.
- `skill-architect` — stage 1 of the Master Skill Suite; design a new skill and produce `design.md`.
- `skill-planner` — stage 2; convert `design.md` into implementation `todo.md`.
- `skill-builder` — stage 3; implement/validate the skill from design + todo.
- `spec-generator-has-api` — generate validated feature specs: `api.json`, `business.md`, `flow.md`, `tasks.md`.

## Recommended Workflow

When Steve asks to create or improve an agent skill:

1. Use `skill-architect` to clarify intent and create the architecture/design.
2. Use `skill-planner` to derive concrete implementation tasks from the design.
3. Use `skill-builder` to implement the skill, validate quality gates, and produce build logs.
4. Use `deep-session-learner` after complex sessions to capture durable lessons.

## Local Skill Structure Convention

Each skill should prefer this structure:

```text
skill-name/
├── SKILL.md
├── knowledge/      # domain/process knowledge loaded when needed
├── templates/      # reusable output/input templates
├── scripts/        # validation or generation scripts
├── loop/           # checklists and recurring workflow loops
├── references/     # examples and larger reference material
├── data/           # YAML/JSON lookup tables, matrices, taxonomies
└── assets/         # static assets if needed
```

`SKILL.md` frontmatter should include at minimum:

```yaml
---
name: skill-name
description: Use when ...
version: "1.0.0"
author: "Steve Void Team"
license: private
metadata:
  hermes:
    tags: [relevant, tags]
    related_skills: []
---
```

## Important Notes for Hermes

- These are project-local skills, not bundled Hermes core skills.
- Do not assume new skills should be written to `~/.hermes/skills/` when the task is explicitly about this project; prefer this repository's `.hermes/skills/` tree.
- `_shared/` contains shared knowledge, schemas, fixtures, and validators used by the local skill suite. Keep it as `_shared` because existing `progressive_disclosure` paths reference `../_shared/...`.
- If a newly created local skill is not visible, run `/reload-skills` or restart Hermes.
- External skill directories are read-only from Hermes' automatic skill creation flow; manual file edits inside this project are OK.
