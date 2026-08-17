# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 10 QA PASS; Phase 11 repository-engineering-safety read-only next**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Phase 2 PRE-SCOPE: `d9610a7da4fe8fc759e9809843d989f1befcda5c`
- Phase 2 content HEAD before closure markers: `dfc1f4e124f362d342c336485e166c8ac57afba4`
- Phase 3 PRE-SCOPE: `d2f190de06bf0e4e1e491c0c2dc601eb48668da9`
- Phase 3 content HEAD before closure marker: `50731dbee3d2cc661972700ef0bce521b67098c6`
- Phase 4 PRE-SCOPE: `46b963394e29179fadf20cb3b11c35dbf3b6edc2`
- Phase 4 content HEAD before closure markers: `d67cd83f462611b2cc6d341937432e705f7a8682`
- Phase 5 PRE-SCOPE: `e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f`
- Phase 5 content HEAD before global closure markers: `c29cfe4bde47d5df4f46507a5f1717acd1903112`
- Phase 5 propagation HEAD before handoff marker: `26882e376f1a6ad826d5aabfb4364f2a2ba30dd5`
- Phase 6 PRE-SCOPE: `40728080ae7a69703d40d14dd256a556516ccc58`
- Phase 6 content HEAD before global closure markers: `67d6a0d63ecaf39379912606dcf5113550718594`
- Phase 6 propagation HEAD before handoff marker: `5f9c2285f0de4a0f7c497ad36c12fae9b7548f1f`
- Coordinated Phase 7–9 PRE-SCOPE: `2cf77ea7e3d548147bbe2b0d87304b4d5393ff5f`
- Phase 7 checkpoint HEAD: `022131c2568c0375e74563e46a22c9347b277fc5`
- Phase 8 checkpoint HEAD: `1d92f9e77ecc808095086fc5497eaac88e2039fa`
- Phase 9 checkpoint HEAD: `95df2a17b1187a590b5cba646ba0e107c038e5d3`
- Phase 7–9 content HEAD before global closure markers: `4cbf50ec23ede3b02a49c75bc52fa57c3b192a6d`
- Phase 7–9 propagation HEAD before handoff marker: `d930ef5818df566a3bf9c5b2b36e9ba38e4e7b8a`
- Phase 10 PRE-SCOPE: `01df10a4267880a213ede8582b0193ff616f9a70`
- Phase 10 content HEAD before global closure markers: `057df9bdc19d89ea74fcee0e5d999ebc34cf93dc`
- Phase 10 propagation HEAD before this handoff marker: `0a9d80fa9d2ecaf373f0d5ad22b7953b73412a8c`
- Started: 2026-08-17
- Production backend code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Core Domain Model / Domain Atlas: **CLOSED / unchanged**
- Logical Model: **CLOSED / unchanged**

## Purpose

This workstream bridges the closed Domain + Logical Models and any later Physical Model authorization.

It makes repository/current architecture truth coherent, defines pre-Physical technical requirements and benchmark inputs, and will close with a clean-room QA before any Physical Model begins.

A genuine material semantic contradiction triggers a separate explicit Domain/Logical reopen. Cleanup or implementation convenience must not silently alter closed semantics.

## Current accepted stage

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL / DOMAIN ATLAS
CLOSED

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active

PRE-PHYSICAL COHERENCE
ACTIVE
Phase 0 PASS
Phase 1 QA PASS
Phase 2 QA PASS
Phase 3 QA PASS
Phase 4 QA PASS
Phase 5 QA PASS
Phase 6 QA PASS
Phase 7 QA PASS WITH CONDITIONAL RANKING
Phase 8 QA PASS
Phase 9 QA PASS
Phase 10 QA PASS

NEXT
Phase 11 — repository engineering safety
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

## Mandatory bootstrap

Before later work:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read `docs/development/operating-rules.md`;
6. read `docs/development/documentation-and-handoff.md`;
7. read `docs/development/branching-and-environments.md`;
8. read this complete handoff;
9. read `docs/architecture/README.md` and all current linked architecture sources;
10. read `docs/architecture/pre-physical-architecture-baseline.md`;
11. read `docs/architecture/requirements/README.md` + all four Phase 5 packages;
12. read `docs/architecture/ai-context-runtime-boundaries.md` and `docs/architecture/integration-hub-boundaries.md`;
13. read `docs/architecture/durable-execution-benchmark.md`;
14. read `docs/architecture/governed-operation-effect-contract.md`;
15. read `docs/architecture/search-observability-calendar-solver-boundaries.md`;
16. read `docs/architecture/physical-benchmark-specification.md`;
17. read `docs/architecture/physical-benchmark-scenario-corpus.md`;
18. read `docs/architecture/physical-benchmark-register.md`;
19. read complete canonical split/continuation chains where a logical document is physically split;
20. read relevant ADR/evidence/methodology;
21. verify current branch/ref and relation to `main`;
22. before any new write phase, issue a fresh exact PRE-SCOPE/write gate.

## Documentation lifecycle rule

Current specifications contain **current truth only**; they are not chronological design logs.

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

Before replacing/deleting stale current docs:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

The objective is clean current documentation **without losing useful knowledge**.

### Size/tool-limit split rule — mandatory

A physical split does not create separate logical authority. `*-part-N` continuation chains must be read as one complete logical document.

For size/tool-limit splitting specifically:

```text
ONE COMPLETE LOGICAL PAYLOAD
→ LOSSLESS PHYSICAL PARTITION
→ ONE COMPLETE LOGICAL PAYLOAD
```

A size/tool-limit split is **not** summarization, condensation, omission, paraphrase-as-compression or a hidden semantic cleanup.

If content needs semantic/current-truth revision, that is a separate content operation. Chronological/evidence continuation is distinct and may append genuine later evidence after the previous payload.

Never use “split” as permission to replace earlier complete content with a summary.

## Current architecture navigation

Current sources include:

- `docs/architecture/pre-physical-architecture-baseline.md`;
- `docs/architecture/requirements/README.md` + all four linked Phase 5 requirement packages;
- `docs/architecture/ai-context-runtime-boundaries.md`;
- `docs/architecture/integration-hub-boundaries.md`;
- `docs/architecture/durable-execution-benchmark.md`;
- `docs/architecture/governed-operation-effect-contract.md`;
- `docs/architecture/search-observability-calendar-solver-boundaries.md`;
- `docs/architecture/physical-benchmark-specification.md`;
- `docs/architecture/physical-benchmark-scenario-corpus.md`;
- `docs/architecture/physical-benchmark-register.md`;
- `docs/architecture/README.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- accepted complete Domain Atlas + Language Map logical documents;
- closed Whole Logical Model + complete decision/assumption-register logical document + remote closure;
- current ADR statuses;
- this workstream for still-open Pre-Physical obligations.

Historical `docs/architecture/domain-model-logical-readiness*` files remain transition/validation evidence and are not current architecture specifications.

## Non-negotiable Whole-Logical hardenings

Later architecture/Physical/runtime work must preserve:

- `WL-H01` — Agreement terms bind justified material owner/state;
- `WL-H02` — governed operation/effect contract;
- `WL-H03` — bounded projection/disclosure surface;
- `WL-H04` — absence/unknown is not universally false;
- `WL-H05` — expected-state semantics for consequential writes;
- `WL-H06` — idempotency is not semantic identity;
- `WL-H07` — truthful atomic/staged multi-owner consistency;
- `WL-H08` — canonical state != provider sync state;
- `WL-H09` — consequential derived-state use requires freshness/material basis;
- `WL-H10` — retention/redaction/tombstone integrity and non-reused identity;
- `WL-H11` — reconstructible consequential AuthZ provenance;
- `WL-H12` — selective disclosure includes non-interference/inference leakage.

Phase 5 requirement packages, Phase 6 boundary contracts, Phase 7–9 architecture contracts and the Phase 10 benchmark-method package add current downstream requirements without replacing these hardenings.

## Semantic non-reopen boundary

Do not create universal Domain owners merely because a product/runtime term is useful.

Unless separately revalidated, terms such as Memory, Agent, Automation, Job, Workflow, Notification, Reminder, Priority, Preference, Context, Task, Workspace, Risk, Focus Time, Out of Office and Working Location remain product/runtime/composition/profile/projection/policy concepts rather than new universal Domain roots.

Product labels such as `Project` and `Program` do not create kernel owners by naming alone; current Domain language maps them to accepted semantics such as a `Plan` profile according to the actual case.

Current high-risk invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical LifeOS state
derived projection != canonical truth
AI / solver inference != accepted canonical effect
runtime workflow completion != Actual automatically
technical cancellation != Domain cancellation automatically
search miss != canonical nonexistence
telemetry != Domain Provenance / audit automatically
preferred / registered benchmark candidate != selected technology
```

## Completed work

### Phase 0 — freeze/current-state inventory — PASS

The workstream opened from the integrated Domain+Logical baseline with Physical/backend implementation not started. A broader repository-wide clean-room audit remains part of Phase 12 closure.

### Phase 1 — global current-truth entry-point alignment — QA PASS

Original Phase 0+1 PRE-SCOPE:

`148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`

Phase 0+1 final HEAD:

`d9610a7da4fe8fc759e9809843d989f1befcda5c`

Verified physical classification:

```text
added      1
modified   7
deleted    0
unexpected 0
```

### Phase 2 — architecture supersession/current-truth cleanup — QA PASS

Approved Phase 2 PRE-SCOPE:

`d9610a7da4fe8fc759e9809843d989f1befcda5c`

Verified content HEAD:

`dfc1f4e124f362d342c336485e166c8ac57afba4`

Verified content delta:

```text
linear content commits 17
added                  1
modified              15
deleted                 1
unexpected              0
main changed            0
```

Architecture moved to current-truth specifications; Physical persistence remains benchmark-driven; PostgreSQL hybrid remains preferred baseline rather than mandate; TypeDB/Neo4j/event/document candidates remain bounded; generic universal meta-model is rejected; Python/FastAPI/Pydantic retained; SQLAlchemy/Alembic conditional.

The retired `docs/architecture/personal-data-ai-integration.md` passed knowledge coverage before deletion:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
retired file absent = PASS
historical evidence unchanged = PASS
Domain reopen = 0
Logical reopen = 0
```

### Phase 3 — Backend Foundation handoff cleanup — QA PASS

Approved Phase 3 PRE-SCOPE:

`d2f190de06bf0e4e1e491c0c2dc601eb48668da9`

Phase 3 content HEAD:

`50731dbee3d2cc661972700ef0bce521b67098c6`

The future Backend Foundation handoff is current but deferred. It consumes Domain + Logical rather than recreating them, treats SQLAlchemy/Alembic as Physical-dependent candidates, keeps PostgreSQL as benchmark posture rather than mandate, defers concrete API/Auth/workflow/provider mechanisms, removes the old fixed product-label slice as a canonical contract, and preserves valid future Python/FastAPI/Pydantic/modular-monolith/testing/provider-boundary requirements.

### Phase 4 — Current Pre-Physical Architecture Baseline — QA PASS

Phase 4 reconstructed current authority across complete split/continuation logical documents and established `docs/architecture/pre-physical-architecture-baseline.md` as the current bridge source.

Key rule:

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
```

Approved PRE-SCOPE:

`46b963394e29179fadf20cb3b11c35dbf3b6edc2`

Content HEAD:

`d67cd83f462611b2cc6d341937432e705f7a8682`

Remote Phase 4 path QA through the first closure marker:

```text
ahead_by       8
behind_by      0
total_commits  8
added           1
modified        7
deleted         0
unexpected      0
```

Domain and Logical semantics were not changed. No Physical/runtime implementation decision was introduced.

## Operational anomaly — accidental branch ref

During Phase 4 execution an incorrect tool invocation created an unrelated temporary branch ref:

```text
__no-op__
→ 46b963394e29179fadf20cb3b11c35dbf3b6edc2
```

It does **not** alter `chore/pre-physical-coherence`, `main` or project content. The available connector exposes no branch/ref deletion action, so this ref remains repository-hygiene cleanup for later. Do not use it as a work branch or source of truth.

### Phase 5 — requirements that can constrain Physical design — QA PASS

Phase 5 established four distinct requirement owners:

```text
AuthN / AuthZ
Security / Privacy / Retention / Security-aware Recovery
Consistency / Side Effects
Non-functional / Multi-device / Operational Recovery
```

Classification discipline:

```text
MUST / MUST NOT = accepted requirement
OPEN PARAMETER / OPEN DECISION = later required value/policy
DEFERRED MECHANISM = intentionally later implementation choice
```

Approved Phase 5 PRE-SCOPE:

`e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f`

Phase 5 content HEAD:

`c29cfe4bde47d5df4f46507a5f1717acd1903112`

Remote content QA:

```text
ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

Propagation HEAD before handoff marker:

`26882e376f1a6ad826d5aabfb4364f2a2ba30dd5`

Remote compare at propagation point:

```text
ahead_by       14
behind_by       0
total_commits   14
added            5
modified         9
deleted          0
unexpected       0
```

No numeric RPO/RTO/SLA/latency/scale/offline-duration targets, Auth mechanism, security mechanism, workflow mechanism or Physical persistence were invented/selected.

### Phase 6 — AI/context/runtime/integration boundaries — QA PASS

Phase 6 established:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

and Integration Hub modes:

```text
canonical import
synchronized/mirrored provider state
live federated read
retrieval/index projection
action/tool integration
```

Approved Phase 6 write gate:

```text
PRE-SCOPE
40728080ae7a69703d40d14dd256a556516ccc58

CREATE
docs/architecture/ai-context-runtime-boundaries.md
docs/architecture/integration-hub-boundaries.md
```

Phase 6 content HEAD:

`67d6a0d63ecaf39379912606dcf5113550718594`

Remote content QA:

```text
ahead_by        8
behind_by       0
total_commits    8
added             2
modified          6
deleted           0
unexpected        0
```

Propagation HEAD before handoff marker:

`5f9c2285f0de4a0f7c497ad36c12fae9b7548f1f`

Current Phase 6 invariants include:

```text
AI/context/runtime representation != canonical truth by default
model output != accepted canonical effect
tool invocation != governed operation
runtime Agent / Principal != Domain Actor automatically
ExternalRef != NativeRef
provider revision != MaterialStateRef by identity
provider state != canonical LifeOS state
```

No AI provider/model, agent framework, memory store, MCP/A2A implementation, workflow engine, provider adapter or tool schema was selected.

## Coordinated Phase 7–9 architecture tranche — QA PASS

### Tranche rule

Phases 7, 8 and 9 were executed as one coordinated outer tranche to reduce repeated navigation/status churn while preserving three strict internal acceptance checkpoints:

```text
PHASE 7
Durable workflow / async benchmark
        ↓ checkpoint QA
PHASE 8
Governed API / command / effect contract
        ↓ checkpoint QA
PHASE 9
Search / observability / calendar / solver pressure
        ↓ checkpoint QA
COMMON PROPAGATION
```

A failure/HOLD at one internal checkpoint would have stopped dependent work.

### Approved Phase 7–9 write gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
2cf77ea7e3d548147bbe2b0d87304b4d5393ff5f

CREATE
docs/architecture/durable-execution-benchmark.md
docs/architecture/governed-operation-effect-contract.md
docs/architecture/search-observability-calendar-solver-boundaries.md

UPDATE
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/workstreams/backend-foundation.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md

DELETE
none
```

### Phase 7 checkpoint

Created:

`docs/architecture/durable-execution-benchmark.md`

Checkpoint HEAD:

`022131c2568c0375e74563e46a22c9347b277fc5`

Remote checkpoint QA:

```text
ahead_by       1
behind_by      0
total_commits  1
added           1
modified        0
deleted         0
unexpected      0
```

Verdict:

```text
PHASE 7
PASS WITH CONDITIONAL RANKING

BOUNDED ASYNC BASELINE CLASS
PostgreSQL + worker/outbox style

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Current boundary:

```text
bounded background work
MAY use simple DB/worker/outbox style mechanism

material long-running/recoverable coordination
SHOULD use/benchmark dedicated durable execution
where operation-class requirements justify it
```

No runtime is selected/implemented. Durable execution does not create exactly-once external reality, and runtime completion/cancellation does not manufacture Domain Actual/Outcome/Confirmation/cancellation.

### Phase 8 checkpoint

Created:

`docs/architecture/governed-operation-effect-contract.md`

Checkpoint HEAD:

`1d92f9e77ecc808095086fc5497eaac88e2039fa`

Remote cumulative checkpoint QA from tranche PRE-SCOPE:

```text
ahead_by       2
behind_by      0
total_commits  2
added           2
modified        0
deleted         0
unexpected      0
```

Verdict:

```text
PHASE 8
PASS
```

Current consequential-operation contract preserves where applicable:

```text
contract/version
semantic target/facet
requested effect
input/candidate
purpose/context
material/expected state
derived/live basis + freshness
Principal / actual Actor / represented party
governance basis
autonomy / preview / confirmation
idempotency
correlation/causation
execution class
deadline/expiry/cancellation semantics
canonical result
provider result
runtime result
conflict/partial/reconciliation/provenance
```

Current hard non-collapse:

```text
HTTP route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect

request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

A single success/generic operation status cannot replace independent result axes. No concrete REST/RPC/GraphQL surface, route, DTO, command bus or runtime binding is selected.

### Phase 9 checkpoint

Created:

`docs/architecture/search-observability-calendar-solver-boundaries.md`

Checkpoint HEAD:

`95df2a17b1187a590b5cba646ba0e107c038e5d3`

Remote cumulative checkpoint QA from tranche PRE-SCOPE:

```text
ahead_by       3
behind_by      0
total_commits  3
added           3
modified        0
deleted         0
unexpected      0
```

Verdict:

```text
PHASE 9
PASS
```

Current posture:

```text
SEARCH
structured filters + lexical/full-text = BASELINE
semantic/vector retrieval = BOUNDED CANDIDATE
pgvector = BOUNDED if PostgreSQL survives Physical selection
dedicated search/vector service = NOT JUSTIFIED BY DEFAULT

OBSERVABILITY
OpenTelemetry-first / equivalent = CURRENT DIRECTION
vendor/backend = NOT SELECTED

CALENDAR
iCalendar / JSCalendar / provider APIs
= interoperability/adaptor pressure
!= LifeOS ontology

SOLVER
simple deterministic rules / heuristics = BASELINE
OR-Tools CP-SAT = PREFERRED SPECIALIZED BENCHMARK CANDIDATE — NOT implemented
```

Current non-collapse includes:

```text
search miss != canonical nonexistence
ranking / vector similarity != semantic truth
telemetry != Domain Provenance / security audit / material history automatically
provider calendar sync token / recurrence id != LifeOS MaterialStateRef / NativeRef by identity
solver UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

### Phase 7–9 content integration

After all three checkpoints passed, the three contracts were integrated into:

- `docs/architecture/README.md`;
- `docs/architecture/pre-physical-architecture-baseline.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- `docs/workstreams/backend-foundation.md`.

Content integration HEAD:

`4cbf50ec23ede3b02a49c75bc52fa57c3b192a6d`

Remote content QA from tranche PRE-SCOPE:

```text
ahead_by       8
behind_by      0
total_commits  8
added           3
modified        5
deleted         0
unexpected      0
```

### Phase 7–9 global propagation

After content QA passed, current state was propagated to:

- root `README.md`;
- `docs/README.md`;
- `docs/PROJECT-STATUS.md`;
- `docs/ROADMAP.md`.

Propagation HEAD before handoff marker:

`d930ef5818df566a3bf9c5b2b36e9ba38e4e7b8a`

Remote compare at propagation point:

```text
ahead_by       12
behind_by      0
total_commits  12
added           3
modified        9
deleted         0
unexpected      0
```

The only approved gated path not yet included at that point was this workstream save-game itself, intentionally written as the final closure marker.

### Phase 7–9 non-reopen / non-authorization result

```text
DOMAIN REOPEN REQUIRED              0
LOGICAL REOPEN REQUIRED             0
NEW DOMAIN OWNER REQUIRED           0
PHYSICAL MODEL SELECTED             0
DURABLE ENGINE SELECTED             0
CONCRETE API SELECTED               0
SEARCH ENGINE SELECTED              0
VECTOR DATABASE SELECTED            0
OBSERVABILITY VENDOR SELECTED       0
CALENDAR PROVIDER MODEL ADOPTED     0
SOLVER IMPLEMENTED                  0
BACKEND IMPLEMENTATION STARTED      0
ADR CHANGED                         0
```

Preferred benchmark candidate remains distinct from implementation selection.

## Phase 10 — Physical benchmark specification/register — QA PASS

### Purpose / non-authority

Phase 10 defines the **method** a later separately authorized Physical Model workstream must execute.

```text
PHASE 10
HOW TO BENCHMARK

!=

PHYSICAL MODEL
WHAT TO SELECT / DESIGN
```

Phase 10 did not create a Physical schema, benchmark harness implementation or database selection.

### Approved Phase 10 write gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
01df10a4267880a213ede8582b0193ff616f9a70

CREATE
docs/architecture/physical-benchmark-specification.md
docs/architecture/physical-benchmark-scenario-corpus.md
docs/architecture/physical-benchmark-register.md

UPDATE
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/workstreams/backend-foundation.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md

DELETE
none
```

### Phase 10 core package

Created as three distinct logical documents, with no size/tool split required:

1. `docs/architecture/physical-benchmark-specification.md`;
2. `docs/architecture/physical-benchmark-scenario-corpus.md`;
3. `docs/architecture/physical-benchmark-register.md`.

Core create HEAD:

`d4ff738b3e722b412ca5800b6cede2d86673d95c`

Remote core QA from Phase 10 PRE-SCOPE:

```text
ahead_by       3
behind_by      0
total_commits  3
added           3
modified        0
deleted         0
unexpected      0
```

### Phase 10 accepted benchmark method

#### Candidate competition by role

```text
PRIMARY CANONICAL PERSISTENCE
P0 PostgreSQL hybrid — mandatory preferred baseline, NOT selected
P1 TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH / TRAVERSAL
G0 no-specialized-store / primary-only baseline
G1 Neo4j — serious specialized secondary challenger

SEARCH / SEMANTIC RETRIEVAL
S0 structured + lexical/full-text baseline
S1 bounded pgvector where PostgreSQL is applicable

EVENT / DOCUMENT
bounded native mechanisms first
specialized product admitted only on explicit requirement gap / structural benefit
```

A candidate competes in the role it claims to fill. Neo4j cannot become primary merely by winning traversal benchmarks; pgvector cannot become semantic/canonical truth by winning retrieval benchmarks.

#### Hard-gate-first rule

Primary candidates must pass non-compensable hard gates for:

```text
HG-01 semantic ownership / no generic meta-model collapse
HG-02 reference-family integrity
HG-03 typed / n-ary relation fidelity
HG-04 expected-state consequential concurrency
HG-05 truthful multi-owner consistency
HG-06 history / correction / reconciliation reconstructibility
HG-07 state-layer separation
HG-08 governance / selective disclosure / WL-H12
HG-09 retention / redaction / tombstone / restore integrity
HG-10 temporal / recurrence / timezone fidelity
HG-11 schema/data evolution integrity
HG-12 recoverability / evidence quality
```

A hard-gate failure cannot be compensated by latency, throughput or operational familiarity.

Secondary/search candidates inherit applicable non-canonical-state, deletion/access-propagation, non-interference and freshness gates.

#### Fairness

The future Physical benchmark uses:

```text
SAME logical corpus
SAME semantic assertions
SAME operation/scenario semantics

+

IDIOMATIC candidate-specific Physical mapping
```

Do not force TypeDB into a relational imitation; do not force PostgreSQL into a universal edge/EAV shape; do not allow Neo4j/search/vector projections to redefine canonical truth.

#### Scenario corpus

The common corpus includes:

- all 57 Domain concepts and critical Logical representation/relationship/governance cases;
- deep personal history and efficient current-state access;
- population + hot-target concurrency;
- Authority/Consent/Visibility/Representation disclosure pressure;
- ExternalRef/provider divergence/reconciliation;
- recurrence, occurrence overrides, timezone/DST history;
- structured/full-text/vector retrieval with access filtering;
- backup/restore/deletion/redaction/evolution;
- expected-state races;
- idempotency conflicting reuse;
- atomic multi-owner mutation;
- provider unknown outcome and callback replay;
- revoked governance during delayed execution;
- stale LR-08 basis;
- offline multi-device divergence;
- search/index deletion/staleness;
- provider calendar sync-token invalidation;
- solver stale snapshot / UNKNOWN vs INFEASIBLE;
- crash between canonical and external effect;
- in-flight durable execution across version change;
- schema/mapping evolution with historical references;
- capacity/backpressure failure.

#### Synthetic qualification tiers

The scenario corpus defines LOW / BASE / HIGH qualification envelopes.

These values are explicitly:

```text
BENCHMARK ENVELOPES
!= BUSINESS / USER-GROWTH FORECASTS
```

They exist to make scale sensitivity reproducible until accepted product evidence exists.

Phase 5 open RPO/RTO/availability/latency/scale/offline values remain sensitivity dimensions rather than invented permanent targets.

If candidate preference changes materially across accepted scenarios, the future result is `SENSITIVITY-DEPENDENT`.

#### Evidence contract

Every future benchmark subject is pinned to:

```text
product
exact version
edition/license class
deployment mode/topology
driver/runtime version
```

Every run records source/benchmark commits, hardware/configuration, candidate mapping revision, deterministic fixture seed/tier, scenario IDs/load profile, correctness results, performance/resource evidence, backup/recovery/evolution evidence, manual tuning, caveats and raw artifact locations.

Materially contradictory/unstable capability evidence becomes `HOLD`/conditional until verified rather than receiving assumed points.

#### Result vocabulary

```text
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
```

`PREFERRED != SELECTED`.

Selection belongs only to the later separately authorized Physical Model workstream.

### Phase 10 current technical-evidence caveats

The Phase 10 register records current evidence areas that must be pinned/revalidated at execution time rather than treated as timeless claims.

Examples:

- TypeDB must be benchmarked as exact version + edition + deployment mode, especially where cluster/HA/backup maturity materially affects scoring;
- Neo4j must be benchmarked using the then-current schema/constraint capability and exact edition rather than an outdated “schemaless graph” assumption;
- pgvector ANN/search must be judged after actual scope/Visibility filtering and deletion/staleness pressure rather than unfiltered top-k latency alone.

These are benchmark questions/caveats, not candidate rejection or selection.

### Phase 10 content integration

The core package was integrated into:

- `docs/architecture/README.md`;
- `docs/architecture/pre-physical-architecture-baseline.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- `docs/workstreams/backend-foundation.md`.

Content HEAD:

`057df9bdc19d89ea74fcee0e5d999ebc34cf93dc`

Remote content QA from Phase 10 PRE-SCOPE:

```text
ahead_by       8
behind_by      0
total_commits  8
added           3
modified        5
deleted         0
unexpected      0
```

### Phase 10 global propagation

After content QA passed, current state was propagated to:

- root `README.md`;
- `docs/README.md`;
- `docs/PROJECT-STATUS.md`;
- `docs/ROADMAP.md`.

Propagation HEAD before this handoff marker:

`0a9d80fa9d2ecaf373f0d5ad22b7953b73412a8c`

Remote compare at propagation point:

```text
ahead_by       12
behind_by      0
total_commits  12
added           3
modified        9
deleted         0
unexpected      0
```

The only approved gated path not included at that point was this workstream save-game itself, intentionally written as the final closure marker.

### Phase 10 non-reopen / non-authorization result

```text
DOMAIN REOPEN REQUIRED                  0
LOGICAL REOPEN REQUIRED                 0
NEW DOMAIN OWNER REQUIRED               0
PHYSICAL MODEL SELECTED                 0
PHYSICAL SCHEMA DESIGNED                0
DATABASE SELECTED                       0
POSTGRESQL MAPPING IMPLEMENTED          0
TYPEDB MAPPING IMPLEMENTED              0
NEO4J PROJECTION IMPLEMENTED            0
PGVECTOR INDEX IMPLEMENTED              0
BENCHMARK HARNESS IMPLEMENTED           0
BACKEND IMPLEMENTATION STARTED          0
ADR CHANGED                             0
```

Phase 10 is method/acceptance preparation only.

## Current exact task — Phase 11 repository engineering safety read-only inventory

Next work is **read-only**. Do not write Phase 11 until a fresh exact gate is presented and approved.

Phase 11 owns repository engineering safety needed before future production backend/Physical implementation can be safely integrated.

The read-only inventory must determine at minimum:

1. current GitHub repository visibility/settings that materially affect controls;
2. current default branch and existing branch/ruleset protection state;
3. existing CI/workflows/check names, if any;
4. which checks can be mandatory **now** versus only after backend implementation exists;
5. pull-request/review requirements appropriate to the current project/team mode;
6. force-push/deletion/direct-push protection posture for `main`;
7. secret scanning / push protection / dependency/security update posture available to the repository;
8. test/lint/type/security check categories future backend work must provide before they can become required checks;
9. artifact/evidence retention expectations for important CI/benchmark runs;
10. release/tag/environment protections that are useful now versus premature;
11. branch naming/temporary branch cleanup and stale-branch hygiene;
12. how the accidental `__no-op__` ref should be removed without changing project truth;
13. whether repository settings require user-side/manual action because the connector cannot perform them;
14. exact Phase 11 output and acceptance conditions without inventing CI jobs or implementation that do not exist.

Phase 11 must not start backend code, Physical benchmark execution, schema design or deployment infrastructure.

## Remaining roadmap

### Phase 11 — repository engineering safety — NEXT

Read-only first. Produce the bounded safety/rules/checks plan and only write after a fresh exact gate.

### Phase 12 — clean-room QA and closure

Target:

```text
REPOSITORY / ARCHITECTURE COHERENCE PASS
DOMAIN UNCHANGED / CLOSED
LOGICAL UNCHANGED / CLOSED
PHYSICAL READY FOR SEPARATE AUTHORIZATION / NOT STARTED
```

Only after Phase 12 closure may the user separately decide whether to authorize a Physical Model workstream.

## Specialized infrastructure rule

Specialized infrastructure requires demonstrated benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Current application:

- dedicated durable execution is structurally justified for material long-running operation classes, but no engine is selected;
- dedicated search/vector infrastructure is not justified by default;
- OR-Tools CP-SAT is a preferred specialized solver benchmark candidate, not an implementation selection;
- Neo4j must beat a no-specialized-store graph/traversal baseline on net benefit before adoption;
- specialized event/document products are not shortlisted until a concrete gap/benefit admission trigger exists.

## Explicitly out of scope until separately gated

- Domain semantic changes;
- Logical semantic changes;
- Domain/Logical split rewriting;
- Physical Model or concrete schema;
- SQL/TypeQL/Cypher schema/query implementation;
- tables/keys/indexes/constraints/migrations;
- Physical benchmark execution/harness;
- concrete API/backend implementation;
- concrete Auth provider/runtime selection;
- Restate/Temporal/DBOS adoption;
- bounded worker/outbox implementation;
- AI provider/model/agent implementation;
- MCP/A2A adoption/implementation;
- provider adapters;
- dedicated search/vector deployment;
- observability vendor deployment;
- calendar provider implementation;
- solver implementation;
- frontend/prototype changes inside this workstream;
- direct modification of `main`.

## Exact continuation

```text
PHASE 7
QA PASS WITH CONDITIONAL RANKING

PHASE 8
QA PASS

PHASE 9
QA PASS

COORDINATED PHASE 7–9 TRANCHE
QA PASS

PHASE 10
QA PASS

CURRENT PHASE 10 SOURCES
docs/architecture/physical-benchmark-specification.md
docs/architecture/physical-benchmark-scenario-corpus.md
docs/architecture/physical-benchmark-register.md

NEXT
PHASE 11 — REPOSITORY ENGINEERING SAFETY
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

NO PHASE 11 WRITES YET
```
