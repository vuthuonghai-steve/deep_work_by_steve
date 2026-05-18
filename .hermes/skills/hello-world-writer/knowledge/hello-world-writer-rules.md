# Hello World Writer — File Write Rules

> **Usage**: Reference this file when implementing file write behavior and path validation for hello-world-writer skill.

---

## 1. Path Validation Rules

### 1.1 Absolute vs Relative Paths

| Path Type | Example | Behavior |
|-----------|--------|----------|
| Absolute | `/home/steve/file.txt` | Use as-is, validate parent exists |
| Relative | `file.txt` or `./file.txt` | Resolve against working directory |
| Relative with parent | `../file.txt` | Allow but warn about parent traversal |

### 1.2 Path Traversal Prevention

**Rule**: Block paths containing `..` that would escape the working directory.

```
❌ Blocked: /etc/passwd, ../../../etc/passwd
✅ Allowed: ./subdir/file.txt, subdir/file.txt
```

---

## 2. File Write Rules

### 2.1 Overwrite Behavior

| Scenario | Default Action | User Option |
|----------|--------------|-------------|
| File does not exist | Create new file | N/A |
| File exists | **Ask user** before overwriting | User can cancel |

### 2.2 Content Specification

- **Content**: Exactly `"Hello World"` (no quotes, no extra whitespace)
- **Encoding**: UTF-8
- **Line Ending**: Unix-style (LF `\n`)

---

## 3. Permission Requirements

### 3.1 Required Permissions

| Check | Command | Success Criteria |
|-------|---------|------------------|
| Parent directory exists | `os.path.exists(parent)` | `True` |
| Parent is directory | `os.path.isdir(parent)` | `True` |
| Write permission | `os.access(parent, os.W_OK)` | `True` |

### 3.2 Error Handling

| Error | Message | Action |
|-------|---------|--------|
| Parent doesn't exist | "Directory [path] does not exist" | Create directory or abort |
| No write permission | "Cannot write to [path]: Permission denied" | Abort |
| Disk full | "Write failed: No space left on device" | Abort |

---

## 4. Verification Rules

### 4.1 Read-Back Verification

After every write, **MUST** verify:

1. Read the file back using `read_file`
2. Compare content with original: must match exactly
3. Report success/failure

### 4.2 Verification Checklist

- [ ] File was created at correct path
- [ ] Content is exactly "Hello World"
- [ ] No extra newlines or whitespace
- [ ] File is readable

---

## 5. Security Considerations

| Risk | Mitigation |
|------|------------|
| Path traversal attack | Block `..` in path, validate against allowed directories |
| Permission escalation | Check parent directory permissions before write |
| Symbolic link attack | Resolve symlinks before validation |
