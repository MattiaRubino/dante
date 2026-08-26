# ADR-003: Primary Database

- Status: **Superseded as final selection / retained as historical rationale**
- Date: 2026-08-02
- Updated: 2026-08-10
- Superseded for current execution: 2026-08-17
- Current replacement authority: closed Physical Model + ADR-010 + closed CP6-02 PostgreSQL Persistence Constitution

## Original decision

Use PostgreSQL as the primary source of truth.

The original decision assumed a hybrid persistence model:

- typed relational structures for stable domain concepts and invariants;
- metadata/JSONB for genuinely flexible properties;
- graph-like relationship mechanisms for personal/emergent links;
- version/audit/event history for traceability.

## Original rationale

LifeOS requires strong transactions, constraints, indexing, relational consistency, history and cross-domain queryability while also supporting bounded flexible/provider-specific data. PostgreSQL offered a practical single-primary-database foundation without introducing multiple specialized stores prematurely.

## Historical post-Logical / pre-Physical posture

At the checkpoint when this ADR was qualified, the final Physical database had not yet been selected. The then-current benchmark posture was:

```text
PostgreSQL hybrid
PREFERRED PHYSICAL BASELINE AT THAT CHECKPOINT
NOT YET FINAL SELECTION

TypeDB
MANDATORY PHYSICAL BENCHMARK CHALLENGER AT THAT CHECKPOINT

Neo4j / property graph
SERIOUS SECONDARY / READ-PROJECTION CANDIDATE AT THAT CHECKPOINT

event/document mechanisms
BOUNDED CANDIDATES

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

That posture is historical evidence of the selection process. It is not current architecture.

## Consequences at that historical checkpoint

At that time:

- no final Physical database had yet been selected;
- PostgreSQL schema/table/index/key strategy was not yet authorized by the Physical phase;
- Mongo/document storage was not accepted as a universal canonical kernel;
- a graph store was not accepted as a universal canonical ontology;
- specialized stores could be adopted only where demonstrated benefit justified them;
- persistence had to preserve the closed Domain + Logical semantics regardless of technology;
- the final primary-store decision still required the separate Physical Model benchmark.

## Current replacement truth

The later Physical Model completed that benchmark and selection. Current authority is:

```text
PostgreSQL 18 major family
CLOSED / SELECTED / ACCEPTED
sole canonical DANTE persistence + material-history authority

Physical exact phase-time patch
18.4 / HISTORICAL

current repository-controlled maintenance patch
18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS
```

The detailed reusable PostgreSQL persistence doctrine is now governed by:

- `ADR-010-postgresql-persistence-constitution.md`;
- `../development/backend-cp6-02-postgresql-persistence-constitution.md`.

TypeDB/Neo4j are no longer open competitors for canonical persistence unless a future explicit architecture reopen is justified by materially changed requirements/evidence.

## Historical value retained

The original rationale remains useful evidence for why PostgreSQL became the primary candidate and why DANTE rejected premature multi-database complexity. This ADR does not override the later closed Physical selection or CP6-02 persistence doctrine.