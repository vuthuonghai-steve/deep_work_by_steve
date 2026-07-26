# Feature Specification Domain Rules & Guidelines

> Knowledge Zone (Zone 2) for `feature-spec-designer`  
> Aligned with [standards.md](file:///home/stveve/Documents/workspace/Steve/build-workflow/deep_work_by_steve/standards.md)

---

## 1. Storage Isolation Directives
- **Spec Root Path**: `Docs/Specs/{feature-name}/`
- **Final Spec File**: `Docs/Specs/{feature-name}/spec.md`
- **Diagrams Directory**: `Docs/Specs/{feature-name}/diagrams/`
  - `sequence.mmd`: Sequence Diagram showing interaction between User, SpecDesigner, Storage, Evaluator.
  - `flowchart.mmd`: Flowchart showing Happy Path, Alternative Clarification Path, and Exception Path.
  - `erd.mmd`: Entity Relationship Diagram for Spec Entities.

---

## 2. Mermaid Diagram Construction Rules
1. **Double Quote Wrapper**: Every node and edge label MUST be wrapped in double quotes.
   - ✅ `A["Start: Process Input"] --> B["Step 1: XML Enclosure"]`
   - ❌ `A[Start: Process Input] --> B[Step 1: XML Enclosure]`
2. **Zero HTML Tags**: Never place HTML tags like `<br>`, `<b>`, `<i>` inside Mermaid labels. Use clean text.
3. **Storage Location**: Always output raw `.mmd` files or code blocks targeted to `Docs/Specs/{feature-name}/diagrams/`.

---

## 3. Interactive Clarification Rules (Step 3)
1. **Trigger Condition**: Activated when input text contains vague adjectives (`nhanh`, `tốt`, `nhiều`, `ổn định`) or unquantified latency/throughput metrics.
2. **Options Pattern**: Generate 3-5 multiple-choice questions. Each question must offer:
   - Option A: Specific metric choice (e.g. Latency p95 < 500ms) marked `[Khuyến nghị]`.
   - Option B: Alternative metric choice (e.g. Latency p95 < 1000ms).
   - Option C: Custom write-in input.
3. **Timeout / Fallback Rule**: If running in automated mode or user is unresponsive (300s timeout), automatically select Option A `[Khuyến nghị]` and append a notice in `clarification-log.md`.

---

## 4. Depth Signals (S1 - S4)
- **S1 Negation**: Never check validation at step initiation. Validation Gate runs DUY NHẤT at step completion.
- **S2 Reverse Question**: "What if validation fails or user times out?" -> Auto-trigger Self-Correction or Default Option Fallback.
- **S3 Multi-Stakeholder**: Ensure output caters to Developer, PM, BA, Architect, and LLM Code Executor.
- **S4 Constraint Anchoring**: Enforce exact paths `Docs/Specs/{feature-name}/` and `Docs/Specs/{feature-name}/diagrams/`.

---

## 5. Compliance Checklist with `standards.md`
- Use GitHub-style Alerts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`).
- Use Markdown tables for multi-column data.
- Use clickable file links with line numbers `[file.md:L1-10](file:///path/to/file#L1-L10)`. Do NOT wrap display text in backticks (`[`file.md`](...)` is FORBIDDEN).
- Zero forbidden placeholders (`TODO`, `TBD`, `...`).
