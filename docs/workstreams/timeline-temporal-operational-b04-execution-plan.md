# Timeline / Temporal-Operational — B04 Temporal Constraints + Movement Policy Execution Plan

- **Status:** PRE-SCOPE COMPLETE / EXECUTION PLAN FROZEN — B04-A NEXT
- **Date:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Previous block:** B03 Event Core ✅ CLOSED / PROVEN
- **Candidate DB authority entering B04:** PostgreSQL 18.6 / Alembic `20260917_29`
- **Candidate topology entering B04:** `101|5|31|78|198|119|297|0|0|0`
- **Primary Domain authority:** `docs/domain/concepts/temporal-constraint.md` + canonical continuation `temporal-constraint-part-2.md`
- **Logical authority:** `docs/logical-model/slices/time-reality-v1.md` + validation checkpoint
- **Physical authority:** accepted PostgreSQL Physical Model + explicit owner-specific typed relational LR-05 mapping
- **Detailed capability freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`
- **Live map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **CI:** not implicitly authorized

B04 activates Temporal Constraint truth and the first bounded Movement Policy capability without collapsing either into Schedule, Actual, Availability or future solver semantics.

---

# 0. Binding semantic boundary

Canonical separation:

```text
Temporal Constraint
= rule restricting or preferring placement, duration or temporal relation

Schedule
= current accepted temporal assignment

Movement Policy
= bounded rule governing who/what may alter accepted placement and under which authority path

Actual
= truthful realization/reality
```

Therefore:

```text
Temporal Constraint != Schedule
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
Temporal Constraint != Availability / Capacity
Temporal Constraint != Dependency
Movement Policy != solver result
Movement Policy != Authority itself
proposal != accepted effect
constraint revision != Schedule revision
hard planning violation != impossible reality
passing deadline != Outcome
```

Identical temporal geometry does not establish identical semantics.

---

# 1. Authority reopening result

## 1.1 Domain

Temporal Constraint v0 is already accepted and sufficiently strong for implementation. B04 must preserve:

- multiple simultaneous constraints;
- typed constrained facet/relation;
- hard vs soft semantics;
- lower/upper boundaries;
- explicit window relationship semantics;
- duration/spacing/relative families;
- exact temporal anchoring/precision without false precision;
- constraint revision/history distinct from Schedule history;
- narrower exception distinct from base-rule revision;
- truthful Actual even when reality violates a hard planning rule;
- AI proposal/inference distinct from accepted/authoritative constraint.

Deadline is a latest-bound specialization, not a separate kernel root. A raw window is only a shape; its semantics come from typed context.

## 1.2 Logical

The accepted Time/Reality logical model classifies Temporal Constraint as **LR-05 rule/policy definition**.

Logical invariants relevant to B04 include:

```text
Schedule != Recurrence != Temporal Constraint != Session != Actual
geometry != semantic meaning
hard planning constraint may be violated by Actual
```

No universal `TemporalEvent`, generic rule root or lifecycle status collapse is authorized.

## 1.3 Physical

The accepted PostgreSQL mapping requires LR-05 rules/specifications to use **owner-specific structured relational representation** and explicitly rejects a universal `Rule(type,payload)` root / generic JSON escape.

Material consequential revisions must use stable semantic preconditions/current-state control rather than last-write-wins timestamps.

## 1.4 Current candidate database gap

At `_29` the Dictionary contains no canonical Temporal Constraint table family. Existing `scoped_address` is currently bounded to `schedule | actual`, and MaterialState facets do not yet include Temporal Constraint.

Therefore:

```text
B04 forward DDL is REQUIRED
```

The first materialized constraint family must extend existing bounded address/current/material-state infrastructure rather than create a parallel versioning engine.

---

# 2. Existing frontend state is prototype intent, not canonical truth

The Create model already contains prototype fields such as:

```text
constraintKind:
  none | open | bounded-window | deadline | preferred-window

movementPolicy:
  locked | window | confirm | free

window / earliest / deadline / preferred values
fallback policy
```

Current runtime deliberately fails closed when non-baseline constraint intent is submitted. This is correct pre-B04 behavior.

B04 must **not** serialize that whole object as canonical JSON merely because the UI already has it.

The UI vocabulary can be reused only where it maps losslessly to the accepted Domain model.

---

# 3. B04 implementation strategy

B04 is split into six bounded slices.

```text
B04-A  Temporal Constraint canonical core
B04-B  Boundary / Deadline constraints
B04-C  Window / preference evaluation + explanation
B04-D  Movement Policy
B04-E  Advanced-family applicability + integration hardening
B04-F  Whole-B04 closure
```

Each slice must preserve B00–B03 regressions and update the live ledger in the same change.

---

# 4. B04-A — Temporal Constraint canonical core

## Goal

Establish stable canonical identity, subject ownership, MaterialState/current/history, idempotent mutation and read semantics for Temporal Constraint before activating individual rule families.

## Required design

A material independently revisable constraint is a bounded dependent/rule record, **not a new LR-01 NativeRef root**.

The implementation should reuse the existing scoped/material control pattern by extending it deliberately for Temporal Constraint rather than inventing a second history mechanism.

Expected bounded shape, subject to exact migration proof:

```text
temporal_constraint
  constraint_ref              stable ScopedRecordRef-style identity
  subject_native_ref          currently accepted subject union

scoped_address
  add temporal_constraint family

material_state_address
  add temporal_constraint.rule facet

scoped_current_material_state
  add temporal_constraint.rule facet

temporal_constraint_state
  material_state_ref
  constraint_ref
  family/kind
  strength
  constrained facet/relation

constraint current-history
operation/idempotency receipts
```

The exact table names are implementation detail, but the semantic ownership is fixed.

## Initial subject union

B04-A must support the currently active schedulable native owners without a generic Entity shortcut:

```text
Activity | Event
```

Future Plan/Routine/Occurrence scope extension must be possible through explicit typed eligibility when those owners become active; do not pretend they are implemented now.

## B04-A operations

At minimum:

```text
CreateConstraint
GetConstraint
ListEffective/CurrentConstraintsForSubject
ReviseConstraint with expected MaterialStateRef
Remove/retire current constraint through explicit governed operation
idempotent replay + changed-intent collision
self-Person scope
```

“Remove” must preserve reconstructible material history where the prior rule mattered; no destructive rewrite.

## B04-A proof

- typed identity/reference tests;
- real PostgreSQL create/read/current/history;
- stale expected-state conflict;
- operation-id replay/collision;
- Activity/Event self-scope isolation;
- no generic JSON rule payload;
- downgrade guard where canonical B04 state would otherwise be discarded;
- Dictionary / SQLAlchemy / Alembic / current-catalog reconciliation.

---

# 5. B04-B — Boundary / Deadline constraints

## Goal

Activate the first high-value constraint families using typed temporal boundaries.

Required families:

```text
earliest-start
latest-start
latest-completion / delivery Deadline
```

Do not model these as one generic `due_at`.

## Constrained facet

The canonical state must say **what temporal fact is constrained**.

Initial B04 facets should be bounded to semantics we can evaluate against current Schedule truth without inventing B08/B10 reality:

```text
schedule.start
schedule.completion
```

Product vocabulary may say “deadline”, but canonical state remains an explicit latest-bound constraint on a facet.

Future `actual.*`, arrival/delivery specialist facts or related-owner anchors are not silently manufactured.

## Boundary temporal forms

Constraint boundaries must preserve meaning/precision. The implementation must support only forms it can represent and evaluate truthfully, with an extension seam for the rest.

No conversion such as:

```text
date-only -> 00:00 UTC
floating local -> device-zone instant
named-zone source -> fixed UTC-only intent
```

is allowed.

The exact first supported boundary form matrix is frozen during B04-B implementation after reuse analysis of the Schedule temporal-value machinery; unsupported forms fail closed.

## Deadline semantics

Passing the boundary may derive `past deadline`; it must **not** establish `missed`, `failed`, `not completed` or another Outcome.

## B04-B proof

- earliest-start acceptance/rejection;
- latest-start acceptance/rejection;
- latest-completion acceptance/rejection;
- hard/soft validation where applicable;
- precision/zone/date semantics;
- deadline passage `!= Outcome`;
- constraint revision independent from Schedule revision.

---

# 6. B04-C — Window / preference evaluation + explanation

## Goal

Activate range-shaped constraint semantics without treating every range alike.

Initial range families:

```text
hard validity window
soft preferred window
```

## Explicit relationship semantics

A range must specify the required relationship, for example:

```text
start-within
completion-within
full-placement-contained
placement-overlaps
```

No bare `min_at/max_at` semantics.

Boundary inclusion/exclusion must be explicit in canonical state or fixed by a documented family contract; it must not be accidental PostgreSQL operator behavior.

## Evaluation

B04-C introduces a deterministic evaluation boundary over:

```text
current/proposed Schedule placement
+
current effective Temporal Constraints
```

Result must distinguish:

```text
admissible
inadmissible due to hard constraint(s)
admissible with soft preference violation(s)
not evaluable / unsupported
```

Violation/explanation is derived state by default, not duplicated foundational truth.

## Infeasibility

A set of hard constraints that cannot all be satisfied is `INFEASIBLE` for planning. B04 must not silently ignore one rule to manufacture a complete-looking plan.

B12 owns the broad optimizer/solver. B04 only provides typed rules, deterministic evaluation and explanation sufficient to protect mutations and future solver input.

## B04-C proof

- same geometry / different semantics tests;
- hard validity rejection;
- soft preference trade-off/explanation;
- simultaneous-constraint composition;
- infeasible hard set surfaced honestly;
- no stored universal `overdue/invalid` flag;
- frontend explanation uses backend/canonical evaluation truth.

---

# 7. B04-D — Movement Policy

## Goal

Activate movement governance separately from Temporal Constraint.

Canonical distinction:

```text
constraint -> where/when placement is valid/preferred
movement policy -> what class of actor/automation may alter an accepted placement and through which acceptance path
Authority -> whether the acting context is legitimately empowered for that bounded effect
```

B04-D must not claim to implement the entire future multi-actor Authority model.

For the current self-Person product slice, the first policy can be bounded to self-governed scheduling behavior while retaining an extension seam for later Authority/Participation work.

## Current product vocabulary review

The prototype choices:

```text
locked
window
confirm
free
```

are **inputs to review**, not automatically the kernel enum.

The B04-D state model must answer operational questions such as:

```text
may this accepted Schedule move automatically?
may it move only when the resulting placement remains hard-admissible?
is explicit user confirmation required?
is the placement locked against automatic movement?
```

It must not encode future solver scope, fallback strategy or multi-actor grants into one opaque enum.

## Enforcement boundary

All real Schedule revisions performed through B04-enabled product paths must respect the current Movement Policy and hard Temporal Constraint evaluation before canonical Schedule mutation.

Manual/explicit user override must be modeled as an explicit authorized action/change path, not as silent hard-rule violation.

## B04-D proof

- locked policy blocks automation;
- confirmation-required path remains proposal/pending until accepted;
- authorized self auto-move path can commit only an admissible placement;
- same Constraint + different Movement Policy produce different mutation authority behavior;
- Movement Policy revision != Schedule revision;
- stale-state/idempotency behavior preserved.

---

# 8. B04-E — Advanced-family applicability + integration hardening

B04's frozen map also names duration, contiguous-session, spacing/recovery and relative constraints. These must be handled through explicit applicability gates, not fake checkmarks.

## TC-008 minimum/maximum duration

Can be activated in B04 where the constrained facet is **planned Schedule placement duration** and semantics are independent of future Session/Actual truth.

It must remain distinct from estimated Activity effort.

## TC-009 minimum contiguous Session duration

Runtime enforcement depends on B08 Session ownership. B04 may establish the semantic/type seam if useful, but must not claim runtime Session enforcement before B08 exists.

Closure disposition may be:

```text
applicability gate satisfied / runtime deferred to B08
```

with explicit reopening trigger and test ownership.

## TC-010 spacing/recovery

When the anchor is previous Session/Actual/Occurrence, exact runtime evaluation depends on later B06/B08/B10 state. Do not create fake “last time” timestamps on Activity/Event.

Only activate a B04 subset if it can be expressed against already canonical anchors without semantic compromise; otherwise close the applicability gate with later owner/reopening trigger.

## TC-011 relative-before/after

Relative geometry is canonical Temporal Constraint semantics, but exact heterogeneous relation/reference persistence must not be improvised as `related_id + type` or JSON.

Activate only the bounded subset whose reference contract can be represented safely with existing ReferenceAddress machinery. Otherwise preserve the typed extension seam and transfer exact runtime activation to the appropriate relation/owner block.

## Fallback/replanning prototype fields

Current frontend fallback choices are not automatically B04 canonical truth. Broad replanning/fallback/solver semantics belong primarily to B12 unless a narrow B04 movement rule specifically requires one.

---

# 9. B04-F — Whole-B04 closure

B04 closure requires all applicable slices plus explicit disposition of every frozen-map item.

Required evidence:

```text
B04 typed/domain validation
real PostgreSQL migration/current/history/CAS/idempotency
Schedule integration and Activity/Event regression
hard vs soft evaluation
Deadline passage != Outcome
Movement Policy enforcement
frontend Create/edit/read explanation paths actually backed by backend truth
real-stack browser proof for accepted product slice
manual userTest constraint/explanation/movement acceptance
broad affected backend/frontend regressions
Dictionary / SQLAlchemy / Alembic / OpenAPI/client reconciliation
map / roadmap / handoff / closure record reconciliation
```

No PASS may be recorded from prototype-only fields.

---

# 10. Explicit stop lines

B04 must not silently implement:

```text
B05 Calendar/Life Area/Tags organization
B05 postponed/TBD Event rediscovery UI beyond transferred requirement
B06 Recurrence/Occurrence generation
B08 Session runtime
B09 multi-actor Participation semantics
B10 Actual/Outcome/Confirmation
B11 advanced conditional/reminder policy
B12 optimizer/solver/replan engine
B13 provider synchronization
```

A hard constraint violated by future Actual remains recordable reality.

A solver candidate remains derived proposal, not Schedule.

---

# 11. Frozen B04 capability ledger

```text
TC-001  Re-open Temporal Constraint authority                           ✅ PRE-SCOPE PROVEN
TC-002  First typed persistence/runtime; no due_at/JSON escape          ⬜ B04-A
TC-003  Earliest-start                                                   ⬜ B04-B
TC-004  Latest-start                                                     ⬜ B04-B
TC-005  Latest-completion/delivery Deadline + explicit facet             ⬜ B04-B
TC-006  Hard validity window                                             ⬜ B04-C
TC-007  Preferred/soft window                                            ⬜ B04-C
TC-008  Min/max duration where applicable                                ⬜ B04-E
TC-009  Min contiguous Session duration applicability                    ⬜ B04-E / B08 runtime
TC-010  Spacing/recovery applicability                                   ⬜ B04-E / later-anchor runtime
TC-011  Relative-before/after applicability                              ⬜ B04-E
TC-012  Movement Policy separate from Temporal Constraint                ⬜ B04-D
TC-013  Hard planning violation does not block truthful Actual           ⬜ B04 semantic/proof + B10 runtime continuation
TC-014  Hard/soft conflict explanation                                   ⬜ B04-C

B04-T01 typed validation                                                  ⬜
B04-T02 persistence/direct PostgreSQL                                    ⬜
B04-T03 hard vs soft placement behavior                                  ⬜
B04-T04 deadline passage != Outcome                                      ⬜
B04-T05 manual constraint/explanation acceptance                         ⬜
```

---

# 12. B04-A start checklist

Before writing migration code:

1. inventory the existing scoped/material/current/history constraints and triggers at `_29`;
2. decide the exact `TemporalConstraintRef` representation under the accepted Reference Contract;
3. define the minimal Activity/Event subject eligibility check;
4. define the first material state envelope without a generic rule JSON payload;
5. define create/revise/remove operation receipts and fingerprints;
6. define downgrade fail-closed behavior;
7. define Dictionary/SQLAlchemy topology delta;
8. write migration + direct PostgreSQL proof together;
9. only then expose application/API/frontend paths.

The first implementation target is **B04-A Temporal Constraint canonical core**.