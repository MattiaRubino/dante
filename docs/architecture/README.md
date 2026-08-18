# Architecture Documentation

- Status: **Current navigation**
- Last updated: 2026-08-18

## Purpose

This directory separates **current architectural truth** from historical transition/validation evidence.

Current specifications describe the architecture as it is understood now. They are not chronological logs. Historical rationale and transition state remain recoverable through Git, ADRs, checkpoints and explicitly historical evidence.

## Current architecture sources

Read these for current architecture state:

1. [`pre-physical-architecture-baseline.md`](pre-physical-architecture-baseline.md) — closed/integrated Pre-Physical bridge and downstream constraints;
2. [`requirements/README.md`](requirements/README.md) + all four Phase 5 requirement packages;
3. [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) — Phase 6 AI/context/runtime contract;
4. [`integration-hub-boundaries.md`](integration-hub-boundaries.md) — Phase 6 provider/integration contract;
5. [`durable-execution-benchmark.md`](durable-execution-benchmark.md) — Phase 7 durable-execution posture;
6. [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) — Phase 8 governed-operation/effect contract;
7. [`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md) — Phase 9 pressure contract;
8. [`physical-benchmark-specification.md`](physical-benchmark-specification.md) — Phase 10 benchmark methodology now consumed by the active Physical workstream;
9. [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md) — Phase 10 common corpus/scenarios;
10. [`physical-benchmark-register.md`](physical-benchmark-register.md) — Phase 10 candidate-role register; all execution slots remain `NOT RUN` at PM-00;
11. [`../physical-model/README.md`](../physical-model/README.md) — active Physical Model execution authority/index;
12. [`../physical-model/execution-methodology-v1.md`](../physical-model/execution-methodology-v1.md) — PM-00..PM-14 execution methodology;
13. [`../physical-model/acceptance-test-matrix-v1.md`](../physical-model/acceptance-test-matrix-v1.md) — executable hard-gate/corpus/scenario ledger;
14. [`../physical-model/result-register-v1.md`](../physical-model/result-register-v1.md) — current Physical result/disposition state;
15. [`../development/repository-engineering-safety.md`](../development/repository-engineering-safety.md) — repository-safety contract;
16. [`pre-physical-clean-room-qa.md`](pre-physical-clean-room-qa.md) — Phase 12 evidence;
17. [`pre-physical-final-coherence-audit.md`](pre-physical-final-coherence-audit.md) — independent Pre-Physical closure evidence;
18. [`system-overview.md`](system-overview.md) — current logical/system boundary overview;
19. [`technical-decisions.md`](technical-decisions.md) — current directions/open choices;
20. [`../workstreams/physical-model.md`](../workstreams/physical-model.md) — active Physical save-game;
21. [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md) — completed Pre-Physical workstream evidence.

## Domain and Logical closure authority

The Domain and Logical Models are closed. Their canonical content/evidence is intentionally cumulative, so a historical status inside an earlier payload does not override a later explicit closure record.

For Domain current closure, do not stop at the early payload. Read:

- [`../domain/README.md`](../domain/README.md);
- [`../domain/README-part-20.md`](../domain/README-part-20.md);
- [`../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`../domain/language-map.md`](../domain/language-map.md) + [`../domain/language-map-part-22.md`](../domain/language-map-part-22.md).

Current Domain result:

```text
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED
```

For Logical closure read both:

- [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md);
- complete `decision-and-assumption-register-v1*` chain;
- [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md).

A physically split/cumulative canonical document is **one logical document**. A size/tool-limit split is a lossless physical partition, never permission to summarize/omit/change semantics.

## Phase 5 requirement package

Current requirement owners are:

- [`requirements/authn-authz.md`](requirements/authn-authz.md);
- [`requirements/security-privacy-retention-recovery.md`](requirements/security-privacy-retention-recovery.md);
- [`requirements/consistency-side-effects.md`](requirements/consistency-side-effects.md);
- [`requirements/nonfunctional-multidevice-recovery.md`](requirements/nonfunctional-multidevice-recovery.md).

They define requirements/open parameters, not provider/database/schema/workflow/offline-engine selection or invented numeric targets.

Phase 10 already converted their pressure into benchmark method. The active Physical Model now executes applicable evidence and may resolve ranking-dependent parameters only through explicit evidence/selection gates.

## Phase 6 boundaries

Keep distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration modes remain distinct:

```text
canonical import
sync/mirror
live federated read
retrieval/index projection
action/tool integration
```

```text
AI/model/tool/runtime representation != canonical truth/effect by default
provider state != canonical LifeOS state
runtime Agent / Principal != Domain Actor automatically
ExternalRef != NativeRef
```

Material consequential AI changes require versioned/reproducible evaluation before promotion. Eval evidence is not canonical truth/authorization.

## Phase 7–9 contracts

### Durable execution

```text
bounded asynchronous work
→ DB/worker/outbox class valid baseline

material long-running/recoverable coordination
→ dedicated durable execution structurally justified

Restate   preferred candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          local/bounded Python SQLite-capable
          production PostgreSQL-recommended
          distributed multi-server PostgreSQL-coupled
```

### Governed operation/effect

Consequential meaning remains independent from route/UI/tool/AuthZ/workflow implementation. Request/runtime/canonical/provider/reconciliation axes remain distinct.

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text baseline
semantic/vector bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider models = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred specialized benchmark candidate — NOT implemented
```

## Phase 10 method + active Physical execution

Phase 10 defines **how** Physical candidates must be benchmarked. The now-authorized Physical workstream executes that method; it does not rewrite it.

Current roles:

```text
PRIMARY CANONICAL
PostgreSQL hybrid — mandatory preferred baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
G0 no-specialized-store baseline vs G1 Neo4j

SEARCH / SEMANTIC RETRIEVAL
S0 structured + lexical/full-text vs S1 bounded pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first; specialist only on demonstrated gap/benefit
```

Primary candidates must pass non-compensable hard gates before weighted scoring. LOW/BASE/HIGH are synthetic qualification tiers, not forecasts. Unexecuted upper envelopes remain unverified. Evidence is pinned to exact product + version + edition/license + deployment mode. `PREFERRED != SELECTED`.

Physical bootstrap adds execution discipline in `docs/physical-model/**`:

```text
PM-00 bootstrap
PM-01 current candidate/environment freeze — READ-ONLY FIRST
PM-02 mapping design
PM-03 hard-gate preflight
PM-04 harness/fixture design
PM-05 correctness/destructive execution
PM-06 performance/tiers
PM-07 recovery/evolution/failure
PM-08 secondary lanes
PM-09 scoring/sensitivity
PM-10 recommendation
PM-11 explicit selection gate
PM-12 accepted Physical Model
PM-13 clean-room QA
PM-14 closure/main integration
```

## Phase 11 repository engineering safety

Phase 11 is QA-verified. Current `main` policy requires PR integration, blocks deletion/non-fast-forward, requires review-thread resolution, uses zero approvals while no independent reviewer exists and no required CI checks until stable real contexts exist.

The active Physical branch must remain bounded; benchmark evidence paths/checks do not become required `main` checks automatically.

## Phase 12 + independent total audit

Phase 12 clean-room QA and the independent total audit passed. They found no Domain/Logical reopen need, major knowledge loss, accidental Physical/backend start or hidden technology selection. Pre-Physical was integrated via PR #13 and current-truth aligned via PR #14.

## Current stage boundary

```text
Product / North Star                      CURRENT
Domain Model / Domain Atlas              CLOSED
Logical Model                            CLOSED
Phase 5 requirements                     CURRENT
Phase 6 boundaries                       CURRENT
Phase 7 durable-execution contract       CURRENT
Phase 8 governed-effect contract         CURRENT
Phase 9 pressure contract                CURRENT
Phase 10 benchmark method                CURRENT / QA PASS / ACTIVE INPUT
Phase 11 repository engineering safety   QA PASS
Phase 12 clean-room QA                    QA PASS / CLOSED
Pre-Physical Coherence                   CLOSED / INTEGRATED / VERIFIED

Physical Model
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
branch feature/physical-model
base main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79
mapping NOT STARTED
benchmark NOT STARTED
selection NONE

Backend production implementation
NOT STARTED / DEFERRED
```

After PM-00 QA the exact next step is **PM-01 READ-ONLY candidate/version/edition/deployment/environment freeze**. No mapping/schema/harness write is authorized until a fresh gate.

## Historical transition / validation evidence

The `domain-model-logical-readiness*` chain records truthful Domain → Logical transition history. It is evidence, not current architecture authority.

## ADR handling

ADRs preserve rationale and explicit supersession/qualification. Preferred benchmark candidates/methods do not justify an ADR claiming implementation selection.

## Documentation rule

```text
CURRENT SPECIFICATION = current truth only
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
ADR = rationale + explicit supersession/qualification
GIT / PR HISTORY = recoverable history
```

Before replacing/deleting stale current documentation prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```