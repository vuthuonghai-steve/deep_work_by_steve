#!/usr/bin/env python3
"""
PDF Parser - Extract text from PDF files
"""

import subprocess
import sys
from pathlib import Path


class PDFParser:
    """Parse PDF files to markdown/text"""

    def __init__(self):
        self.tools = ['marker-pdf', 'pymupdf', 'pdftotext']

    def _get_available_tool(self):
        """Find available PDF tool"""
        for tool in self.tools:
            try:
                result = subprocess.run(
                    ['which', tool],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return tool
            except Exception:
                continue
        return None

    def parse(self, input_path):
        """Extract text from PDF"""
        tool = self._get_available_tool()

        if not tool:
            return {
                'success': False,
                'error': 'No PDF tool available. Install: marker-pdf, pymupdf, or pdftotext'
            }

        try:
            if tool == 'marker-pdf':
                return self._parse_marker(input_path)
            elif tool == 'pymupdf':
                return self._parse_pymupdf(input_path)
            else:
                return self._parse_pdftotext(input_path)
        except Exception as e:
            return {
                'success': False,
                'error': f'PDF parsing failed: {str(e)}'
            }

    def _parse_marker(self, input_path):
        """Parse using marker-pdf"""
        output_dir = Path(input_path).parent
        cmd = [
            'marker-pdf',
            input_path,
            '--output_dir', str(output_dir)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return {
                'success': False,
                'error': f'marker-pdf failed: {result.stderr}'
            }

        # marker-pdf outputs .md file
        md_path = Path(input_path).with_suffix('.md')
        if md_path.exists():
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                'success': True,
                'content': content,
                'tool': 'marker-pdf'
            }

        return {
            'success': False,
            'error': 'marker-pdf did not produce output'
        }

    def _parse_pymupdf(self, input_path):
        """Parse using pymupdf"""
        try:
            import fitz  # pymupdf
        except ImportError:
            return {
                'success': False,
                'error': 'pymupdf not installed'
            }

        doc = fitz.open(input_path)
        text_parts = []

        for page in doc:
            text_parts.append(page.get_text())

        content = '\n\n'.join(text_parts)
        return {
            'success': True,
            'content': content,
            'tool': 'pymupdf'
        }

    def _parse_pdftotext(self, input_path):
        """Parse using pdftotext"""
        cmd = ['pdftotext', '-layout', input_path, '-']
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return {
                'success': False,
                'error': f'pdftotext failed: {result.stderr}'
            }

        return {
            'success': True,
            'content': result.stdout,
            'tool': 'pdftotext'
        }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: pdf_parser.py <input.pdf>")
        sys.exit(1)

    parser = PDFParser()
    result = parser.parse(sys.argv[1])

    if result['success']:
        print(result['content'])
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
