# 3-Tier Knowledge Analysis for Planner

> **Framework**: How to decompose blueprint into executable tasks
> **Purpose**: Guide Planner's analysis process for each Zone

---

## 1. The 3 Tiers

| Tier | Name | Question | Output |
|------|------|----------|--------|
| **1** | **Domain** | "What must I UNDERSTAND before doing?" | Resource audit, gap identification |
| **2** | **Technical** | "What TOOLS and SKILLS are needed?" | Technical prerequisites |
| **3** | **Packaging** | "How do I STRUCTURE this for the agent?" | Task definitions with zone mapping |

---

## 2. Tier 1 — Domain Audit

### Purpose
Determine what domain knowledge exists vs. what's missing.

### Process

1. **List required knowledge** from blueprint §Zone Mapping
2. **Compare** with actual files in `resources/`
3. **Classify** each resource:
   - **Rich**: Complete, actionable, examples included
   - **Thin**: Has headings but lacks detail
   - **Missing**: Not present at all

### Decision Matrix

| Resource Status | Action |
|-----------------|--------|
| Rich | ✅ Mark as `rich`, no action needed |
| Thin | ⚠️ Mark as `thin`, add Task to expand |
| Missing | ❌ Mark as `missing`, add Task to create |

### Output

```yaml
pre_requisites:
  - tier: "domain"
    resource: "Prompt Injection Defense"
    status: "thin"
    action: "Expand from 2 paragraphs to comprehensive guide"
```

---

## 3. Tier 2 — Technical Requirements

### Purpose
Identify tools, syntax, and external dependencies.

### Process

1. **List technical needs** from blueprint:
   - Programming languages
   - External tools/APIs
   - Syntax requirements
2. **Check availability** of documentation
3. **Flag gaps** as prerequisites

### Common Technical Prerequisites

| Category | Example Prerequisites |
|----------|---------------------|
| Language | Python syntax, YAML format |
| Tooling | Docker, gVisor, sandbox |
| APIs | Claude API, tool use patterns |
| Frameworks | Mermaid, schema validation |

---

## 4. Tier 3 — Packaging to Zones

### Purpose
Map blueprint deliverables to actual tasks.

### Process

1. **Read §3 Zone Mapping** from blueprint
2. **For each Zone with content**:
   - Extract `Files cần tạo`
   - Determine file placement (zone)
   - Create Task with proper dependencies

### Zone Assignment

| Zone | File Types | Examples |
|------|------------|----------|
| core | SKILL.md, main entry | `SKILL.md`, `SPEC.md` |
| knowledge | .md files | `knowledge/*.md`, `policy/*.md` |
| scripts | executables | `scripts/*.py`, `scripts/*.sh` |
| templates | output formats | `templates/*.md`, `templates/*.yaml` |
| data | configs, schemas | `data/*.json`, `data/*.yaml` |
| loop | checklists | `loop/*.yaml`, `loop/*.md` |
| assets | static files | `assets/*` |

---

## 5. Conversion Checklist

For each Zone in blueprint §3, apply this checklist:

| # | Question | If YES → | If NO → |
|---|----------|----------|---------|
| C1 | Domain knowledge exists? | PRE-REQ rich | TASK: create/expand |
| C2 | Technical docs available? | PRE-REQ | TASK: prepare docs |
| C3 | Files to create in §3? | TASK per file | Skip |
| C4 | Templates needed? | TASK: create template | Skip |
| C5 | Scripts required? | TASK: create script | Skip |
| C6 | Loop checklists needed? | TASK: create checklist | Skip |

---

## 6. Example: skill-flow-designer

### Blueprint §3 Zone Mapping

```
Zone: Core
Files: SKILL.md, SPEC.md
Content: Persona Flow Architect, 3 phases

Zone: Knowledge  
Files: knowledge/uml-flow-rules.md
Content: UML Activity Diagram standards

Zone: Scripts
Files: scripts/validate-flow.py
Content: Mermaid syntax validation
```

### Applying 3-Tier Analysis

**Tier 1 — Domain:**
- UML standards needed → `resources/uml-rules.md` exists but is Thin
- → PRE-REQ: expand uml-rules.md
- → TASK: T0.1 Expand domain knowledge

**Tier 2 — Technical:**
- Python needed for validation script
- → PRE-REQ: ensure Python docs available

**Tier 3 — Packaging:**
- SKILL.md in Core → TASK: T1.1 Create SKILL.md
- uml-flow-rules.md in Knowledge → TASK: T2.1 Create knowledge/uml-flow-rules.md
- validate-flow.py in Scripts → TASK: T2.2 Create scripts/validate-flow.py

---

## 7. Trace Requirements

Every task MUST trace to a source:

```yaml
tasks:
  - task_id: "T1.1"
    trace: "[TỪ DESIGN §3.1]"    # From §3 Zone Mapping
  - task_id: "T0.1"
    trace: "[TỪ AUDIT TÀI NGUYÊN]" # Generated from gap
```

### Valid Trace Sources

| Source | When to Use |
|--------|-------------|
| `[TỪ DESIGN §N]` | Explicit in blueprint |
| `[TỪ AUDIT TÀI NGUYÊN]` | Resource gap identified |
| `[GỢI Ý BỔ SUNG]` | Planner adds, not in blueprint |
| `[CẦN LÀM RÕ]` | Cannot determine, need user |

---

## Key Takeaways

1. **Tier 1 asks**: What do I need to know?
2. **Tier 2 asks**: What tools do I need?
3. **Tier 3 asks**: What files do I create?
4. **Gap → Task**: Missing resources become PH0 tasks
5. **Trace everything**: No orphan tasks allowed
