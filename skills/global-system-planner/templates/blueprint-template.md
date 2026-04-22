# Blueprint Template

## System Overview

**Project Name:** [Tên dự án]
**Version:** 1.0
**Date:** YYYY-MM-DD

### Mục tiêu cốt lõi
[Mô tả mục tiêu chính của hệ thống]

### Kiến trúc chung
[Tổng quan kiến trúc - layers, components chính]

---

## Actor & Entity Cốt lõi

### Actors
| Actor | Mô tả | Quyền |
|-------|-------|-------|
| Guest | Người dùng chưa đăng nhập | Xem công khai |
| User | Người dùng đã đăng nhập | Thao tác cá nhân |
| Admin | Quản trị viên | Toàn quyền |

### Core Entities
| Entity | Mô tả | Quan hệ |
|--------|-------|---------|
| [Entity1] | [Mô tả] | hasMany [Entity2] |
| [Entity2] | [Mô tả] | belongsTo [Entity1] |

---

## Business Flow Breakdown

### Module Map
| Module | Tên | Dependencies | Mô tả |
|--------|-----|-------------|-------|
| M1 | [Tên] | - | [Mô tả] |
| M2 | [Tên] | M1 | [Mô tả] |

### Cross-Module Dependencies
- M2 phụ thuộc M1 vì...
- M3 phụ thuộc M1, M2 vì...

---

## Guidelines

### Flow Agent Guidelines
[Hướng dẫn cho Flow Design Analyst]

### Sequence Agent Guidelines
[Hướng dẫn cho Sequence Design Analyst]

### Class & DB Agent Guidelines
[Hướng dẫn cho Class Diagram & Schema Analyst]
