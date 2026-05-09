# Brainstorm: Testing Strategy cho Skill Suite

**Ngày:** 2026-05-09  
**Chủ đề:** Testing Strategy cho Skill Suite (skill-architect, skill-planner, skill-builder)  
**Ngôn ngữ:** Tiếng Việt

---

## 1. Testing Pyramid cho Skill Suite

```
           ┌─────────────────────┐
           │     E2E Tests       │  ← 10%
           │   (Smoke + Flow)    │
           ├─────────────────────┤
           │  Integration Tests   │  ← 30%
           │   (Pipeline Flow)   │
           ├─────────────────────┤
           │    Unit Tests       │  ← 60%
           │ (Validator, Parser, │
           │  Template Engine)   │
           └─────────────────────┘
```

### Lý do pyramid này phù hợp với Skill Suite

- **Unit (60%):** Skill suite xử lý nhiều input phức tạp (design.md, todo.md) — lỗi logic nội bộ dễ gây fail hàng loạt
- **Integration (30%):** Pipeline architect→planner→builder có strict handoff contract — cần verify data flow
- **E2E (10%):** Chỉ smoke test cho mỗi operation type, không cần cover hết edge cases ở tầng này

---

## 2. Unit Tests cho Validator v3

### 2.1 Phạm vi test

Validator v3 xử lý nhiều loại input:
- `design.md` schema validation
- `todo.md` phase breakdown validation
- Skill metadata validation
- Template placeholder validation

### 2.2 Test cases cần cover

#### Design Schema Validation
```
✅ Valid design.md → pass
✅ Missing §1 (Pain Points) → fail với message rõ ràng
✅ Missing §4 (Mermaid diagram) → fail
✅ Mermaid syntax invalid → fail với line number
✅ Missing required sections → fail với list còn thiếu
```

#### Todo Schema Validation
```
✅ Valid todo.md → pass
✅ Phase không có tasks → fail
✅ Trace tag format sai → fail (format: #T{n})
✅ Dependency cycle trong phases → fail
```

#### Skill Metadata Validation
```
✅ Valid SKILL.md frontmatter → pass
✅ Invalid YAML frontmatter → fail
✅ Missing required fields (name, version, triggers) → fail
```

### 2.3 Test structure đề xuất

```
tests/
└── unit/
    └── validator/
        ├── test_design_schema.py
        ├── test_todo_schema.py
        ├── test_skill_metadata.py
        └── test_placeholder_pattern.py
```

### 2.4 Mocking strategy

- Mock filesystem reads để test validation logic isolated
- Dùng fixture với sample design.md/todo.md ở nhiều trạng thái (valid, missing sections, invalid syntax)
- Không mock parser — unit test validator phải chạy real parsing

---

## 3. Integration Tests cho Architect→Planner→Builder Pipeline

### 3.1 Test handoff contracts

Mỗi stage có output là input của stage tiếp theo. Cần verify:

```
architect output (design.md)
    ↓ [contract: 10+ sections, Mermaid diagram]
planner input ✓
    ↓ [contract: phase breakdown, trace tags]
builder input ✓
    ↓ [contract: skill package structure]
final output ✓
```

### 3.2 Test cases cho pipeline flow

#### Happy Path
```
Test: full_pipeline_với_valid_input
1. Run skill-architect với requirement mẫu
2. Assert design.md có đủ 10 sections
3. Run skill-planner với design.md
4. Assert todo.md có phase breakdown
5. Run skill-builder với design.md + todo.md
6. Assert SKILL.md tồn tại và valid
```

#### Contract Violation Detection
```
Test: architect_output_invalid_design
1. Run skill-architect với requirement mơ hồ
2. Assert planner nhận ra design thiếu sections
3. Assert planner fail hoặc clarify chủ động
```

### 3.3 Test structure đề xuất

```
tests/
└── integration/
    └── pipeline/
        ├── test_architect_to_planner.py
        ├── test_planner_to_builder.py
        └── test_full_pipeline.py
```

### 3.4 Environment setup

- Dùng temporary directory cho mỗi test run
- Cleanup sau mỗi test để tránh state leak
- Có thể mock LLM calls với pre-recorded responses để test deterministic

---

## 4. Smoke Tests cho Mỗi Operation Type

### 4.1 Operation types trong Skill Suite

| Operation | Mô tả | Smoke test focus |
|-----------|-------|------------------|
| `skill-architect.analyze` | Phân tích requirement | Output có design.md |
| `skill-architect.design` | Tạo Mermaid diagram | Diagram parse được |
| `skill-planner.audit` | Audit tài nguyên | Output có resource assessment |
| `skill-planner.plan` | Tạo phase breakdown | Phase có tasks |
| `skill-builder.prepare` | Đọc inputs | Không raise exception |
| `skill-builder.build` | Generate skill files | Files tồn tại |
| `skill-builder.verify` | Quality gate check | Pass/fail rõ ràng |

### 4.2 Smoke test template

```python
def test_smoke_skill_architect_analyze():
    """Smoke test: architect.analyze với sample requirement"""
    result = skill_architect.analyze("Build a file organizer skill")
    
    assert result is not None
    assert hasattr(result, 'design')
    assert 'design.md' in result.files_created
```

### 4.3 Criteria cho smoke test

- **Runtime:** < 30s mỗi test
- **Coverage:** Chỉ happy path, không edge cases
- **Deterministic:** Luôn pass hoặc fail consistent
- **Fast fail:** Nếu smoke fail → không chạy integration

---

## 5. Test Coverage Targets

### 5.1 Coverage matrix

| Component | Target | Priority |
|-----------|--------|----------|
| Validator v3 | 90% | P0 |
| Parser (Mermaid, YAML) | 85% | P0 |
| Template engine | 80% | P1 |
| Handoff contract validation | 95% | P0 |
| Skill file generator | 75% | P1 |

### 5.2 Coverage goals by test type

```
Unit Tests:
- Validator: 90% line coverage
- Parser: 85% line coverage
- Template: 80% line coverage

Integration Tests:
- Pipeline flow: 100% happy path covered
- Contract violations: 80% scenarios covered

E2E/Smoke:
- All operation types: 100% covered
- All skill types: At least 1 smoke per skill
```

### 5.3 Quality gates

| Gate | Threshold | Action if fail |
|------|-----------|----------------|
| Unit coverage | < 80% | Block merge |
| Integration pass rate | < 95% | Block merge |
| Smoke pass rate | < 100% | Alert, block deploy |
| Validator accuracy | < 95% | Investigate |

---

## 6. Testing Tools & Framework

### 6.1 Đề xuất stack

- **pytest** — test runner chính
- **pytest-cov** — coverage reporting
- **pytest-mock** — mocking
- **pytest-asyncio** — async test support (nếu cần)

### 6.2 CI/CD integration

```
GitHub Actions:
├── unit-tests.yml      # Chạy on PR, coverage report
├── integration-tests.yml # Chạy on PR, full pipeline
└── smoke-tests.yml     # Chạy on merge to main
```

---

## 7. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| LLM output non-deterministic | High | Mock LLM calls trong unit/integration, chỉ dùng real LLM ở smoke |
| Complex pipeline state | Medium | Use temporary directories, strict cleanup |
| Validator false positives | Medium | 2-person review cho validator rules |
| Coverage targets quá cao | Low | Bắt đầu với 70%, tăng dần |

---

## 8. Next Steps

1. **Immediately:** Thiết lập test directory structure
2. **Week 1:** Viết unit tests cho validator v3 (P0)
3. **Week 2:** Viết integration tests cho architect→planner
4. **Week 3:** Viết smoke tests cho tất cả operation types
5. **Week 4:** Setup CI/CD và coverage reporting

---

*Document được tạo trong quá trình brainstorm testing strategy cho skill suite.*