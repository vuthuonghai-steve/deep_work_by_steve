# Skill Suite Pipeline — Knowledge Extraction

**Extracted from:** Current session
**Date:** 2026-05-08
**Category:** experience

---

## Overview

Quy trình xây dựng Agent Skill bài bản qua 3-stage pipeline: Architect → Planner → Builder, với spec-generator như một công cụ bổ trợ độc lập.

---

## Key Insights

### Insight 1: Pipeline-Driven Development

**What:** Cách tiếp cận xây dựng skill theo pipeline với sự phân tách rõ ràng giữa design, planning, và implementation.

**Why:** Mỗi stage có focus riêng, giảm cognitive load và đảm bảo chất lượng ở mỗi bước.

**Context:** Khi xây dựng bộ skill cho deep_work_by_steve, cần một quy trình có hệ thống để đảm bảo consistency.

### Insight 2: 7 Zones Structure

**What:** Mọi skill đều follow 7-zone structure: Core, Knowledge, Scripts, Templates, Data, Loop, Assets.

**Why:** Chuẩn hóa cấu trúc giúp AI dễ navigate và user dễ maintain.

**Context:** Từ shared framework `_shared/knowledge/framework.md`.

### Insight 3: Progressive Disclosure

**What:** 3-tier loading system: Tier 1 (mandatory boot), Tier 2 (conditional), Tier 3 (on-demand).

**Why:** Tránh overload context window, chỉ load file thực sự cần thiết cho từng phase.

**Context:** Áp dụng trong tất cả 4 skills của bộ rebuild.

### Insight 4: Traceability via Tags

**What:** Mọi task/requirement đều phải có trace tag: `[TỪ DESIGN §N]`, `[GỢI Ý BỔ SUNG]`, `[TỪ AUDIT TÀI NGUYÊN]`, `[CẦN LÀM RÕ]`.

**Why:** Đảm bảo mọi thứ có nguồn gốc rõ ràng, không hallucinate.

**Context:** Anti-hallucination rule trong framework.

---

## Lessons Learned

### Lesson 1: Hardcoded Paths are OK for MVP

**Situation:** Cần specify knowledge base path ngay lập tức cho session-learner skill.

**Learning:** Với initial version, hardcoded path `/home/steve/Work-space/deep_work_by_steve/knowledge/` là acceptable. Có thể refactor thành config sau.

**Action:** Khi xây dựng skill mới, đánh dấu hardcoded parts với TODO comment để track.

### Lesson 2: Pipeline là cách tốt để structure complex tasks

**Situation:** User muốn tạo một skill phức tạp nhưng không biết bắt đầu từ đâu.

**Learning:** Pipeline approach (Architect → Planner → Builder) chia nhỏ thành từng bước manageable, mỗi bước có gate confirmation.

**Action:** Với mọi complex task, suggest breaking down thành pipeline thay vì attempt tất cả một lần.

---

## Related

- [[Master Framework — Shared Knowledge Base]]
- [[skill-architect documentation]]
- [[skill-builder documentation]]

---

## Source

Session: 2026-05-08 deep_work_by_steve workspace setup + skill suite review
