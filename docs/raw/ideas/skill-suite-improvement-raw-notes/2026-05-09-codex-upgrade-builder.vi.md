# Đề xuất nâng cấp skill-builder cho Hermes-native + Multi-Operation Support

> Ngày: 2026-05-09
> Tác giả: Codex CLI Agent
> Trạng thái: Actionable proposal
> Nguồn: Tổng hợp từ research master skill suite + gaps analysis

---

## 1. Operation Type Detection và Adaptive Workflow

### 1.1 Operation Type Enum

```yaml
operation_type:
  - create_new        # Tạo skill hoàn toàn mới từ design.md + todo.md
  - patch_existing    # Sửa một phần nhỏ của skill hiện có
  - refactor_existing # Tái cấu trúc lại skill, giữ nguyên chức năng
  - migrate_platform  # Di chuyển skill từ Claude platform sang Hermes
  - consolidate_skills# Gộp nhiều skill trùng lặp thành một
  - deprecate_skill   # Đánh dấu skill là deprecated, không còn maintain
```

### 1.2 Detection Logic (Pseudocode)

```python
def detect_operation_type(context) -> str:
    """
    Input: context chứa các signal từ hệ thống
    Output: operation_type phù hợp
    """
    signals = {
        'has_design_md': exists(context.design_md),
        'has_todo_md': exists(context.todo_md),
        'has_existing_skill': exists(context.target_skill_path),
        'target_platform': detect_platform(context),
        'operation_hint': context.user_hint or None
    }

    # Priority detection
    if signals['operation_hint']:
        return signals['operation_hint']  # User chỉ định rõ ràng

    if signals['has_design_md'] and signals['has_todo_md']:
        if not signals['has_existing_skill']:
            return 'create_new'
        else:
            return 'patch_existing'  # Có design mới + skill cũ → patch

    if signals['target_platform'] == 'hermes' and signals['has_existing_skill']:
        # Skill hiện có không phải Hermes → migrate
        current_platform = detect_existing_skill_platform(signals['has_existing_skill'])
        if current_platform != 'hermes':
            return 'migrate_platform'

    if signals['has_existing_skill'] and signals.get('consolidation_candidate'):
        return 'consolidate_skills'

    if signals['has_existing_skill'] and signals.get('deprecation_signal'):
        return 'deprecate_skill'

    # Fallback: refactor nếu có skill cũ nhưng không rõ intent
    if signals['has_existing_skill']:
        return 'refactor_existing'

    return 'create_new'  # Safe default
```

### 1.3 Per-Operation-Type Workflow Pseudocode

#### `create_new`
```python
def workflow_create_new(context):
    # 1. PREPARE: đọc design.md + todo.md + resources
    read_all_inputs(context)

    # 2. CLARIFY: hỏi user nếu có ambiguity (max 5 items)
    ask_clarifications(context, max_items=5)

    # 3. BUILD: tạo full skill package từ design §3 Zone Mapping
    for zone in design.zones:
        create_zone_files(zone, context)

    # 4. VERIFY: chạy validate_skill.py + placeholder check
    run_validation(context)

    # 5. DELIVER: ghi build-log.md + output ra install_target
    finalize_and_output(context)
```

#### `patch_existing`
```python
def workflow_patch_existing(context):
    # 1. READ: đọc skill hiện tại + design.md mới (nếu có)
    read_existing_skill(context)
    read_patch_spec(context)  # Có thể là diff hoặc partial design

    # 2. DIFF: so sánh existing vs patch spec
    diff_result = compute_diff(context.existing, context.patch_spec)

    # 3. PATCH: chỉ apply những thay đổi cần thiết
    apply_minimal_patch(diff_result, context)

    # 4. VALIDATE: chạy targeted validation (không full pipeline)
    run_targeted_validation(context, changed_files_only=True)

    # 5. LOG: ghi patch log vào build-log.md
    log_patch_operation(context, diff_result)
```

#### `refactor_existing`
```python
def workflow_refactor_existing(context):
    # 1. AUDIT: đọc toàn bộ skill hiện tại
    full_skill_audit(context)

    # 2. DESIGN_PLAN: tạo refactor plan dựa trên framework mới
    create_refactor_plan(context)

    # 3. REBUILD: tái tạo lại files theo plan (vẫn giữ chức năng)
    rebuild_skill_with_unchanged_semantics(context)

    # 4. VERIFY: đảm bảo refactor không thay đổi behavior
    verify_behavior_preservation(context)

    # 5. DELIVER: output + update build-log.md với refactor evidence
    finalize_with_refactor_evidence(context)
```

#### `migrate_platform`
```python
def workflow_migrate_platform(context):
    # 1. DETECT_SOURCE: xác định platform source (Claude, Codex, etc.)
    detect_source_platform(context)

    # 2. ANALYZE: đọc skill source + frontmatter metadata
    analyze_skill_for_migration(context)

    # 3. TRANSFORM: convert paths + references sang Hermes format
    transform_to_hermes_format(context)
    # - Thay .claude/skills/ → ~/.hermes/skills/
    # - Convert SKILL.md frontmatter sang Hermes schema
    # - Rewrite @references paths

    # 4. VALIDATE: Hermes-specific validation
    run_hermes_validation(context)

    # 5. OUTPUT: ghi ra Hermes-compatible target
    output_to_hermes_install_target(context)
```

#### `consolidate_skills`
```python
def workflow_consolidate_skills(context):
    # 1. INVENTORY: liệt kê các skills trùng lặp
    list_duplicate_candidates(context)

    # 2. ANALYZE: so sánh chức năng + overlap
    analyze_overlap_and_dedupe(context)

    # 3. MERGE_PLAN: tạo kế hoạch gộp
    create_merge_plan(context)

    # 4. EXECUTE: gộp files + deduplicate references
    execute_merge(context)

    # 5. CREATE_REDIRECT: tạo redirect/deprecation notice
    create_deprecation_redirects(context)
```

#### `deprecate_skill`
```python
def workflow_deprecate_skill(context):
    # 1. ARCHIVE: đánh dấu skill là deprecated trong metadata
    mark_deprecated(context)

    # 2. CREATE_NOTICE: tạo deprecation notice trong skill
    add_deprecation_notice(context)

    # 3. LOG: ghi lý do deprecation vào build-log
    log_deprecation_reason(context)

    # 4. CLEANUP: không xóa files, chỉ đánh dấu
    # (保留历史记录 cho future reference)
```

---

## 2. install_target Resolution Logic

### 2.1 Resolution Decision Tree

```
START
├── user_specified_install_target?
│   └── YES → use user-specified path
│
└── NO → detect from context
    │
    ├── platform === 'hermes'?
    │   ├── scope === 'user-local'
    │   │   └── YES → ~/.hermes/skills/{category}/{skill-name}/
    │   │
    │   └── scope === 'repo'
    │       └── YES → {repo_root}/skills/{category}/{skill-name}/
    │
    ├── platform === 'claude'?
    │   └── YES → ~/.claude/skills/{skill-name}/
    │
    └── platform === 'both' or 'auto'
        └── use whichever platform context is active
```

### 2.2 Resolution Rules (Priority Order)

```python
def resolve_install_target(context) -> str:
    """
    Resolution priority (highest to lowest):
    1. Explicit user override (cli flag --install-target)
    2. Frontmatter in design.md (install_target field)
    3. Platform detection from environment
    4. Default fallback per platform
    """

    # Rule 1: User override
    if context.user_install_target:
        return context.user_install_target

    # Rule 2: Frontmatter in design.md
    if context.design_md and has_yaml_frontmatter(context.design_md):
        frontmatter = parse_yaml_frontmatter(context.design_md)
        if 'install_target' in frontmatter:
            return resolve_path_template(
                frontmatter['install_target'],
                {
                    'skill_name': context.skill_name,
                    'category': context.category or 'general',
                    'platform': context.platform
                }
            )

    # Rule 3: Platform detection
    platform = detect_active_platform(context)

    if platform == 'hermes':
        scope = context.scope or 'user-local'
        if scope == 'user-local':
            return f"~/.hermes/skills/{context.category or 'general'}/{context.skill_name}/"
        elif scope == 'repo':
            return f"{context.repo_root}/skills/{context.category or 'general'}/{context.skill_name}/"

    elif platform == 'claude':
        return f"~/.claude/skills/{context.skill_name}/"

    # Rule 4: Default fallback
    return f"~/.hermes/skills/general/{context.skill_name}/"
```

### 2.3 Platform vs Scope Matrix

| Platform | Scope | Target Path |
|----------|-------|-------------|
| hermes | user-local | `~/.hermes/skills/{category}/{skill-name}/` |
| hermes | repo | `{repo}/skills/{category}/{skill-name}/` |
| hermes | project-local | `{project}/.hermes/skills/{skill-name}/` |
| claude | user-local | `~/.claude/skills/{skill-name}/` |
| claude | repo | (rarely used) |
| both | user-local | `~/.hermes/skills/...` (preferred) |

### 2.4 install_target Frontmatter Schema

```yaml
---
name: {skill-name}
install_target:
  platform: hermes  # hermes | claude | both
  scope: user-local # user-local | repo | project-local
  path: ~/.hermes/skills/{category}/{skill-name}/
---
```

---

## 3. Validator Upgrade: YAML-First + Markdown Migration Validation

### 3.1 Upgrade Strategy

**Problem hiện tại:**
- Validator dùng regex parse Markdown tables → fragile
- Không đọc frontmatter trước → miss canonical contract
- Hardcode expected files → không linh hoạt

**Solution:**
- Read YAML frontmatter TRƯỚC khi parse Markdown
- Dùng frontmatter như canonical source of truth
- Markdown body chỉ là giải thích cho con người

### 3.2 YAML Frontmatter Schema cho các artifacts

```yaml
---
# design.md frontmatter
contract_version: "1.0"
skill_name: {skill-name}
operation_type: create_new
install_target:
  platform: hermes
  scope: user-local
  path: ~/.hermes/skills/general/{skill-name}/
zone_mapping:
  SKILL.md:
    tier: 1
    mandatory: true
  knowledge/architect.md:
    tier: 2
    mandatory: true
  scripts/validate_skill.py:
    tier: 2
    mandatory: false
progressive_disclosure:
  tier1: [SKILL.md]
  tier2: [knowledge/*, scripts/*]
  tier3: [loop/*, templates/*, assets/*]
execution_mode: standard
---

<!-- Markdown body for human readers -->
```

```yaml
---
# todo.md frontmatter
contract_version: "1.0"
skill_name: {skill-name}
phases:
  - id: 1
    name: PREPARE
    tasks:
      - id: 1.1
        description: Read design.md and audit resources
        source_ref: design.md §1
      - id: 1.2
        description: Assess feasibility
        source_ref: design.md §2
  - id: 2
    name: BUILD
    tasks:
      - id: 2.1
        description: Create SKILL.md
        block_by: [1.1, 1.2]
blockers:
  - id: B1
    description: Ambiguous routing rules
    phase: PREPARE
prerequisites:
  - design.md
  - todo.md
  - resources/
---

<!-- Markdown body: human-readable task list -->
```

```yaml
---
# build-log.md frontmatter
contract_version: "1.0"
skill_name: {skill-name}
operation_type: create_new
execution_trace:
  - timestamp: "2026-05-09T10:00:00Z"
    phase: PREPARE
    action: read_inputs
    files_read: [design.md, todo.md, resources/domain.md]
  - timestamp: "2026-05-09T10:15:00Z"
    phase: BUILD
    action: create_file
    output: knowledge/architect.md
    source: resources/domain.md
quality_metrics:
  placeholder_count: 3
  files_created: 12
  validation_passed: true
resource_usage:
  design.md: Critical
  resources/domain.md: Critical
  loop/build-checklist.md: Supportive
---

<!-- Markdown body: human-readable execution log -->
```

### 3.3 Validator Upgrade Pseudocode

```python
def validate_skill(skill_path, design_path=None, options=None):
    validator = HermesSkillValidator(options)

    # BƯỚC 1: Đọc YAML frontmatter TRƯỚC
    design_frontmatter = None
    if design_path and exists(design_path):
        design_frontmatter = parse_yaml_frontmatter(design_path)

    skill_frontmatter = None
    skill_md_path = join(skill_path, "SKILL.md")
    if exists(skill_md_path):
        skill_frontmatter = parse_yaml_frontmatter(skill_md_path)

    # BƯỚC 2: Extract canonical contract từ frontmatter
    if design_frontmatter:
        expected_zones = design_frontmatter.get('zone_mapping', {})
        expected_files = [f for f in expected_zones.keys()]

        # Override hardcoded expected_files bằng frontmatter
        validator.set_expected_files(expected_files)

    if skill_frontmatter:
        validator.set_skill_metadata(skill_frontmatter)

    # BƯỚC 3: Migration detection - validate Markdown → YAML conversion
    if design_frontmatter and design_frontmatter.get('source_format') == 'markdown':
        validator.check_migration_integrity(design_path)

    # BƯỚC 4: Các checks hiện tại (vẫn giữ để backward compat)
    validator.check_structure()
    validator.check_skill_md_constraints()
    validator.check_pd_links()

    # BƯỚC 5: Frontmatter-based validation (NEW)
    if design_frontmatter:
        validator.validate_zone_mapping(expected_zones, skill_path)
        validator.validate_progressive_disclosure(
            design_frontmatter.get('progressive_disclosure', {})
        )
        validator.validate_install_target_contracts(
            design_frontmatter.get('install_target', {})
        )

    return validator.report()
```

### 3.4 Migration Validation (Markdown → YAML)

```python
def check_migration_integrity(design_path):
    """
    Khi design.md được migrate từ pure Markdown sang YAML-first,
    validator cần check:
    1. YAML frontmatter có đầy đủ không?
    2. Markdown body có tương thích với frontmatter contract không?
    3. Zone mapping trong frontmatter có khớp với §3 table không?
    """

    frontmatter = parse_yaml_frontmatter(design_path)
    markdown_body = extract_markdown_body(design_path)

    # Check 1: Required fields in frontmatter
    required_frontmatter_fields = [
        'contract_version',
        'skill_name',
        'operation_type',
        'zone_mapping'
    ]
    for field in required_frontmatter_fields:
        if field not in frontmatter:
            raise ValidationError(f"Migration incomplete: missing {field} in frontmatter")

    # Check 2: Zone mapping consistency
    frontmatter_zones = set(frontmatter['zone_mapping'].keys())
    markdown_zones = extract_zone_table_from_markdown(markdown_body)

    if frontmatter_zones != markdown_zones:
        raise ValidationError(
            f"Zone mapping mismatch: frontmatter has {frontmatter_zones}, "
            f"markdown table has {markdown_zones}"
        )

    # Check 3: No data loss during migration
    critical_sections = ['## 1', '## 3', '## 7', '## 10']
    for section in critical_sections:
        if section not in markdown_body and section.replace('## ', '') not in frontmatter:
            log_warning(f"Critical section {section} may be lost in migration")
```

---

## 4. Patch Mode: Detect và Generate Diff

### 4.1 Patch Detection Logic

```python
def detect_patch_mode(context) -> bool:
    """
    Detect khi nào nên dùng patch mode thay vì full rebuild.
    """

    # Signal 1: Có file skill hiện tại + design.md mới
    if context.existing_skill_path and context.design_md:
        return True

    # Signal 2: Operation hint là 'patch_existing'
    if context.operation_type == 'patch_existing':
        return True

    # Signal 3: User chỉ định --diff flag
    if context.diff_mode_requested:
        return True

    # Signal 4: Design.md frontmatter có operation_type = patch
    if context.design_md:
        fm = parse_yaml_frontmatter(context.design_md)
        if fm.get('operation_type') in ['patch_existing', 'refactor_existing']:
            return True

    # Signal 5: Chỉ có một vài files thay đổi trong design
    if context.design_md and context.existing_skill_path:
        changed_zones = get_changed_zones(context.design_md, context.existing_skill_path)
        if len(changed_zones) <= 2:  # Chỉ 1-2 zones thay đổi
            return True

    return False
```

### 4.2 Diff Generation Workflow

```python
def generate_minimal_diff(context) -> DiffResult:
    """
    Chỉ generate diff thay vì full package.
    """

    existing_skill = read_existing_skill(context.existing_skill_path)
    new_spec = parse_design_spec(context.design_md)

    diff = {
        'added': [],
        'modified': [],
        'removed': [],
        'unchanged': []
    }

    # Compare each zone
    for zone_name, zone_spec in new_spec.zones.items():
        existing_zone = existing_skill.get(zone_name)

        if existing_zone is None:
            # Zone mới → add
            diff['added'].append({
                'zone': zone_name,
                'files': zone_spec.files,
                'action': 'CREATE'
            })
        elif zone_spec != existing_zone:
            # Zone khác → check files cụ thể
            file_diff = compare_zone_files(existing_zone, zone_spec)
            if file_diff['has_changes']:
                diff['modified'].append({
                    'zone': zone_name,
                    'files': file_diff,
                    'action': 'PATCH'
                })
        else:
            diff['unchanged'].append(zone_name)

    # Check for removed zones
    for zone_name in existing_skill.zones:
        if zone_name not in new_spec.zones:
            diff['removed'].append({
                'zone': zone_name,
                'action': 'DEPRECATE'
            })

    return diff
```

### 4.3 Builder Patch Workflow

```python
def builder_patch_workflow(context):
    """
    Workflow dành riêng cho patch mode.
    """

    # STEP 1: Analyze existing vs new spec
    diff = generate_minimal_diff(context)

    # STEP 2: Validate diff is minimal and safe
    if diff['added'] > 3 or diff['removed']:
        log_warning("Patch involves many changes. Consider refactor_existing instead.")
        context.user_confirm_required = True

    # STEP 3: Generate only changed files
    for change in diff['modified']:
        for file_change in change['files']:
            if file_change['type'] == 'modified':
                # Chỉ regenerate file đó, không touch toàn bộ zone
                regenerate_file(
                    file_change['path'],
                    context.new_spec,
                    context.existing_skill
                )
            elif file_change['type'] == 'added':
                create_file(file_change['path'], context.new_spec)

    # STEP 4: Write patch manifest
    patch_manifest = {
        'operation': 'patch',
        'target': context.existing_skill_path,
        'changes': diff,
        'timestamp': now(),
        'minimal': True
    }
    write_json(join(context.output_dir, 'patch-manifest.json'), patch_manifest)

    # STEP 5: Validate only affected files
    run_targeted_validation(context, affected_files=diff.get_all_files())

    # STEP 6: Update build-log with patch evidence
    append_to_build_log(context, {
        'operation': 'patch',
        'diff_summary': diff.summary(),
        'files_affected': len(diff.get_all_files()),
        'mode': 'minimal'
    })
```

### 4.4 Example Patch Manifest Output

```json
{
  "operation": "patch",
  "target": "~/.hermes/skills/general/prompt-cleaner",
  "timestamp": "2026-05-09T10:30:00Z",
  "mode": "minimal",
  "changes": {
    "added": [],
    "modified": [
      {
        "zone": "knowledge",
        "files": [
          {"path": "knowledge/new-topic.md", "type": "added"},
          {"path": "knowledge/existing-rule.md", "type": "modified"}
        ]
      }
    ],
    "removed": []
  },
  "files_affected_count": 2,
  "validation": "targeted_only"
}
```

---

## 5. Tổng hợp Action Items

| # | Action | Priority | Ghi chú |
|---|--------|----------|---------|
| A1 | Thêm `operation_type` detection vào skill-builder workflow | P0 | Detect tự động từ context |
| A2 | Thêm `install_target` resolution với priority order | P0 | Ưu tiên frontmatter > user flag > platform default |
| A3 | Nâng cấp validator đọc YAML frontmatter trước | P1 | backward compatible với Markdown |
| A4 | Thêm migration validation cho Markdown→YAML | P1 | Đảm bảo không lose data |
| A5 | Thêm patch mode workflow với diff generation | P1 | Chỉ generate changed files |
| A6 | Tạo `skill-builder/knowledge/hermes-skill-standards.md` | P2 | Hermes-specific standards |
| A7 | Thêm execution_mode vào design.md frontmatter | P2 | lightweight/standard/strict |

---

## 6. Files cần tạo mới

```
skill-builder/
├── knowledge/
│   └── hermes-skill-standards.md    # NEW: Hermes-native standards
├── schemas/                         # NEW: Schema directory
│   ├── design.schema.yaml
│   ├── todo.schema.yaml
│   └── build-log.schema.yaml
└── validators/                      # NEW: Validators
    ├── frontmatter_validator.py    # Read YAML frontmatter first
    ├── migration_validator.py      # Markdown → YAML validation
    └── patch_validator.py          # Diff validation for patch mode
```

---

## 7. Backward Compatibility

- Validator phải chạy được với cả design.md cũ (Markdown-only) và mới (YAML-first)
- Patch mode chỉ activate khi detect được signal rõ ràng
- install_target default vẫn giữ nguyên behavior cũ nếu không có frontmatter