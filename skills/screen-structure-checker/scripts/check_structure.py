#!/usr/bin/env python3
"""
Screen Structure Checker
Kiem tra cau truc thu muc screens theo kien truc quan ly tap trung.

Usage:
    python3 check_structure.py /path/to/screen
    python3 check_structure.py /path/to/screens --all
    python3 check_structure.py /path/to/screen --json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Violation:
    rule: str
    message: str
    severity: Severity
    path: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class ScreenReport:
    name: str
    path: str
    passed: int = 0
    failed: int = 0
    violations: List[Violation] = field(default_factory=list)
    
    @property
    def score(self) -> str:
        total = self.passed + self.failed
        if total == 0:
            return "N/A"
        return f"{self.passed}/{total}"
    
    @property
    def status(self) -> str:
        if self.failed == 0:
            return "✅ PASS"
        return "❌ NEEDS IMPROVEMENT"


class ScreenStructureChecker:
    """Kiem tra cau truc thu muc screen."""
    
    # Cac thu muc/file bat buoc
    REQUIRED_FILES = ["index.tsx"]
    
    # Cac thu muc khuyen nghi
    RECOMMENDED_DIRS = ["components", "hooks"]
    
    # Cac thu muc optional
    OPTIONAL_DIRS = ["types", "utils", "constants"]
    
    # Naming conventions
    COMPONENT_PATTERN = r'^[A-Z][a-zA-Z0-9]*\.tsx$'  # PascalCase
    HOOK_PATTERN = r'^use[A-Z][a-zA-Z0-9]*\.ts$'     # useXxx
    
    # File size limit (lines)
    MAX_FILE_LINES = 200
    
    def __init__(self, screen_path: str):
        self.screen_path = Path(screen_path)
        self.screen_name = self.screen_path.name
        self.report = ScreenReport(
            name=self.screen_name,
            path=str(self.screen_path)
        )
    
    def check_all(self) -> ScreenReport:
        """Chay tat ca cac kiem tra."""
        self._check_main_component()
        self._check_components_dir()
        self._check_hooks_dir()
        self._check_types_dir()
        self._check_naming_convention()
        self._check_file_sizes()
        self._check_barrel_exports()
        return self.report
    
    def _check_main_component(self):
        """Kiem tra co index.tsx hoac {ScreenName}.tsx."""
        has_index = (self.screen_path / "index.tsx").exists()
        has_named = (self.screen_path / f"{self.screen_name}.tsx").exists()
        
        if has_index or has_named:
            self.report.passed += 1
        else:
            self.report.failed += 1
            self.report.violations.append(Violation(
                rule="has_main_component",
                message=f"Thieu file component chinh (index.tsx hoac {self.screen_name}.tsx)",
                severity=Severity.ERROR,
                path=str(self.screen_path),
                suggestion=f"Tao file index.tsx hoac {self.screen_name}.tsx lam component chinh"
            ))
    
    def _check_components_dir(self):
        """Kiem tra thu muc components/."""
        components_dir = self.screen_path / "components"
        
        if components_dir.exists() and components_dir.is_dir():
            self.report.passed += 1
        else:
            self.report.failed += 1
            self.report.violations.append(Violation(
                rule="has_components_dir",
                message="Thieu thu muc components/",
                severity=Severity.WARNING,
                path=str(self.screen_path),
                suggestion="Tao thu muc components/ de chua cac sub-components"
            ))
    
    def _check_hooks_dir(self):
        """Kiem tra thu muc hooks/."""
        hooks_dir = self.screen_path / "hooks"
        
        if hooks_dir.exists() and hooks_dir.is_dir():
            self.report.passed += 1
        else:
            self.report.failed += 1
            self.report.violations.append(Violation(
                rule="has_hooks_dir",
                message="Thieu thu muc hooks/",
                severity=Severity.WARNING,
                path=str(self.screen_path),
                suggestion="Tao thu muc hooks/ de chua custom hooks (useScreenData, useScreenActions...)"
            ))
    
    def _check_types_dir(self):
        """Kiem tra thu muc types/."""
        types_dir = self.screen_path / "types"
        
        if types_dir.exists() and types_dir.is_dir():
            self.report.passed += 1
        else:
            self.report.violations.append(Violation(
                rule="has_types_dir",
                message="Thieu thu muc types/",
                severity=Severity.INFO,
                path=str(self.screen_path),
                suggestion="Tao thu muc types/ de chua TypeScript interfaces/types"
            ))
    
    def _check_naming_convention(self):
        """Kiem tra quy uoc dat ten."""
        violations_found = False
        
        # Kiem tra components
        components_dir = self.screen_path / "components"
        if components_dir.exists():
            for item in components_dir.iterdir():
                if item.is_file() and item.suffix == ".tsx":
                    # Phai la PascalCase
                    if not item.stem[0].isupper():
                        violations_found = True
                        self.report.violations.append(Violation(
                            rule="naming_convention",
                            message=f"Component '{item.name}' khong dung PascalCase",
                            severity=Severity.ERROR,
                            path=str(item),
                            suggestion=f"Doi ten thanh '{item.stem.title()}.tsx'"
                        ))
        
        # Kiem tra hooks
        hooks_dir = self.screen_path / "hooks"
        if hooks_dir.exists():
            for item in hooks_dir.iterdir():
                if item.is_file() and item.suffix == ".ts" and item.name != "index.ts":
                    # Phai bat dau bang "use"
                    if not item.stem.startswith("use"):
                        violations_found = True
                        self.report.violations.append(Violation(
                            rule="naming_convention",
                            message=f"Hook '{item.name}' khong bat dau bang 'use'",
                            severity=Severity.ERROR,
                            path=str(item),
                            suggestion=f"Doi ten thanh 'use{item.stem.title()}.ts'"
                        ))
        
        if not violations_found:
            self.report.passed += 1
        else:
            self.report.failed += 1
    
    def _check_file_sizes(self):
        """Kiem tra kich thuoc file."""
        large_files = []
        
        for file_path in self.screen_path.rglob("*.tsx"):
            try:
                line_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
                if line_count > self.MAX_FILE_LINES:
                    large_files.append((file_path, line_count))
            except Exception:
                pass
        
        for file_path in self.screen_path.rglob("*.ts"):
            if file_path.name == "index.ts":
                continue
            try:
                line_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
                if line_count > self.MAX_FILE_LINES:
                    large_files.append((file_path, line_count))
            except Exception:
                pass
        
        if not large_files:
            self.report.passed += 1
        else:
            self.report.failed += 1
            for file_path, line_count in large_files:
                self.report.violations.append(Violation(
                    rule="file_size_limit",
                    message=f"File '{file_path.name}' qua lon ({line_count} lines > {self.MAX_FILE_LINES})",
                    severity=Severity.WARNING,
                    path=str(file_path),
                    suggestion="Tach file thanh cac module nho hon hoac tao thu muc rieng"
                ))
    
    def _check_barrel_exports(self):
        """Kiem tra barrel exports (index.ts)."""
        missing_barrels = []
        
        for subdir in ["components", "hooks", "types"]:
            dir_path = self.screen_path / subdir
            if dir_path.exists() and dir_path.is_dir():
                index_file = dir_path / "index.ts"
                if not index_file.exists():
                    missing_barrels.append(subdir)
        
        if not missing_barrels:
            self.report.passed += 1
        else:
            for subdir in missing_barrels:
                self.report.violations.append(Violation(
                    rule="barrel_exports",
                    message=f"Thieu index.ts trong {subdir}/",
                    severity=Severity.INFO,
                    path=str(self.screen_path / subdir),
                    suggestion=f"Tao {subdir}/index.ts de export tap trung cac modules"
                ))


def format_report_text(report: ScreenReport) -> str:
    """Format bao cao dang text."""
    lines = [
        f"\n📊 Screen Structure Report: {report.name}",
        "=" * 50,
        f"\n{report.status} ({report.score} rules passed)",
        ""
    ]
    
    if report.violations:
        lines.append("📋 Chi tiet:")
        for v in report.violations:
            icon = "❌" if v.severity == Severity.ERROR else "⚠️" if v.severity == Severity.WARNING else "💡"
            lines.append(f"  {icon} [{v.rule}] {v.message}")
            if v.suggestion:
                lines.append(f"     → {v.suggestion}")
    else:
        lines.append("✨ Khong co van de nao duoc phat hien!")
    
    return "\n".join(lines)


def format_report_json(report: ScreenReport) -> str:
    """Format bao cao dang JSON."""
    data = {
        "name": report.name,
        "path": report.path,
        "status": "pass" if report.failed == 0 else "fail",
        "score": report.score,
        "passed": report.passed,
        "failed": report.failed,
        "violations": [
            {
                "rule": v.rule,
                "message": v.message,
                "severity": v.severity.value,
                "path": v.path,
                "suggestion": v.suggestion
            }
            for v in report.violations
        ]
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def check_all_screens(screens_dir: str) -> List[ScreenReport]:
    """Kiem tra tat ca screens trong thu muc."""
    reports = []
    screens_path = Path(screens_dir)
    
    for item in screens_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            checker = ScreenStructureChecker(str(item))
            reports.append(checker.check_all())
    
    return reports


def main():
    parser = argparse.ArgumentParser(
        description="Kiem tra cau truc thu muc screens"
    )
    parser.add_argument(
        "path",
        help="Duong dan den screen hoac thu muc screens"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Kiem tra tat ca screens trong thu muc"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Xuat ket qua dang JSON"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"❌ Duong dan khong ton tai: {args.path}")
        sys.exit(1)
    
    if args.all:
        reports = check_all_screens(args.path)
        if args.json:
            all_reports = [json.loads(format_report_json(r)) for r in reports]
            print(json.dumps(all_reports, indent=2, ensure_ascii=False))
        else:
            for report in reports:
                print(format_report_text(report))
            
            # Summary
            total_pass = sum(1 for r in reports if r.failed == 0)
            print(f"\n{'='*50}")
            print(f"📊 TONG KET: {total_pass}/{len(reports)} screens dat chuan")
    else:
        checker = ScreenStructureChecker(args.path)
        report = checker.check_all()
        
        if args.json:
            print(format_report_json(report))
        else:
            print(format_report_text(report))
    
    # Exit code
    if args.all:
        sys.exit(0 if all(r.failed == 0 for r in reports) else 1)
    else:
        sys.exit(0 if report.failed == 0 else 1)


if __name__ == "__main__":
    main()
