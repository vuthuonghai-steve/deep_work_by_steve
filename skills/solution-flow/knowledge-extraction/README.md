# Knowledge Extraction — Trích xuất kiến thức thành Markdown chuẩn CLAUDE.md

## 1. Mục đích

Trích xuất kiến thức từ **repo được clone** hoặc **tài liệu (PDF, HTML, MD, Text)** thành các tài liệu markdown theo tiêu chuẩn CLAUDE.md.

## 2. Nhu cầu sử dụng

- Clone repo → khai thác code → tạo tài liệu skill
- Đọc PDF/tài liệu → chuyển thành knowledge base
- Xây dựng micro-skill từ tài liệu nguồn

## 3. Kiến trúc Knowledge Processor

```
knowledge-processor (Meta-Orchestrator)
├── pdf-extractor       — PDF → text (sandboxed, gVisor)
├── html-cleaner         — HTML → semantic Markdown
├── text-normalizer      — plain text → standard format
└── markdown-fixer      — Markdown → structure repair
```

## 4. Skills liên quan

### 4.1 Core Skills (Đã build từ pipeline)

| Skill | Chức năng | Vị trí |
|-------|-----------|---------|
| pdf-extractor | PDF → text (sandboxed gVisor) | skills/rebuild/pdf-extractor/ |
| html-cleaner | HTML → semantic Markdown | skills/rebuild/html-cleaner/ |
| text-normalizer | Text → standard format | skills/rebuild/text-normalizer/ |
| markdown-fixer | Markdown → structure repair | skills/rebuild/markdown-fixer/ |

### 4.2 Supporting Skills

| Skill | Chức năng | Vị trí |
|-------|-----------|---------|
| source-gatherer | Quét codebase, lọc nhiễu, bọc XML | skills/rebuild/source-gatherer/ |
| sandbox-validator | Kiểm định an toàn Docker | skills/rebuild/sandbox-validator/ |
| index-builder | Xây dựng chỉ mục llms.txt | skills/rebuild/index-builder/ |

## 5. Pipeline hoàn chỉnh

```
┌─────────────────────────────────────────────────────────────┐
│  KNOWLEDGE EXTRACTION PIPELINE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INPUT: PDF / HTML / MD / Text / Repo                       │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────┐                                      │
│  │ pdf-extractor   │ ← PDF → text (sandboxed)            │
│  │ html-cleaner    │ ← HTML → Markdown                    │
│  │ text-normalizer │ ← Text → standard                    │
│  │ markdown-fixer  │ ← MD → structure                    │
│  └────────┬────────┘                                      │
│           │                                                │
│           ▼                                                │
│  ┌─────────────────┐                                      │
│  │ source-gatherer │ ← Quét, lọc nhiễu, bọc XML         │
│  └────────┬────────┘                                      │
│           │                                                │
│           ▼                                                │
│  ┌─────────────────┐                                      │
│  │sandbox-validator│ ← Kiểm định an toàn                  │
│  └────────┬────────┘                                      │
│           │                                                │
│           ▼                                                │
│  ┌─────────────────┐                                      │
│  │  index-builder  │ ← Tạo chỉ mục llms.txt              │
│  └────────┬────────┘                                      │
│           │                                                │
│           ▼                                                │
│  OUTPUT: Markdown chuẩn CLAUDE.md                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 6. Vị trí Skills

```
skills/rebuild/
├── pdf-extractor/              # ✅ BUILD — PDF extraction
│   ├── SKILL.md
│   ├── knowledge/pdf-processing.md
│   ├── scripts/pdf-extractor.py
│   ├── data/normalize-rules.yaml
│   └── loop/validate-output.md

├── html-cleaner/              # ✅ BUILD — HTML to Markdown
│   ├── SKILL.md
│   ├── knowledge/html-sanitization.md
│   ├── scripts/html-cleaner.py
│   ├── data/normalize-rules.yaml
│   └── loop/validate-output.md

├── text-normalizer/           # ✅ BUILD — Text standardization
│   ├── SKILL.md
│   ├── scripts/text-normalizer.py
│   ├── data/normalize-rules.yaml
│   └── loop/validate-output.md

├── markdown-fixer/            # ✅ BUILD — Markdown repair
│   ├── SKILL.md
│   ├── knowledge/markdown-cleaning.md
│   ├── scripts/md-fixer.py
│   ├── data/normalize-rules.yaml
│   └── loop/validate-output.md

├── source-gatherer/           # Quét codebase
│   └── SKILL.md

├── sandbox-validator/          # Kiểm định
│   └── SKILL.md

└── index-builder/             # Chỉ mục
    └── SKILL.md
```

## 7. Cách sử dụng

### 7.1 PDF

```bash
python3 skills/rebuild/pdf-extractor/scripts/pdf-extractor.py input.pdf -o output.txt
```

### 7.2 HTML

```bash
python3 skills/rebuild/html-cleaner/scripts/html-cleaner.py input.html -o output.md
```

### 7.3 Text

```bash
python3 skills/rebuild/text-normalizer/scripts/text-normalizer.py input.txt -o output.md
```

### 7.4 Markdown

```bash
python3 skills/rebuild/markdown-fixer/scripts/md-fixer.py input.md -o output.md
```

### 7.5 Repository

```bash
# Chạy source-gatherer
python3 skills/rebuild/source-gatherer/scripts/gather.py /path/to/repo

# Chạy các micro-skills lần lượt
python3 skills/rebuild/pdf-extractor/scripts/pdf-extractor.py ...
python3 skills/rebuild/html-cleaner/scripts/html-cleaner.py ...
python3 skills/rebuild/text-normalizer/scripts/text-normalizer.py ...
python3 skills/rebuild/markdown-fixer/scripts/md-fixer.py ...
```

## 8. Trigger Keywords

| Từ khóa | Action |
|----------|--------|
| "doc pdf", "extract pdf" | pdf-extractor |
| "clean html", "html to md" | html-cleaner |
| "normalize text", "standardize" | text-normalizer |
| "fix markdown", "repair md" | markdown-fixer |
| "chuyen doi tai lieu", "knowledge extraction" | Tất cả |

## 9. Output

Tài liệu markdown theo tiêu chuẩn CLAUDE.md:
- **L0:** Root guide (anchor rules) — YAML frontmatter + XML boundaries
- **L1:** Policy/working rules — YAML blocks
- **L2:** Domain knowledge — Markdown + YAML snippets
- **L3:** Examples/evidence — XML wrapped

## 10. Output Location

```
knowledge/
├── {input-name}/              # Mỗi input là 1 thư mục cha
│   ├── README.md             # Mô tả nguồn
│   ├── source/               # Tài liệu gốc
│   └── processed/            # Đã xử lý (Markdown chuẩn CLAUDE.md)
└── knowledge-processor/      # Hệ thống xử lý
    └── README.md
```

## 11. Bảo mật

- pdf-extractor chạy trong sandbox (gVisor, `--network none`)
- HTML cleaner có sanitization chống XSS
- External content wrapped in XML boundaries
- Cấm execute code từ input

## 12. Liên quan

- **Knowledge Base:** `knowledge/`
- **Knowledge Processor:** `knowledge/knowledge-processor/`
- **CLAUDE.md chuẩn:** `/home/steve/Work-space/deep_work_by_steve/CLAUDE.md`
- **Skill Suite:** `skills/solution-flow/skill-builder-suite/README.md`
- **Agent Guide:** `skills/rebuild/AGENT.md`
