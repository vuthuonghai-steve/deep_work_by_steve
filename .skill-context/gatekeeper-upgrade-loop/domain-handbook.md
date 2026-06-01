# Technical Handbook: Dynamic Quality Gates Synthesis Framework
*Enabling Heavy Thinking and Deliberation in Production Quality Gatekeeping*

---

## §1. Core Philosophy: Dynamic Quality Gates vs. Static Checklists
According to the **Karpathy Standards Handbook** (Kỷ luật — Trung thực — Sáng tạo) and the **Heavy Thinking Framework** (arXiv:2605.02396):
1. **Dynamic Quality Gates Synthesis** represents a shift from *syntactic correctness* to *semantic/business correctness*.
2. When an AI Agent is tasked with writing code, it must not be measured by generic rules (PEP 8, word counts, formatting) that are completely blind to the actual task. Instead, the system must **dynamically synthesize a customized Quality Matrix** representing the precise high-fidelity business invariants, structural patterns, and security boundaries required by the specific task.
3. This synthesis is powered by a **2-Stage Heavy Thinking Pipeline** operating within the gatekeeper:
   - **Parallel Reasoning (Stage 1)**: Formulate $K$ independent analytical chains (different perspectives of risk, edge cases, data structures, and failure patterns for the target task).
   - **Deliberation (Stage 2)**: Combine these chains, analyze their logic, filter out AI hallucinations, and synthesize the **Final Dynamic Quality Gates Matrix** containing 5-10 targeted business gates.

---

## §2. System Architecture: Dynamic Synthesis Pipeline

```
USER INPUT / ARCHITECT DESIGN
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 0.5: K-CHAIN PARALLEL REASONING                  │
│  Generate K=8 independent chains analyzing:             │
│  - Threat model & security boundaries                   │
│  - Business invariants & domain logic                   │
│  - Transactional safety & concurrency hazards           │
│  - Error handling & resilience patterns                 │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼ (K Chains cached)
┌─────────────────────────────────────────────────────────┐
│  STAGE 0.5: DELIBERATION ENGINE                         │
│  - Merges and filters K chains                          │
│  - Synthesizes 5-10 task-specific High-Fidelity Gates    │
│  - Generates custom programmatic check configurations   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
 📊 DYNAMIC QUALITY MATRIX (data/dynamic-gates.yaml)
 └── Custom business/security gates tailored *only* to this task!
```

### The K=8 Parallel Reasoning sweet spot
To synthesize high-fidelity gates without confirmation bias, the Gatekeeper leverages K=8 independent chains:
1. **Chain 1**: Threat Modeling (OWASP Top 10, Data Exfiltration, Spoofing, Signature Verifications).
2. **Chain 2**: ACID & Concurrency (Race conditions, dirty reads, distributed locks, double spend, replay attacks).
3. **Chain 3**: Invariant Mapping (State machine validation, range limits, data structures integrity).
4. **Chain 4**: Resiliency & Protocol (Retries, backoffs, timeouts, circuit breakers, dead-letter queues).
5. **Chain 5**: Performance & Memory (Connection pooling, cache invalidation, chunked streaming, leaks).
6. **Chain 6**: API / Protocol compliance (REST/GraphQL schema compliance, idempotency keys).
7. **Chain 7**: Observability & Audit (Structured logging, telemetry tags, sensitive data masking).
8. **Chain 8**: Exceptional Path Isolation (Zero-state, corrupted payloads, timeout recoveries).

The **Deliberation Engine** acts as the critic, merging these vectors into 5-10 explicit, testable, high-fidelity gate specifications.

---

## §3. The 5-10 Dynamic Business & Security Gates: Taxonomy & Synthesis Specs
For any developer task, the Gatekeeper must dynamically synthesize 5-10 gates matching the following taxonomy:

### 1. Webhook Signature & Authenticity Gates
- **Synthesized Check**: Must verify signature authenticity (e.g., Stripe, Shopify webhook signatures).
- **Programmatic AST Check**: Enforce `stripe.Webhook.construct_event` (or library equivalent) wrapped in exception handlers.

### 2. Idempotency & Replay Attack Gates
- **Synthesized Check**: Every mutations/financial debit API must enforce an idempotency check (e.g., using `Idempotency-Key` headers or database level constraints).
- **Programmatic AST Check**: Ensure the API parses an idempotency header and queries a key-store or DB uniquely before fulfillment.

### 3. Transactional Consistency & Atomic State Gates
- **Synthesized Check**: State transitions must be atomic.
- **Programmatic AST Check**: Ensure use of database transaction blocks (`transaction.atomic()`, `with session.begin()`, etc.) whenever multiple writes/updates occur.

### 4. Zero-Leak Memory & Log Scrubbing Gates
- **Synthesized Check**: Sensitive user data (PII, tokens, credit card CVVs) must not be printed to stdout/logs or stored in plaintext.
- **Programmatic AST Check**: Verify that logging calls do not pass variables matching sensitive regex patterns, and check that model properties utilize encryption or hashing.

### 5. Algorithmic Edge-Case/Invariant Gates
- **Synthesized Check**: Domain-specific bounds must be mechanically verified (e.g., transaction value must be positive, pagination page size must be capped).
- **Programmatic AST Check**: Enforce parameter assertion guards (`assert`, `raise ValueError`) at the entry boundary.

---

## §4. Programmatic Verification Mechanics
To verify these dynamic gates, the new gatekeeper does not use a hardcoded python file. Instead, it generates a **dynamic verification script** (`scripts/dynamic_critic.py`) alongside `data/dynamic-gates.yaml`. 

This script reads the synthesized rules and parses the target code using AST (Abstract Syntax Trees) to verify:
1. **Required imports**: The specific security packages imported.
2. **Control structures**: Critical lines wrapped in `try-except` blocks.
3. **Database constructs**: Database queries encapsulated inside transaction contexts.
4. **Keyword/Semantic logic**: Targeted checking of domain rules.

### Anti-Hallucination and Honesty Rules
1. **No speculation**: If the dynamic gates require a Stripe signature verification, the programmatic critic must look for exact AST structures matching `stripe.Webhook`. It must *never* guess or assume.
2. **Failure explanation**: If a gate fails, the critic outputs clear, surgical directions detailing the precise line and logic that was breached, along with Karpathy-compliant advice (no speculative code rewriting).

---
*Handbook completed by Stage 0.5 (Skill Knowledge Miner).*
*Stored under: `/home/steve/Work-space/deep_work_by_steve/.skill-context/gatekeeper-upgrade-loop/domain-handbook.md`*
