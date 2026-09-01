# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-03 — Context / Retrieval / Memory
- **AI-03A:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE / 13 HARDENINGS
- **AI-03B:** CANDIDATE / STRUCTURAL PASS PENDING FINAL INDEPENDENT VALIDATION
- **Current macro-phase:** AI-03B — Final Independent Retrieval + Memory Validation
- **Created:** 2026-09-01
- **Refreshed after AI-03B candidate materialization:** 2026-09-01
- **PRE-SCOPE for AI-03B candidate materialization:** `cd98a1e76864aa91f098e7391c91cce48cefa20a`
- **AI-03B candidate commit:** `2a120d6a5467a78edd64dd6e74c03fcadfe4eb94`
- **AI-03 charter alignment checkpoint:** `3ddb2e8e9ff9133d20e73425b8716b3b62156dd7`
- **Current branch HEAD:** fetch live before every write; this handoff refresh itself advances HEAD beyond the checkpoint above

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architectural truth lives in the architecture/workstream/current-status sources named below.

Repository truth outranks this handoff if any disagreement appears.

---

# 1. Resume rule

A new chat/session does **not** start a new project, repository, branch or AI workstream.

Resume exactly:

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
phase       AI-03 Context / Retrieval / Memory
current     AI-03B Final Independent Retrieval + Memory Validation
```

Do not recreate AI-00, AI-01, AI-02 or AI-03A from scratch.

Do not rebuild the AI-03B candidate from scratch unless final validation finds a concrete contradiction. The current candidate is durable branch authority but is **not yet CLOSED**.

Do not treat the old exploratory AI-00..AI-12 planning sequence as current routing.

Before any remote write:

1. fetch live `feature/ai-architecture` HEAD;
2. inspect relation to protected `main` where relevant;
3. read current authority in the order below;
4. issue the exact repository write gate;
5. require exact PRE-SCOPE match immediately before the first branch-changing write;
6. if HEAD moved, stop and re-gate;
7. after writes run exact-path compare/readback QA.

---

# 2. Mandatory reading order for a fresh chat

Read current truth in this order:

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/development/documentation-lifecycle-policy.md
docs/development/branching-and-environments.md
docs/development/repository-engineering-safety.md

docs/workstreams/ai-architecture.md
this live handoff

docs/architecture/dante-ai-foundation.md
docs/architecture/ai-production-engineering-state-of-the-art-2026.md
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
```

For any AI-03B conclusion that touches semantic/persistence boundaries, inspect the relevant accepted source directly rather than relying only on summaries:

```text
North Star / Product
Domain concepts
Whole Logical / WL-H01..WL-H12
Physical Model
PostgreSQL Persistence Constitution / ADR-010
Database System of Record / Dictionary
current Alembic / SQLAlchemy / PostgreSQL truth
Recovery / retirement / anti-resurrection contracts
```

Repository truth beats conversation memory.

---

# 3. Closed/accepted project state that must not be casually reopened

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN
CLOSED

LOGICAL
CLOSED / 57 OF 57 / WL-H01..WL-H12

PHYSICAL
CLOSED / PostgreSQL 18 major family accepted
PostgreSQL = sole canonical persistence/material-history authority

BACKEND CP1–CP5
CLOSED / integrated

CP6 DATABASE
CLOSED / integrated

CURRENT PostgreSQL
18.6
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs
0 custom enum/domain / 0 sequences / 0 materialized views / 0 RLS

LOCAL RECOVERY
CP01–CP07 PASS / CLOSED / integrated
material_state_retirement materialized
suppression / anti-resurrection semantics active
remote provider TBD / not activated
production/cloud recovery not claimed
```

AI work consumes these contracts.

Do **not** reopen them because:

```text
a vector DB prefers a different model
a memory framework assumes generic Fact/Memory rows
an agent framework wants one state graph
a provider thread API looks convenient
an ORM schema would be easier another way
an embedding/index technology wants different identity semantics
```

Reopen only the smallest affected boundary if real contradictory evidence appears.

---

# 4. Repository engineering / quality standard

The project standard remains deliberately high:

```text
repository-first truth
semantic correctness before framework convenience
maximum quality != maximum abstraction
bounded contracts over universal meta-models
no ceremonial services/tables/modules
simple deterministic path stays simple
provider/model/runtime remain replaceable
privacy/security are design inputs, not late polish
historical truth is preserved
unknown/absence/ambiguity remain explicit
architecture acceptance != implementation PASS
```

Rejected recurring shortcuts include:

```text
universal Entity / Thing
universal Relationship edge
canonical EAV/property bag
generic Fact/Memory ontology
generic Repository[T]
BaseService / service locator
raw ORM/SQL authority exposed to model
one microservice for each architecture box
one table for every architecture noun
vector/search/provider state as canonical truth
```

If a later structural DB change is genuinely justified, same-change discipline applies:

```text
Alembic forward migration
+ SQLAlchemy mapping/metadata
+ Database Dictionary
+ human DB reference
+ governed generated artifacts if applicable
+ direct tests
+ affected recovery/operational assertions
+ current documentation
```

Applied migrations are immutable.

---

# 5. Current compact AI roadmap

```text
AI-00 — SEMANTIC & PRODUCT FOUNDATION
COMPLETE

AI-01 — PRODUCT FORM + PRODUCTION ENGINEERING RESEARCH
COMPLETE

AI-02 — INTELLIGENCE RUNTIME ARCHITECTURE
COMPLETE / STRUCTURALLY ACCEPTED
AI-02.1 v0.5

AI-03 — CONTEXT / RETRIEVAL / MEMORY
ACTIVE

  AI-03A — FULL CONTEXT ARCHITECTURE
  CLOSED / STRUCTURALLY ACCEPTED
  FINAL REVALIDATION COMPLETE / 13 HARDENINGS / C01..C33

  AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
  CANDIDATE / STRUCTURAL PASS
  FINAL INDEPENDENT VALIDATION NEXT

  AI-03C — DESTRUCTIVE VALIDATION + MATERIALIZATION BLUEPRINT
  FUTURE

AI-04 — PRODUCTIONIZATION ARCHITECTURE
FUTURE

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE
```

Security, privacy, simulations and evals are cross-cutting disciplines throughout the design. Dedicated later passes validate the concrete design; they do not introduce those concerns for the first time.

---

# 6. AI-00 accepted baseline

Durable authority:

```text
docs/architecture/dante-ai-foundation.md
```

Key inherited constraints:

```text
DANTE != model/provider/chat transcript
PostgreSQL canonical authority
model/provider state != canonical state
AI inference != confirmed fact
AI confidence != Confirmation
Authority != AuthZ
Visibility != Authority
Consent != Authority
processing != disclosure != mutation authority
unknown/unresolved are legitimate
no universal AI fact/action/memory tables
retention/redaction/anti-resurrection apply to derivatives
multi-actor cannot collapse to generic user_id
```

AI-00's old sequencing toward AI-01 is historical chronology only.

---

# 7. AI-01 completed research/product-form evidence

The product/research work established:

```text
ONE DANTE / MANY SURFACES / ONE SEMANTIC REALITY
Ask / Work / Watch / Resolve
DANTE Presence / Workspace product form
API-first frontier intelligence posture
provider-independent semantic contracts
provider-native optimization permitted behind adapters/HarnessProfile
context as runtime resource
deterministic compute first-class
capability registry/discovery/runtime separation
verification separate from model self-report
explicit effect semantics
security/information flow outside model
sandbox/isolation only under real workload/threat model
no automatic microservice zoo
```

The production engineering thesis remains:

```text
RESEARCH / TECHNOLOGY LANDSCAPE / NON-DANTE-DECISION
```

Technology appearing in research is not selected DANTE technology.

---

# 8. AI-02.1 — accepted runtime architecture

Durable authority:

```text
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
```

AI-02.1 v0.5 is:

```text
CLOSED / STRUCTURALLY ACCEPTED
```

after:

```text
Round I
Round II
Final Kill-Test
Last Mega Stress-Test
Targeted v0.5 structural verification
```

Do not run more AI-02 mega-test cycles unless later evidence reveals a real contradiction.

Accepted responsibilities include:

```text
Interaction Edge
Interaction Session
Work Intake
WorkContract
Work Supersession
Reference / Target Resolution
ConsequenceProfile
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
ModelTarget / HarnessProfile
Deterministic Compute
Solver
Capability Runtime
Execution Environment
Verifier
Policy mesh
ChangeSet / EffectGraph
Effect Runtime
Application / Domain boundary
Result Maturity
Disclosure
Safe Result Publication
Attention
```

Important AI-02 invariants:

```text
Interaction Session != Run != Worker
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF INDIVIDUAL EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION
DANTE representation != external System-of-Record authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
```

AI-02 closure is architecture acceptance only, not backend/runtime/provider implementation PASS.

---

# 9. AI-03A — CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE

Durable authority:

```text
docs/architecture/dante-ai-03a-full-context-architecture.md
```

This file is now the authoritative detailed Context contract.

## 9.1 Result chronology

AI-03A did **not** pass on the first architecture candidate.

```text
INITIAL CANDIDATE
FAIL / HARDENING REQUIRED

        ↓
DEDICATED CONTEXT MEGA-TEST

        ↓
9 INITIAL MATERIAL HARDENINGS

        ↓
HARDENED CANDIDATE
STRUCTURAL PASS

        ↓
INDEPENDENT REVERSE-ENGINEERING / SECOND KILL-TEST

        ↓
4 ADDITIONAL BOUNDARY HARDENINGS

        ↓
FINAL HARDENED CONTRACT
13 TOTAL HARDENINGS
C01..C33
STRUCTURAL PASS
```

The second revalidation did not treat the earlier PASS as evidence. It reconstructed real Context obligations from North Star/Product, Domain, Logical, PostgreSQL/Recovery, AI-02 and the simulation corpus, then attacked the seven-contract architecture independently.

Final closure:

```text
AI-03A FULL CONTEXT ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED
FINAL REVALIDATION COMPLETE

new top-level Context contract  NO
Domain reopen                   NO
Logical reopen                  NO
Physical reopen                 NO
PostgreSQL change               NO
Alembic change                  NO
implementation PASS             NO
```

## 9.2 Accepted Context definition

> DANTE Context is a purpose-bound, consumer-specific and currently eligible runtime projection of source-linked information and execution configuration assembled to satisfy explicit InformationNeeds for a bounded piece of work. Context is not canonical reality, persistent memory, a chat transcript, a retrieval index or a copy of everything DANTE knows.

Context quality is based on:

```text
required-information coverage
correct source binding
currentness
Reality Scope / coherence
preserved material contradiction
correct information-flow eligibility
minimum unnecessary exposure
```

not raw token volume.

## 9.3 Accepted AI-03A contracts

Seven runtime contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
```

plus inherited:

```text
BasisManifest
```

These are not automatic services or tables.

## 9.4 Accepted pipeline

```text
BOUNDED WORK CONTRACT
  ↓
CONTEXT PLAN
  ├ contract/policy needs
  ├ user/request needs
  └ dynamic/discovered needs
  ↓
INFORMATION NEEDS
  ↓
REALITY SCOPE / RUNTIME INTERPRETATION FRAME where material
  ↓
CONTEXT STRATEGY per need
  ↓
DISCOVERY / ACQUISITION PEP
  ↓
GOVERNED ACQUISITION
including provider-native/JIT/tool acquisition
  ↓
SOURCE READ / SOURCE BINDING
  ↓
CONTEXT FRAGMENTS
  ↓
Reality Scope / Provenance / Source Standing /
Integrity / Canonicality / Instruction Provenance /
Confidentiality / Derived Sensitivity /
Temporal Validity / Contradiction
  ↓
COVERAGE + COHERENCE
  ↓
CONTEXT READINESS
  ↓
MINIMISE / TRANSFORM
  ↓
RESOURCE PACKING
  ↓
CONSUMER EXPOSURE PEP
  ↓
CONSUMER CONTEXT
  ↓
HARNESS / ADAPTER
  ↓
ACTUAL CONSUMER CALL
  ↓
ESTABLISH WHAT EFFECTIVE EXPOSURE CAN ACTUALLY BE PROVED
  ↓
CONTEXT MANIFEST
  exposure receipt
  ↓
bounded iterative/JIT acquisition when legitimate need remains
  ↓
reasoning
  ↓
BASIS MANIFEST
  material dependency/currentness evidence
```

A WorkContract may be bounded but partially unresolved when context is needed for interpretation/reference resolution.

```text
UNRESOLVED != UNBOUNDED
```

## 9.5 The thirteen hardenings that close AI-03A

### GAP-01 — Reality Scope / Scenario binding — P0

Problem: Scenario A/B/current/historical material could otherwise be mixed into an impossible world.

Accepted:

```text
CANONICAL_CURRENT
MATERIAL_HISTORICAL / AS-OF
SCENARIO <workspace/branch>
OPEN-WORLD ASSERTION
explicit MIXED frame

SCENARIO A != SCENARIO B != CANONICAL CURRENT
```

No cross-frame laundering.

### GAP-02 — Interaction continuity != provider-context continuity — P0

Same product conversation/session does not mean the same provider-visible context forever.

Reuse of provider thread/cache/compaction/prior ConsumerContext requires compatibility with current purpose, WorkContract, identity/representation context, confidentiality compartment and consumer/provider eligibility.

```text
INTERACTION SESSION CONTINUITY
!= PROVIDER-CONTEXT CONTINUITY
```

The same human-visible session may continue with a new clean/sanitized ConsumerContext.

### GAP-03 — Model-discovered InformationNeed scope ceiling — P0

Model-discovered need is an acquisition proposal.

```text
MAY REFINE current ContextPlan
MUST NOT WIDEN WorkContract/policy/security/purpose envelope
```

Hostile document/web/tool content therefore cannot trick the model into obtaining unrelated private sources.

### GAP-04 — Reference resolution requirement per InformationNeed — P0

Discovery may tolerate unresolved candidates; person-specific/consequential work may require unique/exact canonical binding.

```text
AMBIGUITY != CONFIDENCE
```

Required unresolved reference can make ContextReadiness `NOT_READY`.

### GAP-05 — Explicit negative Context constraints — P0

ContextPlan supports:

```text
FORBIDDEN SOURCE
FORBIDDEN DATA CLASS
FORBIDDEN PURPOSE
FORBIDDEN PROVIDER EXPOSURE
FORBIDDEN DERIVATION / USE
```

```text
relevant != allowed
```

### GAP-06 — Child/delegated context minimisation — P0

```text
CHILD WORK CONTRACT
inherits protected obligations

CHILD CONTEXT
is independently minimized to child InformationNeeds
```

```text
WORKCONTRACT PROPAGATION
!= PARENT-CONTEXT INHERITANCE
```

Applies also to external AI delegation.

### GAP-07 — Instruction provenance — P0

A user turn can contain both direct instruction and quoted/untrusted data.

```text
"summarize this email"
→ direct user instruction

quoted email body
→ DATA
```

```text
USER-ORIGINATED
!= INSTRUCTION-AUTHORIZED
```

PDF/web/OCR/tool output remain data unless an explicit trusted runtime contract gives them another control role.

### GAP-08 — ContextReadiness non-monotonicity — P1

```text
READY now
!= READY forever
```

New contradiction, revocation or freshness expiry may make a later consumer step NOT_READY. Old ContextManifest remains an honest historical receipt.

### GAP-09 — Minimisation relative to objective — P1

Minimum necessary context is relative to the legitimate objective.

A narrow metric query may need tiny context. A legitimate cross-life feasibility question may require staged information from work, goals, capacity, family, travel, budget and other relevant domains.

Broad orchestration is allowed; indiscriminate data dumping is not.

### GAP-10 — Governed acquisition / no hidden provider-tool bypass — P0

Every mechanism capable of introducing new information into reasoning participates in the same acquisition boundary.

This includes provider-native search/file retrieval, connected-source tools, browser/computer-use discovery, remote capabilities and child/sub-agent acquisition where present.

```text
PROVIDER-NATIVE ACQUISITION != POLICY BYPASS
MODEL-DISCOVERED TOOL USE != NEW PURPOSE
TECHNICAL CONNECTIVITY != PROCESSING ELIGIBILITY
```

Related clarification:

```text
ACQUISITION AUTHORIZATION != EFFECT AUTHORIZATION
```

A read-like operation that causes a material effect remains governed by AI-02 Effect Runtime semantics.

### GAP-11 — Derived sensitivity closure — P0

Individually lower-sensitivity inputs can compose into a more sensitive health/relationship/identity or other private inference.

```text
DERIVATION MAY TIGHTEN SENSITIVITY
AGGREGATION / SUMMARY / INFERENCE != DECLASSIFICATION
```

A derivative never automatically gets weaker restrictions than material inputs and may require stronger use/exposure restrictions because of what the composite inference reveals.

### GAP-12 — Runtime Interpretation Frame — P0/P1

Reality Scope does not resolve relative/deictic meaning by itself.

Material requests may require:

```text
reference instant
timezone / offset
source/target timezone
DST resolution
calendar/day-boundary semantics
spatial anchor
location source/timestamp/precision
locale/unit/calendar interpretation
```

```text
REALITY SCOPE != RUNTIME INTERPRETATION FRAME
```

Consequential unresolved interpretation may make ContextReadiness NOT_READY rather than permitting a guess.

### GAP-13 — Consumer delivery / transformation integrity — P0

DANTE assembling a correct ConsumerContext does not prove a provider/Harness preserved every required element after truncation, compaction, context editing, server-side tool context or opaque continuation.

```text
ASSEMBLED CONSUMER CONTEXT
!= ESTABLISHED CONSUMER EXPOSURE
```

Unknown effective exposure remains UNKNOWN. Consequence may require declared limitation, rebuild, different consumer/Harness or NOT_READY.

This is not a claim about token-level model attention/causal use.

## 9.6 InformationNeed accepted semantics

Conceptually preserves:

```text
origin
  USER_EXPLICIT
  WORK_CONTRACT
  POLICY_REQUIRED
  CAPABILITY_REQUIRED
  MODEL_DISCOVERED
  SOLVER_REQUIRED
  VERIFIER_REQUIRED

scope
  targets / subjects
  Actor / represented party where material
  temporal scope
  Reality Scope
  Runtime Interpretation Frame where material
  purpose

reference-resolution requirement

criticality
  REQUIRED
  USEFUL
  OPTIONAL

coverage
  COMPLETE_REQUIRED
  BOUNDED_COMPLETE
  BEST_EFFORT
  SAMPLE_ACCEPTABLE

acceptable source semantics
freshness/currentness requirement
coherence requirement
representation/fidelity requirement
consumer constraints

status
  SATISFIED
  PARTIAL
  MISSING
  CONFLICTED
  STALE
  POLICY_BLOCKED
  SOURCE_UNAVAILABLE
  SOURCE_RETIRED
  AMBIGUOUS_TARGET
  AMBIGUOUS_INTERPRETATION
```

Coverage matters because:

```text
bounded authoritative query returns 0
!=
best-effort web search returns 0
```

Absence does not acquire stronger meaning without a justified completeness contract.

## 9.7 ContextFragment accepted semantics

ContextFragment is runtime source-linked representation, **not** a new Domain entity/fact/version/memory root.

Material dimensions may include:

```text
runtime fragment ref / InformationNeed refs
source binding
Reality/source class
Reality Scope
reference binding
Source Standing relative to need
uncertainty/conflict membership
Domain Provenance reference/projection where applicable
runtime transform lineage
confidentiality / instruction provenance / purpose restrictions
derived-sensitivity classification where material
currentness / effective/observed time / validity
Runtime Interpretation Frame where material
MaterialStateRef only where actual source has MaterialState semantics
representation type
resource cost
```

Do not invent fake MaterialStateRefs for web pages, conversation turns, provider revisions or arbitrary tool output.

Accepted separation:

```text
PROVENANCE
!= SOURCE STANDING
!= INTEGRITY / AUTHENTICITY
!= CANONICALITY
!= INSTRUCTION AUTHORITY
!= CONFIDENTIALITY
!= DOMAIN AUTHORITY
```

No universal `trust_score` is accepted.

Reuse existing Domain Provenance semantics plus runtime transform lineage; do not create parallel AIContextProvenance ontology.

## 9.8 ContextReadiness

Top-level:

```text
READY
READY_WITH_DECLARED_LIMITATIONS
NOT_READY
```

Detailed cause belongs to InformationNeed states.

Readiness is consequence/consumer-specific and non-monotonic.

## 9.9 ConsumerContext

Actual DANTE-assembled consumer surface may include:

```text
DANTE/system instructions
WorkContract projection
current direct user instructions
session bindings
ContextFragments
attachments / multimodal input
capability/tool projection
tool results
working state
eligible provider continuation/compaction
```

Different consumers receive different purpose-bound projections.

DANTE-assembled ConsumerContext must not be confused with established effective exposure after provider/Harness transformation.

## 9.10 ContextManifest

ContextManifest is an immutable **exposure receipt** for one invocation.

```text
ConsumerContext != ContextManifest
ContextManifest != BasisManifest
EXPOSED != USED BY MODEL != MATERIAL DEPENDENCY
```

The manifest records only what DANTE can legitimately establish about effective exposure and should normally reference rather than permanently duplicate all sensitive prompt content.

It may preserve consumer/invocation, WorkContract/ContextPlan revisions, exposed fragment/source/version refs, Reality Scope, Runtime Interpretation Frame where material, representation/instruction/tool versions, provider/HarnessProfile, opaque-state/transform declaration, policy refs, resource allocation, digest/limitations and timestamps where useful.

Opaque provider state stays explicitly opaque; DANTE must not invent internal provider provenance or effective exposure it cannot observe.

## 9.11 Source lifecycle / anti-resurrection

Acquisition semantics distinguish:

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

An old ContextManifest may remain historically true while the source/derivative becomes ineligible for new use.

Future embeddings/summaries/indexes/caches/provider state inherit source lifecycle. Old backup bytes do not restore semantic eligibility by themselves.

## 9.12 Fast path

Context Engine is not universal middleware.

Example:

```text
"how much did I run in August?"
→ structured semantic query
→ SQL aggregate
→ typed result
→ publication
```

No RAG/model/context assembly is required if deterministic application logic suffices.

---

# 10. AI-03A accepted invariants C01–C33

```text
C01  CONTEXT != CANONICAL REALITY.

C02  CONTEXT != MEMORY != RETRIEVAL.

C03  Every material context inclusion must be explainable
     by one or more InformationNeeds.

C04  Policy/contract-required needs cannot be silently removed
     by model planning or resource pressure.

C05  Acquisition strategy is selected per InformationNeed;
     DANTE has no universal RAG strategy.

C06  Permission/purpose filtering participates in acquisition,
     not only in final disclosure.

C07  Processing eligibility != consumer/provider exposure
     != recipient disclosure.

C08  Provenance, Source Standing, Integrity, Canonicality,
     Instruction Authority and Confidentiality remain distinct.

C09  DATA != INSTRUCTION.
     Transformation does not elevate instruction authority.

C10  ContextFragment is runtime representation,
     not a new Domain fact/entity/version/memory root.

C11  MaterialStateRef is used only where the actual source
     possesses MaterialState semantics.

C12  Missing != false.
     Search absence has meaning only under declared coverage semantics.

C13  Contradiction is preserved when material;
     retrieval/reranking does not manufacture reconciliation.

C14  Fresh fragments do not automatically form a coherent basis.

C15  ContextReadiness is requirement-based,
     not token-count/model-success based.

C16  Lossy compaction cannot be sole carrier
     of stronger authoritative/protected semantics.

C17  Retired/deleted/redacted information cannot regain eligibility
     through embedding, summary, cache or provider state.

C18  ConsumerContext != ContextManifest.
     ContextManifest is an exposure receipt.

C19  ContextManifest != BasisManifest.
     Exposure != material dependency.

C20  Context machinery is bypassable where deterministic application
     logic can answer correctly without composed context.

C21  Scenario / historical / canonical reality
     must remain explicitly framed.
     No cross-frame laundering.

C22  Interaction Session continuity
     does not imply provider-context continuity.

C23  Model-discovered InformationNeeds
     may refine but never silently widen
     the current WorkContract/policy scope.

C24  Reference resolution requirements
     are explicit per InformationNeed.
     Ambiguity is not confidence.

C25  Explicit source/use exclusions
     are first-class ContextPlan constraints.

C26  Child/delegated work inherits protected obligations,
     not the parent's entire context.

C27  User-originated content
     does not automatically possess user-instruction authority.
     Quoted/attached/forwarded content remains data.

C28  ContextReadiness is consumer-specific and non-monotonic.

C29  Minimum necessary context
     is relative to the legitimate objective.
     Broad orchestration may legitimately require
     broad but staged cross-domain acquisition.

C30  Any mechanism that introduces new information into reasoning
     participates in governed acquisition.
     Provider-native tools/connectors/subagents do not bypass
     WorkContract, purpose, InformationNeed or acquisition policy.
     Acquisition authorization does not imply effect authorization.

C31  Derived representations do not automatically receive weaker
     sensitivity/use restrictions than their material inputs
     and may require stricter restrictions because of what
     composition/inference itself reveals.

C32  Reality Scope does not replace Runtime Interpretation Frame.
     Material relative temporal/spatial/locale expressions must be
     resolved sufficiently for the InformationNeed/consequence;
     ambiguous consequential interpretation may make Context NOT_READY.

C33  Assembled ConsumerContext does not prove established effective
     consumer exposure when a provider/Harness may transform,
     compact, truncate or augment context opaquely.
     Unknown effective exposure remains UNKNOWN rather than fabricated.
```

Treat these as fixed upstream contracts for AI-03B unless real contradictory evidence appears.

---

# 11. AI-03A validation result

The final hardened architecture was retested against representative prior simulations and hostile/scale/compound cases including:

```text
student + external deadline
farmer + weather + machinery
group trip
friends/free-busy
household conflicting sources
child pickup
caregiver medication
shared car
team release
shift swap
lawyer/client
surgery / specialist System of Record
photographer/weather replan
creator/release
low-digital participant
professional document
15-year history / millions of rows
2,000-page document
1M+ context window
context-window exhaustion
SQL-zero vs web-zero
provider cache after revocation
source deletion after exposure
backup restoring deleted derivative bytes
Consent revocation during reasoning
provider failover
opaque provider state
voice ambiguous target
OCR error
cumulative inference leakage
malicious child agent
Work Supersession / changed objective
provider-native private connector acquisition
malicious source inducing additional tool acquisition
read-like acquisition with hidden material side effect
low-sensitivity signals composing into sensitive inference
travel/timezone-relative requests
DST-overlap ambiguous consequential time
provider automatic compaction/truncation
partially unresolved conversational-target bootstrap
```

Final structural result:

```text
NORTH STAR CAPABILITY COVERAGE         PASS
SINGLE-USER / CROSS-DOMAIN             PASS
MULTI-ACTOR                            PASS
EXTERNAL / SPECIALIST SOR              PASS
SCENARIOS / ALTERNATIVE FUTURES        PASS after hardening
HISTORY / CURRENTNESS                  PASS
REFERENCE AMBIGUITY                    PASS after hardening
PRIVACY / PURPOSE                      PASS after hardening
PROVIDER CONTINUITY                    PASS after hardening
PROVIDER-NATIVE ACQUISITION            PASS after final hardening
DERIVED SENSITIVITY                    PASS after final hardening
RUNTIME INTERPRETATION FRAME           PASS after final hardening
CONSUMER DELIVERY / TRANSFORMATION     PASS after final hardening
CHILD / EXTERNAL AGENT CONTEXT         PASS after hardening
PROMPT / CONTEXT INJECTION             PASS structurally after hardening
REVOCATION                             PASS
ANTI-RESURRECTION                      PASS structurally
LONG CONTEXT                           PASS
LARGE HISTORY                          PASS
LARGE DOCUMENTS                        PASS architecturally
CONTEXT WINDOW PRESSURE                PASS
OPAQUE PROVIDER STATE                  PASS
MULTIMODAL / VOICE                     PASS
FUTURE MODEL REPLACEMENT               PASS
FAST DETERMINISTIC PATH                PASS

NEW TOP-LEVEL CONTEXT CONTRACT         NO
DOMAIN REOPEN REQUIRED                 NO
LOGICAL REOPEN REQUIRED                NO
PHYSICAL REOPEN REQUIRED               NO
DATABASE CHANGE REQUIRED               NO
ALEMBIC CHANGE REQUIRED                NO
```

Do not claim this proves runtime retrieval accuracy, performance or physical invalidation behavior.

---

# 12. What AI-03A explicitly did NOT prove/decide

Still open and belonging to AI-03B/C or later:

```text
retrieval accuracy at large scale
best chunking algorithm/size
embedding model
dimensions
pgvector/HNSW/IVFFlat behavior
PostgreSQL FTS/trigram exact design
hybrid retrieval formula
reranker
conversation persistence
Run/working persistence
memory admission implementation
memory correction implementation
summary persistence
provider-native memory use
prompt-cache economics
physical derivative invalidation latency/recovery
specialist vector DB
Redis
model/provider choice
SDK/gateway
local model/GPU/server
```

Do not infer any of these choices from AI-03A closure.

---

# 13. CURRENT WORK — AI-03B Final Independent Validation

Durable candidate authority:

```text
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
```

Current state:

```text
DANTE-FIRST INTERNAL DESIGN           COMPLETE
TARGETED MODERN CHALLENGER RESEARCH  COMPLETE
RECONCILIATION                       COMPLETE
FIRST HEAVY KILL-TEST                PASS CANDIDATE
B01..B30                             CANDIDATE
AI-03B CLOSED                        NO
FINAL INDEPENDENT VALIDATION         NEXT
```

Do **not** restart AI-03B as a blank-slate architecture exercise. Do **not** treat the candidate's first PASS as proof either.

The fresh validation must independently reconstruct the required Retrieval/Memory obligations from Product/Domain/Logical/PostgreSQL/Recovery/AI-02/AI-03A and try to break the materialized candidate.

## 13.1 Retrieval candidate architecture

Two additional runtime architecture contracts are currently proposed:

```text
RetrievalPlan
RetrievalCandidate
```

They are not Domain roots, database tables or mandatory services.

The candidate flow is:

```text
AI-03A InformationNeed
        ↓
RetrievalPlan
        ├ eligible search universe
        ├ retrieval guarantee / coverage requirement
        ├ source semantics
        ├ Reality Scope
        ├ Runtime Interpretation Frame where material
        ├ reference/currentness/coherence requirements
        ├ explicit exclusions
        └ resource / latency / cost bounds
        ↓
least-complex adequate route
        ├ structured / exact
        ├ material history
        ├ typed relation traversal
        ├ lexical / fuzzy
        ├ semantic / ANN
        ├ hybrid / rerank
        ├ hierarchical document
        ├ direct long-context
        ├ Interaction / Run
        ├ provider/federated
        └ open-world / bounded JIT
        ↓
RetrievalCandidate
        ↓
source / policy / lifecycle / currentness / identity validation
        ↓
ContextFragment
        ↓
AI-03A ContextReadiness
```

Key retrieval candidate rules:

```text
RETRIEVAL != TRUTH
APPROXIMATE != COMPLETE
candidate count != coverage proof
rank/similarity/rerank != Source Standing
multiple chunks/derivatives of one lineage != independent corroboration
index/cache/embedding != source
consequential derived retrieval may require source reread
permission-safe acquisition defines the eligible search universe
```

## 13.2 Memory candidate architecture

Memory classes remain separated:

```text
CANONICAL APPLICATION MEMORY
→ already Domain/PostgreSQL
→ not generic AI memory

INTERACTION MEMORY
→ discourse/session/referent continuity
→ transcript != canonical truth

RUN / WORKING MEMORY
→ intermediate research/calculation/tool state
→ transient by default

COMPACTION / CHECKPOINT
→ continuity optimization
→ lossy / not source

ADAPTIVE / DERIVED USER MEMORY
→ bounded user-specific hypotheses/patterns
→ candidate, not confirmed truth

OPERATIONAL / EXPERIENCE MEMORY
→ verified reusable knowledge about bounded environment/provider/workflow behavior
→ experience != policy

PROVIDER MEMORY / THREAD / CACHE
→ replaceable optimization

RETRIEVAL REPRESENTATIONS
→ chunks/summaries/FTS/vector/embedding/index state
→ technical derivatives

EXECUTION EVIDENCE
→ effect/runtime reconstruction
→ not user memory
```

Common admission rule:

```text
DEFAULT NONCANONICAL SURVIVAL = NO
MEMORY SURVIVAL MUST BE EARNED
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
MEMORY EXISTS != MEMORY MAY BE RECALLED
MEMORY RECALL = GOVERNED ACQUISITION
```

## 13.3 Correction / suppression hardening

The candidate distinguishes:

```text
CORRECT
FORGET
SOURCE SUPPRESSION
USE SUPPRESSION
INFERENCE DISPOSITION
```

This is required to prevent semantic re-inference resurrection.

Example:

```text
truthful late-night history
→ derived "prefers working late"
→ user rejects hypothesis
→ same history remains
→ future system MUST NOT silently recreate equivalent rejected hypothesis
```

Durable adaptive memory therefore needs bounded typed semantics sufficient for correction/scope/expiry/disposition. Free-form prose alone is not accepted as durable semantic authority.

Also:

```text
DERIVATIVE != INDEPENDENT EVIDENCE OF ITS ANCESTRY
```

so a memory cannot increase its own apparent confidence through repeated re-derivation.

## 13.4 Operational/experience poisoning boundary

Operational memory can survive only on adequate verified basis such as, where appropriate:

```text
verified execution outcome
provider receipt / reread
Verifier result
repeated independently verified execution
trusted operational specification
```

Not sufficient by itself:

```text
model self-report
untrusted webpage
malicious document/tool output
assistant-generated success summary
```

```text
PAST EXPERIENCE != POLICY
EXPERIENCE != INSTRUCTION AUTHORITY
```

## 13.5 Recovery / anti-resurrection

All retrieval/memory derivatives inherit current source lifecycle.

```text
RESTORED BYTES != RESTORED ELIGIBILITY
```

Old summary/embedding/cache/provider-memory bytes cannot become active merely because restore/recovery made them physically available again.

The existing PostgreSQL `material_state_retirement` / suppression semantics remain the canonical source-lifecycle boundary.

---

# 14. Targeted challenger research — COMPLETE

Do not run another generic retrieval/memory landscape study before final validation unless a new specific technical contradiction appears.

The candidate was already challenged against current evidence for:

```text
PostgreSQL FTS / pg_trgm / pgvector 0.8.x
filtered approximate ANN / iterative scans
hybrid lexical+dense retrieval
long-context vs RAG/retrieval
hierarchical/contextual retrieval
reranking / late interaction challenger patterns
LongMemEval / LongMemEval-V2
LoCoMo-Plus
memory poisoning / MemoryGraft-style attacks
Mem0
Zep / Graphiti
Letta / agent memory patterns
current provider-native search/thread/cache/compaction/continuation behavior
```

Material consequences already incorporated:

```text
APPROXIMATE != COMPLETE
eligible search universe must be explicit
no universal RAG-first route
Operational/Experience Memory is distinct from Adaptive User Memory
poisoned experience requires verified admission basis
provider state remains replaceable/noncanonical
correct non-recall / non-application is part of memory quality
```

Technology/framework appearance in research does not select it for DANTE.

---

# 15. First AI-03B kill-test result

The reconciled candidate has already survived a first heavy internal adversarial pass including:

```text
ANN used for COMPLETE_REQUIRED
permission filtering only after ANN
vector zero interpreted as absence
many chunks from one source pretending to corroborate
stale embedding after source correction
old embedding restored from backup
rejected inference recreated from surviving history
same rejected inference paraphrased
self-confirming memory loop
poisoned fake-success operational memory
provider behavior/version drift
model says "remember this"
malicious source says "remember this secret"
old chat memory enters a new purpose
same Interaction Session switches represented party
private caregiver fact enters shared output
provider persistent thread after revocation
long Run resumes after days
retrieval cache survives Visibility change
direct long-context vs indexed retrieval
RAG used where bounded exact SQL was required
operational experience treated as instruction
forgotten AI memory while canonical state remains
old user statement conflicts with newer canonical state
15-year history / millions of rows
very large context/history
source-derived duplicate memories
source retirement during active Run
```

Current result:

```text
AI-03B RECONCILED CANDIDATE
STRUCTURAL PASS CANDIDATE

new Domain owner                 NO
Logical reopen                   NO
Physical reopen                  NO
PostgreSQL/Alembic change        NO
new generic Memory/Fact ontology NO
knowledge graph required         NO
vector DB required               NO
Redis required                   NO
provider selection               NO
```

This is **not** final closure evidence. The next validation must start from the source obligations again rather than trusting this table.

---

# 16. AI-03B candidate invariants B01–B30

```text
B01  RETRIEVAL != TRUTH.
B02  RetrievalCandidate != ContextFragment.
B03  Retrieval guarantee must match InformationNeed coverage.
B04  APPROXIMATE != COMPLETE.
B05  Candidate count != coverage proof.
B06  Eligibility defines the permitted search universe;
     post-filtering alone is not a universal permission proof.
B07  Rank / similarity / rerank != Source Standing.
B08  Multiple representations of one lineage != independent corroboration.
B09  Index / cache / embedding != source.
B10  Consequential derived retrieval may require source reread/current-state validation.
B11  Memory survival defaults to NO.
B12  MEMORY EXISTS != MEMORY MAY BE RECALLED.
B13  Memory recall is governed acquisition under AI-03A.
B14  MODEL REQUEST TO REMEMBER != MEMORY ADMISSION.
B15  Canonical application semantics belong to Domain/PostgreSQL, not generic AI memory.
B16  Durable adaptive memory requires bounded typed semantics;
     free-form prose alone is not durable semantic authority.
B17  Derived memory != independent evidence of its ancestry.
B18  Correction != Forgetting != Source Suppression
     != Use Suppression != Inference Disposition.
B19  Rejected/corrected inference must not silently resurrect
     from materially equivalent surviving basis.
B20  Operational experience requires verified basis
     and bounded environment/version applicability.
B21  PAST EXPERIENCE != POLICY.
B22  Provider memory is replaceable optimization.
B23  Retrieval representations inherit source lifecycle.
B24  Restored bytes != restored eligibility.
B25  Memory promotion may propose a Domain/application change;
     it cannot mint canonical truth itself.
B26  Interaction memory != transcript truth.
B27  Run/working memory defaults transient.
B28  Compaction/checkpoint != source.
B29  Execution evidence != user memory.
B30  Correct non-recall / non-application is part of memory quality.
```

Treat these as candidate contracts only until the final independent validation closes AI-03B.

---

# 17. AI-03B things that remain explicitly OPEN

The following remain deliberately unselected/unmaterialized:

```text
conversation table
Run/working table
memory table
adaptive-memory table
operational-memory table
summary table
chunk table
embedding table
embedding model/dimension
pgvector activation
HNSW / IVFFlat parameters
new FTS indexes
retrieval cache store
specialist vector DB
Redis
Mem0 / Zep / Graphiti / Letta adoption
provider-native memory/thread strategy
prompt-cache persistence
exact retention jobs
exact physical anti-resurrection propagation
OpenAI / Anthropic / Gemini / Qwen choice
local model/server/GPU
model gateway/router
SDK/framework
sandbox implementation
MCP/A2A implementation
```

A research technique is not a decision.

AI-03C, not AI-03B, owns physical/materialization classification after AI-03B is closed.

---

# 18. Final independent AI-03B validation process

Do not add dozens of micro-phases.

Current flow:

```text
1. RECONSTRUCT INTERNAL REQUIREMENTS
   COMPLETE for candidate construction
   REPEAT INDEPENDENTLY for final validation

2. BUILD DEEP INITIAL RETRIEVAL + MEMORY ARCHITECTURE
   COMPLETE

3. TARGETED MODERN RETRIEVAL/MEMORY RESEARCH
   COMPLETE

4. RECONCILE AI-03B CANDIDATE
   COMPLETE

5. FIRST HEAVY CANDIDATE KILL-TEST
   COMPLETE / PASS CANDIDATE

6. FINAL INDEPENDENT READBACK + DESTRUCTIVE VALIDATION
   NEXT

7. HARDEN ONLY REAL NEW GAPS
   IF FOUND

8. CLOSE AI-03B STRUCTURALLY
   ONLY IF FINAL VALIDATION PASSES

9. AI-03C
   whole Context/Retrieval/Memory destructive validation
   + physical/materialization blueprint
```

Final validation must pressure at minimum:

```text
permission-safe approximate retrieval
coverage guarantees / false absence
source lifecycle + stale derivative paths
multi-lineage vs same-lineage evidence
inference resurrection
self-confirming memory
poisoned operational experience
correction / forgetting / suppression semantics
multi-actor / represented-party switching
provider state after revocation/failover
long-running Run resume
large history / documents / context pressure
correct non-recall / non-application
Recovery / anti-resurrection
future stronger models / larger context windows
```

If a concrete gap requires fresh outside evidence, run research only on that exact gap.

---

# 19. Git write-gate discipline

Before any new remote write use exactly:

```text
BRANCH
<exact branch>

PRE-SCOPE
<exact current SHA>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<purpose>

EXPLICITLY OUT OF SCOPE
<out of scope>
```

Then re-fetch live branch HEAD immediately before first write.

If the exact PRE-SCOPE differs:

```text
STOP
RE-GATE
```

After writes:

```text
compare PRE-SCOPE..HEAD
verify exact changed paths
verify create/update/delete classification
verify no scope creep
verify branch relation
read back current status/routing
never claim implementation PASS from documentation-only work
```

---

# 20. Documentation / handoff lifecycle

Durable architecture decisions belong in architecture/current sources.

This file is only a branch-operational save-game.

Update it only at meaningful checkpoints such as:

```text
macro-phase closure
large accepted architecture change
chat/context saturation
partially completed write set
important unresolved tactical continuation point
```

Do not turn it into an append-only diary.

Before `feature/ai-architecture` is integrated into protected `main`:

```text
classify meaningful handoff content
→ propagate durable current truth/rationale/evidence
→ verify knowledge coverage
→ delete this live handoff
```

Temporary handoff count entering protected `main` must be zero.

---

# 21. Exact safe next action for the next chat

```text
NO REPOSITORY WRITE IS REQUIRED JUST TO BEGIN FINAL AI-03B VALIDATION.
```

First:

1. fetch live branch/ref and verify current HEAD;
2. read the mandatory current authority above, especially `dante-ai-03b-retrieval-memory-architecture.md`;
3. acknowledge AI-03A as CLOSED / C01..C33 and AI-03B as **CANDIDATE, NOT CLOSED**;
4. do not restart generic retrieval/memory research or architecture ideation;
5. independently reconstruct AI-03B requirements from Product/Domain/Logical/PostgreSQL/Recovery/AI-02/AI-03A;
6. attack `RetrievalPlan`, `RetrievalCandidate`, coverage/eligibility semantics, memory classes and the Survival/Admission lifecycle as if the existing PASS label were untrusted;
7. specifically attack approximate retrieval, permission filtering, stale derivatives, inference resurrection, self-corroboration, poisoned experience, cross-purpose/multi-actor reuse, provider revocation/failover, long-running currentness and anti-resurrection;
8. classify every finding as real gap vs already-covered failure vs implementation/materialization question;
9. if a real structural gap exists, harden the smallest AI-03B boundary and retest before any closure;
10. if no unresolved structural contradiction remains, issue a separate exact write gate to close AI-03B and update routing toward AI-03C;
11. do not create DB/index/provider implementation or enter AI-03C materialization before AI-03B closure.

The new chat must continue this exact checkpoint rather than inventing a fresh AI architecture.