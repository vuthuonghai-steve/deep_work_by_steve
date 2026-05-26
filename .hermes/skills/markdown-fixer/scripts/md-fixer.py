#!/usr/bin/env python3
"""
Markdown Fixer — Fix Markdown structure issues.
Fixes heading hierarchy, list indentation, code blocks, and tables.
"""

import argparse
import sys
import re
from pathlib import Path


class MarkdownFixer:
    """Fix Markdown structural issues."""
    
    def __init__(self, input_path: str, output_path: str = None):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else None
        self.warnings = []
        self.fixes_applied = []
        
    def fix_headings(self, text: str) -> str:
        """Fix heading hierarchy issues."""
        lines = text.split('\n')
        result = []
        current_h1_count = 0
        last_level = 0
        
        for line in lines:
            # Match ATX headings
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                content = match.group(2).rstrip()
                
                # Track if we have h1
                if level == 1:
                    current_h1_count += 1
                    
                # Check for skipped levels (e.g., h1 -> h4)
                if level > last_level + 1 and last_level > 0:
                    self.fixes_applied.append(f"heading_skip: h{last_level} -> h{level}")
                    # Don't auto-fix, just warn
                    
                last_level = level
                result.append(f"{'#' * level} {content}")
            else:
                result.append(line)
                
        return '\n'.join(result)
        
    def fix_list_indentation(self, text: str) -> str:
        """Fix list item indentation (2 spaces per level)."""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Match list items
            list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', line)
            if list_match:
                indent = list_match.group(1)
                marker = list_match.group(2)
                content = list_match.group(3)
                
                # Count leading spaces
                leading_spaces = len(indent)
                
                # Check for incorrect nesting (should be multiples of 2)
                if leading_spaces % 2 != 0 and leading_spaces > 0:
                    # Fix: round to nearest even number
                    fixed_indent = leading_spaces + (leading_spaces % 2)
                    self.fixes_applied.append(f"list_indent: {leading_spaces} -> {fixed_indent}")
                    leading_spaces = fixed_indent
                    
                result.append(' ' * leading_spaces + marker + ' ' + content)
            else:
                result.append(line)
                
        return '\n'.join(result)
        
    def fix_code_blocks(self, text: str) -> str:
        """Fix code block formatting."""
        lines = text.split('\n')
        result = []
        in_code_block = False
        code_block_start = -1
        
        for i, line in enumerate(lines):
            # Check for indented code blocks (4+ spaces)
            if not in_code_block and (line.startswith('    ') or line.startswith('\t')):
                # Convert to fenced code block
                if result and result[-1].strip():
                    self.fixes_applied.append("code_block: indented -> fenced")
                    result.append('```')
                result.append(line[4:] if line.startswith('    ') else line[1:])
                in_code_block = True
                code_block_start = i
            elif in_code_block:
                if line.startswith('    ') or line.startswith('\t'):
                    result.append(line[4:] if line.startswith('    ') else line[1:])
                elif not line.strip():
                    result.append(line)
                else:
                    # End of indented code block
                    result.append('```')
                    result.append(line)
                    in_code_block = False
            else:
                result.append(line)
                
        if in_code_block:
            result.append('```')
            
        return '\n'.join(result)
        
    def fix_tables(self, text: str) -> str:
        """Fix table formatting to GFM standard."""
        lines = text.split('\n')
        result = []
        in_table = False
        table_lines = []
        
        for line in lines:
            # Detect table start (has | characters)
            if '|' in line and not in_table:
                # Check if previous line or this line looks like a table
                if re.search(r'\|.*\|', line):
                    in_table = True
                    table_lines = [line]
                else:
                    result.append(line)
            elif in_table:
                if '|' in line:
                    table_lines.append(line)
                else:
                    # End of table
                    fixed_table = self._fix_table_rows(table_lines)
                    result.extend(fixed_table)
                    result.append('')
                    in_table = False
                    table_lines = []
                    result.append(line)
            else:
                result.append(line)
                
        if table_lines:
            fixed_table = self._fix_table_rows(table_lines)
            result.extend(fixed_table)
            
        return '\n'.join(result)
        
    def _fix_table_rows(self, rows: list[str]) -> list[str]:
        """Fix a single table's formatting."""
        if not rows:
            return []
            
        result = []
        
        # First row is header
        if len(rows) == 1:
            # Just header, add divider
            header = rows[0].strip()
            if header.endswith('|'):
                header = header[:-1]
            cols = [c.strip() for c in header.split('|')]
            result.append('| ' + ' | '.join(cols) + ' |')
            result.append('|' + '|'.join([' --- '] * len(cols)) + '|')
        else:
            # Has header and data rows
            header = rows[0].strip()
            if header.endswith('|'):
                header = header[:-1]
            cols = [c.strip() for c in header.split('|')]
            result.append('| ' + ' | '.join(cols) + ' |')
            
            # Check second row for delimiter
            if not re.match(r'^\|?\s*[:\-]+\s*\|', rows[1]):
                # Add delimiter row
                result.append('|' + '|'.join([' --- '] * len(cols)) + '|')
                data_rows = rows[1:]
            else:
                # Delimiter exists, normalize it
                result.append(self._normalize_delimiter(rows[1]))
                data_rows = rows[2:]
                
            # Process data rows
            for row in data_rows:
                row = row.strip()
                if row.endswith('|'):
                    row = row[:-1]
                cells = [c.strip() for c in row.split('|')]
                # Ensure same number of cells
                while len(cells) < len(cols):
                    cells.append('')
                result.append('| ' + ' | '.join(cells[:len(cols)]) + ' |')
                
        return result
        
    def _normalize_delimiter(self, row: str) -> str:
        """Normalize table delimiter row."""
        row = row.strip()
        if row.startswith('|'):
            row = row[1:]
        if row.endswith('|'):
            row = row[:-1]
            
        cols = row.split('|')
        normalized = []
        for col in cols:
            col = col.strip()
            if ':' in col:
                # Has alignment
                normalized.append(col)
            else:
                normalized.append('---')
                
        return '| ' + ' | '.join(normalized) + ' |'
        
    def fix_blockquotes(self, text: str) -> str:
        """Fix blockquote formatting."""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Count > symbols
            count = 0
            for ch in line:
                if ch == '>':
                    count += 1
                else:
                    break
                    
            if count > 0:
                content = line[count:].strip()
                # Ensure space after >
                result.append('> ' * count + content)
            else:
                result.append(line)
                
        return '\n'.join(result)
        
    def fix_emphasis(self, text: str) -> str:
        """Fix emphasis markers to standard."""
        # Prefer * over _ for emphasis
        # This is a simple version - complex regex would be needed for full implementation
        return text
        
    def fix_horizontal_rules(self, text: str) -> str:
        """Fix horizontal rules to standard ---."""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            stripped = line.strip()
            if re.match(r'^[-*_]{3,}$', stripped):
                result.append('---')
            else:
                result.append(line)
                
        return '\n'.join(result)
        
    def fix(self) -> str:
        """Main fixing pipeline."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
            
        with open(self.input_path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
            
        if not text.strip():
            raise ValueError("Empty Markdown input")
            
        # Fix pipeline
        text = self.fix_headings(text)
        text = self.fix_lists(text)
        text = self.fix_code_blocks(text)
        text = self.fix_tables(text)
        text = self.fix_blockquotes(text)
        text = self.fix_horizontal_rules(text)
        
        # Final cleanup
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text
        
    def fix_lists(self, text: str) -> str:
        """Fix list formatting (separate method for clarity)."""
        return self.fix_list_indentation(text)
        
    def save(self, content: str):
        """Save output to file."""
        output = self.output_path or self.input_path.with_suffix(".fixed.md")
        
        # Prepend fixes summary
        preamble = []
        if self.fixes_applied:
            unique_fixes = list(set(self.fixes_applied))
            preamble.append(f"[FIXES: {', '.join(unique_fixes)}]")
            
        full_content = "\n".join(preamble + [content]) if preamble else content
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        return str(output)


def main():
    parser = argparse.ArgumentParser(description="Fix Markdown structure issues")
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("-o", "--output", help="Output Markdown file path")
    
    args = parser.parse_args()
    
    fixer = MarkdownFixer(
        input_path=args.input,
        output_path=args.output
    )
    
    try:
        content = fixer.fix()
        output_path = fixer.save(content)
        print(f"Fixed Markdown: {output_path}")
        if fixer.fixes_applied:
            print(f"Fixes applied: {', '.join(set(fixer.fixes_applied))}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
