# Documentation Index

This directory is the durable project memory for LifeOS. It is designed so a new human/AI contributor can resume from the repository without reconstructing decisions from chat history.

## Start here

Read in this order:

1. [`../README.md`](../README.md)
2. [`PROJECT-STATUS.md`](PROJECT-STATUS.md)
3. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
4. [`development/operating-rules.md`](development/operating-rules.md)
5. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
6. [`development/branching-and-environments.md`](development/branching-and-environments.md)
7. the active [`workstreams/`](workstreams/) handoff
8. current model/architecture index and linked current sources
9. relevant ADRs/evidence/methodologies
10. relevant implementation/tests

## Current backend/architecture stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — PR #10

LOGICAL MODEL
CLOSED — PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS
Phase 0–9 QA PASS
Phase 10 Physical benchmark specification/register NEXT — READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Active handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

## Current semantic/model sources

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.
- [`domain/README.md`](domain/README.md) — Domain Atlas entry point. Read the complete canonical continuation chain when the document is physically split.
- [`domain/language-map.md`](domain/language-map.md) — current Domain language map. Read its complete canonical continuation chain where required.
- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md) — closed Whole Logical Model.
- the complete `logical-model/decision-and-assumption-register-v1*` chain — current Logical decisions/hardenings/deferrals unless explicitly superseded inside that logical document.
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md) — canonical Logical closure evidence.

A physical `*-part-N` chain is one logical document; do not treat one part as the whole authority.

If a document is split only because of size/tool limits, all canonical parts together must preserve the complete logical payload losslessly. A split is not a summary, condensation or hidden content rewrite.

Product/UI terminology does not override accepted Domain/Logical semantics.

## Current architecture sources

Start with:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) — current Pre-Physical bridge for decided/prohibited/open/mandatory downstream constraints;
- [`architecture/requirements/README.md`](architecture/requirements/README.md) — current Phase 5 requirement-package index; read all four linked requirement packages;
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md) — current Phase 6 AI/context/runtime contract;
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) — current Phase 6 Integration Hub/provider contract;
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md) — current Phase 7 durable execution benchmark and runtime-class/candidate posture;
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md) — current Phase 8 transport-/engine-neutral consequential-operation contract;
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md) — current Phase 9 search/observability/calendar/solver pressure contract;
- [`architecture/README.md`](architecture/README.md) — architecture navigation and current/evidence separation;
- [`architecture/system-overview.md`](architecture/system-overview.md);
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md).

## Phase 5 requirement package

The Phase 5 package constrains later Physical/runtime/API/backend work without selecting the implementation mechanism. It covers:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Open parameters inside those packages are explicit downstream obligations and must not be silently defaulted by implementation.

## Phase 6 AI/context/runtime/integration boundary

Phase 6 establishes:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

plus the five Integration Hub modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

AI/provider/runtime/protocol choices remain deferred. Runtime Agent/Principal is not Domain Actor automatically; tool/protocol actions are not canonical governed effects; `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`.

## Phase 7 durable execution posture

LifeOS distinguishes bounded asynchronous work from material durable long-running coordination.

```text
BOUNDED ASYNC
DB + worker/outbox style remains a valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Dedicated durable execution is structurally justified for classes involving material long waits, human review, callbacks, crash-resume, cancellation/timeouts, compensation or reconciliation. Runtime completion/cancellation is not Domain truth by identity, and no runtime creates exactly-once external reality automatically.

## Phase 8 governed operation/effect posture

The current operation contract preserves, where applicable:

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

A single `success` or generic status cannot replace materially different request/canonical/provider/runtime/domain result axes. Concrete routes/DTOs/API style remain later decisions.

## Phase 9 search / observability / calendar / solver posture

### Search

- structured filters + lexical/full-text — baseline;
- semantic/vector retrieval — bounded candidate;
- pgvector — bounded candidate if PostgreSQL survives Physical selection;
- dedicated search/vector infrastructure — not justified by default.

Search/index/ranking/vector state is derived; search miss != canonical nonexistence; vector similarity != semantic truth. Result inclusion/count/ranking/snippets/autocomplete/timing are disclosure/non-interference surfaces.

### Observability

OpenTelemetry-first or equivalent standards-based instrumentation is the current direction. No telemetry backend/vendor is selected. Telemetry is technical and does not replace Domain Provenance, security audit or required material effect history by identity.

### Calendar

iCalendar/JSCalendar/provider APIs are interoperability/adaptor pressure rather than ontology. Recurrence exceptions, all-day/floating/zoned time, DST/history and provider sync-token/deletion state must be preserved without equating provider identity/revision with LifeOS identity/material state.

### Solver

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT IMPLEMENTED
```

Hard constraints are not silently relaxed; `UNKNOWN != INFEASIBLE`; solver output remains candidate/scenario until accepted through the Phase 8 governed-effect boundary.

## Historical/current-document boundary

The old mixed `personal-data-ai-integration.md` current specification has been retired after knowledge coverage; its useful current content is carried by current architecture/ADR/Logical sources, and its old payload remains recoverable in Git history.

Historical `domain-model-logical-readiness*` files remain truthful transition/validation evidence and are **not** current architecture specifications.

## ADR status

ADRs preserve rationale and explicit current status:

- ADR-001 — accepted client platforms;
- ADR-002 — accepted backend platform direction, qualified at ORM/migration boundary;
- ADR-003 — superseded as final database selection; retained PostgreSQL rationale;
- ADR-004 — accepted storage abstraction;
- ADR-005 — accepted replaceable AI gateway, Logical + Phase 6 boundary-qualified;
- ADR-006 — superseded as canonical generic hybrid semantic model;
- ADR-007 — accepted semantic persistence guardrail, qualified for Physical posture.

An older `Accepted` label is not timeless authority; use the current status inside the ADR and current model/architecture sources.

No ADR is created merely because a benchmark candidate is currently preferred. Preferred candidate != implementation selection.

## Current Physical benchmark posture

```text
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — not final selection

TypeDB
MANDATORY CHALLENGER

Neo4j / property graph
SERIOUS SECONDARY / READ-PROJECTION CANDIDATE

event/document mechanisms
BOUNDED CANDIDATES

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Phase 10 prepares the detailed Physical benchmark specification/register and must consume Phase 5 open parameters plus Phase 6–9 pressure. The Physical Model remains separately unauthorized.

## Workstreams

- [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md) — active backend/architecture preparation workstream; Phase 0–9 are QA-closed and Phase 10 Physical benchmark specification/register is next, read-only first.
- [`workstreams/today-home.md`](workstreams/today-home.md) — active separate Phase 4 UX/product-structure workstream.
- [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md) — **current deferred future handoff**. It consumes the Pre-Physical Architecture Baseline, Phase 5 requirements and Phase 6–9 contracts, and must not be executed until Pre-Physical Coherence closes, a separate Physical Model is accepted, and applicable current runtime/security/integration/API prerequisites are accepted.
- Domain/Logical workstream documents are closed-stage evidence; `main` is authoritative for integrated state.

## Documentation lifecycle rule

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit current status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

Before a stale current document is replaced/deleted:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

Do not accumulate obsolete design history inside current specifications. Do not delete useful knowledge before coverage proves it safe.

## Development process

- [`development/agent-operating-manual.md`](development/agent-operating-manual.md) — exact write gates, remote QA, documentation lifecycle, split/tool-failure rules, including the lossless size/tool-limit split rule.
- [`development/operating-rules.md`](development/operating-rules.md) — authority, branches/path ownership, coherence gates.
- [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md) — current-truth/evidence separation and handoff protocol.
- [`development/branching-and-environments.md`](development/branching-and-environments.md) — Git/environment policy.

## Source-of-truth rule

For integrated state, current `main` wins over conversation memory and historical branches/files. For an active unmerged workstream, its bounded handoff/current files may contain newer work only inside that scope.
