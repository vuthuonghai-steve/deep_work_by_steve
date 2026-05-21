---
name: build-crud-admin-page-rebuild
skill_schema_version: "3.0.0"
artifact_type: "design"
skill_name: "build-crud-admin-page"
generated_by: "skill-architect"
generated_at: "2026-05-16T22:30:00+07:00"
stage: "architect"
status: "ready_for_planner"
canonical_source:
  zone_mapping: "frontmatter.zone_mapping"
  progressive_disclosure: "frontmatter.progressive_disclosure"
zone_mapping:
  core:
    files:
      - path: "SKILL.md"
        file_required: true
        content_type: "orchestration"
    zone_required: true
  knowledge:
    files:
      - path: "knowledge/README.md"
        file_required: true
        content_type: "overview"
      - path: "knowledge/architecture.md"
        file_required: true
        content_type: "folder-structure-data-flow"
      - path: "knowledge/template-guide.md"
        file_required: true
        content_type: "step-by-step-guide"
      - path: "knowledge/implementation-logic.md"
        file_required: true
        content_type: "detailed-logic"
      - path: "knowledge/errors.md"
        file_required: true
        content_type: "error-handling"
      - path: "knowledge/ui-skills-summary.md"
        file_required: true
        content_type: "ui-ux-skills"
    zone_required: true
  scripts:
    files: []
    zone_required: false
  templates:
    files: []
    zone_required: false
  data:
    files: []
    zone_required: false
  loop:
    files:
      - path: "loop/checklist.md"
        file_required: true
        content_type: "implementation-checklist"
    zone_required: true
  assets:
    files: []
    zone_required: false
progressive_disclosure:
  tier1:
    - path: "SKILL.md"
      base: "skill_dir"
    - path: "knowledge/README.md"
      base: "skill_dir"
  tier2:
    - path: "knowledge/architecture.md"
      base: "skill_dir"
      load_when: "Step 1: Understand folder structure"
    - path: "knowledge/implementation-logic.md"
      base: "skill_dir"
      load_when: "Step 2: Implement form mode pattern"
    - path: "knowledge/template-guide.md"
      base: "skill_dir"
      load_when: "Step 3: Create new collection screens"
    - path: "knowledge/errors.md"
      base: "skill_dir"
      load_when: "When encountering errors"
    - path: "knowledge/ui-skills-summary.md"
      base: "skill_dir"
      load_when: "Before UI implementation"
    - path: "loop/checklist.md"
      base: "skill_dir"
      load_when: "Quality gate before delivery"
  tier3: []
required_sections:
  - "§1_problem_statement"
  - "§2_capability_map"
  - "§3_zone_mapping"
  - "§4_folder_structure"
  - "§5_execution_flow"
  - "§6_interaction_points"
  - "§7_progressive_disclosure"
  - "§8_risks"
  - "§9_open_questions"
  - "§10_metadata"
handoff:
  next_stage: "planner"
  ready_condition:
    required:
      frontmatter_valid: true
      zone_mapping_complete: true
      required_sections_present: true
      no_blockers: true
---

# §1 Problem Statement

## Pain Point

Skill `build-crud-admin-page` hiện tại được đóng gói dạng **flat zip** với cấu trúc:
```
build-crud-admin-page/
├── SKILL.md
└── references/
    ├── README.md
    ├── architecture.md
    ├── template-guide.md
    ├── implementation-logic.md
    ├── checklist.md
    ├── errors.md
    └── ui-skills-summary.md
```

**Vấn đề:**
1. **Không tuân thủ 7-Zone framework** — references/ nằm phẳng, không có zone phân tách rõ ràng
2. **SKILL.md quá dài (210 lines)** — chứa quá nhiều nội dung cần tách vào knowledge/
3. **Progressive Disclosure không rõ ràng** — không có Tier 1/2/3 loading strategy
4. **Không có YAML frontmatter** — thiếu metadata cần thiết cho tooling
5. **Quality gates không formal** — thiếu checklist.yaml machine-readable
6. **Không có trace tags** — không trace content về nguồn gốc
7. **Boot sequence không documented** — không biết đọc gì trước

## User & Context

- **User:** Developer/Agent cần tạo admin CRUD page cho PayloadCMS collection
- **Context:** Next.js + PayloadCMS admin screens
- **Trigger phrases:** "tạo trang admin", "build CRUD page", "tạo màn hình quản lý"

## Expected Output

Rebuild hoàn chỉnh theo **3-Tier Master Skill Suite**:
```
build-crud-admin-page/
├── SKILL.md                    # Tier 1: Core orchestration (< 150 lines)
├── knowledge/                  # Tier 2: Domain knowledge
│   ├── README.md
│   ├── architecture.md
│   ├── template-guide.md
│   ├── implementation-logic.md
│   ├── errors.md
│   └── ui-skills-summary.md
├── loop/                       # Quality gates
│   ├── checklist.md
│   └── checklist.yaml          # Machine-readable
└── .skill-context/             # Build artifacts
```

---

# §2 Capability Map

## 3 Pillars Analysis

### Pillar 1: Knowledge

**Domain Knowledge cần thiết:**
- PayloadCMS collections & REST API
- Next.js App Router structure
- react-hook-form + zod validation
- shadcn/ui components
- Form mode pattern (create/view/edit)
- Product/Collection metadata fetching

**Knowledge Files cần tạo:**
- `knowledge/README.md` — Overview & index
- `knowledge/architecture.md` — Folder structure, data flow (lấy từ references/architecture.md)
- `knowledge/template-guide.md` — Step-by-step cho collection mới
- `knowledge/implementation-logic.md` — Chi tiết logic (form mode, metadata)
- `knowledge/errors.md` — Lỗi thường gặp
- `knowledge/ui-skills-summary.md` — 4 UI/UX skills reference

### Pillar 2: Process

**Workflow 2-Phase:**

```
PHASE 1: Research & Analysis
├── Step 1: Confirm collection name & fields
├── Step 2: Read existing BouquetScreen patterns
├── Step 3: Read architecture.md & template-guide.md
└── Output: Summary + folder structure proposal

PHASE 2: Implementation
├── Step 1: Create folder structure
├── Step 2: Implement types/constants
├── Step 3: Build ListView + Filters
├── Step 4: Build FormView (3 modes)
├── Step 5: Create route files
└── Output: Complete CRUD admin page
```

**Key Patterns:**
- FormMode: 'create' | 'view' | 'edit'
- Route → Mode determination từ URL
- Category scoping cho Accessory

### Pillar 3: Guardrails

**AI thường sai ở đâu:**
1. **Không đọc references trước** — tự đoán cấu trúc thay vì follow architecture.md
2. **Bỏ qua form mode logic** — không phân biệt create/view/edit behavior
3. **Quên category scoping** — Accessory cần danh mục con của "Phụ kiện"
4. **Hardcode fields** — không đọc từ PayloadCMS schema
5. **Không apply UI skills** — skip ui-ux-pro-max, vercel-react-best-practices

---

# §3 Zone Mapping

| Zone | Files cần tạo | Nội dung | Bắt buộc? |
|------|---------------|----------|-----------|
| **Core** | `SKILL.md` | Persona, workflow, guardrails, triggers | ✅ |
| **Knowledge** | `knowledge/README.md` | Tổng quan references | ✅ |
| | `knowledge/architecture.md` | Folder structure, data flow, component responsibilities | ✅ |
| | `knowledge/template-guide.md` | Step-by-step guide cho collection mới | ✅ |
| | `knowledge/implementation-logic.md` | Form mode, metadata, categories | ✅ |
| | `knowledge/errors.md` | Common errors & solutions | ✅ |
| | `knowledge/ui-skills-summary.md` | 4 UI/UX skills tóm tắt | ✅ |
| **Scripts** | Không cần | | ❌ |
| **Templates** | Không cần | | ❌ |
| **Data** | Không cần | | ❌ |
| **Loop** | `loop/checklist.md` | Checklist implementation | ✅ |
| | `loop/checklist.yaml` | Machine-readable validation | ✅ |
| **Assets** | Không cần | | ❌ |

---

# §4 Folder Structure

## Mindmap

```mermaid
mindmap
  root((build-crud-admin-page))
    Core
      SKILL.md
        triggers
        workflow_phases
        guardrails
        boot_sequence
    Knowledge
      README.md
        references_index
        modules_map
      architecture.md
        folder_structure
        data_flow
        component_responsibilities
        form_mode_pattern
      template-guide.md
        step1_copy_structure
        step2_update_types
        step3_update_constants
        step4_update_hooks
        step5_update_sections
        step6_update_views
        step7_create_routes
        step8_update_entry
      implementation-logic.md
        form_mode
        metadata_categories
        product_filters
        field_sets
        payload_cms_query
      errors.md
        typescript_errors
        form_errors
        image_errors
        bom_errors
        mode_switching
        unsaved_changes
        metadata_errors
        filters_errors
        zod_validation
        debug_tips
      ui-skills-summary.md
        ui-ux-pro-max
        vercel-react-best-practices
        vercel-composition-patterns
        web-design-guidelines
        apply_order
    Loop
      checklist.md
        pre-implementation
        setup
        list_view
        form_view
        form_sections
        form_validation
        form_submission
        ux_features
        routes
        responsive
        accessibility
        performance
        final_review
      checklist.yaml
        quality_gates
        trace_validation
```

---

# §5 Execution Flow

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant SKILLMD as SKILL.md
    participant Architecture as knowledge/architecture.md
    participant Template as knowledge/template-guide.md
    participant Checklist as loop/checklist.md
    participant Codebase

    User->>Agent: "Tạo trang admin CRUD cho collection X"

    rect rgb(240, 248, 255)
        Note over Agent: PHASE 1: Research & Analysis
        Agent->>SKILLMD: Read triggers + workflow
        Agent->>Architecture: Read folder structure + patterns
        Agent->>Codebase: Find BouquetScreen reference
        Agent->>User: Confirm collection + fields
    end

    rect rgb(255, 250, 240)
        Note over Agent: PHASE 2: Implementation
        Agent->>Template: Read step-by-step guide
        loop Per file
            Agent->>Codebase: Create/Update files
            Agent->>Checklist: Mark complete
        end
    end

    rect rgb(240, 255, 240)
        Note over Agent: Quality Gate
        Agent->>Checklist: Run checklist validation
        Agent->>User: Report completion
    end
```

## Boot Sequence

```
1. Read SKILL.md (this file)
2. Read knowledge/README.md (references index)
3. Proceed to Phase 1
4. Load Tier 2 files as needed per Phase
5. Before deliver: read loop/checklist.md
```

---

# §6 Interaction Points

## When Agent MUST Stop and Ask User

| # | Interaction Point | Question/Action |
|---|------------------|------------------|
| 1 | **Before Phase 1** | Confirm collection name & fields |
| 2 | **After Phase 1** | Confirm folder structure proposal |
| 3 | **After Phase 2** | Report completion + checklist results |

## When Agent Can Proceed Without Asking

| # | Situation | Action |
|---|-----------|--------|
| 1 | Missing fields | Auto-read from PayloadCMS schema |
| 2 | Existing BouquetScreen | Reference for patterns |
| 3 | Errors | Read knowledge/errors.md and self-correct |

---

# §7 Progressive Disclosure Plan

## Tier 1 (Mandatory — always load at boot)

| File | Purpose |
|------|---------|
| `SKILL.md` | Core orchestration, triggers, workflow |
| `knowledge/README.md` | References index, modules map |

## Tier 2 (Conditional — load when needed)

| File | Load When |
|------|-----------|
| `knowledge/architecture.md` | Step 1: Understand folder structure |
| `knowledge/implementation-logic.md` | Step 2: Implement form mode pattern |
| `knowledge/template-guide.md` | Step 3: Create new collection screens |
| `knowledge/errors.md` | When encountering errors |
| `knowledge/ui-skills-summary.md` | Before UI implementation |
| `loop/checklist.md` | Quality gate before delivery |

## Tier 3 (Optional — on-demand)

None required for this skill.

---

# §8 Risks & Blind Spots

## Identified Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| 1 | Agent skip references, use wrong folder structure | High | High | Explicitly list "Read X before Y" in workflow |
| 2 | Agent confuse form mode logic (create/view/edit) | Medium | High | Include concrete code example in implementation-logic.md |
| 3 | Agent forget category scoping for Accessory | Medium | Medium | Add note in template-guide.md Step 4 |
| 4 | Agent hardcode fields instead of reading schema | Medium | Medium | Include PayloadCMS schema reading instruction |
| 5 | Agent skip UI/UX skills, poor code quality | Low | Medium | List skills in order of application |

## Anti-Patterns to Avoid

```yaml
anti_patterns:
  - "Copy-paste from BouquetScreen without understanding patterns"
  - "Use boolean props instead of mode string"
  - "Hardcode collection name in multiple files"
  - "Skip form validation"
  - "No loading/error states"
```

---

# §9 Open Questions

| # | Question | Status | Resolution |
|---|----------|--------|------------|
| 1 | Should this skill support collection types beyond Bouquet/Accessory/SingleFlower? | Open | Limit to existing patterns first |
| 2 | Should we auto-generate types from PayloadCMS schema? | Open | Manual first, auto later |
| 3 | Should route files be in app/(frontend) or app/(admin)? | Resolved | app/(frontend) for consistency |
| 4 | Should we include copy-button for UI code blocks? | Open | Low priority |

---

# §10 Metadata

```yaml
skill_name: build-crud-admin-page
version: "2.0.0"  # Rebuilt from 1.x
author: "Steve Void Team"
status: "ready_for_planner"
created: "2026-05-16"
rebuilt_from: "build-crud-admin-page.zip (original flat structure)"
architecture_version: "3.0.0"
pipeline_stage: 1
```

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-05-16 | Rebuild entire skill | Flat structure → 7-Zone framework |
| | Add YAML frontmatter | Machine-readable metadata |
| | Add Progressive Disclosure | Tier 1/2 loading |
| | Add checklist.yaml | Automated validation |
| | Compact SKILL.md | < 150 lines target |
