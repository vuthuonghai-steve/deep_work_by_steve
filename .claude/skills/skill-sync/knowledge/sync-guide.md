# Skill Sync — Knowledge Base

## Overview

Skill `skill-sync` duoc thiet ke de dong bo skills tu `skills/rebuild/` den cac vi tri khac nhau trong workspace va user-level directories.

## Locations

| Level | Hermes | Claude |
|-------|--------|--------|
| Workspace | `.hermes/skills/` | `.claude/skills/` |
| User | `~/.hermes/skills/` | `~/.claude/skills/` |

## Change Detection

Su dung MD5 hash de phat hien thay doi:

```bash
md5sum SKILL.md
```

Neu hash khac nhau giua source va destination → can sync.

## Sync Method

Rsync voi `--delete` flag:

```bash
rsync -av --delete source/ dest/
```

Flag `--delete` dam bao cac file cu bi xoa o source cung bi xoa o destination.

## Usage

```bash
# Sync all skills
python scripts/sync_skills.py

# Sync specific skill
python scripts/sync_skills.py skill-architect

# Compare only (no sync)
python scripts/sync_skills.py --compare

# Dry run
python scripts/sync_skills.py --dry-run
```
