# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **AI-03 final closure PRE-SCOPE:** `281e4cb5a6883e3c562d11db8a0ae34c7eb89d1b`
- **Current branch HEAD:** FETCH LIVE before every write

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architecture truth lives in the architecture/current-status sources below.

Repository truth outranks this handoff.

---

# 1. Resume rule

A new chat/session does **not** start a new project or reinterpret DANTE.

Resume:

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
current     AI-04 Productionization Architecture
```

Closed upstream AI architecture:

```text
AI-02.1 v0.5   CLOSED / STRUCTURALLY ACCEPTED
AI-03A         CLOSED / C01..C33
AI-03B         CLOSED / B01..B35
AI-03C         CLOSED / MAT-01..MAT-15
AI-03 overall  CLOSED / STRUCTURALLY ACCEPTED
```

Do not restart generic Context/Retrieval/Memory research or redesign without concrete contradictory downstream evidence.

---

# 2. Mandatory reading order

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
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
```

For any AI-04 conclusion touching semantics/persistence, inspect directly:

```text
North Star / Product
Domain
Whole Logical / WL-H01..WL-H12
Physical Model
CP6 PostgreSQL Persistence Constitution / ADR-010
Database System of Record / Dictionary
current Alembic / SQLAlchemy / PostgreSQL truth
Recovery / material-state-retirement / anti-resurrection
physical benchmark corpus / PSV register
```

---

# 3. Closed project state that must not be casually reopened

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN
CLOSED

LOGICAL
CLOSED / 57 OF 57 / WL-H01..WL-H12

PHYSICAL
CLOSED
PostgreSQL 18 major family accepted
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

RECOVERY
CP01–CP07 LOCAL PASS / CLOSED / integrated
material_state_retirement materialized
suppression / anti-resurrection semantics active
remote provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

AI work consumes these contracts.

Do not reopen them because a model/provider/vector DB/memory framework prefers another ontology or persistence shape.

---

# 4. Repository engineering standard

```text
repository-first truth
semantic correctness before framework convenience
maximum quality != maximum abstraction
bounded contracts over universal meta-models
no ceremonial services/tables/modules
simple deterministic path stays simple
provider/model/runtime remain replaceable
privacy/security/retention are design inputs
historical truth preserved
unknown/absence/ambiguity explicit
architecture acceptance != implementation PASS
```

Rejected recurring shortcuts:

```text
universal Entity / Thing
universal Relationship edge
canonical EAV/property bag
generic Fact/Memory ontology
generic Repository[T]
service-locator architecture
raw ORM/SQL authority exposed to model
microservice per architecture box
table per architecture noun
vector/search/provider state as canonical truth
```

Any future structural DB change requires the normal same-change package:

```text
forward Alembic
+ SQLAlchemy mapping/metadata
+ Database Dictionary
+ human DB reference
+ generated artifacts where applicable
+ direct tests
+ affected recovery assertions
+ current docs
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
CLOSED / STRUCTURALLY ACCEPTED

  AI-03A — FULL CONTEXT ARCHITECTURE
  CLOSED / C01..C33

  AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
  CLOSED / B01..B35

  AI-03C — DESTRUCTIVE VALIDATION + MATERIALIZATION BLUEPRINT
  CLOSED / MAT-01..MAT-15

AI-04 — PRODUCTIONIZATION ARCHITECTURE
CURRENT / NEXT

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE
```

Security, privacy, simulations and evals remain cross-cutting.

---

# 6. AI-02.1 accepted runtime baseline

Durable authority:

`docs/architecture/dante-ai-02-1-intelligence-reengineering.md`

Accepted responsibility map includes:

```text
Interaction Edge
Interaction Session
Work Intake / WorkContract / Supersession
Reference / Target Resolution
ConsequenceProfile
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
ModelTarget / HarnessProfile
Deterministic Compute / Solver
Capability Runtime
Execution Environment
Verifier
Policy mesh
ChangeSet / EffectGraph
Effect Runtime
Application / Domain boundary
Result Maturity
Disclosure / Safe Result Publication
Attention
```

Do not infer services/tables from responsibility boxes.

---

# 7. AI-03A closure

Durable authority:

`docs/architecture/dante-ai-03a-full-context-architecture.md`

Accepted contracts:

```text
ContextPlan
InformationNeed
ContextStrategy
ContextFragment
ContextReadiness
ConsumerContext
ContextManifest
```

Core binding:

```text
Context != canonical reality
Context != Memory != Retrieval
no universal RAG
DATA != INSTRUCTION
Interaction Session != provider continuity
Reality Scope != Runtime Interpretation Frame
provider-native/JIT acquisition remains governed
acquisition authority != effect authority
derivation may tighten sensitivity
assembled context != established effective provider exposure
```

C01..C33 accepted.

---

# 8. AI-03B closure

Durable authority:

`docs/architecture/dante-ai-03b-retrieval-memory-architecture.md`

Additional contracts:

```text
RetrievalPlan
RetrievalCandidate
```

Retrieval:

```text
least-complex adequate route
EXACT / BOUNDED_COMPLETE / BEST_EFFORT / APPROXIMATE / SAMPLED
APPROXIMATE != COMPLETE
candidate count != coverage proof
eligibility defines search universe
rank/similarity != standing
index/cache/embedding != source
```

Memory:

```text
canonical application memory = Domain/PostgreSQL
noncanonical survival defaults NO
processing != retention != future reuse
memory recall = governed acquisition
model remember-request != admission
admission != durable write permit
Correction != Forgetting != Source Suppression
           != Use Suppression != Inference Disposition
self-corroboration forbidden
operational experience requires verified basis
provider memory replaceable
canonical promotion does not duplicate authority
```

B01..B35 accepted.

---

# 9. AI-03C closure

Durable authority:

`docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md`

Final materialization model:

```text
SEMANTIC AUTHORITY
!= FUNCTIONAL ROLE
!= SURVIVAL DISPOSITION
!= PHYSICAL OWNER/LOCATION
!= CURRENT ELIGIBILITY
```

Default:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
```

Key posture:

```text
ContextPlan / InformationNeed / RetrievalPlan /
RetrievalCandidate / ContextFragment / ConsumerContext
→ NO-STORE runtime

ordinary interaction/work/run state
→ transient

Class-B durable execution
→ Restate only when a real consumer triggers it

Class-A durable technical coordination
→ transactional outbox when real async external/publication need exists

rebuild/invalidation cursor, generation selector,
provider binding/locator
→ bounded technical coordination only when activated need exists

adaptive inference
→ recompute default

user suppression/retention/inference control
→ durable truthful governance owner

provider state
→ replaceable optimization

OCR/chunks/summaries/FTS/embeddings/ANN
→ source-linked derived retrieval plane

one-shot upload
→ no forced ContentArtifact

reusable raw bytes
→ object storage only with proper content lifecycle

semantic reconciliation obligation
→ proper Domain/application owner

technical provider receipt/trace
→ separate evidence
```

---

# 10. MAT-01..MAT-15

```text
MAT-01  architecture contract != persistence owner; default no-store
MAT-02  durable execution state != PostgreSQL/derived/provider state
MAT-03  durable journal is privacy surface; minimize payload
MAT-04  user control durability != derivative durability
MAT-05  persistent derivative requires truthful source basis + generation
MAT-06  async invalidation != current eligibility authority
MAT-07  recomputable derivative is sacrificial during recovery
MAT-08  runtime/provider/derived recovery cannot outrun canonical recovery
MAT-09  ANN is optimization; exact eligible-universe baseline first
MAT-10  representation generations do not mix silently
MAT-11  semantic authority/function/survival/owner/eligibility are orthogonal
MAT-12  durable technical coordination is its own role;
        Class-A outbox != Class-B Restate;
        convergence cannot rely only on one-shot invalidation
MAT-13  scalable basis envelope allowed;
        MaterialStateRef != MVCC/LSN/hash/digest
MAT-14  build/catch-up/readiness/atomic generation cutover;
        invocation/cache generation binding; recovery coherence check
MAT-15  semantic obligation != execution/audit evidence
```

---

# 11. Search/vector/runtime activation stance

No activation is implied by architecture closure.

Lexical:

```text
structured/exact
→ owner/query-specific lexical/fuzzy
→ application merge
→ unified projection only with measured evidence
```

Vector:

```text
no real consumer → no vector path
→ source-linked embedding if value exists
→ EXACT nearest-neighbor baseline in eligible universe
→ benchmark
→ ANN comparison only if exact insufficient
→ HNSW/IVFFlat only after direct proof
```

Restate/R2/PowerSync/provider state remain trigger-bound.

---

# 12. Direct proof obligations remain UNEXECUTED

Architecture closure must not be confused with these future proofs:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query correctness
PSV-08 / SC-019 vector recall after real filtering
PSV-09 / SC-020 projection freshness/material-basis behavior
PSV-10 / SC-021 deletion/redaction propagation
PSV-21..28B durable execution / Restate / journal privacy / recovery
PSV-37 pgvector source/model/freshness provenance
```

No implementation or production PASS is claimed.

---

# 13. AI-03 closure chronology

```text
AI-03A
first test FAIL / 9 hardenings
→ independent test / +4
→ C01..C33 PASS

AI-03B
internal design + targeted research
→ candidate
→ independent validation FAIL / +5
→ B01..B35 PASS

AI-03C
materialization reconstruction + targeted physical research
→ first kill-test FAIL
→ MAT-01..10
→ PASS candidate
→ independent reverse-engineering FAIL / +5
→ MAT-11..15
→ final compound PASS
```

Final:

```text
AI-03A CLOSED
AI-03B CLOSED
AI-03C CLOSED
AI-03 CLOSED / STRUCTURALLY ACCEPTED
```

No Domain/Logical/Physical-target/PostgreSQL-Constitution reopen.
No DB migration.
No new table/index.
No provider/model selection.

---

# 14. Current work — AI-04

AI-04 is **Productionization Architecture**.

It must consume AI-02.1 + AI-03 closures rather than redesign them.

Expected concerns include concrete production choices and contracts for:

```text
provider/model/gateway posture
HarnessProfile implementation boundary
streaming/realtime/cancel behavior
capability/tool runtime
execution isolation
Restate activation contract where justified
object/content execution boundary
security/secrets/provider credentials
observability vs audit vs eval separation
model/retrieval/effect evaluation architecture
cost/latency/resource budgets
failure/degradation/fallback policy
provider failover
privacy/retention/provider data handling
release/deployment/rollback/incident posture
concrete activation gates for dormant capabilities
```

AI-04 must not activate technologies merely to make the architecture look complete.

---

# 15. Exact safe next action

Before doing AI-04 design:

1. fetch live branch HEAD;
2. read `docs/ROADMAP.md`, `docs/PROJECT-STATUS.md` and AI workstream authority;
3. read AI-02.1 and AI-03 closure documents;
4. reconstruct AI-04 acceptance criteria from current repository truth;
5. separate what can be decided architecturally now from what requires benchmark/implementation evidence;
6. use fresh web research for current provider/runtime/security/production details where material;
7. do not reopen AI-03 unless a concrete contradiction appears;
8. do not implement provider/DB/runtime changes without a separate exact gate.

---

# 16. Git write-gate discipline

Before every new remote write:

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
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<out of scope>
```

Re-fetch HEAD immediately before first write. If it differs, STOP and re-gate.

After writes compare PRE-SCOPE..HEAD and prove exact path classification/no scope creep.

---

# 17. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.
