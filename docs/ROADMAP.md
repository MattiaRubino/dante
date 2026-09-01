# DANTE Roadmap

- **Status:** CURRENT
- **Last reconciled:** 2026-09-01
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA

## 1. Completed foundations

```text
Product / North Star
        CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED / 57 OF 57 / WL-H01..WL-H12
          ↓
Pre-Physical Repository & Architecture Coherence
        CLOSED / FINAL QA PASS
          ↓
Physical Model / Target Selection
        CLOSED / SELECTED / ACCEPTED
        PostgreSQL 18 major family canonical
        exact Physical phase-time patch 18.4 / historical
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        CLOSED / ACCEPTED / INTEGRATED VIA PR #22
          ↓
Frontend Production Materialization
        CLOSED / PASS / INTEGRATED VIA PR #28
          ↓
Backend CP1–CP5 Scaffold
        CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
          ↓
Backend CP6 Concrete PostgreSQL Database
        CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #42
          ↓
PostgreSQL LOCAL Recovery
        CP01–CP07 CLOSED / LOCAL PASS / INTEGRATED VIA PR #47
          ↓
Access Pre-Backend Web Materialization
        CLOSED / ACCEPTED / RELEASE-HARDENED
        AF-01D / AF-02A / AF-02B / AF-03A PASS
```

Architecture closure remains distinct from product/runtime completion. Closing the pre-backend Access frontend does not close the real full-stack Access/Auth product vertical. Closing LOCAL PostgreSQL Recovery does not claim remote/cloud production recovery.

## 2. Current PostgreSQL / Recovery baseline

Historical pre-Recovery CP6 baseline:

```text
PostgreSQL          18.6
Alembic             20260826_08
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

Current protected-main database / Recovery baseline:

```text
PostgreSQL          18.6
Alembic             20260830_09
69 tables
5 views
15 routines
76 triggers
97 physical indexes
69 foreign keys
123 CHECK constraints
CP01–CP07           LOCAL PASS / CLOSED
Recovery            INTEGRATED VIA PR #47
remote provider     TBD / NOT ACTIVATED
cloud recovery      NOT CLAIMED
```

CP6 and Recovery checkpoint chronology are historical implementation/acceptance work. Do not route new work through old Gate 03, DB-U*, CP6-04, Recovery CP01–CP07 or protected-main-alignment steps.

Current database / Recovery authority:

- `database/README.md`
- `database/dictionary/`
- `operations/postgres-recovery-runbook.md`
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `development/backend-cp6-05-whole-database-qa.md`
- executable Recovery harnesses under `../infra/local/postgres/recovery/`

## 3. Active bounded unmerged workstreams

At the 2026-09-01 reconciliation, bounded unmerged work includes:

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-architecture         active AI architecture design/reengineering work
```

These branches remain intentionally independent. Each owns only its bounded newer truth until protected-main integration.

## 4. Database evolution after CP6 / Recovery

Permanent same-change rule:

```text
real structural database change
→ Alembic forward migration
→ SQLAlchemy mapping/metadata update
→ Database Dictionary update
→ human-readable reference update when meaning/topology changes
→ generated artifacts/diagrams where governed
→ direct tests
→ affected recovery/operational assertions updated when head/topology changes
```

Applied revisions are immutable. A product vertical may reveal a legitimate schema evolution need; that becomes a normal reviewed forward change and does not reopen CP6 or the closed Recovery workstream.

Current protected-main migration baseline: `20260830_09`.

## 5. Capability-triggered implementation

Selected specialist components activate only at real product/operational triggers:

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

PgBouncer
→ concrete connection-management need + direct validation

pgBackRest LOCAL recovery
→ implemented, directly rehearsed and integrated via PR #47

remote backup provider
→ TBD; trigger only at a real production deployment boundary

AI Execution Environment isolation
→ activate only for generated-code/untrusted/browser/computer-use or comparable workload/threat-model needs
```

A selected component is not implemented merely because it appears in architecture. Research challengers do not become dependencies merely because they appear in the landscape.

## 6. Current AI architecture roadmap

The earlier exploratory AI-00..AI-12 decomposition is **historical planning only**. It is not current routing and must not be used to infer that already-resolved Authority, conversation, tool, execution, security or simulation work is still waiting as an independent phase.

The current compact roadmap is:

```text
AI-00 — SEMANTIC & PRODUCT FOUNDATION
COMPLETE
        ↓
AI-01 — PRODUCT FORM + PRODUCTION ENGINEERING RESEARCH
COMPLETE
        ↓
AI-02 — INTELLIGENCE RUNTIME ARCHITECTURE
COMPLETE / STRUCTURALLY ACCEPTED
AI-02.1 v0.5
        ↓
AI-03 — CONTEXT / RETRIEVAL / MEMORY
ACTIVE
    ├ AI-03A FULL CONTEXT ARCHITECTURE
    ├ AI-03B RETRIEVAL + MEMORY ARCHITECTURE
    └ AI-03C DESTRUCTIVE VALIDATION + MATERIALIZATION BLUEPRINT
        ↓
AI-04 — PRODUCTIONIZATION ARCHITECTURE
FUTURE
    ├ evals + model/provider/economics
    ├ concrete runtime/capabilities/external intelligence
    └ security/privacy + persistence/control-plane/operations
        ↓
AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE
```

Security, privacy, simulation and evaluation are cross-cutting disciplines. They are applied while each phase is designed and receive dedicated assurance/acceptance passes later; they are not ignored until a late numbered stage.

The AI workstream remains **design/reengineering only**. No provider integration, AI backend runtime, new AI persistence or database evolution is claimed by roadmap text.

### 6.1 AI-00 — complete

`architecture/dante-ai-foundation.md` preserves inherited semantic and architectural constraints. It keeps canonical truth, Authority, Visibility/disclosure, provider state, unresolved/candidate state, multi-actor reasoning, stale-state handling, reconciliation, memory classes and durable-execution boundaries distinct. It does not select an SDK, provider, schema or implementation.

AI-00's original statement that AI-01 was the next step is historical sequencing only.

### 6.2 AI-01 — complete research/product-form layer

This phase label groups completed product-form/interaction research and production-engineering research.

`architecture/ai-production-engineering-state-of-the-art-2026.md` remains `RESEARCH / TECHNOLOGY LANDSCAPE / NON-DANTE-DECISION`.

Current applicability constraints include:

```text
frontier intelligence expected API-first
NO foundation-model training
NO DANTE-owned frontier model
NO fine-tuning requirement as baseline
NO large always-on self-hosted model fleet
NO GPU cluster as baseline
small/local inference optional and benchmark-gated
provider/model/SDK selection still open
```

### 6.3 AI-02 — complete / structurally accepted

AI-02.1 pressure-tested the runtime/intelligence architecture against Product/Domain/Logical/Physical/PostgreSQL authority.

Completed evidence:

```text
Round I
Round II
Final Kill-Test
Last Mega Stress-Test
Targeted v0.5 consistency verification
```

Accepted structural responsibilities include:

```text
Interaction Session
WorkContract
Work Supersession
Reference / Target Resolution
ConsequenceProfile
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
ModelTarget / HarnessProfile
Capability Runtime
Execution Environment
Verifier
Policy mesh
ChangeSet / EffectGraph
Effect Runtime
Result Maturity
Disclosure
Safe Result Publication
Attention
```

AI-02.1 is now:

```text
v0.5
CLOSED / STRUCTURALLY ACCEPTED
NO MORE AI-02 MEGA TESTS
NO DOMAIN / LOGICAL / PHYSICAL / POSTGRESQL REOPEN
NO RUNTIME / BACKEND / PROVIDER IMPLEMENTATION PASS CLAIMED
```

### 6.4 AI-03 — active

Durable phase charter:

- `architecture/dante-ai-03-context-retrieval-memory.md`

Current macro-phase:

```text
AI-03A — FULL CONTEXT ARCHITECTURE
```

AI-03A owns the complete path from `WorkContract` to the exact purpose-bound, authorized, provenance-bearing, freshness/coherence-aware `ContextManifest` delivered to a reasoning consumer.

AI-03B then defines structured/lexical/semantic/hybrid retrieval and Interaction/working/derived/provider/retrieval-memory classes with admission, correction, decay, retirement, deletion and anti-resurrection.

AI-03C finally runs destructive validation and produces the materialization blueprint that decides what stays transient, what is recomputable, what is provider-owned optimization, what is justified durable derived state, what may require PostgreSQL/index evolution and what must not be stored.

Explicit AI-03 rule:

```text
AI-03 ACTIVE
!=
authorization to create memory tables / embeddings / vector indexes
```

Materialization follows demonstrated semantic need and destructive validation.

### 6.5 AI-04 — future productionization architecture

After AI-03 closure, AI-04 resolves the remaining concrete production architecture in three tightly related areas:

```text
A. representative DANTE eval workload, quality floors,
   model/provider/economics, routing/fallback/local-model triggers

B. concrete runtime/capabilities/external-intelligence implementation,
   background/durable work, MCP/A2A/API boundaries,
   browser/computer-use/code execution and Execution Environment

C. whole-design security/privacy assurance plus justified
   AI persistence/control-plane/observability/audit/resource operations
```

Provider/model selection follows workload/evaluation evidence rather than preceding it.

### 6.6 AI-05 — future whole-system acceptance + implementation blueprint

AI-05 is the final architecture-to-build boundary.

It will run representative end-to-end acceptance across the fully specified Context/Memory/provider/runtime/persistence design, then produce:

```text
module / port / adapter boundaries
physical schemas
migration sequence
backend/frontend contracts
provider adapters
workers
feature flags
eval gates
rollout strategy
first implementation vertical
```

AI-05 is not a license to reopen accepted semantics for implementation convenience.

## 7. Persistent frontend direction

The generic frontend engineering foundation, production materialization and pre-backend Access Web materialization are closed. Future frontend work is vertical/product work.

Persistent rules remain:

```text
backend + PostgreSQL own canonical accepted effect
Web baseline online-first
Mobile local/offline state remains noncanonical
identity-scoped local data
feature-first app boundaries
route/navigation adapters remain thin
shared packages require real multi-consumer value
production never imports prototypes
current design tokens / i18n / time contracts remain governed
```

## 8. Infrastructure / release boundaries still deferred

Still trigger-bound/not currently complete:

```text
production backend compute provider / sizing
IaC engine and production infrastructure rollout
production registry/release pipeline where not yet required
remote-provider production recovery/retention acceptance
real V1→V2 business-schema evolution rehearsal
PowerSync product activation
Restate product activation
AI provider/model adapter implementation
AI Execution Environment implementation
AI local-model activation
AI Context/Retrieval/Memory persistence
AI runtime module/service implementation
exact target-resolution implementation
exact policy-composition engine/product
exact safe-streaming/publication implementation
production deployment
```

When these become real workstreams, current evidence must replace design-time assumptions.

## 9. Documentation lifecycle baseline

```text
current specifications state current truth directly
temporary live/session handoffs do not enter protected main
completed branch history is retained only when materially useful
historical evidence is explicitly non-authoritative
frozen split documents are compacted only when lossless knowledge coverage is proven
Git remains the complete recoverable chronology
post-merge documentation must be reconciled from candidate state to protected-main state
```

## 10. Persistent engineering rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 RUNTIME CLAIM
POSTGRESQL PATCH REFRESH != PHYSICAL ARCHITECTURE REOPEN
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
DATABASE MATERIALIZATION != PRODUCT APPLICATION IMPLEMENTATION
RESEARCH TECHNOLOGY != DANTE IMPLEMENTATION SELECTION
MODEL/PROVIDER OUTPUT != CANONICAL EFFECT
MODEL CAPABILITY != AUTHORITY
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
DISPLAY NAME != EFFECT TARGET
SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF INDIVIDUAL EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
DANTE-GENERATED SIGNAL != AUTOMATIC JUSTIFICATION FOR ANOTHER ADAPTATION
USER AUTONOMY != EXTERNAL/INSTITUTIONAL AUTHORITY
SOURCE VERSION UNCHANGED != SOURCE NECESSARILY FRESH
DANTE REPRESENTATION != EXTERNAL SYSTEM-OF-RECORD AUTHORITY
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
```

## 11. Immediate sequence

```text
1. Recovery is CLOSED / integrated; do not resume feature/postgres-recovery
2. continue feature/access-auth, feature/home-react and feature/platform-observability independently under their own scopes
3. feature/ai-architecture has closed AI-02.1 v0.5 as STRUCTURALLY ACCEPTED
4. AI-03 Context / Retrieval / Memory is ACTIVE
5. current exact AI task = AI-03A Full Context Architecture
6. complete AI-03A, then AI-03B, then AI-03C before any AI Context/Memory materialization
7. after AI-03 closure proceed to AI-04 Productionization Architecture
8. finish with AI-05 Whole-System Acceptance + Implementation Blueprint
```
