# Boot Checklist — skill-suite-upgrade

> **Purpose**: Verify boot sequence is correct before proceeding to Phase 1

---

## Boot Sequence Verification

### Step 1: Read SKILL.md ✓
- [ ] SKILL.md exists in skill directory
- [ ] SKILL.md has YAML frontmatter
- [ ] SKILL.md has `progressive_disclosure` section

### Step 2: Run check_status.py ✓
```bash
python scripts/check_status.py .skill-context/{skill-name}/design.md
```
- [ ] Script exits with code 0
- [ ] JSON output has `phase`, `gates_passed`, `resume_from`
- [ ] If exit code != 0 → STOP and report error

### Step 3: Determine Position ✓

| phase value | Action |
|------------|--------|
| 0 | Fresh start — proceed to Phase 1 |
| 1-3 | Ask user: Resume or Restart? |
| 4 | Skill already complete — report |

### Step 4: Resume Flow (if phase > 0)
- [ ] Display last checkpoint info:
  - Last phase: {phase}
  - Gates passed: {gates_passed}
  - Last actor: {last_actor}
  - Last updated: {updated}
- [ ] Ask user: "Resume từ Phase {phase} hay bắt đầu mới?"
- [ ] If resume → load checkpoint and continue
- [ ] If restart → reset status and begin fresh

### Step 5: Load Tier 2 Files (Conditional)
Based on `progressive_disclosure` section:

| File | Trigger | Loaded? |
|------|---------|---------|
| `knowledge/case-system.md` | skill-name confirmed OR entering Phase 1 | [ ] |
| `knowledge/state-management.md` | boot OR resuming | [ ] |
| `scripts/check_status.py` | boot | [ ] |

### Step 6: Pre-Phase Check
- [ ] All Tier 1 files readable
- [ ] All required Tier 2 files exist
- [ ] design.md path determined
- [ ] Confidence level noted (from status block)

---

## Boot Complete

If all checkboxes pass → proceed to Phase 1.

If any checkbox fails → STOP and fix before proceeding.

---

## Exit Criteria

| Criterion | Pass | Fail |
|-----------|------|------|
| check_status.py runs successfully | ✅ | ❌ |
| Tier 2 files exist when triggered | ✅ | ❌ |
| User position confirmed | ✅ | ❌ |
