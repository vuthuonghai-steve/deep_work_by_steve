## Cơ chế load skill trong tài liệu

Có, tài liệu Claude có đề cập đến cơ chế load skill. Theo tài liệu, skills sử dụng kiến trúc progressive disclosure (tiết lộ dần dần)[(6)](https://code.claude.com/docs/en/skills#advanced-patterns):

**Cơ chế progressive disclosure:**

* Khi khởi động, Claude quét metadata của mỗi skill (name và description)[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)
* Khi bạn trò chuyện với Claude và yêu cầu điều gì đó liên quan, Claude nhận ra cần skill đó và đọc phần còn lại của file chính[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)
* Skills load thông tin theo từng giai đoạn khi cần, thay vì tiêu thụ context ngay từ đầu[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)

**Trong session thông thường:**

* Mô tả skill được load vào context để Claude biết những gì có sẵn[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)
* Nội dung skill đầy đủ chỉ load khi được gọi[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)

**Tuy nhiên, có một bug đã được báo cáo:** Theo GitHub issue #15286, hành vi thực tế mâu thuẫn với tài liệu - skills do người dùng định nghĩa load toàn bộ nội dung khi khởi động thay vì chỉ metadata[(8)](https://github.com/anthropics/claude-code/issues/15286). Issue này đã được đóng, có thể đã được sửa trong các phiên bản gần đây.

## Subagents và Skills

Khi subagents sử dụng skills, có hai cách khác nhau:

### 1. Preload skills vào subagent

Subagents có thể preload skills cụ thể thông qua trường `skills:` trong frontmatter[(5)](https://code.claude.com/docs/en/sub-agents#configure-subagents). Khi preload,  **toàn bộ nội dung skill được inject vào context của subagent khi khởi động** , không chỉ làm cho nó có sẵn để gọi[(5)](https://code.claude.com/docs/en/sub-agents#configure-subagents).

Ví dụ:

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
skills:
  - api-conventions
  - security-guidelines
---
```

[(5)](https://code.claude.com/docs/en/sub-agents#configure-subagents)

**Lưu ý quan trọng:** Subagents không kế thừa skills từ cuộc hội thoại chính[(5)](https://code.claude.com/docs/en/sub-agents#configure-subagents)[(6)](https://code.claude.com/docs/en/skills#advanced-patterns). Bạn phải chỉ định rõ ràng skills nào subagent cần.

### 2. Skills với nhiều file hỗ trợ

Skills có thể bao gồm nhiều file trong thư mục của chúng[(6)](https://code.claude.com/docs/en/skills#advanced-patterns):

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)

**Cách để Claude load các file hỗ trợ:**

Bạn cần **tham chiếu các file hỗ trợ từ SKILL.md** để Claude biết chúng chứa gì và khi nào load chúng[(6)](https://code.claude.com/docs/en/skills#advanced-patterns):

```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

[(6)](https://code.claude.com/docs/en/skills#advanced-patterns)

**Khuyến nghị:** Giữ SKILL.md dưới 500 dòng[(6)](https://code.claude.com/docs/en/skills#advanced-patterns). Chuyển tài liệu tham khảo chi tiết sang các file riêng biệt[(6)](https://code.claude.com/docs/en/skills#advanced-patterns).

## Giải pháp cho vấn đề của bạn

Dựa trên vấn đề bạn mô tả - các file trong thư mục con của skill không được load - đây là các cách tiếp cận:

### Giải pháp 1: Tham chiếu rõ ràng trong SKILL.md

Trong file `SKILL.md` của bạn, hãy tham chiếu rõ ràng đến các file hỗ trợ:

```markdown
---
name: my-automation-skill
description: Automates deployment workflow
---

This skill handles automated deployment.

## Supporting files

- Deployment configuration: [config/deploy.yaml](config/deploy.yaml)
- Validation scripts: [scripts/validate.sh](scripts/validate.sh)
- Templates: [templates/notification.md](templates/notification.md)

When running deployment, first check the configuration file, then execute validation scripts.
```

### Giải pháp 2: Sử dụng imports trong SKILL.md

Mặc dù tài liệu không nói rõ về imports trong skills như CLAUDE.md, bạn có thể thử cú pháp tương tự:

```markdown
---
name: my-skill
description: Complex automation skill
---

Main instructions here.

Additional context:
@config/settings.md
@templates/workflow.md
```

### Giải pháp 3: Inline nội dung quan trọng

Nếu các file hỗ trợ nhỏ và quan trọng, hãy inline chúng trực tiếp vào SKILL.md thay vì để trong thư mục con. Điều này đảm bảo chúng luôn được load.

### Giải pháp 4: Hướng dẫn subagent đọc file

Trong frontmatter của subagent, đảm bảo nó có quyền truy cập tool `Read`[(5)](https://code.claude.com/docs/en/sub-agents#configure-subagents), sau đó trong SKILL.md, hướng dẫn rõ ràng:

```markdown
---
name: deployment-skill
description: Handles deployment automation
---

To execute deployment:

1. Read the configuration from `scripts/deploy-config.yaml`
2. Execute validation using `scripts/validate.sh`
3. Follow the template in `templates/deploy-steps.md`
```

Cách này yêu cầu subagent chủ động đọc các file thay vì chúng được load tự động vào context.

**Khuyến nghị tổng thể:** Kết hợp giải pháp 1 và 4 - tham chiếu rõ ràng các file trong SKILL.md và đảm bảo subagent có tool `Read` để truy cập chúng khi cần.
