# Physical Model Execution Methodology v1

- Status: **CURRENT — PM-04A EVIDENCE-FIRST REVISION**
- Workstream: `feature/physical-model`
- Base authority: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Direct execution: **NOT STARTED**
- Selection: **NONE**

## Purpose

Define the mandatory operating sequence for producing a real LifeOS Physical Model from the accepted Pre-Physical architecture and Phase-10 benchmark method.

This methodology governs **how the Physical workstream proceeds**. It does not replace the Phase-10 benchmark specification/corpus/register and does not change Domain or Logical semantics.

## Global operating rules

Every PM phase follows the same repository discipline:

1. re-read current branch HEAD and `main`;
2. identify exact authority inputs;
3. perform read-only discovery first where the phase depends on current external facts;
4. present exact branch/PRE-SCOPE/CREATE-UPDATE-DELETE gate before write;
5. write only approved paths;
6. preserve current-vs-history separation;
7. perform remote compare QA from PRE-SCOPE;
8. read back critical outputs from the remote branch;
9. record exact result/checkpoint in the Physical handoff;
10. do not advance if the phase acceptance criteria are not met.

A tool failure/no-op never counts as repository state. Verify remote state before retry.

## Research/source rule

Current product capabilities, versions, editions, licenses, HA/backup behavior, client compatibility and deployment constraints are temporally unstable.

For such claims:

```text
official primary product documentation
or official release notes/API docs
= required baseline evidence
```

Secondary articles may help discovery but cannot override exact official/version-specific evidence.

If current official documentation is contradictory or insufficient, mark the affected question `HOLD` and test it directly where feasible **only when the unresolved behavior remains materially decision-relevant**.

## Evidence-sufficiency / execution-minimization rule

Direct local execution is an evidence tool, not the default database-selection method.

Before creating a fixture, harness, database deployment or local/server benchmark, exhaust existing evidence and classify the unresolved question.

Allowed PM-04A evidence classes:

```text
EXT-SUFFICIENT
= authoritative external evidence establishes the relevant engine capability/limitation

MAP-SUFFICIENT
= accepted LifeOS mapping + documented engine guarantee is sufficient for current comparative reasoning

KNOWN-STRUCTURAL-COST
= uncertainty has resolved into a known design/operational burden that a toy test cannot remove

DEFER-FINALIST
= direct LifeOS rehearsal may be warranted before final acceptance, but testing all candidates now is disproportionate

RESIDUAL-GAP
= evidence remains materially incomplete

EXECUTION-WORTHY
= residual gap is unresolved AND capable of materially changing the recommendation
```

Execution admission rule:

```text
RESIDUAL-GAP
+ decision relevance
+ external/reasoned evidence exhausted
+ test can actually resolve the question
= EXECUTION-WORTHY
```

Only an `EXECUTION-WORTHY` result opens PM-04B by default.

Important separation:

```text
external evidence sufficiency
!= direct LifeOS execution

public benchmark
!= LifeOS benchmark

production case study
!= proof of LifeOS mapping

MAP-SUFFICIENT
!= executed HG PASS
```

Therefore direct scenario/tier slots remain `NOT RUN` unless a direct run actually occurs.

The benchmark-host HOLD is dormant/non-blocking for evidence-only phases. It becomes blocking before any reproducible direct execution claim.

## Technology discovery and quality/cost policy

The Physical Model must search for the **best technology fit for LifeOS**, not merely choose among the products that happened to be named before PM-01.

Existing Phase-10 candidates remain mandatory anchors/challengers where their registered lane applies, but they are not a closed universe.

PM-01 read-only discovery may identify additional plausible products, engines or bounded technology combinations when there is a concrete LifeOS fit rationale. A new candidate does not automatically enter PM-02 execution: it must first pass an explicit bounded admission decision based on likely semantic fit, operational realism, maturity and distinct value versus already registered candidates.

The economic posture is:

```text
TARGET OPERATING POSTURE
initial direct technology/license cost = EUR 0 where realistically possible

BUT
EUR 0 != semantic requirement
EUR 0 != permission to lower correctness, durability, security or evolvability
paid != automatic rejection
free != automatic preference
```

Decision priority is:

```text
1. semantic correctness / preservation of Domain + Logical invariants
2. consistency, integrity, security, privacy and recoverability
3. real LifeOS workload and capability fit
4. operability, maturity, maintainability and Python/tooling fit
5. performance and scalable resource efficiency where it can affect the decision
6. total cost of ownership and deployment requirements
7. lock-in, exit risk and realistic migration path
```

Cost is therefore a decision dimension and can be a strong differentiator between otherwise comparable candidates, but it cannot rescue a materially inferior or semantically unsafe technology.

If a materially better candidate requires payment, proprietary infrastructure or meaningful lock-in, do not discard it silently. Record the exact benefit and cost/constraint, then evaluate in order:

1. whether an equivalent or near-equivalent zero-cost/open alternative exists;
2. whether the paid capability is actually required now or only under a future condition;
3. whether a zero-cost starting topology can preserve the accepted Physical semantics without creating a dead end;
4. whether an explicit migration/exit strategy is justified by the real risk.

Do not create portability abstraction for hypothetical future migrations if it materially degrades the selected technology or adds unjustified complexity.

```text
portable where cheap and structurally useful
candidate-native where materially better
no gratuitous lock-in
no gratuitous abstraction
```

The best LifeOS result may be one primary canonical store plus bounded specialized mechanisms. Every additional technology must independently justify its operational and semantic cost; multi-store complexity is never rewarded by itself.

## Fixed-gate / evolutionary-roadmap rule

The Physical Model is neither a free-form exploration nor a rigid list of predetermined products.

The **sequence and semantic gates are fixed** unless a separately authorized process revision changes them:

```text
PM-00 -> PM-01 -> PM-02 -> ... -> PM-14
correctness before performance
PREFERRED != SELECTED
explicit write gates
explicit selection gate
clean-room QA before closure
```

PM-04A is an authorized process refinement **inside PM-04**. It does not insert/remove a numbered phase or weaken hard gates.

The **content inside those gates is evolutionary**:

```text
candidate universe may expand/contract on evidence
exact versions/editions/topologies may change before freeze
mapping designs are candidate-native and may be repaired before execution
secondary lanes activate only when justified
paid/free/managed/self-hosted alternatives are evaluated when materially relevant
benchmark sensitivity may force reruns or conditional recommendations
direct execution breadth may contract when authoritative evidence makes it non-decision-relevant
```

This prevents premature lock-in and ritual benchmarking while keeping the project reproducible and resumable.

## Fairness rule

```text
SAME
accepted semantics
scenario inputs
truth oracle
correctness assertions
result semantics
measurement protocol where comparable

IDIOMATICALLY DIFFERENT
physical schema/mapping
query language
index/constraint mechanism
candidate-native storage representation
```

Do not force one candidate to imitate another. Do not relax a LifeOS invariant because a candidate makes it inconvenient.

# PM-00 — Bootstrap / Authority Freeze

Goal: create the Physical workstream, operational rules, test/evidence contracts and resumable handoff.

Required output:

- Physical directory/index;
- execution methodology;
- run/evidence template;
- acceptance-test matrix;
- result register;
- workstream handoff;
- current project/architecture status activation;
- Phase-10 documents marked as consumed by an authorized Physical workstream without altering their method/result slots.

Acceptance:

```text
branch created from approved main
bootstrap path delta exact
main unchanged
Domain/Logical unchanged
benchmark execution NOT STARTED
technology selection NONE
bootstrap readback PASS
```

# PM-01 — Candidate / Environment Freeze — READ-ONLY FIRST

Goal: perform broad read-only technology discovery, admit only serious LifeOS candidates, and turn admitted abstract candidates into exact benchmark subjects.

For each candidate/lane record where applicable:

```text
product
exact current candidate version to test
edition/license class
deployment mode/topology
supported OS/container/runtime
client/driver version
HA/cluster mode
backup/restore mechanism
schema/constraint capability
migration/evolution tooling
observability/tooling
known license/feature boundaries
direct and likely infrastructure cost posture
lock-in / exit characteristics
```

Mandatory starting anchors, **not a closed shortlist**:

- PostgreSQL hybrid;
- TypeDB.

PM-01 must also scan credible current alternatives across relevant technology families and record why each serious candidate is `ADMIT`, `DEFER`, `HOLD` or `REJECT-FROM-BENCHMARK`. Discovery breadth is required; benchmark breadth is not. Products must earn execution scope through a bounded admission rationale rather than being added for list size.

Secondary lane subjects are frozen when their lane is admitted/executed, including registered anchors such as:

- G0 baseline / Neo4j;
- S0 baseline / pgvector;
- ED specialized only after explicit admission.

PM-01 may also discover alternatives to these secondary-lane anchors; no secondary product becomes canonical or selected by discovery alone.

Execution environment is frozen only when direct execution is admitted. Until then, record the benchmark-host requirement as HOLD/dormant rather than inventing an environment.

When execution is admitted, freeze:

```text
CPU
RAM
storage/media/filesystem where material
OS
container/runtime
network topology
single-node vs HA capability
available disk budget
time budget
reproducibility constraints
zero-cost/local/self-hosted constraints where applicable
unavailable paid or external infrastructure
```

PM-01 is read-only with respect to Physical mapping/harness/schema implementation. Its output is a technology landscape, admission register, exact candidate inventory and environment requirements without forcing premature host selection.

Acceptance:

- no candidate capability inferred from memory;
- discovery is not artificially limited to previously named products;
- exact version/edition/deployment questions identified for admitted candidates;
- official sources captured;
- license/cost/deployment constraints distinguished from semantic capability;
- contradictions marked HOLD;
- benchmark environment requirement documented honestly;
- no schema/harness write started;
- no candidate selected.

# PM-02 — Primary Mapping Design

Goal: design idiomatic candidate-specific Physical mappings for the explicitly admitted primary candidates against the same accepted semantic corpus.

PostgreSQL and TypeDB remain mandatory primary mappings unless PM-01 produces a separately reviewed hard blocker. Additional primary candidates require PM-01 admission plus the PM-02 write gate.

Required mapping package per primary candidate:

```text
semantic owner -> physical representation
reference-family mapping
binary/n-ary relation representation
material/current/history representation
governance/policy representation
expected-state mechanism
multi-owner transaction boundary
provider/external state separation
derived/projection separation
temporal/recurrence representation
retention/redaction/tombstone representation
schema/evolution strategy
backup/recovery assumptions
query-family strategy
```

Rules:

- no universal Entity/Thing/EAV/generic-edge canonical kernel;
- technical registries/discriminators allowed only if semantics remain explicit;
- storage revision != `MaterialStateRef`;
- provider revision != `MaterialStateRef`;
- runtime/workflow IDs do not become semantic identity;
- mapping complexity itself is evidence.

No performance claim counts in PM-02.

# PM-03 — Semantic Mapping Preflight

Goal: determine whether candidate mappings are semantically eligible for further evidence qualification.

Evaluate applicable `HG-01..HG-12` using static design review plus executable proof where already available.

Each gate result:

```text
PASS
PASS-CONDITIONAL
HOLD
REJECT
NOT-APPLICABLE with rationale
```

Rules:

- material hard-gate failure cannot be averaged away;
- insufficient evidence = HOLD, not PASS;
- a REJECTed primary candidate does not receive weighted performance scoring unless a later explicit repair/reopen proves the hard gate can be satisfied without semantic weakening.

# PM-04 — Evidence Sufficiency + Conditional Harness

PM-04 has two bounded sub-stages under the same numbered phase.

## PM-04A — External Evidence Sufficiency — DEFAULT FIRST

Goal: exhaust authoritative/public evidence and LifeOS mapping reasoning before manufacturing local execution.

Required output:

```text
candidate × HG-01..HG-12 evidence-sufficiency matrix
source ledger per candidate
confidence and source class
known structural costs
residual-gap register
decision relevance per residual gap
EXECUTION-WORTHY count
PM-04B admission decision
```

Rules:

- official engine guarantees may establish capabilities/limitations for comparative reasoning but never become fictional direct LifeOS execution;
- public/vendor benchmarks may support viability/performance context but are not LifeOS benchmark runs;
- production cases are supporting architecture/maturity evidence, not proof of our mapping;
- do not locally re-prove settled generic engine properties merely to fill a matrix;
- a known structural limitation should count directly as a candidate cost rather than be converted into an unnecessary local test;
- `DEFER-FINALIST` is allowed for recovery/migration/system proof that should not be repeated across all candidates;
- benchmark host is not required for PM-04A;
- no executed hard-gate result changes from `NOT RUN` without direct evidence.

PM-04A completion does not automatically authorize PM-04B.

## PM-04B — Targeted Fixture / Oracle / Harness — CONDITIONAL

PM-04B opens only when PM-04A identifies one or more `EXECUTION-WORTHY` gaps, or when a later explicit gate proves direct execution is required for a finalist/closure obligation.

Goal: implement the minimum common semantic fixtures/oracles and candidate-specific adapters necessary to resolve the admitted gaps without contaminating the evidence with candidate-specific semantics.

Possible components when actually required:

```text
deterministic fixture generator
seed handling
dataset manifest/hash
semantic truth oracle
candidate setup/teardown
candidate mutation/query adapters
metrics capture
resource capture
failure-injection hooks
backup/restore hooks
migration/evolution hooks
raw artifact manifest
```

Harness code is benchmark infrastructure, not production backend code.

Rules:

- common scenario meaning lives above candidate adapters;
- candidate adapter may use native query/schema features;
- expected result must not be derived from candidate output itself;
- build only the fixtures/adapters needed for admitted questions; do not create a four-engine harness by ritual;
- raw run artifacts must be retained or summarized with durable hash/location metadata where size prevents repository storage;
- freeze the actual benchmark host before the first reproducible direct execution claim.

If PM-04A finds zero `EXECUTION-WORTHY` gaps:

```text
PM-04B
NOT ADMITTED

HARNESS
NOT STARTED

DATABASE DEPLOYMENT
NOT STARTED
```

# PM-05 — Correctness / Destructive Evidence Qualification

Goal: qualify mandatory applicable `C0..C7` and `SC-001..SC-035` correctness/destructive pressure using the strongest available evidence while preserving exact direct-run truth.

PM-05 starts from PM-04A evidence rather than assuming every scenario must be re-executed locally across every candidate.

For each scenario/gate distinguish:

```text
external capability evidence
LifeOS mapping reasoning
known structural limitation/cost
finalist-only direct obligation
direct execution result, if any
```

Minimum direct-run result per scenario **when direct execution is admitted**:

```text
scenario ID
candidate
mapping revision
dataset/seed
assertions
raw PASS/FAIL
failure-injection state
evidence artifact
observed caveat
hard-gate linkage
```

Rules:

- external evidence never changes a direct execution slot from `NOT RUN`;
- a direct hard-gate failure cannot be averaged away;
- if a mandatory unresolved semantic question remains material and cannot be responsibly closed from external/mapping evidence, it becomes `EXECUTION-WORTHY` and PM-04B is reopened through a fresh gate;
- finalist-only destructive obligations remain explicit rather than being silently waived;
- do not perform broad local testing when it cannot change the recommendation.

# PM-06 — Qualification Scale + Performance Evidence

Goal: determine whether scale/performance/resource behavior can materially change the recommendation or sensitivity result.

Evidence order:

```text
credible published/product evidence
+ production evidence
+ architectural scaling limits
        ↓
identify unresolved LifeOS-specific sensitivity
        ↓ only when decision-relevant
admit direct LOW/BASE/HIGH execution
```

Rules:

- tiers are not business forecasts;
- vendor benchmarks are supporting evidence and their methodology/bias must be disclosed;
- do not rerun generic CRUD benchmarks merely because they exist in the historical method;
- local performance execution is admitted only when the result could materially change ranking/sensitivity or validate a required deployment condition;
- actual executed dataset counts must be recorded;
- latency distributions preferred over averages;
- throughput alone is insufficient;
- resource consumption must accompany performance;
- unexecuted HIGH is never labeled VERIFIED-RUN;
- progressive saturation/scaling evidence may support sensitivity analysis if limitations are explicit;
- if no direct tier is admitted, LOW/BASE/HIGH remain `NOT RUN` and the recommendation must disclose the evidence basis instead.

Capture where applicable when a run exists:

```text
p50/p95/p99
throughput
conflicts/retries
CPU
RAM
storage growth
index/projection size
write amplification
query plan/profile
manual tuning
warm/cold/cache condition
```

# PM-07 — Recovery / Evolution / Failure Evidence

Goal: qualify recovery/evolution/failure characteristics for the exact candidate/deployment subjects without confusing a documented capability with a LifeOS rehearsal.

Evidence-first treatment:

- compare exact edition/topology backup/restore mechanisms from authoritative documentation;
- compare migration/evolution mechanics and operational burden;
- record known topology/HA/RPO/RTO sensitivity instead of inventing commitments;
- use production/incident evidence where reliable and clearly classified;
- identify what direct destructive rehearsal remains mandatory for a finalist before final Physical acceptance.

Direct pressure, **when admitted for a finalist or material unresolved gap**, includes applicable:

- backup + destructive restore + semantic verification;
- redaction/deletion anti-resurrection after old-backup restore;
- schema/mapping V1→V2 evolution;
- historical reference preservation;
- crash/failure boundaries;
- capacity/backpressure;
- HA/failover only where the exact edition/topology claims it and that capability affects scoring;
- recovery observations reported as measured observations, not invented RPO/RTO commitments.

A backup command's existence is not a LifeOS anti-resurrection PASS. Conversely, the existence of such a finalist-only proof obligation does not justify repeating a destructive lab across candidates that are no longer competitive.

# PM-08 — Secondary Lanes

## Lane G

Compare G0 primary-store baseline versus G1 Neo4j only on workloads that make graph specialization meaningful, while allowing PM-01-admitted alternatives where they offer a materially distinct graph/read-projection proposition.

A graph projection remains secondary/rebuildable. It cannot become canonical truth because traversal is faster.

## Lane S

Compare structured/lexical S0 against bounded semantic/vector S1 where applicable. When PostgreSQL survives/is present, pgvector is the registered candidate; PM-01 may admit alternatives only with a concrete reason to incur another technology.

Vector quality must be measured after real scope/Visibility filtering.

## Lane E/D

Do not benchmark a named specialist by default. First create an admission record proving a concrete gap/benefit over bounded accepted mechanisms.

# PM-09 — Scoring + Sensitivity

Only candidates with applicable hard-gate/evidence status sufficient for honest comparison proceed to scoring. Any unresolved material hard-gate remains explicit and can block recommendation/selection.

Primary weighted dimensions remain the Phase-10 100-point model:

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

Every score requires evidence/rationale. A dimension may use disclosed external evidence where direct execution is not decision-relevant; do not fabricate measured values.

The 5-point cost/exit dimension must not be used to conceal material cost or lock-in differences. In addition to the numeric score, PM-09 must show direct-cost/TCO conditions and exit consequences explicitly whenever they could change the practical decision. A zero-cost candidate may win on practicality when quality is materially comparable; zero cost does not compensate for a hard-gate or major structural deficit.

Sensitivity must explicitly test whether ranking changes with:

- LOW/BASE/HIGH or equivalent evidence-backed scale bands;
- history depth;
- concurrency/read-write mix;
- deployment topology;
- stronger/weaker RPO/RTO assumptions;
- projection/search pressure;
- edition/license/cost constraints.

Ranking instability becomes `SENSITIVITY-DEPENDENT`.

# PM-10 — Recommendation

Produce a role-specific recommendation register using only:

```text
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
```

`PREFERRED` is a recommendation, not selection.

Required recommendation contents:

- evidence summary;
- hard-gate/evidence sufficiency result;
- direct execution coverage, if any, explicitly separate;
- weighted result where applicable;
- conditions;
- sensitivity;
- operational burden;
- direct/TCO cost posture where material;
- migration/exit risk;
- unresolved HOLD/finalist-proof items;
- why alternatives lost/were deferred.

If the technically strongest candidate is materially paid/proprietary, PM-10 must expose that fact rather than silently replacing it with a weaker free candidate. It must also identify credible lower-cost alternatives and whether a lower-cost starting architecture preserves a realistic future migration path.

# PM-11 — Explicit Selection Gate

No candidate is selected automatically.

Before changing any result to `SELECTED`, present a separate selection gate containing:

```text
candidate/role
exact subject version/edition/topology
evidence basis
direct execution coverage and unexecuted obligations
hard-gate result/conditions
score/sensitivity
material conditions
cost/TCO conditions where material
rejected/held alternatives
known downstream consequences
migration/exit consequences
new Physical authority paths to update
```

User approval is required.

# PM-12 — Accepted Physical Model

After explicit selection approval, produce the durable accepted Physical Model:

- selected role architecture;
- canonical persistence mapping;
- secondary lanes if selected;
- identity/reference mapping rules;
- transaction/concurrency rules;
- history/current/state-layer strategy;
- retention/redaction/recovery strategy;
- evolution/migration strategy;
- required deployment conditions;
- evidence caveats/sensitivity;
- direct execution coverage and any accepted residual conditions;
- material cost/licensing conditions;
- downstream implementation constraints;
- explicitly rejected alternatives and why.

Do not hide unresolved HOLD/finalist-proof items.

# PM-13 — Independent Clean-Room QA

A separate read-only-first audit must reconstruct the Physical result from repository truth without conversation memory and verify:

```text
Domain unchanged unless separately reopened
Logical unchanged unless separately reopened
Phase-5..10 constraints preserved
hard-gate/evidence claims traceable
direct execution never fabricated
score/recommendation reproducible
selection explicitly authorized
no production backend accidentally started
current docs coherent
```

Bounded repair gate follows if needed.

# PM-14 — Closure / Protected Main Integration

Only after PM-13 PASS:

```text
Physical workstream definitive closure
→ exact final compare
→ protected PR to main
→ merge commit
→ post-merge tree verification
→ current-truth alignment if required
→ Backend Foundation becomes eligible for separate authorization only if all its prerequisites are satisfied
```

Physical closure does not automatically start Backend Foundation.

## Stop conditions

Stop and re-gate immediately if:

- Domain/Logical contradiction appears;
- a new semantic owner/root seems necessary;
- a registered candidate requires weakening a hard gate;
- a new product/lane is proposed for benchmark admission beyond the authorized discovery/admission process;
- direct execution needs unapproved infrastructure/path scope;
- candidate capability evidence materially conflicts with the frozen subject;
- an admitted benchmark environment changes enough to affect comparability;
- a path outside the approved physical scope must be written;
- selection is about to be inferred from preference rather than explicitly authorized.