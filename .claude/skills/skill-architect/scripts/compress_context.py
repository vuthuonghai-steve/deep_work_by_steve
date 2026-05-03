#!/usr/bin/env python3
"""
compress_context.py — Token compression for skill context.

Usage:
    python compress_context.py <skill-dir>

Compresses knowledge files and templates by removing redundancy.
"""

import sys
import re
from pathlib import Path


def remove_html_comments(content: str) -> str:
    return re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)


def remove_redundant_headers(content: str) -> str:
    lines = content.split("\n")
    result = []
    prev_empty = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_empty:
                result.append(line)
            prev_empty = True
        else:
            result.append(line)
            prev_empty = False
    return "\n".join(result)


def summarize_sections(content: str, max_lines: int = 50) -> str:
    lines = content.split("\n")
    if len(lines) <= max_lines:
        return content

    # Keep first 30% and last 20%, summarize middle
    head_end = max_lines // 3
    tail_start = len(lines) - max_lines // 5

    head = lines[:head_end]
    tail = lines[tail_start:]

    summary = [
        "",
        "...[CONTENT COMPRESSED: middle section summarized]...",
        f"Original: {len(lines)} lines | Compressed: {head_end + len(tail)} lines",
        "",
    ]

    return "\n".join(head + summary + tail)


def compress_file(filepath: Path) -> str:
    content = filepath.read_text(encoding="utf-8")

    # Step 1: Remove HTML comments
    content = remove_html_comments(content)

    # Step 2: Remove redundant blank lines
    content = remove_redundant_headers(content)

    # Step 3: Summarize if very long
    lines = content.split("\n")
    if len(lines) > 100:
        content = summarize_sections(content)

    return content


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python compress_context.py <skill-dir>", file=sys.stderr)
        return 1

    skill_dir = Path(sys.argv[1])
    if not skill_dir.is_dir():
        print(f"ERROR: Not a directory: {skill_dir}", file=sys.stderr)
        return 1

    total_saved = 0

    def compress_dir(directory: Path, pattern: str) -> int:
        saved = 0
        if not directory.is_dir():
            return saved
        for f in directory.glob(pattern):
            original = f.read_text(encoding="utf-8")
            compressed = compress_file(f)
            delta = len(original) - len(compressed)
            if delta > 0:
                f.write_text(compressed, encoding="utf-8")
                saved += delta
                print(f"Compressed: {f.name} (saved {delta} chars)")
            else:
                print(f"Skipped: {f.name} (no savings)")
        return saved

    total_saved += compress_dir(skill_dir / "knowledge", "*.md")
    total_saved += compress_dir(skill_dir / "templates", "*.template")

    print(f"\nTotal saved: {total_saved} characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
