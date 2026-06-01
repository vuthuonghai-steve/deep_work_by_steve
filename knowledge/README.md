# Knowledge Base — Trung tâm lưu trữ tài liệu đã chuyển đổi

## 1. Mục đích

Lưu trữ tài liệu kiến thức đã được chuyển đổi từ input (PDF, HTML, Text, Markdown) sang Markdown theo tiêu chuẩn CLAUDE.md.

## 2. Cấu trúc

```
knowledge/
├── README.md                         # File này
├── {input-name}/                    # Mỗi input là 1 thư mục cha
│   ├── README.md                    # Mô tả nguồn
│   ├── source/                      # Tài liệu gốc (PDF, MD, etc)
│   └── processed/                   # Tài liệu đã xử lý (Markdown chuẩn)
├── knowledge-processor/             # Hệ thống xử lý tài liệu
│   ├── README.md
│   ├── pdf-extractor/
│   ├── html-cleaner/
│   ├── text-normalizer/
│   └── markdown-fixer/
└── micro-skills/                   # Micro-skills đã tạo
```

## 3. Quy tắc đặt tên

| Loại | Quy tắc | Ví dụ |
|------|---------|-------|
| Thư mục cha | Tên repo/document | `siinstore-api`, `CLAUDE.md` |
| Tài liệu gốc | Giữ nguyên tên + extension | `README.pdf`, `architecture.md` |
| Tài liệu xử lý | Thêm suffix `.md` | `README.pdf.md`, `architecture.md` |

## 4. Trạng thái tài liệu

| Trạng thái | Nơi lưu | Mô tả |
|------------|----------|--------|
| Gốc | `source/` | Tài liệu ban đầu, không sửa |
| Đã xử lý | `processed/` | Đã chuyển đổi theo CLAUDE.md |

## 5. Thêm tài liệu mới

```bash
# Tạo thư mục cho input mới
mkdir -p knowledge/{input-name}/{source,processed}

# Copy tài liệu gốc
cp /path/to/original.pdf knowledge/{input-name}/source/

# Xử lý bằng knowledge-processor
python3 skills/rebuild/pdf-extractor/scripts/pdf-extractor.py \
  knowledge/{input-name}/source/original.pdf \
  -o knowledge/{input-name}/processed/original.pdf.md
```

## 6. Knowledge Processor

Hệ thống xử lý tài liệu với 4 micro-skills:

| Micro-skill | Chức năng |
|-------------|-----------|
| pdf-extractor | PDF → text (sandboxed) |
| html-cleaner | HTML → semantic Markdown |
| text-normalizer | Text → standard format |
| markdown-fixer | Markdown → structure repair |

Xem chi tiết: `knowledge-processor/README.md`

## 7. Tiêu chuẩn

Tất cả tài liệu trong `processed/` phải tuân theo CLAUDE.md:
- YAML frontmatter
- XML boundaries cho external content
- 4 layers (L0-L3)
- Token budget

## 8. Liên quan

- **Solution Flow:** `skills/solution-flow/knowledge-extraction/`
- **Skill Builder:** `skills/solution-flow/skill-builder-suite/`
- **Agent Guide:** `skills/rebuild/AGENT.md`
