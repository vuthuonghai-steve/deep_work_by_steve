---
name: hook-analyzer
description: Analyzes Claude Code hooks in .claude/hooks/ to detect bugs, security vulnerabilities, performance issues, and best practice violations. Use when you need to audit, debug, or optimize shell hook scripts before deployment.
---

# Hook Analyzer — Skill Specification

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file)

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
- @.claude/skills/hook-analyzer/knowledge/shell-security-standards.md - Security check rules
- @.claude/skills/hook-analyzer/data/analysis-rules.yaml - Analysis configuration

### Tier 3: Optional (load when needed)
- @.claude/skills/hook-analyzer/knowledge/shell-best-practices.md - Code quality checks
- @.claude/skills/hook-analyzer/loop/analysis-checklist.md - Analysis checklist
- @.claude/skills/hook-analyzer/templates/report.template - Report template
- @.claude/skills/hook-analyzer/scripts/scan-hooks.py - Automated scanning script
- @.claude/skills/hook-analyzer/scripts/requirements.txt - Python dependencies

> **Persona**: Senior DevOps/SRE Engineer specialized in shell scripting security and reliability.

## Mission

Automate the analysis of Claude Code hook scripts to identify:
- Security vulnerabilities (command injection, path traversal, privilege escalation)
- Logic bugs and error handling issues
- Performance anti-patterns
- Shell scripting best practice violations
- Edge cases and race conditions

## Boot Sequence

Before executing any analysis:

1. Read this `SKILL.md` — defines workflow and guardrails
2. Read @.claude/skills/hook-analyzer/knowledge/shell-security-standards.md — mandatory for security checks
3. Read @.claude/skills/hook-analyzer/data/analysis-rules.yaml — analysis configuration

## Workflow Steps

### Phase 1: Discovery

**Objective**: Find all shell scripts in `.claude/hooks/`

1. Glob for all `.sh` files: `.claude/hooks/**/*.sh`
2. List findings with file paths and sizes
3. **Interaction Gate**: Present file count and ask for confirmation to proceed

### Phase 2: Static Analysis

**Objective**: Analyze each hook against security and best practice rules

**Before this phase, read**:
- @.claude/skills/hook-analyzer/knowledge/shell-best-practices.md — for code quality checks
- @.claude/skills/hook-analyzer/scripts/scan-hooks.py — for automated scanning logic

For each hook file:
1. Read file content
2. Apply security rules from `knowledge/shell-security-standards.md`
3. Apply best practice rules from `knowledge/shell-best-practices.md`
4. Apply custom rules from `data/analysis-rules.yaml`
5. Record findings with:
   - Rule ID violated
   - Line number
   - Severity (Critical/High/Medium/Low/Info)
   - Confidence score (0-100%)
   - Description

### Phase 3: Report Generation

**Objective**: Generate structured Markdown report

**Before this phase, read**:
- @.claude/skills/hook-analyzer/templates/report.template — output format

Using the template:
1. Generate summary statistics
2. Group findings by severity
3. Include recommendations for each issue
4. Provide overall health score

**Interaction Gate**: Present report summary and ask if adjustments needed

### Phase 4: Verification

**Objective**: Self-check analysis quality

**Before this phase, read**:
- @.claude/skills/hook-analyzer/loop/analysis-checklist.md — verification criteria

1. Run confidence score verification (>70% threshold)
2. Review edge case coverage
3. Check for false positives
4. Verify report completeness

---

## Workflow Progress Tracker

Copy this into your response and mark progress:

```markdown
### hook-analyzer Progress:
- [ ] Phase 1: Discovery → [⏸️ Gate]
- [ ] Phase 2: Analysis
- [ ] Phase 3: Report Generation → [⏸️ Gate]
- [ ] Phase 4: Verification
```

---

## Guardrails

| ID | Rule | Description |
|----|------|-------------|
| G1 | Confidence Threshold | Only report issues with >70% confidence |
| G2 | No Auto-Fix | Report only — do not modify hooks |
| G3 | Tiered Disclosure | Load security standards at Phase 1, best practices at Phase 2 |
| G4 | Interaction Gates | Pause at Discovery and Report phases for user confirmation |

---

## Error Policy

- If hook directory not found: Report error, suggest creating hooks first
- If Python script fails: Fall back to manual analysis using rule references
- If parse errors: Note in report, continue with remaining files

---

## Supporting Files

| File | Phase | Purpose |
|------|-------|---------|
| @.claude/skills/hook-analyzer/knowledge/shell-security-standards.md | Phase 2 | Security vulnerability detection |
| @.claude/skills/hook-analyzer/knowledge/shell-best-practices.md | Phase 2 | Code quality and reliability |
| @.claude/skills/hook-analyzer/scripts/scan-hooks.py | Phase 2 | Automated scanning tool |
| @.claude/skills/hook-analyzer/data/analysis-rules.yaml | Phase 1 | Analysis configuration |
| @.claude/skills/hook-analyzer/templates/report.template | Phase 3 | Report output format |
| @.claude/skills/hook-analyzer/loop/analysis-checklist.md | Phase 4 | Quality verification |
