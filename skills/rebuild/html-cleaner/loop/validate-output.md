# HTML Cleaner Output Quality Checklist

## Pre-Validation

- [ ] Output file exists
- [ ] File size > 0 bytes
- [ ] UTF-8 encoding verified

## Security Sanitization

- [ ] No `<script>` tags present
- [ ] No `<style>` tags present
- [ ] No `<iframe>` tags present
- [ ] No `onclick`, `onerror`, `onload` attributes
- [ ] No `javascript:` protocol in URLs
- [ ] No inline styles present

## Structure Preservation

- [ ] Heading hierarchy intact (h1-h6)
- [ ] Lists properly formatted (- or 1.)
- [ ] Tables in Markdown syntax
- [ ] Code blocks with language hints
- [ ] Blockquotes as > quotes
- [ ] Links preserved with proper syntax

## Content Quality

- [ ] No excessive whitespace
- [ ] No blank lines > 2 consecutive
- [ ] Images as `![alt](src)` format
- [ ] Strong/em properly wrapped

## Error Handling

- [ ] Warnings logged if tags were removed
- [ ] Malformed HTML handled gracefully
- [ ] Empty input returns error
