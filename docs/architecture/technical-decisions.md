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

The Physical benchmark must test LifeOS-specific correctness/history/governance/concurrency pressure, not only synthetic throughput.

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

Current mode distinction:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Imported/synchronized data requires provenance, external identifiers/revisions as appropriate, deduplication/reconciliation semantics, and explicit separation from canonical LifeOS state.

Protocol surfaces such as MCP/A2A/future tool protocols are adapters, not LifeOS ontology.

## AI

AI access is isolated behind a replaceable/provider-neutral gateway and bounded Context Builder.

AI may:

- interpret natural language/ambiguous input;
- produce structured proposals/candidates;
- support planning/replanning/explanation;
- request additional context through bounded tools/contracts.

AI may not:

- invent physical schema;
- bypass authorization/governance;
- convert uncertainty directly into canonical truth;
- treat conversation memory as authoritative LifeOS state.

Persistent canonical state, material history, retrieved context, derived context, live external context, candidate/unresolved state and transient LLM working context remain distinct.

See [`../decisions/ADR-005-ai-gateway.md`](../decisions/ADR-005-ai-gateway.md).

## Governed effects

A concrete API route, UI action or AuthZ action string is not the canonical semantic meaning of an operation.

Later API/runtime design must preserve the Logical governed-operation/effect contract, including semantic target, effect, material/expected state where required, input/context/purpose, governance basis, idempotency/correlation and result/provenance semantics.

## Security and authorization boundary

Detailed AuthN/AuthZ architecture is not yet fixed.

Later technical design must preserve at least:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

Consequential AuthZ decisions must be reconstructible where audit/consequence requires, without turning technical enforcement state into Domain governance identity.

## Search / projections / observability

Canonical persistence, search/index projection, cache/materialization and telemetry are separate responsibilities.

Current direction:

- prefer simple/native mechanisms until demonstrated benefit justifies specialized infrastructure;
- PostgreSQL structured/full-text capability is a baseline candidate if PostgreSQL survives Physical selection;
- pgvector is a bounded semantic-retrieval candidate;
- dedicated search/vector infrastructure is not assumed;
- OpenTelemetry-first or equivalent standards-based instrumentation is the preferred observability direction, subject to privacy/data-minimization constraints.

## Durable execution

No workflow engine is selected.

A later benchmark must compare at least:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

Selection must be based on LifeOS long-running/provider/human-approval/retry/reconciliation/crash-recovery pressure.

## Development / deployment

DEV, UAT and PROD are deployment environments, not permanent Git branches.

The architecture should remain portable across local development, single-server/managed deployment and later orchestration if justified. Kubernetes is not a default requirement.

## Specialized-infrastructure rule

Specialized infrastructure requires demonstrated benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

## Current stage

```text
Domain CLOSED
Logical CLOSED
Pre-Physical Coherence IN PROGRESS
Physical NOT STARTED / NOT AUTHORIZED
Backend production implementation NOT STARTED
```

See [`README.md`](README.md) for current architecture navigation.
