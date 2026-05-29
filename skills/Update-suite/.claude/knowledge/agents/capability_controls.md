# Subagent Capability Controls

This document details the methods used to manage, restrict, and extend the capabilities of subagents through tools, permission overrides, custom skills, and persistent memories.

---

## 1. Tool Access Controls

Subagents inherit all internal tools and active MCP tools from the main session by default. 

### Unavailable Tools
The following tools depend on the active UI or session-wide state and are **never** available to subagents:
* `Agent` (cannot spawn nested subagents)
* `AskUserQuestion`
* `EnterPlanMode`
* `ExitPlanMode` (unless the subagent is in plan mode)
* `ScheduleWakeup`
* `WaitForMcpServers`

### Restricting Tools
Use `tools` (allowlist) or `disallowedTools` (denylist) in frontmatter to control access:

```yaml
tool_resolution_rules:
  allowlist_only:
    tools: ["Read", "Grep", "Glob", "Bash"]
    outcome: "Subagent can only use these 4 tools; cannot edit/write files."
  denylist_only:
    disallowedTools: ["Write", "Edit"]
    outcome: "Subagent inherits all tools except Write and Edit."
  combined:
    disallowed_applied_first: true
    rule: "If a tool is in both lists, it is denied."
```

### Spawning Control
To restrict what subagents a session-level agent can spawn, use the `Agent(agent_type)` syntax in the parent's `tools` list:
* `tools: Agent(worker, researcher)` -> Only allow spawning these two custom subagents.
* `tools: Agent` -> Allow spawning any subagent.
* (Omitted) -> The agent cannot spawn any subagents.

---

## 2. Permission Modes & Overrides

The `permissionMode` field dictates how permission prompts are handled inside the subagent context.

| Mode | Behavior |
| :--- | :--- |
| `default` | Standard interactive permission checking with user prompts. |
| `acceptEdits` | Auto-accepts file edits and filesystem commands in allowed workspace directories. |
| `auto` | Commands and writes are vetted silently in the background by an auto-classifier. |
| `dontAsk` | Auto-denies all permission prompts (explicitly allowed tools still run). |
| `bypassPermissions` | Skips all permission prompts (warning: allows deep writes without approval). |
| `plan` | Plan mode; executes read-only exploration and blocks modifications. |

> [!WARNING]
> If the parent session is set to `bypassPermissions`, `acceptEdits`, or `auto`, the parent's mode takes absolute precedence and the subagent's `permissionMode` is ignored.

---

## 3. Scoping MCP Servers

You can register MCP servers that are accessible **only** to a specific subagent. This avoids polluting the main conversation's tool list and keeps context windows clean.

```yaml
mcp_scoping_patterns:
  inline_definition:
    description: "Server is started when subagent opens, and killed when it stops."
    syntax:
      - playwright:
          type: "stdio"
          command: "npx"
          args: ["-y", "@playwright/mcp@latest"]
  named_reference:
    description: "Reuses an existing, configured MCP server from the parent session."
    syntax:
      - "github"
```

---

## 4. Preloading Skills

The `skills` frontmatter field preloads the **entire content** (not just descriptions) of specified skills into the subagent's startup context.

```yaml
skills_policy:
  preloading:
    field: "skills"
    example: ["api-conventions", "error-handling-patterns"]
    benefit: "Saves agentic turns by injecting domain rules directly without discovery loops."
  runtime_access:
    discovery: "Unless the 'Skill' tool is disallowed, subagents can still discover and invoke other workspace skills at runtime."
```

---

## 5. Persistent Memory System

Subagents can have a dedicated persistent folder that survives across conversation sessions.

```yaml
memory_scopes:
  user:
    location: "~/.claude/agent-memory/<agent-name>/"
    use_case: "Broad learnings that span multiple completely unrelated projects."
  project:
    location: ".claude/agent-memory/<agent-name>/"
    use_case: "Conventions and learnings checked into git, shared with the team."
  local:
    location: ".claude/agent-memory-local/<agent-name>/"
    use_case: "Project-specific learnings kept local (excluded from version control)."
```

### Memory Rules & Mechanics
* **System Prompt Injection**: When memory is active, the first 200 lines or 25KB of `MEMORY.md` in the memory folder is auto-loaded into the system prompt.
* **Auto Tool Activation**: `Read`, `Write`, and `Edit` tools are automatically enabled for the subagent to update memory files.
* **Size Management**: The subagent is instructed to keep `MEMORY.md` curated. If it exceeds 25KB, the agent must condense/summarize older entries.
* **Steering Patterns**:
  * *Proactive Consult*: "Run code-reviewer, and check your memory for patterns you've seen before."
  * *Proactive Save*: "Save what you learned from this fix into your memory."
