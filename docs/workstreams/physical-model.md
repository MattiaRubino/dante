# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-01 READ-ONLY PASS-CONDITIONAL / PM-02 NOT AUTHORIZED**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Started: 2026-08-18
- PM-00 bootstrap QA: **PASS**
- PM-00 content-QA checkpoint: `8549e1c95bef2e354bd47028259e6816bf5e9272`
- PM-00 QA-status propagation checkpoint: `f5e7f5c3ea38dd02b54192705575b0a48ea3854c`
- PM-01 technology-discovery methodology checkpoint: `1da012c28bf8f9de00bdf9deee1ab407fda4ba99`
- PM-01 research PRE-SCOPE: `622767d5435d59766459bb25a57e5afeb7dd7336`
- PM-01 evidence-QA checkpoint before this handoff: `8b6cc25dfc042389be0a985c96a3a7025e20e275`
- PM-01 technology/candidate freeze: **PASS-CONDITIONAL**
- PM-01 benchmark-host freeze: **HOLD**
- Physical mapping execution: **NOT STARTED**
- Benchmark execution: **NOT STARTED**
- Primary persistence selected: **NONE**
- Secondary graph selected: **NONE**
- Search/vector specialization selected: **NONE**
- Production backend: **NOT STARTED / DEFERRED**

## Purpose

Produce the accepted LifeOS Physical Model by designing idiomatic candidate mappings, executing the already-approved Phase-10 benchmark method, preserving all closed Domain/Logical semantics, and making any technology selection only through explicit evidence-backed selection gates.

This handoff is the live save-game for the workstream. A new chat/AI must be able to continue from this repository without relying on previous conversation memory.

# 1. Current repository boundary

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL / DOMAIN ATLAS
CLOSED / INTEGRATED
DO NOT REOPEN IMPLICITLY

LOGICAL MODEL
CLOSED / INTEGRATED
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 ACTIVE DOWNSTREAM

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED INTO main VIA PR #13
POST-MERGE CURRENT-TRUTH ALIGNMENT VIA PR #14

MAIN AT PHYSICAL AUTHORIZATION
3de84bb49f9cef30e88e9bde4961ed84335daa79

PHYSICAL MODEL
AUTHORIZED / IN PROGRESS
PM-00 BOOTSTRAP QA PASS
PM-01 READ-ONLY PASS-CONDITIONAL
PM-02 NOT AUTHORIZED

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE

BACKEND FOUNDATION
NOT STARTED / DEFERRED
```

No Pre-Physical repair is pending at this workstream stage.

# 2. Mandatory bootstrap for every new chat

Before proposing or executing Physical work:

1. verify `feature/physical-model` remote HEAD and compare to current `main`;
2. read root `README.md`;
3. read `docs/README.md`;
4. read `docs/PROJECT-STATUS.md`;
5. read `docs/development/agent-operating-manual.md`;
6. read `docs/development/operating-rules.md`;
7. read `docs/development/documentation-and-handoff.md`;
8. read `docs/development/branching-and-environments.md`;
9. read `docs/development/repository-engineering-safety.md`;
10. read this complete handoff;
11. read `docs/physical-model/README.md`;
12. read `docs/physical-model/execution-methodology-v1.md`;
13. read `docs/physical-model/execution-template-v1.md`;
14. read `docs/physical-model/acceptance-test-matrix-v1.md`;
15. read `docs/physical-model/result-register-v1.md`;
16. read `docs/physical-model/pm-01-technology-landscape-v1.md`;
17. read `docs/architecture/physical-benchmark-specification.md`;
18. read `docs/architecture/physical-benchmark-scenario-corpus.md`;
19. read `docs/architecture/physical-benchmark-register.md`;
20. read the current Pre-Physical Architecture Baseline and architecture index;
21. read all four Phase-5 requirement packages;
22. read Phase-6 AI/context/runtime + Integration Hub boundaries;
23. read Phase-7 durable-execution contract;
24. read Phase-8 governed-operation/effect contract;
25. read Phase-9 search/observability/calendar/solver contract;
26. read complete Domain closure authority when mapping semantics are involved;
27. read complete Logical Model/decision register and `WL-H01..WL-H12` when mapping semantics are involved;
28. read current ADR statuses, especially superseded/qualified decisions;
29. verify current external product facts from official primary sources when versions/features are material;
30. issue an exact PRE-SCOPE/write gate before every new write scope.

Conversation history is secondary to repository truth.

# 3. Absolute semantic guardrails

The Physical Model implements/represents accepted semantics. It does not redesign them by convenience.

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
PRODUCT LABEL != ONTOLOGY ROOT
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
POPULAR != CORRECT
USED ELSEWHERE != SELECTED
PREFERRED != SELECTED
BENCHMARK PASS != IMPLEMENTATION AUTHORIZATION
```

Reject as canonical shortcuts unless a separately authorized semantic reopen changes upstream truth:

```text
universal Entity / Thing root
generic Relationship/edge as universal semantic root
generic EAV/property-bag canonical kernel
generic Command/Terms/Projection semantic root
provider IDs/schema as ontology
absent/unknown == false
ETag/storage revision == MaterialStateRef
route/UI/AuthZ string == canonical effect
AI/solver inference == accepted canonical state/effect
runtime workflow completion == Actual automatically
technical cancellation == Domain cancellation automatically
```

Contextual `Actor`, `Subject`, `Resource` remain roles/capabilities rather than universal native identities.

# 4. Identity / reference invariants

Preserve the accepted distinctions among applicable:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Never collapse by convenience:

```text
storage PK/MVCC token != MaterialStateRef automatically
provider opaque ID/revision != NativeRef/MaterialStateRef automatically
workflow/runtime ID != semantic operation identity
index/vector ID != canonical identity
```

# 5. State-layer invariants

Where applicable keep distinguishable:

```text
canonical state
material history
retrieved context
derived/projection state
live external/provider state
candidate/unresolved state
runtime/security state
transient LLM working context
```

Co-location is allowed when technically sensible; semantic equivalence is not implied by co-location.

# 6. Governed-effect / concurrency invariants

Physical design must preserve:

- expected-state conflict detection for consequential mutations;
- no universal silent last-write-wins;
- idempotency distinct from semantic identity;
- atomic multi-owner change where an accepted invariant requires it;
- truthful partial/pending/reconciliation state across non-atomic external boundaries;
- Authority/Consent/Visibility/Representation separation;
- delayed-effect governance/material revalidation where required;
- provider result separate from canonical result;
- runtime result separate from Domain/user result;
- provenance sufficient for consequential authorization/effect reconstruction.

# 7. Retention / history / recovery invariants

Physical design must support:

- current-state access without lifetime replay by default;
- material historical reconstruction where required;
- correction without pretending corrected knowledge always existed;
- category/purpose-sensitive retention;
- redaction/tombstone truthfulness;
- native identity non-reuse;
- derived/index/provider deletion propagation where applicable;
- old-backup restore that does not silently resurrect forbidden current data;
- schema/mapping evolution that preserves identity, references and historical meaning.

# 8. Temporal / search / disclosure invariants

Preserve:

- recurrence series/occurrence distinctions;
- timezone/local/floating/all-day semantics where applicable;
- DST gaps/folds and historical interpretation;
- provider calendar IDs/tokens as external state;
- search/index miss != canonical nonexistence;
- embedding similarity != relationship/evidence;
- hidden records not leaking via counts/ranking/errors/timing beyond accepted disclosure;
- stale projections exposing enough freshness/material basis for consequential revalidation.

# 9. Candidate lanes — current authority

Phase-10 remains authority for the original registered roles. PM-01 adds admitted primary challengers without selecting them.

```text
LANE P — PRIMARY

P0 PostgreSQL 18.4
mandatory preferred baseline
PM-01 ADMIT
NOT SELECTED

P1 TypeDB CE 3.12.3
mandatory semantic challenger
PM-01 ADMIT
NOT SELECTED

P2 XTDB 2.1.0
PM-01-admitted temporal/bitemporal challenger
ADMIT / PRODUCTION-TOPOLOGY HOLD
NOT SELECTED

P3 SurrealDB Community 3.2.3
PM-01-admitted multimodel challenger
ADMIT-CONDITIONAL
NOT SELECTED

LANE G — SECONDARY GRAPH
G0 no-specialized-store baseline
G1 Neo4j specialized secondary/read-projection challenger
DEFER TO PM-08
NOT SELECTED

LANE S — SEARCH/VECTOR
S0 structured + lexical/full-text baseline
S1 pgvector conditional when PostgreSQL present/applicable
DEFER TO PM-08
NOT SELECTED

LOCAL/OFFLINE
SQLite
DEFER — future bounded local/client role

LANE E/D
ED0 bounded native mechanisms first
specialized candidate only after explicit admission trigger
```

Primary reserves and current primary-benchmark rejections are recorded in `docs/physical-model/pm-01-technology-landscape-v1.md`.

No candidate may be injected because it is fashionable or merely to enlarge the shortlist. Discovery is broad; execution remains selective. A newly discovered product/lane requires a bounded admission rationale and explicit gate before mapping/benchmark execution.

# 10. Durable runtime posture — not a Physical selection

Keep Phase-7 result separate:

```text
bounded async
DB/worker/outbox mechanism class = valid baseline

Restate
preferred structural-fit dedicated durable candidate — NOT SELECTED

Temporal
strongest mandatory challenger — NOT SELECTED

DBOS
conditional challenger — NOT SELECTED
local/bounded Python SQLite-capable
production PostgreSQL-recommended
distributed multi-server PostgreSQL-coupled
```

Physical benchmarking may expose infrastructure coupling/cost effects. It must not award primary-persistence semantic points to workflow runtimes or select a runtime implicitly.

# 11. AI evaluation requirement

Material consequential AI behavior changes remain promotion-gated by versioned/reproducible evaluation.

```text
eval result != canonical LifeOS truth
eval PASS != Authority
eval PASS != governed-effect authorization
```

The Physical Model may store evaluation metadata/results only according to accepted state-layer semantics; it does not turn an eval store into canonical LifeOS truth.

# 12. Phase-10 benchmark authority

The Physical workstream MUST consume rather than reinvent:

- `physical-benchmark-specification.md`;
- `physical-benchmark-scenario-corpus.md`;
- `physical-benchmark-register.md`.

Primary hard gates:

```text
HG-01..HG-12
```

Cross-lane hard gates:

```text
CG-01..CG-04
```

Corpus/scenarios:

```text
C0..C7
SC-001..SC-035
LP-01..LP-05
LOW / BASE / HIGH synthetic qualification tiers
```

Correctness/hard gates precede performance scoring.

# 13. Evidence contract

Every meaningful run must record at least:

```text
LifeOS commit
Phase-10 commits
candidate product/version/edition/deployment
hardware/runtime
candidate configuration
mapping revision
fixture generator/seed/actual counts/hash
scenario/load profile
correctness assertions/raw result
latency/throughput where relevant
CPU/RAM/storage
query plan/profile where relevant
backup/restore evidence
migration/evolution evidence
failure-injection evidence
manual tuning
known caveats
raw artifact locations/hashes
summary/disposition
```

No secrets or real personal production data in fixtures/artifacts.

Large raw evidence may live outside Git only if durable location/hash/reproduction metadata is committed. Ephemeral CI retention alone is not closure evidence.

# 14. External research rule

Current versions/features/editions/licensing/HA/backup/driver support may change.

When they matter:

1. browse current official primary documentation;
2. pin exact subject and source applicability;
3. distinguish official claim from direct execution proof;
4. record contradictory/unclear claims as `HOLD` until resolved;
5. do not use generic marketing copy as executed capability evidence.

## Technology quality / cost / exit policy

LifeOS must seek the best technology fit, not the cheapest technology and not the most fashionable technology.

The current operating target is:

```text
INITIAL DIRECT TECHNOLOGY / LICENSE COST
EUR 0 where realistically possible

BUT
EUR 0 != semantic requirement
EUR 0 != permission to lose quality
paid != automatic rejection
free != automatic preference
```

Decision priority:

```text
1. semantic correctness / Domain + Logical preservation
2. consistency / integrity / security / privacy / recovery
3. real LifeOS capability and workload fit
4. maturity / operability / maintainability / Python-tooling fit
5. measured performance and resource efficiency
6. total cost of ownership / deployment requirements
7. lock-in / exit risk / realistic migration path
```

Cost can strongly break a near-tie, but cannot compensate for a hard semantic failure or a major structural deficit.

If the strongest technology is materially paid, proprietary or infrastructure-heavy, do not hide or discard that result. Record the actual advantage and then evaluate whether:

- an equivalent/near-equivalent zero-cost or open alternative exists;
- the paid capability is required now or only under a future condition;
- LifeOS can begin on a zero-cost topology without weakening accepted semantics or creating a dead end;
- a migration/exit strategy is justified by a real, observed risk.

Do not build large abstraction layers for hypothetical migrations. Preserve portability where cheap and structurally useful; use candidate-native strengths where they materially improve the system.

```text
portable where cheap and useful
candidate-native where materially better
no gratuitous lock-in
no gratuitous abstraction
```

The best Physical result may use one primary canonical store plus bounded specialized mechanisms. Every additional engine must independently justify its semantic, operational and cost burden.

## Application architecture reconnaissance rule

PM-01 now also consumes public primary-source architecture evidence from directly similar and structurally adjacent applications.

Current PM-01 evidence includes Notion, Linear, Anytype/any-sync, AppFlowy, Immich, Home Assistant and Cal.com.

Purpose:

```text
learn from real scale/recovery/sync/offline/search patterns
!= copy competitor architecture
!= technology popularity vote
!= semantic authority
```

Recorded structural lessons include:

- do not prepay distributed complexity before real pressure exists;
- local/offline storage is a separate architecture dimension from server canonical persistence;
- cache/sync/projection state can diverge from canonical truth and must be propagated/governed deliberately;
- tested restoration evidence is stronger than nominal backup/PITR capability;
- bounded pgvector/search, Redis/jobs, object storage and ML services can coexist with a canonical store without becoming canonical truth;
- ORM-level database portability does not guarantee equivalent semantics or real migration support;
- successful universal-object/block models elsewhere do not override LifeOS's closed rejection of generic universal semantic roots.

Full evidence and official source inventory: `docs/physical-model/pm-01-technology-landscape-v1.md`.

# 15. Physical execution phases

The current mandatory progression is:

```text
PM-00  Bootstrap / authority freeze
PM-01  Technology discovery + candidate/version/edition/deployment/environment freeze — READ-ONLY FIRST
PM-02  Admitted primary candidate mapping design
PM-03  Semantic mapping hard-gate preflight
PM-04  Common fixture/oracle + candidate harness design
PM-05  Correctness/destructive execution
PM-06  LOW/BASE/HIGH + performance execution
PM-07  Recovery/evolution/failure evidence
PM-08  Secondary lanes where justified
PM-09  Scoring + sensitivity
PM-10  Recommendation
PM-11  Explicit selection gate
PM-12  Accepted Physical Model
PM-13  Independent clean-room QA
PM-14  Closure / protected main integration
```

The **sequence and gates are fixed**: semantic authority, correctness-before-performance, explicit writes, explicit selection and clean-room closure cannot be skipped by convenience.

The **content inside the gates is evolutionary**: candidate universe, exact versions/editions/topologies, candidate-native mappings, activated secondary lanes, cost conditions and rerun/sensitivity needs may change as evidence is collected.

This is deliberate: the Physical Model has a stable process without prematurely freezing the answer.

Do not skip directly from bootstrap to a database winner.

# 16. PM-00 approved bootstrap scope

Authorized by the user on 2026-08-18.

```text
BRANCH
feature/physical-model

PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE 6
docs/physical-model/README.md
docs/physical-model/execution-methodology-v1.md
docs/physical-model/execution-template-v1.md
docs/physical-model/acceptance-test-matrix-v1.md
docs/physical-model/result-register-v1.md
docs/workstreams/physical-model.md

UPDATE 16
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/README.md
docs/workstreams/backend-foundation.md
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/architecture/physical-benchmark-specification.md
docs/architecture/physical-benchmark-scenario-corpus.md
docs/architecture/physical-benchmark-register.md
docs/development/branching-and-environments.md
docs/development/operating-rules.md
docs/development/repository-engineering-safety.md

DELETE
0

UNIQUE PATHS
22
```

Bootstrap explicitly excludes:

```text
Domain/Logical semantic edits
SQL / TypeQL / Cypher
Physical candidate schema/mapping implementation
benchmark harness code
fixture generator code
database/container deployment
technology selection
backend source/API/Auth/provider implementation
frontend/prototype
main write / PR / merge
```

## PM-00 remote QA evidence

The initial six CREATEs were isolated first and remotely compared before any consumer propagation:

```text
CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626

ahead_by       6
behind_by      0
added          6
modified       0
deleted        0
unexpected     0
```

After all 16 authorized consumer updates, the remote branch was verified at:

```text
CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272

PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

ahead_by       22
behind_by      0
total_commits  22
unique_paths   22
added           6
modified       16
deleted         0
unexpected      0
```

`main` was separately re-read and remained exactly:

```text
3de84bb49f9cef30e88e9bde4961ed84335daa79
```

The branch was independently compared from checkpoint `8549e1c95bef2e354bd47028259e6816bf5e9272` to `feature/physical-model` and returned `status=identical`, proving that checkpoint was the exact content-QA branch HEAD.

Critical remote readback confirmed:

```text
Physical workstream active                     PASS
Phase-10 register consumed but unchanged       PASS
PostgreSQL result slots                        NOT RUN
TypeDB result slots                            NOT RUN
mapping execution                              NOT STARTED
benchmark execution                            NOT STARTED
technology selection                           NONE
Backend Foundation                             NOT STARTED / DEFERRED
Domain/Logical reopen                          0
main write                                     0
unexpected physical paths                      0
```

Therefore:

```text
PM-00 BOOTSTRAP
QA PASS
```

After that proof, current status consumers on the same already-approved bootstrap paths were aligned from `QA pending` to `PM-00 QA PASS / PM-01 READ-ONLY NEXT`. The last such consumer write was:

```text
QA-STATUS PROPAGATION CHECKPOINT
f5e7f5c3ea38dd02b54192705575b0a48ea3854c
```

The later PM-01 discovery-policy update changed only Physical documentation methodology/handoff and did not start mapping or benchmark execution.

## PM-01 read-only evidence

Authorized read-only research and documentation write on 2026-08-18.

```text
RESEARCH PRE-SCOPE
622767d5435d59766459bb25a57e5afeb7dd7336

EVIDENCE-QA CHECKPOINT BEFORE HANDOFF
8b6cc25dfc042389be0a985c96a3a7025e20e275

CREATE BEFORE HANDOFF
1
docs/physical-model/pm-01-technology-landscape-v1.md

UPDATE BEFORE HANDOFF
2
docs/physical-model/result-register-v1.md
docs/physical-model/README.md

COMPARE PRE-SCOPE -> EVIDENCE-QA CHECKPOINT
ahead_by       3
behind_by      0
added          1
modified       2
deleted        0
unexpected     0
```

Read-only PM-01 disposition recorded at that checkpoint:

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

P0 PostgreSQL 18.4     ADMIT
P1 TypeDB CE 3.12.3   ADMIT
P2 XTDB 2.1.0         ADMIT / production-topology HOLD
P3 SurrealDB CE 3.2.3 ADMIT-CONDITIONAL

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE
```

This handoff update is the terminal PM-01 current-truth propagation within the same approved write scope. A new chat must re-fetch the current branch HEAD rather than relying on a self-referential SHA inside this file.

# 17. Git / write discipline — mandatory

For every future write scope:

```text
BRANCH
feature/physical-model unless a later approved workstream split changes it

PRE-SCOPE
exact remote HEAD immediately before first write

CREATE
exact paths

UPDATE
exact paths

DELETE
exact paths

OUT OF SCOPE
explicitly listed
```

After approval:

- re-fetch branch HEAD immediately before first write;
- if HEAD differs from PRE-SCOPE, STOP/re-gate;
- do not add an extra path because it seems convenient;
- post-write compare from PRE-SCOPE;
- classify added/modified/deleted/unexpected paths;
- require `behind_by 0` unless an explicit main-update/rebase process is separately authorized;
- read back critical remote outputs;
- update this handoff last with the verified checkpoint.

No direct `main` writes.

# 18. Documentation lifecycle

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

Do not rewrite historical evidence merely because current state advanced.

Size/tool-limit split rule remains mandatory:

```text
ONE COMPLETE LOGICAL PAYLOAD
→ LOSSLESS PHYSICAL PARTITION
→ ONE COMPLETE LOGICAL PAYLOAD
```

A transport split is not summarization or semantic cleanup.

# 19. Test/result language

Use exact terms:

```text
NOT RUN
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
SELECTED — only after PM-11 explicit gate
```

Never call a planned test PASS, an official documentation claim executed evidence, or an unexecuted HIGH tier verified.

# 20. Selection rule

`PREFERRED != SELECTED` is mandatory.

Before any selection, PM-11 must show:

- exact benchmark subject;
- all applicable hard-gate results;
- raw/evidence-backed scores;
- sensitivity;
- material topology/edition conditions;
- operational/cost/exit tradeoffs;
- rejected/held alternatives;
- downstream consequences;
- explicit user approval.

# 21. Backend boundary

Backend Foundation remains **NOT STARTED / DEFERRED**.

Do not create `feature/backend-foundation`, production SQL/migrations, FastAPI routes/DTOs, Auth mechanisms, provider adapters or runtime implementation merely because Physical benchmark code exists.

Benchmark-only mapping/harness code is allowed only in later explicitly gated Physical scopes and must remain clearly non-production unless separately promoted after Physical acceptance.

# 22. Current exact next step — PM-02 gate only

```text
PM-01
READ-ONLY PASS-CONDITIONAL
RESULT RECORDED

PM-02
NOT STARTED
NOT AUTHORIZED
```

Before any PM-02 mapping write:

1. re-read this handoff and `docs/physical-model/pm-01-technology-landscape-v1.md`;
2. re-fetch current `feature/physical-model` HEAD and compare to current `main`;
3. verify the final PM-01 write delta from `622767d5435d59766459bb25a57e5afeb7dd7336` contains only the authorized PM-01 documentation paths and `behind_by 0` unless later explicitly accounted for;
4. keep the four admitted primary hypotheses separate:
   - PostgreSQL 18.4;
   - TypeDB CE 3.12.3;
   - XTDB 2.1.0;
   - SurrealDB Community 3.2.3;
5. design each mapping idiomatically against the same closed LifeOS semantics; do not make one candidate imitate another;
6. carry candidate-specific caveats into mapping design rather than pre-resolving them by prose;
7. keep every `HG-01..HG-12` result `NOT RUN` until PM-03 evidence exists;
8. do not build benchmark harness/fixtures/database deployments in PM-02 unless a later separately authorized scope explicitly combines phases;
9. keep the benchmark-host environment `HOLD` until actually verified; it must be closed before executable benchmark claims;
10. issue a fresh exact PM-02 write gate before creating any mapping path.

No candidate is selected by PM-01.

# 23. Resume summary

If a new chat reads this section after the mandatory sources, the operative state is:

```text
REPO
MattiaRubino/lifeos

ACTIVE WORKSTREAM
Physical Model

BRANCH
feature/physical-model

BASE / BOOTSTRAP PRE-SCOPE
main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-00
BOOTSTRAP QA PASS
create checkpoint 6d76bc150dfd7b3cefe56c6e05c96404e7494626
content-QA checkpoint 8549e1c95bef2e354bd47028259e6816bf5e9272
QA-status propagation checkpoint f5e7f5c3ea38dd02b54192705575b0a48ea3854c

PM-01
READ-ONLY PASS-CONDITIONAL
research PRE-SCOPE 622767d5435d59766459bb25a57e5afeb7dd7336
evidence-QA checkpoint before handoff 8b6cc25dfc042389be0a985c96a3a7025e20e275
technology discovery PASS
application architecture reconnaissance PASS
candidate admission PASS
benchmark host HOLD

PM-01 EVIDENCE
docs/physical-model/pm-01-technology-landscape-v1.md

DOMAIN
CLOSED / DO NOT REOPEN IMPLICITLY

LOGICAL
CLOSED / DO NOT REOPEN IMPLICITLY

PHASE 10
BENCHMARK METHOD AUTHORITY — DO NOT REINVENT

ADMITTED PRIMARY MAPPING CANDIDATES
P0 PostgreSQL 18.4
   self-host single-node / psycopg 3.3.4
   ADMIT / pre-existing PREFERRED BASELINE / NOT SELECTED

P1 TypeDB CE 3.12.3
   self-host single-node / driver 3.12.3
   ADMIT / NOT SELECTED

P2 XTDB 2.1.0
   ADMIT / PRODUCTION-TOPOLOGY HOLD / NOT SELECTED

P3 SurrealDB Community 3.2.3
   single-node RocksDB / Python SDK 2.0.0
   ADMIT-CONDITIONAL / NOT SELECTED

PRIMARY RESERVES
MariaDB 11.8 LTS DEFER
Gel 7 DEFER
CockroachDB DEFER
YugabyteDB DEFER

SECONDARY / BOUNDED
Neo4j DEFER PM-08
pgvector DEFER PM-08
Qdrant/OpenSearch specialist trigger only
SQLite future local/offline role

APPLICATION RECONNAISSANCE
Notion / Linear / Anytype / AppFlowy / Immich / Home Assistant / Cal.com
SUPPORTING EVIDENCE ONLY
USED ELSEWHERE != SELECTED

COST POSTURE
EUR 0 initial direct technology/license cost where realistically possible
quality/correctness outrank cost
paid candidates remain eligible when materially better
migration/exit work only when justified by real risk

MAPPING
NOT STARTED

HARD GATES
NOT RUN

BENCHMARK
NOT STARTED

SELECTION
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
STOP
fresh explicit PM-02 mapping-design write gate required
benchmark-host HOLD must close before executable benchmark evidence
```
