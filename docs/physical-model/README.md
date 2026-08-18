# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-00 QA PASS / PM-01 READ-ONLY NEXT**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00 bootstrap: **QA PASS**
- PM-01 candidate/environment freeze: **READY / NOT STARTED — READ-ONLY FIRST**
- Mapping execution: **NOT STARTED**
- Benchmark execution: **NOT STARTED**
- Selected primary persistence: **NONE**
- Selected secondary graph: **NONE**
- Selected search/vector specialization: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn the already accepted Pre-Physical requirements and Phase-10 benchmark method into an evidence-backed Physical Model without reopening Domain/Logical semantics or selecting infrastructure by intuition.

This directory is the current Physical workstream authority for execution state. It does not replace upstream semantic/model authority.

```text
PHASE 10
HOW TO BENCHMARK

PHYSICAL MODEL
DESIGN + EXECUTE + EVALUATE + SELECT
```

## Mandatory authority order

Before any Physical write or benchmark action, read current repository truth in this order:

1. root `README.md`;
2. `docs/README.md`;
3. `docs/PROJECT-STATUS.md`;
4. `docs/development/agent-operating-manual.md`;
5. `docs/development/operating-rules.md`;
6. `docs/development/documentation-and-handoff.md`;
7. `docs/development/branching-and-environments.md`;
8. `docs/development/repository-engineering-safety.md`;
9. `docs/workstreams/physical-model.md`;
10. this file;
11. complete CLOSED Domain authority and final closure continuations;
12. complete CLOSED Logical authority and `WL-H01..WL-H12`;
13. all Phase-5 requirement packages;
14. Phase-6 AI/context/runtime + Integration Hub boundaries;
15. Phase-7 durable-execution contract;
16. Phase-8 governed-operation/effect contract;
17. Phase-9 search/observability/calendar/solver contract;
18. Phase-10 benchmark specification, scenario corpus and register;
19. current ADRs with supersession/qualification state;
20. the current Physical execution/evidence files in this directory;
21. current Git refs and branch relation to `main`.

Conversation memory never outranks repository current truth.

## Non-negotiable upstream invariants

```text
DOMAIN
CLOSED — DO NOT REOPEN IMPLICITLY

LOGICAL
CLOSED — DO NOT REOPEN IMPLICITLY

WL-H01..WL-H12
MANDATORY

SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
PREFERRED != SELECTED
BENCHMARK PASS != IMPLEMENTATION AUTHORIZATION
```

A candidate that cannot preserve accepted semantics loses. LifeOS semantics are not weakened to rescue a technology.

## Current candidate lanes

Phase 10 remains authoritative for candidate roles.

```text
LANE P — PRIMARY CANONICAL
P0 PostgreSQL hybrid — mandatory preferred baseline — NOT SELECTED
P1 TypeDB            — mandatory challenger        — NOT SELECTED

LANE G — SECONDARY GRAPH
G0 no specialized graph store — baseline
G1 Neo4j — specialized secondary/read-projection challenger — NOT SELECTED

LANE S — SEARCH / VECTOR
S0 structured + lexical/full-text baseline
S1 pgvector where PostgreSQL is present/applicable — NOT SELECTED

LANE E/D — EVENT / DOCUMENT
bounded native mechanisms first
specialized product only after explicit admission trigger
```

No additional product enters a lane merely to create a larger shortlist.

## Physical work products

Current bootstrap files:

- `execution-methodology-v1.md` — mandatory PM-00..PM-14 operating sequence;
- `execution-template-v1.md` — reproducible run/mapping evidence template;
- `acceptance-test-matrix-v1.md` — hard-gate/corpus/scenario execution matrix;
- `result-register-v1.md` — current Physical results/dispositions; starts with all results NOT RUN;
- `../workstreams/physical-model.md` — live save-game/handoff.

Later gated scopes may add, without changing this rule automatically:

```text
candidate mapping specifications
benchmark harness/source
fixture generators
candidate-specific adapters/query packs
raw-evidence manifests
benchmark reports
recovery/evolution evidence
selection record
accepted Physical Model specification
```

Every new physical path requires a fresh exact write gate.

## Evidence-before-claim rules

```text
no benchmark from memory
no current capability claim from marketing alone
product + version + edition + deployment = benchmark subject
raw evidence before summary
unexecuted tier != VERIFIED-RUN
semantic hard-gate failure cannot be offset by speed
missing/contradictory evidence = HOLD
candidate-specific tuning must be disclosed
same semantics + same assertions + idiomatic candidate mapping
selection requires explicit selection gate
```

Current/version-sensitive product claims must be checked against official primary documentation and pinned to the exact subject under test.

## Hard-gate order

Performance does not count until applicable semantic/correctness gates pass.

Primary lane:

```text
HG-01 Semantic ownership preservation
HG-02 Reference-family integrity
HG-03 Typed / n-ary relation fidelity
HG-04 Expected-state consequential concurrency
HG-05 Multi-owner consistency truthfulness
HG-06 History / correction / reconciliation reconstructibility
HG-07 State-layer separation
HG-08 Governance / selective disclosure
HG-09 Retention / redaction / tombstone / restore integrity
HG-10 Temporal / recurrence / timezone fidelity
HG-11 Schema/data evolution integrity
HG-12 Recoverability / evidence quality
```

Cross-lane:

```text
CG-01 Secondary state is not canonical truth
CG-02 Deletion/correction/access propagation
CG-03 Non-interference under filtering/ranking
CG-04 Freshness/material basis
```

## Corpus and scenario authority

Phase 10 defines corpus families `C0..C7` and scenarios `SC-001..SC-035`. The Physical workstream executes them; it does not silently rewrite their semantic assertions.

Synthetic `LOW / BASE / HIGH` tiers are qualification envelopes, not business forecasts. Progressive saturation/sensitivity evidence is allowed where explicitly reported; an unmaterialized tier cannot be labeled `VERIFIED-RUN`.

## Selection boundary

Allowed interim result vocabulary:

```text
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
```

```text
PREFERRED != SELECTED
```

A final technology becomes `SELECTED` only through PM-11 explicit selection gate after required evidence, comparison and sensitivity review.

## Backend boundary

The Physical workstream may create benchmark-only mappings/harnesses in later gated scopes. It does **not** authorize production backend implementation, concrete product API surface, Auth implementation, provider adapters or `feature/backend-foundation`.

Backend Foundation stays deferred until the Physical result is separately accepted and its downstream prerequisites are satisfied.

## PM-00 QA evidence

```text
PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626
6 added / 0 modified / behind 0

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272
22 unique paths
6 added
16 modified
0 deleted
0 unexpected
behind 0

main
3de84bb49f9cef30e88e9bde4961ed84335daa79 unchanged
```

Post-QA current-truth propagation remains on the same approved 22-path scope.

## Current exact next step

```text
PM-01 — CANDIDATE / ENVIRONMENT FREEZE
READ-ONLY FIRST
READY / NOT STARTED

- re-fetch current branch/main relation
- freeze exact current PostgreSQL and TypeDB versions/editions/deployment modes
- use official primary sources for current capability claims
- capture Python driver/client compatibility
- verify backup/restore/HA/schema/evolution claims for exact subjects
- freeze available benchmark hardware/environment constraints
- build execution inventory and evidence plan
- identify unresolved environment/tooling prerequisites
- STOP before first Physical mapping/harness/schema/database write
- present a fresh exact write gate for PM-02+
```

Do not choose PostgreSQL or TypeDB during PM-01. No SQL, TypeQL, Cypher, database instance, benchmark harness or schema is authorized yet.