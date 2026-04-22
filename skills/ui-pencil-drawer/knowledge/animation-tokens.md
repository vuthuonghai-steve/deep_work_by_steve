****# Animation Tokens — Pencil Context Guide

> **Source**: `Docs/life-2/ui/animation-spec-guide.md` (100% transform)
> **Mục đích**: Mapping animation tokens → Framer Motion specs → Pencil `context` field assignment.
> **Phạm vi**: Áp dụng trong Phase 3 Pencil Drawer khi gán animation metadata vào nodes. Đặc biệt dùng trong Fluid Zones.

---

## I. NGUYÊN TẮC CHUNG (ANIMATION PHILOSOPHY)

1. **Subtle over Flashy**: Hiệu ứng phải nhẹ nhàng, hỗ trợ người dùng nhận biết hệ thống, không gây xao nhãng.
2. **Standard Timing**:
   - *Fast*: 150ms — Hover states, micro-feedbacks
   - *Normal*: 300ms — Page transitions, entry animations
   - *Slow*: 500ms — Complex layout shifts, onboarding sequences
3. **Primary Triggers** (dùng để ghi vào Pencil `context.trigger`):
   - `initial` — Tự động chạy khi component mount
   - `hover` — Khi di chuột vào element
   - `tap` — Khi click / chạm
   - `viewport` — Khi node xuất hiện trên màn hình (scroll-triggered)

---

## II. BỘ TỪ ĐIỂN ANIMATION TOKENS

Dưới đây là các token keys AI dùng để gán vào trường `context.animation` trong Pencil node JSON.

| Token | Mô tả | Framer Motion Spec |
| :--- | :--- | :--- |
| `fade-up` | Hiện dần và trượt nhẹ từ dưới lên | `initial: {opacity: 0, y: 10}, animate: {opacity: 1, y: 0}` |
| `fade-in` | Hiện dần tại chỗ | `initial: {opacity: 0}, animate: {opacity: 1}` |
| `scale-in` | Phóng to nhẹ từ tâm | `initial: {opacity: 0, scale: 0.95}, animate: {opacity: 1, scale: 1}` |
| `hover-lift` | Nổi nhẹ lên khi hover (Card) | `whileHover: {y: -4, shadow: "lg"}` |
| `hover-scale` | Phóng to nhẹ khi hover (Button) | `whileHover: {scale: 1.02}` |
| `stagger-child` | Hiệu ứng xuất hiện lần lượt cho con | `transition: {staggerChildren: 0.1}` |
| `bounce-subtle` | Nhấp nhô nhẹ — dùng cho CTA quan trọng | `animate: {y: [0, -5, 0]}, transition: {repeat: Infinity}` |

---

## III. GÁN TOKEN VÀO PENCIL NODE (batch_design context)

Khi vẽ bằng Pencil MCP `batch_design`, AI gán animation metadata vào trường `context` của node:

```json
{
  "id": "card-01",
  "type": "ref",
  "context": {
    "animation": "fade-up",
    "delay": 100,
    "priority": "high"
  }
}
```

### Quy tắc gán trong batch_design

- Gán `context.animation` = token key (từ bảng §II) vào node khi Insert (I) hoặc Update (U).
- Gán `context.delay` (ms) nếu component là phần tử trong danh sách (staggered entry).
- Gán `context.trigger` nếu khác `initial` (mặc định).

**Ví dụ batch_design operation:**
```javascript
card=I("mainContent", {type: "ref", ref: "CardNodeId", context: {animation: "fade-up", delay: 100}})
btn=I("mainContent", {type: "ref", ref: "ButtonNodeId", context: {animation: "hover-scale"}})
```

### Self-Critique sau khi gán

- AI gọi `get_screenshot()` để xác nhận "Final State" của animation (vị trí kết thúc).
- Nếu animation có `fade-up` (`y: 10` shift), AI phải đảm bảo `padding-bottom` của container đủ để không bị clip.
- Nếu animation có `hover-lift` (`y: -4`), AI phải đảm bảo không có element nào che phủ phía trên card.

---

## IV. MAPPING TOKEN → COMPONENT TYPE

Gợi ý ánh xạ token → loại component phù hợp (dùng khi Phase 3 gán context):

| Component Type | Token được khuyến nghị | Lý do |
| :--- | :--- | :--- |
| Card / Post item | `fade-up` + `hover-lift` | Entry animation + interactive feedback |
| Button / CTA | `hover-scale` hoặc `bounce-subtle` (chỉ CTA quan trọng) | Micro-interaction rõ ràng |
| Modal / Dialog | `scale-in` | Xuất hiện từ tâm màn hình |
| List / Feed | `stagger-child` trên container | Lần lượt xuất hiện |
| Hero / Banner | `fade-in` | Nhẹ nhàng, không phô trương |
| Notification | `fade-up` với `delay: 0` | Immediate but smooth |

---

## V. CHECKLIST ANIMATION (Tích hợp vào §P3 Self-Verify)

Khi `context.animation` được gán, thêm các kiểm tra sau vào Phase 3 self-verify:

- [ ] Token nằm trong danh sách §II (không tự đặt tên mới)?
- [ ] Animation không gây layout shift cho elements xung quanh (`transform` + `opacity` only)?
- [ ] Container có đủ padding để animation không bị clip (`fade-up` → padding-bottom ≥ 10px)?
- [ ] `reduced-motion` scenario đã được xem xét (animation chỉ là enhancement, không mang thông tin)?
- [ ] Chỉ CTA quan trọng mới dùng `bounce-subtle` (không lạm dụng)?

---

## VI. WORKFLOW CHUYỂN ĐỔI SANG CODE (Tham khảo cho Phase Code-Gen)

Khi Agent chuyển từ `.pen` sang Next.js code:

1. **Detect Token**: AI đọc `context.animation` từ node JSON.
2. **Generate Wrapper**: Bọc Radix UI component (hoặc Tailwind element) bằng `motion`:

```tsx
// Output Code mẫu — Framer Motion wrapper
import { motion } from 'framer-motion'

export const MyCard = () => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3 }}
  >
    {/* Radix UI / Tailwind component content */}
  </motion.div>
)
```

**Tech stack note**: Project sử dụng **Radix UI + Tailwind v4** (không phải shadcn/ui). Wrapper pattern `motion.div` áp dụng bên ngoài Radix primitives, không thay thế chúng.
