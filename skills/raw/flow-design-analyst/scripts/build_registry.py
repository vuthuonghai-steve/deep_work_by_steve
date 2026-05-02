#!/usr/bin/env python3
"""
build_registry.py — Auto-Indexing Script for flow-design-analyst skill

Mục đích:
    Quét tự động toàn bộ thư mục tài liệu của một dự án (docs_dir),
    trích xuất các thành phần có cấu trúc từ file Markdown, và sinh ra
    file `project-registry.json` — nguồn tri thức dự án cho Skill sử dụng
    ở Phase 0 DETECT và Phase 1 DISCOVER.

Trích xuất:
    - Headings (H1, H2, H3) → tạo outline cấu trúc tài liệu
    - UC-ID references (UC01, UC-1, USE-CASE-01, v.v.)
    - Actor mentions (User, Admin, Guest, System, DB...)
    - Keywords từ heading và context xung quanh
    - Metadata: file path, last modified, line count

Sử dụng:
    python build_registry.py --docs-dir ./Docs --output ./project-registry.json
    python build_registry.py --docs-dir ./Docs --output ./project-registry.json --verbose
    python build_registry.py --docs-dir ./Docs --include "specs/**" --include "user-stories/**"

Output format: project-registry.json (xem §5 trong code)

Exit codes:
    0 = Thành công, sinh được registry file
    1 = Lỗi (không tìm thấy docs_dir, không có file .md nào, v.v.)
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from fnmatch import fnmatch
from dataclasses import dataclass, field, asdict
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# §1. CONSTANTS — Tập hợp patterns trích xuất
# ─────────────────────────────────────────────────────────────────────────────

# Pattern nhận diện UC-ID (linh hoạt theo nhiều convention phổ biến)
UC_ID_PATTERNS = [
    r"\bUC[\s\-_]?\d{1,3}\b",          # UC01, UC-01, UC_01, UC 01
    r"\bUC[\s\-_]?\d{1,3}[a-zA-Z]?\b", # UC01a, UC-01-A
    r"\bUSE[\s\-_]CASE[\s\-_]\d{1,3}\b", # USE-CASE-01
    r"\b(?:UC|F|FR|US|USER[\s\-]?STORY)[\s\-_]?\d+\b",  # FR-1, US-3, F01
]
UC_COMPILED = [re.compile(p, re.IGNORECASE) for p in UC_ID_PATTERNS]

# Keywords actor — nhận diện "diễn viên" trong flow
ACTOR_KEYWORDS = [
    "user", "guest", "member", "admin", "administrator",
    "system", "server", "backend", "api", "service",
    "database", "db", "mongodb", "postgres", "mysql", "redis",
    "client", "browser", "mobile", "frontend",
    "người dùng", "quản trị viên", "hệ thống", "máy chủ", "cơ sở dữ liệu",
    # Có thể mở rộng theo dự án
]

# Stop words — từ không có giá trị làm keyword
STOP_WORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "for", "on", "at",
    "is", "are", "was", "be", "been", "being", "have", "has", "with",
    "this", "that", "will", "can", "may", "from", "by", "as", "it",
    "not", "but", "all", "so", "do", "its", "if", "when", "where",
    "how", "what", "which", "who", "then", "than", "into", "over",
    "more", "also", "any", "each", "their", "them", "they",
    # Tiếng Việt stop words
    "và", "hoặc", "của", "để", "trong", "là", "với", "các", "một",
    "tất", "cả", "đến", "từ", "theo", "nếu", "khi", "thì", "cho",
    "được", "bởi", "do", "về", "có", "này", "đó", "như", "vào",
}

# Pattern nhận diện heading Markdown
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")

# Pattern nhận diện "Use Case" title trong heading
UC_TITLE_HINTS = re.compile(
    r"(?:use\s*case|use-case|uc|tính\s*năng|chức\s*năng|luồng|flow|scenario|feature)",
    re.IGNORECASE
)

# Pattern trích xuất từ có nghĩa (min 3 ký tự, tiếng Anh hoặc Việt)
TOKEN_PATTERN = re.compile(r"\b[a-zA-ZÀ-ỹ][a-zA-ZÀ-ỹ]{2,}\b")


# ─────────────────────────────────────────────────────────────────────────────
# §2. DATA MODELS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class HeadingNode:
    """Một heading trong file Markdown"""
    level: int          # 1–6 (H1–H6)
    text: str           # Nội dung heading
    line_number: int    # Dòng trong file
    uc_ids: list[str] = field(default_factory=list)    # UC-ID trích xuất từ heading
    actors: list[str] = field(default_factory=list)    # Actors trích xuất
    keywords: list[str] = field(default_factory=list)  # Keywords trích xuất
    context_lines: list[str] = field(default_factory=list)  # 3 dòng context sau heading


@dataclass
class FileEntry:
    """Đại diện cho một file .md đã được index"""
    relative_path: str          # Đường dẫn tương đối từ docs_dir
    absolute_path: str          # Đường dẫn tuyệt đối
    file_name: str              # Tên file (không có extension)
    last_modified: str          # ISO 8601
    line_count: int
    h1_title: Optional[str]     # H1 đầu tiên của file (main title)
    uc_ids: list[str] = field(default_factory=list)    # Tất cả UC-ID trong file
    actors: list[str] = field(default_factory=list)    # Tất cả actors trong file
    keywords: list[str] = field(default_factory=list)  # Top keywords
    headings: list[dict] = field(default_factory=list) # List HeadingNode dạng dict
    is_spec: bool = False        # Có phải spec file không?
    is_user_story: bool = False  # Có phải user story không?
    is_use_case: bool = False    # Có phải use case diagram không?


# ─────────────────────────────────────────────────────────────────────────────
# §3. EXTRACTION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def extract_uc_ids(text: str) -> list[str]:
    """Trích xuất tất cả UC-ID từ đoạn text"""
    found = set()
    for pattern in UC_COMPILED:
        for m in pattern.finditer(text):
            # Normalize: chuyển thành dạng chuẩn "UC01"
            raw = m.group(0).strip()
            normalized = re.sub(r"[\s\-_]", "", raw).upper()
            # Chỉ giữ lại dạng UCXX, FRXX, USXX
            if re.match(r"^(UC|FR|US|F)\d+", normalized):
                found.add(normalized)
    return sorted(found)


def extract_actors(text: str) -> list[str]:
    """Trích xuất tên actors được nhắc đến trong text"""
    found = set()
    text_lower = text.lower()
    for actor in ACTOR_KEYWORDS:
        if actor in text_lower:
            found.add(actor.title())  # Capitalize: "user" → "User"
    return sorted(found)


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """
    Trích xuất keywords có ý nghĩa từ text.
    Loại bỏ stop words, đếm tần suất, trả top_n từ phổ biến nhất.
    """
    tokens = TOKEN_PATTERN.findall(text.lower())
    freq: dict[str, int] = {}
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 2:
            freq[token] = freq.get(token, 0) + 1
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_tokens[:top_n]]


def classify_file(relative_path: str, h1_title: Optional[str]) -> tuple[bool, bool, bool]:
    """
    Phân loại loại file: is_spec, is_user_story, is_use_case.
    Dựa trên tên file và H1 title.
    """
    path_lower = relative_path.lower()
    title_lower = (h1_title or "").lower()

    spec_hints = ["spec", "specification", "requirement", "prd", "srs", "feature"]
    us_hints = ["user-stor", "user_stor", "stories", "userstory", "us-", "sprint"]
    uc_hints = ["use-case", "use_case", "usecase", "uc-", "diagram"]

    is_spec = any(h in path_lower or h in title_lower for h in spec_hints)
    is_user_story = any(h in path_lower or h in title_lower for h in us_hints)
    is_use_case = any(h in path_lower or h in title_lower for h in uc_hints)

    return is_spec, is_user_story, is_use_case


def parse_markdown_file(
    file_path: Path,
    docs_dir: Path,
    context_lines_count: int = 3,
    verbose: bool = False,
) -> Optional[FileEntry]:
    """
    Parse một file Markdown và trả về FileEntry đầy đủ.
    Trích xuất: headings, UC-ID, actors, keywords, metadata.
    """
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        if verbose:
            print(f"  ⚠️  Không đọc được {file_path}: {e}", file=sys.stderr)
        return None

    lines = content.splitlines()
    line_count = len(lines)
    relative_path = str(file_path.relative_to(docs_dir)).replace("\\", "/")

    stat = file_path.stat()
    last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

    # Trích xuất headings
    headings: list[HeadingNode] = []
    h1_title: Optional[str] = None

    for i, line in enumerate(lines):
        m = HEADING_PATTERN.match(line.strip())
        if not m:
            continue

        level = len(m.group(1))
        text = m.group(2).strip()

        # H1 đầu tiên = main title
        if level == 1 and h1_title is None:
            h1_title = text

        # Context: lấy context_lines_count dòng sau heading (không phải heading)
        context = []
        for j in range(i + 1, min(i + 1 + context_lines_count * 2, len(lines))):
            stripped = lines[j].strip()
            if not stripped or HEADING_PATTERN.match(stripped):
                break
            context.append(stripped)
            if len(context) >= context_lines_count:
                break

        context_text = " ".join(context)
        combined = f"{text} {context_text}"

        node = HeadingNode(
            level=level,
            text=text,
            line_number=i + 1,
            uc_ids=extract_uc_ids(combined),
            actors=extract_actors(combined),
            keywords=extract_keywords(combined, top_n=5),
            context_lines=context,
        )
        headings.append(node)

    # Tổng hợp từ toàn file
    all_uc_ids = sorted(set(uid for h in headings for uid in h.uc_ids))
    all_actors = sorted(set(a for h in headings for a in h.actors))

    # Keywords từ toàn bộ nội dung (top 15)
    all_keywords = extract_keywords(content, top_n=15)

    # Phân loại loại file
    is_spec, is_user_story, is_use_case = classify_file(relative_path, h1_title)

    return FileEntry(
        relative_path=relative_path,
        absolute_path=str(file_path),
        file_name=file_path.stem,
        last_modified=last_modified,
        line_count=line_count,
        h1_title=h1_title,
        uc_ids=all_uc_ids,
        actors=all_actors,
        keywords=all_keywords,
        headings=[asdict(h) for h in headings],
        is_spec=is_spec,
        is_user_story=is_user_story,
        is_use_case=is_use_case,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §4. SCANNER — Duyệt docs_dir và index tất cả file .md
# ─────────────────────────────────────────────────────────────────────────────

def should_include_file(file_path: Path, docs_dir: Path, include_patterns: list[str]) -> bool:
    """
    Kiểm tra xem file có nên được index không, dựa trên include_patterns.
    Nếu không có pattern nào, index tất cả .md files.
    """
    if not include_patterns:
        return True
    rel = str(file_path.relative_to(docs_dir)).replace("\\", "/")
    return any(fnmatch(rel, pat) for pat in include_patterns)


def scan_docs_dir(
    docs_dir: Path,
    include_patterns: list[str],
    exclude_dirs: list[str],
    verbose: bool = False,
) -> list[FileEntry]:
    """
    Duyệt đệ quy docs_dir, parse mọi file .md và trả list FileEntry.
    """
    entries: list[FileEntry] = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".agent", ".skill-context"}
    skip_dirs.update(d.lower() for d in exclude_dirs)

    all_md_files = []
    for root, dirs, files in os.walk(docs_dir):
        # Loại bỏ thư mục không cần scan
        dirs[:] = [d for d in dirs if d.lower() not in skip_dirs]

        for filename in files:
            if not filename.endswith(".md"):
                continue
            file_path = Path(root) / filename
            if should_include_file(file_path, docs_dir, include_patterns):
                all_md_files.append(file_path)

    total = len(all_md_files)
    if verbose:
        print(f"📂 Tìm thấy {total} file .md trong '{docs_dir}'")

    for i, file_path in enumerate(sorted(all_md_files), 1):
        rel = str(file_path.relative_to(docs_dir))
        if verbose:
            print(f"  [{i:03d}/{total:03d}] Parsing: {rel}")

        entry = parse_markdown_file(file_path, docs_dir, verbose=verbose)
        if entry:
            entries.append(entry)

    return entries


# ─────────────────────────────────────────────────────────────────────────────
# §5. REGISTRY BUILDER — Tổng hợp thành project-registry.json
# ─────────────────────────────────────────────────────────────────────────────

def build_registry(
    docs_dir: Path,
    output_path: Path,
    include_patterns: list[str],
    exclude_dirs: list[str],
    project_name: Optional[str],
    verbose: bool,
) -> dict:
    """
    Orchestrate scan → parse → tổng hợp → ghi JSON.

    Output format (project-registry.json):
    {
      "meta": {
        "generated_at": "ISO-8601",
        "docs_dir": "...",
        "project_name": "...",
        "total_files": N,
        "tool_version": "1.0.0"
      },
      "summary": {
        "all_uc_ids": [...],     # Tất cả UC-ID tìm được
        "all_actors": [...],     # Tất cả actors tìm được
        "file_types": {
          "spec_files": [...],        # Relative paths của spec files
          "user_story_files": [...],  # Relative paths của US files
          "use_case_files": [...],    # Relative paths của UC diagram files
          "other_files": [...]        # Còn lại
        }
      },
      "files": [
        {
          "relative_path": "...",
          "file_name": "...",
          "h1_title": "...",
          "uc_ids": [...],
          "actors": [...],
          "keywords": [...],
          "is_spec": true/false,
          "is_user_story": true/false,
          "is_use_case": true/false,
          "last_modified": "...",
          "line_count": N,
          "headings": [
            {
              "level": 2,
              "text": "...",
              "line_number": N,
              "uc_ids": [...],
              "actors": [...],
              "keywords": [...],
              "context_lines": [...]
            }
          ]
        },
        ...
      ]
    }
    """
    print(f"\n🔍 build_registry.py — Project Document Auto-Indexer")
    print(f"   docs_dir : {docs_dir}")
    print(f"   output   : {output_path}")
    if include_patterns:
        print(f"   include  : {include_patterns}")
    print()

    # Scan & parse
    entries = scan_docs_dir(docs_dir, include_patterns, exclude_dirs, verbose)

    if not entries:
        print("❌ Không tìm thấy file .md nào có thể index.", file=sys.stderr)
        sys.exit(1)

    # Tổng hợp summary
    all_uc_ids = sorted(set(uid for e in entries for uid in e.uc_ids))
    all_actors = sorted(set(a for e in entries for a in e.actors))

    spec_files = [e.relative_path for e in entries if e.is_spec]
    us_files = [e.relative_path for e in entries if e.is_user_story]
    uc_files = [e.relative_path for e in entries if e.is_use_case]
    other_files = [
        e.relative_path for e in entries
        if not e.is_spec and not e.is_user_story and not e.is_use_case
    ]

    # Build registry dict
    registry = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "docs_dir": str(docs_dir),
            "project_name": project_name or docs_dir.parent.name,
            "total_files": len(entries),
            "tool_version": "1.1.0",
        },
        "summary": {
            "all_uc_ids": all_uc_ids,
            "all_actors": all_actors,
            "file_types": {
                "spec_files": spec_files,
                "user_story_files": us_files,
                "use_case_files": uc_files,
                "other_files": other_files,
            },
        },
        "files": [asdict(e) for e in entries],
    }

    # Ghi file JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    return registry


# ─────────────────────────────────────────────────────────────────────────────
# §6. REPORT — In kết quả tóm tắt sau khi build
# ─────────────────────────────────────────────────────────────────────────────

def print_report(registry: dict) -> None:
    meta = registry["meta"]
    summary = registry["summary"]
    files = registry["files"]

    print(f"\n{'='*55}")
    print(f"  📋 REGISTRY BUILD REPORT")
    print(f"{'='*55}")
    print(f"  Project      : {meta['project_name']}")
    print(f"  Generated at : {meta['generated_at'][:19]}")
    print(f"  Total files  : {meta['total_files']}")
    print()

    ft = summary["file_types"]
    print(f"  📁 File Classification:")
    print(f"     Spec files       : {len(ft['spec_files'])}")
    print(f"     User story files : {len(ft['user_story_files'])}")
    print(f"     Use case files   : {len(ft['use_case_files'])}")
    print(f"     Other files      : {len(ft['other_files'])}")
    print()

    uc_ids = summary["all_uc_ids"]
    if uc_ids:
        print(f"  🔖 UC-IDs found ({len(uc_ids)}): {', '.join(uc_ids[:20])}")
        if len(uc_ids) > 20:
            print(f"     ... và {len(uc_ids) - 20} UC-ID khác")
    else:
        print(f"  🔖 UC-IDs: Không tìm thấy UC-ID nào")
    print()

    actors = summary["all_actors"]
    if actors:
        print(f"  👥 Actors found: {', '.join(actors)}")
    print()

    # Top 5 files nhều heading nhất (phức tạp nhất)
    top_files = sorted(files, key=lambda f: len(f.get("headings", [])), reverse=True)[:5]
    print(f"  📊 Top files (by heading count):")
    for f in top_files:
        h_count = len(f.get("headings", []))
        ucs = ", ".join(f.get("uc_ids", [])[:5]) or "—"
        print(f"     [{h_count:3d} headings] {f['relative_path']}")
        print(f"               UC-IDs: {ucs}")

    print(f"\n{'='*55}")
    print(f"  ✅ Registry saved successfully!\n")


# ─────────────────────────────────────────────────────────────────────────────
# §7. ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "build_registry.py — Tự động index tài liệu Markdown và sinh "
            "project-registry.json cho flow-design-analyst skill."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  # Index toàn bộ thư mục Docs/
  python build_registry.py --docs-dir ./Docs --output ./project-registry.json

  # Chỉ index file trong specs/ và user-stories/
  python build_registry.py --docs-dir ./Docs --output ./project-registry.json \\
      --include "specs/**" --include "user-stories/**"

  # Đặt tên project và xem verbose
  python build_registry.py --docs-dir ./Docs --output ./project-registry.json \\
      --project-name "My E-Commerce App" --verbose
        """,
    )
    parser.add_argument(
        "--docs-dir",
        required=True,
        help="Đường dẫn đến thư mục tài liệu cần index (bắt buộc)",
    )
    parser.add_argument(
        "--output",
        default="./project-registry.json",
        help="Đường dẫn file output JSON (mặc định: ./project-registry.json)",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Glob pattern để lọc file (có thể dùng nhiều lần, ví dụ: 'specs/**')",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        metavar="DIR",
        help="Tên thư mục cần bỏ qua (ví dụ: 'archive', 'draft')",
    )
    parser.add_argument(
        "--project-name",
        default=None,
        help="Tên dự án (mặc định: tên thư mục cha của docs_dir)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Hiển thị chi tiết quá trình parsing từng file",
    )

    args = parser.parse_args()

    docs_dir = Path(args.docs_dir).resolve()
    if not docs_dir.is_dir():
        print(f"❌ Lỗi: --docs-dir không tồn tại hoặc không phải thư mục: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output).resolve()

    registry = build_registry(
        docs_dir=docs_dir,
        output_path=output_path,
        include_patterns=args.include,
        exclude_dirs=args.exclude_dir,
        project_name=args.project_name,
        verbose=args.verbose,
    )

    print_report(registry)
    sys.exit(0)


if __name__ == "__main__":
    main()
