# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
- **AI-02.1:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03:** CLOSED / STRUCTURALLY ACCEPTED / C01..C33 / B01..B35 / MAT-01..MAT-15
- **AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04A:** CLOSED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / RT-01..RT-31
- **AI-04C:** CLOSED / PA-01..PA-61
- **AI-04 whole-phase:** CLOSED / WP-01..WP-22
- **PRE-AI05 hardening:** CANDIDATE / PRE05-H01..H16
- **First post-materialization retest:** FAIL BOUNDED / H15-H16 ADDED
- **Full retest after H15-H16:** NOT YET EXECUTED
- **AI-05:** FUTURE / NEXT ONLY AFTER PRE-AI05 PASS + CURRENT-TRUTH RECONCILIATION
- **Implementation claim:** NONE
- **Provider/model selection:** OPEN / EVIDENCE-DRIVEN
- **Commercial packaging:** OPEN / ENTITLEMENT BOUNDARY ONLY
- **Merge status:** UNMERGED

Repository truth outranks conversation memory.

---

## 1. Current compact roadmap

```text
AI-00  Semantic & Product Foundation                    COMPLETE
AI-01  Product Form + Production Engineering Research    COMPLETE
AI-02  Intelligence Runtime Architecture                 CLOSED
AI-03  Context / Retrieval / Memory                      CLOSED
AI-04  Productionization Architecture                    CLOSED STRUCTURALLY

CURRENT
PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
  PRE05-H01..H16 candidate
  first retest FAIL bounded
  full retest required after H15-H16

THEN IF PASS
GLOBAL CURRENT-TRUTH RECONCILIATION

THEN
AI-05  Whole-System Acceptance + Implementation Blueprint

THEN
actual AI implementation workstream(s)
```

No architecture closure implies implementation/provider PASS.

---

## 2. Current mandatory AI authority

```text
docs/architecture/dante-ai-foundation.md
docs/architecture/ai-production-engineering-state-of-the-art-2026.md
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/architecture/dante-ai-04-productionization-architecture.md
docs/architecture/dante-ai-04a-direct-eval-specification.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md
docs/architecture/dante-ai-pre05-cross-phase-hardening.md   CURRENT CANDIDATE SUPPLEMENT
```

Temporary branch continuity:

```text
docs/workstreams/ai-architecture-live-handoff.md
MUST NOT MERGE TO PROTECTED main
```

---

## 3. Accepted upstream foundation

```text
Product / North Star         CURRENT
Domain                       CLOSED
Logical                      CLOSED / 57 OF 57 / WL-H01..WL-H12
Physical                     CLOSED
PostgreSQL                   18.6 / sole canonical persistence + material-history authority
Alembic                      20260830_09
DB topology                  69 tables / 5 views / 15 routines / 76 triggers /
                             97 indexes / 69 FKs / 123 CHECKs
Recovery                     CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED
remote backup provider       TBD / NOT ACTIVATED
production/cloud recovery    NOT CLAIMED
```

No AI convenience creates a second canonical database or generic universal Fact/Memory root.

---

## 4. Retained semantic/runtime invariants

```text
Interaction Session != Run != Worker
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
DISPLAY NAME != EFFECT TARGET
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SCENARIO STATE != CANONICAL CURRENT STATE
CONTEXT ACCESS != DISCLOSURE PERMISSION
APPROVAL != PERPETUAL AUTHORIZATION
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
SAFE SINGLE DISCLOSURE != SAFE CUMULATIVE DISCLOSURE
AUTONOMY != AUTHORITY != AUTHZ != APPROVAL
```

AI-02 also owns Attention/aggregate attention budgeting, causal-loop/oscillation protection, surface-aware disclosure and cumulative/cross-query protection.

---

## 5. AI-04 base closure

```text
AI-04A  DANTE-E01..E13 / A01..A30 / EV01..EV20
AI-04B  RT-01..RT-31
AI-04C  PA-01..PA-61
WHOLE   WP-01..WP-22
```

Core route/provider rules:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
EVAL CANDIDATE != PRODUCTION ROUTE
fallback independently qualifies
route selection/context assembly != egress authorization
ENTITLED != SERVABLE
model picker != routing Authority
```

---

## 6. PRE-AI05 candidate hardening

Durable candidate:

```text
docs/architecture/dante-ai-pre05-cross-phase-hardening.md
```

```text
H01 AttentionBudget != ResourceBudget != commercial/provider quota
H02 trigger fired != material change/current work eligibility
H03 causal-loop / oscillation safety is production-critical
H04 DANTE-E14 proactive/Attention/loop safety is core eval
H05 cumulative disclosure may span related work
H06 recipient != surface != channel
H07 scoped autonomy is policy ceiling, not Authority/AuthZ/approval
H08 evaluate unsafe autonomy separately from excessive over-asking
H09 current-tree executable eval coverage E01..E14
H10 AI-01 old ModelTarget shorthand is historical terminology
H11 WP route composition outranks older AI-04B local sequence
H12 old pre-Physical AI/context boundary is historical in current navigation
H13 formal IFC/leakage-budget/ACS mechanisms remain challengers
H14 commercial tier cannot buy weaker attention/autonomy/privacy safety
H15 AttentionDecision != proactive Work Admission != Effect authorization
H16 cumulative disclosure may span Runs/Interactions/surfaces/known related sinks
```

First post-materialization retest found H15-H16. No PASS claim is allowed until the full chain is restarted and passes.

---

## 7. Current eval workload contract

The current tree now carries implementation-readable coverage through the PRE-AI05 supplement:

```text
E01 deterministic/model avoidance
E02 target resolution
E03 extraction
E04 query/history/absence
E05 context/privacy/cumulative disclosure
E06 planning/replanning/scenario
E07 documents/long-context/multimodal
E08 tool/capability use
E09 consequential effect/scoped autonomy
E10 multi-actor/delegation/surface disclosure
E11 adaptive memory/learning
E12 failure/currentness/supersession/failover
E13 open-world research/grounding
E14 proactivity/Attention/causal-loop safety
```

Hard failures remain non-averageable.

---

## 8. Commercial/service-tier boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ eligible route set
```

Commercial tiers cannot weaken truth, privacy, Authority, target safety, provider/data eligibility, reconciliation, scoped autonomy or Attention/disclosure policy.

Names/prices/quotas remain OPEN.

---

## 9. Direct proof obligations remain distinct

Still unexecuted where applicable:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query
PSV-08 / SC-019 vector recall after filtering
PSV-09 / SC-020 projection freshness/material basis
PSV-10 / SC-021 deletion/redaction propagation
PSV-21..28B durable execution / Restate / journal privacy / recovery
PSV-37 pgvector source/model/freshness provenance
```

No implementation PASS is claimed.

---

## 10. Current exact action

```text
RESTART FULL AI-01→AI-04 DESTRUCTIVE RETEST FROM ZERO
→ reverse-order retest
→ refreshed state-of-the-art regression check
```

Required focus includes:

```text
AttentionDecision vs Work admission
cross-Run/cross-surface cumulative disclosure
scoped autonomy/current authorization
proactive loop safety
AI-03 lifecycle + AI-04 provider/cache/failover
whole-phase route composition
commercial/resource pressure without safety downgrade
```

If PASS:

```text
mark PRE-AI05 hardening accepted
→ global current-truth reconciliation
→ AI-05 current
```

If FAIL, reopen only the smallest affected boundary.

---

## 11. Decisions still open

```text
provider/model set and SDKs
direct provider benchmark results / eval runner
exact runtime modules/contracts
Attention implementation/state persistence if any
cumulative-disclosure enforcement algorithm / persistence if any
formal IFC / leakage-budget / ACS adoption
control-plane physical topology
commercial names/prices/quotas / billing
AI gateway / guardrail / secret-manager products
MCP/A2A activation
Execution Environment technology
Restate / R2 / pgvector / ANN / FTS activation
production regions/residency mappings
```

Do not preselect them without applicable evidence.

---

## 12. Live handoff policy

`docs/workstreams/ai-architecture-live-handoff.md` is temporary and MUST NOT merge to protected `main`.

Before integration:

```text
propagate durable truth
→ verify coverage
→ DELETE live handoff
```
