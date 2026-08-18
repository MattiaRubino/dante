# System Overview

- Status: **Current architecture overview — Physical Model target selected/accepted**
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

Phase 8 governed-operation/effect contract
CURRENT

Repository engineering safety
QA PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

Physical Model target
CLOSED / SELECTED / ACCEPTED
PM-13 clean-room architecture/documentation QA PASS
selected canonical primary PostgreSQL 18.4

Direct selected-stack implementation validation
NOT STARTED / DIRECT HG PASS 0

Backend Foundation / production implementation
NOT STARTED / DEFERRED

Development Profile v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE
```

Domain semantics are defined by the CLOSED Domain Atlas; Logical representation/downstream hardenings by the CLOSED Whole Logical Model. This overview introduces no new semantic owner.

## Logical/system architecture

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
                                                  |-- search / retrieval services
                                                  |-- Integration Hub / provider adapters
                                                  |-- AI Gateway + Context Builder
                                                  |-- AI evaluation / promotion boundary
                                                  |-- bounded async + durable execution boundary
                                                  |-- observability / operational controls
                                                            |
                                                            v
                                                   PostgreSQL 18.4
                                                   canonical persistence
                                                      /    |    \
                                                     /     |     \
                                                 PostGIS  pgvector  FTS
                                                    |
                 -----------------------------------+-----------------------------------
                 |                                  |                                  |
          PowerSync / SQLite                 Restate runtime                    Cloudflare R2
          local/sync projection              Class-B execution                 raw object bytes
                 |                                  |                                  |
                 +-------------------------- backend authority -------------------------+
                                                    |
                                                pgBackRest
                                                    |
                                      AWS S3 recovery repositories

Operational telemetry:
OpenTelemetry -> Grafana Alloy -> Grafana Cloud EU

Constraint solving:
OR-Tools CP-SAT -> candidate output -> governed acceptance path
```

External providers, assistants, caches, indexes, projections, solver candidates, workflow/runtime state and device-local stores are not alternate canonical LifeOS truth merely because they contain data.

## Canonical ownership

```text
CANONICAL LIFEOS TRUTH
PostgreSQL 18.4

MATERIAL HISTORY
PostgreSQL 18.4

RAW OBJECT BYTES
Cloudflare R2

LOCAL/OFFLINE COPY
encrypted SQLite / noncanonical

SYNC PROJECTION
PowerSync / noncanonical

DURABLE RUNTIME STATE
Restate / noncanonical

BACKUPS
S3 / recovery only

SOLVER OUTPUT
OR-Tools / candidate only

TELEMETRY
OTel/Grafana / operational only
```

## Client responsibilities

Clients own presentation, navigation, local interaction state, secure session handling, platform capabilities and collection of user intent/confirmation where required.

Multi-device/offline behavior must obey operation-specific freshness, expected-state, conflict, governance and sensitive-data requirements. Clients do not own canonical persistence or critical authorization/Domain invariants.

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
- solver candidate generation rather than direct canonical writes;
- AI context construction/provider-neutral routing;
- versioned/reproducible evaluation before promotion of materially consequential AI behavior changes;
- provider/integration orchestration;
- bounded background work vs durable long-running coordination by operation class;
- search/retrieval separated from canonical meaning;
- privacy-safe observability and operational controls.

Concrete routes/DTOs, AuthZ engine and Development Profile v0 remain later decisions. Physical persistence technology is selected, but backend production implementation has not started.

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
PostgreSQL transactional outbox + bounded worker

DEDICATED DURABLE CLASS-B
Restate runtime — SELECTED
```

Restate deployment:

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

The deployment profile chooses between them based on privacy, operability, availability and cost. Current Python use must not assume TypeScript-only client-side journal encryption; journal minimization remains mandatory.

No runtime creates exactly-once external reality. Runtime/workflow IDs remain technical and do not become Domain/material-state identity.

## Offline / multi-device responsibility

```text
PostgreSQL canonical
→ approved PowerSync projection
→ encrypted SQLite local copy
→ offline mutation
→ LifeOS backend expected-state/governance/AuthZ revalidation
→ PostgreSQL canonical commit if valid
```

Local arrival order is not semantic conflict resolution. Universal consequential LWW is rejected. Visibility/delete/redaction changes must propagate to affected sync/local copies.

## Object responsibility

```text
ContentArtifact identity/metadata/authority
PostgreSQL

raw object bytes
Cloudflare R2 Standard / EU / private
```

R2 is not a semantic database. Public permanent object URLs/buckets are not the default.

## Recovery responsibility

```text
PostgreSQL backup
pgBackRest 2.59.0 -> AWS S3 Standard eu-south-1

R2 object backup
-> separate S3 repository
```

Versioning and Object Lock GOVERNANCE with finite policy-bound retention are the target recovery posture. Recovery copies are not canonical and restore must preserve anti-resurrection/deletion semantics.

## Canonical state responsibility

Physical persistence preserves owner-specific identity/lifecycle boundaries, discriminated reference families, planned/current/actual/observed/derived distinctions, relationship/governance semantics, provider/canonical separation, material history/correction/reconciliation/retention integrity, bounded flexible/provider metadata and unresolved/candidate meaning where not established.

```text
Person != Account != Principal != Actor
provider state != canonical state
derived projection != canonical truth
absence / unknown != false
AI / solver inference != accepted canonical effect
```

All `WL-H01..WL-H12` remain mandatory downstream.

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

- Search: PostgreSQL native FTS + `pg_trgm` + `unaccent`; pgvector for bounded vector retrieval; search/index state remains derived and disclosure-aware.
- Graph traversal: explicit PostgreSQL mappings + recursive SQL; no dedicated graph database in the accepted target.
- Calendar: standards/providers are adapter pressure; recurrence/overrides/DST/floating/all-day/provider-resync semantics remain LifeOS-owned.
- Solver: OR-Tools 9.15 CP-SAT is selected; `UNKNOWN != INFEASIBLE`; output crosses governed acceptance before canonical change.
- Observability: OpenTelemetry + Grafana Alloy + Grafana Cloud EU target; telemetry identifiers do not replace NativeRef/MaterialStateRef/Provenance/audit.

## Direct implementation-validation truth

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE/MIGRATION         NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                 NOT RUN
RESTATE                   NOT RUN
OBJECT RECOVERY           NOT RUN
SOLVER                    NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

Applicable obligations remain in `docs/physical-model/recommendation/post-selection-validation-register-v1.md`.

## Repository engineering safety

Effective `main` protections remain the integration mechanism. Normal work uses bounded branches and PRs; no direct-main bypass is authorized.

## Development Profile v0 boundary

The accepted Physical target does not decide initial deployment activation. A separate Development Profile v0 may choose which selected services run immediately, self-hosted/managed modes where allowed, free-tier/local operational choices, accounts/environments and upgrade triggers.

## Next boundary

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

PROTECTED-MAIN INTEGRATION
normal PR path

THEN
Development Profile v0

Backend Foundation
NOT STARTED / requires separate explicit authorization
```
