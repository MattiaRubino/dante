# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** MATERIALIZED / DIRECT PROVIDER EVIDENCE DEFERRED UNTIL DECISION-CRITICAL
- **AI-04B:** RUNTIME/CAPABILITY CANDIDATE MATERIALIZED / RT-01..RT-20 / FRESH INDEPENDENT VALIDATION CURRENT
- **AI-04C:** FUTURE / NEXT AFTER AI-04B CLOSURE
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **Current gate PRE-SCOPE:** `cef3105aafc7adbbe77f60a578a1e450e5cad5d3`
- **AI-04B candidate commit:** `76db6e3e188caccaa3aea05f43961f0b42f7f0d0`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architecture truth lives in architecture/current workstream sources.

Repository truth outranks this handoff.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     AI-04B Fresh Independent Destructive Runtime Validation
next        AI-04C only after AI-04B closure
```

Closed upstream:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
```

Do not restart generic Context/Retrieval/Memory or AI-02 redesign without concrete contradictory downstream evidence.

---

# 2. Mandatory reading order

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/development/documentation-lifecycle-policy.md
docs/development/branching-and-environments.md
docs/development/repository-engineering-safety.md

docs/workstreams/ai-architecture.md
this live handoff

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
```

For any AI-04 conclusion touching semantics/persistence, inspect Product/North Star, Domain, Whole Logical/WL-H01..H12, Physical, CP6/PostgreSQL Constitution, current DB/Alembic/SQLAlchemy truth, Recovery and PSV obligations directly.

---

# 3. Closed project state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN
CLOSED

LOGICAL
CLOSED / 57 OF 57 / WL-H01..H12

PHYSICAL
CLOSED
PostgreSQL = sole canonical persistence/material-history authority

BACKEND CP1–CP5
CLOSED / integrated

CP6 DATABASE
CLOSED / integrated

CURRENT PostgreSQL
18.6
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs

RECOVERY
CP01–CP07 LOCAL PASS / CLOSED / integrated
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

No provider/runtime convenience may redefine these contracts.

---

# 4. Current compact roadmap

```text
AI-00  COMPLETE
AI-01  COMPLETE
AI-02  CLOSED / STRUCTURALLY ACCEPTED
AI-03  CLOSED / STRUCTURALLY ACCEPTED

AI-04  PRODUCTIONIZATION ARCHITECTURE — CURRENT

  AI-04A
  eval/model/provider/economics + entitlement boundary
  MATERIALIZED
  direct provider/model eval evidence DEFERRED UNTIL NEEDED

  AI-04B
  concrete runtime + capabilities
  CANDIDATE MATERIALIZED
  first kill-test FAIL
  RT-01..RT-20
  compound retest PASS CANDIDATE
  fresh independent validation CURRENT

  AI-04C
  security/privacy/control-plane/operations
  FUTURE / NEXT AFTER AI-04B CLOSURE

AI-05
WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT — FUTURE

THEN
ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

---

# 5. AI-04A retained authority

Durable sources:

```text
docs/architecture/dante-ai-04-productionization-architecture.md
docs/architecture/dante-ai-04a-direct-eval-specification.md
```

Provider boundary:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

```text
DANTE need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ serving platform/model/deployment
```

Eval authority remains DANTE-owned. Hard semantic/privacy/safety failures cannot be averaged away by quality/cost.

No provider/model/default is selected.

Direct eval tooling remains deferred until provider/model selection is actually blocked on evidence; no API key is required for current work.

---

# 6. Commercial/service-tier boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER
!= DANTE DOMAIN Plan
```

Candidate chain:

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

```text
COMMERCIAL TIER != MODEL
COMMERCIAL TIER != PROVIDER
COMMERCIAL TIER != DEPLOYMENT
```

Commercial tiers may bound resources; they may not weaken semantic correctness, privacy, Authority, target safety, provider/data eligibility, effect verification/reconciliation or anti-resurrection/currentness.

No Base/Plus/Pro names, prices or quotas are fixed.

---

# 7. AI-04B durable authority

```text
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
```

Current candidate status:

```text
research / protocol verification COMPLETE ENOUGH
first candidate BUILT
first destructive kill-test FAIL
RT-01..RT-20 incorporated
compound retest PASS CANDIDATE
independent validation CURRENT
```

Runtime shape:

```text
Interaction / WorkContract
        ↓
Execution Kernel
        ├ deterministic compute
        ├ solver
        ├ Model Access Runtime
        ├ Capability Runtime
        ├ Execution Environment Broker
        └ Async / Durable Supervisor
        ↓
Verifier
        ↓
ChangeSet / EffectGraph / Effect Runtime
        ↓
Safe Publication
```

Responsibilities do not imply microservices/tables.

---

# 8. AI-04B binding separations

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CLIENT DISCONNECT != STREAM STOP != INVOCATION CANCEL != RUN CANCEL != EFFECT ROLLBACK
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST
PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH PARALLEL AUTHORIZATION
PROVIDER BACKGROUND EXECUTION != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION STATE != DANTE SESSION/CONTEXT/MEMORY
REFUSAL != INFRASTRUCTURE FAILURE
PROVIDER SERVER-SIDE FALLBACK != DANTE ROUTING AUTHORITY
PROVIDER TOOL != DANTE CAPABILITY
MCP DISCOVERY/DESCRIPTION != TRUST/AUTHORITY
MCP ELICITATION != DANTE APPROVAL
MCP TASK != DANTE RUN
A2A TASK/STATUS != DANTE RUN/CANONICAL STATE/AUTHORITY
PROVIDER-HOSTED EXECUTION != DANTE Execution Environment
```

---

# 9. Runtime routing/failure posture

Routing uses minimum necessary metadata plus current qualification/eligibility/budget.

Failover is:

```text
classify failure
→ determine if failover allowed
→ qualify alternate binding now
→ fresh provider/data eligibility
→ rebuild/minimize ConsumerContext if required
→ alternate HarnessProfile
→ new ProviderAttempt
```

No blind request replay.
No refusal/provider safety shopping.
No hedged multi-provider requests by default.

Retry must distinguish safe pre-acceptance failure from outcome-unknown state requiring reconciliation.

Cancellation cannot erase already-dispatched effect verification/reconciliation.

---

# 10. Tool/capability posture

```text
model request/deltas
→ finalized args
→ parse/schema
→ semantic validation
→ capability resolution
→ policy
→ effect policy if consequential
→ dispatch
→ receipt
→ verify/reconcile
→ normalized result
```

Keep distinct:

```text
Capability Registry
Capability Discovery
Capability Runtime
```

Provider native tools/MCP/A2A adapters do not define DANTE semantic capability authority.

---

# 11. Durable/background posture

```text
INLINE
BOUNDED ASYNC
ELIGIBLE PROVIDER BACKGROUND
CLASS-B DURABLE
```

Accepted project decision remains:

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate selected / dormant until real qualifying consumer
```

Provider background execution does not replace Class-B durability semantics.

---

# 12. Execution Environment posture

Execution Environment is trigger-based for code/browser/file/untrusted execution.

```text
PROVIDER-HOSTED EXECUTION
!= DANTE Execution Environment
```

Isolation technology remains open:

```text
T0 trusted deterministic compute
T1 WASM/WASI where compatible
T2 hardened container/syscall isolation
T3 microVM/VM where required
```

Untrusted/model-generated execution does not receive broad DB/service secrets; privileged actions go through trusted typed capability/credential/egress brokerage.

---

# 13. RT-01..RT-20

```text
RT-01  RUN != MODEL INVOCATION != PROVIDER ATTEMPT.
RT-02  RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT.
RT-03  CLIENT DISCONNECT != STREAM STOP != INVOCATION CANCEL != RUN CANCEL != EFFECT ROLLBACK.
RT-04  PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST.
RT-05  PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH PARALLEL AUTHORIZATION.
RT-06  PROVIDER BACKGROUND EXECUTION != DANTE DURABLE EXECUTION.
RT-07  PROVIDER-STORED CONTINUATION STATE != DANTE SESSION / CONTEXT / MEMORY.
RT-08  RETRY CLASSIFICATION MUST ACCOUNT FOR ACCEPTANCE AND SIDE-EFFECT UNCERTAINTY.
RT-09  REFUSAL != INFRASTRUCTURE FAILURE; NO SAFETY-ARBITRAGE FALLBACK.
RT-10  SERVER-SIDE PROVIDER FALLBACK != DANTE ROUTING AUTHORITY.
RT-11  ROUTING MUST USE MINIMUM NECESSARY INFORMATION AND SELECT ONLY QUALIFIED CURRENT BINDINGS.
RT-12  HEDGED MULTI-PROVIDER EXECUTION IS NOT A SAFE DEFAULT.
RT-13  PROVIDER TOOL != DANTE CAPABILITY; NATIVE TOOLS DO NOT BYPASS SOURCE/EFFECT GOVERNANCE.
RT-14  MCP DISCOVERY / DESCRIPTION != TRUST / AUTHORITY.
RT-15  MCP ELICITATION != DANTE APPROVAL; MCP TASK != DANTE RUN.
RT-16  A2A DISCOVERY / TASK STATUS != DANTE AUTHORITY / CANONICAL STATE / RUN.
RT-17  PROVIDER-HOSTED EXECUTION != DANTE EXECUTION ENVIRONMENT.
RT-18  PROVIDER EVENT SEQUENCE / REPLAY != DANTE SEMANTIC EVENT IDENTITY.
RT-19  ENTITLEMENT/BUDGET CHANGE MAY GOVERN FUTURE WORK BUT CANNOT ERASE EFFECT/RECONCILIATION OBLIGATIONS.
RT-20  NO MODEL/PROVIDER FEATURE MAY SILENTLY REDEFINE DANTE RUNTIME SEMANTICS.
```

---

# 14. Exact next action

```text
AI-04B — FRESH INDEPENDENT DESTRUCTIVE RUNTIME VALIDATION
```

Must pressure at least:

```text
stream reconnect + duplicate tool/effect prevention
cancel + supersession + outcome-unknown
provider failover after partial output/tool state
provider background + crash + deletion/revocation
quota/downgrade during consequential work
MCP catalog/cache/trust drift
MCP input-required vs DANTE approval
A2A delegation/confused-deputy
provider-native tools + prompt injection + egress
provider-hosted execution + credential boundary
multi-agent parallelism + Authority
retry/idempotency/reconciliation
```

If AI-04B closes, route next to:

```text
AI-04C — SECURITY / PRIVACY / CONTROL PLANE / OPERATIONS
```

Do not start production AI backend or AI-05 yet.

---

# 15. Current non-claims

```text
AI-04 CLOSED                         NO
AI-04B CLOSED                        NO
AI-04B FINAL INDEPENDENT PASS         NO
DIRECT PROVIDER EVAL PASS            NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
PROVIDER SDK SELECTED                NO
EVAL RUNNER SELECTED                 NO
API CREDENTIALS USED                 NO
PAID API CALL EXECUTED               NO
COMMERCIAL TIER NAMES/PRICES SET     NO
AI BACKEND IMPLEMENTED               NO
FRONTEND STREAMING IMPLEMENTED       NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN/FTS ACTIVATED           NO
RESTATE/R2 ACTIVATED                 NO
MCP/A2A ACTIVATED                    NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SANDBOX TECHNOLOGY SELECTED          NO
SC/PSV DIRECT PROOFS EXECUTED        NO
AI-05 STARTED                        NO
```

---

# 16. Git write-gate discipline

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

# 17. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.