# LifeOS Roadmap

- Last updated: 2026-08-17
- Purpose: delivery order and architecture-stage sequencing, not a calendar commitment

## Completed foundations

### Product / North Star

Completed at the level required for current product, semantic-model and architecture work:

- accepted Product Identity / North Star;
- detailed V1 product definitions and behavior studies;
- privacy/safety/history principles;
- adaptive-intelligence and integration principles;
- multi-actor/collaboration discovery evidence for later-stage pressure.

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

The accepted Domain Atlas defines the current kernel owner set, identities/roles, semantic boundaries and reopen discipline. Product/UI terminology does not override the accepted Domain Atlas.

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

Whole-Logical state:

```text
PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream constraints
```

Logical closure does not select a concrete persistence technology, schema, API, Auth runtime or backend implementation.

## In progress

### Phase 4 — UX prototype and product-structure validation

This remains a separate product/design workstream on `prototype/phase-4-today-home`.

Primary focus includes:

- Home / Today / whole-LifeOS information architecture;
- timeline density and progressive disclosure;
- grouped views and navigation;
- complex daily scenarios;
- mobile/touch/accessibility implications;
- structural product rebaseline against the accepted Product Identity / North Star.

The UX work may continue independently, but it does not authorize backend/model implementation or redefine Domain/Logical semantics.

### Pre-Physical Repository & Architecture Coherence

**CURRENT backend/architecture preparation workstream.**

Branch: `chore/pre-physical-coherence`  
Handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)

Purpose:

- repair stale repository current-truth documentation;
- make architecture supersession explicit without destroying history;
- realign the Backend Foundation handoff to the closed Domain + Logical Models;
- establish one current Pre-Physical Architecture Baseline;
- define technical requirements that can materially constrain a future Physical Model;
- prepare technology benchmarks using LifeOS-specific pressure cases;
- finish with a clean-room repository/architecture coherence QA.

This workstream does **not** itself start the Physical Model.

## Pre-Physical work sequence

The exact operational details live in the workstream handoff. The intended high-level order is:

1. current-state inventory and freeze;
2. global entry-point alignment (`README`, roadmap, indexes, status, mandatory workflow entry docs);
3. architecture supersession cleanup;
4. Backend Foundation handoff cleanup;
5. current Pre-Physical Architecture Baseline;
6. AuthN/AuthZ requirements;
7. security/privacy, retention and recovery requirements;
8. transaction/consistency/outbox/side-effect requirements;
9. non-functional, multi-device and recovery envelope;
10. AI context/memory boundaries;
11. agent/workflow/automation/notification runtime boundaries;
12. integration modes, capability contracts and protocol-neutral boundaries;
13. durable-workflow / async benchmark;
14. governed API/command contract;
15. search, observability, calendar-interoperability and solver pressure tests;
16. Physical technology benchmark specification/register;
17. repository engineering safety alignment;
18. full clean-room coherence QA;
19. close Pre-Physical Coherence;
20. **separate explicit user gate** to decide whether to authorize a Physical Model workstream.

## Current Physical technology posture — benchmark, not selection

The closed Logical Model enters the future Physical benchmark with this posture:

- **PostgreSQL hybrid:** current preferred baseline, not final selection;
- **TypeDB:** mandatory challenger;
- **Neo4j / property graph:** serious secondary/read-projection challenger;
- **event store / event stream:** bounded history/integration mechanism, not primary ontology;
- **document store:** bounded provider/specialist/flexible use, not canonical kernel;
- **generic EAV / generic edge / universal meta-model:** hard reject for the canonical kernel;
- **pgvector:** bounded semantic-retrieval candidate if useful;
- **durable workflow technologies:** separate runtime benchmark where justified, not persistence ontology.

Technology decisions must be driven by LifeOS correctness and operational pressure rather than synthetic popularity comparisons.

## Physical Model — future separate workstream

**NOT STARTED / NOT AUTHORIZED.**

A future Physical Model may start only after Pre-Physical Coherence closes and the user explicitly authorizes a new bounded workstream with its own:

- branch;
- PRE-SCOPE;
- exact write gate;
- benchmark criteria;
- technology-selection boundary;
- validation/QA contract.

Expected benchmark pressure includes, at minimum:

- concurrent consequential mutation;
- expected-state conflict handling;
- multi-owner atomic/staged mutation;
- selective disclosure and inference leakage;
- provider divergence + reconciliation;
- material history after correction/redaction;
- recurrence/time-zone/DST behavior;
- derived-state freshness;
- AuthZ provenance;
- search projection security;
- AI proposal → approval → governed effect;
- consent/authority change during long-running execution;
- crash/retry/recovery behavior;
- backup/restore and schema evolution over existing history.

## Backend Foundation — deferred until architecture/model prerequisites are ready

**NOT STARTED.**

The old roadmap sequence in which Backend Foundation and Domain Model v0 developed in parallel is superseded by the completed Domain + Logical work.

Backend Foundation must eventually receive as inputs:

```text
CLOSED Domain Atlas
+
CLOSED Logical Model
+
accepted Physical Model
+
current architecture/runtime/security/integration contracts
```

Only then should production bootstrap, API skeleton, persistence/migrations and the first vertical slice be authorized.

The current backend toolchain direction remains Python + FastAPI + Pydantic, with SQLAlchemy + Alembic conditional on the accepted Physical persistence design. This is a direction, not a current implementation task.

## Backend implementation and vertical slices — later

After the required architecture/model stages close, implementation should proceed through bounded vertical slices rather than attempting the whole platform at once.

The old conceptual slice `Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation` must **not** be copied literally as a kernel model. Any future slice must be re-derived from the accepted Domain Atlas, Logical Model and Physical Model. Product/UI labels such as Project/Program may map to accepted profiles/compositions rather than new kernel primitives.

## Runtime and integration expansion — later

After a stable production foundation exists, later V1 work may include:

- richer scheduling/replanning;
- real AI provider integration behind governed internal contracts;
- Integration Hub adapters;
- durable async/workflow mechanisms if benchmarked/justified;
- notifications/device integrations;
- health/device providers where product flows require them;
- weather/maps and other provider integrations;
- data export/deletion/privacy operations;
- DEV/UAT/PROD deployment pipelines;
- release/versioning processes.

## Explicitly rejected or deferred by default

Do not introduce by default:

- permanent `dev`, `uat` or `prod` Git branches;
- microservices merely for architectural fashion;
- Kubernetes merely for architectural fashion;
- Mongo/document storage as the universal canonical kernel;
- a graph database as the universal canonical ontology;
- generic EAV/generic-edge/meta-model persistence for kernel semantics;
- Redis, ClickHouse, Timescale, search clusters, vector databases, event buses or workflow engines without demonstrated benefit;
- full specialist schemas for every imaginable life domain;
- implicit V2 collaboration/social implementation inside personal-first V1 work.

Specialized infrastructure may be justified by measured workload **or** sufficiently strong structural benefit in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

## Roadmap maintenance

This file defines broad sequencing and boundaries. [`PROJECT-STATUS.md`](PROJECT-STATUS.md) records the current global state. Workstream handoffs record exact operational continuation state.

Historical checkpoints and old roadmaps remain reconstructible from Git history; current roadmap wording must not rewrite historical documents to pretend later decisions were known earlier.