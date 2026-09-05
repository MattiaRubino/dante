# DANTE — Project Status

- **Status:** CURRENT TRUTH
- **Last reconciled:** 2026-09-05
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA
- **Backend CP6 integration:** PR #42 MERGED
- **PostgreSQL Recovery integration:** PR #47 MERGED / CP01–CP07 LOCAL PASS / CLOSED
- **Current product boundary:** Access/Auth, Home React and platform observability remain active bounded workstreams; AI architecture is closed; `feature/ai-implementation` is finishing only the low-level ModelAccess foundation before being frozen

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED / 57 OF 57 CLASSIFIED
WL-H01..WL-H12 BINDING

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family
sole canonical persistence / material-history authority

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
CLOSED / PASS / INTEGRATED VIA PR #28

PRODUCTION BACKEND SCAFFOLD
CP1–CP5 CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24

CP6 — CONCRETE POSTGRESQL DATABASE
CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #42

POSTGRESQL LOCAL RECOVERY
CP01–CP07 CLOSED / LOCAL PASS / INTEGRATED VIA PR #47

ACCESS PRE-BACKEND FRONTEND
CLOSED / ACCEPTED / RELEASE-HARDENED

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE UNMERGED WORKSTREAM

AI ARCHITECTURE DESIGN / REENGINEERING
CLOSED / STRUCTURALLY ACCEPTED
POST-AI05 FINAL MEGA TEST PASS

AI LOW-LEVEL IMPLEMENTATION
feature/ai-implementation
I0 CLOSED / PASS
I1 CLOSED / PASS
I2 CLOSED / PASS
I3 REAL SEARCH FAMILY DEFERRED / OWNER-SEAM GATE
C6 CLOSED / PASS
C7 CLOSED / PASS
DEVELOPMENT MODEL/BINDING DECISION COMPLETE
Gemini 3.8 Flash selected for both active logical ModelTargets
native ModelAccess foundation materialized
FINAL LOCAL REGRESSION + ONE NATIVE SMOKE PENDING
production qualification NO
private-data eligibility NO
```

Architecture closure is not runtime/product completion. The current AI branch is deliberately stopping at the low-level model-access foundation rather than manufacturing an early Ask DANTE vertical.

## 2. Current protected-main backend/database truth

```text
PostgreSQL          18.6
Alembic head        20260830_09
schema              dante

tables              69
views                5
routines             15
triggers             76
physical indexes     97
foreign keys         69
CHECK constraints    123
custom enum/domain    0
sequences             0
materialized views    0
RLS policies          0
```

Recovery posture:

```text
material_state_retirement  materialized
suppression ledger         versioned / fail-closed
CP01–CP07                  LOCAL PASS / CLOSED
whole operator rehearsal   PASS
database-local reopen      PASS
remote backup provider     TBD / NOT ACTIVATED
production/cloud recovery  NOT CLAIMED
```

## 3. Persistence authority

```text
Domain / Logical / Physical
→ semantic and architectural source

CP6 Constitution + ADR-010
→ durable PostgreSQL doctrine

Database System of Record
→ current human-readable meaning + machine Dictionary

Alembic
→ deployed schema evolution authority

SQLAlchemy metadata/mappings
→ application representation

real PostgreSQL introspection
→ observed materialized schema

direct tests
→ executable proof
```

Permanent reconciliation remains:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata/mappings
≈ Alembic head
≈ real PostgreSQL schema
```

The AI foundation work introduces no database/Alembic change.

## 4. Binding semantic invariants

Project-wide invariants remain unchanged, including:

```text
Person != Account != Principal != Actor
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Authority != Visibility
Agreement != Consent
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
PostgreSQL = sole canonical persistence/material-history authority
```

AI-specific invariants retained:

```text
GLOBAL SEARCH != INTELLIGENCE
ASK MAY USE SEARCH != ASK REQUIRES SEARCH GENERALLY
SEARCH READINESS != GLOBAL INTELLIGENCE PREREQUISITE
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
MODEL OUTPUT != PUBLISHABLE OUTPUT
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
Context != Retrieval != Memory
DATA != INSTRUCTION
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
PROVIDER SDK != APPLICATION CONTRACT
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED != ROLLOUT-ACTIVE
DEFAULT NONCANONICAL AI PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
RUN != MODEL INVOCATION != PROVIDER ATTEMPT
PROVIDER FAILOVER != BLIND REQUEST REPLAY
```

## 5. Backend technical foundation

```text
Python                    3.14.x
uv                        package authority
FastAPI                    inbound/process host
SQLAlchemy                 async 2.0 stable line
psycopg                    3
Alembic                    one environment / one DAG / one head
one AsyncEngine            per process
one async_sessionmaker     per process
one AsyncSession           per app operation
autobegin                  false
autoflush                  true
expire_on_commit           false
transaction owner          outer application operation
adapter commit             forbidden / flush only
READ COMMITTED             default
```

No generic Repository/UoW/BaseService architecture is introduced merely for uniformity.

## 6. Current AI implementation authority

Architecture/design authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
docs/architecture/dante-ai-search-intelligence-boundary-amendment-2026-09.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
```

Current development binding/closure authority:

```text
docs/workstreams/ai-runtime-model-target-closure-acceptance-2026-09-05.md
docs/workstreams/ai-foundation-closure-2026-09-05.md
docs/ROADMAP.md
```

Historical provider records retained as evidence:

```text
docs/workstreams/ai-provider-candidate-admission-2026-09.md
docs/workstreams/ai-c9-pre-live-checkpoint-2026-09.md
```

Those historical OpenAI/Terra records no longer define the current blocker.

## 7. Current AI low-level foundation

Accepted reasoning peers:

```text
DETERMINISTIC COMPUTE
SOLVER
MODEL ACCESS
```

Accepted development routes:

```text
STRUCTURED_INTERPRETATION -> Gemini 3.8 Flash
GENERAL_REASONING         -> Gemini 3.8 Flash
DEEP_REASONING            -> dormant / no physical binding
```

Current provider route:

```text
provider                  Google Gemini Developer API
protocol                  native Interactions API v1beta
model                     gemini-3.8-flash
binding state             development
reasoning level            low
streaming                  off
background                 off
provider continuation      off
provider-native tools      off
provider storage           off / store=false
fallback                   off
DANTE retry                off for foundation
private data               ineligible
production                 off
```

Materialized low-level pieces:

```text
ModelTarget / ModelInvocation contracts
ModelAccessPort
ModelAccessRuntime
ProviderAttempt/error/acceptance taxonomy
detailed usage evidence including reasoning/cached/tool-use tokens
typed immutable route configuration v2
deterministic champion routing
champion/challenger/fallback config slots
native Gemini Interactions adapter
private HTTP transport
provider-independent structured-output validation
deadline/timeout bounding
minimized runtime evidence
unit adapter/runtime/transport/config tests
guarded native smoke tooling
```

The OpenAI-compatible Gemini adapter remains evaluation history only and is not the canonical Google runtime protocol.

## 8. AI roadmap disposition

```text
I0  CLOSED
I1  CLOSED
I2  CLOSED
I3  DEFERRED / real owner-data-seam gate
I4  CLOSED FOR DEVELOPMENT FOUNDATION
I5  FOUNDATION CLOSURE CANDIDATE
    remaining = lock regeneration + deterministic/full regression + one native smoke
I6  DEFERRED / product-readiness gate
I7  partially front-loaded only for low-level ModelAccess concerns; full stage future
I8  FUTURE
I9  FUTURE
I10 FUTURE / trigger-gated
```

Old provider overlay:

```text
C6  CLOSED / retained
C7  CLOSED / retained + typed route v2
C8  OpenAI/Terra admission = historical evidence
C9  old Terra live blocker = superseded as current path
C10 development model evidence = complete
C11 development binding decision = complete / Gemini 3.8 Flash
production qualification/promotion = not complete
```

No stage is being falsely marked complete: integration-heavy stages remain deferred until their real owner/product seams exist.

## 9. Explicit non-claims

```text
production qualification              NO
private-data Gemini eligibility        NO
production Search                      NO
production Ask                         NO
first real Intelligence vertical       NOT YET SELECTED
AI memory integration                  NO
consequential AI Effect vertical       NO
proactivity/background activation      NO
second provider/failover activation    NO
local model activation                 NO
deep-reasoning physical binding        NO
FTS/vector/pgvector activation         NO
new AI persistence                     NO
new PostgreSQL/Alembic change          NO
```

## 10. Active/unmerged workstreams

```text
feature/access-auth             active product implementation
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-implementation       low-level AI foundation closure candidate
feature/ai-architecture         architecture design CLOSED / retained authority/evidence
```

Do not infer one branch's implementation from another branch.

## 11. Current exact next action

```text
feature/ai-implementation
→ regenerate apps/backend/uv.lock after explicit httpx2 runtime dependency
→ run full deterministic/backend regression gate
→ run native Gemini smoke dry-run
→ run exactly one synthetic native Gemini Interactions smoke through ModelAccessRuntime
→ if PASS: mark docs/workstreams/ai-foundation-closure-2026-09-05.md CLOSED / PASS
→ freeze/leave feature/ai-implementation
→ return to broader DANTE/main-oriented work
```

No additional broad model benchmark and no artificial Ask DANTE vertical are required to close this low-level foundation.
