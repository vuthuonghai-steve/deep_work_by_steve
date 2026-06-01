# Upgraded Quality Matrix & Test Verification Plan

This matrix defines the test cases, expected criteria, verification commands, and exit criteria for validating the redesigned **Dynamic Quality Gates Synthesis** engine itself.

---

## §1. Programmatic Test Scenarios & Invariants

We verify the upgraded Gatekeeper engine by supplying it with three complex, high-fidelity real-world tasks and validating that it synthesizes correct gates and makes correct pass/fail verdicts on target drafts.

### Scenario 1: Stripe Payment Integration (Financial/Security Domain)
* **Goal**: Validate that the synthesizer generates webhook signature gates and idempotency requirements, and that the critic correctly flags insecure code.
* **Test Draft A (Insecure PEP 8 Compliant Code)**:
  - Has perfect docstrings, camelCase, snake_case formatting.
  - *Vulnerability*: Lacks Stripe webhook signature checks (`construct_event`), lacks idempotency keys, updates DB without transactions.
  - **Expected Verdict**: **FAIL** (Specifically reports missing Stripe signature block and idempotency validation).
* **Test Draft B (Secure Production Code)**:
  - Implements signature checks, transactions, and unique keys.
  - **Expected Verdict**: **PASS** (100% score).

### Scenario 2: High-Performance Concurrent Async Downloader (Concurrency Domain)
* **Goal**: Verify that concurrent safety and lock syncing gates are synthesized and evaluated.
* **Test Draft A**: Lacks thread safety/mutex locks when updating a shared queue/counter state.
  - **Expected Verdict**: **FAIL** (Reports concurrency race hazard).
* **Test Draft B**: Implements explicit context-manager lock limits (`asyncio.Lock()` or `threading.Lock()`).
  - **Expected Verdict**: **PASS**.

### Scenario 3: PII Data Sanitizer & Logger (Privacy/Security Domain)
* **Goal**: Verify log scrubbing and memory leaks prevention.
* **Test Draft A**: Prints raw user email and password directly to console/logs (`logger.info(f"User login: {email} / {password}")`).
  - **Expected Verdict**: **FAIL** (Reports raw PII logging vulnerability).
* **Test Draft B**: Scrubs data before logging and utilizes encryption/hashes.
  - **Expected Verdict**: **PASS**.

---

## §2. Verification Matrix Table

| Test Case ID | Domain Focus | Input Task Intent | Draft Code Shape | Synthesized Quality Gate Check | Expected Verdict (Exit Code) |
| --- | --- | --- | --- | --- | --- |
| **TC-GATE-01** | Stripe/Fintech | Webhook transaction event fulfillment. | PEP8 Style compliant but lacks signature check, idempotency check, or atomic write context. | - Webhook Signature Authenticity Gate<br/>- Idempotency Key Gate<br/>- DB Atomic Transaction Gate | **FAIL (Exit 1)** with feedback on missing Stripe imports & signature blocks |
| **TC-GATE-02** | Stripe/Fintech | Webhook transaction event fulfillment. | Implements Stripe webhook signature construction, atomic DB writes, and unique key validation. | - Webhook Signature Authenticity Gate<br/>- Idempotency Key Gate<br/>- DB Atomic Transaction Gate | **PASS (Exit 0)** |
| **TC-GATE-03** | Concurrency | Asynchronous job pipeline with shared count tracking. | Loops writing directly to shared array in threaded worker without locks. | - Concurrency Synchronization Gate (Mutex/Lock) | **FAIL (Exit 1)** indicating race hazard on shared variable |
| **TC-GATE-04** | Privacy | PII data management API endpoint. | Plaintext print or unencrypted log of variables matching email/pass/cvv patterns. | - PII / Secrets Log Leak Protection Gate | **FAIL (Exit 1)** highlighting PII log leak |

---

## §3. Mechanical Validation Scripts

The test suite will execute the following assertions inside our integration environment to verify the new gatekeeper design:

```bash
# 1. Run the gate synthesizer on the Stripe intent
python3 scripts/gate_synthesizer.py --task "Stripe webhook integration" --out data/dynamic-gates.yaml

# Assert 1: Verify data/dynamic-gates.yaml has synthesized gates specifically for Stripe
grep -q "stripe.Webhook" data/dynamic-gates.yaml && echo "Synthesizer PASSED" || echo "Synthesizer FAILED"

# 2. Run the dynamic critic on a styled but highly insecure Stripe webhook handler
python3 scripts/dynamic_critic.py --gates data/dynamic-gates.yaml --input tests/draft_insecure_stripe.py

# Assert 2: Verify it exits with code 1 (failure) and writes feedback.yaml
if [ $? -eq 1 ] && [ -f .skill-context/production-quality-gatekeeper/feedback.yaml ]; then
    echo "Critic correctly flagged insecure code (PASSED)"
else
    echo "Critic failed to flag insecure code (FAILED)"
fi
```

---
*Quality Matrix completed by Stage 2 (Quality Gatekeeper Upgrade verification).*
*Stored under: `/home/steve/Work-space/deep_work_by_steve/.skill-context/gatekeeper-upgrade-loop/quality-matrix.md`*
