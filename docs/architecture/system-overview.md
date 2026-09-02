# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-09-02
- **Backend foundation:** CP1–CP6 CLOSED / integrated / directly validated
- **Current PostgreSQL:** 18.6
- **Current Alembic head:** `20260830_09`
- **Current product work:** full Access/Auth vertical active and unmerged on `feature/access-auth`; AI-02.1, AI-03, AI-04 and PRE-AI05 structurally accepted; AI-05 Whole-System Acceptance + Implementation Blueprint current on `feature/ai-architecture`

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
RUN-START AUTONOMY != PERPETUAL AUTONOMY
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
PROCESSING / RETRIEVAL ELIGIBILITY != RETENTION / FUTURE-REUSE ELIGIBILITY
APPROXIMATE != COMPLETE
SEMANTIC AUTHORITY != FUNCTIONAL ROLE != SURVIVAL DISPOSITION != PHYSICAL OWNER
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
ATTENTION DECISION != PROACTIVE WORK ADMISSION != EFFECT AUTHORIZATION
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
RECIPIENT != SURFACE != CHANNEL
SOURCE FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
```

Logical hardenings `WL-H01..WL-H12` remain active implementation contracts. AI-03 adds accepted Context `C01..C33`, Retrieval/Memory `B01..B35` and Materialization `MAT-01..MAT-15`; AI-04 adds `A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22`; PRE-AI05 adds `PRE05-H01..H19` and current eval coverage `DANTE-E01..DANTE-E14`.

The AI architecture is layered across:

```text
docs/architecture/dante-ai-foundation.md
→ AI-00 inherited/derived semantic baseline

docs/architecture/ai-production-engineering-state-of-the-art-2026.md
→ external production-engineering research / NON-DANTE-DECISION

docs/architecture/dante-ai-02-1-intelligence-reengineering.md
→ AI-02.1 v0.5 CLOSED / STRUCTURALLY ACCEPTED

docs/architecture/dante-ai-03-context-retrieval-memory.md
→ AI-03 CLOSED / STRUCTURALLY ACCEPTED

docs/architecture/dante-ai-03a-full-context-architecture.md
→ AI-03A CLOSED / C01..C33

docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
→ AI-03B CLOSED / B01..B35

docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
→ AI-03C CLOSED / MAT-01..MAT-15

docs/architecture/dante-ai-04-productionization-architecture.md
→ AI-04 CLOSED / STRUCTURALLY ACCEPTED

docs/architecture/dante-ai-04a-direct-eval-specification.md
→ AI-04A CLOSED / A01..A30 / EV01..EV20 / E01..E14 current

docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
→ AI-04B CLOSED / RT-01..RT-31

docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
→ AI-04C CLOSED / PA-01..PA-61

docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md
→ AI-04 WHOLE-PHASE CLOSED / WP-01..WP-22

docs/architecture/dante-ai-pre05-cross-phase-hardening.md
→ PRE-AI05 CLOSED / PRE05-H01..H19

docs/workstreams/ai-architecture.md
→ current branch-local routing: AI-05
```

`docs/architecture/ai-context-runtime-boundaries.md` remains historical pre-Physical evidence and is not current runtime authority.

AI-02.1 does not supersede AI-00. It pressure-tested and refined runtime/intelligence responsibilities while preserving the accepted semantic baseline. AI-03 then closed detailed Context, Retrieval, Memory and materialization boundaries. AI-04 closed productionization responsibilities. PRE-AI05 hardened the cross-phase joins. AI-05 now turns the accepted architecture into a buildable blueprint without weakening it.

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

Conversation state, embeddings, provider threads, agent/runtime journals, scenario overlays, ChangeSets, BasisManifests, WorkContracts, ContextPlans, ContextFragments, ContextManifests, target-resolution metadata, policy decisions, Attention accounting or generated summaries do not become canonical DANTE truth by convenience.

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
     RESULT / DISCLOSURE / SAFE PUBLICATION / ATTENTION
```

This retained AI-02 diagram is a responsibility skeleton. AI-04/PRE-AI05 subsequently refine the model route into qualified HarnessProfile + ProviderBinding compositions and separate Attention decision from proactive work admission.

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

## 9. AI-03 Context / Retrieval / Memory contracts

The accepted Context structural path is:

```text
WorkContract
→ ContextPlan
→ InformationNeeds
→ Reality Scope / Runtime Interpretation Frame where material
→ ContextStrategy per need
→ discovery/acquisition PEP
→ source read + source binding
→ ContextFragments
→ source standing / provenance / integrity / canonicality /
  instruction provenance / confidentiality /
  temporal validity / contradiction
→ coverage + coherence
→ ContextReadiness
→ minimisation / transformation
→ resource-aware packing
→ consumer/provider exposure PEP
→ ConsumerContext
→ Harness / consumer invocation
→ established exposure / ContextManifest
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

AI-03B adds retrieval and memory boundaries:

```text
RetrievalCandidate != ContextFragment
APPROXIMATE != COMPLETE
candidate count != coverage proof
rank/similarity/rerank != Source Standing
index/cache/embedding != source
Memory survival defaults to NO
MEMORY EXISTS != MEMORY MAY BE RECALLED
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
canonical application memory belongs to Domain/PostgreSQL
correction != forgetting != source/use/inference suppression
provider memory is replaceable optimization
successful canonical promotion must not leave duplicate noncanonical authority
```

AI-03C adds physical survival/materialization boundaries:

```text
ARCHITECTURE CONTRACT != PERSISTENCE OWNER
DEFAULT NONCANONICAL PERSISTENCE = NO
semantic authority != functional role != survival != physical owner
Class-A durable coordination != Class-B durable execution
DURABLE JOURNAL != PRIVACY-FREE RUNTIME
persistent derivative requires truthful/scalable source basis
ASYNC INVALIDATION != CURRENT ELIGIBILITY
recomputable derived state is sacrificial in recovery
ANN is optimization, not prerequisite
representation generations do not mix silently
serving generation requires build/catch-up/readiness/cutover discipline
semantic obligation != execution/audit evidence
```

AI-03 is structurally closed at `C01..C33 / B01..B35 / MAT-01..MAT-15`. No new generic AI memory/conversation/Run/search table, database migration, vector/FTS activation, Restate/R2 activation or provider/model selection was justified by closure.

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

AI-03C additionally permits scalable typed basis envelopes where a derivative depends on a very large source set; this does not turn MVCC/LSN/hash/digest into `MaterialStateRef` or semantic truth.

## 11. Context continuity, provider state and compaction

Human-visible Interaction Session continuity and reasoning-provider continuity are different.

```text
INTERACTION SESSION CONTINUITY
!= PROVIDER-CONTEXT CONTINUITY
```

Provider thread, prompt cache, provider compaction and prior ConsumerContext may be reused only when compatible with current purpose, WorkContract, Principal/Actor/represented party, processing rules, confidentiality compartment and consumer/provider eligibility.

If not compatible, the same product Interaction Session may continue with a new clean/sanitized ConsumerContext.

Provider-managed opaque state remains explicitly opaque. DANTE records what it knows rather than inventing the provider's internal retained representation.

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

AI-03 explicitly preserves the fast path: Context/retrieval machinery is bypassable where deterministic application logic can answer correctly without composed model context.

Potential isolation-triggering workloads include:

```text
model-generated code
untrusted executable/archive content
browser/computer use
hostile document processing where execution risk exists
other arbitrary execution workloads
```

`Execution Environment` may constrain filesystem/artifact mounts, network/egress, credential mediation, CPU/RAM/disk, wall clock, process count, lifecycle/cleanup and execution evidence.

No specific WASM/container/gVisor/microVM technology is mandated by the accepted structural architecture. Concrete technology remains evidence-gated in AI-05/later implementation.

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

Current autonomy is also re-evaluated where an autonomous consequential dispatch depends on it:

```text
RUN-START AUTONOMY != PERPETUAL AUTONOMY
```

```text
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
```

Outcome-unknown effects remain real obligations. Optional resource/budget exhaustion may stop additional optional work but must not erase required reconciliation.

AI-03C further separates the semantic pending/staged/reconciliation obligation from technical provider receipt/trace evidence; technical evidence does not become a new Domain reconciliation root.

## 16. Context, disclosure and publication

```text
Context Projection / ConsumerContext
= what reasoning consumer may receive for purpose P

Disclosure Projection
= what representation recipient R may receive

Safe Publication
= what may cross recipient/surface boundary now
```

AI-03 adds a pre-disclosure distinction:

```text
acquisition eligibility
!= consumer/provider exposure eligibility
!= retention/future-reuse eligibility
!= recipient disclosure
```

Cumulative/cross-query inference protection applies when individually safe answers could compose into a protected fact/relationship. PRE-AI05 makes this explicit across related Runs/Interactions/surfaces and known related sinks when the threat model requires.

Safe Publication also checks result maturity, current work/supersession state, recipient/surface/channel policy/current authorization, information-flow lineage and external effect truth.

A superseded Run may reconcile old work but must not continue streaming obsolete output as the current recommendation.

Result/presentation maturity may include `WORKING`, `PROVISIONAL`, `VERIFIED`, `ACCEPTED_EFFECT` without redefining Domain Confirmation/Actual/Outcome/Reconciliation.

Lock-screen notification, private in-app view, shared UI and voice/realtime are different surfaces and may require different disclosure.

## 17. Source lifecycle and anti-resurrection

Context/retrieval must distinguish materially different source states instead of collapsing them all to `None`:

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

An old ContextManifest may remain a truthful historical receipt that a consumer was exposed to material at time T. That does not make a now-retired source or derivative eligible for future retrieval.

Durable derivatives such as embeddings, summaries, indexes, context caches, provider state or compaction checkpoints inherit source lifecycle/anti-resurrection obligations. Restoring old bytes from backup does not by itself restore semantic eligibility.

AI-03C closes the architecture rule: restored derived bytes are non-serving until rebuilt or explicitly reconciled against current authoritative lifecycle/suppression/basis state.

PRE-AI05 adds another orthogonal distinction:

```text
SOURCE CONTENT / FUTURE SOURCE ELIGIBILITY
!= PRIOR DISCLOSURE OCCURRENCE
```

Deleting or retiring a source does not make a disclosure that already occurred retroactively nonexistent. Where cumulative-disclosure safety still requires it, only minimum non-content technical exposure accounting may survive under its own purpose/access/retention/deletion lifecycle; it is not Context/Memory/source evidence and cannot reconstruct deleted content.

## 18. Attention / proactivity

Trigger is not Attention, and Attention is not Work Admission.

Correct composition:

```text
Trigger / Signal
→ authenticity / currentness / materiality
→ Work Intake / WorkContract when new work may be justified
→ current autonomy + policy + provider/data + resource admission
→ optional bounded work

Result / Signal that may require user attention
→ relevance / materiality / urgency / causal-loop check
→ AttentionPolicy + AttentionBudget
→ SILENT / DEFER-BATCH / REVIEW / NOTIFY / ESCALATE
→ recipient/surface/channel disclosure checks
→ governed transport
→ truthful communication state from evidence
```

```text
ATTENTION DECISION != PROACTIVE WORK ADMISSION != EFFECT AUTHORIZATION
ATTENTION BUDGET != RESOURCE BUDGET != COMMERCIAL QUOTA
NOTIFY != SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
```

The oscillation guard uses causal lineage/hysteresis/cooldown/material change so DANTE does not recursively react to its own adaptations without new reality.

This behavior is now explicitly covered by core eval family `DANTE-E14`.

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

For delegated reasoning, AI-03A requires minimum-necessary child/delegated ConsumerContext. Parent context is not copied wholesale.

## 20. Observability / audit / evaluation privacy

```text
TELEMETRY != AUDIT
```

Observability and evaluation pipelines are not privileged data sinks.

Sensitive prompts, ContextFragments, ContextManifests, tool results, traces or production examples remain subject to purpose, retention, redaction and provider/data-policy constraints.

Production trace reuse in an evaluation corpus requires legitimate purpose/handling rather than being automatic.

AI-04C closes the corresponding production-assurance responsibility. AI-05 must translate it into implementation boundaries without exporting sensitive runtime state merely because a telemetry/eval vendor supports it.

## 21. Future rich intelligence and provider replaceability

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

Even a much more capable future model with huge context or persistent provider memory remains replaceable cognition. It does not inherit ownership of canonical memory, canonical application state, Domain semantics, Authority, Visibility, accepted-effect rules or material history.

A much larger context window changes `ContextStrategy`/packing economics; it does not remove privacy, source lifecycle, contradiction, Reality Scope or purpose requirements.

Provider thread/memory is an optimization/integration detail, not DANTE truth.

Current provider-replaceability seam:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Production route composition:

```text
DANTE work / capability need
→ ModelTarget / deterministic need
→ eligible qualified route compositions
→ Routing Policy
→ compatible qualified:
   HarnessProfile
   + ProviderBinding
   + feature mode
   + capability projection
   + security/control profile
→ route-specific resource admission
→ current egress authorization
→ Provider Adapter when model route selected
→ concrete provider / model / deployment
```

This boundary permits a V1 with one primary provider while keeping later rebinding/provider addition bounded. Auxiliary/sub-model calls are first-class governed data recipients; route selection/context assembly is not egress authorization; fallback does not inherit primary qualification; direct eval does not imply production-capacity qualification.

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

AI-03 evidence:

```text
AI-03A final closure             CLOSED / C01..C33
AI-03B final closure             CLOSED / B01..B35
AI-03C final closure             CLOSED / MAT-01..MAT-15
AI-03 overall                    CLOSED / STRUCTURALLY ACCEPTED
```

AI-04 / PRE-AI05 evidence:

```text
AI-04A                          CLOSED / A01..A30 / EV01..EV20
AI-04B                          CLOSED / RT-01..RT-31
AI-04C                          CLOSED / PA-01..PA-61
AI-04 whole                     CLOSED / WP-01..WP-22
AI-04 overall                   CLOSED / STRUCTURALLY ACCEPTED
PRE-AI05                        CLOSED / PRE05-H01..H19
current core eval               DANTE-E01..DANTE-E14
fresh post-H19 hostile retest   PASS / 26 OF 26
compound retest                 PASS
reverse-order retest            PASS
2026 state-of-art regression    PASS
Domain/Logical/Physical reopen  NO
PostgreSQL/Alembic change       NO
provider/model selection        NO
implementation PASS             NOT CLAIMED
```

No evidence was found to reopen Domain, Logical, Physical or PostgreSQL. Future-extensibility structural criterion: **PASS**.

Current phase state:

```text
AI-05
WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
ACTIVE / CURRENT
FINAL ARCHITECTURE-TO-BUILD BOUNDARY
```

Current routing authority:

- `docs/workstreams/ai-architecture.md`.

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

Any later structural DB recommendation arising during AI-05 or implementation must enter normal forward Alembic + SQLAlchemy + Dictionary + human reference + direct-test + recovery-impact governance. AI architecture documentation cannot bypass that same-change rule.

## 26. Current non-claims

```text
FULL ACCESS/AUTH PRODUCT VERTICAL       NOT CLAIMED CLOSED
DANTE AI-02.1                           CLOSED STRUCTURALLY / NOT IMPLEMENTATION PASS
DANTE AI-03                             CLOSED STRUCTURALLY / NOT IMPLEMENTATION PASS
DANTE AI-04                             CLOSED STRUCTURALLY / NOT IMPLEMENTATION PASS
PRE-AI05 H01..H19                       CLOSED STRUCTURALLY / NOT IMPLEMENTATION PASS
AI-05                                   ACTIVE DESIGN / BLUEPRINT / NOT IMPLEMENTATION PASS
AI RUNTIME                              NOT IMPLEMENTED BY THIS DOCUMENT
AI PROVIDER/MODEL                       NOT SELECTED
DIRECT PROVIDER EVAL                    NOT EXECUTED
PRODUCTION CAPACITY                     NOT PROVEN
AI EXECUTION ENVIRONMENT TECHNOLOGY     NOT SELECTED / NOT IMPLEMENTED
AI MEMORY/EMBEDDING/INDEX PERSISTENCE   NOT ACTIVATED / NOT IMPLEMENTED
ATTENTION ENGINE                        NOT IMPLEMENTED
CUMULATIVE-DISCLOSURE MECHANISM         NOT SELECTED / NOT IMPLEMENTED
FORMAL IFC / LEAKAGE-BUDGET / ACS       NOT SELECTED
RESTATE/R2 AI ACTIVATION                NOT CLAIMED
SC/PSV DIRECT AI PROOFS                 NOT CLAIMED
REMOTE/CLOUD RECOVERY                   NOT CLAIMED
```

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.