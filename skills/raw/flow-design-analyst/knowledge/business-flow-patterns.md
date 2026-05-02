# Business Flow Patterns — Happy Path, Alternative Path, Exception Path

> **Usage**: Đọc khi flow có > 2 nhánh alternative hoặc exception path (Tầng 2). Cung cấp định nghĩa chuẩn và Mermaid conventions cho 3 loại path.
> **Source**: Transformed 100% from `resources/business-flow-patterns.md`; verified: modernanalyst.com, wikipedia.org, processmaker.com, zeplin.io

---

## 1. Happy Path — Luồng Thành Công Lý Tưởng

### Định nghĩa
**Happy Path** (hay "Golden Path" / "Main Scenario") là luồng lý tưởng, không có lỗi, thể hiện chuỗi thao tác thành công theo con đường ngắn nhất để đạt được mục tiêu use case.

> Business Analyst luôn thiết kế Happy Path **trước**, sau đó mới mở rộng ra Alternative và Exception Paths.

### Đặc điểm nhận biết
- Không có bất kỳ lỗi validation, conflict, hay timeout
- Mọi điều kiện đều thỏa mãn theo mặc định
- Số bước là ít nhất có thể để hoàn thành use case
- Kết thúc bằng success state: resource được tạo/cập nhật, user nhận feedback tích cực

### Nhận biết trong spec/US
Keyword: `"successfully"`, `"returns"`, `"is valid"`, `"completes"`, `"is created"`, `"đăng ký thành công"`, `"tạo được"`, `"hợp lệ"`, `"xác nhận"`

### Mermaid Convention
- Dùng solid arrow `-->` làm main flow
- Có thể dùng `==>` (thick arrow) để nhấn mạnh critical path step
- Nodes theo trình tự tuyến tính ít phân nhánh nhất

### Ví dụ — UC01: Đăng ký tài khoản (Happy Path only)

```mermaid
flowchart TD
  subgraph User ["👤 User"]
    U1["Điền form đăng ký"] --> U2["Nhấn Submit"]
    U5["✅ Thấy thông báo thành công"]
  end
  subgraph System ["⚙️ System"]
    S1["Validate schema (Zod)"] ==> S2["Hash password"]
    S2 ==> S3["Gửi email xác nhận"]
    S3 ==> S4["Trả 201 Created"]
  end
  subgraph DB ["🗄️ Database"]
    D1[("INSERT user record")]
  end
  U2 --> S1 --> S2 --> D1 --> S3 --> S4 --> U5
```

---

## 2. Alternative Path — Luồng Hợp Lệ Thay Thế

### Định nghĩa
**Alternative Path** (hay "Alternate Flow" / "Extension Scenario") là luồng vẫn hợp lệ và **vẫn đạt được mục tiêu thành công**, nhưng lệch khỏi Happy Path do user choice hoặc business rule khác nhau.

> Alternative ≠ Exception: Alternative vẫn kết thúc thành công, chỉ theo cách khác.

### Đặc điểm nhận biết
- Vẫn đạt mục tiêu cuối cùng (success outcome) nhưng qua đường khác
- Thường được kích hoạt bởi: lựa chọn của user, điều kiện kinh doanh, trạng thái hiện tại của hệ thống
- Business rule phân nhánh: "IF condition THEN do X ELSE do Y" — cả hai kết thúc OK

### Nhận biết trong spec/US
Keyword: `"alternatively"`, `"hoặc"`, `"if the user chooses"`, `"in case of"`, `"otherwise"`, `"nếu đã tồn tại thì"`, `"toggle"`, `"switch"`

### Mermaid Convention
- Từ Decision Diamond `{}` phân ra 2 solid arrows `-->`
- Cả hai nhánh đều kết thúc bằng success state (dù là success khác nhau)
- Label nhánh rõ ràng: `-- "Đã bookmark" -->` / `-- "Chưa bookmark" -->`

### Ví dụ — UC19: Lưu/Bỏ lưu bài viết (Happy + Alternative)

```mermaid
flowchart TD
  subgraph User ["👤 User"]
    U1["Nhấn nút Bookmark"]
    U2["✅ Icon đổi: Đã lưu"]
    U3["✅ Icon đổi: Đã bỏ lưu"]
  end
  subgraph System ["⚙️ System"]
    S1{"Bài đã bookmark?"}
    S2["Trả 201 bookmark added"]
    S3["Trả 200 bookmark removed"]
  end
  subgraph DB ["🗄️ Database"]
    D1[("Query bookmarks")]
    D2[("INSERT bookmark")]
    D3[("DELETE bookmark")]
  end

  U1 --> S1 --> D1
  D1 -- "Chưa bookmark" --> D2 --> S2 --> U2
  D1 -- "Đã bookmark" --> D3 --> S3 --> U3
```

---

## 3. Exception Path — Luồng Lỗi/Thất Bại

### Định nghĩa
**Exception Path** (hay "Error Flow" / "Failure Scenario") xảy ra khi lỗi, validation fail, timeout, hoặc điều kiện nằm ngoài mong đợi. Kết quả: **KHÔNG đạt mục tiêu ban đầu** của use case.

> Exception Path KHÔNG có nghĩa là "lỗi code" — nó có thể là business exception hợp lệ (ví dụ: email đã tồn tại là expected business exception trong UC01).

### Đặc điểm nhận biết
- Kết thúc bằng error state, không phải success
- User nhận thông báo lỗi (toast error, error page, redirect to error)
- System trả non-2xx HTTP response code (400, 401, 403, 404, 409, 500)
- Thường là: validation fail, auth fail, not found, conflict, server error

### Nhận biết trong spec/US
Keyword: `"if invalid"`, `"on error"`, `"fails"`, `"not found"`, `"unauthorized"`, `"already exists"`, `"timeout"`, `"lỗi"`, `"không hợp lệ"`, `"không tìm thấy"`, `"đã tồn tại"`, `"quá thời hạn"`

### Mermaid Convention
- Dùng dotted arrow `-.->` cho async error hoặc unexpected failure
- Solid arrow `-->` cho expected exception (validation error là đủ expected)
- Label nhánh exception: `-- "Invalid" -->`, `-- "Không hợp lệ" -->`, `-- "Error" -->`
- Kết thúc có tên rõ: `U_err["❌ Hiển thị lỗi: Email đã tồn tại"]`

### Ví dụ — UC01: Đăng ký tài khoản (Exception Paths)

```mermaid
flowchart TD
  subgraph User ["👤 User"]
    U1["Submit form"]
    U_v["❌ Lỗi: Dữ liệu không hợp lệ"]
    U_c["❌ Lỗi: Email đã được sử dụng"]
  end
  subgraph System ["⚙️ System"]
    S1["Validate schema (Zod)"]
    S2{"Schema OK?"}
    S3{"Email đã tồn tại?"}
    S4["Trả 400: Validation Error"]
    S5["Trả 409: Conflict"]
  end
  subgraph DB ["🗄️ Database"]
    D1[("SELECT users WHERE email=?")]
  end

  U1 --> S1 --> S2
  S2 -- "Không hợp lệ" --> S4 --> U_v
  S2 -- "Hợp lệ" --> S3 --> D1
  D1 -- "Đã tồn tại" --> S5 --> U_c
```

---

## 4. Combined Example — UC01: Đăng ký (Ba path types đầy đủ)

Flow hoàn chỉnh tích hợp cả Happy Path, Alternative Path (auto-generate username), và Exception Paths:

```mermaid
flowchart TD
  %% UC01: Đăng ký tài khoản — M1 Auth & Profile
  %% Happy: Đăng ký thành công | Alt: Username tự sinh | Exception: Email trùng / Validation fail

  subgraph User ["👤 User"]
    direction TB
    U1["Truy cập trang Register"]
    U2["Điền Email, Password<br/>(Username optional)"]
    U3["Nhấn Submit"]
    U_OK["✅ Redirect Login<br/>+ Thông báo: Kiểm tra email"]
    U_ValidErr["❌ Hiển thị lỗi validation<br/>(field highlight đỏ)"]
    U_ConflictErr["❌ Thông báo: Email đã được sử dụng"]
  end

  subgraph System ["⚙️ System"]
    direction TB
    S1["Nhận POST /api/users/register"]
    S2{"Schema hợp lệ?<br/>(Zod validate)"}
    S3{"Username trống?"}
    S4["Auto-generate username<br/>từ email prefix"]
    S5{"Email đã tồn tại?"}
    S6["Trả 400: Validation Error"]
    S7["Trả 409: Email Conflict"]
    S8["Hash password (bcrypt)"]
    S9["Gửi email xác nhận (SendGrid)"]
    S10["Trả 201: User Created"]
  end

  subgraph DB ["🗄️ Database"]
    direction TB
    D1[("SELECT users WHERE email=?")]
    D2[("INSERT user record")]
  end

  %% Flow
  U1 --> U2 --> U3 --> S1 --> S2

  %% Exception: Validation fail
  S2 -- "Không hợp lệ" --> S6 --> U_ValidErr

  %% Alternative: Auto-generate username
  S2 -- "Hợp lệ" --> S3
  S3 -- "Username trống" --> S4
  S3 -- "Username có sẵn" --> S5
  S4 --> S5

  %% Check duplicate email
  S5 --> D1
  D1 -- "Đã tồn tại" --> S7 --> U_ConflictErr

  %% Happy Path: Success
  D1 -- "Chưa tồn tại" --> S8 --> D2 --> S9 --> S10 --> U_OK
```

---

## Tóm tắt — Khi nào dùng path nào?

| Path | Kết thúc | Trigger | Example |
|------|---------|---------|---------|
| **Happy Path** | ✅ Success | Mọi điều kiện thỏa mãn, không có lỗi | Đăng ký thành công |
| **Alternative Path** | ✅ Success (khác) | User choice, toggle state, business rule | Username auto-generate, remove bookmark |
| **Exception Path** | ❌ Failure | Validation fail, auth error, conflict, server error | Email trùng, JWT hết hạn, 500 error |
