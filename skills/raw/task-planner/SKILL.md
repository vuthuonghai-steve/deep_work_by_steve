---
name: task-planner
description: 'Skill phan tach yeu cau/tinh nang thanh cac phase, task va subtask cu the. Tao bo tai lieu planning clean, khong chua code mau, tap trung mo ta logic va nghiep vu. Su dung khi: (1) nhan yeu cau tinh nang moi can lap ke hoach, (2) co tai lieu nghien cuu can chuyen thanh task plan, (3) nguoi dung yeu cau phan tach cong viec, (4) can tao roadmap trien khai cho du an/tinh nang. Trigger: /task-planner, /plan-tasks, "phan tach task", "lap ke hoach", "tao plan", "chia phase".'
category: utility
pipeline:
  stage_order: 0
  input_contract: []
  output_contract: []
  dependencies: []
---

## Progressive Disclosure

### Tier 1: Always Load (Required)
- **SKILL.md** (this file)

### Tier 2: Required Knowledge (BẮT BUỘC phải đọc)
- [references/document-format.md](references/document-format.md) - Quy chuẩn định dạng tài liệu

### Tier 3: Optional (load when needed)
- [assets/templates/PHASE.template.md](assets/templates/PHASE.template.md) - Template cho Phase
- [assets/templates/INDEX.template.md](assets/templates/INDEX.template.md) - Template cho Index
- [assets/templates/TASK.template.md](assets/templates/TASK.template.md) - Template cho Task

> 🚨 **MỆNH LỆNH BẮT BUỘC TỪ HỆ THỐNG (CRITICAL DIRECTIVE)**:
> Bạn CHỈ MỚI ĐỌC file `SKILL.md` này. Trí tuệ của bạn chưa được nạp đầy đủ.
> Hệ thống **KHÔNG** tự động nạp các file kiến thức khác trong thư mục.
> Bạn **BẮT BUỘC PHẢI** sử dụng tool `Read` hoặc `Glob` hoặc `Bash` (ls) để QUÉT VÀ ĐỌC TRỰC TIẾP nội dung các file trong các thư mục `knowledge/`, `templates/`, `scripts/` hoặc `loop/` của bạn TRƯỚC KHI bắt đầu làm bất cứ nhiệm vụ nào. 
> Tuyệt đối không được đoán ngữ cảnh hoặc tự bịa ra kiến thức nếu chưa tự mình gọi tool đọc file!


# Task Planner

## Tong quan

Skill nay giup phan tach yeu cau hoac tai lieu nghien cuu thanh bo tai lieu task planning co cau truc, bao gom:
- **Phase**: Cac giai doan lon cua du an/tinh nang
- **Task**: Cac cong viec cu the trong moi phase
- **Subtask**: Cac buoc nho trong moi task

**Nguyen tac cot loi**: Tai lieu output **KHONG CHUA CODE MAU**. Chi tap trung mo ta logic, nghiep vu, va cac buoc can thuc hien.

---

## Workflow

### Buoc 1: Thu thap Context

Khi skill duoc goi, thuc hien thu thap thong tin:

#### 1.1 Xac dinh nguon input

| Nguon | Hanh dong |
|-------|-----------|
| File tai lieu | Doc file bang Read tool, phan tich noi dung |
| Yeu cau truc tiep | Ghi nhan yeu cau tu nguoi dung |
| URL/link | Su dung WebFetch neu can |

#### 1.2 Hoi thong tin can thiet

Su dung AskUserQuestion de hoi:

1. **Thu muc output** - Noi luu cac file tai lieu plan
2. **Ten du an/tinh nang** - De dat ten cho bo tai lieu
3. **Pham vi** - Xac dinh ranh gioi cua yeu cau

#### 1.3 Nghien cuu codebase

Su dung Task tool voi `subagent_type=Explore` de:
- Tim hieu cau truc du an hien tai
- Xac dinh cac file/module lien quan
- Hieu cac pattern dang duoc su dung

---

### Buoc 2: Phan tich va Phan chia

#### 2.1 Phan tich yeu cau

Doc ky input va xac dinh:
- Muc tieu chinh can dat duoc
- Cac thanh phan/module can xay dung
- Cac phu thuoc va rang buoc

#### 2.2 Chia thanh Phase

Moi phase nen:
- Co muc tieu ro rang
- Co the demo/kiem tra doc lap
- Thoi gian hop ly (khong qua lon/nho)

Quy tac chia phase:
```
Phase 1: Nen tang (setup, config, schema)
Phase 2: Core logic (business logic chinh)
Phase 3: Integration (ket noi cac phan)
Phase 4: Polish (UI, UX, optimization)
Phase 5: Testing & Documentation
```

#### 2.3 Chia thanh Task trong moi Phase

Moi task nen:
- Hoan thanh duoc trong 1 session lam viec
- Co input/output ro rang
- Co tieu chi hoan thanh cu the

#### 2.4 Chia thanh Subtask

Moi subtask nen:
- La 1 don vi cong viec nho nhat
- Mo ta duoc logic can thuc hien
- Co the verify ket qua

---

### Buoc 3: Hoi Clarification

Truoc khi tao tai lieu final, su dung AskUserQuestion de:

1. **Xac nhan pham vi** - "Toi da xac dinh {N} phase, {M} task. Day co phu hop khong?"
2. **Lam ro mo ho** - Hoi ve cac diem chua ro trong yeu cau
3. **Xac nhan uu tien** - "Phase nao can uu tien truoc?"
4. **Kiem tra rang buoc** - "Co rang buoc nao ve tech stack/pattern khong?"

---

### Buoc 4: Tao Bo Tai lieu

#### 4.1 Doc format guidelines

Tham khao file `references/document-format.md` de dam bao format dung chuan.

#### 4.2 Tao cau truc thu muc

```bash
{output-path}/
├── INDEX.md
├── phase-01-{slug}/
│   ├── PHASE.md
│   ├── task-01-{slug}.md
│   └── task-02-{slug}.md
└── phase-02-{slug}/
    ├── PHASE.md
    └── ...
```

#### 4.3 Viet noi dung

**Thu tu viet:**
1. Viet INDEX.md truoc (tong quan)
2. Viet PHASE.md cho tung phase
3. Viet task-{so}-{slug}.md cho tung task

**Noi dung moi file:**
- INDEX.md: Tong quan, muc tieu, danh sach phase
- PHASE.md: Muc tieu phase, danh sach task, phu thuoc
- task-*.md: Logic xu ly, subtasks, edge cases, DoD

#### 4.4 Tich hop TodoWrite

Sau khi tao tai lieu, su dung TodoWrite de tao todo list tu cac task:

```
- Phase 1: {ten}
  - Task 1.1: {ten}
  - Task 1.2: {ten}
- Phase 2: {ten}
  - Task 2.1: {ten}
  ...
```

---

## Nguyen tac Viet Tai lieu

### KHONG lam

1. **KHONG chen code mau** - Khong snippet, khong example code
2. **KHONG copy syntax** - Khong dan syntax tu docs
3. **KHONG qua chi tiet implementation** - Khong mo ta tung dong code
4. **KHONG gia dinh** - Hoi neu chua ro

### NEN lam

1. **Mo ta logic ro rang** - "Kiem tra dieu kien A, neu thoa thi thuc hien B"
2. **Liet ke edge cases** - "Truong hop input rong, xu ly bang cach..."
3. **Chi ro phu thuoc** - "Can hoan thanh Task 1 truoc khi bat dau"
4. **Dinh nghia DoD** - "Task hoan thanh khi: checklist..."

---

## Vi du Mo ta Logic (KHONG code)

### SAI (co code):
```
// Tao function validate email
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
```

### DUNG (mo ta logic):
```
## Logic validate email

1. Kiem tra input khong rong
2. Kiem tra format co dang: {text}@{domain}.{extension}
3. Kiem tra domain hop le (khong chua ky tu dac biet)
4. Tra ve true neu hop le, false neu khong

### Edge cases
- Email rong -> tra ve false
- Email khong co @ -> tra ve false
- Email co nhieu @ -> tra ve false
```

---

## Resources

### references/
- `document-format.md` - Huong dan chi tiet ve format cac file tai lieu

### assets/templates/
- `INDEX.template.md` - Template cho file INDEX.md
- `PHASE.template.md` - Template cho file PHASE.md
- `TASK.template.md` - Template cho file task

---

## Checklist Hoan thanh

Truoc khi ket thuc, dam bao:

- [ ] Da tao INDEX.md voi day du thong tin
- [ ] Da tao PHASE.md cho moi phase
- [ ] Da tao task-*.md cho moi task
- [ ] Tat ca file khong chua code mau
- [ ] Moi task co Definition of Done
- [ ] Da tao TodoWrite list tu cac task
- [ ] Da thong bao nguoi dung ve vi tri thu muc output
