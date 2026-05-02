---
name: adaptive-workflow
description: Adaptive workflow - non-blocking questions, continuous execution, parallel tasks
user-invocable: true
context: fork
allowed-tools: Agent,AskUserQuestion,TaskCreate,TaskOutput,Bash,Read,Glob,Edit,Write
---

# Adaptive Workflow Skill

## Triết lý

Claude là người trợ lý liên tục - không bao giờ dừng chờ, luôn tiếp tục với assumptions hợp lý, thích ứng với thông tin mới.

## Commands

### /continue [reason]

Tiếp tục với current approach:
- Ghi nhận reason vào log
- Tiếp tục execution
- Monitor for contradictions

**Ví dụ:**
```
/continue Using password requirements from docs, will verify with user later
```

### /parallel [task1] | [task2]

Chạy tasks song song:
- Spawn Agent cho mỗi task
- Tiếp tục workflow chính
- Merge khi có results

**Ví dụ:**
```
/parallel Analyze auth flow | Research best practices
```

### /checkpoint

Lưu current state trước khi risky operation:
- Ghi current context to checkpoint file
- Tiếp tục execution
- Có thể rollback nếu cần

**Ví dụ:**
```
/checkpoint Before refactoring auth module
```

### /adapt [new-info]

Cập nhật direction dựa trên thông tin mới:
- Merge new info vào context
- Re-evaluate current approach
- Adjust nếu needed

**Ví dụ:**
```
/adapt Password must be 12+ chars with special chars
```

## Workflow Behavior

### Khi user yêu cầu clarification

Thay vì dừng lại chờ:

1. **Đánh giá context hiện có**
2. **Đưa ra reasonable assumption**
3. **Tiếp tục với assumption đó**
4. **Log assumption để track**

### Khi cần hỏi user

1. **Ưu tiên /btw** cho câu hỏi ngắn
2. **Spawn background agent** cho câu hỏi phức tạp
3. **Tiếp tục main workflow** trong khi chờ response
4. **Merge response** khi có

### Khi có new information

1. **Assess** - New info có contradict current approach?
2. **Adapt** - Nếu có, điều chỉnh direction
3. **Continue** - Tiếp tục với updated context

## Anti-Patterns (Tránh)

- ❌ Dừng lại chờ user response mà không continue
- ❌ Assume user sẽ respond ngay lập tức
- ❌ Ignore new information contradictory to approach
- ❌ Không log assumptions

## Best Practices

- ✅ Luôn log assumptions trước khi tiếp tục
- ✅ Sử dụng /btw cho quick questions
- ✅ Spawn background tasks cho complex questions
- ✅ Re-evaluate khi có new info
- ✅ Be explicit về đang work với assumption nào

---

*Adaptive Workflow Skill v1.0 - 2026-03-17*
