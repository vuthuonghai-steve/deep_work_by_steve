#!/usr/bin/env python3
"""
Manage file backups for rollback capability.
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def create_backup(target_files: List[Path], backup_dir: Path) -> None:
    """Create backup of target files."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / timestamp
    backup_path.mkdir(parents=True, exist_ok=True)

    backed_up = []

    for file_path in target_files:
        if not file_path.exists():
            print(f"Warning: File not found, skipping: {file_path}")
            continue

        # Preserve directory structure
        relative_path = file_path.relative_to(file_path.anchor)
        backup_file = backup_path / relative_path

        backup_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_file)
        backed_up.append(file_path)

    # Create backup manifest
    manifest_file = backup_path / "MANIFEST.txt"
    with open(manifest_file, 'w') as f:
        f.write(f"Backup created: {timestamp}\n")
        f.write(f"Files backed up: {len(backed_up)}\n\n")
        for file_path in backed_up:
            f.write(f"{file_path}\n")

    print(f"✓ Backup created: {backup_path}")
    print(f"✓ Files backed up: {len(backed_up)}")


def restore_backup(backup_path: Path, target_project: Path) -> None:
    """Restore files from backup."""
    manifest_file = backup_path / "MANIFEST.txt"

    if not manifest_file.exists():
        print("Error: Backup manifest not found", file=sys.stderr)
        sys.exit(1)

    # Read manifest
    files_to_restore = []
    with open(manifest_file, 'r') as f:
        lines = f.readlines()
        for line in lines[3:]:  # Skip header lines
            file_path = line.strip()
            if file_path:
                files_to_restore.append(Path(file_path))

    restored = []

    for file_path in files_to_restore:
        relative_path = file_path.relative_to(file_path.anchor)
        backup_file = backup_path / relative_path

        if not backup_file.exists():
            print(f"Warning: Backup file not found: {backup_file}")
            continue

        # Restore file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_file, file_path)
        restored.append(file_path)

    print(f"✓ Restored {len(restored)} files from backup")


def list_backups(backup_dir: Path) -> None:
    """List available backups."""
    if not backup_dir.exists():
        print("No backups found")
        return

    backups = sorted([d for d in backup_dir.iterdir() if d.is_dir()])

    if not backups:
        print("No backups found")
        return

    print("Available backups:\n")
    for backup in backups:
        manifest = backup / "MANIFEST.txt"
        if manifest.exists():
            with open(manifest, 'r') as f:
                first_line = f.readline().strip()
                second_line = f.readline().strip()
            print(f"  {backup.name}")
            print(f"    {first_line}")
            print(f"    {second_line}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Manage file backups for conversion rollback"
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["backup", "restore", "list"],
        help="Action to perform"
    )
    parser.add_argument(
        "--context",
        required=True,
        help="Path to session context directory"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Files to backup (required for backup action)"
    )
    parser.add_argument(
        "--backup-id",
        help="Backup ID for restore action (timestamp)"
    )

    args = parser.parse_args()
    context_dir = Path(args.context)

    if not context_dir.exists():
        print(f"Error: Context directory not found: {context_dir}", file=sys.stderr)
        sys.exit(1)

    backup_dir = context_dir / "backups"

    if args.action == "backup":
        if not args.files:
            print("Error: --files required for backup action", file=sys.stderr)
            sys.exit(1)

        print("Creating backup...")
        target_files = [Path(file_path) for file_path in args.files]
        create_backup(target_files, backup_dir)

    elif args.action == "restore":
        if not args.backup_id:
            print("Error: --backup-id required for restore action", file=sys.stderr)
            sys.exit(1)

        backup_path = backup_dir / args.backup_id

        if not backup_path.exists():
            print(f"Error: Backup not found: {backup_path}", file=sys.stderr)
            sys.exit(1)

        print(f"Restoring backup: {args.backup_id}")
        target_project = Path(".")  # Would be from context
        restore_backup(backup_path, target_project)

    elif args.action == "list":
        list_backups(backup_dir)

    print("\n" + "=" * 60)
    print(f"Backup operation complete: {args.action}")
    print("=" * 60)


if __name__ == "__main__":
    main()
