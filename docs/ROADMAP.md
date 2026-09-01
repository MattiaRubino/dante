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

## 6. AI architecture sequence

The AI workstream remains **design/reengineering only**. No provider integration, AI backend runtime, new AI persistence or database evolution is claimed by roadmap text.

Current branch-local sequence:

```text
AI-00
DANTE AI Foundation
semantic / architectural baseline
        ↓
PRODUCT-FORM / INTERACTION RESEARCH
completed earlier in the workstream; AI-00's original "AI-01 next" wording is historical
        ↓
PRODUCTION AI / AGENT ENGINEERING RESEARCH
state-of-the-art techniques
technology challengers
failure/security/performance evidence
DANTE applicability boundary
        ↓
AI-02.1
ACTIVE — DANTE INTELLIGENCE REENGINEERING
v0.5 CANDIDATE STRUCTURAL FREEZE
Round I complete
Round II complete
Final Kill-Test complete
Last Mega Stress-Test complete
Targeted v0.5 consistency verification complete
NO MORE MEGA TESTS
future-extensibility structural criterion PASS
NOT CLOSED — additional user-requested pre-AI-03 review pending
        ↓
AI-03
CONTEXT / RETRIEVAL / MEMORY
BLOCKED until explicit AI-02.1 acceptance/closure
```

### 6.1 AI-00

`architecture/dante-ai-foundation.md` preserves inherited semantic and architectural constraints. It keeps canonical truth, Authority, Visibility/disclosure, provider state, unresolved/candidate state, multi-actor reasoning, stale-state handling, reconciliation, memory classes and durable-execution boundaries distinct. It does not select an SDK, provider, schema or implementation.

The original AI-00 statement that AI-01 was the next step is retained only as historical phase sequencing. It is not current work-queue authority.

### 6.2 Production engineering research

`architecture/ai-production-engineering-state-of-the-art-2026.md` is `RESEARCH / TECHNOLOGY LANDSCAPE / NON-DANTE-DECISION`.

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

### 6.3 AI-02.1 — v0.5 candidate

AI-02.1 asks whether the intelligence architecture survives what DANTE must actually do under the accepted Product/Domain/Logical/Physical/PostgreSQL contracts.

Inputs:

```text
Product / North Star
existing simulations and scenario evidence
accepted Domain semantics
Whole Logical Model / WL-H01..WL-H12
Physical / PostgreSQL authority
AI-00
production engineering research
```

#### Round I

Introduced:

```text
Interaction Session first-class
Semantic Query / Projection Gateway
Context Engine distinct from structured semantic query
Scenario Workspace
ChangeSet / EffectGraph above individual governed effects
Verifier
Attention boundary
Context Projection != recipient-aware Disclosure Projection
DANTE-native + open-world paths composable in one Execution Kernel
ModelTarget + provider-specific HarnessProfile
```

#### Round II

Hardened with:

```text
cumulative / cross-query disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest + dependency-aware invalidation
revocable active-Run validity
Attention budgeting
cancel Run != undo already-dispatched effects
```

#### Final Kill-Test

Added:

```text
Reference / Target Resolution Gate
Policy Composition / Precedence
ConsequenceProfile
Safe Result Publication / Streaming Gate
BasisManifest temporal validity
DANTE canonical representation != external institutional System-of-Record authority
sent != delivered != seen != acknowledged != accepted
```

#### Last Mega Stress-Test

The final broad test combined ordinary life, family, school, shift work, caregiving, agriculture, business, legal/sensitive work, public/institutional boundaries, large fan-out, offline, malicious content, crashes, revocation, supersession, code/computer-use and future much-more-capable intelligence.

It found one remaining fundamental P0 responsibility:

```text
Execution Environment / Isolation
```

and bounded hardenings:

```text
WorkContract propagation through decomposition/child Runs
approval binding/rebinding to the materially approved proposal/basis/effect
Basis coherence in addition to freshness
publication currentness / superseded output suppression
external-agent effect containment
mandatory reconciliation survives optional-resource exhaustion
surface-aware disclosure / realtime input authenticity
telemetry/eval purpose/privacy constraints
future cache hit != current disclosure authorization
```

`Execution Environment` is a logical/runtime boundary, not a mandatory sandbox service. Ordinary trusted deterministic/application work remains on the cheap path. Isolation activates lazily only when the workload/threat model requires it.

Generated/untrusted code must not receive raw privileged DANTE/provider/database credentials. Where it needs privileged action, it uses bounded trusted brokers/capabilities subject to current policy and evidence.

#### Targeted v0.5 verification

The post-test targeted verification checked:

```text
generated-code secret isolation                         PASS STRUCTURAL
execution-environment crash vs Run durability           PASS STRUCTURAL
browser/computer-use effect verification                PASS STRUCTURAL
superseded publication                                  PASS STRUCTURAL
Basis coherence                                         PASS STRUCTURAL
approval rebinding                                      PASS STRUCTURAL
external-agent side effects                             PASS STRUCTURAL
resource exhaustion after ambiguous effect              PASS STRUCTURAL
deterministic fast path bypassing unnecessary isolation PASS STRUCTURAL
```

No additional fundamental responsibility gap emerged. No evidence was found to reopen Domain, Logical, Physical or PostgreSQL.

### 6.4 Future-extensibility acceptance

Structural criterion: **PASS**.

A future DANTE may host much richer general-purpose conversational intelligence, realtime voice, multimodal understanding, code/artifact work, web research, external specialists and substantially stronger future models without transferring ownership of:

```text
canonical memory
canonical application state
Domain semantics
Authority
Visibility
accepted-effect rules
material history
```

Provider/model intelligence remains replaceable cognition around DANTE-owned contracts.

### 6.5 AI-02.1 remaining work

There will be **no more mega-test cycles** in AI-02.1.

The only remaining pre-AI-03 architecture work is the additional review explicitly requested by the user, followed by an explicit AI-02.1 closure/acceptance decision.

If that review reveals a real contradiction, reopen the smallest affected boundary. Do not restart broad simulations merely to keep testing indefinitely.

### 6.6 AI-03 — blocked until closure

AI-03 owns detailed:

```text
Context
Retrieval
Memory
```

AI-03 must consume the accepted structural result of AI-02.1 rather than pre-committing embeddings, vector-store, conversation-history or memory persistence choices from industry fashion.

It must not be used to hide an unresolved AI-02.1 responsibility gap.

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
3. feature/ai-architecture is now at AI-02.1 v0.5 CANDIDATE STRUCTURAL FREEZE
4. perform the additional user-requested pre-AI-03 review
5. if the review passes, make an explicit AI-02.1 closure/acceptance decision
6. only then start AI-03 Context / Retrieval / Memory
```
