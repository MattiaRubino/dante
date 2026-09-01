# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Workstream:** AI architecture
- **Current phase:** AI-03 — Context / Retrieval / Memory
- **Current macro-phase:** AI-03A — Full Context Architecture
- **Created:** 2026-09-01
- **PRE-SCOPE for AI-03 transition:** `17bdc95a3abf08ac7a74d4d9d66a9ae6570f3a48`
- **Last substantive AI-03 transition checkpoint before this handoff refresh:** `ae0601e76fa4f2bd91e4fd256577a509d66860e7`
- **Current branch HEAD:** verify live before any write; the handoff refresh itself may advance HEAD beyond the substantive checkpoint above

This document exists only to survive chat/session/context saturation while `feature/ai-architecture` is active. Durable architectural truth must live in the architecture/workstream/current-status sources named below.

---

## 1. Resume rule

A new chat/session does **not** start a new project, branch or workstream.

Resume:

```text
repository  MattiaRubino/dante
branch      feature/ai-architecture
workstream  DANTE AI architecture
```

Before writes:

1. fetch the live branch;
2. verify exact HEAD and relation to its upstream/protected `main` as applicable;
3. read the current authority below;
4. use the repository write gate before remote writes;
5. if a previously approved PRE-SCOPE no longer matches, stop and re-gate.

---

## 2. Mandatory reading order for a fresh chat

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
```

For AI-03A also inspect the source corpus explicitly listed by the AI-03 charter: North Star, Domain, Logical Whole/WL-H01..WL-H12, Physical, Persistence Constitution, DB/Alembic/Recovery truth.

Repository truth beats this handoff if they disagree.

---

## 3. Closed/accepted state that must not be casually reopened

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN
CLOSED

LOGICAL
CLOSED / 57 OF 57 / WL-H01..WL-H12

PHYSICAL
CLOSED / PostgreSQL 18 family accepted

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
remote provider TBD / not activated
production/cloud recovery not claimed
```

AI work must consume these contracts rather than reopen them because an AI framework/vector store/provider prefers another shape.

---

## 4. AI phases completed before this handoff

### AI-00

Semantic/product foundation recorded in `dante-ai-foundation.md`.

Key constraints:

```text
DANTE != model/provider/chat transcript
PostgreSQL canonical authority
AI inference != confirmed fact
Authority/AuthZ/Consent/Visibility distinct
provider state != canonical state
unknown/unresolved legitimate
no universal AI fact/action/memory ontology
anti-resurrection applies to derivatives
```

### AI-01

Product-form and production-engineering research completed.

Durable production research is explicitly `NON-DANTE-DECISION`; technology challengers are not implementation selections.

### AI-02 / AI-02.1

Structurally accepted runtime architecture after:

```text
Round I
Round II
Final Kill-Test
Last Mega Stress-Test
Targeted v0.5 structural verification
```

No more AI-02 mega-test cycles.

Accepted runtime responsibilities include:

```text
Interaction Session
WorkContract
Work Supersession
Reference / Target Resolution
ConsequenceProfile
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
ModelTarget / HarnessProfile
Capability Runtime
Execution Environment
Verifier
Policy mesh
ChangeSet / EffectGraph
Effect Runtime
Result Maturity
Disclosure
Safe Result Publication
Attention
```

Important invariants:

```text
Interaction Session != Run != Worker
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO DISPATCHED EFFECTS
Context access != disclosure permission
Scenario state != canonical current state
DANTE representation != external System-of-Record authority
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
Execution Environment != mandatory sandbox
fresh inputs != automatically coherent basis
approval != authorization for materially changed work
cache hit != current disclosure authorization
```

AI-02 structural acceptance is not backend/runtime/provider implementation PASS.

---

## 5. Current compact roadmap

```text
AI-00  Semantic & Product Foundation
       COMPLETE

AI-01  Product Form + Production Engineering Research
       COMPLETE

AI-02  Intelligence Runtime Architecture
       COMPLETE / STRUCTURALLY ACCEPTED

AI-03  Context / Retrieval / Memory
       ACTIVE
       ├ AI-03A Full Context Architecture
       ├ AI-03B Retrieval + Memory Architecture
       └ AI-03C Destructive Validation + Materialization Blueprint

AI-04  Productionization Architecture
       FUTURE

AI-05  Whole-System Acceptance + Implementation Blueprint
       FUTURE
```

The earlier longer AI-00..AI-12 exploratory decomposition is historical planning only and must not be used as current routing.

---

## 6. AI-03 exact scope

Durable phase charter:

```text
docs/architecture/dante-ai-03-context-retrieval-memory.md
```

AI-03 must design Context, Retrieval and Memory before selecting physical persistence or providers.

Forbidden shortcut:

```text
AI-03 starts
→ create memory table
→ create embeddings
→ pick vector database
```

Required sequence:

```text
semantic/context need
→ architecture
→ retrieval/memory lifecycle
→ destructive validation
→ materialization classification
→ smallest justified physical design
```

---

## 7. Current exact task — AI-03A

Next chat should begin directly with:

# AI-03A — FULL CONTEXT ARCHITECTURE

Do **not** break it into many tiny micro-steps.

The user explicitly requested a professional, highly detailed architecture pass with maximum care and documentation quality.

First reconstruct constraints from:

```text
North Star
Domain
Whole Logical + WL-H01..WL-H12
Physical
CP1–CP6 / Persistence Constitution
current PostgreSQL/Alembic/Recovery
AI-00
AI-02.1 v0.5
production engineering research
```

Then design the complete context flow:

```text
WorkContract
→ information needs
→ candidate source discovery
→ processing-policy eligibility
→ provenance / source authority
→ confidentiality / integrity / instruction authority
→ freshness / temporal validity / MaterialState binding
→ contradiction / coherence
→ relevance / deduplication
→ resource/token/latency budget
→ packing
→ consumer/provider-specific rendering
→ exact ContextManifest
→ reasoning
→ iterative information acquisition when needed
→ invalidation/revocation/supersession handling
```

Must cover at least:

```text
structured DANTE current state
material history
people/relations/multi-actor
session/conversation continuity
working/Run state
documents/notes/artifacts
open-world/web/provider information
derived/candidate information
external professional/source material
large histories and large corpora
sensitive context
conflicting evidence
future multimodal/general-purpose models
```

No DB/model/provider decision yet.

---

## 8. AI-03A expected outputs

The architecture should end with a current specification detailed enough to answer, for every context fragment:

```text
what is it?
why is it needed?
what source owns it?
canonical / historical / derived / external / candidate / runtime class?
who may process it?
for what purpose?
what is its provenance?
what is its integrity/trust?
does it have instruction authority?
what is its confidentiality?
what MaterialState/source version/time does it bind to?
when is it stale?
how does it relate to BasisManifest?
what contradictions exist?
how much context budget does it consume?
which consumer actually received it?
what transformation/compaction occurred?
what invalidates or retires it?
```

The design must preserve simple fast paths; trivial structured queries must not become giant RAG/model workflows.

---

## 9. Explicitly open later questions

Do not accidentally close these during AI-03A:

```text
final memory persistence schema
conversation table
Run table
embedding model
vector dimensions
pgvector activation
specialist vector DB
chunk table/index
summary persistence
provider thread strategy
OpenAI/Anthropic/Gemini/Qwen selection
local model/server/GPU
provider pricing/routing
SDK/gateway
sandbox implementation
Restate activation
MCP/A2A implementation
```

---

## 10. Documentation protocol during AI-03

Durable architecture decisions go into the AI-03 architecture document/current architecture sources.

This handoff is updated only when continuation would otherwise be difficult, for example:

```text
macro-phase checkpoint completed
large architecture decision set accepted
chat/context close to saturation
write partially completed
important tactical issue remains unresolved
```

Do not use this file as an append-only diary.

Before merge to `main`:

```text
classify meaningful handoff content
→ propagate current truth/rationale/evidence
→ delete this file
```

Temporary handoff count entering protected `main` must be zero.

---

## 11. Safe next action

```text
NO REPOSITORY WRITE REQUIRED TO BEGIN THE DESIGN.

Start AI-03A in chat/review mode.
Build the Full Context Architecture in depth.
Only materialize after the architecture pass is coherent and a new exact write gate is approved.
```
