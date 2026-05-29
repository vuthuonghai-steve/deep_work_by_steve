# Gate Checklist — skill-suite-upgrade

> **Purpose**: Define exit criteria for each gate
> **Usage**: AI self-validates before requesting user confirmation

---

## Gate 1: Problem Statement

### Exit Criteria

| # | Criterion | Check |
|---|-----------|-------|
| 1.1 | §1 Problem Statement exists | [ ] File section not empty |
| 1.2 | §1 has ≥50 words | [ ] Word count >= 50 |
| 1.3 | §1 mentions Problem | [ ] "problem" or "vấn đề" found |
| 1.4 | §1 mentions User | [ ] "user" or "người" found |
| 1.5 | §1 mentions Reason | [ ] "reason" or "lý do" found |
| 1.6 | skill_name is kebab-case | [ ] No spaces, no underscores |
| 1.7 | confidence >= 70% OR explicitly declared lower | [ ] In status block |

### Self-Verification Command
```bash
python scripts/validate_gate.py .skill-context/{skill-name}/design.md --gate 1
```

### Gate 1 Failures → STOP
- §1 empty or < 50 words
- Missing Problem/User/Reason
- skill_name not kebab-case

---

## Gate 2: Capability Map + Zone Mapping

### Exit Criteria

| # | Criterion | Check |
|---|-----------|-------|
| 2.1 | §2 Capability Map exists | [ ] Not empty |
| 2.2 | §2 has Pillar 1 (Knowledge) | [ ] "Pillar 1" or "Knowledge" found |
| 2.3 | §2 has Pillar 2 (Process) | [ ] "Pillar 2" or "Process" found |
| 2.4 | §2 has Pillar 3 (Guardrails) | [ ] "Pillar 3" or "Guardrails" found |
| 2.5 | §3 Zone Mapping exists | [ ] Table with '\|' found |
| 2.6 | §3 has Core zone | [ ] "core" found in Zone column |
| 2.7 | §3 no empty cells | [ ] No '—' or empty cells |
| 2.8 | §8 has ≥3 risks | [ ] At least 3 risk entries |
| 2.9 | Status block updated | [ ] gates_passed includes 1 |

### Self-Verification Command
```bash
python scripts/validate_zone_mapping.py .skill-context/{skill-name}/design.md
python scripts/validate_gate.py .skill-context/{skill-name}/design.md --gate 2
```

### Gate 2 Failures → STOP
- Missing any Pillar
- Zone Mapping table incomplete
- Empty cells in Zone Mapping
- Less than 3 risks

---

## Gate 3: Design + Diagrams

### Exit Criteria

| # | Criterion | Check |
|---|-----------|-------|
| 3.1 | §4 Folder Structure exists | [ ] Not empty |
| 3.2 | §4 has Mermaid mindmap | [ ] "mermaid" and "mindmap" found |
| 3.3 | §5 Execution Flow exists | [ ] Not empty |
| 3.4 | §5 has Mermaid sequenceDiagram | [ ] "mermaid" and "sequence" found |
| 3.5 | §6 Interaction Points exists | [ ] Not empty |
| 3.6 | §6 has ≥1 interaction point | [ ] Table with entries |
| 3.7 | §7 Progressive Disclosure exists | [ ] Not empty |
| 3.8 | §7 has Tier 1 defined | [ ] "Tier 1" or "mandatory" found |
| 3.9 | §7 has Tier 2 defined | [ ] "Tier 2" or "conditional" found |
| 3.10 | Status block updated | [ ] gates_passed includes 2 |

### Self-Verification Command
```bash
python scripts/validate_gate.py .skill-context/{skill-name}/design.md --gate 3
```

### Gate 3 Failures → STOP
- Missing required diagrams
- Interaction Points empty
- Progressive Disclosure incomplete

---

## Validation Summary

### Before User Confirmation (AI Self-Check)

```
1. Run: python scripts/validate_gate.py <design_path> --gate N
2. If exit code != 0 → Fix issues first
3. If exit code == 0 → Present to user
4. After user confirms → Update status block
```

### Gate Status Block Update

| After Gate | Update |
|------------|--------|
| Gate 1 confirmed | `status.phase = 1`, `gates_passed = [1]` |
| Gate 2 confirmed | `status.phase = 2`, `gates_passed = [1, 2]` |
| Gate 3 confirmed | `status.phase = 3`, `gates_passed = [1, 2, 3]` |

---

## Exit Codes Reference

| Code | Meaning | Action |
|------|---------|--------|
| 0 | PASS | Proceed |
| 1 | FAIL | Fix issues, re-validate |
| 2 | EMERGENCY | Stop and report |
