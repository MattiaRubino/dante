<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1.md" -->
> **Canonical continuation of `decision-and-assumption-register-v1.md`.** This physical file is Part 2 of the same logical register. Earlier decisions/assumptions remain preserved; this continuation appends Slice-C Time / Reality decisions, alternatives, assumptions, evidence and physical deferrals.

# 2026-08-17 — Slice C Time / Reality decision register

## 26. Slice C — accepted decisions

### DEC-C01 — Layered Typed Time & Reality Model

```text
SLICE / SCOPE
C — Time / Reality

QUESTION
How can LifeOS represent repeated expectation, instance identity, accepted placement, actual execution and result without a universal calendar/timeline/status object?

SELECTED CANDIDATE
Layered Typed Time & Reality Model

CORE SHAPE
typed temporal value semantics
+
typed Recurrence rules
+
stable Occurrence / Session identity
+
dependent Schedule / Actual / Outcome records where material
+
material history/state references
+
provider mappings
+
derived comparison/projection state

STATUS
ACCEPTED WITH HARDENING — activation conditional on exact Slice-C remote QA

REGRESSION IMPACT
R3 WHOLE-LOGICAL
```

### DEC-C02 — typed temporal value semantics; no UTC-only logical model

```text
DECISION
The logical layer preserves materially distinct temporal interpretations including date-only, floating local wall-clock, named-zone wall-clock, absolute instant, range/interval, duration, precision/granularity and period-frame semantics.

RULE
Operational resolution to UTC/instants may occur later, but original semantic interpretation must remain reconstructible.

DST gap/overlap resolution must not silently promote a library/parser default into canonical user intent when consequence matters.

STATUS
ACCEPTED WITH PHYSICAL POLICY DEFERRAL
```

### DEC-C03 — Recurrence is LR-05 with multiple semantic families

```text
DECISION
Recurrence uses typed LR-05 rule/policy semantics and must preserve at least:
- calendar/wall-clock
- elapsed interval
- quota per period
- completion-relative
- anchor-stream-relative
- cyclic positional

One future engine/DSL may implement several families only if the family-specific anchors/frames/behavior remain explicit and testable.

STATUS
ACCEPTED
```

### DEC-C04 — Occurrence identity survives lazy materialization

```text
DECISION
Occurrence is stable semantic identity for one expected generated instance.
When persistent independent addressability/history is required, Occurrence is LR-01 and uses NativeRef.
Future derivable instances need not be eagerly materialized.

RULE
materialization/addressability != creation of a different semantic Occurrence

STATUS
ACCEPTED WITH PHYSICAL ID/locator PROOF OBLIGATION
```

### DEC-C05 — no generic VirtualRef address family

```text
DECISION
Virtual/lazy recurrence does not justify a universal `VirtualRef` ReferenceAddress variant.
Before persistent addressability, a bounded occurrence locator/generation context under the governing source/material state may identify derivation.
When persistent addressability is required, the same semantic Occurrence uses NativeRef.

MECHANISM RESULT
ReferenceAddress RETAIN + HARDEN

STATUS
ACCEPTED
```

### DEC-C06 — Schedule is LR-02 accepted placement, and absence is valid

```text
DECISION
Schedule is a dependent semantic record for current accepted temporal assignment.
Stable addressability may use ScopedRecordRef where material.
A subject may have zero or multiple current accepted placements depending on semantics.
No synthetic UNSCHEDULED temporal record is required.

STATUS
ACCEPTED
```

### DEC-C07 — Schedule history is material state, not Actual overwrite

```text
DECISION
Prior/current accepted Schedule placements remain reconstructible where material.
Actual execution does not overwrite planned Schedule.
Explicit in-execution expectation revision is a Schedule revision; mere overrun/early start is Actual deviation.

STATUS
ACCEPTED WITH Slice-D Version/history dependency
```

### DEC-C08 — Session is LR-01 actual execution episode

```text
DECISION
Session has stable independent identity across ordinary timestamp correction/provider reconciliation.
Pause/resume normally remains one Session; explicit end/restart normally forms another execution episode unless correction establishes otherwise.
Session may exist without prior Schedule or Activity.

STATUS
ACCEPTED WITH Slice-D correction-lineage dependency
```

### DEC-C09 — Actual is contextual realization; unknown remains valid

```text
DECISION
Actual is LR-06 contextual realization and may use LR-02/ScopedRecordRef when material history/reference is needed.
Actual is not a universal reality root.

CANONICAL BARRIER
no established Actual != known non-realization

Time passage, Schedule expiry and provider silence do not establish completion/failure/miss/non-execution.

STATUS
ACCEPTED WITH Slice-D Provenance/Reconciliation dependency
```

### DEC-C10 — Outcome is contextual/optional; no universal result enum

```text
DECISION
Outcome is optional contextual result/disposition of an Actual realization.
No universal result/status enum is canonical across domains.
Operational lifecycle state remains separate.

STATUS
ACCEPTED
```

### DEC-C11 — Temporal Constraint remains typed LR-05 rule and reality may violate it

```text
DECISION
Temporal Constraint preserves the temporal facet/relationship/strength that gives a time geometry meaning.
Identical intervals may represent different semantics.
A hard planning constraint defines planning admissibility but does not make contradictory truthful Actual unrecordable.

STATUS
ACCEPTED
```

### DEC-C12 — Conditional Policy remains distinct from Recurrence and effect

```text
DECISION
Conditional Policy is LR-05 bounded response semantics.
Time/Recurrence/Schedule may form part of activation basis, but activation does not become Recurrence/Schedule/Actual and does not imply downstream effect success.

STATUS
ACCEPTED
```

### DEC-C13 — provider recurrence identity remains external

```text
DECISION
Provider series/instance/original-start/current-start IDs and markers remain ExternalRef/source state.
They may map/reconcile to LifeOS Occurrence/Schedule but do not define canonical LifeOS identity.

Lossless provider export is not a kernel invariant.

STATUS
ACCEPTED
```

### DEC-C14 — current-state access must not require lifetime replay

```text
DECISION
Historical reconstructibility and current-state queryability must coexist.
The logical contract does not mandate global event sourcing or application-memory replay of full lifetime history to answer current Schedule/Session/Actual state.

STATUS
ACCEPTED WITH Physical Model proof obligation
```

---

## 27. Slice C — rejected / retained alternatives

### ALT-C01 — Universal TemporalEvent / TimelineRecord

```text
WHY PLAUSIBLE
one timeline, one polymorphic search surface, uniform start/end/status/parent handling

FAILURE
false semantic root;
Occurrence/Schedule/Session/Actual/Outcome/Constraint collapse into kind/status/metadata;
same temporal geometry loses meaning;
provider/calendar schema pressure becomes ontology.

CLASS
LOGICALLY REJECTED

RETEST
only as derived/read-model projection; not canonical ontology unless Domain Atlas is legitimately reopened
```

### ALT-C02 — fully owner-specific timestamps and temporal tables

```text
WHY PLAUSIBLE
maximum local FK/type specificity; simple physical schemas for narrow owners

RESULT
VIABLE STRONG ALTERNATIVE / PHYSICAL INGREDIENT

WHY NOT COMPLETE LOGICAL BASELINE
repeats temporal interpretation/recurrence/revision/provider/history mechanisms across owners;
direct overwritable timestamps encourage history loss;
high-value cross-domain planned-vs-actual queries become ad hoc.

RETEST
Physical Model may use this heavily if all Slice-C contracts remain intact
```

### ALT-C03 — universal append-only temporal/event-sourced ledger

```text
WHY PLAUSIBLE
excellent chronology/audit and rebuildability

FAILURE AS UNIVERSAL LOGICAL REQUIREMENT
technical event stream becomes semantic pressure;
current state still needs typed owners/projections;
simple cases over-modeled;
current queries risk lifetime replay dependence.

CLASS
REJECTED AS UNIVERSAL LOGICAL REQUIREMENT

RETEST
bounded physical event sourcing remains permitted where measured value justifies it
```

### ALT-C04 — external calendar / RFC recurrence model as kernel

```text
WHY PLAUSIBLE
mature recurrence/instance exception/time-zone semantics and broad interoperability

FAILURE
calendar-set orientation is not sufficient for quota, completion-relative, anchor-stream and some cyclic recurrence;
external original datetime cannot universally define LifeOS occurrence identity.

CLASS
LOGICALLY REJECTED AS KERNEL

RETAINED USE
adapter/interoperability/benchmark evidence
```

### ALT-C05 — new generic VirtualRef for lazy future instances

```text
WHY PLAUSIBLE
uniform address for objects not yet physically materialized

FAILURE
derivation/materialization state is not a semantic identity family;
would pressure computed candidates into one universal referential ontology;
ReferenceAddress + bounded generation context already preserves required distinction.

CLASS
REJECTED

RETEST
only if a later concrete requirement proves an independently stable cross-context reference must exist before Occurrence becomes persistently addressable and cannot be represented without a new bounded address variant
```

---

## 28. Slice C — assumptions / proof obligations

### ASM-C01 — lazy Occurrence materialization can preserve same semantic identity

```text
STATEMENT
A physical implementation can derive future Occurrences lazily and later persist/address them without changing which semantic Occurrence the derivation referred to.

CONFIDENCE
HIGH logical plausibility

STABILITY
EVOLVING until Physical Model proof

EVIDENCE
accepted Domain virtual-occurrence contract; recurring-instance external patterns; bounded scheduling-horizon products

FAILURE CONSEQUENCE
reopen Slice-C reference/materialization mechanism under LM-WF-21; Domain reopen only if every feasible logical representation contradicts accepted semantics

REFRESH TRIGGER
Physical Model start / concrete recurrence engine design / WD-05 discharge

STATUS
ACCEPTED WITH PHYSICAL PROOF OBLIGATION
```

### ASM-C02 — Slice D can preserve temporal material-state/history bindings

```text
STATEMENT
Slice D can provide Version/Provenance/Reconciliation mechanisms sufficient for governing source state, Schedule revision history, Session correction lineage and Actual/Outcome assertion correction without collapsing their owners.

CONFIDENCE
HIGH

STABILITY
STABLE logical requirement / mechanism deferred

FAILURE CONSEQUENCE
targeted C+D logical reopen, not automatic Domain reopen

REFRESH TRIGGER
Slice D

STATUS
ACCEPTED WITH LATER-SLICE PROOF OBLIGATION
```

### ASM-C03 — timezone/DST rule evolution can remain representation-safe

```text
STATEMENT
LifeOS can preserve enough original temporal interpretation/zone/basis metadata that later physical/runtime time-zone rules do not require pretending a previously accepted wall-clock intention was merely a UTC instant.

CONFIDENCE
HIGH principle / implementation strategy open

STABILITY
IANA/runtime rules evolve; semantic principle stable

FAILURE CONSEQUENCE
physical temporal-state hardening; targeted Slice-C reopen only if original intent cannot be reconstructed

REFRESH TRIGGER
Physical Model temporal type/serialization choice; provider/time-zone adapter work

STATUS
ACCEPTED WITH PHYSICAL DEFERRAL
```

### ASM-C04 — current-state materialization can coexist with full historical audit

```text
STATEMENT
Current Schedule/Session/Actual state can be queried directly while material history remains reconstructible without forcing universal event-sourcing replay.

CONFIDENCE
HIGH

STABILITY
STABLE architectural principle

FAILURE CONSEQUENCE
reconsider history/material-state implementation options, not Domain semantics automatically

REFRESH TRIGGER
Slice D and Physical Model

STATUS
ACCEPTED WITH PHYSICAL PROOF OBLIGATION
```

No Slice-C PASS depends on a material assumption classified as `UNPROVEN` without an explicit later-stage proof obligation.

---

## 29. Slice C — external evidence register

```text
EVID-C01 RFC 5545 iCalendar temporal/recurrence instance semantics       STANDARD / STRUCTURAL PRINCIPLE
EVID-C02 Google Calendar recurring originalStartTime                    CURRENT PRODUCT / INSTANCE-ID PRESSURE
EVID-C03 Microsoft Graph pattern/range recurrence                       CURRENT PRODUCT / STRUCTURAL PRINCIPLE
EVID-C04 Todoist scheduled-date vs completion-date recurrence           CURRENT PRODUCT / ANCHOR PRESSURE
EVID-C05 Reclaim Habit recurrence vs conflict/movement behavior         CURRENT PRODUCT / BOUNDED HORIZON
EVID-C06 Motion task constraints vs dynamic schedule blocks             CURRENT PRODUCT / PLAN-SCHEDULE SEPARATION
EVID-C07 Android Health Connect planned vs completed exercise           SPECIALIST / PLAN-ACTUAL SEPARATION
EVID-C08 Apple HealthKit workout Session pause/resume                    SPECIALIST / SESSION LIFECYCLE
EVID-C09 HL7 FHIR Appointment vs Encounter                              SPECIALIST / PLAN-ACTUAL SEPARATION
EVID-C10 PostgreSQL date/time/interval/DST semantics                    INFRASTRUCTURE / PHYSICAL FEASIBILITY
EVID-C11 Reclaim legacy elapsed-event completion pressure               NEGATIVE BENCHMARK
```

Canonical source URLs/dispositions: `benchmarks/time-reality-v1.md`.

All current vendor behaviors were verified from official documentation on 2026-08-17 and are freshness-scoped. No logical PASS depends materially on one vendor implementation detail.

---

## 30. Slice C — physical deferrals

```text
DEFER-C01 exact PostgreSQL temporal column/type strategy
DEFER-C02 exact timezone-database/version metadata strategy
DEFER-C03 DST gap/overlap runtime resolution policy representation
DEFER-C04 recurrence DSL/library/expansion implementation
DEFER-C05 occurrence locator / native-key issuance algorithm
DEFER-C06 virtual-occurrence materialization horizon/cache
DEFER-C07 exact Schedule record/placement table/cardinality strategy
DEFER-C08 exact Session pause/segment storage
DEFER-C09 exact Actual/Outcome table/value split
DEFER-C10 exact Version/Provenance/Reconciliation history model — Slice D
DEFER-C11 provider recurrence adapter schemas and controlled degradation
DEFER-C12 query/index/partition strategy
DEFER-C13 event sourcing usage, if any
DEFER-C14 API serialization for date/floating/zoned/coarse time values
DEFER-C15 runtime scheduler/replanner/optimizer
DEFER-C16 runtime policy/Authority enforcement
```

All remain stage-deferred. None may weaken INV-101..130.

---

## 31. Slice C — mechanism/technology reconsideration

### TECH-C-A — owner-specific references only

```text
RESULT
strong physical ingredient, still logically viable

NOT SELECTED AS SOLE LOGICAL CONTRACT
cross-owner address/state semantics would repeatedly reconstruct the same union/reference mechanisms
```

### TECH-C-B — global Node / TemporalObject registry

```text
RESULT
rejected as logical baseline

WHY
uniform addressability does not solve temporal semantics and creates false root/ontology pressure
```

### TECH-C-C — generic VirtualRef

```text
RESULT
rejected

WHY
lazy derivation/materialization is not an independent semantic address space
```

### TECH-C-D — ReferenceAddress + bounded occurrence locator/generation context

```text
RESULT
SELECTED

RULE
pre-persistent derivation can be located by governing source/material-state + bounded generation context;
persistently addressable Occurrence uses NativeRef for the same semantic instance.

TECHNOLOGY / MECHANISM VERDICT
RETAIN + HARDEN
```

The previous A+B mechanism receives no incumbency credit; it was re-compared because Slice C changed the constraint surface.

---

## 32. Slice-C decision state

```text
SLICE C LOCAL DECISIONS
ACCEPTED WITH HARDENING

REFERENCE MECHANISM
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED
0

NEW DOMAIN OWNER REQUIRED
0

LOGICAL STRUCTURAL BLOCKER
0

ACTIVATION
conditional on exact remote write QA

NEXT REQUIRED SEMANTIC STEP AFTER QA
Integrated A+B+C cumulative checkpoint

SLICE D
HOLD until cumulative checkpoint passes
```
