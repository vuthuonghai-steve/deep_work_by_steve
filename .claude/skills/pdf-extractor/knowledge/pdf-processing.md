---
name: pdf-processing-knowledge
description: PDF extraction domain knowledge for pdf-extractor skill
---

# PDF Processing Knowledge

> **Usage**: Load when pdf-extractor processes PDF input. Contains OCR options, table handling patterns, and security requirements.

## 1. PDF Text Extraction Methods

### Primary Method: pdftotext (poppler-utils)
```bash
pdftotext -layout input.pdf output.txt
```
- Preserves layout and spacing
- Best for text-based PDFs

### Fallback: pypdf
```python
from pypdf import PdfReader
reader = PdfReader("input.pdf")
for page in reader.pages:
    text = page.extract_text()
```
- Pure Python, no external dependencies
- Good for basic text extraction

### OCR Fallback: Tesseract
```python
import pytesseract
from pdf2image import convert_from_path
images = convert_from_path("input.pdf", dpi=300)
text = pytesseract.image_to_string(images[0])
```

## 2. OCR Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| dpi | 300 | Standard for readable text |
| lang | eng+unicode | Multi-language support |
| config | --psm 1 | Automatic page segmentation |

## 3. Table Handling

### Detection
- Look for consistent spacing patterns
- Detect vertical/horizontal line boundaries
- Use tabula-py for complex tables

### Output Markers
```
[TABLE_AMBIGUOUS] — merged cells or nested tables
[TABLE_EXTRACTED] — well-structured table
```

## 4. Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| Sandbox isolation | Docker with gVisor runtime |
| Script stripping | Remove /InterlateObjects, /XRef streams |
| No network | --network none |
| No filesystem | Read-only mount |

## 5. Error Handling

| Error | Response |
|-------|----------|
| Empty extraction | Try OCR fallback |
| Encrypted PDF | Return [ENCRYPTED] marker |
| OCR fails | Return error + HITL trigger |
| File > 10MB | Stream processing or reject |

## 6. Output Format

```markdown
# Document Title

## Section 1

Content paragraph...

### Subsection 1.1

[TABLE_EXTRACTED]
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |

[IMAGE_REMOVED]

## Section 2
```
