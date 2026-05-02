# Actor Lane Taxonomy — 3-Lane Swimlane Model

> **Usage**: Đọc khi không chắc action thuộc lane nào (Tầng 2). Định nghĩa rõ trách nhiệm từng lane trong kiến trúc KLTN.
> **Source**: Transformed 100% from `resources/actor-lane-taxonomy.md`; verified: lucidchart.com, geeksforgeeks.org, wikipedia.org

---

## 1. Ba Lane và Định Nghĩa

| Lane | Tên đầy đủ | Màu sơ đồ (gợi ý) | Chứa những gì |
|------|-----------|-------------------|---------------|
| **User** | 👤 User Lane | #E3F2FD (xanh nhạt) | Mọi hành động của con người thực hiện qua UI |
| **System** | ⚙️ System Lane | #E8F5E9 (xanh lá nhạt) | Mọi logic backend, business rules, external API calls |
| **DB** | 🗄️ Database Lane | #FFF8E1 (vàng nhạt) | Mọi thao tác trực tiếp lên MongoDB / cơ sở dữ liệu |

> ⚠️ **Lưu ý quan trọng**: 3-lane swimlane là **convention** của KLTN project, không phải BPMN formal standard. Nó được thiết kế để phản ánh kiến trúc thực của hệ thống.

### 1.1 User Lane — CON NGƯỜI + GIAO DIỆN

**Định nghĩa**: Mọi thao tác mà **người dùng thực sự thực hiện** thông qua giao diện (React/Next.js UI).

- Bao gồm: click, nhập liệu, submit form, kéo thả, upload file, đọc kết quả trên màn hình
- Actor: Primary Actor (Guest, Member, Admin) — người khởi phát use case
- Hệ thống KLTN frontend: **Next.js/React** components

**Keyword nhận dạng**: `user clicks`, `user inputs`, `user submits`, `user sees`, `user navigates`, `user uploads`, `hiển thị cho user`, `user nhận thấy`

### 1.2 System Lane — PHẦN MỀM + LOGIC + EXTERNAL SERVICES

**Định nghĩa**: Mọi xử lý của phần mềm backend — business rules, validation, transformation, và gọi external services.

- Bao gồm: validate, authenticate, authorize, process, transform, call API, build response, decide
- Hệ thống KLTN backend: **Express.js** (hoặc Next.js API Routes), PayloadCMS hooks
- External services: SendGrid (email), NextAuth.js (OAuth), bcrypt (hash), Sharp (image processing)

**Keyword nhận dạng**: `system validates`, `API processes`, `service calls`, `logic decides`, `backend handles`, `hệ thống xử lý`, `server validates`

### 1.3 DB Lane — PERSISTENCE + DATABASE ONLY

**Định nghĩa**: Mọi thao tác đọc/ghi trực tiếp lên cơ sở dữ liệu — chỉ database operations, không có business logic ở đây.

- Bao gồm: SELECT, INSERT, UPDATE, DELETE, INDEX operations trên MongoDB
- Hệ thống KLTN: **MongoDB** (via Mongoose/PayloadCMS)
- KHÔNG bao gồm: logic xử lý dữ liệu sau khi query (đó là System Lane)

**Keyword nhận dạng**: `stores in DB`, `queries database`, `saves to collection`, `retrieves from`, `MongoDB operation`, `lưu vào cơ sở dữ liệu`, `truy vấn`

---

## 2. Decision Table — Action → Lane (25+ ví dụ KLTN)

| # | Hành động | Lane | Lý do |
|---|-----------|------|-------|
| 1 | User nhấn nút "Đăng ký" | **User** | Người dùng click button trên UI |
| 2 | User điền form (email, username, password) | **User** | Người dùng nhập liệu |
| 3 | User nhấn Submit | **User** | Người dùng gửi form |
| 4 | User nhìn thấy thông báo thành công | **User** | Người dùng đọc kết quả |
| 5 | Validate schema Zod (check required fields, format) | **System** | Backend business rule |
| 6 | Kiểm tra email đã tồn tại | **System** | Logic quyết định → thực ra DB query |
| 7 | Hash password bằng bcrypt | **System** | Backend processing, không phải DB op |
| 8 | Gọi SendGrid API gửi email | **System** | External service call |
| 9 | Gọi Google OAuth API | **System** | External service call |
| 10 | Build JWT token | **System** | Backend logic |
| 11 | Parse request body | **System** | Backend middleware |
| 12 | Trả HTTP response (201, 400, 409) | **System** | Backend responds |
| 13 | SELECT users WHERE email = ? | **DB** | Direct MongoDB query |
| 14 | INSERT new user record | **DB** | Direct MongoDB write |
| 15 | UPDATE user.profile | **DB** | Direct MongoDB update |
| 16 | DELETE bookmark record | **DB** | Direct MongoDB delete |
| 17 | Query bookmarks collection | **DB** | Direct MongoDB read |
| 18 | User nhấn Like | **User** | Người dùng click icon |
| 19 | UPDATE post.likes counter | **DB** | MongoDB atomic update |
| 20 | Hiển thị số like trên UI | **User** | Người dùng thấy kết quả |
| 21 | Kiểm tra JWT token hợp lệ | **System** | Auth middleware logic |
| 22 | User cuộn feed (scroll) | **User** | Người dùng tương tác UI |
| 23 | Load thêm bài viết (pagination query) | **DB** | MongoDB query với limit/skip |
| 24 | Resize ảnh upload bằng Sharp | **System** | Backend image processing |
| 25 | Store ảnh vào S3/r2 | **System** | External storage service call |
| 26 | INSERT image metadata vào media collection | **DB** | MongoDB write |
| 27 | Đọc Atlas Search index | **DB** | MongoDB full-text search operation |

---

## 3. Edge Cases — Tình huống Khó Phân Định

| Hành động | Lane đúng | Giải thích |
|-----------|-----------|------------|
| `Gọi SendGrid gửi email` | **System** | External service call, không phải DB |
| `Kiểm tra rate limit (Redis)` | **System** | Cache layer check — business logic |
| `SET/GET từ Redis cache` | **DB** | Trực tiếp đọc/ghi cache storage |
| `Upload ảnh lên Cloudflare R2` | **System** | External storage API call |
| `Hiển thị toast error cho user` | **User** | Người dùng thấy kết quả |
| `Log error vào winston/console` | **System** | Backend logging, không phải DB op |
| `INSERT log vào logs collection (MongoDB)` | **DB** | Direct MongoDB write |
| `Middleware kiểm tra quyền (RBAC)` | **System** | Authorization business logic |
| `User nhìn thấy lỗi "404 Not Found"` | **User** | Người dùng đọc error message trên UI |
| `Atlas Search (full-text search)` | **DB** | MongoDB native feature, direct DB op |

---

## 4. Ví dụ Đúng / Sai (3 cặp)

### Cặp 1: Validate dữ liệu

```
❌ SAI (Validate ở User Lane):
  subgraph User
    U1["User submit form"] --> U2["Validate email format"]  ← SAI
  end

✅ ĐÚNG (Validate ở System Lane):
  subgraph User
    U1["User submit form"]
  end
  subgraph System
    S1["Validate email format (Zod)"]  ← ĐÚNG
  end
  U1 --> S1
```

**Lý do**: Validation là business rule của backend, không phải hành động người dùng. Người dùng chỉ submit form.

---

### Cặp 2: Gửi email

```
❌ SAI (Email ở DB Lane):
  subgraph DB
    D1[("Gửi email xác nhận")]  ← SAI — không phải DB op
  end

✅ ĐÚNG (Email ở System Lane):
  subgraph System
    S1["Gọi SendGrid: Gửi email xác nhận"]  ← ĐÚNG
  end
  subgraph DB
    D1[("INSERT email_queue hoặc log")]  ← Nếu cần persist
  end
```

**Lý do**: Gọi SendGrid là external API call = System Lane. Chỉ khi cần lưu email log vào DB mới xuất hiện DB Lane.

---

### Cặp 3: Hiển thị kết quả cho user

```
❌ SAI (System trả response và "user thấy" trong cùng 1 System node):
  subgraph System
    S1["Trả 200 OK và user thấy danh sách bài viết"]  ← SAI — gộp 2 lane
  end

✅ ĐÚNG (Tách biệt rõ):
  subgraph System
    S1["Trả 200 OK với danh sách bài viết"]  ← System response
  end
  subgraph User
    U1["Xem danh sách bài viết trên Feed"]  ← User sees
  end
  S1 --> U1
```

**Lý do**: Trả HTTP response là System action. Người dùng nhìn thấy kết quả là User action. Phải tách ra 2 nodes trong 2 lane khác nhau.
