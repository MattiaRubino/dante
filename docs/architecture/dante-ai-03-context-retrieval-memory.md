# DANTE AI-03 — Context / Retrieval / Memory Architecture

- **Status:** ACTIVE / BRANCH-LOCAL ARCHITECTURE WORKSTREAM
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Upstream structural baseline:** AI-02.1 v0.5 / STRUCTURALLY ACCEPTED
- **AI-03A:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE / 13 HARDENINGS / C01..C33
- **AI-03B:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE / 5 FINAL HARDENINGS / B01..B35
- **AI-03C:** CANDIDATE / FIRST MATERIALIZATION KILL-TEST FAIL / MAT-01..MAT-10 INCORPORATED / HARDENED RETEST PASS / FINAL INDEPENDENT VALIDATION PENDING
- **Implementation:** NOT STARTED by this document
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT
- **Provider/model selection:** OPEN
- **Current macro-phase:** AI-03C — FINAL INDEPENDENT DESTRUCTIVE VALIDATION OF MATERIALIZATION BLUEPRINT

---

## 1. Purpose

AI-03 defines how DANTE obtains, scopes, validates, composes, retains, retrieves and retires information used by intelligence without creating a second reality beside the accepted Product/Domain/Logical/Physical/PostgreSQL system.

The central question is not "which vector database should DANTE use?" or "which memory framework should DANTE adopt?".

The central question is:

> **How does DANTE build the minimum sufficiently complete, currently valid, authorized and purpose-relevant representation of reality required for a piece of work, how does it find that material, which noncanonical information earns survival, and what — if anything — deserves physical materialization?**

AI-03 consumes the closed Product/Domain/Logical/Physical/database authority and the structurally accepted AI-02 runtime architecture. It must not reopen those layers for retrieval or memory convenience.

---

## 2. Authoritative source corpus

AI-03 must be read against the following sources before material architecture decisions are made.

### Product / North Star

- `docs/product/product-identity-and-north-star.md`
- `docs/product/v1-data-history-and-privacy.md`
- `docs/product/v1-user-context-and-safety.md`
- `docs/product/v1-adaptive-intelligence-and-future-social.md`
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
- Recovery / material-state-retirement / anti-resurrection authority

### Intelligence authority

- `docs/architecture/dante-ai-foundation.md`
- `docs/architecture/ai-production-engineering-state-of-the-art-2026.md`
- `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`
- `docs/architecture/dante-ai-03a-full-context-architecture.md`
- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`
- `docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`
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

AI-03A adds accepted Context invariants `C01..C33`.

AI-03B adds accepted Retrieval/Memory invariants `B01..B35`.

AI-03C currently adds candidate physical/materialization hardenings `MAT-01..MAT-10`; they remain pending final independent validation and are not yet an AI-03 closure claim.

No Context/Retrieval/Memory design is accepted if it creates a generic semantic escape hatch around closed Domain/Logical meaning.

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
!= DANTE should always use X
!= DANTE may disclose X
!= X should be copied into every model context
!= X may be retained as durable AI memory
!= X may be reused for a different future purpose
```

Purpose limitation, minimisation, retention limitation and user control are architecture requirements, not launch-time polish.

---

## 5. Core AI-03 distinction

AI-03 keeps three responsibilities separate:

```text
CONTEXT
= the purpose-bound runtime view available to a specific reasoning/execution step

RETRIEVAL
= governed discovery + validation of candidate material for Context

MEMORY
= noncanonical information/state that survives beyond the immediate step or Run
  under an explicit lifecycle
```

A single item may participate in more than one responsibility over time, but the responsibilities are not synonyms.

Canonical application memory is not a fourth generic AI layer: durable structured DANTE meaning remains owned by accepted Domain/PostgreSQL.

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

plus inherited AI-02 `BasisManifest`.

AI-03A chronology:

```text
initial candidate
→ dedicated mega-test
→ FAIL / 9 hardenings
→ structural PASS candidate
→ independent reverse-engineering / second kill-test
→ 4 additional hardenings
→ final compound retest PASS
→ C01..C33 accepted
```

No new Domain/Logical/Physical/PostgreSQL owner was required.

### AI-03B — Retrieval + Memory Architecture

**Status:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE

Durable authority:

- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Accepted additional runtime contracts:

```text
RetrievalPlan
RetrievalCandidate
```

These are not Domain roots, database tables or mandatory services.

Accepted Retrieval/Memory architecture includes:

```text
least-complex adequate retrieval route per InformationNeed
explicit coverage / retrieval-guarantee semantics
permission-safe eligible search universe
structured/current/history/relation retrieval
lexical / fuzzy / semantic / ANN / hybrid / rerank routes
hierarchical document and direct long-context routes
provider/federated/open-world/JIT acquisition under AI-03A governance
query-rewrite / transformation integrity
source reread / currentness validation
lineage-aware dedup / no fake corroboration

Canonical Application Memory remains Domain/PostgreSQL
Interaction Memory
Run / Working Memory
Compaction / Checkpoint State
Adaptive / Derived User Memory
Operational / Experience Memory
Provider Memory / Thread / Cache
Retrieval Representations
Execution Evidence

Memory Survival / Admission Gate
processing != retention != future reuse
retention admission != durable write permit
user-memory inspectability/control
memory recall = governed acquisition
canonical promotion + non-duplication
Correction / Forgetting / Source Suppression /
Use Suppression / Inference Disposition
inference-resurrection protection
self-corroboration / ancestry protection
operational-memory poisoning protection
derived-memory basis currentness
provider-state replaceability
Recovery / anti-resurrection inheritance
```

AI-03B chronology:

```text
DANTE-first internal architecture
→ targeted modern challenger research
→ reconciled candidate
→ first heavy kill-test PASS CANDIDATE
→ fresh independent validation
→ FAIL / 5 final hardenings
→ final compound retest PASS
→ B01..B35 accepted
→ CLOSED / STRUCTURALLY ACCEPTED
```

Final hardenings:

```text
FINAL-GAP-01 retention admission / governed memory mutation
FINAL-GAP-02 durable user-memory inspectability and control
FINAL-GAP-03 retrieval transformation / query-rewrite integrity
FINAL-GAP-04 derived-memory basis currentness
FINAL-GAP-05 canonical-promotion non-duplication
```

No new Domain/Logical/Physical/PostgreSQL owner, vector database, memory framework or provider selection was required.

### AI-03C — Destructive Validation + Materialization Blueprint

**Status:** CANDIDATE / HARDENED COMPOUND RETEST PASS / FINAL INDEPENDENT VALIDATION PENDING

Durable candidate authority:

- `docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`

AI-03C has now completed the first materialization pass:

```text
state-family reconstruction
→ initial materialization matrix
→ targeted physical research
→ first materialization kill-test FAIL
→ MAT-01..MAT-10
→ hardened compound retest PASS CANDIDATE
```

The candidate adds one explicit physical class that was previously missing from the coarse materialization vocabulary:

```text
DURABLE EXECUTION RUNTIME STATE
```

It remains distinct from canonical PostgreSQL, derived memory, provider state and retrieval indexes. Restate remains the selected Physical target for Class-B durable execution when a real consumer activates that need.

The refined materialization classes are:

```text
M0 existing canonical Domain/PostgreSQL state
M1 transient runtime state
M2 durable execution runtime state
M3 recomputable derived state
M4 bounded durable derived state
M5 provider-owned optimization state
M6 retrieval representation / index
M7 execution / audit / reconciliation evidence
M8 object bytes / artifact representation storage
M9 NOT JUSTIFIED TO STORE
```

The candidate currently concludes:

```text
ContextPlan / InformationNeed             transient / no-store
RetrievalPlan / RetrievalCandidate        transient / no-store
ContextFragment / ConsumerContext         transient / no-store
ordinary Interaction / Run state          transient by default
Class-B resumable execution               durable runtime / Restate target when activated
adaptive user inference                   recomputable by default
confirmed user meaning                    promote to proper Domain owner
user use/inference suppression            canonical governance durability
provider memory/thread/cache              replaceable optimization
OCR/chunks/summaries                      recomputable/source-linked derivatives
FTS/trigram                               query-specific derived indexes only when justified
embeddings                                not activated
HNSW / IVFFlat                            not activated
retrieval cache                           no durable default
ContentArtifact raw reusable bytes        object-storage target only when content vertical requires
ContextManifest / BasisManifest           selective minimal evidence only where justified
```

Candidate hardenings:

```text
MAT-01 architecture contract != persistence owner
MAT-02 Durable Execution Runtime State is a distinct physical class
MAT-03 durable journal != privacy-free runtime
MAT-04 user-control durability != derivative durability
MAT-05 persistent derivative requires valid source basis
MAT-06 async invalidation != current eligibility
MAT-07 recomputable derived state is sacrificial in recovery
MAT-08 runtime/provider/derived recovery cannot outrun canonical recovery
MAT-09 ANN is optimization, not retrieval prerequisite
MAT-10 derived representation generations do not mix silently
```

No PostgreSQL/Alembic/SQLAlchemy change, provider selection, pgvector activation, ANN selection, FTS activation, Restate activation or R2 activation is justified merely by this candidate.

Direct SC/PSV benchmark obligations remain UNEXECUTED.

---

## 7. Accepted Context architecture principles

AI-03B/AI-03C inherit these from AI-03A.

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

## 8. Accepted Retrieval architecture principles

### 8.1 RetrievalPlan and RetrievalCandidate stay runtime contracts

```text
RetrievalPlan
!= Domain owner
!= database table requirement

RetrievalCandidate
!= ContextFragment
!= Evidence
!= Observation
!= canonical fact
```

### 8.2 Retrieval guarantee must match InformationNeed coverage

Accepted guarantee semantics include:

```text
EXACT
BOUNDED_COMPLETE
BEST_EFFORT
APPROXIMATE
SAMPLED
```

```text
APPROXIMATE != COMPLETE
candidate count != coverage proof
```

ANN/semantic/hybrid Top-K cannot alone satisfy a complete-required need merely because K results were returned.

### 8.3 Search universe is governed before ranking semantics

The Retrieval Eligibility Envelope defines the candidate/source universe that may legitimately participate for the current purpose/security/representation context.

Post-filtering alone is not a universal permission-safe discovery proof when unauthorized candidates can influence rank, count, candidate exhaustion, timing or other observable surfaces.

### 8.4 Rank and similarity are not standing/truth

```text
LEXICAL SCORE != SOURCE STANDING
VECTOR SIMILARITY != SOURCE STANDING
RERANK SCORE != SOURCE STANDING
MULTIPLE CHUNKS != MULTIPLE INDEPENDENT SOURCES
```

Lineage-aware dedup is required where one source has many derivative representations.

### 8.5 Source reread/currentness may be required

```text
INDEX SAYS X
!= SOURCE STILL SAYS X
```

Consequential/currentness-sensitive work may require source reread or current material-state validation before a derived retrieval candidate becomes a material Context basis.

### 8.6 Query transformations cannot redefine the need

```text
QUERY REWRITE != NEW INFORMATION NEED
QUERY EXPANSION != PURPOSE EXPANSION
GENERATED / HYPOTHETICAL QUERY REPRESENTATION != SOURCE EVIDENCE
```

Translation, decomposition, expansion or model-generated search terms must preserve the accepted InformationNeed. New material dependencies require explicit bounded need refinement under AI-03A.

---

## 9. Accepted Memory architecture principles

### 9.1 Canonical application memory already exists

DANTE's durable structured understanding of life is the accepted application/domain/database model. It is not recreated as a generic AI memory layer.

### 9.2 Memory classes remain semantically distinct

```text
CANONICAL APPLICATION MEMORY
INTERACTION MEMORY
RUN / WORKING MEMORY
COMPACTION / CHECKPOINT STATE
ADAPTIVE / DERIVED USER MEMORY
OPERATIONAL / EXPERIENCE MEMORY
PROVIDER MEMORY / THREAD / CACHE
RETRIEVAL REPRESENTATIONS
EXECUTION EVIDENCE
```

One storage technology may later support multiple classes only if their semantics/lifecycles remain explicit; one generic `Memory` ontology is not accepted.

### 9.3 Survival defaults to no

```text
DEFAULT NONCANONICAL SURVIVAL = NO
MEMORY SURVIVAL MUST BE EARNED
```

The common Survival/Admission protocol evaluates purpose, Subject/Actor/represented party, source/lineage, sensitivity, retention/future-use eligibility, validity, correction, suppression, deletion/anti-resurrection, environment applicability and whether canonical Domain state is the proper home.

### 9.4 Processing, retention and future reuse are distinct

```text
PROCESSING / RETRIEVAL ELIGIBILITY
!= RETENTION / MEMORY-ADMISSION ELIGIBILITY
!= FUTURE-REUSE ELIGIBILITY
```

A source may be usable for the current task but forbidden from durable reuse.

### 9.5 Admission does not bypass effect governance

```text
MEMORY ADMISSION DECISION
!= MEMORY WRITE PERMIT
```

Durable memory mutation requires current admission plus applicable AI-02 effect/governance authorization. Delayed writes must not rely on stale authorization.

### 9.6 Model/provider memory requests are proposals

```text
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
PROVIDER AUTOMATIC MEMORY != DANTE RETENTION AUTHORITY
```

### 9.7 Durable user-specific memory is inspectable/control-capable

Reusable personal semantic memory must preserve enough typed meaning to support appropriate source/inference status, scope/validity, correction, deactivation and deletion control.

This obligation does not turn every technical index/cache row into a user-facing profile record.

### 9.8 Memory recall is governed retrieval

```text
MEMORY EXISTS != MEMORY MAY BE USED
MEMORY RECALL = GOVERNED ACQUISITION
```

Remembered state re-enters reasoning only through current InformationNeed/purpose/policy/eligibility.

### 9.9 Derived/adaptive memory is candidate, not confirmed truth

Observed patterns or AI-derived hypotheses do not become confirmed preference/fact merely because they are useful.

Durable adaptive memory requires bounded typed semantics sufficient for correction/scope/validity/inference disposition.

### 9.10 Derived memory is not self-freshening

```text
ALL ORIGINAL SOURCE BYTES STILL VALID
!= DERIVED MEMORY STILL CURRENT
```

New material evidence can make a derived memory stale/conflicted/superseded without deleting its original sources.

### 9.11 Correction / forgetting / suppression remain distinct

```text
CORRECT
!= FORGET
!= SOURCE SUPPRESSION
!= USE SUPPRESSION
!= INFERENCE DISPOSITION
```

Inference Disposition prevents a rejected/corrected derived meaning from silently resurrecting through materially equivalent surviving basis.

### 9.12 Derivatives do not self-corroborate

```text
DERIVATIVE
!= INDEPENDENT EVIDENCE OF ITS ANCESTRY
```

Repeated model generations from the same basis cannot manufacture independent corroboration.

### 9.13 Operational experience requires verified basis

```text
PAST EXPERIENCE != POLICY
MODEL SAYS SUCCESS != VERIFIED SUCCESS
EXPERIENCE != INSTRUCTION AUTHORITY
```

Operational/Experience Memory requires adequate verified basis and bounded environment/provider/version applicability.

### 9.14 Provider memory remains replaceable

Provider thread/native memory/prompt cache can be useful optimization but not canonical DANTE state. It must be discardable/reconstructable and current-retention compatible.

### 9.15 Canonical promotion does not duplicate authority

```text
AI MEMORY CANNOT MINT CANONICAL TRUTH BY ITSELF
CANONICAL PROMOTION != DUPLICATION
```

After a memory candidate is successfully promoted into accepted Domain/application state, the old noncanonical representation must not continue as independent authority or independent corroboration.

### 9.16 Execution evidence is not user memory

Audit/evidence needed to explain effects/runtime behavior remains separate from adaptive/personal memory semantics.

---

## 10. Privacy, retention and anti-resurrection

AI-03 must provide a lifecycle in which deletion/redaction/retirement/suppression propagates to every eligible derivative.

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

The current PostgreSQL `material_state_retirement` contract and Recovery suppression model are inherited constraints, not implementation details AI-03 may ignore.

```text
RESTORED BYTES != RESTORED ELIGIBILITY
```

A restore of old bytes must not make a retired/suppressed derivative retrieval-eligible again.

Retention denial also survives future workflows: current processing does not grant a latent right to convert the same data into reusable memory later without a current eligible basis.

AI-03C strengthens the physical interpretation:

```text
RESTORED DERIVED BYTES
→ NOT SERVING-ELIGIBLE BY DEFAULT
→ verify source lifecycle / suppression / generation / basis
→ discard + rebuild OR explicitly reconcile
→ only then eligible
```

Consequential durable runtime/provider state is also fenced from resume until canonical PostgreSQL recovery/reconciliation is serving-ready and current authorization/basis/supersession has been revalidated.

---

## 11. Security requirements

AI-03 is built under security/privacy constraints from the start.

Required properties include:

```text
policy-aware discovery/acquisition
permission-safe search universe
provider-native/JIT acquisition under the same scope/policy
query-rewrite/transformation integrity
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
processing != retention != future reuse
current effect authorization for durable memory mutation
durable user-memory inspectability/control
explicit source/use/inference exclusions
Runtime Interpretation Frame where material
provider eligibility / minimisation
provider retention compatibility
surface-aware disclosure
cache re-authorization
memory poisoning resistance
retrieval poisoning resistance
derived-memory basis-currentness revalidation
canonical-promotion non-duplication
trace/eval minimisation
journal/checkpoint minimisation at durable runtime boundaries
current source-basis eligibility for durable derivatives
recovery/serving fence across canonical and durable runtime/provider/derived state
```

A later AI-04 security assurance pass attacks the concrete production design; it does not introduce these requirements for the first time.

---

## 12. Physical/materialization discipline

Current physical truth at this AI-03 checkpoint:

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

Current available retrieval capabilities include PostgreSQL native FTS, `pg_trgm`, `unaccent` and `pgvector`, but availability does not mean activation is justified.

Forbidden shortcut:

```text
AI-03B closed
→ therefore create memory tables / embeddings / vector index
```

Required sequence remains:

```text
accepted semantic need
→ closed Context/Retrieval/Memory architecture
→ AI-03C destructive whole-system validation
→ persistence/materialization classification
→ smallest justified physical design
→ normal reviewed forward migration if needed
```

AI-03C candidate discipline additionally requires:

```text
persist the obligation, not the transient blob
persistent derivative -> truthful source basis + generation identity
async derivative cleanup != current eligibility
exact eligible-universe vector baseline before ANN
representation upgrades -> explicit generation/build/validate/cutover/retire
```

No structural DB change is authorized by this document.

---

## 13. Non-goals / still-open physical technology

AI-03 has not selected:

```text
OpenAI / Anthropic / Gemini / Qwen
specific model
specific embedding model
specific vector dimension
specialist vector database
Mem0 / Zep / Graphiti / Letta or comparable framework
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
MCP/A2A implementation
```

It has also not activated:

```text
pgvector semantic retrieval
HNSW
IVFFlat
new FTS indexes
new pg_trgm indexes
Restate durable execution
R2 content storage
```

Any later selection/activation must be justified by completed AI-03C materialization evidence plus the applicable direct Physical/production proof.

---

## 14. AI-03A closure record

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

---

## 15. AI-03B closure record

Durable proof/rationale:

- `docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Closure chronology:

```text
DANTE-FIRST INTERNAL DESIGN             COMPLETE
TARGETED MODERN CHALLENGER RESEARCH    COMPLETE
RECONCILIATION                         COMPLETE
FIRST HEAVY KILL-TEST                  PASS CANDIDATE
FINAL INDEPENDENT VALIDATION           FAIL / 5 HARDENINGS
FINAL HARDENINGS                       COMPLETE
FINAL COMPOUND RETEST                  PASS
B01..B35                               ACCEPTED
```

Five final hardenings:

```text
FINAL-GAP-01 retention admission / governed memory mutation
FINAL-GAP-02 durable user-memory inspectability/control
FINAL-GAP-03 retrieval transformation/query-rewrite integrity
FINAL-GAP-04 derived-memory basis currentness
FINAL-GAP-05 canonical-promotion non-duplication
```

Final structural result:

```text
RETRIEVAL SEMANTICS                     PASS
MEMORY CLASS / LIFECYCLE SEMANTICS      PASS
PRIVACY / RETENTION BOUNDARY            PASS after hardening
QUERY-TRANSFORMATION INTEGRITY          PASS after hardening
DERIVED-MEMORY CURRENTNESS              PASS after hardening
CANONICAL PROMOTION BOUNDARY            PASS after hardening
INFERENCE RESURRECTION                  PASS
SELF-CORROBORATION                      PASS
OPERATIONAL MEMORY POISONING            PASS
PROVIDER REPLACEABILITY                 PASS
MULTI-ACTOR                             PASS
RECOVERY / ANTI-RESURRECTION            PASS

further structural gap                  NONE FOUND
new top-level AI contract               NO
Domain reopen                           NO
Logical reopen                          NO
Physical reopen                         NO
PostgreSQL/Alembic change               NO
implementation PASS                     NO
```

Do not restart generic AI-03B mega-testing merely to search indefinitely for hypothetical gaps. Reopen only if later AI-03C/production evidence reveals a concrete contradiction that cannot be resolved downstream.

---

## 16. AI-03C candidate checkpoint

Durable candidate proof/rationale:

- `docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`

Current chronology:

```text
STATE-FAMILY RECONSTRUCTION             COMPLETE
INITIAL MATERIALIZATION MATRIX          COMPLETE
TARGETED PHYSICAL RESEARCH              COMPLETE ENOUGH FOR CANDIDATE
FIRST MATERIALIZATION KILL-TEST         FAIL / HARDENING REQUIRED
MAT-01..MAT-10                          INCORPORATED
HARDENED COMPOUND RETEST                PASS CANDIDATE
FINAL INDEPENDENT AI-03C VALIDATION     PENDING
```

Current candidate result:

```text
further material structural gap         NONE FOUND after hardening
AI-03A reopen                            NO
AI-03B reopen                            NO
Domain reopen                            NO
Logical reopen                           NO
Physical target reopen                   NO
PostgreSQL/Alembic change                NONE JUSTIFIED
new generic memory table                 NO
conversation table                       NO / NOT JUSTIFIED
PostgreSQL Run table                     NO / NOT JUSTIFIED
Redis                                    NO / NOT JUSTIFIED
specialist vector DB                     NO / NOT JUSTIFIED
pgvector activation                      NOT YET
HNSW / IVFFlat                           NOT YET
FTS / pg_trgm activation                 NOT YET
Restate activation                       NOT YET
R2 activation                            NOT YET
implementation PASS                      NOT CLAIMED
```

Direct Physical proof obligations such as SC-017..SC-021, PSV-06..10, PSV-21..28B and PSV-37 remain UNEXECUTED and must not be relabeled PASS by architecture reasoning.

AI-03C remains a candidate until a fresh independent reverse-engineering tries to break MAT-01..MAT-10 and the complete materialization matrix against C01..C33, B01..B35 and current Product/Domain/Logical/Physical/PostgreSQL/Recovery truth.

---

## 17. AI-03 overall closure gate

AI-03 itself remains ACTIVE until final AI-03C validation proves:

```text
Context semantics coherent under whole-system pressure
Retrieval semantics coherent under materialized workload assumptions
Memory classes/lifecycle coherent under physical persistence choices
canonical vs derived boundary preserved
privacy / Authority / Visibility / retention preserved
source lifecycle / anti-resurrection preserved
durable runtime privacy/recovery boundary preserved
performance strategy bounded
provider state replaceable
no unjustified persistence
materialization blueprint complete
no unresolved structural contradiction
```

Only then may the project route to AI-04 Productionization Architecture.

---

## 18. Immediate next action

Current next action:

```text
AI-03C — FRESH INDEPENDENT DESTRUCTIVE VALIDATION
OF THE MATERIALIZATION BLUEPRINT CANDIDATE
```

Do **not** rebuild AI-03A or AI-03B from scratch.

Start from:

```text
AI-03A C01..C33
AI-03B B01..B35
AI-03C MAT-01..MAT-10 candidate
```

Then independently attack:

```text
M0..M9 state classification completeness
no-store defaults
Durable Execution Runtime State separation
Restate journal/checkpoint privacy
canonical/runtime/provider recovery fencing
persistent-derivative source basis
async invalidation vs current eligibility
derived-state sacrificial recovery
representation generation/cutover
exact-before-ANN retrieval strategy
permission-safe ANN/FTS behavior
adaptive inference/control durability
ContentArtifact/object/derivative separation
canonical promotion non-duplication
```

Pressure with:

```text
large structured history / high cardinality
large document corpora
permission-safe retrieval performance
approximate retrieval recall under filters
retention/future-reuse denial
correction/deletion/suppression propagation
inference disposition
material-basis drift
canonical-promotion duplicate cleanup
provider persistent state and revocation
provider failover
backup recovery / anti-resurrection
long-running Runs
query-transform semantic drift
cross-actor / represented-party isolation
privacy/cumulative inference
source retirement while derivatives exist
future stronger models / larger context windows
```

If that fresh review finds a real gap, harden the smallest affected AI-03C boundary and retest.

If it passes, AI-03C may close structurally and AI-03 overall may route to AI-04. Any actual PostgreSQL/index/provider/runtime implementation remains a separate later gate and must follow normal CP6/Alembic same-change discipline.

Do not infer implementation PASS from architecture closure.