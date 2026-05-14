#!/usr/bin/env python3
"""
Heavy Thinking Manual — Chain Spawner
Spawns K=8 parallel reasoning chains using opencode-go or delegate_task
"""

import json
import subprocess
import sys
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

# Constants
DEFAULT_K = 8
CHAIN_TIMEOUT_SECONDS = 300  # 5 minutes per chain
OPENCODE_MODEL = "opencode-go/deepseek-v4-flash"

# Chain lens definitions
CHAIN_LENSES = [
    {
        "id": 1,
        "name": "Context & State",
        "focus": "Input sufficiency, cached vs fresh knowledge",
        "prompt_template": "Analyze the task from Context & State perspective. What context is provided vs assumed? Is context current or stale? What's the gap?"
    },
    {
        "id": 2,
        "name": "Handoff & Contract",
        "focus": "Session/agent/skill boundaries",
        "prompt_template": "Analyze the task from Handoff & Contract perspective. How does information transfer between boundaries? Where might info degrade?"
    },
    {
        "id": 3,
        "name": "Error Handling",
        "focus": "Hallucination, silent failures",
        "prompt_template": "Analyze the task from Error Handling perspective. Where might the LLM hallucinate? What failures could happen silently?"
    },
    {
        "id": 4,
        "name": "Propagation",
        "focus": "Codebase impact, side effects",
        "prompt_template": "Analyze the task from Propagation perspective. What other parts will this affect? What's the blast radius?"
    },
    {
        "id": 5,
        "name": "Quality Assurance",
        "focus": "Verification, diff, metrics",
        "prompt_template": "Analyze the task from Quality Assurance perspective. How to verify output correctness? What are acceptance criteria?"
    },
    {
        "id": 6,
        "name": "Risk Assessment",
        "focus": "Failure modes, risk mitigation",
        "prompt_template": "Analyze the task from Risk Assessment perspective. What's the worst case? What assumptions could be wrong?"
    },
    {
        "id": 7,
        "name": "Alternative Paths",
        "focus": "Other valid approaches",
        "prompt_template": "Analyze the task from Alternative Paths perspective. What are alternative solutions? What are the trade-offs?"
    },
    {
        "id": 8,
        "name": "Dependency Analysis",
        "focus": "External dependencies",
        "prompt_template": "Analyze the task from Dependency Analysis perspective. What external services do we depend on? What could break us?"
    }
]


def generate_task_id(trigger_keyword: str) -> str:
    """Generate task ID in format: {date}-{trigger}-{uuid}"""
    date = datetime.now().strftime("%Y-%m-%d")
    # Normalize trigger keyword
    trigger = trigger_keyword.lower().replace(" ", "-")[:20]
    short_uuid = str(uuid.uuid4())[:7]
    return f"{date}-{trigger}-{short_uuid}"


def spawn_opencode_chain(chain: Dict, context: Dict, task_id: str) -> Dict[str, Any]:
    """
    Spawn a single chain using opencode-go/deepseek-v4-flash.
    Primary method with fallback to delegate_task.
    """
    result = {
        "chain_id": chain["id"],
        "lens": chain["name"],
        "status": "pending",
        "execution_method": "opencode",
        "started_at": None,
        "completed_at": None,
        "findings": None,
        "error": None
    }
    
    try:
        result["started_at"] = datetime.utcnow().isoformat() + "Z"
        
        # Build prompt
        prompt = f"""You are Chain {chain['id']} of {DEFAULT_K} independent analysis chains.
Your lens: {chain['name']}
Focus: {chain['focus']}

TASK: Analyze the following task using your lens.

CONTEXT:
{json.dumps(context, indent=2)}

RULES:
- You CANNOT see other chains
- You CANNOT reference other chains  
- You CAN ONLY use the provided context
- Think independently and provide detailed findings

Output format:
```
⚡ Chain {chain['id']}: {chain['name']}
[SOURCE]: Where the finding came from
[GAP]: What context is missing
[RISK]: Potential risk identified
[RECOMMENDATION]: What to do
```

Analyze and provide your findings."""

        # Execute opencode
        cmd = [
            "opencode",
            "--model", OPENCODE_MODEL,
            "run", prompt
        ]
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CHAIN_TIMEOUT_SECONDS
        )
        
        if process.returncode == 0:
            result["status"] = "complete"
            result["findings"] = process.stdout
        else:
            result["status"] = "failed"
            result["error"] = process.stderr
        
        result["completed_at"] = datetime.utcnow().isoformat() + "Z"
        
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["error"] = f"Chain exceeded {CHAIN_TIMEOUT_SECONDS}s timeout"
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
    
    return result


def spawn_delegate_chain(chain: Dict, context: Dict, task_id: str) -> Dict[str, Any]:
    """
    Spawn a single chain using delegate_task (fallback method).
    This would be called if opencode fails.
    """
    result = {
        "chain_id": chain["id"],
        "lens": chain["name"],
        "status": "pending",
        "execution_method": "delegate_task",
        "started_at": datetime.utcnow().isoformat() + "Z",
        "completed_at": None,
        "findings": None,
        "error": None
    }
    
    # Note: In actual implementation, this would use the delegate_task tool
    # For now, return structure ready for delegation
    
    result["status"] = "pending_delegation"
    result["delegation_params"] = {
        "goal": f"Analyze task from {chain['name']} perspective: {chain['prompt_template']}",
        "context": json.dumps(context),
        "toolsets": ["terminal", "file"]
    }
    
    return result


def spawn_k_chains(context: Dict, task_id: str, task_type: str = None) -> Dict[str, Any]:
    """
    Spawn K=8 parallel reasoning chains.
    
    Primary: opencode-go/deepseek-v4-flash
    Fallback: delegate_task (if opencode fails)
    """
    print(f"Spawning K={DEFAULT_K} chains for task {task_id}...", file=sys.stderr)
    
    results = {
        "task_id": task_id,
        "spawned_at": datetime.utcnow().isoformat() + "Z",
        "total_chains": DEFAULT_K,
        "chains": [],
        "summary": {
            "completed": 0,
            "failed": 0,
            "pending": 0
        }
    }
    
    for chain in CHAIN_LENSES:
        print(f"  Spawning chain {chain['id']}: {chain['name']}...", file=sys.stderr)
        
        # Try opencode first
        chain_result = spawn_opencode_chain(chain, context, task_id)
        
        # Fallback to delegate if opencode failed
        if chain_result["status"] == "failed":
            print(f"    opencode failed, falling back to delegate_task...", file=sys.stderr)
            chain_result = spawn_delegate_chain(chain, context, task_id)
        
        results["chains"].append(chain_result)
        
        # Update summary
        status = chain_result["status"]
        if status == "complete":
            results["summary"]["completed"] += 1
        elif status == "failed":
            results["summary"]["failed"] += 1
        else:
            results["summary"]["pending"] += 1
    
    results["completed_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Print summary
    print(f"Chains complete: {results['summary']['completed']}/{DEFAULT_K}", file=sys.stderr)
    if results["summary"]["failed"] > 0:
        print(f"Chains failed: {results['summary']['failed']}/{DEFAULT_K}", file=sys.stderr)
    
    return results


def add_extra_chain_if_needed(chains: List[Dict], task_type: str) -> List[Dict]:
    """
    Add extra chain based on task type.
    
    - fix bug → Root Cause analysis
    - build feature → Impact analysis
    - ideation → Alternative exploration
    - spec → Dependency specification
    """
    extra_chain = None
    
    if task_type == "bugfix":
        extra_chain = {
            "id": 9,
            "name": "Root Cause",
            "focus": "Bug reproduction and root cause",
            "prompt_template": "Analyze from Root Cause perspective. What is the exact bug? How to reproduce? What is the underlying cause?"
        }
    elif task_type == "feature":
        extra_chain = {
            "id": 9,
            "name": "Impact Analysis",
            "focus": "Feature scope and impact",
            "prompt_template": "Analyze from Impact perspective. What is the feature scope? What systems does it affect?"
        }
    elif task_type == "ideation":
        extra_chain = {
            "id": 9,
            "name": "Alternative Exploration",
            "focus": "Idea validation and alternatives",
            "prompt_template": "Analyze from Alternative Exploration. Is this idea worth pursuing? What are the alternatives?"
        }
    elif task_type == "spec":
        extra_chain = {
            "id": 9,
            "name": "Dependency Specification",
            "focus": "Complete dependency specification",
            "prompt_template": "Analyze from Dependency Specification. What dependencies need to be specified? What is complete?"
        }
    
    if extra_chain:
        chains.append(extra_chain)
    
    return chains


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Heavy Thinking Chain Spawner")
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.add_argument("--context", required=True, help="JSON file with context")
    parser.add_argument("--task-type", help="Task type (bugfix, feature, ideation, spec)")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    # Load context
    with open(args.context, "r") as f:
        context = json.load(f)
    
    # Add extra chain if task type specified
    if args.task_type:
        add_extra_chain_if_needed(CHAIN_LENSES, args.task_type)
    
    # Spawn chains
    results = spawn_k_chains(context, args.task_id, args.task_type)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
