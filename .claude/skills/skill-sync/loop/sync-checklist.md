# Sync Checklist

## Pre-Sync Quality Gate

- [ ] Source directory exists and is accessible
- [ ] All 4 destinations are writable
- [ ] Skills exist in source

## Post-Sync Verification

- [ ] Source hash matches hermes-ws
- [ ] Source hash matches claude-ws  
- [ ] Source hash matches hermes-usr
- [ ] Source hash matches claude-usr
- [ ] All files copied (rsync --delete verified)

## Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied | Check directory permissions |
| Source not found | Verify skills/rebuild/{skill}/SKILL.md exists |
| Partial sync | Re-run with --dry-run first |
