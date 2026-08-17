# System Overview

- Status: **Current architecture overview**
- Last updated: 2026-08-17

## Stage boundary

This document describes the current logical/system architecture without selecting the future Physical Model.

```text
Core Domain Model / Domain Atlas
CLOSED

Logical Model
CLOSED

Pre-Physical Repository & Architecture Coherence
IN PROGRESS
Phase 5 requirements CURRENT
Phase 6 AI/context/runtime/integration boundaries CURRENT
Phase 7 durable-execution benchmark CURRENT
Phase 8 governed-operation/effect contract CURRENT
Phase 9 search/observability/calendar/solver pressure CURRENT
Phase 10 Physical benchmark method CURRENT

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED
```

Domain semantics are defined by the accepted Domain Atlas. Logical representation and downstream hardenings are defined by the closed Logical Model. This overview must not introduce a universal semantic Entity/Relationship root, a generic canonical property model, or a concrete persistence design by convenience.

## Logical architecture

```text
Web client (Next.js) -----------------------\
                                             \
Mobile client (Expo / React Native) ----------> Versioned LifeOS backend boundary
                                                  |-- authentication context / AuthZ enforcement
                                                  |-- governed operation/effect boundary
                                                  |-- scheduling / planning / reasoning services
                                                  |-- deterministic solver boundary
                                                  |-- provenance / history / reconciliation services
                                                  |-- projection / disclosure services
                                                  |-- search / retrieval projection services
                                                  |-- Integration Hub / provider adapters
                                                  |-- AI Gateway + Context Builder
                                                  |-- provider-neutral tool/action interfaces
                                                  |-- bounded async + durable-execution runtime boundary
                                                  |-- observability / operational controls
                                                            |
                                                            v
                                                Physical persistence/runtime
                                                TO BE SELECTED / BENCHMARKED
                                                            |
                                                StorageProvider / object storage
```

External providers, assistants, caches, indexes, projections, solver candidates, workflow/runtime state and device-local stores are not alternate canonical LifeOS truth merely because they contain data.

## Client responsibilities

Clients are responsible for presentation, navigation, local interaction state, secure session handling, platform-specific capabilities and collection of user intent/confirmation where required.

A later multi-device/offline implementation may authorize bounded local caches, queues or synchronization behavior. This document does not preselect those semantics beyond the Phase 5 requirement envelope.

Clients do not hold primary persistence credentials and do not own critical authorization or canonical domain invariants.

Client/UI actions may request governed operations but UI labels/buttons do not define semantic operation identity.

## Backend responsibilities

The backend boundary is responsible for enforcing accepted Domain/Logical semantics through technical services, including:

- validation of semantic target and operation intent;
- governed operation/effect admission and result semantics;
- authorization enforcement without collapsing Principal, Actor, Authority, Consent or Visibility into one concept;
- expected-state/conflict handling for consequential writes where required;
- autonomy/preview/confirmation handling according to consequence and governance;
- provenance, history, correction and reconciliation behavior;
- truthful multi-owner consistency or explicit staged/partial outcomes;
- provider-state versus canonical-state separation;
- selective projection/disclosure enforcement;
- scheduling/reasoning/replanning services;
- deterministic calculations and constraint handling where appropriate;
- optional specialized solver invocation producing candidates rather than direct canonical writes;
- AI context construction, proposal/effect-request validation and provider routing;
- integration/provider orchestration;
- bounded background work and durable long-running coordination according to operation class;
- search/retrieval projections separated from canonical state;
- privacy-safe technical observability and operational controls.

Concrete API routes, DTOs, transaction mechanics, AuthZ engine, durable-execution engine binding and persistence structures remain later stage decisions.

## Governed operation/effect responsibility

Consequential callers converge on the current [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) rather than bypassing semantics through transport-specific operations.

Where material, the boundary preserves:

```text
contract/version
semantic target/facet
requested effect
input / candidate
purpose/context
material/expected state
derived/live input basis + freshness
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
request accepted != effect completed
provider acknowledgement != canonical completion automatically
runtime cancellation != Domain cancellation automatically
```

One generic status/success flag is not sufficient for materially consequential operations.

## Durable execution responsibility

The system distinguishes bounded asynchronous work from material long-running durable processes.

Current Phase 7 posture:

```text
BOUNDED ASYNC
DB + worker/outbox style remains valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate  preferred structural-fit candidate — NOT selected
Temporal strongest mandatory challenger — NOT selected
DBOS     conditional PostgreSQL-dependent challenger — NOT selected
```

Dedicated durable execution is justified where correctness materially depends on long waits/timers, human review, provider callbacks, crash-resume, material cancellation/timeouts, compensation or multi-step reconciliation.

No runtime creates exactly-once external reality by itself. Provider ambiguity/idempotency/reconciliation remain explicit.

Runtime workflow/job IDs are technical references and do not become Domain identity or material-state identity.

See [`durable-execution-benchmark.md`](durable-execution-benchmark.md).

## Canonical-state responsibility

LifeOS owns canonical state and its material history. Physical representation remains open until the separately authorized Physical Model benchmark/design stage.

Any future persistence must preserve the closed Logical Model, including:

- owner-specific identity and lifecycle boundaries;
- discriminated references rather than a universal semantic root;
- planned/current/actual/observed/derived distinctions;
- specific relationship/governance semantics;
- provider identity/state as external representation rather than automatic canonical identity/truth;
- material history, correction, reconciliation and retention/tombstone integrity;
- bounded flexible/provider metadata without generic semantic fallback;
- unresolved/candidate interpretation where meaning is not yet established.

Current Physical benchmark posture:

```text
PRIMARY CANONICAL LANE
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — not final selection

TypeDB
MANDATORY CHALLENGER

SECONDARY GRAPH LANE
primary-only/no-specialized-store baseline
vs Neo4j / property graph

SEARCH / SEMANTIC RETRIEVAL LANE
structured + lexical/full-text baseline
vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms only unless explicit gap/benefit admits a specialized candidate

generic EAV / generic edge / universal meta-model
REJECTED FOR CANONICAL KERNEL
```

## Phase 10 benchmark-method responsibility

The current Phase 10 package defines the future Physical decision method:

- [`physical-benchmark-specification.md`](physical-benchmark-specification.md);
- [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md);
- [`physical-benchmark-register.md`](physical-benchmark-register.md).

It does **not** create Physical schemas or select a technology.

The method enforces:

```text
hard semantic/correctness gates
        ↓
role-specific weighted scoring
        ↓
low/base/high + NFR sensitivity review
        ↓
version/edition/deployment-pinned evidence
        ↓
future PREFERRED / PASS-CONDITIONAL / HOLD / REJECT result
```

Primary-candidate hard gates cover semantic ownership, reference families, typed/n-ary relation fidelity, expected-state concurrency, multi-owner consistency, history/reconciliation, state-layer separation, governance/disclosure, retention/restore, temporal fidelity, schema evolution and recoverability.

A candidate that fails a non-compensable hard gate cannot win by being faster.

Low/base/high dataset values are synthetic qualification envelopes, not business/user-growth forecasts. Open RPO/RTO/latency/availability/scale targets remain sensitivity inputs until accepted values exist.

Every future benchmark subject is pinned as:

```text
product + exact version + edition/license + deployment mode
```

The benchmark must use common semantic assertions with candidate-idiomatic physical mappings rather than forcing all technologies into one storage shape.

## Integration responsibility

External applications and services are isolated behind provider/capability boundaries. Provider-specific payloads do not define LifeOS ontology.

The current Integration Hub contract preserves five distinct modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Each flow must identify the applicable mode or bounded composition rather than treating all integrations as equivalent.

External identifiers, revisions and source data retain enough provenance for reconciliation and remain distinguishable from canonical LifeOS identity/state. `ExternalRef != NativeRef`; provider revision/token != `MaterialStateRef` by identity.

Canonical import requires explicit validation/mapping/acceptance. Sync/mirror preserves canonical and provider apply states separately. Live reads retain source/freshness/unknown state. Retrieval/index state remains derived and deletion-aware. Action/tool integration preserves governance, idempotency, ambiguous-outcome and reconciliation truth.

Provider callbacks/webhooks/polling are adapter mechanisms; duplicate/out-of-order delivery does not create latest-arrival canonical truth.

Calendar provider synchronization additionally remains adapter state: provider sync/delta tokens, recurrence IDs and API status do not become canonical LifeOS identity/material state.

See [`integration-hub-boundaries.md`](integration-hub-boundaries.md).

## AI responsibility

AI access remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

AI may interpret ambiguous input, help reason across domains, generate proposals and support explanation. It does not become canonical truth by producing output and does not bypass domain validation, governance, expected-state checks or confirmation/autonomy policy.

The runtime keeps distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder is purpose-, disclosure-, provenance- and freshness-aware. It does not default to unrestricted database or complete-history exposure.

LifeOS does not maintain a generic second source of truth called `AI memory`: durable AI-relevant information must be classified into an accepted canonical/history/candidate/derived/source/provider representation.

AI output is classified according to task: answer/explanation, candidate/unresolved interpretation, structured extraction, Proposal/proposal-like candidate, scenario/recommendation or governed-effect request. Model output is not an accepted effect merely because it is structured.

Runtime Agent, service Principal, Tool, Workflow or Automation state remains technical/product/runtime state unless a separate accepted semantic role applies. `Principal != Actor`; tool/protocol action strings != canonical governed operation.

MCP/A2A/future tool/agent protocols are adapters, not ontology or LifeOS governance.

See [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md).

## Search / retrieval responsibility

Search/index state is a downstream projection, not canonical truth.

Current posture:

```text
structured filters + lexical/full-text
BASELINE

semantic/vector retrieval
BOUNDED CANDIDATE

pgvector
BOUNDED CANDIDATE IF POSTGRESQL SURVIVES PHYSICAL SELECTION

dedicated search/vector infrastructure
NOT ASSUMED
```

Search ranking, snippets, counts, autocomplete, candidate lists and errors are disclosure surfaces subject to `WL-H12`. Search miss != canonical nonexistence; embedding similarity != truth.

Actions from search results re-resolve/revalidate through the governed-operation boundary rather than mutating from stale index payload.

Phase 10 additionally requires vector/search quality to be measured after scope/Visibility filtering and through deletion/redaction/index-staleness scenarios rather than top-k latency alone.

## Calendar interoperability responsibility

LifeOS scheduling/time semantics remain Domain/Logical-owned.

```text
iCalendar / JSCalendar / provider APIs
= interoperability + adapter pressure
!= LifeOS ontology
```

Adapters must pressure-test recurrence exceptions/overrides, source/occurrence history, all-day/floating/zoned time, DST transitions, provider token invalidation/full resync and provider deletion/cancellation without collapsing provider representation into canonical state.

Free/busy remains a bounded disclosure projection that may hide private source/reason detail.

## Solver responsibility

Deterministic calculations, constraints and straightforward planning logic remain deterministic services where appropriate.

Current posture:

```text
simple rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT IMPLEMENTED

AI
interpretation / ambiguity / explanation / cross-domain reasoning
NOT deterministic constraint authority
```

Solver results preserve states such as feasible/infeasible/unknown where applicable. `UNKNOWN != INFEASIBLE`.

A solver produces candidate/scenario output bound to an input/material basis. Accepted Schedule/Plan/etc state changes only through the governed-operation contract.

Phase 10 uses stale-snapshot and solver-status scenarios as Physical support pressure; the primary database is not expected to become the solver itself.

## Storage responsibility

Large object/file bytes remain behind a provider abstraction rather than normal domain rows. Domain semantics refer to accepted Content Artifact identity/meaning; blob path, URL, provider object or storage identifier is representation/integration state, not automatically domain identity.

The current storage abstraction direction remains compatible with local development and future S3-compatible/cloud object storage.

## Observability responsibility

Current direction is OpenTelemetry-first or equivalent standards-based instrumentation without selecting a telemetry vendor.

```text
trace/span/request/workflow ids
!= NativeRef / MaterialStateRef / ExternalRef
```

Telemetry may be sampled/expired and does not replace Domain Provenance, security audit or required material effect history by identity.

Observability must support diagnosis of conflicts, retries, durable waits, provider failures/unknown outcomes, sync/reconciliation lag, index/deletion propagation, solver status and recovery pressure without indiscriminate sensitive payload logging.

## Scalability and specialized infrastructure

The current backend architecture direction is a modular monolith.

Specialized infrastructure is introduced only when it demonstrates material benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Search/vector stores, caches, graph stores, analytics/time-series systems, workflow engines, policy engines, event infrastructure and solver runtimes are therefore evaluated as bounded mechanisms rather than assumed defaults.

Phase 7 establishes structural justification for dedicated durable execution in material long-running classes; this does not justify routing every job through such an engine.

Phase 9 establishes OR-Tools CP-SAT as a preferred specialized solver benchmark candidate and does not yet justify a dedicated search/vector service.

Phase 10 adds an explicit candidate-admission rule: a new specialized stateful product enters later benchmarking only when it addresses an accepted gap or demonstrates strong structural/measured benefit over the baseline for its role.

## Non-negotiable Logical hardenings

Any later Physical/API/runtime architecture must preserve `WL-H01..WL-H12`, including:

- justified material Agreement terms;
- governed operation/effect semantics;
- bounded projection/disclosure surfaces;
- absence/unknown not collapsing to false;
- expected-state consequential writes;
- idempotency distinct from identity;
- truthful multi-owner consistency;
- canonical/provider-state separation;
- derived-state freshness/material basis;
- retention/redaction/tombstone integrity;
- reconstructible consequential AuthZ provenance;
- non-interference/inference-leakage protection.

Phase 5 requirement packages, Phase 6 AI/context/runtime + Integration Hub contracts, Phase 7–9 architecture contracts and the Phase 10 benchmark-method package are mandatory downstream constraints.

See [`../logical-model/decision-and-assumption-register-v1-part-9.md`](../logical-model/decision-and-assumption-register-v1-part-9.md).

## Current navigation

For architecture navigation and the distinction between current specifications and historical transition evidence, read [`README.md`](README.md).
