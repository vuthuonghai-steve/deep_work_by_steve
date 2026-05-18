# YAML Authoring Rules

## Problem

YAML parsers (including the Hermes linter) reject Markdown-style block quotes inside YAML files. Block scalar indicators (`>` or `|`) followed by text on the same line are parsed as YAML content, not comments.

## Symptom

```
YAMLError: while scanning a block scalar
expected a comment or a line break, but found '*'
```

## Wrong

```yaml
# **Usage**: Load at Phase 3.1 — FAILS because `>` is block scalar indicator
format_selection:
  markdown:
    use_for: [overview, rationale]
```

## Correct

### Option 1: Pure YAML data file

```yaml
# Use hash for comments only
format_selection:
  markdown:
    use_for: [overview, rationale]
```

### Option 2: Separate .md documentation

For documentation about a YAML config, create a separate Markdown file:
- `knowledge/format-selection-rules.md` (describes the YAML)
- `data/format-selection-rules.yaml` (pure data)

Reference the .md from SKILL.md.

## Inline comment rules

- `#` comments must have space after `#`
- Block scalar `>` or `|` cannot be followed by text on same line
- Multi-line strings: `|` (preserve) or `>` (fold) on their own line
