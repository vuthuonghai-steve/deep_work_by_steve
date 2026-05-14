# Trigger Keywords Configuration

## Purpose

Defines keywords that trigger Heavy Thinking Manual activation.

## Bug Fix Triggers

```
fix bug
sửa lỗi
bug
fix error
sửa bug
khắc phục lỗi
```

## Feature Build Triggers

```
xây dựng tính năng
build feature
new feature
tạo tính năng
phát triển tính năng
```

## Ideation Triggers

```
lên ý tưởng
brainstorm
ideation
ý tưởng
đề xuất
định hướng
```

## Spec Creation Triggers

```
tạo spec
create spec
viết spec
thiết kế spec
tạo tài liệu
```

## Keyword Matching Rules

| Pattern | Match Type | Example |
|---------|-----------|---------|
| Exact match | case-insensitive | "fix bug" matches "FIX BUG" |
| Contains | substring | "bug" matches "fix bug" |
| Vietnamese | exact | "sửa lỗi" matches exactly |

## Trigger Detection Flow

1. User input received
2. Normalize input (lowercase, trim)
3. Match against trigger keywords
4. If match → Activate Heavy Thinking Manual
5. Classify task type from trigger
6. Proceed to context loading

## Task Type Mapping

| Trigger | Task Type |
|---------|-----------|
| fix bug, sửa lỗi, bug | bugfix |
| xây dựng tính năng, build feature, new feature | feature |
| lên ý tưởng, brainstorm, ideation | ideation |
| tạo spec, create spec, viết spec | spec |

## Multiple Trigger Detection

- If multiple triggers match → Use most specific match
- Priority: bug > feature > ideation > spec
- Report detected triggers to user

## Configuration

- case_sensitive: false
- min_keyword_length: 3
- match_strategy: contains
- priority_order: bugfix, feature, ideation, spec
