# Technical Decisions

- Status: **Current technical direction**
- Last updated: 2026-08-17

This document contains current technical direction only. Historical rationale belongs in ADRs/Git/checkpoints; superseded implementation assumptions do not remain here as narrative history.

## Clients

### Web

- Next.js
- React
- TypeScript

### Mobile

- Expo
- React Native
- TypeScript
- Android and iOS from the same mobile codebase where practical

Web and mobile are separate clients of the same product. They share contracts/types/design primitives where useful while retaining platform-appropriate interfaces.

## Backend platform direction

Current direction:

- Python
- FastAPI
- Pydantic
- modular monolith

SQLAlchemy and Alembic are **not yet final architecture commitments**. They remain likely implementation candidates if the accepted Physical Model uses a relational persistence design compatible with them.

Clients use versioned LifeOS backend contracts and do not connect directly to primary persistence.

## Semantic/model authority

Technical design must follow:

1. accepted Domain Atlas;
2. closed Logical Model;
3. active Pre-Physical requirements/contracts;
4. separately accepted Physical Model when later authorized.

Technical convenience does not create a universal Entity/Thing/Relationship ontology.

The following remain rejected for canonical kernel meaning:

- universal semantic Entity/Thing root;
- universal generic Relationship/edge root;
- arbitrary canonical property bag/EAV meta-model;
- provider schema as LifeOS ontology;
- AI output schema as LifeOS ontology.

Bounded generic technical registries, discriminators, references, JSON/provider metadata, projections and indexes remain allowed where semantic ownership is preserved.

## Physical persistence posture

No Physical Model is currently selected or authorized.

Benchmark posture entering later Physical work:

- PostgreSQL hybrid — current preferred baseline;
- TypeDB — mandatory challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event-stream/event-store — bounded history/integration candidate, not primary ontology;
- document store — bounded provider/specialist/flexible candidate, not canonical kernel;
- pgvector — bounded semantic-retrieval candidate;
- generic EAV/generic edge/universal meta-model — hard reject for canonical kernel.

The Physical benchmark must test LifeOS-specific correctness/history/governance/concurrency/runtime/search/solver pressure, not only synthetic throughput.

## Data semantics and history

The system must preserve accepted distinctions including:

- intended/planned state versus current accepted state versus actual realization;
- Actual versus Observation/Outcome;
- source/provider state versus canonical LifeOS state;
- derived/projection state versus material basis;
- unresolved/candidate state versus established canonical meaning;
- correction/version/reconciliation versus silent overwrite;
- owner identity versus storage/provider identity.

Consequential writes must support expected-state semantics where stale mutation could corrupt meaning. Multi-owner changes must be atomic where required or expose staged/partial state plus reconciliation/compensation truthfully.

## Flexible and provider data

JSON/metadata may be used for genuinely flexible, low-consequence, provider-specific or specialist detail.

It must not hide a required but unresolved kernel semantic owner/relation/material state.

AI uncertainty is retained as proposal/candidate/source-backed unresolved state rather than silently persisted as generic canonical relation/property truth.

## Files / objects

Large file bytes remain behind a StorageProvider/object-storage abstraction.

Current direction:

- local development storage may be used initially;
- S3-compatible/cloud object storage may replace it later;
- LifeOS domain state stores logical references/metadata rather than machine-specific absolute paths;
- Content Artifact identity is not identical to blob/path/URL/provider-object identity.

See [`../decisions/ADR-004-storage.md`](../decisions/ADR-004-storage.md).

## Integrations

External systems are isolated behind provider/capability boundaries. Provider-specific concepts must not leak into canonical LifeOS semantics.

Current Integration Hub mode distinction:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Each material flow must identify its mode or bounded composition. Imported/synchronized data requires provenance, external identifiers/revisions as appropriate, deduplication/reconciliation semantics, and explicit separation from canonical LifeOS state.

Current hard boundaries:

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef by identity
provider state != canonical LifeOS state
provider/tool operation string != canonical governed effect
```

Canonical import requires explicit acceptance/mapping. Sync direction/conflict behavior is bounded per integration rather than universal last-write-wins. Live reads retain freshness/source/unknown state. Retrieval/index projections remain derived and deletion-aware. Action/tool integrations preserve AuthZ, expected-state, idempotency, external-effect and reconciliation semantics.

Callbacks/webhooks/polling/push are adapter mechanisms and do not create canonical truth by arrival order.

Protocol surfaces such as MCP/A2A/future tool protocols are adapters, not LifeOS ontology or governance.

See [`integration-hub-boundaries.md`](integration-hub-boundaries.md).

## AI / context / runtime

AI access is isolated behind a replaceable/provider-neutral gateway and bounded Context Builder.

The runtime preserves these categories:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder applies purpose, minimization, disclosure, provenance and freshness constraints before context is exposed to a model/tool/provider. It does not treat whole-user-history access as the default.

LifeOS does not establish a generic second canonical store called `AI memory`. Durable information receives an explicit accepted representation: canonical state, material history, candidate/unresolved, derived projection, source/content artifact, provider/external state or another bounded accepted form.

AI may:

- interpret natural language/ambiguous input;
- produce structured proposals/candidates;
- support planning/replanning/explanation;
- request additional context through bounded tools/contracts;
- request governed effects through technical contracts.

AI may not:

- invent physical schema;
- bypass authorization/governance;
- convert uncertainty directly into canonical truth;
- treat conversation memory as authoritative LifeOS state;
- treat a model/tool call as authorization or as the canonical effect itself.

AI output must be classified appropriately as answer/explanation, candidate/unresolved interpretation, structured extraction, Proposal/proposal-like candidate, scenario/recommendation or governed-effect request. Model output does not become an accepted target state merely because it is structured or high-confidence.

Configurable autonomy is consequence/governance/policy based; AI does not require universal confirmation, nor may autonomy bypass stronger constraints for sensitive/destructive/shared consequences.

Runtime Agent, Tool, Workflow, Automation, Job, service account and provider callback are technical/runtime concepts unless a separately accepted semantic role applies.

```text
runtime Agent / Principal != Domain Actor automatically
tool invocation != canonical governed operation
protocol scope != Authority / Consent / Visibility
```

External/retrieved content cannot self-authorize actions or expand Authority merely by containing instructions.

Provider/model routing, fallback, quota/cost handling and transport adaptation live in the AI Gateway. A fallback must not silently widen privacy/provider eligibility.

See [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) and [`../decisions/ADR-005-ai-gateway.md`](../decisions/ADR-005-ai-gateway.md).

## Governed operations / effects

Current detailed contract: [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md).

A concrete API route, UI action, tool name, workflow step or AuthZ action string is not the canonical semantic meaning of an operation.

Consequential operation handling preserves as applicable:

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

Current non-collapse rules include:

```text
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow complete != Actual automatically
technical cancellation != Domain cancellation automatically
```

A single `success` boolean or universal operation status is insufficient for consequential LifeOS effects.

Concrete REST/RPC/GraphQL design, route/DTO shape, command-bus implementation, public error taxonomy and runtime binding remain later decisions.

AI/tool callers use the same governed boundary as other callers. A governed-effect request is a request to the application/effect boundary, not the effect itself.

## Security and authorization boundary

Detailed AuthN/AuthZ implementation is not fixed.

Later technical design must preserve at least:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

Consequential AuthZ decisions must be reconstructible where audit/consequence requires, without turning technical enforcement state into Domain governance identity. Non-human Principals do not bypass the same semantic governance requirements.

## Durable execution

Current detailed benchmark: [`durable-execution-benchmark.md`](durable-execution-benchmark.md).

LifeOS does not adopt one universal async/workflow mechanism.

### Bounded asynchronous work

For short, bounded, cheaply reconstructible work such as publication, reindexing or simple retries:

```text
PostgreSQL + worker / transactional-outbox style
RETAIN AS BASELINE MECHANISM CLASS
```

This remains a mechanism class rather than a committed implementation; exact outbox/queue design depends on later Physical/runtime choices.

### Material durable long-running work

Dedicated durable execution is structurally justified where correctness depends on long waits/timers, human review, provider callbacks, crash-resume, material cancellation/timeouts, compensation or multi-step reconciliation.

Current dedicated candidate ranking:

```text
Restate
PREFERRED STRUCTURAL-FIT CANDIDATE — NOT SELECTED

Temporal
STRONGEST MANDATORY CHALLENGER — NOT SELECTED

DBOS
CONDITIONAL POSTGRESQL-DEPENDENT CHALLENGER — NOT SELECTED
```

No workflow engine is implemented or adopted by this ranking.

External provider reality remains outside exactly-once guarantees of any runtime. Durable replay must preserve idempotency, unknown outcome and reconciliation semantics.

If the later Physical choice/RPO/RTO/SLO/deployment assumptions materially change the coupling or operating cost, Phase 10 must pressure-test this ranking again.

## Search / retrieval projections

Canonical persistence, search/index projection, cache/materialization and semantic/vector retrieval are separate responsibilities.

Current posture:

```text
structured filters + lexical/full-text search
BASELINE

PostgreSQL native full-text
BASELINE CANDIDATE IF POSTGRESQL SURVIVES PHYSICAL SELECTION

semantic/vector retrieval
BOUNDED CAPABILITY CANDIDATE

pgvector
BOUNDED CANDIDATE IF POSTGRESQL SURVIVES PHYSICAL SELECTION

dedicated search/vector service
NOT JUSTIFIED BY DEFAULT
```

Search ranking is derived state, not canonical priority/truth. Search miss != canonical nonexistence. Index/embedding identity != Domain identity. Vector similarity != Evidence/Authority/Decision/relationship truth.

Search result inclusion, counts, ranking, snippets, autocomplete, explanations and timing remain disclosure/non-interference surfaces under `WL-H12`.

Approximate vector search must be benchmarked under authorization/scope filters, recall and deletion/redaction propagation before adoption.

See [`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md).

## Observability

Current direction:

```text
OpenTelemetry-first or equivalent standards-based instrumentation
```

No observability vendor/backend is selected.

Telemetry identifiers and semantic conventions remain technical:

```text
trace/span/request/workflow ids
!= NativeRef / MaterialStateRef / ExternalRef
```

Telemetry does not replace Domain Provenance, security audit or required material effect history by identity. Required effect/governance reconstruction cannot depend solely on sampled/expiring observability data.

Observability must support conflict/retry/backlog/provider-sync/reconciliation/search-index/deletion-propagation/solver/recovery pressure without indiscriminate sensitive payload logging.

## Calendar interoperability

LifeOS Domain/Logical time and scheduling semantics remain authoritative.

Current direction:

```text
iCalendar / JSCalendar
INTEROPERABILITY / TEST / ADAPTER PRESSURE

Google / Microsoft / other provider APIs
PROVIDER-SPECIFIC ADAPTER PRESSURE

LifeOS model
SEMANTIC AUTHORITY
```

No internal persistence shape is selected from iCalendar/JSCalendar/provider schemas.

Adapters must preserve recurrence exceptions/overrides, all-day/floating/zoned time, DST/effective-time semantics, provider identity/revision/sync-token state and provider deletion/cancellation without collapsing those into LifeOS native/material identity automatically.

Provider sync token invalidation/full resync does not invalidate or erase canonical LifeOS history.

## Solver / planning engine

Current posture:

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT IMPLEMENTED

AI
interpretation / ambiguity / explanation / cross-domain reasoning
NOT deterministic constraint authority
```

Hard constraints must not be silently relaxed. Soft preferences/objective weights remain explicit model inputs rather than universal Domain priority truth.

Solver outcomes preserve distinctions such as feasible/optimal/infeasible/unknown where applicable; `UNKNOWN != INFEASIBLE`.

Solver output remains candidate/scenario/derived state bound to a material input basis. It reaches canonical Schedule/Plan/etc state only through the governed-operation/effect contract.

No solver-service topology or objective/weighting policy is selected by this phase.

## Development / deployment

DEV, UAT and PROD are deployment environments, not permanent Git branches.

The architecture should remain portable across local development, single-server/managed deployment and later orchestration if justified. Kubernetes is not a default requirement.

## Specialized-infrastructure rule

Specialized infrastructure requires demonstrated benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Current application of the rule:

- dedicated durable execution is structurally justified for material long-running classes, but no engine is selected;
- dedicated search/vector infrastructure is not justified by default;
- OR-Tools CP-SAT is a preferred specialized solver benchmark candidate where deterministic scheduling/constraint pressure warrants it;
- policy engines, graph stores, analytics/time-series systems and other specialized systems remain bounded candidates requiring their own evidence.

## Current stage

```text
Domain CLOSED
Logical CLOSED
Phase 5 requirements CURRENT
Phase 6 AI/context/runtime/integration boundaries CURRENT
Phase 7 durable-execution benchmark CURRENT
Phase 8 governed-operation/effect contract CURRENT
Phase 9 search/observability/calendar/solver contract CURRENT
Pre-Physical Coherence IN PROGRESS
Physical NOT STARTED / NOT AUTHORIZED
Backend production implementation NOT STARTED
```

Next architecture stage after coordinated Phase 7–9 closure is Phase 10 — Physical benchmark specification/register — read-only first. This does not start or authorize the Physical Model.

See [`README.md`](README.md) for current architecture navigation.