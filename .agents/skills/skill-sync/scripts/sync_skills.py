#!/usr/bin/env python3
"""
Sync skills from source to all destinations.
Usage: python sync_skills.py [skill-name] [--all]
"""

import os
import hashlib
import subprocess
import yaml
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR.parent / "data" / "sync-locations.yaml"
SOURCE_BASE = "/home/steve/Work-space/deep_work_by_steve/skills/rebuild"

def load_config():
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def get_md5(path):
    """Get MD5 hash of a file."""
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def get_skills_in_source():
    """List all skills in source directory."""
    source_path = Path(SOURCE_BASE)
    if not source_path.exists():
        return []
    return [d.name for d in source_path.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

def compare_hashes(skill_name, config):
    """Compare hashes across all destinations."""
    source_file = Path(SOURCE_BASE) / skill_name / "SKILL.md"
    if not source_file.exists():
        return None, {}

    source_hash = get_md5(str(source_file))
    results = {}

    for dest_name, dest_config in config['destinations'].items():
        dest_path = Path(dest_config['path']) / skill_name / "SKILL.md"
        results[dest_name] = {
            'hash': get_md5(str(dest_path)),
            'path': str(dest_path),
            'exists': dest_path.exists()
        }

    return source_hash, results

def sync_skill(skill_name, config, dry_run=False):
    """Sync a single skill to all destinations."""
    source = Path(SOURCE_BASE) / skill_name

    if not source.exists():
        print(f"❌ Source not found: {source}")
        return False

    print(f"\n=== Syncing: {skill_name} ===")

    for dest_name, dest_config in config['destinations'].items():
        dest_path = Path(dest_config['path']) / skill_name

        # Create destination directory if needed
        dest_path.mkdir(parents=True, exist_ok=True)

        # rsync command
        cmd = ['rsync', '-av']
        if dry_run:
            cmd.append('--dry-run')
        cmd.extend([str(source) + '/', str(dest_path) + '/'])

        print(f"\n  → {dest_name}: {dest_config['path']}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    ✅ Synced")
        else:
            print(f"    ❌ Error: {result.stderr}")

    return True

def print_comparison_table(skill_name, source_hash, results):
    """Print a comparison table."""
    print(f"\n{'='*80}")
    print(f"Skill: {skill_name}")
    print(f"Source: {source_hash}")
    print(f"{'='*80}")
    print(f"{'Destination':<25} {'Hash':<35} {'Status'}")
    print(f"{'-'*80}")

    for dest_name, data in results.items():
        hash_str = data['hash'] or 'N/A'
        if data['hash'] == source_hash:
            status = '✅ SYNCED'
        elif data['hash'] is None:
            status = '🆕 NEW'
        else:
            status = '❌ DIFFERENT'
        print(f"{dest_name:<25} {hash_str:<35} {status}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sync skills to destinations')
    parser.add_argument('skill', nargs='?', help='Skill name to sync (default: all)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be synced')
    parser.add_argument('--compare', action='store_true', help='Compare hashes only, no sync')
    args = parser.parse_args()

    config = load_config()
    skills = get_skills_in_source()

    if args.skill:
        skills = [args.skill] if args.skill in skills else []
        if not skills:
            print(f"❌ Skill '{args.skill}' not found in source")
            return

    if not skills:
        print("❌ No skills found")
        return

    # Compare phase
    print("\n" + "="*80)
    print("HASH COMPARISON")
    print("="*80)

    all_synced = True
    for skill in sorted(skills):
        source_hash, results = compare_hashes(skill, config)
        print_comparison_table(skill, source_hash, results)

        if any(r['hash'] != source_hash for r in results.values() if r['hash'] is not None):
            all_synced = False

    # Sync phase (if not --compare)
    if not args.compare:
        if not all_synced or args.skill:
            print("\n" + "="*80)
            print("SYNCING...")
            print("="*80)

            for skill in sorted(skills):
                sync_skill(skill, config, dry_run=args.dry_run)

            # Final comparison
            print("\n" + "="*80)
            print("FINAL VERIFICATION")
            print("="*80)
            for skill in sorted(skills):
                source_hash, results = compare_hashes(skill, config)
                print_comparison_table(skill, source_hash, results)

if __name__ == '__main__':
    main()
