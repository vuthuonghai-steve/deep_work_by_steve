# 📊 Biểu diễn Trực quan & Chia sẻ Skill

> **Cấp độ tài liệu:** L2 Playbook & Reference Code

Skill có thể chạy các kịch bản lệnh (scripts) bằng bất kỳ ngôn ngữ lập trình nào được cài đặt trên hệ thống. Một mô hình thiết kế cực kỳ mạnh mẽ là **tự động tạo giao diện trực quan** (Interactive HTML) hiển thị dữ liệu phân tích, báo cáo hoặc sơ đồ cấu trúc rồi tự động khởi chạy trình duyệt web để hiển thị kết quả.

---

## 1. Phương pháp Tạo Giao diện Trực quan

Kịch bản thiết kế dưới đây xây dựng một **Codebase Visualizer** — công cụ phân tích cấu trúc cây thư mục dự án, tính toán dung lượng, đếm loại tệp và render ra một trang HTML tương tác tuyệt đẹp có khả năng co giãn các thư mục và hiển thị biểu đồ phân bố dung lượng tệp.

### Cấu trúc Thư mục Skill Package
```text
codebase-visualizer/
├── SKILL.md           # Khai báo hướng dẫn chạy script
└── scripts/
    └── visualize.py   # Script Python xử lý phân tích và sinh HTML
```

### Nội dung SKILL.md
```yaml
---
name: codebase-visualizer
description: Tạo sơ đồ cây thư mục tương tác động hiển thị cấu trúc codebase. Kích hoạt khi người dùng muốn khám phá cấu trúc dự án, tìm các file lớn, hoặc phân tích loại tệp.
allowed-tools: Bash(python3 *)
---
# Trình Trực quan hóa Codebase
Chạy kịch bản phân tích mã nguồn sau để tạo sơ đồ tương tác động:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```
Lệnh này sẽ tạo tệp `codebase-map.html` tại thư mục hiện tại và tự động khởi chạy trình duyệt mặc định của bạn để hiển thị sơ đồ.
```

---

## 2. Mã nguồn Kịch bản Phân tích (`visualize.py`)

Kịch bản Python dưới đây chỉ sử dụng các thư viện chuẩn (built-in libraries) có sẵn của Python 3 để đảm bảo khả năng tương thích tối đa, không cần cài đặt thêm gói thư viện ngoài:

<examples>
```python
#!/usr/bin/env python3
"""Trình trực quan hóa cấu trúc dự án dưới dạng sơ đồ cây HTML tương tác."""

import json
import sys
import webbrowser
from html import escape
from pathlib import Path
from collections import Counter

# Các thư mục mặc định cần bỏ qua khi quét dự án để tránh nhiễu dữ liệu
IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    """Quét thư mục đệ quy và tính toán dung lượng tệp tin."""
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    """Tạo tệp HTML tự chứa (Self-contained) với CSS và JS tương tác."""
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    
    # Bảng màu đại diện cho các ngôn ngữ lập trình phổ biến
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Tóm tắt codebase</h1>
      <div class="stat"><span>Số tệp</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Thư mục</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Tổng dung lượng</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>Loại tệp</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>Phân bố loại tệp</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 Thư mục gốc: {escape(data["name"])}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function esc(s) {{ return s.replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c])); }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{esc(node.name)}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{esc(node.name)}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html, encoding='utf-8')

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Đã sinh bản đồ cấu trúc tại: {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```
</examples>

---

## 3. Cách thức Kiểm thử & Chia sẻ

1.  **Chạy thử nghiệm:** Khởi động Claude Code trong bất kỳ dự án nào của bạn và yêu cầu: *"Hãy vẽ trực quan hóa dự án này cho tôi"* hoặc gõ trực tiếp lệnh `/codebase-visualizer`. Claude sẽ kích hoạt công thức, thực thi tệp Python chạy phân tích và tự động hiển thị sơ đồ cây trên trình duyệt mặc định.
2.  **Mở rộng khả năng:** Mô hình này hoạt động hiệu quả cho mọi đầu ra dạng giao diện trực quan như:
    *   Sơ đồ liên kết phụ thuộc (Dependency graphs).
    *   Báo cáo độ bao phủ kiểm thử (Test coverage reports).
    *   Tài liệu hóa API tự động.
    *   Bản đồ quan hệ cơ sở dữ liệu (Database schemas).
