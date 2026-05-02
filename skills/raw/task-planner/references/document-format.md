# Document Format Guidelines

## Nguyen tac co ban

### KHONG bao gom trong tai lieu task

1. **Code mau** - Khong chen code snippet, code example vao tai lieu
2. **Implementation details** - Khong mo ta chi tiet cach viet code
3. **Syntax references** - Khong dan link toi docs ve syntax
4. **Copy-paste snippets** - Khong cung cap doan code de copy

### CO bao gom trong tai lieu task

1. **Mo ta logic** - Giai thich ro logic can thuc hien
2. **Nghiep vu** - Mo ta nghiep vu can dat duoc
3. **Dieu kien** - Cac dieu kien, edge cases can xu ly
4. **Ket qua mong doi** - Output expected khi hoan thanh
5. **Phu thuoc** - Cac task/file/module lien quan

---

## Cau truc thu muc output

```
{output-path}/
├── INDEX.md                    # File routing chinh
├── phase-01-{ten-phase}/
│   ├── PHASE.md               # Tong quan phase
│   ├── task-01-{ten-task}.md  # Chi tiet task
│   ├── task-02-{ten-task}.md
│   └── ...
├── phase-02-{ten-phase}/
│   ├── PHASE.md
│   ├── task-01-{ten-task}.md
│   └── ...
└── ...
```

---

## Format file INDEX.md

```markdown
# {Ten du an/Tinh nang} - Task Planning Index

> **Tao boi**: task-planner skill
> **Ngay tao**: {ngay-thang-nam}
> **Trang thai**: Draft | In Progress | Completed

## Tong quan

{Mo ta ngan gon ve yeu cau/tinh nang can trien khai}

## Muc tieu

- {Muc tieu 1}
- {Muc tieu 2}
- ...

## Danh sach Phase

| Phase | Ten | Mo ta | So task | Trang thai |
|-------|-----|-------|---------|------------|
| 01 | {ten} | {mo ta ngan} | {so} | Pending |
| 02 | {ten} | {mo ta ngan} | {so} | Pending |

## Thu tu thuc hien

1. [Phase 01: {ten}](./phase-01-{slug}/PHASE.md)
2. [Phase 02: {ten}](./phase-02-{slug}/PHASE.md)
...

## Ghi chu quan trong

{Cac luu y quan trong cho nguoi trien khai}
```

---

## Format file PHASE.md

```markdown
# Phase {so}: {Ten Phase}

> **Thuoc ve**: [{Ten du an}](../INDEX.md)
> **Trang thai**: Pending | In Progress | Completed

## Muc tieu phase

{Mo ta muc tieu cua phase nay}

## Phu thuoc

- **Phase truoc**: {ten phase truoc hoac "Khong"}
- **Input can co**: {cac input can co truoc khi bat dau}

## Danh sach Task

| Task | Ten | Mo ta | Do phuc tap | Trang thai |
|------|-----|-------|-------------|------------|
| 01 | {ten} | {mo ta} | Low/Medium/High | Pending |
| 02 | {ten} | {mo ta} | Low/Medium/High | Pending |

## Thu tu thuc hien

1. [Task 01: {ten}](./task-01-{slug}.md)
2. [Task 02: {ten}](./task-02-{slug}.md)

## Ket qua mong doi khi hoan thanh phase

- {Ket qua 1}
- {Ket qua 2}
```

---

## Format file task-{so}-{slug}.md

```markdown
# Task {so}: {Ten Task}

> **Phase**: [{Ten Phase}](./PHASE.md)
> **Do phuc tap**: Low | Medium | High
> **Trang thai**: Pending | In Progress | Completed

## Muc tieu

{Mo ta ro muc tieu cua task}

## Yeu cau nghiep vu

### Dau vao (Input)
- {Mo ta input 1}
- {Mo ta input 2}

### Dau ra (Output)
- {Mo ta output mong doi 1}
- {Mo ta output mong doi 2}

### Dieu kien (Constraints)
- {Dieu kien/rang buoc 1}
- {Dieu kien/rang buoc 2}

## Logic xu ly

### Buoc 1: {Ten buoc}
{Mo ta logic can thuc hien - KHONG chen code}

### Buoc 2: {Ten buoc}
{Mo ta logic can thuc hien - KHONG chen code}

## Cac truong hop dac biet (Edge Cases)

| Truong hop | Xu ly |
|------------|-------|
| {Case 1} | {Cach xu ly} |
| {Case 2} | {Cach xu ly} |

## Subtasks

### Subtask 1: {Ten subtask}
- **Mo ta**: {mo ta chi tiet}
- **Logic**: {logic can thuc hien}
- **Ket qua**: {ket qua mong doi}

### Subtask 2: {Ten subtask}
- **Mo ta**: {mo ta chi tiet}
- **Logic**: {logic can thuc hien}
- **Ket qua**: {ket qua mong doi}

## File/Module lien quan

| File/Module | Vai tro | Hanh dong |
|-------------|---------|-----------|
| {path/to/file} | {vai tro} | Create/Modify/Reference |

## Tieu chi hoan thanh (Definition of Done)

- [ ] {Tieu chi 1}
- [ ] {Tieu chi 2}
- [ ] {Tieu chi 3}

## Ghi chu cho nguoi trien khai

{Cac luu y quan trong, tips, warnings}
```

---

## Quy tac dat ten

### Thu muc phase
- Format: `phase-{so 2 chu so}-{slug}`
- Slug: chu thuong, khong dau, noi bang dash
- Vi du: `phase-01-khoi-tao-du-an`, `phase-02-xay-dung-api`

### File task
- Format: `task-{so 2 chu so}-{slug}.md`
- Vi du: `task-01-tao-database-schema.md`, `task-02-xay-dung-models.md`

### Quy tac slug
- Khong dau tieng Viet
- Chu thuong
- Thay khoang trang bang dash `-`
- Toi da 50 ky tu

---

## Muc do phuc tap (Complexity)

| Muc do | Mo ta | Thoi gian uoc tinh |
|--------|-------|-------------------|
| Low | Task don gian, logic thang | 1-2 subtask |
| Medium | Can suy nghi, nhieu buoc | 3-5 subtask |
| High | Phuc tap, nhieu edge case | 6+ subtask |

---

## Luu y quan trong

1. **Tap trung mo ta "What" va "Why"** - Khong mo ta "How to code"
2. **Ngon ngu ro rang** - Tranh mo ho, cung cap vi du cu the
3. **Chia nho hop ly** - Moi subtask nen co the hoan thanh doc lap
4. **Lien ket ro rang** - Chi ro phu thuoc giua cac task/phase
5. **Tieu chi hoan thanh** - Moi task phai co Definition of Done ro rang
