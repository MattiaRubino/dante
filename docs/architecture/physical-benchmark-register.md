# Physical Benchmark Register

- Status: **CURRENT — Phase 10 candidate/register content; closure pending remote QA**
- Stage: Pre-Physical Repository & Architecture Coherence
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Technology selection: **NONE**

## Purpose

Register the current candidate set, candidate role, mandatory benchmark status, known evidence/caveats, execution-time pinning requirements and future result slots for the separately authorized Physical Model benchmark.

This register is not a winner list. It prevents candidate-role drift and undocumented technology injection.

```text
REGISTERED
!= SELECTED

PREFERRED BENCHMARK CANDIDATE
!= IMPLEMENTATION AUTHORIZATION
```

## Required companion documents

Read with:

- `physical-benchmark-specification.md`;
- `physical-benchmark-scenario-corpus.md`;
- the current Pre-Physical Architecture Baseline;
- all current Phase 5–9 contracts.

# Role register

## Lane P — primary canonical persistence

### P0 — PostgreSQL hybrid

```text
ROLE
PRIMARY CANONICAL PERSISTENCE

STATUS
MANDATORY PREFERRED BASELINE
NOT SELECTED

BENCHMARK REQUIRED
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

Future result slots:

```text
HG-01..HG-12         NOT RUN
weighted score       NOT RUN
LOW                   NOT RUN
BASE                  NOT RUN
HIGH                  NOT RUN
sensitivity           NOT RUN
final disposition     NOT RUN
```

### P1 — TypeDB

```text
ROLE
PRIMARY CANONICAL PERSISTENCE

STATUS
MANDATORY CHALLENGER
NOT SELECTED

BENCHMARK REQUIRED
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

Future result slots:

```text
HG-01..HG-12         NOT RUN
weighted score       NOT RUN
LOW                   NOT RUN
BASE                  NOT RUN
HIGH                  NOT RUN
sensitivity           NOT RUN
final disposition     NOT RUN
```

# Lane G — secondary graph / traversal projection

### G0 — no specialized graph store

```text
ROLE
GRAPH/TRAVERSAL BASELINE

STATUS
MANDATORY BASELINE FOR G-LANE COMPARISON
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

Future result slots:

```text
scenario set           NOT RUN
score                   NOT RUN
operational burden      NOT RUN
final disposition       NOT RUN
```

### G1 — Neo4j / property graph

```text
ROLE
SECONDARY GRAPH / READ-PROJECTION CANDIDATE

STATUS
SERIOUS CHALLENGER
NOT SELECTED
NOT PRIMARY-LANE CANDIDATE IN PHASE 10
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

Phase 10 preparation observed that current Neo4j documentation includes GA Graph Types in recent 2026 releases. The future benchmark must therefore use the exact current capability set and edition, not an outdated assumption that the candidate lacks schema controls entirely.

Future result slots:

```text
CG-01..CG-04          NOT RUN
G-lane score          NOT RUN
LOW/BASE/HIGH         NOT RUN
net benefit           NOT RUN
final disposition     NOT RUN
```

# Lane S — search / semantic retrieval

### S0 — structured + lexical/full-text baseline

```text
ROLE
SEARCH BASELINE

STATUS
MANDATORY BASELINE
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

Future result slots:

```text
search correctness      NOT RUN
LOW/BASE/HIGH           NOT RUN
privacy/disclosure      NOT RUN
final disposition       NOT RUN
```

### S1 — pgvector

```text
ROLE
BOUNDED SEMANTIC RETRIEVAL CANDIDATE

STATUS
BOUNDED CANDIDATE
CONDITIONAL ON POSTGRESQL PRESENCE/APPLICABILITY
NOT SELECTED
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

Future result slots:

```text
CG-01..CG-04          NOT RUN
recall/precision       NOT RUN
filtered recall        NOT RUN
LOW/BASE/HIGH          NOT RUN
final disposition      NOT RUN
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

Phase 7 remains current:

```text
bounded async baseline
PostgreSQL + worker/outbox style

preferred dedicated durable candidate
Restate — NOT SELECTED

mandatory strongest challenger
Temporal — NOT SELECTED

conditional PostgreSQL-dependent challenger
DBOS — NOT SELECTED
```

Physical benchmarking must record coupling effects without turning workflow runtime into persistence ontology.

Examples:

- if PostgreSQL wins primary, DBOS economics/operational coupling may change;
- if PostgreSQL does not win primary, PostgreSQL-backed runtime choices incur an additional infrastructure dependency;
- Restate/Temporal remain independent runtime candidates and must not receive primary-persistence points;
- bounded outbox/worker feasibility is pressure on transactional primary architecture, not proof that all durable workflows belong in the primary database.

No Phase 10 result selects a durable runtime.

# Solver interaction register

Current Phase 9 posture:

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE
NOT IMPLEMENTED
```

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

# Physical benchmark result table template

The later Physical workstream SHALL fill one row per candidate/role.

| ID | Candidate | Role | Version/Edition | Hard Gates | Weighted/Role Score | LOW | BASE | HIGH | Sensitivity | Conditions | Disposition |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| P0 | PostgreSQL hybrid | primary | TBD | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| P1 | TypeDB | primary | TBD | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| G0 | no graph store | graph baseline | follows primary | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| G1 | Neo4j | secondary graph | TBD | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| S0 | structured + lexical/FTS | search baseline | follows primary | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |
| S1 | pgvector | bounded vector | TBD | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | PostgreSQL applicable | NOT RUN |
| ED0 | native/bounded event/document | bounded adjunct baseline | follows architecture | NOT RUN | — | NOT RUN | NOT RUN | NOT RUN | NOT RUN | — | NOT RUN |

# Register-level hard rules

```text
PostgreSQL baseline cannot bypass P1 TypeDB challenge
TypeDB challenge cannot bypass operational/recovery evidence
Neo4j cannot win primary role from G-lane results
pgvector cannot become semantic truth store from S-lane results
event/document mechanisms cannot become universal ontology
preferred cannot be reported as selected
candidate capability cannot be scored without version/edition/deployment context
```

# Phase 10 closure condition for this register

This register is complete for Phase 10 when remote QA confirms:

```text
primary lane candidates classified              PASS
secondary graph lane classified                  PASS
search/vector lane classified                    PASS
bounded event/document lane classified           PASS
durable-runtime coupling recorded                PASS
solver coupling recorded                         PASS
admission/removal rules present                  PASS
evidence maturity vocabulary present             PASS
future result slots present                      PASS
technology selected                              0
Physical Model started                           0
```

Phase 11/12 may consume this register, but candidate execution belongs only to a later separately authorized Physical Model workstream.
