# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-04 — Productionization Architecture
- **AI-04A:** CANDIDATE MATERIALIZED / DIRECT DANTE EVAL SPECIFICATION CURRENT
- **AI-03A:** CLOSED / C01..C33
- **AI-03B:** CLOSED / B01..B35
- **AI-03C:** CLOSED / MAT-01..MAT-15
- **AI-03 overall:** CLOSED / STRUCTURALLY ACCEPTED
- **Refreshed:** 2026-09-02
- **AI-04A materialization PRE-SCOPE:** `aff3d7153aa0c4cf99d4bc28f569bc3db2e82703`
- **AI-04A candidate commit:** `3aef3ec593f6b40d8f22379df75ae84b423c6747`
- **AI-04A durable-workstream checkpoint:** `af6b13705397f6c871afab0478edb824f8b45b32`
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
next        AI-04A Direct DANTE Eval Specification
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
docs/architecture/dante-ai-04-productionization-architecture.md
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
CURRENT

  AI-04A — EVAL / MODEL / PROVIDER PRODUCTIONIZATION BOUNDARY
  CANDIDATE MATERIALIZED
  DIRECT DANTE EVAL SPECIFICATION CURRENT

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

# 14. AI-04A current candidate

Durable authority:

`docs/architecture/dante-ai-04-productionization-architecture.md`

The initial AI-04 productionization boundary is now materialized.

## 14.1 Workload-first eval matrix

```text
DANTE-E01  model avoidance / deterministic fast path
DANTE-E02  intent + reference / target resolution
DANTE-E03  structured extraction / understanding
DANTE-E04  native query + history + absence semantics
DANTE-E05  context + privacy + Reality Scope
DANTE-E06  planning / replanning / scenario reasoning
DANTE-E07  document / long-context / multimodal reasoning
DANTE-E08  tool / capability use
DANTE-E09  consequential effect preparation/execution boundary
DANTE-E10  multi-actor / delegation / disclosure
DANTE-E11  adaptive memory / learning
DANTE-E12  currentness / failure / supersession / failover
DANTE-E13  open-world research / grounding
```

Trigger-gated until real product need:

```text
voice/realtime
browser/computer-use
code execution
durable background work
embedding/vector retrieval
specialized generation
```

## 14.2 Hard gates

A weighted quality score cannot compensate for:

```text
wrong consequential target
unauthorized effect
private/cross-actor disclosure
fabricated canonical fact
false effect success
false Actual/completion
stale/superseded result published as current
Reality Scope laundering
invalid memory promotion
blind failover to an ineligible provider
source/derivative resurrection
```

Hard eligibility precedes graded quality/latency/economics.

## 14.3 Provider boundary

Binding:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != PROVIDERS IDENTICAL
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

Production chain:

```text
DANTE work/capability need
→ ModelTarget
→ HarnessProfile
→ ProviderBinding
→ ProviderAdapter
→ concrete serving platform / model / deployment
```

This deliberately supports cases such as direct provider versus cloud-hosted deployment without rewriting DANTE semantics.

## 14.4 Evaluation tracks

```text
CORE PORTABILITY TRACK
same DANTE semantic obligation
+ provider-specific HarnessProfile allowed

PROVIDER-NATIVE AUGMENTATION TRACK
native search/files/cache/state/background/browser/computer/etc.
```

Do not force lowest-common-denominator provider use, and do not treat native feature quality as portability proof.

## 14.5 Binding eligibility

```text
FEATURE AVAILABLE != FEATURE ELIGIBLE
```

Provider-native persistence/state/cache/files/background/tools require WorkContract/data/purpose/retention/region/third-party eligibility.

## 14.6 Failover

```text
PRIMARY FAIL
→ alternate binding qualification
→ fresh provider/data eligibility
→ rebuild/minimize ConsumerContext if needed
→ alternate HarnessProfile
→ invoke
```

Failover is never blind replay.

## 14.7 Economics

Use:

```text
EFFECTIVE COST PER SUCCESSFUL DANTE TASK
```

including tokenization, thinking, cache, native tools/search, retries, failures and fallbacks.

## 14.8 Current official-source landscape snapshot

As of the AI-04A research pass on 2026-09-02, current official documentation supports evaluating candidate families including:

```text
OpenAI direct / Azure OpenAI
→ GPT-5.6 Sol / Terra / Luna

Anthropic direct / qualified alternate hosting
→ Claude Opus 5 / Sonnet 5 / cost-tier candidates

Google Gemini
→ Gemini 3.7 Flash stable/GA
→ Gemini 3.5 Flash-Lite cost candidate
→ preview models challenger-only unless separately qualified
```

Provider-native retention/state differences are material inputs to binding eligibility. The landscape is version-sensitive and must be rechecked before final selection.

## 14.9 AI-04A candidate hardenings

Initial conceptual kill-test hardened:

```text
same-prompt fairness fallacy
model-judge truth ownership
native-tool vs portability conflation
model vs serving-platform qualification conflation
cheap-failure weighted-score problem
preview winner production promotion
feature-available therefore feature-use
blind failover
floating alias drift
missing no-model route
needle-only long-context testing
list-price economics
```

Durable candidate invariants: `A01..A22`.

No concrete provider/model/default/routing decision is accepted yet.

---

# 15. Exact safe next action

Current exact task:

```text
AI-04A — DIRECT DANTE EVAL SPECIFICATION
```

Required next sequence:

```text
DANTE-E01..E13
→ executable-grade fixture definitions
→ expected-state / hard-fail contracts
→ deterministic vs rubric grading rules
→ development / validation / held-out regression split
→ candidate ModelTarget hypotheses
→ small current candidate model/binding set
→ freeze exact model snapshot + serving binding + HarnessProfile
→ direct benchmark/proof where decision-relevant
→ compare hard failures + quality + latency + effective cost
→ provider/model/routing/fallback candidate
```

Do **not** select OpenAI/Azure/Anthropic/Gemini from public benchmark reputation alone.

After the provider/eval boundary has real evidence, continue AI-04 concrete runtime/capabilities and security/privacy/control-plane/operations architecture before AI-04 closure.

Do not start AI-05 or production implementation yet.

---

# 16. AI-04 current non-claims

```text
AI-04 CLOSED                         NO
DIRECT DANTE EVAL PASS               NO
PROVIDER SELECTED                    NO
MODEL DEFAULT SELECTED               NO
MULTI-PROVIDER REQUIRED              NO
PROVIDER SDK SELECTED                NO
AI BACKEND IMPLEMENTED               NO
POSTGRESQL/ALEMBIC CHANGED           NO
NEW AI TABLE/INDEX                   NO
PGVECTOR/ANN ACTIVATED               NO
FTS/PG_TRGM ACTIVATED                NO
RESTATE ACTIVATED                    NO
R2 ACTIVATED                         NO
MCP/A2A IMPLEMENTED                  NO
EXECUTION ENVIRONMENT IMPLEMENTED    NO
SC/PSV DIRECT PROOFS EXECUTED        NO
```

---

# 17. Git write-gate discipline

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

# 18. Handoff lifecycle

This file is temporary and **MUST NOT MERGE TO PROTECTED `main`**.

Before branch integration:

```text
classify meaningful handoff content
→ propagate durable truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS FILE
```

Temporary handoff count entering protected main must be zero.