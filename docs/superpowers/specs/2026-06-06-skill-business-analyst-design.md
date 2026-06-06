# Skill Business Analyst — Design Spec

> **Date**: 2026-06-06
> **Status**: Pending user review
> **Stage**: Brainstorming → Design

---

## 1. Problem Statement

Pipeline tạo skill hiện tại (Explorer → Architect → Planner → Builder → Tester → Indexer) thiếu khâu **phân tích nghiệp vụ** trước Explorer. Khi người dùng mô tả nhu cầu skill, không có cơ chế bài bản !

- Phân rã yêu cầu thành luồng xử lý, cấu trúc dữ liệu, tiêu chí nghiệm thu
- Phát hiện và phản biện các vùng thông tin mơ hồ
- Sinh tài liệu BA chuẩn (Sequence Diagram, ERD, Gherkin, Risk Matrix)

---

## 2. Solution Overview

Hệ thống **3 micro-skills** hoạt động ở **Stage -1** (trước Explorer), phối hợp theo **Sequential Pipeline**:

```
User Input → ba-elicitor → ba-analyst → ba-synthesizer → Explorer
```

### 2.1 ba-elicitor (Tầng Tư duy)
- **Vai trò**: Normalize input, kích hoạt tư duy phản biện, phát hiện gap
- **Mindset Keywords**: Systems Thinking, Root Cause Isolation, MECE, First Principles, Impact Analysis, Structural Decomposition
- **Output**: `elicitation-report.md`

### 2.2 ba-analyst (Tầng Kiến thức + Kỹ năng)  
- **Vai trò**: Phân loại yêu cầu, sinh sơ đồ kỹ thuật, thiết kế dữ liệu
- **Deliverables**: FR/NFR Classification, MoSCoW, Sequence Diagram, Activity/Flowchart, ERD, Acceptance Criteria (Gherkin), Risk Matrix
- **Output**: `analysis-report.md`

### 2.3 ba-synthesizer (Tầng Tổng hợp)
- **Vai trò**: Consolidate, quality gate, handoff metadata
- **Output**: `business-analysis.md` → feed vào Explorer Stage 0

---

## 3. Technical Design

### 3.1 Input Contract
- **Flexible**: Raw text hoặc structured YAML
- **XML Boundary**: `<user_skill_request>...</user_skill_request>`
- **One-shot mode**: Phân tích và sinh output ngay, hỏi lại nếu mơ hồ

### 3.2 Output Contract
- **Final deliverable**: `business-analysis.md` trong `.skill-context/skill-business-analyst/`
- **YAML frontmatter** handoff metadata cho Explorer
- **7 deliverables** tổng hợp trong 1 file

### 3.3 State Management
- **State ledger**: `.skill-context/skill-business-analyst/`
- **Intermediate artifacts**: `elicitation-report.md`, `analysis-report.md`
- **Logs**: `.skill-context/skill-business-analyst/log/`

### 3.4 Progressive Disclosure
- **Tier 1 (Boot)**: SKILL.md cho active micro-skill
- **Tier 2 (Phase)**: knowledge/ files (mindset-keywords, mermaid-syntax, gherkin-guide)
- **Tier 3 (Output)**: templates/ cho output formatting

---

## 4. Quality Criteria (Production-Grade)

### Foundation (LLM-1.x)
- `<instructions>` block với must/must_not trong mỗi SKILL.md
- XML boundaries cho user input
- `<output_contract>` cuối mỗi SKILL.md

### Operational (LLM-2.x)
- SKILL.md < 500 tokens/micro-skill
- 3-Tier Progressive Disclosure
- Trace tags: `[TỪ INPUT]`, `[SUY LUẬN]`, `[CẦN LÀM RÕ]`

### Safety (LLM-3.x)
- Prompt injection defense via XML boundaries
- Self-verification via loop/ checklists
- ba-synthesizer runs cross-reference validation

### AGENTS.md Compliance
- YAML frontmatter đầy đủ
- Zero placeholders
- ≥5 acceptance criteria + ≥2 test cases

---

## 5. Architecture — Zone Mapping per Micro-Skill

### ba-elicitor (8 files)
```
ba-elicitor/
├── SKILL.md                          # Core orchestration
├── knowledge/
│   ├── mindset-keywords.md           # 6 BA Mindset Keywords
│   └── elicitation-rules.md          # Câu hỏi chuẩn hóa
├── templates/
│   └── elicitation-report.md.template
├── loop/
│   └── elicitor-checklist.md
└── data/
    └── input-schema.yaml             # Optional structured input schema
```

### ba-analyst (10 files)
```
ba-analyst/
├── SKILL.md
├── knowledge/
│   ├── classification-rules.md       # FR/NFR + MoSCoW
│   ├── mermaid-syntax.md             # Sequence, Activity, ERD syntax
│   ├── gherkin-guide.md              # Acceptance Criteria format
│   └── risk-assessment.md            # Risk & Impact framework
├── templates/
│   └── analysis-report.md.template
└── loop/
    └── analyst-checklist.md
```

### ba-synthesizer (7 files)
```
ba-synthesizer/
├── SKILL.md
├── knowledge/
│   └── quality-criteria.md           # Tiêu chí chất lượng
├── templates/
│   └── business-analysis.md.template
├── loop/
│   └── synthesizer-checklist.md
└── data/
    └── quality-matrix.yaml
```

---

## 6. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Input quá mơ hồ | High | Fallback: tag `[CẦN LÀM RÕ]`, sinh câu hỏi, chờ HITL |
| Mermaid syntax lỗi | Medium | Validated syntax trong knowledge/mermaid-syntax.md |
| Context overflow | Medium | Sequential pipeline, 1 micro-skill active/time |
| Handoff information loss | Medium | State ledger + frontmatter metadata bắt buộc |
| Explorer chưa đọc BA output | Low | Cần update Explorer Phase 1 |

---

## 7. Open Questions (Resolved)

| # | Question | Answer |
|---|----------|--------|
| 1 | Pipeline position? | Stage -1 (trước Explorer) |
| 2 | Analysis scope? | Chỉ cho skill AI Agent/LLM |
| 3 | Deliverables? | 7 loại (Elicitation, FR/NFR, MoSCoW, Sequence, Activity, ERD, Gherkin, Risk) |
| 4 | Input format? | Flexible (raw + structured) |
| 5 | Interaction mode? | One-shot với follow-up |
| 6 | Decomposition? | 3 micro-skills (elicitor, analyst, synthesizer) |
