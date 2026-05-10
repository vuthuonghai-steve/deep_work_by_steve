# Đề xuất: Operation Types, Execution Modes & Refinement Loop

> Ngày: 2026-05-09  
> Tác giả: Hermes Agent  
> Trạng thái: Raw proposal cho Issue #9.5, #9.6, #9.7  
> Thư mục: `docs/raw/ideas/`

---

## Tóm tắt vấn đề

| Issue | Mô tả | Hệ quả |
|-------|-------|--------|
| **#9.5** | Vòng học từ feedback chưa hoàn chỉnh | Không có cơ chế cải thiện liên tục |
| **#9.6** | Quá nhiều gate cho task nhỏ | Overhead không phù hợp với patch nhỏ |
| **#9.7** | Chỉ hỗ trợ create_new | Không support patch/refactor/migrate |

---

## 1. Operation Type Enum

### 1.1 Enum Definition

```yaml
operation_type:
  enum:
    - create_new       # Tạo skill hoàn toàn mới
    - patch_existing   # Sửa một phần nhỏ của skill hiện có
    - refactor_existing # Tái cấu trúc toàn bộ skill (đổi tên, split, merge)
    - migrate_platform # Di chuyển skill giữa các platform (Claude ↔ Hermes)
    - consolidate_skills # Gộp nhiều skill thành một
    - deprecate_skill  # Đánh dấu skill là deprecated

  behavior_modifiers:
    create_new:
      requires_full_pipeline: true
      gates: [design, plan, build, verify]
      output_scope: full_skill_package
      persona_emphasis: architect_mode
      
    patch_existing:
      requires_full_pipeline: false
      gates: [verify]
      output_scope: minimal_delta
      persona_emphasis: surgical_mode
      
    refactor_existing:
      requires_full_pipeline: true
      gates: [design, build, verify]
      output_scope: full_skill_package_with_migration
      persona_emphasis: refactor_mode
      
    migrate_platform:
      requires_full_pipeline: true
      gates: [verify]
      output_scope: adapted_skill_package
      persona_emphasis: migrate_mode
      
    consolidate_skills:
      requires_full_pipeline: true
      gates: [design, build, verify]
      output_scope: merged_skill_package
      persona_emphasis: consolidate_mode
      
    deprecate_skill:
      requires_full_pipeline: false
      gates: []
      output_scope: deprecation_notice
      persona_emphasis: cleanup_mode
```

### 1.2 Detection Logic (Pseudocode)

```python
def detect_operation_type(context):
    """
    Builder tự động detect operation type từ input context.
    """
    
    # Case 1: Hoàn toàn mới — không có skill reference
    if not context.get('existing_skill_path'):
        if context.get('scope') == 'new_domain':
            return 'create_new'
    
    # Case 2: Có reference đến skill hiện có
    existing_skill = context.get('existing_skill_path')
    
    # Patch detection: chỉ thay đổi < 20% content, < 3 files
    changed_files = context.get('changed_files', [])
    if len(changed_files) <= 3:
        return 'patch_existing'
    
    # Refactor detection: thay đổi cấu trúc, split, merge
    if context.get('action') in ['split', 'merge', 'rename']:
        return 'refactor_existing'
    
    # Migrate detection: có platform context
    if context.get('source_platform') != context.get('target_platform'):
        return 'migrate_platform'
    
    # Deprecate detection
    if context.get('intent') == 'deprecate':
        return 'deprecate_skill'
    
    # Default: fallback to standard create
    return 'create_new'
```

### 1.3 Persona Adjustments by Operation Type

| Operation Type | Persona Shift | Prompt Modifier |
|---------------|---------------|-----------------|
| `create_new` | Full architect mode | "Thiết kế từ đầu, đầy đủ 3 stage" |
| `patch_existing` | Surgical mode | "Chỉ thay đổi tối thiểu cần thiết" |
| `refactor_existing` | Refactor mode | "Giữ nguyên behavior, cải cấu trúc" |
| `migrate_platform` | Migrate mode | "Thích ứng sang target platform" |
| `consolidate_skills` | Consolidate mode | "Gộp và chuẩn hóa các skill" |
| `deprecate_skill` | Cleanup mode | "Đánh dấu và cleanup" |

**Chi tiết persona adjustments:**

```yaml
persona_adjustments:
  patch_existing:
    default_persona: "Senior Implementation Engineer"
    modifier: |
      Bỏ qua Design Phase hoàn toàn.
      Đọc skill hiện có và chỉ thay đổi những phần được chỉ định.
      KHÔNG tạo design.md hay todo.md mới — chỉ tạo patch diff.
      
    output_contract: |
      Output: Patch delta thay vì full skill package.
      Format: unified diff hoặc JSON patch.
      
    gate_behavior: |
      Bỏ qua confirmation gates.
      Chỉ chạy validate_skill.py cho các file bị thay đổi.
      
  refactor_existing:
    default_persona: "Senior Refactoring Engineer"
    modifier: |
      Design Phase tập trung vào migration plan thay vì tạo mới.
      Phân tích skill hiện có và đề xuất cấu trúc mới.
      Đảm bảo behavior equivalence sau refactor.
      
    output_contract: |
      Output: Refactored skill + migration guide.
      Phải có diff giữa old và new structure.
      
  migrate_platform:
    default_persona: "Platform Migration Engineer"
    modifier: |
      Tập trung vào platform-specific adaptations.
      Map paths và conventions từ source → target platform.
      
    output_contract: |
      Output: Platform-adapted skill.
      Đảm bảo skill load được trên target platform.
```

---

## 2. Execution Mode Configuration

### 2.1 Mode Enum

```yaml
execution_mode:
  enum:
    - lightweight  # Minimal gates, fast execution
    - standard     # Balanced workflow (default)
    - strict       # Full gates, maximum validation
  
  mode_parameters:
    lightweight:
      description: "Cho task nhỏ, patch nhanh, hotfix"
      
      gates:
        pre_build: false
        post_build: false
        confirmation: false
        design_phase: abbreviated  # Chỉ checkpoint ngắn
      
      output:
        format: "patch_delta"
        validation_level: "syntax_only"
        build_log: "minimal"
        
      timing:
        timeout: 300  # 5 phút max
        
      interaction:
        ask_before_proceed: false
        
    standard:
      description: "Workflow bình thường cho hầu hết task"
      
      gates:
        pre_build: true   # Feasibility check
        post_build: true  # Quality gate
        confirmation: true  # Phase transitions
        design_phase: full  # Đầy đủ 3 phase
      
      output:
        format: "full_skill_package"
        validation_level: "standard"
        build_log: "standard"
        
      timing:
        timeout: 1800  # 30 phút
        
      interaction:
        ask_before_proceed: true
        
    strict:
      description: "Cho critical skills, production deployment"
      
      gates:
        pre_build: true
        post_build: true
        confirmation: true
        design_phase: full
        extra_validation: true  # Thêm manual review step
        
      output:
        format: "full_skill_package + audit_bundle"
        validation_level: "comprehensive"
        build_log: "detailed_trace"
        
      timing:
        timeout: 3600  # 60 phút
        
      interaction:
        ask_before_proceed: true
        manual_signoff_required: true
```

### 2.2 Mode × Operation Type Matrix

| Operation \ Mode | lightweight | standard | strict |
|------------------|-------------|----------|--------|
| `create_new` | ⚠️ N/A (needs design) | ✅ Default | ✅ Full |
| `patch_existing` | ✅ Default | ✅ Available | ⚠️ Overkill |
| `refactor_existing` | ❌ N/A (needs design) | ✅ Default | ✅ Full |
| `migrate_platform` | ⚠️ Limited | ✅ Default | ✅ Full |
| `consolidate_skills` | ❌ N/A | ✅ Default | ✅ Full |
| `deprecate_skill` | ✅ Default | ✅ Available | ⚠️ Overkill |

### 2.3 Workflow Changes by Mode

**Lightweight Mode Workflow:**

```
1. DETECT operation_type
2. PATCH (minimal):
   - Đọc skill hiện có
   - Áp dụng thay đổi được chỉ định
   - Syntax check nhanh
3. DELIVER:
   - Output patch diff
   - Không tạo build log đầy đủ
```

**Standard Mode Workflow:**

```
1. DETECT operation_type
2. PREPARE:
   - Đọc inputs (design.md, todo.md nếu có)
   - Assess feasibility
3. CLARIFY (nếu cần)
4. BUILD phase-by-phase
5. VERIFY (quality gate)
6. DELIVER:
   - Full skill package
   - Standard build log
```

**Strict Mode Workflow:**

```
1. DETECT operation_type
2. PREPARE + AUDIT:
   - Đọc inputs đầy đủ
   - Audit existing skills thoroughly
3. DESIGN REVIEW (formal):
   - Xuất design.md
   - Review và approval
4. PLAN REVIEW:
   - Xuất todo.md
   - Verify coverage
5. BUILD + VALIDATE:
   - Implement theo plan
   - Chạy full validation suite
   - Unit tests, integration tests
6. POST-BUILD REVIEW:
   - Manual code review
   - Manual signoff
7. DELIVER:
   - Full package + audit bundle
   - Detailed build log
```

---

## 3. Refinement Loop — 6-Step Formalization

### 3.1 Loop Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    REFINE CYCLE                              │
│                                                              │
│   [1. OBSERVE] ──→ [2. IDENTIFY] ──→ [3. DECIDE]            │
│         │                  │                 │               │
│         │                  │                 ▼               │
│         │                  │         ┌─────────────┐         │
│         │                  │         │   ACTION    │         │
│         │                  │         │ memory |     │         │
│         │                  │         │ patch |      │         │
│         │                  │         │ new |        │         │
│         │                  │         │ refactor    │         │
│         │                  │         └─────────────┘         │
│         │                  │                 │               │
│         ▼                  ▼                 ▼               │
│   [4. APPLY] ──→ [5. DOCUMENT] ──→ [6. VERIFY]              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Step Definitions

```yaml
refinement_loop:
  
  step_1_observe:
    name: "Observe Session"
    description: "Thu thập data từ session thật"
    
    inputs:
      - session_transcript
      - user_feedback
      - error_logs
      - skill_invocation_logs
    
    actions:
      - Track which skills được invoke
      - Track success/failure patterns
      - Note confusion points hoặc breakdowns
      - Measure time-to-completion
    
    output: "session_analysis_report"
    
  step_2_identify:
    name: "Identify Pain Points"
    description: "Phân tích observation để tìm pattern"
    
    triggers:
      - Same error > 3 lần trong 10 session
      - User manually bypasses skill flow
      - Skill produces wrong format output
      - Missing capability được request > 5 lần
    
    analysis:
      - Categorize: missing_knowledge | broken_flow | wrong_prompting | missing_edge_case
      - Prioritize: critical | major | minor
      - Root cause analysis
    
    output: "pain_point_list with severity"
    
  step_3_decide:
    name: "Decide Action"
    description: "Chọn action phù hợp nhất"
    
    decision_tree:
      - memory_update:
          condition: "Knowledge missing but skill logic correct"
          action: "Ghi vào memory/knowledge file"
          
      - patch_existing:
          condition: "Skill hoạt động nhưng thiếu/chứa lỗi nhỏ"
          action: "Áp dụng minimal patch"
          scope: "≤ 3 files, ≤ 20% content changes"
          
      - create_new:
          condition: "Hoàn toàn new capability, không liên quan skill hiện có"
          action: "Tạo skill mới"
          
      - refactor_existing:
          condition: "Skill structure không phù hợp, cần tái cấu trúc"
          action: "Refactor toàn bộ skill"
          
      - deprecate_skill:
          condition: "Skill lỗi thời hoặc duplicate"
          action: "Đánh dấu deprecated"
    
    output: "action_plan with type"
    
  step_4_apply:
    name: "Apply Minimal Patch"
    description: "Thực thi action đã chọn với minimal change"
    
    principles:
      - Change tối thiểu cần thiết
      - Preserve working functionality
      - Testable outputs
    
    constraints:
      - patch_existing: "Chỉ thay đổi phần được xác định"
      - create_new: "Dùng standard pipeline"
      - refactor: "Maintain behavior equivalence"
    
    output: "modified_skill_content"
    
  step_5_document:
    name: "Document Change"
    description: "Ghi lại lý do và nội dung thay đổi"
    
    required_fields:
      - timestamp
      - operation_type
      - trigger_reason
      - specific_changes
      - before_after_diff_summary
    
    format: |
      ```yaml
      # .skill-context/{skill-name}/refinement-log.yaml
      refinement_history:
        - date: 2026-05-09
          operation_type: patch_existing
          trigger: "User reported wrong output format in Phase 2"
          changes:
            - file: SKILL.md
              section: workflow
              before: "Use format X"
              after: "Use format Y"
         验证: passed
      ```
    
    output: "refinement_log entry"
    
  step_6_verify:
    name: "Verify Skill"
    description: "Đảm bảo skill vẫn load được và đủ gọn"
    
    verification_checks:
      - skill_loads: true
      - size_within_limit: true  # SKILL.md ≤ 500 lines
      - no_hallucination: validated
      - output_format_correct: verified
    
    tools:
      - validate_skill.py
      - size check
      - syntax validation
    
    output: "verification_report"
```

### 3.3 Trigger Conditions

```yaml
refinement_triggers:
  
  automatic:
    schedule: "After every 10 skill invocations"
    checks:
      - error_rate > 5%
      - user_abort_rate > 10%
      - average_time_increased > 30%
  
  manual:
    triggers:
      - User explicitly reports issue
      - Developer reviews skill performance
      - New capability request
  
  session_end:
    triggers:
      - Session contains > 3 skill invocations
      - Any invocation failed
```

---

## 4. Skill-Builder Detection & Adaptation

### 4.1 Detection Flow

```yaml
skill_builder_detection:
  
  entry_point:
    description: "Builder được invoke với context"
    
  detection_sequence:
    1_check_existing_skill:
      condition: "context.existing_skill_path exists"
      result: "operation_type = patch|refactor|migrate|deprecate"
      
    2_check_scope:
      condition: "context.scope == 'new_domain'"
      result: "operation_type = create_new"
      
    3_check_platform_context:
      condition: "context.source_platform != context.target_platform"
      result: "operation_type = migrate_platform"
      
    4_check_action_verb:
      condition: "context.action in ['split', 'merge', 'rename']"
      result: "operation_type = refactor_existing"
      
    5_check_intent:
      condition: "context.intent == 'deprecate'"
      result: "operation_type = deprecate_skill"
  
  default_fallback:
    if_no_match:
      operation_type: "create_new"
      execution_mode: "standard"
```

### 4.2 Behavior Adaptation Matrix

| Context Signal | Default | Override |
|---------------|---------|----------|
| `execution_mode: lightweight` | Full pipeline | Skip gates, output patch |
| `operation_type: patch_existing` | 3-stage pipeline | Skip design/plan, output delta |
| `operation_type: deprecate_skill` | Normal workflow | Skip build, output notice |
| `operation_type: migrate_platform` | 3-stage pipeline | Add platform mapping phase |

### 4.3 Workflow Pseudo-code

```python
def skill_builder_workflow(context):
    # Step 1: Detect
    operation_type = detect_operation_type(context)
    execution_mode = context.get('execution_mode', 'standard')
    
    # Step 2: Load persona modifier
    persona = get_adjusted_persona(operation_type)
    
    # Step 3: Apply workflow based on operation_type + mode
    
    if operation_type == 'patch_existing':
        if execution_mode == 'lightweight':
            return patch_lightweight_workflow(context)
        else:
            return patch_standard_workflow(context)
            
    elif operation_type == 'create_new':
        return standard_3stage_pipeline(context)
        
    elif operation_type == 'refactor_existing':
        return refactor_workflow(context)
        
    elif operation_type == 'migrate_platform':
        return migrate_workflow(context)
        
    elif operation_type == 'deprecate_skill':
        return deprecate_workflow(context)
    
    elif operation_type == 'consolidate_skills':
        return consolidate_workflow(context)
```

### 4.4 Minimal Patch Workflow (lightweight)

```python
def patch_lightweight_workflow(context):
    """
    For lightweight patch operations.
    """
    
    # 1. Read existing skill
    skill_path = context.existing_skill_path
    existing_skill = read_skill(skill_path)
    
    # 2. Apply minimal changes
    changes = context.get('changes', [])
    patched_skill = apply_delta(existing_skill, changes)
    
    # 3. Syntax validation only
    validate_syntax(patched_skill)
    
    # 4. Output patch diff (not full package)
    return PatchResult(
        format='diff',
        files_changed=changes.keys(),
        validation='syntax_only'
    )
```

### 4.5 Refactor Workflow

```python
def refactor_workflow(context):
    """
    For refactor operations - maintains behavior equivalence.
    """
    
    # 1. Read existing skill
    existing_skill = read_skill(context.existing_skill_path)
    
    # 2. Analyze current structure
    current_structure = analyze_structure(existing_skill)
    
    # 3. Create refactoring plan (abbreviated design)
    # - Keep same behavior
    # - Improve structure
    # - Split if needed
    # - Merge if needed
    
    # 4. Execute refactor
    new_skill = execute_refactor(existing_skill, context.plan)
    
    # 5. Verify behavior equivalence
    verify_equivalence(existing_skill, new_skill)
    
    # 6. Output: new skill + migration guide
    return RefactorResult(
        new_skill=new_skill,
        migration_guide=generate_diff(existing_skill, new_skill)
    )
```

---

## 5. YAML Schema Examples

### 5.1 Context Input Schema

```yaml
# Input cho skill-builder invocation
context:
  # Operation detection
  operation_type: patch_existing  # detected hoặc specified
  execution_mode: lightweight      # lightweight | standard | strict
  
  # Skill identification
  existing_skill_path: ~/.hermes/skills/coding-agent/
  target_skill_path: ~/.hermes/skills/coding-agent/
  
  # Change specification (for patch)
  changes:
    - file: SKILL.md
      section: workflow
      before: "..."
      after: "..."
    - file: knowledge/errors.md
      action: append
      content: |
        ## New Error Pattern
        
  # Platform context (for migrate)
  source_platform: claude
  target_platform: hermes
  
  # User preferences
  skip_confirmation: true
  validation_level: syntax_only
```

### 5.2 Output Contract by Operation Type

```yaml
# create_new → standard mode
output:
  type: full_skill_package
  files:
    - SKILL.md
    - knowledge/
    - scripts/
    - templates/
    - data/
    - loop/
  build_log: build-log.md

# patch_existing → lightweight mode
output:
  type: patch_delta
  files:
    - {changed_files_only}
  diff_format: unified
  validation: syntax_only

# migrate_platform → standard mode
output:
  type: adapted_skill_package
  files:
    - {all_skill_files}
    - platform-mapping.yaml
  migration_notes: migration-log.md

# deprecate_skill → any mode
output:
  type: deprecation_notice
  files:
    - DEPRECATED.md
    - {original_skill}_archived/
```

---

## 6. Integration với Existing Suite

### 6.1 Frontmatter Extensions

```yaml
# design.md frontmatter — thêm operation_type
---
name: skill-name
operation_type: create_new | patch_existing | refactor_existing | ...
execution_mode: lightweight | standard | strict
zone_mapping:
  # ... existing
---

# todo.md frontmatter — thêm operation context
---
operation_type: patch_existing
affected_files:
  - SKILL.md
  - knowledge/errors.md
patch_scope: minimal
---
```

### 6.2 Validator Updates

```python
# validate_skill.py — thêm detection logic

def validate_operation(context):
    operation_type = context.get('operation_type', 'create_new')
    
    if operation_type == 'patch_existing':
        # Chỉ validate changed files
        for file in context.changed_files:
            validate_file_syntax(file)
            
    elif operation_type == 'deprecate_skill':
        # Chỉ check deprecation notice format
        validate_deprecation_notice(context)
        
    else:
        # Full validation như hiện tại
        full_validation(context)
```

### 6.3 Skill-Builder SKILL.md Update

```markdown
## Skill Behavior by Operation Type

Khi được invoke, skill-builder tự động detect operation_type và điều chỉnh workflow:

| Operation Type | Workflow | Gates | Output |
|----------------|----------|-------|--------|
| `create_new` | 3-stage pipeline | Design → Plan → Build → Verify | Full package |
| `patch_existing` | Abbreviated | Verify only | Patch delta |
| `refactor_existing` | Full pipeline | Design → Build → Verify | Refactored + diff |
| `migrate_platform` | Full pipeline | Verify (platform checks) | Adapted package |
| `deprecate_skill` | Minimal | None | Notice only |

## Execution Modes

| Mode | Gates | Speed | Use Case |
|------|-------|-------|----------|
| `lightweight` | None | Fast | Hotfix, small patches |
| `standard` | Standard | Normal | Most operations |
| `strict` | Full | Slow | Critical skills |
```

---

## 7. Summary

### Điểm chính

1. **Operation Type Enum** — 6 loại với behavior modifiers rõ ràng
2. **Execution Mode** — 3 mức độ từ lightweight đến strict  
3. **Refinement Loop** — 6-step formal process với trigger conditions
4. **Auto-detection** — Builder tự detect và adapt workflow

### Files cần tạo mới

- `skill-builder/knowledge/operation-types.md`
- `skill-builder/knowledge/execution-modes.md`
- `skill-builder/loop/refinement-loop.md`
- `skill-builder/schemas/context-input.schema.yaml`

### Files cần update

- `skill-builder/SKILL.md` — thêm detection logic và behavior matrix
- `skill-builder/scripts/validate_skill.py` — thêm operation-aware validation
- `_shared/knowledge/framework.md` — thêm operation type definitions

---

*Document này phục vụ như raw input cho giai đoạn tiếp theo của skill suite improvement.*