# Schema Bàn giao — ba-synthesizer

Nguồn: ba-synthesizer-analysis.md §6.2

## YAML Frontmatter (business-analysis.md)

```yaml
skill_handoff:
  target_skill_name: "ten-kebab-skill"
  version: "1.0.0"
  scs_complexity_score: 3.6
  decomposition_recommended: true
  sub_skills_proposed: ["sub-1", "sub-2"]
  scope_boundary:
    in_scope: ["Yêu cầu 1"]
    out_scope: ["Giới hạn 1"]
  technical_frameworks_recommended: ["Mermaid.js", "Gherkin"]
  detected_risks: ["Rủi ro 1"]
  quality_gate_status: "PASS"  # hoặc WARNING
  quality_score_percentage: 92.5
```

## Input Contract (§6.1)

```
<elicitation_report_input>...</elicitation_report_input>
<analysis_report_input>...</analysis_report_input>
```

## Output Contract (§6.2)

File: business-analysis.md → Explorer (Stage 0). Format: Markdown + YAML frontmatter. Bắt buộc quality_gate_status + quality_score.

## Cross-Reference

- ba-analyst output đủ 7 deliverables (QG-BA-02) — khớp checklist §3.2
- ba-elicitor elicitation-report.md có frontmatter + gap_analysis — khớp input contract §6.1
