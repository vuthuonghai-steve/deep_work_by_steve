---
name: pipeline-runner
description: Orchestrates multi-stage skill pipelines by spawning sub-agents sequentially. Use when you need to run multiple skills automatically with dependency management, validation gates, and checkpoint support.
trigger_patterns:
  - "/pipeline-runner <path>"
  - "/uml-pipeline <path>"
  - "chạy pipeline"
  - "run pipeline"
  - "generate uml"
---

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào.
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file)

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
- @.claude/skills/pipeline-runner/knowledge/pipeline-config.md - Pipeline YAML schema
- @.claude/skills/pipeline-runner/knowledge/skills-registry.md - Skills registry definition
- @.claude/skills/pipeline-runner/knowledge/error-codes.md - Error codes reference

### Tier 3: Optional (load when needed)
- @.claude/skills/pipeline-runner/loop/checklist.md - Pipeline execution checklist
- @.claude/skills/pipeline-runner/loop/verify-complete.md - Completion verification
- @.claude/skills/pipeline-runner/templates/pipeline-init.yaml - Pipeline init template
- @.claude/skills/pipeline-runner/templates/pipeline-uml-generation.yaml - UML generation template
- @.claude/skills/pipeline-runner/templates/task-input.json - Task input template
- @.claude/skills/pipeline-runner/scripts/validate_stage.py - Stage validation script
- @.claude/skills/pipeline-runner/scripts/resume_pipeline.py - Pipeline resume script
- @.claude/skills/pipeline-runner/scripts/parse_pipeline.py - Pipeline parser
- @.claude/skills/pipeline-runner/scripts/spawn_skill.py - Skill spawner

# Pipeline Runner — Orchestrator Skill

## Mission

**Persona:** Pipeline Orchestrator. Automatically chain and execute multiple skills in sequence, managing dependencies, validation, and state persistence.

## Boot Sequence

1. Read this `SKILL.md` (Core orchestration logic).
2. Read `knowledge/pipeline-config.md` — Pipeline YAML schema.
3. **Read `.claude/skills/skills.yaml`** ← PRIMARY SOURCE FOR PIPELINE DEFINITIONS
4. Extract pipeline definition by name (e.g., `uml-generation`, `skill-creation`)
5. Read `.skill-context/{pipeline_name}/_queue.json` — Runtime state (if resuming).

*Additional files load per-step below (Progressive Disclosure).*

---

## CRITICAL: Load Pipeline from skills.yaml

The pipeline runner MUST load pipeline definitions from `.claude/skills/skills.yaml` NOT from hardcoded configs.

### Loading Process

1. **Read skills.yaml** at `.claude/skills/skills.yaml`
2. **Find pipeline by name** in `pipelines` section
3. **Extract stages** with full DAG metadata:
   - `id`: Stage identifier
   - `skill`: Skill name to invoke
   - `depends_on`: Array of stage IDs this depends on
   - `checkpoint`: Boolean (true = pause after this stage)
   - `input_contract`: Required inputs
   - `output_contract`: Expected outputs

4. **Validate all skills exist** in the skills registry

5. **Create queue** with ALL stages (not just first 4)

---

## Workflow Phases

### Phase 1: INIT — Initialize Pipeline

1. **Read skills.yaml** to get stages, dependencies, checkpoints ← PRIMARY SOURCE
2. **Extract pipeline definition** by name (from trigger or default)
3. **Validate all skills referenced** exist in skills registry
4. **Create or resume _queue.json** with status tracking for ALL stages
5. **Notify user**: pipeline name, stage count (e.g., "7 stages"), checkpoint locations

### Phase 2: EXECUTE — Run Stage Loop

For each stage (in dependency order):

1. **Find Runnable**: Check if all dependencies are COMPLETED.
2. **Prepare Task**: Create task-input.json in .skill-context/{pipeline}/tasks/ with:
   - Full pipeline_context (see Phase 4)
   - Predecessor outputs from depends_on stages
3. **Spawn Sub-agent**: Use Task tool to invoke skill-executor agent with task spec.
4. **Execute**: skill-executor runs the skill with isolated context.
5. **Validate**: Run validation_script, check exit code = 0.
6. **Update Queue**: Write _queue.json with COMPLETED or FAILED.
7. **Checkpoint**: Read `checkpoint` field from skills.yaml stage definition (NOT hardcoded)

### Phase 3: COMPLETE — Finalize

1. Generate summary.md with all outputs.
2. Report completion to user.

---

## Interaction Points (Gates)

| Gate | When | Action |
|------|------|--------|
| **Pipeline Start** | Before INIT | Show: pipeline name, stages, input |
| **Checkpoint** | After stage with checkpoint=true | Ask: "Continue / Stop / View Details" |
| **Validation Failed** | After stage fails | Ask: "Retry / Skip / Stop" |
| **Skill Not Found** | During validation | Ask: "Select alternative / Stop" |
| **Pipeline Complete** | After all stages | Show: summary path, all outputs |

---

## Guardrails

| ID | Rule | Mechanism |
|----|------|----------|
| G1 | Dependency Enforcement | Only run stage when all depends_on are COMPLETED |
| G2 | Validation Gate | Hard stop if exit code != 0 |
| G3 | Checkpoint Pause | Pause at checkpoint=true stages |
| G4 | Atomic State | Write _queue.tmp first, then rename to _queue.json |
| G5 | Source Citation | Require each skill cite input from previous stage |

---

## Progressive Disclosure

### Tier 1: Always Load
- SKILL.md (this file)
- knowledge/pipeline-config.md
- `.claude/skills/skills.yaml` ← PRIMARY PIPELINE SOURCE

### Tier 2: Per-Stage
- Current skill's SKILL.md (when spawning sub-agent)
- knowledge/error-codes.md (when error occurs)

### Tier 3: Debug
- loop/checklist.md (when verifying quality)
- scripts/resume_pipeline.py (when resuming failed pipeline)

---

## Quick Trigger

### Command Patterns

```
/pipeline-runner <input-path>     # Run pipeline with input path
/uml-pipeline <input-path>       # Quick UML generation shortcut
```

### Example Usage

```bash
# Generate UML from FR docs
/pipeline-runner Docs/life-1/01-vision/FR/

# Resume failed pipeline
/pipeline-runner --resume

# Check status
/pipeline-runner --status
```

---

## Reference

See TRIGGER.md for full trigger documentation.
See templates/pipeline-uml-generation.yaml for example pipeline config.
