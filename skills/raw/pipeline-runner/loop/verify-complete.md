# Pipeline Runner — Post-Pipeline Verification

> Verification checklist after pipeline completes

---

## Completion Verification

### All Stages Complete
- [ ] All stages marked COMPLETED in _queue.json
- [ ] No stages marked FAILED
- [ ] No stages marked IN_PROGRESS

### Outputs Generated
- [ ] All required_outputs exist
- [ ] All validation scripts passed
- [ ] summary.md generated

### State Cleanup
- [ ] _queue.json shows final state
- [ ] No temporary files remain (.tmp)
- [ ] Backup files cleaned up

---

## Final Report Checklist

| Item | Status |
|------|--------|
| Pipeline name | [ ] |
| Total stages | [ ] |
| Completed stages | [ ] |
| Failed stages | [ ] |
| Total time | [ ] |
| Output paths | [ ] |

---

## Error Summary (if any)

| Stage | Error | Recovery Attempted |
|-------|-------|-------------------|
| | | |

---

## Next Steps

- [ ] User notified of completion
- [ ] Output paths provided to user
- [ ] Summary report accessible
