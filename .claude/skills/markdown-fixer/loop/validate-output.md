# Markdown Fixer Output Quality Checklist

## Pre-Validation

- [ ] Output file exists
- [ ] File size > 0 bytes
- [ ] UTF-8 encoding verified

## Heading Hierarchy

- [ ] No skipped heading levels (e.g., h1 directly to h3)
- [ ] Only one h1 at document start (or none)
- [ ] ATX syntax used (# not underlined)
- [ ] Proper spacing after #

## List Formatting

- [ ] Consistent bullet style (hyphen preferred)
- [ ] Proper indentation (2 spaces per level)
- [ ] No bare paragraphs in lists
- [ ] Ordered lists sequential

## Code Blocks

- [ ] Fenced code blocks use triple backticks
- [ ] Language hints preserved
- [ ] No mixed indentation in blocks
- [ ] Indented blocks converted to fenced

## Table Structure

- [ ] GFM pipe syntax used
- [ ] Header row present
- [ ] Delimiter row with dashes
- [ ] Consistent cell count
- [ ] Pipes at start and end

## Blockquotes

- [ ] Consistent > prefix
- [ ] Proper spacing after >
- [ ] Nested quotes formatted correctly

## General Formatting

- [ ] No multiple blank lines (>2)
- [ ] Horizontal rules as ---
- [ ] Links and images properly formatted
- [ ] No trailing whitespace

## Content Integrity

- [ ] All text content preserved
- [ ] No words or phrases altered
- [ ] Links unchanged
- [ ] Headings text preserved
