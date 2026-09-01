# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-09-01
- **Backend foundation:** CP1–CP6 CLOSED / integrated / directly validated
- **Current PostgreSQL:** 18.6
- **Current Alembic head:** `20260830_09`
- **Current product work:** full Access/Auth vertical active and unmerged on `feature/access-auth`; AI-02.1 v0.5 and AI-03A Full Context Architecture structurally accepted; AI-03B Retrieval + Memory current on `feature/ai-architecture`

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Implementation consumes closed Product/Domain/Logical/Physical models and closed engineering foundations. Framework, model, provider or storage convenience does not redefine accepted semantics.

Core invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI/solver output != accepted canonical effect
client local state != canonical accepted effect
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SCENARIO STATE != CANONICAL CURRENT STATE
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
DANTE canonical representation != external institutional System-of-Record authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
CONTEXT != RETRIEVAL != MEMORY
CONSUMER CONTEXT != CONTEXT MANIFEST
CONTEXT MANIFEST != BASIS MANIFEST
SOURCE STANDING != DOMAIN AUTHORITY
INTERACTION SESSION CONTINUITY != PROVIDER-CONTEXT CONTINUITY
MODEL-DISCOVERED INFORMATION NEED != WORKCONTRACT/POLICY SCOPE EXPANSION
WORKCONTRACT PROPAGATION != PARENT-CONTEXT INHERITANCE
```

Logical hardenings `WL-H01..WL-H12` remain active implementation contracts. AI-03A adds accepted Context hardenings `C01..C29`.

The AI architecture is layered across:

```text
docs/architecture/dante-ai-foundation.md
→ AI-00 inherited/derived semantic baseline

docs/architecture/ai-production-engineering-state-of-the-art-2026.md
→ external production-engineering research / NON-DANTE-DECISION

docs/architecture/dante-ai-02-1-intelligence-reengineering.md
→ AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED

docs/architecture/dante-ai-03a-full-context-architecture.md
→ AI-03A Full Context Architecture CLOSED / STRUCTURALLY ACCEPTED

docs/architecture/dante-ai-03-context-retrieval-memory.md
→ AI-03 ACTIVE / current macro-phase AI-03B Retrieval + Memory Architecture
```

AI-02.1 does not supersede AI-00. It pressure-tested and refined runtime/intelligence responsibilities while preserving the accepted semantic baseline. AI-03A then fixed detailed Context contracts inside that runtime. AI-03B consumes both and owns detailed Retrieval + Memory design.

## 2. Repository / application topology

One product monorepo:

```text
DANTE repository
│
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

Backend accepted internal shape remains capability-first modular monolith:

```text
apps/backend/src/dante
├── bootstrap
├── kernel
├── platform
└── modules/<capability>
    ├── domain
    ├── application
    ├── ports
    └── adapters
        ├── inbound/http
        └── outbound/persistence|integrations
```

FastAPI is an inbound adapter/process host. SQLAlchemy/provider/runtime objects stay outside Domain identity. Capability boundaries are behavior/cohesion based, not one owner/table/route per module.

AI responsibility boxes are not automatic deployable services and do not alter the accepted modular-monolith posture.

## 3. Backend technical foundation

```text
CP1 process/config foundation                   CLOSED / DIRECT QA PASS
CP2 LOCAL PostgreSQL foundation                 CLOSED / DIRECT QA PASS
CP3 persistence/migrations/privileges           CLOSED / DIRECT QA PASS
CP4 CI enforcement                              CLOSED / DIRECT REMOTE QA PASS
CP5 integrated scaffold QA                      CLOSED / DIRECT INTEGRATED QA PASS
Backend scaffold integration PR #24             MERGED
CP6 concrete PostgreSQL database                CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL Recovery evolution                   CLOSED / LOCAL DIRECT QA / INTEGRATED VIA PR #47
```

Current technical baseline:

```text
Python 3.14.x
uv
FastAPI
SQLAlchemy async
psycopg 3
Alembic
PostgreSQL 18.6
schema dante
owner / migrator / runtime role separation
explicit application transaction ownership
real PostgreSQL acceptance testing
```

The earlier CP2/CP3 PostgreSQL 18.4 runs and pre-Recovery `20260826_08` database shape remain exact historical phase-time evidence.

## 4. Canonical persistence authority

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY

current patch
18.6

current Alembic head
20260830_09
```

Current concrete topology:

```text
69 tables
5 ordinary views
15 integrity routines
76 triggers
97 physical indexes
69 foreign keys
123 named CHECK constraints
0 custom enum/domain
0 sequences
0 materialized views
0 RLS policies
```

Accepted relational thesis:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical address/control structures only for genuine heterogeneous addressing
+ separate provider / derived / runtime concerns
```

Rejected globally:

```text
universal Entity / Thing
universal Relationship / generic edge
canonical EAV/property bag
universal event ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
```

Conversation state, embeddings, provider threads, agent/runtime journals, scenario overlays, ChangeSets, BasisManifests, WorkContracts, ContextPlans, ContextFragments, ContextManifests, target-resolution metadata, policy decisions or generated summaries do not become canonical DANTE truth by convenience.

## 5. Reference / material-state architecture

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Current PostgreSQL rules preserve:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ stable PostgreSQL UUID address
→ bounded material-state address/control
→ exact owner + facet
→ owner-specific material-state row
→ explicit current accepted-state binding where required
```

Provider revisions, MVCC tokens, timestamps and ETags do not become MaterialStateRef.

For consequential operations, expected material state remains the semantic concurrency basis. A stale AI/tool/scenario request must conflict/re-read/re-evaluate/reconcile rather than silently overwrite newer accepted state.

AI adds orthogonal checks:

```text
Reference / Target Resolution
→ are we acting on the intended canonical target?

InformationNeed reference-resolution requirement
→ is the target/referent resolved enough for this specific context need?

BasisManifest validity
→ are target state and other dependencies still valid/fresh enough?

Basis coherence
→ can the relevant independently read values legitimately be treated as one combined decision basis?
```

Expected MaterialState cannot compensate for a wrong-but-current target. Fresh individual inputs do not prove that a multi-source basis was ever simultaneously coherent.

## 6. Accepted AI-02.1 structural architecture

AI-02.1 v0.5 is a **structurally accepted responsibility architecture**, not a deployment diagram or implementation PASS.

```text
┌──────────────────────────────────────────────────────────────────┐
│                        INTERACTION EDGE                          │
│ Web · Mobile · Voice · Capture · API · External AI             │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
                       INTERACTION SESSION
                                │
                                ▼
                           WORK INTAKE
                                │
                          WORK CONTRACT
      objective / scope / target bindings / protected constraints
          purpose / consequence / governance / approval terms
                                │
                                ▼
                         EXECUTION KERNEL
                                │
       ┌────────────────────────┼─────────────────────────┐
       │                        │                         │
       ▼                        ▼                         ▼
SEMANTIC QUERY /            CONTEXT                  SCENARIO
PROJECTION GATEWAY          ENGINE                   WORKSPACE
       │                        │                         │
       └────────────────────────┼─────────────────────────┘
                                ▼
                         BASIS MANIFEST
            dependencies / freshness / temporal validity /
             assumptions / coherence / source lineage
                                │
                                ▼
                         REASONING LAYER
           ┌────────────────────┼────────────────────┐
           ▼                    ▼                    ▼
     ModelTarget +         Deterministic           Solver
     HarnessProfile           Compute
           │                    │                    │
           └────────────────────┼────────────────────┘
                                ▼
                        CAPABILITY RUNTIME
                                │
                    ┌───────────┴───────────┐
                    │                       │
             normal trusted path      EXECUTION ENVIRONMENT
                                     when workload/threat model
                                     requires isolation
                    │                       │
                    └───────────┬───────────┘
                                ▼
                            VERIFIER
                                │
                                ▼
                    CHANGESET / EFFECTGRAPH
                                │
                                ▼
                         EFFECT RUNTIME
                                │
                                ▼
                     APPLICATION / DOMAIN
                                │
                                ▼
                           PostgreSQL
                                │
                                ▼
          RESULT / DISCLOSURE / SAFE PUBLICATION
```

Cross-cutting:

```text
Policy mesh / Authority / AuthZ / Consent / Visibility
ConsequenceProfile
Information flow / provider eligibility
Autonomy
Attention + attention budgeting
Causal lineage / oscillation protection
Run durability / Work Supersession
Approval binding / rebinding
Resource governance
Artifact handling
Publication currentness / Result Maturity
Cumulative inference protection
Control Plane
Observability
Audit / execution evidence
Evals
```

## 7. WorkContract and decomposition integrity

`WorkContract` is the authoritative runtime contract carried through decomposition/child Runs.

It preserves materially relevant:

```text
objective
scope
resolved target bindings
protected constraints
purpose
consequence/governance obligations
approval conditions
```

Derived execution may refine this contract but may not silently relax/drop protected requirements.

If the user intentionally changes a material requirement, that arrives through a new/superseding interaction/decision and updates the current work relationship.

```text
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
```

A superseded Run may still finish reconciliation/evidence for already-attempted work. It must not dispatch newly obsolete effects or keep publishing obsolete output as current.

AI-03A adds the decomposition privacy complement:

```text
CHILD WORK CONTRACT
inherits protected obligations

CHILD CONTEXT
is separately minimized to the child's InformationNeeds

WORKCONTRACT PROPAGATION
!= PARENT-CONTEXT INHERITANCE
```

## 8. Semantic Query vs Context vs Scenario

### Semantic Query / Projection Gateway

Application-owned, permission-aware access to structured DANTE meaning such as current commitments, workload, open responsibilities, Goal trajectory, current Program material state or safe availability.

It is not raw model SQL access and not a generic Entity API.

### Context Engine

Builds purpose-bound, consumer-specific context under the accepted AI-03A contracts. It may compose structured projections with documents, notes, external/open-world material, session/working state and other eligible sources without becoming a second canonical store.

Accepted Context contracts are:

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

`ContextFragment` is runtime source-linked representation, not a new Domain Fact/Observation/Evidence/ContentArtifact/Version/MaterialState/Memory root.

`ConsumerContext` is what one consumer actually receives. `ContextManifest` is the exposure receipt. Neither is the canonical world.

### Scenario Workspace

Hypothetical/derived overlays over an explicit basis. It does not duplicate the canonical database and does not become current reality merely because a model/solver produced it.

AI-03A requires explicit Reality Scope:

```text
CANONICAL_CURRENT
MATERIAL_HISTORICAL / AS-OF
SCENARIO <workspace/branch>
OPEN-WORLD ASSERTION
explicit MIXED frame
```

No cross-frame laundering is allowed.

## 9. AI-03A Context assembly contract

The accepted structural path is:

```text
WorkContract
→ ContextPlan
→ InformationNeeds
→ ContextStrategy per need
→ discovery/acquisition PEP
→ source read + source binding
→ ContextFragments
→ Reality Scope / Provenance / Source Standing /
  Integrity / Canonicality / Instruction Provenance /
  Confidentiality / Temporal Validity / Contradiction
→ coverage + coherence
→ ContextReadiness
→ minimisation / transformation
→ resource-aware packing
→ consumer/provider exposure PEP
→ ConsumerContext
→ Harness / consumer invocation
→ ContextManifest exposure receipt
→ bounded iterative/JIT acquisition if legitimate need remains
```

Core distinctions:

```text
CONTEXT != RETRIEVAL != MEMORY
PROVENANCE != SOURCE STANDING != INTEGRITY != CANONICALITY
SOURCE STANDING != DOMAIN AUTHORITY
DATA != INSTRUCTION
USER-ORIGINATED CONTENT != USER INSTRUCTION AUTOMATICALLY
CONSUMER CONTEXT != CONTEXT MANIFEST
CONTEXT MANIFEST != BASIS MANIFEST
EXPOSED != USED != MATERIAL DEPENDENCY
```

InformationNeed carries explicit criticality, coverage/currentness/coherence and reference-resolution requirements. Model-discovered needs may refine but cannot silently widen the WorkContract/policy scope.

ContextPlan also supports explicit exclusions such as forbidden sources, data classes, purposes, provider exposure or derivative use.

ContextReadiness is requirement-based, consumer-/step-specific and non-monotonic.

```text
READY now != READY forever
```

## 10. BasisManifest / freshness / coherence

`BasisManifest` is runtime/evidence metadata, not a new Domain Version/Fact root.

It may retain enough evidence to answer:

```text
what state/source/assumption did this depend on?
what changed?
what is stale?
what must be recomputed?
what remains valid?
```

Relevant fields/concepts may include:

```text
MaterialStateRefs
source identities / versions
observed_at
valid_for / valid_until
revalidate_after
acquisition window
freshness requirement
assumptions / constraints
policy/config versions when consequential
capability/harness versions when needed for evidence
```

For DANTE-native work requiring one coherent view, application/database reads should provide the needed coherence semantics. For independent external sources, DANTE records the actual acquisition limits and revalidates volatile consequential dependencies instead of fabricating atomicity.

```text
ContextManifest
= exposure receipt

BasisManifest
= material dependency/currentness basis
```

They may overlap in source references but are not interchangeable.

## 11. Context continuity, provider state and compaction

Human-visible Interaction Session continuity and reasoning-provider continuity are different.

```text
INTERACTION SESSION CONTINUITY
!= PROVIDER-CONTEXT CONTINUITY
```

Provider thread, prompt cache, provider compaction and prior ConsumerContext may be reused only when compatible with current:

```text
purpose
WorkContract
Principal / Actor / represented party
processing rules
confidentiality compartment
consumer/provider eligibility
recipient-related constraints where materially relevant
```

If not compatible, the same product Interaction Session may continue with a new clean/sanitized ConsumerContext.

Provider-managed opaque state remains explicitly opaque. DANTE records what it knows rather than inventing the provider's internal retained representation.

Compaction is not source or memory authority:

```text
COMPACTION != MEMORY != SOURCE != CANONICAL STATE
```

Lossy compacted representations must preserve a recoverable route to stronger source material where that material legitimately survives. Protected material semantics must not exist only in lossy summary/compaction when they can be rehydrated from stronger sources.

## 12. Policy composition is a mesh, not one model decision

Several enforcement questions exist at different boundaries:

```text
Discovery / Acquisition PEP
→ may this work search for / acquire this source/category for this purpose?

Consumer Context PEP
→ may this exact representation be exposed to this consumer/provider now?

Capability PEP
→ may this capability be discovered/invoked?

Effect PEP
→ may this exact consequential effect execute now?

Publication/Egress PEP
→ may this representation leave to this recipient/provider/surface now?
```

The policy layer may compose Authority, AuthZ, Consent, Visibility, autonomy, hard constraints, safety/institutional rules and purpose/data/provider eligibility.

The model does not improvise precedence.

Potential decision shapes include:

```text
ALLOW
DENY
REQUIRE_CONFIRMATION
REQUIRE_EXTERNAL_APPROVAL
LIMIT_SCOPE
```

`ConsequenceProfile` sets a minimum governance/verification/publication floor without becoming a universal semantic risk score.

## 13. Reference / Target Resolution

Natural-language references may resolve only after authorized semantic query/context is available. Target Resolution is therefore an Execution Kernel responsibility that may consume the Semantic Query / Projection Gateway; it is **not** a magical pre-query oracle.

Consequential targets must become adequately bound to canonical references before execution.

```text
EXACT / UNIQUE_IN_SCOPE
→ may proceed subject to normal governance

AMBIGUOUS
→ clarify / preview / disambiguate

UNRESOLVED
→ no consequential effect
```

AI-03A further makes reference-resolution level an explicit InformationNeed requirement.

```text
AMBIGUITY != MODEL CONFIDENCE
```

Model confidence is not target identity proof.

## 14. Capability execution and isolation

Most requests do **not** require isolation.

Cheap path examples:

```text
semantic query
SQL aggregation
deterministic calculation
normal application/domain capability
```

AI-03A explicitly preserves the fast path: Context machinery is bypassable where deterministic application logic can answer correctly without composed context.

Potential isolation-triggering workloads include:

```text
model-generated code
untrusted executable/archive content
browser/computer use
hostile document processing where execution risk exists
other arbitrary execution workloads
```

`Execution Environment` may constrain as appropriate:

```text
filesystem/artifact mounts
network/egress
credential mediation
CPU
RAM
disk
wall clock
process count
lifecycle/cleanup
execution evidence
```

No specific WASM/container/gVisor/microVM technology is mandated by this architecture.

Generated/untrusted code must not receive raw privileged database/application/provider credentials. Privileged action uses bounded trusted broker/capability calls subject to current identity/delegation/policy/evidence.

```text
Execution Environment != Domain concept
Execution Environment != mandatory microservice
Execution Environment != every request gets a sandbox
```

## 15. ChangeSet / effects / approval

One user decision may require several operations.

`ChangeSet / EffectGraph` coordinates dependencies, protected invariants, atomic groups, external-effect boundaries, previews, partial outcomes, compensation and reconciliation requirements.

It does not replace individual effect governance:

```text
EffectIntent
→ EffectPermit
→ EffectAttempt
→ EffectReceipt
→ Verification / Reconciliation
```

Approval must bind to the materially approved target/proposal/basis/effect semantics. If a material ChangeSet changes after approval, old approval is not automatically reusable.

```text
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
```

Outcome-unknown effects remain real obligations. Optional resource/budget exhaustion may stop additional optional work but must not erase required reconciliation.

## 16. Context, disclosure and publication

```text
Context Projection / ConsumerContext
= what reasoning consumer may receive for purpose P

Disclosure Projection
= what representation recipient R may receive

Safe Publication
= what may cross recipient/surface boundary now
```

AI-03A adds a pre-disclosure distinction:

```text
acquisition eligibility
!= consumer/provider exposure eligibility
!= recipient disclosure
```

Cumulative/cross-query inference protection applies when individually safe answers could compose into a protected fact/relationship.

Safe Publication also checks:

```text
result maturity
current work/supersession state
recipient/surface
policy/current authorization
information-flow lineage
external effect truth
```

A superseded Run may reconcile old work but must not continue streaming obsolete output as the current recommendation.

Result/presentation maturity may include `WORKING`, `PROVISIONAL`, `VERIFIED`, `ACCEPTED_EFFECT` without redefining Domain Confirmation/Actual/Outcome/Reconciliation.

Lock-screen notification, private in-app view, shared UI and voice/realtime are different surfaces and may require different disclosure.

## 17. Source lifecycle and anti-resurrection

Context acquisition must distinguish materially different source states instead of collapsing them all to `None`:

```text
NOT_FOUND
FOUND_CURRENT
FOUND_HISTORICAL
PAYLOAD_RETIRED / REDACTED
CURRENTLY_NOT_PROCESSABLE
CURRENTLY_NOT_VISIBLE
TEMPORARILY_UNAVAILABLE
STALE
CONFLICTED
```

An old ContextManifest may remain a truthful historical receipt that a consumer was exposed to material at time T.

That does not make a now-retired source or derivative eligible for future retrieval.

Future durable derivatives such as embeddings, summaries, indexes, context caches, provider state or compaction checkpoints inherit source lifecycle/anti-resurrection obligations. Restoring old bytes from backup does not by itself restore semantic eligibility.

Exact physical invalidation mechanics remain AI-03C work if/when such durable derivatives exist.

## 18. Attention / proactivity

Trigger is not Attention.

```text
Signal
→ relevance
→ materiality
→ urgency
→ causal-loop check
→ attention policy + aggregate attention budget
→ silent / review / notify / start work / escalate
```

Attention considers aggregate interruption load and batchability, not only whether each signal is individually relevant.

The oscillation guard uses causal lineage/hysteresis/cooldown/material change so DANTE does not recursively react to its own adaptations without new reality.

## 19. External AI / external-agent effects

DANTE may use models/agents internally and may expose bounded capabilities to external AI clients.

External protocol adapters remain edge adapters, not Domain contracts.

An external intelligent worker that performs a consequential side effect must either:

```text
route the side effect through governed DANTE capabilities
```

or be represented honestly as:

```text
an external autonomous system performed an external effect
→ DANTE observes/verifies/reconciles the outcome
```

DANTE must not claim its effect governance covered a side effect that happened outside it.

For delegated reasoning, AI-03A additionally requires minimum-necessary child/delegated ConsumerContext. Parent context is not copied wholesale.

## 20. Observability / audit / evaluation privacy

```text
TELEMETRY != AUDIT
```

Observability and evaluation pipelines are not privileged data sinks.

Sensitive prompts, ContextFragments, ContextManifests, tool results, traces or production examples remain subject to purpose, retention, redaction and provider/data-policy constraints.

Production trace reuse in an evaluation corpus requires legitimate purpose/handling rather than being automatic.

## 21. Future rich intelligence

DANTE supports one semantic/application core with multiple interaction/intelligence surfaces.

A future rich surface may include:

```text
text
voice
image/camera
documents
web research
general Q&A
creative work
code
artifacts
long-running work
computer use
DANTE-aware planning and effects
```

Even a much more capable future model with huge context or persistent provider memory remains replaceable cognition.

It does not inherit ownership of:

```text
canonical memory
canonical application state
Domain semantics
Authority
Visibility
accepted-effect rules
material history
```

A much larger context window changes `ContextStrategy`/packing economics; it does not remove privacy, source lifecycle, contradiction, Reality Scope or purpose requirements.

Provider thread/memory is an optimization/integration detail, not DANTE truth.

## 22. AI phase state

Completed AI-02 evidence:

```text
Round I                         COMPLETE
Round II                        COMPLETE
Final Kill-Test                 COMPLETE
Last Mega Stress-Test           COMPLETE
Targeted v0.5 verification      COMPLETE
More AI-02 mega-test cycles     NONE
```

AI-03A evidence:

```text
Initial candidate               FAIL / HARDENING REQUIRED
Dedicated AI-03A mega-test      COMPLETE
Hardenings                      9
Hardened candidate              STRUCTURAL PASS
C01..C29                        ACCEPTED
More AI-03A mega-test cycles    NONE unless contradictory downstream evidence
```

No evidence was found to reopen Domain, Logical, Physical or PostgreSQL.

Future-extensibility structural criterion: **PASS**.

Current phase state:

```text
AI-02.1
v0.5 CLOSED / STRUCTURALLY ACCEPTED
NO RUNTIME/BACKEND/PROVIDER IMPLEMENTATION CLAIM

AI-03A
FULL CONTEXT ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED

AI-03
ACTIVE — CONTEXT / RETRIEVAL / MEMORY
CURRENT MACRO-PHASE AI-03B RETRIEVAL + MEMORY ARCHITECTURE
```

Current AI-03 authority:

- `docs/architecture/dante-ai-03-context-retrieval-memory.md`;
- `docs/architecture/dante-ai-03a-full-context-architecture.md`.

## 23. Frontend / client data authority

Frontend Data Authority Matrix remains:

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite noncanonical
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API
online governed command           FastAPI/backend
form draft                        TanStack Form
component transient               React
cross-tree transient              Zustand only when justified
```

The future AI interaction surface preserves the same authority boundary: chat/UI state may express draft, candidate, hypothetical, superseded, provisional or pending state without pretending it is accepted canonical effect.

## 24. Offline / specialist capabilities

Selected Physical targets remain activation-triggered:

```text
PowerSync + encrypted SQLite      real offline/sync consumer required
PgBouncer                         real connection-pressure value
PostgreSQL outbox                 real Class-A async requirement
Restate                           real Class-B durable workflow
Cloudflare R2                     real ContentArtifact byte flow
pgBackRest                        current LOCAL recovery implementation
remote recovery provider         TBD / not activated
OR-Tools                          solver-backed capability
AI Execution Environment          workload/threat-model trigger
```

Specialist/institutional systems keep their own authority boundary. DANTE may coordinate or mirror relevant personal facts without pretending to replace healthcare, school, judicial, financial, governmental or other specialist Systems of Record.

## 25. Transactions / migrations / privileges

Current durable posture:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per app operation
autobegin=False
autoflush=True
expire_on_commit=False
outer application operation owns transaction
adapter may flush / never implicit commit
READ COMMITTED default
one Alembic DAG / one canonical head
metadata.create_all() not deployment authority

dante_owner      NOLOGIN
dante_migrator   LOGIN NOINHERIT + bounded SET ROLE
dante_runtime    LOGIN NOINHERIT / runtime DML posture
```

Future AI execution passes through application/domain mutation contracts rather than receiving direct unrestricted database mutation authority.

Any future AI-03C structural DB recommendation must enter normal forward Alembic + SQLAlchemy + Dictionary + human reference + direct-test + recovery-impact governance; AI architecture documentation cannot bypass that same-change rule.

## 26. Current non-claims

```text
FULL ACCESS/AUTH PRODUCT VERTICAL       NOT CLAIMED CLOSED
DANTE AI-02.1                           CLOSED STRUCTURALLY / NOT IMPLEMENTATION PASS
DANTE AI-03A                            CLOSED STRUCTURALLY / NOT IMPLEMENTATION PASS
AI-03 RETRIEVAL/MEMORY                  ACTIVE DESIGN / NOT MATERIALIZED
AI RUNTIME                              NOT IMPLEMENTED BY THIS DOCUMENT
AI PROVIDER/MODEL                       NOT SELECTED
AI EXECUTION ENVIRONMENT TECHNOLOGY     NOT SELECTED / NOT IMPLEMENTED
AI MEMORY/EMBEDDING/INDEX PERSISTENCE   NOT SELECTED / NOT IMPLEMENTED
REMOTE/CLOUD RECOVERY                   NOT CLAIMED
```

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.
