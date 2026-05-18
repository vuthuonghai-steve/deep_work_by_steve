---
name: hello-world-writer
description: Writes "Hello World" string to a specified file path. Use when you need to create a simple text file with the content "Hello World".
---

> **Usage**: Write "Hello World" to a target file with verification.

## Workflow Progress Tracker

Copy this checklist into your response and mark progress:

```markdown
### [hello-world-writer] Progress:
- [ ] Phase 1: Validate Path
- [ ] Phase 2: Write Content
- [ ] Phase 3: Verify Write
```

---

## Phase 1: Validate Path

**Goal**: Ensure the target path is valid and writable.

1. Check if parent directory exists
2. Check write permissions
3. Confirm with user if file already exists (overwrite risk)

**Interaction Point**: Before writing, confirm with user:
- Target file path
- Whether to overwrite if file exists

---

## Phase 2: Write Content

**Goal**: Write "Hello World" to the target file.

**Action**: Use `write_file` tool to create the file with content:
```
Hello World
```

---

## Phase 3: Verify Write

**Goal**: Confirm the write was successful.

1. Read back the file to verify content
2. Report success or failure

---

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | Path Safety | Validate path does not traverse outside allowed directories |
| G2 | Permission Check | Verify write permissions before attempting write |
| G3 | Verify Success | Always read-back to confirm write succeeded |

---

## Examples

**Example 1 — Simple write:**
```
User: Write "Hello World" to /tmp/test.txt
Agent: 
1. Validates /tmp/ is writable
2. Writes "Hello World" to /tmp/test.txt
3. Reads back /tmp/test.txt to verify
4. Confirms: "✅ Written successfully"
```

**Example 2 — File exists:**
```
User: Write "Hello World" to /tmp/existing.txt
Agent:
1. Detects file exists
2. Asks: "File exists. Overwrite? [Y/N]"
3. User confirms
4. Writes and verifies
```
