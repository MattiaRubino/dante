# LifeOS Logical Model — Slice C: Time / Reality v1

**Status:** accepted candidate baseline pending checkpoint remote QA  
**Date:** 2026-08-17  
**Slice:** C — Time / Reality  
**Authority:** accepted Domain Atlas > Product North Star > ADR-007 > Domain→Logical readiness contract > Logical Model methodology > accepted Slice A+B contract > current external evidence

---

## 1. Purpose

Slice C defines the logical representation contract for temporal expectation, recurrence, instance identity, accepted placement, actual execution and realized result without collapsing them into one calendar object, one timestamp pair, one generic temporal event, one status field or one universal event log.

The slice covers pressure around:

- Recurrence;
- Occurrence;
- Schedule;
- Session;
- Actual;
- Outcome;
- Temporal Constraint;
- Conditional Policy interaction;
- temporal value semantics and precision;
- provider recurrence/instance synchronization;
- material history needed to preserve planned-versus-actual truth;
- Slice-A ReferenceAddress and Slice-B governing-state interaction.

It does **not** select SQL tables, PostgreSQL column types, indexes, event sourcing, API payloads, recurrence libraries, runtime schedulers or workflow engines.

---

## 2. Core conclusion

The selected logical direction is the **Layered Typed Time & Reality Model**.

The name is a representation strategy only. It does not introduce a Domain superclass called `TemporalEvent`, `TimelineItem`, `TimeObject`, `RealityRecord` or equivalent.

Canonical separation:

```text
RECURRING / GENERATIVE SOURCE
!= RECURRENCE RULE
!= EXPECTED OCCURRENCE IDENTITY
!= ACCEPTED SCHEDULE PLACEMENT
!= ACTUAL EXECUTION SESSION
!= ACTUAL REALIZATION
!= OUTCOME
!= TEMPORAL CONSTRAINT
!= CONDITIONAL RESPONSE
```

A useful conceptual path is:

```text
Routine / recurring Event / other approved source
        ↓
Recurrence
        ↓
Occurrence
        ↓
Schedule, when accepted placement exists
        ↓
Session(s), where executable episodes are tracked
        ↓
Actual
        ↓
Outcome, where result/disposition is meaningful
```

This path is not mandatory for every case. One-off Event, spontaneous Session, Observation-only reality and unscheduled Activity remain valid without synthetic wrappers.

---

## 3. Temporal value semantics

Slice C requires a reusable typed temporal-value family but does not create a semantic Time object hierarchy.

The logical representation must preserve, where materially relevant, distinctions among:

```text
civil date / date-only meaning
floating local wall-clock meaning
named-zone wall-clock meaning
absolute instant
bounded/open interval or range geometry
duration / elapsed amount
precision or granularity
period-frame semantics
```

These are LR-04 value semantics.

### 3.1 No premature UTC collapse

A named-zone wall-clock intention such as:

```text
08:00 Europe/Rome every day
```

is not semantically equivalent to:

```text
one fixed UTC instant sequence
```

and neither is equivalent to:

```text
every 24 elapsed hours
```

Resolution to instants may be required operationally, but the originating temporal meaning must remain recoverable.

### 3.2 DST gaps and overlaps

A local wall-clock expression can be nonexistent or ambiguous under a time-zone rule set.

Example pressure for Europe/Rome in 2026:

```text
2026-03-29 02:30 local
DST spring gap — no ordinary civil occurrence

2026-10-25 02:30 local
DST fall overlap — two possible instants
```

The logical model must permit an explicit resolution/policy basis where consequence matters. It must not silently treat a parser/library default as the user's canonical intention.

### 3.3 Date-only is not a 24-hour busy block

A date-based/all-day Schedule retains calendar-date meaning. It does not imply exact midnight-to-midnight instant occupation or capacity consumption.

### 3.4 Precision must not be invented

The following remain distinct:

```text
Tuesday
Tuesday afternoon
Tuesday at 18:00
Tuesday 18:00-20:00
start known / end unknown
approximate historical interval
```

A physical database may later normalize/calculate representations, but canonical logical meaning must retain the accepted precision.

---

## 4. Recurrence

Logical role:

```text
structured repeated temporal/generative rule
```

Disposition:

```text
LR-05 rule/policy definition
```

Recurrence may have a persistent scoped address/material state when independent history/reference matters, but addressability does not create a universal recurrence root or equate Recurrence with its parent source.

Required semantic families include at least:

1. calendar / wall-clock recurrence;
2. elapsed-interval recurrence;
3. quota-per-period recurrence;
4. completion-relative recurrence;
5. anchor-stream-relative recurrence;
6. cyclic positional recurrence.

### 4.1 One recurrence engine does not imply one semantic algorithm

The following are not interchangeable syntax:

```text
Every Monday at 18:00 Europe/Rome
Every 12 elapsed hours
3 times per week
30 days after qualifying Actual completion
After each qualifying photography Session
2 days on / 2 days off
```

A later implementation may share an engine or DSL only if the semantic family remains explicit and testable.

### 4.2 Pattern anchor, range and parent lifecycle are distinct

Where relevant:

```text
pattern anchor
!= effective range
!= source pause/end lifecycle
!= generated Occurrence
```

Creation time is not a default semantic recurrence anchor.

### 4.3 Quota period frame

For quota recurrence, period membership must retain an explicit frame when locale/time-zone/domain boundaries can change which period contains an instance.

```text
3 times per week
```

must not depend silently on an unrelated library default for first day of week or current device zone.

### 4.4 Recurrence count is expectation count

```text
10 generated Occurrences
!= 10 successful completions
```

Success belongs to Actual/Outcome/Evaluation semantics.

---

## 5. Occurrence

Logical role:

```text
stable identity of one expected instance generated by a recurring/generative source
```

Disposition:

```text
LR-01 native identity-bearing logical record once persistently addressable/materially historical
```

Occurrence identity is independent of current start/end, provider ID and current Schedule.

### 5.1 Virtual versus materialized occurrence

Semantic identity does not require eager database materialization.

Conceptually:

```text
source + governing MaterialStateRef + generation context
        ↓
derivable future semantic instance
        ↓ meaningful interaction/history
stable persisted/addressable Occurrence
```

Future expansion may remain virtual inside an operational horizon. Once an instance acquires material independent history, LifeOS must preserve it stably.

Materialization triggers include pressure such as:

- occurrence-specific edit;
- accepted Schedule;
- skip/cancellation;
- exception;
- Actual/attendance;
- provider synchronization identity;
- notification/confirmation history where consequential;
- Evidence/analysis tied to that instance.

### 5.2 No new generic VirtualRef

Slice C reopens the Slice-A+B reference mechanism under LM-WF-21.

Result:

```text
ReferenceAddress family
RETAIN + HARDEN
```

A virtual derivation does not require a new generic `VirtualRef` address space.

Before persistent addressability, a bounded **occurrence locator/generation context** may identify the derivation under a governing source material state. When the instance becomes persistently addressable, LifeOS establishes a stable NativeRef for that same semantic Occurrence and persists enough generation/source context to prevent later re-expansion from changing what the instance meant.

```text
semantic occurrence identity
!= eager row existence

materialization
!= creation of a different Occurrence
```

The exact key-generation or deterministic-locator algorithm remains physical-stage work.

### 5.3 Generation coordinate is not universal datetime or ordinal

Depending on recurrence family, generation context may involve:

```text
calendar position
quota period + distinguishable slot
qualifying Actual anchor
qualifying Session/Event anchor
cycle position
source-version-relative generation context
```

For equivalent quota slots, LifeOS must not invent semantic `first/second/third` order merely to generate keys unless source semantics establish that order.

### 5.4 Source revision does not rewrite past occurrences

Historical Occurrences must retain enough governing source/material-state context that a later recurrence revision cannot regenerate the past under the new rule.

---

## 6. Schedule

Logical role:

```text
current accepted temporal assignment of a schedulable subject
```

Disposition:

```text
LR-02 dependent semantic record
+
material-state/history semantics where consequential
```

When an individual Schedule record/placement requires stable reference, it may use `ScopedRecordRef` under an applicable Reference Contract.

### 6.1 Schedule absence is valid

```text
Activity exists
Temporal Constraints exist
Schedule = none
```

is valid.

No synthetic `UNSCHEDULED Schedule` record is required.

An Event may also preserve identity/historical accepted placements while having no current Schedule after postponement with date TBD.

### 6.2 Multiple planned placements

A divisible Activity can legitimately have multiple accepted placements:

```text
Activity estimated effort 3h
Schedule placements 2h + 1h
```

The model must not require one universal `start_at/end_at` pair on the Activity.

### 6.3 Revision history

Current accepted Schedule and prior accepted placements must be reconstructible.

```text
original accepted placement
→ revision 1
→ revision 2
→ current accepted placement
```

A material Schedule revision during execution is allowed when the expectation itself is explicitly changed; simple overrun/early start remains Actual deviation, not an implicit Schedule rewrite.

### 6.4 Schedule boundaries

```text
Schedule != Recurrence
Schedule != Temporal Constraint
Schedule != Deadline/target by default
Schedule != Availability/Capacity reservation
Schedule != Session
Schedule != Actual
Schedule != movement Authority/policy
```

The same time range can represent different semantics; geometry alone does not classify it.

---

## 7. Session

Logical role:

```text
persistent identity of one logically continuous actual execution episode
```

Disposition:

```text
LR-01 native identity-bearing logical record
```

Session identity remains stable across ordinary timestamp correction and provider reconciliation.

### 7.1 Session can exist without prior Schedule or Activity

Spontaneous execution is truthful reality.

LifeOS must not fabricate a historical Activity/Schedule merely to make the data look orderly.

### 7.2 Pause/resume

Pause normally remains within one Session identity:

```text
start
pause
resume
end
```

Elapsed, paused and active duration remain distinguishable when known.

Explicit end/close followed by later restart normally creates another Session unless correction/reconciliation proves the capture was structurally wrong.

### 7.3 Split/merge correction

Structural capture errors may require Session split/merge while preserving lineage to the original captured record. Slice D must supply exact correction/version/provenance mechanics.

### 7.4 Overlap is not universally invalid

Two real Sessions can overlap where behavior is compatible.

Therefore:

```text
SUM(Session.duration)
!= universal total unique wall-clock time
```

Aggregation semantics must be explicit/derived.

---

## 8. Actual

Logical role:

```text
contextual realization of a specific intended/expected subject
```

Disposition:

```text
LR-06 material realization
+
LR-02 dependent semantic record when persistent identity/reference is required
```

A materialized Actual may use `ScopedRecordRef`; stable contextual identity does not promote Actual into a universal native reality root.

### 8.1 Actual is contextual, not universal reality

Observation, spontaneous Session, imported specialist transaction and other real facts may exist without Actual when there is no expectation to reconcile.

### 8.2 Unknown versus known non-realization

Canonical distinction:

```text
no established Actual
!= known non-realization
```

Time passage, Schedule expiry or absence of provider data does not establish completion, miss, skip, failure or non-execution.

Known non-realization requires an applicable assertion/evidence/reconciliation basis.

### 8.3 Correction

Current accepted Actual may change through correction/reconciliation while preserving relevant prior assertions, source history and material state. Exact mechanics are Slice D.

### 8.4 Shared versus actor-scoped reality

Shared Event Actual does not imply identical Participation/attendance for every Actor. Slice F owns final actor/governance mapping.

---

## 9. Outcome

Logical role:

```text
contextual result/disposition of a specific Actual realization
```

Disposition:

```text
LR-06 / LR-02 when a materially persistent result record is justified
```

Outcome is optional.

No universal result enum is accepted.

```text
Outcome != lifecycle state
Outcome != Actual
Outcome != Session
Outcome != Observation
Outcome != Milestone
Outcome != Confirmation/Provenance
```

Absence of Outcome is not a negative Outcome. Partial does not universally mean failure.

---

## 10. Temporal Constraint

Logical role:

```text
rule restricting or preferring placement, duration or temporal relation
```

Disposition:

```text
LR-05 rule/policy definition
```

The logical model must preserve, where applicable:

- hard vs soft planning semantics;
- relevant temporal facet being constrained;
- lower/upper bounds;
- containment/overlap/start/completion relationship to a range;
- duration constraints;
- spacing/recovery/relative constraints;
- recurring applicability without confusing it with Occurrence generation.

A hard planning constraint can be violated by reality. LifeOS records truthful Actual first, then derives/records the violation under applicable evaluation semantics.

---

## 11. Conditional Policy boundary

Conditional Policy remains LR-05 conditional-response semantics.

```text
Recurrence
= repeated generation/applicability structure

Conditional Policy
= bounded response when activation basis is established

Trigger
= activation role/facet
```

Therefore:

```text
policy activation != Recurrence
policy activation != Schedule
policy activation != Actual
policy activation != successful downstream effect
```

A time fact may supply activation basis without turning Schedule/Constraint/Recurrence into the policy.

---

## 12. Material-state and history contract

Slice C requires later Slice-D history/version mechanisms to preserve at least:

- governing recurrence/source material state for historical Occurrences where material;
- occurrence-specific exception history;
- prior/current accepted Schedule placements;
- which Schedule state was effective when an Actual/Session occurred where comparison matters;
- Session correction/split/merge history;
- Actual/Outcome assertion and correction history;
- provider mapping/reconciliation history;
- temporal interpretation/precision basis where later re-resolution could alter meaning.

The current-state query path must not require replaying the entire lifetime history in application memory.

This does not mandate global event sourcing or global bitemporality.

---

## 13. Provider and interoperability contract

Provider data remains external/source state.

Recurring-provider synchronization may need to retain:

```text
provider series identity
provider instance identity
provider original-instance anchor
provider current placement
provider revision/tombstone
LifeOS source/Occurrence identity
LifeOS accepted Schedule
reconciliation state
```

None of those provider identifiers becomes the LifeOS Occurrence/Session identity automatically.

Lossless export to RFC 5545, Google Calendar, Microsoft Graph or another provider is not a kernel invariant. Controlled degradation, adapter metadata or explicit incompatibility is preferable to weakening LifeOS semantics.

---

## 14. High-value logical queries

The representation must support at least:

1. what Schedule is currently accepted for a subject and what was accepted at time T?
2. which Occurrence is this after one-off rescheduling?
3. which source/material recurrence state generated a historical Occurrence?
4. which future Occurrences are derivable without eagerly materializing all future rows?
5. which material Occurrences were skipped/cancelled/moved rather than never generated?
6. which recurring expectations are quota-based, completion-relative, anchor-stream or wall-clock?
7. which time interpretation applies: date-only, floating, named-zone or absolute?
8. which planned placements existed for one divisible Activity?
9. which Sessions actually realized an Activity/Occurrence and with what overlap?
10. what elapsed/active/paused time is known without inventing precision?
11. did the user actually act, or did only the Schedule time pass?
12. which Actual represents known non-realization rather than unknown reality?
13. what Outcome was established and which operational/lifecycle state remains separate?
14. which Temporal Constraints were applicable and did Actual violate them?
15. which provider instance maps to which LifeOS Occurrence despite moved start time/provider-ID churn?
16. can current state be queried without lifetime event replay?
17. can a simple one-off appointment remain compact without artificial Occurrence/Session/Outcome wrappers?
18. can a spontaneous Session remain truthful without retrospective fake intention?

---

## 15. Candidate comparison

### Candidate A — Universal TemporalEvent / TimelineRecord

Shape:

```text
TemporalEvent(kind,start,end,status,recurrence,parent)
```

**Verdict:** REJECTED.

Failure: collapses Occurrence/Schedule/Session/Actual/Outcome/Constraint into `kind/status/metadata`, recreates a universal semantic root and makes same-geometry/different-meaning cases indistinguishable.

### Candidate B — owner-specific timestamps only

**Verdict:** RETAINED STRONG PHYSICAL INGREDIENT, not selected as complete logical baseline.

Strength: maximum FK/local specificity and simple storage for trivial cases.

Failure as complete logical baseline: repeats temporal precision, recurrence, revision, provider and planned-vs-actual mechanisms across owners; direct overwritable timestamps destroy history; heterogeneous high-value queries become ad hoc.

### Candidate C — Layered Typed Time & Reality Model

**Verdict:** SELECTED.

Shape:

```text
typed temporal value semantics
+ typed recurrence rules
+ stable Occurrence/Session identities
+ dependent Schedule/Actual/Outcome records where material
+ explicit history/material-state references
+ provider mappings
+ derived comparisons/projections
```

### Candidate D — Universal append-only temporal/event-sourced ledger

**Verdict:** REJECTED AS UNIVERSAL LOGICAL REQUIREMENT.

Excellent audit technique in bounded contexts, but semantics still require the typed owners above; forcing all current-state reads through lifetime replay over-models simple cases and turns technical events into ontology pressure.

### Candidate E — Provider/calendar recurrence model as kernel

**Verdict:** REJECTED.

RRULE/calendar-series models are strong for calendar recurrence and interop but cannot safely define quota-per-period, completion-relative, anchor-stream and some cyclic semantics as the LifeOS-wide kernel.

---

## 16. Falsification summary

The selected candidate survived deliberate mutations including:

```text
Occurrence ID = current datetime                         REJECTED mutation
Occurrence ID = original datetime universally           REJECTED mutation
persist every future Occurrence forever                 REJECTED mutation
one recurring Activity moved forward forever            REJECTED mutation
one generic status across Schedule/Actual/Outcome       REJECTED mutation
Schedule elapsed => Actual completed                    REJECTED mutation
Deadline passed => missed Outcome                       REJECTED mutation
Schedule timestamps overwritten by Actual               REJECTED mutation
one start/end pair per Activity                         REJECTED mutation
all-day => 24h capacity reservation                     REJECTED mutation
UTC-only storage meaning                                REJECTED logical mutation
calendar-day recurrence = fixed elapsed seconds         REJECTED mutation
quota recurrence = arbitrary weekdays                   REJECTED mutation
pause always creates new Session                        REJECTED mutation
Session overlap globally forbidden                      REJECTED mutation
provider recurring instance ID = LifeOS Occurrence ID   REJECTED mutation
Conditional Policy = Recurrence                         REJECTED mutation
hard planning Constraint blocks truthful Actual         REJECTED mutation
```

No mutation exposed a Domain-level contradiction in Candidate C.

---

## 17. External evidence summary

Fresh primary/official evidence verified on 2026-08-17 supports the structural direction:

- RFC 5545 distinguishes date/date-time/floating/zoned/UTC semantics and recurrence-instance identity;
- Google Calendar keeps `originalStartTime` separate from current `start` for moved recurring instances;
- Microsoft Graph separates recurrence pattern from recurrence range/time-zone framing;
- Todoist distinguishes scheduled-date recurrence from completion-date recurrence;
- Reclaim separates recurring default event semantics from move/shorten/skip/defend conflict rules and uses bounded scheduling horizons;
- Motion treats task inputs/constraints separately from dynamically produced scheduled blocks;
- Android Health Connect distinguishes planned exercise sessions from completed exercise-session records;
- Apple HealthKit keeps pause/resume inside workout-session lifecycle and distinguishes active duration;
- FHIR distinguishes Appointment planning from Encounter actual occurrence and separately exposes planned versus actual timing;
- PostgreSQL current documentation confirms that named-zone rules/DST and calendar intervals cannot be reduced safely to naive fixed-offset/fixed-second assumptions.

These are benchmark mechanisms, not LifeOS ontology authorities.

Canonical source/disposition record: `../benchmarks/time-reality-v1.md`.

---

## 18. Cross-slice dependencies

### Slice A/B — Identity / Reference + Intention / Execution

Slice C retains and hardens ReferenceAddress.

```text
materialized/addressable Occurrence -> NativeRef
Session -> NativeRef
Schedule/Actual/Outcome material record -> ScopedRecordRef where needed
historical governing state -> MaterialStateRef
provider identity -> ExternalRef
```

Virtual occurrence derivation does not introduce a universal new reference space.

### Slice D — Evidence / Knowledge / History

Must prove exact Version/Provenance/Reconciliation representation for source-state binding, Schedule history, Session correction and Actual/Outcome assertion correction.

### Slice E — Resources / Values / Capacity

Must preserve:

```text
Schedule != capacity reservation
Temporal Constraint != Availability/Capacity
Actual resource use != Allocation
```

### Slice F — Relationships / Multi-Actor / Governance

Must preserve actor-specific Participation, Authority, Visibility and conditional policy governance around shared Schedule/Actual without duplicating shared reality.

---

## 19. Physical deferrals

```text
exact PostgreSQL temporal column/type mapping
exact timezone database/version capture strategy
DST gap/overlap runtime policy representation
exact recurrence DSL/library/expansion algorithm
occurrence locator/key-generation algorithm
virtual-occurrence operational horizon/materialization cache
exact Schedule placement table/cardinality
exact Session pause-segment persistence
exact Actual/Outcome table/value representation
exact Version/Provenance history model
provider recurrence adapter schemas
query/index/partition strategy
event sourcing usage, if any
API serialization of coarse/floating/zoned temporal values
runtime scheduler/optimizer
```

All are stage-deferred. None may weaken the Slice-C logical contract.

---

## 20. Slice-C acceptance contract

Slice C becomes active only after:

```text
canonical Slice-C document written
validation checkpoint written
external benchmark record written
representation framework continuation written
test corpus continuation written
traceability ledger continuation written
decision/assumption register continuation written
workstream continuation written
exact remote compare/readback passes
main remains unchanged
```

Until remote QA succeeds, this document records an accepted candidate baseline rather than final active closure.

---

## 21. Current verdict

```text
SLICE C — TIME / REALITY

SELECTED
Layered Typed Time & Reality Model

LOCAL VERDICT
PASS WITH HARDENING

ReferenceAddress
REOPENED UNDER LM-WF-21
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED      0
NEW DOMAIN OWNER REQUIRED   0
LOGICAL STRUCTURAL BLOCKER  0

REMOTE ACTIVATION
PENDING CHECKPOINT QA
```
