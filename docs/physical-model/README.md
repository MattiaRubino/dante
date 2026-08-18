# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-02 DESIGN COMPLETE / PM-03 NEXT**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00 bootstrap: **QA PASS**
- PM-01 technology/candidate freeze: **PASS-CONDITIONAL**
- PM-01 benchmark-host freeze: **HOLD**
- PM-02 primary mapping design: **DESIGN COMPLETE / PM-03 NOT RUN**
- Mapping execution/deployment: **NOT STARTED**
- Benchmark execution: **NOT STARTED**
- Selected primary persistence: **NONE**
- Selected secondary graph: **NONE**
- Selected search/vector specialization: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn the accepted Pre-Physical requirements and Phase-10 benchmark method into an evidence-backed Physical Model without reopening Domain/Logical semantics or selecting infrastructure by intuition, popularity or vendor marketing.

This directory is the current Physical workstream authority for execution state. It does not replace upstream semantic/model authority.

```text
PHASE 10
HOW TO BENCHMARK

PHYSICAL MODEL
DISCOVER + DESIGN + PREFLIGHT + EXECUTE + EVALUATE + SELECT
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
11. `pm-01-technology-landscape-v1.md`;
12. `pm-02-primary-mapping-overview-v1.md` and all four PM-02 candidate mapping documents;
13. complete CLOSED Domain authority and final closure continuations when mapping semantics are involved;
14. complete CLOSED Logical authority and `WL-H01..WL-H12` when mapping semantics are involved;
15. all Phase-5 requirement packages;
16. Phase-6 AI/context/runtime + Integration Hub boundaries;
17. Phase-7 durable-execution contract;
18. Phase-8 governed-operation/effect contract;
19. Phase-9 search/observability/calendar/solver contract;
20. Phase-10 benchmark specification, scenario corpus and register;
21. current ADRs with supersession/qualification state;
22. the current Physical execution/evidence files in this directory;
23. current Git refs and branch relation to `main`.

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
POPULAR != CORRECT
USED ELSEWHERE != SELECTED
PREFERRED != SELECTED
MAPPING DESIGNED != HARD-GATE PASS
BENCHMARK PASS != IMPLEMENTATION AUTHORIZATION
```

A candidate that cannot preserve accepted semantics loses. LifeOS semantics are not weakened to rescue a technology.

## PM-01 evidence

Current read-only result:

- `pm-01-technology-landscape-v1.md` — broad technology landscape, admission/freeze evidence, cost/license/operations review and public architecture reconnaissance of similar/adjacent applications;
- `result-register-v1.md` — current candidate/disposition/result state.

PM-01 status:

```text
TECHNOLOGY DISCOVERY                 PASS
APPLICATION ARCHITECTURE RECON       PASS
PRIMARY ADMISSION                    PASS
EXACT SUBJECT FREEZE                 PASS for P0/P1/P2/P3 qualification subjects
LICENSE/COST REVIEW                  PASS-CONDITIONAL
PYTHON/CLIENT REVIEW                 PASS
BACKUP/EVOLUTION REVIEW              PASS-CONDITIONAL
HA/PRODUCTION-TOPOLOGY REVIEW        PASS-CONDITIONAL
BENCHMARK HOST FREEZE                HOLD

PM-01 OVERALL
PASS-CONDITIONAL
```

The host HOLD must be closed before executable benchmark evidence begins. It does not imply a technology failure and does not block static PM-02/PM-03 design review.

## Current admitted primary candidates

```text
P0 PostgreSQL 18.4
self-hosted single-node qualification subject
psycopg 3.3.4
ADMIT
pre-existing preferred baseline
NOT SELECTED

P1 TypeDB CE 3.12.3
self-hosted single-node qualification subject
official driver 3.12.3
ADMIT
mandatory semantic challenger
NOT SELECTED

P2 XTDB 2.1.0
self-hosted qualification subject
ADMIT
production topology HOLD
temporal/bitemporal challenger
NOT SELECTED

P3 SurrealDB Community 3.2.3
self-hosted single-node RocksDB
Python SDK 2.0.0
ADMIT-CONDITIONAL
multimodel challenger
NOT SELECTED
```

`ADMIT` means only that the candidate merits Physical mapping/hard-gate evidence. No hard gate has passed yet.

## PM-02 primary mapping package

PM-02 designs the best candidate-native representation of the **same** closed Logical Model for all four admitted primary candidates.

Current package:

- `pm-02-primary-mapping-overview-v1.md` — cross-candidate mapping oracle, comparison and PM-03 proof obligations;
- `mappings/postgresql-18.4-v1.md` — `PM02-PG-001`;
- `mappings/typedb-3.12.3-v1.md` — `PM02-TDB-001`;
- `mappings/xtdb-2.1.0-v1.md` — `PM02-XT-001`;
- `mappings/surrealdb-3.2.3-v1.md` — `PM02-SDB-001`.

PM-02 status:

```text
P0 PostgreSQL mapping   DESIGN COMPLETE
P1 TypeDB mapping       DESIGN COMPLETE
P2 XTDB mapping         DESIGN COMPLETE
P3 SurrealDB mapping    DESIGN COMPLETE

HG-01..HG-12            NOT RUN
DDL/TypeQL/SurrealQL    NOT DEPLOYED
DATABASE INSTANCES      NOT STARTED
HARNESS/FIXTURES         NOT STARTED
BENCHMARK                NOT STARTED
SELECTION                NONE
```

### Common PM-02 rule

```text
SAME
accepted semantic owners
Reference Contracts
WL-H01..WL-H12
truth oracle
history/concurrency/governance meaning

IDIOMATICALLY DIFFERENT
physical identity anchor
relation representation
history substrate
constraint mechanism
concurrency hardening
query strategy
```

No mapping is forced into a lowest-common-denominator representation.

### Mapping distinctions

```text
PostgreSQL
owner-specific relational model
+ direct FKs where homogeneous
+ bounded technical address/state anchors where heterogeneous
+ explicit material state/history
+ transactional/serializable hardening

TypeDB
concrete owner types
+ first-class named-role relations/n-ary structures
+ role eligibility as Reference Contract enforcement
+ explicit state objects
+ narrow technical consistency guards for write-skew-sensitive invariants

XTDB
owner-specific tables
+ four separated address spaces
+ explicit MaterialStateRef records
+ native bitemporality where semantically truthful
+ ASSERT-based integrity/expected-state checks
+ serialized DML transaction model

SurrealDB
SCHEMAFULL owner tables
+ typed record links
+ specific binary relation tables only where semantically binary
+ contextual records for n-ary/material structures
+ explicit state history
+ narrow technical consistency guards under snapshot isolation
```

### MaterialStateRef remains explicit

```text
PostgreSQL xmin/xid      != MaterialStateRef
TypeDB IID/snapshot      != MaterialStateRef
XTDB system/valid time   != MaterialStateRef
SurrealDB change version != MaterialStateRef
```

Each mapping creates an explicit stable material-state address/binding where the Logical Model requires material state.

### Current vs historical state

All mappings must provide direct current-state access without lifetime replay while retaining reconstructible material history. World/effective applicability and knowledge/recording chronology stay distinguishable where material.

### Relation fidelity

Simple binary LR-03 relations may use compact candidate-native mechanisms. Qualified/consequential relations escalate to explicit contextual/material representation.

Material Agreement always preserves:

```text
one Agreement context
+ one justified terms MaterialStateRef
+ N party assent bindings to the same terms state
```

No candidate may infer this from unrelated pairwise edges.

### Expected-state / multi-owner strategy

```text
PostgreSQL
expected-state check + transaction/locks/SERIALIZABLE where required

TypeDB
expected-state match + one write transaction
+ narrow consistency guard for write-skew-sensitive invariant sets

XTDB
ASSERT preconditions + one serialized non-interactive DML transaction

SurrealDB
conditional expected-state mutation + one transaction
+ narrow consistency guard for write-skew-sensitive invariant sets
```

These are design hypotheses. PM-03 must prove they preserve WL-H05/WL-H07; no PASS is implied.

### Lazy Occurrence

All four mappings preserve the same semantic rule:

```text
pre-persistent bounded locator
= governing source + governing MaterialStateRef + recurrence family + semantic coordinate where available

when individually distinguished/addressable
-> same semantic Occurrence receives NativeRef
```

No artificial early ordinal is created for indistinguishable quota slots.

## Deferred and bounded lanes

```text
PRIMARY RESERVES
MariaDB 11.8 LTS  DEFER — first reserve
Gel 7              DEFER
CockroachDB        DEFER until real distributed/geo requirement
YugabyteDB         DEFER until real distributed/geo requirement

LANE G — SECONDARY GRAPH
G0 no-specialized-store baseline
G1 Neo4j — DEFER TO PM-08

LANE S — SEARCH / VECTOR
S0 structured + lexical/full-text baseline
S1 pgvector — DEFER TO PM-08 when PostgreSQL applicable
Qdrant/OpenSearch — specialist trigger only

LOCAL/OFFLINE
SQLite — DEFER to future bounded local/client lane

LANE E/D
bounded native mechanisms first
specialist only after explicit admission trigger
```

PM-02 does not activate these lanes.

## Technology-discovery and cost rule

LifeOS seeks the best technology fit, not the cheapest or most fashionable option.

```text
INITIAL DIRECT TECHNOLOGY / LICENSE COST
EUR 0 where realistically possible

BUT
EUR 0 != semantic requirement
EUR 0 != permission to lose quality
paid != automatic rejection
free != automatic preference
```

Decision priority remains:

```text
1. semantic correctness / Domain + Logical preservation
2. consistency / integrity / security / privacy / recovery
3. real LifeOS capability and workload fit
4. maturity / operability / maintainability / Python-tooling fit
5. measured performance and resource efficiency
6. total cost of ownership / deployment requirements
7. lock-in / exit risk / realistic migration path
```

Portability is preserved where cheap and structurally useful. Candidate-native strengths are allowed where materially better. Do not build a lowest-common-denominator abstraction to insure against a hypothetical migration.

## Application architecture reconnaissance rule

Public architecture evidence from similar/adjacent products remains supporting evidence only. It may reveal real patterns around canonical stores, sync/offline, recovery, projections, vector/search and bounded specialist infrastructure, but:

```text
USED BY NOTION != RIGHT FOR LIFEOS
USED BY LINEAR != RIGHT FOR LIFEOS
LOCAL-FIRST ELSEWHERE != LIFEOS REQUIREMENT
```

Domain + Logical + LifeOS direct evidence remain authority.

## Physical work products

Current files:

- `execution-methodology-v1.md` — mandatory PM-00..PM-14 operating sequence;
- `execution-template-v1.md` — reproducible run/mapping evidence template;
- `acceptance-test-matrix-v1.md` — hard-gate/corpus/scenario execution matrix;
- `result-register-v1.md` — current Physical results/dispositions;
- `pm-01-technology-landscape-v1.md` — PM-01 discovery/freeze evidence;
- `pm-02-primary-mapping-overview-v1.md` — PM-02 common mapping design/oracle;
- `mappings/*.md` — candidate-specific PM-02 mappings;
- `../workstreams/physical-model.md` — live save-game/handoff.

Later explicitly gated scopes may add:

```text
hard-gate preflight evidence
benchmark harness/source
fixture generators
candidate-specific executable adapters/query packs
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
NOT RUN
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

Physical benchmark-only design/code in later scopes does **not** authorize production backend implementation, concrete product API surface, Auth implementation, provider adapters or `feature/backend-foundation`.

Backend Foundation stays deferred until the Physical result is separately accepted and downstream prerequisites are satisfied.

## PM-00 QA evidence

```text
PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272

STATUS
QA PASS
```

## PM-01 evidence state

```text
RESEARCH PRE-SCOPE
622767d5435d59766459bb25a57e5afeb7dd7336

EVIDENCE
pm-01-technology-landscape-v1.md
result-register-v1.md

STATUS
PASS-CONDITIONAL

BENCHMARK HOST
HOLD
```

## PM-02 evidence state

```text
PM-02 PRE-SCOPE
fac3b5baf1813f886c4773594e6234810e5ba8c6

EVIDENCE
pm-02-primary-mapping-overview-v1.md
mappings/postgresql-18.4-v1.md
mappings/typedb-3.12.3-v1.md
mappings/xtdb-2.1.0-v1.md
mappings/surrealdb-3.2.3-v1.md

STATUS
DESIGN COMPLETE
PM-03 NOT RUN

MAPPING DEPLOYMENT
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE
```

## Current exact next step

```text
PM-02
DESIGN COMPLETE / PENDING FINAL WRITE-SCOPE QA

PM-03
NEXT AFTER PM-02 REMOTE QA
SEMANTIC MAPPING HARD-GATE PREFLIGHT

BENCHMARK HOST
HOLD — must close before executable PM-04/05+ benchmark evidence
```

Do not create executable database schemas, database instances, fixture generators or benchmark harnesses merely because the design package exists. PM-03 must challenge the mapping first.