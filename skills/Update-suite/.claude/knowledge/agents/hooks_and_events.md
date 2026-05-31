# Subagent Hooks & Lifecycle Events

This document details the configuration of lifecycle hooks, validation scripts, and custom events that execute during subagent initialization, runtime tool usage, and teardown.

---

## 1. Types of Hooks

Hooks can be configured at two levels: in the subagent's YAML frontmatter (scoped to that subagent) or in the project's `settings.json` (applied to all subagent actions).

### Hook Scopes & Execution

| Type | Defined in | Event Target | Scope of Effect |
| :--- | :--- | :--- | :--- |
| **Frontmatter Hooks** | Subagent Markdown file | `PreToolUse`, `PostToolUse`, `Stop` | Fires **only** when this specific subagent is running. |
| **Project/Global Hooks** | `.claude/settings.json` | `SubagentStart`, `SubagentStop` | Fires in the main session when **any** subagent starts or stops. |

> [!NOTE]
> `Stop` hooks defined in a subagent's frontmatter are automatically converted to `SubagentStop` events in the host process when the subagent exits.

---

## 2. Frontmatter Hook Syntax

Use the `hooks` object in your subagent's frontmatter. Matchers filters which tools trigger the hook.

```yaml
---
name: strict-reviewer
description: Review changes and enforce code styles
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "./scripts/validate-cmd.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: "command"
          command: "npm run lint"
---
```

---

## 3. Dynamic Tool Validation with PreToolUse

`PreToolUse` hooks are highly effective for fine-grained security validation. You can intercept a command, analyze it, and conditionally abort execution.

### Stdin Communication Protocol

When a hook executes, Claude Code passes details about the pending tool call as a JSON payload to the hook command's standard input (`stdin`).

```json
{
  "event": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules && npm install"
  },
  "agent_type": "strict-reviewer"
}
```

### Exit Code Rules

Your script should parse the JSON and exit with one of the following codes:
* `exit 0`: Validation passed. Allow the tool to execute.
* `exit 2`: Block execution. Aborts the tool call and returns the `stderr` string of the hook back to the AI.
* `exit 1` or other: Uncaught hook crash.

---

## 4. Script Example: Read-Only SQL Validator

This Bash script intercepts a subagent's Bash tool and blocks database-altering operations while allowing SELECT queries.

```bash
#!/bin/bash
# ./scripts/validate-readonly-query.sh

# Read JSON payload from stdin
INPUT=$(cat)

# Extract command using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Regex block for write/mutation commands (case-insensitive)
MUTATION_PATTERN='\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b'
if echo "$COMMAND" | grep -iE "$MUTATION_PATTERN" > /dev/null; then
  echo "Blocked: Only SELECT queries are permitted in this subagent." >&2
  exit 2
fi

exit 0
```

> [!TIP]
> Ensure the script is executable by running:
> `chmod +x ./scripts/validate-readonly-query.sh`

For Windows hosts running PowerShell, add `shell: powershell` inside the hook schema and design the script accordingly.

---

## 5. Project-Level Hooks (settings.json)

To trigger host processes when subagents run, add `SubagentStart` and `SubagentStop` configurations in `.claude/settings.json`.

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/open-tunnel.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/close-tunnel.sh" }
        ]
      }
    ]
  }
}
```
