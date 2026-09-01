# DANTE AI Architecture Workstream

- **Status:** ACTIVE / BRANCH-LOCAL DURABLE WORKSTREAM RECORD
- **Branch:** `feature/ai-architecture`
- **Current phase:** AI-03 — Context / Retrieval / Memory
- **Current macro-phase:** AI-03A — Full Context Architecture
- **Implementation claim:** NONE
- **Merge status:** UNMERGED

This document is the durable branch-local continuation record for the DANTE AI architecture workstream. It describes current branch scope, accepted architecture checkpoints, what must not be casually reopened, the current roadmap and the exact next design boundary.

It is not a chat transcript and must not duplicate all evidence already preserved in architecture/checkpoint documents.

---

## 1. Branch identity

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
```

Protected `main` remains integrated authority for closed shared foundations and the current PostgreSQL baseline. This workstream owns only its bounded newer AI architecture truth until normal protected-main integration.

A new chat/session does not create a new AI branch. Continue this real workstream on this branch unless explicitly deciding otherwise.

---

## 2. Mandatory reading order for continuation

Before making architecture or repository changes in this workstream, read:

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

this file

docs/workstreams/ai-architecture-live-handoff.md
  only while it exists on the active branch

current AI architecture sources relevant to the phase
current branch/ref and relation to protected main
```

For AI-03 specifically, also read the source corpus in `docs/architecture/dante-ai-03-context-retrieval-memory.md`.

Repository truth beats conversation memory.

---

## 3. Accepted upstream foundation

AI work consumes, rather than reinterprets casually:

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED

LOGICAL MODEL
CLOSED / 57 OF 57
WL-H01..WL-H12 BINDING

PHYSICAL MODEL
CLOSED / ACCEPTED
PostgreSQL 18 major family
sole canonical persistence + material-history authority

BACKEND CP1–CP5
CLOSED / INTEGRATED

CP6 CONCRETE POSTGRESQL DATABASE
CLOSED / INTEGRATED

CURRENT POSTGRESQL
18.6
Alembic 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs

POSTGRESQL LOCAL RECOVERY
CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED
remote backup provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED
```

No AI convenience may create a second canonical database, universal Entity/Fact/Memory ontology or generic semantic root around these accepted contracts.

---

## 4. Current AI roadmap

The old exploratory AI-00..AI-12 decomposition is no longer current routing. Git/evidence preserve its historical planning value.

Current compact roadmap:

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
  AI-03A Full Context Architecture
  AI-03B Retrieval + Memory Architecture
  AI-03C Destructive Validation + Materialization Blueprint

AI-04 — PRODUCTIONIZATION ARCHITECTURE
FUTURE
  eval/model/provider/economics
  concrete runtime/capabilities/external intelligence
  security/privacy/persistence/control-plane/operations

AI-05 — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
FUTURE
```

Security, privacy, simulations and eval thinking remain cross-cutting requirements throughout the workstream; later dedicated assurance/acceptance passes validate concrete decisions rather than introducing those concerns for the first time.

---

## 5. AI-00 — accepted semantic/product foundation

Durable source:

- `docs/architecture/dante-ai-foundation.md`

Key inherited constraints:

```text
DANTE != model/provider/chat transcript
PostgreSQL remains canonical authority
AI output begins noncanonical unless governed application semantics say otherwise
AI inference != confirmed fact
Authority != AuthZ
Visibility != Authority
processing != disclosure != mutation authority
provider state != canonical state
unknown/unresolved are legitimate
no universal AI action/fact/memory tables
retention/redaction applies to derivatives
multi-actor cannot collapse to user_id
```

AI-00's original sequencing toward AI-01 is historical, not current work routing.

---

## 6. AI-01 — completed research/product-form evidence

This phase label groups the completed product-form and production-engineering research used by later architecture work.

Durable evidence includes:

- DANTE interaction/product-form research;
- `docs/architecture/ai-production-engineering-state-of-the-art-2026.md`.

Important direction retained:

```text
ONE DANTE / MANY SURFACES / ONE SEMANTIC REALITY
Ask / Work / Watch / Resolve
Interaction Session continuity
provider independence without lowest-common-denominator design
context as runtime resource
capability registry/discovery/runtime separation
deterministic compute first-class
verification separate from model self-report
effects explicit
security/information flow explicit
sandbox/isolation by workload/threat model
no automatic microservice explosion
```

Research technologies remain challengers/evidence unless explicitly selected later.

---

## 7. AI-02 — structurally accepted runtime architecture

Durable source:

- `docs/architecture/dante-ai-02-1-intelligence-reengineering.md`

AI-02.1 completed four destructive/pressure-test rounds plus targeted v0.5 verification.

Accepted structural responsibilities include:

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

Critical invariants include:

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
DANTE representation != external System-of-Record authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
```

AI-02 is architecture acceptance only. It is not backend/runtime/provider implementation PASS.

Do not reopen AI-02 broadly merely because AI-03 reveals a persistence or retrieval implementation preference. Reopen only the smallest affected boundary if a real contradiction appears.

---

## 8. AI-03 — current work

Durable phase charter:

- `docs/architecture/dante-ai-03-context-retrieval-memory.md`

AI-03 owns detailed Context / Retrieval / Memory architecture and eventual materialization recommendations.

### AI-03A — Full Context Architecture

Current exact focus.

Must design, in one deep architecture pass:

```text
WorkContract -> information needs
candidate source classes
structured current state
material history
conversation/session context
working/run context
documents/artifacts
open-world/external context
multi-actor context

ContextFragment
ContextManifest
provenance
source authority
confidentiality
integrity/trust
instruction authority
processing eligibility
purpose
freshness/temporal validity
MaterialState/Basis binding
coherence/contradiction
relevance/deduplication
packing/budgets
provider rendering
iterative retrieval
compaction
context cache semantics
failure/degradation
```

Acceptance requires an end-to-end explanation of what entered each reasoning invocation, why, under which permissions, from which source and with what validity.

### AI-03B — Retrieval + Memory Architecture

After AI-03A.

Must define:

```text
structured semantic retrieval
history queries
FTS / fuzzy / semantic / hybrid retrieval
source reread
reranking
chunk/document hierarchy

Interaction memory
Run/working memory
derived/adaptive memory
provider memory/cache
retrieval representations

admission
promotion
correction
contradiction
decay
expiry
retirement
deletion
forgetting
anti-resurrection
```

No generic AI memory ontology by default.

### AI-03C — Destructive Validation + Materialization Blueprint

After A+B.

Must attack scale, privacy, stale/corrected/deleted sources, provider memory, caches, embeddings, long history, huge documents, multi-actor, offline, prompt/retrieval poisoning and future-model/context-window pressure.

Only then classify what is:

```text
canonical already
transient
recomputable
durable derived
provider optimization
retrieval representation
execution/audit evidence
object bytes
not justified to store
```

Only after this may new PostgreSQL structures or retrieval indexes be proposed.

---

## 9. Database/materialization rule for AI-03

Current DB truth must be treated as fixed input until a genuine new requirement is justified.

If AI-03C eventually requires structural DB evolution, the same reviewed change must keep aligned, as applicable:

```text
Alembic forward migration
SQLAlchemy metadata/mappings
Database Dictionary
human-readable DB reference
generated artifacts/diagrams where governed
direct tests
recovery/operational assertions affected by the change
current project/workstream docs
```

Applied migrations are immutable.

No table is created simply because an architecture noun exists.

---

## 10. Decisions explicitly still open

Do not claim these are decided before evidence:

```text
conversation persistence physical form
Run/working persistence physical form
embedding model
dimensions
pgvector activation
FTS index additions
chunk schema
summary persistence
adaptive-memory persistence
provider memory/thread use
prompt-cache implementation
OpenAI/Anthropic/Gemini/Qwen selection
local model activation
model router/gateway
runtime SDK
concrete sandbox technology
Restate activation for AI work
MCP/A2A exact implementation
production AI server/GPU topology
AI commercial/pricing model
```

---

## 11. Cross-cutting quality bar

Every architecture decision must be reviewed against:

```text
semantic correctness
source/canonicality integrity
historical truth
multi-actor correctness
privacy / Authority / Visibility
security / prompt/retrieval injection
revocation / deletion / anti-resurrection
concurrency / stale state
provider replaceability
failure/reconciliation
latency / token / compute / storage cost
simple-path performance
future extensibility
operational recoverability
observability/evaluation feasibility
```

Maximum quality does not mean maximum abstraction.

---

## 12. Live handoff policy

Temporary session continuity is stored only when useful in:

- `docs/workstreams/ai-architecture-live-handoff.md`

That document:

```text
is TEMPORARY
is branch-operational only
must not merge to protected main
is updated only at meaningful continuation checkpoints
must not become the only home of durable architecture decisions
```

Before branch integration, its meaningful payload must be classified and propagated to durable current/reference/evidence docs, then the live handoff must be deleted.

---

## 13. Current next action

```text
AI-03A — FULL CONTEXT ARCHITECTURE
```

The next design pass must first reconstruct constraints from North Star -> Domain -> Logical -> Physical -> CP/Persistence/Alembic/PostgreSQL -> AI-00 -> AI-02.1 -> production research, then build the context architecture in depth before materialization.
