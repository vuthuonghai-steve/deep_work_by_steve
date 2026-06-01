# Knowledge Processor — Hệ thống chuyển đổi tài liệu thành Markdown chuẩn CLAUDE.md

## 1. Tổng quan

Hệ thống **Knowledge Processor** gồm 4 micro-skills để chuyển đổi tài liệu nguồn (PDF, HTML, Text, Markdown) thành Markdown theo tiêu chuẩn CLAUDE.md.

## 2. Kiến trúc

```
knowledge-processor (Meta-Orchestrator)
├── pdf-extractor       — PDF → text (sandboxed, gVisor)
├── html-cleaner        — HTML → semantic Markdown
├── text-normalizer     — plain text → standard format
└── markdown-fixer      — Markdown → structure repair
```

## 3. Pipeline

```
INPUT: PDF / HTML / Text / Markdown
         │
         ▼
┌─────────────────┐
│ pdf-extractor   │ ← PDF → text (sandboxed)
│ html-cleaner    │ ← HTML → Markdown
│ text-normalizer │ ← Text → standard
│ markdown-fixer  │ ← MD → structure
└────────┬────────┘
         │
         ▼
   OUTPUT: Markdown chuẩn CLAUDE.md
```

## 4. Danh sách Micro-skills

| Micro-skill | Chức năng | Vị trí |
|-------------|-----------|---------|
| pdf-extractor | PDF → text | skills/rebuild/pdf-extractor/ |
| html-cleaner | HTML → Markdown | skills/rebuild/html-cleaner/ |
| text-normalizer | Text → standard | skills/rebuild/text-normalizer/ |
| markdown-fixer | MD → structure | skills/rebuild/markdown-fixer/ |

## 5. Trigger Keywords

| Từ khóa | Micro-skill |
|----------|-------------|
| "doc pdf", "extract pdf" | pdf-extractor |
| "clean html", "html to md" | html-cleaner |
| "normalize text", "standardize" | text-normalizer |
| "fix markdown", "repair md" | markdown-fixer |
| "chuyen doi tai lieu" | Tất cả |

## 6. Tiêu chuẩn Output

Tất cả output đều tuân theo CLAUDE.md:
- **L0:** YAML frontmatter + anchor rules
- **L1:** Policy/constraints (YAML blocks)
- **L2:** Domain knowledge (Markdown)
- **L3:** Examples/evidence (XML wrapped)

## 7. Sử dụng

### 7.1 Python API

```python
from scripts.pdf_extractor import pdf_to_text
from scripts.html_cleaner import html_to_markdown
from scripts.text_normalizer import normalize_text
from scripts.md_fixer import fix_markdown
```

### 7.2 CLI

```bash
# PDF
python scripts/pdf-extractor.py input.pdf -o output.txt

# HTML
python scripts/html-cleaner.py input.html -o output.md

# Text
python scripts/text-normalizer.py input.txt -o output.md

# Markdown
python scripts/md-fixer.py input.md -o output.md
```

## 8. Validation

Mỗi micro-skill có `loop/validate-output.md` checklist.

## 9. Bảo mật

- pdf-extractor chạy trong sandbox (gVisor)
- HTML cleaner có sanitization chống XSS
- External content wrapped in XML boundaries

## 10. Liên quan

- **Context:** `.skill-context/knowledge-processor/`
- **Design:** `design.md`
- **Todo:** `todo.md`
- **Build Log:** `build-log.md`
- **Skill Suite:** `skills/solution-flow/skill-builder-suite/`
