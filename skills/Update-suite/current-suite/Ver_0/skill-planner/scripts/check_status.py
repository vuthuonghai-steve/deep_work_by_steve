#!/usr/bin/env python3
"""
check_status.py — Check skill-planner status from blueprint.json
Ver_2.0.0 compatible

Usage:
    python check_status.py <context_dir> <skill_name>
"""

import sys
import json
import os
from datetime import datetime, timedelta

def check_status(context_dir, skill_name):
    """Check the current status of a skill's planning process."""

    blueprint_path = os.path.join(context_dir, skill_name, "blueprint.json")
    dag_plan_path = os.path.join(context_dir, skill_name, "dag_plan.json")

    # Check if blueprint exists
    if not os.path.exists(blueprint_path):
        return {
            'error': 'blueprint.json not found',
            'message': f'Run skill-architect first to create {blueprint_path}'
        }

    # Read blueprint
    with open(blueprint_path, 'r') as f:
        blueprint = json.load(f)

    result = {
        'skill_name': skill_name,
        'blueprint_exists': True,
        'dag_plan_exists': os.path.exists(dag_plan_path),
        'generated_at': blueprint.get('generated_at'),
        'last_actor': blueprint.get('generated_by', 'unknown'),
        'stage': 'planner'
    }

    # Check dag_plan if exists
    if os.path.exists(dag_plan_path):
        with open(dag_plan_path, 'r') as f:
            dag_plan = json.load(f)
        result['dag_plan_status'] = dag_plan.get('status', 'unknown')
        result['dag_plan_phase'] = detect_current_phase(dag_plan)
        result['dag_plan_updated'] = dag_plan.get('generated_at')

    # Check staleness
    if result.get('dag_plan_updated'):
        updated = datetime.fromisoformat(result['dag_plan_updated'])
        age = datetime.now() - updated
        result['is_stale'] = age.days > 7
        result['age_days'] = age.days
    else:
        result['is_stale'] = False
        result['age_days'] = 0

    return result

def detect_current_phase(dag_plan):
    """Detect current phase from dag_plan status."""
    status = dag_plan.get('status', 'in_progress')

    if status == 'ready_for_builder':
        return 4  # Complete
    elif status == 'blocked':
        # Check which phase has incomplete tasks
        for phase in reversed(dag_plan.get('phases', [])):
            for task in phase.get('tasks', []):
                if task.get('status') != 'done':
                    return int(phase.get('phase_id', 'PH0')[2:])
        return 3
    else:
        # Find first non-done task
        for phase in dag_plan.get('phases', []):
            for task in phase.get('tasks', []):
                if task.get('status') != 'done':
                    return int(phase.get('phase_id', 'PH0')[2:])
        return 4

def print_status(status):
    """Print status in human-readable format."""
    print("=" * 50)
    print(f"Skill: {status.get('skill_name', 'unknown')}")
    print("=" * 50)
    print(f"Blueprint: {'✅ exists' if status.get('blueprint_exists') else '❌ missing'}")
    print(f"DAG Plan: {'✅ exists' if status.get('dag_plan_exists') else '❌ missing'}")

    if status.get('dag_plan_exists'):
        print(f"Status: {status.get('dag_plan_status', 'unknown')}")
        print(f"Phase: PH{status.get('dag_plan_phase', 0)}")
        print(f"Updated: {status.get('dag_plan_updated', 'unknown')}")

        if status.get('is_stale'):
            print(f"⚠️  WARNING: DAG Plan is stale ({status.get('age_days')} days old)")
        else:
            print(f"✅ DAG Plan is fresh ({status.get('age_days')} days old)")

    if status.get('error'):
        print(f"\n❌ ERROR: {status['error']}")
        print(f"   {status.get('message', '')}")

    print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_status.py <context_dir> <skill_name>")
        print("Example: python check_status.py .skill-context my-skill")
        sys.exit(0)

    context_dir = sys.argv[1]
    skill_name = sys.argv[2]

    status = check_status(context_dir, skill_name)
    print_status(status)

    if status.get('error'):
        sys.exit(2)  # EMERGENCY
    elif status.get('is_stale'):
        sys.exit(1)  # WARNING
    else:
        sys.exit(0)  # SUCCESS
