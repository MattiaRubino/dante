# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** POST-AI-04 GLOBAL CURRENT-TRUTH RECONCILIATION
- **AI-04 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04A:** CLOSED / A01..A30 / EV01..EV20 / DIRECT PROVIDER EVIDENCE NOT EXECUTED
- **AI-04B:** CLOSED / RT-01..RT-31
- **AI-04C:** CLOSED / PA-01..PA-61
- **AI-04 whole-phase:** CLOSED / WP-01..WP-22
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-05:** NEXT AFTER GLOBAL RECONCILIATION
- **Refreshed:** 2026-09-02
- **AI-04 closure PRE-SCOPE:** `57d9b6b325d0873e46efbe88eee646f994027d2d`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` remains active.

Repository truth outranks this handoff.

The complete pre-closure handoff/workstream state is preserved at commit `57d9b6b325d0873e46efbe88eee646f994027d2d`.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     GLOBAL CURRENT-TRUTH RECONCILIATION
next        AI-05 Whole-System Acceptance + Implementation Blueprint
then        actual AI implementation workstream(s)
```

Closed architecture:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
AI-04A         CLOSED / A01..A30 / EV01..EV20
AI-04B         CLOSED / RT-01..RT-31
AI-04C         CLOSED / PA-01..PA-61
AI-04 whole    CLOSED / WP-01..WP-22
AI-04 overall  CLOSED / STRUCTURALLY ACCEPTED
```

Do not restart AI-02/03/04 redesign without concrete contradictory downstream evidence.

---

# 2. Mandatory AI authority

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
```

For AI-05 and any conclusion touching persistence/semantics, also inspect Product/North Star, Domain, Whole Logical/WL-H01..H12, Physical, CP6/PostgreSQL Constitution, current Alembic/DB truth, Recovery, Access/Home/current app workstreams and PSV obligations directly.

---

# 3. AI-04 closure truth

Accepted invariants:

```text
A01..A30
EV01..EV20
RT-01..RT-31
PA-01..PA-61
WP-01..WP-22
```

Key whole-phase rules:

```text
EVAL CANDIDATE != PRODUCTION ROUTE
HARNESSPROFILE != PROVIDERBINDING
routing selects compatible qualified Harness+Binding composition
fallback independently qualifies
auxiliary/sub-model inference is governed first-class
route selection/context assembly != egress authorization
fallback capability contraction != silent context truncation
capability version N != automatic version N+1 compatibility
CACHE HIT != Harness/tool/security/Auth continuity
operational behavior must preserve hidden-result non-interference
model picker/preference != routing Authority
route selection + resource admission must be coherent
per-invocation coherent snapshot != whole-Run immutable config
DIRECT EVAL != PRODUCTION CAPACITY QUALIFICATION
```

Provider/model selection remains OPEN.

---

# 4. Commercial/service-tier truth

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ resource/capability envelope
→ Budget / Routing Policy
→ eligible route set
```

```text
COMMERCIAL TIER != MODEL / PROVIDER / DEPLOYMENT
ENTITLED != SERVABLE
```

No Base/Plus/Pro names, prices or quotas are fixed.

Commercial tiers may not weaken correctness/privacy/Authority/target safety/provider-data eligibility/reconciliation.

---

# 5. Provider activation gate

AI-04 architecture closure does not activate a provider.

Before a concrete production route is activated, applicable direct DANTE evidence must cover the actual material production composition, including as required:

```text
workload quality
hard semantic/privacy/safety gates
serving-binding reliability
feature/data eligibility
Harness+binding compatibility
security/control compatibility
effective production-route quality
economics/resource behavior
intended production capacity/service envelope
```

No API credentials are required for the current global-reconciliation / AI-05 design work.

---

# 6. Current exact action

```text
GLOBAL CURRENT-TRUTH RECONCILIATION
```

Expected bounded targets are global/current navigation and status documents only, so that repository truth consistently says:

```text
AI-04 CLOSED / STRUCTURALLY ACCEPTED
AI-05 NEXT / CURRENT AFTER RECONCILIATION
```

No implementation/provider/database claim should be added.

This reconciliation requires a fresh Git write gate.

---

# 7. AI-05 intent

After reconciliation:

```text
AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
```

AI-05 must reconcile the accepted project layers into a concrete architecture-to-build plan:

```text
Product / North Star
Domain
Whole Logical
Physical / PostgreSQL
Access / app boundaries
AI-02 runtime semantics
AI-03 context/retrieval/memory
AI-04 productionization
```

and produce exact implementation boundaries, ports/adapters/config/control-plane/evidence responsibilities, first vertical sequencing and decision-specific proof gates.

AI-05 is still architecture/blueprint work until explicitly gated implementation begins.

---

# 8. Current non-claims

```text
AI-04 CLOSED                         YES / STRUCTURAL
AI-05 STARTED                        NO
DIRECT PROVIDER EVAL PASS            NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
PROVIDER SDK SELECTED                NO
EVAL RUNNER SELECTED                 NO
API CREDENTIALS USED                 NO
PAID API CALL EXECUTED               NO
PRODUCTION CAPACITY PASS             NO
AI BACKEND IMPLEMENTED               NO
FRONTEND AI IMPLEMENTED              NO
CONTROL PLANE IMPLEMENTED            NO
COMMERCIAL TIER NAMES/PRICES SET     NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN/FTS ACTIVATED           NO
RESTATE/R2 ACTIVATED                 NO
MCP/A2A ACTIVATED                    NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SC/PSV DIRECT PROOFS EXECUTED        NO
```

---

# 9. Git write-gate discipline

Before every new remote write:

```text
BRANCH
<exact branch>

PRE-SCOPE
<exact current SHA>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<out of scope>
```

Re-fetch HEAD immediately before first write. If it differs, STOP and re-gate.

After writes compare PRE-SCOPE..HEAD and prove exact path classification/no scope creep.

---

# 10. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.
