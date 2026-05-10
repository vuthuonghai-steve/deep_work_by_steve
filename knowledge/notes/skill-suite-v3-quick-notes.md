# Skill Suite v3.0 — Quick Notes

**Date:** 2026-05-09
**Category:** notes

---

## Session Summary

Task: Upgrade skill suite (skill-architect, skill-planner, skill-builder) từ v2.x lên v3.0

**Kết quả đạt được:**
- 3 research files
- 3 design files
- 3 brainstorm files
- 6 proposal/idea files

---

## Key Achievements (Keywords)

1. **parallel delegation** — orchestrator pattern, 3 agents working simultaneously
2. **YAML-first validation** — frontmatter as canonical contract
3. **Hermes-native paths** — ~/.hermes/skills/ vs ~/.claude/skills/
4. **operation_type enum** — 6 types (create_new, patch_existing, etc.)
5. **execution_mode** — 3 modes (lightweight, standard, strict)
6. **install_target resolution** — 4 priority levels
7. **refinement_loop** — 6-step continuous improvement
8. **progressive_disclosure tiering** — 3-tier skill loading

---

## Session Flow

1. Read research evaluation doc và 3 skill files
2. Vòng 1: Delegate 3 agents (Claude Code, Codex + subagent) để brainstorm upgrade proposals
3. Read 4 proposal files từ vòng 1
4. Vòng 2: Delegate 3 nhóm agent (research, designs, brainstorm) để tạo documents
5. Results: 11 files created in docs/raw/{category}/

---

## Next Steps

- [ ] Implement v3.0 based on design documents
- [ ] Update skill files to match new architecture
- [ ] Test operation type workflows
- [ ] Validate YAML frontmatter contracts

---

## Ideas to Explore

- Auto-detection of operation type from git diff?
- Integration với Hermes Hub cho skill publishing
- Automated testing cho skill validation patterns

---

## Source

Session: skill-suite-upgrade-session
Knowledge entries created: 3 (experience, projects, programming)