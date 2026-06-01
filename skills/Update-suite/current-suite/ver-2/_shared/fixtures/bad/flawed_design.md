# ===========================================================================
# FL Flawed Design Fixture violating ARC-03 (Zone Mapping Placeholders)
# ===========================================================================

# §1. Problem Statement
We need a dynamic billing system.

# §2. Capability Map
- Handle payments

# §3. Zone Mapping
| Zone | Files cần tạo | Nội dung | Bắt buộc? |
|------|--------------|----------|-----------|
| Core | `SKILL.md` | Persona | Yes |
| Scripts | `scripts/xxx.py` | Placeholder script | Yes |  # Violates ARC-03 (Contains "xxx" placeholder!)
| Knowledge | `...` | Missing details | Yes |       # Violates ARC-03 (Contains "..." placeholder!)
