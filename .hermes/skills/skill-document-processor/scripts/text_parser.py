#!/usr/bin/env python3
"""
Text Parser - Convert plain text to structured markdown
"""

import re
from pathlib import Path


class TextParser:
    """Parse and convert plain text files"""

    def parse(self, input_path):
        """Read and convert text to markdown"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert to markdown
            markdown = self._text_to_markdown(content)

            return {
                'success': True,
                'content': markdown,
                'tool': 'text-parser'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Text parsing failed: {str(e)}'
            }

    def _text_to_markdown(self, content):
        """Convert plain text to markdown structure"""
        lines = content.split('\n')
        result_lines = []
        current_section = None

        for line in lines:
            stripped = line.strip()

            # Empty lines
            if not stripped:
                result_lines.append('')
                continue

            # Detect headers (ALL CAPS or numbered patterns)
            if self._is_header(stripped):
                level = self._header_level(stripped)
                clean_header = self._clean_header(stripped)
                result_lines.append(f"{'#' * level} {clean_header}")
                current_section = clean_header
                continue

            # Detect list items
            if self._is_list_item(stripped):
                result_lines.append(f"- {stripped}")
                continue

            # Regular text
            result_lines.append(stripped)

        return '\n'.join(result_lines)

    def _is_header(self, line):
        """Check if line is a header"""
        # ALL CAPS pattern
        if line.isupper() and len(line) > 3:
            return True
        # Numbered pattern like "1. Title" or "1.1 Title"
        if re.match(r'^\d+(\.\d+)*\.\s+\S', line):
            return True
        return False

    def _header_level(self, line):
        """Determine header level"""
        if re.match(r'^\d+\.\d+\.', line):
            return 3
        elif re.match(r'^\d+\.', line):
            return 2
        return 1

    def _clean_header(self, line):
        """Clean header text"""
        # Remove numbering
        cleaned = re.sub(r'^\d+(\.\d+)*\.\s+', '', line)
        # Title case
        return cleaned.title()

    def _is_list_item(self, line):
        """Check if line is a list item"""
        patterns = [
            r'^[-*+]\s+',      # - * +
            r'^\d+\.\s+',       # 1. 2.
            r'^[a-z]\)\s+',     # a) b)
            r'^[A-Z]\)\s+',     # A) B)
        ]
        return any(re.match(p, line) for p in patterns)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: text_parser.py <input.txt>")
        sys.exit(1)

    parser = TextParser()
    result = parser.parse(sys.argv[1])

    if result['success']:
        print(result['content'])
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
