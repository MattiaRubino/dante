# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** DANTE AI architecture
- **Current phase:** AI-03 — Context / Retrieval / Memory
- **AI-03A:** CLOSED / STRUCTURALLY ACCEPTED / FINAL REVALIDATION COMPLETE / 13 HARDENINGS / C01..C33
- **AI-03B:** CLOSED / STRUCTURALLY ACCEPTED / FINAL INDEPENDENT VALIDATION COMPLETE / 5 FINAL HARDENINGS / B01..B35
- **Current macro-phase:** AI-03C — Destructive Validation + Materialization Blueprint
- **Created:** 2026-09-01
- **Refreshed after AI-03B closure:** 2026-09-01
- **PRE-SCOPE for AI-03B final hardening/closure:** `9e8e0fd92733e1b54d5a69b981a11e0a1874d1f0`
- **AI-03B closure document commit:** `0c8fbda577f4625dc188c8808d43770d8e370b70`
- **AI-03 charter alignment checkpoint:** `5935e2c276edaa8df59786484c71fdcf1901599d`
- **Current branch HEAD:** fetch live before every write; this handoff refresh itself advances HEAD beyond the checkpoint above

This file exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architectural truth lives in the architecture/current-status sources named below.

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
current     AI-03C Destructive Validation + Materialization Blueprint
```

Do not recreate AI-00, AI-01, AI-02, AI-03A or AI-03B from scratch.

Treat:

```text
AI-03A C01..C33
AI-03B B01..B35
```

as closed upstream architecture unless a concrete downstream contradiction genuinely requires reopening the smallest affected boundary.

Do not treat the old exploratory AI-00..AI-12 planning sequence as current routing.

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

Reopen only the smallest affected boundary when real contradictory evidence requires it.

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
privacy/security/retention are design inputs, not late polish
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
  FINAL REVALIDATION COMPLETE / 13 HARDENINGS / C01..C33

  AI-03B — RETRIEVAL + MEMORY ARCHITECTURE
  CLOSED / STRUCTURALLY ACCEPTED
  FINAL INDEPENDENT VALIDATION COMPLETE
  5 FINAL HARDENINGS / B01..B35

  AI-03C — DESTRUCTIVE VALIDATION + MATERIALIZATION BLUEPRINT
  ACTIVE / CURRENT

AI-04 — PRODUCTIONIZATION ARCHITECTURE
FUTURE

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE
```

Security, privacy, simulations and evals are cross-cutting disciplines throughout the design. Later passes validate concrete design; they do not introduce those concerns for the first time.

---

# 6. AI-02.1 accepted runtime baseline

Durable authority:

```text
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
```

AI-02.1 v0.5 is CLOSED / STRUCTURALLY ACCEPTED.

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

Key runtime invariants include:

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
DANTE representation != external SoR authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX
FRESH INPUTS != AUTOMATICALLY COHERENT BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
DATA != INSTRUCTION
```

AI-02 closure is architecture acceptance only, not runtime/provider implementation PASS.

---

# 7. AI-03A — CLOSED

Durable authority:

```text
docs/architecture/dante-ai-03a-full-context-architecture.md
```

Accepted definition:

> DANTE Context is a purpose-bound, consumer-specific and currently eligible runtime projection of source-linked information and execution configuration assembled to satisfy explicit InformationNeeds for bounded work. Context is not canonical reality, persistent memory, a chat transcript, a retrieval index or a copy of everything DANTE knows.

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

Closure chronology:

```text
INITIAL CANDIDATE
FAIL
→ 9 initial hardenings
→ structural PASS candidate
→ independent reverse-engineering / second kill-test
→ 4 additional hardenings
→ final compound retest PASS
→ C01..C33 accepted
```

The 13 hardenings include:

```text
GAP-01 Reality Scope / scenario binding
GAP-02 Interaction continuity != provider-context continuity
GAP-03 model-discovered need scope ceiling
GAP-04 explicit reference-resolution requirement
GAP-05 negative Context constraints
GAP-06 child/delegated minimisation
GAP-07 instruction provenance / DATA != INSTRUCTION
GAP-08 readiness non-monotonicity
GAP-09 minimisation relative to legitimate objective
GAP-10 governed acquisition / no hidden provider-tool bypass
GAP-11 derived-sensitivity closure
GAP-12 Runtime Interpretation Frame
GAP-13 consumer-delivery / transformation integrity
```

No Domain/Logical/Physical/PostgreSQL reopen was required.

---

# 8. AI-03B — CLOSED / STRUCTURALLY ACCEPTED

Durable authority:

```text
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
```

## 8.1 Core architecture

```text
RETRIEVAL
= governed discovery + validation of candidate material
  required by an InformationNeed

MEMORY
= noncanonical information/state that survives beyond
  the immediate step or Run under an explicit lifecycle

CANONICAL APPLICATION MEMORY
= already owned by Domain/PostgreSQL
```

Additional runtime contracts:

```text
RetrievalPlan
RetrievalCandidate
```

No new Domain root, table or microservice is implied.

Retrieval routes may include, when justified:

```text
structured / exact
material history
typed relation traversal
lexical
fuzzy
semantic / ANN
hybrid / rerank
hierarchical document
direct long-context
Interaction / Run
federated/provider
open-world / bounded JIT
```

Primary route rule:

```text
USE THE LEAST-COMPLEX ROUTE
THAT CAN SATISFY THE REQUIRED GUARANTEES.
```

## 8.2 Retrieval guarantees

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
index/cache/embedding != source
multiple chunks/derivatives of one lineage != independent corroboration
```

The eligible search universe is governed before treating ranking results as legitimate discovery. Post-filtering alone is not a universal permission-safe proof.

Consequential derived retrieval may require source reread/current-state validation.

## 8.3 Retrieval transformation integrity

Final hardening requires:

```text
QUERY REWRITE != NEW INFORMATION NEED
QUERY EXPANSION != PURPOSE EXPANSION
GENERATED / HYPOTHETICAL QUERY REPRESENTATION != SOURCE EVIDENCE
```

Translation/decomposition/expansion/model-generated search terms may optimize retrieval only while preserving the accepted InformationNeed. A new material dependency must become/refine an explicit bounded need under AI-03A.

## 8.4 Memory classes

```text
CANONICAL APPLICATION MEMORY
→ Domain/PostgreSQL; not generic AI memory

INTERACTION MEMORY
→ discourse/session/referent continuity

RUN / WORKING MEMORY
→ intermediate state; transient by default

COMPACTION / CHECKPOINT
→ continuity optimization; not source

ADAPTIVE / DERIVED USER MEMORY
→ bounded typed user-specific hypothesis/pattern

OPERATIONAL / EXPERIENCE MEMORY
→ verified bounded environment/provider/workflow knowledge

PROVIDER MEMORY / THREAD / CACHE
→ replaceable optimization

RETRIEVAL REPRESENTATIONS
→ chunks/summaries/FTS/vector/embedding/index derivatives

EXECUTION EVIDENCE
→ runtime/effect reconstruction; not user memory
```

## 8.5 Survival / admission / retention

```text
DEFAULT NONCANONICAL SURVIVAL = NO
MEMORY SURVIVAL MUST BE EARNED
MODEL REQUEST TO REMEMBER != MEMORY ADMISSION
MEMORY EXISTS != MEMORY MAY BE RECALLED
MEMORY RECALL = GOVERNED ACQUISITION
```

Final hardening adds:

```text
PROCESSING / RETRIEVAL ELIGIBILITY
!= RETENTION / MEMORY-ADMISSION ELIGIBILITY
!= FUTURE-REUSE ELIGIBILITY

MEMORY ADMISSION DECISION
!= MEMORY WRITE PERMIT

DURABLE MEMORY MUTATION
REQUIRES CURRENT ADMISSION
+
CURRENT GOVERNED EFFECT AUTHORIZATION
```

A source may be usable now while explicitly ineligible for durable memory or later reuse.

## 8.6 Durable user-memory control

Reusable personal semantic memory must remain inspectable/control-capable at the appropriate semantic level, including source/inference status, scope/validity and correction/deactivation/deletion paths.

This does not turn technical indexes/caches into user-profile records.

## 8.7 Correction / forgetting / suppression

```text
CORRECT
!= FORGET
!= SOURCE SUPPRESSION
!= USE SUPPRESSION
!= INFERENCE DISPOSITION
```

Inference Disposition prevents rejected/corrected derived meaning from silently resurrecting from materially equivalent surviving basis.

```text
DERIVATIVE
!= INDEPENDENT EVIDENCE OF ITS ANCESTRY
```

Repeated re-derivation cannot manufacture corroboration.

## 8.8 Derived-memory basis currentness

```text
ALL ORIGINAL SOURCE BYTES STILL VALID
!= DERIVED MEMORY STILL CURRENT
```

New evidence may make a derived memory stale/conflicted/superseded even when original sources remain valid. TTL alone is not semantic currentness proof.

## 8.9 Operational-memory poisoning

```text
PAST EXPERIENCE != POLICY
MODEL SAYS SUCCESS != VERIFIED SUCCESS
EXPERIENCE != INSTRUCTION AUTHORITY
```

Operational/Experience Memory requires adequate verified basis and bounded environment/provider/version applicability.

## 8.10 Canonical promotion non-duplication

```text
AI MEMORY CANNOT MINT CANONICAL TRUTH BY ITSELF
CANONICAL PROMOTION != DUPLICATION
```

After successful promotion into accepted Domain/application state, materially equivalent noncanonical memory must not remain active as independent authority/corroboration.

## 8.11 Recovery / provider state

```text
PROVIDER MEMORY = REPLACEABLE OPTIMIZATION
RESTORED BYTES != RESTORED ELIGIBILITY
```

Source lifecycle, suppression, retention/future-reuse policy and current authorization still apply after provider reuse or backup restore.

---

# 9. AI-03B accepted invariants B01–B35

```text
B01  RETRIEVAL != TRUTH.
B02  RetrievalCandidate != ContextFragment.
B03  Retrieval guarantee must match InformationNeed coverage.
B04  APPROXIMATE != COMPLETE.
B05  Candidate count != coverage proof.
B06  Eligibility defines the permitted search universe;
     post-filtering alone is not a universal permission proof.
B07  Rank / similarity / rerank != Source Standing.
B08  Multiple representations of one lineage != independent corroboration.
B09  Index / cache / embedding != source.
B10  Consequential derived retrieval may require source reread/current-state validation.
B11  Memory survival defaults to NO.
B12  MEMORY EXISTS != MEMORY MAY BE RECALLED.
B13  Memory recall is governed acquisition under AI-03A.
B14  MODEL REQUEST TO REMEMBER != MEMORY ADMISSION.
B15  Canonical application semantics belong to Domain/PostgreSQL,
     not generic AI memory.
B16  Durable adaptive memory requires bounded typed semantics;
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
B30  Correct non-recall / non-application is part of memory quality.
B31  Processing/retrieval eligibility does not imply retention
     or future-reuse eligibility. Durable memory mutation requires
     current admission plus governed effect authorization.
B32  Durable user-specific reusable memory must be semantically
     inspectable and support appropriate source/inference status,
     scope/validity, correction, deactivation and deletion control.
B33  Retrieval rewrite / expansion / translation / decomposition /
     hypothetical query generation must not silently redefine an
     InformationNeed. Generated query representations are not source evidence.
B34  Durable derived memory is not self-freshening. Material basis
     change or new contradictory evidence may make it stale,
     conflicted or superseded even when original sources remain valid.
B35  Successful canonical promotion must not leave a materially
     equivalent noncanonical memory acting as independent authority
     or independent corroboration.
```

These are binding upstream contracts for AI-03C.

---

# 10. AI-03B validation chronology

AI-03B did not close from the first PASS label.

```text
DANTE-FIRST INTERNAL DESIGN
        ↓
TARGETED MODERN CHALLENGER RESEARCH
        ↓
RECONCILED CANDIDATE
        ↓
FIRST HEAVY KILL-TEST
PASS CANDIDATE / B01..B30
        ↓
FRESH INDEPENDENT VALIDATION
FAIL / 5 REAL HARDENINGS
        ↓
FINAL-GAP-01 retention admission / governed memory mutation
FINAL-GAP-02 durable user-memory inspectability/control
FINAL-GAP-03 retrieval transformation/query-rewrite integrity
FINAL-GAP-04 derived-memory basis currentness
FINAL-GAP-05 canonical-promotion non-duplication
        ↓
FINAL COMPOUND RETEST
PASS
        ↓
B01..B35 ACCEPTED
AI-03B CLOSED / STRUCTURALLY ACCEPTED
```

Final retest included:

```text
private document usable now + do-not-remember
sensitive imported data with reuse denied
third-party remember request
provider automatic persistent memory
delayed memory write after revocation
user inspection/deactivation of learned memory
query rewrite introducing health semantics
hypothetical retrieval text confused for source evidence
material-basis drift without source deletion
provider/environment version drift
canonical promotion followed by stale derivative
inference resurrection
self-confirming memory
poisoned operational experience
permission-filtered ANN
complete-required via approximate Top-K
source retirement / backup restore
cross-actor / represented-party switch
long-running Run resume
correct non-recall / non-application
large history / large documents / context pressure
```

Result:

```text
FURTHER MATERIAL STRUCTURAL GAP   NONE FOUND
NEW TOP-LEVEL AI CONTRACT         NO
DOMAIN REOPEN                     NO
LOGICAL REOPEN                    NO
PHYSICAL REOPEN                   NO
POSTGRESQL/ALEMBIC CHANGE         NO
VECTOR DB REQUIRED                NO
MEMORY FRAMEWORK REQUIRED         NO
PROVIDER SELECTION                NO
IMPLEMENTATION PASS               NOT CLAIMED
```

Do not run more generic AI-03B mega-tests unless AI-03C or production evidence finds a concrete contradiction.

---

# 11. Current work — AI-03C

AI-03C asks:

> **Given the closed Context + Retrieval + Memory contracts, which runtime/derived/provider/evidence states actually need persistence or indexing, under which lifecycle, scale, recovery and performance guarantees?**

and:

> **Can the whole accepted architecture survive destructive scale/privacy/recovery/provider pressure before any physical schema is selected?**

AI-03C is not permission to immediately create tables or indexes.

---

# 12. AI-03C required classification

Before physical design, classify each candidate state into exactly the smallest justified category:

```text
ALREADY CANONICAL IN EXISTING DOMAIN/POSTGRESQL
TRANSIENT RUNTIME STATE
RECOMPUTABLE DERIVED STATE
BOUNDED DURABLE DERIVED STATE
PROVIDER-OWNED OPTIMIZATION STATE
RETRIEVAL REPRESENTATION / INDEX
EXECUTION / AUDIT EVIDENCE
OBJECT BYTES / ARTIFACT STORAGE
NOT JUSTIFIED TO STORE
```

Potential state families to classify include:

```text
Interaction Session continuity
Run / working state
checkpoint / compaction
ContextPlan / InformationNeed runtime state where durability is actually required
ContextManifest references/receipts where justified
adaptive/derived memory
Inference Disposition / suppression-related derived controls where they are not already owned elsewhere
operational/experience memory
retrieval candidate/cache state
text extraction / OCR derivatives
chunk/span metadata
hierarchical summaries
lexical/trigram indexes
embeddings/vector indexes
provider thread/cache/native memory metadata
retrieval evaluation artifacts
execution/reconciliation evidence
artifact/object bytes
retention / invalidation / rebuild bookkeeping
```

Do not infer that every architecture noun becomes a table.

---

# 13. AI-03C destructive pressure

At minimum attack:

```text
15+ years history
millions of structured rows
very large document corpora
permission-safe approximate retrieval under filters
recall/performance degradation
same-name / ambiguous referents
multi-actor private context
represented-party switching
Consent / Visibility / AuthZ revocation during Run
source correction / retirement / deletion
retention denial / future-reuse denial
material-basis drift
canonical promotion / duplicate derivative cleanup
backup restore / anti-resurrection
stale summary / stale embedding
provider persistent memory
provider automatic retention
provider failover
cache after authorization change
prompt/retrieval poisoning
malicious documents
query-rewrite semantic expansion
cross-query inference / cumulative disclosure
derived-sensitivity amplification
relative time/location/DST ambiguity
consumer/provider opaque compaction/truncation
context-window exhaustion
long-running Run resume
offline/delayed state
multimodal/voice/files
future larger context windows / stronger models
```

For each materialization candidate test:

```text
semantic owner
source / lineage / material basis
identity model
scope / Subject / Actor / represented party
purpose / retention / reuse eligibility
Authority / Consent / Visibility implications
currentness / expiry / supersession
correction / forgetting / suppression
anti-resurrection / recovery
provider replacement
rebuildability
performance / cardinality / storage cost
failure mode / safe fallback
eval proof required
```

---

# 14. Physical decisions that remain OPEN

Do not preselect:

```text
conversation table
Run/working table
memory table
adaptive-memory table
operational-memory table
summary table
chunk table
embedding table
embedding model/dimension
pgvector activation
HNSW / IVFFlat parameters
new FTS indexes
retrieval cache store
Redis
specialist vector DB
Mem0 / Zep / Graphiti / Letta adoption
provider-native memory/thread strategy
prompt-cache persistence
exact retention/invalidation jobs
OpenAI / Anthropic / Gemini / Qwen choice
local model/server/GPU
model gateway/router
SDK/framework
sandbox implementation
MCP/A2A implementation
```

Research technique or installed PostgreSQL extension availability is not a decision.

---

# 15. AI-03C working method

Recommended flow remains deliberately large-grained:

```text
1. RECONSTRUCT MATERIALIZATION REQUIREMENTS
   from AI-03A C01..C33 + AI-03B B01..B35
   + Product/Domain/Logical/PostgreSQL/Recovery

2. ENUMERATE CANDIDATE STATE FAMILIES
   without assuming persistence

3. CLASSIFY EACH STATE
   canonical / transient / recomputable / bounded durable /
   provider-owned / retrieval index / evidence / object bytes / no-store

4. BUILD ONE MATERIALIZATION BLUEPRINT CANDIDATE
   including lifecycle/recovery/performance obligations

5. ATTACK THE WHOLE CONTEXT/RETRIEVAL/MEMORY + BLUEPRINT
   with destructive simulations and scale/privacy/recovery cases

6. USE TARGETED TECH RESEARCH/BENCHMARKS ONLY WHERE
   a concrete physical question cannot be answered from current evidence

7. HARDEN REAL GAPS

8. ONLY THEN DECIDE WHETHER ANY POSTGRESQL/INDEX/PROVIDER
   STRUCTURAL CHANGE IS JUSTIFIED

9. IF A DB CHANGE IS NEEDED
   use a separate exact write gate and normal CP6 same-change discipline

10. CLOSE AI-03 ONLY WHEN AI-03C PASSES
```

No implementation write is required merely to begin this analysis.

---

# 16. Git write-gate discipline

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

# 17. Documentation / handoff lifecycle

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

# 18. Exact safe next action for the next chat

```text
NO REPOSITORY WRITE IS REQUIRED JUST TO BEGIN AI-03C.
```

First:

1. fetch live branch/ref and verify current HEAD;
2. read the mandatory current authority above, especially AI-03A and AI-03B durable documents;
3. acknowledge AI-03A as CLOSED / C01..C33 and AI-03B as CLOSED / B01..B35;
4. do not restart generic Context/Retrieval/Memory architecture or generic research;
5. independently reconstruct the concrete state/materialization obligations implied by the closed contracts;
6. enumerate state families without assuming they deserve storage;
7. classify each state into canonical/transient/recomputable/bounded-durable/provider/index/evidence/object/no-store;
8. preserve processing != retention != future reuse, query-transform integrity, derived-memory basis currentness, canonical-promotion non-duplication and anti-resurrection throughout materialization;
9. pressure the blueprint with scale, privacy, multi-actor, provider, recovery and lifecycle cases;
10. use fresh research/benchmarks only for concrete unresolved physical questions;
11. do not create tables/indexes/provider integration merely because AI-03B is closed;
12. if physical change is justified later, issue a separate exact write gate and follow CP6/PostgreSQL same-change discipline;
13. close AI-03 only after AI-03C destructive validation/materialization blueprint passes.

The new chat must continue this exact checkpoint rather than inventing a fresh AI architecture.