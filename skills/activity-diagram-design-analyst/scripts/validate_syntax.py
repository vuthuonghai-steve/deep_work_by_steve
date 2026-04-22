import re
import sys

def validate_mermaid_flowchart(content):
    """
    Kiem tra cu phap Mermaid flowchart co ban.
    Tap trung vao: Initial node, Final node, va dau mui ten.
    """
    errors = []
    
    # Kiem tra xem co phai flowchart TD/LR khong
    if not re.search(r'flowchart\s+(TD|LR|BT|RL)', content):
        errors.append("[Error] Khong tim thay khai bao flowchart (TD/LR/...).")

    # Kiem tra Initial Node (Start)
    if not re.search(r'\(\(.*?\)\)', content):
        errors.append("[Warning] Thieu Initial Node hoac Fork/Join Node (dung cu phap (( )) ).")

    # Kiem tra Action Nodes [ ]
    if not re.search(r'\[.*?\]', content):
        errors.append("[Warning] Khong thay Action Nodes (dung cu phap [ ] ).")

    # Kiem tra Decision Nodes { }
    if re.search(r'\{.*?\}', content) and not re.search(r'--\s*.*?\s*-->', content):
        errors.append("[Error] Decision Node hien tai thieu cac canh ranh nhanh hop le.")

    # Kiem tra mui ten
    if not re.search(r'-->|-.->|==>', content):
        errors.append("[Error] Khong tim thay Control Flow hoac Object Flow.")

    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_syntax.py <mermaid_file_or_content>")
        sys.exit(1)
        
    path_or_content = sys.argv[1]
    
    try:
        with open(path_or_content, 'r') as f:
            content = f.read()
    except:
        content = path_or_content

    print(f"--- Dang kiem tra syntax Mermaid ---")
    results = validate_mermaid_flowchart(content)
    
    if not results:
        print("✅ Syntax Mermaid co ve hop le.")
    else:
        for err in results:
            print(err)
