#!/usr/bin/env python3
"""
Resume pipeline from checkpoint or failure

Usage:
    python resume_pipeline.py <_queue.json>
"""

import sys
import json
from pathlib import Path


def load_queue(path: str) -> dict:
    """Load _queue.json"""
    with open(path, 'r') as f:
        return json.load(f)


def find_failed_stage(queue: dict) -> str | None:
    """Find first failed stage"""
    for stage_id, stage in queue.get('stages', {}).items():
        if stage.get('status') == 'FAILED':
            return stage_id
    return None


def find_last_completed(queue: dict) -> str | None:
    """Find last completed stage"""
    completed = []
    for stage_id, stage in queue.get('stages', {}).items():
        if stage.get('status') == 'COMPLETED':
            completed.append(stage_id)
    return completed[-1] if completed else None


def reset_pipeline(queue: dict) -> dict:
    """Reset pipeline to resume from last completed stage"""
    last_completed = find_last_completed(queue)

    if not last_completed:
        # Start fresh
        for stage_id in queue.get('stages', {}):
            queue['stages'][stage_id]['status'] = 'PENDING'
        return queue

    # Reset stages after last completed
    reset_after = False
    for stage_id in queue.get('stages', {}):
        if reset_after:
            queue['stages'][stage_id]['status'] = 'PENDING'
        if stage_id == last_completed:
            reset_after = True

    return queue


def main():
    if len(sys.argv) < 2:
        print("Usage: resume_pipeline.py <_queue.json>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        queue = load_queue(path)

        # Show status
        print(f"📊 Pipeline Status: {queue.get('pipeline_name')}")

        failed = find_failed_stage(queue)
        if failed:
            print(f"   ⚠️ Failed stage: {failed}")

        last = find_last_completed(queue)
        if last:
            print(f"   ✅ Last completed: {last}")

        # Ask to reset
        print("\nReset pipeline to resume from last completed? [y/n]", end=' ')

        # For automation, just reset
        queue = reset_pipeline(queue)

        # Save
        with open(path, 'w') as f:
            json.dump(queue, f, indent=2)

        print("✅ Pipeline reset for resume")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
