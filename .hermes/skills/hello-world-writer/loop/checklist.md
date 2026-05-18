# Hello World Writer — Verification Checklist

> **Usage**: Run through this checklist after writing a file to ensure the write was successful and safe.

---

## Pre-Write Verification

Before writing, verify:

- [ ] Target path is valid (no path traversal `..`)
- [ ] Parent directory exists and is accessible
- [ ] Write permission is available
- [ ] User has confirmed target path (if file exists, user confirmed overwrite)

---

## Post-Write Verification

After writing, verify:

- [ ] File exists at the specified path
- [ ] File content is exactly `Hello World` (12 characters, no extra whitespace)
- [ ] File is readable
- [ ] No errors occurred during write

---

## Error Handling Checklist

If any check fails:

- [ ] Log the error with specific failure reason
- [ ] Report failure to user with actionable message
- [ ] Do NOT claim success if verification failed

---

## Success Confirmation

When all checks pass:

```
✅ Write Successful
📄 File: [path]
📝 Content: "Hello World"
🔍 Verified: Read-back match confirmed
```
