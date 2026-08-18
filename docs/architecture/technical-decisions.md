# Technical Decisions

- Status: **Current technical direction — Physical Model target selected/accepted/integrated**
- Last updated: 2026-08-18
- Current product/app name: **DANTE** (`LifeOS` is the previous working/project name retained only where historical/technical continuity requires it)
- Pre-Physical closure activation: `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`
- Pre-Physical integration: `74593ae283ce5a1d22335502480ee3fa54be0436` via PR #13
- Post-merge Pre-Physical alignment / Physical base: `3de84bb49f9cef30e88e9bde4961ed84335daa79` via PR #14
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15

This document is a current technical summary. Detailed requirements/contracts remain authoritative in their dedicated sources; historical rationale remains in ADRs, evidence and Git.

## Stage boundary

```text
Product / North Star                         CURRENT
Domain Model / Domain Atlas                 CLOSED
Logical Model                               CLOSED
Phase 5 requirements                        CURRENT
Phase 6 AI/context/runtime/integration      CURRENT
Phase 7 durable-execution contract          CURRENT / PHYSICAL MECHANISM RESOLVED
Phase 8 governed operation/effect           CURRENT
Phase 9 search/observability/calendar/solver CURRENT / PHYSICAL MECHANISMS RESOLVED WHERE SELECTED
Phase 10 benchmark method                   CURRENT METHOD / HISTORICAL DECISION-EVIDENCE AUTHORITY
Repository engineering safety              QA PASS
Pre-Physical Coherence                      CLOSED / INTEGRATED / VERIFIED

Physical Model target
CLOSED / SELECTED / ACCEPTED
PM-13 clean-room architecture/documentation QA PASS
INTEGRATED INTO MAIN VIA PR #15
former feature/physical-model MERGED / AUTO-DELETED
selected canonical primary PostgreSQL 18.4

Direct selected-stack implementation validation
NOT STARTED / DIRECT HG PASS 0

Backend Foundation
NOT STARTED / DEFERRED

Development Profile v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE
```

## Clients and backend direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Architecture direction: modular monolith first.
- Clients use versioned governed backend contracts, not direct primary-persistence access.
- Domain/application logic remains independent from HTTP/framework handling.
- SQLAlchemy/Alembic may now be evaluated/used against the accepted PostgreSQL target within a separately authorized backend/development scope.

No production backend implementation is authorized merely by Physical closure/integration.

## Semantic/model authority

Technical design follows the accepted Domain Atlas and closed Logical Model; storage/runtime convenience does not create ontology.

Rejected for the canonical kernel:

```text
universal semantic Entity / Thing
universal generic Relationship / edge
generic EAV / property-bag ontology
provider schema as DANTE ontology
AI-output schema as DANTE ontology
unresolved AI meaning persisted as fabricated generic canonical truth
```

Bounded technical registries, discriminators, references, JSON/provider metadata, indexes and projections remain allowed where semantic ownership stays explicit.

## Accepted Physical persistence/runtime target

### Canonical primary

```text
PostgreSQL 18.4
SELECTED / ACCEPTED
```

PostgreSQL is the sole canonical persistence authority for DANTE current truth/material history through the accepted owner-specific mapping.

### PostgreSQL capability envelope

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2
```

These are implementation capabilities, not new Domain owners.

### Offline / multi-device

```text
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync sync storage
```

```text
LOCAL != CANONICAL
sync arrival order != semantic conflict resolution
consequential offline mutation -> DANTE backend revalidation -> PostgreSQL
```

No universal consequential LWW.

### Async / durable execution

```text
BOUNDED CLASS A
PostgreSQL transactional outbox + bounded worker

MATERIAL CLASS B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
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

Restate is the selected technology; deployment remains a later privacy/operability/cost profile decision. Current Python use must not assume the client-side journal encryption that current Restate Cloud documentation exposes only through TypeScript. Journal payload minimization is mandatory.

No workflow runtime creates exactly-once external reality by itself and runtime state does not become Domain ontology/history by identity.

### Object storage

```text
Cloudflare R2 Standard
EU jurisdiction
private
```

R2 stores raw bytes. `ContentArtifact` identity/metadata/provenance/Visibility/retention/hashes/object locator remain PostgreSQL-owned.

### Recovery

```text
pgBackRest 2.59.0
-> AWS S3 Standard eu-south-1
-> Versioning
-> Object Lock GOVERNANCE
-> finite policy-bound retention

R2 raw-object backup
-> separate AWS S3 eu-south-1 repository
```

Recovery copies remain noncanonical. `Object Lock Compliance` is not the default.

### Solver

```text
OR-Tools 9.15 CP-SAT
```

Solver output remains candidate/derived state. `UNKNOWN != INFEASIBLE`; solver output != accepted canonical effect.

### Observability

```text
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

Telemetry remains privacy-minimized operational state, not Domain Provenance/security audit/canonical history automatically.

## State/history/consistency direction

Implementation must preserve, where applicable:

- intended/planned vs accepted/current vs actual realization;
- Actual vs Observation/Outcome;
- canonical vs provider/external state;
- material state/history vs derived projection;
- candidate/unresolved vs established canonical meaning;
- correction/version/reconciliation vs silent overwrite;
- owner identity vs storage/provider/runtime identity;
- expected-state semantics for consequential writes;
- atomic multi-owner changes where required or truthful staged/partial state with reconciliation/compensation.

```text
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
ETag / MVCC token / provider revision != MaterialStateRef by identity
idempotency != semantic identity
absence / unknown != false
```

## Flexible/provider data and object storage

JSON/metadata may represent genuinely flexible, low-consequence, provider-specific or specialist detail; it must not hide unresolved kernel semantics.

Large file bytes remain behind the selected object-storage boundary; Content Artifact identity is not identical to blob/path/URL/provider-object identity.

## Integration Hub

Five modes remain distinct:

```text
canonical import
sync / mirror
live federated read
retrieval / index projection
action / tool integration
```

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef
provider state/effect != canonical DANTE state/effect automatically
provider/tool operation string != canonical governed effect
```

Callbacks/webhooks/polling/push are adapter mechanisms. MCP/A2A/future protocols remain adapters, not ontology/governance authority.

## AI / context / runtime

AI remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

```text
AI memory != second canonical truth store
model output != accepted canonical effect
tool invocation != authorization
runtime Agent / Principal != Domain Actor automatically
```

### Consequential AI change evaluation

Before promotion of materially consequential changes to model/version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy, DANTE requires versioned/reproducible evaluation appropriate to affected behavior.

```text
eval result != canonical DANTE truth
eval PASS != Authority
eval PASS != governed-effect authorization
```

## Governed operations/effects

Consequential operation meaning remains independent from route/UI/tool/AuthZ/workflow implementation.

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completion != Actual automatically
technical cancellation != Domain cancellation automatically
```

Where material, preserve semantic target/effect, purpose/context, expected/material state, Principal/Actor/represented party, governance, autonomy/confirmation, idempotency/equivalence, correlation/causation, execution class, deadlines/cancellation semantics and independent canonical/provider/runtime/reconciliation outcomes.

## Security / AuthZ

Later implementation preserves:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

Consequential authorization/effect provenance must be reconstructible where required. Non-human Principals do not bypass semantic governance.

## Specialized-infrastructure decision

The accepted target deliberately does **not** add a dedicated graph/search/vector/event-broker zoo.

Not selected in the target include:

```text
TypeDB / XTDB / SurrealDB primary
Neo4j
Qdrant
OpenSearch
Redis / Valkey
Kafka / RabbitMQ / NATS
Debezium
Temporal
DBOS
Celery + broker
```

Any reintroduction requires a material later requirement/evidence reopen.

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

Applicable direct obligations remain in `docs/physical-model/recommendation/post-selection-validation-register-v1.md`.

## Repository safety

Effective `main` protections remain the integration policy: PR required, main deletion/non-fast-forward blocked, review-thread resolution required, no invented required checks before stable real contexts exist. Physical integration successfully used that path through PR #15.

## Development Profile v0 boundary

The next operational design may decide which selected components are activated immediately, local/self-hosted/managed/free-tier choices where allowed, account/environment setup and upgrade triggers.

That profile does not reopen the accepted Physical target merely because a selected component is dormant or deployed differently during development.

## Explicit next boundary

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15

DIRECT IMPLEMENTATION VALIDATION
NOT STARTED / CARRIED FORWARD

NEXT
Development Profile v0 — separate operational design

Backend Foundation
NOT STARTED / requires separate explicit authorization
```
