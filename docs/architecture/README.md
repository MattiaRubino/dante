# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-09-01

This file describes the current architecture state directly. Phase-time reviews, old branch overlays and pre-closure status remain evidence in their owning documents/Git history and do not override this index.

## 1. Current architecture state

```text
Domain Model                         CLOSED
Logical Model                        CLOSED / 57 OF 57 / REMOTE QA PASS
WD-03 / WD-05                        PASS
Pre-Physical coherence               CLOSED / FINAL QA PASS
Physical target                      CLOSED / ACCEPTED
Engineering Foundation               CLOSED / ACCEPTED
Frontend Engineering Foundation      CLOSED / INTEGRATED VIA PR #22
Frontend Materialization             CLOSED / PASS / INTEGRATED VIA PR #28
Backend CP1–CP5 scaffold             CLOSED / DIRECT QA / INTEGRATED VIA PR #24
Backend CP6 PostgreSQL database       CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL architecture              18 major family / sole canonical persistence + material-history authority
Current PostgreSQL patch             18.6
Current Alembic head                 20260830_09
Current DB topology                  69 tables / 5 views / 15 routines / 76 triggers / 97 indexes / 69 FKs / 123 CHECKs
PostgreSQL local Recovery            CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED VIA PR #47
Full Access/Auth product vertical    ACTIVE / UNMERGED ON feature/access-auth
AI architecture                      ACTIVE / DESIGN ONLY ON feature/ai-architecture
AI-02.1                              v0.5 CLOSED / STRUCTURALLY ACCEPTED
AI mega/pressure-test program        COMPLETE
AI targeted v0.5 verification        COMPLETE
AI-03                                ACTIVE / CONTEXT + RETRIEVAL + MEMORY
AI-03A                               CLOSED / STRUCTURALLY ACCEPTED / C01..C29
AI-03 current macro-phase            AI-03B RETRIEVAL + MEMORY ARCHITECTURE
```

Protected `main` is the integrated authority for closed shared foundations, CP6 and the integrated Recovery evolution. Active unmerged product/architecture work remains branch-local until normal protected-main integration.

## 2. Current architecture entry points

Read according to the subject:

- [`system-overview.md`](system-overview.md) — system/component/authority overview;
- [`dante-ai-foundation.md`](dante-ai-foundation.md) — AI-00 semantic/architectural baseline; inherited constraints remain active and are not superseded by later AI phases;
- [`ai-production-engineering-state-of-the-art-2026.md`](ai-production-engineering-state-of-the-art-2026.md) — production AI/agent engineering research thesis; state-of-the-art evidence and DANTE applicability boundaries, explicitly **not** the final DANTE Intelligence Architecture;
- [`dante-ai-02-1-intelligence-reengineering.md`](dante-ai-02-1-intelligence-reengineering.md) — **AI-02.1 accepted structural runtime architecture**; v0.5 after all pressure/kill-test rounds and targeted consistency verification;
- [`dante-ai-03-context-retrieval-memory.md`](dante-ai-03-context-retrieval-memory.md) — **active AI-03 architecture charter**; current macro-phase AI-03B Retrieval + Memory Architecture;
- [`dante-ai-03a-full-context-architecture.md`](dante-ai-03a-full-context-architecture.md) — **AI-03A accepted Full Context Architecture**; hardened candidate, C01..C29, dedicated mega-test evidence;
- [`technical-decisions.md`](technical-decisions.md) — current architecture decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical semantic compatibility contract;
- [`../domain/README.md`](../domain/README.md) — current Domain entry point;
- [`../logical-model/README.md`](../logical-model/README.md) — current Logical Model entry point and closure routing;
- [`../physical-model/README.md`](../physical-model/README.md) — accepted Physical Model target;
- [`../database/README.md`](../database/README.md) — current concrete PostgreSQL System of Record;
- [`../decisions/`](../decisions/) — ADR authority;
- [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md) — backend engineering foundation;
- [`frontend-engineering-foundation.md`](frontend-engineering-foundation.md) and accepted companion/review records — frontend engineering foundation;
- [`../frontend/README.md`](../frontend/README.md) — current frontend documentation entry point.

Active branch continuation additionally uses:

- [`../workstreams/ai-architecture.md`](../workstreams/ai-architecture.md) — durable branch-local AI workstream record;
- [`../workstreams/ai-architecture-live-handoff.md`](../workstreams/ai-architecture-live-handoff.md) — TEMPORARY branch-operational save-game; must not merge to protected `main`.

Important persistence ADRs:

- [`../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`](../decisions/ADR-007-domain-model-informed-persistence-boundaries.md);
- [`../decisions/ADR-010-postgresql-persistence-constitution.md`](../decisions/ADR-010-postgresql-persistence-constitution.md);
- [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md) — historical PostgreSQL-selection rationale where explicitly historical.

Important frontend ADRs:

- [`../decisions/ADR-008-frontend-engineering-stack.md`](../decisions/ADR-008-frontend-engineering-stack.md);
- [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md).

## 3. Current system direction

DANTE remains one product monorepo. The backend remains a capability-first modular monolith. Responsibility boundaries are not automatically deployable services.

Canonical persistence direction:

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current repository/runtime patch
= PostgreSQL 18.6

current Alembic head
= 20260830_09
```

The accepted Domain → Logical → Physical chain has already been concretely materialized through CP6 and the bounded Recovery lifecycle evolution. Later backend/product/AI work consumes that database rather than reopening the architecture because a feature/framework/provider prefers a different shape.

AI architecture inherits the same rule: model/provider/runtime output is not accepted canonical effect, and no AI-specific persistence shortcut may redefine closed Domain/Logical/Physical/database semantics.

## 4. AI authority layering and current roadmap

Current branch-local AI authority is deliberately layered:

```text
AI-00
DANTE AI Foundation
→ inherited / derived semantic guardrails

AI-01
Product Form + Production Engineering Research
→ completed interaction/product-form + engineering evidence
→ research technology remains NON-DANTE-DECISION unless later selected

AI-02
DANTE Intelligence Runtime Architecture
→ AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED

AI-03A
Full Context Architecture
→ CLOSED / STRUCTURALLY ACCEPTED
→ dedicated mega-test / 9 hardenings / C01..C29

AI-03
Context / Retrieval / Memory
→ ACTIVE
→ current macro-phase AI-03B Retrieval + Memory Architecture
```

The previous longer exploratory AI-00..AI-12 decomposition is historical planning only. Current routing is:

```text
AI-00  Semantic & Product Foundation                         COMPLETE
AI-01  Product Form + Production Engineering Research         COMPLETE
AI-02  Intelligence Runtime Architecture                      COMPLETE / STRUCTURALLY ACCEPTED
AI-03  Context / Retrieval / Memory                           ACTIVE
       ├ AI-03A Full Context Architecture
       │        CLOSED / STRUCTURALLY ACCEPTED
       ├ AI-03B Retrieval + Memory Architecture
       │        ACTIVE / CURRENT
       └ AI-03C Destructive Validation + Materialization Blueprint
                FUTURE
AI-04  Productionization Architecture                         FUTURE
AI-05  Whole-System Acceptance + Implementation Blueprint     FUTURE
```

Security, privacy, simulations and evals remain cross-cutting disciplines rather than late afterthoughts.

AI-02.1 does not normatively rewrite AI-00. AI-00's original sequencing toward AI-01 is historical workstream chronology; later product-form/research/reengineering work has already consumed that scheduling note.

## 5. AI-02.1 v0.5 accepted structural model

The completed test program converged on the following responsibilities.

### Interaction / work

```text
Interaction Edge
Interaction Session
Work Intake
WorkContract
Work lineage / continuation / supersession
ConsequenceProfile
Reference / Target Resolution
```

`Interaction Session != Run != Worker`.

`WorkContract` preserves the authoritative execution meaning across decomposition and child Runs:

```text
objective
scope
resolved target bindings
protected constraints
purpose
consequence/governance obligations
approval conditions
```

Derived work may refine this contract but must not silently drop a protected requirement. A material relaxation requires a new/superseding decision.

### State / context / scenarios

```text
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
```

Semantic Query and Context are distinct. Structured DANTE-native state is accessed through application-owned semantic query/projection contracts; arbitrary unstructured/external/contextual material is assembled by the Context Engine.

Scenario Workspace is hypothetical/derived and does not create a second canonical reality.

`BasisManifest` tracks relevant dependencies, source identity/version, temporal validity, assumptions and constraints. It also captures **Basis coherence**: independently fresh values are not automatically one coherent world-state.

Detailed Context is now fixed by AI-03A; Retrieval/Memory details are owned by active AI-03B.

### Reasoning / capabilities

```text
ModelTarget + HarnessProfile
Deterministic Compute
Solver
Capability Runtime
Verifier
Execution Environment
```

A simple deterministic request must stay on the cheap path and may use no model and no isolated environment.

`Execution Environment` is a runtime/security responsibility for workloads whose threat model requires isolation, such as generated code, hostile executable artifacts, browser/computer-use or comparable workloads.

```text
Execution Environment != mandatory sandbox/container
```

Isolation is selected lazily by workload and may use different techniques. Generated/untrusted code does not receive raw privileged DANTE/provider/database credentials; privileged operations flow through bounded trusted capabilities/brokers.

### Governance / effects

```text
Policy Composition / policy mesh
Authority / AuthZ / Consent / Visibility
Autonomy
ConsequenceProfile
ChangeSet / EffectGraph
Effect Runtime
Approval binding
Verification / Reconciliation
```

Policy is not one model-chosen linear verdict. Enforcement may occur at context, capability, effect and publication/egress boundaries.

Approval binds to the materially approved target/proposal/basis/effect semantics. A materially changed ChangeSet cannot silently reuse an old approval.

`ChangeSet / EffectGraph` coordinates compound change but does not bypass individual governed effects.

`CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS`.

Resource exhaustion may stop optional work but must not erase a reconciliation obligation created by an already-dispatched ambiguous effect.

### Publication / privacy / attention

```text
Context Projection
Disclosure Projection
cumulative inference protection
Safe Result Publication
Result Maturity
publication currentness
Attention + Attention budgeting
causal-loop / oscillation guard
```

```text
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
```

Safe Publication rechecks recipient/surface eligibility, result maturity and work currentness. A superseded/stale Run may reconcile old work but must not continue presenting obsolete output as the current result.

Disclosure is surface-aware: lock screen, voice/realtime, shared UI and another recipient may require different safe representations.

Attention is a scarce resource and may aggregate/suppress individually relevant signals.

### External AI / agents

DANTE supports both directions conceptually:

```text
AI inside DANTE
DANTE exposed to external AI/agent clients
```

External protocol adapters such as MCP/A2A remain edge adapters, not internal Domain ontology.

A delegated external intelligent system may perform consequential effects only when either:

```text
1. the effect returns through governed DANTE capabilities
or
2. it is honestly treated as an externally performed effect whose outcome must be observed/reconciled
```

DANTE must not falsely claim its own governance for a side effect performed outside that boundary.

## 6. AI-03A accepted Full Context Architecture

Durable authority:

- [`dante-ai-03a-full-context-architecture.md`](dante-ai-03a-full-context-architecture.md)

AI-03A closes Context around seven accepted runtime contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
```

plus inherited `BasisManifest`.

The accepted flow is:

```text
WorkContract
→ ContextPlan
→ InformationNeeds
→ strategy per need
→ discovery/acquisition eligibility
→ source read / source binding
→ ContextFragments
→ Reality Scope / Provenance / Source Standing /
  Integrity / Canonicality / Instruction Provenance /
  Confidentiality / Temporal Validity / Contradiction
→ coverage + coherence
→ ContextReadiness
→ minimisation/transformation
→ resource-aware packing
→ consumer/provider exposure eligibility
→ ConsumerContext
→ Harness/consumer invocation
→ ContextManifest exposure receipt
→ bounded JIT acquisition when required
```

The initial candidate failed and was hardened through:

```text
GAP-01 Reality Scope / Scenario binding
GAP-02 Interaction Session continuity != provider-context continuity
GAP-03 model-discovered InformationNeed scope ceiling
GAP-04 per-need Reference Resolution requirement
GAP-05 explicit source/use exclusions
GAP-06 child/delegated context minimisation
GAP-07 user-originated content != automatic instruction authority
GAP-08 non-monotonic ContextReadiness
GAP-09 objective-relative minimisation
```

After retest:

```text
AI-03A HARDENED CANDIDATE      STRUCTURAL PASS
AI-03A invariants              C01..C29 ACCEPTED
Domain/Logical/Physical reopen NO
PostgreSQL/Alembic change      NO
implementation claim           NONE
```

Key non-collapse rules:

```text
CONTEXT != CANONICAL REALITY
CONTEXT != RETRIEVAL != MEMORY
SOURCE STANDING != DOMAIN AUTHORITY
CONSUMER CONTEXT != CONTEXT MANIFEST
CONTEXT MANIFEST != BASIS MANIFEST
EXPOSURE != MATERIAL DEPENDENCY
DATA != INSTRUCTION
INTERACTION SESSION CONTINUITY != PROVIDER-CONTEXT CONTINUITY
WORKCONTRACT PROPAGATION != PARENT-CONTEXT INHERITANCE
MODEL-DISCOVERED NEED != SCOPE EXPANSION
SCENARIO A != SCENARIO B != CANONICAL CURRENT
```

Context machinery is bypassable for deterministic structured work that does not need a composed ConsumerContext.

## 7. AI-03B current architecture boundary

Durable phase charter:

- [`dante-ai-03-context-retrieval-memory.md`](dante-ai-03-context-retrieval-memory.md)

Current exact task:

```text
AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
```

AI-03B must consume every AI-03A Context invariant while defining:

```text
RETRIEVAL
structured/current/history query paths
relation traversal
metadata / lexical / fuzzy retrieval
semantic/vector retrieval where justified
hybrid retrieval / reranking
source reread/currentness
coverage-aware retrieval
permission-aware discovery/retrieval
iterative/JIT retrieval
large-document hierarchy/chunking
long-context vs indexed retrieval
retrieval evaluation

MEMORY
canonical application memory — already Domain/PostgreSQL
Interaction memory/session continuity
Run/working memory
compaction/checkpoint state
derived/adaptive memory candidates
provider thread/memory/cache
retrieval representations/indexes/embeddings
execution evidence separation

LIFECYCLE
admission / promotion
confirmation/correction
contradiction/supersession
decay/expiry
retirement/redaction/deletion/forgetting
anti-resurrection
provider/cache/index invalidation
```

AI-03B does not authorize persistence simply because these nouns exist.

AI-03C later pressure-tests the whole Context/Retrieval/Memory design and only then produces physical/materialization classification.

Forbidden shortcut:

```text
AI-03B starts
→ therefore create memory table / embeddings / vector index
```

No database evolution, embedding/index activation, vector-store decision or provider/model selection is authorized by AI-03B activation.

## 8. Non-negotiable AI invariants

```text
DANTE != chatbot/model/provider/thread
MODEL != canonical truth
MODEL != authorization engine
MODEL != policy-precedence authority
MODEL != effect success
PostgreSQL = sole canonical persistence/material-history authority
AI inference != confirmed fact
AI confidence != Confirmation
provider state != canonical DANTE state
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SCENARIO STATE != CANONICAL CURRENT STATE
CONTEXT ACCESS != DISCLOSURE PERMISSION
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
DANTE REPRESENTATION != EXTERNAL SYSTEM-OF-RECORD AUTHORITY
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
TELEMETRY/EVAL PIPELINE != PRIVILEGED DATA SINK
SEARCH INDEX != SOURCE OF TRUTH
EMBEDDING != SOURCE / FACT
SUMMARY != SOURCE / FACT
PROVIDER MEMORY != DANTE CANONICAL MEMORY
CONTEXT != RETRIEVAL != MEMORY
SOURCE STANDING != DOMAIN AUTHORITY
CONSUMER CONTEXT != CONTEXT MANIFEST
CONTEXT MANIFEST != BASIS MANIFEST
MODEL-DISCOVERED NEED != SCOPE EXPANSION
WORKCONTRACT PROPAGATION != PARENT-CONTEXT INHERITANCE
```

## 9. Pressure-test acceptance state

```text
AI-02 Round I                         COMPLETE
AI-02 Round II                        COMPLETE
AI-02 Final Kill-Test                 COMPLETE
AI-02 Last Mega Stress-Test           COMPLETE
AI-02 Targeted v0.5 verification      COMPLETE
Additional AI-02 mega-tests           NONE
AI-02.1 closure                       CLOSED / STRUCTURALLY ACCEPTED

AI-03A initial candidate               FAIL / HARDENING REQUIRED
AI-03A hardenings                      9
AI-03A hardened candidate              STRUCTURAL PASS
AI-03A C01..C29                        ACCEPTED
Additional AI-03A mega-tests           NONE unless contradictory downstream evidence
```

AI-02 targeted v0.5 structural checks:

```text
generated-code secret isolation                         PASS
environment crash vs Run durability                     PASS
browser/computer-use effect verification                PASS
superseded publication                                  PASS
Basis coherence                                         PASS
approval rebinding                                      PASS
external-agent side effects                             PASS
resource exhaustion after ambiguous effect              PASS
deterministic fast path bypassing unnecessary isolation PASS
```

AI-03A retests cover North Star capability reach, cross-domain/multi-actor, scenarios, historical/currentness, reference ambiguity, privacy/purpose, provider continuity, child/delegated context, context injection, revocation, anti-resurrection, long context, large histories/documents, context pressure, opaque provider state, multimodal/voice, future provider replacement and deterministic fast paths.

The completed tests produced no evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

The future-extensibility structural criterion also passes: future substantially stronger general-purpose conversational intelligence can be added without transferring canonical memory, Authority, application state, Domain semantics or effect ownership to the provider/model.

## 10. Current bounded deferrals

Still open or trigger-bound:

- exact AI model/provider set and routing policy;
- AI agent/runtime/SDK implementation;
- exact policy-engine technology;
- exact Execution Environment/sandbox technology;
- exact target-resolution implementation;
- exact safe-streaming/publication implementation;
- exact Scenario Workspace physical representation;
- exact ChangeSet physical persistence, if any;
- exact Interaction Session persistence, if any;
- AI-03B retrieval algorithms and memory lifecycle decisions;
- conversation history persistence;
- embeddings/index lifecycle and activation;
- optional local-model choice/activation;
- provider-specific commercial/cost selections;
- cloud compute/IaC and production infrastructure activation.

A deferral does not authorize violating already accepted semantic/runtime/context invariants.

## 11. Architecture reopen discipline

Closed Domain, Logical, Physical, Engineering and Frontend Foundation decisions are not casually reselected.

Implementation evidence first reopens the smallest affected technology/adapter/boundary. A wider architectural reopen requires a demonstrated contradiction that cannot be resolved locally.

Do not reopen architecture because of ORM convenience, table shape preference, provider naming, UI naming, framework fashion, agent-framework conventions, vector-store convenience or one isolated implementation annoyance.

AI-03A is likewise not reopened merely because a retrieval or memory technology prefers a weaker Context contract.

## 12. Current next architecture posture

```text
DATABASE / CP6 + RECOVERY EVOLUTION
CLOSED / INTEGRATED

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE ON feature/access-auth / UNMERGED

AI ARCHITECTURE
ACTIVE ON feature/ai-architecture
DESIGN / REENGINEERING ONLY

AI-02.1
v0.5 CLOSED / STRUCTURALLY ACCEPTED
ALL AI-02 PRESSURE/MEGA TESTS COMPLETE
TARGETED v0.5 VERIFICATION COMPLETE

AI-03A
FULL CONTEXT ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED
9 HARDENINGS / C01..C29

AI-03
CONTEXT / RETRIEVAL / MEMORY
ACTIVE
CURRENT MACRO-PHASE AI-03B RETRIEVAL + MEMORY ARCHITECTURE
```

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.
