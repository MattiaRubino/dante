# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-03 — Context / Retrieval / Memory
- **AI-03A:** CLOSED / STRUCTURALLY ACCEPTED
- **Current macro-phase:** AI-03B — Retrieval + Memory Architecture
- **Created:** 2026-09-01
- **Refreshed after AI-03A closure:** 2026-09-01
- **PRE-SCOPE for this reconciliation:** `1181f402aa187a04cd268ba3fa947c6a63ab9ead`
- **Last substantive checkpoint before this handoff refresh:** `8b5a37d94124f200c8a11d71ea24020f4ba35f48`
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
current     AI-03B Retrieval + Memory Architecture
```

Do not recreate AI-00, AI-01, AI-02 or AI-03A from scratch.

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

  AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
  ACTIVE / CURRENT

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

# 9. AI-03A — CLOSED / STRUCTURALLY ACCEPTED

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
9 MATERIAL HARDENINGS

        ↓
HARDENED CANDIDATE
STRUCTURAL PASS
```

Final closure:

```text
AI-03A FULL CONTEXT ARCHITECTURE
CLOSED / STRUCTURALLY ACCEPTED

Domain reopen       NO
Logical reopen      NO
Physical reopen     NO
PostgreSQL change   NO
Alembic change      NO
implementation PASS NO
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
WORK CONTRACT
  ↓
CONTEXT PLAN
  ├ contract/policy needs
  ├ user/request needs
  └ dynamic/discovered needs
  ↓
INFORMATION NEEDS
  ↓
CONTEXT STRATEGY per need
  ↓
DISCOVERY / ACQUISITION PEP
  ↓
SOURCE READ / SOURCE BINDING
  ↓
CONTEXT FRAGMENTS
  ↓
Reality Scope / Provenance / Source Standing /
Integrity / Canonicality / Instruction Provenance /
Confidentiality / Temporal Validity / Contradiction
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

## 9.5 The nine hardenings that closed AI-03A

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
currentness / effective/observed time / validity
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

Actual consumer-visible surface may include:

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

## 9.10 ContextManifest

ContextManifest is an immutable **exposure receipt** for one invocation.

```text
ConsumerContext != ContextManifest
ContextManifest != BasisManifest
EXPOSED != USED BY MODEL != MATERIAL DEPENDENCY
```

The manifest should normally reference rather than permanently duplicate all sensitive prompt content.

It may preserve consumer/invocation, WorkContract/ContextPlan revisions, exposed fragment/source/version refs, Reality Scope, representation/instruction/tool versions, provider/HarnessProfile, opaque-state declaration, policy refs, resource allocation, digest/limitations and timestamps where useful.

Opaque provider state stays explicitly opaque; DANTE must not invent internal provider provenance it cannot observe.

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

# 10. AI-03A accepted invariants C01–C29

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
```

Treat these as fixed upstream contracts for AI-03B unless real contradictory evidence appears.

---

# 11. AI-03A validation result

Hardened architecture was retested against representative prior simulations and hostile/scale cases including:

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

# 13. CURRENT WORK — AI-03B Retrieval + Memory Architecture

This is the exact work a fresh chat must start.

Do **not** go back to another generic Context mega-test.

Do **not** materialize tables/indexes first.

AI-03B asks two linked questions:

> **How does DANTE actually find the candidate information required by an accepted AI-03A InformationNeed?**

and:

> **Which noncanonical information/state, if any, legitimately survives beyond the immediate step/Run, under what lifecycle and correction/deletion rules?**

## 13.1 Retrieval scope

Design in depth:

```text
Semantic Query / Projection Gateway consumption
structured current-state retrieval
material-history retrieval
specific relation traversal
metadata filtering
PostgreSQL native FTS
pg_trgm / fuzzy retrieval
semantic/vector retrieval where justified
hybrid retrieval
reranking
source reread
freshness/currentness validation
coverage-aware retrieval
permission-aware discovery/retrieval
iterative/JIT retrieval
query decomposition/reformulation where justified
document hierarchy / chunking
large-corpus retrieval
long-context vs indexed retrieval decisions
retrieval caches and lifecycle
retrieval evaluation / failure metrics
```

Retrieval must satisfy AI-03A semantics, not replace them.

At minimum preserve:

```text
InformationNeed coverage
Reality Scope
reference-resolution requirement
source binding
Source Standing / Provenance / integrity distinctions
purpose/acquisition eligibility
currentness/coherence requirements
explicit exclusions
anti-resurrection
```

Retrieval rank/similarity never establishes canonical truth or source currentness.

## 13.2 Memory scope

Separate memory classes before selecting storage:

```text
CANONICAL APPLICATION MEMORY
already owned by Domain/PostgreSQL
not an AI memory layer

INTERACTION MEMORY
conversation/session continuity
referents / attachments / current discourse state
not automatically canonical

RUN / WORKING MEMORY
intermediate calculations / research / working artifacts
transient by default

COMPACTION / CHECKPOINT STATE
continuity optimization
lossy unless proven otherwise
not source authority

DERIVED / ADAPTIVE MEMORY
patterns / hypotheses / inferred preferences
candidate by default
requires provenance/evidence/scope/time/conflict lifecycle

PROVIDER MEMORY / THREAD / PROMPT CACHE
replaceable optimization
never DANTE authority

RETRIEVAL REPRESENTATIONS
chunks / summaries / FTS/vector representations / embeddings/indexes
technical derivatives
not facts

EXECUTION EVIDENCE
runtime/effect reconstruction
not user memory
```

## 13.3 Memory lifecycle

AI-03B must explicitly resolve:

```text
admission
why something is allowed to survive
purpose
scope
source/provenance
promotion
confirmation
correction
contradiction
supersession
decay
expiry
retirement
redaction
deletion
forgetting
anti-resurrection
provider/cache invalidation
index invalidation
```

Primary rule:

```text
MEMORY SURVIVAL MUST BE EARNED
```

Canonical DANTE state is not copied into generic memory merely to make retrieval easier.

---

# 14. Research expectation for AI-03B

Use targeted modern research as challenger evidence, not as architecture authority.

A deep Retrieval/Memory review should examine at least:

```text
PostgreSQL FTS / pg_trgm / pgvector behavior
filtered ANN / HNSW / IVFFlat limitations
hybrid lexical+dense retrieval
reranking
late interaction / contextual retrieval where relevant
query decomposition/adaptive retrieval
hierarchical/parent-child document retrieval
source reread/currentness
retrieval evaluation
long-context tradeoffs

Mem0
Zep / Graphiti
Letta
LangGraph/LangMem
LlamaIndex / Haystack memory/retrieval patterns
provider-native memory/thread/cache mechanisms
modern memory benchmarks / temporal memory / knowledge update
memory poisoning
correction/deletion through summaries/embeddings/cache
```

Do not adopt a framework because it appears modern.

For every technique ask:

```text
what problem does it solve?
does DANTE actually have that problem?
does it preserve AI-03A contracts?
is it a semantic responsibility or implementation optimization?
what are failure modes?
what is mature vs experimental?
what lifecycle/deletion burden does it create?
what is the simplest adequate alternative?
```

If current provider/pricing/features matter, use fresh primary-source research rather than stale memory.

---

# 15. AI-03B quality bar

The architecture should be professional and detailed enough to answer:

```text
For each InformationNeed, which retrieval strategy can satisfy it and why?
What does completeness mean for each source class?
When is SQL/structured query enough?
When is FTS/fuzzy retrieval enough?
When is semantic/vector retrieval justified?
When is direct long-context better?
How are multi-stage/JIT strategies bounded?
How do permissions participate before candidate exposure?
How is source reread/currentness verified?
How are Reality Scope and target identity preserved through indexes?
How do chunk/summary/embedding representations retain source lineage?
What happens when a source is corrected/retired/deleted?
What may survive as Interaction/working/derived memory?
What cannot survive?
What promotes a user statement/inference toward durable application semantics, if anything?
How are contradictions handled without latest-wins laundering?
How are memory poisoning and stale memory detected/contained?
How can provider memory be discarded/rebuilt?
What metrics prove retrieval/memory quality rather than only final answer quality?
```

Performance requirements remain architectural:

```text
simple structured read stays cheap
no vector search for every request
no model call for deterministic aggregation
no context dump of entire history
no specialist store without measured need
```

---

# 16. AI-03B things that remain explicitly OPEN

Do not close these before the architecture/evidence earns them:

```text
conversation table
Run/working table
memory table
summary table
chunk table
embedding table
embedding model/dimension
pgvector activation
HNSW / IVFFlat parameters
new FTS indexes
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

---

# 17. Expected AI-03B process

The user does not want dozens of micro-phases.

Recommended flow:

```text
1. RECONSTRUCT INTERNAL REQUIREMENTS
   AI-03A + Domain/Logical/DB/Recovery + Product cases

2. BUILD ONE DEEP INITIAL RETRIEVAL + MEMORY ARCHITECTURE
   semantic classes / lifecycle / retrieval paths

3. TARGETED MODERN RETRIEVAL/MEMORY RESEARCH
   challenge weak assumptions and compare modern production patterns

4. RECONCILE INTO AI-03B CANDIDATE

5. DEDICATED RETRIEVAL/MEMORY ADVERSARIAL TEST
   only after the candidate is complete

6. HARDEN REAL GAPS

7. CLOSE AI-03B STRUCTURALLY IF IT PASSES

8. AI-03C
   whole Context/Retrieval/Memory destructive validation
   + physical/materialization blueprint
```

Do not materialize AI-03B before the architecture and its lifecycle are coherent.

---

# 18. Git write-gate discipline

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

# 19. Documentation / handoff lifecycle

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

# 20. Exact safe next action for the next chat

```text
NO REPOSITORY WRITE IS REQUIRED JUST TO BEGIN AI-03B.
```

First:

1. fetch live branch/ref and verify current HEAD;
2. read the mandatory current authority above;
3. explicitly acknowledge AI-03A as CLOSED / STRUCTURALLY ACCEPTED;
4. do not reopen its nine hardenings/C01..C29 without contradictory evidence;
5. start **AI-03B — Retrieval + Memory Architecture** in analysis/design mode;
6. reconstruct retrieval/memory needs from actual DANTE Product/Domain/Logical/DB semantics and simulations;
7. use modern primary-source/paper/framework research as challenger evidence;
8. build the architecture deeply in one large pass;
9. only after it is coherent decide whether a dedicated AI-03B mega-test is ready;
10. do not create DB/index/provider implementation before a later exact write gate and the AI-03C materialization discipline.

The new chat should behave as a continuation of this workstream, not as an agent asked to invent a fresh AI architecture.
