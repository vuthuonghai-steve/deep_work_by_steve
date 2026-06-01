# Sourced: _shared/knowledge/framework.md

## Thông tin nguồn
- **Path**: `skills/rebuild/_shared/knowledge/framework.md`
- **Version**: N/A (shared framework)
- **Mục đích**: Single source of truth cho 3 meta-skills (explorer, architect, planner, builder)

## Tri thức trích xuất

### 7 Zones Structure
| Zone | Folder | Purpose | Required |
|------|--------|---------|----------|
| Core | `SKILL.md` | Orchestration, persona, workflow, guardrails | ✅ |
| Knowledge | `knowledge/` | References, standards, guidelines | ✅ Usually |
| Scripts | `scripts/` | Executable automation | As needed |
| Templates | `templates/` | Output format templates | As needed |
| Data | `data/` | Config, static data, schemas | As needed |
| Loop | `loop/` | Checklists, logs, test cases | ✅ Usually |
| Assets | `assets/` | Images, icons | Rarely |

### Pipeline Flow
```
skill-explorer → skill-architect → skill-planner → skill-builder
     │                │                │
     ▼                ▼                ▼
exploration.md   design.md       todo.md → skill files
 (§6 Arch Recs)   (§3 Zone Map)   (phase breakdown)
```

### Handoff Contracts
- **Explorer → Architect**: §3 (Golden Standards) → Architect designs §2 (Capability Map) + §8 (Risks)
- **Explorer → Architect**: §4 (AI Instructions) → Architect guides §3.loop
- **Explorer → Architect**: §6 (Arch Recommendations) → Architect defines §3 (Zone Mapping) + §7 (PD Plan)

### Anti-Hallucination Rules
| Rule | Mô tả |
|------|--------|
| AH1 | Every task MUST trace to source — task without `[TỪ DESIGN §N]` |
| AH2 | Only decompose, don't add requirements |
| AH3 | Don't guess domain knowledge |
| AH4 | Always label sources — `[TỪ DESIGN]` / `[GỢI Ý]` distinction |
| AH5 | Verify resources before completion |

### Version Management
- MAJOR.MINOR.PATCH
- New section → MINOR
- Zone Mapping format change → MAJOR
- Typo fix, add example → PATCH

---

## Áp dụng cho knowledge-processor

**Đã tuân thủ**:
- ✅ Tuân thủ 7 Zones structure
- ✅ Pipeline flow đúng: exploration.md → design.md → todo.md → skill files
- ✅ Trace tags cho source attribution
- ✅ Exploration document có đầy đủ 8 sections
