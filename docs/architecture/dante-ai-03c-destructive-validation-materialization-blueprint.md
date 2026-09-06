# DANTE AI-03C — Destructive Validation + Materialization Blueprint

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **Closed:** 2026-09-02
- **Upstream Context authority:** AI-03A CLOSED / C01..C33
- **Upstream Retrieval/Memory authority:** AI-03B CLOSED / B01..B35
- **Implementation:** NOT STARTED by this document
- **PostgreSQL schema evolution:** NONE AUTHORIZED / NONE REQUIRED BY AI-03C
- **Alembic change:** NONE
- **SQLAlchemy mapping change:** NONE
- **Provider/model/embedding selection:** NONE
- **Direct Physical benchmark execution:** NOT CLAIMED

---

## 1. Purpose

AI-03C answers the final AI-03 question:

> **Which accepted Context/Retrieval/Memory states actually deserve physical survival, where may they live, how are they invalidated/recovered, and which apparently useful structures should still not exist?**

AI-03C does not translate architecture nouns into tables.

```text
ARCHITECTURE CONTRACT
!= PERSISTENCE OWNER
!= TABLE
!= INDEX
!= SERVICE
```

Default:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
```

A state earns survival only when a concrete correctness, continuity, recovery, latency, audit, cost or product requirement cannot be satisfied safely through current canonical state plus reread/recomputation.

---

## 2. Authority consumed

AI-03C consumes without reinterpretation:

```text
Product / North Star
Domain CLOSED
Whole Logical CLOSED / WL-H01..WL-H12
Physical Model CLOSED
PostgreSQL 18 = sole canonical persistence/material-history authority
CP6 PostgreSQL Persistence Constitution / ADR-010
Database System of Record / Dictionary
current Alembic + SQLAlchemy + real PostgreSQL truth
Recovery / material_state_retirement / anti-resurrection
AI-02.1 runtime architecture
AI-03A C01..C33
AI-03B B01..B35
```

Primary repository sources include:

- `docs/product/product-identity-and-north-star.md`
- `docs/domain/README.md`
- `docs/logical-model/whole-logical-model-v1.md`
- `docs/physical-model/README.md`
- `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/operations/postgres-recovery-runbook.md`
- `docs/architecture/physical-benchmark-scenario-corpus.md`
- `docs/physical-model/recommendation/post-selection-validation-register-v1.md`
- `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`
- `docs/architecture/dante-ai-03a-full-context-architecture.md`
- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Repository truth outranks this document if later direct implementation evidence reveals a concrete contradiction.

---

## 3. Current concrete physical boundary

Current repository/database truth entering closure:

```text
PostgreSQL 18.6
Alembic 20260830_09
schema dante
69 tables
5 views
15 routines
76 triggers
97 physical indexes
69 foreign keys
123 CHECK constraints
```

Extensions available:

```text
PostGIS 3.6.4
pgvector 0.8.6
pg_trgm 1.6
unaccent 1.1
pg_stat_statements 1.12
```

Availability is not activation.

Accepted Physical ownership remains:

```text
PostgreSQL
= canonical DANTE truth + material history

FTS / pg_trgm / unaccent / pgvector
= derived/query retrieval capability

Restate
= Class-B durable execution runtime target

transactional outbox
= Class-A technical coordination mechanism when triggered

R2
= object-byte target when a real ContentArtifact vertical requires it

provider thread/cache/native memory
= replaceable provider optimization, never canonical truth
```

---

## 4. Final materialization model — orthogonal facets

The initial M0..M9 shorthand was useful for enumeration but the final independent validation found that it mixed independent axes. A physical item can be, for example, both a retrieval representation and recomputable, or provider-owned and retrieval-related.

Binding final model:

### 4.1 Semantic authority

```text
CANONICAL DANTE
NONCANONICAL DANTE-DERIVED
EXTERNAL / PROVIDER-OWNED
TECHNICAL-ONLY
```

### 4.2 Functional role

```text
runtime context/work state
durable execution state
durable technical coordination/binding
derived semantic assessment
retrieval representation/index
cache/optimization
execution/effect evidence
object bytes/artifact representation
canonical governance/control
```

### 4.3 Survival disposition

```text
NO-STORE
TRANSIENT
RECOMPUTABLE
BOUNDED-DURABLE
EXTERNALLY-RETAINED / PROVIDER-OWNED
CANONICAL-DURABLE
```

### 4.4 Physical owner/location

```text
PostgreSQL
Restate
object storage
provider
local/client projection where explicitly accepted
process/runtime memory
NONE
```

### 4.5 Current eligibility / lifecycle

Every retained or externally reused item additionally has current eligibility determined by its applicable source/governance/retention/generation/recovery state.

Binding:

```text
SEMANTIC AUTHORITY
!= FUNCTIONAL ROLE
!= SURVIVAL DISPOSITION
!= PHYSICAL OWNER
!= CURRENT ELIGIBILITY
```

No single enum/classification value may collapse these axes.

---

## 5. Useful shorthand M0..M9

M0..M9 remain documentation shorthand only; they are not exclusive physical types.

```text
M0 existing canonical Domain/PostgreSQL state
M1 transient runtime
M2 durable execution runtime
M3 recomputable derived state
M4 bounded durable derived state
M5 provider-owned optimization
M6 retrieval representation/index
M7 execution/audit/reconciliation evidence
M8 object bytes/artifact representation storage
M9 not justified to store
```

Where an item previously appeared as `M1/M3` or `M3/M6`, the final faceted model is authoritative.

---

## 6. State-family materialization result

| State family | Final posture |
|---|---|
| `ContextPlan` | runtime / NO-STORE |
| `InformationNeed` | runtime / NO-STORE |
| `RetrievalPlan` | runtime / NO-STORE |
| `RetrievalCandidate` | runtime / NO-STORE |
| `ContextFragment` | runtime / NO-STORE |
| `ConsumerContext` | runtime / NO-STORE |
| query rewrite / expansion / HyDE-like state | ephemeral derived / NO-STORE by default |
| model scratch/reasoning | NO-STORE |
| Interaction discourse/referent continuity | transient/session by default |
| full conversation transcript | NOT JUSTIFIED as canonical/durable AI memory |
| ordinary `WorkContract`/Run state | transient by default |
| crash-safe resumable Class-B work | durable execution / Restate target when activated |
| transactional outbox | Class-A durable technical coordination when triggered |
| rebuild/invalidation cursor/watermark | durable technical coordination only when an activated derivative needs it |
| serving-generation selector | durable technical binding when multi-generation serving is activated |
| DANTE-owned provider locator/binding | minimal technical binding when required; provider state itself remains noncanonical |
| checkpoint/compaction | minimum continuity state; not source |
| `ContextManifest` | selective minimal evidence only where consequence requires |
| `BasisManifest` | selective minimal evidence/dependency metadata only where consequence requires |
| confirmed user fact/preference | proper Domain owner/PostgreSQL |
| adaptive/inferred user hypothesis | recompute by default; bounded durable only when survival is earned |
| explicit retention/use/inference suppression | durable canonical governance/control; never disposable with derivative |
| operational/experience memory | recompute by default; bounded durable only with verified basis + utility |
| provider thread/native memory/cache | provider optimization / replaceable |
| OCR/extracted text | derived/recomputable; persist only with justified content/search need |
| chunk/span representation | derived retrieval representation; no generic chunk table requirement |
| hierarchical summaries | derived/recomputable; no durable default |
| FTS representation/index | query-specific derived index only when a real consumer earns activation |
| trigram index | query-specific only |
| embeddings | source-linked derived representation; NOT ACTIVATED |
| HNSW / IVFFlat | ANN optimization; NOT ACTIVATED |
| retrieval/result cache | disposable optimization by default |
| reusable raw document/media bytes | object storage when ContentArtifact lifecycle requires |
| `ContentArtifact` identity/material metadata | canonical Domain/PostgreSQL owner |
| one-shot transient upload | ephemeral; need not become `ContentArtifact` |
| semantic pending/reconciliation obligation | proper affected Domain/application owner where material |
| provider receipt/dispatch trace/outcome evidence | minimal execution/evidence role |
| Scenario Workspace | runtime / NO-STORE by default |
| accepted saved scenario | promote to proper `Possibility` / `Proposal` / `Plan` / other accepted owner |
| retrieval/eval artifacts | bounded technical evidence only when needed to prove behavior |

A closed Domain concept does not imply that every specialist table exists in the current schema. AI-03C authorizes no new table merely from this matrix.

---

## 7. Persist the obligation, not the blob

A durable obligation does not automatically justify retaining every transient payload that preceded it.

Example:

```text
external effect outcome becomes UNKNOWN
→ semantic pending/reconciliation obligation may exist
→ minimal provider/effect evidence may be needed
```

The semantic obligation belongs to the truthful affected Domain/application owner when material. Technical receipts/traces remain separate evidence.

Not automatically retained:

```text
full ConsumerContext
all ContextFragments
full model scratch state
entire transcript
all retrieved document text
all intermediate candidates
```

Binding:

```text
SEMANTIC OBLIGATION
!= EXECUTION / AUDIT EVIDENCE
```

No generic `Reconciliation` or `AIObligation` semantic root is introduced.

---

## 8. Durable execution and technical coordination

### 8.1 Class-B durable execution

```text
DURABLE EXECUTION RUNTIME STATE
!= POSTGRESQL CANONICAL STATE
!= DERIVED MEMORY
!= PROVIDER MEMORY
```

Restate remains the selected target when a real Class-B operation requires crash-safe suspension/resume/retry.

No generic PostgreSQL `run` / `run_step` schema is justified by AI-03C.

### 8.2 Class-A technical coordination

The accepted CP6 transactional outbox remains a separate trigger-bound mechanism.

Technical state that may require bounded durability includes:

```text
transactional outbox rows
invalidation/rebuild work
projection/index catch-up cursor or watermark
serving-generation selector
DANTE-owned provider binding/locator
quarantine/rebuild bookkeeping
```

Binding:

```text
DURABLE TECHNICAL COORDINATION
!= DOMAIN TRUTH
!= DURABLE RUN PAYLOAD
!= USER MEMORY
!= PROVIDER STATE
```

The concrete schema is activation-specific and not designed by AI-03C.

---

## 9. Journal/checkpoint privacy

Durable runtime persistence is a privacy surface.

```text
DURABLE JOURNAL
!= PRIVACY-FREE RUNTIME
```

Default convenience payloads rejected for durable journaling include:

```text
full ConsumerContext
full private prompt
raw sensitive document corpus
entire transcript
unbounded tool output
privileged credentials
```

Prefer minimum typed state:

```text
stable/bounded refs
operation/effect IDs
expected-state bindings
small receipts/digests
minimum checkpoint necessary to resume
```

After resume, reread/revalidate current canonical/source state rather than trusting a private duplicate where practical.

Existing Restate PSV obligations, including journal privacy and Python/deployment/encryption posture, remain UNEXECUTED.

---

## 10. Adaptive/derived memory

Derived user hypotheses remain noncanonical.

Preferred default:

```text
eligible canonical/history basis
→ bounded Evaluation / derived assessment
→ use under current purpose
→ discard / recompute
```

Bounded durable derived survival is exceptional and requires:

```text
measured continuity/latency/cost/reproducibility need
truthful source basis
currentness/supersession revalidation
retention/future-reuse eligibility
appropriate user control
no better canonical Domain owner
```

When a derived meaning is confirmed and belongs in canonical state:

```text
derived candidate
→ governed proposal/effect
→ proper Domain owner/PostgreSQL
→ old derivative stops acting as independent authority/corroboration
```

User controls such as retention/use/inference suppression must not live only inside disposable derived state.

```text
CONTROL-PLANE DURABILITY
!= DERIVED-PLANE DURABILITY
```

Applicable controls belong to truthful accepted governance semantics such as Decision, Conditional Policy, Consent, Visibility or another specific owner according to meaning.

---

## 11. Persistent derivative basis

Any persistent derivative must remain source-linked enough to prevent orphan alternate truth.

Possible basis information includes:

```text
source identity/family/location
source reality class
real MaterialStateRef where one exists
external snapshot/revision identity where truthful
query/projection contract + version
as-of/window/acquisition boundary
scope/inclusion/exclusion semantics
purpose/security boundary where material
transformation/model/configuration generation
creation/derivation time
```

For large source sets:

```text
DERIVED BASIS
!= ENUMERATE EVERY SOURCE ROW
```

A scalable typed basis envelope is allowed when it remains sufficient to reconstruct/revalidate the source population and lifecycle.

Technical boundaries such as MVCC/xmin/LSN/digest/hash may participate as technical evidence when appropriate but:

```text
MVCC / LSN / HASH / DIGEST
!= MaterialStateRef
!= semantic truth
```

If a durable derivative cannot preserve/reconstruct adequate basis, do not persist it.

---

## 12. Async invalidation and convergent repair

Activated derived/search/provider/object systems require explicit invalidation/purge/reconciliation ownership.

```text
ASYNC CLEANUP
!= CURRENT ELIGIBILITY AUTHORITY
```

A stale physical derivative may exist while already logically ineligible. Serving must enforce current authoritative lifecycle/governance before material use/exposure.

In addition:

```text
ONE-SHOT INVALIDATION DELIVERY
!= SUFFICIENT CONVERGENCE GUARANTEE
```

A lost/rolled-back outbox cursor or external failure must be recoverable through bounded reconcile/rebuild/repair that can rediscover stale state.

This preserves CP6 LIFE-07 and Recovery anti-resurrection semantics.

---

## 13. Recovery fence

```text
RUNTIME RECOVERY
!= CANONICAL RECOVERY
```

Consequential durable work cannot resume merely because Restate/provider/runtime bytes are available.

After PostgreSQL restore/reconciliation reaches serving-ready state, durable work must reread/revalidate as applicable:

```text
canonical/source state
AuthZ
Consent
Visibility
Actor / represented party
Work Supersession / cancellation
expected MaterialState/basis
retention/reuse eligibility
```

Recovered derived/search/provider/object state is non-serving by default until rebuilt or explicitly reconciled.

```text
RESTORED DERIVED BYTES
!= RESTORED ELIGIBILITY
```

Derived state is intentionally sacrificial where recomputable.

---

## 14. Representation generations and atomic serving cutover

Silent mixing of incompatible retrieval generations is forbidden.

Generation identity may cover:

```text
embedding model/version/dimension/metric/normalization
OCR/extraction implementation
chunking algorithm
text normalization
FTS dictionary/configuration
summary/hierarchy algorithm
reranker/contextualization representation
```

Candidate lifecycle:

```text
GENERATION A serving
→ build B from declared source basis
→ catch up mutations + suppressions
→ validate correctness/security/recall/resource behavior
→ mark B READY
→ atomic serving-selector cutover A -> B
→ bind each retrieval invocation/cache entry to applicable generation
→ do not silently mix A/B inside one invocation
→ retire A
→ bounded cleanup
```

After recovery:

```text
selector exists
!= referenced generation is available/current/eligible
```

Selector/generation/basis coherence must be verified before serving.

Generation identity is technical metadata and not a fake `MaterialStateRef`.

---

## 15. Search / FTS / trigram posture

PostgreSQL FTS, `pg_trgm` and `unaccent` remain available but not globally activated.

Preferred progression:

```text
structured/exact semantic query
→ owner/query-specific lexical/fuzzy search when needed
→ application merge when adequate
→ unified derived search projection only with measured justification
```

Rejected:

```text
AI needs search
→ add tsvector/GIN/trigram everywhere
```

SC-017/SC-018 and PSV-06/07 remain direct future proof obligations.

---

## 16. Vector / ANN posture

pgvector availability does not imply embeddings or ANN.

Final progression:

```text
PHASE 0  no vector path without a real consumer
PHASE 1  source-linked embedding only if semantic retrieval adds value
PHASE 2  EXACT nearest-neighbor baseline inside current eligible universe
PHASE 3  benchmark correctness/latency/resource behavior
PHASE 4  compare ANN only if exact becomes insufficient
PHASE 5  activate HNSW/IVFFlat only after direct recall/security/recovery/resource proof
```

Binding:

```text
ANN IS AN OPTIMIZATION
NOT A RETRIEVAL PREREQUISITE

APPROXIMATE != COMPLETE
```

ANN acceptance must measure after real filtering, including hidden/non-interference effects.

No embedding model, dimension, metric, HNSW/IVFFlat parameters or specialist vector DB is selected.

SC-019 / PSV-08 / PSV-37 remain UNEXECUTED direct proof obligations.

---

## 17. ContentArtifact/object boundary

One-shot input:

```text
upload
→ parse/OCR/extract
→ bounded current work
→ discard when retention basis ends
```

It need not become a permanent `ContentArtifact`.

Reusable content:

```text
ContentArtifact identity/material semantics
→ PostgreSQL canonical owner

raw reusable bytes
→ object storage when activated

OCR / extraction / chunks / summaries / embeddings
→ derived retrieval plane
```

Same bytes reused by different artifacts do not collapse artifact identity/governance merely because object-level deduplication may later be technically possible.

AI-03C does not create `artifact_chunks`, `artifact_embeddings` or R2 flows ahead of the real content vertical.

---

## 18. Provider/cache posture

Provider thread/native memory/file search/cache is replaceable optimization.

```text
PROVIDER STATE != DANTE CANONICAL STATE
CACHE HIT != CURRENT AUTHORIZATION
CACHE HIT != CURRENT SOURCE ELIGIBILITY
CACHE HIT != CURRENT DISCLOSURE PERMISSION
CACHE HIT != CURRENT MEMORY-REUSE PERMISSION
```

DANTE-owned provider bindings/locators may be minimal durable technical coordination state when needed, but do not promote provider state to canonical memory.

Cache/retrieval reuse must remain compartmented by all material dimensions including Actor, represented party, purpose, policy and applicable representation generation.

---

## 19. Final hardening record — MAT-01..MAT-15

```text
MAT-01
ARCHITECTURE CONTRACT != PERSISTENCE OWNER.
DEFAULT NONCANONICAL PERSISTENCE = NO.

MAT-02
DURABLE EXECUTION RUNTIME STATE is its own physical role.
Restate != PostgreSQL != derived memory.

MAT-03
DURABLE JOURNAL != PRIVACY-FREE RUNTIME.
Journal/checkpoint minimization is mandatory.

MAT-04
USER CONTROL / SUPPRESSION / INFERENCE DISPOSITION
must not be disposable merely because a governed derivative is.

MAT-05
PERSISTENT DERIVATIVE REQUIRES
truthful source basis + transformation/generation identity.

MAT-06
ASYNC INVALIDATION != CURRENT ELIGIBILITY AUTHORITY.

MAT-07
RECOMPUTABLE DERIVED STATE is sacrificial during recovery
and cannot serve until rebuilt/reconciled.

MAT-08
RUNTIME / PROVIDER / DERIVED RECOVERY
cannot outrun canonical PostgreSQL recovery/reconciliation readiness.

MAT-09
ANN IS AN OPTIMIZATION, NOT A RETRIEVAL PREREQUISITE.
Exact eligible-universe baseline precedes ANN activation.

MAT-10
DERIVED REPRESENTATION GENERATIONS MUST NOT MIX SILENTLY.
Embedding/OCR/chunk/FTS/summary/etc. upgrades need explicit generations.

MAT-11
SEMANTIC AUTHORITY != FUNCTIONAL ROLE
!= SURVIVAL DISPOSITION != PHYSICAL OWNER != ELIGIBILITY.
Materialization is faceted, not one exclusive class.

MAT-12
DURABLE TECHNICAL COORDINATION/BINDING STATE
is distinct from Domain truth and Class-B durable execution.
Class-A outbox, rebuild/invalidation state, generation selectors
and DANTE-owned provider locators remain trigger-bound technical state.
Convergence cannot depend only on one-shot event delivery.

MAT-13
SCALABLE DERIVED BASIS does not require enumerating every source row.
Typed reconstructable basis envelopes are allowed;
MaterialStateRef != MVCC/LSN/hash/digest.

MAT-14
SERVING GENERATION must have build/catch-up/readiness/atomic-cutover semantics.
Retrieval invocations and applicable caches bind to one serving generation;
recovery revalidates selector/generation/basis coherence.

MAT-15
SEMANTIC OBLIGATION != EXECUTION/AUDIT EVIDENCE.
Canonical pending/staged/reconciliation meaning stays with the truthful
Domain/application owner; provider receipts/traces remain technical evidence.
```

---

## 20. Validation chronology

```text
STATE-FAMILY RECONSTRUCTION
→ COMPLETE

INITIAL MATERIALIZATION MATRIX
→ COMPLETE

TARGETED PHYSICAL RESEARCH
PostgreSQL FTS/trigram
pgvector/ANN
Restate durability/privacy
→ COMPLETE ENOUGH FOR ARCHITECTURE

FIRST MATERIALIZATION KILL-TEST
→ FAIL

MAT-01..MAT-10
→ HARDENED CANDIDATE

COMPOUND RETEST
→ PASS CANDIDATE

FRESH INDEPENDENT REVERSE-ENGINEERING
→ FAIL / 5 FINAL HARDENINGS

MAT-11..MAT-15
→ INCORPORATED

FINAL COMPOUND RETEST
→ PASS
```

Final hostile cases included:

```text
private one-shot source + retention denial
inference suppression surviving derivative rebuild
provider-native private file search + local provider locator
outbox/invalidation loss + stale external index
large 50M-scale generation build during writes/deletions
long-history derived inference with non-enumerable basis
PostgreSQL/Restate/provider/index recovery mismatch
selector/index generation mismatch after restore
index offline/degraded serving
cache across Actor/represented-party/generation change
ContentArtifact bytes shared across distinct semantic lifecycles
external effect UNKNOWN + reconciliation requirement
canonical promotion + stale derivative
source deletion + lost invalidation event + later repair sweep
future model/representation generation replacement
```

Result:

```text
FURTHER MATERIAL STRUCTURAL GAP     NONE FOUND
AI-03A REOPEN                       NO
AI-03B REOPEN                       NO
DOMAIN REOPEN                       NO
LOGICAL REOPEN                      NO
PHYSICAL TARGET REOPEN              NO
POSTGRESQL CONSTITUTION REOPEN      NO
NEW TOP-LEVEL AI CONTRACT           NO
NEW DOMAIN OWNER                    NO
POSTGRESQL/ALEMBIC CHANGE NOW       NO
NEW TABLE REQUIRED NOW              NO
NEW INDEX REQUIRED NOW              NO
PGVECTOR/ANN ACTIVATION              NO
FTS/TRIGRAM ACTIVATION               NO
RESTATE ACTIVATION                   NO
R2 ACTIVATION                        NO
PROVIDER/MODEL SELECTION             NO
IMPLEMENTATION PASS                  NOT CLAIMED
```

---

## 21. Direct proof obligations remain UNEXECUTED

Architecture closure does not relabel Physical direct-proof work.

Especially still open:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query correctness
PSV-08 / SC-019 vector recall/relevance after real filtering
PSV-09 / SC-020 projection freshness/material-basis behavior
PSV-10 / SC-021 deletion/redaction propagation

PSV-21..28B durable execution / Restate
including journal privacy, recovery and deployment-mode obligations

PSV-37 pgvector model/source/freshness provenance
```

Synthetic retrieval tiers remain benchmark envelopes, not forecasts:

```text
LOW   ~100k searchable chunks
BASE  ~5M searchable chunks
HIGH  ~50M searchable chunks
```

No runtime/search/vector/object mechanism receives production acceptance until its applicable direct evidence exists.

---

## 22. Intentionally absent

AI-03C deliberately does not justify today:

```text
generic conversation-history table
generic Run table
generic AI memory table
adaptive-memory mega-table
operational-memory mega-table
generic chunk table
generic summary table
generic embedding table
unified cross-domain search table
Redis
specialist vector database
provider-thread canonical schema
provider-native memory authority
one index on every text field
one durable row for every ContextManifest/BasisManifest
```

Absence is architectural restraint, not incompleteness.

---

## 23. Closure verdict

AI-03C is **CLOSED / STRUCTURALLY ACCEPTED**.

This means the materialization architecture has survived two destructive passes and the final hardening set MAT-01..MAT-15 without requiring a semantic or physical-target-stack reopen.

It does **not** mean:

```text
implementation exists
PostgreSQL was migrated
Restate was deployed
R2 was deployed
embeddings exist
pgvector is activated
ANN was benchmarked
FTS indexes exist
provider/model was selected
SC/PSV direct proofs passed
```

These remain later activation/production work.

AI-03 Context / Retrieval / Memory may therefore close structurally and route to AI-04 Productionization Architecture.

---

## 24. Binding handoff to AI-04

AI-04 inherits without reinterpretation:

```text
AI-03A C01..C33
AI-03B B01..B35
AI-03C MAT-01..MAT-15
```

AI-04 may choose concrete deployment/runtime/security/provider/observability/evaluation designs only inside these boundaries.

Any structural PostgreSQL/index change still requires its own exact gate and CP6 same-change discipline.

Do not reopen AI-03 merely because a provider/framework prefers a different ontology or storage model. Reopen the smallest affected boundary only if concrete implementation/direct-proof evidence exposes an actual contradiction.
