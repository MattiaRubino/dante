# DANTE AI-03B — Retrieval + Memory Architecture

- **Status:** CANDIDATE / STRUCTURAL PASS PENDING FINAL INDEPENDENT VALIDATION
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **PRE-SCOPE:** `cd98a1e76864aa91f098e7391c91cce48cefa20a`
- **Phase:** AI-03B — Retrieval + Memory Architecture
- **Upstream context baseline:** AI-03A / CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE / C01..C33
- **Implementation claim:** NONE
- **Database evolution:** NONE
- **Alembic evolution:** NONE
- **Provider/model selection:** NONE
- **Physical retrieval technology selection:** NONE
- **Next gate:** final independent AI-03B readback + destructive validation before closure

---

## 1. Purpose

AI-03B defines how DANTE finds candidate information required by an accepted AI-03A `InformationNeed`, how candidate material becomes eligible Context, and which noncanonical information/state — if any — earns the right to survive beyond the immediate step or Run.

The governing questions are:

> **How does DANTE retrieve the least-complex set of candidates that can satisfy the declared coverage/currentness/security guarantees of an InformationNeed without treating ranking as truth?**

and:

> **Which noncanonical information may survive, under which explicit class, purpose, source, sensitivity, correction, forgetting, suppression and anti-resurrection lifecycle?**

AI-03B is not a universal RAG design, vector-database choice, generic memory ontology, conversation-schema proposal, provider-memory decision or database migration.

The architecture starts from the closed DANTE stack:

```text
Product / North Star
→ Domain
→ Whole Logical / WL-H01..WL-H12
→ Physical
→ PostgreSQL / CP6 / Recovery
→ AI-02.1 runtime
→ AI-03A Context C01..C33
→ AI-03B Retrieval + Memory
```

Repository truth outranks research/framework convenience.

---

## 2. Core position

```text
RETRIEVAL
= governed discovery + validation of candidate material
  required by an InformationNeed

MEMORY
= noncanonical information/state that survives beyond
  the immediate step or Run under an explicit lifecycle

CANONICAL APPLICATION MEMORY
= already owned by accepted Domain/PostgreSQL
```

Therefore:

```text
RETRIEVAL != RAG
MEMORY != VECTOR DATABASE
MEMORY != CHAT HISTORY
MEMORY != PROVIDER THREAD
MEMORY != GENERIC FACT STORE
VECTOR RESULT != TRUTH
RANK != AUTHORITY
```

DANTE must not recreate canonical application meaning inside a generic AI memory layer.

---

## 3. Inherited non-negotiable boundaries

AI-03B inherits without reinterpretation:

```text
PostgreSQL = sole canonical persistence/material-history authority

CANONICAL STATE != DERIVED STATE
CANONICAL STATE != PROVIDER STATE
CANONICAL STATE != RETRIEVAL INDEX
CANONICAL STATE != CONVERSATION MEMORY

Person != Account != Principal != Actor
Authority != AuthZ
Consent != Authority
Visibility != Authority

AI inference != confirmed fact
search rank != truth
vector similarity != truth
summary != source
embedding != source
cache != source

absence / unknown != false
current != historical
correction != silent overwrite

Scenario != canonical current
Interaction Session != Run != Worker
ContextManifest != BasisManifest
ConsumerContext != ContextManifest

DATA != INSTRUCTION
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION

retired/deleted/redacted source
must not regain eligibility through
index / chunk / summary / embedding / cache /
provider state / derived memory / backup restore
```

AI-03A `C01..C33` remains binding, including governed acquisition, derived-sensitivity closure, Runtime Interpretation Frame and consumer-delivery/transformation integrity.

---

# PART I — RETRIEVAL ARCHITECTURE

## 4. Retrieval flow

```text
AI-03A INFORMATION NEED
        │
        ▼
RETRIEVAL PLAN
        │
        ├ eligible search universe
        ├ required retrieval guarantee
        ├ acceptable source semantics
        ├ Reality Scope
        ├ Runtime Interpretation Frame where material
        ├ reference/target requirement
        ├ currentness/coherence requirement
        ├ explicit exclusions
        ├ consequence
        └ latency/cost/resource budget
        │
        ▼
ROUTE SELECTION
        │
        ├ structured / exact
        ├ material history
        ├ typed relation traversal
        ├ lexical
        ├ fuzzy
        ├ semantic / ANN
        ├ hybrid
        ├ hierarchical document
        ├ direct long-context
        ├ Interaction / Run
        ├ federated/provider
        └ open-world / bounded JIT
        │
        ▼
RETRIEVAL CANDIDATES
        │
        ▼
VALIDATION
        │
        ├ acquisition eligibility
        ├ source binding
        ├ source lifecycle
        ├ currentness
        ├ exact reference where required
        ├ sensitivity / derived sensitivity
        ├ Reality Scope
        ├ interpretation applicability
        └ contradiction
        │
        ▼
CONTEXT FRAGMENTS
        │
        ▼
AI-03A ContextReadiness
```

Only candidate material that survives validation may become an AI-03A `ContextFragment`.

---

## 5. RetrievalPlan contract

`RetrievalPlan` is the bounded execution projection of one or more accepted `InformationNeed`s. It is not a new Domain object, database owner or orchestration service requirement.

Conceptually it preserves:

```text
InformationNeed refs/revisions
WorkContract / ContextPlan binding
consumer / step
purpose
Actor / represented party / Subject where material
Reality Scope
Runtime Interpretation Frame where material
reference-resolution requirement
eligible source classes / source set
explicit source/use exclusions
required retrieval guarantee
freshness/currentness requirement
coherence requirement
representation/fidelity requirement
permitted provider/tool acquisition
resource / latency / cost budget
stopping criteria
JIT refinement ceiling
```

A RetrievalPlan may choose multiple routes when no single route satisfies the need, but cannot widen the WorkContract/policy/purpose envelope.

```text
RETRIEVAL PLANNING
MAY REFINE ACQUISITION
MUST NOT CREATE NEW PURPOSE / AUTHORITY / VISIBILITY
```

---

## 6. Retrieval guarantee semantics

AI-03B separates result count/rank from coverage proof.

Candidate guarantee classes:

```text
EXACT
= exact lookup/identity semantics for the declared target

BOUNDED_COMPLETE
= the route can establish completeness within a declared bounded universe

BEST_EFFORT
= useful discovery with no completeness claim

APPROXIMATE
= retrieval may omit relevant items by mechanism design/budget

SAMPLED
= deliberate sample; never completeness
```

Examples:

```text
bounded authoritative SQL query
→ potentially BOUNDED_COMPLETE

exact NativeRef / ScopedRecordRef / MaterialStateRef lookup
→ EXACT

lexical search
→ normally BEST_EFFORT unless a bounded source contract proves otherwise

semantic ANN Top-K
→ APPROXIMATE

hybrid Top-K + reranker
→ BEST_EFFORT / APPROXIMATE unless independently proven otherwise

open web search
→ BEST_EFFORT
```

Binding rule:

```text
APPROXIMATE RETRIEVAL
!= COMPLETE RETRIEVAL

candidate count
!= coverage proof
```

An `InformationNeed` requiring `COMPLETE_REQUIRED` / bounded completeness cannot be marked satisfied solely because an ANN/hybrid/reranker returned `K` candidates.

---

## 7. Retrieval Eligibility Envelope / search universe

The permitted candidate universe is part of retrieval semantics.

```text
RETRIEVAL ELIGIBILITY ENVELOPE
=
the source/candidate universe that this InformationNeed
may legitimately search under current purpose, identity,
representation, policy and lifecycle state.
```

Preferred conceptual order:

```text
current eligible universe
→ retrieval
→ ranking
→ candidate validation
```

not:

```text
search all private data
→ top-K
→ permission filter only at the end
```

Post-retrieval filtering can be one physical mechanism but cannot, by itself, prove permission-safe discovery where unobservable/unauthorized candidates can affect rank, count, timing, candidate exhaustion or other WL-H12 surfaces.

The exact physical method — prefilter, source-local query, partitioning, partial index, filtered ANN, oversampling, bounded exact scan or another design — remains open to AI-03C/implementation evidence.

---

## 8. Route selection

DANTE has no universal retrieval pipeline.

Primary rule:

```text
USE THE LEAST-COMPLEX ROUTE
THAT CAN SATISFY THE REQUIRED GUARANTEES.
```

### 8.1 Structured / deterministic route

Use semantic query/projection + SQL/deterministic compute when the answer is structured and the required semantics are owned by DANTE.

Example:

```text
"how much did I run in August?"
→ semantic interpretation
→ bounded structured aggregate
→ typed result
```

No vector retrieval or model-generated synthesis is required to manufacture a deterministic answer.

### 8.2 Material history

History queries must preserve owner/material-state semantics, world/effective vs recorded/learned chronology where material, retirement state and Reality Scope.

Historical retrieval never means "latest row wins".

### 8.3 Typed relation traversal

Known semantic relationships use accepted Domain/Logical relation contracts rather than generic graph edges.

`Person → Responsibility → Activity`, for example, remains a typed semantic route, not an arbitrary knowledge-graph edge.

### 8.4 Lexical / fuzzy

Useful for identifiers, titles, names, document terms, near-matches and discovery where exact structured binding is not yet available.

Lexical/fuzzy rank does not establish source standing, identity or truth.

### 8.5 Semantic / vector

Vector retrieval is candidate-discovery technology only.

```text
VECTOR
!= SOURCE
!= TRUTH
!= IDENTITY
!= FRESHNESS
!= AUTHORIZATION
!= MEMORY
```

Vector use is justified only when semantic similarity solves a concrete retrieval problem better than simpler routes.

### 8.6 Hybrid

Hybrid retrieval may combine lexical, semantic, metadata, relation or other candidate sources.

```text
candidate merge
→ lineage/source-aware dedup
→ optional rerank
→ source/currentness validation
```

Hybrid ranking cannot reconcile contradictory sources.

### 8.7 Hierarchical document retrieval

Large documents/corpora may use parent-child hierarchy, contextualized chunks, section summaries, lexical/vector indexes or other bounded derived representations.

```text
chunk != Content Artifact
summary != source
embedding != source
```

Small bounded document sets may be safer/simpler to read directly rather than pre-index.

### 8.8 Direct long-context

A large context window is a runtime resource, not an instruction to use all available tokens. Direct source/context loading is legitimate when the eligible bounded source set fits the consumer and preserves required guarantees more simply than indexed retrieval.

### 8.9 Interaction / Run retrieval

Conversation/session continuity, discourse bindings, attachments and Run working state remain explicit source classes. Transcript presence does not promote utterances into canonical user facts.

### 8.10 Federated/provider-native retrieval

Provider search/file retrieval/connectors/browser/submodels/remote tools remain inside AI-03A governed acquisition.

```text
PROVIDER-NATIVE ACQUISITION
!= ACQUISITION BYPASS
```

If DANTE cannot sufficiently constrain/account for a protected/private source path, that route is ineligible for the protected need.

### 8.11 Open-world / JIT

Web/open-world retrieval is normally best-effort and source-standing aware.

Iterative/JIT acquisition is bounded:

```text
reason
→ legitimate missing dependency?
→ create/refine bounded InformationNeed
→ acquire under same WorkContract ceiling
→ continue
```

No unbounded `while model wants more: search everything` loop.

---

## 9. RetrievalCandidate contract

A `RetrievalCandidate` is a runtime discovery object before Context inclusion.

It is not a new Domain root, canonical fact, Evidence, Observation or ContextFragment.

Conceptually it may preserve:

```text
candidate ref
InformationNeed / RetrievalPlan refs
source locator / source class
source NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef when legitimately available
retrieval representation ref/version
retrieval mechanism
rank / score / retrieval metadata
retrieved_at
Reality Scope
Runtime Interpretation Frame applicability where material
source lifecycle hint
security/purpose scope
lineage to source/derivative
currentness hint
resource cost
```

A rank/score is retrieval evidence only.

---

## 10. Candidate validation / source reread

For consequential or currentness-sensitive work:

```text
INDEX SAYS X
!= SOURCE STILL SAYS X
```

A candidate produced from an embedding, FTS representation, summary, provider index or cache may require direct source reread or current material-state validation before it becomes a `ContextFragment` / material basis.

Candidate validation can yield:

```text
ELIGIBLE_CURRENT
ELIGIBLE_HISTORICAL
ELIGIBLE_WITH_LIMITATION
STALE
CONFLICTED
SOURCE_RETIRED
SOURCE_REDACTED
POLICY_BLOCKED
NOT_CURRENTLY_VISIBLE
SOURCE_UNAVAILABLE
AMBIGUOUS_TARGET
AMBIGUOUS_INTERPRETATION
INVALID_DERIVATIVE
```

No stale index representation may override the source lifecycle.

---

## 11. Ranking, reranking and corroboration

Binding separation:

```text
LEXICAL SCORE != SOURCE STANDING
VECTOR SIMILARITY != SOURCE STANDING
RERANK SCORE != SOURCE STANDING
FREQUENCY != TRUTH
MULTIPLE CHUNKS != MULTIPLE INDEPENDENT SOURCES
```

Reranking may improve candidate order; it is not a Verifier or Reconciliation engine.

Source/lineage-aware dedup must prevent one source split into many chunks/summaries from becoming artificial corroboration.

---

## 12. Retrieval representation lifecycle

Technical retrieval representations include, where later justified:

```text
text extraction / OCR output
chunk/span metadata
lexical representation / FTS
trigram/fuzzy representation
summary / hierarchical summary
embedding
vector index
retrieval cache
provider file/index object
```

They remain derived state.

A future material representation must preserve enough to reconstruct, as applicable:

```text
source locator / owner
source revision/material basis
MaterialStateRef only where real
representation/chunk version
embedding model + version
dimension / metric / normalization where material
generated_at
security/purpose scope
source lifecycle status
rebuild/invalidation policy
```

Selection/availability of PostgreSQL FTS, pg_trgm, unaccent or pgvector does not activate any of these structures by itself.

---

# PART II — MEMORY ARCHITECTURE

## 13. Memory principle

Primary rule:

```text
MEMORY SURVIVAL MUST BE EARNED.

DEFAULT FOR NONCANONICAL STATE
= DO NOT SURVIVE.
```

Canonical application semantics already belong to accepted Domain/PostgreSQL.

AI-03B therefore separates memory classes rather than creating one universal `Memory` object.

---

## 14. Memory classes

### 14.1 Canonical Application Memory

```text
owner
= Domain / PostgreSQL
```

Examples include accepted people, goals, plans, schedules, actuals, observations, relationships, decisions and other current/historical application state where the Domain/Logical model already owns the meaning.

This is not an AI memory layer.

### 14.2 Interaction Memory

Purpose:

```text
conversation/session continuity
current discourse bindings
references such as "that one" / "the file from before"
attachment continuity
bounded topic state
```

```text
CHAT TRANSCRIPT != USER TRUTH
```

An utterance can be retained for conversational continuity without becoming a permanent user fact/preference.

### 14.3 Run / Working Memory

Includes:

```text
search candidates
partial calculations
intermediate summaries
solver state
tool results
research notes
working hypotheses
```

Default is transient.

Long-running/resumable work may justify bounded checkpointing, but:

```text
RESUMABLE RUN STATE != USER MEMORY
```

### 14.4 Compaction / Checkpoint State

Used for continuity/resource optimization.

```text
COMPACTION != SOURCE
COMPACTION != CANONICAL SUMMARY
```

Lossy compaction cannot be the sole carrier of stronger authoritative/protected semantics.

### 14.5 Adaptive / Derived User Memory

Reusable user-specific pattern/hypothesis inferred from legitimate material.

Examples may include a tentative scheduling tendency or repeated preference-like pattern, but the class is candidate by default.

```text
INFERENCE != CONFIRMED FACT
```

Durable adaptive memory must have bounded typed semantics sufficient for correction/scope/expiry/suppression. Free-form prose alone is not accepted as durable semantic authority.

### 14.6 Operational / Experience Memory

Reusable noncanonical knowledge about how a bounded environment, provider, capability or workflow behaves.

Examples:

```text
provider X requires a reread after state Y
workflow Z fails unless prerequisite Q is performed
this bounded external environment has a known operational gotcha
```

This is distinct from user memory and requires verified basis plus environment/version applicability.

```text
PAST EXPERIENCE != POLICY
MODEL SAYS SUCCESS != VERIFIED SUCCESS
```

### 14.7 Provider Memory / Thread / Prompt Cache

Provider-owned continuation/optimization state.

```text
PROVIDER MEMORY
= replaceable optimization
!= DANTE authority
!= canonical memory
```

Reuse requires current purpose/privacy/representation/authorization/Harness compatibility.

### 14.8 Retrieval Representations

Chunks, summaries, embeddings, indexes and caches are technical derivative state, not user facts.

### 14.9 Execution Evidence

Runtime/effect/audit evidence exists to reconstruct execution/governance/outcomes where required.

```text
EXECUTION EVIDENCE != USER MEMORY
```

---

## 15. Memory Survival / Admission Gate

AI-03B defines a common admission protocol, not a universal memory ontology or mandatory service.

Before noncanonical state survives, determine:

```text
which memory class?
what future legitimate purpose?
what concrete future utility?
whose information / Subject?
which Actor / represented party context?
source / lineage / basis?
independent evidence or derivative?
sensitivity / derived sensitivity?
purpose/use restrictions?
validity / temporal scope?
review / expiry / decay?
correction path?
contradiction behavior?
forgetting semantics?
source/use/inference suppression?
deletion / anti-resurrection path?
provider/environment applicability?
can it simply be recomputed?
is canonical Domain state the proper home instead?
```

Possible outcomes:

```text
DROP
retain only for current step
retain for Run
retain for Interaction Session
bounded durable-memory candidate
provider optimization allowed
propose canonical Domain/application update
```

Binding rule:

```text
MODEL REQUEST TO REMEMBER
!= MEMORY ADMISSION
```

A model/tool may propose admission; DANTE owns the gate.

---

## 16. Memory recall is governed retrieval

```text
MEMORY EXISTS
!= MEMORY MAY BE USED
```

Any memory re-entering reasoning must be acquired through the same AI-03A purpose/policy/eligibility boundary:

```text
InformationNeed
→ RetrievalPlan
→ eligible memory/source universe
→ RetrievalCandidate
→ validation
→ ContextFragment
```

Therefore:

```text
MEMORY RECALL
IS GOVERNED ACQUISITION
```

No architecture rule injects every remembered item into every prompt/session.

---

## 17. Canonical promotion boundary

If a user/model supplies information whose durable meaning belongs to an existing accepted Domain owner, the correct action is not to hide it in generic memory.

Possible flow:

```text
candidate information
→ classify semantic owner/facet
→ propose bounded canonical application update
→ ordinary governance / expected-state / effect semantics
→ accepted Domain/PostgreSQL state if authorized
```

```text
AI MEMORY
CANNOT MINT CANONICAL TRUTH BY ITSELF.
```

If no accepted owner is justified, AI-03B does not invent a generic Fact/UserMemory domain root.

---

# PART III — CORRECTION, SUPPRESSION AND ANTI-RESURRECTION

## 18. Distinct lifecycle operations

These are not synonyms:

```text
CORRECT
= this retained claim/memory meaning is wrong or superseded

FORGET
= stop retaining/reusing this memory under its lifecycle

SOURCE SUPPRESSION
= this source is ineligible

USE SUPPRESSION
= source may exist but is ineligible for a bounded purpose/use

INFERENCE DISPOSITION
= a derived semantic hypothesis has been rejected/corrected
  and must not silently be recreated from materially equivalent basis
```

Forgetting an AI memory does not rewrite truthful canonical history.

---

## 19. Inference-resurrection protection

Failure case:

```text
15 late-night Sessions
→ derived adaptive hypothesis
  "prefers working late"

user rejects hypothesis
→ memory deleted

same history remains truthful
→ future model derives equivalent hypothesis again
```

Deleting the derived bytes is insufficient.

AI-03B therefore requires semantic disposition for durable adaptive-memory families:

```text
REJECTED / CORRECTED DERIVED MEANING
MUST NOT SILENTLY RESURRECT
FROM MATERIALLY EQUIVALENT SURVIVING BASIS.
```

Disposition applies to bounded typed meaning, not exact text strings; paraphrase does not bypass correction.

This is not a universal predicate graph. A durable adaptive-memory family must simply be semantically typed enough to be corrected/suppressed reliably.

---

## 20. Self-confirming memory / ancestry protection

Failure case:

```text
source S
→ inference M1
→ future reasoning sees M1
→ produces M2
→ M2 appears to corroborate M1
```

Binding rule:

```text
DERIVATIVE
MUST NOT BECOME
INDEPENDENT CORROBORATION
OF ITS OWN ANCESTRY.
```

Multiple derivatives sharing materially the same lineage do not count as independent Evidence simply because they were produced at different times/models.

Lineage/dedup semantics must preserve the distinction.

---

## 21. Poisoned operational-experience protection

Operational/Experience Memory has a high-risk failure mode: untrusted or model-generated content can look like successful prior experience and later act as a persistent behavioral template.

Admission therefore requires adequate basis, such as where appropriate:

```text
verified execution outcome
provider receipt / independent reread
Verifier result
repeated independently verified execution
trusted operational specification
```

Insufficient by itself:

```text
model self-report
untrusted webpage statement
malicious document/tool output
assistant-generated "success" summary
```

And:

```text
EXPERIENCE != INSTRUCTION AUTHORITY
EXPERIENCE != POLICY
```

Operational memories require bounded environment/provider/version applicability and revalidation when those conditions change.

---

## 22. Source lifecycle / recovery inheritance

Retrieval and memory derivatives inherit source lifecycle.

```text
SOURCE RETIRED / REDACTED / DELETED / SUPPRESSED
        ↓
all eligible derivative paths are re-evaluated
        ↓
embedding / summary / chunk / cache /
provider state / adaptive memory /
retrieval representation
cannot remain eligible merely because bytes survive
```

Recovery rule:

```text
RESTORED BYTES
!= RESTORED ELIGIBILITY
```

Old backup/index/provider bytes must pass current source/suppression/lifecycle reconciliation before serving.

This consumes the existing PostgreSQL Recovery / `material_state_retirement` anti-resurrection contract rather than creating a second authority.

---

# PART IV — MULTI-ACTOR, PROVIDER AND CURRENTNESS

## 23. Multi-actor memory / retrieval

No memory/retrieval scope collapses to generic `user_id + text`.

Where material, preserve independently:

```text
Subject / target
source speaker/author
actual Actor
represented party
Principal/security context
purpose
Authority / Consent / Visibility basis
recipient/consumer
```

A shared fact can coexist with private personal overlays, notes, constraints and histories without becoming shared wholesale.

Memory retained in one representation/purpose context is not automatically reusable in another.

---

## 24. Provider state lifecycle

Provider thread/cache/compaction/native memory may improve continuity, latency or cost but remains discardable.

Reuse requires current compatibility with at least:

```text
WorkContract / purpose
privacy/confidentiality compartment
Actor / represented party context
current authorization/Consent/Visibility as applicable
consumer/provider eligibility
HarnessProfile / continuation semantics
known transformation/compaction limitations
```

If opaque provider state cannot be established compatible:

```text
DO NOT REUSE
→ reconstruct DANTE-controlled context
```

Provider failover must not require provider-owned memory as canonical state.

---

## 25. Currentness is non-monotonic

A previously valid retrieval/memory candidate can become ineligible because of:

```text
source correction
new contradiction
Visibility/Consent/AuthZ change
purpose change
represented-party change
source retirement/redaction
provider/environment version change
freshness expiry
Work Supersession
```

`VALID BEFORE != VALID NOW`.

Long-running Run resume therefore re-evaluates currentness/eligibility before consequential reuse.

---

# PART V — RESEARCH RECONCILIATION

## 26. Targeted external challenger evidence

AI-03B was challenged against current retrieval/memory/provider patterns after the internal DANTE-first candidate was constructed. Research is challenger evidence only; it is not semantic authority.

Material findings incorporated:

```text
pgvector 0.8.x
→ approximate ANN + filtering/iterative-scan behavior reinforces
  APPROXIMATE != COMPLETE and explicit eligible search-universe proof

long-context vs retrieval literature
→ no universal winner; route selection remains per InformationNeed

hybrid/contextual/hierarchical retrieval + reranking
→ useful candidate strategies, not truth/reconciliation mechanisms

LongMemEval / LongMemEval-V2 / LoCoMo-Plus
→ memory quality includes temporal update, abstention,
  implicit-constraint application and correct non-application

MemoryGraft-style poisoning research
→ persistent operational/experience memory needs verified admission basis

provider-native continuity/tool/context mechanisms
→ provider thread/cache/compaction/search remain governed,
  replaceable and noncanonical

Mem0 / Zep / Graphiti / Letta / related frameworks
→ useful implementation patterns exist, but generic fact/memory/graph
  ontologies are rejected where they would duplicate DANTE semantics
```

No framework/provider/store is selected by this evidence.

---

# PART VI — EVALUATION

## 27. Retrieval evaluation

AI-03B cannot be validated solely by final-answer quality.

Required evaluation families include:

```text
coverage satisfaction
bounded recall / exactness where applicable
precision / relevance
reference-binding accuracy
source-binding accuracy
stale-candidate rate
source-reread/currentness failure
policy/discovery leakage
cross-actor leakage
unsupported-negative rate
contradiction preservation
retrieval-route correctness
latency p50/p95
cost / provider calls
tokens per satisfied InformationNeed
JIT rounds/depth
rerank improvement/regression
```

A good-looking answer cannot hide retrieval leakage or missing required context.

---

## 28. Memory evaluation

Required families include:

```text
correct memory recall
correct memory non-recall
correct constraint application
correct constraint non-application
stale-memory reuse
false durable inference
false canonical promotion
correction propagation
forgetting propagation
source/use suppression propagation
inference resurrection
self-corroboration / ancestry inflation
poisoned-experience admission
cross-purpose leakage
cross-actor leakage
provider failover continuity
compaction drift
anti-resurrection failure
```

`correct non-application` is first-class: retrieving/applying a stale or wrongly scoped memory is a failure even if the remembered content is factually related.

---

# PART VII — CANDIDATE INVARIANTS

## 29. AI-03B candidate invariants B01–B30

```text
B01  RETRIEVAL != TRUTH.

B02  RetrievalCandidate != ContextFragment.

B03  Retrieval guarantee must match InformationNeed coverage.

B04  APPROXIMATE != COMPLETE.

B05  Candidate count != coverage proof.

B06  Eligibility defines the permitted search universe;
     post-filtering alone is not a universal permission proof.

B07  Rank / similarity / rerank != Source Standing.

B08  Multiple representations of one lineage
     != independent corroboration.

B09  Index / cache / embedding != source.

B10  Consequential derived retrieval may require
     source reread / current-state validation.

B11  Memory survival defaults to NO.

B12  MEMORY EXISTS != MEMORY MAY BE RECALLED.

B13  Memory recall is governed acquisition under AI-03A.

B14  MODEL REQUEST TO REMEMBER != MEMORY ADMISSION.

B15  Canonical application semantics belong to Domain/PostgreSQL,
     not generic AI memory.

B16  Durable adaptive memory must have bounded typed semantics;
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

B30  Correct non-recall / non-application
     is part of memory quality.
```

These remain candidate invariants until final independent AI-03B validation closes the phase.

---

# PART VIII — CANDIDATE DESTRUCTIVE VALIDATION

## 30. First candidate kill-test

The reconciled candidate was attacked after internal design + targeted external challenge.

Representative compound cases:

```text
ANN used for COMPLETE_REQUIRED
permission filter applied only after ANN
vector returns zero
100 chunks from one source
stale embedding after source correction
old embedding restored from backup
rejected adaptive inference recreated from surviving history
same rejected inference paraphrased
self-confirming memory loop
poisoned fake-success operational memory
provider behavior changes after experience retention
model says "remember this"
malicious PDF says "remember this secret"
old chat memory enters new purpose
same Interaction Session switches represented party
caregiver private context enters shared output
provider thread reused after revocation
long Run resumes after days
retrieval cache survives Visibility change
direct long-context vs indexed retrieval
RAG used where exact SQL was required
operational experience treated as instruction
AI memory forgotten while canonical record remains
old user statement conflicts with newer canonical state
15-year history / millions of rows
very large conceptual history
source-derived duplicate memories
source retirement during active Run
```

Candidate response:

```text
ANN for completeness                     route rejected / architecture holds
post-filter-only permission proof         rejected / eligibility envelope holds
zero vector results                       no false absence claim
source chunk multiplicity                 no fake corroboration
stale derivative                          source/currentness validation required
backup resurrection                       current lifecycle suppresses eligibility
inference resurrection                    Inference Disposition required
paraphrase resurrection                   typed adaptive semantics required
self-confirming memory                    ancestry rule blocks fake evidence
poisoned experience                       verified admission basis required
provider/environment drift                applicability + revalidation required
model memory request                      proposal only
malicious source memory request           DATA / no admission authority
cross-purpose chat memory                 governed recall blocks reuse
represented-party switch                  eligibility re-evaluation
private→shared disclosure                 AI-03A disclosure separation preserved
provider revocation                       provider-memory reuse blocked
Run resume                                currentness revalidation
Visibility change                         cache/retrieval reauthorization
long-context vs RAG                       both supported; per-need route
exact structured need                     deterministic route preserved
experience-as-instruction                 rejected
forget vs canonical state                 semantic separation preserved
old vs new state                          contradiction/reconciliation preserved
large history                             bounded query/aggregate/JIT strategy
large context                             hierarchy/JIT; no dump-all requirement
derivative duplicates                     lineage/dedup
retirement mid-Run                        non-monotonic eligibility
```

First result:

```text
AI-03B RECONCILED CANDIDATE
STRUCTURAL PASS CANDIDATE
```

This is not yet final closure. A fresh independent readback/kill-test must attempt to find contradictions without treating this candidate PASS as evidence.

---

## 31. Structural impact result

Current candidate requires none of:

```text
new Domain owner
Logical reopen
Physical reopen
PostgreSQL/Alembic change
new generic Memory root
new generic Fact ontology
new knowledge graph
new vector database
Redis
memory framework
provider/model selection
new microservice per architecture noun
```

The architecture can begin as contracts/modules inside the existing application/runtime boundary. Extraction requires measured operational evidence later.

---

# PART IX — EXPLICIT DEFERRALS

## 32. Physical/materialization decisions deferred to AI-03C

AI-03B does not authorize:

```text
conversation table
Run/working table
memory table
adaptive-memory table
operational-memory table
summary/chunk table
embedding table
embedding model / dimensions
pgvector activation
HNSW / IVFFlat parameters
new FTS indexes
retrieval cache store
Redis
specialist vector DB
provider thread schema
retention jobs
exact derivative invalidation mechanism
```

AI-03C first classifies every candidate state as:

```text
already canonical in Domain/PostgreSQL
transient runtime
recomputable derived
bounded durable derived
provider-owned optimization
retrieval representation/index
execution/audit evidence
object bytes/artifact storage
NOT JUSTIFIED TO STORE
```

Only then may physical change be proposed under normal CP6/Alembic same-change discipline.

---

## 33. Provider/framework decisions remain open

No selection is made for:

```text
OpenAI / Anthropic / Gemini / Qwen
specific foundation/small/local model
embedding model
Mem0 / Zep / Graphiti / Letta
LangGraph/LangMem
LlamaIndex/Haystack
vector DB
Redis
model gateway/router
SDK
MCP/A2A
sandbox/browser implementation
```

Research technique != DANTE decision.

---

# PART X — CLOSURE GATE

## 34. AI-03B final closure requirements

AI-03B may be closed only if a fresh independent validation can establish:

```text
RetrievalPlan semantics coherent
RetrievalCandidate boundary coherent
coverage guarantees coherent
permission-safe search-universe rule coherent
structured/history/document/open-world routes coherent
ranking/reconciliation separation preserved
source-reread/currentness lifecycle coherent
memory classes explicit and noncollapsed
Memory Survival Gate coherent
canonical promotion boundary preserved
correction/forgetting/suppression distinct
inference resurrection contained
self-corroboration contained
operational-memory poisoning contained
provider memory replaceable
multi-actor scope preserved
source retirement/recovery anti-resurrection preserved
evaluation directly tests retrieval/memory quality
no new semantic escape hatch
no unresolved structural contradiction
```

If a real contradiction appears, reopen the smallest affected AI-03B boundary. Do not reopen Domain/Logical/Physical/AI-03A unless the contradiction genuinely cannot be resolved downstream.

---

## 35. Current verdict / next action

```text
AI-03B
RETRIEVAL + MEMORY ARCHITECTURE

INTERNAL DANTE-FIRST DESIGN          COMPLETE
TARGETED MODERN CHALLENGER RESEARCH COMPLETE
RECONCILIATION                      COMPLETE
FIRST HEAVY KILL-TEST               PASS CANDIDATE
B01..B30                            CANDIDATE

STATUS
CANDIDATE / STRUCTURAL PASS
PENDING FINAL INDEPENDENT VALIDATION
```

Next action:

```text
fresh readback of repository authority
→ independent AI-03B reverse-engineering / destructive validation
→ harden only real gaps
→ close AI-03B if it still holds
→ then AI-03C whole Context/Retrieval/Memory destructive validation
   + materialization blueprint
```

No implementation, database change or physical retrieval activation is authorized by this document.
