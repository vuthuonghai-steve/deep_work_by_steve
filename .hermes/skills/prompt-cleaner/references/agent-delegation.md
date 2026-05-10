# Agent Delegation Reference

## Running Claude Code as Subagent

### Via Terminal (Direct)
```bash
cd /home/steve/Work-space/deep_work_by_steve
claude-code --print "Your prompt here"
```

### Via delegate_task
```python
delegate_task(
  goal="Fix P1-05 typo",
  context="Working directory: ...",
  toolsets=["terminal", "file"]
)
```

## Claude Code flags
- `--print`: Non-interactive, output to stdout
- `--output-format json`: Machine-readable output
- `--no-input`: No user prompts

## Timeout Handling
- Default timeout is agent's internal timeout
- For long tasks: break into phases, verify after each
- If timeout occurs: check what was created with `find`, `git status`

## Verification Pattern
```bash
cd <workdir>
git status  # what changed
git diff   # actual changes
pytest tests/ -v  # run tests
```
