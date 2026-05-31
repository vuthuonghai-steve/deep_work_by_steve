# Conversation Forks (Experimental)

This document details the functionality, differences, panel controls, and optimization strategies for conversation forks in Claude Code.

> [!NOTE]
> Forked subagents are experimental and require **Claude Code v2.1.117 or later**. Enable them by setting the environment variable:
> `CLAUDE_CODE_FORK_SUBAGENT=1`

---

## 1. What is a Conversation Fork?

Unlike standard named subagents that start with a clean context, a **fork** inherits the **entire conversation history, system prompt, toolset, and active model** of the parent session at the moment of spawning.

### When to Use a Fork
* When you want a subagent to take on a side task without repeating context or re-explaining the codebase state.
* When you want to attempt multiple distinct refactoring strategies in parallel from a shared checkpoint.
* When a standard named subagent would require too much setup context to perform a simple task.

---

## 2. Fork Mechanics & Behaviors

Enabling `CLAUDE_CODE_FORK_SUBAGENT=1` alters Claude Code behavior in three main ways:

```yaml
fork_behaviors:
  general_purpose_override:
    description: "Claude automatically spawns a fork whenever it would otherwise delegate to the general-purpose subagent. Named subagents (e.g. Explore) remain unchanged."
  background_by_default:
    description: "Every subagent spawn (fork or named) runs in the background. You can restrict this to synchronous runs by setting `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`."
  command_registration:
    description: "The `/fork <directive>` command spawns a custom background fork rather than acting as an alias for `/branch`."
    syntax: "/fork draft unit tests for the parser changes so far"
```

---

## 3. Forks vs. Named Subagents

| Feature | Forked Subagent | Named Subagent |
| :--- | :--- | :--- |
| **Context Window** | Full conversation history at spawn time. | Fresh context window containing only the active task. |
| **System Prompt & Tools** | Identical to the main parent session. | Declared in the subagent's [definition file](configuration.md). |
| **Model** | Same model as the active main session. | Specified in the subagent's `model` frontmatter. |
| **Permissions** | Prompts are passed through and surfaced in the host terminal. | Auto-denies permission prompts (runs with pre-granted tokens). |
| **Prompt Cache** | Reuses the parent's active prompt cache. | Uses a separate, isolated cache. |
| **File Isolation** | Supports `isolation: "worktree"` to isolate edits in a git worktree. | Uses the current working directory of the main workspace. |

---

## 4. Prompt Cache Optimization

Because a fork's system prompt, tools, and message history are completely identical to the parent session at the time of fork creation, its initial turn reuses the parent's **Prompt Cache**.
* **Financial Advantage**: This makes spawning forks significantly cheaper and faster than starting a named subagent, which must rebuild and cache its own distinct context window from scratch.

---

## 5. Observing & Steering Forks

Running forks are listed in a concurrent interactive panel below the primary terminal prompt input.

### Panel Controls

| Key | Action |
| :--- | :--- |
| `↑` / `↓` | Navigate between running background fork rows. |
| `Enter` | Expand the selected fork's transcript and send follow-up steering prompt messages. |
| `x` | Dismiss a completed fork or terminate an active, runaway fork. |
| `Esc` | Return terminal cursor focus to the primary prompt input line. |
