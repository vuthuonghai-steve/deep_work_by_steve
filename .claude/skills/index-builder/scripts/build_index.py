#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
scripts/build_index.py
Tự động quét thư mục tri thức, tính toán token, kiểm tra liên kết và sinh tệp chỉ mục llms.txt.
"""

import os
import sys
import argparse
import re

# Blacklist các thư mục ẩn và thư mục hệ thống
BLACKLIST_DIRS = {
    '.git',
    'node_modules',
    '__pycache__',
    '.agents',
    '.gemini',
    '.hermes',
    '.claude',
    'venv',
    'env',
    'tmp'
}

# Các đuôi file tri thức được chấp nhận
ALLOWED_EXTENSIONS = {'.md', '.yaml', '.yml', '.xml'}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Tự động biên dịch chỉ mục tri thức llms.txt")
    parser.add_argument(
        '--target-dir',
        type=str,
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        help="Thư mục tri thức đích cần quét (mặc định là thư mục cha của script này)"
    )
    parser.add_argument(
        '--output-file',
        type=str,
        default=None,
        help="Đường dẫn lưu tệp llms.txt kết quả (mặc định sẽ lưu vào thư mục data/ của target-dir)"
    )
    return parser.parse_args()

def estimate_tokens(file_path):
    """
    Ước lượng số lượng token bằng cách đọc file và đếm từ (words).
    Công thức xấp xỉ: số từ / 0.75 (hoặc nhân 1.33)
    """
    try:
        if not os.path.exists(file_path):
            return 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Đếm số từ bằng regex
        words = len(re.findall(r'\w+', content))
        if words == 0:
            return 0
        return int(words / 0.75)
    except Exception as e:
        print(f"[Cảnh báo] Không thể tính toán token cho {file_path}: {e}")
        return 0

def classify_file(relative_path):
    """
    Phân loại file vào các tầng tri thức (L0-L3) dựa trên đường dẫn và tên file.
    - L0 & L1 (Core Guides): CLAUDE.md, SKILL.md, loop/checklist.md hoặc các file chứa rules/policy.
    - L2 (Domain Knowledge): Các file trong knowledge/ hoặc chứa các tài liệu nghiệp vụ.
    - L3 (Examples & Checklists): Các file trong examples/, templates/, scripts/ hoặc fixtures.
    """
    lower_path = relative_path.lower()
    
    # L0 & L1: Core Guides
    if (
        relative_path == 'SKILL.md' or 
        lower_path.endswith('claude.md') or 
        'loop/' in lower_path or
        'rules' in lower_path or
        'policy' in lower_path
    ):
        return 'L0_L1'
    
    # L2: Domain Knowledge
    elif 'knowledge/' in lower_path or 'docs/' in lower_path:
        return 'L2'
    
    # L3: Examples & Templates & Scripts
    elif 'examples/' in lower_path or 'templates/' in lower_path or 'scripts/' in lower_path or 'data/' in lower_path:
        return 'L3'
    
    # Mặc định xếp vào L2 nếu là tài liệu, L3 nếu là file dữ liệu/code khác
    return 'L2' if lower_path.endswith('.md') else 'L3'

def extract_manual_descriptions(llms_txt_path):
    """
    Đọc tệp llms.txt cũ nếu tồn tại, trích xuất các mô tả viết tay của người dùng
    cho từng liên kết để bảo lưu thông tin.
    Trả về dict: {relative_path: manual_description}
    """
    manual_desc = {}
    if not os.path.exists(llms_txt_path):
        return manual_desc
    
    try:
        with open(llms_txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex tìm các dòng dạng: - [Tên hiển thị](file_link): Mô tả
        pattern = r'-\s+\[([^\]]+)\]\(([^)]+)\):\s*(.*)'
        matches = re.findall(pattern, content)
        for name, link, desc in matches:
            # Loại bỏ file:/// hoặc các path prefix để lấy relative path
            clean_link = link.replace('file:///', '').strip()
            # Loại bỏ phần token/byte statistics ở cuối mô tả nếu có
            desc_clean = re.sub(r'\s*\(\s*~\s*\d+\s+tokens,\s*\d+\s+bytes\s*\)\s*$', '', desc.strip())
            # Nếu là absolute path trong workspace, chuyển về relative path
            # (chúng ta sẽ lưu key là clean_link)
            manual_desc[clean_link] = desc_clean
    except Exception as e:
        print(f"[Cảnh báo] Không thể đọc mô tả từ file cũ: {e}")
    
    return manual_desc

def scan_directory(target_dir):
    """
    Quét đệ quy thư mục đích và gom tất cả các file tri thức hợp lệ.
    Trả về danh sách các dict chứa thông tin chi tiết của từng file.
    """
    scanned_files = []
    
    for root, dirs, files in os.walk(target_dir):
        # Loại bỏ các thư mục trong blacklist
        dirs[:] = [d for d in dirs if d not in BLACKLIST_DIRS and not d.startswith('.')]
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in ALLOWED_EXTENSIONS:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, target_dir)
                
                # Bỏ qua chính file llms.txt
                if file.lower() == 'llms.txt':
                    continue
                
                size_bytes = os.path.getsize(abs_path)
                tokens_est = estimate_tokens(abs_path)
                category = classify_file(rel_path)
                
                scanned_files.append({
                    'rel_path': rel_path,
                    'abs_path': abs_path,
                    'filename': file,
                    'size_bytes': size_bytes,
                    'tokens_est': tokens_est,
                    'category': category
                })
                
    return scanned_files

def build_llms_txt(target_dir, scanned_files, manual_descriptions):
    """
    Tạo nội dung cho tệp llms.txt dựa trên danh sách file quét được và mô tả thủ công.
    """
    # Khởi tạo các nhóm
    core_guides = []
    domain_knowledge = []
    examples_checklists = []
    
    for f in scanned_files:
        rel_path = f['rel_path']
        # Lấy mô tả thủ công nếu có, nếu không thì sinh mô tả tự động
        desc = manual_descriptions.get(rel_path)
        if not desc:
            # Tìm kiếm mô tả trong data/llms.txt nếu link có format file:///...
            desc = manual_descriptions.get(f"file:///{rel_path}")
            
        if not desc:
            desc = f"Tài liệu tri thức {f['filename']}." if rel_path.endswith('.md') else f"Tệp tin cấu hình {f['filename']}."
            
        # Format dòng hiển thị
        line = f"- [{rel_path}]({rel_path}): {desc} (~{f['tokens_est']} tokens, {f['size_bytes']} bytes)"
        
        if f['category'] == 'L0_L1':
            core_guides.append(line)
        elif f['category'] == 'L2':
            domain_knowledge.append(line)
        else:
            examples_checklists.append(line)
            
    # Xây dựng văn bản Markdown hoàn chỉnh
    lines = []
    lines.append("# index-builder — AI Knowledge Index")
    lines.append("")
    lines.append("> Bản đồ tri thức giúp AI Agent tự động định tuyến và nạp ngữ cảnh phù hợp.")
    lines.append("")
    
    lines.append("## Core Guides (L0 & L1)")
    if core_guides:
        lines.extend(core_guides)
    else:
        lines.append("- (Chưa có hướng dẫn cốt lõi)")
    lines.append("")
    
    lines.append("## Domain Knowledge (L2)")
    if domain_knowledge:
        lines.extend(domain_knowledge)
    else:
        lines.append("- (Chưa có tri thức nghiệp vụ)")
    lines.append("")
    
    lines.append("## Examples & Checklists (L3)")
    if examples_checklists:
        lines.extend(examples_checklists)
    else:
        lines.append("- (Chưa có ví dụ và danh sách kiểm tra)")
    lines.append("")
    
    return "\n".join(lines)

def verify_links(output_file, target_dir):
    """
    Kiểm duyệt chất lượng: Quét tệp llms.txt đã sinh và xác thực xem mọi link tương đối
    có thực sự trỏ tới một tệp tin tồn tại hay không.
    """
    if not os.path.exists(output_file):
        print(f"[Lỗi] File chỉ mục không tồn tại để kiểm tra liên kết: {output_file}")
        return False
        
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex tìm các link dạng [text](link)
    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', content)
    broken_links = []
    
    for link in links:
        # Bỏ qua các link tuyệt đối hoặc không phải file local
        if link.startswith(('http://', 'https://', 'mailto:')):
            continue
            
        # Chuyển link về dạng đường dẫn cục bộ thực tế
        clean_link = link.replace('file:///', '').strip()
        abs_link_path = os.path.join(target_dir, clean_link)
        
        if not os.path.exists(abs_link_path):
            broken_links.append(link)
            
    if broken_links:
        print(f"[Cảnh báo] Phát hiện các liên kết chết trong {os.path.basename(output_file)}:")
        for bl in broken_links:
            print(f"  - {bl}")
        return False
        
    print(f"[Thành công] Xác thực liên kết: 100% liên kết hoạt động tốt!")
    return True

def main():
    args = parse_arguments()
    target_dir = os.path.abspath(args.target_dir)
    
    print(f"--- BẮT ĐẦU QUÉT THƯ MỤC TRI THỨC ---")
    print(f"Thư mục quét: {target_dir}")
    
    if not os.path.exists(target_dir):
        print(f"[Lỗi] Thư mục đích không tồn tại: {target_dir}")
        sys.exit(1)
        
    # Thiết lập đường dẫn lưu tệp đầu ra llms.txt
    if args.output_file:
        output_file = os.path.abspath(args.output_file)
    else:
        # Mặc định lưu vào data/llms.txt trong thư mục đích
        data_dir = os.path.join(target_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        output_file = os.path.join(data_dir, 'llms.txt')
        
    print(f"Tệp đầu ra: {output_file}")
    
    # 1. Trích xuất các mô tả thủ công từ tệp llms.txt cũ
    manual_descriptions = extract_manual_descriptions(output_file)
    if manual_descriptions:
        print(f"Đã nạp {len(manual_descriptions)} mô tả thủ công từ tệp cũ để bảo lưu.")
        
    # 2. Quét đệ quy thư mục
    scanned_files = scan_directory(target_dir)
    print(f"Đã tìm thấy {len(scanned_files)} tệp tin tri thức hợp lệ.")
    
    # 3. Sinh nội dung llms.txt
    llms_txt_content = build_llms_txt(target_dir, scanned_files, manual_descriptions)
    
    # 4. Ghi file đầu ra
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(llms_txt_content)
        print(f"[Thành công] Ghi tệp chỉ mục thành công tại {output_file}")
    except Exception as e:
        print(f"[Lỗi] Không thể ghi tệp chỉ mục: {e}")
        sys.exit(1)
        
    # 5. Xác thực liên kết (Link Checker)
    verify_links(output_file, target_dir)
    
    print(f"--- HOÀN THÀNH TỔNG HỢP CHỈ MỤC ---")

if __name__ == '__main__':
    main()
