# Architecture Documentation

- Status: **Current navigation**
- Last updated: 2026-08-18

## Purpose

This directory separates **current architectural truth** from historical transition/validation evidence.

Current specifications describe the architecture as it is understood now. They are not chronological logs. Historical rationale and transition state remain recoverable through Git, ADRs, checkpoints and explicitly historical evidence.

## Current architecture sources

Read these for current architecture state:

1. [`pre-physical-architecture-baseline.md`](pre-physical-architecture-baseline.md) — closed/integrated Pre-Physical bridge, downstream constraints and authorization boundary;
2. [`requirements/README.md`](requirements/README.md) + all four Phase 5 requirement packages;
3. [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) — Phase 6 AI/context/runtime boundary contract, including consequential AI change evaluation/regression requirements;
4. [`integration-hub-boundaries.md`](integration-hub-boundaries.md) — Phase 6 Integration Hub/provider boundary contract;
5. [`durable-execution-benchmark.md`](durable-execution-benchmark.md) — Phase 7 durable-execution posture and conditional candidate ranking;
6. [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) — Phase 8 engine-/transport-neutral governed-operation/effect contract;
7. [`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md) — Phase 9 search, observability, calendar and solver pressure contract;
8. [`physical-benchmark-specification.md`](physical-benchmark-specification.md) — Phase 10 benchmark methodology;
9. [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md) — Phase 10 common scenario/destructive corpus;
10. [`physical-benchmark-register.md`](physical-benchmark-register.md) — Phase 10 candidate/role register; registered/preferred does not mean selected;
11. [`../development/repository-engineering-safety.md`](../development/repository-engineering-safety.md) — Phase 11 repository-safety contract and verified main-protection posture;
12. [`pre-physical-clean-room-qa.md`](pre-physical-clean-room-qa.md) — Phase 12 clean-room evidence;
13. [`pre-physical-final-coherence-audit.md`](pre-physical-final-coherence-audit.md) — final independent total-audit/closure evidence;
14. [`system-overview.md`](system-overview.md) — current logical/system boundary overview;
15. [`technical-decisions.md`](technical-decisions.md) — current technical directions and explicitly open choices;
16. [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md) — exact closed/integrated workstream record and integration checkpoints.

## Domain and Logical closure authority

The Domain and Logical Models are closed. Their canonical content/evidence is intentionally cumulative, so a historical status inside an earlier payload does not override a later explicit closure record.

For Domain current closure, do not stop at the early `README.md` / `README-part-2.md` / `README-part-3.md` payload. Read the closure/status continuations and final evidence:

- [`../domain/README.md`](../domain/README.md) — Domain Atlas entry payload;
- [`../domain/README-part-20.md`](../domain/README-part-20.md) — final corrected Domain Atlas status / closure activation;
- [`../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md) — final closure evidence;
- [`../domain/language-map.md`](../domain/language-map.md) — Language Map entry payload;
- [`../domain/language-map-part-22.md`](../domain/language-map-part-22.md) — final Whole-Domain language disposition.

Current Domain result:

```text
DOMAIN ATLAS / WHOLE-DOMAIN
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED
```

For Logical current closure, read both:

- [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md) — canonical Whole-Logical content payload;
- [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md) — separate closure activation / `LOGICAL MODEL CLOSED` evidence.

The complete `decision-and-assumption-register-v1*` logical chain remains a mandatory downstream Logical source.

A physically split/cumulative canonical document is **one logical document**. Never treat an isolated first path, newest continuation or `*-part-N` file as complete authority.

A size/tool-limit split is a lossless physical partition of a complete logical payload; it is not permission to summarize, condense, omit or silently change semantics.

## Phase 5 requirement package

Current Pre-Physical requirement owners are:

- [`requirements/authn-authz.md`](requirements/authn-authz.md);
- [`requirements/security-privacy-retention-recovery.md`](requirements/security-privacy-retention-recovery.md);
- [`requirements/consistency-side-effects.md`](requirements/consistency-side-effects.md);
- [`requirements/nonfunctional-multidevice-recovery.md`](requirements/nonfunctional-multidevice-recovery.md).

They define requirements and explicit open parameters. They do not select Auth providers, policy engines, databases, schemas, transaction mechanisms, workflow/queue/outbox technologies, offline-sync engines or arbitrary numeric RPO/RTO/SLA targets.

Phase 10 already consumed these requirements into the benchmark method. The later separately authorized Physical Model executes the applicable candidate evidence and resolves materially ranking-dependent open parameters.

## Phase 6 boundaries

Current AI/context/runtime categories remain distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration Hub modes remain distinct:

```text
canonical import
synchronized/mirrored provider state
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

Material consequential changes to AI model/version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion. Evaluation evidence is not canonical truth or authorization.

No AI provider/model, agent framework, MCP/A2A implementation, provider adapter or workflow engine is selected by Phase 6.

## Phase 7–9 contracts

### Durable execution

```text
bounded asynchronous work
→ DB/worker/outbox style remains a valid baseline class

material long-running/recoverable coordination
→ dedicated durable execution is structurally justified
```

Current dedicated candidates:

```text
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          SQLite-capable for local/bounded Python use
          PostgreSQL recommended for production
          distributed multi-server deployment PostgreSQL-coupled
```

### Governed operation/effect

Consequential operation meaning remains independent from route/UI/tool/AuthZ/workflow implementation. Request, runtime, canonical, provider and reconciliation result axes remain distinct.

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

## Phase 10 Physical benchmark method

Phase 10 defines **how** a later separately authorized Physical Model must be benchmarked. It does not choose a technology or create a Physical schema.

Current role-specific posture:

```text
PRIMARY CANONICAL
PostgreSQL hybrid — mandatory preferred baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / SEMANTIC RETRIEVAL
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first; specialized candidate only on demonstrated gap/benefit
```

Primary candidates must pass non-compensable semantic/correctness hard gates before weighted performance/operability scoring. LOW/BASE/HIGH values are synthetic qualification tiers, not business forecasts. Unexecuted upper envelopes remain unverified; progressive saturation/scaling evidence must be recorded honestly. Evidence is pinned to exact product version + edition/license + deployment mode. `PREFERRED != SELECTED`.

## Phase 11 repository engineering safety

Phase 11 is remotely QA-verified. The current owner-driven `main` ruleset requires pull-request integration, blocks deletion and non-fast-forward/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists and carries no required CI status checks until real stable checks exist.

Repository-safety documentation is not proof by itself; Phase 11 verified the effective remote rules. Security settings that the connector cannot read remain explicitly connector-unverifiable rather than fabricated as PASS.

## Phase 12 + independent total audit

Phase 12 clean-room QA is **QA PASS / CLOSED**.

The later independent total repository audit rechecked the full Pre-Physical delta against `main`, Domain/Logical closure, current architecture/requirements, repository safety, branch hygiene, knowledge-retention treatment and Physical/backend authorization boundaries.

It found no major semantic/architectural contradiction, Domain/Logical reopen need, material knowledge loss or accidental Physical/backend start. The bounded current-truth/factual/engineering repairs included:

- stale stage-handoff prose in current specifications;
- precise Phase 10 method vs future Physical execution wording;
- DBOS SQLite/PostgreSQL deployment-coupling correction;
- explicit consequential AI evaluation/regression requirement;
- final operating/navigation propagation;
- honest `unexecuted benchmark tier != VERIFIED-RUN` treatment.

The activation checkpoint `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d` proved the exact approved 23-path delta, `behind_by 0`, unchanged `main` and critical readback PASS.

PR #13 subsequently integrated the closed Pre-Physical workstream into protected `main` at merge commit `74593ae283ce5a1d22335502480ee3fa54be0436`. Post-merge verification proved the final branch tree and merged `main` tree differ by one merge commit and zero files. The source branch was auto-deleted.

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
Phase 10 benchmark method                CURRENT / QA PASS
Phase 11 repository engineering safety   QA PASS
Phase 12 clean-room QA                    QA PASS / CLOSED
Independent total audit                  PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED INTO MAIN VIA PR #13
POST-MERGE VERIFIED

Physical readiness
ESTABLISHED

Physical Model
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED / DEFERRED

Main integration
COMPLETE / POST-MERGE VERIFIED
```

Pre-Physical integration is complete. Physical authorization remains a separate new workstream decision; no Physical persistence/runtime/backend implementation may begin merely from readiness.

## Historical transition / validation evidence

The `domain-model-logical-readiness*` chain records truthful Domain → Logical transition history. It is evidence, not a current architecture specification. READY/HOLD/reopen/restoration chronology inside it is intentionally preserved.

## ADR handling

ADRs preserve rationale and explicit supersession/qualification. An older ADR may remain valuable evidence while no longer being current execution authority. Preferred benchmark candidates/methods do not justify an ADR claiming implementation selection.

## Documentation rule

```text
CURRENT SPECIFICATION
= current truth only

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology preserved

ADR
= decision rationale + explicit supersession/qualification

GIT / PR HISTORY
= recoverable change history
```

Before replacing/deleting a stale current document, prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```