# DANTE AI-03 — Context / Retrieval / Memory Architecture

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / BRANCH-LOCAL ARCHITECTURE WORKSTREAM
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Closed:** 2026-09-02
- **Upstream structural baseline:** AI-02.1 v0.5 / STRUCTURALLY ACCEPTED
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **Implementation:** NOT STARTED by this document
- **Database evolution:** NONE AUTHORIZED BY AI-03
- **Provider/model selection:** OPEN
- **Next macro-phase:** AI-04 — PRODUCTIONIZATION ARCHITECTURE

---

## 1. Purpose

AI-03 defines how DANTE obtains, scopes, validates, composes, retrieves, retains, retires and physically materializes information used by intelligence without creating a second reality beside the accepted Product/Domain/Logical/Physical/PostgreSQL system.

Core separation:

```text
CONTEXT
= purpose-bound runtime view for one consumer/work step

RETRIEVAL
= governed discovery + validation of candidate material

MEMORY
= noncanonical state that may survive beyond the immediate step/Run
  under an explicit lifecycle

MATERIALIZATION
= the later physical decision about whether any accepted state
  deserves storage/index/runtime survival at all
```

Canonical application meaning remains owned by accepted Domain/PostgreSQL.

Repository truth outranks conversation memory and provider/framework assumptions.

---

## 2. Authoritative source corpus

Read AI-03 against:

### Product / North Star

- `docs/product/product-identity-and-north-star.md`
- `docs/product/v1-data-history-and-privacy.md`
- `docs/product/v1-user-context-and-safety.md`
- `docs/product/v1-adaptive-intelligence-and-future-social.md`
- `docs/product/v1-learning-context-and-ai-boundary.md`
- relevant V1 product contracts and cross-domain/multi-actor simulations

### Semantic authority

- `docs/domain/README.md`
- accepted Domain concept specifications
- `docs/logical-model/README.md`
- `docs/logical-model/whole-logical-model-v1.md`
- WL-H01..WL-H12

### Physical/persistence authority

- `docs/physical-model/README.md`
- `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- current Alembic / SQLAlchemy / real PostgreSQL truth
- `docs/operations/postgres-recovery-runbook.md`
- Recovery / material-state-retirement / anti-resurrection authority

### Intelligence authority

- `docs/architecture/dante-ai-foundation.md`
- `docs/architecture/ai-production-engineering-state-of-the-art-2026.md`
- `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`
- `docs/architecture/dante-ai-03a-full-context-architecture.md`
- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`
- `docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`
- `docs/architecture/system-overview.md`

---

## 3. Inherited non-negotiable invariants

AI-03 preserves:

```text
DANTE != model
DANTE != provider
DANTE != chat transcript

PostgreSQL = sole canonical persistence/material-history authority
CANONICAL STATE != DERIVED STATE
CANONICAL STATE != PROVIDER STATE
CANONICAL STATE != RETRIEVAL INDEX
CANONICAL STATE != MODEL MEMORY

Person != Account != Principal != Actor
Authority != AuthZ
Consent != Authority
Visibility != Authority
Context access != disclosure permission

AI inference != confirmed fact
AI confidence != Confirmation
search rank/vector similarity/rerank != truth
summary/chunk/embedding/cache != source

NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
MaterialStateRef != provider revision / ETag / MVCC / LSN / hash

absence / unknown != false
current != historical
correction != silent overwrite

Interaction Session != Run != Worker
Scenario != canonical current
WorkContract != transcript
ContextManifest != BasisManifest

MODEL OUTPUT != PUBLISHABLE OUTPUT
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
DATA != INSTRUCTION

retired/deleted/redacted/suppressed information
must not silently re-enter through
derived memory / cache / summary / embedding / provider state / restore
```

AI-03A contributes C01..C33.
AI-03B contributes B01..B35.
AI-03C contributes MAT-01..MAT-15.

---

## 4. AI-03A — Full Context Architecture

**Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE.

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

plus AI-02 `BasisManifest`.

Closure chronology:

```text
initial candidate
→ destructive test
→ FAIL / 9 hardenings
→ structural PASS candidate
→ independent reverse-engineering / second kill-test
→ 4 additional hardenings
→ final compound retest PASS
→ C01..C33 accepted
```

Important final Context properties include:

```text
Context != canonical reality
Context != Memory != Retrieval
InformationNeed owns sufficiency/coverage/currentness
no universal RAG
permission-aware acquisition
processing != consumer/provider exposure != recipient disclosure
DATA != INSTRUCTION
Reality Scope != Runtime Interpretation Frame
Interaction Session != provider continuity
model-discovered need may refine, not widen scope
source/use exclusions are first-class
child obligations propagate; parent context does not
readiness is consumer-specific and non-monotonic
assembled ConsumerContext != established effective provider exposure
provider-native acquisition remains governed
acquisition authority != effect authority
derivation may tighten sensitivity
```

No Domain/Logical/Physical/PostgreSQL reopen was required.

---

## 5. AI-03B — Retrieval + Memory Architecture

**Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE.

Durable authority:

- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Accepted additional runtime contracts:

```text
RetrievalPlan
RetrievalCandidate
```

Primary retrieval rule:

```text
USE THE LEAST-COMPLEX ROUTE
THAT CAN SATISFY THE REQUIRED GUARANTEES.
```

Supported strategy classes when justified include:

```text
structured/exact
material history
typed relation traversal
lexical/fuzzy
semantic/ANN
hybrid/rerank
hierarchical document
direct long-context
Interaction/Run
federated/provider
open-world/bounded JIT
```

Accepted guarantee semantics:

```text
EXACT
BOUNDED_COMPLETE
BEST_EFFORT
APPROXIMATE
SAMPLED
```

Binding:

```text
APPROXIMATE != COMPLETE
candidate count != coverage proof
rank/similarity/rerank != Source Standing
multiple representations of one lineage != independent evidence
index/cache/embedding != source
```

Memory classes remain distinct:

```text
Canonical Application Memory = Domain/PostgreSQL
Interaction Memory
Run / Working Memory
Compaction / Checkpoint State
Adaptive / Derived User Memory
Operational / Experience Memory
Provider Memory / Thread / Cache
Retrieval Representations
Execution Evidence
```

Core memory rules:

```text
DEFAULT NONCANONICAL SURVIVAL = NO
MEMORY SURVIVAL MUST BE EARNED
MEMORY EXISTS != MEMORY MAY BE RECALLED
MEMORY RECALL = GOVERNED ACQUISITION
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
PROCESSING != RETENTION != FUTURE REUSE
MEMORY ADMISSION != MEMORY WRITE PERMIT
CORRECT != FORGET != SOURCE SUPPRESSION
        != USE SUPPRESSION != INFERENCE DISPOSITION
DERIVATIVE != INDEPENDENT EVIDENCE OF ITS ANCESTRY
PAST EXPERIENCE != POLICY
PROVIDER MEMORY = REPLACEABLE OPTIMIZATION
CANONICAL PROMOTION != DUPLICATION
```

Closure chronology:

```text
DANTE-first design
→ targeted challenger research
→ first heavy kill-test PASS CANDIDATE
→ fresh independent validation FAIL / 5 hardenings
→ final compound retest PASS
→ B01..B35 accepted
```

No generic memory/Fact ontology, vector DB, memory framework, provider choice or DB change was required.

---

## 6. AI-03C — Destructive Validation + Materialization Blueprint

**Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE.

Durable authority:

- `docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`

AI-03C asks what actually deserves physical survival after Context/Retrieval/Memory semantics are closed.

Final binding model is orthogonal/faceted:

```text
SEMANTIC AUTHORITY
!= FUNCTIONAL ROLE
!= SURVIVAL DISPOSITION
!= PHYSICAL OWNER/LOCATION
!= CURRENT ELIGIBILITY
```

Materialization default:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
```

Final materialization posture includes:

```text
ContextPlan / InformationNeed / RetrievalPlan /
RetrievalCandidate / ContextFragment / ConsumerContext
→ runtime / NO-STORE

ordinary Interaction / Work / Run state
→ transient by default

Class-B crash-safe durable work
→ Restate target when activated

Class-A async external/publication coordination
→ transactional outbox when triggered

invalidation/rebuild cursor, generation selector,
DANTE-owned provider locator
→ bounded durable technical coordination only when required

adaptive/user inference
→ recompute by default; bounded durable only when earned

user suppression/retention/inference controls
→ truthful canonical governance durability

provider memory/thread/cache
→ replaceable provider optimization

OCR/chunks/summaries/FTS/vector/embeddings
→ source-linked derived retrieval plane

one-shot upload
→ ephemeral; no forced ContentArtifact

reusable object bytes
→ object storage only with real ContentArtifact lifecycle

semantic pending/reconciliation obligation
→ proper Domain/application owner where material

provider receipt/dispatch trace/outcome proof
→ separate technical evidence
```

---

## 7. AI-03C hardenings MAT-01..MAT-15

```text
MAT-01  Architecture contract != persistence owner; default no-store.
MAT-02  Durable Execution Runtime State is distinct from canonical/derived/provider state.
MAT-03  Durable journal != privacy-free runtime; checkpoint/journal minimization mandatory.
MAT-04  User control/suppression/inference disposition cannot be disposable with derivative.
MAT-05  Persistent derivative requires truthful source basis + transform/generation identity.
MAT-06  Async invalidation != current eligibility authority.
MAT-07  Recomputable derived state is sacrificial in recovery and non-serving until reconciled/rebuilt.
MAT-08  Runtime/provider/derived recovery cannot outrun canonical PostgreSQL recovery readiness.
MAT-09  ANN is optimization, not prerequisite; exact eligible-universe baseline first.
MAT-10  Derived representation generations do not silently mix.
MAT-11  Semantic authority != functional role != survival != owner != eligibility.
MAT-12  Durable technical coordination/binding is distinct from Domain truth and Class-B execution;
        convergence cannot depend only on one-shot invalidation delivery.
MAT-13  Large derived basis may use scalable typed basis envelopes;
        MaterialStateRef != MVCC/LSN/hash/digest.
MAT-14  Representation build/catch-up/readiness/atomic serving cutover is required;
        retrieval/cache binds to one applicable serving generation.
MAT-15  Semantic obligation != execution/audit evidence.
```

---

## 8. Recovery / anti-resurrection

Binding:

```text
RESTORED BYTES != RESTORED ELIGIBILITY
RUNTIME RECOVERY != CANONICAL RECOVERY
```

PostgreSQL recovery/reconciliation must reach serving-ready state before consequential durable runtime resumes.

Then current source state, AuthZ, Consent, Visibility, represented party, supersession/cancellation, expected state/basis and retention/reuse eligibility are reread/revalidated as applicable.

Recovered derived/search/provider/object state is non-serving by default until rebuilt or explicitly reconciled.

Activated projection/search/provider/object systems require explicit invalidation/purge/reconciliation ownership and a convergent repair path. One lost invalidation event cannot be the only path to correctness.

---

## 9. Search/vector posture after AI-03 closure

Available PostgreSQL capabilities remain dormant until a real consumer earns activation.

Lexical progression:

```text
structured/exact
→ owner/query-specific lexical/fuzzy
→ application merge
→ unified projection only if measured evidence requires it
```

Vector progression:

```text
no vector path without real consumer
→ source-linked embedding if semantic retrieval adds value
→ EXACT nearest-neighbor baseline in eligible universe
→ direct benchmark
→ ANN comparison only if exact becomes insufficient
→ HNSW/IVFFlat only after recall/security/recovery/resource proof
```

No embedding model/dimension/metric/index family is selected.

---

## 10. Representation generation/cutover

Embedding/OCR/chunk/normalization/FTS/summary/reranker generations must not mix silently.

Required pattern:

```text
A serving
→ build B from declared basis
→ catch up writes/deletions/suppressions
→ validate
→ B READY
→ atomic serving-selector cutover
→ invocation/cache bound to one generation
→ A retire
→ bounded cleanup
```

After recovery, selector/generation/basis coherence must be revalidated before serving.

---

## 11. Direct Physical proof obligations remain open

AI-03 structural closure does not claim implementation/direct benchmark PASS.

Especially still UNEXECUTED:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query correctness
PSV-08 / SC-019 vector recall/relevance after filtering
PSV-09 / SC-020 projection freshness/material-basis behavior
PSV-10 / SC-021 deletion/redaction propagation
PSV-21..28B Restate/durable execution/journal privacy/recovery
PSV-37 pgvector source/model/freshness provenance
```

LOW/BASE/HIGH searchable-corpus tiers remain benchmark envelopes, not forecasts.

---

## 12. AI-03 validation chronology

```text
AI-03A
Context architecture
→ first destructive test FAIL / 9 hardenings
→ independent test / 4 additional hardenings
→ C01..C33 PASS / CLOSED

AI-03B
Retrieval + Memory
→ internal design + targeted research
→ first heavy test PASS candidate
→ independent validation FAIL / 5 hardenings
→ B01..B35 PASS / CLOSED

AI-03C
Materialization
→ state reconstruction + physical research
→ first materialization kill-test FAIL
→ MAT-01..10
→ compound PASS candidate
→ independent reverse-engineering FAIL / 5 final hardenings
→ MAT-11..15
→ final compound retest PASS
```

Final AI-03 structural result:

```text
Context architecture                   PASS
Retrieval architecture                 PASS
Memory classes/lifecycle               PASS
materialization boundary               PASS
privacy/retention boundary             PASS
multi-actor/represented-party boundary PASS
source lifecycle/anti-resurrection     PASS
runtime/canonical recovery boundary    PASS
provider replaceability                PASS
no unjustified persistence             PASS

AI-03A                                 CLOSED
AI-03B                                 CLOSED
AI-03C                                 CLOSED
AI-03                                  CLOSED / STRUCTURALLY ACCEPTED
```

No Domain, Logical, Physical-target or PostgreSQL-Constitution reopen was required.

---

## 13. What AI-03 did NOT decide

Still open by design:

```text
OpenAI / Anthropic / Gemini / Qwen choice
specific model
specific embedding model/dimension
specific provider SDK/gateway
conversation table
Run table
memory table
chunk table
embedding table
new FTS/trigram indexes
pgvector activation
HNSW / IVFFlat
Redis
specialist vector DB
Mem0 / Zep / Graphiti / Letta adoption
Restate deployment
R2 deployment
PowerSync activation
MCP/A2A implementation
sandbox implementation
exact cache implementation
exact retention/invalidation schemas/jobs
```

Any future structural DB change uses the normal CP6 same-change discipline and a separate exact write gate.

---

## 14. Closure and routing

AI-03 is now **CLOSED / STRUCTURALLY ACCEPTED**.

Accepted downstream contract:

```text
AI-03A C01..C33
AI-03B B01..B35
AI-03C MAT-01..MAT-15
```

AI-04 Productionization Architecture is next.

AI-04 may choose concrete runtime, provider, security, evaluation, observability, deployment and activation designs only inside these closed boundaries.

Do not reopen AI-03 because a framework/provider/storage product prefers a different ontology. Reopen the smallest affected boundary only if direct implementation or benchmark evidence exposes a real contradiction.
