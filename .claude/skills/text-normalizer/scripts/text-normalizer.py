#!/usr/bin/env python3
"""
Text Normalizer — Standardize plain text to clean Markdown format.
Normalizes encoding, line endings, and whitespace.
"""

import argparse
import sys
import re
from pathlib import Path


class TextNormalizer:
    """Normalize plain text with encoding and whitespace standardization."""
    
    def __init__(self, input_path: str, output_path: str = None):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else None
        self.warnings = []
        
    def detect_encoding(self, raw_bytes: bytes) -> tuple[str, str]:
        """Detect file encoding."""
        # Try common encodings in order of preference
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                decoded = raw_bytes.decode(encoding)
                # Check for null bytes which indicate binary
                if '\x00' in decoded:
                    continue
                return encoding, decoded
            except (UnicodeDecodeError, LookupError):
                continue
                
        # Fallback: decode with replacement
        return 'utf-8', raw_bytes.decode('utf-8', errors='replace')
        
    def normalize_encoding(self, text: str) -> str:
        """Normalize to UTF-8."""
        # Replace common problematic characters
        replacements = {
            '\u2018': "'",  # Left single quote
            '\u2019': "'",  # Right single quote
            '\u201c': '"',  # Left double quote
            '\u201d': '"',  # Right double quote
            '\u2013': '-',  # En dash
            '\u2014': '--', # Em dash
            '\xa0': ' ',    # Non-breaking space
            '\u200b': '',   # Zero-width space
            '\ufeff': '',   # BOM
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        return text
        
    def normalize_line_endings(self, text: str) -> str:
        """Convert all line endings to Unix style."""
        # First convert Windows (\r\n) and old Mac (\r)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        return text
        
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving structure."""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Collapse multiple spaces to one
            line = re.sub(r' +', ' ', line)
            # Trim trailing whitespace
            line = line.rstrip()
            result.append(line)
            
        # Collapse multiple blank lines (max 2 consecutive)
        text = '\n'.join(result)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text
        
    def detect_code_blocks(self, text: str) -> str:
        """Detect and preserve code blocks (heuristic)."""
        lines = text.split('\n')
        result = []
        in_code_block = False
        
        for line in lines:
            # Detect code block markers
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                else:
                    in_code_block = False
                result.append(line)
            elif line.startswith('    ') or line.startswith('\t'):
                # Indented code lines
                if not in_code_block:
                    result.append('```')
                    in_code_block = True
                result.append(line)
            else:
                if in_code_block and line.strip():
                    # Check if we should close
                    result.append(line)
                elif in_code_block:
                    result.append('```')
                    in_code_block = False
                    result.append(line)
                else:
                    result.append(line)
                    
        if in_code_block:
            result.append('```')
            
        return '\n'.join(result)
        
    def add_paragraph_breaks(self, text: str) -> str:
        """Ensure proper paragraph separation."""
        # Split into paragraphs (double newlines or single significant breaks)
        # Then rejoin with proper spacing
        lines = text.split('\n')
        result = []
        paragraph = []
        
        for line in lines:
            stripped = line.strip()
            if stripped:
                paragraph.append(line)
            else:
                if paragraph:
                    result.append('\n'.join(paragraph))
                    result.append('')
                    paragraph = []
                    
        if paragraph:
            result.append('\n'.join(paragraph))
            
        return '\n'.join(result)
        
    def normalize(self) -> str:
        """Main normalization pipeline."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
            
        # Read raw bytes
        with open(self.input_path, 'rb') as f:
            raw_bytes = f.read()
            
        # Detect encoding
        encoding, text = self.detect_encoding(raw_bytes)
        if encoding != 'utf-8':
            self.warnings.append(f"Detected encoding: {encoding}")
            
        # Normalization pipeline
        text = self.normalize_line_endings(text)
        text = self.normalize_encoding(text)
        text = self.normalize_whitespace(text)
        text = self.detect_code_blocks(text)
        
        # Ensure trailing newline
        text = text.rstrip('\n') + '\n'
        
        return text
        
    def save(self, content: str):
        """Save output to file."""
        output = self.output_path or self.input_path.with_suffix(".md")
        
        # Prepend warnings
        preamble = []
        if self.warnings:
            preamble.append(f"[WARNINGS: {'; '.join(self.warnings)}]")
            
        full_content = "\n".join(preamble + [content]) if preamble else content
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        return str(output)


def main():
    parser = argparse.ArgumentParser(description="Normalize plain text to clean format")
    parser.add_argument("input", help="Input text file path")
    parser.add_argument("-o", "--output", help="Output file path")
    
    args = parser.parse_args()
    
    normalizer = TextNormalizer(
        input_path=args.input,
        output_path=args.output
    )
    
    try:
        content = normalizer.normalize()
        output_path = normalizer.save(content)
        print(f"Normalized to: {output_path}")
        if normalizer.warnings:
            print(f"Warnings: {'; '.join(normalizer.warnings)}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
