# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-02 DESIGN COMPLETE / PM-03 NEXT**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Started: 2026-08-18
- PM-00 bootstrap QA: **PASS**
- PM-00 content-QA checkpoint: `8549e1c95bef2e354bd47028259e6816bf5e9272`
- PM-00 QA-status propagation checkpoint: `f5e7f5c3ea38dd02b54192705575b0a48ea3854c`
- PM-01 technology-discovery methodology checkpoint: `1da012c28bf8f9de00bdf9deee1ab407fda4ba99`
- PM-01 research PRE-SCOPE: `622767d5435d59766459bb25a57e5afeb7dd7336`
- PM-01 evidence-QA checkpoint before handoff: `8b6cc25dfc042389be0a985c96a3a7025e20e275`
- PM-01 technology/candidate freeze: **PASS-CONDITIONAL**
- PM-01 benchmark-host freeze: **HOLD**
- PM-02 PRE-SCOPE: `fac3b5baf1813f886c4773594e6234810e5ba8c6`
- PM-02 evidence checkpoint before this terminal handoff: `d23f9a8a54c59835a41256b5fa1b452ce115591e`
- PM-02 primary mapping design: **DESIGN COMPLETE / PM-03 NOT RUN**
- Executable mapping/schema deployment: **NOT STARTED**
- Benchmark execution: **NOT STARTED**
- Primary persistence selected: **NONE**
- Secondary graph selected: **NONE**
- Search/vector specialization selected: **NONE**
- Production backend: **NOT STARTED / DEFERRED**

## Purpose

Produce the accepted LifeOS Physical Model by designing idiomatic candidate mappings, challenging them against the closed semantic model, executing the approved benchmark method only after semantic eligibility, and making technology selection only through explicit evidence-backed gates.

This handoff is the live save-game for the workstream. A new chat/AI must be able to continue from repository truth without relying on conversation memory.

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
57 / 57 owners classified
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
PM-00 QA PASS
PM-01 PASS-CONDITIONAL
PM-02 DESIGN COMPLETE
PM-03 NEXT

EXECUTABLE MAPPING / DATABASE DEPLOYMENT
NOT STARTED

HARD GATES
NOT RUN

BENCHMARK
NOT STARTED

SELECTION
NONE

BACKEND FOUNDATION
NOT STARTED / DEFERRED
```

No Pre-Physical repair is pending.

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
17. read `docs/physical-model/pm-02-primary-mapping-overview-v1.md`;
18. read all four current PM-02 mapping documents under `docs/physical-model/mappings/`;
19. read `docs/architecture/physical-benchmark-specification.md`;
20. read `docs/architecture/physical-benchmark-scenario-corpus.md`;
21. read `docs/architecture/physical-benchmark-register.md`;
22. read the current Pre-Physical Architecture Baseline and architecture index;
23. read all four Phase-5 requirement packages;
24. read Phase-6 AI/context/runtime + Integration Hub boundaries;
25. read Phase-7 durable-execution contract;
26. read Phase-8 governed-operation/effect contract;
27. read Phase-9 search/observability/calendar/solver contract;
28. read complete Domain closure authority when semantic pressure is involved;
29. read complete Logical Model/decision register and `WL-H01..WL-H12` when semantic pressure is involved;
30. read current ADR statuses, especially superseded/qualified decisions;
31. verify current external product facts from official primary sources when versions/features are material;
32. issue an exact PRE-SCOPE/write gate before every new write scope.

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
MAPPING DESIGNED != HARD-GATE PASS
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

Preserve the accepted address spaces:

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

The exact Physical representation may differ per candidate, but reverse mapping to the logical address family must remain deterministic.

# 5. State-layer invariants

Keep distinguishable where applicable:

```text
canonical state
material history
retrieved context
derived/projection state
live external/provider state
candidate/unresolved state
runtime/security state
transient LLM/computation context
```

Co-location is allowed when technically sensible; semantic equivalence is not implied by co-location.

# 6. Whole-Logical hardenings — mandatory Physical obligations

```text
WL-H01 Agreement terms require justified owned material state
WL-H02 Governed Operation / Effect Contract
WL-H03 Projection / Disclosure Surface Contract
WL-H04 absence != false
WL-H05 expected-state / optimistic-concurrency contract
WL-H06 idempotency != identity
WL-H07 multi-owner consistency boundary
WL-H08 canonical state != provider sync state
WL-H09 consequential LR-08 freshness/material basis
WL-H10 retention/redaction/tombstone integrity
WL-H11 consequential AuthZ provenance
WL-H12 non-interference / inference leakage
```

No Physical candidate can compensate for failure of an applicable hardening with performance or operational convenience.

# 7. Retention / history / recovery invariants

Physical design must support:

- current-state access without lifetime replay by default;
- material historical reconstruction where required;
- correction without pretending corrected knowledge always existed;
- world/effective versus knowledge/recording chronology where material;
- category/purpose-sensitive retention;
- redaction/tombstone truthfulness;
- native identity non-reuse;
- derived/index/provider deletion propagation where applicable;
- old-backup restore that does not silently resurrect forbidden current data;
- schema/mapping evolution that preserves identity, references and historical meaning.

# 8. Temporal / search / disclosure invariants

Preserve:

- date-only / floating / named-zone / instant / interval semantics where applicable;
- recurrence family distinctions;
- lazy Occurrence identity without premature invented ordinal;
- Schedule / Session / Actual / Outcome separation;
- provider calendar IDs/tokens as external state;
- search/index miss != canonical nonexistence;
- embedding similarity != relationship/evidence;
- hidden records not leaking via counts/ranking/errors/timing beyond accepted disclosure;
- stale projections exposing enough freshness/material basis for consequential revalidation.

# 9. Candidate lanes — current authority

```text
LANE P — PRIMARY

P0 PostgreSQL 18.4
mandatory preferred baseline
PM-01 ADMIT
PM-02 MAPPING COMPLETE
NOT SELECTED

P1 TypeDB CE 3.12.3
mandatory semantic challenger
PM-01 ADMIT
PM-02 MAPPING COMPLETE
NOT SELECTED

P2 XTDB 2.1.0
PM-01 temporal/bitemporal challenger
ADMIT / PRODUCTION-TOPOLOGY HOLD
PM-02 MAPPING COMPLETE
NOT SELECTED

P3 SurrealDB Community 3.2.3
PM-01 multimodel challenger
ADMIT-CONDITIONAL
PM-02 MAPPING COMPLETE
NOT SELECTED

LANE G — SECONDARY GRAPH
G0 no-specialized-store baseline
G1 Neo4j
DEFER TO PM-08
NOT SELECTED

LANE S — SEARCH / VECTOR
S0 structured + lexical/full-text baseline
S1 pgvector when PostgreSQL is applicable
DEFER TO PM-08
NOT SELECTED

LOCAL / OFFLINE
SQLite
DEFER — future bounded client/local role

LANE E/D
bounded native mechanisms first
specialist only after explicit admission trigger
```

Primary reserves/rejections remain in PM-01 evidence and are not erased by PM-02.

# 10. Cost / technology-discovery policy

```text
TARGET
initial direct technology/license cost = EUR 0 where realistically possible

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
3. real LifeOS workload/capability fit
4. maturity / operability / maintainability / Python/tooling fit
5. measured performance/resource efficiency
6. TCO / deployment requirements
7. lock-in / exit risk / realistic migration path
```

Use candidate-native strengths when materially better. Preserve portability where cheap/useful. Do not build large abstraction layers for hypothetical migrations.

# 11. Application architecture reconnaissance rule

PM-01 incorporated public architecture evidence from directly similar and structurally adjacent applications including Notion, Linear, Anytype/any-sync, AppFlowy, Immich, Home Assistant and Cal.com.

Use that evidence to learn about:

```text
canonical store boundaries
local/offline/sync separation
projection/cache divergence
recovery rehearsal
bounded vector/search specialization
jobs/files/AI separation
schema evolution
real migration/portability limits
```

Never infer:

```text
USED ELSEWHERE -> SELECTED FOR LIFEOS
```

Domain + Logical + direct LifeOS evidence remain authority.

# 12. Durable runtime posture — separate from persistence selection

```text
bounded async DB/worker/outbox class
valid baseline

Restate
preferred structural-fit dedicated candidate — NOT SELECTED

Temporal
mandatory strong challenger — NOT SELECTED

DBOS
conditional challenger — NOT SELECTED
```

Runtime preference cannot award persistence points or select a primary database implicitly.

# 13. AI / solver / provider boundary

```text
solver output != accepted canonical effect
AI evaluation/result != canonical truth
provider revision != MaterialStateRef
runtime workflow completion != Actual automatically
```

No AI/solver/provider/runtime product is selected by the Physical workstream.

# 14. Phase-10 benchmark authority

Consume rather than reinvent:

- `physical-benchmark-specification.md`;
- `physical-benchmark-scenario-corpus.md`;
- `physical-benchmark-register.md`.

Primary hard gates:

```text
HG-01..HG-12
```

Cross-lane gates:

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

# 15. Physical execution roadmap

```text
PM-00  Bootstrap / authority freeze                       PASS
PM-01  Technology discovery / subject freeze              PASS-CONDITIONAL
PM-02  Admitted primary candidate mapping design          DESIGN COMPLETE
PM-03  Semantic mapping hard-gate preflight               NEXT
PM-04  Common fixture/oracle + candidate harness design   NOT STARTED
PM-05  Correctness/destructive execution                  NOT STARTED
PM-06  LOW/BASE/HIGH + performance execution              NOT STARTED
PM-07  Recovery/evolution/failure evidence                 NOT STARTED
PM-08  Secondary lanes where justified                    NOT STARTED
PM-09  Scoring + sensitivity                              NOT STARTED
PM-10  Recommendation                                      NOT STARTED
PM-11  Explicit selection gate                            NOT STARTED
PM-12  Accepted Physical Model                            NOT STARTED
PM-13  Independent clean-room QA                          NOT STARTED
PM-14  Closure / protected main integration               NOT STARTED
```

The sequence/gates are fixed; the candidate content within gates is evidence-driven/evolutionary.

# 16. PM-00 historical checkpoint

Authorized bootstrap scope started from:

```text
main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79
```

Key evidence:

```text
CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272

QA-STATUS PROPAGATION
f5e7f5c3ea38dd02b54192705575b0a48ea3854c

PM-00
QA PASS
```

Historical PM-00 evidence remains truthful and is not rewritten by later phase progress.

# 17. PM-01 result

Research PRE-SCOPE:

```text
622767d5435d59766459bb25a57e5afeb7dd7336
```

Evidence:

```text
docs/physical-model/pm-01-technology-landscape-v1.md
```

Disposition:

```text
TECHNOLOGY DISCOVERY             PASS
APPLICATION ARCHITECTURE RECON   PASS
PRIMARY ADMISSION                PASS
EXACT SUBJECT FREEZE             PASS for P0/P1/P2/P3
LICENSE/COST                     PASS-CONDITIONAL
BACKUP/EVOLUTION                 PASS-CONDITIONAL
HA/PRODUCTION TOPOLOGY           PASS-CONDITIONAL
BENCHMARK HOST                   HOLD

PM-01
PASS-CONDITIONAL
```

Admitted mapping candidates:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

No selection resulted from PM-01.

# 18. PM-02 authorized scope and result

User authorized PM-02 on 2026-08-18.

```text
BRANCH
feature/physical-model

PRE-SCOPE
fac3b5baf1813f886c4773594e6234810e5ba8c6

CREATE 5
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/mappings/typedb-3.12.3-v1.md
docs/physical-model/mappings/xtdb-2.1.0-v1.md
docs/physical-model/mappings/surrealdb-3.2.3-v1.md

UPDATE 3
docs/physical-model/README.md
docs/physical-model/result-register-v1.md
docs/workstreams/physical-model.md

DELETE
0
```

Explicitly excluded:

```text
Domain/Logical edits
executable SQL / TypeQL / SurrealQL schema deployment
benchmark harness/source
fixture generator
container/database deployment
PM-03 hard-gate PASS/REJECT verdict
performance claims
technology selection
production backend/API/Auth/provider implementation
frontend/prototype
main write / PR / merge
```

Before this terminal handoff write, the remote compare from PM-02 PRE-SCOPE returned:

```text
CHECKPOINT
d23f9a8a54c59835a41256b5fa1b452ce115591e

ahead_by       7
behind_by      0
added          5
modified       2
deleted         0
unexpected      0
```

The only remaining approved PM-02 mutation at that checkpoint was this terminal handoff update.

# 19. PM-02 mapping package

Common design/oracle:

```text
docs/physical-model/pm-02-primary-mapping-overview-v1.md
```

Candidate mappings:

```text
PM02-PG-001
docs/physical-model/mappings/postgresql-18.4-v1.md

PM02-TDB-001
docs/physical-model/mappings/typedb-3.12.3-v1.md

PM02-XT-001
docs/physical-model/mappings/xtdb-2.1.0-v1.md

PM02-SDB-001
docs/physical-model/mappings/surrealdb-3.2.3-v1.md
```

Current mapping status:

```text
PostgreSQL  DESIGN COMPLETE / PM-03 NOT RUN
TypeDB      DESIGN COMPLETE / PM-03 NOT RUN
XTDB        DESIGN COMPLETE / PM-03 NOT RUN
SurrealDB   DESIGN COMPLETE / PM-03 NOT RUN
```

# 20. PostgreSQL PM-02 design

```text
owner-specific relational tables
+ direct FKs where Reference Contract is homogeneous
+ bounded technical native/scoped/material/external anchors only where heterogeneous addressability requires them
+ explicit material-state/history rows
+ current-state bindings
+ specific relation tables
+ contextual/n-ary records for consequential relations
+ transactional/locking/SERIALIZABLE strategy where required
```

Key rule:

```text
technical anchor != Entity / Thing ontology
xmin/xid/updated_at != MaterialStateRef
```

Primary PM-03 pressures:

- anchor leakage / heterogeneous reference integrity;
- owner-specific history maintainability;
- expected-state + multi-owner concurrency;
- Agreement/governance materiality;
- temporal/history separation;
- lazy Occurrence;
- selective disclosure/non-interference;
- tombstone/restore integrity.

# 21. TypeDB PM-02 design

```text
concrete entity types for the 15 native owners
+ explicit keyed LR-02/context/state types
+ first-class specific relation types with named roles
+ role eligibility expressing Reference Contracts
+ explicit MaterialStateRef state objects
+ relation-native n-ary Agreement structure
+ narrow technical consistency guards for write-skew-sensitive invariant sets
```

Key rules:

```text
TypeDB IID != NativeRef
TypeDB IID/snapshot != MaterialStateRef
shared type/interface != universal semantic owner
consistency guard != Domain Transaction
```

Primary PM-03 pressures:

- reverse mapping of address families;
- generic-root leakage;
- material-state/history ergonomics;
- snapshot-isolation stale/write-skew protection;
- n-ary common terms state;
- lazy Occurrence;
- retention/tombstone;
- selective disclosure/inference;
- schema evolution.

# 22. XTDB PM-02 design

```text
owner-specific tables
+ four separated technical address spaces
  native_address
  scoped_address
  material_state_address
  external_address
+ explicit material-state rows
+ native bitemporal history where semantically truthful
+ ASSERT-based target/expected-state/invariant checks
+ one serialized non-interactive DML transaction for co-located multi-owner effects
```

Key rules:

```text
SYSTEM_TIME != MaterialStateRef
VALID_TIME != MaterialStateRef
transaction token != MaterialStateRef
valid-time != all LifeOS temporal semantics
```

Primary PM-03 pressures:

- referential/cardinality integrity without conventional FK/general unique constraints;
- separated anchors remain technical;
- bitemporal semantic alignment;
- non-interactive governed-operation ergonomics;
- ASSERT failure atomicity;
- dynamic-schema containment/evolution;
- lazy Occurrence;
- ERASE/tombstone integrity;
- current-state practicality.

XTDB production topology remains HOLD; no HA/production credit is implied.

# 23. SurrealDB PM-02 design

```text
SCHEMAFULL owner-specific tables
+ typed record links/unions for bounded Reference Contracts
+ specific binary relation tables only for genuinely binary LR-03 relations
+ contextual normal records for n-ary/material relations
+ explicit material-state records/history
+ narrow technical consistency guards for write-skew-sensitive invariant sets
```

Key rules:

```text
FLEXIBLE canonical fallback = forbidden
binary graph edge != universal Relationship
changefeed/version metadata != MaterialStateRef
consistency guard != semantic owner
```

Primary PM-03 pressures:

- document/meta-model escape hatch;
- generic graph ontology pressure;
- address-family discrimination;
- explicit material history independent from bounded changefeed;
- snapshot-isolation write-skew;
- n-ary Agreement;
- deletion/tombstone behavior;
- selective disclosure through graph traversal;
- SCHEMAFULL evolution;
- Community vs Enterprise topology boundary.

# 24. Cross-candidate PM-02 invariants

## MaterialStateRef

```text
PostgreSQL storage/MVCC token != MaterialStateRef
TypeDB IID/snapshot              != MaterialStateRef
XTDB system/valid/tx coordinate  != MaterialStateRef
SurrealDB change/version metadata!= MaterialStateRef
```

Every mapping uses explicit stable semantic state addressability.

## Expected state

Every consequential stale-sensitive mutation must:

```text
bind expected MaterialStateRef
check current applicable state
reject mismatch
establish new state atomically where co-located
retain/reconstruct bounded provenance
```

## Multi-owner

```text
PostgreSQL
transaction + constraints/locks/SERIALIZABLE where needed

TypeDB
one write transaction + narrow consistency guard for write-skew-sensitive invariant sets

XTDB
one serialized DML transaction + ASSERT preconditions

SurrealDB
one transaction + narrow consistency guard for write-skew-sensitive invariant sets
```

These remain **design hypotheses** until PM-03 proof.

## Lazy Occurrence

```text
before persistent differentiation
source + governing MaterialStateRef + recurrence family + semantic coordinate where available
= bounded occurrence locator

once individually distinguished/addressable
-> same semantic Occurrence receives NativeRef
```

No fake early ordinal for indistinguishable quota slots.

## N-ary Agreement

Every mapping preserves one common contextual Agreement and one materially specific terms state shared by all applicable party assent bindings. Pairwise relatedness cannot substitute.

# 25. PM-02 deliberate non-decisions

PM-02 does **not** decide:

```text
winner / selected primary
hard-gate PASS/REJECT
performance winner
production HA topology
exact benchmark host
AuthZ engine
secondary graph store
vector/search store
runtime/orchestrator
production API/ORM/backend schema
```

It designs the representations necessary to test those questions truthfully later.

# 26. Benchmark-host HOLD

Still unresolved:

```text
CPU/RAM actually allocated to benchmark
OS/runtime exact build
Docker/native execution availability
filesystem/storage characteristics
available disk budget
network/topology constraints
resource-limit policy
```

Do not invent these from conversation/user hardware memory.

This HOLD:

```text
DOES NOT block static PM-03 mapping preflight
DOES block claiming reproducible executable PM-04/05+ benchmark evidence until closed
```

# 27. Git/write discipline — mandatory

For every future write scope:

```text
BRANCH
feature/physical-model unless later approved split

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

- re-fetch branch state before first write;
- if remote state diverges unexpectedly, STOP/re-gate;
- write only approved paths;
- compare PRE-SCOPE -> HEAD;
- classify added/modified/deleted/unexpected;
- require `behind_by 0` unless an explicit main-update process is authorized;
- read back critical remote outputs;
- update this handoff last.

No direct `main` writes.

# 28. Documentation lifecycle

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

Do not rewrite historical evidence because current state advanced.

Lossless split rule remains:

```text
ONE COMPLETE LOGICAL PAYLOAD
-> LOSSLESS PHYSICAL PARTITION
-> ONE COMPLETE LOGICAL PAYLOAD
```

A file-size split is not summarization or semantic cleanup.

# 29. Test/result vocabulary

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

Never call a design proof an executed test, an official documentation claim direct evidence, or an unexecuted tier verified.

# 30. Selection rule

`PREFERRED != SELECTED` remains mandatory.

Before selection PM-11 must show:

- exact benchmark subject;
- all applicable hard-gate results;
- raw/evidence-backed scores;
- sensitivity;
- material topology/edition conditions;
- operational/cost/exit tradeoffs;
- rejected/held alternatives;
- downstream consequences;
- explicit user approval.

# 31. Backend boundary

Backend Foundation remains **NOT STARTED / DEFERRED**.

Do not create production SQL/migrations, FastAPI routes/DTOs, Auth mechanisms, provider adapters or production runtime implementation because PM-02 mapping docs now exist.

Executable benchmark-only mapping/harness code begins only in later explicitly gated Physical scopes and remains non-production unless separately promoted after Physical acceptance.

# 32. Current exact next step — PM-03

```text
PM-02
DESIGN COMPLETE
FINAL REMOTE WRITE-SCOPE QA REQUIRED AFTER THIS HANDOFF

PM-03
SEMANTIC MAPPING HARD-GATE PREFLIGHT
NEXT

GOAL
challenge each mapping against HG-01..HG-12
using static destructive review + executable proof only where later separately authorized/available

RESULT PER GATE
PASS
PASS-CONDITIONAL
HOLD
REJECT
NOT-APPLICABLE with rationale

RULE
insufficient evidence = HOLD, never PASS
```

PM-03 must not award performance points.

PM-03 may repair a candidate mapping if the repair preserves all closed semantics and remains within a separately gated documentation scope. A material semantic contradiction triggers explicit upstream reopen review; it is never silently solved by weakening Domain/Logical meaning.

# 33. PM-03 primary pressure list

At minimum pressure all candidates on:

```text
HG-01 semantic owner preservation
HG-02 ReferenceAddress family integrity
HG-03 typed/n-ary relation fidelity
HG-04 expected-state consequential concurrency
HG-05 multi-owner consistency
HG-06 material history/correction/reconciliation
HG-07 state-layer separation
HG-08 governance/selective disclosure
HG-09 retention/redaction/tombstone/restore integrity
HG-10 temporal/recurrence/timezone/lazy Occurrence fidelity
HG-11 schema/mapping evolution
HG-12 recoverability/evidence quality
```

Candidate-specific risks are in each mapping document and the PM-02 overview.

# 34. Resume summary

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
benchmark host HOLD

PM-02
DESIGN COMPLETE
PRE-SCOPE fac3b5baf1813f886c4773594e6234810e5ba8c6
P0 PostgreSQL mapping PM02-PG-001 COMPLETE
P1 TypeDB mapping     PM02-TDB-001 COMPLETE
P2 XTDB mapping       PM02-XT-001 COMPLETE
P3 SurrealDB mapping  PM02-SDB-001 COMPLETE

HARD GATES
NOT RUN

EXECUTABLE DATABASE/HARNESS
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-03 semantic mapping hard-gate preflight

STOP BEFORE
PM-04 harness/database execution unless separately authorized
benchmark-host HOLD must close before reproducible executable evidence
```

This handoff is the terminal PM-02 save-game. A new chat must re-fetch the actual remote branch HEAD rather than relying on any self-referential SHA that cannot be embedded in its own creating commit.