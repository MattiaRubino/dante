# Pre-Physical Architecture Baseline

- Status: **CURRENT CONSTRAINT BASELINE — PRE-PHYSICAL DEFINITIVE CLOSED / FINAL QA PASS / INTEGRATED**
- Activation checkpoint: `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`
- Main integration checkpoint: `74593ae283ce5a1d22335502480ee3fa54be0436` via PR #13 — **POST-MERGE VERIFIED**
- Post-merge alignment / Physical base: `3de84bb49f9cef30e88e9bde4961ed84335daa79` via PR #14
- Physical handoff snapshot in this document: **AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP** at the time of Pre-Physical closure
- Current Physical truth: **CLOSED / SELECTED / ACCEPTED / integrated via PR #15**
- Backend production implementation: **NOT STARTED / DEFERRED**

> **Current-truth qualification:** this file remains authoritative for the accepted **Pre-Physical constraints and handoff rationale**. Statements below that describe `Physical Model AUTHORIZED / IN PROGRESS`, `Technology selection NONE`, `feature/physical-model` or candidate preferences are preserved as the truthful **handoff-time snapshot** and are superseded for current selection/status by PM-11, PM-12, PM-13, the Physical workstream handoff and `docs/PROJECT-STATUS.md`.
>
> **Naming continuity:** `DANTE` is the current product/app name. `LifeOS` references retained in this Pre-Physical record reflect the previous working/project name for the same product lineage.

## Purpose

This is the closed/current bridge from the accepted Product/North Star, CLOSED Domain Atlas and CLOSED Logical Model into Physical/runtime/API/backend work.

It consolidates downstream constraints. The completed Physical Model consumed this baseline; later implementation must not rewrite these constraints by implementation convenience.

It does not replace the detailed Domain/Logical sources, ADRs, Phase 5 requirement packages, Phase 6 boundary contracts, Phase 7–9 architecture contracts, Phase 10 benchmark package, Phase 11 repository-safety contract, Phase 12 clean-room evidence or final independent audit evidence.

## Authority

Read current truth through:

1. Product / North Star;
2. complete Domain Atlas + Language Map cumulative authority and final closure evidence;
3. CLOSED Whole Logical Model + complete decision/assumption-register chain + remote closure evidence;
4. current ADR statuses;
5. all four Phase 5 requirement packages;
6. Phase 6 AI/context/runtime and Integration Hub contracts;
7. Phase 7 durable-execution contract/evidence;
8. Phase 8 governed-operation/effect contract;
9. Phase 9 search/observability/calendar/solver contract;
10. Phase 10 Physical benchmark specification + scenario corpus + register;
11. Phase 11 repository-engineering-safety contract + effective main rules;
12. Phase 12 clean-room evidence;
13. final independent audit evidence;
14. PR #13 / merge commit `74593ae283ce5a1d22335502480ee3fa54be0436` post-merge verification;
15. PR #14 / `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79` current-truth alignment;
16. this baseline for Pre-Physical constraints and handoff-time evidence;
17. PM-11/12/13 plus current `docs/physical-model/**`, `docs/workstreams/physical-model.md` and `docs/PROJECT-STATUS.md` for current selected Physical truth.

A physical split/cumulative continuation is one logical document. Size/tool-limit splitting is lossless physical partitioning, not summarization or semantic cleanup.

## Decided != authorized != selected

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
PREFERRED BENCHMARK CANDIDATE != TECHNOLOGY SELECTION
REGISTERED BENCHMARK CANDIDATE != TECHNOLOGY SELECTION
ACCEPTED REQUIREMENT != IMPLEMENTATION MECHANISM SELECTION
ACCEPTED BOUNDARY CONTRACT != PROVIDER / RUNTIME / PROTOCOL SELECTION
BENCHMARK METHOD ACCEPTED != PHYSICAL TECHNOLOGY SELECTED
PHYSICAL WORKSTREAM AUTHORIZED != PHYSICAL RESULT ACCEPTED
BENCHMARK PASS != PRODUCTION BACKEND AUTHORIZATION
```

## Pre-Physical closure / Physical-handoff snapshot

The following block records the state **at Pre-Physical closure and Physical authorization**. It is not the current PM-11/12 selection status.

```text
Product / North Star        CURRENT
Domain Atlas                CLOSED
Logical Model               CLOSED
Phase 5 requirements        CURRENT
Phase 6 boundaries          CURRENT
Phase 7 benchmark           CURRENT
Phase 8 effect contract     CURRENT
Phase 9 pressure contract   CURRENT
Phase 10 benchmark method   CURRENT / QA PASS / ACTIVE INPUT
Phase 11 repository safety  QA PASS
Phase 12 clean-room QA      QA PASS / CLOSED
Independent total audit     PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

Physical readiness          ESTABLISHED
Physical Model              AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
Physical mapping            NOT STARTED
Benchmark execution         NOT STARTED
Technology selection        NONE
Backend Foundation          NOT STARTED / DEFERRED
```

Historical Physical branch at handoff: `feature/physical-model`.
Bootstrap base/PRE-SCOPE: `3de84bb49f9cef30e88e9bde4961ed84335daa79`.

### Current resolution after the completed Physical workstream

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED VIA PR #15

CANONICAL PRIMARY
PostgreSQL 18.4

DURABLE CLASS-B
Restate runtime selected

SEARCH / VECTOR
PostgreSQL FTS + pg_trgm + unaccent + pgvector

SOLVER
OR-Tools 9.15 CP-SAT

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED / DIRECT HG PASS 0

NEXT
Development Profile v0
```

## Technical direction at Pre-Physical closure

The following direction is retained as the Pre-Physical input snapshot. Later PM-11/12 selections resolve the candidate-only statements without weakening the constraints.

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Modular monolith first.
- Domain/application logic remains independent from HTTP/framework handling.
- Clients use governed backend contracts, not direct canonical persistence.
- Object/file storage remains behind a provider abstraction.
- AI remains behind replaceable/provider-neutral boundaries and a bounded Context Builder.
- Material consequential AI behavior changes are promotion-gated by versioned/reproducible evaluation.
- Provider state remains distinct from canonical LifeOS state.
- Consequential operations use an engine-/transport-neutral governed operation/effect contract.
- Bounded async work and material long-running durable execution are distinct runtime classes.
- Restate remains preferred dedicated durable candidate; Temporal remains the strongest mandatory challenger; DBOS remains conditional with deployment-dependent PostgreSQL coupling.
- Structured + lexical/full-text search is baseline; semantic/vector retrieval is bounded.
- OpenTelemetry-first or equivalent is current observability direction, not a vendor selection at this snapshot.
- Calendar standards/providers are adapter pressure, not ontology authority.
- Deterministic rules/heuristics remain solver baseline; OR-Tools CP-SAT is a preferred specialized benchmark candidate at this snapshot.
- Physical candidate comparison is role-specific; correctness hard gates precede performance/operability scoring.
- Unknown NFR/business-scale values remain explicit sensitivity/scenario inputs rather than invented forecasts.
- Unexecuted benchmark envelopes cannot be reported as verified runs.
- Specialized infrastructure requires demonstrated structural or measured benefit.
- SQLAlchemy/Alembic remain conditional on the accepted Physical design.

## Semantic guardrails

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Actor / Subject / Resource = contextual roles/capabilities, not universal native owners
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Responsibility != Participation != Coordination Stewardship
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical state
derived projection != canonical truth
AI / solver inference != accepted canonical effect
```

Hard rejects for canonical kernel meaning:

```text
universal Entity / Thing
universal generic Relationship / edge
generic EAV / property-bag ontology
generic unresolved-AI semantic fallback
provider schema/identifier as ontology or native identity
product/UI vocabulary as ontology authority
```

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
PRODUCT LABEL != ONTOLOGY ROOT
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
```

## Logical representation and state separation

The closed Logical Model preserves `LR-01..LR-13` and discriminated references including:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

State categories remain distinct where applicable:

```text
canonical state
material history / lineage / correction
derived/effective projection
provider/external state
unresolved/candidate interpretation
security/AuthZ/runtime state
```

Phase 6 context further distinguishes retrieved context, live external context and transient LLM working context.

## Mandatory WL-H01..WL-H12

All Physical and later implementation work must preserve:

1. Agreement terms bind justified owner/facet/material state; no universal Terms root.
2. Consequential work uses a governed operation/effect contract; route/UI/AuthZ strings are not canonical effects.
3. Projection/disclosure surfaces remain bounded by source/facet/derivation/version/purpose/exposure/disclosure.
4. Absence/unknown != false.
5. Consequential writes preserve expected-state semantics.
6. Idempotency != identity; conflicting key/equivalence reuse rejects.
7. Multi-owner changes are atomic where required or explicitly staged/partial with reconciliation/compensation.
8. Canonical LifeOS state != provider sync state.
9. Consequential derived/live-state use revalidates freshness or binds material basis/snapshot.
10. Retention/redaction/tombstone handling preserves integrity; native identity is not reused.
11. Consequential authorization/effect provenance can reconstruct Actor, represented party, Principal/security context, governance basis and effect.
12. Non-interference/inference leakage includes existence, counts, ranking, errors, timing, free-busy, candidates, explanations and aggregates.

## Phase 5 requirement envelope

### AuthN/AuthZ

Preserve `Person != Account != Principal != Actor`, Authority distinct from AuthZ decision, actual Actor vs represented party, non-human Principal governance, delayed revalidation and reconstructible consequential provenance.

### Security/privacy/retention/recovery

Support purpose-aware minimization, secret/sensitive-data handling, category-sensitive retention, truthful deletion/redaction/tombstones, deletion propagation and secure recovery without forbidden-data resurrection.

### Consistency/side effects

Preserve expected-state semantics, idempotency distinct from identity, no silent material last-write-wins, truthful multi-owner atomic/staged behavior, provider/canonical separation, ambiguous-failure safety and effect/reconciliation provenance.

### NFR/multi-device/recovery

Preserve device divergence, operation-specific offline semantics, truthful degraded/provider state, current-state access alongside long history, temporal/DST semantics, recovery testing and explicit later RPO/RTO/latency/availability/scale targets where material.

Phase 10 defines method/scenarios; the completed Physical workstream consumed them for the accepted decision.

## AI/context/runtime boundary

```text
AI/context/runtime representation != canonical truth by default
model output != accepted canonical effect
tool invocation != governed operation
runtime Agent / Principal != Domain Actor automatically
```

LifeOS does not create a second generic AI-memory truth store.

Before promoting materially consequential changes to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy, the applicable behavior must pass versioned/reproducible evaluation.

Minimum pressure includes structured output, false canonical claims, candidate/canonical classification, tool errors, governance bypass, privacy/inference leakage, stale context, substitution regression, fallback/refusal, approval flows and material cost/latency.

```text
eval result != canonical truth
eval PASS != Authority / governed-effect authorization
```

Concrete eval tooling/thresholds remain later decisions.

## Integration Hub boundary

Five modes remain explicit:

```text
canonical import
synchronized / mirrored provider state
live federated read
retrieval / index projection
action / tool integration
```

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider outcome != canonical LifeOS effect truth automatically. MCP/A2A/future protocols remain adapters.

## Durable execution posture at Pre-Physical closure

```text
BOUNDED ASYNC
DB + worker/outbox style remains a valid baseline class

MATERIAL DURABLE
Restate   preferred structural-fit candidate — NOT selected at this snapshot
Temporal  strongest mandatory challenger — NOT selected at this snapshot
DBOS      conditional challenger — NOT selected at this snapshot
          SQLite-capable local/bounded Python use
          PostgreSQL recommended for production
          distributed multi-server PostgreSQL-coupled
```

Current PM-11/12 resolution: Restate is selected for material Class-B durable execution; deployment remains profile-dependent between first-class self-hosted and allowed Cloud EU.

No runtime creates exactly-once external reality by itself. Runtime completion/cancellation does not manufacture Domain realization/cancellation.

## Governed operation/effect contract

Consequential operations preserve by materiality target/effect, expected state, purpose/context, derived/live basis + freshness, Principal/Actor/represented party, governance, confirmation/autonomy, idempotency/equivalence, correlation/causation, execution class, expiry/cancellation semantics and independent canonical/provider/runtime/reconciliation results.

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
runtime cancellation != Domain cancellation automatically
workflow completed != Actual automatically
```

## Search / observability / calendar / solver

- Search: structured + lexical/full-text baseline; semantic/vector bounded; search miss != nonexistence; index != truth.
- Observability: OpenTelemetry-first/equivalent; telemetry != Domain Provenance/audit automatically.
- Calendar: standards/providers are interoperability pressure; provider token != `MaterialStateRef`; recurrence/DST/override semantics remain LifeOS-owned.
- Solver: deterministic rules/heuristics baseline; OR-Tools CP-SAT preferred candidate at this snapshot; `UNKNOWN != INFEASIBLE`; solver result crosses governed effect before canonical change.

Current PM-11/12 resolution selects PostgreSQL FTS + `pg_trgm` + `unaccent`, pgvector, OpenTelemetry + Grafana Alloy/Grafana Cloud EU target and OR-Tools 9.15 CP-SAT while preserving the contract above.

## Physical benchmark posture at handoff

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected at this snapshot
TypeDB            — mandatory challenger, NOT selected at this snapshot

SECONDARY GRAPH
G0 no-specialized-store baseline vs G1 Neo4j

SEARCH / VECTOR
S0 structured + lexical/full-text baseline vs S1 bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first; specialized only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Hard correctness gates precede weighted scoring. Candidate mappings may be idiomatic but must satisfy common semantic assertions. LOW/BASE/HIGH are synthetic envelopes, not forecasts. Unexecuted tiers remain unverified. Evidence is pinned to exact product/version/edition/deployment. `PREFERRED != SELECTED`.

The completed Physical workstream applied the execution rules under `docs/physical-model/**`: evidence-before-claim, PM-00..PM-14 progression, exact subject pinning, explicit PM-11 selection gate and independent PM-13 clean-room QA.

## Repository engineering safety at handoff

Phase 11 is QA PASS. Effective `main` protection was verified remotely. Current owner-driven posture requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists, has no required status checks until real stable contexts exist and auto-deletes merged head branches.

The historical `feature/physical-model` branch was bounded, later merged through PR #15 and auto-deleted. Benchmark-only code/evidence does not automatically become production infrastructure or required CI.

## Definitive Pre-Physical closure and integration evidence

Phase 12 clean-room QA is closed. The independent total audit found no major semantic/architectural contradiction, Domain/Logical reopen need, material knowledge loss or accidental Physical/backend start.

The final repairs were activated at `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`; protected PR #13 integrated the final tree at `74593ae283ce5a1d22335502480ee3fa54be0436`; PR #14 aligned current truth at `3de84bb49f9cef30e88e9bde4961ed84335daa79`.

Therefore Pre-Physical Coherence is **DEFINITIVE CLOSED / FINAL QA PASS / INTEGRATED / POST-MERGE VERIFIED** and is an input to, not an open task inside, later Physical/backend work.

## Explicitly unauthorized at the PM-00 handoff snapshot

The following block is retained as historical authorization evidence for the start of the Physical workstream. It does not describe the current closed Physical status.

```text
candidate Physical schema/tables/keys/indexes/constraints
SQL / TypeQL / Cypher implementation
benchmark harness/fixture-generator code
database/container deployment
technology selection
production migrations
concrete API routes/DTOs
Auth implementation
runtime adoption
provider adapters
AI provider/model/agent framework
dedicated search/vector deployment
observability vendor
solver implementation
production backend code
feature/backend-foundation
```

Those items required later exact Physical/Backend gates as applicable. Domain/Logical changes still require a separate explicit reopen gate.

## Current next boundary

The handoff-time `PM-00 BOOTSTRAP` next step is complete historical evidence. Current truth is:

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED VIA PR #15

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED / DIRECT HG PASS 0

BACKEND FOUNDATION
NOT STARTED / DEFERRED

NEXT
Development Profile v0
```
