# Error Recovery Procedures

> Usage: Load when errors or hallucinations detected
> Purpose: Guide AI to recover gracefully from failures

---

## Error Detection Triggers

AI detect loi khi:
- Verification loop FAIL
- User reject design
- Context corruption (file not found, parse error)
- Hallucination detected (claim khong co source)
- Token overflow (context > 80%)
- Confidence score < 50 sau khi da hoi them

---

## Recovery Procedures

### Type 1: Verification FAIL

**Detection**: Self-check phat hien thieu section, placeholder, hoac inconsistent.

**Recovery**:
1. Identify specific issues tu verification output
2. Fix tung issue mot
3. Re-run verification loop
4. Neu khong fix duoc → trigger Type 2 (rollback)

---

### Type 2: User Reject

**Detection**: User tu choi mot phan hoac toan bo design.

**Recovery**:
1. Xac dinh phase nao bi reject
2. Rollback ve phase do:
   - Phase 1 reject → Reset §1 + §10, thu thap lai
   - Phase 2 reject → Reset §2 + §3 + §8, phan tich lai
   - Phase 3 reject → Reset §4-§7 + §9 + §11-§14, giu §2+§3+§8
3. Neu reject vi scope qua lon → offer degradation (Pattern 5)

---

### Type 3: Context Corruption

**Detection**: File not found, parse error, hoac missing references.

**Recovery**:
1. Reload Tier 1 files (SKILL.md, architect.md, checklist)
2. Bo qua cache, re-initiate tu dau phase hien tai
3. Neu van loi → thong bao user ve corrupted file

---

### Type 4: Hallucination Detected

**Detection**: Claim khong trace duoc ve source.

**Recovery**:
1. Trace claim ve source reference
2. Neu tim duoc source → update reference
3. Neu khong tim duoc source → remove claim hoac mark as [NEEDS VERIFICATION]
4. Neu nhieu claim bi hallucinate → trigger Type 2 (rollback phase)

---

### Type 5: Token Overflow

**Detection**: Context window > 80% hoac > 95%.

**Recovery**:
1. Chay compress_context.py
2. Drop non-essential Tier 2 files
3. Switch sang summary mode
4. Neu van > 95% → offer split task thanh nhieu skill nho hon

---

### Type 6: Low Confidence

**Detection**: Confidence score < 50 sau khi da hoi them va redesign.

**Recovery**:
1. Thong bao user ve low confidence
2. Offer alternatives:
   - Thu thap them thong tin tu user
   - Giam scope (degradation)
   - Split thanh nhieu skill don gian hon
3. Khong bao gio deliver design voi confidence < 50

---

## Graceful Degradation

Khi skill gap van de khong recover duoc:

1. **Thong bao user** ve issue cu the
2. **Offer alternatives**:
   - Simplify scope
   - Split into multiple skills
   - Manual design with AI assistance
3. **Never deliver** incomplete hoac incorrect design.md
4. **Ghi nhan** issue vao progress.txt de cai thien trong tuong lai

---

## Emergency Rollback

**Trigger**: Phat hien loi nghiem trong trong design da xuat.

**Procedure**:
1. Dung ngay lap tuc
2. Thong bao user ve loi phat hien
3. Xac dinh phase gay ra loi
4. Rollback ve phase do
5. Tiep tuc lai tu dau phase do
