# Physical Model Execution Methodology v1

- Status: **CURRENT — PM-05 COMPLETE / PM-06+PM-07 JOINT NEXT**
- Workstream: `feature/physical-model`
- Base authority: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Direct execution: **NOT STARTED**
- Selection: **NONE**

## Purpose

Define the mandatory operating sequence for producing a real LifeOS Physical Model from the accepted Domain, Logical, Pre-Physical and Phase-10 authority.

The methodology is correctness-first, evidence-first and execution-minimizing:

```text
use authoritative evidence where it already resolves a question
use LifeOS mapping reasoning where engine guarantees are sufficient
retain structural costs as costs
run local/direct tests only when a residual question is decision-relevant and test-resolvable
never convert documentation into fictional direct execution
```

This document governs the process. PM-specific evidence lives in the PM-01..PM-05 records and their candidate records.

## Global operating rules

Every Physical scope follows the same discipline:

1. verify current remote branch HEAD and relation to current `main`;
2. reconstruct current authority from repository truth, not conversation memory;
3. perform read-only discovery first where current external facts matter;
4. present exact branch/PRE-SCOPE/CREATE/UPDATE/DELETE gate;
5. obtain explicit approval before first remote write;
6. write only approved paths;
7. preserve current truth vs historical/evidence separation;
8. compare PRE-SCOPE -> final branch HEAD;
9. verify exact path/mutation set and `behind_by` truth;
10. remotely read back critical payloads;
11. update the workstream handoff last where practical;
12. do not advance on intention/tool invocation alone.

A failed/no-op tool call is not repository state.

## Source and evidence rule

For version/edition/topology-sensitive product facts:

```text
official product documentation
or official release/API/operations documentation
= baseline authority
```

Production case studies, engineering reports, public benchmarks and independent research may strengthen comparative evidence, but their source class and limitations must remain explicit.

```text
OFFICIAL ENGINE GUARANTEE
!= LIFEOS DIRECT EXECUTION

PUBLIC/VENDOR BENCHMARK
!= LIFEOS BENCHMARK

PRODUCTION CASE
!= PROOF OF OUR MAPPING

MAP-SUFFICIENT
!= EXECUTED HG PASS
```

## Evidence-sufficiency classes

Use:

```text
EXT-SUFFICIENT
MAP-SUFFICIENT
KNOWN-STRUCTURAL-COST
DEFER-FINALIST
RESIDUAL-GAP
EXECUTION-WORTHY
```

Execution admission requires all of:

```text
RESIDUAL-GAP
+ materially decision-relevant
+ external/reasoned evidence exhausted
+ controlled test can actually resolve it
= EXECUTION-WORTHY
```

Direct execution is therefore a last-mile evidence mechanism, not the default technology-selection method.

## Semantic guardrails

The Physical Model consumes closed Domain/Logical semantics. It does not reopen them by convenience.

Never introduce as canonical shortcuts:

```text
universal Entity / Thing root
universal generic Relationship/edge root
generic EAV/property-bag canonical kernel
universal Rule / Fact / WorkItem / Command root
provider IDs/revisions as canonical identity/material state
missing row == false
storage/MVCC/system-time/changefeed token == MaterialStateRef
technical AuthZ allow/deny == Domain Authority/Consent
AI/solver output == canonical truth/effect
per-recipient duplicate canonical reality
```

Required address families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Required state layers remain distinguishable:

```text
canonical LifeOS state
material historical state
derived/projection state
external/provider state
candidate/unresolved state
security/runtime state
```

`WL-H01..WL-H12` remain non-negotiable downstream constraints.

## Quality / cost / architecture policy

Decision priority:

1. semantic correctness;
2. consistency, integrity, security, privacy and recoverability;
3. real LifeOS workload/capability fit;
4. maturity, operability, maintainability and Python/tooling fit;
5. performance/resource efficiency where decision-relevant;
6. TCO/deployment requirements;
7. lock-in/exit/migration risk.

Economic posture:

```text
initial direct technology/license target = EUR 0 where realistically possible

BUT
free != automatic preference
paid != automatic rejection
cost cannot rescue semantic/operational inferiority
```

Architecture posture:

```text
one primary canonical store
+
bounded specialists only when each independently earns its complexity
```

A secondary engine cannot hide a primary hard-gate weakness.

## Fairness rule

Keep the following the same across candidates where direct comparison is admitted:

```text
accepted semantics
scenario meaning
truth oracle/assertions
result semantics
measurement protocol where comparable
```

Allow candidate-native differences in:

```text
physical schema
query language
constraint/index mechanisms
storage representation
transaction technique
```

Never force one engine to imitate another.

# PM roadmap

## PM-00 — Bootstrap / Authority Freeze — COMPLETE

Established Physical authority, methodology, evidence contracts, result register, acceptance matrix and resumable workstream.

Status: `QA PASS`.

## PM-01 — Technology Discovery / Candidate Freeze — COMPLETE

Broad discovery plus exact candidate subjects, editions/topologies, cost/license and operability evidence.

Current primary subjects:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

Status: `PASS-CONDITIONAL`.

Benchmark host remains:

```text
HOLD / DORMANT
```

It becomes blocking only before a separately admitted reproducible direct run.

## PM-02 — Primary Mapping Design — COMPLETE

Produced candidate-native mappings against the same accepted LifeOS semantics.

Rules:

- no universal meta-model;
- storage revision != MaterialStateRef;
- provider revision != MaterialStateRef;
- runtime/workflow identity != semantic identity;
- mapping complexity itself is evidence.

## PM-03 — Semantic Mapping Preflight — COMPLETE

Static hard-gate review across `HG-01..HG-12`.

Direct execution remained `NOT RUN`.

PM-03 preflight result remains historical/current evidence and is not rewritten into direct PASS by later evidence.

## PM-04A — External Evidence Sufficiency — COMPLETE

Classified all `4 × 12 = 48` candidate/hard-gate cells.

Result:

```text
EXECUTION-WORTHY gaps  0
PM-04B                 NOT ADMITTED
FULL LOCAL BENCHMARK   NOT ADMITTED
TARGETED LOCAL PROOFS  0 ADMITTED
```

## PM-04B — Targeted Fixture / Oracle / Harness — CONDITIONAL / NOT ADMITTED

Open only if a later phase identifies an `EXECUTION-WORTHY` gap or a finalist/closure obligation that genuinely requires direct execution.

Possible components, only when admitted:

```text
deterministic fixture generator
semantic oracle
candidate-specific adapter/schema
metrics/resource capture
failure injection
backup/restore hook
migration/evolution hook
raw artifact manifest
```

Harness code is benchmark infrastructure, not production backend code.

## PM-05 — Correctness / Destructive Evidence Qualification — COMPLETE

Goal: qualify `C0..C7` and `SC-001..SC-035` by decision value rather than executing every scenario ritualistically.

Scenario classes:

```text
PRIMARY-EVIDENCE-SUFFICIENT
PRIMARY-KNOWN-COST
SYSTEM-BOUNDARY
PM-06/07-FINALIST
PM-08-SECONDARY
EXECUTION-WORTHY
```

PM-05 result:

```text
PM-05 EXECUTION-WORTHY gaps  0
PM-04B reopened               NO
DIRECT scenario/HG execution NOT RUN
```

Primary semantic scenarios are evidence-qualified for current comparison.

System/provider/runtime scenarios remain valid architectural obligations but are not standalone four-database benchmark reasons.

Recovery/evolution/scale scenarios move to finalist qualification.

Primary finalist set:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
```

Deferred from primary finalist set, **not rejected**:

```text
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

Reopen deferred candidates only on an explicit material trigger recorded in PM-05 candidate qualification evidence.

# PM-06 + PM-07 — Joint Finalist Qualification Campaign — NEXT

PM-06 and PM-07 remain separate numbered/result layers but are operated as one evidence campaign for the primary finalists.

## Shared campaign rule

Use one finalist inventory and reuse evidence collection where product/version/topology/workload sources overlap.

```text
PRIMARY FINALISTS
PostgreSQL 18.4
TypeDB CE 3.12.3
```

Default evidence order:

```text
authoritative product/operations evidence
+ credible production scale evidence
+ published benchmark evidence with source bias/method disclosed
+ LifeOS mapping implications
        ↓
identify unresolved ranking-critical residual
        ↓ only if necessary
admit targeted direct proof
```

The campaign does **not** authorize a local benchmark by default.

## PM-06 result layer — Scale / Performance / Resource

Assess:

```text
current-state access under history depth
mixed read/write/consequential workload suitability
contention/conflict model cost
resource efficiency
storage/index growth behavior
scale/topology cliffs
manual tuning burden
published/production performance evidence quality
```

LOW/BASE/HIGH remain synthetic Phase-10 envelopes. If no direct execution is admitted:

```text
LOW  NOT RUN
BASE NOT RUN
HIGH NOT RUN
```

Do not invent p50/p95/p99 or throughput values.

Performance may affect ranking/sensitivity only after semantic/integrity requirements are satisfied.

## PM-07 result layer — Recovery / Evolution / Failure / Operations

Assess:

```text
backup/restore mechanism and edition/topology constraints
PITR/snapshot/export semantics where applicable
old-backup anti-resurrection strategy
schema/data evolution mechanics
historical reference preservation
failure/crash boundaries
capacity/backpressure behavior
HA/failover conditions where materially relevant
operations/tooling burden
RPO/RTO capability bands without inventing business commitments
```

Finalist/direct obligations carried from PM-05:

```text
SC-011 redaction + old backup
SC-013 deep-history scale sensitivity
SC-030 V1 -> V2 evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure
```

A documented backup feature is not a LifeOS anti-resurrection PASS. However, a direct destructive rehearsal is admitted only if still required to make/close the finalist decision.

## Joint-campaign acceptance

The campaign can close evidence-first when:

```text
PM-06 evidence basis complete
PM-07 evidence basis complete
remaining direct obligations explicit
ranking-critical residual gaps counted
execution admission decision explicit
PM-06 and PM-07 results reported separately
PREFERRED/SELECTED still not inferred
```

If a ranking-critical residual remains, re-open PM-04B through a new exact gate and freeze the benchmark host before execution.

## PM-08 — Secondary Lanes

Evaluate secondary/specialist mechanisms only after primary finalist qualification is sufficiently clear.

### Graph lane

Compare no-specialist primary baseline with Neo4j or another admitted graph specialist only if graph workloads justify another engine.

Secondary graph state must remain rebuildable/projection state, not alternate canonical truth.

### Search/vector lane

Compare structured/lexical baseline with pgvector or another admitted specialist only when semantic/vector retrieval has a demonstrated product need.

Filtering/Visibility boundaries apply before quality claims.

### Local/offline lane

SQLite or another local mechanism may be evaluated as bounded device/client state, never as automatic canonical peer.

### Event/document/specialist lanes

No named specialist is benchmarked by default. First prove a concrete gap/benefit.

## PM-09 — Scoring + Sensitivity

Only evidence-qualified candidates/roles proceed.

Primary 100-point framework remains:

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

Every score requires an explicit evidence basis. Unmeasured dimensions must not be presented as measured.

Sensitivity must consider:

```text
scale/history depth
concurrency/contention
production topology
RPO/RTO assumptions
search/projection pressure
edition/license/TCO
```

Unstable ranking becomes `SENSITIVITY-DEPENDENT`.

## PM-10 — Recommendation

Produce evidence-backed role recommendation using:

```text
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
```

`PREFERRED` is recommendation only.

Expose:

- evidence basis;
- conditions/holds;
- direct-execution coverage;
- score/sensitivity;
- operations/TCO;
- lock-in/exit consequences;
- why alternatives lost/were deferred.

## PM-11 — Explicit Selection Gate

No technology becomes `SELECTED` automatically.

Before selection present:

```text
candidate/role
exact version/edition/topology
evidence basis
remaining direct obligations
hard-gate conditions
score/sensitivity
TCO/cost conditions
rejected/deferred alternatives
migration/exit consequences
downstream implementation consequences
```

Explicit user approval is required.

## PM-12 — Accepted Physical Model

After PM-11 approval, write the durable accepted Physical authority:

- selected primary canonical persistence;
- selected bounded specialists if any;
- identity/reference mapping;
- transaction/concurrency rules;
- history/current/state-layer strategy;
- retention/recovery/evolution strategy;
- deployment conditions;
- evidence caveats/sensitivity;
- downstream backend constraints;
- explicitly deferred/rejected alternatives.

Do not hide unresolved HOLD items.

## PM-13 — Independent Clean-Room QA

Reconstruct the Physical result from repository truth without conversation memory and verify:

```text
Domain unchanged unless explicitly reopened
Logical unchanged unless explicitly reopened
Phase-5..10 constraints preserved
claims traceable
no direct execution fabricated
score/recommendation reproducible
selection explicitly authorized
no production backend started accidentally
current docs coherent
```

## PM-14 — Closure / Protected Main Integration

Only after PM-13 PASS:

```text
final compare
protected PR to main
merge commit
post-merge verification
current-truth alignment if required
```

Physical closure does not automatically start Backend Foundation.

## Direct execution protocol

Before changing any direct HG/scenario/tier from `NOT RUN`:

1. prove the question is execution-worthy or a required finalist/closure obligation;
2. obtain a fresh execution/write gate;
3. freeze exact host/runtime/topology;
4. freeze exact mapping/schema/harness revision;
5. freeze scenario/corpus/fixture revision and seed where applicable;
6. retain raw evidence/artifact hashes;
7. classify candidate failure vs tooling/environment failure;
8. update only evidence-backed direct results;
9. never fabricate measured values.

Benchmark-host fields when activated:

```text
host identity
CPU/RAM
storage/filesystem/free disk
OS/build/kernel
container/native runtime
network/topology
resource limits
background-load policy
clock/timezone
```

## Stop conditions

Stop and re-gate if:

- Domain/Logical contradiction appears;
- a new semantic owner/root seems necessary;
- a candidate requires weakening a hard gate;
- a deferred/new candidate is to be re-admitted without its documented trigger;
- direct execution requires unapproved infrastructure/path scope;
- version/edition/topology evidence materially conflicts with the frozen subject;
- benchmark environment changes comparability;
- an out-of-scope path is required;
- `PREFERRED` or `SELECTED` is about to be inferred without its proper gate.
