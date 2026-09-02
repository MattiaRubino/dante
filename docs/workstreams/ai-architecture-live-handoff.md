# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** MATERIALIZED / A01..A30 / EV01..EV20
- **AI-04B:** CLOSED / STRUCTURALLY ACCEPTED / RT-01..RT-31
- **AI-04C:** CLOSED / STRUCTURALLY ACCEPTED / PA-01..PA-61
- **Current action:** AI-04 WHOLE-PHASE DESTRUCTIVE ACCEPTANCE
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **AI-04C closure PRE-SCOPE:** `d7c13bacc170fe14645d5f4bf69408c5e31d128b`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architecture truth lives in architecture/current workstream sources.

Repository truth outranks this handoff.

---

# 1. Resume rule

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     AI-04 Whole-Phase Destructive Acceptance
next        AI-04 closure only if whole-phase PASS
then        AI-05 Whole-System Acceptance + Implementation Blueprint
```

Closed upstream:

```text
AI-02.1        CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
AI-04B         CLOSED / RT-01..RT-31
AI-04C         CLOSED / PA-01..PA-61
```

Do not restart generic AI-02/AI-03/AI-04B/AI-04C redesign without concrete contradictory evidence.

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
this file

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
```

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

---

# 4. Current compact roadmap

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / STRUCTURALLY ACCEPTED

AI-04 PRODUCTIONIZATION ARCHITECTURE — CURRENT
  AI-04A MATERIALIZED / A01..A30 / EV01..EV20
  AI-04B CLOSED / RT-01..RT-31
  AI-04C CLOSED / PA-01..PA-61
  WHOLE-PHASE DESTRUCTIVE ACCEPTANCE CURRENT

AI-05 WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT — FUTURE
THEN ACTUAL AI IMPLEMENTATION WORKSTREAM(S)
```

---

# 5. AI-04A retained boundary

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
```

```text
DANTE need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ qualified serving platform/model/deployment/feature mode
```

Direct provider/model evidence remains deferred until a concrete decision requires it.

---

# 6. Commercial boundary

```text
COMMERCIAL SUBSCRIPTION / SERVICE TIER != DANTE DOMAIN Plan
COMMERCIAL TIER != MODEL / PROVIDER / DEPLOYMENT
```

```text
CommercialOffering / ServiceTier
→ EntitlementProfile
→ capability + quota + resource envelope
→ Budget / Routing Policy
→ ModelTarget eligibility
→ ProviderBinding
```

No Base/Plus/Pro names, prices or quotas are fixed.

---

# 7. AI-04B retained runtime truth

```text
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
RAW PROVIDER EVENT != DANTE RUNTIME EVENT != PUBLICATION EVENT
CANCELLATION REQUESTED != CANCELLATION CONFIRMED != EXECUTION QUIESCED
PARTIAL TOOL ARGS != EXECUTABLE TOOL CALL
PROVIDER BACKGROUND != DANTE DURABLE EXECUTION
PROVIDER CONTINUATION != DANTE MEMORY/SESSION
PROVIDER CALL ID != DANTE SEMANTIC IDEMPOTENCY
FROZEN CONFIG != PERPETUAL CURRENT AUTHORIZATION
REMOTE CALLBACK != CURRENT RUN ELIGIBILITY
BUDGET ADMISSION != FINAL COST / GUARANTEED PROVIDER STOP
```

Full RT-01..RT-31 lives in AI-04B.

---

# 8. AI-04C retained production-assurance truth

```text
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED
new material model/provider/feature mode inactive by default
control-plane config versioned + coherent
revocation/emergency deny beats stale cached Allow
existing DANTE Authority remains authoritative
guardrail result != DANTE Authority
security service itself is a governed recipient
short-lived scoped identity preferred where supported
admin/runtime/delegated/sandbox credentials are distinct
telemetry != audit != eval != canonical truth
full private content telemetry OFF by default
admission estimate != reservation != settlement
provider metering != DANTE commercial settlement authority
commercial exhaustion cannot starve reconciliation
shadow traffic is real disclosure
shadow result != production result
rollback config != rollback effects
rollback target must still be currently safe
provider health scoped by binding/region/feature mode
withheld/security-ineligible != absent/false
post-generation masking may invalidate verified meaning
required audit evidence has integrity/failure semantics distinct from debug logs
critical degraded/recovery paths require exercise
reliability/security state can freeze non-essential rollout
```

Full PA-01..PA-61 lives in AI-04C.

---

# 9. Whole-phase acceptance target

Review AI-04A/B/C **together**, not as three already-correct modules.

Generate cross-phase attacks before reading local conclusions.

At minimum pressure:

```text
quality winner but privacy-ineligible
quality/economics winner but operationally unavailable
commercial tier grants capability with zero routable bindings
cheaper route below quality floor
feature-mode/retention change invalidates previous eval qualification
HarnessProfile/model/guard profile versions drift independently
fallback satisfies runtime but violates capacity/budget/residency
partial attempt + failover duplicates cost/effect intent
shadow/canary violates eval-purpose/data-eligibility constraints
guard/DLP transformation invalidates evaluated output quality
control-plane chooses ModelTarget with no current qualified binding
provider requalification changes during active background/durable work
commercial downgrade during reservation/reconciliation
telemetry/audit accidentally leaks hidden oracle or private context
security kill switch removes model path but deterministic route remains
all-provider outage and safe deterministic/read-only mode
```

Classify each finding as:

```text
STRUCTURAL CONTRADICTION
→ must harden AI-04 before closure

DIRECT-EVIDENCE BLOCKER
→ architecture coherent, but concrete provider/model choice requires benchmark/proof

IMPLEMENTATION-BLUEPRINT DETAIL
→ defer to AI-05

PRODUCT/COMMERCIAL CHOICE
→ remain open unless required for architecture
```

---

# 10. Current non-claims

```text
AI-04 CLOSED                         NO
AI-04 WHOLE-PHASE PASS                NO
DIRECT PROVIDER EVAL PASS            NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
PROVIDER SDK SELECTED                NO
API CREDENTIALS USED                 NO
PAID API CALL EXECUTED               NO
COMMERCIAL TIER NAMES/PRICES SET     NO
AI BACKEND IMPLEMENTED               NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN/FTS ACTIVATED           NO
RESTATE/R2 ACTIVATED                 NO
MCP/A2A ACTIVATED                    NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SC/PSV DIRECT PROOFS EXECUTED        NO
AI-05 STARTED                        NO
```

---

# 11. Git write-gate discipline

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

# 12. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```
