# System Overview

- Status: **Current architecture overview — Pre-Physical DEFINITIVE CLOSED / FINAL QA PASS / INTEGRATED**
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

Phase 7 durable-execution benchmark
CURRENT

Phase 8 governed-operation/effect contract
CURRENT

Phase 9 search/observability/calendar/solver pressure
CURRENT

Phase 10 Physical benchmark method
CURRENT / QA PASS

Phase 11 repository engineering safety
QA PASS

Phase 12 clean-room QA
QA PASS / CLOSED

Independent total audit
PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED INTO MAIN VIA PR #13
POST-MERGE VERIFIED
activation checkpoint 9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d
main integration checkpoint 74593ae283ce5a1d22335502480ee3fa54be0436

Physical readiness
ESTABLISHED

Physical Model
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

Backend Foundation / production implementation
NOT STARTED / DEFERRED

Main integration
COMPLETE / POST-MERGE VERIFIED
```

Domain semantics are defined by the CLOSED Domain Atlas; Logical representation/downstream hardenings by the CLOSED Whole Logical Model. This overview introduces no new semantic owner or Physical mechanism.

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
                                                TO BE SELECTED / BENCHMARKED
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

Concrete routes/DTOs, transaction mechanics, AuthZ engine, AI eval tooling, durable-runtime binding and persistence structures remain later decisions.

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

No runtime creates exactly-once external reality. Runtime/workflow IDs remain technical and do not become Domain identity/material-state identity.

## Canonical state responsibility

Any future persistence must preserve owner-specific identity/lifecycle boundaries, discriminated reference families, planned/current/actual/observed/derived distinctions, specific relationship/governance semantics, provider/canonical separation, material history/correction/reconciliation/retention integrity, bounded flexible/provider metadata and unresolved/candidate meaning where not established.

```text
Person != Account != Principal != Actor
provider state != canonical state
derived projection != canonical truth
absence / unknown != false
AI / solver inference != accepted canonical effect
```

All `WL-H01..WL-H12` remain mandatory downstream.

## Physical benchmark posture

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first; specialized candidate only on demonstrated gap/benefit
```

Phase 10 defines how later evidence is produced/judged. Hard correctness gates precede scoring. Candidate mappings are idiomatic but must satisfy common semantic assertions. LOW/BASE/HIGH are synthetic envelopes, not forecasts; unexecuted tiers remain unverified. `PREFERRED != SELECTED`.

## Integration responsibility

Five Integration Hub modes remain distinct:

1. canonical import;
2. sync/mirror;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider acknowledgement/result != canonical effect completion automatically. MCP/A2A/future protocols remain adapters.

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

Material consequential changes to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

Concrete eval datasets/frameworks/runners/thresholds/CI remain later engineering choices.

## Search / calendar / solver / observability responsibility

- Search/index state is derived, disclosure-aware and deletion/freshness aware; search miss != canonical nonexistence.
- Calendar standards/providers are adapter pressure; recurrence/overrides/DST/floating/all-day/provider-resync semantics remain LifeOS-owned.
- Simple deterministic rules/heuristics remain solver baseline; OR-Tools CP-SAT is a preferred candidate; `UNKNOWN != INFEASIBLE`; solver output crosses governed effect before canonical change.
- OpenTelemetry-first/equivalent is direction; telemetry identifiers do not replace NativeRef/MaterialStateRef/Provenance/audit.

## Repository engineering safety

Phase 11 verified effective `main` protections remotely. Current owner-driven posture requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists, has zero required checks until real stable contexts exist and auto-deletes merged head branches.

PR #13 successfully exercised that protected integration path and auto-deleted `chore/pre-physical-coherence` after merge.

## Definitive Pre-Physical closure and integration evidence

Phase 12 is QA PASS/CLOSED. The subsequent independent total audit found no major semantic/architectural contradiction, Domain/Logical reopen need, material knowledge loss or accidental Physical/backend start.

Activation checkpoint:

`9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`

proved:

```text
PRE-SCOPE     1bd142afe51221211bc777f6271a642911c650fc
unique paths  23
added          1
modified      22
deleted        0
unexpected     0
behind_by      0
main unchanged
critical readback PASS
```

That evidence established definitive branch-local closure. PR #13 then integrated final branch HEAD `34e9ea3b547922600cb472adf1549a321e6ddfe4` into protected `main` at merge commit `74593ae283ce5a1d22335502480ee3fa54be0436`. Post-merge compare showed one merge commit and zero file differences.

Therefore Pre-Physical Coherence is **DEFINITIVE CLOSED / FINAL QA PASS / INTEGRATED / POST-MERGE VERIFIED**.

## Next boundary

Pre-Physical integration is complete. The **Physical Model is READY FOR SEPARATE AUTHORIZATION but remains NOT STARTED / NOT AUTHORIZED**. A new explicit user authorization and fresh workstream gate are required before any Physical design/benchmark execution; Backend Foundation remains deferred until a Physical result is separately accepted.