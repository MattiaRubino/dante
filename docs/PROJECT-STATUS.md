# Project Status

- Last updated: 2026-08-17
- Canonical integrated branch: `main`
- Accepted `main` baseline for this Pre-Physical workstream: `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Active backend/architecture preparation branch: `chore/pre-physical-coherence`
- Production application code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**

## Current stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated through PR #10

LOGICAL MODEL
CLOSED — integrated through PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS
Phase 0–10 QA PASS
Phase 11 repository engineering safety — QA PASS

NEXT
Phase 12 clean-room repository/architecture coherence QA — READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Phase 4 UX remains a separate active product/design workstream on `prototype/phase-4-today-home`.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
9. active workstream handoff
10. current architecture navigation beginning at [`architecture/README.md`](architecture/README.md) and [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
11. complete Phase 5 requirement package + Phase 6–10 current contracts/method package
12. relevant ADR/evidence/methodology and implementation/tests

Conversation history is secondary to repository truth.

A canonical split chain is one logical document. A size/tool-limit split is lossless physical partitioning, not summary/condensation/hidden semantic rewrite.

## Accepted/current foundations

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current Product/North Star.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` are active downstream constraints.
- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) — **CURRENT** bridge; `DECIDED != AUTHORIZED TO IMPLEMENT`.
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + four linked Phase 5 packages — **CURRENT** requirements.
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md) — **CURRENT** Phase 6 AI/context/runtime contract.
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) — **CURRENT** Phase 6 Integration Hub contract.
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md) — **CURRENT** Phase 7 posture.
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md) — **CURRENT** Phase 8 contract.
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md) — **CURRENT** Phase 9 pressure contract.
- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md), [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md), [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md) — **CURRENT** Phase 10 method package.
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md) — **CURRENT** Phase 11 repository safety policy.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional on accepted Physical persistence.
- DEV/UAT/PROD — deployment environments, not permanent Git branches.
- Repository visibility — public.

## Current Phase 5 requirement inputs

The Phase 5 package separates accepted requirements, open parameters and deferred mechanisms.

Current owners:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Current requirements include `Person != Account != Principal != Actor`, consequential AuthZ provenance, actual Actor vs represented party, purpose-aware minimization, truthful deletion/redaction/tombstones, secure restore, expected-state writes, idempotency != identity, no silent material last-write-wins, truthful multi-owner consistency, canonical/provider separation, multi-device divergence, operation-specific offline semantics and recovery testing.

RPO/RTO/latency/availability/scale/offline-duration values remain explicit open parameters until accepted later.

## Current Phase 6 boundary inputs

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Context is purpose/minimization/disclosure/provenance/freshness bounded. Generic AI memory is not a second canonical truth store. Runtime Agent/Principal != Domain Actor automatically; tool invocation != authorization/governed effect.

Integration Hub modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect != canonical state/effect automatically.

## Current Phase 7–9 inputs

### Phase 7 — durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

### Phase 8 — governed operation/effect

Consequential semantics preserve target/effect, material expected state, purpose/context, Principal/Actor/represented party, governance, confirmation/autonomy, idempotency/correlation, execution class and independent canonical/provider/runtime/reconciliation outcomes.

```text
HTTP/UI/tool/AuthZ/workflow step != canonical governed operation
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

### Phase 9 — search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text = baseline
semantic/vector = bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred benchmark candidate — NOT implemented
```

## Current Phase 10 benchmark-method inputs

Phase 10 defines how a later separately authorized Physical benchmark must run. It does not select or implement a Physical Model.

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector

EVENT / DOCUMENT
bounded native mechanisms first; specialized candidate only on demonstrated gap/benefit
```

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Evidence pins exact product/version/edition/deployment. `PREFERRED != SELECTED`.

## Phase 11 repository engineering safety — QA PASS

Current policy: [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md).

Verified core state:

```text
ruleset                              lifeos-main-safety
ruleset enforcement                  active
target                               ~DEFAULT_BRANCH
bypass                               none
main deletion                        blocked
force-push / non-fast-forward        blocked
pull request before merge            required
required approvals                   0
review-thread resolution             required
allowed merge method                 merge
required status checks               0
GitHub Actions workflows             0
auto-delete merged head branches     enabled
confirmed accidental refs            absent
```

Dependabot/secret/code-scanning state is connector-unverifiable because those security endpoints return 403 to the integration. The requested admin settings were applied by the repository owner; the limitation remains explicit rather than inferred.

No fake CI workflow or fake required check was introduced. Future implementation must create real stable check contexts before any are promoted into main protection.

## Pre-Physical workstream milestone ledger

| Scope | Result / key remote point |
|---|---|
| Phase 0–1 | QA PASS |
| Phase 2 | PRE-SCOPE `d9610a7d...`; content HEAD `dfc1f4e1...`; QA PASS |
| Phase 3 | PRE-SCOPE `d2f190de...`; content HEAD `50731dbe...`; QA PASS |
| Phase 4 | PRE-SCOPE `46b96339...`; content HEAD `d67cd83f...`; QA PASS |
| Phase 5 | PRE-SCOPE `e26f95af...`; content HEAD `c29cfe4b...`; QA PASS |
| Phase 6 | PRE-SCOPE `40728080...`; content HEAD `67d6a0d6...`; QA PASS |
| Phase 7 | checkpoint `022131c2...`; PASS WITH CONDITIONAL RANKING |
| Phase 8 | checkpoint `1d92f9e7...`; QA PASS |
| Phase 9 | checkpoint `95df2a17...`; QA PASS |
| Phase 7–9 | PRE-SCOPE `2cf77ea7...`; content HEAD `4cbf50ec...`; QA PASS |
| Phase 10 | PRE-SCOPE `01df10a4...`; content HEAD `057df9bd...`; QA PASS |
| Phase 11 | PRE-SCOPE `7a87cba8...`; content/settings checkpoint `62d9118d...`; QA PASS |

Full exact SHAs and detailed evidence remain in [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md) and Git history.

## Current Physical benchmark posture

No Physical technology is selected.

- PostgreSQL hybrid — preferred primary baseline;
- TypeDB — mandatory primary challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- pgvector — bounded semantic-retrieval candidate where applicable;
- generic EAV/generic-edge/universal meta-model — hard reject for canonical kernel.

Physical selection requires a later separate user authorization and benchmark/design scope.

## Active workstreams

### Pre-Physical Repository & Architecture Coherence

- **IN PROGRESS**
- Branch: `chore/pre-physical-coherence`
- Phase 0–11: **QA PASS**
- Next: **Phase 12 clean-room repository/architecture coherence QA — READ-ONLY FIRST**
- Handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`
- Handoff: [`workstreams/today-home.md`](workstreams/today-home.md)

## Deferred production/model workstreams

### Physical Model

**NOT STARTED / NOT AUTHORIZED.** Phase 10 defines the benchmark method only. A separate explicit user authorization is required after Pre-Physical closure.

### Backend Foundation

**NOT STARTED / DEFERRED.** Current future handoff: [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md).

Do not create `feature/backend-foundation`, SQL/schema/migrations, concrete API/Auth/provider/runtime implementation or persistence-specific bootstrap before the accepted prerequisites exist.

## Current documentation policy

Current specifications contain current truth only. ADRs preserve rationale + explicit supersession/qualification. Historical validation/checkpoint files preserve truthful chronology. Git preserves recoverable history.

Before replacing/deleting stale current documentation:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

## Immediate next work

```text
PHASE 12
CLEAN-ROOM REPOSITORY / ARCHITECTURE COHERENCE QA
READ-ONLY FIRST
```

Phase 12 must independently reconstruct current truth and verify the final target:

```text
REPOSITORY / ARCHITECTURE COHERENCE PASS
DOMAIN UNCHANGED / CLOSED
LOGICAL UNCHANGED / CLOSED
PHYSICAL MODEL READY FOR SEPARATE AUTHORIZATION / NOT STARTED
```

Until Phase 12 closes, the Physical Model remains unauthorized.
