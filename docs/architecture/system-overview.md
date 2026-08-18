# System Overview

- Status: **Current architecture overview — Physical Model authorized / PM-00 bootstrap**
- Last updated: 2026-08-18

## Stage boundary

```text
Product / North Star
CURRENT

Core Domain Model / Domain Atlas
CLOSED

Logical Model
CLOSED

Phase 5 requirements
CURRENT

Phase 6 AI/context/runtime/integration boundaries
CURRENT

Phase 7 durable-execution contract
CURRENT

Phase 8 governed-operation/effect contract
CURRENT

Phase 9 search/observability/calendar/solver pressure
CURRENT

Phase 10 Physical benchmark method
CURRENT / QA PASS / ACTIVE INPUT

Phase 11 repository engineering safety
QA PASS

Phase 12 + independent Pre-Physical audit
CLOSED / PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

Physical readiness
ESTABLISHED

Physical Model
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
feature/physical-model
base main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79
mapping NOT STARTED
benchmark NOT STARTED
selection NONE

Backend Foundation / production implementation
NOT STARTED / DEFERRED
```

Domain semantics are defined by the CLOSED Domain Atlas; Logical representation/downstream hardenings by the CLOSED Whole Logical Model. This overview introduces no new semantic owner and does not select a Physical mechanism.

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
                                                  |-- AI evaluation / promotion boundary
                                                  |-- provider-neutral tool/action interfaces
                                                  |-- bounded async + durable execution runtime boundary
                                                  |-- observability / operational controls
                                                            |
                                                            v
                                                Physical persistence/runtime
                                                ACTIVE BENCHMARK/DESIGN WORKSTREAM
                                                NONE SELECTED YET
                                                            |
                                                StorageProvider / object storage
```

External providers, assistants, caches, indexes, projections, solver candidates, workflow/runtime state and device-local stores are not alternate canonical LifeOS truth merely because they contain data.

## Client responsibilities

Clients own presentation, navigation, local interaction state, secure session handling, platform capabilities and collection of user intent/confirmation where required.

Any future multi-device/offline implementation must obey Phase 5 operation-specific freshness, expected-state, conflict, governance and sensitive-data requirements. Clients do not own canonical persistence or critical authorization/Domain invariants.

UI actions may request governed operations; UI labels/buttons do not define semantic operation identity.

## Backend boundary responsibilities

A future backend must enforce accepted semantics through technical services, including:

- semantic target/operation validation;
- governed operation/effect admission + multi-axis result semantics;
- authorization enforcement without collapsing Principal, Actor, Authority, Consent or Visibility;
- expected-state/conflict handling;
- autonomy/preview/confirmation according to consequence/governance;
- provenance/material history/correction/reconciliation;
- truthful multi-owner consistency or explicit staged/partial outcomes;
- provider-state vs canonical-state separation;
- selective projection/disclosure;
- scheduling/replanning and deterministic calculation/constraint services;
- optional solver candidate generation rather than direct canonical writes;
- AI context construction/provider-neutral routing;
- versioned/reproducible evaluation before promotion of materially consequential AI behavior changes;
- provider/integration orchestration;
- bounded background work vs durable long-running coordination by operation class;
- search/retrieval projections separated from canonical state;
- privacy-safe observability and operational controls.

Concrete routes/DTOs, AuthZ engine, AI eval tooling and durable-runtime binding remain later decisions. Physical persistence structures are now the subject of the active Physical workstream, but no candidate mapping/schema is authorized by PM-00 bootstrap itself.

## Governed operation/effect responsibility

Where material, consequential operations preserve:

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
idempotency/equivalence
correlation/causation
execution class
deadline/expiry/technical cancellation
canonical result
provider/external result
runtime result
conflict/partial/reconciliation/provenance
```

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completion != Actual automatically
runtime cancellation != Domain cancellation automatically
```

## Durable execution responsibility

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          SQLite-capable local/bounded Python use
          PostgreSQL-recommended production
          distributed multi-server PostgreSQL-coupled
```

No runtime creates exactly-once external reality. Runtime/workflow IDs remain technical and do not become Domain/material-state identity.

## Canonical state responsibility

Any Physical persistence must preserve owner-specific identity/lifecycle boundaries, discriminated reference families, planned/current/actual/observed/derived distinctions, relationship/governance semantics, provider/canonical separation, material history/correction/reconciliation/retention integrity, bounded flexible/provider metadata and unresolved/candidate meaning where not established.

```text
Person != Account != Principal != Actor
provider state != canonical state
derived projection != canonical truth
absence / unknown != false
AI / solver inference != accepted canonical effect
```

All `WL-H01..WL-H12` remain mandatory downstream.

## Active Physical benchmark posture

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
G0 no-specialized-store baseline vs G1 Neo4j

SEARCH / VECTOR
S0 structured + lexical/full-text vs S1 bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first; specialist only on demonstrated gap/benefit
```

Phase 10 defines evidence methodology. `docs/physical-model/**` defines how the active workstream executes it.

```text
hard correctness gates before score
same semantics + candidate-idiomatic mapping
LOW/BASE/HIGH = synthetic qualification envelopes
unexecuted tier != VERIFIED-RUN
product + version + edition + deployment = benchmark subject
PREFERRED != SELECTED
```

Current execution state is still `NOT STARTED`; PM-00 only establishes rules/test/evidence/handoff infrastructure.

## Integration responsibility

Five Integration Hub modes remain distinct:

1. canonical import;
2. sync/mirror;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider acknowledgement/result != canonical completion automatically. MCP/A2A/future protocols remain adapters.

## AI / Context Builder responsibility

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

Material consequential AI changes require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

## Search / calendar / solver / observability responsibility

- Search/index state is derived, disclosure-aware and deletion/freshness aware; search miss != canonical nonexistence.
- Calendar standards/providers are adapter pressure; recurrence/overrides/DST/floating/all-day/provider-resync semantics remain LifeOS-owned.
- Deterministic rules/heuristics remain solver baseline; OR-Tools CP-SAT is a preferred candidate; `UNKNOWN != INFEASIBLE`; solver output crosses governed effect before canonical change.
- OpenTelemetry-first/equivalent is direction; telemetry identifiers do not replace NativeRef/MaterialStateRef/Provenance/audit.

## Repository engineering safety

Effective `main` protections are remotely verified. Current owner-driven posture requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists, has zero required checks until real stable contexts exist and auto-deletes merged head branches.

`feature/physical-model` is now an active bounded branch. Benchmark-only code/evidence is not production backend infrastructure and does not become a required CI check automatically.

## Pre-Physical closure evidence

Phase 12 + independent audit passed; PR #13 integrated Pre-Physical and PR #14 aligned current truth. Physical starts from accepted `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79` without reopening that completed workstream.

## Next boundary

```text
PM-00 BOOTSTRAP
complete and remotely QA first

THEN
PM-01 READ-ONLY FIRST
freeze current PostgreSQL/TypeDB subjects and benchmark environment
verify version/edition/deployment capabilities from official primary sources
build execution inventory/evidence plan
STOP before first mapping/schema/harness write
```

Backend Foundation remains deferred until a Physical result is explicitly selected/accepted and its remaining prerequisites are satisfied.