# PDF Extractor Output Quality Checklist

## Pre-Validation

- [ ] Output file exists
- [ ] File size > 0 bytes
- [ ] UTF-8 encoding verified

## Content Quality

- [ ] Heading hierarchy preserved (##, ###, etc.)
- [ ] Code blocks intact with language markers
- [ ] Tables extracted or [TABLE_AMBIGUOUS] marker present
- [ ] Images marked as [IMAGE_REMOVED] (not embedded)
- [ ] No binary content in body system

## Security Markers

- [ ] [ENCRYPTED] present if password-protected
- [ ] [OCR_APPLIED] present if Tesseract used
- [ ] No embedded scripts or executable content

## Error Handling

- [ ] Confidence score >= 70% OR HITL triggered
- [ ] Warnings logged if any extraction warnings
- [ ] Fallback chain documented in output

## Completeness

- [ ] All pages processed (page count verified)
- [ ] No empty sections where content expected
- [ ] Footnotes handled appropriately
