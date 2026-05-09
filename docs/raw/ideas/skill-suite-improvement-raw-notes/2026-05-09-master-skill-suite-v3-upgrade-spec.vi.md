# Master Skill Suite v3.0 — Specification cho bản nâng cấp

> Ngày: 2026-05-09
> Tác giả: Tổng hợp từ 4 agent (Hermes + Claude Code + Codex + Subagents)
> Trạng thái: **DRAFT** — cần review và apply
> Nguồn:
> - `docs/raw/ideas/skill-suite-improvement-raw-notes/2026-05-09-research-master-skill-suite-evaluation.vi.md`
> - `docs/raw/ideas/2026-05-09-proposal-operation-types-execution-modes-refinement-loop.vi.md`
> - `docs/raw/ideas/2026-05-09-claude-code-upgrade-architect.vi.md`
> - `docs/raw/ideas/2026-05-09-codex-upgrade-builder.vi.md`

---

## Tóm tắt Executive

Bộ 3 skill (skill-architect, skill-planner, skill-builder) hiện tại có 7 vấn đề cốt lõi cần fix:

| # | Vấn đề | Mức độ |
|---|--------|--------|
| #9.1 | Hardcode `.claude/skills/` — không support Hermes path | Nghiêm trọng |
| #9.2 | Markdown table là contract quá fragile | Nghiêm trọng |
| #9.3 | Contract nội bộ mâu thuẫn (skill-planner 5 vs 6 sections) | Trung bình |
| #9.4 | Validator phụ thuộc regex quá nhiều | Trung bình |
| #9.5 | Vòng feedback chưa hoàn chỉnh | Trung bình |
| #9.6 | Quá nhiều gate cho task nhỏ | Thấp |
| #9.7 | Chỉ hỗ trợ create_new operation | Thấp |

**Mục tiêu v3.0**: Hệ thống skill suite hoạt động được trên cả Hermes và Claude, support multi-operation (create/patch/refactor/migrate), có YAML frontmatter là contract chính, và có refinement loop chính thức.

---

## Phần I: skill-architect — Nâng cấp v3.0

### 1.1 Phase 1 Collect — Thêm 3 trường bắt buộc

**Thêm vào prompt thu thập yêu cầu:**

```yaml
platform_target:
  type: enum
  options: [hermes, claude, both]
  default: both
  prompt: "Skill nhắm đến nền tảng nào? (hermes/claude/both)"
  required: true

operation_type:
  type: enum
  options: [create_new, patch_existing, refactor_existing, migrate_platform, consolidate_skills, deprecate_skill]
  default: create_new
  prompt: "Loại operation chính là gì?"
  required: true

execution_mode:
  type: enum
  options: [lightweight, standard, strict]
  default: standard
  prompt: "Chế độ thực thi? (lightweight=patch nhanh, standard=pipeline đầy đủ, strict=full+audit)"
  required: true
```

**Lý do**: 3 trường này quyết định toàn bộ pipeline phía sau. Architect cần biết đang thiết kế cho platform nào, operation nào, và mode nào.

### 1.2 Zone Structure theo Platform Target

| Target | Zone Structure | Đặc điểm |
|--------|---------------|----------|
| **Hermes** | `core/`, `tools/`, `manifest/`, `runtime/` | Nhẹ, embeddable, tập trung tool execution |
| **Claude** | `core/`, `skills/`, `context/`, `capabilities/` | Mở rộng, multi-skill orchestration |
| **Both** | `core/`, `tools/`, `skills/`, `manifest/`, `runtime/`, `context/` | Union của 2 bên |

**Hermes zone gọn hơn** — skill như một tool có manifest riêng.
**Claude zone phong phú hơn** — skill như một agent với system prompt.
**Both** cần bridge layer ở `core/` để hai hệ thống giao tiếp được.

### 1.3 Frontmatter Schema cho design.md

Design.md **PHẢI** có YAML frontmatter ở đầu file, chứa machine-readable contract:

```yaml
---
name: {skill-name}
version: "1.0.0"
status: in-progress | complete | deprecated

# Operation context
platform_target: hermes | claude | both
operation_type: create_new | patch_existing | refactor_existing | migrate_platform | consolidate_skills | deprecate_skill
execution_mode: lightweight | standard | strict

# Install target — quan trọng cho Builder biết output đâu
install_target:
  platform: hermes | claude | both
  scope: user-local | repo | project-local
  path: ~/.hermes/skills/{category}/{skill-name}/

# Zone Mapping — contract chính giữa Architect và Planner
# Frontmatter là machine-readable; Markdown body là human-readable summary
zone_mapping:
  - zone: core
    files:
      - path: SKILL.md
        tier: 1  # tier 1 = mandatory at boot
        mandatory: true
        content_summary: "Persona, phases, guardrails"
  - zone: knowledge
    files:
      - path: knowledge/architect.md
        tier: 2
        mandatory: true
        content_summary: "Domain knowledge, standards"
  - zone: scripts
    files:
      - path: scripts/validate_skill.py
        tier: 2
        mandatory: false

# 3 Pillars Analysis
pillars:
  knowledge:
    domains: [list]
    gaps: [list]
  process:
    phases: [list]
    branches: [list]
  guardrails:
    risks: [list]
    mitigations: [list]

# Progressive Disclosure Plan
progressive_disclosure:
  tier1:
    - SKILL.md
    - ../_shared/knowledge/framework.md
  tier2:
    - path: knowledge/architect.md
      load_when: "Phase requiring domain knowledge"

# Metadata
metadata:
  author: Steve Void Team
  date_created: YYYY-MM-DD
  date_modified: YYYY-MM-DD
---

<!-- Markdown body for human readers -->
```

**Quy tắc**: Frontmatter PHẢI khớp 1:1 với §3 Zone Mapping table trong Markdown body. Frontmatter là machine-readable, Markdown là human-readable.

### 1.4 Phase 1 Gate — Yêu cầu xác nhận từ user

Sau khi thu thập đủ thông tin, Architect trình bày tóm tắt và chờ user confirm **TRƯỚC KHI** ghi vào design.md:

```
✅ Đã hiểu yêu cầu:

Skill name: {skill-name}
Platform target: {platform_target}
Operation type: {operation_type}
Execution mode: {execution_mode}

Pain point: {pain_point}
User: {user}
Expected output: {expected_output}

→ Xác nhận để tiếp tục Phase 2 (Analyze)?
```

### 1.5 Rollback Procedures — Bổ sung

Thêm Phase 0 rollback (Collect):

```markdown
### Phase 0 Rollback — Operation Context

**Trigger**: User muốn thay đổi platform_target, operation_type, hoặc execution_mode sau khi đã bắt đầu.

**Rollback Steps:**
1. Reset § Metadata (operation context fields)
2. Quay lại Phase 1: Collect — thu thập lại operation context
```

---

## Phần II: skill-planner — Nâng cấp v3.0

### 2.1 Fix mâu thuẫn 5 vs 6 sections

**Vấn đề**: SKILL.md dòng 109 nói "MUST contain exactly 5 sections" nhưng dòng 153-171 lại định nghĩa đầy đủ section 6 "Builder Feedback Integration".

**Giải pháp**: Chuẩn hóa thành **6 sections** với cấu trúc chính thức:

```markdown
## 1. Pre-requisites
## 2. Phase Breakdown
## 3. Knowledge & Resources Needed
## 4. Definition of Done
## 5. Notes
## 6. Builder Feedback Integration
```

Cập nhật lại SKILL.md line 109:
```diff
- The file MUST contain exactly 5 sections:
+ The file MUST contain exactly 6 sections:
```

### 2.2 Frontmatter Schema cho todo.md

Todo.md **PHẢI** có YAML frontmatter:

```yaml
---
name: {skill-name}
version: "1.0.0"
date_created: YYYY-MM-DD
status: draft | complete | in-progress

# Operation context từ design.md
operation_type: create_new
execution_mode: standard

# Phase Breakdown — tasks grouped by execution phase
phases:
  - id: 0
    name: Resource Preparation
    description: "Chuẩn bị tài nguyên domain còn thiếu"
    tasks:
      - id: "0.1"
        description: "Soạn tài liệu domain cho {Topic}"
        priority: critical | high | medium | low
        estimated_hours: 4-8
        trace: "[TỪ AUDIT TÀI NGUYÊN]"
        dependencies: []
        status: pending | in-progress | done
  - id: 1
    name: Core Implementation
    description: "Build phần core của skill"
    tasks:
      - id: "1.1"
        description: "Tạo SKILL.md với persona và workflow"
        priority: critical
        estimated_hours: 2-4
        trace: "[TỪ DESIGN §3]"
        dependencies: ["0.1"]
        status: pending

# Pre-requisites
prerequisites:
  - tier: domain
    topic: "API design patterns"
    resource_path: "resources/api-patterns.md"
    status: rich | thin | missing
    trace: "[TỪ DESIGN §2]"

# Blockers
blockers:
  - id: "B1"
    description: "Chưa rõ output format là JSON hay YAML"
    trace: "[CẦN LÀM RÕ §9]"
    resolved: false

# Traceability
traceability:
  task_to_design:
    "0.1": ["§3 Zone Mapping", "Audit Tài Nguyên"]
    "1.1": ["§3 Zone Mapping → Core"]
  task_to_resource:
    "1.1": ["resources/api-patterns.md"]
---

<!-- Markdown body: human-readable task list -->
```

### 2.3 Operation type affects planner behavior

| operation_type | Planner behavior change |
|----------------|-------------------------|
| `create_new` | Standard full pipeline |
| `patch_existing` | Skip Phase 0 (Resource Prep) nếu resources đã có; giảm confirm gates |
| `refactor_existing` | Thêm audit step; tập trung vào behavior preservation check |
| `migrate_platform` | Thêm platform analysis step; map source → target conventions |
| `consolidate_skills` | Thêm inventory step; analyze overlap trước |
| `deprecate_skill` | Minimal plan — chỉ tạo deprecation notice |

### 2.4 Execution mode affects gate behavior

| Mode | Planner gates |
|------|--------------|
| **lightweight** | Không có gate; tự động proceed |
| **standard** | Confirm sau mỗi phase |
| **strict** | Full review + signoff requirement |

---

## Phần III: skill-builder — Nâng cấp v3.0

### 3.1 Fix output_contract — Dynamic install_target

**Thay đổi từ:**
```yaml
output_contract:
  - type: directory
    path: ".claude/skills/{skill-name}"
    format: directory
```

**Thành:**
```yaml
output_contract:
  - type: directory
    path: "{install_target.path}"
    format: directory
    # install_target được resolve từ design.md frontmatter
    # hoặc user override, hoặc platform detection
```

### 3.2 install_target Resolution Logic

**Resolution priority (highest to lowest):**

1. **Explicit user override** — CLI flag `--install-target`
2. **Frontmatter in design.md** — `install_target` field
3. **Platform detection from environment** — Hermes vs Claude
4. **Default fallback per platform**

**Platform vs Scope Matrix:**

| Platform | Scope | Target Path |
|----------|-------|-------------|
| hermes | user-local | `~/.hermes/skills/{category}/{skill-name}/` |
| hermes | repo | `{repo}/skills/{category}/{skill-name}/` |
| hermes | project-local | `{project}/.hermes/skills/{skill-name}/` |
| claude | user-local | `~/.claude/skills/{skill-name}/` |
| both | user-local | `~/.hermes/skills/...` (preferred) |

### 3.3 Operation Type Detection + Adaptive Workflow

Builder tự động detect operation_type từ context:

```python
def detect_operation_type(context) -> str:
    signals = {
        'has_design_md': exists(context.design_md),
        'has_todo_md': exists(context.todo_md),
        'has_existing_skill': exists(context.target_skill_path),
        'target_platform': detect_platform(context),
        'operation_hint': context.user_hint or None
    }

    # Priority 1: User chỉ định rõ ràng
    if signals['operation_hint']:
        return signals['operation_hint']

    # Priority 2: design.md + todo.md + không có skill cũ → create_new
    if signals['has_design_md'] and signals['has_todo_md']:
        if not signals['has_existing_skill']:
            return 'create_new'
        else:
            return 'patch_existing'  # Có design mới + skill cũ → patch

    # Priority 3: Platform migration
    if signals['target_platform'] == 'hermes' and signals['has_existing_skill']:
        current_platform = detect_existing_skill_platform(signals['has_existing_skill'])
        if current_platform != 'hermes':
            return 'migrate_platform'

    # Priority 4: Fallback
    if signals['has_existing_skill']:
        return 'refactor_existing'

    return 'create_new'
```

### 3.4 Per-Operation-Type Workflow

#### `create_new` (standard pipeline)
```python
def workflow_create_new(context):
    # 1. PREPARE: đọc design.md + todo.md + resources
    # 2. CLARIFY: hỏi user nếu ambiguity (max 5 items)
    # 3. BUILD: tạo full skill package từ design §3 Zone Mapping
    # 4. VERIFY: chạy validate_skill.py + placeholder check
    # 5. DELIVER: ghi build-log.md + output ra install_target
```

#### `patch_existing` (minimal delta)
```python
def workflow_patch_existing(context):
    # 1. READ: đọc skill hiện tại + patch spec
    # 2. DIFF: so sánh existing vs patch spec
    # 3. PATCH: chỉ apply những thay đổi cần thiết
    # 4. VALIDATE: targeted validation (chỉ file bị thay đổi)
    # 5. LOG: ghi patch log vào build-log.md (không full log)
    # Output: unified diff thay vì full package
```

#### `migrate_platform` (platform adaptation)
```python
def workflow_migrate_platform(context):
    # 1. DETECT_SOURCE: xác định platform source
    # 2. ANALYZE: đọc skill source + frontmatter metadata
    # 3. TRANSFORM: convert paths + references sang Hermes format
    #    - .claude/skills/ → ~/.hermes/skills/
    #    - Convert SKILL.md frontmatter sang Hermes schema
    # 4. VALIDATE: Hermes-specific validation
    # 5. OUTPUT: ghi ra Hermes-compatible target
```

### 3.5 Validator Upgrade — YAML-first

**Nguyên tắc**: Đọc YAML frontmatter TRƯỚC, dùng frontmatter làm canonical contract.

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
        validator.set_expected_files(expected_files)

    # BƯỚC 3: Migration detection - check Markdown → YAML integrity
    if design_frontmatter and design_frontmatter.get('source_format') == 'markdown':
        validator.check_migration_integrity(design_path)

    # BƯỚC 4: Các checks hiện tại (backward compat)
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

### 3.6 Patch Mode Detection + Diff Generation

**5 signals detect patch mode:**
1. Có existing skill + design.md mới
2. User flag `--diff`
3. Frontmatter `operation_type: patch_existing`
4. ≤2 zones changed trong design.md §3
5. ≤3 files changed theo todo.md

**Minimal diff workflow:**
- Chỉ generate changed files
- Targeted validation thay vì full pipeline
- Output là unified diff hoặc JSON patch

---

## Phần IV: Validator Scripts — Nâng cấp

### 4.1 Validator Architecture

```python
class HermesSkillValidator:
    """YAML-first validator cho Hermes skills."""

    def __init__(self, options=None):
        self.options = options or {}
        self.errors = []
        self.warnings = []

    def parse_frontmatter(self, file_path):
        """Parse YAML frontmatter từ Markdown file."""
        with open(file_path, 'r') as f:
            content = f.read()

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
        return None

    def validate_zone_mapping(self, frontmatter_zones, skill_path):
        """Validate zone mapping từ frontmatter."""
        # Đọc expected files từ frontmatter
        # Kiểm tra actual files trong skill_path
        # Report mismatches
```

### 4.2 Migration Validation

Khi design.md được migrate từ pure Markdown sang YAML-first, validator check:

1. YAML frontmatter có đầy đủ required fields
2. Markdown body tương thích với frontmatter contract
3. Zone mapping trong frontmatter khớp với §3 table

---

## Phần V: Refinement Loop — 6-Step Formalization

### 5.1 Loop Overview

```
[1. OBSERVE] → [2. IDENTIFY] → [3. DECIDE] → [ACTION]
                                    ↓
                              memory | patch | new | refactor
                                    ↓
[4. APPLY] → [5. DOCUMENT] → [6. VERIFY]
```

### 5.2 Step Definitions

| Step | Name | Description |
|------|------|-------------|
| 1 | Observe | Thu thập data từ session thật |
| 2 | Identify | Phân tích observation để tìm pattern |
| 3 | Decide | Chọn action phù hợp nhất |
| 4 | Apply | Thực thi action đã chọn với minimal change |
| 5 | Document | Ghi lại lý do và nội dung thay đổi |
| 6 | Verify | Đảm bảo skill vẫn load được và đủ gọn |

### 5.3 Decision Tree (Step 3)

```yaml
decision_tree:
  memory_update:
    condition: "Knowledge missing but skill logic correct"
    action: "Ghi vào memory/knowledge file"

  patch_existing:
    condition: "Skill hoạt động nhưng thiếu/chứa lỗi nhỏ"
    action: "Áp dụng minimal patch"
    scope: "≤ 3 files, ≤ 20% content changes"

  create_new:
    condition: "Hoàn toàn new capability, không liên quan skill hiện có"
    action: "Tạo skill mới"

  refactor_existing:
    condition: "Skill structure không phù hợp, cần tái cấu trúc"
    action: "Refactor toàn bộ skill"

  deprecate_skill:
    condition: "Skill lỗi thời hoặc duplicate"
    action: "Đánh dấu deprecated"
```

### 5.4 Refinement Log Format

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
    verification: passed
```

---

## Phần VI: Shared Framework Updates

### 6.1 Update `_shared/knowledge/framework.md`

Thêm section mới về Hermes-native conventions:

```markdown
## Hermes-Native Skill Conventions

### Install Target Resolution

| Platform | Scope | Path |
|----------|-------|------|
| hermes | user-local | `~/.hermes/skills/{category}/{skill-name}/` |
| hermes | repo | `{repo}/skills/{category}/{skill-name}/` |
| claude | user-local | `~/.claude/skills/{skill-name}/` |
| both | user-local | `~/.hermes/skills/...` (preferred) |

### Frontmatter Schema Version

```yaml
contract_version: "1.0"  # Semantic versioning cho contract format
```

### Operation Types

- `create_new` — tạo skill hoàn toàn mới
- `patch_existing` — sửa một phần nhỏ (≤3 files, ≤20% content)
- `refactor_existing` — tái cấu trúc, giữ nguyên behavior
- `migrate_platform` — di chuyển Claude ↔ Hermes
- `consolidate_skills` — gộp nhiều skill trùng lặp
- `deprecate_skill` — đánh dấu deprecated

### Execution Modes

- `lightweight` — không gate, syntax-only validation, output là patch diff
- `standard` — đầy đủ pipeline, confirmation gates, full package
- `strict` — thêm manual signoff, comprehensive validation, audit bundle
```

---

## Phần VII: Implementation Priority

### P0 (Ngay lập tức — fix breakage)

| # | Action | File | Lý do |
|---|--------|------|-------|
| P0.1 | Fix output_contract hardcode `.claude/skills/` | skill-builder/SKILL.md | Không hoạt động trên Hermes |
| P0.2 | Thêm install_target resolution logic | skill-builder | Builder cần biết output đâu |
| P0.3 | Fix skill-planner 5 vs 6 sections contradiction | skill-planner/SKILL.md | Contract mâu thuẫn |
| P0.4 | Thêm platform_target + operation_type + execution_mode vào Phase 1 | skill-architect | 3 trường quyết định pipeline |

### P1 (Short-term — strengthen contract)

| # | Action | Lý do |
|---|--------|-------|
| P1.1 | Thêm YAML frontmatter vào design.md template | Contract yếu |
| P1.2 | Thêm YAML frontmatter vào todo.md template | Contract yếu |
| P1.3 | Upgrade validator đọc YAML trước | Validator fragile |
| P1.4 | Thêm install_target schema vào design.md frontmatter | Builder cần biết output |

### P2 (Medium-term — operational flexibility)

| # | Action | Lý do |
|---|--------|-------|
| P2.1 | Implement operation type detection + adaptive workflow | Chỉ support create_new |
| P2.2 | Implement execution mode gates | Quá nhiều gate cho task nhỏ |
| P2.3 | Formalize refinement loop | Vòng feedback chưa hoàn chỉnh |
| P2.4 | Add migration validation to validator | Platform migration not supported |

---

## Phần VIII: Files cần tạo mới

```
skills/rebuild/
├── _shared/
│   └── knowledge/
│       └── hermes-native-conventions.md   # NEW: Hermes-specific conventions
├── skill-architect/
│   ├── templates/
│   │   └── design.md.template.v3         # NEW: with YAML frontmatter
├── skill-planner/
│   └── templates/
│       └── todo.md.template.v3           # NEW: with YAML frontmatter
├── skill-builder/
│   └── scripts/
│       └── validate_skill_v3.py          # NEW: YAML-first validator
└── schemas/
    ├── design-frontmatter.schema.yaml     # NEW: JSON schema for design.md frontmatter
    ├── todo-frontmatter.schema.yaml       # NEW: JSON schema for todo.md frontmatter
    └── build-log-frontmatter.schema.yaml  # NEW: JSON schema for build-log.md frontmatter
```

---

## Phần IX: Migration Plan

### Phase M1: Immediate Fixes (Ngày 1)

1. Update `skill-builder/SKILL.md`:
   - Change `output_contract.path` từ `.claude/skills/{skill-name}` thành `{install_target.path}`
   - Thêm install_target resolution logic

2. Update `skill-planner/SKILL.md` line 109:
   - `exactly 5 sections` → `exactly 6 sections`

3. Update `skill-architect/SKILL.md` Phase 1:
   - Thêm 3 field prompts (platform_target, operation_type, execution_mode)

### Phase M2: Contract Strengthening (Ngày 2-3)

1. Tạo `design.md.template.v3` với YAML frontmatter
2. Tạo `todo.md.template.v3` với YAML frontmatter
3. Update `validate_skill.py` → `validate_skill_v3.py` với YAML-first logic
4. Update `knowledge/architect.md` để reflect new schema

### Phase M3: Operational Flex (Ngày 4-7)

1. Implement operation type detection in builder
2. Implement execution mode gates
3. Create refinement loop documentation
4. Create schema files

---

## Checklist cho từng skill

### skill-architect v3.0 Checklist

- [ ] Phase 1 Collect có 3 field mới: platform_target, operation_type, execution_mode
- [ ] Zone suggestion logic dựa trên platform_target
- [ ] design.md template với YAML frontmatter
- [ ] § Metadata trong design.md chứa install_target
- [ ] Phase 0 Rollback cho operation context changes
- [ ] Execution mode affects gate behavior

### skill-planner v3.0 Checklist

- [ ] Fixed: 6 sections thay vì 5 (dòng 109)
- [ ] todo.md template với YAML frontmatter
- [ ] Operation type affects planner behavior
- [ ] Execution mode affects gate behavior
- [ ] §6 Builder Feedback Integration chính thức hóa

### skill-builder v3.0 Checklist

- [ ] output_contract dùng `{install_target.path}` thay vì hardcode
- [ ] install_target resolution logic (4 priority levels)
- [ ] Operation type detection function
- [ ] Per-operation-type workflow implementations
- [ ] YAML-first validator
- [ ] Migration validation logic
- [ ] Patch mode detection + diff generation

---

## Summary of Changes by File

### skill-architect/SKILL.md
- Thêm 3 field vào Phase 1 Collect
- Zone suggestion theo platform
- design.md template v3 với frontmatter
- Rollback procedure mới

### skill-planner/SKILL.md
- Fix 5 → 6 sections
- todo.md template v3 với frontmatter
- Operation type affects behavior
- §6 Builder Feedback Integration chính thức

### skill-builder/SKILL.md
- Fix output_contract hardcode
- Install target resolution
- Operation type detection
- Adaptive workflows
- Error policy: support patch mode

### validate_skill.py → validate_skill_v3.py
- YAML-first reading
- Frontmatter-based validation
- Migration integrity checks
- Hermes-specific checks

### _shared/knowledge/framework.md
- Hermes-native conventions section
- Install target matrix
- Operation types enum
- Execution modes enum
- Frontmatter schema versioning