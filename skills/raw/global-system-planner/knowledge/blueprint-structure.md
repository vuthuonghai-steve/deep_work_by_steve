# Blueprint Structure

## Overview

Blueprint là tài liệu tổng quan hệ thống, định nghĩa:
- Kiến trúc tổng thể của hệ thống
- Các module và mối quan hệ giữa chúng
- Hướng dẫn cho các agent pipeline phía sau

## Cấu Trúc Blueprint

```markdown
# Module Blueprint: [Tên Dự Án]

## 1. System Overview
- Mục tiêu cốt lõi
- Kiến trúc chung

## 2. Actor & Entity Cốt Lõi
- Guest, User, Admin
- Các thực thể chính

## 3. Business Flow Breakdown
- Module breakdown
- Dependencies giữa các module

## 4. Guidelines
- Flow Agent guidelines
- Sequence Agent guidelines
- Class & DB Agent guidelines
```

## Quy Tắc Viết

1. **Không vẽ UML** - Chỉ viết Markdown văn xuôi
2. **Dùng headings/bullets** rõ ràng
3. **Liệt kê đầy đủ** các actor và entity
