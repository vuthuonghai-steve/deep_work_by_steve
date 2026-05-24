# Context Sources — Memory, Session, Project Loading

## Overview

Heavy Thinking Manual loads context from 3 primary sources. This document details how to load each source, what format to return, and how to audit for gaps.

---

## Source 1: Hermes Memory

### What It Contains
- User profile (name, preferences, communication style)
- User's active projects
- Past session summaries
- Tool configurations and quirks
- Stable conventions and patterns

### How to Load

```python
# Via memory tool
memory(action='list')
```

### Expected Output Format

```json
{
  "source": "hermes_memory",
  "loaded_at": "2026-05-11T12:00:00Z",
  "entries": [
    {
      "type": "user_profile",
      "content": "Name: Steve, prefers Vietnamese, called 'anh yêu'"
    },
    {
      "type": "project_context",
      "content": "siinstore workspace at /home/steve/Work-space/siin/"
    },
    {
      "type": "convention",
      "content": "Prefers YAML output for verification reports"
    }
  ],
  "size_bytes": 1234,
  "status": "loaded|partial|unavailable"
}
```

### Gap Detection
- Check if user preferences are current
- Check if project context matches current workspace
- Flag stale entries (>7 days old)

---

## Source 2: Session History

### What It Contains
- Current conversation transcript
- Recent commands and outputs
- Pending tasks or todos
- Tool execution history
- User corrections and feedback

### How to Load

```python
# Via session_search tool
session_search(query="", limit=10)
```

### Expected Output Format

```json
{
  "source": "session_history",
  "loaded_at": "2026-05-11T12:00:00Z",
  "session_id": "abc123",
  "recent_messages": [
    {
      "role": "user|assistant",
      "content": "...",
      "timestamp": "2026-05-11T11:30:00Z"
    }
  ],
  "pending_tasks": ["..."],
  "recent_corrections": ["..."],
  "size_bytes": 5678,
  "status": "loaded|partial|unavailable"
}
```

### Gap Detection
- Check for "continuation" patterns ("làm tiếp", "continue")
- Identify broken chains of thought
- Flag missing context from previous sessions

---

## Source 3: Project Files

### What It Contains
- AGENTS.md / CLAUDE.md (project guidelines)
- Source code files
- Configuration files
- Documentation
- Test files

### How to Load

```python
# Via terminal + file tools
# 1. Read AGENTS.md if exists
# 2. Read relevant source files
# 3. Read configs
read_file(path="AGENTS.md")
search_files(pattern="...", path="src/")
```

### Expected Output Format

```json
{
  "source": "project_files",
  "loaded_at": "2026-05-11T12:00:00Z",
  "workspace": "/home/steve/Work-space/siin/siinstore-api",
  "files_loaded": [
    {
      "path": "AGENTS.md",
      "size_bytes": 4096,
      "type": "guidelines"
    },
    {
      "path": "src/configs/app.ts",
      "size_bytes": 2048,
      "type": "source"
    }
  ],
  "guidelines_found": {
    "coding_standards": true,
    "architecture_patterns": true,
    "naming_conventions": true
  },
  "size_bytes": 27648,
  "status": "loaded|partial|unavailable"
}
```

### Gap Detection
- Check if AGENTS.md exists
- Check if key source files are accessible
- Flag files that are too large (>50KB)

---

## Context Audit Process

### Step 1: Load All Sources

```python
context_sources = []
for source in ["hermes_memory", "session_history", "project_files"]:
    data = load_source(source)
    context_sources.append(data)
```

### Step 2: Aggregate Status

```json
{
  "audit_summary": {
    "total_sources": 3,
    "loaded": 2,
    "partial": 1,
    "unavailable": 0
  },
  "missing_sources": [],
  "gap_analysis": {
    "user_preferences": "current",
    "project_context": "partial - missing submodule info",
    "session_continuity": "complete"
  }
}
```

### Step 3: Report to User

```
Found 3 context sources:
- ✅ Hermes Memory: loaded (1.2KB)
- ✅ Session History: loaded (5.6KB)  
- ⚠️ Project Files: partial (27KB, AGENTS.md missing)

Missing context:
- Project guidelines (AGENTS.md not found)
- Recent commits from git history

Continue with available context, or provide missing information?
```

---

## Size Limits

| Source | Max Size | Behavior if Exceeded |
|--------|----------|---------------------|
| Hermes Memory | 50KB | Truncate oldest entries |
| Session History | 50KB | Keep recent 50 messages |
| Project Files | 50KB per file | Load summary only |

---

## Context Enrichment

After loading raw sources, enrich with:

1. **Temporal Context**: Add timestamps, time gaps
2. **Spatial Context**: Add file paths, workspace location
3. **Semantic Context**: Add domain labels, entity types
4. **Relationship Context**: Add "related to", "depends on"

### Enriched Context Template

```json
{
  "raw": { /* original source data */ },
  "enriched": {
    "temporal": {
      "created": "...",
      "modified": "...",
      "age_days": 3
    },
    "spatial": {
      "workspace": "...",
      "paths": ["..."]
    },
    "semantic": {
      "domain": "e-commerce",
      "entities": ["product", "order", "user"],
      "relationships": ["has_many", "belongs_to"]
    }
  }
}
```
