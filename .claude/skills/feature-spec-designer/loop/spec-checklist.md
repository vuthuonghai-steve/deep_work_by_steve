# Binary Quality Gate Checklist: `feature-spec-designer`

> Applied at the END of each step in the 6-Step Workflow.  
> Rule: PASS = (Check 1) AND (Check 2) AND ... AND (Check N)

---

## Step 1 Validation Gate (End of Step 1)
- [ ] Raw request enclosed in `<user_skill_request>` XML tag?
- [ ] Core business intent extracted?
- [ ] Step 1 latency p95 < 1000ms?

## Step 2 Validation Gate (End of Step 2)
- [ ] User Requirements separated from Provided Context?
- [ ] 100% of raw inputs labeled and categorized?
- [ ] Initial normalizations saved under `Docs/Specs/{feature-name}/`?

## Step 3 Validation Gate (End of Step 3)
- [ ] Ambiguities detected and 3-5 multiple-choice questions generated?
- [ ] Each question includes 2-3 specific options + 1 `[Khuyến nghị]` default option?
- [ ] Default option applied upon 300s timeout / user silence and logged to `clarification-log.md`?

## Step 4 Validation Gate (End of Step 4)
- [ ] 4 Use Case categories (Basic, Must-Have, Nice-To-Have, Exception) fully covered?
- [ ] 100% of NFRs quantified (Latency p95 < 3000ms)?
- [ ] BDD Gherkin scenarios written for all flows?
- [ ] Zero forbidden placeholder words (`TODO`, `TBD`, `nhanh`, `tốt`)?

## Step 5 Validation Gate (End of Step 5)
- [ ] Sub-steps 5.1, 5.2, and 5.3 executed?
- [ ] All Mermaid diagrams (`sequence.mmd`, `flowchart.mmd`, `erd.mmd`) isolated under `Docs/Specs/{feature-name}/diagrams/`?
- [ ] 100% of Mermaid node/edge labels wrapped in double quotes `""` with zero HTML tags?
- [ ] Self-Correction loop triggered if syntax/path error detected?

## Step 6 Validation Gate (End of Step 6)
- [ ] Final spec file saved strictly at `Docs/Specs/{feature-name}/spec.md`?
- [ ] 100% compliance with `standards.md` (Alerts, Tables, Clickable relative links)?
- [ ] Final Quality Score ≥ 0.80 (PASS)?
