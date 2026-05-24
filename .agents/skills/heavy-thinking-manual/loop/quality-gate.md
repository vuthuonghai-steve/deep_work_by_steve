# Quality Gate — Pre-Implementation Verification

## Purpose

This checklist ensures Heavy Thinking analysis is complete and ready for implementation. All items must pass before proceeding.

---

## Quality Gate Checklist

### Category: CONTEXT

| ID | Item | Criteria | Status | Evidence |
|----|------|----------|--------|----------|
| CONTEXT-1 | Hermes Memory loaded | Status = loaded or partial | _ | Source status in context-sources.json |
| CONTEXT-2 | Session History loaded | Status = loaded or partial | _ | Source status in context-sources.json |
| CONTEXT-3 | Project Files loaded | Status = loaded or partial | _ | Source status in context-sources.json |
| CONTEXT-4 | No critical sources unavailable | All critical sources = loaded | _ | Audit summary |
| CONTEXT-5 | Context size within limits | Each source ≤ 50KB | _ | Size bytes in context-sources.json |
| CONTEXT-6 | Gap analysis completed | All gaps identified | _ | Gap analysis in context-sources.json |

### Category: CHAINS

| ID | Item | Criteria | Status | Evidence |
|----|------|----------|--------|----------|
| CHAINS-1 | K=8 chains executed | All 8 chains have findings | _ | chain_count = 8 |
| CHAINS-2 | No chain contamination | No cross-chain references | _ | Chain isolation verified |
| CHAINS-3 | All chains completed | All status = complete | _ | Chain statuses |
| CHAINS-4 | Chain timeout handled | No chain exceeded 5 min | _ | Execution times |
| CHAINS-5 | Task-type augmentation applied | Extra chain if applicable | _ | chain_count |
| CHAINS-6 | Isolation enforced | Level 1 isolation followed | _ | Isolation log |

### Category: DELIBERATION

| ID | Item | Criteria | Status | Evidence |
|----|------|----------|--------|----------|
| DELIB-1 | Findings aggregated | All chain findings collected | _ | Total findings count |
| DELIB-2 | Consensus identified | Consensus levels assigned | _ | Consensus map |
| DELIB-3 | Conflicts resolved | All conflicts documented | _ | Conflicts resolved |
| DELIB-4 | CORE problems identified | 3-5 CORE problems | _ | Core problems count |
| DELIB-5 | CASE system applied | PREVENT/DETECT/RECOVER filled | _ | CASE analysis present |
| DELIB-6 | No unresolved major conflicts | All major conflicts resolved | _ | Unresolved conflicts |

### Category: OUTPUT

| ID | Item | Criteria | Status | Evidence |
|----|------|----------|--------|----------|
| OUTPUT-1 | Task ID valid | Pattern: {date}-{keyword}-{uuid} | _ | task_id field |
| OUTPUT-2 | All files created | All 7 files present | _ | File existence check |
| OUTPUT-3 | task-meta.yaml valid | Schema validation pass | _ | Schema validation |
| OUTPUT-4 | context-sources.json valid | Schema validation pass | _ | Schema validation |
| OUTPUT-5 | analysis-chains.md complete | All chain findings present | _ | Chain count |
| OUTPUT-6 | deliberation.md complete | All sections present | _ | Section check |
| OUTPUT-7 | prepared-context.json valid | Schema validation pass | _ | Schema validation |
| OUTPUT-8 | diagrams.mmd valid | Mermaid syntax valid | _ | Mermaid render |
| OUTPUT-9 | checklist.yaml valid | Schema validation pass | _ | Schema validation |

### Category: QUALITY

| ID | Item | Criteria | Status | Evidence |
|----|------|----------|--------|----------|
| QUAL-1 | Confidence level assigned | high/medium/low | _ | Confidence field |
| QUAL-2 | Implementation blockers identified | Blocker list present | _ | Blockers field |
| QUAL-3 | Ready for implementation | ready_for_implementation = true | _ | Flag |
| QUAL-4 | User interaction points satisfied | All IPs completed | _ | IP log |

---

## Quality Gate Summary

```
Total Items: ___
Passed: ___
Failed: ___
Pending: ___
Pass Rate: ___%

Status: [ ] PASS  [ ] FAIL  [ ] REVIEW REQUIRED
```

---

## Failure Actions

| If | Then |
|----|------|
| CONTEXT items fail | Request user to provide missing context |
| CHAINS items fail | Regenerate chains with fixes |
| DELIB items fail | Re-run deliberation |
| OUTPUT items fail | Regenerate output with schema fixes |
| QUAL items fail | Address blockers before proceeding |

---

## Sign-off

```
Analyst: ________________
Date: ________________
Status: [ ] APPROVED  [ ] REJECTED

Notes: ________________
```
