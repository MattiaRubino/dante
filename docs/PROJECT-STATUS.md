# DANTE — Project Status

- **Status:** CURRENT TRUTH
- **Last reconciled:** 2026-09-04
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA
- **Backend CP6 integration:** PR #42 MERGED
- **PostgreSQL Recovery integration:** PR #47 MERGED / CP01–CP07 LOCAL PASS / CLOSED
- **Current product boundary:** protected `main` includes the accepted PostgreSQL Recovery evolution; Access/Auth, Home React and platform observability remain active bounded workstreams; AI architecture is closed on `feature/ai-architecture`; AI implementation is active on `feature/ai-implementation` with I0-I2, C6, C7 and C8 CLOSED, I3 deferred pending owner data/seams, OpenAI native Responses API + GPT-5.6 Terra admitted for qualification only, and C9 OPEN / PRE-LIVE READY with real provider live compatibility still NOT RUN

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

CURRENT POSTGRESQL
18.6

CURRENT PROTECTED-MAIN DATABASE / RECOVERY BASELINE
ALEMBIC 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs
CP01–CP07 LOCAL PASS / CLOSED
RECOVERY INTEGRATED VIA PR #47
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED

ACCESS PRE-BACKEND FRONTEND
CLOSED / ACCEPTED / RELEASE-HARDENED
AF-01D / AF-02A / AF-02B / AF-03A PASS

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE UNMERGED WORKSTREAM
feature/access-auth owns branch-local implementation truth

AI ARCHITECTURE DESIGN / REENGINEERING
CLOSED / STRUCTURALLY ACCEPTED ON feature/ai-architecture
AI-00 COMPLETE
AI-01 COMPLETE
AI-02.1 CLOSED / STRUCTURALLY ACCEPTED
AI-03 CLOSED / C01..C33 / B01..B35 / MAT-01..MAT-15
AI-04 CLOSED / A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
PRE-AI05 CLOSED / PRE05-H01..H19
AI-05A CLOSED / BD-01..BD-41
AI-05B CLOSED / AI05B-H01..H15 / B05-01..B05-50 PASS
AI-05 WHOLE-SYSTEM CLOSED / STRUCTURALLY ACCEPTED
POST-AI05 HARDENING CLOSED / POST05-H01..H25
POST-AI05 FINAL MEGA TEST PASS
MKT-001..MKT-100 PASS
C01..C20 COMPOUND PASS
REVERSE AUTHORITY PASS
PRODUCT/SIMULATION REPLAY PASS

CURRENT AI IMPLEMENTATION AUTHORITY
docs/architecture/dante-ai-implementation-baseline-final.md

AI IMPLEMENTATION WORKSTREAM
feature/ai-implementation
I0 CLOSED / PASS
I1 CLOSED / PASS
I2 CLOSED / PASS
I2 validated code checkpoint 359707b8d628347f82a0344d44f9fd42d0f59dcd
C6 CLOSED / PASS
C6 validated code checkpoint 2f96d4fb85300fdbfd00e66b9b6d23b26141397f
C7 CLOSED / PASS
C7 validated code checkpoint 65b4bdfe6987e7a2cbb9d543fd4a92b87264cf97
I3/C3 DEFERRED / WAITING OWNER DATA + SEAMS
C8/P1 CLOSED / PROVIDER CANDIDATE ADMITTED FOR QUALIFICATION ONLY
provider     OpenAI native API
API          Responses API
model        gpt-5.6-terra
record       docs/workstreams/ai-provider-candidate-admission-2026-09.md
C9          OPEN / PRE-LIVE READY
SDK         openai 3.7.0 / locked / private provider adapter only
adapter     MATERIALIZED / INACTIVE / QUALIFICATION-ONLY
pre-live validated code checkpoint 4bc02b783fad58ca32acd577881ccf1a9ee0998c
checkpoint  docs/workstreams/ai-c9-pre-live-checkpoint-2026-09.md
P4 live     NOT RUN / no user-owned qualification API credential provisioned

CURRENT AI EXECUTION OVERLAY
C6 control/safety/publication contracts CLOSED / PASS
→ C7 route-config identity/loader/digest CLOSED / PASS
→ C8/P1 provider candidate admission CLOSED
→ C9 P2/P3 + SDK + material conformance + P4 pre-live PASS
→ C9 P4 real provider compatibility NOT RUN
→ C10 direct DANTE qualification
→ C11 qualification/promotion decision

I3/C3 remains parallel/conditional and must converge before I6
when real owner data/seams and required permission/currentness proofs are ready

PARALLEL BOUNDED UNMERGED WORKSTREAMS
feature/access-auth
feature/home-react
feature/platform-observability
feature/ai-implementation — active / I0-I2 + C6+C7+C8 closed / C9 OPEN-PRE-LIVE-READY
feature/ai-architecture — architecture closed / retained authority/evidence
```

Architecture closure is not runtime/product completion. I0-I2, C6 and C7 are implemented and directly validated; C8 is a reviewed evidence/admission decision. C9 has now materially implemented the admitted inactive provider SDK/adapter and passed deterministic/material pre-live gates, but no real provider live call, production qualification, private-data eligibility, production Search/Ask or new persistence is claimed.

## 2. Current protected-main backend/database truth

PR #42 integrated CP6. PR #47 subsequently integrated the closed PostgreSQL Recovery workstream, including forward evolution `20260830_09`.

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

Historical pre-Recovery CP6 baseline remains:

```text
Alembic 20260826_08
68 tables / 5 views / 14 routines / 75 triggers /
95 indexes / 68 FKs / 120 CHECKs
```

Current Recovery posture:

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

CP6-02 Constitution + ADR-010
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

Permanent reconciliation:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata/mappings
≈ Alembic head
≈ real PostgreSQL schema
```

A later structural change remains a normal forward same-change package. AI I0-I2/C6/C7/C8/C9 pre-live introduced **no database/Alembic change**.

## 4. Binding semantic invariants

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
client local state != canonical accepted effect
```

Current AI implementation invariants additionally include:

```text
GLOBAL SEARCH != INTELLIGENCE
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
MODEL OUTPUT != PUBLISHABLE OUTPUT
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
Context != Retrieval != Memory
RetrievalCandidate != ContextFragment
ConsumerContext != ContextManifest != BasisManifest
DATA != INSTRUCTION
MASKING / REDACTION != SEMANTIC EQUIVALENCE
APPROXIMATE != COMPLETE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
RUN-START AUTONOMY != PERPETUAL AUTONOMY
AUXILIARY MODEL CALL != FREE PROVIDER CALL
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
HARNESSPROFILE != PROVIDERBINDING
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED != ROLLOUT-ACTIVE
DEFAULT NONCANONICAL PERSISTENCE = NO
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

## 5. Backend technical foundation

```text
Python                    3.14.x / initial exact pin 3.14.7
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

## 6. Current AI implementation boundary

Final implementation-facing authority:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
```

Branch-local execution record:

```text
docs/workstreams/ai-implementation.md
```

Current provider admission record:

```text
docs/workstreams/ai-provider-candidate-admission-2026-09.md
```

Current C9 pre-live evidence:

```text
docs/workstreams/ai-c9-pre-live-checkpoint-2026-09.md
```

Final structural acceptance evidence:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
```

Accepted first technical vertical:

```text
GLOBAL SEARCH subset
+ READ-ONLY ASK DANTE

private authenticated in-app
single-turn
inline/request-owned
READ_ONLY
public streaming OFF
background/durable resume OFF
consequential mutation OFF
```

Search remains independently deterministic. Structured semantic questions consume owning capability typed query seams. Provider SDKs remain private adapters behind `ModelAccessPort`.

C8 admitted exactly one initial qualification candidate, and C9 has materially implemented its inactive qualification-only adapter:

```text
OpenAI native API
Responses API
gpt-5.6-terra
openai SDK 3.7.0
ADMITTED FOR QUALIFICATION ONLY
INACTIVE / PRODUCTION OFF
```

This does not establish production qualification, private-data eligibility, entitlement, availability or rollout. Claude Sonnet 5 and Gemini 3.8 Flash on Vertex AI remain non-admitted shortlist challengers.

No generic persistence is justified for Work, Run, Context, SearchResult, ProviderAttempt, AI memory, conversation or embeddings.

Current branch-local implementation posture:

```text
I0 architecture boundaries                           CLOSED / PASS
I1 Search contracts/registry/application shell        CLOSED / PASS
I2 Work/Context/Reference/SemanticQuery/Retrieval     CLOSED / PASS
I3 real deterministic Search/structured families      DEFERRED / WAITING OWNER SEAMS
C6 Policy/Resource/Verification/Publication/
   Effect/Egress/Evidence contracts                   CLOSED / PASS
C7 route-config identity/loader/digest                CLOSED / PASS
C8/P1 provider candidate admission                    CLOSED / ADMITTED FOR QUALIFICATION ONLY
C9 inactive adapter + SDK + conformance + P4 pre-live OPEN / PRE-LIVE READY
C9 P4 real provider compatibility                     NOT RUN
```

I3 is not cancelled or falsely closed. It remains a conditional lane and must re-enter before I6 when the accepted first vertical requires the real deterministic source/query path.

## 7. Provider / direct-proof state

Current admitted qualification candidate:

```text
provider          OpenAI native API
API               Responses API
model             gpt-5.6-terra
SDK               openai 3.7.0
adapter           MATERIALIZED / INACTIVE
pre-live          PASS
live provider     NOT RUN
production status NOT QUALIFIED
```

Correct sequence:

```text
candidate shortlist                         COMPLETE
→ reviewed candidate admission              C8 / COMPLETE
→ inactive adapter/binding                  C9 / MATERIALIZED
→ deterministic + material SDK conformance  C9 / PASS
→ P4 pre-live                               C9 / PASS
→ final deterministic + PostgreSQL regression C9 / PASS
→ live compatibility on synthetic/public/minimized data C9 / NOT RUN
→ direct DANTE eval                         C10
→ applicable security/privacy/capacity/economics evidence
→ qualification
→ promotion                                 C11
```

C9 remains fail-closed: `store=false`, SDK automatic retries disabled, background/provider conversation/built-in tools OFF, no private/sensitive data until the applicable retention/ZDR/regional/security evidence passes.

Candidate admission and pre-live PASS are not production qualification. Direct proof obligations remain trigger/applicability gated, including protected Search/reference non-interference, FTS/vector behavior, projection freshness, deletion propagation, durable execution and pgvector provenance.

Missing applicable evidence is not `N/A`.

## 8. Active/unmerged workstreams

```text
feature/access-auth             active product implementation
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-implementation       active AI implementation / C9 OPEN-PRE-LIVE-READY
feature/ai-architecture         architecture design CLOSED / retained authority/evidence
```

Do not infer one branch's implementation from another branch.

## 9. Current next action

```text
feature/ai-implementation
→ C9 P4 real OpenAI Responses / gpt-5.6-terra live compatibility
→ requires a user-owned qualification credential
→ synthetic/public/minimized fixture only
→ no private DANTE data

parallel conditional lane:
I3/C3 resumes only when real owner data/seams are integration-ready
and must converge before I6 read-only Ask DANTE
```

Until that credential is provisioned, C9 remains **OPEN / PRE-LIVE READY** rather than falsely CLOSED. C9 is not production activation. User-visible/private-data Search/Ask still requires the real integration and activation gates defined by the final baseline.