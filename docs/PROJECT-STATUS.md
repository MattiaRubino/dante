# Project Status

- Last updated: 2026-08-17
- Canonical integrated branch: `main`
- Current accepted main baseline for this workstream: `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Active backend/architecture preparation branch: `chore/pre-physical-coherence`
- Production application code: **NOT STARTED**

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

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS
Phase 0 + Phase 1 QA PASS
Phase 2 architecture supersession/current-truth cleanup — QA PASS
Phase 3 Backend Foundation handoff cleanup — QA PASS
Phase 4 Current Pre-Physical Architecture Baseline — QA PASS
Phase 5 requirements that can constrain Physical design — QA PASS
Phase 6 AI/context/runtime/integration boundaries — QA PASS
Phase 7 durable workflow/async benchmark — QA PASS WITH CONDITIONAL RANKING
Phase 8 governed API/command/effect contract — QA PASS
Phase 9 search/observability/calendar/solver pressure — QA PASS
Phase 10 Physical benchmark specification/register — QA PASS

NEXT
Phase 11 repository engineering safety — READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Phase 4 UX remains a separate active product/design workstream.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. active workstream handoff
9. current architecture navigation beginning at [`architecture/README.md`](architecture/README.md) and [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
10. complete Phase 5 requirement package + Phase 6–10 current contracts/method package
11. relevant ADR/evidence/methodology
12. relevant implementation/tests

Conversation history is secondary to repository truth.

When a canonical document is physically split, read the complete split/continuation chain rather than treating the first path or newest part as the whole logical document.

A split caused only by size/tool limits is a lossless physical partition of the complete logical payload. It is not a summary/condensation or a hidden semantic rewrite.

## Accepted/current foundations

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**, with `WL-H01..WL-H12` active downstream constraints.
- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) — **CURRENT** Pre-Physical bridge; `DECIDED != AUTHORIZED TO IMPLEMENT`.
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + four linked Phase 5 packages — **CURRENT** requirements constraining later Physical/runtime/API/backend design.
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md) — **CURRENT** Phase 6 AI/context/runtime contract.
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) — **CURRENT** Phase 6 five-mode Integration Hub/provider contract.
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md) — **CURRENT** Phase 7 benchmark/posture.
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md) — **CURRENT** Phase 8 consequential-operation contract.
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md) — **CURRENT** Phase 9 pressure contract.
- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md) — **CURRENT** Phase 10 benchmark method.
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md) — **CURRENT** Phase 10 common scenario/destructive corpus and synthetic qualification tiers.
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md) — **CURRENT** Phase 10 candidate-role/evidence register and future result slots.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional candidates depending on accepted Physical persistence.
- DEV/UAT/PROD are deployment environments, not permanent Git branches.
- Repository visibility: **public**.

## Current Phase 5 requirement inputs

The Phase 5 package defines requirements, open parameters and deferred mechanisms separately.

Current packages:

- [`architecture/requirements/authn-authz.md`](architecture/requirements/authn-authz.md);
- [`architecture/requirements/security-privacy-retention-recovery.md`](architecture/requirements/security-privacy-retention-recovery.md);
- [`architecture/requirements/consistency-side-effects.md`](architecture/requirements/consistency-side-effects.md);
- [`architecture/requirements/nonfunctional-multidevice-recovery.md`](architecture/requirements/nonfunctional-multidevice-recovery.md).

Current constraints include, among others:

- `Person != Account != Principal != Actor` and technical allow/deny != canonical Authority/Consent/Visibility;
- actual Actor and represented party remain distinct;
- consequential AuthZ/effect provenance and delayed-governance revalidation;
- purpose-aware minimization, sensitive-data handling, truthful deletion/redaction/tombstone semantics and secure restore without forbidden-data resurrection;
- expected-state writes, idempotency != identity, no silent material last-write-wins, truthful multi-owner atomic/staged consistency and canonical/provider-effect separation;
- multi-device divergence, operation-specific offline semantics, truthful degraded/provider state, long-history/current-state access and recovery testing;
- RPO/RTO/latency/availability/scale/offline-duration values remain explicit open parameters, not invented Phase 5 constants.

## Current Phase 6 boundary inputs

### AI / context / runtime

Current contract preserves:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder is purpose-, minimization-, disclosure-, provenance- and freshness-aware. Whole-history/full-database exposure is not the default.

LifeOS does not use generic `AI memory` as a second canonical truth store. AI output does not become effective solely because it is structured/high-confidence.

```text
runtime Agent / Principal != Domain Actor automatically
tool invocation != authorization
tool/protocol action != canonical governed operation
```

### Integration Hub

Five current modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Current invariants include:

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef by identity
provider state/effect != canonical LifeOS state/effect automatically
```

Sync conflict does not use universal last-write-wins; live-read failure can remain unknown/degraded; indexes/projections remain derived/deletion-aware; external effects preserve idempotency, ambiguous-outcome and reconciliation truth. MCP/A2A/future protocols remain adapters, not ontology/governance.

## Current Phase 7–9 architecture inputs

### Phase 7 — durable execution / async

LifeOS distinguishes bounded background work from material long-running durable coordination.

```text
BOUNDED ASYNC
DB + worker/outbox style remains a valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Dedicated durable execution is structurally justified for classes involving material long waits, human review, callbacks, crash-resume, cancellation/timeouts, compensation or reconciliation.

Runtime completion/cancellation is not Domain truth by identity. No runtime creates exactly-once external reality automatically.

### Phase 8 — governed operation / effect

Current contract preserves as applicable:

```text
contract/version
semantic target/facet
requested effect
input/candidate
purpose/context
material/expected state
derived/live basis + freshness
Principal / actual Actor / represented party
governance basis
autonomy / preview / confirmation
idempotency
correlation/causation
execution class
deadline/expiry/cancellation semantics
canonical result
provider result
runtime result
conflict/partial/reconciliation/provenance
```

```text
HTTP route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect
```

A single `success`/generic status cannot replace distinct request/canonical/provider/runtime/domain result axes. Concrete route/DTO/API design remains deferred.

### Phase 9 — search / observability / calendar / solver

Current posture:

```text
SEARCH
structured + lexical/full-text = baseline
semantic/vector = bounded candidate
pgvector = bounded candidate if PostgreSQL selected
no dedicated search/vector infrastructure by default

OBSERVABILITY
OpenTelemetry-first / equivalent
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs
= interoperability/adaptor pressure, not ontology

SOLVER
simple deterministic rules / heuristics = baseline
OR-Tools CP-SAT = preferred specialized benchmark candidate — NOT implemented
```

Search miss != canonical nonexistence; vector similarity != semantic truth; telemetry != Domain Provenance/audit by identity; provider calendar tokens/IDs != LifeOS native/material identity; solver `UNKNOWN != INFEASIBLE`; solver result != accepted canonical effect.

## Current Phase 10 benchmark-method inputs

Phase 10 creates three current documents:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md);
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md);
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md).

Phase 10 decides **how** the later separately authorized Physical Model benchmark must be run. It does not select or implement a Physical Model.

### Role-specific candidate lanes

```text
PRIMARY CANONICAL PERSISTENCE
P0 PostgreSQL hybrid — mandatory preferred baseline, NOT selected
P1 TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH / TRAVERSAL
G0 no-specialized-store baseline
G1 Neo4j serious secondary challenger

SEARCH / SEMANTIC RETRIEVAL
S0 structured + lexical/full-text baseline
S1 bounded pgvector where PostgreSQL is applicable

EVENT / DOCUMENT
bounded native mechanisms first
specialized candidate admitted only on demonstrated gap/benefit
```

### Hard-gate-first method

Primary candidates must pass non-compensable gates for semantic ownership, reference integrity, typed/n-ary relation fidelity, expected-state concurrency, multi-owner consistency, history/reconciliation, state-layer separation, governance/selective disclosure, retention/restore, temporal fidelity, schema evolution and recoverability.

Performance/operability scoring applies only after hard-gate PASS.

### Scenario/sensitivity treatment

LOW/BASE/HIGH numbers in the scenario corpus are **synthetic qualification envelopes, not business forecasts**.

Phase 5 open RPO/RTO/availability/latency/scale values remain sensitivity dimensions. If preference changes materially across accepted scenarios, the future result is `SENSITIVITY-DEPENDENT` rather than one averaged winner.

### Evidence contract

Future benchmark evidence pins exact product/version/edition/deployment mode plus source/benchmark commits, mapping revision, fixture seed/tier, hardware/config, correctness/performance/recovery evidence, manual tuning and raw artifact locations.

Result vocabulary:

```text
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
```

`PREFERRED != SELECTED`.

## Current Physical benchmark posture

No Physical technology is finally selected.

- PostgreSQL hybrid — current preferred primary baseline;
- TypeDB — mandatory primary challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- pgvector — bounded semantic-retrieval candidate where applicable;
- generic EAV/generic-edge/universal meta-model — hard reject for canonical kernel.

Physical selection requires a later separate user authorization and benchmark/design scope.

## Active workstreams

### Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)
- Phase 0 + 1: **QA PASS**.
- Phase 2: **QA PASS** — current architecture/supersession cleanup completed with exact remote path QA and knowledge-coverage QA.
- Phase 2 content HEAD before closure markers: `dfc1f4e124f362d342c336485e166c8ac57afba4`.
- Phase 3: **QA PASS** — Backend Foundation handoff cleaned against closed Domain/Logical/current architecture.
- Phase 4: **QA PASS** — current Pre-Physical Architecture Baseline established and made mandatory downstream input without authorizing Physical/backend implementation.
- Phase 4 content HEAD before global closure markers: `d67cd83f462611b2cc6d341937432e705f7a8682`.
- Phase 5: **QA PASS** — four requirement packages plus index established; lossless size/tool-limit split rule hardened.
- Phase 5 PRE-SCOPE: `e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f`.
- Phase 5 content HEAD: `c29cfe4bde47d5df4f46507a5f1717acd1903112`.
- Phase 6: **QA PASS** — AI/context/runtime + Integration Hub contracts established.
- Phase 6 PRE-SCOPE: `40728080ae7a69703d40d14dd256a556516ccc58`.
- Phase 6 content HEAD: `67d6a0d63ecaf39379912606dcf5113550718594`.
- Coordinated Phase 7–9 PRE-SCOPE: `2cf77ea7e3d548147bbe2b0d87304b4d5393ff5f`.
- Phase 7 checkpoint HEAD: `022131c2568c0375e74563e46a22c9347b277fc5`.
- Phase 8 checkpoint HEAD: `1d92f9e77ecc808095086fc5497eaac88e2039fa`.
- Phase 9 checkpoint HEAD: `95df2a17b1187a590b5cba646ba0e107c038e5d3`.
- Coordinated Phase 7–9 content HEAD: `4cbf50ec23ede3b02a49c75bc52fa57c3b192a6d`.
- Phase 7–9 content QA: **PASS** — 8 commits, 3 added, 5 modified, 0 deleted, 0 unexpected, behind 0.
- Phase 10 PRE-SCOPE: `01df10a4267880a213ede8582b0193ff616f9a70`.
- Phase 10 content HEAD: `057df9bdc19d89ea74fcee0e5d999ebc34cf93dc`.
- Phase 10 content QA: **PASS** — 8 commits, 3 added, 5 modified, 0 deleted, 0 unexpected, behind 0.
- Next: **Phase 11 — repository engineering safety, READ-ONLY FIRST** after final Phase 10 propagation/closure QA recorded in the workstream handoff.
- Domain/Logical remain closed/unchanged.

### Phase 4 — Home / Today UX

- Status: **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`
- Handoff: [`workstreams/today-home.md`](workstreams/today-home.md)
- Does not override backend/domain/logical architecture.

## Deferred production/model workstreams

### Physical Model

- **NOT STARTED / NOT AUTHORIZED**.
- Phase 10 defines the benchmark method only; it does not start the Physical Model.
- A separate explicit user authorization remains required before a Physical Model workstream can begin.

### Backend Foundation

- **NOT STARTED / DEFERRED**.
- Current future handoff: [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md).
- The handoff consumes the Pre-Physical Architecture Baseline, Phase 5 requirements, Phase 6–9 contracts, Phase 10 benchmark method and later accepted Physical result and remains intentionally non-executable.
- Backend Foundation may start only after Pre-Physical Coherence closes, a separate Physical Model is accepted, and applicable accepted Physical/runtime/security/integration/API prerequisites exist.
- Do not create `feature/backend-foundation`, SQL/schema/migrations, concrete API/backend/Auth/provider/runtime implementation or persistence-specific bootstrap from this status.

## Current architecture documentation policy

Current specifications contain current truth only. ADRs preserve rationale + explicit supersession/qualification. Historical validation/checkpoint files preserve truthful chronology. Git preserves recoverable history.

Stale current docs are replaced/deleted only after knowledge coverage proves meaningful content is safely mapped.

Current architecture navigation starts at [`architecture/README.md`](architecture/README.md) and includes all Phase 5–10 current sources linked there.

## Verified earlier phase results

### Phase 2

Approved PRE-SCOPE: `d9610a7da4fe8fc759e9809843d989f1befcda5c`.

Verified content HEAD: `dfc1f4e124f362d342c336485e166c8ac57afba4`.

Remote fallback QA:

```text
linear content commits 17
added                  1
modified              15
deleted                 1
unexpected              0
main changed            0
```

The native compare endpoint returned `404`; equivalent remote evidence was used and explicitly recorded. Knowledge coverage for retired `architecture/personal-data-ai-integration.md` passed with zero unclassified meaningful content and zero valid requirement loss.

### Phase 3

Backend Foundation handoff was cleaned against current Domain/Logical/architecture truth and remains deferred/non-executable.

### Phase 4

The current Pre-Physical Architecture Baseline was established without reopening Domain/Logical or authorizing Physical/runtime implementation.

### Phase 5

Remote content QA:

```text
ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

The split rule was hardened explicitly:

```text
SIZE / TOOL-LIMIT SPLIT
= LOSSLESS PHYSICAL PARTITION
!= SUMMARY / CONDENSATION / HIDDEN CONTENT REWRITE
```

### Phase 6

Remote content QA:

```text
ahead_by        8
behind_by       0
total_commits    8
added             2
modified          6
deleted           0
unexpected        0
```

Phase 6 selected no AI provider/model, agent framework, workflow engine, MCP/A2A implementation or provider adapter.

## Coordinated Phase 7–9 result

Internal checkpoints were executed and remotely verified in dependency order:

```text
PHASE 7
Durable execution benchmark
commit 022131c2568c0375e74563e46a22c9347b277fc5
PASS WITH CONDITIONAL RANKING
        ↓
PHASE 8
Governed operation/effect contract
commit 1d92f9e77ecc808095086fc5497eaac88e2039fa
PASS
        ↓
PHASE 9
Search/observability/calendar/solver pressure
commit 95df2a17b1187a590b5cba646ba0e107c038e5d3
PASS
```

The three current contracts were then integrated into five architecture/backend consumers.

Content HEAD:

`4cbf50ec23ede3b02a49c75bc52fa57c3b192a6d`

Remote content integration QA from Phase 7–9 PRE-SCOPE:

```text
ahead_by       8
behind_by      0
total_commits  8
added           3
modified        5
deleted         0
unexpected      0
```

No Domain/Logical/ADR/Physical/backend implementation path was changed by the content package.

## Phase 10 result

Phase 10 converts the open Physical posture into an executable future benchmark method without starting Physical design.

Current created package:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md);
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md);
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md).

Content HEAD:

`057df9bdc19d89ea74fcee0e5d999ebc34cf93dc`

Remote content QA from Phase 10 PRE-SCOPE:

```text
ahead_by       8
behind_by      0
total_commits  8
added           3
modified        5
deleted         0
unexpected      0
```

The method establishes role-specific candidate competition, non-compensable correctness hard gates, candidate-idiomatic physical mappings under common semantic assertions, synthetic low/base/high qualification tiers, explicit NFR sensitivity handling, version/edition/deployment-pinned evidence and future result vocabulary.

No PostgreSQL/TypeDB/Neo4j schema, SQL/TypeQL/Cypher benchmark implementation, database winner, search/vector deployment or Physical Model was created/selected.

## Immediate next work

```text
PHASE 11
REPOSITORY ENGINEERING SAFETY
READ-ONLY FIRST
```

Phase 11 must determine the repository protection/CI/required-check baseline appropriate before future production implementation without starting backend code or Physical design.

## Non-negotiable downstream obligations

`WL-H01..WL-H12`, all accepted Phase 5 requirements, both Phase 6 boundary contracts, all three Phase 7–9 current architecture contracts and the Phase 10 benchmark method must survive later Physical/runtime work.

Open parameters/decisions must be resolved at the appropriate later gate rather than silently defaulted. Phase 10 benchmark preferences/registrations remain distinct from Physical selection.
