# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-03 STATIC PREFLIGHT COMPLETE / PM-04 NOT STARTED**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Started: 2026-08-18
- Domain: **CLOSED / INTEGRATED**
- Logical: **CLOSED / INTEGRATED / WL-H01..WL-H12 ACTIVE**
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL / benchmark-host HOLD**
- PM-02: **PRIMARY MAPPING DESIGN COMPLETE**
- PM-03: **STATIC SEMANTIC HARD-GATE PREFLIGHT COMPLETE / 0 STATIC REJECTS**
- Executed hard gates: **NOT RUN**
- Database/harness: **NOT STARTED**
- Benchmark/performance: **NOT STARTED**
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
common fixture/oracle/harness
correctness/destructive execution
performance/resource qualification
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
19. read Phase-10 benchmark specification, scenario corpus and register;
20. when semantic mapping/execution is involved, read complete Whole-Logical authority and relevant decision-register continuations;
21. verify current external product/version facts from official primary sources where material;
22. issue an exact PRE-SCOPE/write gate before any new repository write.

Conversation history is secondary to repository truth.

## 3. Absolute semantic guardrails

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
STATIC PREFLIGHT != EXECUTED HARD-GATE PASS
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

A candidate failure is evidence against the candidate, not permission to weaken these.

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
5. measured performance/resource efficiency;
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

PM-00 introduced Physical methodology/evidence docs and propagated current Physical state without starting mapping/schema/backend.

## 7. PM-01 — technology discovery / candidate freeze

```text
RESEARCH PRE-SCOPE
622767d5435d59766459bb25a57e5afeb7dd7336

STATUS
PASS-CONDITIONAL

TECHNOLOGY DISCOVERY
PASS

APPLICATION ARCHITECTURE RECON
PASS

BENCHMARK HOST
HOLD
```

Evidence:

`docs/physical-model/pm-01-technology-landscape-v1.md`

PM-01 scanned relational, semantic/typed, bitemporal, multimodel, distributed SQL, graph, document, EAV/immutable, local/embedded, search/vector and adjacent application architectures.

Application reconnaissance included public architecture evidence from Notion, Linear, Anytype/any-sync, AppFlowy, Immich, Home Assistant and Cal.com as supporting evidence only.

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

All mappings remained `HG-01..HG-12 NOT RUN / NOT SELECTED` at PM-02 closure.

## 9. PM-03 — semantic hard-gate static preflight

```text
PRE-SCOPE
 db127af8c759aacf69b43d0f5a5444b04fd43759

STATUS
STATIC PREFLIGHT COMPLETE

STATIC CANDIDATE REJECTS
0

EXECUTED HARD GATES
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

### PM-03 candidate interpretation

```text
P0 PostgreSQL
9 PASS-CONDITIONAL / 3 HOLD / 0 REJECT
ADVANCE
candidate-specific static blocker: none

P1 TypeDB
7 PASS-CONDITIONAL / 5 HOLD / 0 REJECT
ADVANCE WITH CONCURRENCY HOLD
candidate-specific: HG-04/HG-05

P2 XTDB
7 PASS-CONDITIONAL / 5 HOLD / 0 REJECT
ADVANCE WITH REFERENCE/CONSTRAINT HOLD
candidate-specific: HG-02/HG-03
production topology HOLD remains

P3 SurrealDB
7 PASS-CONDITIONAL / 5 HOLD / 0 REJECT
ADVANCE WITH CONCURRENCY HOLD
candidate-specific: HG-04/HG-05
```

Counts are not scores.

### Generic execution HOLDs for all candidates

```text
HG-09
old-backup restore / redaction anti-resurrection not executed

HG-11
V1->V2 evolution not executed

HG-12
backup/restore/recovery evidence not executed
```

These HOLDs are mandatory honesty, not negative candidate judgments.

## 10. PM-03 critical findings

### PostgreSQL

No static semantic blocker. Main future risk is keeping heterogeneous address anchors purely technical and choosing transaction strength that actually closes each consequential race.

### TypeDB

Relation/role/cardinality mapping is structurally strongest. Snapshot isolation is the central risk. PM-02's narrow `consistency-guard` must prove write-skew closure on the exact subject.

### XTDB

Native bitemporal/serialized-DML model is structurally strong for chronology and concurrency. Main risk is reference/cardinality integrity without conventional FK/cardinality constraints. Complete `ASSERT` mutation discipline must be proved, not assumed.

### SurrealDB

Multimodel mapping survives only because canonical tables remain SCHEMAFULL and n-ary/material relations are not forced into binary graph edges. Snapshot-isolation guard proof remains mandatory.

## 11. Executed proof remains zero

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

Do not promote PM-03 preflight results to executed HG PASS.

## 12. First executable correctness pressure pack

Shared core:

```text
SC-001 same-base consequential race
SC-003 atomic multi-owner mutation
SC-009 stale/offline divergence
SC-010 correction without false rewrite
SC-012 NativeRef non-reuse
SC-015 typed n-ary relation fidelity
SC-016 selective disclosure without source leakage
SC-022/023 DST gap/fold
SC-024 occurrence override
SC-030 V1->V2 evolution
SC-011/031 old-backup restore + anti-resurrection
```

Candidate-specific:

```text
PostgreSQL
wrong-family/dangling anchor
Read-Committed negative control
stronger transaction/locking positive control

TypeDB
snapshot write-skew negative control
shared consistency-guard positive control

XTDB
missing/wrong-family reference
cardinality/uniqueness race
incomplete ASSERT negative control
complex non-interactive governed mutation

SurrealDB
snapshot write-skew negative control
shared consistency-guard positive control
record-union/reference rejection
binary relation vs n-ary Agreement
```

## 13. Benchmark-host HOLD

Before reproducible executable evidence, the actual execution host must be verified and frozen.

Required fields:

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

Do not infer this from remembered conversation hardware.

The host HOLD does not invalidate PM-01/02/03 documentation evidence, but it blocks truthful executable benchmark claims.

## 14. Fixed Physical roadmap

```text
PM-00  Bootstrap / authority freeze                         PASS
PM-01  Technology discovery / candidate freeze             PASS-CONDITIONAL
PM-02  Primary candidate mapping design                    COMPLETE
PM-03  Semantic hard-gate static preflight                 COMPLETE
PM-04  Common fixture/oracle + candidate harness           NOT STARTED
PM-05  Correctness/destructive execution                   NOT STARTED
PM-06  LOW/BASE/HIGH + performance                         NOT STARTED
PM-07  Recovery/evolution/failure evidence                 NOT STARTED
PM-08  Secondary lanes where justified                     NOT STARTED
PM-09  Scoring + sensitivity                               NOT STARTED
PM-10  Recommendation                                      NOT STARTED
PM-11  Explicit selection gate                             NOT STARTED
PM-12  Accepted Physical Model                             NOT STARTED
PM-13  Independent clean-room QA                           NOT STARTED
PM-14  Closure / protected main integration                NOT STARTED
```

The gates/order are fixed; evidence/content inside them is evolutionary.

## 15. PM-04 boundary

PM-04 is the next roadmap phase, but it must not be silently conflated with production backend implementation.

Allowed after a fresh explicit gate and host-resolution plan:

```text
common synthetic fixture generator
semantic oracle/assertion pack
candidate-specific benchmark-only schemas/adapters/query packs
container/native qualification deployment files
raw evidence manifest structure
```

Still forbidden:

```text
production backend schema/migrations
FastAPI routes/DTOs
AuthN/AuthZ production mechanism
provider production adapters
frontend
main write/merge
technology selection
```

## 16. Test/result vocabulary

Use exact terms:

```text
NOT RUN
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
SELECTED — PM-11 explicit user-approved gate only
```

Tool invocation or official docs are never direct executed evidence.

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
5. record checkpoint here last;
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
benchmark-host HOLD

PM-02
DESIGN COMPLETE
P0 PM02-PG-001 COMPLETE
P1 PM02-TDB-001 COMPLETE
P2 PM02-XT-001 COMPLETE
P3 PM02-SDB-001 COMPLETE

PM-03
STATIC PREFLIGHT COMPLETE
0 STATIC REJECTS

P0 PostgreSQL
ADVANCE

P1 TypeDB
ADVANCE WITH CONCURRENCY HOLD

P2 XTDB
ADVANCE WITH REFERENCE/CONSTRAINT HOLD
production topology HOLD

P3 SurrealDB
ADVANCE WITH CONCURRENCY HOLD

EXECUTED HG-01..HG-12
NOT RUN ALL CANDIDATES

BENCHMARK HOST
HOLD

DATABASE/HARNESS
NOT STARTED

PERFORMANCE
NOT STARTED

SELECTION
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-04 common fixture/oracle/harness after fresh gate and benchmark-host resolution plan
```

The exact PM-03 final remote HEAD/checkpoint must be taken from Git after this handoff write; do not rely on a self-referential SHA embedded in its own creating commit.
