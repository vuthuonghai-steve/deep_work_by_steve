# Subagent Configuration Reference

This document outlines the scopes, directory locations, YAML frontmatter configuration, and model preferences for custom subagents in Claude Code.

<context>
Subagents are defined in Markdown files with YAML frontmatter. Store them in different locations depending on the desired scope. When multiple subagents share the same name, the higher-priority location wins.
</context>

## 1. Subagent Scopes & Discovery

```yaml
scopes_and_precedence:
  - scope: "Managed settings"
    location: "Deployed via organization-wide settings files"
    priority: 1 # Highest
    shareability: "Organization-wide"

  - scope: "CLI flag"
    location: "Passed as a JSON string to `claude --agents`"
    priority: 2
    shareability: "Session-only (for automation/scripting)"

  - scope: "Project subagents"
    location: "Project root: `.claude/agents/`"
    priority: 3
    shareability: "Shareable via git version control"
    note: "Discovered recursively walking up from CWD. `--add-dir` directories are ignored."

  - scope: "User subagents"
    location: "Home directory: `~/.claude/agents/`"
    priority: 4
    shareability: "Personal, available in all local projects"
    note: "Scanned recursively."

  - scope: "Plugin subagents"
    location: "Inside plugin package: `agents/`"
    priority: 5 # Lowest
    shareability: "Distributed with the plugin"
    note: "Identifier is scoped by plugin name (e.g., `my-plugin:code-reviewer`)."
```

---

## 2. Writing Subagent Files

Subagent Markdown files must begin with a YAML frontmatter block, followed by the system prompt in Markdown.

### Example File Casing

```markdown
---
name: code-reviewer
description: Reviews code for quality, performance, and security
tools: Read, Glob, Grep
model: sonnet
---

You are a senior code reviewer. When invoked, analyze the code changes and provide
specific, actionable feedback on quality, security, and best practices.
```

> [!NOTE]
> Subagents are loaded at session startup. If you edit or add a subagent file directly on disk, you must restart the Claude Code session to apply the changes. Subagents created through the `/agents` interface take effect immediately without a restart.

---

## 3. Supported Frontmatter Schema

All custom subagent configurations must match the following schema.

```yaml
frontmatter_schema:
  name:
    type: "string (lowercase and hyphens only)"
    required: true
    description: "Unique identifier. Hooks receive this value as `agent_type`."
  description:
    type: "string"
    required: true
    description: "Tells Claude when to delegate to this subagent. Write a clear, proactive description."
  tools:
    type: "string | array"
    required: false
    description: "Allowlist of tools. Inherits all tools if omitted. Preload Skills with the 'skills' field rather than listing them here."
  disallowedTools:
    type: "string | array"
    required: false
    description: "Denylist of tools to exclude from the inherited or specified list."
  model:
    type: "string"
    required: false
    description: "Model alias (sonnet, haiku, opus), full ID, or 'inherit'. Defaults to 'inherit'."
  permissionMode:
    type: "string"
    required: false
    options: ["default", "acceptEdits", "auto", "dontAsk", "bypassPermissions", "plan"]
    description: "Overrides parent permissions. Ignored for plugin subagents."
  maxTurns:
    type: "integer"
    required: false
    description: "Maximum agentic turns allowed before the subagent stops."
  skills:
    type: "array of strings"
    required: false
    description: "List of custom skills to preload into the subagent's context window."
  mcpServers:
    type: "array"
    required: false
    description: "MCP servers scoped strictly to this subagent (inline definition or string reference)."
  hooks:
    type: "object"
    required: false
    description: "Lifecycle hooks (PreToolUse, PostToolUse, Stop) scoped to this subagent."
  memory:
    type: "string"
    required: false
    options: ["user", "project", "local"]
    description: "Enables cross-session learning for this subagent."
  background:
    type: "boolean"
    required: false
    default: false
    description: "If true, runs this subagent as a concurrent background task."
  effort:
    type: "string"
    required: false
    options: ["low", "medium", "high", "xhigh", "max"]
    description: "Effort level. Defaults to inheriting the main session."
  isolation:
    type: "string"
    required: false
    options: ["worktree"]
    description: "Runs the subagent in an isolated git worktree rather than your current checkout."
  color:
    type: "string"
    required: false
    options: ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]
    description: "UI display color for the subagent's transcript."
  initialPrompt:
    type: "string"
    required: false
    description: "Automatically submitted as the first turn when this agent runs as the main session."
```

---

## 4. Model Configuration

Subagents can target specific models or inherit the active session model.

```yaml
model_resolution_order:
  1: "The `CLAUDE_CODE_SUBAGENT_MODEL` environment variable (if set)"
  2: "The per-invocation `model` parameter passed by Claude"
  3: "The subagent frontmatter `model` definition"
  4: "The main conversation model"
```

### Supported Aliases
- `sonnet`: Balanced capability and speed (e.g., standard code reviews).
- `haiku`: Fast, low-latency (e.g., simple exploration).
- `opus`: High reasoning (e.g., complex debugging).
- `inherit`: Inherits the active model of the parent conversation.
