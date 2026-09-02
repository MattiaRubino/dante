# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-09-02
- **Backend foundation:** CP1–CP6 CLOSED / integrated / directly validated
- **Current PostgreSQL:** 18.6
- **Current Alembic head:** `20260830_09`
- **Current AI state:** architecture design/reengineering CLOSED / post-AI05 mega PASS / implementation entry authorized at I0

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Framework, model, provider or storage convenience does not redefine accepted Product/Domain/Logical/Physical semantics.

Core invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
AI/solver output != accepted canonical effect
client local state != canonical accepted effect
Occurrence != Schedule != Session != Actual
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
Context != Retrieval != Memory
ConsumerContext != ContextManifest != BasisManifest
RetrievalCandidate != ContextFragment
DATA != INSTRUCTION
MASKING / REDACTION != SEMANTIC EQUIVALENCE
APPROXIMATE != COMPLETE
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
GLOBAL SEARCH != INTELLIGENCE
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
AUXILIARY MODEL INFERENCE != FREE PROVIDER CALL
DEFAULT NONCANONICAL PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

## 2. Repository / application topology

One product monorepo:

```text
DANTE repository
├── apps/backend
├── apps/web
├── apps/mobile
├── packages
├── infra
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Backend posture remains a capability-first modular monolith.

```text
apps/backend/src/dante
├── bootstrap
├── kernel only for proven stable cross-capability primitives
├── platform for shared technical mechanics
└── modules/<capability>
```

Responsibility boundary != module != table != deployable service.

FastAPI is an inbound/process host. SQLAlchemy/provider runtime objects do not own Domain identity. Bootstrap wires; it does not become the service layer.

## 3. Current backend / PostgreSQL foundation

```text
Python                3.14.x / initial exact pin 3.14.7
uv                    package authority
FastAPI               inbound/process host
SQLAlchemy            async 2.0 stable line
psycopg               3
Alembic               one environment / one DAG / one head
PostgreSQL            18.6
schema                dante
Alembic head          20260830_09
transaction owner     outer application operation
adapter commit        forbidden / flush only
READ COMMITTED        default
```

Current concrete topology:

```text
69 tables
5 views
15 routines
76 triggers
97 indexes
69 foreign keys
123 CHECK constraints
0 custom enum/domain
0 sequences
0 materialized views
0 RLS policies
```

PostgreSQL 18 major family is the sole canonical persistence/material-history authority.

Rejected globally remain universal Entity/Thing roots, generic relationship graph, canonical EAV/property bag, universal Fact/Version payload and generic JSONB semantic escape hatches.

## 4. AI architecture closure

Completed architecture chain:

```text
AI-00  COMPLETE
AI-01  COMPLETE
AI-02.1 CLOSED / STRUCTURALLY ACCEPTED
AI-03  CLOSED / C01..C33 / B01..B35 / MAT-01..MAT-15
AI-04  CLOSED / A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
PRE05  CLOSED / PRE05-H01..H19
AI-05A CLOSED / BD-01..BD-41
AI-05B CLOSED / AI05B-H01..H15
AI-05 whole-system CLOSED / STRUCTURALLY ACCEPTED
POST05 hardening CLOSED / POST05-H01..H25
MKT-001..MKT-100 PASS
C01..C20 compound PASS
reverse authority PASS
Product/simulation replay PASS
```

Current implementation-facing authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
```

Final independent acceptance evidence:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
```

Architecture design/reengineering is closed. Runtime/provider/product activation is not claimed.

## 5. Final Search / Intelligence split

```text
modules/search
→ independent Global Search/discovery capability
→ deterministic/no-model capable
→ permission-safe bounded cross-capability read projection for Search
→ no canonical mutation authority

modules/intelligence
→ Work / Context / Reference Resolution / Semantic Query / Retrieval orchestration
→ optional governed ModelAccess
→ Verification / Result Maturity / Effect / Safe Publication
→ no raw database or canonical business ownership
```

Search's cross-capability read projection is Search-specific. It is not an excuse for Intelligence to perform arbitrary cross-capability SQL.

Structured DANTE-native questions use owning capability typed query seams. If no such seam exists, the capability is not integration-ready; the model does not receive SQL authority.

## 6. Context / retrieval / reference model

Accepted runtime chain as applicable:

```text
WorkContract
→ ContextPlan
→ InformationNeed
→ ContextStrategy
→ ReferenceResolution where required
→ SemanticQuery and/or RetrievalPlan
→ RetrievalCandidate
→ validation
→ ContextFragment
→ ContextReadiness
→ ConsumerContext
→ ContextManifest exposure evidence
→ BasisManifest currentness/coherence
```

Reality Scope and Runtime Interpretation Frame remain explicit. Relative dates/times, timezone/DST, current/history/scenario/open-world distinctions are not inferred from server-local accidents.

Search/reference resolution operate over the eligible universe before observable rank/count/facet/ambiguity behavior.

## 7. Model/provider boundary

```text
Intelligence application
→ DANTE-owned ModelAccessPort
→ ModelAccessRuntime
→ private ProviderAdapter
→ provider SDK/protocol
```

Provider/model/SDK remains OPEN / evidence-driven.

Correct lifecycle:

```text
candidate shortlist
→ candidate admission
→ inactive adapter/binding
→ conformance
→ live compatibility with eligible/minimized data
→ direct DANTE eval using production-owned composition
→ applicable privacy/security/capacity/economics evidence
→ qualification
→ promotion
```

Candidate admission != production qualification.

Every auxiliary inference—router, query rewrite, resolver helper, summarizer, verifier/judge—uses the same governed ModelAccess/data-egress/resource/eval boundary.

## 8. Provider attempts / disclosure / retry

DANTE allocates `ProviderAttemptId` before dispatch and owns the effective retry budget.

```text
provider outcome unknown
→ no blind replay

provider failed/timed out
!= data disclosure did not happen
```

Request-local `EgressAttempt` distinguishes `NOT_SENT | POSSIBLE | ESTABLISHED` exposure from provider completion.

Fallback rebuilds/minimizes ConsumerContext and reevaluates current provider eligibility, cumulative disclosure and resources. Server-side multi-provider hedging is OFF until explicitly qualified.

SDK/gateway hidden retries are disabled or every material attempt is accounted under DANTE attempt/resource/disclosure evidence.

## 9. Verification / Effect / publication

```text
provider completed
!= verified
!= publishable
```

`VerificationResult`, `ResultMaturity` and `PublicationDecision` remain distinct.

First vertical:

```text
ConsequenceProfile = READ_ONLY
proposed effects = []
→ EffectOutcome.NO_EFFECT
```

Any mutation intent under that envelope is rejected before mutation dispatch.

Publication revalidates current Work, Auth/AuthZ/Consent/Visibility, recipient/surface, disclosure, Basis/currentness and transformed final representation.

First public Ask is non-streaming. External streaming is a later proof-gated capability.

## 10. Evidence / observability

```text
CANONICAL DATA
!= AUDIT/EXECUTION EVIDENCE
!= OPERATIONAL TELEMETRY
!= EVAL/QUALIFICATION EVIDENCE
```

Operational telemetry is minimized and excludes raw private context/search candidates/model output/secrets by default.

Telemetry exporter failure is operational degradation, not permission to weaken safety/privacy or fabricate canonical state.

Sensitive cases requiring durable audit remain activation-gated until a real audit owner/integrity/retention/access contract exists.

## 11. Persistence posture

Request-local/no-store by default includes Work/Run state, Context contracts, Search results, RetrievalCandidate, ContextManifest, BasisManifest, ProviderAttempt, EgressAttempt, Verification/Publication and NO_EFFECT state.

Independent triggers are required for:

```text
conversation/session persistence
durable Run/resume
AI memory
Context cache
cross-Run prior-disclosure accounting
commercial/shared usage ledger
idempotency/saga/reconciliation state
background durable Work
vector/embedding representations
```

No generic AI persistence is justified by the first vertical.

## 12. Capability-triggered components

Remain dormant until real triggers/proofs:

```text
FTS / pg_trgm
pgvector / ANN / embeddings
Restate
R2
MCP / A2A
Execution Environment
external result streaming
multi-provider hedging
commercial/shared accounting
cross-Run disclosure accounting
```

## 13. Current implementation sequence

```text
I0  repository/application ownership + architecture-test skeleton
I1  Search contracts/registry/application shell
I2  Intelligence pure contracts + deterministic fakes
I3  first real deterministic Search/structured query families when integration-ready
I4  provider candidate admission + inactive adapter candidate
I5  conformance/live compatibility/direct qualification
I6  read-only Ask DANTE
I7  production hardening / observability / privacy / audit / resource / rollout
I8  scenario/planning proposal
I9  first bounded consequential Effect
I10 proactive/background/durable/external-agent work only on trigger
```

Current exact next action is **I0**.

I0 is build-authorized. It does not activate production Search, Ask, provider routes, new persistence or database changes.