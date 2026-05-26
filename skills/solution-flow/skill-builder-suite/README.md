# Skill Builder Suite — Quản lý bộ công cụ xây dựng Agent Skill

## 1. Tổng quan

Bộ **Master Skill Suite** gồm 4 skill phục vụ việc xây dựng agent skill mới.

## 2. Danh sách Skills

| # | Skill | Stage | Output | Mục đích |
|---|-------|-------|--------|-----------|
| 1 | skill-explorer | 0 | exploration.md | Khám phá nghiệp vụ |
| 2 | skill-architect | 1 | design.md | Thiết kế kiến trúc |
| 3 | skill-planner | 2 | todo.md | Lập kế hoạch triển khai |
| 4 | skill-builder | 3 | {skill-name}/ | Triển khai skill |

## 3. Pipeline Flow

```
EXPLORER → ARCHITECT → PLANNER → BUILDER
    ↓           ↓          ↓          ↓
exploration  design.md  todo.md    skill files
    .md        §1-§10
```

## 4. Trigger Keywords

| Từ khóa | Skill kích hoạt |
|----------|-----------------|
| "tao skill", "xay dung skill" | skill-explorer |
| "thiet ke", "design.md", "mermaid" | skill-architect |
| "lap ke hoach", "tao todo" | skill-planner |
| "build skill", "trien khai" | skill-builder |
| "tao agent skill", "bo skill" | Toàn pipeline |

## 5. Vị trí Skills

```
skills/rebuild/
├── AGENT.md                    # Root guide cho bộ skill
├── skill-explorer/
│   └── SKILL.md
├── skill-architect/
│   └── SKILL.md
├── skill-planner/
│   └── SKILL.md
├── skill-builder/
│   └── SKILL.md
└── _shared/                   # Shared resources
    └── knowledge/
        └── framework.md       # 7 Zones, Pipeline
```

## 6. Context Directory

Pipeline sử dụng thư mục `.skill-context/{skill-name}/`:

```
.skill-context/{skill-name}/
├── exploration.md              # Stage 0
├── design.md                  # Stage 1
├── todo.md                    # Stage 2
├── build-log.md              # Stage 3
├── resources/                # Domain knowledge
├── data/                     # Config, schemas
└── loop/                     # Quality gates
```

## 7. Đồng bộ

Sau khi build hoàn tất, chạy:
```bash
python3 skills/rebuild/skill-sync/scripts/sync_skills.py
```

Sync đến 4 destinations:
- `.hermes/skills/`
- `.claude/skills/`
- `~/.hermes/skills/`
- `~/.claude/skills/`

## 8. Liên quan

- **Root Guide:** `skills/rebuild/AGENT.md`
- **Validation:** `skills/rebuild/skill-builder/scripts/validate_skill.py`
