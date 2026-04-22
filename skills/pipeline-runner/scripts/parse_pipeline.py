#!/usr/bin/env python3
"""
Parse and validate pipeline.yaml or load from skills.yaml

Usage:
    python parse_pipeline.py <pipeline.yaml>
    python parse_pipeline.py --skills-yaml <pipeline_name>
"""

import sys
import yaml
import json
from pathlib import Path


SKILLS_YAML_PATH = ".claude/skills/skills.yaml"


def load_pipeline_from_skills(pipeline_name: str) -> dict:
    """Load pipeline definition from skills.yaml instead of hardcoded config"""
    with open(SKILLS_YAML_PATH, 'r') as f:
        skills_data = yaml.safe_load(f)

    pipelines = skills_data.get('pipelines', {})
    pipeline = pipelines.get(pipeline_name)

    if not pipeline:
        available = list(pipelines.keys())
        raise ValueError(f"Pipeline '{pipeline_name}' not found in skills.yaml. Available: {available}")

    # Extract stages with full DAG metadata
    return {
        'pipeline_name': pipeline.get('name', pipeline_name),
        'description': pipeline.get('description', ''),
        'pipeline_awareness': pipeline.get('pipeline_awareness', {}),
        'global_context': pipeline.get('global_context', {}),
        'stages': pipeline.get('stages', []),
        'execution': pipeline.get('execution', {}),
    }


def load_pipeline_config(path: str) -> dict:
    """Load and validate pipeline.yaml"""
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    required_fields = ['pipeline_name', 'stages']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")

    # Validate stages
    for stage in config['stages']:
        if 'id' not in stage:
            raise ValueError("Stage missing 'id' field")
        if 'skill' not in stage:
            raise ValueError(f"Stage {stage['id']} missing 'skill' field")

    return config


def find_runnable_stages(config: dict, completed: list) -> list:
    """Find stages that can run (dependencies satisfied)"""
    runnable = []

    for stage in config['stages']:
        stage_id = stage['id']

        # Skip already completed
        if stage_id in completed:
            continue

        # Check dependencies
        depends_on = stage.get('depends_on', [])
        if all(dep in completed for dep in depends_on):
            runnable.append(stage)

    return runnable


def resolve_variables(config: dict, context: dict) -> dict:
    """Resolve {} placeholders in config"""
    config_str = json.dumps(config)

    for key, value in context.items():
        placeholder = f"{{{key}}}"
        config_str = config_str.replace(placeholder, str(value))

    return json.loads(config_str)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  parse_pipeline.py <pipeline.yaml>           # Load from yaml file")
        print("  parse_pipeline.py --skills-yaml <name>     # Load from skills.yaml")
        sys.exit(1)

    # Mode 1: Load from skills.yaml (PRIMARY)
    if sys.argv[1] == '--skills-yaml':
        if len(sys.argv) < 3:
            print("Error: pipeline name required")
            sys.exit(1)
        pipeline_name = sys.argv[2]
        try:
            config = load_pipeline_from_skills(pipeline_name)
            print(f"✅ Pipeline loaded from skills.yaml: {config['pipeline_name']}")
            print(f"   Stages: {len(config['stages'])}")
            print(f"   Source: .claude/skills/skills.yaml")

            # Show stages with checkpoint info
            for stage in config['stages']:
                deps = stage.get('depends_on', [])
                checkpoint = stage.get('checkpoint', False)
                cp_marker = " [CHECKPOINT]" if checkpoint else ""
                print(f"   - {stage['id']}: {stage['skill']} (depends: {deps}){cp_marker}")

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    # Mode 2: Load from legacy pipeline.yaml
    else:
        path = sys.argv[1]
        try:
            config = load_pipeline_config(path)
            print(f"✅ Pipeline loaded: {config['pipeline_name']}")
            print(f"   Stages: {len(config['stages'])}")

            # Show stages
            for stage in config['stages']:
                deps = stage.get('depends_on', [])
                print(f"   - {stage['id']}: {stage['skill']} (depends: {deps})")

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
