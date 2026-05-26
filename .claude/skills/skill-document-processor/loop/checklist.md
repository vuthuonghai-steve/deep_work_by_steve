# Document Processor Checklist

## Pre-Processing

- [ ] Input file exists
- [ ] Input file is readable
- [ ] File type detected correctly

## Processing

- [ ] PDF parsed successfully (if PDF input)
- [ ] Markdown cleaned (if MD input)
- [ ] Text converted to markdown (if text input)
- [ ] Content not empty

## Format Conversion

- [ ] YAML frontmatter added
- [ ] Content classified into L0-L3 layers
- [ ] YAML blocks extracted for rules
- [ ] XML boundaries added for external content
- [ ] Examples wrapped in XML tags

## Quality Gates

- [ ] L0 <= 400 tokens
- [ ] L1 <= 1200 tokens
- [ ] L2 <= 2500 tokens
- [ ] L3 <= 5000 tokens
- [ ] YAML syntax valid
- [ ] XML boundaries properly closed

## Output

- [ ] Output file created
- [ ] Content matches input
- [ ] Format complies with CLAUDE.md standard
