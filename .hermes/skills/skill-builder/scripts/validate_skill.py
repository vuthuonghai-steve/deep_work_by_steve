import os
import sys
import re
import json
from datetime import datetime

class SkillValidator:
    """
    Kỹ sư thẩm định chất lượng Agent Skill.
    Đảm bảo tính chính trực giữa thiết kế (design) và thực thi (build).
    """
    def __init__(self, skill_path: str, design_path: str | None = None, log_mode: bool = False, strict_context: bool = False):
        self.skill_path: str = os.path.abspath(skill_path)
        self.skill_name: str = os.path.basename(self.skill_path.rstrip('/'))
        self.design_path: str | None = os.path.abspath(design_path) if design_path else None
        self.log_mode: bool = log_mode
        self.strict_context: bool = strict_context
        self.workspace_root: str = self.find_workspace_root()
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.reports: list[str] = []

    def find_workspace_root(self) -> str:
        """
        Return the project workspace root (parent of .skill-context/{skill_name}).
        Strategy:
        1. Walk up from skill_path for .skill-context/{skill_name}, return its parent.
        2. Use design_path parent if provided (common OMC layout).
        3. Fallback to three-level-up from skill_path.
        """
        # Strategy 1: walk up from skill_path — return PARENT of the context dir
        current = self.skill_path
        for _ in range(12):
            marker = os.path.join(current, ".skill-context", self.skill_name)
            if os.path.isdir(marker):
                # marker is .skill-context/{skill_name}, its parent is the project root
                return current
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent

        # Strategy 2: design_path ends in .skill-context/{skill_name}/design.md.
        # We need the project root (two levels up).
        if self.design_path and os.path.isabs(self.design_path):
            # design_path: /project/.skill-context/{skill_name}/design.md
            # step 1: parent = /project/.skill-context/{skill_name}
            # step 2: parent = /project/.skill-context  ← NOT what we want
            # step 3: parent = /project                ← project root = .skill-context grandparent
            sc = self.design_path
            for _ in range(5):
                parent = os.path.dirname(sc)
                if os.path.basename(parent) == '.skill-context' or parent == '/':
                    break
                sc = parent
            return os.path.dirname(parent) if os.path.basename(parent) == '.skill-context' else parent

        # Strategy 3: fallback
        return os.path.dirname(os.path.dirname(os.path.dirname(self.skill_path)))

    def log(self, message, level="INFO"):
        prefix = f"[{level}] " if level != "INFO" else ""
        formatted_message = f"{prefix}{message}"
        self.reports.append(formatted_message)
        print(formatted_message)

    def check_structure(self):
        self.log("1. Checking 4 Zones Structural Integrity...")
        # Core zones: SKILL.md + knowledge + loop are mandatory; scripts is optional
        core_zones = ["SKILL.md", "knowledge", "loop"]
        all_zones = core_zones + ["scripts"]
        passed = True
        for zone in all_zones:
            path = os.path.join(self.skill_path, zone)
            if not os.path.exists(path):
                if zone in core_zones:
                    self.errors.append(f"[E01] CRITICAL: Missing mandatory zone: {zone}")
                    passed = False
                else:
                    self.warnings.append(f"[W01] WARNING: Missing optional zone: {zone}")
        return passed

    def check_skill_md_constraints(self):
        skill_md_path = os.path.join(self.skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path): return False
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = "".join(lines)
        
        self.log(f"2. Analyzing SKILL.md (Lines: {len(lines)})")
        
        if len(lines) > 500:
            self.errors.append(f"[E03] ERROR: SKILL.md exceeds 500 lines limit ({len(lines)})")

        mandatory_keywords = ["## Persona", "Workflow", "Guardrails"]
        for kw in mandatory_keywords:
            if kw not in content:
                self.errors.append(f"[E04] ERROR: SKILL.md missing mandatory section keyword: '{kw}'")
        
        return len(self.errors) == 0

    def check_pd_links(self):
        self.log("3. Progressive Disclosure (PD) Integrity Check...")
        skill_md_path = os.path.join(self.skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path): return False
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tier2_files = []
        for root, _, files in os.walk(self.skill_path):
            rel_root = os.path.relpath(root, self.skill_path)
            if any(rel_root.startswith(z) for z in ["knowledge", "scripts", "loop"]):
                for file in files:
                    if not file.startswith('.'):
                        rel_path = os.path.normpath(os.path.join(rel_root, file))
                        tier2_files.append(rel_path)

        orphan_count = 0
        for f_path in tier2_files:
            # Pattern: [Label](path) - must use markdown link as per User's request
            regex_path = re.escape(f_path)
            pattern = rf"\[.*\]\(.*{regex_path}.*\)"
            if not re.search(pattern, content):
                self.warnings.append(f"WARNING: Orphan file detected: '{f_path}' is not linked in SKILL.md via Markdown link.")
                self.log(f"   -> Orphan (Missing MD Link): {f_path}", "WARN")
                orphan_count += 1
        
        return orphan_count == 0

    def check_file_mapping(self):
        design_file = self.design_path
        if not design_file:
            # Policy High: Design path is required if provided in arguments
            return True
            
        if not os.path.exists(design_file):
            self.errors.append(f"[E06] CRITICAL: Design file not found at {design_file}")
            self.log(f"   -> Design not found: {design_file}", "FAIL")
            return False

        self.log(f"4. File Mapping (Actual vs Design §3) Check...")
        with open(design_file, 'r', encoding='utf-8') as f:
            design_content = f.read()

        expected_files: set[str] = set()
        # Parse from Zone Mapping table
        lines = design_content.split('\n')
        in_zone_mapping = False
        for line in lines:
            if '## 3. Zone Mapping' in line:
                in_zone_mapping = True
            elif in_zone_mapping and line.startswith('##'):
                if '## 3.' not in line: # Another section started
                    in_zone_mapping = False
            
            if in_zone_mapping:
                # Find file paths in backticks like `knowledge/architect.md`
                matches = re.findall(r"`([a-zA-Z0-9_\-\./]+\.[a-z]{2,4})`", line)
                for m in matches:
                    if "/" in m or m == "SKILL.md":
                        expected_files.add(os.path.normpath(m))
        
        # Ensure SKILL.md is expected
        expected_files.add("SKILL.md")

        actual_files: set[str] = set()
        for root, _, files in os.walk(self.skill_path):
            rel_root = os.path.relpath(root, self.skill_path)
            for file in files:
                if not file.startswith('.'):
                    rel_path = os.path.normpath(os.path.join(rel_root, file)) if rel_root != "." else file
                    actual_files.add(rel_path)

        missing = expected_files - actual_files
        # Exclude loop/build-log.md if it's dynamic
        ignore_extra = {"scripts/validate_skill.py", "loop/build-log.md", "loop/build-checklist.md", "templates/cleaned-prompt.xml.template"}
        extra = actual_files - expected_files - ignore_extra

        if missing:
            for f in missing:
                self.errors.append(f"[E02] ERROR: Missing file from design: {f}")
                self.log(f"   -> Missing: {f}", "FAIL")
        
        if extra:
            for f in extra:
                self.warnings.append(f"WARNING: Extra file not in design: {f}")
                self.log(f"   -> Extra: {f}", "WARN")

        return len(missing) == 0

    def check_placeholder_density(self):
        self.log("5. Placeholder Density Check...")
        total_placeholders = 0
        for root, _, files in os.walk(self.skill_path):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        total_placeholders += f.read().count("[MISSING_DOMAIN_DATA]")
        
        self.log(f"   -> Total Placeholders: {total_placeholders}")
        if total_placeholders >= 10:
            self.errors.append(f"[E05] FAIL: High Placeholder Density ({total_placeholders}). >10 is unacceptable.")
        elif total_placeholders >= 5:
            self.warnings.append(f"WARNING: Medium Placeholder Density ({total_placeholders}). Progressing to failure.")
        
        return total_placeholders < 10

    def check_error_handling(self):
        """Logic P0: Kiểm tra tính tuân thủ Error STOP policy"""
        # Look for build-log.md in loop/
        log_path = os.path.join(self.skill_path, "loop", "build-log.md")
        if not os.path.exists(log_path):
            return True
            
        self.log("6. Error Handling Policy Check...")
        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        # If system error occurred but build didn't stop (no final status or more files added)
        # This is a simplified check
        if "ERROR" in log_content.upper() and "Log-Notify-Stop" in log_content:
            self.log("   -> System Error detected in log. Verifying STOP stance.", "INFO")
        return True

    def get_context_dir(self):
        """
        Return .skill-context/{skill_name}.
        workspace_root is the project root (where .skill-context/ lives),
        so join workspace_root + .skill-context + skill_name.
        """
        return os.path.join(self.workspace_root, ".skill-context", self.skill_name)

    def collect_context_critical_files(self):
        """
        Critical coverage contract:
        - design.md, todo.md
        - all files under resources/
        - all files under data/
        """
        context_dir = self.get_context_dir()
        critical: list[str] = []
        if not os.path.isdir(context_dir):
            return critical

        for fixed in ("design.md", "todo.md"):
            fixed_path = os.path.join(context_dir, fixed)
            if os.path.isfile(fixed_path):
                critical.append(fixed)

        for rel_root in ("resources", "data"):
            root_dir = os.path.join(context_dir, rel_root)
            if not os.path.isdir(root_dir):
                continue
            for root, _, files in os.walk(root_dir):
                for name in files:
                    if name.startswith("."):
                        continue
                    full = os.path.join(root, name)
                    rel = os.path.relpath(full, context_dir)
                    critical.append(rel.replace("\\", "/"))

        # Stable ordering for deterministic validation output
        return sorted(set(critical))

    def check_context_resource_coverage(self):
        """
        Verify builder actually captured context usage in .skill-context/{skill-name}/build-log.md.
        """
        self.log("7. Context Resource Coverage Check...")
        context_dir = self.get_context_dir()
        if not os.path.isdir(context_dir):
            self.warnings.append(f"WARNING: Context directory not found for coverage check: {context_dir}")
            self.log(f"   -> Missing context dir: {context_dir}", "WARN")
            return True

        build_log = os.path.join(context_dir, "build-log.md")
        if not os.path.isfile(build_log):
            code = "[E07]" if self.strict_context else "[W07]"
            msg = f"{code} {'ERROR' if self.strict_context else 'WARNING'}: Missing context build log required for coverage: {build_log}"
            (self.errors if self.strict_context else self.warnings).append(msg)
            self.log(f"   -> Missing build-log: {build_log}", "FAIL")
            return not self.strict_context

        with open(build_log, "r", encoding="utf-8") as f:
            build_log_content = f.read()

        for section in ("## Resource Inventory", "## Resource Usage Matrix"):
            if section not in build_log_content:
                code = "[E08]" if self.strict_context else "[W08]"
                msg = f"{code} {'ERROR' if self.strict_context else 'WARNING'}: build-log.md missing mandatory section '{section}'"
                (self.errors if self.strict_context else self.warnings).append(msg)
                self.log(f"   -> Missing section: {section}", "FAIL")

        critical_files = self.collect_context_critical_files()
        if not critical_files:
            self.warnings.append(
                "WARNING: No critical context files detected (design/todo/resources/data)."
            )
            self.log("   -> No critical context files detected.", "WARN")
            return len(self.errors) == 0

        uncovered = []
        for rel in critical_files:
            rel_norm = rel.replace("\\", "/")
            full_norm = os.path.join(context_dir, rel).replace("\\", "/")
            if rel_norm not in build_log_content and full_norm not in build_log_content:
                uncovered.append(rel_norm)

        if uncovered:
            for rel in uncovered:
                code = "[E09]" if self.strict_context else "[W09]"
                msg = f"{code} {'ERROR' if self.strict_context else 'WARNING'}: Critical context resource has no usage evidence in build-log.md: {rel}"
                (self.errors if self.strict_context else self.warnings).append(msg)
                self.log(f"   -> Uncovered critical resource: {rel}", "FAIL")
        else:
            self.log(
                f"   -> Coverage OK: {len(critical_files)}/{len(critical_files)} critical resources traced.",
                "INFO",
            )

        return len(uncovered) == 0 if self.strict_context else True

    def check_fidelity_heuristics(self):
        """
        Check for potential summarization by comparing line counts between sources and targets.
        """
        self.log("8. Fidelity Heuristics Check...")
        context_dir = self.get_context_dir()
        build_log_path = os.path.join(context_dir, "build-log.md")
        if not os.path.isfile(build_log_path):
            return True

        with open(build_log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        # Extract Resource Usage Matrix rows (support multi-file sources)
        # Format: | `resources/...` | Target | Notes | OR | Source | Target | Notes |
        # Multi-file case: part-a + part-b → knowledge/claude-code-prompt-patterns.md
        matrix_rows = re.findall(r'\|\s*`([^`]+)`\s*\|\s*Critical\s*\|\s*[^\|]+\|(?:\s*`([^`]+)`\s*\|)?', log_content)
        
        for source_rel, target_rel in matrix_rows:
            if not target_rel: continue
            
            source_path = os.path.join(context_dir, source_rel)
            target_path = os.path.join(self.skill_path, target_rel)
            
            if os.path.isfile(source_path) and os.path.isfile(target_path):
                with open(source_path, 'r', encoding='utf-8') as fs:
                    source_lines = len(fs.readlines())
                with open(target_path, 'r', encoding='utf-8') as ft:
                    target_lines = len(ft.readlines())
                
                # If target is less than 60% of source and source is significant (> 50 lines)
                if source_lines > 50 and target_lines < source_lines * 0.6:
                    self.warnings.append(f"FIDELITY WARNING: '{target_rel}' is significantly shorter than its source '{source_rel}' ({target_lines} vs {source_lines} lines). Potential summarization detected.")
                    self.log(f"   -> Potential summarization: {target_rel} ({target_lines} lines) vs {source_rel} ({source_lines} lines)", "WARN")
                else:
                    self.log(f"   -> Fidelity OK: {target_rel} maintains healthy ratio to {source_rel}.", "INFO")
        
        return True

    def report(self):
        print("\n" + "="*50)
        print("   AGENT SKILL VALIDATION REPORT")
        print(f"   Target: {self.skill_name}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        self.check_structure()
        self.check_skill_md_constraints()
        self.check_pd_links()
        self.check_file_mapping()
        self.check_placeholder_density()
        self.check_error_handling() # Fix Medium: Call checking error handling
        self.check_context_resource_coverage()
        self.check_fidelity_heuristics()
        
        print("="*50)
        final_status = "PASS" if not self.errors else "FAIL"
        if self.warnings and final_status == "PASS":
            final_status = "PASS (With Warnings)"
            
        print(f"FINAL STATUS: {final_status}")
        
        if self.log_mode:
            self.write_log(final_status)
            
        if self.errors:
            sys.exit(1)
        sys.exit(0)

    def write_log(self, status):
        """Append validation result to build-log.md in .skill-context/{skill-name}/"""
        target_log_path = os.path.join(
            self.workspace_root, ".skill-context", self.skill_name, "build-log.md"
        )

        if not os.path.exists(target_log_path):
            self.log(f"Warning: Build log not found at {target_log_path}", "WARN")
            return

        with open(target_log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## Validation Result ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write(f"- **Final Status**: {status}\n")
            f.write(f"- **Errors**: {len(self.errors)}\n")
            f.write(f"- **Warnings**: {len(self.warnings)}\n")
            if self.errors:
                f.write("### Issues Found:\n")
                for err in self.errors:
                    f.write(f"- [FAILED] {err}\n")
            self.log(f"Results appended to {target_log_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the skill directory")
    parser.add_argument("--design", help="Path to design.md")
    parser.add_argument("--log", action="store_true", help="Append results to build-log.md")
    parser.add_argument(
        "--strict-context",
        action="store_true",
        help="Fail validation if context resource coverage in .skill-context/{skill-name}/build-log.md is incomplete",
    )
    args = parser.parse_args()
    
    validator = SkillValidator(
        args.path,
        design_path=args.design,
        log_mode=args.log,
        strict_context=args.strict_context,
    )
    validator.report()
