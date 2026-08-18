# Physical Model Execution Methodology v1

- Status: **CURRENT — PM-06/07 JOINT EVIDENCE-FIRST QUALIFICATION COMPLETE**
- Workstream: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Direct execution: **NOT STARTED**
- Primary finalists: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- Preferred: **NONE**
- Selected: **NONE**

## Purpose

Define how LifeOS converts accepted Domain + Logical semantics into an evidence-backed Physical Model without selecting infrastructure by popularity, vendor marketing, ritual benchmark breadth or implementation convenience.

This methodology does not alter Domain/Logical authority or the Phase-10 semantic benchmark corpus.

## Repository discipline

Every Physical write scope must:

1. verify actual remote `feature/physical-model` HEAD;
2. compare against current `main`;
3. re-read the active workstream handoff and relevant authority;
4. perform temporally unstable research read-only first;
5. present exact PRE-SCOPE / CREATE / UPDATE / DELETE allow-list;
6. write only approved paths;
7. preserve evidence-history/current-truth separation;
8. compare PRE-SCOPE -> final HEAD remotely;
9. verify added/modified/deleted/unexpected paths;
10. read back critical output from the remote branch;
11. save the terminal handoff last where practical.

A tool invocation/no-op is not repository evidence.

## Semantic barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
PROVIDER STATE != CANONICAL STATE
DERIVED STATE != CANONICAL STATE
TECHNICAL AUTHZ != DOMAIN AUTHORITY
MISSING != FALSE
EVIDENCE-QUALIFIED != DIRECT PASS
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
```

Do not introduce a universal Entity/Thing/EAV/generic-edge canonical kernel merely to fit a candidate.

`WL-H01..WL-H12` remain non-negotiable downstream obligations.

## Research/source policy

For current product capabilities, version/edition/topology, licensing, backup, HA, driver support and deployment constraints:

```text
official product documentation / release notes
= baseline authority
```

Secondary/public benchmark/case-study evidence may support context, but must disclose source class and cannot become a fictional LifeOS run.

## Evidence-first / execution-minimization rule

Direct execution is a last-mile evidence tool.

Before any fixture/harness/database deployment/local benchmark, classify the question:

```text
EXT-SUFFICIENT
MAP-SUFFICIENT
KNOWN-STRUCTURAL-COST
SYSTEM-BOUNDARY
DEFER-FINALIST / POST-SELECTION VALIDATION
RESIDUAL-GAP
EXECUTION-WORTHY
```

Execution opens only when:

```text
RESIDUAL-GAP
+ decision relevance
+ external/mapping evidence exhausted
+ controlled execution can resolve it
= EXECUTION-WORTHY
```

The benchmark-host HOLD is therefore dormant until a direct run is actually admitted.

## Cost/quality policy

```text
TARGET
initial direct technology/license cost = EUR 0 where realistically possible

BUT
free != automatic preference
paid != automatic rejection
quality/correctness outrank cost
```

Decision priority:

1. semantic correctness;
2. consistency/integrity/security/privacy/recovery;
3. LifeOS workload/capability fit;
4. maturity/operability/maintainability/Python tooling;
5. performance/resource efficiency where decision-relevant;
6. TCO/deployment requirements;
7. lock-in/exit/migration risk.

The final architecture may be one canonical primary plus bounded specialists. Every extra technology must earn its complexity.

## Fixed roadmap

```text
PM-00 Bootstrap / authority freeze
PM-01 Technology discovery / candidate freeze
PM-02 Primary mapping design
PM-03 Semantic static preflight
PM-04 Evidence sufficiency + conditional harness
PM-05 Correctness/destructive evidence qualification
PM-06 Scale/performance evidence
PM-07 Recovery/evolution/failure evidence
PM-08 Secondary/specialist lanes
PM-09 Scoring + sensitivity
PM-10 Recommendation
PM-11 Explicit selection
PM-12 Accepted Physical Model
PM-13 Independent clean-room QA
PM-14 Closure / protected-main integration
```

The numbered gates remain distinct. PM-06 and PM-07 are operated as one **Joint Finalist Qualification Campaign**, while their result layers remain separate.

## PM-00 — Bootstrap

Status: `QA PASS`.

Established Physical authority, evidence vocabulary, repository discipline and resumable handoff. No technology selected.

## PM-01 — Discovery / Candidate Freeze

Status: `PASS-CONDITIONAL`.

Admitted primary subjects:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

Benchmark host remained HOLD and is now dormant until direct execution admission.

## PM-02 — Primary Mapping Design

Status: `COMPLETE`.

All four candidate-native mappings remain historical evidence. No mapping is selected by existence.

## PM-03 — Semantic Preflight

Status: `STATIC COMPLETE / 0 STATIC REJECTS`.

Direct hard gates remained `NOT RUN`.

## PM-04 — Evidence Sufficiency + Conditional Harness

### PM-04A

Status: `COMPLETE / 48 OF 48 CELLS CLASSIFIED / 0 EXECUTION-WORTHY GAPS`.

### PM-04B

Status: `NOT ADMITTED / HARNESS NOT STARTED`.

A later phase may reopen PM-04B only through a fresh exact gate for a ranking-critical or mandatory implementation proof.

## PM-05 — Correctness / Destructive Evidence Qualification

Status: `COMPLETE`.

Primary finalists:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
```

Deferred, not rejected:

```text
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

Primary semantic scenarios were evidence-qualified; provider/runtime scenarios were classified as system-boundary; secondary search/graph scenarios were deferred to PM-08.

## PM-06 + PM-07 — Joint Finalist Qualification

Status: **COMPLETE — EVIDENCE-FIRST / DIRECT RUNS NOT ADMITTED**.

### Joint operating rule

Collect shared evidence once, then emit two separate judgments:

```text
PM-06
scale/performance/resource viability and sensitivity

PM-07
backup/recovery/evolution/failure/topology/operations
```

Performance cannot compensate for recovery/evolution failure.

### PM-06 acceptance

A finalist may advance without LOW/BASE/HIGH direct execution when:

- credible evidence establishes viability;
- no accepted product SLA makes performance discriminating;
- no residual scale question can materially change ranking;
- unexecuted tiers remain explicitly `NOT RUN`.

Current result:

```text
PostgreSQL       VIABLE / HIGH CONFIDENCE
TypeDB CE        VIABLE / MEDIUM-HIGH CONFIDENCE
LOW/BASE/HIGH    NOT RUN
performance reversal signal NONE
```

TypeDB exact-subject conditions include single-query single-threading, CE single-node topology and documented resource/index sizing pressure.

### PM-07 acceptance

A finalist may advance on evidence qualification when engine recovery/evolution paths are viable and remaining semantic restore/migration proof is implementation-specific rather than ranking-critical.

Current result:

```text
PostgreSQL
clear operations/recovery/topology advantage

TypeDB CE
viable recovery/evolution
higher self-hosted operations/topology cost
```

Direct SC-011/030/031/032 execution is moved to **post-selection implementation validation** rather than declared PASS.

SC-013 remains a reopen trigger only if PM-09 becomes performance-sensitive.

## Direct execution truth

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
LOW/BASE/HIGH            NOT RUN
DIRECT HG PASS            0
RESTORE REHEARSAL         NOT RUN
MIGRATION REHEARSAL       NOT RUN
FAILURE INJECTION         NOT RUN
BENCHMARK HOST            HOLD / DORMANT
```

Do not mutate these values without real execution artifacts.

## PM-08 — Secondary Lanes

Next phase.

PM-08 asks which specialist capabilities, if any, earn additional technology cost after the primary comparison has narrowed.

Relevant lanes include:

```text
GRAPH
G0 primary-store baseline
Neo4j or PM-01-admitted alternative only if graph specialization materially wins

SEARCH/VECTOR
primary-native structured/lexical baseline
pgvector when PostgreSQL applicable
Qdrant/OpenSearch only on concrete specialist trigger

LOCAL/OFFLINE
SQLite only as bounded client/local state, never silent canonical authority
```

Secondary state must be rebuildable/reconcilable where the accepted architecture requires it. No specialist may hide a primary hard-gate weakness.

## PM-09 — Scoring + Sensitivity

Only after PM-08 evidence is coherent.

Primary 100-point dimensions remain:

```text
semantic mapping simplicity/evolvability 20
transaction/concurrency ergonomics       15
query/report/traversal                   15
history/current efficiency               10
operations/backup/restore/HA             15
schema evolution/migration               10
performance/resource efficiency          10
Python/tooling/cost/exit risk             5
```

Scores require evidence. Unexecuted measurements cannot be invented.

Sensitivity must test whether ranking changes under scale/history/concurrency/topology/recovery/cost assumptions. Instability => `SENSITIVITY-DEPENDENT`.

## PM-10 — Recommendation

May produce `PREFERRED`; cannot produce `SELECTED`.

## PM-11 — Explicit Selection

`SELECTED` requires separate user approval with candidate, exact subject, evidence basis, conditions, sensitivity, cost/topology implications and rejected/deferred alternatives.

## PM-12..PM-14

After selection:

```text
PM-12 accepted Physical Model
PM-13 independent clean-room QA
PM-14 protected PR/merge/main verification
```

Physical closure does not automatically start Backend Foundation.

## Stop/reopen conditions

Stop and re-gate if:

- Domain/Logical contradiction appears;
- a candidate requires semantic weakening;
- a new semantic owner/root appears necessary;
- PM-08 proposes a new engine without bounded admission rationale;
- direct execution needs unapproved infrastructure/path scope;
- official capability evidence contradicts the frozen subject;
- a ranking-critical residual gap appears;
- selection is being inferred rather than explicitly authorized;
- a path outside the approved scope must be written.

## Current next step

```text
PM-06 COMPLETE
PM-07 COMPLETE
DIRECT EXECUTION NOT RUN
CURRENT LEADER PostgreSQL
PRINCIPAL CHALLENGER TypeDB
PREFERRED NONE
SELECTED NONE

NEXT
PM-08 secondary/specialist lanes after fresh explicit gate
```