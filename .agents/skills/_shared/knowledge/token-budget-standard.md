# Token Budget Standard

**Reference**: CLAUDE.md L1_working_policy
**Purpose**: Define token limits for SKILL.md and knowledge files to prevent LLM context overflow

```yaml
token_budget:
  # Per L1_working_policy in CLAUDE.md
  L0_limit: 400        # Root guide / SKILL.md body
  L1_limit: 1200       # Working policy / knowledge files
  L2_limit: 2500       # Domain context / architecture docs
  tokenizer: cl100k_base  # tiktoken encoding for accurate counting
  enforcement: soft     # Warning at 80%, soft fail at limit
  warning_threshold: 0.8  # Warn when 80% of limit reached
```

## Usage

Reference in SKILL.md frontmatter:

```yaml
token_budget:
  $ref: "../_shared/knowledge/token-budget-standard.md#token_budget"
```

Or copy values directly with comment:

```yaml
token_budget:
  # Per L1_working_policy in CLAUDE.md
  L0_limit: 400
  L1_limit: 1200
  L2_limit: 2500
  tokenizer: cl100k_base
  enforcement: soft
```

## Enforcement

| Level | Threshold | Behavior |
|-------|-----------|----------|
| OK | < 80% | No warning |
| Warning | 80-100% | Log warning, continue |
| Exceeded | > 100% | Log error, block if hard enforcement |

## Token Counting Notes

- **cl100k_base**: GPT-4/Claude default tokenizer
- Vietnamese text: ~3-5 chars/token (higher than English's 4 chars/token)
- XML tags overhead: ~15-25 tokens per wrapper
