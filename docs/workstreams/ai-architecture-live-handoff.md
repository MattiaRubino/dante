# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-03 — Context / Retrieval / Memory
- **AI-03A:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE / 13 HARDENINGS / C01..C33
- **AI-03B:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE / 5 FINAL HARDENINGS / B01..B35
- **AI-03C:** CANDIDATE / FIRST MATERIALIZATION KILL-TEST FAIL / MAT-01..MAT-10 / HARDENED RETEST PASS / FINAL INDEPENDENT VALIDATION PENDING
- **Current macro-phase:** AI-03C — Fresh Independent Destructive Validation of the Materialization Blueprint
- **Created:** 2026-09-01
- **Refreshed:** 2026-09-02
- **Approved AI-03C materialization PRE-SCOPE:** `0ca142f984db71f40f2cb8a31c0a3929bb1e172e`
- **AI-03C candidate document commit:** `b48b62e15f3bf41d036a419a46263618694c0b29`
- **AI-03 charter alignment commit:** `66835d4cccd159b446ac78d976d698f5c46b3498`
- **Current branch HEAD:** fetch live before every write; this handoff refresh itself advances HEAD beyond the checkpoint above

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architectural truth lives in the architecture/current-status sources below.

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
current     AI-03C fresh independent destructive validation
```

Do not recreate AI-00, AI-01, AI-02, AI-03A or AI-03B from scratch.

Treat:

```text
AI-03A C01..C33
AI-03B B01..B35
```

as closed upstream architecture unless a concrete downstream contradiction genuinely requires reopening the smallest affected boundary.

Treat:

```text
AI-03C MAT-01..MAT-10
```

as a **candidate hardened materialization contract pending independent validation**, not as accepted closure yet.

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
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
```

For AI-03C conclusions touching semantics or persistence, inspect directly:

```text
North Star / Product contracts
Domain concepts
Whole Logical / WL-H01..WL-H12
Physical Model
PostgreSQL Persistence Constitution / ADR-010
Database System of Record / Dictionary
current Alembic / SQLAlchemy / PostgreSQL truth
Recovery / material-state-retirement / anti-resurrection contracts
Physical benchmark scenario corpus
post-selection validation register
```

Repository truth beats conversation memory.

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

LOCAL RECOVERY
CP01–CP07 PASS / CLOSED / integrated
material_state_retirement materialized
suppression / anti-resurrection semantics active
remote provider TBD / not activated
production/cloud recovery not claimed
```

Do not reopen these because an AI/search/memory framework prefers another ontology, storage shape or state graph.

---

# 4. Repository engineering standard

The operating standard remains:

```text
repository-first truth
semantic correctness before framework convenience
maximum quality != maximum abstraction
bounded contracts over universal meta-models
no ceremonial services/tables/modules
simple deterministic path stays simple
provider/model/runtime remain replaceable
privacy/security/retention are design inputs
historical truth is preserved
unknown/absence/ambiguity remain explicit
architecture acceptance != implementation PASS
```

Rejected shortcuts include:

```text
universal Entity / Thing
universal Relationship edge
canonical EAV/property bag
generic Fact/Memory ontology
generic AI memory table
one table for every architecture noun
raw ORM/SQL authority exposed to model
vector/search/provider state as canonical truth
```

Any future structural DB change must use normal same-change discipline:

```text
forward Alembic migration
+ SQLAlchemy mapping/metadata
+ Database Dictionary
+ human DB reference
+ governed generated artifacts where applicable
+ direct tests
+ affected recovery/operational assertions
+ current documentation
```

Applied migrations are immutable.

---

# 5. Compact AI roadmap

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
  CLOSED / C01..C33

  AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
  CLOSED / B01..B35

  AI-03C — DESTRUCTIVE VALIDATION + MATERIALIZATION BLUEPRINT
  CANDIDATE / MAT-01..MAT-10
  HARDENED RETEST PASS
  FINAL INDEPENDENT VALIDATION PENDING

AI-04 — PRODUCTIONIZATION ARCHITECTURE
FUTURE

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE
```

Security, privacy, simulations and evals are cross-cutting throughout; later stages validate concrete mechanisms rather than introducing those concerns for the first time.

---

# 6. AI-02.1 accepted runtime baseline

Durable authority:

```text
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
```

Important accepted distinctions:

```text
Interaction Session != Run != Worker
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION
FRESH INPUTS != AUTOMATICALLY COHERENT BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
DATA != INSTRUCTION
```

Restate remains the selected Physical target for genuine Class-B durable execution; selection is not activation.

---

# 7. AI-03A — CLOSED

Durable authority:

```text
docs/architecture/dante-ai-03a-full-context-architecture.md
```

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

plus AI-02 `BasisManifest`.

Closure:

```text
initial candidate FAIL
→ 9 hardenings
→ first structural PASS candidate
→ independent kill-test
→ 4 additional hardenings
→ final compound retest PASS
→ C01..C33 accepted
```

Important late hardenings include:

```text
governed provider/JIT acquisition
acquisition authorization != effect authorization
derived-sensitivity closure
Runtime Interpretation Frame
assembled ConsumerContext != established consumer exposure
```

No Domain/Logical/Physical/PostgreSQL reopen was required.

---

# 8. AI-03B — CLOSED

Durable authority:

```text
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
```

Additional runtime contracts:

```text
RetrievalPlan
RetrievalCandidate
```

Core rules:

```text
USE LEAST-COMPLEX ADEQUATE RETRIEVAL ROUTE
APPROXIMATE != COMPLETE
candidate count != coverage proof
eligible search universe is governed before ranking
rank / similarity / rerank != Source Standing
index/cache/embedding != source
multiple derivatives != independent corroboration
source reread/current-state validation may be required
```

Memory classes remain distinct:

```text
Canonical Application Memory = Domain/PostgreSQL
Interaction Memory
Run / Working Memory
Compaction / Checkpoint
Adaptive / Derived User Memory
Operational / Experience Memory
Provider Memory / Thread / Cache
Retrieval Representations
Execution Evidence
```

Survival/control rules:

```text
DEFAULT NONCANONICAL SURVIVAL = NO
MEMORY SURVIVAL MUST BE EARNED
PROCESSING != RETENTION != FUTURE REUSE
MEMORY ADMISSION != MEMORY WRITE PERMIT
MEMORY RECALL = GOVERNED ACQUISITION
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
PROVIDER MEMORY != DANTE RETENTION AUTHORITY
CORRECT != FORGET != SOURCE SUPPRESSION
        != USE SUPPRESSION != INFERENCE DISPOSITION
DERIVED MEMORY IS NOT SELF-FRESHENING
CANONICAL PROMOTION != DUPLICATE AUTHORITY
```

Final independent validation found 5 real gaps, incorporated them, and the final compound retest passed. B01..B35 are accepted.

---

# 9. AI-03C materialization candidate

Durable candidate authority:

```text
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
```

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

The first kill-test did **not** reveal a contradiction in C01..C33 or B01..B35. It exposed physical survival/recovery boundaries that become visible only when accepted architecture is mapped onto durable mechanisms.

---

# 10. AI-03C physical classes M0..M9

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

Important consequence:

```text
DURABLE EXECUTION RUNTIME STATE
```

is a distinct physical class. It is not canonical PostgreSQL and not derived memory. Restate is the selected Physical target when real Class-B work activates this requirement.

---

# 11. Current materialization matrix

```text
ContextPlan                       M1 / NO STORE
InformationNeed                   M1 / NO STORE
RetrievalPlan                     M1 / NO STORE
RetrievalCandidate                M1 / NO STORE
ContextFragment                   M1 / NO STORE
ConsumerContext                   M1 / NO STORE
query rewrite / HyDE-like state   M1/M3 / NO STORE default
model scratch/reasoning           M1 / NO STORE
Interaction continuity            M1 default
full conversation persistence     M9 / NOT JUSTIFIED
ordinary WorkContract/Run         M1 default
Class-B resumable work            M2 / Restate target when activated
checkpoint/compaction             minimal M1/M2/M3; not source
ContextManifest                   M7 selective/minimal only
BasisManifest                     M7 selective/minimal only
confirmed user fact/preference    M0 proper Domain owner
adaptive inferred pattern         M3 default / M4 only if earned
user inference/use suppression    M0 governance durability
operational experience            M3 default / M4 only if earned
provider thread/cache/memory      M5 replaceable
OCR/extracted text                M3/M6 recomputable
chunks/spans                      M3/M6 recomputable
hierarchical summary              M3/M6 recomputable
FTS/trigram                       M6 query-specific if justified
embeddings                        M6 / NOT ACTIVATED
HNSW / IVFFlat                    M6 optimization / NOT ACTIVATED
retrieval cache                   disposable default
reusable raw Artifact bytes       M8 / object storage when vertical requires
ContentArtifact identity/metadata M0 canonical owner
transient upload                  M1/M9; no forced Artifact identity
consequential effect evidence     M7 minimal durable evidence
Scenario Workspace               M1 default
saved scenario                    promote to existing Possibility/Proposal/Plan/etc.
```

Do not infer that a closed Domain concept means every specialist table already exists in the current 69-table schema.

---

# 12. AI-03C MAT-01..MAT-10

```text
MAT-01
ARCHITECTURE CONTRACT != PERSISTENCE OWNER.
DEFAULT NONCANONICAL PERSISTENCE = NO.

MAT-02
DURABLE EXECUTION RUNTIME STATE
is its own physical class.
Restate != PostgreSQL != derived memory.

MAT-03
DURABLE JOURNAL != PRIVACY-FREE RUNTIME.
Journal/checkpoint payload minimisation is mandatory.

MAT-04
USER CONTROL / SUPPRESSION / INFERENCE DISPOSITION
must not be disposable merely because the governed derivative is.

MAT-05
PERSISTENT DERIVATIVE REQUIRES
truthful source basis + transformation/generation identity.

MAT-06
ASYNC INVALIDATION
!= CURRENT ELIGIBILITY AUTHORITY.

MAT-07
RECOMPUTABLE DERIVED STATE
is sacrificial during recovery and cannot serve until rebuilt/reconciled.

MAT-08
RUNTIME / PROVIDER / DERIVED RECOVERY
cannot outrun canonical PostgreSQL recovery/reconciliation readiness.

MAT-09
ANN IS AN OPTIMIZATION, NOT A RETRIEVAL PREREQUISITE.
Exact eligible-universe baseline precedes ANN activation.

MAT-10
DERIVED REPRESENTATION GENERATIONS MUST NOT MIX SILENTLY.
Embedding/OCR/chunk/FTS/summary/etc. upgrades need explicit generation/cutover.
```

---

# 13. Durable-runtime privacy and recovery

Do not journal full private runtime context merely for convenience.

Default rejection/minimisation applies to:

```text
full ConsumerContext
full private prompt
raw sensitive documents
entire transcript
unbounded tool outputs
raw privileged credentials
```

Prefer:

```text
bounded refs
minimal typed DTOs
operation/effect identifiers
expected-state bindings
small receipts/digests
minimum resume checkpoint
```

Recovery rule:

```text
RUNTIME RECOVERY != CANONICAL RECOVERY
```

Consequential resume must wait for canonical recovery/reconciliation serving readiness and then reread/revalidate current:

```text
source/canonical state
AuthZ
Consent
Visibility
represented party
Work Supersession/cancellation
expected MaterialState/basis
```

---

# 14. Derived-state lifecycle / recovery

A persistent derivative must preserve enough basis to establish:

```text
source identity/location
source reality class
source MaterialState/revision/snapshot basis where truthful
transformation/generation
purpose/security/retention scope where material
creation/derivation time
current lifecycle/eligibility
```

Never invent `MaterialStateRef` for an external/provider/index revision that is not a real semantic material state.

If durable basis cannot be established sufficiently:

```text
DO NOT PERSIST THE DERIVATIVE
```

Recovery:

```text
RESTORED DERIVED BYTES
!= RESTORED ELIGIBILITY

restore canonical candidate
→ reconciliation / serving readiness
→ derived state non-serving by default
→ verify source lifecycle / suppression / generation / basis
→ discard+rebuild OR explicitly reconcile
→ eligible only afterward
```

Async worker cleanup is allowed, but stale rows/index entries do not become eligible merely because cleanup has not run yet.

---

# 15. Search / pgvector / ANN current stance

PostgreSQL already has FTS, pg_trgm, unaccent and pgvector available, but none is globally activated by AI-03C.

Lexical progression:

```text
structured/exact first
→ owner/query-specific lexical search when needed
→ application merge when adequate
→ unified search projection only if measured evidence justifies it
```

Vector progression:

```text
PHASE 0 no vector path without a real consumer
PHASE 1 source-linked embedding only if semantic retrieval adds value
PHASE 2 EXACT nearest-neighbor baseline inside eligible universe
PHASE 3 direct correctness/latency/resource benchmark
PHASE 4 compare ANN only when exact becomes insufficient
PHASE 5 HNSW/IVFFlat only after recall/security/recovery/resource proof
```

Binding:

```text
ANN IS AN OPTIMIZATION
NOT A RETRIEVAL PREREQUISITE
```

No embedding model, dimension, metric, HNSW/IVFFlat parameters or specialist vector DB has been selected.

Representation upgrades use explicit generations; silent mixing is rejected.

---

# 16. Physical benchmark obligations remain UNEXECUTED

Architecture reasoning does not turn these into PASS:

```text
PSV-06 / SC-017 hidden-result non-interference
PSV-07 / SC-018 FTS mixed filter/query correctness
PSV-08 / SC-019 vector recall after real filtering
PSV-09 / SC-020 projection freshness/material-basis behavior
PSV-10 / SC-021 deletion/redaction propagation

PSV-21..28B durable execution / Restate
including journal privacy, recovery and deployment-mode obligations

PSV-37 pgvector model/source/freshness provenance
```

Physical synthetic retrieval tiers remain benchmark envelopes, not forecasts:

```text
LOW   ~100k searchable chunks
BASE  ~5M
HIGH  ~50M
```

---

# 17. Current AI-03C candidate verdict

```text
FURTHER MATERIAL STRUCTURAL GAP      NONE FOUND after MAT-01..10
AI-03A REOPEN                        NO
AI-03B REOPEN                        NO
DOMAIN REOPEN                        NO
LOGICAL REOPEN                       NO
PHYSICAL TARGET REOPEN               NO
NEW TOP-LEVEL AI CONTRACT            NO
NEW GENERIC MEMORY TABLE             NO
GENERIC SEARCH TABLE                 NO / NOT JUSTIFIED
CONVERSATION TABLE                   NO / NOT JUSTIFIED
POSTGRESQL RUN TABLE                 NO / NOT JUSTIFIED
REDIS                                NO / NOT JUSTIFIED
SPECIALIST VECTOR DB                 NO / NOT JUSTIFIED
PGVECTOR ACTIVATION                  NOT YET
HNSW / IVFFlat                       NOT YET
FTS / pg_trgm ACTIVATION             NOT YET
RESTATE ACTIVATION                   NOT YET
R2 ACTIVATION                        NOT YET
POSTGRESQL/ALEMBIC CHANGE            NONE JUSTIFIED
IMPLEMENTATION PASS                  NOT CLAIMED
```

This is still a **PASS CANDIDATE**. Do not call AI-03C or AI-03 closed until the fresh independent validation passes.

---

# 18. Exact next action

Do not start AI-04 yet.

Next:

```text
FRESH INDEPENDENT AI-03C REVERSE-ENGINEERING / KILL-TEST
```

Independently attack the candidate rather than confirming it.

Start from:

```text
AI-03A C01..C33
AI-03B B01..B35
AI-03C MAT-01..MAT-10 candidate
M0..M9 classification
```

Pressure at minimum:

```text
classification completeness / overlap
no-store defaults
Durable Execution Runtime State boundary
journal/checkpoint privacy
PostgreSQL/Restate/provider recovery mismatch
persistent derivative basis loss
async invalidation race
source retirement while derivatives survive
representation-generation cutover
exact-before-ANN validity
ANN recall after security filters
hidden-result non-interference
adaptive-inference suppression resurrection
canonical promotion duplicate authority
ContentArtifact/object/derivative boundary
multi-actor/represented-party switching
Consent/Visibility/AuthZ revocation mid-Run
large history / large corpora
provider failover
future stronger models / larger context windows
```

If a real gap appears:

```text
harden smallest affected AI-03C boundary
→ rerun compound matrix
```

If no unresolved structural contradiction remains:

```text
close AI-03C structurally
→ close AI-03 overall
→ route to AI-04 Productionization Architecture
```

Any actual PostgreSQL/index/provider/runtime implementation remains a separate later gate.

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
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<out of scope>
```

Then re-fetch live branch HEAD immediately before the first write.

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
read back current status/routing
never claim implementation PASS from documentation-only work
```

---

# 20. Handoff lifecycle

This file is **temporary**.

Before `feature/ai-architecture` is integrated into protected `main`:

```text
classify meaningful handoff content
→ propagate durable current truth/rationale/evidence
→ verify knowledge coverage
→ DELETE THIS LIVE HANDOFF
```

Temporary handoff count entering protected `main` must be zero.
