# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** MATERIALIZED / DIRECT PROVIDER EVIDENCE DEFERRED UNTIL DECISION-CRITICAL
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CURRENT / STATE-OF-THE-ART SECURITY + PRIVACY + CONTROL PLANE + OPERATIONS RESEARCH
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **AI-04B closure PRE-SCOPE:** `221cb9473df8f7b3264d3cef2f3bc6a3ab145430`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architecture truth lives in architecture/current workstream sources.

Repository truth outranks this handoff.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     AI-04C State-of-the-Art Production Assurance Research
next        AI-04C candidate → kill-test → hardening/retest
```

Closed upstream:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
AI-04B         CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
```

Do not restart generic AI-02/AI-03/AI-04B redesign without concrete contradictory downstream evidence.

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

For AI-04C conclusions touching semantics/persistence, inspect Product/North Star, Domain, Whole Logical/WL-H01..H12, Physical, CP6/PostgreSQL Constitution, current DB/Alembic truth, Recovery and PSV obligations directly.

---

# 3. Current project truth

```text
PRODUCT / NORTH STAR       CURRENT
DOMAIN                     CLOSED
LOGICAL                    CLOSED / 57 OF 57 / WL-H01..WL-H12
PHYSICAL                   CLOSED
PostgreSQL                 18.6 / sole canonical persistence + material-history authority
Alembic                    20260830_09
DB topology                69 tables / 5 views / 15 routines / 76 triggers /
                           97 indexes / 69 FKs / 123 CHECKs
RECOVERY                   CP01–CP07 LOCAL PASS / CLOSED / integrated
remote backup provider     TBD / NOT ACTIVATED
production/cloud recovery  NOT CLAIMED
```

No AI provider/runtime convenience may redefine these contracts.

---

# 4. Current compact roadmap

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / STRUCTURALLY ACCEPTED

AI-04 PRODUCTIONIZATION ARCHITECTURE — CURRENT
  AI-04A eval/model/provider/economics
    MATERIALIZED
    direct provider/model evidence DEFERRED UNTIL DECISION-CRITICAL

  AI-04B concrete runtime/capabilities
    CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31

  AI-04C security/privacy/control-plane/operations
    CURRENT

AI-05 WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT — FUTURE
THEN ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

---

# 5. AI-04A retained authority

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
→ qualified serving platform/model/deployment/feature mode
```

DANTE owns eval semantics. Hard semantic/privacy/safety failure cannot be averaged away.

No provider/model/default is selected.

---

# 6. Commercial/service-tier boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
```

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

Commercial tiers may bound resources but may not weaken correctness, privacy, Authority, target safety, provider/data eligibility or reconciliation obligations.

No Base/Plus/Pro names, prices or quotas are fixed.

---

# 7. AI-04B closure chronology

```text
first candidate
→ destructive kill-test FAIL
→ RT-01..RT-20
→ compound retest PASS CANDIDATE
→ fresh independent validation FAIL
→ RT-21..RT-31
→ final compound retest PASS
→ CLOSED / STRUCTURALLY ACCEPTED
```

The independent pass found and closed gaps around cancellation acknowledgement, continuation rebinding, feature-mode qualification, provider-state revocation, semantic idempotency, frozen config/current auth, irreversible publication, late callbacks, attached/detached work, budget settlement and MCP auto-fulfilment.

No Domain/Logical/Physical/PostgreSQL reopen was required.

---

# 8. RT-01..RT-31 summary

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CLIENT DISCONNECT != STREAM STOP != INVOCATION CANCEL != RUN CANCEL != EFFECT ROLLBACK
CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED
PARTIAL TOOL ARGUMENTS != EXECUTABLE TOOL REQUEST
PROVIDER PARALLEL TOOL CALL != EFFECTGRAPH AUTHORIZATION
PROVIDER BACKGROUND != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION != DANTE SESSION/CONTEXT/MEMORY
CONTINUATION HANDLE != CURRENT HARNESS/POLICY/TOOLS/CAPABILITIES
REFUSAL != INFRA FAILURE / no safety-arbitrage fallback
SERVER-SIDE FALLBACK != DANTE ROUTING AUTHORITY
PROVIDER TOOL != DANTE CAPABILITY
MCP/A2A discovery/task state != DANTE trust/authority/run truth
PROVIDER-HOSTED EXECUTION != DANTE Execution Environment
PROVIDER EVENT/TOOL IDs != DANTE semantic identity/idempotency
ENTITLEMENT CHANGE cannot erase consequence/reconciliation obligations
FEATURE MODE participates in provider/binding qualification
DANTE revocation suppresses provider-state reuse before provider purge confirmation
FROZEN EXECUTION CONFIG != PERPETUAL CURRENT AUTHORIZATION
PUBLISHED DELTA = EXTERNALIZATION
REMOTE CALLBACK != CURRENT RUN ELIGIBILITY
ATTACHED CHILD != DETACHED CHILD
BUDGET ADMISSION != FINAL COST / GUARANTEED PROVIDER STOP
MCP INPUT_REQUIRED/AUTO-FULFIL != USER INPUT/CONSENT/APPROVAL
```

Full normative wording lives in the AI-04B durable document.

---

# 9. Class-A / Class-B durability

```text
Class A → PostgreSQL transactional outbox + bounded worker
Class B → Restate selected / dormant until first real qualifying consumer
```

Provider background execution does not replace Class-B semantics.

Restate activation still requires applicable direct proof/privacy/recovery obligations.

---

# 10. AI-04C current scope

```text
provider/data/feature-mode eligibility
privacy / retention / residency
information-flow / prompt-injection containment
credential/workload identity
secret brokerage / key lifecycle
control-plane registry and configuration ownership
routing policy governance
configuration promotion / emergency kill switches
CommercialOffering / EntitlementProfile / Budget Policy integration
budget reservation / settlement / overshoot
rate limits / concurrency / backpressure / fairness
observability vs audit vs eval evidence
privacy-safe logs/traces
SLOs / error budgets
provider incidents / degraded modes
shadow / canary / progressive rollout / rollback
model/harness/provider requalification triggers
runtime evidence retention
security incident response
operational recovery / reconciliation
```

Research must use current 2026 state-of-the-art sources and publicly documented production patterns from relevant large platforms. Clearly separate verified public evidence from architectural inference.

---

# 11. Exact next action

```text
AI-04C — STATE-OF-THE-ART PRODUCTION ASSURANCE RESEARCH
```

Required approach:

```text
DANTE obligations + RT-01..RT-31
→ current official provider/cloud/security docs
→ publicly documented large-app/platform patterns
→ candidate security/privacy/control-plane/ops architecture
→ destructive kill-test
→ hardening
→ compound retest
→ fresh independent validation
→ AI-04C closure only if no structural contradiction remains
```

Do not select provider/model/SDK merely from documentation or popularity.

---

# 12. Current non-claims

```text
AI-04 CLOSED                         NO
AI-04B CLOSED                        YES / STRUCTURAL
AI-04C CLOSED                        NO
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

# 13. Git write-gate discipline

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

# 14. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.