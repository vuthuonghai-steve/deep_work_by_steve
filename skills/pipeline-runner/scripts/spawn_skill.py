#!/usr/bin/env python3
"""
Task Preparation Helper for Pipeline Runner

NOTE: This script prepares task spec for Claude Code's Task tool.
      Actual spawning is done by Claude Code (not Python).

Usage:
    python spawn_skill.py <task-input.json>
"""

import sys
import json
import subprocess
from pathlib import Path


def prepare_task_with_awareness(pipeline_config: dict, stage: dict, queue_state: dict) -> dict:
    """Build task input with full pipeline awareness context"""

    # Build predecessors from depends_on
    predecessors = []
    for dep_id in stage.get('depends_on', []):
        if dep_id in queue_state.get('stages', {}):
            dep_stage = queue_state['stages'][dep_id]
            predecessors.append({
                'stage_id': dep_id,
                'skill': dep_stage.get('skill', ''),
                'output_dir': dep_stage.get('output_dir', '')
            })

    # Calculate stage position
    all_stages = pipeline_config.get('stages', [])
    current_idx = next((i for i, s in enumerate(all_stages) if s['id'] == stage['id']), 0)
    total_stages = len(all_stages)
    percentage = f"{int((current_idx + 1) / total_stages * 100)}%"

    # Build pipeline context
    pipeline_context = {
        'pipeline_id': queue_state.get('pipeline_id', ''),
        'pipeline_name': pipeline_config.get('pipeline_name', ''),
        'current_stage_index': current_idx,
        'total_stages': total_stages,
        'stage_percentage': percentage,
        'predecessors': predecessors,
        'global_context': pipeline_config.get('global_context', {})
    }

    return pipeline_context


def spawn_subagent(task_input: dict) -> dict:
    """Spawn sub-agent to execute skill"""

    skill_name = task_input['skill_name']
    skill_path = task_input.get('skill_path')
    input_data = task_input.get('input', {})
    output_dir = task_input.get('output', {}).get('target_dir')

    # Include pipeline context in prompt if available
    pipeline_context = task_input.get('pipeline_context', {})
    context_info = ""
    if pipeline_context:
        context_info = f"""
## Pipeline Context
- Pipeline: {pipeline_context.get('pipeline_name', 'N/A')}
- Stage: {pipeline_context.get('current_stage_index', 0) + 1}/{pipeline_context.get('total_stages', 0)} ({pipeline_context.get('stage_percentage', 'N/A')})
- Predecessors: {len(pipeline_context.get('predecessors', []))}
"""

    # Build prompt for sub-agent
    prompt = f"""Execute skill: {skill_name}
{context_info}
Task Input:
{json.dumps(input_data, indent=2)}

Output Directory: {output_dir}

Read the skill definition from: {skill_path}
Execute the skill and write results to the designated output directory.
"""

    # NOTE: This returns the prompt for Claude Code's Task tool to use.
    # Claude Code will invoke skill-executor agent via Task tool automatically.
    return {
        'status': 'PREPARED_FOR_TASK_TOOL',
        'skill': skill_name,
        'prompt': prompt,
        'agent': 'skill-executor'
    }


def find_skill_path(skill_name: str) -> str:
    """Find skill SKILL.md path from skills.yaml registry"""

    import yaml

    # Try skills.yaml first (PRIMARY)
    skills_yaml_path = ".claude/skills/skills.yaml"
    if Path(skills_yaml_path).exists():
        with open(skills_yaml_path, 'r') as f:
            skills_data = yaml.safe_load(f)

        # Find skill in registry
        for skill in skills_data.get('skills', []):
            if skill.get('name') == skill_name:
                skill_path = skill.get('path', '')
                if skill_path:
                    skill_md = f"{skill_path}/SKILL.md"
                    if Path(skill_md).exists():
                        return skill_md

    # Fallback to search paths
    search_paths = [
        f'.claude/skills/{skill_name}/SKILL.md',
        f'.agent/skills/{skill_name}/SKILL.md',
        f'.codex/skills/{skill_name}/SKILL.md',
    ]

    for path in search_paths:
        if Path(path).exists():
            return path

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: spawn_skill.py <task-input.json>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, 'r') as f:
        task_input = json.load(f)

    # Find skill path
    skill_path = task_input.get('skill_path')
    if not skill_path:
        skill_path = find_skill_path(task_input['skill_name'])

    if not skill_path:
        print(f"❌ Skill not found: {task_input['skill_name']}")
        sys.exit(1)

    task_input['skill_path'] = skill_path

    # Spawn sub-agent
    result = spawn_subagent(task_input)

    print(f"✅ Spawned: {result['skill']}")
    print(f"   Prompt length: {len(result['prompt'])} chars")


if __name__ == "__main__":
    main()
