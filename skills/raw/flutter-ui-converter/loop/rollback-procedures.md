# Rollback Procedures

Emergency procedures for reverting changes when conversion fails.

---

## Overview

Rollback capability exists for each phase. Use appropriate procedure based on where failure occurred.

---

## Phase 1 Rollback — Analysis

**Trigger**: Analysis is incorrect, incomplete, or user rejects approach.

### Rollback Steps

1. **Delete analysis outputs**
   ```bash
   rm -rf .skill-context/flutter-ui-converter/session-{timestamp}/analysis/*
   rm -rf .skill-context/flutter-ui-converter/session-{timestamp}/mappings/*
   ```

2. **Reset context status**
   - Edit `conversion-context.yaml`
   - Set `status: initialized`
   - Set `phase: analysis`

3. **Re-run analysis**
   - Provide the Agent with the target and source paths.
   - Instruct the Agent to re-run Phase 1 Analysis according to `SKILL.md`.
   - The Agent will use `grep_search` and `view_file` to perform the analysis manually.

### Data Preserved

- Session context metadata
- Source and target snapshots
- Backup directory (empty at this phase)

### Impact

- **Low** - No code changes made yet
- Only analysis documents affected

---

## Phase 2 Rollback — Code Generation

**Trigger**: Generated code has bugs, breaks logic, or doesn't compile.

### Rollback Steps

1. **Identify backup timestamp**
   ```bash
   python scripts/backup_manager.py --action list --context .skill-context/flutter-ui-converter/session-{timestamp}/
   ```

2. **Restore from backup**
   ```bash
   python scripts/backup_manager.py \
     --action restore \
     --context .skill-context/flutter-ui-converter/session-{timestamp}/ \
     --backup-id {backup-timestamp}
   ```

3. **Verify restoration**
   ```bash
   git diff  # Should show restored files
   flutter analyze  # Should pass
   ```

4. **Review conversion log**
   - Open `conversion-log.md`
   - Identify root cause of failure
   - Document in `known-issues.yaml`

5. **Update guardrails** (if needed)
   - Add validation rule to catch this issue
   - Review and update `data/forbidden-patterns.yaml` if a new forbidden pattern was discovered

6. **Re-run Phase 2** (with fixes)
   - Apply lessons learned
   - Re-generate code with corrections
   - Re-run validation

### Data Preserved

- Original target files (in backup)
- Conversion log (for analysis)
- Analysis documents from Phase 1

### Impact

- **Medium** - Code changes reverted
- Time lost on failed conversion
- Knowledge gained for future conversions

---

## Phase 3 Rollback — Feedback Loop

**Trigger**: User wants to undo feedback submission (e.g., false positive error report).

### Rollback Steps

1. **Edit conversion log**
   - Open `.skill-context/flutter-ui-converter/session-{timestamp}/conversion-log.md`
   - Remove incorrect issue entries
   - Save changes

2. **Re-run feedback extraction**
   - The Agent manually analyzes the `conversion-log.md`.
   - The Agent updates `data/known-issues.yaml` based on findings.

3. **Verify knowledge base**
   - Check `data/known-issues.yaml`
   - Ensure incorrect issue not added
   - If added, manually remove

4. **Regenerate pattern library**
   - Check `data/pattern-library.yaml`
   - Remove any patterns based on incorrect feedback

### Data Preserved

- Previous version of `known-issues.yaml` (versioned)
- Previous version of `pattern-library.yaml` (versioned)

### Impact

- **Low** - Only knowledge base affected
- No code changes
- Prevents skill from learning incorrect patterns

---

## Emergency Rollback (Any Phase)

**Trigger**: Critical bug detected in skill logic (e.g., G1 guardrail failed → business logic modified).

### Immediate Actions

1. **STOP immediately**
   - Do not output any more code
   - Do not make any more changes

2. **Restore backups** (if Phase 2 or later)
   ```bash
   python scripts/backup_manager.py \
     --action restore \
     --context .skill-context/flutter-ui-converter/session-{timestamp}/ \
     --backup-id {latest-backup}
   ```

3. **Notify user**
   - Use **AskUserQuestion** tool
   - Explain critical issue detected
   - Provide details of what went wrong
   - Apologize for the error

4. **Log incident**
   - Add to `data/known-issues.yaml` with `severity: CRITICAL`
   - Document exact failure scenario
   - Include steps to reproduce

5. **Enter safe mode**
   - Skill only runs Phase 1 (analysis only)
   - No code generation until bug fixed
   - Update `SKILL.md` with safe mode notice

### Recovery Steps

1. **Identify root cause**
   - Review conversion log
   - Review validation report
   - Identify which guardrail failed

2. **Fix skill logic**
   - Update validation rules
   - Update guardrail checks
   - Update knowledge files

3. **Test fix**
   - Create test case for this scenario
   - Verify fix prevents recurrence
   - Document in skill documentation

4. **Exit safe mode**
   - Remove safe mode notice from `SKILL.md`
   - Update `known-issues.yaml` with fix
   - Resume normal operations

### Data Preserved

- All backups
- All logs and analysis
- Incident report in known-issues.yaml

### Impact

- **CRITICAL** - Potential data loss prevented
- Skill temporarily disabled for code generation
- User trust affected - must rebuild confidence

---

## Rollback Decision Matrix

| Scenario | Phase | Rollback Type | Impact | Recovery Time |
|----------|-------|---------------|--------|---------------|
| Analysis incorrect | 1 | Phase 1 | Low | 15-30 min |
| Code doesn't compile | 2 | Phase 2 | Medium | 30-60 min |
| Logic broken | 2 | Emergency | Critical | 1-2 hours |
| False feedback | 3 | Phase 3 | Low | 5-10 min |
| Skill bug detected | Any | Emergency | Critical | 2-4 hours |

---

## Prevention Best Practices

### Before Phase 2

- [ ] Thoroughly review Phase 1 analysis
- [ ] Get explicit user approval
- [ ] Verify all guardrails understood

### During Phase 2

- [ ] Create backup BEFORE any changes
- [ ] Run validation AFTER code generation
- [ ] Test incrementally (don't change everything at once)

### After Phase 2

- [ ] User tests before marking complete
- [ ] Document any issues immediately
- [ ] Extract feedback promptly

---

## Rollback Checklist

When performing rollback:

- [ ] Identify rollback type needed
- [ ] Follow appropriate procedure above
- [ ] Verify restoration successful
- [ ] Document root cause
- [ ] Update knowledge base
- [ ] Notify user of status
- [ ] Plan corrective action
- [ ] Test fix before retry

---

## Contact & Support

If rollback procedures fail or critical bug detected:

1. Stop all operations
2. Preserve all logs and backups
3. Document exact state
4. Notify user immediately
5. Escalate to skill maintainer

---

**Remember**: Rollback is a safety feature, not a failure. It's better to rollback and retry than to push forward with broken code.
