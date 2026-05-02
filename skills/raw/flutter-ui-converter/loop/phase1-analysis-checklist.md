# Phase 1: Analysis & Documentation Checklist

Use this checklist to verify Phase 1 completion before requesting user approval.

---

## 1. Context Initialization

- [ ] Session directory created (`.skill-context/flutter-ui-converter/session-{timestamp}/`)
- [ ] `conversion-context.yaml` created with metadata
- [ ] Source and target paths resolved (Relative → Absolute)
- [ ] DESIGN.md path validated

---

## 2. Source Project Scan

- [ ] Source Dart files identified
- [ ] Widget classes extracted
- [ ] Asset references collected
- [ ] Color usage documented
- [ ] Dependencies listed
- [ ] `source-analysis.md` generated

**Verification**:
- [ ] At least 1 Dart file found
- [ ] Widget list is not empty
- [ ] Analysis file is readable and complete

---

## 3. Target Project Scan

- [ ] Target screen file located (or noted as new)
- [ ] BlocBuilder/BlocConsumer/BlocListener identified
- [ ] Event triggers documented
- [ ] State references extracted
- [ ] Theme constants found (or noted as using Theme.of(context))
- [ ] Dependencies listed
- [ ] `target-analysis.md` generated

**Verification**:
- [ ] Bloc hooks documented (even if none found)
- [ ] Theme approach identified
- [ ] Analysis file is readable and complete

---

## 4. Mapping Generation

- [ ] `component-mapping.md` created
- [ ] `asset-checklist.md` created with all source assets
- [ ] `theme-mapping.md` created
- [ ] `flow-diagram.mmd` created
- [ ] `risk-assessment.md` created

**Verification**:
- [ ] All source assets appear in asset checklist
- [ ] All source colors appear in theme mapping
- [ ] Risk assessment covers all 6 risk categories

---

## 5. Knowledge Application

- [ ] Read `knowledge/flutter-ui-patterns.md`
- [ ] Read `knowledge/conversion-rules.md`
- [ ] Read `knowledge/component-mapping-guide.md`
- [ ] Read `knowledge/asset-management.md`
- [ ] Read `knowledge/flutter-sdk-compatibility.md`
- [ ] Read `knowledge/state-management-preservation.md`
- [ ] Read `knowledge/localization-mapping.md`
- [ ] Read `knowledge/responsive-layout-rules.md`
- [ ] Read project global `DESIGN.md` (colors, typography, constants)

**Verification**:
- [ ] All 8 knowledge files loaded
- [ ] Guidelines applied to analysis

---

## 6. Quality Checks

### Completeness
- [ ] No placeholder text like "TBD" without explanation
- [ ] All sections in templates filled
- [ ] Asset paths are absolute or clearly relative

### Accuracy
- [ ] Widget names match actual Dart classes
- [ ] Asset paths match actual file structure
- [ ] Bloc/Cubit names are correct

### Clarity
- [ ] Risk assessment is specific (not generic)
- [ ] Mapping strategies are clear
- [ ] Notes explain non-obvious decisions

---

## 7. Presentation Preparation

- [ ] Analysis documents formatted properly
- [ ] Mermaid diagram syntax is valid
- [ ] Tables are aligned
- [ ] No broken markdown

**Verification**:
- [ ] Preview `analysis-doc.md` - renders correctly
- [ ] Preview `flow-diagram.mmd` - valid Mermaid syntax
- [ ] All links between documents work

---

## 8. User Approval Gate

- [ ] Present analysis documents to user
- [ ] Highlight key findings:
  - Number of widgets to convert
  - Number of assets to copy
  - Number of Bloc hooks to preserve
  - Risk level (High/Medium/Low)
- [ ] Ask for approval to proceed to Phase 2

**User Questions**:
- [ ] "Does the component mapping look correct?"
- [ ] "Are there any assets we should exclude?"
- [ ] "Any concerns about the identified risks?"

---

## Completion Criteria

✅ **Phase 1 is complete when**:
- All checkboxes above are marked
- User has reviewed analysis documents
- User has approved proceeding to Phase 2
- No critical risks remain unaddressed

---

**Next Phase**: Phase 2 - Code Generation
