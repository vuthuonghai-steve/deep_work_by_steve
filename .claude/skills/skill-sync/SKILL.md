---
name: skill-sync
description: 'Sync skills tu source (skills/rebuild/) den cac vi tri: workspace-level (.hermes/skills, .claude/skills) va user-level (~/.hermes/skills, ~/.claude/skills). Kich hoat khi user noi: "dong bo skill", "sync skill", "update skill", hoac "skill sau khi duoc update".'
category: meta
tags: [sync, rsync, skill-management, hermes, claude]
version: "1.0.0"
author: "Steve Void Team"
---

```yaml
token_budget:
  SKILL_md: 400 tokens max
  L1_limit: 800
  L2_limit: 1200
  enforcement: hard

priority_order:
  - detect_changes
  - verify_hash
  - sync_destinations
  - confirm
```

<instructions>
## BOOT SEQUENCE

1. Read `SKILL.md` (this file) — done
2. Read `data/sync-locations.yaml` — destination paths
3. Read `loop/sync-checklist.md` — quality gate
4. Execute sync workflow

## Core Constraints

```yaml
must:
  - use_md5_hash_for_change_detection
  - compare_source_vs_destination_before_sync
  - sync_all_4_destinations_uniformly
  - show_before_after_hash_verification
  - use_rsync_with_delete_flag_for_full_sync

must_not:
  - sync_without_verifying_source_exists
  - skip_any_destination
  - use_copy_instead_of_rsync
  - modify_source_files
```

## Stop Conditions

```yaml
stop_conditions:
  - source_skill_not_found: abort and report
  - user_declines_sync: wait for confirmation
```
</instructions>

<context>
## Routing Map

| File | Load when |
|------|-----------|
| `data/sync-locations.yaml` | Always |
| `loop/sync-checklist.md` | Pre/post sync |
| `scripts/sync_skills.py` | Execution |
</context>

---

# Skill Sync — Dong bo Skill

## Mission

Sync skills tu `skills/rebuild/` den cac destination folders.

## Source & Destinations

```yaml
source_base: "{workspace}/skills/rebuild"
destinations:
  workspace_hermes: "{workspace}/.hermes/skills"
  workspace_claude: "{workspace}/.claude/skills"
  user_hermes: "~/.hermes/skills"
  user_claude: "~/.claude/skills"
```

## Sync Workflow

### Step 1: Detect Skills

```bash
ls {source_base}/
```

List all skills in source.

### Step 2: Compare Hashes

For each skill:
1. Get MD5 hash of source SKILL.md
2. Get MD5 hash of each destination SKILL.md
3. Flag if different

### Step 3: Sync

```bash
rsync -av --delete {source}/skill-name/ {destination}/skill-name/
```

### Step 4: Verify

Re-check hashes after sync to confirm match.

## Output Format

```
| Skill | hermes-ws | claude-ws | hermes-usr | claude-usr | Status |
|-------|-----------|-----------|------------|------------|--------|
| xxx   | ✅        | ✅        | ✅         | ✅         | SYNCED |
```

<output_contract>
After sync, show table with all skills and their sync status across all 4 destinations.
</output_contract>
