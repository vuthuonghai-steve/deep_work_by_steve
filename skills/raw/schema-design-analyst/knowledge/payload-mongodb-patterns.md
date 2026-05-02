# PayloadCMS & MongoDB Modeling Patterns
> Nguồn sự thật (Source of Truth) cho tư duy thiết kế Database Schema trong dự án KLTN (PayloadCMS v3 + MongoDB).
> Tài liệu này được dùng làm Input Knowledge (Pillar 1) cho Schema Design Analyst Agent.

---

## 1. Nguyên Tắc Cốt Lõi (Code-First)

PayloadCMS sử dụng tư duy "Code-First":
- Mọi Collection/Global đều được định nghĩa bằng TypeScript Code.
- Cấu trúc TypeScript map thẳng xuống MongoDB fields.
- PayloadCMS tự động lo liệu phần REST/GraphQL API và Admin UI dựa trên cấu hình schema này.
- **Trọng tâm khi thiết kế Schema**: Suy nghĩ xem dữ liệu lưu trữ trực tiếp trên Disk (MongoDB) thế nào cho tối ưu Read/Write, đồng thời tuân thủ 16MB Document Limit của MongoDB.

---

## 2. Chiến Lược Embed vs Reference (Nhúng vs Tham Chiếu)

Quyết định sống còn của Data Architect: Node này là một Collection độc lập (Aggregate Root) hay Nhúng (Embedded) vào một Collection khác?

### 2.1. Khi nào dùng Reference (Aggregate Root / Tách Collection)
- **Truy cập độc lập**: Entity này cần được query riêng lẻ, không cần thông qua Parent. (Ví dụ: `Users`, `Posts`).
- **Data mọc vô hạn**: Nếu dữ liệu con cứ đẻ ra liên tục và đe dọa giới hạn 16MB/document của MongoDB. (Ví dụ: Lịch sử thanh toán của User, Log thông báo).
- **Mối quan hệ Nhiều-Nhiều (N:M)**: PayloadCMS xử lý bằng mảng chứa ID hoặc Join Table ẩn. Tách ra collection độc lập sẽ dùng field type: `relationship` với `hasMany: true`.

*Cú pháp Payload:*
```typescript
{ 
  name: 'categories', 
  type: 'relationship', 
  relationTo: 'categories', 
  hasMany: true // N:M
}
```

### 2.2. Khi nào dùng Embed (Array / Group / Blocks)
- **Truy cập phụ thuộc (Data That is Accessed Together...)**: Nếu dữ liệu con CHỈ được đọc ra khi đọc dữ liệu cha. (Ví dụ: `address` của `User`, `variants` của một `Product`).
- **Số lượng nhỏ và giới hạn (Bound)**: Chắc chắn số lượng phần tử con dưới vài trăm và không bao giờ vượt 16MB. (Ví dụ: 5 Tấm ảnh cover của một Post).
- **Snapshot Data (Dữ liệu tĩnh)**: Lưu lại giá tại thời điểm mua hàng (Vd: Nhúng thông tin Product vào màn Order thay vì Reference id, vì giá thay đổi thì Order không được phép thay đổi).

*Cú pháp Payload:*
```typescript
{
  name: 'address',
  type: 'group', // Trở thành Object trong Mongo
  fields: [...]
}
// Hoặc
{
  name: 'items',
  type: 'array', // Trở thành Array trong Mongo
  fields: [...]
}
```

---

## 3. MongoDB Advanced Patterns (Dành riêng cho Payload)

### 3.1. Polymorphic Pattern (Mẫu Đa Hình)
Lưu trữ nhiều loại data khác nhau trong cùng một mảng. Rất phù hợp cho luồng Activity Feed, Layout Builder, Timeline sự kiện.
- **Trong Payload**: Sử dụng trường `blocks`. Field này lưu cấu trúc tùy ý dựa vào `blockType`.
- **Hoặc Polymorphic Relationship**: Một field ID có thể trỏ vào `Posts` HOẶC `Videos`.
*Ví dụ Notification Polymorphic:*
```typescript
{
  name: 'targetEntity',
  type: 'relationship',
  relationTo: ['posts', 'comments', 'users'] // Entity này là ai?
}
```

### 3.2. Computed Pattern (Denormalized / Tính toán sẵn)
Trong NoSQL, **không** Join realtime để đếm `count()`. Chúng ta tính sẵn và lưu `likes_count`, `comments_count` ngay trên bảng `Posts`.
- **Trong Payload**: Sử dụng Local API trong **Hooks** (`afterChange`, `afterDelete`) để increment (`$inc`) counter ở collection cha.
*Ví dụ Behavior Hook từ Contract YAML:*
- Khi Create Like (afterChange) -> `payload.update({ id: post_id, data: { likes_count: old + 1 } })`.

### 3.3. Bucket / Outlier Pattern (Xô chứa tràn biên)
Dành cho dữ liệu IoT hoặc hệ thống Notifications có lưu lượng khổng lồ.
Thay vì nhúng 1.000.000 notifications vào document `User` (Gây nổ 16MB MongoDB) -> Tách `notifications` thành collection ngoại vi, sử dụng `user_id` làm Index để query. Hoặc lưu theo "cụm" (Bucket theo ngày/tháng). PayloadCMS hỗ trợ chia Collection theo từng domain.

---

## 4. Map Types: YAML Contract to Payload Fields

| YAML Contract Type | PayloadCMS Field Type | Mô tả kỹ thuật Database (MongoDB) |
|-------------------|-----------------------|----------------------------------|
| `string` / `text` | `text` / `textarea`   | String thông thường. |
| `number`          | `number`              | Float / Integer mặc định. |
| `boolean`         | `checkbox`            | Boolean `true`/`false`. |
| `select` / `enum` | `select`              | String bị giới hạn options. Có thể `hasMany` (Array of Strings). |
| `date` / `time`   | `date`                | ISODate MongoDB. Quản lý createdAt/updatedAt tự động (`timestamps: true`). |
| `email`           | `email`               | String có Regex email validate sẵn của Payload. |
| `upload` / `media`| `upload`              | Reference tới ObjectId của Collection chứa file. Yêu cầu field `relationTo: 'media'`. |
| `relationship`    | `relationship`        | Lưu ObjectId hoặc mảng ObjectId (`hasMany: true`). Yêu cầu `relationTo`. |
| `array`           | `array`               | Mảng các Object con. Lưu embedded. |
| `group` / `object`| `group`               | Object con tĩnh. Lưu embedded object `{}`. |
| `richText`        | `richText`            | Lưu định dạng lexical JSON block trong MongoDB. |
| `blocks`          | `blocks`              | Polymorphic array (mỗi element có 1 `blockType` riêng). |

---

## 5. Metadata Khác Của Schema (Hành Vi & Quyền)

### 5.1. Hooks (Vận hành sự kiện)
- Mọi Logic Behavior của object (gửi email, tính tiền, tạo thông báo, sync count) ĐỀU phải được thiết kế thành Hook file rời tại `collections/TênCollection/config/hooks/*.ts`.
- Móc nối vào `beforeChange`, `afterChange`, `beforeDelete`, `afterRead`.

### 5.2. Access Control (Check Quyền)
RBAC trong Payload được viết dưới dạng hàm trong Schema.
- Payload cấp sẵn Object `req.user`
- Mẫu Access rule:
  - `anyone`: `() => true`
  - `admin`: `({ req: { user } }) => user?.role === 'admin'`
  - `owner`: `({ req: { user } }) => ({ user_id: { equals: user?.id } })` (MongoDB query hạn chế field read/write).

### 5.3. Indexing (Truy vấn nhanh)
- Khai báo `{ index: true }` ở mọi field được query lấy danh sách (`user_id`, `status`, `createdAt`, `unique_code`).
- Đặc biệt chú ý Compound Index nếu có nhiều query filter kết hợp (VD: Feed Sort theo `createdAt` + Filter theo `status`).
