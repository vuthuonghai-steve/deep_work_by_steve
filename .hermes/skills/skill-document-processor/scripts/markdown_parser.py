#!/usr/bin/env python3
"""
Markdown Parser - Clean and structure markdown files
"""

import re
from pathlib import Path


class MarkdownParser:
    """Parse and clean markdown files"""

    def parse(self, input_path):
        """Read and clean markdown content"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Clean markdown
            cleaned = self._clean_markdown(content)

            return {
                'success': True,
                'content': cleaned,
                'tool': 'markdown-parser'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Markdown parsing failed: {str(e)}'
            }

    def _clean_markdown(self, content):
        """Clean markdown content"""
        lines = content.split('\n')
        cleaned_lines = []
        in_code_block = False

        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                cleaned_lines.append(line)
                continue

            # Preserve code blocks as-is
            if in_code_block:
                cleaned_lines.append(line)
                continue

            # Remove excessive whitespace
            if line.strip():
                cleaned_lines.append(line.rstrip())

        return '\n'.join(cleaned_lines)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: markdown_parser.py <input.md>")
        sys.exit(1)

    parser = MarkdownParser()
    result = parser.parse(sys.argv[1])

    if result['success']:
        print(result['content'])
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
