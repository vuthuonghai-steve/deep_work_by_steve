# Quality Checklist

> **Usage**: Quality checklist for normalization output. Run through this before delivering results.

---

## Pre-Normalization Checklist

- [ ] Input directory exists and is accessible
- [ ] All input files are readable (no permission errors)
- [ ] Document types have been identified

---

## Post-Normalization Checklist

### General

- [ ] All documents have unique IDs in correct format
- [ ] All documents have `source` field with file path
- [ ] All documents have `createdAt` timestamp (ISO 8601)
- [ ] `originalContent` preserved for all documents
- [ ] No source files were modified or deleted

### Functional Requirements

- [ ] All FRs have: id, title, description, priority, module, source
- [ ] Priority values are normalized (critical/high/medium/low)
- [ ] Module values are normalized (M1-M6)
- [ ] Dependencies is an array (even if empty)

### User Stories

- [ ] All USs have: id, title, description, acceptanceCriteria, priority, module, source
- [ ] Acceptance criteria is a non-empty array
- [ ] Priority normalized (must-have/should-have/could-have/won't-have)
- [ ] Labels is an array (even if empty)

### Use Cases

- [ ] All UCs have: id, name, actor, preconditions, postconditions, flow, module, source
- [ ] Preconditions is a non-empty array
- [ ] Postconditions is a non-empty array
- [ ] Flow has main steps array

### Validation Report

- [ ] Report includes document count by type
- [ ] Report includes all errors and warnings
- [ ] Report includes summary of changes

---

## Non-Destructive Verification

- [ ] Original files in Docs/life-1/ are unchanged
- [ ] New normalized files created in Docs/life-2/normalization/
- [ ] No files were overwritten

---

## Output File Verification

- [ ] JSON files are valid (parseable)
- [ ] File names match convention: `{module}-{docType}-normalized.json`
- [ ] Validation report is in Markdown format

---

## Risk Mitigation Check

- [ ] R1 (unexpected format): Best-effort parsing with warnings ✓
- [ ] R2 (context loss): Original content preserved ✓
- [ ] R3 (validation too strict): Warnings vs errors separated ✓
- [ ] R4 (duplicate IDs): Sequence counters reset per module ✓
