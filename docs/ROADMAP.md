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

## 2. CP6 and PostgreSQL Recovery are complete

CP6 converted the closed Domain + Logical + Physical model into the concrete DANTE PostgreSQL database.

```text
CP6-00  COMPLETE
CP6-01  CLOSED / GATE 01 PASS
CP6-02  CLOSED / GATE 02 PASS
CP6-03  CLOSED / GATE 03 PASS
CP6-04  CLOSED / MATERIALIZATION PASS
CP6-05  CLOSED / DIRECT QA PASS
CP6      CLOSED / CONCRETE POSTGRESQL DATABASE PASS
         INTEGRATED VIA PR #42
```

Historical pre-recovery CP6 baseline:

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

PR #47 integrated the closed Recovery branch into protected `main` with merge commit `bdd2b2370d41423dbaecd00fde86bb2bf2466f2b`. Recovery is therefore no longer an integration candidate or active branch boundary.

CP6 and Recovery checkpoint chronology are historical implementation/acceptance work now. Do not route new work through old Gate 03, DB-U*, CP6-04, Recovery CP01–CP07 or protected-main-alignment steps.

Current database / Recovery authority:

- `database/README.md`
- `database/dictionary/`
- `operations/postgres-recovery-runbook.md`
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `development/backend-cp6-05-whole-database-qa.md`
- executable Recovery harnesses under `../infra/local/postgres/recovery/`

Historical branch records:

- `archive/branches/2026-08-feature-logical-postgresql.md`
- `archive/branches/2026-08-feature-postgres-recovery.md`

## 3. Access frontend materialization is closed

The pre-backend Access Web workstream completed:

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

It intentionally stops backend-authoritative transitions instead of fabricating authentication success. Current frontend truth is `frontend/access.md` plus current code/tests. The closed branch history is `archive/branches/2026-08-feature-access-frontend.md`.

Closing this workstream does not mean real Access/Auth is complete.

## 4. Active bounded unmerged workstreams

The project is no longer waiting to start its first post-CP6 vertical. At the 2026-09-01 reconciliation, bounded unmerged work includes:

```text
feature/access-auth             active full-stack product work
feature/home-react              active frontend work
feature/platform-observability  active platform work
feature/ai-architecture         active AI-02.1 architecture reengineering / design-only
```

Additional live refs may exist and remain authoritative for their own later changes. PostgreSQL Recovery is intentionally absent from this list because it is closed and integrated via PR #47.

These active branches are intentionally independent and own only their bounded truth until integration. Do not collapse them into a single mega-branch and do not rewrite protected-main truth from an unmerged branch.

## 5. Database evolution after CP6 / Recovery

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

The current protected-main migration baseline is `20260830_09`. Any branch-local migration chain created from an older common baseline must be explicitly reconciled before its own integration rather than creating accidental multiple Alembic heads.

## 6. Capability-triggered implementation

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
```

A selected component is not implemented merely because it appears in architecture. Research challengers such as DBOS, ReBAC engines, alternative sandbox implementations, learned model routers, self-hosted inference servers or specialist vector databases do not reopen an accepted component or become dependencies merely because they appear in the AI research landscape.

AI-02.1 responsibility boundaries and hardenings are likewise not activated technologies or separate services by virtue of appearing in architecture.

## 7. AI architecture sequence

The AI workstream remains **design/reengineering only**. No provider integration, AI backend runtime, new AI persistence or database evolution is claimed by roadmap text.

Current branch-local sequence:

```text
AI-00
DANTE AI Foundation
semantic / architectural baseline
        ↓
PRODUCTION AI / AGENT ENGINEERING RESEARCH
state-of-the-art techniques
technology challengers
failure/security/performance evidence
DANTE applicability boundary
        ↓
AI-02.1
ACTIVE — DANTE INTELLIGENCE REENGINEERING
v0.3 current checkpoint
Round I complete
Round II complete
final kill-test still required
future-extensibility acceptance still required
NOT CLOSED
        ↓
AI-03
CONTEXT / RETRIEVAL / MEMORY
BLOCKED until AI-02.1 structural acceptance
```

### AI-00

`architecture/dante-ai-foundation.md` preserves the inherited semantic and architectural constraints. It keeps canonical truth, Authority, visibility/disclosure, provider state, unresolved/candidate state, multi-actor reasoning, stale-state handling, reconciliation, memory classes and durable-execution boundaries distinct. It does not select an SDK, provider, schema or implementation.

### Production engineering research

`architecture/ai-production-engineering-state-of-the-art-2026.md` records external production-engineering evidence as of 2026-09-01. It is deliberately marked `RESEARCH / TECHNOLOGY LANDSCAPE / NON-DANTE-DECISION`.

The current DANTE applicability constraints recorded by that research are:

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

The research may recommend patterns or list challengers without pre-activating technologies.

### AI-02.1 — ACTIVE

AI-02.1 is not a provider-selection phase. It is a **reengineering and pressure-test of the DANTE Intelligence Architecture** starting from actual product obligations.

Required inputs include:

```text
Product / North Star
existing DANTE simulations and scenario evidence
what DANTE must actually be able to do
accepted Domain semantics
Whole Logical Model / WL-H01..WL-H12
Physical / PostgreSQL authority
AI-00
production engineering research
```

Round I produced the initial reengineering checkpoint and introduced:

```text
Interaction Session first-class
Semantic Query / Projection Gateway
Context Engine kept distinct from structured semantic query
Simulation / Hypothetical State Workspace
ChangeSet / EffectGraph above individual governed effects
Verifier / Auditor primitive
Proactivity / Attention boundary
Context Projection != recipient-aware Disclosure Projection
DANTE-native + open-world paths composable in one Execution Kernel
ModelTarget + provider-specific HarnessProfile
```

Round II then deliberately combined concurrency, stale basis, multi-actor privacy, revocation, partial effects, crashes, corrections, feedback loops and superseding user intent. It found no evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL, but it did require the v0.3 hardenings:

```text
cumulative / cross-query disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest + dependency-aware invalidation
revocable active-Run validity
Attention budgeting
cancel Run != undo already-dispatched effects
```

These are responsibility/runtime contracts, not new Domain owners or automatic persistence tables/services.

The final acceptance round must now attack those exact hardenings in combination rather than replaying the easier cases. Required dimensions include:

```text
cumulative privacy probing
scope-aware work supersession
stale scenario dependencies
revoked Authority/Consent during durable waits
self-generated feedback / oscillation
multiple simultaneous Attention demands
partial external effects + timeout + crash/recovery
source correction/retirement
non-DANTE participants
conflicting evidence
cancellation after partial dispatch
future mixed open-world + DANTE-native work
```

The architecture is accepted only if that final kill-test does not require semantic collapse, hidden provider ownership of truth, a duplicate application ontology or unjustified infrastructure.

A specific acceptance criterion remains **future extensibility**:

> If DANTE later gains a much richer integrated general-purpose conversational intelligence — including capabilities comparable to future frontier chat systems — or adopts substantially more capable future models/providers/specialists, the architecture must absorb that improvement without transferring canonical memory, Authority, application state or effect ownership to the model/provider and without requiring a fundamental redesign of the product core.

AI-02.1 may refine architecture responsibilities and contracts. Any impact on closed Domain/Logical/Physical/database authority must satisfy normal reopen discipline rather than being silently reinterpreted for AI convenience.

### AI-03 — after AI-02.1

AI-03 owns the detailed **Context / Retrieval / Memory** architecture. It must consume the structurally accepted result of AI-02.1 rather than pre-committing retrieval, embeddings, vector-store, conversation-history or memory persistence decisions from industry fashion.

AI-03 must not be used to hide or repair an unresolved AI-02.1 responsibility gap.

## 8. Persistent frontend direction

The generic frontend engineering foundation, production materialization and pre-backend Access Web materialization are closed. Future frontend work is vertical/product work rather than another generic foundation phase.

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

## 9. Infrastructure / release boundaries still deferred

Do not prematurely materialize infrastructure merely to complete a diagram.

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
AI sandbox implementation
AI local-model activation
AI context/retrieval/memory persistence
AI-02.1 runtime module/service implementation
production deployment
```

When these become real workstreams, current evidence must replace design-time assumptions.

## 10. Documentation lifecycle baseline

```text
current specifications state current truth directly
temporary live/session handoffs do not enter protected main
completed branch history is retained only when materially useful
historical evidence is explicitly non-authoritative
frozen split documents are compacted only when lossless knowledge coverage is proven
Git remains the complete recoverable chronology
post-merge documentation must be reconciled from candidate state to protected-main state
```

Current authority:

- `development/documentation-lifecycle-policy.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/operating-rules.md`
- `docs/README.md`

Fewer files is not a success criterion by itself. Remove/compact only after knowledge coverage.

## 11. Persistent engineering rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
HISTORICAL 18.4 EVIDENCE != CURRENT 18.6 RUNTIME CLAIM
POSTGRESQL PATCH REFRESH != PHYSICAL ARCHITECTURE REOPEN
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
DATABASE MATERIALIZATION != PRODUCT APPLICATION IMPLEMENTATION
DETERMINABLE SCHEMA EVOLUTION != SPECULATIVE PRE-MATERIALIZATION
TEMPORARY HANDOFF != DURABLE main DOCUMENTATION
MERGED BRANCH CANDIDATE STATE != CURRENT protected-main STATUS
RESEARCH TECHNOLOGY != DANTE IMPLEMENTATION SELECTION
MODEL/PROVIDER OUTPUT != CANONICAL EFFECT
MODEL CAPABILITY != AUTHORITY
SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF INDIVIDUAL EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
DANTE-GENERATED SIGNAL != AUTOMATIC JUSTIFICATION FOR ANOTHER ADAPTATION
```

## 12. Immediate sequence

```text
1. Recovery is CLOSED / integrated; do not resume feature/postgres-recovery
2. continue feature/access-auth, feature/home-react and feature/platform-observability independently
3. on feature/ai-architecture, continue AI-02.1 from the recorded v0.3 checkpoint
4. execute the final kill-test against cumulative disclosure, supersession, causal loops, revocation, stale dependencies and partial effects
5. complete the additional pre-AI-03 review explicitly required by the active workstream before starting AI-03
6. keep future-extensibility against a rich integrated frontier-chat-style intelligence as an acceptance criterion
7. AI-03 owns Context / Retrieval / Memory only after AI-02.1 structural acceptance
8. before each integration, reconcile the active branch against the then-current protected-main baseline
9. evolve the database only through same-change forward migrations when a real vertical requires it
10. keep remote backup/cloud recovery deferred until production deployment creates a real need
11. apply documentation lifecycle cleanup before integration AND post-merge current-state reconciliation afterward
12. use live Git refs and branch-local authority rather than stale global assumptions
```

This roadmap intentionally does not pre-create future branches, migrations, APIs, provider integrations or infrastructure before their concrete scope is authorized.
