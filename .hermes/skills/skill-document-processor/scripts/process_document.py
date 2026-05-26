#!/usr/bin/env python3
"""
Document Processor Main Script
Process PDF, MD, Text files to CLAUDE.md standard
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.pdf_parser import PDFParser
from scripts.markdown_parser import MarkdownParser
from scripts.text_parser import TextParser


class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {
            '.pdf': 'pdf',
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.txt': 'text',
            '.text': 'text'
        }

    def detect_type(self, file_path):
        """Detect file type by extension"""
        ext = Path(file_path).suffix.lower()
        return self.supported_formats.get(ext, 'unknown')

    def process(self, input_path, output_path=None):
        """Process document based on type"""
        file_type = self.detect_type(input_path)

        if file_type == 'unknown':
            return {
                'success': False,
                'error': f'Unsupported file type: {Path(input_path).suffix}'
            }

        # Select parser
        parsers = {
            'pdf': PDFParser(),
            'markdown': MarkdownParser(),
            'text': TextParser()
        }

        parser = parsers.get(file_type)
        if not parser:
            return {
                'success': False,
                'error': f'No parser for type: {file_type}'
            }

        # Process
        result = parser.parse(input_path)

        if result['success'] and output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result['content'])

        return result


def main():
    parser = argparse.ArgumentParser(
        description='Process documents to CLAUDE.md standard'
    )
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-t', '--type', choices=['pdf', 'md', 'text', 'auto'],
                        default='auto', help='Input type (default: auto)')

    args = parser.parse_args()

    processor = DocumentProcessor()
    result = processor.process(args.input, args.output)

    if result['success']:
        if args.output:
            print(f"✅ Processed: {args.input} -> {args.output}")
        else:
            print(result['content'])
    else:
        print(f"❌ Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
