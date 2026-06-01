#!/usr/bin/env python3
"""
gather.py — Quét codebase đệ quy, lọc theo blacklist và đóng gói dữ liệu thô vào XML an toàn.
"""

import os
import sys
import argparse
import yaml
import fnmatch
from datetime import datetime, timezone

def parse_args():
    parser = argparse.ArgumentParser(
        description="Quét codebase đệ quy, lọc theo blacklist và đóng gói dữ liệu thô vào XML an toàn."
    )
    parser.add_argument(
        "--target", "-t", required=True,
        help="Thư mục mục tiêu cần quét đệ quy."
    )
    parser.add_argument(
        "--output", "-o", default="data/raw_source.xml",
        help="Đường dẫn lưu tệp XML kết quả (Mặc định: data/raw_source.xml)."
    )
    parser.add_argument(
        "--blacklist", "-b", default="data/search-blacklist.yaml",
        help="Đường dẫn đến tệp cấu hình blacklist YAML."
    )
    parser.add_argument(
        "--max-size", type=int, default=500,
        help="Kích thước tệp lớn nhất cho phép quét (KB). Mặc định: 500 KB."
    )
    return parser.parse_args()

def load_blacklist(blacklist_path):
    """Nạp danh sách các glob patterns loại trừ từ tệp YAML."""
    if not os.path.exists(blacklist_path):
        print(f"[WARNING] Không tìm thấy tệp blacklist tại: {blacklist_path}. Sử dụng danh sách trống.", file=sys.stderr)
        return []
    
    try:
        with open(blacklist_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and "blacklist" in data:
                return data["blacklist"]
            elif isinstance(data, list):
                return data
            else:
                print(f"[WARNING] Định dạng tệp blacklist không hợp lệ. Mong đợi một list hoặc dict chứa key 'blacklist'.", file=sys.stderr)
                return []
    except Exception as e:
        print(f"[ERROR] Lỗi khi đọc tệp blacklist: {e}", file=sys.stderr)
        return []

def should_exclude(rel_path, blacklist_patterns):
    """Kiểm tra đường dẫn tương đối có khớp với bất kỳ pattern nào trong blacklist không."""
    # Chuẩn hóa dấu phân tách đường dẫn sang '/' để đồng bộ
    rel_path = rel_path.replace('\\', '/').lstrip('/')
    parts = rel_path.split('/')
    
    for pattern in blacklist_patterns:
        # Chuẩn hóa pattern
        pattern = pattern.replace('\\', '/').strip('/')
        
        # Trường hợp 1: folder/** (Ví dụ: node_modules/**)
        if pattern.endswith('/**'):
            prefix = pattern[:-3]
            if rel_path.startswith(prefix + '/') or rel_path == prefix:
                return True
        
        # Trường hợp 2: folder/ (Ví dụ: build/)
        elif pattern.endswith('/'):
            prefix = pattern[:-1]
            if prefix in parts:
                return True
                
        # Trường hợp 3: Chứa ký tự wildcard đơn giản (Ví dụ: *.log)
        elif '*' in pattern or '?' in pattern:
            # Nếu không có dấu '/' trong pattern, so khớp với từng segment của path (như tên file)
            if '/' not in pattern:
                if any(fnmatch.fnmatch(part, pattern) for part in parts):
                    return True
            else:
                # So khớp với toàn bộ đường dẫn tương đối
                if fnmatch.fnmatch(rel_path, pattern):
                    return True
                    
        # Trường hợp 4: So khớp chính xác
        else:
            if pattern == rel_path or pattern in parts:
                return True
                
    return False

def is_binary_file(filepath):
    """Kiểm tra tệp tin có phải là nhị phân hay không."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return True
            # Thử decode thử một phần file
            chunk.decode("utf-8")
            return False
    except UnicodeDecodeError:
        return True
    except Exception:
        return True

def escape_xml_attr(val):
    """Escape các ký tự đặc biệt của XML cho giá trị thuộc tính (attribute)."""
    val = str(val)
    val = val.replace('&', '&amp;')
    val = val.replace('<', '&lt;')
    val = val.replace('>', '&gt;')
    val = val.replace('"', '&quot;')
    val = val.replace("'", '&apos;')
    return val

def escape_cdata(content):
    """Escape chuỗi kết thúc CDATA ']]>' bằng cách chia nhỏ nó thành các khối CDATA liên tiếp."""
    return content.replace("]]>", "]]]]><![CDATA[>")

def main():
    args = parse_args()
    
    target_dir = os.path.abspath(args.target)
    if not os.path.exists(target_dir):
        print(f"[ERROR] Thư mục mục tiêu không tồn tại: {target_dir}", file=sys.stderr)
        sys.exit(1)
        
    print(f"[*] Bắt đầu quét thư mục mục tiêu: {target_dir}")
    
    # Nạp danh sách loại trừ
    blacklist_patterns = load_blacklist(args.blacklist)
    print(f"[*] Đã nạp {len(blacklist_patterns)} mẫu loại trừ từ blacklist.")
    
    # Đảm bảo thư mục đầu ra tồn tại
    output_path = os.path.abspath(args.output)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    # Thống kê
    stat_total_found = 0
    stat_skipped_blacklist = 0
    stat_skipped_size = 0
    stat_skipped_binary = 0
    stat_gathered = 0
    stat_bytes = 0
    
    # Chuẩn bị file XML
    try:
        with open(output_path, "w", encoding="utf-8") as out_file:
            # Ghi tiêu đề XML
            out_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            out_file.write('<external_inputs>\n')
            
            # Mở thẻ cha cho codebase nguồn
            escaped_target = escape_xml_attr(os.path.basename(target_dir))
            out_file.write(f'  <external_input source="codebase" target_path="{escaped_target}">\n')
            
            # Quét đệ quy
            max_bytes_limit = args.max_size * 1024
            
            for root, dirs, files in os.walk(target_dir):
                # Lọc danh sách thư mục con ngay tại chỗ để tránh duyệt đệ quy vào các thư mục bị cấm
                dirs_to_keep = []
                for d in dirs:
                    d_path = os.path.join(root, d)
                    d_rel = os.path.relpath(d_path, target_dir)
                    if not should_exclude(d_rel, blacklist_patterns):
                        dirs_to_keep.append(d)
                    else:
                        stat_skipped_blacklist += 1
                dirs[:] = dirs_to_keep # Thay đổi dirs tại chỗ để os.walk áp dụng lọc
                
                for file in files:
                    stat_total_found += 1
                    file_path = os.path.join(root, file)
                    file_rel = os.path.relpath(file_path, target_dir)
                    
                    # 1. Kiểm tra blacklist
                    if should_exclude(file_rel, blacklist_patterns):
                        stat_skipped_blacklist += 1
                        continue
                        
                    # 2. Kiểm tra kích thước
                    try:
                        file_size = os.path.getsize(file_path)
                    except OSError:
                        stat_skipped_binary += 1
                        continue
                        
                    if file_size > max_bytes_limit:
                        stat_skipped_size += 1
                        continue
                        
                    # 3. Kiểm tra file nhị phân
                    if is_binary_file(file_path):
                        stat_skipped_binary += 1
                        continue
                        
                    # 4. Đọc nội dung và ghi nhận
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                            content = f.read()
                            
                        # Thống kê
                        stat_gathered += 1
                        stat_bytes += file_size
                        
                        # Thời gian sửa đổi lần cuối
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc).isoformat()
                        
                        # Ghi file XML con
                        esc_path = escape_xml_attr(file_rel)
                        esc_content = escape_cdata(content)
                        
                        out_file.write(f'    <file path="{esc_path}" size_bytes="{file_size}" last_modified="{mtime}">\n')
                        out_file.write(f'      <![CDATA[{esc_content}]]>\n')
                        out_file.write(f'    </file>\n')
                        
                    except Exception as e:
                        print(f"[WARNING] Không thể đọc tệp {file_rel}: {e}", file=sys.stderr)
                        
            out_file.write('  </external_input>\n')
            out_file.write('</external_inputs>\n')
            
        print(f"[+] Thu thập hoàn tất! Dữ liệu được lưu tại: {output_path}")
        print(f"--- Báo cáo Thống kê ---")
        print(f"  - Tổng số tệp tin phát hiện: {stat_total_found}")
        print(f"  - Đã loại bỏ do Blacklist: {stat_skipped_blacklist}")
        print(f"  - Đã bỏ qua do quá kích thước (>{args.max_size}KB): {stat_skipped_size}")
        print(f"  - Đã bỏ qua do là file nhị phân: {stat_skipped_binary}")
        print(f"  - Số lượng tệp tin đã đóng gói thành công: {stat_gathered}")
        print(f"  - Tổng dung lượng dữ liệu văn bản thu thập: {stat_bytes} bytes (~{stat_bytes/1024:.2f} KB)")
        print(f"------------------------")
        
    except Exception as e:
        print(f"[ERROR] Lỗi nghiêm trọng trong quá trình ghi tệp XML: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
