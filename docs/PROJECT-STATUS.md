# DANTE — Project Status

- **Status:** CURRENT TRUTH
- **Last reconciled:** 2026-09-01
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA
- **Backend CP6 integration:** PR #42 MERGED
- **PostgreSQL Recovery integration:** PR #47 MERGED / CP01–CP07 LOCAL PASS / CLOSED
- **Current product boundary:** protected `main` includes the accepted PostgreSQL Recovery evolution; Access/Auth, Home React, platform observability and AI architecture remain bounded unmerged workstreams

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED
57 / 57 CLASSIFIED
WL-H01..WL-H12 ACTIVE AS BINDING HARDENINGS

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family
sole canonical persistence / material-history authority
Physical phase-time exact patch 18.4 / HISTORICAL

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
CLOSED / PASS / INTEGRATED VIA PR #28

PRODUCTION BACKEND SCAFFOLD
CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
CP3 CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS

CP6 — CONCRETE POSTGRESQL DATABASE
CLOSED / CONCRETE POSTGRESQL DATABASE PASS
INTEGRATED IN PROTECTED main VIA PR #42
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 CLOSED / GATE 03 PASS
CP6-04 CLOSED / MATERIALIZATION PASS
CP6-05 CLOSED / DIRECT QA PASS

CURRENT POSTGRESQL TECHNICAL PATCH
18.6

HISTORICAL PRE-RECOVERY CP6 BUSINESS DATABASE BASELINE
ALEMBIC 20260826_08
68 tables / 5 views / 14 routines / 75 triggers /
95 indexes / 68 FKs / 120 CHECKs

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

AI ARCHITECTURE
ACTIVE UNMERGED DESIGN / REENGINEERING WORKSTREAM
feature/ai-architecture
AI-00 COMPLETE
AI-01 PRODUCT-FORM + PRODUCTION-ENGINEERING RESEARCH COMPLETE
AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED
AI-02 PRESSURE/MEGA TEST PROGRAM COMPLETE
AI-02 TARGETED v0.5 CONSISTENCY VERIFICATION COMPLETE
NO MORE AI-02 MEGA TESTS
FUTURE-EXTENSIBILITY STRUCTURAL CRITERION PASS
AI-03 CONTEXT / RETRIEVAL / MEMORY ACTIVE
AI-03A FULL CONTEXT ARCHITECTURE CLOSED / STRUCTURALLY ACCEPTED
AI-03A INITIAL CANDIDATE FAIL / 9 HARDENINGS / HARDENED CANDIDATE STRUCTURAL PASS
AI-03A C01..C29 ACCEPTED
CURRENT MACRO-PHASE AI-03B RETRIEVAL + MEMORY ARCHITECTURE
NO AI BACKEND / DB / PROVIDER IMPLEMENTATION CLAIMED

PARALLEL ACTIVE UNMERGED WORKSTREAMS
feature/access-auth
feature/home-react
feature/platform-observability
feature/ai-architecture
```

Architecture/design closure is not runtime/product completion. AI-02.1 and AI-03A closure record structural architecture acceptance only.

## 2. Current protected-main backend/database truth

PR #42 integrated CP6. PR #47 subsequently integrated the closed PostgreSQL Recovery workstream, including forward database evolution `20260830_09`.

Current protected-main database:

```text
PostgreSQL          18.6
Alembic head        20260830_09

tables              69
views                5
routines             15
triggers             76
physical indexes    97
foreign keys         69
CHECK constraints   123

custom enum/domain    0
sequences             0
materialized views    0
RLS policies          0
```

Historical pre-Recovery CP6 baseline:

```text
PostgreSQL          18.6
Alembic head        20260826_08
68 / 5 / 14 / 75 / 95 / 68 / 120
```

Recovery state:

```text
material_state_retirement            materialized
suppression ledger                   versioned / fail-closed
CP01–CP07                            LOCAL PASS / CLOSED
whole operator rehearsal             PASS
database-local reopen                PASS
remote backup provider               TBD / NOT ACTIVATED
production/cloud recovery            NOT CLAIMED
```

Current durable Recovery authority:

- `database/README.md`
- `operations/postgres-recovery-runbook.md`
- `archive/branches/2026-08-feature-postgres-recovery.md` — non-authoritative branch history
- versioned recovery code/harnesses under `infra/local/postgres/recovery/`

## 3. Persistence authority

```text
Domain / Logical / Physical
→ semantic and architectural source

CP6-02 Constitution + ADR-010
→ durable PostgreSQL doctrine

Database System of Record
→ current human-readable database meaning + machine Dictionary

Alembic
→ deployed application-schema evolution authority

SQLAlchemy metadata / mappings
→ application representation of deployed database contract

real PostgreSQL introspection
→ observed materialized database

direct tests
→ executable proof
```

Permanent reconciliation invariant:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

A later structural DB change is incomplete if these representations are left inconsistent.

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

AI architecture adds no exception. Current AI correctness invariants include:

```text
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF INDIVIDUAL EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
USER AUTONOMY != EXTERNAL/INSTITUTIONAL AUTHORITY
DANTE REPRESENTATION != EXTERNAL SYSTEM-OF-RECORD AUTHORITY
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
CONTEXT != RETRIEVAL != MEMORY
CONSUMER CONTEXT != CONTEXT MANIFEST
CONTEXT MANIFEST != BASIS MANIFEST
SOURCE STANDING != DOMAIN AUTHORITY
MODEL-DISCOVERED NEED != WORKCONTRACT/POLICY SCOPE EXPANSION
SESSION CONTINUITY != PROVIDER-CONTEXT CONTINUITY
WORKCONTRACT PROPAGATION != PARENT-CONTEXT INHERITANCE
```

## 5. Reference / material-state baseline

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Consequential AI work uses two orthogonal correctness checks:

```text
Reference / Target Resolution
→ are we acting on the intended canonical target?

BasisManifest / expected state
→ are target state and dependent information still valid/coherent/fresh enough?
```

AI-03A further requires each relevant `InformationNeed` to state the level of reference resolution required for readiness. `AMBIGUOUS` is not solved by model confidence.

Expected MaterialState does not compensate for selecting the wrong-but-current target.

## 6. Backend technical foundation

```text
Python                              3.14.x / initial exact pin 3.14.7
uv                                  repository package authority
schema                              dante
SQLAlchemy                          async 2.0 stable line
psycopg                             3
Alembic                             one environment / one DAG / one head
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per app operation
autobegin=False
autoflush=True
expire_on_commit=False
outer application operation owns transaction
adapter may flush / never implicit commit
READ COMMITTED default

dante_owner                         NOLOGIN ownership identity
dante_migrator                      LOGIN migration identity
dante_runtime                       LOGIN application runtime identity
```

No generic Repository/UoW/BaseService architecture is introduced merely for uniformity.

## 7. Access frontend baseline

The completed pre-backend Access frontend remains the accepted baseline consumed by the current full-stack `feature/access-auth` workstream.

Accepted checkpoints:

```text
AF-01D  PASS
AF-02A  PASS
AF-02B  PASS
AF-03A  PASS
```

The full Access/Auth product vertical is not claimed closed here; its branch-local docs/code/tests own current implementation truth.

## 8. Current bounded unmerged workstreams

```text
feature/access-auth             active unmerged product vertical
feature/home-react              active unmerged frontend workstream
feature/platform-observability  active unmerged platform workstream
feature/ai-architecture         active unmerged AI architecture workstream
                                design/reengineering only
```

Do not infer one branch's implementation from another branch or from this global summary.

A legitimate schema evolution continues to use a reviewed forward Alembic migration synchronized with mappings, Dictionary, human-readable database reference and tests. CP6 is not reopened.

## 9. AI architecture branch-local state

Current durable sources:

```text
docs/architecture/dante-ai-foundation.md
→ AI-00 semantic / architectural baseline

docs/architecture/ai-production-engineering-state-of-the-art-2026.md
→ external production-engineering research / NON-DANTE-DECISION

docs/architecture/dante-ai-02-1-intelligence-reengineering.md
→ AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED

docs/architecture/dante-ai-03-context-retrieval-memory.md
→ AI-03 ACTIVE / AI-03B RETRIEVAL + MEMORY CURRENT

docs/architecture/dante-ai-03a-full-context-architecture.md
→ AI-03A CLOSED / STRUCTURALLY ACCEPTED / C01..C29

docs/workstreams/ai-architecture.md
→ durable active branch/workstream record

docs/workstreams/ai-architecture-live-handoff.md
→ TEMPORARY branch-operational session handoff / MUST NOT MERGE TO main
```

### 9.1 Completed AI-02 simulation/reengineering program

```text
Round I                          COMPLETE
Round II                         COMPLETE
Final Kill-Test                  COMPLETE
Last Mega Stress-Test            COMPLETE
Targeted v0.5 verification       COMPLETE
Additional mega-test cycles      NONE
Domain reopen evidence           NONE
Logical reopen evidence          NONE
Physical/PostgreSQL reopen       NONE
```

Round I established:

```text
Interaction Session
Semantic Query / Projection Gateway
Context Engine separation
Scenario Workspace
ChangeSet / EffectGraph
Verifier
Attention
Context Projection != Disclosure Projection
DANTE-native + open-world composition
ModelTarget + HarnessProfile
```

Round II established/hardened:

```text
cumulative disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest / dependency-aware invalidation
revocable active-Run validity
Attention budgeting
cancel Run != undo already-dispatched effects
```

Final Kill-Test established/hardened:

```text
Reference / Target Resolution
Policy Composition / Precedence
ConsequenceProfile
Safe Result Publication
Basis temporal validity
DANTE representation != external System-of-Record authority
sent != delivered != seen != acknowledged != accepted
```

Last Mega Stress-Test established/hardened:

```text
Execution Environment / Isolation
WorkContract propagation
approval rebinding
Basis coherence
publication currentness
external-agent effect containment
mandatory reconciliation survives resource exhaustion
surface-aware disclosure / consequential realtime input authenticity
telemetry/eval purpose and privacy constraints
future cache hit != current disclosure authorization
```

These are architecture responsibilities/contracts, not implemented modules/services or new Domain/persistence owners.

### 9.2 AI-02 closure

AI-02.1 is formally accepted at the branch-local architecture level:

```text
AI-02.1 v0.5
CLOSED / STRUCTURALLY ACCEPTED
```

This does not claim runtime implementation, provider selection, backend implementation, database materialization or production proof.

### 9.3 AI-03A closure

AI-03A durable authority:

- `docs/architecture/dante-ai-03a-full-context-architecture.md`

The first candidate failed its dedicated mega-test. Nine gaps were hardened and retested before acceptance:

```text
Reality Scope / Scenario binding
Context continuity compartment
model-discovered need scope ceiling
reference-resolution requirement
explicit negative context constraints
child/delegated context minimisation
instruction provenance
non-monotonic ContextReadiness
objective-relative minimisation
```

Accepted Context contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
+ inherited BasisManifest
```

Final result:

```text
AI-03A HARDENED CANDIDATE
STRUCTURAL PASS
C01..C29 ACCEPTED
NO Domain / Logical / Physical / PostgreSQL reopen
NO Alembic change
NO implementation PASS claim
```

### 9.4 Current AI-03 work

Current compact roadmap:

```text
AI-00 COMPLETE
AI-01 COMPLETE
AI-02 COMPLETE / STRUCTURALLY ACCEPTED
AI-03 ACTIVE
  AI-03A Full Context Architecture
           CLOSED / STRUCTURALLY ACCEPTED
  AI-03B Retrieval + Memory Architecture
           ACTIVE / CURRENT
  AI-03C Destructive Validation + Materialization Blueprint
           FUTURE
AI-04 FUTURE Productionization Architecture
AI-05 FUTURE Whole-System Acceptance + Implementation Blueprint
```

Current exact task:

```text
AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
```

AI-03B must consume AI-03A and define retrieval + memory semantics/lifecycle before physical choices. It must not pre-commit memory tables, embeddings, vector-store, conversation persistence, provider memory or model/provider choices.

## 10. Capability-triggered components

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

PostgreSQL transactional outbox
→ real Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first real Class-B durable workflow

pgBackRest LOCAL recovery
→ implemented / whole LOCAL operator rehearsal PASS / integrated via PR #47

remote backup provider
→ TBD; production activation/proof deferred until deployment requires it

AI Execution Environment isolation
→ dormant until a workload/threat model requires it
```

No model provider, SDK, model gateway, local model, sandbox technology, learned router, policy engine or new AI persistence is activated by current documentation.

## 11. Repository / documentation truth

Protected `main` remains integrated authority. Unmerged branch truth remains bounded to its branch until merge.

Current documentation states present truth; historical evidence remains explicitly historical. Temporary handoffs must not become durable `main` authority. Git remains the complete recoverable chronology.

## 12. Next sequence

```text
feature/access-auth
→ continue under its own product gates

feature/home-react
→ continue under its own frontend gates

feature/platform-observability
→ continue under its own platform gates

feature/ai-architecture
→ AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED
→ AI-03 Context / Retrieval / Memory ACTIVE
→ AI-03A Full Context Architecture CLOSED / STRUCTURALLY ACCEPTED
→ current macro-phase AI-03B Retrieval + Memory Architecture
→ then AI-03C Destructive Validation + Materialization Blueprint
→ then AI-04 Productionization Architecture
→ then AI-05 Whole-System Acceptance + Implementation Blueprint
```

No runtime, provider, backend implementation or database PASS is claimed by the AI architecture documentation.
