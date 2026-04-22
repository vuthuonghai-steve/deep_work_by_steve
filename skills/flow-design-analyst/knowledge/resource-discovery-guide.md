# Resource Discovery Guide — Intent Detection & Confidence Scoring

> **Usage**: Đọc bắt buộc (Tầng 1) tại Phase 0 DETECT. Cung cấp NLU framework để phân tích intent mơ hồ và tìm UC ứng viên trước khi hỏi user bất kỳ câu nào.
> **Source**: Transformed 100% from `resources/resource-discovery-guide.md`; verified: genesys.com, mypurecloud.com, voiceflow.com (NLU best practices)
> **Implements**: Guardrail G6 "Discover Before Ask"

---

## 1. Nguyên Tắc Cốt Lõi — "Discover Before Ask"

**G6 Guardrail**: Skill PHẢI hoàn thành Resource Discovery **trước** khi hỏi user bất kỳ câu nào.

```
❌ VI PHẠM G6:
  User: "vẽ flow bookmark"
  Skill: "Bạn muốn vẽ flow cho UC nào trong M5?"  ← Câu mở — CẤM

✅ TUÂN THỦ G6:
  User: "vẽ flow bookmark"
  Skill: [Phase 0] Detect: "bookmark" → M5, UC19/UC20
         [Phase 1] Discover: tìm use-case-m5-bookmarking.md, m5-bookmarking-spec.md
         [Gate 1] Report: "🔍 Tôi tìm thấy 2 UC trong M5... Bạn muốn vẽ [1] hay [2]?"
```

---

## 2. Intent Parsing Framework — 3 Loại Keyword

### 2.1 Action Verb (+20pt) — Nhận biết user muốn tạo flow

| Tiếng Việt | Tiếng Anh |
|-----------|----------|
| vẽ, vẽ flow, vẽ sơ đồ | draw, diagram |
| tạo, tạo flow, tạo diagram | create, generate, make |
| làm flow, làm sơ đồ | build flow |
| sinh, sinh diagram | produce, output |
| show flow, hiển thị flow | show, display |
| phân tích flow, phân tích luồng | analyze flow |
| giải thích flow | explain flow |

> Nếu KHÔNG có Action Verb rõ ràng nhưng user đang trong phiên làm việc flow skill → mặc định +20pt.

### 2.2 Domain Noun (+30pt) — Xác định UC/Module

| Keyword (Tiếng Việt) | Keyword (Tiếng Anh) | Module | UC chính |
|---------------------|---------------------|--------|----------|
| đăng ký, tạo tài khoản, tạo account | register, sign up, create account | M1 | UC01 |
| đăng nhập, login, xác thực | login, sign in, authenticate | M1 | UC02 |
| google login, đăng nhập google, oauth | oauth, google sign in, social login | M1 | UC03 |
| đăng xuất, logout | logout, sign out | M1 | UC04 |
| quên mật khẩu, reset password, đặt lại mật khẩu | forgot password, reset password, password recovery | M1 | UC05 |
| hồ sơ, profile, chỉnh hồ sơ, cập nhật thông tin | profile, edit profile, update profile, bio | M1 | UC06 |
| xem hồ sơ người khác, trang cá nhân công khai | public profile, view profile, user page | M1 | UC07 |
| tạo bài, viết bài, post bài, đăng bài | create post, write post, new post, publish | M2 | UC08 |
| sửa bài, chỉnh bài, edit post, cập nhật bài | edit post, update post, modify post | M2 | UC09 |
| quyền riêng tư bài, privacy, bài công khai, bài riêng tư | post privacy, visibility, public post, private post | M2 | UC10 |
| feed, bảng tin, news feed, xem bài viết, home | feed, news feed, home feed, timeline, view posts | M3 | UC11 |
| tìm kiếm, search, tìm người, tìm bài | search, find, lookup, discover, search user | M3 | UC12 |
| gợi ý tìm kiếm, autocomplete search | autocomplete, search suggest, search hint | M3 | UC13 |
| like, thích bài, unlike, bỏ thích | like, unlike, react, heart | M4 | UC14 |
| bình luận, comment, phản hồi, reply | comment, reply, nested comment, discussion | M4 | UC15 |
| chia sẻ bài, share, repost | share, repost, share post | M4 | UC16 |
| follow, theo dõi, unfollow, bỏ theo dõi | follow, unfollow, subscribe | M4 | UC17 |
| chặn, block, chặn người dùng | block, mute, block user | M4 | UC18 |
| bookmark, lưu bài, bỏ lưu | bookmark, save, unsave, save post | M5 | UC19 |
| collection bookmark, quản lý bookmark, nhóm bookmark | manage bookmark, bookmark collection, organize bookmarks | M5 | UC20 |
| thông báo, notification, realtime notification | notification, alert, push notification, bell | M6 | UC21 |
| đọc thông báo, mark read, xem thông báo | mark as read, read notification, view notification | M6 | UC22 |
| báo cáo vi phạm, report, tố cáo | report, flag, abuse, report violation | M6 | UC23 |
| kiểm duyệt, moderation, duyệt báo cáo, admin review | review report, moderate, admin action, moderation | M6 | UC24 |

### 2.3 Module Hint (+30pt) — Tăng confidence nhanh

| Hint (Tiếng Việt / Tiếng Anh) | Module |
|-------------------------------|--------|
| "M1", "auth", "authentication", "identity", "account" | M1 |
| "M2", "content", "post", "article", "bài viết" | M2 |
| "M3", "feed", "discovery", "search", "khám phá" | M3 |
| "M4", "engagement", "social", "connection", "kết nối" | M4 |
| "M5", "bookmark", "save", "collection", "đã lưu" | M5 |
| "M6", "notification", "moderation", "admin", "thông báo" | M6 |

---

## 3. Confidence Score Rubric — Thang điểm 0-100

| Thành phần | Điểm | Ghi chú |
|-----------|------|---------|
| **Action Verb** detected | +20pt | Ít nhất 1 từ trong bảng §2.1 |
| **Domain Noun** matched | +30pt | Ít nhất 1 keyword trong bảng §2.2 |
| **Module Hint** explicit | +30pt | User đề cập "M1", "auth", v.v. trong bảng §2.3 |
| **UC matched** trong registry | +20pt | Domain Noun dẫn đến ≤ 2 UC candidates |
| **Tổng tối đa** | **100pt** | |

### 3.1 Ngưỡng Quyết định (3-tier)

| Score | Mode | Hành động tại Gate 1 |
|-------|------|---------------------|
| **≥ 70pt** (và không tie) | **Confident Mode** | Discovery Report + Yes/No question |
| **40–69pt** hoặc tie | **Gray Zone** | Numbered options (tối đa 3) |
| **< 40pt** | **Rejection** | Danh sách module để user chọn |

### 3.2 Tie-break Rule

Nếu ≥ 2 UC candidates có score chênh nhau **≤ 10pt** → **LUÔN đưa numbered options**, dù tổng điểm ≥ 70pt.

**Ví dụ Tie-break**: Input "flow post" → UC08 (+85pt) vs UC09 (+75pt) → chênh 10pt → Đưa numbered options dù score UC08 = 85pt (≥ 70pt).

---

## 4. Quy Tắc Phân Nhánh — Decision Tree

```
INPUT User
  │
  ├─► [Phase 0 DETECT] Keyword extraction
  │     ├─ Action Verb?   → +20pt
  │     ├─ Domain Noun?   → +30pt → map to UC candidates
  │     └─ Module Hint?   → +30pt
  │
  ├─► [Phase 1 DISCOVER] Tìm file trong project
  │     ├─ UC matched in uc-id-registry.yaml?  → +20pt
  │     └─ Spec file found?  → ghi vào Discovery Report
  │
  ├─► [Tính Confidence Score]
  │
  ├─ Score ≥ 70 AND no tie?
  │     └─► GATE 1: Discovery Report đầy đủ + "Xác nhận không?" (Yes/No)
  │
  ├─ Score 40–69 OR tie?
  │     └─► GATE 1: Numbered options (tối đa 3 candidates)
  │
  └─ Score < 40?
        └─► GATE 1: Danh sách 6 module + hướng dẫn nhập thêm chi tiết
```

---

## 5. Discovery Report Templates — 3 Mẫu Chuẩn

### Mẫu 1: Confident Mode (Score ≥ 70, no tie)

> Trigger: User nhập "vẽ flow đăng nhập M1"

```
🔍 **Discovery Report**

📌 **Flow được yêu cầu:**
- Use Case: UC02 — Đăng nhập Email/Password
- Module: M1 — Auth & Profile
- Confidence: 90/100

📂 **Tài liệu tìm thấy:**
- Use Case: `Docs/life-2/diagrams/UseCase/use-case-m1-auth-profile.md`
- Spec: `Docs/life-2/specs/m1-auth-profile-spec.md`

⚙️ **Kỹ thuật phát hiện:**
- Action Verb: "vẽ" (+20pt)
- Domain Noun: "đăng nhập" → UC02 (+30pt)
- Module Hint: "M1" (+30pt)
- UC matched in registry (+10pt)

→ **Xác nhận tiến hành vẽ flow UC02 — Đăng nhập không?** (Yes/No)
```

### Mẫu 2: Gray Zone (Score 40–69 hoặc tie)

> Trigger: User nhập "flow post bài"

```
🔍 **Discovery Report**

⚠️ **Tôi tìm thấy 2 Use Case phù hợp với "post bài":**

[1] **UC08 — Tạo bài viết** (M2, confidence: 85/100)
    Spec: `Docs/life-2/specs/m2-content-engine-spec.md`
    Mô tả: Flow tạo bài viết mới, upload ảnh, chọn privacy.

[2] **UC09 — Chỉnh sửa/Xóa bài viết** (M2, confidence: 75/100)
    Spec: `Docs/life-2/specs/m2-content-engine-spec.md`
    Mô tả: Flow sửa nội dung hoặc xóa bài đã đăng.

→ **Bạn muốn vẽ flow nào? Nhập 1 hoặc 2.**
```

### Mẫu 3: Rejection (Score < 40)

> Trigger: User nhập "vẽ flow cho tính năng social"

```
⚠️ **Tôi chưa xác định được Use Case cụ thể.**

"Social" có thể liên quan đến nhiều module:

[1] **M4 — Engagement & Connections**: Like, Comment, Share, Follow, Block
[2] **M1 — Auth & Profile**: Profile công khai, quản lý tài khoản
[3] **M3 — Discovery & Feed**: News Feed, Tìm kiếm người dùng
[4] **M5 — Bookmarking**: Lưu bài, quản lý collection
[5] **M6 — Notifications & Moderation**: Thông báo, báo cáo vi phạm

→ **Bạn đang nghĩ đến chức năng nào? Nhập số module hoặc mô tả cụ thể hơn.**
(Ví dụ: "follow người dùng" hoặc "like bài viết")
```

---

## 6. Worked End-to-End Example — "flow bookmark"

### Input từ user
```
"flow bookmark"
```

### Step 1 — Phase 0: DETECT

```
Input phân tích: "flow bookmark"

Keyword detection:
- "flow" → Action Verb (context = flow skill)  → +20pt
- "bookmark" → Domain Noun
  → match: "bookmark, lưu bài, bỏ lưu" trong bảng §2.2
  → UC candidates: UC19 (Lưu/Bỏ lưu bài viết) AND UC20 (Quản lý collection)
  → +30pt (Domain Noun detected)
- Không có Module Hint explicit → +0pt

Chưa query UC-ID registry → UC match pending
```

### Step 2 — Phase 1: DISCOVER

```
Tra uc-id-registry.yaml với keyword "bookmark":
→ UC19: keywords bao gồm "bookmark", "lưu bài" → match (+10pt)
→ UC20: keywords bao gồm "bookmark collection" → match (+10pt)

Tìm file:
→ use-case-m5-bookmarking.md: UC19, UC20 ← tìm thấy
→ m5-bookmarking-spec.md ← tìm thấy

Score tính:
→ UC19: Action(20) + Domain(30) + Module(0) + UC(10) = 60pt
→ UC20: Action(20) + Domain(30) + Module(0) + UC(10) = 60pt
```

### Step 3 — SCORE & BRANCH

```
Score: UC19 = 60pt, UC20 = 60pt
Threshold: 60pt < 70pt → Gray Zone
Tie: chênh = 0pt ≤ 10pt → Numbered Options

→ Mode: Gray Zone → Mẫu 2 (Numbered options)
```

### Step 4 — Gate 1 Output

```
🔍 **Discovery Report**

⚠️ **Tôi tìm thấy 2 Use Case trong M5 — Bookmarking:**

[1] **UC19 — Lưu/Bỏ lưu bài viết** (confidence: 60/100)
    Spec: `Docs/life-2/specs/m5-bookmarking-spec.md`
    Mô tả: Flow toggle bookmark — add/remove một bài viết cụ thể.

[2] **UC20 — Quản lý collection bookmark** (confidence: 60/100)
    Spec: `Docs/life-2/specs/m5-bookmarking-spec.md`
    Mô tả: Flow tạo/sửa/xóa collection, thêm bài vào collection.

→ **Bạn muốn vẽ flow nào? Nhập 1 hoặc 2.**
```

---

## 7. File Path Registry — Mapping UC → Files

| Module | UC-ID Range | Use Case File | Spec File |
|--------|-------------|--------------|-----------|
| M1 | UC01–UC07 | `Docs/life-2/diagrams/UseCase/use-case-m1-auth-profile.md` | `Docs/life-2/specs/m1-auth-profile-spec.md` |
| M2 | UC08–UC10 | `Docs/life-2/diagrams/UseCase/use-case-m2-content-engine.md` | `Docs/life-2/specs/m2-content-engine-spec.md` |
| M3 | UC11–UC13 | `Docs/life-2/diagrams/UseCase/use-case-m3-discovery-feed.md` | `Docs/life-2/specs/m3-discovery-feed-spec.md` |
| M4 | UC14–UC18 | `Docs/life-2/diagrams/UseCase/use-case-m4-engagement-connections.md` | `Docs/life-2/specs/m4-engagement-spec.md` |
| M5 | UC19–UC20 | `Docs/life-2/diagrams/UseCase/use-case-m5-bookmarking.md` | `Docs/life-2/specs/m5-bookmarking-spec.md` |
| M6 | UC21–UC24 | `Docs/life-2/diagrams/UseCase/use-case-m6-notifications-moderation.md` | `Docs/life-2/specs/m6-notifications-moderation-spec.md` |
