# Markdown Cleaning Knowledge

> **Usage**: Load when markdown-fixer processes Markdown input. Contains heading hierarchy rules, list formatting patterns, and table standards.

## 1. Heading Hierarchy Rules

### Standard Heading Levels
| Level | Syntax | Common Use |
|-------|--------|------------|
| h1 | `# Title` | Document title |
| h2 | `## Title` | Major sections |
| h3 | `### Title` | Subsections |
| h4 | `#### Title` | Minor sections |
| h5 | `##### Title` | Details |
| h6 | `###### Title` | Fine details |

### Hierarchy Violations
```markdown
# Title
## Section
#### Subsection  (VIOLATION: skipped h3)
```

**Fix**: Insert missing level or restructure.

### ATX vs Setext
- ATX preferred: `# Heading`
- Setext allowed: `Heading\n===` for h1, `Heading\n---` for h2
- Convert Setext to ATX for consistency

## 2. List Formatting

### Unordered Lists
| Style | Example |
|-------|---------|
| hyphen | `- item` |
| asterisk | `* item` |
| plus | `+ item` |

**Standard**: hyphen preferred.

### Ordered Lists
```markdown
1. First
2. Second
3. Third
```

### Nesting Rules
```markdown
- Level 1
  - Level 2 (2 spaces indent)
    - Level 3 (4 spaces indent)
```

**Common Error**: 4 spaces instead of 2 for first nesting.

### List Item Spacing
```markdown
- Item 1

- Item 2 (double newline = new paragraph)
```

## 3. Code Block Formatting

### Fenced Code Blocks
```markdown
```python
def hello():
    print("world")
```
```

### Inline Code
| Content | Syntax |
|---------|--------|
| Single word | `` `code` `` |
| Multiple words | `` `code here` `` |
| With backticks | ``` ``code`with`backticks`` ``` |

### Indented Code Blocks (not preferred)
```markdown
    def hello():
        print("world")
```

**Fix**: Convert to fenced code blocks.

## 4. Table Structure (GFM)

### Standard Table
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|:--------:|--------:|
| Left     | Center   | Right   |
| Data     | Data     | Data    |
```

### Alignment
| Syntax | Alignment |
|--------|-----------|
| `:---` | Left |
| `:---:` | Center |
| `---:` | Right |
| `---` | Default (left) |

### Common Issues
```markdown
| A | B | C |   (missing pipe at end)
|---|---|---|

| A | B | C |
|--|--|--|   (inconsistent dashes)
|---|---|---|
```

## 5. Blockquote Formatting

### Standard
```markdown
> This is a blockquote
> spanning multiple lines
```

### Nested
```markdown
> Outer quote
> > Nested quote
> Back to outer
```

## 6. Link and Image Syntax

### Links
```markdown
[Link Text](https://example.com)
[Link Text](./relative/path)
```

### Images
```markdown
![Alt Text](./image.png)
```

### Reference Links (less common)
```markdown
[Link Text][reference]
[reference]: https://example.com
```

## 7. Emphasis and Strong

| Style | Syntax | Result |
|-------|--------|--------|
| Em | `*text*` or `_text_` | *text* |
| Strong | `**text**` or `__text__` | **text** |
| Both | `***text***` | ***text*** |

**Preference**: Use `*` for consistency.

## 8. Horizontal Rules

| Syntax | Behavior |
|--------|----------|
| `---` | Most compatible |
| `***` | Also common |
| `___` | Less common |

**Standard**: `---` preferred.

## 9. Escaping Characters

| Character | Escaped |
|-----------|---------|
| `\` | `\\` |
| `` ` `` | `` \` `` |
| `*` | `\*` |
| `#` | `\#` |
| `[]` | `\[` `\]` |
| `<>` | `\<` `\>` |
