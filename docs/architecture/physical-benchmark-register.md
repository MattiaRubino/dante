# Physical Benchmark Register

- Status: **CURRENT HISTORICAL LEDGER / Phase 10 QA PASS — consumed by the closed Physical Model**
- Stage: Physical Model candidate-role and direct-execution ledger
- Phase-time Physical state at register handoff: **AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP**
- Current Physical truth: **CLOSED / SELECTED / ACCEPTED / integrated via PR #15**
- Current selected canonical primary: **PostgreSQL 18.4**
- Direct mapping/benchmark execution recorded by this register: **NOT RUN / DIRECT HG PASS 0**
- Verified-run score: **NOT AVAILABLE**

> **Current-truth qualification:** this register preserves the Phase-10 candidate roles, evidence caveats and direct-execution slots. `NOT SELECTED` candidate labels below are truthful **Phase-10/hand-off state**, not the present winner status. PM-11/12 later selected PostgreSQL 18.4 and the bounded companion target. Conversely, later selection does **not** change any `NOT RUN` direct slot into PASS.
>
> **Naming continuity:** `DANTE` is the current product/app name. `LifeOS` references retained in this ledger reflect the previous working/project name for the same product lineage and are preserved as benchmark/evidence history.

## Purpose

Register the candidate set, candidate roles, mandatory benchmark status, known evidence/caveats, execution-time pinning requirements and direct result slots used by the Physical Model decision process.

This register was never a winner list. It prevents candidate-role drift and undocumented technology injection, while PM-11/12 own the later explicit selected truth.

```text
REGISTERED
!= SELECTED

PREFERRED BENCHMARK CANDIDATE
!= IMPLEMENTATION AUTHORIZATION

SELECTED
!= DIRECT PASS
```

## Required companion documents

Read with:

- `physical-benchmark-specification.md`;
- `physical-benchmark-scenario-corpus.md`;
- the Pre-Physical Architecture Baseline for historical constraint/handoff context;
- all current Phase 5–9 contracts;
- `docs/physical-model/pm-11-explicit-selection-v1.md` and `pm-12-accepted-physical-model-v1.md` for current selected truth;
- `docs/physical-model/README.md`, the current Physical methodology/result register and PSV register.

# Role register

## Lane P — primary canonical persistence

### P0 — PostgreSQL hybrid

```text
ROLE
PRIMARY CANONICAL PERSISTENCE

PHASE-10 STATUS
MANDATORY PREFERRED BASELINE
NOT SELECTED AT THAT PHASE

CURRENT PM-11/12 STATUS
PostgreSQL 18.4 SELECTED / ACCEPTED CANONICAL PRIMARY

BENCHMARK REQUIRED BY ORIGINAL VERIFIED-RUN METHOD
YES
```

Current rationale carried forward:

- mature transactional/relational integrity tooling;
- broad query/reporting ecosystem;
- mature concurrency primitives;
- temporal/range and full-text capabilities;
- bounded JSON/provider metadata support;
- established backup/recovery ecosystem;
- operational familiarity and broad Python support.

Primary benchmark questions:

1. Can an idiomatic PostgreSQL hybrid mapping preserve all accepted semantic owners/typed/n-ary relation families without falling into generic edge/EAV escape hatches?
2. Can expected-state and multi-owner consistency be implemented cleanly without making `MaterialStateRef` a storage token?
3. Can long material history coexist with efficient current-state queries?
4. Can selective disclosure and `WL-H12` be enforced without unsafe query/index leakage?
5. Can retention/redaction/tombstone semantics survive restore and migration?
6. Can recurrence/timezone/history semantics remain explicit and queryable?
7. Does the physical mapping remain maintainable rather than degenerating into excessive table/trigger/application-only invariant complexity?

Execution-time pinning:

```text
PostgreSQL version
extensions enabled
server configuration
HA/single-node topology
backup/PITR method
Python driver / ORM if used for benchmark harness
```

Direct result slots retained from Phase 10:

```text
HG-01..HG-12         NOT RUN
verified-run score   NOT AVAILABLE
LOW                   NOT RUN
BASE                  NOT RUN
HIGH                  NOT RUN
verified-run sensitivity NOT RUN
```

The later evidence-weighted PM-09 score is a separate ledger and does not mutate these direct slots.

### P1 — TypeDB

```text
ROLE
PRIMARY CANONICAL PERSISTENCE

PHASE-10 STATUS
MANDATORY CHALLENGER
NOT SELECTED AT THAT PHASE

CURRENT PM-11/12 STATUS
NOT SELECTED / HISTORICAL SEMANTIC RUNNER-UP

BENCHMARK REQUIRED BY ORIGINAL VERIFIED-RUN METHOD
YES
```

Current structural rationale:

- native typed entities/relations/roles/cardinality concepts are attractive for LifeOS typed and n-ary relationship families;
- type-system/inference/query model may reduce some accidental mapping complexity;
- official Python client support exists;
- candidate deserves direct whole-system competition rather than theoretical dismissal.

Primary benchmark questions:

1. Does native relation/role modeling materially simplify LifeOS semantics across the whole corpus, not only selected relationship examples?
2. Can consequential concurrency and expected-state semantics be enforced with acceptable clarity and reliability?
3. Can current-state, deep-history, reporting and aggregation workloads meet LifeOS requirements without awkward secondary systems by default?
4. Are schema evolution/migration workflows sufficiently controllable for long-lived personal history?
5. Are backup/restore/recovery capabilities adequate for the exact deployment mode under test?
6. Are clustering/HA capabilities production-suitable for the exact version/edition under test?
7. Is Python/tooling/observability/operations maturity sufficient for the target deployment envelope?
8. Does operational or ecosystem complexity offset semantic modeling benefits?

Current caveat requiring execution-time verification:

Current official TypeDB 3.x documentation observed during Phase 10 preparation contains materially different maturity framing around clustered deployment across documentation sections. The benchmark MUST NOT award HA/cluster maturity points from a generic brand claim.

Required action:

```text
pin exact TypeDB version
pin edition
pin self-hosted/cloud/deployment mode
verify authoritative version-specific cluster/HA support
execute failover/recovery where that capability affects scoring
```

Backup/recovery capabilities must likewise be tested for the exact deployment mode rather than inferred from generic documentation.

Direct result slots:

```text
HG-01..HG-12         NOT RUN
verified-run score   NOT AVAILABLE
LOW                   NOT RUN
BASE                  NOT RUN
HIGH                  NOT RUN
verified-run sensitivity NOT RUN
```

# Lane G — secondary graph / traversal projection

### G0 — no specialized graph store

```text
ROLE
GRAPH/TRAVERSAL BASELINE

PHASE-10 STATUS
MANDATORY BASELINE FOR G-LANE COMPARISON

CURRENT TARGET STATUS
NO DEDICATED GRAPH STORE IN ACCEPTED TARGET
```

Meaning:

Use the accepted primary-store query/projection capabilities for the selected graph/traversal scenarios without adding a dedicated graph database.

Purpose:

Measure whether a specialized graph system provides enough net structural/performance value to justify:

- another stateful service;
- projection synchronization;
- access/deletion propagation;
- operational/licensing burden;
- rebuild/recovery complexity.

Direct result slots:

```text
scenario set           NOT RUN
score                   NOT RUN
operational burden      NOT RUN
```

### G1 — Neo4j / property graph

```text
ROLE
SECONDARY GRAPH / READ-PROJECTION CANDIDATE

PHASE-10 STATUS
SERIOUS CHALLENGER
NOT SELECTED
NOT PRIMARY-LANE CANDIDATE IN PHASE 10

CURRENT TARGET STATUS
NOT SELECTED
```

Current rationale:

- graph traversal/query ergonomics may provide material benefit for selected LifeOS relationship/navigation workloads;
- current Neo4j releases provide stronger schema/type/constraint capabilities than older generic `schemaless graph` assumptions;
- a serious benchmark should therefore test current product capability rather than historical stereotypes.

Primary benchmark questions:

1. Which accepted LifeOS query/traversal families materially improve versus G0?
2. How much complexity is introduced when n-ary/material-state relations are projected into graph structures?
3. Can the projection remain clearly secondary/rebuildable rather than becoming hidden canonical truth?
4. How reliable/fast is incremental synchronization and full rebuild?
5. How are Visibility/access/deletion changes propagated without `WL-H12` leakage?
6. Which exact constraint/schema/backup/HA capabilities require a specific edition/license?
7. Does the net value justify operating another stateful system?

Execution-time pinning:

```text
Neo4j version
Community / Enterprise / managed edition
Graph Type / constraint features used
cluster/single-instance topology
backup/recovery capability
Python driver version
```

Current evidence note:

Phase 10 preparation observed that current Neo4j documentation includes GA Graph Types in recent 2026 releases. The benchmark must use the exact current capability set and edition, not an outdated assumption that the candidate lacks schema controls entirely.

Direct result slots:

```text
CG-01..CG-04          NOT RUN
G-lane score          NOT RUN
LOW/BASE/HIGH         NOT RUN
net benefit           NOT RUN
```

# Lane S — search / semantic retrieval

### S0 — structured + lexical/full-text baseline

```text
ROLE
SEARCH BASELINE

PHASE-10 STATUS
MANDATORY BASELINE

CURRENT TARGET STATUS
PostgreSQL native FTS + pg_trgm + unaccent SELECTED
```

Purpose:

Demonstrate how far accepted primary-store structured filtering and lexical/full-text search can satisfy LifeOS discovery/retrieval needs before specialized vector/search infrastructure is introduced.

Benchmark includes:

- structured filtering;
- lexical relevance;
- mixed text + semantic-owner/time/Visibility filters;
- deletion/access propagation;
- result non-interference;
- long-history/current-source search pressure.

Direct result slots:

```text
search correctness      NOT RUN
LOW/BASE/HIGH           NOT RUN
privacy/disclosure      NOT RUN
```

### S1 — pgvector

```text
ROLE
BOUNDED SEMANTIC RETRIEVAL CANDIDATE

PHASE-10 STATUS
BOUNDED CANDIDATE
CONDITIONAL ON POSTGRESQL PRESENCE/APPLICABILITY
NOT SELECTED AT THAT PHASE

CURRENT PM-11/12 STATUS
pgvector 0.8.6 SELECTED / DERIVED RETRIEVAL
```

Current rationale:

- can add vector similarity inside PostgreSQL deployment when PostgreSQL is part of the accepted architecture;
- supports exact and approximate vector search mechanisms;
- may avoid a separate vector service for bounded semantic retrieval.

Primary benchmark questions:

1. Does semantic retrieval materially improve accepted use cases versus S0?
2. What recall/latency tradeoff appears under exact vs ANN techniques?
3. What is recall **after** tenant/scope/Visibility filtering?
4. How quickly do deletion/redaction/access changes propagate?
5. Does vector index growth or memory/storage pressure alter primary-store operations materially?
6. Is a separate vector system actually justified beyond this bounded option?

Execution-time pinning:

```text
PostgreSQL version
pgvector version
vector dimensionality/model basis
exact / HNSW / IVFFlat or other tested technique
index parameters
filter strategy
embedding corpus/version
```

Current evidence note:

Phase 9/10 preparation identified filtering/ANN recall as material pressure. The future run must not score vector quality from unfiltered top-k latency alone.

Direct result slots:

```text
CG-01..CG-04          NOT RUN
recall/precision       NOT RUN
filtered recall        NOT RUN
LOW/BASE/HIGH          NOT RUN
```

# Lane E/D — bounded event / document mechanisms

### ED0 — native/bounded mechanism baseline

```text
ROLE
BOUNDED HISTORY / INTEGRATION / PROVIDER / FLEXIBLE REPRESENTATION

STATUS
BASELINE
```

Examples of allowed bounded uses include:

- transactional outbox/inbox records where later runtime design accepts them;
- append/audit/history structures where they do not replace canonical semantic ownership;
- provider payload remnants;
- specialist/flexible document detail;
- export/import artifacts;
- operational/event publication records.

This lane does **not** authorize universal event sourcing or document/EAV canonical modeling.

### ED-SPECIALIZED — future specialized candidate slot

```text
STATUS
NOT ADMITTED BY DEFAULT
```

A specific event-store/stream/document product is added only after an admission record proves a concrete gap or structural benefit.

Admission record must include:

```text
candidate product/version
claimed role
accepted requirement/gap
ED0 limitation
expected benefit
additional state-consistency burden
additional operational burden
benchmark scenarios added
scope/gate approval
```

Until then there is no arbitrary product shortlist.

# Durable-runtime interaction register

Phase-7 ranking at the time of this register:

```text
bounded async baseline
PostgreSQL + worker/outbox style

preferred dedicated durable candidate
Restate — NOT SELECTED AT PHASE 7/10

mandatory strongest challenger
Temporal — NOT SELECTED

conditional challenger
DBOS — NOT SELECTED
```

Current PM-11/12 resolution later selected:

```text
Class A bounded async
PostgreSQL transactional outbox + bounded worker

Class B durable runtime
Restate
```

DBOS coupling is deployment-dependent rather than universally PostgreSQL-required in Python:

```text
local / prototype / bounded single-node
SQLite-capable

production guidance
PostgreSQL recommended

distributed multi-server application
shared PostgreSQL system database required by current DBOS architecture
```

This posture was reverified against current official DBOS Python database-connection/configuration and distributed-architecture documentation on 2026-08-18.

Physical/runtime benchmarking must record coupling effects without turning workflow runtime into persistence ontology.

Examples:

- if PostgreSQL wins primary, production/distributed DBOS economics/operational coupling may improve;
- if PostgreSQL does not win primary, a production/distributed DBOS topology may introduce an additional PostgreSQL infrastructure dependency;
- SQLite capability does not by itself establish a distributed/HA production topology;
- Restate/Temporal remain independent runtime candidates and must not receive primary-persistence points;
- bounded outbox/worker feasibility is pressure on transactional primary architecture, not proof that all durable workflows belong in the primary database.

Phase 10 itself selected no durable runtime; PM-11/12 later selected Restate.

# Solver interaction register

Phase-9 posture at the time of this register:

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE
NOT IMPLEMENTED
```

Current PM-11/12 resolution later selected OR-Tools 9.15 CP-SAT. Direct solver implementation/validation remains `NOT RUN`.

Physical candidates must support efficient retrieval/material snapshot assembly and governed application of solver candidates, but solver implementation is not part of primary database selection.

A primary candidate is not penalized merely because it is not itself a constraint solver.

# Candidate admission / removal rules

## Add candidate

Add a new candidate only when at least one is true:

1. accepted requirements expose a gap in the registered set;
2. new current technology plausibly offers strong structural/measured benefit for a registered role;
3. a mandatory candidate becomes unavailable/deprecated;
4. later product/scale evidence changes the infrastructure problem materially.

A new candidate requires explicit role assignment and bounded benchmark scenarios. Do not add `interesting technologies` with no LifeOS pressure.

## Remove candidate

A mandatory candidate may be removed from future execution only with an explicit recorded rationale such as:

- product discontinued/unavailable;
- hard incompatibility proven from authoritative current evidence before implementation work;
- role superseded by an accepted upstream architecture change.

Preference is not sufficient reason to skip a mandatory challenger.

# Evidence maturity register

Before execution, classify every candidate capability used in scoring:

```text
VERIFIED-RUN
proven directly by benchmark execution

PINNED-PRIMARY-DOC
supported by version/edition-specific primary documentation

INFERRED
reasonable inference requiring validation

CONTRADICTORY / UNSTABLE
material source conflict or maturity ambiguity

UNKNOWN
not yet established
```

Operational/HA/backup hard-gate PASS should rely on `VERIFIED-RUN` where the scenario is executable, supplemented by pinned primary documentation.

`INFERRED`, `CONTRADICTORY/UNSTABLE` or `UNKNOWN` material evidence produces `HOLD` or `PASS-CONDITIONAL`, not invented certainty.

# Physical benchmark result table — historical direct-execution ledger

The rows below preserve the direct execution slots from the Phase-10 register. They are **not** the PM-09 evidence-weighted score or PM-11/12 selection record.

| ID | Candidate | Role | Phase-10 Version/Edition | Direct Hard Gates | Verified-run Score | LOW | BASE | HIGH | Direct Sensitivity | Conditions | Direct Disposition |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| P0 | PostgreSQL hybrid | primary | TBD at Phase 10 | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| P1 | TypeDB | primary | TBD at Phase 10 | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| G0 | no graph store | graph baseline | follows primary | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| G1 | Neo4j | secondary graph | TBD | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| S0 | structured + lexical/FTS | search baseline | follows primary | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| S1 | pgvector | bounded vector | TBD at Phase 10 | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | PostgreSQL applicable | NOT RUN |
| ED0 | native/bounded event/document | bounded adjunct baseline | follows architecture | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |

Current PM-11/12 selection does not alter this direct ledger. The evidence-weighted scoring/result is maintained separately under `docs/physical-model/**`.

# Register-level hard rules

```text
PostgreSQL baseline cannot bypass P1 TypeDB challenge inside the original Phase-10 method
TypeDB challenge cannot bypass operational/recovery evidence
Neo4j cannot win primary role from G-lane results
pgvector cannot become semantic truth store from S-lane results
event/document mechanisms cannot become universal ontology
preferred cannot be reported as selected before PM-11
candidate capability cannot be scored without version/edition/deployment context
selected cannot be reported as direct PASS without execution
```

# Phase 10 register status — current historical ledger

The register is remotely QA-verified complete for Phase 10 and was consumed by the now-closed Physical workstream:

```text
primary lane candidates classified              PASS
secondary graph lane classified                  PASS
search/vector lane classified                    PASS
bounded event/document lane classified           PASS
durable-runtime coupling recorded                PASS
solver coupling recorded                         PASS
admission/removal rules present                  PASS
evidence maturity vocabulary present             PASS
direct result slots present                      PASS

PHASE-TIME HANDOFF STATE
Physical workstream authorized                   PASS
Physical mapping started                         0 at handoff
benchmark execution started                      0 at handoff
technology selected                              0 at handoff

CURRENT PHYSICAL STATE
PM-11 explicit selection                         COMPLETE
PM-12 Accepted Physical Model                    COMPLETE
PM-13 architecture/documentation QA              PASS
PM-14 branch closure                             COMPLETE
PR #15 integration                               COMPLETE
selected canonical primary                       PostgreSQL 18.4
DIRECT HG PASS                                   0
LOW/BASE/HIGH                                    NOT RUN
VERIFIED-RUN SCORE                               NOT AVAILABLE
```

Phases 11 and 12 consumed the register during repository-safety and clean-room verification. The completed Physical workstream used the evidence-first method to reach an evidence-weighted decision without mutating this direct-execution ledger. Applicable direct proofs remain carried forward in the post-selection validation register.
