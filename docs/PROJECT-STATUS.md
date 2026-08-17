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
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated through PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
FINAL CLOSURE CANDIDATE
Phase 0–11 QA PASS
Phase 12 clean-room closure record written
Phase 12 activation requires exact final remote gate QA

AFTER PHASE 12 ACTIVATION
independent total repository audit REQUIRED before definitive Pre-Physical closure
NO main integration yet

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
9. active/final-verification workstream handoff
10. [`architecture/README.md`](architecture/README.md) and [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
11. complete Phase 5 requirement package + Phase 6–10 current contracts/method package
12. [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md)
13. relevant ADR/evidence/methodology and implementation/tests

Conversation history is secondary to repository truth.

A canonical split/cumulative continuation chain is one logical document. A size/tool-limit split is lossless physical partitioning, not summary/condensation/hidden semantic rewrite.

## Accepted/current foundations

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current Product/North Star.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` active downstream.
- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) — **CURRENT** bridge; `DECIDED != AUTHORIZED TO IMPLEMENT`.
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + four Phase 5 packages — **CURRENT** requirements.
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md) — **CURRENT** Phase 6 AI/context/runtime contract.
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) — **CURRENT** Phase 6 Integration Hub contract.
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md) — **CURRENT** Phase 7 posture.
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md) — **CURRENT** Phase 8 contract.
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md) — **CURRENT** Phase 9 contract.
- Phase 10 benchmark-method package — **CURRENT / QA PASS**.
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md) — **CURRENT / Phase 11 QA PASS**.
- [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md) — Phase 12 clean-room evidence and activation contract.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional on accepted Physical persistence.
- DEV/UAT/PROD — deployment environments, not permanent Git branches.

## Domain closure authority

The early Domain Atlas entry payload contains truthful historical in-progress state. Current closure is established by later cumulative continuation/evidence, including:

- `domain/README-part-20.md`;
- `domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`;
- `domain/language-map-part-22.md`.

Current state:

```text
DOMAIN ATLAS / WHOLE-DOMAIN
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED
```

No Phase 12 Domain semantic write is authorized or performed.

## Logical closure authority

`logical-model/whole-logical-model-v1.md` is canonical content; `logical-model/checkpoints/whole-logical-v1-remote-qa.md` separately activates closure.

Current state:

```text
WHOLE-LOGICAL
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE
WD-03 PASS
WD-05 PASS
LOGICAL MODEL CLOSED
```

No Phase 12 Logical semantic write is authorized or performed.

## Current Phase 5 requirement inputs

Current owners:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Requirements include `Person != Account != Principal != Actor`, consequential AuthZ provenance, actual Actor vs represented party, purpose-aware minimization, truthful deletion/redaction/tombstones, secure restore, expected-state writes, idempotency != identity, no silent material last-write-wins, truthful multi-owner consistency, canonical/provider separation, multi-device divergence, operation-specific offline semantics and recovery testing.

Open RPO/RTO/latency/availability/scale/offline-duration values remain explicit parameters until accepted later where needed.

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

### Durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

### Governed operation/effect

Consequential semantics preserve target/effect, expected material state, purpose/context, Principal/Actor/represented party, governance, confirmation/autonomy, idempotency/equivalence, correlation/causation, execution class and independent canonical/provider/runtime/reconciliation outcomes.

```text
HTTP/UI/tool/AuthZ/workflow step != canonical governed operation
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text = baseline
semantic/vector = bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent = direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred benchmark candidate — NOT implemented
```

## Current Phase 10 benchmark posture

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

Verified core state:

```text
ruleset                              lifeos-main-safety
ruleset enforcement                  active
target                               default branch
main deletion                        blocked
force-push / non-fast-forward        blocked
pull request before merge            required
required approvals                   0
review-thread resolution             required
required status checks               0 while no real stable contexts exist
auto-delete merged head branches     enabled
confirmed accidental refs            absent
```

Security endpoints inaccessible to the connector remain explicitly connector-unverifiable rather than inferred.

## Phase 12 clean-room result

Initial clean-room review reconstructed Product/Domain/Logical/Phase 5–11 state from repository evidence and found:

```text
DOMAIN REOPEN REQUIRED              0
LOGICAL REOPEN REQUIRED             0
SEMANTIC CONTRADICTION              0
ARCHITECTURAL CONTRADICTION         0
PHYSICAL MODEL STARTED              0
BACKEND STARTED                     0
BOUNDED CURRENT-TRUTH REPAIRS       5
REPAIRS REMAINING AFTER RERUN       0
```

The five repairs were current-consumer/discoverability fixes only:

- `CONTRIBUTING.md`;
- architecture navigation;
- Pre-Physical baseline;
- system overview;
- Backend Foundation handoff.

No Domain/Logical/Physical/backend implementation path was changed.

Phase 12 closure record: [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md).

Phase 12 becomes **QA PASS / CLOSED** only when final remote QA proves exactly:

```text
unique paths  11
added          1
modified      10
deleted        0
unexpected     0
behind_by      0
main unchanged at 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0
```

## Pre-Physical milestone ledger

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
| Phase 10 | PRE-SCOPE `01df10a4...`; content HEAD `057df9bd...`; final HEAD `7a87cba8...`; QA PASS |
| Phase 11 | PRE-SCOPE `7a87cba8...`; Step-A `62d9118d...`; final HEAD `d7fe5828...`; QA PASS |
| Phase 12 | PRE-SCOPE `d7fe5828...`; repair HEAD `4d4c5eac...`; closure evidence `ab945295...`; final gate QA pending |

Full exact SHAs/evidence remain in [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md) and Git history.

## Active workstreams

### Pre-Physical Repository & Architecture Coherence

- **FINAL CLOSURE CANDIDATE**
- Branch: `chore/pre-physical-coherence`
- Phase 0–11: **QA PASS**
- Phase 12: **closure activation pending final remote gate QA**
- After Phase 12: **independent total repository audit**
- `main` integration: **NOT AUTHORIZED YET**

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`

## Deferred production/model workstreams

### Physical Model

**NOT STARTED / NOT AUTHORIZED.** A separate explicit user authorization is required only after definitive Pre-Physical closure.

### Backend Foundation

**NOT STARTED / DEFERRED.** Current handoff: [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md).

Do not create `feature/backend-foundation`, SQL/schema/migrations, concrete API/Auth/provider/runtime implementation or persistence-specific bootstrap before accepted prerequisites exist.

## Documentation policy

```text
CURRENT SPECIFICATION = current truth
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

Before replacing/deleting stale current documentation:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

## Immediate next work

If the Phase 12 final remote activation gate passes:

```text
PHASE 12
QA PASS / CLOSED

NEXT
INDEPENDENT TOTAL REPOSITORY AUDIT
```

That audit must review the entire relevant repository/workstream for mistakes, contradictions, knowledge loss, unintended scope changes and false closure claims before the user authorizes definitive Pre-Physical closure.

Until that later audit passes:

```text
PRE-PHYSICAL COHERENCE
NOT YET DEFINITIVELY CLOSED

MAIN INTEGRATION
NOT AUTHORIZED

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED
```
