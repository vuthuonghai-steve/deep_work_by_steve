# Brainstorm: Migration Strategy v2.x → v3.0

> Ngày: 2026-05-09
> Ngôn ngữ: Tiếng Việt

---

## 1. Breaking Changes trong v3.0

### 1.1 API Changes

- **Authentication**: JWT token format thay đổi từ HS256 sang RS256
- **Endpoints**: REST API v2.x deprecated → `/api/v3/` endpoints mới
- **Response format**: JSON structure thay đổi (bổ sung field `metadata`)
- **Rate limiting**: Headers và status codes khác biệt

### 1.2 Configuration Schema

- Config file format: `config.yaml` → `config.toml`
- Environment variables prefix: `APP_` → `V3_`
- Database schema: Migration required cho 3 tables (users, sessions, logs)

### 1.3 Dependencies

- Node.js version: 14.x → 20.x LTS (required)
- Breaking changes trong 5+ npm packages cốt lõi
- Go modules version: v1.x → v2.x

### 1.4 Behavioral Changes

- Background jobs: Synchronous → Asynchronous queue
- Caching strategy: In-memory → Redis cluster
- Error handling: Exception-based → Error codes

---

## 2. Backward Compatibility Approach

### 2.1 Dual Mode Operation

```
┌─────────────────────────────────────────┐
│         API Gateway (v3.0)              │
│                                         │
│   /api/v2/*  →  Compatibility Layer     │
│                 (transform + forward)   │
│                                         │
│   /api/v3/*  →  Native v3 handlers      │
└─────────────────────────────────────────┘
```

### 2.2 Adapter Pattern

| Component | Adapter Strategy |
|-----------|-----------------|
| Auth | JWT adapter: decode v2 + encode v3 |
| Config | Config transformer: TOML ↔ YAML converter |
| Database | ORM layer: handle schema diff |
| API | Response transformer: inject metadata |

### 2.3 Feature Flags

```python
FEATURE_FLAGS = {
    "v3_native_endpoints": False,  # Enable sau M2
    "new_auth_flow": False,         # Enable sau M3
    "async_jobs": False,            # Enable gradually
}
```

---

## 3. Migration Phases

### Phase M1: Foundation (Week 1-2)

**Mục tiêu:** Infrastructure preparation

- [ ] Provision v3.0 environment (staging)
- [ ] Run database migration scripts
- [ ] Deploy API gateway với dual-mode
- [ ] Setup monitoring: Prometheus + Grafana

**Exit Criteria:**
- v3.0 staging accessible
- v2.x fallback operational
- Zero downtime deployment verified

### Phase M2: Shadow Mode (Week 3-4)

**Mục tiêu:** Parallel run, validate outputs

- [ ] Route 10% traffic qua v3.0 (canary)
- [ ] Compare response consistency v2 vs v3
- [ ] Capture diff metrics
- [ ] Fix critical bugs discovered

**Exit Criteria:**
- <1% response divergence
- P99 latency <200ms
- No data integrity issues

### Phase M3: Cutover (Week 5-6)

**Mục tiêu:** Full production migration

- [ ] Redirect 50% → 100% traffic
- [ ] Enable v3-native feature flags
- [ ] Decommission v2.x compatibility layer
- [ ] Update client SDK versions

**Exit Criteria:**
- 100% v3 traffic
- v2.x deprecated notices sent
- Documentation updated

---

## 4. Risk Assessment & Mitigation

### Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|------------|
| Data loss during DB migration | Medium | Critical | Full backup + point-in-time recovery |
| Auth failures post-migration | High | High | Parallel auth run + rollback trigger |
| Performance regression | Medium | Medium | Baseline benchmarks + load testing |
| Client SDK compatibility | Low | Medium | Compatibility layer + SDK update guide |
| Config parsing failures | Low | High | Schema validation + dry-run testing |

### 4.1 Data Migration Risk

```
Mitigation Steps:
1. Create DB snapshot before migration
2. Run migration in transaction (rollback on failure)
3. Validate data integrity post-migration
4. Setup streaming replication to v3 DB
```

### 4.2 Authentication Risk

```
Mitigation Steps:
1. Maintain v2 JWT validation in parallel
2. New tokens issued in both formats during transition
3. Token refresh mechanism for seamless switch
4. Emergency: Revert to v2 auth provider
```

### 4.3 Performance Regression Risk

```
Mitigation Steps:
1. Pre-migration: Load testing với target 10x peak load
2. Real-time: APM monitoring (DataDog/NewRelic)
3. Circuit breaker: Auto-fallback khi error rate >5%
4. Manual approval gate trước M3
```

---

## 5. Rollback Plan

### Rollback Triggers

- Error rate tăng >10% so với baseline
- P99 latency tăng >50%
- Data corruption detected
- Critical business logic failure

### Rollback Procedure

```
Step 1: Stop v3 traffic (flip switch)
        ↓
Step 2: Enable v2-only mode trong API Gateway
        ↓
Step 3: Restore DB from snapshot (if needed)
        ↓
Step 4: Verify v2.x functionality
        ↓
Step 5: Post-mortem analysis
        ↓
Step 6: Plan v3 fix + re-migration
```

### Rollback Timeline

| Action | Duration | Owner |
|--------|:--------:|-------|
| Decision to rollback | 5 min | Tech Lead |
| Traffic switch | 2 min | DevOps |
| DB restoration | 15 min | DBA |
| Verification | 10 min | QA |
| **Total Maximum** | **32 min** | |

### Emergency Contacts

- Primary: [Tech Lead Name]
- Secondary: [DevOps Lead Name]
- Escalation: [CTO/VP Engineering]

---

## 6. Communication Plan

### Internal

- Weekly status updates (Slack #migration-updates)
- Daily standup: migration progress
- Blocker escalation: immediate paged

### External Stakeholders

- 2 weeks notice: Deprecation email
- 1 week notice: Migration timeline
- Day-of: Status page update
- Post-migration: Success announcement

---

## 7. Success Metrics

| Metric | Target | Measurement |
|--------|:------:|-------------|
| Downtime | 0 min | Uptime monitoring |
| Error rate | <0.1% | APM dashboard |
| Latency P99 | <150ms | APM dashboard |
| Data integrity | 100% | Validation scripts |
| Rollback count | 0 | Incident log |

---

**Document Status:** Draft v1.0
**Next Review:** 2026-05-12