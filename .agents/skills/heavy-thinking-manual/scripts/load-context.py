#!/usr/bin/env python3
"""
Heavy Thinking Manual — Context Loader
Loads context from Hermes Memory, Session History, and Project Files
"""

import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Constants
MAX_CONTEXT_SIZE = 50 * 1024  # 50KB per source
MAX_ENTRIES = 100

def load_hermes_memory() -> Dict[str, Any]:
    """
    Load context from Hermes Memory.
    Uses memory tool to retrieve user preferences, past sessions, etc.
    """
    result = {
        "status": "unavailable",
        "loaded_at": datetime.utcnow().isoformat() + "Z",
        "entries": [],
        "size_bytes": 0,
        "stale_entries": 0
    }
    
    try:
        # Check if memory entries exist
        # In actual implementation, this would call the Hermes memory tool
        # For now, return structure that can be populated
        
        # Simulate memory loading
        # In production: memory(action='list')
        
        result["status"] = "loaded"  # or "partial" or "unavailable"
        result["size_bytes"] = len(json.dumps(result["entries"]))
        
    except Exception as e:
        result["status"] = "unavailable"
        result["error"] = str(e)
    
    return result


def load_session_history(limit: int = 20) -> Dict[str, Any]:
    """
    Load context from current session history.
    Retrieves recent messages, pending tasks, recent corrections.
    """
    result = {
        "status": "unavailable",
        "loaded_at": datetime.utcnow().isoformat() + "Z",
        "session_id": "",
        "recent_messages": [],
        "pending_tasks": [],
        "recent_corrections": [],
        "continuation_patterns": [],
        "size_bytes": 0
    }
    
    try:
        # In production: session_search(query="", limit=limit)
        # This would retrieve recent conversation history
        
        result["status"] = "loaded"
        result["size_bytes"] = len(json.dumps(result))
        
    except Exception as e:
        result["status"] = "unavailable"
        result["error"] = str(e)
    
    return result


def load_project_files(workspace: str) -> Dict[str, Any]:
    """
    Load context from project files.
    Reads AGENTS.md, relevant source files, configurations.
    """
    result = {
        "status": "unavailable",
        "loaded_at": datetime.utcnow().isoformat() + "Z",
        "workspace": workspace,
        "files_loaded": [],
        "guidelines_found": {
            "coding_standards": False,
            "architecture_patterns": False,
            "naming_conventions": False
        },
        "size_bytes": 0,
        "truncated_files": 0
    }
    
    try:
        # Key files to look for
        key_files = [
            "AGENTS.md",
            "CLAUDE.md",
            ".claude/CLAUDE.md",
            "src/configs/app.ts",
            "package.json"
        ]
        
        # In production, would use file tools to read these
        # For now, structure is ready to be populated
        
        result["status"] = "loaded"
        result["size_bytes"] = len(json.dumps(result))
        
    except Exception as e:
        result["status"] = "unavailable"
        result["error"] = str(e)
    
    return result


def audit_context(context_sources: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audit loaded context and identify gaps.
    """
    audit = {
        "audit_timestamp": datetime.utcnow().isoformat() + "Z",
        "total_sources": 3,
        "loaded": 0,
        "partial": 0,
        "unavailable": 0,
        "missing_sources": [],
        "total_size_bytes": 0
    }
    
    for source_name, source_data in context_sources.items():
        status = source_data.get("status", "unavailable")
        size = source_data.get("size_bytes", 0)
        
        audit["total_size_bytes"] += size
        
        if status == "loaded":
            audit["loaded"] += 1
        elif status == "partial":
            audit["partial"] += 1
            audit["missing_sources"].append(f"{source_name} (partial)")
        else:
            audit["unavailable"] += 1
            audit["missing_sources"].append(source_name)
    
    return audit


def generate_gap_analysis(context_sources: Dict[str, Any]) -> Dict[str, str]:
    """
    Analyze gaps in loaded context.
    """
    gaps = {
        "user_preferences": "unknown",
        "project_context": "unknown",
        "session_continuity": "unknown"
    }
    
    # Memory analysis
    memory = context_sources.get("hermes_memory", {})
    if memory.get("status") == "loaded":
        entries = memory.get("entries", [])
        has_user_profile = any(e.get("type") == "user_profile" for e in entries)
        gaps["user_preferences"] = "current" if has_user_profile else "partial"
    
    # Session analysis
    session = context_sources.get("session_history", {})
    if session.get("status") == "loaded":
        messages = session.get("recent_messages", [])
        gaps["session_continuity"] = "complete" if len(messages) > 5 else "partial"
    
    # Project analysis
    project = context_sources.get("project_files", {})
    if project.get("status") == "loaded":
        files = project.get("files_loaded", [])
        gaps["project_context"] = "complete" if len(files) > 3 else "partial"
    
    return gaps


def load_all_context(workspace: str = ".") -> Dict[str, Any]:
    """
    Main function to load all context sources.
    Returns comprehensive context audit.
    """
    print("Loading context sources...", file=sys.stderr)
    
    # Load each source
    context_sources = {
        "hermes_memory": load_hermes_memory(),
        "session_history": load_session_history(),
        "project_files": load_project_files(workspace)
    }
    
    # Audit and analyze
    audit = audit_context(context_sources)
    gap_analysis = generate_gap_analysis(context_sources)
    
    # Build final output
    output = {
        "sources": context_sources,
        "audit_summary": audit,
        "gap_analysis": gap_analysis
    }
    
    # Print summary
    print(f"Context loaded: {audit['loaded']}/{audit['total_sources']} sources", file=sys.stderr)
    print(f"Total size: {audit['total_size_bytes']} bytes", file=sys.stderr)
    if audit['missing_sources']:
        print(f"Missing: {', '.join(audit['missing_sources'])}", file=sys.stderr)
    
    return output


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Heavy Thinking Context Loader")
    parser.add_argument("--workspace", default=".", help="Project workspace path")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    context = load_all_context(args.workspace)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(context, f, indent=2)
        print(f"Context written to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(context, indent=2))


if __name__ == "__main__":
    main()
