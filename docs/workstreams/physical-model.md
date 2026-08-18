# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-04A EVIDENCE SUFFICIENCY COMPLETE / PM-04B NOT ADMITTED / PM-05 NEXT**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Started: 2026-08-18
- Domain: **CLOSED / INTEGRATED**
- Logical: **CLOSED / INTEGRATED / WL-H01..WL-H12 ACTIVE**
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL / benchmark-host HOLD-DORMANT**
- PM-02: **PRIMARY MAPPING DESIGN COMPLETE**
- PM-03: **STATIC SEMANTIC HARD-GATE PREFLIGHT COMPLETE / 0 STATIC REJECTS**
- PM-04A: **EXTERNAL EVIDENCE SUFFICIENCY COMPLETE / 48 OF 48 CELLS CLASSIFIED / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED / FIXTURE-HARNESS NOT STARTED**
- Executed hard gates: **NOT RUN**
- Database execution: **NOT STARTED**
- Benchmark/performance execution: **NOT STARTED**
- Primary persistence selected: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## 1. Purpose

This file is the terminal save-game for the active Physical Model workstream.

A new chat/AI must be able to continue from repository truth without relying on conversation memory.

The Physical workstream is responsible for:

```text
technology discovery
candidate admission
candidate-native physical mapping
semantic hard-gate pressure
external-evidence sufficiency
conditional direct proof only when decision-relevant
correctness/destructive evidence qualification
performance/resource evidence where relevant
recovery/evolution evidence
secondary-lane justification
scoring/sensitivity
recommendation
explicit selection gate
accepted Physical Model
clean-room QA
protected-main integration
```

It does **not** authorize production backend/API/Auth implementation.

## 2. Mandatory bootstrap for every continuation

Before any further Physical write/action:

1. verify current remote `feature/physical-model` HEAD;
2. compare branch with current `main` and confirm `behind_by` truth;
3. read root `README.md`;
4. read `docs/README.md` and `docs/PROJECT-STATUS.md`;
5. read `docs/development/agent-operating-manual.md`;
6. read `docs/development/operating-rules.md`;
7. read `docs/development/documentation-and-handoff.md`;
8. read `docs/development/branching-and-environments.md`;
9. read `docs/development/repository-engineering-safety.md`;
10. read this file completely;
11. read `docs/physical-model/README.md`;
12. read `docs/physical-model/execution-methodology-v1.md`;
13. read `docs/physical-model/execution-template-v1.md`;
14. read `docs/physical-model/acceptance-test-matrix-v1.md`;
15. read `docs/physical-model/result-register-v1.md`;
16. read PM-01 landscape;
17. read PM-02 overview + all four mapping records;
18. read PM-03 overview + all four candidate preflight records;
19. read PM-04A overview + all four candidate evidence records;
20. read Phase-10 benchmark specification, scenario corpus and register;
21. when semantic mapping/evidence is involved, read complete Whole-Logical authority and relevant decision-register continuations;
22. verify current external product/version facts from official primary sources where material;
23. issue an exact PRE-SCOPE/write gate before any new repository write.

Conversation history is secondary to repository truth.

## 3. Absolute semantic/evidence guardrails

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
STATIC PREFLIGHT != EXECUTED HARD-GATE PASS
EXTERNAL EVIDENCE != DIRECT LIFEOS RUN
PUBLIC/VENDOR BENCHMARK != LIFEOS BENCHMARK
PREFERRED != SELECTED
USED ELSEWHERE != RIGHT FOR LIFEOS
```

Never introduce by convenience:

```text
universal Entity / Thing root
universal semantic Relationship/edge root
generic EAV/property-bag canonical kernel
universal Rule / Fact / WorkItem / Command root
provider IDs/revisions as canonical identity/material state
missing row == false
storage/MVCC/system-time/changefeed token == MaterialStateRef
technical AuthZ allow/deny == Domain Authority/Consent
AI/solver result == accepted canonical effect
per-recipient duplicate canonical reality
```

Reference family distinctions remain:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

State layers remain distinguishable:

```text
canonical LifeOS state
material historical state
derived/projection state
external/provider state
candidate/unresolved state
security/runtime state
```

## 4. Whole-Logical downstream obligations

`WL-H01..WL-H12` are non-negotiable:

```text
WL-H01 Agreement terms bind justified owned material state
WL-H02 Governed Operation / Effect Contract
WL-H03 Projection / Disclosure Surface Contract
WL-H04 absence != false
WL-H05 expected-state consequential concurrency
WL-H06 idempotency != identity
WL-H07 multi-owner consistency truthfulness
WL-H08 canonical != provider sync state
WL-H09 consequential derived state needs freshness/material basis
WL-H10 retention/redaction/tombstone integrity
WL-H11 consequential AuthZ provenance
WL-H12 non-interference/inference leakage
```

A candidate weakness is evidence against the candidate, not permission to weaken these.

## 5. Cost / technology policy

LifeOS seeks the best technical fit.

```text
INITIAL DIRECT TECHNOLOGY/LICENSE TARGET
EUR 0 where realistically possible

BUT
EUR 0 != semantic requirement
free != automatic preference
paid != automatic rejection
quality/correctness outrank cost
```

Decision order:

1. semantic correctness;
2. consistency/integrity/security/privacy/recovery;
3. LifeOS capability/workload fit;
4. maturity/operability/Python tooling;
5. performance/resource efficiency where decision-relevant;
6. TCO/deployment requirements;
7. lock-in/exit/migration risk.

```text
portable where cheap and useful
candidate-native where materially better
no gratuitous lock-in
no gratuitous abstraction
```

The final architecture may use one primary canonical store plus bounded specialists. Every additional engine must independently justify its complexity and may not compensate for a primary hard-gate failure.

## 6. PM-00 — bootstrap

```text
MAIN BASELINE / PM-00 PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272

QA-STATUS PROPAGATION
f5e7f5c3ea38dd02b54192705575b0a48ea3854c

STATUS
QA PASS
```

## 7. PM-01 — technology discovery / candidate freeze

```text
RESEARCH PRE-SCOPE
622767d5435d59766459bb25a57e5afeb7dd7336

TERMINAL PM-01 HEAD
fac3b5baf1813f886c4773594e6234810e5ba8c6

STATUS
PASS-CONDITIONAL

TECHNOLOGY DISCOVERY
PASS

APPLICATION ARCHITECTURE RECON
PASS

BENCHMARK HOST
HOLD / now DORMANT until direct execution admission
```

Evidence:

`docs/physical-model/pm-01-technology-landscape-v1.md`

### PM-01 admitted primary subjects

```text
P0 PostgreSQL 18.4
self-hosted single-node / psycopg 3.3.4
ADMIT
pre-existing preferred baseline
NOT SELECTED

P1 TypeDB CE 3.12.3
self-hosted single-node / driver 3.12.3
ADMIT
NOT SELECTED

P2 XTDB 2.1.0
self-hosted qualification subject
ADMIT
PRODUCTION TOPOLOGY HOLD
NOT SELECTED

P3 SurrealDB Community 3.2.3
single-node RocksDB / Python SDK 2.0.0
ADMIT-CONDITIONAL
NOT SELECTED
```

Primary reserves:

```text
MariaDB 11.8 LTS DEFER
Gel 7 DEFER
CockroachDB DEFER
YugabyteDB DEFER
```

Secondary/bounded:

```text
Neo4j DEFER PM-08
pgvector DEFER PM-08 when PostgreSQL applicable
Qdrant/OpenSearch trigger-only
SQLite future local/offline lane
```

## 8. PM-02 — candidate-native physical mapping design

```text
PRE-SCOPE
fac3b5baf1813f886c4773594e6234810e5ba8c6

TERMINAL PM-02 HEAD
db127af8c759aacf69b43d0f5a5444b04fd43759

STATUS
DESIGN COMPLETE
```

Evidence:

```text
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/mappings/typedb-3.12.3-v1.md
docs/physical-model/mappings/xtdb-2.1.0-v1.md
docs/physical-model/mappings/surrealdb-3.2.3-v1.md
```

### PM-02 mapping theses

```text
P0 PostgreSQL
owner-specific relational/hybrid
+ direct FK where homogeneous
+ bounded technical anchors for heterogeneous addressability
+ explicit material-state/history

P1 TypeDB
typed concrete entities/relations/roles
+ role/cardinality constraints
+ explicit material-state types
+ narrow consistency guards for write-skew-sensitive invariants

P2 XTDB
owner-specific SQL tables
+ four separated address spaces
+ explicit MaterialStateRef
+ native bitemporal history only where semantically aligned
+ ASSERT + serialized DML transaction

P3 SurrealDB
SCHEMAFULL owner tables
+ typed record links
+ specific binary relation tables
+ contextual records for n-ary/material structures
+ explicit material states
+ narrow consistency guards for write-skew-sensitive invariants
```

## 9. PM-03 — semantic hard-gate static preflight

```text
PRE-SCOPE
db127af8c759aacf69b43d0f5a5444b04fd43759

TERMINAL PM-03 HEAD
0e4212909bd94de076c9074302a79296d474e53f

STATUS
STATIC PREFLIGHT COMPLETE

STATIC CANDIDATE REJECTS
0

DIRECT EXECUTED HARD GATES
NOT RUN
```

Evidence:

```text
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/preflight/postgresql-18.4-v1.md
docs/physical-model/preflight/typedb-3.12.3-v1.md
docs/physical-model/preflight/xtdb-2.1.0-v1.md
docs/physical-model/preflight/surrealdb-3.2.3-v1.md
```

### PM-03 static matrix

| Gate | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| HG-01 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-02 | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-03 | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-04 | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-05 | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-06 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-07 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-08 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-09 | HOLD | HOLD | HOLD | HOLD |
| HG-10 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-11 | HOLD | HOLD | HOLD | HOLD |
| HG-12 | HOLD | HOLD | HOLD | HOLD |

## 10. PM-04A — external evidence sufficiency

```text
PRE-SCOPE
0e4212909bd94de076c9074302a79296d474e53f

STATUS
CONTENT COMPLETE / REMOTE QA PENDING AT HANDOFF WRITE TIME

48 / 48 candidate × HG cells
CLASSIFIED

EXECUTION-WORTHY gaps
0

FULL LOCAL BENCHMARK
NOT ADMITTED

TARGETED LOCAL PROOFS
0 ADMITTED

PM-04B
NOT ADMITTED

BENCHMARK HOST
HOLD / DORMANT
```

Evidence:

```text
docs/physical-model/pm-04-external-evidence-sufficiency-v1.md
docs/physical-model/evidence/postgresql-18.4-v1.md
docs/physical-model/evidence/typedb-3.12.3-v1.md
docs/physical-model/evidence/xtdb-2.1.0-v1.md
docs/physical-model/evidence/surrealdb-3.2.3-v1.md
```

### PM-04A evidence classes

```text
EXT-SUFFICIENT
MAP-SUFFICIENT
KNOWN-STRUCTURAL-COST
DEFER-FINALIST
RESIDUAL-GAP
EXECUTION-WORTHY
```

Direct execution remains a separate ledger. No external evidence class is a direct HG PASS.

### PM-04A key findings

#### PostgreSQL

```text
CURRENT COMPARATIVE LEADER
confidence HIGH engine fundamentals / MEDIUM-HIGH LifeOS mapping
0 execution-worthy gaps
```

Strong external evidence exists for FK/constraint primitives, true Serializable transactions, backup/PITR and controlled upgrades. Remaining LifeOS pressure is mapping discipline, disclosure/system policy and finalist recovery/evolution rehearsal.

#### TypeDB

```text
PRINCIPAL SEMANTIC CHALLENGER
confidence MEDIUM-HIGH
0 execution-worthy gaps
```

Relation/role/n-ary semantics remain strongest. Snapshot-isolation uncertainty is narrowed: documented same-data write conflict makes the narrow shared consistency-guard pattern conditionally credible. Correct guard coverage/scoping remains a design/operability cost, not an unknown primitive requiring a toy local test now.

#### XTDB

```text
DISTINCTIVE TEMPORAL/BITEMPORAL CHALLENGER
confidence MEDIUM-HIGH temporal / MEDIUM overall primary fit
0 execution-worthy gaps
PRODUCTION TOPOLOGY HOLD remains
```

Serialized/serializable DML + ASSERT strongly supports concurrency semantics. No native FK and no general uniqueness beyond `_id` are documented structural costs; a local test cannot remove the permanent requirement for manual integrity discipline.

#### SurrealDB

```text
CREDIBLE MULTIMODEL CHALLENGER
confidence MEDIUM
0 execution-worthy gaps
```

SCHEMAFULL/typed relation capability and write-write conflict semantics are documented. The consistency guard is conditionally credible; explicit long-lived material history still remains necessary. No unique primary advantage has yet displaced the first three.

## 11. Non-scored comparative ordering after PM-04A

Not PM-09 score, `PREFERRED` or `SELECTED`:

```text
1 PostgreSQL
2 TypeDB
3 XTDB
4 SurrealDB
```

Rationale:

- PostgreSQL currently has the lowest aggregate primary-store structural risk and mature integrity/concurrency/recovery tooling;
- TypeDB has the best relation-semantic fit but additional concurrency/operations discipline;
- XTDB has the strongest native chronology proposition but meaningful manual integrity/topology costs;
- SurrealDB has credible multimodel consolidation but not yet a primary advantage strong enough to offset comparative risks.

The ordering remains reopenable by material later evidence.

## 12. Direct execution remains zero

```text
DATABASE INSTANCE
NOT STARTED

FIXTURE GENERATOR
NOT STARTED

HARNESS
NOT STARTED

CONCURRENCY TESTS
NOT RUN

RESTORE TESTS
NOT RUN

MIGRATION TESTS
NOT RUN

LOW/BASE/HIGH
NOT RUN

WEIGHTED SCORES
NOT RUN
```

Do not promote PM-04A sufficiency classifications to direct HG PASS.

## 13. Residual/finalist obligations

### All candidates

```text
HG-08 / WL-H12
system-level non-interference proof may remain for finalist/downstream design

HG-09
old-backup anti-resurrection = DEFER-FINALIST

HG-11
actual LifeOS V1 -> V2 semantic migration = DEFER-FINALIST

HG-12
semantic post-restore verification = DEFER-FINALIST
```

### Candidate-specific

```text
PostgreSQL
heterogeneous anchor complexity = mapping pressure
reopen direct proof only on concrete leakage/unmaintainability

TypeDB
consistency-guard coverage = known design/operability cost
reopen targeted proof only if ranking becomes dependent on it

XTDB
manual RI/cardinality = known structural cost
production topology HOLD remains

SurrealDB
consistency-guard coverage = known design/operability cost
explicit material history remains required
reopen targeted proof only if ranking becomes dependent on it
```

## 14. Benchmark-host posture

```text
BENCHMARK HOST
HOLD / DORMANT
```

It is **not a blocker** for PM-04A or evidence-only PM-05 work.

It becomes an active blocking prerequisite before any separately admitted reproducible direct execution claim.

Required fields then remain:

```text
host identity
CPU
RAM
storage device/type
filesystem
free disk budget
OS/build/kernel
container/native engine + version
network/topology
resource limits
background load policy
clock/timezone
```

Never infer this from remembered conversation hardware.

## 15. Fixed Physical roadmap

```text
PM-00  Bootstrap / authority freeze                         PASS
PM-01  Technology discovery / candidate freeze             PASS-CONDITIONAL
PM-02  Primary candidate mapping design                    COMPLETE
PM-03  Semantic hard-gate static preflight                 COMPLETE
PM-04A External evidence sufficiency                       COMPLETE subject to current remote QA
PM-04B Conditional fixture/oracle/harness                  NOT ADMITTED
PM-05  Correctness/destructive evidence qualification      NEXT / NOT STARTED
PM-06  Scale/performance evidence                           NOT STARTED
PM-07  Recovery/evolution/failure evidence                 NOT STARTED
PM-08  Secondary lanes where justified                     NOT STARTED
PM-09  Scoring + sensitivity                               NOT STARTED
PM-10  Recommendation                                      NOT STARTED
PM-11  Explicit selection gate                             NOT STARTED
PM-12  Accepted Physical Model                             NOT STARTED
PM-13  Independent clean-room QA                           NOT STARTED
PM-14  Closure / protected main integration                NOT STARTED
```

The numbered sequence is unchanged; PM-04A/04B are sub-stages inside PM-04.

## 16. PM-05 next boundary

PM-05 is now an **evidence-backed correctness/destructive qualification** phase.

It must begin with a fresh explicit gate and should:

1. map `C0..C7` / `SC-001..SC-035` to PM-04A external/mapping evidence;
2. distinguish capability proof, mapping proof, known structural cost and direct execution;
3. keep every unexecuted scenario exactly `NOT RUN`;
4. identify finalist-only/direct obligations explicitly;
5. reopen PM-04B only for a genuinely unresolved decision-relevant question;
6. avoid local execution by default.

No schema/harness/database deployment is implicitly authorized by PM-05 being next.

## 17. Git/write discipline

For every next write scope:

```text
BRANCH
feature/physical-model unless explicitly changed

PRE-SCOPE
exact remote HEAD immediately before first write

CREATE
exact allow-list

UPDATE
exact allow-list

DELETE
exact allow-list

OUT OF SCOPE
explicit
```

After writes:

1. compare PRE-SCOPE -> branch HEAD;
2. verify added/modified/deleted/unexpected paths;
3. require `behind_by 0` unless separately authorized integration changed main;
4. read back critical payloads remotely;
5. record checkpoint here last where possible;
6. do not rewrite historical evidence to make current state look cleaner.

## 18. Current resume summary

```text
REPO
MattiaRubino/lifeos

ACTIVE WORKSTREAM
Physical Model

BRANCH
feature/physical-model

MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

DOMAIN
CLOSED

LOGICAL
CLOSED
WL-H01..WL-H12 ACTIVE

PM-00
QA PASS

PM-01
PASS-CONDITIONAL
benchmark-host HOLD / DORMANT

PM-02
DESIGN COMPLETE
P0 PM02-PG-001 COMPLETE
P1 PM02-TDB-001 COMPLETE
P2 PM02-XT-001 COMPLETE
P3 PM02-SDB-001 COMPLETE

PM-03
STATIC PREFLIGHT COMPLETE
0 STATIC REJECTS

PM-04A
EVIDENCE SUFFICIENCY COMPLETE
48/48 cells classified
0 EXECUTION-WORTHY gaps

P0 PostgreSQL
CURRENT COMPARATIVE LEADER

P1 TypeDB
PRINCIPAL SEMANTIC CHALLENGER

P2 XTDB
DISTINCTIVE TEMPORAL CHALLENGER
production topology HOLD

P3 SurrealDB
CREDIBLE MULTIMODEL CHALLENGER

PM-04B
NOT ADMITTED

DIRECT HG-01..HG-12
NOT RUN ALL CANDIDATES

DATABASE/HARNESS
NOT STARTED

PERFORMANCE
NOT STARTED

SELECTION
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-05 evidence-backed correctness/destructive qualification after fresh gate
NO local execution by default
```

The exact PM-04A final remote HEAD/checkpoint must be taken from Git after this handoff write; do not rely on a self-referential SHA embedded in its own creating commit.
