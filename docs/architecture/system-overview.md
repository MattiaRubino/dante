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
FINAL CLOSURE CANDIDATE
Phase 5 requirements CURRENT
Phase 6 AI/context/runtime/integration boundaries CURRENT
Phase 7 durable-execution benchmark CURRENT
Phase 8 governed-operation/effect contract CURRENT
Phase 9 search/observability/calendar/solver pressure CURRENT
Phase 10 Physical benchmark method CURRENT
Phase 11 repository engineering safety QA PASS
Phase 12 clean-room QA closing on this branch
independent total repository audit still required before definitive whole-workstream closure

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED / DEFERRED
```

Domain semantics are defined by the accepted CLOSED Domain Atlas and its final closure/status continuations. Logical representation and downstream hardenings are defined by the CLOSED Whole Logical Model plus its separate remote-QA closure record. This overview does not introduce new semantic owners or Physical mechanisms.

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

Clients own presentation, navigation, local interaction state, secure session handling, platform capabilities and collection of user intent/confirmation where required.

A later multi-device/offline implementation may authorize bounded local caches, queues or synchronization behavior according to the Phase 5 requirement envelope. Clients do not hold primary persistence credentials and do not own critical authorization or canonical Domain invariants.

UI actions may request governed operations; UI labels/buttons do not define semantic operation identity.

## Backend boundary responsibilities

The future backend boundary is responsible for enforcing accepted Domain/Logical semantics through technical services, including:

- semantic target and operation validation;
- governed operation/effect admission and multi-axis result semantics;
- authorization enforcement without collapsing Principal, Actor, Authority, Consent or Visibility;
- expected-state/conflict handling for consequential writes;
- autonomy/preview/confirmation according to consequence/governance;
- provenance, material history, correction and reconciliation;
- truthful multi-owner consistency or explicit staged/partial outcomes;
- provider-state versus canonical-state separation;
- selective projection/disclosure enforcement;
- scheduling/reasoning/replanning services;
- deterministic calculations/constraints;
- optional solver invocation producing candidates rather than direct canonical writes;
- AI context construction and provider-neutral routing;
- provider/integration orchestration;
- bounded background work and durable long-running coordination by operation class;
- search/retrieval projections separated from canonical state;
- privacy-safe observability and operational controls.

Concrete routes, DTOs, transaction mechanics, AuthZ engine, durable-runtime binding and persistence structures remain later decisions.

## Governed operation/effect responsibility

Consequential callers converge on [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md).

Where material, the boundary preserves:

```text
contract / operation version
semantic target / facet
requested effect
input / candidate
purpose / context
material / expected state
freshness/material basis
Principal / actual Actor / represented party
governance basis
autonomy / preview / confirmation
idempotency + operation equivalence
correlation / causation
execution class
deadline / expiry / technical cancellation
canonical result
provider/external result
runtime result
conflict / partial / reconciliation / provenance
```

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completion != Domain Actual automatically
runtime cancellation != Domain cancellation automatically
```

One generic success/status flag is insufficient for materially consequential work.

## Durable execution responsibility

LifeOS distinguishes bounded asynchronous work from material long-running durable processes.

```text
BOUNDED ASYNC
DB + worker/outbox style remains valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Dedicated durable execution is structurally justified where correctness depends on long waits/timers, human review, provider callbacks, crash-resume, material cancellation/timeouts, compensation or multi-step reconciliation.

No runtime creates exactly-once external reality by itself. Runtime workflow/job IDs remain technical references and do not become Domain identity/material-state identity.

See [`durable-execution-benchmark.md`](durable-execution-benchmark.md).

## Canonical-state responsibility

LifeOS owns canonical state and its material history. Physical representation remains open until separately authorized Physical Model work.

Any future persistence must preserve:

- owner-specific identity/lifecycle boundaries;
- discriminated reference families rather than a universal semantic root;
- planned/current/actual/observed/derived distinctions;
- specific relationship/governance semantics;
- provider identity/state as external representation, not automatic canonical identity/truth;
- material history, correction, reconciliation and retention/tombstone integrity;
- bounded flexible/provider metadata without generic semantic fallback;
- unresolved/candidate interpretation where meaning is not established.

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject / Actor / Resource contextual roles != native universal identities
provider state != canonical state
derived projection != canonical truth
absence / unknown != false
AI / solver inference != accepted canonical effect
```

All `WL-H01..WL-H12` remain mandatory downstream constraints.

## Physical benchmark posture

Current role-specific posture:

```text
PRIMARY CANONICAL LANE
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — NOT selected

TypeDB
MANDATORY CHALLENGER — NOT selected

SECONDARY GRAPH LANE
primary/no-specialized-store baseline
vs Neo4j / property graph

SEARCH / SEMANTIC RETRIEVAL LANE
structured + lexical/full-text baseline
vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first; specialized candidate only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
REJECTED FOR CANONICAL KERNEL
```

## Phase 10 benchmark-method responsibility

The Phase 10 package is:

- [`physical-benchmark-specification.md`](physical-benchmark-specification.md);
- [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md);
- [`physical-benchmark-register.md`](physical-benchmark-register.md).

It defines **how** later Physical evidence is produced and judged. It does not select a database or create schemas.

```text
hard semantic/correctness gates
        ↓
role-specific scoring
        ↓
LOW / BASE / HIGH + NFR sensitivity
        ↓
version / edition / deployment-pinned evidence
        ↓
PREFERRED / PASS-CONDITIONAL / HOLD / REJECT / SENSITIVITY-DEPENDENT
```

A candidate failing a non-compensable hard gate cannot win through throughput/latency. Synthetic tiers are qualification envelopes, not business forecasts. Candidate mappings are idiomatic but must satisfy common semantic assertions. `PREFERRED != SELECTED`.

## Integration responsibility

External systems are isolated behind provider/capability boundaries. Provider-specific payloads do not define LifeOS ontology.

Five current Integration Hub modes remain distinct:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider acknowledgement/result != canonical effect completion automatically.

Provider callbacks/webhooks/replays are technical inputs requiring authentication/validation/dedup/mapping. MCP/A2A/future protocols remain adapters rather than ontology/governance.

## AI / Context Builder responsibility

AI remains behind a provider-neutral/replaceable gateway. The Context Builder is purpose-, disclosure-, provenance- and freshness-aware.

Runtime context categories remain distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

AI output/tool invocation never becomes canonical truth/effect merely because a model/runtime produced it. LifeOS does not create a second generic AI-memory source of truth.

## Search responsibility

Current baseline:

```text
structured queries / filters + lexical/full-text search
BASELINE

semantic/vector retrieval
BOUNDED CAPABILITY

dedicated search infrastructure
ONLY ON DEMONSTRATED BENEFIT
```

Search ranking, snippets, counts, suggestions and errors are disclosure surfaces. Search miss != canonical nonexistence; similarity != truth. Search/index state is derived projection and remains deletion/freshness aware.

## Calendar interoperability responsibility

LifeOS scheduling/time semantics remain Domain/Logical-owned.

```text
iCalendar / JSCalendar / provider APIs
= interoperability / adapter pressure
!= LifeOS ontology
```

Adapters must handle recurrence exceptions/overrides, all-day/floating/zoned time, DST transitions, provider resync/token invalidation and provider deletion/cancellation without collapsing provider representation into canonical state. Provider sync token != `MaterialStateRef`.

## Solver responsibility

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT IMPLEMENTED

AI
interpretation / ambiguity / explanation
NOT deterministic constraint authority
```

`UNKNOWN != INFEASIBLE`. Solver output is a candidate bound to an input/material/model/objective basis and crosses the governed-operation boundary before any canonical schedule/plan effect.

## Observability responsibility

OpenTelemetry-first or equivalent is current direction without vendor selection.

```text
trace/span/request/workflow ids
!= NativeRef / MaterialStateRef / ExternalRef / idempotency identity
```

Telemetry may be sampled/expired and does not replace Domain Provenance, security audit or required material effect history. Observability must support diagnosis without indiscriminate sensitive-payload logging.

## Storage responsibility

Large object bytes remain behind a StorageProvider abstraction. Content Artifact identity is not identical to blob path, URL, provider object or storage identifier. Local development and future S3-compatible/cloud storage remain compatible directions; provider selection is not fixed here.

## Repository engineering safety

Phase 11 verified effective `main` protections remotely. Current owner-driven posture:

```text
PR required
main deletion blocked
force-push/non-fast-forward blocked
review-thread resolution required
0 required approvals while no independent reviewer exists
0 required checks until real stable check contexts exist
merge-commit history preserved by current policy
```

Repository settings must be read back before being used as evidence. Connector-unverifiable security settings remain explicitly unverifiable rather than fabricated as PASS.

## Phase 12 / final-verification responsibility

Phase 12 is the repository-first clean-room coherence check. It may repair stale current navigation/status but does not reopen the accepted Domain/Logical semantics.

Current user-required boundary after Phase 12 QA PASS:

```text
DO NOT MERGE TO MAIN
DO NOT DECLARE THE ENTIRE PRE-PHYSICAL WORKSTREAM DEFINITIVELY CLOSED YET

NEXT
run one independent total repository audit for mistakes, contradictions, lost knowledge and scope damage

only if that passes
→ definitive Pre-Physical closure
→ later separately authorized PR/main integration
```

## Scalability and specialized infrastructure

The backend direction remains modular-monolith-first. Caches, graph stores, search/vector services, analytics/time-series systems, workflow engines, policy engines, event infrastructure and solver runtimes are bounded mechanisms admitted only for demonstrated structural or measured benefit.

## Current navigation

For the complete authority map, Domain/Logical closure discoverability and current-vs-history rules, read [`README.md`](README.md). For detailed final-verification state read [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md).
