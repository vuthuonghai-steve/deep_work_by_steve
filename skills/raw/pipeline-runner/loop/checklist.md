# Pipeline Runner — Pre-Stage Checklist

> Based on design.md §8 Risks & Blind Spots

---

## Pre-Stage Verification

Before running each stage, verify:

### Dependency Check
- [ ] All dependencies in `depends_on` are marked COMPLETED in _queue.json
- [ ] No circular dependencies

### Validation Check
- [ ] Validation script exists (if specified)
- [ ] Expected exit code is defined
- [ ] Required outputs are listed

### State Check
- [ ] _queue.json is readable
- [ ] Backup exists (_queue.json.backup)
- [ ] Atomic write will be used

### Skill Check
- [ ] Skill exists in skills.yaml
- [ ] Skill path is valid
- [ ] Input files exist (if specified)

---

## Risk Mitigation Checklist

| Risk | Mitigation | Verified |
|------|------------|----------|
| Skill not found | Pre-flight check skills exist | [ ] |
| Validation bypass | Hard stop if exit code != 0 | [ ] |
| Context overflow | Sub-agent isolation | [ ] |
| State corruption | Atomic writes | [ ] |
| Checkpoint skip | Require --force to skip | [ ] |
| Infinite retry | Max retries cap | [ ] |

---

## Post-Stage Verification

After stage completes:

- [ ] Validation passed (exit code = 0)
- [ ] _queue.json updated with COMPLETED
- [ ] Output files exist
- [ ] Checkpoint pause (if configured)
