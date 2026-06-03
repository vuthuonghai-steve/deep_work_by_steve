---
name: skill-security-reviewer
description: OWASP-based security review skill for sensitive AI Agent skills (auth/payment/upload)
version: 1.0.0
tags:
  - security
  - OWASP
  - review
  - gatekeeper
when_to_use: |
  Khi skill có auth/payment/upload features — tự động invoke trước Gatekeeper approval.
  Không dùng cho documentation-only hoặc guidance skills.
---

# Skill Security Reviewer

## Security Review Workflow

```
Skill Creation → [Auth/Payment/Upload?] → YES → Security Review
                                          → NO → Skip to Gatekeeper
```

## OWASP Checklist (5 Critical Categories)

### SEC-01: Broken Access Control
```yaml
check:
  - "Auth checks present on all protected endpoints"
  - "Role/permission validation exists"
  - "No direct object references without ownership check"
```

### SEC-02: Cryptographic Failures
```yaml
check:
  - "No hardcoded secrets (API keys, passwords, tokens)"
  - "Environment variables for sensitive data"
  - "No credentials in logs or error messages"
```

### SEC-03: Injection
```yaml
check:
  - "No string concatenation in shell commands"
  - "Parameterized queries used"
  - "Input validation on all user inputs"
```

### SEC-04: Insecure Design
```yaml
check:
  - "Skill không tạo security holes trong output"
  - "Sandbox execution specified cho scripts"
  - "Rate limiting documented nếu applicable"
```

### SEC-05: Security Misconfiguration
```yaml
check:
  - "Docker sandboxing specified cho executable scripts"
  - "No default credentials generated"
  - "Error messages không leak sensitive info"
```

## Output Format

```markdown
=== SECURITY REVIEW REPORT ===
Skill: {skill-name}
Timestamp: {date}
Trigger: {auth|payment|upload|manual}

Verdict: APPROVED / REQUEST CHANGES / REJECTED

Findings:
- [CRITICAL] {description}
- [HIGH] {description}
- [MEDIUM] {description}
- [LOW] {description}

Action: {instruction for builder}
```

## Invocation

```yaml
triggers:
  auto:
    - skill has authentication feature
    - skill handles payment/data
    - skill accepts file uploads
  manual:
    - user explicitly requests security review
```

## Limitation

- This is a guidance/checklist skill, not a penetration testing tool
- For production security, always conduct manual review
- Security findings are recommendations, not guarantees

---

**Limitation**: Security review is advisory. Final security responsibility lies with developer.
