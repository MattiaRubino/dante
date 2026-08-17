<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1.md" -->
> **Canonical continuation of `representation-framework-v1.md`.** This physical file is Part 2 of the same logical document. The base file remains unchanged; this continuation records the accepted Slice-C Time / Reality contract and supersedes broader wording only where explicitly stated.

# 2026-08-17 — Slice C Time / Reality representation contract

## 17. Layered Typed Time & Reality Model

Slice C selects the **Layered Typed Time & Reality Model** as the current logical representation baseline.

This is a representation strategy, not a new Domain superclass.

```text
Time / Reality model
!= TemporalEvent root
!= TimelineItem root
!= universal Event log ontology
!= generic status model
```

Canonical semantic layers remain:

```text
source / recurring owner
!= Recurrence
!= Occurrence
!= Schedule
!= Session
!= Actual
!= Outcome
!= Temporal Constraint
!= Conditional Policy
```

---

## 17.1 Temporal value semantics — LR-04

Slice C hardens LR-04 with a reusable typed temporal-value family.

Where materially relevant the logical representation must preserve distinctions among:

```text
civil date / date-only
floating local wall-clock
named-zone wall-clock
absolute instant
interval/range geometry
duration / elapsed quantity
precision / granularity
period frame
```

These are representation/value semantics, not independent Domain owners.

A later physical model may encode several of them using shared database types, but physical normalization must not erase the originating semantic interpretation.

### No UTC-only logical contract

```text
08:00 Europe/Rome
!= 08:00 floating wherever user is
!= one absolute UTC instant
!= every 24 elapsed hours
```

The logical model therefore preserves enough information to reconstruct the intended interpretation before resolving to operational instants.

### DST resolution

Named-zone wall-clock values may be ambiguous or nonexistent at DST transitions. A consequential resolution must retain an explicit applicable policy/basis rather than silently adopting a library default as canonical intent.

Exact runtime resolution is stage-deferred.

---

## 17.2 Recurrence — LR-05

Recurrence is represented as typed rule/policy semantics.

Minimum accepted semantic families:

```text
calendar / wall-clock
elapsed interval
quota per period
completion-relative
anchor-stream-relative
cyclic positional
```

A shared recurrence engine/DSL is allowed later only if the family and its material anchor/frame semantics remain explicit and reverse-mappable.

```text
shared recurrence implementation
!= one recurrence semantic algorithm
```

Pattern anchor, effective range, parent lifecycle and generated Occurrences remain distinct.

Quota recurrence must preserve an explicit period frame where membership can differ materially under calendar/time-zone/domain rules.

---

## 17.3 Occurrence identity and lazy materialization

Occurrence is the stable semantic identity of one expected generated instance.

Once an Occurrence requires persistent independent addressability/history:

```text
Occurrence -> LR-01 -> NativeRef
```

However:

```text
native semantic identity
!= eager physical materialization
```

Future instances may remain derivable/lazy until an operational horizon or meaningful interaction requires persistence.

Before persistent addressability, the recurrence/source material state plus a bounded generation context may locate the derivable semantic instance. This locator is not a new universal `ReferenceAddress` variant and is not an independent Domain owner.

When persistence becomes necessary:

```text
derivable semantic Occurrence
        ↓ materialization/addressability
same semantic Occurrence
        ↓
NativeRef
```

Materialization must not create a different occurrence identity merely because a row/key is now persisted.

Exact native-key issuance, deterministic locator or migration strategy is Physical Model work.

### Generation context

Depending on recurrence family, generation context may include:

```text
calendar position
quota period + distinguishable slot
qualifying Actual anchor
qualifying Session/Event anchor
cycle position
source-material-state-relative generation context
```

No universal current/original datetime identity is accepted.

Equivalent quota slots do not acquire artificial ordinal semantics solely for key generation.

---

## 17.4 Schedule — LR-02

Schedule is a dependent semantic record representing current accepted temporal assignment.

```text
Schedule -> LR-02
```

Where an individual materialized Schedule record/placement requires stable logical addressability:

```text
Schedule -> ScopedRecordRef
```

under the applicable Reference Contract.

Schedule does not gain NativeRef merely because it is addressable.

Required rules:

```text
no current Schedule is valid
one subject may have multiple accepted placements
prior/current accepted placements remain reconstructible where material
Schedule != Recurrence
Schedule != Temporal Constraint
Schedule != Session
Schedule != Actual
Schedule != capacity reservation
Schedule != movement Authority/policy
```

A postponed Event can retain Event identity and historical placements while current Schedule is absent.

---

## 17.5 Session — LR-01

Session has independently meaningful actual-execution identity and is classified:

```text
Session -> LR-01 -> NativeRef
```

Required identity/lifecycle rules:

```text
Session identity != timestamps
Session identity != provider ID
pause/resume != new Session by default
explicit end/restart normally -> separate Session
correction != new Session automatically
split/merge preserves lineage
```

A Session may exist without prior Schedule or pre-existing Activity.

Overlapping Sessions are not globally invalid. Aggregation must distinguish category/domain time, elapsed time, active time and unique wall-clock coverage where relevant.

---

## 17.6 Actual — LR-06 + LR-02 when addressable

Actual remains contextual realization rather than universal reality identity.

```text
Actual -> LR-06
```

When a materialized Actual requires stable contextual addressability/history:

```text
Actual -> LR-02 + ScopedRecordRef
```

This does not promote Actual into a native universal fact/reality root.

Canonical epistemic barrier:

```text
no established Actual
!= known non-realization
```

Schedule passage, deadline passage, silence or missing provider events do not establish Actual by themselves.

Exact assertion/provenance/reconciliation mechanics remain Slice D.

---

## 17.7 Outcome — LR-06 / LR-02 where material

Outcome is contextual result/disposition of a specific realization.

```text
Outcome -> LR-06
```

A material persistent Outcome may use LR-02/ScopedRecordRef when independent reference/history warrants it.

No universal Outcome enum is accepted.

```text
Outcome != lifecycle state
Outcome != Actual
Outcome != Observation
Outcome != Milestone
Outcome != Confirmation/Provenance
```

Outcome remains optional.

---

## 17.8 Temporal Constraint — LR-05

Temporal Constraint uses LR-05 typed rule/policy semantics.

The representation must preserve the semantic relation to time, not only raw range geometry.

Possible dimensions include:

```text
hard / soft
start / completion / arrival / other relevant facet
lower / upper bound
containment / overlap / start-inside / completion-inside relationship
duration rule
spacing / recovery / lead / lag
repeated applicability
```

The same interval geometry may be a Schedule, Constraint, Availability window or target. Geometry is not semantic classification.

A hard planning rule may be violated by truthful Actual.

---

## 17.9 Conditional Policy — LR-05 boundary

Conditional Policy remains LR-05 but is not merged with Recurrence or Time semantics.

```text
Recurrence
= repeated generation/applicability

Temporal Constraint
= temporal admissibility/preference

Schedule
= accepted placement

Conditional Policy
= bounded response when activation basis is established
```

Time may be part of activation basis, but:

```text
activation != downstream effect success
```

---

## 17.10 Material-state/history requirements

Slice D must provide physical/logical history mechanisms sufficient to address:

```text
governing source/recurrence state for historical Occurrence
Occurrence-specific exception state
prior/current accepted Schedule state
Schedule state applicable when Actual occurred
Session corrections and split/merge lineage
Actual/Outcome assertion and correction history
provider mapping/reconciliation history
temporal interpretation/precision basis where consequential
```

Current-state reads must not require replaying the entire lifetime history in application memory.

This requirement does not mandate global bitemporality or event sourcing.

---

## 17.11 Provider mapping

Provider/source identity stays LR-09 / ExternalRef.

Relevant recurring-provider pressure may include:

```text
provider series ID
provider instance ID
provider original-instance marker
provider current placement
provider revision/tombstone
LifeOS Occurrence NativeRef
LifeOS accepted Schedule
mapping/reconciliation state
```

```text
ExternalRef != Occurrence NativeRef
provider original start != universal LifeOS occurrence ID
```

Lossless provider export is not a kernel invariant.

---

## 17.12 ReferenceAddress mechanism reconsideration

Slice C triggered LM-WF-21 because virtual/lazy occurrence identity added new addressability pressure.

Candidates reconsidered:

```text
owner-specific references only
global Node/TemporalObject registry
new generic VirtualRef
discriminated ReferenceAddress + bounded occurrence locator/generation context
```

Verdict:

```text
ReferenceAddress
RETAIN + HARDEN

new generic VirtualRef
REJECTED
```

Reason:

- derivation/materialization state is not itself a semantic reference-space family;
- NativeRef remains the address of a persistently addressable native Occurrence;
- pre-materialization derivation can use source/material-state + bounded generation context without manufacturing a universal reference root;
- exact key issuance remains physically open.

This extends INV-088..100 rather than replacing them.

---

## 17.13 Reverse-mapping summary

```text
LOGICAL
LR-04 typed temporal value
DOMAIN
value/temporal interpretation only
NOT
Time entity/root

LOGICAL
LR-05 Recurrence
DOMAIN
Recurrence
NOT
Routine/Event/source/Occurrence

LOGICAL
LR-01 Occurrence
DOMAIN
one expected generated instance
NOT
Schedule/current datetime/provider instance

LOGICAL
LR-02 Schedule
DOMAIN
accepted temporal assignment
NOT
Constraint/Actual/Capacity

LOGICAL
LR-01 Session
DOMAIN
actual execution episode
NOT
Schedule/Actual result

LOGICAL
LR-06/LR-02 Actual
DOMAIN
contextual realization
NOT
universal reality/Observation

LOGICAL
LR-06/LR-02 Outcome
DOMAIN
contextual result/disposition
NOT
universal lifecycle/status

LOGICAL
LR-05 Temporal Constraint
DOMAIN
placement/duration/temporal-relation rule
NOT
Schedule/Availability

LOGICAL
LR-05 Conditional Policy
DOMAIN
conditional response
NOT
Recurrence/Trigger root/Actual
```

---

## 17.14 Physical freedom retained

Slice C does not choose:

```text
PostgreSQL temporal types/columns
registry vs owner-FK reference implementation
recurrence engine/DSL
occurrence materialization cache/horizon
NativeRef key algorithm
Schedule placement table split
Session pause table/segments
event sourcing usage
history/version tables
provider adapter schemas
API temporal serialization
scheduler/optimizer
```

Any later choice must pass INV-101..130 and cumulative regression.

---

## 17.15 Canonical Slice-C references

- `slices/time-reality-v1.md`
- `checkpoints/time-reality-v1-validation.md`
- `benchmarks/time-reality-v1.md`
- `traceability-and-regression-ledger-v1.md` + canonical Part 2 continuation
- `decision-and-assumption-register-v1.md` + canonical Part 2 continuation
- `test-corpus-v1.md` + canonical Part 2 continuation
- this representation-framework continuation

Slice C is active only after exact remote QA confirms the approved physical scope and `main` remains unchanged.

After Slice C activation, the mandatory next semantic gate is cumulative **Integrated A+B+C** review. Slice D may not start merely because this continuation exists.
