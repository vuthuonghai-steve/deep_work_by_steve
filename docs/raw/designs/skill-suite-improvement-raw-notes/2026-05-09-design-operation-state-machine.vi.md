# Thiết kế: Operation Type State Machine

> Ngày: 2026-05-09
> Tác giả: Hermes Agent
> Trạng thái: Design specification
> Thư mục: `docs/raw/designs/`

---

## 1. Tổng quan

Tài liệu này định nghĩa **Operation Type State Machine** — một hệ thống trạng thái để Builder tự động phát hiện và xử lý 6 loại operation khác nhau khi làm việc với skills. State machine điều phối detection flow, workflow execution, và transition rules giữa các trạng thái.

---

## 2. State Machine Diagram cho 6 Operation Types

```
                                    ┌─────────────────────────────────────────────┐
                                    │                                             │
                                    │   ┌─────────────┐    ┌─────────────┐        │
START ──→ [DETECT] ──→ ┌────────────│   │ create_new  │───→│ BUILDING    │        │
                      │             │   └─────────────┘    └──────┬──────┘        │
                      │             │                          │                │
                      │             │   ┌─────────────┐    ┌─────▼──────┐        │
                      │             │   │patch_existing│───→│  PATCHING  │        │
                      │             │   └─────────────┘    └──────┬─────┘        │
                      │             │                          │                │
                      │             │   ┌─────────────┐    ┌───▼───────┐        │
                      │             └───│refactor_     │───→│REFACTORING│        │
                      │                 │existing     │    └─────┬─────┘        │
                      │                 └─────────────┘          │                │
                      │                                        │                │
                      │                 ┌─────────────┐    ┌───▼───────┐        │
                      │                 │migrate_     │───→│MIGRATING  │        │
                      │                 │platform     │    └─────┬─────┘        │
                      │                 └─────────────┘          │                │
                      │                                        │                │
                      │                 ┌─────────────┐    ┌───▼───────┐        │
                      │                 │consolidate_ │───→│CONSOLIDATING
                      │                 │skills       │    └─────┬─────┘        │
                      │                 └─────────────┘          │                │
                      │                                        │                │
                      │                 ┌─────────────┐    ┌───▼───────┐        │
                      │                 │deprecate_   │───→│DEPRECATING │        │
                      │                 │skill        │    └─────┬─────┘        │
                      │                 └─────────────┘          │                │
                      │                                        │                │
                      └────────────────────────────────────────┘                │
                                                                       │         │
                                                                       ▼         ▼
                                                              ┌─────────────────┐
                                                              │     DONE        │
                                                              │ (terminal state)│
                                                              └─────────────────┘
```

### 2.1 Operation Types Enum

```yaml
operation_types:
  - create_new       # Tạo skill hoàn toàn mới
  - patch_existing   # Sửa một phần nhỏ của skill hiện có
  - refactor_existing # Tái cấu trúc toàn bộ skill
  - migrate_platform # Di chuyển skill giữa các platform
  - consolidate_skills # Gộp nhiều skill thành một
  - deprecate_skill  # Đánh dấu skill là deprecated
```

### 2.2 State Definitions

| State | Mô tả | Entry Condition | Exit Condition |
|-------|-------|-----------------|----------------|
| `DETECT` | Phát hiện operation type | Input received | Type identified |
| `CREATE_NEW` | Tạo skill mới | No existing skill | Skill created |
| `PATCHING` | Áp dụng minimal patch | ≤3 files changed | Patch applied |
| `REFACTORING` | Tái cấu trúc skill | Structural changes needed | Refactor complete |
| `MIGRATING` | Migrate giữa platforms | Source ≠ Target platform | Migration done |
| `CONSOLIDATING` | Gộp nhiều skills | Multiple skills input | Consolidation done |
| `DEPRECATING` | Đánh dấu deprecated | Intent = deprecate | Deprecation notice |
| `DONE` | Hoàn thành | All operations finished | (terminal) |

---

## 3. Detection Flow

### 3.1 Detection Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                      DETECTION FLOW                                   │
└──────────────────────────────────────────────────────────────────────┘

User Input
    │
    ▼
┌─────────────────┐
│   STEP 1:       │
│   USER HINT     │
│   EXTRACTION    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Extract từ input:                                                  │
│   - explicit_operation_type (nếu user chỉ định)                     │
│   - existing_skill_path (nếu có reference)                          │
│   - scope indicator (new_domain | existing | cross-platform)        │
│   - change_scale (< 20% | 20-80% | > 80%)                            │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   STEP 2:       │
│   CONTEXT       │
│   ANALYSIS      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Phân tích context:                                                 │
│   - changed_files count                                             │
│   - action type (split | merge | rename | patch | create)           │
│   - source_platform vs target_platform                               │
│   - intent classification                                            │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   STEP 3:       │
│   PLATFORM      │
│   RESOLUTION    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Platform detection:                                                 │
│   - Detect source platform từ skill metadata                         │
│   - Detect target platform từ target context                         │
│   - Cross-platform = (source ≠ target)                              │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   STEP 4:       │
│   FINAL         │
│   DETECTION     │
└────────┬────────┘
         │
         ▼
    ┌────────────┐
    │ OPERATION  │
    │ TYPE       │
    │ DETERMINED │
    └────────────┘
```

### 3.2 Detection Pseudocode

```python
def detect_operation_type(context):
    """
    Builder tự động detect operation type từ input context.
    Detection flow: User Hint → Context Analysis → Platform Resolution
    """
    
    # === STEP 1: USER HINT EXTRACTION ===
    user_hint = extract_user_hint(context.get('prompt', ''))
    
    if user_hint.explicit_type:
        # User chỉ định rõ operation type
        return user_hint.explicit_type
    
    # === STEP 2: CONTEXT ANALYSIS ===
    existing_skill = context.get('existing_skill_path')
    changed_files = context.get('changed_files', [])
    action = context.get('action')
    intent = context.get('intent')
    scope = context.get('scope')
    
    # Case 1: Hoàn toàn mới — không có skill reference
    if not existing_skill:
        if scope == 'new_domain':
            return 'create_new'
    
    # Case 2: Có reference đến skill hiện có
    if existing_skill:
        
        # Patch detection: chỉ thay đổi < 20% content, ≤ 3 files
        if len(changed_files) <= 3:
            return 'patch_existing'
        
        # Refactor detection: thay đổi cấu trúc, split, merge, rename
        if action in ['split', 'merge', 'rename', 'restructure']:
            return 'refactor_existing'
        
        # Deprecate detection
        if intent == 'deprecate':
            return 'deprecate_skill'
        
        # Consolidate detection: nhiều skill input
        skills_to_consolidate = context.get('skills_to_consolidate', [])
        if len(skills_to_consolidate) > 1:
            return 'consolidate_skills'
    
    # === STEP 3: PLATFORM RESOLUTION ===
    source_platform = detect_platform(existing_skill) if existing_skill else None
    target_platform = context.get('target_platform')
    
    if source_platform and target_platform:
        if source_platform != target_platform:
            return 'migrate_platform'
    
    # === STEP 4: FALLBACK ===
    # Default: fallback to standard create
    return 'create_new'


def extract_user_hint(prompt):
    """
    Trích xuất explicit operation type từ user prompt.
    """
    hints = {
        'create_new': ['tạo skill mới', 'create new skill', 'new skill'],
        'patch_existing': ['sửa', 'patch', 'fix', 'update skill'],
        'refactor_existing': ['refactor', 'tái cấu trúc', 'restructure'],
        'migrate_platform': ['migrate', 'di chuyển sang'],
        'consolidate_skills': ['gộp', 'consolidate', 'merge skills'],
        'deprecate_skill': ['deprecate', 'bỏ', 'loại bỏ']
    }
    
    prompt_lower = prompt.lower()
    
    for op_type, keywords in hints.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                return ExplicitHint(op_type)
    
    return ExplicitHint(None)
```

---

## 4. Per-Operation Workflow Pseudocode

### 4.1 create_new

```python
def workflow_create_new(context, mode):
    """
    Workflow cho create_new operation type.
    Mode: lightweight | standard | strict
    """
    
    if mode == 'lightweight':
        # Lightweight: N/A cho create_new (cần design phase)
        raise ModeNotSupported("create_new requires design phase")
    
    # === STANDARD / STRICT ===
    
    # Phase 1: DESIGN
    if mode == 'strict':
        # Strict: Formal design review
        design_doc = architect_with_review(context)
        approve_design(design_doc)
    else:
        # Standard: Quick design checkpoint
        design_doc = architect_fast(context)
        checkpoint("design_approved")
    
    # Phase 2: PLAN
    todo_doc = planner_from_design(design_doc)
    
    if mode == 'strict':
        approve_plan(todo_doc)
    else:
        checkpoint("plan_approved")
    
    # Phase 3: BUILD
    skill_package = builder_implement(design_doc, todo_doc)
    
    # Phase 4: VERIFY
    verification_result = verify_skill(skill_package)
    
    if mode == 'strict':
        manual_review(skill_package)
        signoff_required()
    
    # Phase 5: DELIVER
    deliver(skill_package, format='full_skill_package')
    
    return skill_package
```

### 4.2 patch_existing

```python
def workflow_patch_existing(context, mode):
    """
    Workflow cho patch_existing operation type.
    Minimal changes, surgical mode.
    """
    
    # === LIGHTWEIGHT ===
    if mode == 'lightweight':
        # 1. Read existing skill
        skill = load_skill(context.existing_skill_path)
        
        # 2. Apply minimal changes
        patch_delta = apply_user_changes(skill, context.changes)
        
        # 3. Syntax check only
        syntax_check(patch_delta)
        
        # 4. Deliver patch diff
        deliver(patch_delta, format='patch_delta')
        
        return patch_delta
    
    # === STANDARD ===
    if mode == 'standard':
        # 1. Assess feasibility
        feasibility = assess_patch(scope=context.scope)
        
        # 2. Apply changes
        skill = load_skill(context.existing_skill_path)
        patched = apply_changes(skill, context.changes)
        
        # 3. Verify
        verify_patched_skill(patched)
        
        # 4. Deliver
        deliver(patched, format='patched_skill')
        
        return patched
    
    # === STRICT ===
    # Strict: Overkill cho patch — gợi ý standard
    raise ModeNotRecommended("patch_existing works better in lightweight/standard")
```

### 4.3 refactor_existing

```python
def workflow_refactor_existing(context, mode):
    """
    Workflow cho refactor_existing operation type.
    Giữ nguyên behavior, cải cấu trúc.
    """
    
    # Refactor cần design phase (không lightweight)
    if mode == 'lightweight':
        raise ModeNotSupported("refactor_existing requires design phase")
    
    # Phase 1: AUDIT existing skill
    existing_skill = load_skill(context.existing_skill_path)
    audit_report = audit_skill_structure(existing_skill)
    
    # Phase 2: DESIGN refactor plan
    if mode == 'strict':
        refactor_design = design_refactor_formal(existing_skill, audit_report)
        approve_design(refactor_design)
    else:
        refactor_design = design_refactor_fast(existing_skill, audit_report)
        checkpoint("refactor_design_approved")
    
    # Phase 3: EXECUTE refactor
    refactored_skill = execute_refactor(existing_skill, refactor_design)
    
    # Phase 4: VERIFY behavior equivalence
    verify_behavior_equivalence(existing_skill, refactored_skill)
    
    # Phase 5: GENERATE migration guide
    migration_guide = generate_diff_report(existing_skill, refactored_skill)
    
    if mode == 'strict':
        manual_review(refactored_skill)
        signoff_required()
    
    # Phase 6: DELIVER
    deliver(refactored_skill, migration_guide, format='full_skill_package + migration_guide')
    
    return refactored_skill
```

### 4.4 migrate_platform

```python
def workflow_migrate_platform(context, mode):
    """
    Workflow cho migrate_platform operation type.
    Di chuyển skill giữa các platform (Claude ↔ Hermes).
    """
    
    # Phase 1: ANALYZE source skill
    source_skill = load_skill(context.existing_skill_path)
    source_platform = detect_platform(source_skill)
    
    # Phase 2: MAPPING (platform-specific adaptations)
    path_mapping = map_paths(source_platform, context.target_platform)
    convention_mapping = map_conventions(source_platform, context.target_platform)
    
    if mode == 'lightweight':
        # Lightweight: Limited adaptation
        adapted = apply_lightweight_adaptations(source_skill, path_mapping)
        syntax_check(adapted)
        deliver(adapted, format='adapted_skill')
        return adapted
    
    # Phase 3: ADAPT full
    adapted_skill = adapt_to_platform(
        source_skill,
        target_platform=context.target_platform,
        path_mapping=path_mapping,
        convention_mapping=convention_mapping
    )
    
    # Phase 4: VERIFY loadability
    verify_loadability(adapted_skill, context.target_platform)
    
    if mode == 'strict':
        # Full validation + manual review
        platform_test_suite = load_platform_tests(context.target_platform)
        run_tests(adapted_skill, platform_test_suite)
        manual_review(adapted_skill)
        signoff_required()
    
    # Phase 5: DELIVER
    deliver(adapted_skill, format='adapted_skill_package')
    
    return adapted_skill
```

### 4.5 consolidate_skills

```python
def workflow_consolidate_skills(context, mode):
    """
    Workflow cho consolidate_skills operation type.
    Gộp nhiều skill thành một unified skill.
    """
    
    if mode == 'lightweight':
        raise ModeNotSupported("consolidate_skills requires full pipeline")
    
    # Phase 1: LOAD all skills
    skills_to_merge = []
    for skill_path in context.skills_to_consolidate:
        skills_to_merge.append(load_skill(skill_path))
    
    # Phase 2: ANALYZE overlaps
    overlap_analysis = analyze_skill_overlaps(skills_to_merge)
    
    # Phase 3: DESIGN consolidated structure
    if mode == 'strict':
        consolidated_design = design_consolidation_formal(
            skills_to_merge, overlap_analysis
        )
        approve_design(consolidated_design)
    else:
        consolidated_design = design_consolidation_fast(
            skills_to_merge, overlap_analysis
        )
        checkpoint("consolidation_design_approved")
    
    # Phase 4: MERGE skills
    merged_skill = merge_skill_packages(
        skills_to_merge, consolidated_design
    )
    
    # Phase 5: VERIFY
    verify_merged_skill(merged_skill)
    
    if mode == 'strict':
        manual_review(merged_skill)
        signoff_required()
    
    # Phase 6: DELIVER
    deliver(merged_skill, format='merged_skill_package')
    
    return merged_skill
```

### 4.6 deprecate_skill

```python
def workflow_deprecate_skill(context, mode):
    """
    Workflow cho deprecate_skill operation type.
    Đánh dấu skill là deprecated.
    """
    
    # Phase 1: VERIFY deprecation is safe
    verify_no_dependencies(context.skill_to_deprecate)
    
    # Phase 2: CHECK for replacement
    replacement = context.get('replacement_skill_path')
    
    if mode == 'lightweight':
        # Lightweight: Just mark deprecated
        deprecation_notice = create_deprecation_notice(
            skill=context.skill_to_deprecate,
            reason=context.deprecation_reason,
            replacement=replacement
        )
        apply_deprecation_tag(context.skill_to_deprecate, deprecation_notice)
        deliver(deprecation_notice, format='deprecation_notice')
        return deprecation_notice
    
    # Standard / Strict
    # Phase 3: CREATE migration path
    if replacement:
        migration_guide = create_migration_guide(
            from_skill=context.skill_to_deprecate,
            to_skill=replacement
        )
    else:
        migration_guide = create_removal_guide(context.skill_to_deprecate)
    
    # Phase 4: APPLY deprecation
    deprecation_notice = create_full_deprecation_package(
        skill=context.skill_to_deprecate,
        reason=context.deprecation_reason,
        migration_guide=migration_guide
    )
    
    # Phase 5: DELIVER
    deliver(deprecation_notice, format='deprecation_notice + migration_guide')
    
    return deprecation_notice
```

---

## 5. Mode × Operation Matrix

### 5.1 Compatibility Matrix

```
┌─────────────────────┬────────────┬───────────┬────────┐
│ Operation \ Mode     │ lightweight│ standard  │ strict │
├─────────────────────┼────────────┼───────────┼────────┤
│ create_new           │    ❌      │    ✅     │   ✅   │
│                      │ N/A       │ Default   │ Full   │
├─────────────────────┼────────────┼───────────┼────────┤
│ patch_existing       │    ✅      │    ✅     │   ⚠️   │
│                      │ Default   │ Available │Overkill│
├─────────────────────┼────────────┼───────────┼────────┤
│ refactor_existing    │    ❌      │    ✅     │   ✅   │
│                      │ N/A       │ Default   │ Full   │
├─────────────────────┼────────────┼───────────┼────────┤
│ migrate_platform     │    ⚠️      │    ✅     │   ✅   │
│                      │ Limited   │ Default   │ Full   │
├─────────────────────┼────────────┼───────────┼────────┤
│ consolidate_skills   │    ❌      │    ✅     │   ✅   │
│                      │ N/A       │ Default   │ Full   │
├─────────────────────┼────────────┼───────────┼────────┤
│ deprecate_skill      │    ✅      │    ✅     │   ⚠️   │
│                      │ Default   │ Available │Overkill│
└─────────────────────┴────────────┴───────────┴────────┘

Legend:
  ✅ = Supported (default cho operation đó)
  ⚠️ = Supported nhưng không khuyến khích
  ❌ = Not supported
```

### 5.2 Mode Parameters by Operation

| Operation Type | Lightweight | Standard | Strict |
|----------------|-------------|----------|--------|
| **create_new** | — | Gates: pre, post, confirm, full design | + manual review, signoff |
| **patch_existing** | No gates, syntax only | Gates: pre, verify | + extra validation |
| **refactor_existing** | — | Gates: design, build, verify | + formal review |
| **migrate_platform** | Limited path mapping | Full adaptation | + test suite |
| **consolidate_skills** | — | Gates: design, merge, verify | + formal review |
| **deprecate_skill** | Mark only | + migration guide | + full audit |

### 5.3 Execution Mode Parameters

```yaml
execution_mode:
  
  lightweight:
    description: "Cho task nhỏ, patch nhanh, hotfix"
    timeout: 300  # 5 phút
    
    gates:
      pre_build: false
      post_build: false
      confirmation: false
      design_phase: none
    
    output:
      format: "patch_delta | adapted_skill"
      validation_level: "syntax_only"
      build_log: "minimal"
    
    interaction:
      ask_before_proceed: false
  
  standard:
    description: "Workflow bình thường cho hầu hết task"
    timeout: 1800  # 30 phút
    
    gates:
      pre_build: true
      post_build: true
      confirmation: true
      design_phase: full
    
    output:
      format: "full_skill_package"
      validation_level: "standard"
      build_log: "standard"
    
    interaction:
      ask_before_proceed: true
  
  strict:
    description: "Cho critical skills, production deployment"
    timeout: 3600  # 60 phút
    
    gates:
      pre_build: true
      post_build: true
      confirmation: true
      design_phase: full
      extra_validation: true
      manual_signoff: true
    
    output:
      format: "full_skill_package + audit_bundle"
      validation_level: "comprehensive"
      build_log: "detailed_trace"
    
    interaction:
      ask_before_proceed: true
      manual_signoff_required: true
```

---

## 6. Transition Rules giữa các States

### 6.1 State Transition Table

```
┌──────────────────┬───────────────┬─────────────────────┬───────────────────┐
│ Current State     │ Event         │ Next State          │ Guard Condition   │
├──────────────────┼───────────────┼─────────────────────┼───────────────────┤
│ START             │ input_recv    │ DETECT              │ always            │
│ DETECT            │ type_identified│ CREATE_NEW          │ type=create_new   │
│ DETECT            │ type_identified│ PATCHING            │ type=patch        │
│ DETECT            │ type_identified│ REFACTORING         │ type=refactor     │
│ DETECT            │ type_identified│ MIGRATING           │ type=migrate      │
│ DETECT            │ type_identified│ CONSOLIDATING       │ type=consolidate  │
│ DETECT            │ type_identified│ DEPRECATING         │ type=deprecate    │
│ CREATE_NEW        │ design_done   │ BUILDING            │ always            │
│ BUILDING          │ build_done    │ VERIFYING           │ always            │
│ VERIFYING         │ verify_pass   │ DONE                │ always            │
│ VERIFYING         │ verify_fail   │ BUILDING            │ retry_available   │
│ PATCHING          │ patch_done    │ DONE                │ always            │
│ REFACTORING       │ refactor_done │ DONE                │ always            │
│ MIGRATING         │ migrate_done  │ DONE                │ always            │
│ CONSOLIDATING     │ consolidate_done│ DONE               │ always            │
│ DEPRECATING       │ deprecate_done│ DONE                │ always            │
└──────────────────┴───────────────┴─────────────────────┴───────────────────┘
```

### 6.2 Transition Rules Definition

```yaml
transition_rules:

  # === DETECT transitions ===
  rule_detect_to_create_new:
    from: DETECT
    event: type_identified
    to: CREATE_NEW
    guard: "operation_type == 'create_new'"
    action: log_detection_result

  rule_detect_to_patch:
    from: DETECT
    event: type_identified
    to: PATCHING
    guard: "operation_type == 'patch_existing'"
    action: load_existing_skill

  rule_detect_to_refactor:
    from: DETECT
    event: type_identified
    to: REFACTORING
    guard: "operation_type == 'refactor_existing'"
    action: audit_existing_skill

  rule_detect_to_migrate:
    from: DETECT
    event: type_identified
    to: MIGRATING
    guard: "operation_type == 'migrate_platform'"
    action: detect_platforms

  rule_detect_to_consolidate:
    from: DETECT
    event: type_identified
    to: CONSOLIDATING
    guard: "operation_type == 'consolidate_skills'"
    action: load_all_source_skills

  rule_detect_to_deprecate:
    from: DETECT
    event: type_identified
    to: DEPRECATING
    guard: "operation_type == 'deprecate_skill'"
    action: verify_no_dependencies

  # === CREATE_NEW pipeline ===
  rule_create_to_building:
    from: CREATE_NEW
    event: design_approved
    to: BUILDING
    guard: "always"
    action: prepare_build_environment

  rule_building_to_verify:
    from: BUILDING
    event: implementation_complete
    to: VERIFYING
    guard: "always"
    action: run_validation

  rule_verify_to_done:
    from: VERIFYING
    event: verification_passed
    to: DONE
    guard: "always"
    action: deliver_output

  rule_verify_retry:
    from: VERIFYING
    event: verification_failed
    to: BUILDING
    guard: "retry_count < max_retries"
    action: increment_retry, log_failure

  # === PATCH pipeline ===
  rule_patch_to_done:
    from: PATCHING
    event: patch_applied
    to: DONE
    guard: "always"
    action: deliver_patch_delta

  # === REFACTOR pipeline ===
  rule_refactor_to_done:
    from: REFACTORING
    event: refactor_complete
    to: DONE
    guard: "always"
    action: deliver_refactored_skill

  # === MIGRATE pipeline ===
  rule_migrate_to_done:
    from: MIGRATING
    event: migration_complete
    to: DONE
    guard: "always"
    action: deliver_migrated_skill

  # === CONSOLIDATE pipeline ===
  rule_consolidate_to_done:
    from: CONSOLIDATING
    event: consolidation_complete
    to: DONE
    guard: "always"
    action: deliver_merged_skill

  # === DEPRECATE pipeline ===
  rule_deprecate_to_done:
    from: DEPRECATING
    event: deprecation_complete
    to: DONE
    guard: "always"
    action: deliver_deprecation_notice
```

### 6.3 Error Handling Rules

```yaml
error_handling:

  detection_failure:
    on_state: DETECT
    condition: "cannot_determine_operation_type"
    action: fallback_to_create_new
    next_state: CREATE_NEW

  verification_failure:
    on_state: VERIFYING
    condition: "verification_failed AND retry_count >= max_retries"
    action: halt_with_error_report
    next_state: ERROR

  platform_detection_failure:
    on_state: MIGRATING
    condition: "cannot_detect_source_platform"
    action: request_explicit_platform_specification
    next_state: MIGRATING (awaiting input)

  dependency_conflict:
    on_state: DEPRECATING
    condition: "skill_has_active_dependencies"
    action: block_deprecation_until_migrated
    next_state: DETECT (suggest migrate first)
```

### 6.4 State Machine Visualization

```
┌─────────┐  input_recv  ┌─────────┐ type_identified ┌──────────────────┐
│  START  │─────────────▶│  DETECT │────────────────▶│ (branch by type) │
└─────────┘              └─────────┘                 └────────┬─────────┘
                                                                │
                        ┌───────────────────────────────────────┼───────────────┐
                        │                                       │               │
                        ▼                                       ▼               ▼
               ┌─────────────┐                          ┌─────────────┐ ┌─────────────┐
               │ CREATE_NEW  │                          │  PATCHING   │ │REFACTORING  │
               └──────┬──────┘                          └──────┬──────┘ └──────┬──────┘
                      │                                          │               │
               design_approved                            patch_applied  refactor_done
                      │                                          │               │
                      ▼                                          │               │
               ┌─────────────┐                                     │               │
               │  BUILDING   │                                     │               │
               └──────┬──────┘                                     │               │
                      │                                            │               │
              build_done                                            │               │
                      │                                            │               │
                      ▼                                            │               │
               ┌─────────────┐                                     │               │
               │ VERIFYING   │                                     │               │
               └──────┬──────┘                                     │               │
                      │                                            │               │
        ┌─────────────┼─────────────┐                             │               │
        │             │             │                             │               │
  verify_pass  verify_fail  verify_fail                            │               │
        │             │       (retry exhausted)                    │               │
        ▼             ▼             ▼                             │               │
   ┌─────────┐  ┌─────────────┐ ┌─────────┐                        │               │
   │  DONE   │  │  BUILDING   │ │  ERROR  │                        │               │
   └─────────┘  └─────────────┘ └─────────┘                        │               │
                                                                    │               │
                        ┌───────────────────────────────────────────┼───────────────┤
                        │                                           │               │
                        ▼                                           ▼               ▼
               ┌─────────────┐                              ┌─────────────┐ ┌─────────────┐
               │ MIGRATING   │                              │CONSOLIDATING│ │ DEPRECATING │
               └──────┬──────┘                              └──────┬──────┘ └──────┬──────┘
                      │                                             │               │
               migrate_done                                   consolidate_done deprecate_done
                      │                                             │               │
                      ▼                                             ▼               ▼
                 ┌─────────┐                                    ┌─────────┐    ┌─────────┐
                 │  DONE   │                                    │  DONE   │    │  DONE   │
                 └─────────┘                                    └─────────┘    └─────────┘
```

---

## 7. Mode × Operation: Detailed Gate Configuration

### 7.1 Gate Matrix

| Operation | Mode | Pre-Build | Post-Build | Confirmation | Design Phase | Extra Validation | Manual Signoff |
|-----------|------|:---------:|:----------:|:------------:|:------------:|:----------------:|:--------------:|
| create_new | lightweight | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_new | standard | ✅ | ✅ | ✅ | ✅ (full) | ❌ | ❌ |
| create_new | strict | ✅ | ✅ | ✅ | ✅ (formal) | ✅ | ✅ |
| patch_existing | lightweight | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| patch_existing | standard | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| patch_existing | strict | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| refactor_existing | lightweight | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| refactor_existing | standard | ✅ | ✅ | ✅ | ✅ (fast) | ❌ | ❌ |
| refactor_existing | strict | ✅ | ✅ | ✅ | ✅ (formal) | ✅ | ✅ |
| migrate_platform | lightweight | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| migrate_platform | standard | ✅ | ✅ | ✅ | ✅ (fast) | ❌ | ❌ |
| migrate_platform | strict | ✅ | ✅ | ✅ | ✅ (formal) | ✅ | ✅ |
| consolidate_skills | lightweight | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| consolidate_skills | standard | ✅ | ✅ | ✅ | ✅ (fast) | ❌ | ❌ |
| consolidate_skills | strict | ✅ | ✅ | ✅ | ✅ (formal) | ✅ | ✅ |
| deprecate_skill | lightweight | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| deprecate_skill | standard | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| deprecate_skill | strict | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |

### 7.2 Timeout Configuration

| Operation | Lightweight | Standard | Strict |
|-----------|:-----------:|:--------:|:------:|
| create_new | — | 1800s | 3600s |
| patch_existing | 300s | 600s | 900s |
| refactor_existing | — | 2400s | 3600s |
| migrate_platform | 600s | 1200s | 1800s |
| consolidate_skills | — | 1800s | 3600s |
| deprecate_skill | 180s | 300s | 600s |

---

## 8. Implementation Notes

### 8.1 State Machine Implementation Pattern

```python
class OperationStateMachine:
    """
    State machine cho operation type detection và execution.
    """
    
    STATES = [
        'START', 'DETECT',
        'CREATE_NEW', 'BUILDING', 'VERIFYING',
        'PATCHING', 'REFACTORING', 'MIGRATING',
        'CONSOLIDATING', 'DEPRECATING',
        'DONE', 'ERROR'
    ]
    
    def __init__(self):
        self.current_state = 'START'
        self.operation_type = None
        self.context = {}
        self.retry_count = 0
        self.max_retries = 3
    
    def transition(self, event):
        """Xử lý event và transition state."""
        
        transition_map = {
            ('START', 'input_recv'): 'DETECT',
            ('DETECT', 'type_identified'): self._get_operation_state(),
            ('CREATE_NEW', 'design_approved'): 'BUILDING',
            ('BUILDING', 'implementation_complete'): 'VERIFYING',
            ('VERIFYING', 'verification_passed'): 'DONE',
            ('VERIFYING', 'verification_failed'): self._handle_verify_fail(),
            ('PATCHING', 'patch_applied'): 'DONE',
            ('REFACTORING', 'refactor_complete'): 'DONE',
            ('MIGRATING', 'migration_complete'): 'DONE',
            ('CONSOLIDATING', 'consolidation_complete'): 'DONE',
            ('DEPRECATING', 'deprecation_complete'): 'DONE',
        }
        
        key = (self.current_state, event)
        next_state = transition_map.get(key)
        
        if next_state:
            self.current_state = next_state
            return next_state
        
        raise InvalidTransition(f"Cannot transition from {self.current_state} on {event}")
    
    def _get_operation_state(self):
        """Map operation type sang initial state."""
        
        type_to_state = {
            'create_new': 'CREATE_NEW',
            'patch_existing': 'PATCHING',
            'refactor_existing': 'REFACTORING',
            'migrate_platform': 'MIGRATING',
            'consolidate_skills': 'CONSOLIDATING',
            'deprecate_skill': 'DEPRECATING',
        }
        
        return type_to_state.get(self.operation_type, 'ERROR')
```

### 8.2 Detection Heuristics

```python
DETECTION_HEURISTICS = {
    'create_new': {
        'required': ['scope == new_domain'],
        'forbidden': ['existing_skill_path'],
        'weight': 1.0
    },
    'patch_existing': {
        'required': ['existing_skill_path'],
        'conditions': ['len(changed_files) <= 3', 'change_percentage < 20'],
        'weight': 0.9
    },
    'refactor_existing': {
        'required': ['existing_skill_path'],
        'conditions': ['action in [split, merge, rename, restructure]'],
        'weight': 0.95
    },
    'migrate_platform': {
        'required': ['source_platform != target_platform'],
        'weight': 1.0
    },
    'consolidate_skills': {
        'required': ['len(skills_to_consolidate) > 1'],
        'weight': 1.0
    },
    'deprecate_skill': {
        'required': ['intent == deprecate'],
        'weight': 1.0
    }
}
```

---

## 9. Appendix

### 9.1 Reference

- Skill Suite Proposal: `docs/raw/ideas/skill-suite-improvement-raw-notes/2026-05-09-proposal-operation-types-execution-modes-refinement-loop.vi.md`
- AGENTS.md: `docs/raw/AGENTS.md`

### 9.2 Changelog

| Ngày | Mô tả |
|------|-------|
| 2026-05-09 | Initial design document |
