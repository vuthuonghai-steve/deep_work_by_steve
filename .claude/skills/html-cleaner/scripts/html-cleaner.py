#!/usr/bin/env python3
"""
HTML Cleaner — Convert HTML to semantic Markdown with sanitization.
Strips scripts, styles, and malicious content while preserving structure.
"""

import argparse
import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import Optional

try:
    from bs4 import BeautifulSoup, NavigableString, Comment
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


# Tags to completely remove with all content
FORBIDDEN_TAGS = {
    'script', 'style', 'iframe', 'object', 'embed',
    'form', 'input', 'button', 'select', 'textarea'
}

# Event handler attributes to remove
EVENT_HANDLERS = {
    'onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onblur',
    'onchange', 'onsubmit', 'onkeydown', 'onkeyup', 'onkeypress',
    'onscroll', 'onwheel', 'oncopy', 'oncut', 'onpaste', 'onabort',
    'onblur', 'oncanplay', 'oncanplaythrough', 'oncontextmenu',
    'oncuechange', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter',
    'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange',
    'onemptied', 'onended', 'onerror', 'onfocus', 'oninput', 'oninvalid',
    'onkeydown', 'onkeypress', 'onkeyup', 'onload', 'onloadeddata',
    'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmousemove',
    'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onpause',
    'onplay', 'onplaying', 'onprogress', 'onratechange', 'onreset',
    'onresize', 'onscroll', 'onseeked', 'onseeking', 'onstalled',
    'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle', 'onvolumechange',
    'onwaiting', 'onwheel'
}

# Dangerous URL protocols
DANGEROUS_PROTOCOLS = {'javascript:', 'vbscript:', 'data:'}


class HTMLCleaner:
    """Clean HTML to semantic Markdown with security sanitization."""
    
    def __init__(self, input_path: str, output_path: str = None):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else None
        self.warnings = []
        self.removed_tags = set()
        
    def sanitize_html(self, html: str) -> str:
        """Remove malicious content from HTML."""
        if not BS4_AVAILABLE:
            raise RuntimeError("BeautifulSoup4 required: pip install beautifulsoup4")
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove forbidden tags
        for tag in FORBIDDEN_TAGS:
            elements = soup.find_all(tag)
            if elements:
                self.removed_tags.add(tag)
            for elem in elements:
                elem.decompose()
                
        # Remove comments (can contain malicious content)
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        # Remove event handlers from all tags
        for tag in soup.find_all():
            for attr in list(tag.attrs.keys()):
                if attr in EVENT_HANDLERS or attr.startswith('on'):
                    del tag[attr]
                # Check for dangerous protocols in URLs
                if attr in ('href', 'src', 'action', 'data'):
                    val = str(tag[attr])
                    if any(val.lower().startswith(p) for p in DANGEROUS_PROTOCOLS):
                        del tag[attr]
                        
        # Remove style attributes
        for tag in soup.find_all():
            if 'style' in tag.attrs:
                del tag['style']
            if 'class' in tag.attrs:
                del tag['class']
            if 'id' in tag.attrs:
                del tag['id']
                
        return str(soup)
        
    def html_to_markdown(self, html: str) -> str:
        """Convert sanitized HTML to Markdown."""
        if not BS4_AVAILABLE:
            raise RuntimeError("BeautifulSoup4 required: pip install beautifulsoup4")
            
        soup = BeautifulSoup(html, 'html.parser')
        return self._convert_node(soup)
        
    def _convert_node(self, node) -> str:
        """Recursively convert HTML node to Markdown."""
        if isinstance(node, NavigableString):
            text = str(node)
            return text
        
        if node.name is None:
            # Text node
            return str(node) if node else ""
            
        tag = node.name.lower() if node.name else ''
        children = list(node.children)
        
        result = []
        
        # Handle specific tags
        if tag == 'h1':
            result.append(f"# {self._get_text_content(node)}\n")
        elif tag == 'h2':
            result.append(f"## {self._get_text_content(node)}\n")
        elif tag == 'h3':
            result.append(f"### {self._get_text_content(node)}\n")
        elif tag == 'h4':
            result.append(f"#### {self._get_text_content(node)}\n")
        elif tag == 'h5':
            result.append(f"##### {self._get_text_content(node)}\n")
        elif tag == 'h6':
            result.append(f"###### {self._get_text_content(node)}\n")
        elif tag == 'p':
            result.append(f"{self._get_text_content(node)}\n\n")
        elif tag == 'br':
            result.append("\n")
        elif tag == 'strong' or tag == 'b':
            result.append(f"**{self._get_text_content(node)}**")
        elif tag == 'em' or tag == 'i':
            result.append(f"*{self._get_text_content(node)}*")
        elif tag == 'code':
            content = self._get_text_content(node)
            if '\n' in content:
                result.append(f"```\n{content}\n```")
            else:
                result.append(f"`{content}`")
        elif tag == 'pre':
            code = node.find('code')
            if code:
                lang = code.get('class', [''])[0].replace('language-', '') if code.get('class') else ''
                result.append(f"```{lang}\n{self._get_text_content(code)}\n```\n")
            else:
                result.append(f"```\n{self._get_text_content(node)}\n```\n")
        elif tag == 'a':
            href = node.get('href', '')
            if href and not any(href.lower().startswith(p) for p in DANGEROUS_PROTOCOLS):
                text = self._get_text_content(node)
                result.append(f"[{text}]({href})")
            else:
                result.append(self._get_text_content(node))
        elif tag == 'img':
            src = node.get('src', '')
            alt = node.get('alt', '')
            if src and not any(src.lower().startswith(p) for p in DANGEROUS_PROTOCOLS):
                result.append(f"![{alt}]({src})")
        elif tag == 'ul':
            for li in node.find_all('li', recursive=False):
                result.append(f"- {self._get_text_content(li)}\n")
            result.append("\n")
        elif tag == 'ol':
            for i, li in enumerate(node.find_all('li', recursive=False), 1):
                result.append(f"{i}. {self._get_text_content(li)}\n")
            result.append("\n")
        elif tag == 'blockquote':
            content = self._get_text_content(node)
            for line in content.split('\n'):
                result.append(f"> {line}\n")
            result.append("\n")
        elif tag == 'table':
            result.append(self._convert_table(node))
        elif tag == 'div':
            # Process children inline
            for child in children:
                result.append(self._convert_node(child))
        else:
            # Default: process children
            for child in children:
                result.append(self._convert_node(child))
                
        return ''.join(result)
        
    def _get_text_content(self, node) -> str:
        """Extract text content from node."""
        texts = []
        for child in node.children:
            if isinstance(child, NavigableString):
                texts.append(str(child))
            elif child.name not in ('script', 'style'):
                texts.append(self._get_text_content(child))
        text = ''.join(texts)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
        
    def _convert_table(self, table) -> str:
        """Convert HTML table to Markdown table."""
        rows = table.find_all('tr')
        if not rows:
            return "[TABLE_AMBIGUOUS]\n\n"
            
        # Get headers
        headers = []
        header_row = table.find('thead')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers.append(self._get_text_content(th).strip() or ' ')
        else:
            first_row = rows[0]
            headers = [self._get_text_content(th).strip() or ' ' 
                      for th in first_row.find_all(['th', 'td'])]
                      
        if not headers:
            return "[TABLE_AMBIGUOUS]\n\n"
            
        # Build Markdown table
        result = []
        result.append(f"| {' | '.join(headers)} |")
        result.append(f"| {' | '.join(['---'] * len(headers))} |")
        
        # Get body rows
        body = table.find('tbody') or table
        data_rows = body.find_all('tr')[1:] if not header_row else body.find_all('tr')
        
        for row in data_rows:
            cells = [self._get_text_content(td).strip() or ' ' 
                    for td in row.find_all(['td', 'th'])]
            if len(cells) == len(headers):
                result.append(f"| {' | '.join(cells)} |")
                
        result.append("\n")
        return '\n'.join(result)
        
    def normalize_markdown(self, md: str) -> str:
        """Clean up Markdown output."""
        # Normalize line endings
        md = md.replace('\r\n', '\n').replace('\r', '\n')
        
        # Fix multiple blank lines (max 2)
        md = re.sub(r'\n{3,}', '\n\n', md)
        
        # Trim trailing whitespace
        lines = [line.rstrip() for line in md.split('\n')]
        md = '\n'.join(lines)
        
        return md.strip() + '\n'
        
    def convert(self) -> str:
        """Main conversion with sanitization."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"HTML file not found: {self.input_path}")
            
        with open(self.input_path, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()
            
        if not html.strip():
            raise ValueError("Empty HTML input")
            
        # Sanitize first
        sanitized = self.sanitize_html(html)
        
        # Convert to Markdown
        md = self.html_to_markdown(sanitized)
        
        # Normalize
        md = self.normalize_markdown(md)
        
        # Add removed tags notice if any
        if self.removed_tags:
            self.warnings.append(f"Removed tags: {', '.join(self.removed_tags)}")
            
        return md
        
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
    parser = argparse.ArgumentParser(description="Convert HTML to clean Markdown")
    parser.add_argument("input", help="Input HTML file path")
    parser.add_argument("-o", "--output", help="Output Markdown file path")
    
    args = parser.parse_args()
    
    cleaner = HTMLCleaner(
        input_path=args.input,
        output_path=args.output
    )
    
    try:
        content = cleaner.convert()
        output_path = cleaner.save(content)
        print(f"Converted to: {output_path}")
        if cleaner.warnings:
            print(f"Warnings: {'; '.join(cleaner.warnings)}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
