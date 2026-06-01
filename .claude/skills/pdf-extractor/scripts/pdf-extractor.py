#!/usr/bin/env python3
"""
PDF Extractor — Extract text and structure from PDF documents.
Runs in sandboxed environment with OCR fallback.
"""

import argparse
import sys
import os
import re
from pathlib import Path

# Try imports, handle gracefully if dependencies missing
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class PDFExtractor:
    """Extract text from PDF with sandboxed execution."""
    
    def __init__(self, input_path: str, output_path: str = None, sandboxed: bool = True):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else None
        self.sandboxed = sandboxed
        self.errors = []
        self.warnings = []
        self.ocr_applied = False
        self.confidence = 100
        
    def extract_with_pdftotext(self) -> str:
        """Extract using poppler pdftotext command."""
        import subprocess
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(self.input_path), "-"],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            return ""
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return ""
            
    def extract_with_pypdf(self) -> str:
        """Extract using pypdf library."""
        if not PYPDF_AVAILABLE:
            self.warnings.append("pypdf not available")
            return ""
            
        try:
            reader = PdfReader(str(self.input_path))
            texts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
            return "\n\n".join(texts)
        except Exception as e:
            self.warnings.append(f"pypdf extraction failed: {e}")
            return ""
            
    def extract_with_ocr(self) -> str:
        """Fallback to Tesseract OCR for scanned PDFs."""
        if not OCR_AVAILABLE:
            self.warnings.append("Tesseract OCR not available")
            return ""
            
        try:
            images = convert_from_path(str(self.input_path), dpi=300)
            texts = []
            for image in images:
                text = pytesseract.image_to_string(image, lang='eng+unicode')
                texts.append(text)
            self.ocr_applied = True
            self.confidence = 65  # OCR typically lower confidence
            return "\n\n".join(texts)
        except Exception as e:
            self.warnings.append(f"OCR extraction failed: {e}")
            return ""
            
    def is_encrypted(self) -> bool:
        """Check if PDF is encrypted."""
        if not PYPDF_AVAILABLE:
            return False
        try:
            reader = PdfReader(str(self.input_path))
            return reader.is_encrypted
        except Exception:
            return False
            
    def normalize_text(self, text: str) -> str:
        """Normalize extracted text to Markdown."""
        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        
        # Fix multiple blank lines (max 2)
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        # Normalize Unicode
        text = text.encode('utf-8', errors='replace').decode('utf-8')
        
        # Preserve code blocks (heuristic: monospace lines)
        lines = text.split("\n")
        result = []
        in_code_block = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("    ") or "\t" in line:
                if not in_code_block:
                    result.append("```")
                    in_code_block = True
                result.append(line)
            else:
                if in_code_block:
                    result.append("```")
                    in_code_block = False
                result.append(line)
                
        if in_code_block:
            result.append("```")
            
        return "\n".join(result)
        
    def extract(self) -> str:
        """Main extraction with fallback chain."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.input_path}")
            
        # Check encryption
        if self.is_encrypted():
            return "[ENCRYPTED]\n\nThis PDF is password-protected and cannot be processed."
            
        # Fallback chain: pdftotext -> pypdf -> OCR
        text = self.extract_with_pdftotext()
        
        if not text.strip():
            text = self.extract_with_pypdf()
            
        if not text.strip():
            text = self.extract_with_ocr()
            
        if not text.strip():
            raise ValueError("All extraction methods failed")
            
        return self.normalize_text(text)
        
    def save(self, content: str):
        """Save output to file."""
        output = self.output_path or self.input_path.with_suffix(".md")
        
        # Prepend markers if OCR was applied
        preamble = []
        if self.ocr_applied:
            preamble.append("[OCR_APPLIED]")
        if self.warnings:
            preamble.append(f"[WARNINGS: {'; '.join(self.warnings)}]")
            
        full_content = "\n".join(preamble + [content]) if preamble else content
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        return str(output)


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF to Markdown")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output Markdown file path")
    parser.add_argument("--no-sandbox", action="store_true", help="Disable sandbox mode")
    
    args = parser.parse_args()
    
    extractor = PDFExtractor(
        input_path=args.input,
        output_path=args.output,
        sandboxed=not args.no_sandbox
    )
    
    try:
        content = extractor.extract()
        output_path = extractor.save(content)
        print(f"Extracted to: {output_path}")
        if extractor.warnings:
            print(f"Warnings: {'; '.join(extractor.warnings)}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
