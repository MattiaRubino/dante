# DANTE AI-03 — Context / Retrieval / Memory Architecture

- **Status:** ACTIVE / BRANCH-LOCAL ARCHITECTURE WORKSTREAM
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Upstream structural baseline:** AI-02.1 v0.5 / STRUCTURALLY ACCEPTED
- **AI-03A:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE / 13 HARDENINGS
- **AI-03B:** CANDIDATE / STRUCTURAL PASS PENDING FINAL INDEPENDENT VALIDATION
- **Implementation:** NOT STARTED by this document
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT
- **Provider/model selection:** OPEN
- **Current macro-phase:** AI-03B — RETRIEVAL + MEMORY ARCHITECTURE

---

## 1. Purpose

AI-03 defines how DANTE obtains, scopes, validates, composes, retains, retrieves and retires information used by intelligence without creating a second reality beside the accepted Product/Domain/Logical/Physical/PostgreSQL system.

The central question is not "which vector database should DANTE use?" or "which memory framework should DANTE adopt?".

The central question is:

> **How does DANTE build the minimum sufficiently complete, currently valid, authorized and purpose-relevant representation of reality required for a piece of work, and which noncanonical information — if any — earns the right to survive beyond that work?**

AI-03 consumes the closed Product/Domain/Logical/Physical/database authority and the structurally accepted AI-02 runtime architecture. It must not reopen those layers for retrieval or memory convenience.

---

## 2. Authoritative source corpus

AI-03 must be read against the following sources before material architecture decisions are made.

### Product / North Star

- `docs/product/product-identity-and-north-star.md`
- `docs/product/v1-data-history-and-privacy.md`
- `docs/product/v1-learning-context-and-ai-boundary.md`
- relevant V1 product contracts for adaptive intelligence, user context/safety, work/meeting lifecycle, confirmation/reminders, scheduling, goal/program lifecycle and execution status
- cross-domain and multi-actor simulation evidence

### Semantic authority

- `docs/domain/README.md`
- accepted Domain concept specifications
- `docs/logical-model/README.md`
- `docs/logical-model/whole-logical-model-v1.md`
- WL-H01..WL-H12

### Physical / persistence authority

- `docs/physical-model/README.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`
- current Alembic / SQLAlchemy / real PostgreSQL truth

### Intelligence authority

- `docs/architecture/dante-ai-foundation.md`
- `docs/architecture/ai-production-engineering-state-of-the-art-2026.md`
- `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`
- `docs/architecture/dante-ai-03a-full-context-architecture.md`
- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`
- `docs/architecture/system-overview.md`

Repository truth outranks conversation memory.

---

## 3. Inherited non-negotiable invariants

AI-03 inherits, without reinterpretation:

```text
DANTE != model
DANTE != provider
DANTE != chat transcript

PostgreSQL = sole canonical persistence / material-history authority

CANONICAL STATE != DERIVED STATE
CANONICAL STATE != PROVIDER STATE
CANONICAL STATE != RETRIEVAL INDEX
CANONICAL STATE != CONVERSATION MEMORY
CANONICAL STATE != MODEL MEMORY

Person != Account != Principal != Actor
Authority != AuthZ
Consent != Authority
Visibility != Authority
Context access != disclosure permission

AI inference != confirmed fact
AI confidence != Confirmation
search rank != truth
vector similarity != truth
summary != source
embedding != source
cache != source

NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
MaterialStateRef != provider revision / ETag / MVCC token

absence / unknown != false
current state != historical state
correction != silent overwrite

Interaction Session != Run != Worker
Scenario state != canonical current state
WorkContract != chat transcript
BasisManifest != prompt log

MODEL OUTPUT != PUBLISHABLE OUTPUT
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
DATA != INSTRUCTION

retired / deleted / redacted source
must not silently re-enter eligibility through
summary / embedding / cache / provider state / derived memory
```

AI-03A adds accepted context invariants `C01..C33`; see `dante-ai-03a-full-context-architecture.md`.

No Context/Memory design is accepted if it creates a generic semantic escape hatch around closed Domain/Logical meaning.

---

## 4. Product obligations inherited by AI-03

The North Star requires DANTE to build sufficiently rich context over time so that it can connect relevant parts of life and avoid restarting from zero, while preserving user authority, history, source integrity, privacy, uncertainty and progressive complexity.

Therefore AI-03 must support:

```text
current structured personal state
material history
people / relationships / responsibilities
constraints / policies / preferences where legitimately represented
plans / schedules / actuals / outcomes
current and historical decisions
external source material
professional/source-authored programs
notes / documents / artifacts
conversation continuity
open-world information
multi-actor selective context
conflicting / uncertain evidence
long-running work
future richer multimodal/general-purpose intelligence
```

But:

```text
DANTE knows X
!=
DANTE should always use X
!=
DANTE may disclose X
!=
X should be copied into every model context
!=
X deserves permanent AI memory
```

Purpose limitation and minimisation are product architecture requirements, not launch-time polish.

---

## 5. Core AI-03 distinction

AI-03 keeps three responsibilities separate:

```text
CONTEXT
= the purpose-bound runtime view available to a specific reasoning/execution step

RETRIEVAL
= the process that discovers and validates candidate material for context

MEMORY
= information/state that survives beyond the immediate step or Run under an explicit lifecycle
```

A single item may participate in more than one responsibility over time, but the responsibilities are not synonyms.

AI-03A has now closed the Context contract after its original hardening cycle and a separate final independent destructive revalidation. AI-03B must consume the final `C01..C33` contract rather than redefine Context around a preferred retrieval or memory technology.

---

## 6. AI-03 roadmap

AI-03 is intentionally divided into only three large architecture passes.

### AI-03A — Full Context Architecture

**Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE

Durable authority:

- `docs/architecture/dante-ai-03a-full-context-architecture.md`

Accepted runtime contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
```

plus the inherited AI-02 `BasisManifest`.

The accepted hardened flow is:

```text
bounded WorkContract
→ ContextPlan
→ InformationNeeds
→ sufficient Reality Scope / Runtime Interpretation Frame where material
→ strategy per need
→ discovery/acquisition eligibility
→ governed acquisition, including provider-native/JIT/tool acquisition
→ source read / source binding
→ source-linked ContextFragments
→ Reality Scope / provenance / Source Standing /
  integrity / canonicality / instruction provenance /
  confidentiality / derived sensitivity / temporal validity / contradiction
→ coverage + coherence
→ ContextReadiness
→ minimisation / transformation
→ resource-aware packing
→ consumer exposure eligibility
→ ConsumerContext
→ Harness / consumer invocation
→ establish what effective consumer exposure can actually be proved
→ ContextManifest exposure receipt
→ bounded iterative/JIT acquisition where required
```

A bounded WorkContract may be partially unresolved when context is required for interpretation/reference resolution, but:

```text
UNRESOLVED != UNBOUNDED
```

The original dedicated AI-03A mega-test found nine real gaps. A later independent reverse-engineering/kill-test reconstructed requirements from the accepted DANTE stack and found four additional boundary hardenings without requiring a new Context contract.

```text
GAP-01 Reality Scope / Scenario binding
GAP-02 Interaction continuity != provider-context continuity
GAP-03 model-discovered need cannot widen WorkContract/policy scope
GAP-04 reference-resolution requirement per InformationNeed
GAP-05 explicit source/use exclusions
GAP-06 child/delegated context minimisation
GAP-07 user-origin content != automatic instruction authority
GAP-08 ContextReadiness is non-monotonic
GAP-09 minimisation remains relative to legitimate broad objective

GAP-10 governed acquisition / no hidden provider-tool bypass
GAP-11 derived sensitivity closure
GAP-12 Runtime Interpretation Frame
GAP-13 consumer delivery / transformation integrity
```

The final revalidation also clarified:

```text
ACQUISITION AUTHORIZATION != EFFECT AUTHORIZATION
UNRESOLVED WORKCONTRACT REFERENCES != UNBOUNDED ACQUISITION
```

After hardening and retest:

```text
AI-03A FINAL HARDENED CONTRACT
13 TOTAL HARDENINGS
C01..C33 ACCEPTED
STRUCTURAL PASS

NO new top-level Context contract
NO Domain reopen
NO Logical reopen
NO Physical reopen
NO PostgreSQL/Alembic change
NO generic Context/Fact/Memory ontology
```

This is architecture/simulation acceptance only, not implementation PASS.

### AI-03B — Retrieval + Memory Architecture

**Status:** CANDIDATE / STRUCTURAL PASS PENDING FINAL INDEPENDENT VALIDATION

Durable candidate authority:

- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Goal: define how candidate information is found under the final AI-03A Context contract and which noncanonical information may legitimately survive.

Required retrieval coverage:

```text
Semantic Query / Projection Gateway
current-state queries
material-history queries
specific relation traversal
metadata filtering
PostgreSQL FTS
pg_trgm / fuzzy matching
semantic/vector retrieval where justified
hybrid retrieval
reranking
source reread
freshness/currentness validation
coverage-aware retrieval
permission-aware discovery/retrieval
provider-native acquisition under the same governed boundary
multi-stage / iterative / JIT retrieval
document hierarchy / chunking where justified
large-corpus retrieval
long-context vs retrieval strategy
retrieval evaluation
```

Required memory coverage:

```text
canonical application memory — already owned by Domain/PostgreSQL
Interaction Session continuity
Run / working memory
compaction/checkpoint state
derived / adaptive memory
operational / experience memory
candidate hypotheses
provider thread / provider memory / prompt cache
retrieval representations / embeddings / indexes
execution evidence — explicitly not user memory
```

Required lifecycle decisions:

```text
admission
purpose
scope
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
source suppression
use suppression
inference disposition
anti-resurrection
provider/cache invalidation
index invalidation
```

Principle:

> **Memory survival must be earned. Canonical application memory already belongs to Domain/PostgreSQL and must not be recreated as generic AI memory.**

The candidate additionally fixes:

```text
RetrievalPlan / RetrievalCandidate separation
APPROXIMATE != COMPLETE
candidate count != coverage proof
permission-safe retrieval universe
rank/similarity/rerank != Source Standing
memory recall = governed acquisition
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
rejected inference must not silently resurrect
memory derivative != independent evidence of its ancestry
PAST EXPERIENCE != POLICY
RESTORED BYTES != RESTORED ELIGIBILITY
```

AI-03B must preserve every accepted AI-03A invariant, including Reality Scope, Runtime Interpretation Frame where material, coverage semantics, model-discovered scope ceiling, governed provider-native acquisition, Context continuity compartments, child-context minimisation, instruction provenance, Source Standing separation, derived-sensitivity closure, non-monotonic readiness, consumer-delivery/transform integrity, anti-resurrection, ConsumerContext/ContextManifest distinction and ContextManifest/BasisManifest separation.

The current candidate has completed DANTE-first design, targeted modern challenger research, reconciliation and a first heavy kill-test. It is not CLOSED until a fresh independent readback/destructive validation treats the candidate PASS as untrusted and fails to find an unresolved structural contradiction.

### AI-03C — Destructive Validation + Materialization Blueprint

Goal: attack the completed Context/Retrieval/Memory architecture and only then decide what deserves physical persistence.

Required pressure includes:

```text
15+ years history
millions of structured rows
very large document corpora
same-name / ambiguous referents
multi-actor private context
Consent / Visibility revocation during Run
source correction / retirement / deletion
backup restore and anti-resurrection
stale summary
stale embedding
provider persistent memory
cache after authorization change
prompt/retrieval poisoning
malicious documents
cross-query inference
provider-native retrieval/tool bypass attempts
derived sensitivity amplification
relative time/location/DST ambiguity
consumer/provider opaque compaction or truncation
context-window exhaustion
provider/model failover
offline delayed state
multimodal/voice/files
long-running Run resume
future much-larger context windows
future much-stronger models
```

Materialization blueprint must classify every proposed state as one of:

```text
already canonical in existing Domain/PostgreSQL
transient runtime state
recomputable derived state
bounded durable derived state
provider-owned optimization state
retrieval index / representation
execution/audit evidence
object bytes / artifact storage
NOT JUSTIFIED TO STORE
```

Only after this classification may AI-03C recommend:

```text
conversation persistence
Run/working persistence
summary persistence
embedding storage
pgvector use
FTS indexes
chunk metadata
provider-cache metadata
retention jobs
new PostgreSQL structures
```

Any structural DB change then enters the normal CP6/PostgreSQL same-change discipline. AI-03 itself does not bypass it.

---

## 7. Accepted Context architecture principles

AI-03B/AI-03C inherit these from the closed AI-03A contract.

### 7.1 Context is a purpose-bound consumer view

```text
CONTEXT != COPY OF DANTE WORLD
```

Minimum necessary is relative to the legitimate objective. Broad cross-life orchestration may require broad but staged InformationNeeds; minimisation must not amputate the North Star.

### 7.2 Context is not merely a prompt

Context may feed:

```text
model invocation
solver
verifier
capability discovery
programmatic compute
human review surface
```

Different consumers may require different projections of the same underlying basis.

### 7.3 InformationNeed owns sufficiency

Every material inclusion must be explainable through an InformationNeed, with explicit criticality, coverage, currentness/coherence, reference-resolution and interpretation requirements where material.

Required needs cannot be dropped by model preference or resource pressure.

### 7.4 Acquisition strategy is per need

DANTE has no universal RAG strategy.

Structured query, deterministic aggregate, live source read, direct long-context, hierarchical/index retrieval and bounded JIT exploration are legitimate strategy classes when justified.

### 7.5 Reality frames remain explicit

```text
CANONICAL CURRENT
!= HISTORICAL / AS-OF
!= SCENARIO A
!= SCENARIO B
!= OPEN-WORLD ASSERTION
```

No cross-frame laundering.

### 7.6 ContextManifest records exposure, not causal use

```text
ConsumerContext != ContextManifest
ContextManifest != BasisManifest
EXPOSED != USED != MATERIAL DEPENDENCY
```

The manifest is an exposure receipt and should not become a permanent duplicate prompt archive by default.

### 7.7 Retrieval is iterative and bounded

Preferred pattern:

```text
understand objective
→ required InformationNeeds
→ acquire bounded eligible context
→ reason
→ discover legitimate missing dependency
→ acquire again under current scope/policy/freshness
→ continue
```

not indiscriminate dump-at-start.

### 7.8 Structured state and unstructured context are different paths

Structured DANTE-native meaning remains accessed through application-owned semantic query/projection contracts.

Documents, notes, web results, attachments and other unstructured/open-world material use Context/Retrieval paths appropriate to their source class.

No model receives unrestricted raw SQL merely because SQL is convenient.

### 7.9 Provenance and information-flow survive transformation

Summarisation, chunking, embedding, reranking, synthesis and compaction must not launder source identity, confidentiality, canonicality or instruction authority.

```text
private source -> summary
summary remains constrained by lineage

untrusted source -> generated derivative
derivative does not inherit instruction authority
```

A derivative may also become more sensitive because of what composition/inference reveals; transformation is not automatic declassification.

### 7.10 Freshness, readiness and coherence remain explicit

```text
source version unchanged != source necessarily fresh
all fragments fresh != combined basis necessarily coherent
READY now != READY forever
```

AI-03 preserves the AI-02 `BasisManifest` relationship rather than creating a parallel dependency/freshness authority.

### 7.11 Context and disclosure remain separate

An internal reasoning context may legitimately contain information that a particular recipient must not receive.

Acquisition eligibility, consumer/provider exposure and recipient disclosure are separate checks.

Safe Result Publication / Disclosure remains the egress authority.

### 7.12 Context continuity is compartmented

```text
Interaction Session continuity
!= provider/model-visible context continuity
```

Provider thread/cache/compaction reuse requires current purpose/policy/confidentiality/consumer compatibility.

### 7.13 Child context is separately minimized

```text
WorkContract protected obligations propagate
!= parent context is copied wholesale
```

Child/delegated workers receive minimum necessary projections for their own InformationNeeds.

### 7.14 Performance is architectural

Good context architecture minimizes:

```text
unnecessary tokens
unnecessary model calls
unnecessary retrieval
unnecessary embeddings
unnecessary provider/network round trips
unnecessary persistent copies
```

Deterministic SQL/projection/aggregation should answer structured questions directly when possible. Context machinery is bypassable on legitimate fast paths.

### 7.15 Provider-native/JIT acquisition remains governed

Every mechanism that can introduce new information into reasoning participates in the current acquisition boundary.

```text
PROVIDER-NATIVE ACQUISITION != POLICY BYPASS
TECHNICAL CONNECTIVITY != PROCESSING ELIGIBILITY
```

Provider-native search/connectors/browser/subagents therefore remain bound by WorkContract, InformationNeed, purpose, source exclusions and acquisition/processing policy.

### 7.16 Acquisition authority is not mutation authority

```text
ACQUISITION AUTHORIZATION != EFFECT AUTHORIZATION
```

A retrieval operation that materially changes DANTE/provider/external state is also an effect and must satisfy the inherited AI-02 effect contracts.

### 7.17 Runtime Interpretation Frame is distinct from Reality Scope

Relative temporal/spatial/locale language may require explicit reference instant, timezone/offset, DST handling, location anchor/precision or other interpretation state.

```text
REALITY SCOPE != RUNTIME INTERPRETATION FRAME
```

A consequential unresolved interpretation can make ContextReadiness NOT_READY.

### 7.18 Assembled context is not automatically established effective exposure

Provider/Harness truncation, compaction, context editing or opaque continuation can make effective exposure differ from DANTE's assembled ConsumerContext.

```text
ASSEMBLED CONSUMER CONTEXT
!= ESTABLISHED CONSUMER EXPOSURE
```

Unknown effective exposure remains UNKNOWN and may require limitation, rebuild or a different eligible consumer/Harness.

---

## 8. Memory architecture principles

AI-03B must preserve these distinctions.

### 8.1 Canonical application memory already exists

DANTE's durable structured understanding of life is the accepted application/domain/database model. It is not recreated as a generic AI memory layer.

### 8.2 Interaction memory is not canonical truth

Conversation continuity may retain turns, references, temporary discourse bindings, attachment context or compacted session state without promoting every utterance to permanent user truth.

### 8.3 Working memory defaults to temporary

Intermediate reasoning artifacts, search results, calculations and partial work should expire unless a concrete durable purpose justifies retention.

### 8.4 Derived/adaptive memory is candidate by default

Observed patterns or AI-derived hypotheses do not become confirmed preference/fact merely because they are useful.

Derived-memory lifecycle must also preserve the AI-03A rule that a composite inference may require stronger sensitivity/use restrictions than its individual source signals.

### 8.5 Retrieval representations are not facts

Embeddings, FTS representations, summaries and indexes are derived technical structures. They inherit source lifecycle obligations.

### 8.6 Provider memory is replaceable optimization

Provider thread state, model memory and prompt cache may be useful but never become DANTE's canonical memory authority.

### 8.7 Execution evidence is not user memory

Audit/evidence needed to explain effects and runtime behavior remains separate from adaptive/personal memory semantics.

### 8.8 Operational/experience memory is bounded noncanonical knowledge

Verified reusable knowledge about a bounded provider/environment/capability/workflow may be useful, but it is not user memory, policy or permanent truth. It requires explicit source/lineage, applicability and revalidation semantics.

---

## 9. Privacy, retention and anti-resurrection

AI-03 must provide a lifecycle in which deletion/redaction/retirement propagates to every eligible derivative.

At minimum consider:

```text
source record
material history visibility
text extraction
chunk metadata
embedding
lexical index
summary
compacted session state
derived memory candidate
operational/experience memory
cache
provider thread/memory
artifact
trace/eval derivative where applicable
```

The current PostgreSQL `material_state_retirement` contract and recovery suppression model are inherited constraints, not implementation details AI-03 may ignore.

A restore of old bytes must not make a retired derivative retrieval-eligible again.

---

## 10. Security requirements

AI-03 is built under security/privacy constraints from the start.

Required properties include:

```text
policy-aware discovery/acquisition
provider-native/JIT acquisition under the same scope/policy
processing/consumer exposure re-evaluation
consumer-delivery/transformation integrity for protected requirements
DATA != INSTRUCTION
instruction provenance
source-to-sink containment
derived-sensitivity re-evaluation
model-discovered need scope ceiling
cross-user / cross-actor isolation
child/delegation minimisation
cumulative inference protection
purpose limitation
explicit source/use exclusions
Runtime Interpretation Frame where material
provider eligibility / minimisation
surface-aware disclosure
cache re-authorization
memory poisoning resistance
retrieval poisoning resistance
trace/eval minimisation
```

A later AI-04 security assurance pass attacks the concrete production design; it does not introduce these requirements for the first time.

---

## 11. Physical/materialization discipline

Current physical truth:

```text
PostgreSQL 18.6
Alembic 20260830_09
69 tables
5 views
15 routines
76 triggers
97 indexes
69 FKs
123 CHECKs
```

Current selected retrieval capabilities include PostgreSQL native FTS, `pg_trgm`, `unaccent` and `pgvector`, but selection/availability does not mean activation is automatically justified.

Forbidden shortcut:

```text
AI-03B begins
→ therefore create memory tables / embeddings / vector index
```

Required sequence remains:

```text
semantic need
→ architecture contract
→ retrieval/memory lifecycle
→ destructive validation
→ persistence classification
→ smallest justified physical design
→ normal reviewed forward migration if needed
```

No structural DB change is authorized by this document.

---

## 12. Non-goals

AI-03 does not currently select:

```text
OpenAI / Anthropic / Gemini / Qwen
specific model
specific embedding model
specific vector dimension
specialist vector database
Mem0 / Zep / Graphiti or comparable framework
Redis
conversation table
memory table
Run table
summary table
chunk table
embedding table
provider thread schema
final prompt-cache implementation
final SDK/gateway
final sandbox/runtime
```

Any later selection must be justified by completed architecture and evidence.

---

## 13. AI-03A closure record

AI-03A is closed at the structural architecture level.

Durable proof/rationale:

- `docs/architecture/dante-ai-03a-full-context-architecture.md`

Closure result:

```text
INITIAL CANDIDATE                 FAIL / HARDENING REQUIRED
INITIAL HARDENINGS               9
FINAL INDEPENDENT REVALIDATION   4 additional hardenings
HARDENINGS TOTAL                 13
FINAL HARDENED CONTRACT          STRUCTURAL PASS
C01..C33                         ACCEPTED AI-03A INVARIANTS
new top-level Context contract   NO
Domain reopen                    NO
Logical reopen                   NO
Physical reopen                  NO
PostgreSQL/Alembic change        NO
runtime/provider implementation  NOT CLAIMED
```

AI-03A is reopened only if later Retrieval/Memory/materialization evidence demonstrates a real contradiction that cannot be resolved inside the smaller downstream boundary.

Do not restart generic AI-03A mega-testing merely to search for hypothetical gaps.

---

## 14. AI-03 overall closure gate

AI-03 closes only after A+B+C prove:

```text
Context semantics coherent
Retrieval semantics coherent
Memory classes explicit
canonical vs derived boundary preserved
privacy / Authority / Visibility preserved
source lifecycle / anti-resurrection preserved
performance strategy bounded
provider state replaceable
no unjustified persistence
materialization blueprint complete
no unresolved structural contradiction
```

Only then may the project move to AI-04 Productionization Architecture.

---

## 15. Immediate next action

Current next action:

```text
AI-03B — FINAL INDEPENDENT RETRIEVAL + MEMORY VALIDATION
```

Use the materialized candidate:

- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Then independently reconstruct the required Retrieval/Memory obligations from Product/Domain/Logical/PostgreSQL/Recovery/AI-02/AI-03A and attack the candidate without treating its first structural PASS as proof.

Required pressure includes at least:

```text
permission-filtered approximate retrieval / recall collapse
complete-required vs ANN/hybrid Top-K
source lifecycle + stale derivatives
multi-source vs same-lineage fake corroboration
inference resurrection after user correction
self-confirming memory loops
poisoned operational/experience memory
cross-purpose / cross-actor memory reuse
provider persistent state after revocation
long-running Run resume/currentness
large history / large document corpora / context pressure
correct non-recall / non-application
Recovery / anti-resurrection
```

If a real gap appears, harden the smallest AI-03B boundary and retest. If the candidate survives without unresolved structural contradiction, close AI-03B and only then enter AI-03C.

Do not select or activate physical retrieval/memory technologies before AI-03C classification/materialization evidence.