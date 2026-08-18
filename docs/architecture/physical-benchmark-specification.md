# Physical Benchmark Specification

- Status: **CURRENT METHOD / HISTORICAL PHASE-TIME EXECUTION STATUS — Phase 10 QA PASS / consumed by the closed Physical Model**
- Stage: Physical Model benchmark/evidence method authority
- Phase-time Physical state recorded by this method: **PM-09 SCORING + SENSITIVITY / selection not yet performed at that point**
- Current Physical truth: **CLOSED / SELECTED / ACCEPTED / integrated via PR #15**
- Current selected canonical primary: **PostgreSQL 18.4**
- Verified-run benchmark score: **NOT AVAILABLE / direct HG PASS 0**

> **Current-truth qualification:** this specification remains the current benchmark/evidence **method**. Candidate labels, `NOT selected`, `Technology selection NONE`, active-PM-09 language and execution-state statements below are truthful phase-time evidence and do not override PM-11/12 selected/accepted truth. No direct hard gate or LOW/BASE/HIGH run has been manufactured by later selection.
>
> **Naming continuity:** `DANTE` is the current product/app name. `LifeOS` references retained in this method reflect the previous working/project name for the same product lineage and are preserved where they belong to the historical method/evidence record.

## Purpose

Define the executable, reproducible method used by the Physical Model workstream to compare LifeOS persistence and bounded specialized-infrastructure candidates.

This document decides **how evidence is produced and judged**. It does not itself select a database, schema, index layout, runtime topology, provider, workflow engine or backend implementation.

```text
PHASE 10
HOW TO BENCHMARK

!=

PHYSICAL MODEL
WHAT TO SELECT / DESIGN
```

The benchmark must be difficult to game: correctness and semantic preservation are hard gates; performance, ergonomics and operational characteristics are scored only after those gates pass.

## Authority and inputs

The benchmark consumes without reopening:

1. current Product / North Star requirements;
2. the complete CLOSED Domain Atlas and Language Map logical documents;
3. the CLOSED Whole Logical Model, complete decision/assumption register and `WL-H01..WL-H12`;
4. current ADR statuses, especially ADR-003 and ADR-007;
5. all Phase 5 requirement packages;
6. Phase 6 AI/context/runtime and Integration Hub contracts, including the requirement for versioned/reproducible evaluation of material consequential AI changes;
7. Phase 7 durable-execution benchmark;
8. Phase 8 Governed Operation / Effect Contract;
9. Phase 9 search/observability/calendar/solver pressure contract;
10. this specification, the Phase 10 scenario corpus and the Phase 10 benchmark register.

A benchmark mapping that requires a semantic shortcut rejected upstream is invalid even if it is fast.

## Core decision rule

```text
HARD-GATE CORRECTNESS
        ↓ only PASS candidates continue
ROLE-SPECIFIC SCORE
        ↓
SENSITIVITY ANALYSIS
        ↓
EVIDENCE QUALITY / OPERABILITY CHECK
        ↓
PREFERRED / PASS-CONDITIONAL / HOLD / REJECT
```

A performance result cannot compensate for semantic corruption, unsafe disclosure, false history, missing expected-state behavior or non-recoverable deletion/reconciliation state.

## Candidate competition by role

Candidates are not forced into one undifferentiated leaderboard. They compete within the role they claim to fill.

### Lane P — primary canonical persistence

Mandatory comparison at Phase 10:

```text
P0  PostgreSQL hybrid
    mandatory preferred baseline
    NOT selected at Phase 10

P1  TypeDB
    mandatory challenger
    NOT selected at Phase 10
```

A primary candidate must be capable of owning canonical LifeOS state and the material/history/governance requirements assigned to canonical persistence under an idiomatic candidate-specific physical mapping.

Current PM-11/12 resolution later selected PostgreSQL 18.4 as canonical primary.

### Lane G — secondary graph / traversal projection

Mandatory baseline-versus-specialized comparison when graph/traversal pressure is executed:

```text
G0  no specialized graph store
    use the accepted primary-store/query/projection baseline

G1  Neo4j / property graph
    serious specialized secondary/read-projection challenger
    NOT accepted as primary by Phase 10
```

A G-lane result cannot become canonical truth merely because traversal performance is superior.

### Lane S — search / semantic retrieval

```text
S0  structured + lexical/full-text baseline

S1  bounded vector retrieval candidate
    pgvector when PostgreSQL is present/applicable
```

A future dedicated search/vector product may enter only if the trigger rule below is satisfied.

### Lane E/D — event / document bounded mechanisms

Baseline is to use bounded capabilities of the accepted primary architecture where they satisfy the requirement.

A specialized event-store, stream or document product enters a later benchmark only when:

- a concrete accepted requirement cannot be met acceptably by the baseline; or
- a sufficiently strong structural benefit in correctness, durability, security, evolvability, operational reliability or migration-risk reduction is demonstrated.

Phase 10 does not manufacture a product shortlist merely to create more competitors.

## Fairness rule — same semantics, idiomatic physical mapping

Every candidate is tested against the same logical corpus, accepted assertions and operation families, but it may use an idiomatic physical representation.

```text
SAME
Domain/Logical meaning
acceptance assertions
scenario inputs
operation semantics
result semantics

DIFFERENT MAY BE
physical schema/mapping
query language
index strategy
constraint mechanism
candidate-native representation
```

Examples:

- PostgreSQL may use typed relational structures, range/temporal facilities and bounded JSON/metadata where semantically valid.
- TypeDB may use native entity/relation/role/cardinality constructs.
- Neo4j may use an idiomatic graph projection in Lane G.
- pgvector may use its native exact/ANN vector index mechanisms in Lane S.

Rejected benchmark manipulation:

```text
force TypeDB into a relational-table imitation
force PostgreSQL into one generic edge/EAV table
force Neo4j projection to own canonical semantics
remove accepted constraints because a candidate lacks a convenient mechanism
allow candidate-specific semantic simplification
```

If a candidate cannot preserve an accepted semantic invariant idiomatically, that is evidence against the candidate, not permission to weaken the invariant.

# Primary-lane hard gates

All applicable gates below are **non-compensable**. A material failure produces `REJECT` unless the evidence is insufficient, in which case the result is `HOLD` pending bounded additional evidence.

## HG-01 — Semantic ownership preservation

The physical design MUST preserve accepted owner/relation/value/policy/history boundaries and MUST NOT require a universal semantic `Entity`, `Thing`, generic edge, EAV/property-bag or other rejected canonical meta-model.

Technical shared registries/discriminators remain allowed where semantics remain explicit and reconstructible.

## HG-02 — Reference-family integrity

The design MUST preserve the distinctions among, where applicable:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Storage IDs, MVCC tokens, ETags, provider revisions and runtime IDs MUST NOT become these references by identity merely because reuse is convenient.

## HG-03 — Typed / n-ary relation fidelity

The design MUST represent accepted typed and n-ary relation/governance structures without collapsing them to a semantically weak generic source-target edge or duplicated facts that lose role/context semantics.

Relation-as-record/object techniques are allowed if the accepted meaning, roles, cardinality and lifecycle remain explicit and testable.

## HG-04 — Expected-state consequential concurrency

For operation classes where stale mutation can materially corrupt meaning, the design MUST support expected-state conflict detection tied to the applicable material basis.

A physical revision token MAY help enforce this but MUST remain distinct from semantic `MaterialStateRef`.

Conflicts MUST remain explicit; silent last-write-wins is not a general LifeOS policy.

## HG-05 — Multi-owner consistency truthfulness

Where an accepted invariant requires atomic co-located multi-owner change, the candidate MUST support a viable atomic boundary.

Where global atomicity is impossible because of external/distributed boundaries, the design MUST support truthful staged/partial state plus reconciliation/compensation rather than hidden partial success.

## HG-06 — History / correction / reconciliation reconstructibility

The design MUST support efficient current-state access while retaining enough material history, version/correction lineage, provenance and reconciliation state to reconstruct consequential past states where required.

Normal current-state reads MUST NOT require lifetime replay by default.

## HG-07 — State-layer separation

The design MUST keep canonical, material-history, derived/projection, provider/external, candidate/unresolved and security/runtime state distinguishable where the accepted contracts require it.

Storage coincidence is not semantic equivalence.

## HG-08 — Governance / selective disclosure

The candidate architecture MUST support enforcement/projection designs capable of preserving Authority, Consent, Visibility, Representation and bounded disclosure without canonical per-recipient duplication by default.

`WL-H12` pressure includes observable existence, counts, rankings, errors, timing, candidate lists, free/busy and explanations.

## HG-09 — Retention / redaction / tombstone / restore integrity

The design MUST support category/purpose-sensitive retention and deletion/redaction behavior without fabricating history or reusing native identity.

The benchmark MUST prove a viable strategy for restoring an older backup after later deletion/redaction without silently resurrecting forbidden state.

## HG-10 — Temporal / recurrence / timezone fidelity

The candidate MUST preserve the semantic information required for time, effective chronology, recurrence, timezone, DST gaps/folds, occurrence exceptions and historical interpretation.

UTC normalization MUST NOT erase required local/timezone meaning.

## HG-11 — Schema/data evolution integrity

An evolution from benchmark schema/mapping version A to B MUST preserve identity, references, historical meaning, governance provenance, material-state bindings and permitted tombstone continuity.

A migration that is fast but silently changes historical semantics fails this gate.

## HG-12 — Recoverability / evidence quality

The candidate must demonstrate a realistic backup/restore/recovery path for the benchmark deployment mode and edition.

A marketing claim or existence of a backup command is insufficient. The benchmark must execute restore/recovery evidence at the level required by the scenario corpus.

# Cross-lane hard gates

Secondary/index candidates also inherit applicable upstream constraints.

## CG-01 — Secondary state is not canonical truth

Graph/search/vector/cache/index/runtime state must remain rebuildable or reconcilable from accepted source/material basis according to its contract and MUST NOT silently become a second canonical source of truth.

## CG-02 — Deletion / correction / access propagation

Downstream projections must have a testable invalidation/deletion/redaction/access-change propagation path. Pending or failed propagation must remain truthful.

## CG-03 — Non-interference under filtering/ranking

Search/vector/graph results, counts, ranking, errors and timing must not expose unauthorized hidden state through the candidate's indexing/query behavior.

## CG-04 — Freshness / material basis

A projection result used in consequential reasoning must expose enough material/freshness basis to support Phase 5/6/8 revalidation requirements.

# Primary-lane score after hard-gate PASS

Only candidates passing all applicable hard gates receive a weighted **verified-run benchmark score**.

| Dimension | Weight | Evaluation focus |
|---|---:|---|
| Semantic mapping simplicity / evolvability | 20 | amount of accidental complexity required to preserve Domain/Logical semantics |
| Transaction / concurrency ergonomics | 15 | expected-state, multi-owner atomicity, contention/conflict handling |
| Query / reporting / traversal | 15 | LifeOS current/history/governance/reporting query families |
| History + current-state efficiency | 10 | long-history growth without lifetime replay for normal reads |
| Operations / backup / restore / HA maturity | 15 | deployment reality for the exact edition/mode tested |
| Schema evolution / migration | 10 | safe controlled evolution with historical/reference integrity |
| Performance / resource efficiency | 10 | latency, throughput, storage, CPU/RAM under accepted tiers |
| Python/tooling/cost/exit risk | 5 | backend fit, ecosystem, licensing/coupling and migration risk |
| **Total** | **100** | |

Scoring MUST include written rationale and raw evidence references. A score without traceable evidence is invalid.

## Secondary graph score

Lane G compares `G0` and `G1` on the bounded workload that justifies a graph projection:

- traversal/query expressiveness;
- latency/throughput for selected multi-hop workloads;
- projection build/update complexity;
- deletion/access propagation;
- operational/licensing burden;
- synchronization/rebuild/reconciliation complexity;
- net complexity versus remaining on the primary store.

Neo4j is adopted only if specialized benefit exceeds the added consistency/operational burden.

## Search/vector score

Lane S evaluates:

- lexical/structured relevance and latency;
- vector recall/precision for accepted retrieval corpus;
- ANN recall after scope/Visibility filtering;
- deletion/redaction/access propagation;
- index freshness;
- rebuild cost;
- storage/memory cost;
- privacy/non-interference behavior;
- operational complexity versus baseline.

`top-k latency` alone is not a sufficient result.

# Workload and target treatment

Phase 5 intentionally left business forecasts and several NFR numbers open. Phase 10 therefore uses **synthetic qualification tiers and sensitivity bands**, not invented product forecasts.

```text
BENCHMARK TIER
!= BUSINESS FORECAST
```

Exact tier definitions live in `physical-benchmark-scenario-corpus.md`.

If later accepted product evidence becomes available, the same methodology may be rerun with updated tiers without changing the semantic hard gates.

## Open parameter treatment

The following kinds of values may materially alter ranking and therefore must be handled as explicit scenario/sensitivity inputs until accepted product/operational targets exist:

- RPO class;
- RTO class;
- availability/SLO class;
- p50/p95/p99 latency expectations by operation class;
- active-account/population scale;
- concurrent sessions/devices;
- read/write concurrency;
- history growth horizon;
- provider/integration traffic;
- intentionally supported offline duration;
- backup cadence / recovery validation expectations;
- deployment topology / single-node vs HA requirement.

A candidate MAY be `PASS-CONDITIONAL` when a requirement is satisfied only under an explicit edition/topology/operational condition.

# Result vocabulary

## PASS

All applicable hard gates pass and the evidence is sufficient for the role being evaluated.

## PASS-CONDITIONAL

Hard gates pass only under an explicit, material condition such as edition, deployment topology, external operational requirement or bounded workload assumption. The condition must be recorded and carried downstream.

## HOLD

Material evidence is missing, contradictory, unstable or not reproducible. `HOLD` is not a negative verdict and does not permit silent assumption.

## REJECT

One or more applicable hard gates fail under an idiomatic good-faith candidate design, or a required capability is structurally unavailable for the role being claimed.

## SENSITIVITY-DEPENDENT

The preferred candidate changes materially across accepted low/base/high or NFR sensitivity scenarios. The exact dependency must be recorded rather than averaging away the difference.

## PREFERRED

Best currently supported candidate among candidates that passed the applicable hard gates, after sensitivity and evidence-quality review.

```text
PREFERRED != SELECTED
```

Selection belonged to the separately authorized Physical Model workstream and required its explicit PM-11 selection gate; that gate later selected PostgreSQL 18.4 plus the bounded companion target stack.

# Evidence contract

Every benchmark execution MUST record enough information to reproduce and review the result.

Required evidence metadata:

```text
LifeOS source commit
benchmark-spec version/commit
scenario-corpus version/commit
benchmark-register version/commit

candidate product
exact product version
edition/license class
deployment mode/topology
driver/client version

hardware CPU/RAM/storage
OS/container/runtime
candidate configuration

physical mapping/schema revision
mapping rationale
query/mutation implementation revision

fixture generator version
seed
dataset tier
row/object/relation/history/search counts
dataset hash where practical

scenario IDs
load/concurrency profile
warm/cold/cache state

correctness assertions
raw pass/fail
latency/throughput
CPU/RAM/disk/storage
query plan/profile where supported

backup/restore/recovery evidence
migration/evolution evidence
failure injection evidence

manual tuning performed
known caveats
raw artifact locations
summary/result vocabulary
reviewer/date
```

Exact product documentation used for capability claims MUST be pinned to the product/version/edition under test where feasible. Current marketing material is not enough evidence for execution-time capability.

## Version / edition / deployment pinning

A candidate is not benchmarked as an abstract brand.

```text
product + version + edition + deployment mode
= benchmark subject
```

This is especially mandatory when HA, clustering, backup, schema/constraint, licensing or driver capabilities vary by version/edition.

If upstream documentation is contradictory or maturity is unclear, the relevant criterion is `HOLD` until behavior is directly verified or authoritative version-specific evidence resolves it.

# Execution protocol

The authorized Physical benchmark SHALL follow this order when direct verified-run execution is admitted.

## Step 1 — Freeze benchmark inputs

Record:

- LifeOS authority commit;
- benchmark-spec/corpus/register commits;
- exact candidate versions/editions;
- hardware/deployment profile;
- dataset tier and seed;
- mapping revision.

No candidate may receive undisclosed extra semantics, relaxed assertions or hidden hardware advantage.

## Step 2 — Implement semantic mapping

For each primary candidate, create the minimum idiomatic Physical mapping necessary to execute the common scenario corpus.

The mapping is reviewed for semantic equivalence **before performance measurements count**.

If equivalence cannot be achieved without violating a hard gate, record `REJECT` or `HOLD`; do not proceed by weakening the LifeOS model.

## Step 3 — Run correctness/destructive corpus

Run all mandatory applicable correctness/destructive scenarios before **verified-run weighted scoring**.

Hard-gate failures invalidate verified-run performance scoring for primary selection.

## Step 4 — Run scale and performance tiers

Execute low/base/high qualification tiers and required sensitivity bands using the same semantic assertions.

Record latency distributions rather than only averages where the tooling supports them. Qualification may proceed progressively, and where a full upper-envelope materialization would be disproportionate, saturation/scaling evidence may support sensitivity analysis only if the limitation is explicit and does not falsely claim an unexecuted tier as `VERIFIED-RUN`.

## Step 5 — Run operations/recovery/evolution evidence

Execute candidate-appropriate backup/restore, destructive recovery and schema/data evolution scenarios for the exact edition/deployment mode.

## Step 6 — Score role-specific dimensions

Calculate **verified-run benchmark scores** only after hard-gate PASS and attach evidence/rationale to each dimension.

## Step 7 — Sensitivity review

Check whether ranking changes under:

- low/base/high dataset/load tiers;
- single-node vs required HA mode where material;
- stronger/weaker RPO/RTO bands;
- history depth;
- read/write ratio;
- projection/search load.

Material instability becomes `SENSITIVITY-DEPENDENT`, not an averaged false certainty.

## Step 8 — Recommendation register

Record:

```text
candidate
role
hard-gate result
weighted result if applicable
conditions
sensitivity
operational caveats
migration/exit risk
recommended disposition
```

No production implementation branch is authorized merely because a benchmark result exists. Selection remains a separate explicit Physical gate.

# Candidate-specific minimum benchmark pressure

## PostgreSQL hybrid

Must be tested for whether an idiomatic typed relational/hybrid design can preserve LifeOS semantics without collapsing into generic EAV/edge patterns or excessive application-only invariant fragility.

Pressure includes:

- typed/n-ary relations;
- material history/current-state access;
- expected-state concurrency;
- multi-owner transactions;
- temporal/range/recurrence queries;
- selective disclosure/index behavior;
- migrations/evolution;
- backup/PITR/restore for the tested deployment mode;
- query/reporting ergonomics;
- bounded JSON/provider payload use.

## TypeDB

Must be tested as a genuine primary challenger using native type/relation/role/cardinality modeling where appropriate.

Pressure includes:

- typed/n-ary relation fidelity;
- current/history modeling ergonomics;
- transaction/conflict semantics for consequential writes;
- reporting/aggregation/query workloads;
- migrations/schema evolution;
- Python driver/tooling;
- exact edition/version clustering/HA maturity;
- backup/restore for the tested deployment mode;
- operational visibility and failure recovery.

No operational capability is awarded points from an unpinned or contradictory documentation claim.

## Neo4j / property graph

Lane G must test a realistic read/projection model against G0, including current product schema/constraint capabilities for the exact edition/version.

Pressure includes:

- multi-hop traversal benefit;
- n-ary/material-state projection complexity;
- projection synchronization/rebuild;
- deletion/access propagation;
- licensing/edition requirements;
- operational/backup burden;
- net complexity versus primary-only query patterns.

Phase 10 does not promote Neo4j to primary canonical competition.

## pgvector

Lane S must compare vector retrieval to S0 under realistic scope/Visibility filtering and deletion/freshness pressure.

Where ANN is used, recall must be measured after filtering rather than inferred from unfiltered nearest-neighbor quality.

# Specialized-infrastructure admission rule

A new specialized candidate not listed in the register may be admitted later only with a short admission record containing:

```text
role
accepted requirement/gap addressed
baseline limitation
expected structural/measured benefit
new operational/state-consistency burden
benchmark scenarios added
explicit user/gate approval where scope changes
```

Do not expand the technology set because a product is fashionable.

# Benchmark integrity checks

Before any **verified-run benchmark recommendation**, verify:

```text
all mandatory primary candidates executed           PASS
all applicable hard gates classified                PASS
candidate versions/editions pinned                  PASS
semantic mapping reviewed before performance        PASS
same corpus/assertions used                         PASS
candidate-specific physical mapping allowed         PASS
hidden semantic relaxation                          0
hidden hardware advantage                           0
unrecorded manual tuning                            0
raw evidence locations present                      PASS
low/base/high sensitivity completed                 PASS
material open NFR dependency classified             PASS
secondary-store benefit measured against baseline   PASS
preferred != selected                               PASS
```

# PM-09 evidence-weighted decision-score reconciliation

This amendment reconciles the original executable Phase-10 benchmark protocol with the subsequently approved evidence-first Physical Model process. It does **not** weaken or remove any hard gate, change any scoring weight, or convert unexecuted evidence into a direct PASS.

## Two scoring ledgers

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable hard-gate PASS
requires direct benchmark/recovery/evolution artifacts
uses the original execution protocol above

EVIDENCE-WEIGHTED DECISION SCORE
may be used by PM-09/PM-10 as a comparative decision aid
only when the evidence-first admission conditions below are satisfied
```

```text
EVIDENCE-WEIGHTED DECISION SCORE
!=
VERIFIED-RUN BENCHMARK SCORE
```

A PM-09 evidence score is never evidence that `HG-01..HG-12` were executed or passed.

## Evidence-weighted admission conditions

PM-09 may produce an evidence-weighted decision score only when all of the following are true:

```text
1. candidate-native mappings are complete enough for comparison;
2. semantic/static/external evidence has been exhausted;
3. no unresolved ranking-critical EXECUTION-WORTHY gap remains;
4. all unexecuted direct scenarios remain explicitly NOT RUN;
5. known structural costs are scored as such rather than assumed away;
6. unmeasured performance is not invented;
7. mandatory selected-implementation proofs remain carried forward;
8. sensitivity analysis checks whether missing execution could plausibly reverse the ranking.
```

If a ranking-critical residual gap appears, the evidence-score path stops and the relevant direct proof must be separately admitted.

## Weight preservation

The evidence-weighted decision score uses the exact same 100-point dimensions and weights already frozen above. This reconciliation does not authorize changing them inside PM-09.

Dimension grades must cite PM-02 through PM-08 evidence and must identify where confidence is weaker because direct execution is absent.

## Result vocabulary under the evidence ledger

An evidence-weighted score may establish:

```text
CURRENT EVIDENCE-SCORE LEADER
ROBUST / SENSITIVITY-DEPENDENT
ADVANCE TO RECOMMENDATION
```

It does **not** by itself establish:

```text
DIRECT HARD-GATE PASS
VERIFIED-RUN PASS
SELECTED
```

PM-10 may use the evidence score, sensitivity and carried conditions to produce a bounded recommendation/PREFERRED status under the active Physical methodology. PM-11 remains the separate explicit selection gate.

## PM-09 reconciliation state at the time of scoring

The Physical Model reached PM-09 with:

```text
DIRECT HG PASS                     0
LOW/BASE/HIGH                      NOT RUN
PM-04B                             NOT ADMITTED
RANKING-CRITICAL EXECUTION GAPS    0
POST-SELECTION PROOFS              CARRIED FORWARD
```

The resulting PM-09 score artifacts live under:

```text
docs/physical-model/pm-09-scoring-sensitivity-v1.md
docs/physical-model/scoring/*
```

These artifacts must continue to label themselves `EVIDENCE-WEIGHTED DECISION SCORE` until direct execution creates a separate verified-run score.

# Phase 10 boundary — current method, historical execution state

This specification plus the scenario corpus and benchmark register is the remotely QA-verified Phase 10 method package, with the bounded PM-09 evidence-score reconciliation above.

Phase 10 itself does **not**:

- implement benchmark harness code;
- design PostgreSQL tables/indexes;
- design TypeDB schema/queries;
- design Neo4j projections;
- choose pgvector indexes;
- select a primary database;
- authorize production backend implementation.

Repository-safety and clean-room Pre-Physical verification were subsequently completed as Phases 11 and 12. Those later phases did not change the semantic hard gates.

The later Physical workstream completed PM-11/12/13/14 and integrated through PR #15. Current selected truth is PostgreSQL 18.4 plus the bounded companion target stack. Direct benchmark execution remains a separate evidence ledger and is still `NOT RUN` where recorded; `DIRECT HG PASS = 0` and `VERIFIED-RUN SCORE = NOT AVAILABLE` remain unchanged.
