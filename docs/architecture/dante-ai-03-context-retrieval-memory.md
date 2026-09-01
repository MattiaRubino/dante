# DANTE AI-03 — Context / Retrieval / Memory Architecture

- **Status:** ACTIVE / BRANCH-LOCAL ARCHITECTURE WORKSTREAM
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Upstream structural baseline:** AI-02.1 v0.5 / STRUCTURALLY ACCEPTED
- **Implementation:** NOT STARTED by this document
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT
- **Provider/model selection:** OPEN
- **Current macro-phase:** AI-03A — FULL CONTEXT ARCHITECTURE

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

AI-03 must keep three responsibilities separate:

```text
CONTEXT
= the purpose-bound runtime view available to a specific reasoning/execution step

RETRIEVAL
= the process that discovers and validates candidate material for context

MEMORY
= information/state that survives beyond the immediate step or Run under an explicit lifecycle
```

A single item may participate in more than one responsibility over time, but the responsibilities are not synonyms.

---

## 6. AI-03 roadmap

AI-03 is intentionally divided into only three large architecture passes.

### AI-03A — Full Context Architecture

Goal: define the entire lifecycle from work meaning to the exact information presented to each reasoning invocation.

Required coverage:

```text
WorkContract -> information needs
source discovery
structured DANTE-native context
material-history context
conversation/session context
working/run context
artifact/document context
external/open-world context
provider/external state
candidate/derived context
multi-actor context

ContextFragment
ContextManifest
provenance
source identity
source authority
information class
confidentiality
integrity / trust
instruction authority
processing eligibility
purpose
recipient/surface relevance where applicable
freshness / temporal validity
MaterialState binding
BasisManifest relationship
coherence
contradiction
uncertainty
relevance
redundancy / deduplication
token / latency / cost / resource budget
provider/model rendering
context caching
iterative acquisition
compaction
context-window pressure
failure / degradation / abstention
```

AI-03A must answer precisely:

```text
what enters context?
why?
from where?
under whose Authority / processing basis?
for which purpose?
with what provenance and trust?
for how long is it valid?
what makes it stale?
what happens if it changes during the Run?
what exactly did the model/tool/solver receive?
what did not enter and why?
```

AI-03A does not choose durable memory tables, vector-store products or embedding models.

### AI-03B — Retrieval + Memory Architecture

Goal: define how candidate information is found and which noncanonical information may legitimately survive.

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
freshness validation
permission-aware retrieval
multi-stage / iterative retrieval
document hierarchy / chunking where justified
large-corpus retrieval
retrieval evaluation
```

Required memory coverage:

```text
canonical application memory — already owned by Domain/PostgreSQL
Interaction Session continuity
Run / working memory
derived / adaptive memory
candidate hypotheses
summaries / compaction state
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
anti-resurrection
provider/cache invalidation
index invalidation
```

Principle:

> **Memory survival must be earned.**

AI-03B must reject "store every useful-looking AI observation" as a default.

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

## 7. Context architecture principles

The following principles are already accepted starting constraints for AI-03A.

### 7.1 Context is a purpose-bound view

```text
CONTEXT != COPY OF DANTE WORLD
```

Context must be sufficient for the objective without indiscriminate over-collection.

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

### 7.3 ContextManifest records actual exposure

The architecture must be able to explain what a consumer actually received, not merely what DANTE could theoretically retrieve.

### 7.4 Retrieval is iterative

Preferred default:

```text
understand objective
→ identify information need
→ retrieve bounded context
→ reason
→ discover missing dependency
→ retrieve again under current policy/freshness
→ continue
```

not:

```text
dump everything at turn start
```

### 7.5 Structured state and unstructured context are different paths

Structured DANTE-native meaning remains accessed through application-owned semantic query/projection contracts.

Documents, notes, web results, attachments and other unstructured/open-world material use Context/ Retrieval paths appropriate to their source class.

No model receives unrestricted raw SQL merely because SQL is convenient.

### 7.6 Provenance and information-flow survive transformation

Summarisation, chunking, embedding, reranking, synthesis and compaction must not launder source identity, confidentiality or integrity constraints.

```text
private source -> summary
summary remains constrained by private source lineage

untrusted source -> generated derivative
derivative does not inherit instruction authority
```

### 7.7 Freshness and coherence are explicit

```text
source version unchanged != source necessarily fresh
all fragments fresh != combined basis necessarily coherent
```

AI-03 must preserve the AI-02 `BasisManifest` relationship rather than creating a parallel freshness model.

### 7.8 Context and disclosure remain separate

An internal reasoning context may legitimately contain information that a particular recipient must not receive.

Safe Result Publication / Disclosure remains the egress authority.

### 7.9 Performance is architectural

Good context architecture minimizes:

```text
unnecessary tokens
unnecessary model calls
unnecessary retrieval
unnecessary embeddings
unnecessary network/provider round trips
unnecessary persistent copies
```

Deterministic SQL/projection/aggregation should answer structured questions directly when possible.

---

## 8. Memory architecture principles

AI-03B must preserve these starting distinctions.

### 8.1 Canonical application memory already exists

DANTE's durable structured understanding of life is the accepted application/domain/database model. It is not recreated as a generic AI memory layer.

### 8.2 Interaction memory is not canonical truth

Conversation continuity may retain turns, references, temporary discourse bindings, attachment context or compacted session state without promoting every utterance to permanent user truth.

### 8.3 Working memory defaults to temporary

Intermediate reasoning artifacts, search results, calculations and partial work should expire unless a concrete durable purpose justifies retention.

### 8.4 Derived/adaptive memory is candidate by default

Observed patterns or AI-derived hypotheses do not become confirmed preference/fact merely because they are useful.

### 8.5 Retrieval representations are not facts

Embeddings, FTS representations, summaries and indexes are derived technical structures. They inherit source lifecycle obligations.

### 8.6 Provider memory is replaceable optimization

Provider thread state, model memory and prompt cache may be useful but never become DANTE's canonical memory authority.

### 8.7 Execution evidence is not user memory

Audit/evidence needed to explain effects and runtime behavior remains separate from adaptive/personal memory semantics.

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
processing-policy filtering before model exposure
DATA != INSTRUCTION
source-to-sink containment
instruction-authority classification
cross-user / cross-actor isolation
cumulative inference protection
purpose limitation
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
AI-03 begins
→ therefore create memory tables / embeddings / vector index
```

Required sequence:

```text
semantic need
→ architecture contract
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

Any later selection must be justified by the completed architecture and evidence.

---

## 13. AI-03A acceptance gate

AI-03A may close only when the architecture can explain end-to-end:

```text
request / WorkContract
→ information needs
→ candidate sources
→ current processing eligibility
→ source/provenance/trust classification
→ freshness / MaterialState / Basis validation
→ contradiction/coherence handling
→ relevance + packing under resource budget
→ provider/consumer-specific representation
→ exact ContextManifest
→ iterative acquisition
→ invalidation / supersession / revocation response
```

and when representative simple, historical, multi-actor, sensitive, document-heavy, open-world and long-running scenarios do not require a generic memory/fact ontology or Domain/Logical reopen.

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
AI-03A — FULL CONTEXT ARCHITECTURE
```

Start by reconstructing constraints from:

```text
North Star
→ Domain
→ Whole Logical / WL-H01..WL-H12
→ Physical
→ CP1–CP6 / Persistence Constitution
→ current Alembic/PostgreSQL/Recovery truth
→ AI-00
→ AI-02.1 v0.5
→ production-engineering research
```

Then design the Context system end-to-end in one large architecture pass before any materialization decision.
