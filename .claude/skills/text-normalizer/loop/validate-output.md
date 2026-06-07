# Text Normalizer Output Quality Checklist

## Pre-Validation

- [ ] Output file exists
- [ ] File size > 0 bytes
- [ ] UTF-8 encoding verified

## Encoding Normalization

- [ ] UTF-8 encoding confirmed
- [ ] No replacement characters (�)
- [ ] Smart quotes converted to ASCII
- [ ] Dashes normalized (– to -, — to --)
- [ ] Non-breaking spaces converted to regular spaces

## Line Ending Normalization

- [ ] No Windows-style line endings (\r\n)
- [ ] No old Mac-style line endings (\r)
- [ ] Unix line endings (\n) throughout

## Whitespace Normalization

- [ ] No leading whitespace on lines
- [ ] No trailing whitespace on lines
- [ ] Multiple spaces collapsed to single space
- [ ] Maximum 2 consecutive blank lines

## Structure Preservation

- [ ] Paragraph breaks preserved
- [ ] Code blocks detected and preserved
- [ ] Indented text handled correctly
- [ ] List-like structures maintained

## Content Integrity

- [ ] No content characters modified
- [ ] No words altered or truncated
- [ ] Special characters preserved
- [ ] Unicode characters maintained where valid
