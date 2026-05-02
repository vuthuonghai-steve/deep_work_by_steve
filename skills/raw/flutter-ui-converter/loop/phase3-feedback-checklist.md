# Phase 3: Feedback Loop & Learning Checklist

Use this checklist when user reports issues or after successful conversion.

---

## 1. Feedback Collection

### If Issues Reported

- [ ] User described the issue clearly
- [ ] Issue categorized:
  - [ ] UI bug (visual mismatch)
  - [ ] Logic break (state not updating)
  - [ ] Asset missing (image not found)
  - [ ] Dependency conflict (package error)
  - [ ] Compilation error (syntax/type error)
  - [ ] Runtime error (crash/exception)
  - [ ] Other: _______________

- [ ] Issue severity assessed:
  - [ ] Critical (app crashes, logic broken)
  - [ ] High (feature unusable)
  - [ ] Medium (visual bug, workaround exists)
  - [ ] Low (minor cosmetic issue)

- [ ] Issue logged in `conversion-log.md` under "Issues to Report"

### If Success Reported

- [ ] User confirmed screen works correctly
- [ ] All interactions tested
- [ ] No visual bugs
- [ ] State management working
- [ ] Assets displaying correctly

---

## 2. Error Analysis

### For Each Issue

- [ ] Root cause identified
- [ ] Related to which guardrail (if any)?
  - [ ] G1: UI-Only Changes
  - [ ] G2: Zero New Dependencies
  - [ ] G3: Logic Hook Preservation
  - [ ] G4: Asset Mapping
  - [ ] G5: i18n Compliance
  - [ ] None (new issue type)

- [ ] Could this have been caught earlier?
  - [ ] Yes → Suggest validation rule
  - [ ] No → Document as edge case

- [ ] Is this a recurring pattern?
  - [ ] Check `data/known-issues.yaml`
  - [ ] If new pattern, add to known issues

---

## 3. Pattern Extraction

### Pattern Extraction Execution

- [ ] Analyze the feedback documented in `conversion-log.md`
- [ ] Identify recurring issues and successful fixes
- [ ] Update `data/known-issues.yaml`
- [ ] Update `data/pattern-library.yaml`

### Manual Pattern Review

- [ ] Review extracted patterns for accuracy
- [ ] Add context/notes if needed
- [ ] Assign pattern IDs
- [ ] Mark patterns as reusable or one-off

---

## 4. Knowledge Base Updates

### If New Issue Type Found

- [ ] Add to `data/known-issues.yaml`:
  - Issue ID
  - Category
  - Description
  - Severity
  - Mitigation strategy
  - Affected widgets

- [ ] Consider updating knowledge files:
  - [ ] `knowledge/conversion-rules.md` (if rule violated)
  - [ ] `knowledge/component-mapping-guide.md` (if mapping issue)
  - [ ] `knowledge/asset-management.md` (if asset issue)
  - [ ] `knowledge/state-management-preservation.md` (if Bloc issue)
  - [ ] Other: _______________

### If Successful Pattern Found

- [ ] Add to `data/pattern-library.yaml`:
  - Pattern ID
  - Name
  - Category
  - Description
  - Example code
  - Success rate
  - Reusable flag

---

## 5. Improvement Suggestions

### AI-Generated Suggestions

- [ ] Agent reviews conversion log and identifies potential process improvements
- [ ] Prioritize suggestions:
  - [ ] High priority (prevents critical issues)
  - [ ] Medium priority (improves quality)
  - [ ] Low priority (nice to have)

### Manual Suggestions

- [ ] Validation rules to add
- [ ] Knowledge files to enhance
- [ ] Script improvements needed
- [ ] Template updates needed
- [ ] Guardrail adjustments needed

**Document in**:
- [ ] `.skill-context/flutter-ui-converter/improvement-suggestions.md`

---

## 6. Skill Evolution Tracking

### Metrics to Track

- [ ] Total conversions performed: ___
- [ ] Success rate: ____%
- [ ] Average issues per conversion: ___
- [ ] Most common issue category: ___
- [ ] Most successful pattern: ___

### Trend Analysis

- [ ] Are issues decreasing over time?
- [ ] Are certain issue types recurring?
- [ ] Are validation rules effective?
- [ ] Are knowledge files comprehensive?

---

## 7. User Communication

### If Issues Found

- [ ] Acknowledge issues
- [ ] Explain root cause (if known)
- [ ] Provide fix or workaround
- [ ] Estimate time to fix
- [ ] Ask if user wants to:
  - [ ] Rollback and retry
  - [ ] Fix manually
  - [ ] Continue with workaround

### If Success

- [ ] Congratulate user
- [ ] Ask for feedback on process
- [ ] Ask if anything was unclear
- [ ] Ask for suggestions to improve skill

---

## 8. Session Closure

- [ ] All issues resolved or documented
- [ ] Feedback extracted and stored
- [ ] Knowledge base updated
- [ ] Improvement suggestions documented
- [ ] Session marked as complete in `conversion-context.yaml`

**Update context**:
```yaml
status: completed
phase: feedback_complete
completed_at: {timestamp}
outcome: success | partial_success | failed
issues_count: {count}
patterns_extracted: {count}
```

---

## 9. Continuous Improvement

### For Next Conversion

- [ ] Review known-issues.yaml before starting
- [ ] Apply lessons learned
- [ ] Use successful patterns from pattern-library.yaml
- [ ] Avoid known pitfalls

### Skill Maintenance

- [ ] Schedule periodic review of knowledge files
- [ ] Update examples with real conversion cases
- [ ] Refine validation rules based on feedback
- [ ] Enhance scripts based on usage patterns

---

## Completion Criteria

✅ **Phase 3 is complete when**:
- All checkboxes above are marked
- Feedback extracted and stored
- Knowledge base updated
- Improvement suggestions documented
- User satisfied with outcome or issues resolved

---

**Session Complete** 🎉

**Next Steps**:
- Archive session for reference
- Apply learnings to next conversion
- Update skill documentation if needed
