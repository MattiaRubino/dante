# Timeline / Temporal-Operational Vertical — Semantic Work Map

- **Status:** FROZEN SEMANTIC MAP / LIVE IMPLEMENTATION LEDGER — reconciled 2026-09-15
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main anchor at semantic freeze:** `981f6cf9ad985d0b811bc4172c12a7529fbc9b15`
- **Roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Required companion audits:**
  - `docs/workstreams/timeline-temporal-operational-second-audit-2026-09-07.md`
  - `docs/workstreams/timeline-temporal-operational-final-pre-roadmap-audit-2026-09-07.md`
- **B02 execution plan:** `docs/workstreams/timeline-temporal-operational-b02-execution-plan.md`
- **Purpose:** freeze the complete semantic/product/runtime work map and act as the live green-check implementation ledger until the whole vertical closes.
- **Important:** semantic sections are architecture/work-map authority, not API/DDL authority, and do not reopen accepted Domain / Logical / Physical / CP1–CP6 decisions.
- **Change-control rule:** implementation convenience, UI convenience, provider shape, ORM convenience, benchmark precedent, or roadmap pressure cannot create a new semantic root or collapse an accepted distinction.
- **Execution rule:** every implemented capability must update the live ledger in this document in the same reviewed slice. `✅` is forbidden until all applicable semantic, persistence, backend, frontend, automated-test, manual-`userTest`, and same-change documentation gates pass.

---

## 0. Authority, reading order, and meaning of this map

This map consumes already-accepted DANTE truth. It does not replace it.

Authority order for this vertical is:

1. current protected `main` code, migrations, tests, accepted current docs and repository governance;
2. accepted Domain concepts and validation checkpoints;
3. closed Whole Logical Model and decision/assumption registers;
4. accepted Physical/PostgreSQL selection and CP6 concrete PostgreSQL baseline;
5. current frontend Home/Timeline/F0/C1 contracts and frozen behavior;
6. this work-map document plus its two required audit companions;
7. the frozen implementation roadmap;
8. external benchmarks only as design pressure/evidence, never as ontology authority.

Permanent inherited rules include, among others:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Schedule != Session != Actual
recurrence rule != generated Occurrence
AI proposal != accepted effect
provider record identity != DANTE identity
source/provenance != truth
absence/unknown != false
```

The CP6 concrete PostgreSQL baseline is closed. Later forward migrations exist on current protected `main`; they do not reopen CP6 historical decisions.

The current frontend baseline is inherited rather than reinterpreted:

```text
H0 Home structure              FROZEN
T1 Timeline behavior           FROZEN
F0 temporal application seam   CLOSED / FROZEN
C1 manual temporal Create      ENGINEERING GREEN / MANUAL OPEN
C2 structured detail           BLOCKED until C1 closes
```

A vertical implementation may consume and extend these owners through explicit boundaries. It must not silently rewrite them.

---

# 1. Vertical boundary

The vertical covers the complete lifecycle from temporal intention/expectation to temporal placement, recurring-instance identity, actual execution/realization, result resolution, user confirmation/correction, history, reconciliation and derived Timeline/operational projections.

It also includes the minimum cross-cutting runtime/application semantics required for those capabilities to behave correctly across web/mobile/provider/offline boundaries.

## 1.1 In-scope semantic owners/capabilities

Core temporal/operational family:

- Activity;
- Event;
- Routine;
- Occurrence;
- Schedule;
- Temporal Constraint;
- Recurrence;
- Session;
- Actual;
- Outcome.

Resolution/knowledge capabilities required by the lifecycle:

- Confirmation;
- Acknowledgement where explicit common-ground state materially matters;
- correction/reconciliation/history;
- provenance needed to explain current accepted truth;
- bounded replacement/substitution semantics;
- resolution/review state derived from unresolved Actual/Outcome/Confirmation needs.

Operational policy required by the lifecycle:

- movement/replanning policy;
- conditional response policy where it governs confirmation/review/reminder behavior;
- reminder intent boundary;
- automatic-outcome policy only when explicitly authorized;
- review cadence/grouped resolution.

Product organization required by Timeline usability:

- Calendar / Life Area product organization;
- tags/secondary organization;
- Context grouping/filter membership;
- appearance as a separate presentation dimension;
- mapping of external calendars/sources into local organization without merging identities.

Technical/application semantics required by this vertical:

- explicit Clock;
- date-only / floating-local / named-zone / absolute temporal forms;
- coarse accepted placement precision where real intent is coarser than an exact block;
- DST/user-local range semantics;
- idempotent mutation operations;
- expected-state concurrency;
- guarded Undo;
- multi-device/offline Session reconciliation;
- provider identity mapping/reconciliation;
- authoritative range/window read model;
- Timeline, Planning Tray, Resolution Queue, Detail/History and Analytics projections.

## 1.2 Connectable but not owned by this vertical

The vertical must interoperate with these already-accepted/future owners without implementing them as temporal subtypes:

- Goal;
- Plan;
- Milestone;
- Responsibility;
- Participation;
- Person / Actor;
- Place;
- Authority / Decision / Visibility;
- Evidence;
- Observation / Measurement;
- Artifact;
- Availability / Capacity / Reservation;
- Resource Requirement / Allocation;
- broader Relationship model;
- provider/integration infrastructure;
- notification delivery infrastructure;
- Search;
- AI orchestration/Intelligence runtime.

Canonical rule:

```text
connectable owner != owner implemented by this vertical
```

## 1.3 Explicitly excluded as top-level creation concepts here

These are not independent `+` entries for the temporal Timeline gateway merely because they participate in the lifecycle:

- Occurrence;
- Schedule;
- Temporal Constraint;
- Recurrence;
- Actual;
- Outcome;
- Confirmation;
- Acknowledgement;
- MaterialStateRef/current binding;
- recurrence checkpoint;
- idempotency key;
- provider reconciliation record;
- Timeline entry/read-model row;
- derived analytics record.

Observation remains owned by the later Observation/Tracking vertical. This vertical may read/link Measurements/Observations where Session/Actual/Outcome require them, but does not turn Observation into a Timeline creation root.

---

# 2. Work-map classifications

The classification is semantic/product-facing, not a statement about SQL table identity.

## 2.1 TOP-LEVEL ORIGINATING

May originate directly from an explicit user act rather than only as lifecycle state of another item.

- Activity;
- Event;
- Routine;
- Session recording.

Important UI qualification:

- conceptual product capability may allow direct Routine creation;
- current C1 manual Timeline Create exposes only `Activity` and `Event` primary actionable types;
- Activity `Repeat` in C1 is a Routine-backed authoring path, not Activity-owned recurrence;
- direct Session recording belongs to the later Session runtime, not current C1.

## 2.2 CONTEXTUAL / LIFECYCLE

Semantically real but normally created/modified as part of another owner's lifecycle or a bounded operation:

- Schedule;
- Temporal Constraint;
- Recurrence;
- Occurrence;
- Session when executing Activity/Occurrence;
- Actual;
- Outcome;
- Confirmation;
- Acknowledgement;
- Conditional Policy relevant to resolution/reminder behavior;
- Responsibility/Participation relations where the concrete operation needs them;
- replacement/replanning relations.

## 2.3 PRODUCT ORGANIZATIONAL CONTEXT

Real product organization, not the temporal item's identity and not automatically a Domain kernel primitive:

- Calendar / Life Area;
- tags;
- external calendar mapping;
- local grouping/focus visibility preferences.

## 2.4 DERIVED / PROJECTION

Never independent canonical truth merely because it is displayed or queryable:

- Timeline;
- Planning Tray;
- Resolution Queue / `Da risolvere`;
- Today/day/week/month/year read models;
- range-query pages/windows;
- current-placement display;
- history/detail projections;
- early/late/overrun/underrun labels;
- recurrence adherence/streak;
- aggregate statistics;
- conflict/infeasibility explanations;
- Signals/analytics projections.

## 2.5 INTERNAL / APPLICATION / PERSISTENCE

Never user-facing creation concepts:

- NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef;
- native/scoped/material addressing;
- explicit current accepted-state binding;
- material-state history controls;
- UUIDv7 issuance;
- operationId/idempotency fingerprint;
- expected projection revision;
- transaction/locking/advisory serialization;
- retry/dedup/replay mechanics;
- SQLAlchemy rows;
- Alembic revisions;
- DB routines/triggers/views/indexes;
- recurrence checkpoints/generation coordinates;
- provider mapping rows;
- sync cursor/checkpoint;
- frontend cache entries.

## 2.6 EXTERNAL SIDE-EFFECT BOUNDARY

Semantics may originate in this vertical, but execution is owned outside it:

- push/email/in-app notification delivery;
- external calendar/provider writes;
- invitations/conferencing/room booking;
- device/health/time-tracker import/export;
- external AI execution;
- external provider receipts/runtime completion.

---

# 3. Complete high-level tree

```text
TIMELINE / TEMPORAL-OPERATIONAL
│
├── ORIGINATING
│   ├── Activity                              TOP-LEVEL
│   │   └── semantic sub-Activity structure
│   ├── Event                                 TOP-LEVEL
│   │   ├── Agenda/internal parts
│   │   └── preparation/follow-up links
│   ├── Routine                               TOP-LEVEL
│   │   └── composite recurring structure
│   └── Session recording                     TOP-LEVEL capture / CONTEXTUAL execution
│
├── TEMPORAL EXPECTATION
│   ├── Schedule                              CONTEXTUAL
│   ├── Temporal Constraint                   CONTEXTUAL
│   ├── movement/replanning policy            CONTEXTUAL
│   ├── Recurrence                            CONTEXTUAL
│   └── Occurrence                            CONTEXTUAL generated/extra identity
│
├── EXECUTION / REALITY
│   ├── Session                               TOP-LEVEL or CONTEXTUAL
│   │   ├── manual/timer/import capture
│   │   ├── pause/resume/end
│   │   ├── correction
│   │   ├── split/merge
│   │   ├── overlap
│   │   └── cross-device/offline reconciliation
│   ├── Actual                                CONTEXTUAL
│   └── Outcome                               CONTEXTUAL
│
├── RESOLUTION / COMMON GROUND
│   ├── Confirmation                          CONTEXTUAL
│   ├── Acknowledgement                       CONTEXTUAL when required
│   ├── awaiting-confirmation                 DERIVED
│   ├── Resolution Queue                      DERIVED
│   └── review/batch-resolution               PRODUCT WORKFLOW
│
├── CONDITIONAL RESPONSE
│   ├── Conditional Policy                    CONTEXTUAL
│   ├── activation/Trigger semantics          ROLE, not root
│   ├── reminder intent                       RESPONSE
│   ├── review scheduling                     RESPONSE
│   └── explicitly-authorized automatic effect
│
├── PRODUCT ORGANIZATION
│   ├── Calendar / Life Area
│   ├── Tags
│   ├── Context/grouping/focus
│   ├── Appearance                            separate
│   └── external-calendar/source mapping
│
├── LIFECYCLE / REPLANNING
│   ├── schedule / reschedule / unschedule
│   ├── postpone
│   ├── cancel
│   ├── skip
│   ├── suspend / pause / resume / end
│   ├── replace
│   ├── reopen
│   ├── correction
│   ├── Undo
│   ├── delete/invalidate false data
│   └── archive/hide organizational state
│
├── SHARED SEMANTIC / RUNTIME INFRASTRUCTURE
│   ├── identity/addressing
│   ├── Material State / Version
│   ├── explicit current accepted state
│   ├── Provenance
│   ├── Reconciliation / Decision boundary
│   ├── Clock / timezone / DST / precision
│   ├── transaction / idempotency / concurrency
│   ├── provider mappings
│   └── multi-device synchronization
│
└── DERIVED PRODUCT / QUERY SURFACES
    ├── Timeline
    ├── Planning Tray
    ├── Resolution Queue / Review
    ├── Detail / History
    ├── range/window queries
    ├── conflict/infeasibility explanation
    └── Analytics / Signals
```

This is a work tree, **not** an inheritance hierarchy, **not** a table hierarchy, and **not** authorization to create one generic temporal mega-entity.

---

# 4. Creation / Recording Gateway

Conceptual final gateway:

```text
+
│
├── CREA
│   ├── Activity
│   ├── Event
│   └── Routine
│
└── REGISTRA
    └── Session
```

Current C1 authority is intentionally narrower:

```text
Timeline manual Create
├── Activity
└── Event
```

Current accepted C1 entry origins:

- Timeline `+`;
- double-click empty timed space;
- Shift-drag/range;
- deterministic structured manual prefill.

Current C1 does **not** include chat/NL interpretation, voice interpretation, AI command execution, real backend persistence, provider execution, canonical recurrence materialization, Session runtime, Actual runtime or notification delivery.

The future top-level gateway must remain an authoring/recording surface, not expose implementation details such as MaterialStateRef, recurrence checkpoint, provider reconciliation or idempotency.

---

# 5. Activity — full vertical surface

Activity is the persistent actionable intention: **what concrete action/work/behavior is intended**.

## 5.1 Internal semantic tree

```text
Activity
├── identity / actionable intention
├── semantic structure
│   ├── simple atomic action
│   └── optional sub-Activity decomposition
│       ├── semantic child work
│       └── independent from Session splitting
├── completion semantics
│   ├── output-bounded
│   ├── quantity-bounded
│   ├── effort/time-bounded
│   ├── checklist/composite
│   ├── partial execution
│   └── specialist completion where justified
├── estimated effort
├── temporal planning
│   ├── Schedule 0..N planned placements as applicable
│   ├── Temporal Constraints
│   ├── movement policy
│   └── unplaced state allowed
├── optional repeated-intent authoring
│   └── Routine-backed recurrence — NOT Activity-owned recurrence
├── responsibility/context
│   ├── Responsibility
│   ├── requester/responsible/performer separation
│   ├── Place where useful
│   ├── Calendar / Life Area
│   ├── tags
│   └── Goal/Plan links as external relations
├── execution
│   └── Session 0..N
├── realization
│   └── Actual optional/current contextual realization
├── result
│   └── Outcome optional
├── resolution
│   ├── Confirmation where policy/purpose requires it
│   └── Acknowledgement only for material common-ground workflows
├── lifecycle operations
│   ├── schedule / reschedule / unschedule
│   ├── start execution
│   ├── postpone
│   ├── replace
│   ├── cancel/expire/close where semantics permit
│   ├── reopen where semantics permit
│   └── correct history
└── projections
    ├── Timeline when placed/relevant
    ├── Planning Tray when unplaced
    ├── Resolution Queue when unresolved
    ├── Detail/History
    └── Analytics
```

## 5.2 Sub-Activity versus Session

```text
Activity: Write article
├── introduction
├── analysis
└── conclusion
```

is semantic decomposition.

```text
Session 1 Monday 20:00-21:00
Session 2 Tuesday 18:00-19:30
```

is temporal execution decomposition.

Canonical rule:

```text
Sub-Activity != Session
```

A long or interrupted Activity does not need artificial child Activities merely because it has several Sessions. Conversely, meaningful sub-work does not become separate Sessions merely because it is a child.

## 5.3 Estimated / scheduled / actual time

```text
estimated effort
!= scheduled duration
!= Session elapsed duration
!= Session active duration
```

These values answer different questions and must remain independently queryable for later estimation learning/analytics.

## 5.4 Unplaced Activity

An Activity may exist with no accepted Schedule.

This is first-class valid intent, not an error and not a fake all-day item.

Current C1 product representation:

```text
Activity placement = Da collocare
→ Planning Tray
```

The same Activity identity is later placed. Placement must not create a duplicate Activity.

## 5.5 Activity recurrence rule

Direct canonical `Activity.repeat` is forbidden.

Current C1 user-facing Repeat is allowed only through explicit ownership:

```text
user chooses Activity + Repeat
→ Activity remains Activity
→ persistent repeated-intent owner = Routine
→ Recurrence belongs to Routine
→ backend evaluator generates canonical Occurrences
```

## 5.6 Activity non-collapse register

```text
Activity != Event
Activity != Routine
Activity != Schedule
Activity != Temporal Constraint
Activity != Recurrence
Activity != Occurrence
Activity != Session
Activity != Actual
Activity != Outcome
Activity != Confirmation
Activity != Acknowledgement
Activity != Responsibility
Activity != requester
Activity != responsible actor / assignee
Activity != eventual performer
Activity != Participation
Activity != Goal
Activity != Plan
Activity != generic Task primitive
Activity != generic completed=true state
Activity != Timeline card
```

Task may remain user-facing/contextual language for an Activity whose primary semantics are defined-unit completion; it is not a second kernel primitive.

---

# 6. Event — full vertical surface

Event is occurrence-centred expectation for which temporal placement is intrinsic to the represented thing.

## 6.1 Semantic tree

```text
Event
├── expected-event identity
├── temporal meaning
│   ├── timed
│   ├── all-day
│   ├── multi-day
│   ├── current Schedule
│   ├── historical/original expectation
│   └── may temporarily have no current Schedule if postponed/TBD
├── Temporal Constraints / buffers as applicable
├── Place / conference intent
├── Participation
│   ├── participant response/intention
│   └── Actual attendance kept separate
├── Recurrence optional — Event-owned
│   └── Occurrences
├── Event-internal structure
│   ├── purpose
│   ├── expected outcome
│   ├── Agenda/internal parts
│   ├── pre-read/resources
│   └── notes/links where product permits
├── linked preparation/follow-up Activities
├── Actual Event occurrence
├── Outcome optional
├── Confirmation/Acknowledgement where required
├── provider identity/reconciliation
├── schedule/lifecycle history
└── projections
    ├── Timeline
    ├── Detail/History
    ├── Resolution Queue
    └── Analytics
```

## 6.2 Original expectation / current Schedule / Actual

Must remain reconstructible as three different layers:

```text
Original expectation
        ↓
Schedule revisions
        ↓
Current accepted Schedule
        ↓
Actual occurrence
```

If an Event is officially moved, Schedule changes.

If the Event simply starts early/late or runs shorter/longer without explicit expectation change, Schedule remains as accepted and Actual records reality.

## 6.3 Event postponed with date TBD

Valid state:

```text
Event identity
+
historical accepted placement
+
postponed/unresolved disposition
+
current Schedule = none
```

Do not fabricate a placeholder time.

This state must not be collapsed with an ordinary unplaced Activity.

## 6.4 Explicit expected-end revision during Event execution

If participants explicitly change the expected end while an Event is running, that can be a Schedule revision.

Example:

```text
Schedule 15:00-16:00
Actual begins 15:02
at 15:50 expected end explicitly extended to 16:30
Actual ends 16:24
```

Preserve both the mid-execution Schedule revision and Actual end.

If nobody revised expectation and the Event merely ran until 16:24, the Schedule remains 15:00-16:00 and `overrun` is derived.

## 6.5 Meeting lifecycle specialization without new kernel root

A meeting remains Event semantics, but product lifecycle can connect richer context.

Before:

- purpose;
- expected outcome;
- agenda;
- required/optional participants;
- preparation Activities;
- pre-read/documents;
- Place/link/room/resource intent;
- buffers;
- temporal constraints.

During:

- agenda progress;
- notes;
- decisions;
- commitments;
- unresolved matters;
- attendance information.

After:

- Actual occurrence;
- Outcome where meaningful;
- confirmed decisions;
- follow-up Activities;
- deadlines/owners as external relations;
- next Event/review;
- reminders;
- continuity across recurring meeting Occurrences.

Follow-up work must be normal linked Activity when it has its own planning/execution lifecycle. Do not trap actionable follow-up as opaque Event-note text.

## 6.6 Event Agenda/internal parts

Current C1 Event Agenda parts are structured internal Event parts and may map to Timeline subitems.

They do **not** automatically become:

```text
Activity
Event
Occurrence
Session
Actual
```

A part becomes an independent owner only if independent identity/lifecycle semantics are genuinely required.

## 6.7 Event participation separation

```text
Event state confirmed/tentative/cancelled...
!= domain Confirmation attestation

Participation response accepted/tentative/declined
!= Actual attendance

Acknowledgement of changed Event time
!= accepted Participation

Actual Event occurrence
!= identical Actual Participation for every Actor
```

Ordinary Event attendance does not create a Session by default.

## 6.8 Event / availability separation

An all-day birthday, optional webinar or similar Event does not automatically block capacity for its full represented interval.

```text
Event != Availability / Capacity Claim
```

## 6.9 Event non-collapse register

```text
Event != Activity
Event != Routine
Event != Schedule
Event != Temporal Constraint
Event != Recurrence
Event != Occurrence
Event != participant
Event != Participation
Event != attendance
Event != Session by default
Event != Actual
Event != Outcome
Event != Confirmation
Event != Place
Event != Deadline
Event != Milestone
Event != Calendar Block / Availability
Event != provider event identity
```

---

# 7. Routine — full vertical surface

Routine is persistent reusable policy for behavior/execution intentionally expected to repeat.

## 7.1 Semantic tree

```text
Routine
├── identity / recurring behavioral policy
├── behavior semantics
├── optional composite internal structure
├── Recurrence
│   ├── calendar / wall-clock
│   ├── elapsed interval
│   ├── quota per period
│   ├── cyclic positional
│   ├── completion-relative — semantically accepted
│   └── anchor-stream-relative — semantically accepted
├── pattern anchor/phase where required
├── effective range
├── effective material state/version
├── future policy revisions
├── temporary pause/override
├── Occurrence generation
│   └── Occurrence identities
├── per-Occurrence exception
│   ├── Schedule
│   ├── skip
│   ├── responsibility substitution
│   ├── Session(s)
│   ├── Actual
│   ├── Outcome
│   └── Confirmation
├── Goal/Plan/Life Area/context relations
└── derived adherence/history/analytics
```

## 7.2 Composite Routine

A Routine can govern a recurring bundle such as a morning routine.

Internal steps do not require one Routine per step. Steps whose own independent work/outcome/history matters may connect to Activity semantics.

Materially changing long-horizon stages/strategy/milestones tend toward Plan, not one mega-Routine.

## 7.3 Skip / pause / end

```text
skip one Occurrence
!= pause Routine
!= end Routine
```

- skip preserves Routine policy;
- pause temporarily suspends future expectation without erasing policy/history;
- end means the repeating policy is no longer expected to continue.

## 7.4 One occurrence versus future policy

```text
this Wednesday only at 20:00
→ Occurrence/Schedule exception

from now on Wednesdays at 20:00
→ Routine/Recurrence material-state revision
```

The source policy must retain effective-dated/material-state history so past Occurrences remain explainable under the policy that actually governed them.

## 7.5 Observed pattern is not Routine intent

Repeated Session history may justify an AI suggestion such as `create Routine?`, but must not silently create canonical Routine intent.

```text
observed repeated behavior != declared recurring policy
```

## 7.6 Derived adherence/streak

Routine does not require canonical `streak` or `adherence` state.

They are derived from:

- Occurrence history;
- Actuals;
- Outcomes;
- confirmation policy/state;
- evaluation period;
- possibly domain-specific acceptance criteria.

## 7.7 Routine non-collapse register

```text
Routine != Activity
Routine != Event
Routine != Recurrence
Routine != Occurrence
Routine != Schedule
Routine != Template
Routine != Trigger
Routine != Goal
Routine != Plan
Routine != observed habit/pattern
Routine identity != performer
Occurrence identity != responsible actor
responsibility rotation != Recurrence identity
```

---

# 8. Recurrence — full vertical surface

Recurrence is a structured rule describing how a temporal/generative pattern repeats from an explicit basis over an effective range.

## 8.1 Required semantic families

Domain semantics require at least:

1. calendar / wall-clock;
2. elapsed interval;
3. quota per period;
4. completion-relative;
5. anchor-stream-relative;
6. cyclic positional.

Current CP6 concrete materialized authoring/runtime family set is exactly:

- `calendar_wall_clock`;
- `elapsed_interval`;
- `quota_per_period`;
- `cyclic_positional`.

Completion-relative and anchor-stream-relative remain semantically accepted but must **not** be faked through generic JSON/RRULE or mislabeled as one of the CP6 four without a dedicated later physical/runtime decision.

## 8.2 Pattern anchor versus effective range

Where recurrence phase matters:

```text
pattern anchor / phase
!= effective range
```

`every 2 weeks` must not silently use `created_at` as its semantic anchor.

Effective range may be conceptually:

- open-ended;
- until a temporal boundary;
- for N expected Occurrences.

```text
N expected Occurrences
!= N successful completions
```

## 8.3 Ownership

```text
repeated Event
→ Event owns recurrence intent

repeated Activity user experience
→ Routine owns persistent repeated intent
```

Recurrence is reused capability; it does not determine the parent's semantic type.

## 8.4 Repeated applicability versus instance generation

A Recurrence pattern may also define repeated applicability of a Temporal Constraint.

Example:

```text
Temporal Constraint
preferred study window weekdays 17:00-21:00
```

may reuse recurrence pattern machinery but does not automatically generate expected Occurrences.

```text
repeated applicability != Occurrence generation universally
```

## 8.5 Calendar time versus elapsed time

```text
every day at 08:00 Europe/Rome
!= every 24 elapsed hours
```

Wall-clock recurrence must preserve calendar/civil semantics across DST.

Elapsed recurrence preserves elapsed interval from its qualifying anchor.

## 8.6 Time-zone modes

Recurrence semantics may distinguish:

- named-zone wall clock;
- floating/current-user-local wall clock;
- absolute/instant-based patterns.

Travel must not silently convert one mode into another.

## 8.7 Quota recurrence

`3 times/week` may establish distinct expected Occurrence identities before any exact dates are selected.

Therefore Recurrence is not merely a timestamp expansion function.

Quota-period membership must preserve an explicit period frame where timezone/calendar boundaries materially change membership.

Stable quota Occurrence identity does not automatically imply arbitrary first/second/third ordinal semantics.

## 8.8 Virtual/materialized series stop line

Do not eagerly create infinite future Occurrence rows.

Conceptual flow:

```text
recurring source + governing material state
→ derivable/virtual future occurrence identities
→ operational horizon / meaningful interaction
→ persistent reconstructible Occurrence state
```

Current frontend C1 only authors recurrence specification. It must not synthesize canonical future cards in the browser.

Canonical future series path:

```text
Routine/Event Recurrence
→ backend recurrence evaluator/checkpoint
→ canonical Occurrences when materialization is justified
→ temporal range/window query
→ normalized Timeline read model
→ Timeline
```

## 8.9 Skip versus structural exclusion

```text
not generated by governing rule
!= generated expected Occurrence later skipped/cancelled
```

The distinction is required for history, adherence and explanation.

## 8.10 Recurrence non-collapse register

```text
Recurrence != Routine
Recurrence != Event
Recurrence != Activity
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Session
Recurrence != Actual
Recurrence != Temporal Constraint
Recurrence != Conditional Policy
Recurrence != Trigger
Recurrence != generic IF/THEN automation
Recurrence != provider RRULE ontology
pattern anchor != effective range
expected count != successful completion count
```

Lossless external-provider mapping is not a kernel invariant.

---

# 9. Occurrence — full vertical surface

Occurrence is the stable logical identity of one distinguished expected instance produced by a recurring/generative source or explicitly added as an extra instance related to that source.

## 9.1 Semantic tree and origin-specific invariant

```text
Occurrence
├── stable DANTE identity
├── source Routine / recurring Event
├── origin
│   ├── recurrence_generated
│   │   ├── exact governing Recurrence MaterialState REQUIRED
│   │   └── compatible generation coordinate REQUIRED
│   │       ├── calendar
│   │       ├── elapsed
│   │       ├── quota
│   │       └── cyclic
│   └── explicit_extra
│       ├── source relation REQUIRED
│       ├── governing Recurrence MaterialState MUST BE ABSENT
│       └── generation coordinate MUST NOT pretend recurrence generation
├── original semantic expectation/anchor where applicable
├── current Schedule optional
├── occurrence-specific exception/material state
├── responsibility/participation context as applicable
├── Session(s) optional
├── Actual optional
├── Outcome optional
├── Confirmation optional
├── provider mapping
├── correction/reconciliation
└── history/provenance
```

Binding CP6 rule:

```text
recurrence_generated
!= explicit_extra
```

An `explicit_extra` belongs to the source context but must not falsely claim a Recurrence MaterialState generated it.

## 9.2 Identity survives movement

Current start/end cannot define Occurrence identity.

```text
Wednesday instance
original Wednesday 18:00
moved to Thursday 19:00
actual Thursday 19:12-20:24
```

is one Occurrence.

## 9.3 One-off owners do not need artificial Occurrence wrappers

```text
one-off Activity
→ Activity identity is sufficient

one-off Event
→ Event identity is sufficient
```

Occurrence exists because recurring/generative instance identity requires it.

## 9.4 Schedule optional

A flexible quota Occurrence may exist before exact placement.

```text
Occurrence != Schedule
```

## 9.5 Actual optional

An Occurrence may remain unresolved with no established Actual.

An unplanned Session/Observation/other reality may exist without prior Occurrence.

## 9.6 Persistent reconstructibility threshold

Future instances can remain virtual while untouched. Once meaningful instance-specific history exists—reschedule, skip, provider mapping, confirmation, actual execution, correction, etc.—the Occurrence must remain reconstructible even when source policy changes.

## 9.7 This occurrence versus this-and-future

```text
modify this occurrence
→ occurrence-specific state

modify this and future
→ source Routine/Event recurrence material-state revision
```

The Occurrence can serve as effective boundary without becoming the owner of future policy.

## 9.8 Provider mapping

Provider series IDs, instance IDs, original-start markers and detached-instance IDs map to DANTE Occurrence identity; they do not replace it.

## 9.9 Concurrent/offline edit requirement

Concurrent occurrence-specific edits may branch from the same material state. Version/reconciliation must preserve competing bases rather than blindly last-write-wins.

## 9.10 Occurrence non-collapse register

```text
Occurrence != Routine
Occurrence != recurring source/series
Occurrence != Recurrence
Occurrence != Activity
Occurrence != Event
Occurrence != Schedule
Occurrence != Session
Occurrence != Actual
Occurrence != Outcome
Occurrence identity != current timestamp
Occurrence identity != original datetime universally
Occurrence identity != provider instance id
recurrence_generated != explicit_extra
not-generated-by-rule != generated-and-skipped
virtual future instance != material history-bearing instance
```

---

# 10. Schedule — full vertical surface

Schedule is the current accepted temporal assignment of a schedulable subject.

## 10.1 Current subject family

- Activity;
- Event;
- Occurrence.

A subject may have multiple planned placements where semantics require split planned execution. Do not force one universal one-to-one subject/Schedule cardinality before the owning logical/physical contract says so.

## 10.2 Temporal forms and precision

Conceptually/current F0-compatible forms include:

- date span/date-only placement;
- floating local wall-clock;
- named-zone/zoned local placement;
- absolute instant placement;
- no current accepted placement.

Accepted temporal precision may also be coarser than an exact block where product semantics require it, for example:

```text
Tuesday
Tuesday afternoon
Tuesday at 18:00
Tuesday 18:00-20:00
start Tuesday 18:00 / end unresolved
```

Canonical boundaries:

```text
coarse accepted placement
!= exact timed block
!= all-day/date span automatically
!= unplaced
!= postponed/TBD
```

Frontend vocabulary and domain/physical vocabulary may differ in technical naming, but semantic distinctions must be preserved through adapters.

## 10.3 Accepted versus proposed

```text
proposal / solver suggestion / AI suggestion
!= accepted Schedule
```

A proposal becomes accepted only through applicable user instruction, Authority/Decision or explicitly authorized policy.

## 10.4 History

Preserve:

- original accepted expectation;
- each materially relevant Schedule revision;
- current accepted Schedule when one exists;
- proposer/source where consequential;
- applicable acceptance/authority basis where consequential;
- reason/context when known.

`current` must be explicit. It is not `latest UUID`, `highest row id`, or provider-most-recent value by assumption.

### 10.4.1 Activated B02-D absence and Undo rule

For the activated self-owned Activity/floating-local path, unschedule means real absence of the `schedule.placement` current binding. It closes the exact open history episode but retains Activity, Schedule, MaterialState payload and history.

```text
unschedule
!= delete Activity
!= delete Schedule
!= delete MaterialState/history
!= create placeholder MaterialState for absence
```

Guarded Undo is authorized by the exact unschedule receipt only while currentness is still absent and no later placement-history episode exists. Successful Undo creates a new immutable MaterialStateRef and a new history episode carrying the prior interval semantics; it never reopens an old history row. Newer truth conflicts instead of being overwritten.

## 10.5 Reschedule in either direction

Schedule changes may move:

- earlier;
- later;
- longer;
- shorter;
- only start;
- only end;
- from exact to coarser/unresolved or vice versa when semantics permit.

Do not hard-code `reschedule = later`.

## 10.6 Schedule change during execution

Explicit new expectation during execution can revise Schedule.

Actual deviation alone does not.

```text
planned 18:00-21:00
starts 17:40 and ends 20:15
→ Schedule remains 18:00-21:00 unless explicitly revised
→ Session/Actual records 17:40-20:15
```

Historical corrections to actual timing must correct Session/Actual, not rewrite Schedule merely to make them match.

## 10.7 Schedule and capacity

A Schedule does not automatically mean busy/capacity blocked.

```text
Schedule != Availability / Capacity Claim
```

## 10.8 Schedule non-collapse register

```text
Schedule != Activity
Schedule != Event
Schedule != Occurrence
Schedule != Routine
Schedule != Recurrence
Schedule != Temporal Constraint
Schedule != Deadline
Schedule != target date/window
Schedule != Availability
Schedule != Capacity Claim
Schedule != Session
Schedule != Actual
Schedule != proposal
scheduled != happened
coarse Schedule != exact block
all-day/date span != fake 24h timed occupancy
```

---

# 11. Temporal Constraint — full vertical surface

Temporal Constraint defines temporal admissibility/requirement/preference for a bounded target/facet. It does not choose the accepted Schedule and does not describe Actual.

## 11.1 Required semantic forms

Examples that must remain expressible:

- earliest start;
- latest start;
- latest completion/delivery;
- Deadline as specialized latest-bound Temporal Constraint;
- hard validity window;
- preferred/soft window;
- minimum/maximum duration;
- minimum contiguous Session duration;
- spacing/recovery requirement;
- relative-before/after relationship;
- open scheduling subject to other constraints;
- repeated applicability via Recurrence pattern where appropriate.

## 11.2 Hard versus soft

```text
hard constraint
→ defines planning admissibility unless explicitly overridden/changed under Authority

soft constraint
→ ranking/preference; may be violated with a valid explained plan
```

Constraint strength is separate from who can change the constraint.

## 11.3 Movement policy separation

```text
Temporal Constraint
= which placements are valid/preferred

Movement policy
= under what governance the accepted Schedule may be changed
```

## 11.4 Reality can violate planning rules

A hard planning constraint does not make contradictory real-world history impossible to record.

```text
constraint says finish by 20:00
Session actually ends 20:15
→ preserve Session/Actual
→ derive/report violation
```

Do not reject reality to protect planner assumptions.

## 11.5 Deadline semantics

A deadline must constrain a defined temporal facet when material:

- start;
- completion;
- delivery;
- arrival;
- another explicit relevant condition.

Do not universalize `deadline = end_at`.

Passing a deadline does not by itself prove `missed`, `not completed` or any other Outcome.

## 11.6 Window semantics

Identical range shape may mean:

- hard validity window;
- preferred window;
- Goal target window;
- Availability window;
- accepted Schedule window.

Shape is not semantics.

## 11.7 Temporal Constraint non-collapse register

```text
Temporal Constraint != Schedule
Temporal Constraint != Recurrence
Temporal Constraint != Availability / Capacity
Temporal Constraint != movement policy
Temporal Constraint != target date/window by default
Temporal Constraint != review date by default
Temporal Constraint != Dependency
Temporal Constraint violation != invalid Actual
deadline != universal due_at
```

---

# 12. Session — complete execution/runtime map

Session is a persistent record of one bounded logically continuous actual execution/performed-behavior episode.

## 12.1 Semantic tree

```text
Session
├── stable DANTE identity
├── actual execution interval
│   ├── start known
│   ├── end optional while running
│   ├── exact or approximate temporal precision
│   └── elapsed-only/retrospective cases where boundaries are uncertain
├── active/pause structure
│   ├── running
│   ├── pause
│   ├── resume
│   └── end/close
├── derived timing
│   ├── elapsed duration
│   ├── paused duration
│   └── active duration
├── execution context
│   ├── Activity optional
│   ├── Occurrence optional
│   ├── Event only when distinct executable episode exists
│   ├── Plan/other semantic context as relation where useful
│   └── descriptive spontaneous context allowed
├── capture provenance
│   ├── stopwatch/timer
│   ├── manual retrospective entry
│   ├── external import
│   └── authorized automatic capture
├── correction
│   ├── timing correction
│   ├── context correction
│   ├── split
│   ├── merge
│   └── false-data deletion/invalidation boundary
├── provider/device mapping
├── multi-device runtime state
├── measurements/Observations links
├── history/reconciliation
└── Timeline/analytics projections
```

## 12.2 Planned slice versus actual slice

```text
planned execution slice = Schedule placement
actual execution slice  = Session
```

Never persist future planned blocks as Session merely because UI language says `study session`.

## 12.3 Session may exist without Schedule

Spontaneous work is valid.

No retrospective fake Schedule should be invented.

## 12.4 Session may exist without pre-existing Activity

Unexpected debugging or other spontaneous execution can be recorded as Session with sufficient semantic context/provenance.

Do not fabricate historical intention.

## 12.5 Pause/resume identity

Pause does not automatically create a new Session.

```text
start 18:00
pause 18:40-18:50
resume
end 19:30
→ one Session
```

No universal pause threshold such as `>30 min => new Session` is accepted.

## 12.6 End then later restart

Explicit end/close followed by later restart normally creates a new Session related to the same Activity/Occurrence.

## 12.7 End Session != complete work

Ending execution only closes that episode.

```text
Session ended
!= Activity completed
!= Occurrence completed
!= Outcome established
```

## 12.8 Capture mechanism != Session type

Timer, manual, imported and automatic capture affect Provenance/confidence/reconciliation, not the semantic Session type.

```text
Timer / Stopwatch != Session
```

## 12.9 Correction preserves identity

Correcting 18:05→17:55 start time normally keeps the same Session identity.

## 12.10 Split / merge

Split when one captured interval actually represented several meaningful execution episodes.

Merge when accidental fragmentation represented one real continuous episode.

Both are reconciliation/correction operations and must preserve lineage to original capture.

## 12.11 Deletion versus correction

```text
real episode + wrong timing/context
→ correction

captured record was false/nonexistent
→ deletion/invalidation according to data-history policy
```

Delete-and-recreate must not be the default correction strategy.

## 12.12 Measurements/Observations

Session may contextualize heart rate, distance, pages, route, focus rating, etc. Those values do not belong in an arbitrary universal Session JSON metadata blob merely because they happened during the Session.

## 12.13 Internal segments

Workout laps/phases or specialist segments do not automatically require separate Sessions or a universal SessionSegment kernel primitive.

## 12.14 Overlapping Sessions

Global non-overlap is forbidden as a universal invariant.

Valid example:

```text
Walking 17:00-18:00
English listening 17:00-18:00
```

Potentially suspicious overlap can be surfaced by semantic compatibility rules without a blanket DB exclusion constraint.

## 12.15 Overlap-aware aggregation

For overlapping Sessions distinguish:

- category/domain time;
- elapsed Session duration;
- active effort;
- unique wall-clock coverage;
- intentionally double-counted multi-domain contribution.

```text
SUM(session.duration) != total unique day time universally
```

## 12.16 Multi-intention Session

One real episode may support more than one intention/Goal/context. Do not duplicate identical Session records merely to attach several semantic relationships.

At the same time, Session must not become an arbitrary list-of-everything relation blob. Exact relation semantics remain under the Relationship model.

## 12.17 Event attendance boundary

Ordinary Event occurrence/attendance does not require Session.

Create Session for Event context only when there is a distinct executable episode, e.g. hands-on coding during a workshop.

## 12.18 Stale running Session

A running Session may become stale because of crash/device loss/forgotten timer.

DANTE may detect anomaly and propose closure/correction, but must not silently fabricate end time or split based on an arbitrary threshold.

## 12.19 Multi-surface runtime

The vertical must eventually support the same canonical execution episode being observed/controlled from multiple clients:

```text
Web
Mobile/App
future device/capture surface
```

Required runtime problems to handle explicitly:

- source device/application provenance;
- operation idempotency;
- expected current Session state/revision;
- concurrent pause/resume/end operations;
- client offline period;
- reconnect/replay;
- stale running Session recovery;
- device clock drift;
- duplicate timer/import reconciliation;
- current accepted state after conflict;
- local pending state versus server-authoritative state.

No silent last-write-wins rule is authorized merely because implementation would be easier.

## 12.20 Session non-collapse register

```text
Session != Schedule
Session != Activity
Session != Occurrence
Session != Routine
Session != Event actual attendance by default
Session != broader Actual
Session != Outcome
Session != Timer
Session != Stopwatch
Session identity != start/end timestamps
Session identity != provider record id
pause != Session boundary by default
end Session != work completion
```

---

# 13. Actual — complete realization map

Actual is the contextual realization record answering **how a specific intended/expected subject resolved in reality**.

## 13.1 Subject family

Primary expectation subjects in this vertical:

- Activity;
- Event;
- Occurrence.

Observed reality without a prior expectation does not require an Actual wrapper.

## 13.2 Semantic tree

```text
Actual
├── stable contextual identity
├── exact intended/expected subject
├── realization state
│   ├── fully realized
│   ├── partially realized
│   ├── differently realized
│   ├── known non-realization
│   ├── replacement/substitution context
│   └── other contextual realization semantics
├── actual temporal facts where applicable
├── Session basis 0..N where applicable
├── Participation facets where applicable
├── Observation/Measurement links where applicable
├── Outcome optional
├── Confirmation optional
├── Provenance/assertion basis
├── current accepted material state
├── competing assertions/reconciliation
└── correction/history
```

## 13.3 Unknown versus known non-realization

```text
no established Actual
!= known non-realization
```

Expected time passing, silence, missing provider event or lack of Session cannot silently create `missed`, `skipped`, `failed` or `not performed`.

## 13.4 One broader Actual may aggregate several Sessions

An Activity may be executed across multiple Sessions while one contextual Actual describes how the Activity expectation was realized overall.

Do not create one Actual per Session by default.

## 13.5 Event Actual without Session

An ordinary Event can have actual start/end and participation/outcome semantics without any Session.

## 13.6 Measurements remain external facts

Distance, heart rate, pages, score, difficulty, etc. remain Observation/Measurement semantics where appropriate.

Do not copy them into a universal Actual mega-record.

## 13.7 Replacement/substitution

Original expectation is preserved even when reality used an alternative.

```text
Activity A expected
→ Actual A not realized as planned
→ replacement relation to alternative execution/object
→ Outcome A may say replaced
```

Do not rewrite Activity A into the replacement.

## 13.8 Shared versus actor-specific reality

Shared Event Actual does not establish identical participation for every actor.

Actual performer, recorder, responsible actor and subject may all differ.

## 13.9 Competing assertions

Provider/user/other actor assertions can coexist while current Actual remains unresolved or is reconciled under applicable Authority/Decision/policy.

```text
assertion != established Actual automatically
```

## 13.10 Actual non-collapse register

```text
Actual != Activity
Actual != Event
Actual != Occurrence
Actual != Schedule
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
Actual != universal reality log
no Actual != failed/skipped/missed
source report != Actual truth automatically
```

---

# 14. Outcome — complete result/disposition map

Outcome answers **what resulted from this realized expectation in the relevant context**.

## 14.1 Optional/contextual

Not every Actual needs Outcome.

Ordinary Event occurrence may be fully represented without a result/disposition when no such result matters.

## 14.2 Contextual vocabulary

Possible result terms depend on context, e.g.:

- completed;
- partially completed;
- skipped;
- known not performed;
- replaced;
- passed/failed;
- approved/rejected;
- decision reached/deferred;
- changes requested;
- resolved/unresolved.

No universal Outcome enum is accepted.

## 14.3 Lifecycle state separation

`closed`, `cancelled`, `in progress`, etc. are operational/lifecycle semantics and do not automatically define Outcome.

Some words may appear in ordinary language in both dimensions; semantic owner/context decides meaning.

## 14.4 Observation/artifact separation

```text
exam score 78/100 = Observation
passed             = Outcome

report.pdf          = Artifact
completed/accepted  = Outcome where meaningful
```

## 14.5 Unknown versus negative

```text
no Outcome
!= negative Outcome
```

`unconfirmed` is epistemic/Confirmation state, not a universal Outcome value.

## 14.6 Partial != failure

Meaning of partial depends on criterion/context. Outcome alone does not decide Goal success or failure.

## 14.7 Shared outcome

Shared Event/Activity Outcome does not flatten actor-specific participation/consequences.

## 14.8 Correction

Outcome correction preserves prior assertions/material states and source history.

## 14.9 Outcome non-collapse register

```text
Outcome != Actual
Outcome != Session
Outcome != Observation
Outcome != Artifact
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
Outcome != universal lifecycle status
no Outcome != failed
```

---

# 15. Confirmation — required resolution capability

Confirmation is a contextual actor-scoped attestation that a specific confirmer affirms a specific material version of a target for a defined purpose/context.

## 15.1 Target/version semantics

A Confirmation may target a specific:

- Actual state;
- Outcome state;
- Observation/assertion;
- schedule/change or another confirmable target where semantics justify it.

It binds to the material state actually affirmed.

```text
Actual S1
└── Confirmation C1

Actual corrected to S2
→ C1 remains historical confirmation of S1
→ C1 does not silently confirm S2
```

## 15.2 Actor/purpose

Preserve where material:

- confirmer Actor;
- actual acting Actor versus represented party;
- target/material state;
- purpose/context;
- relevant time;
- Provenance of the Confirmation itself;
- retraction/supersession history where required.

## 15.3 Conflicting Confirmations

Different actors may legitimately confirm/conflict differently.

One actor's Confirmation is not universal group truth.

## 15.4 Awaiting confirmation is derived

```text
policy requires qualifying Confirmation
+
none exists
→ awaiting / needs Confirmation
```

Do not create negative fake Confirmation rows.

## 15.5 Automation/AI

Explicitly authorized policy may establish an Outcome/Actual without fabricating human Confirmation.

AI confidence/inference does not become human Confirmation.

## 15.6 One UI action may produce multiple semantics

A simple `Fatto` / `Conferma` interaction may, depending on the exact workflow, establish:

- Actual;
- Outcome;
- Confirmation.

The UI can be one-tap while the application/domain consequences remain distinct and atomic.

## 15.7 Confirmation non-collapse register

```text
Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Provenance
Confirmation != Acknowledgement
Confirmation != Participation acceptance
Confirmation != Agreement
Confirmation != Consent
Confirmation != Verification
Confirmation != Authority
Confirmation != Decision
Confirmation != Approval
Confirmation != Visibility
no Confirmation != false/rejected/not-performed
```

---

# 16. Acknowledgement — common-ground boundary

Acknowledgement is explicit actor-scoped taking-notice of a specific target/material version/change/request in a context.

It is optional and consequence-sensitive; ordinary low-risk personal scheduling does not need universal acknowledgement bureaucracy.

Relevant vertical examples:

- material shared Schedule change;
- Responsibility hand-off request;
- changed Event time;
- instruction/update whose explicit common ground matters.

## 16.1 Transport/read telemetry separation

```text
sent
!= delivered
!= displayed/read
!= acknowledged
```

Provider read receipts, UI visibility or telemetry cannot fabricate human Acknowledgement.

## 16.2 Material revision

Acknowledgement of Schedule version S1 does not silently acknowledge materially changed S2.

## 16.3 Acknowledgement non-collapse register

```text
Acknowledgement != Confirmation
Acknowledgement != understanding
Acknowledgement != Acceptance
Acknowledgement != Agreement
Acknowledgement != Consent
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority
Acknowledgement != Decision/Approval
Acknowledgement != effective domain change
Acknowledgement != Actual
silence != Acknowledgement
```

---

# 17. Resolution Queue / Review / automatic outcomes

This is a first-class product workflow but **derived**, not a canonical status root.

## 17.1 Resolution reasons

An item may appear in resolution because:

- expected window ended and Actual is unknown;
- Outcome is required but absent;
- applicable policy requires Confirmation;
- imported/provider assertion conflicts with current state;
- Session appears stale or anomalous;
- correction/reconciliation needs user choice;
- follow-up/replanning is materially blocked by unresolved truth.

## 17.2 Product projection

```text
Resolution Queue / Da risolvere
├── why unresolved
├── exact target/material state
├── quick action when safe
│   ├── Fatto
│   ├── Parziale
│   ├── Saltato
│   ├── Posticipato
│   ├── Sostituito
│   └── other context-specific result
├── Conferma
├── Correggi
├── Vedi dettagli
└── batch/review workflow
```

The visible quick labels must map to exact underlying operations rather than one universal `status` field.

## 17.3 Review cadence

Product policy may request resolution:

- immediately after an important item;
- later in the day;
- end-of-day review;
- selected weekday review;
- weekly review;
- end of Routine/Program cycle;
- only if unresolved truth blocks future planning/statistics.

Grouping multiple unresolved items into one review is preferred over repeated intrusive notifications where user policy allows.

## 17.4 Confirmation policy hierarchy

Policy may be configured at progressively specific levels such as:

1. global default;
2. category/module/life-context default where supported;
3. Routine/Program default;
4. individual item/Occurrence override.

More-specific product policy may override broader defaults only under the owning governance rules.

## 17.5 Automatic outcomes

Possible explicitly configured policies may include:

- ask immediately;
- ask later;
- add to daily/weekly review;
- leave unresolved silently;
- establish a bounded automatic outcome;
- infer provisional result from trusted integration and request confirmation only when uncertain.

Automatic completion/non-completion must never become a hidden universal default.

Automatic effect must preserve its source/policy Provenance and must not masquerade as direct human Confirmation.

## 17.6 Resolution Queue non-collapse register

```text
Resolution Queue != Notification feed
Resolution Queue != canonical state machine
awaiting Confirmation != Confirmation record
unresolved != failed
silence != known non-realization
```

---

# 18. Conditional Policy / Reminder / notification boundary

Conditional Policy describes a bounded downstream response when a qualifying activation basis is established.

## 18.1 Canonical shape

```text
qualifying event/state/evaluation/time
        ↓
activation basis established
        ↓
Conditional Policy
        ↓
bounded downstream response
```

Example:

```text
Schedule window ended
AND realization still unresolved
→ include in end-of-day review
```

## 18.2 Activation semantics

The runtime must keep distinct:

```text
when state crosses a threshold
!= while state remains qualifying
!= on every new qualifying observation/import
```

Duplicate provider/import facts must not automatically create duplicate semantic effects.

## 18.3 Reminder semantics

A Reminder/notification is a possible **response**, not the Conditional Policy itself and not Trigger identity.

```text
Conditional Policy != Reminder
Trigger != Reminder
Reminder delivery != Outcome
policy activated != response succeeded
```

## 18.4 User notification controls

Product policy may include:

- push vs in-app vs review-only;
- quiet hours;
- maximum reminder repetition;
- priority thresholds;
- whether unresolved items trigger replanning;
- whether an explicit user choice should be reusable for similar future items.

A one-time response must not silently become a permanent preference.

## 18.5 Delivery boundary

This vertical may own reminder intent/policy relation. Real push/email/provider delivery belongs to notification infrastructure and must expose truthful pending/sent/failed/delivered states where implemented.

## 18.6 Conditional Policy non-collapse register

```text
Conditional Policy != Dependency
Conditional Policy != Criterion/Evaluation
Conditional Policy != Recurrence
Conditional Policy != Temporal Constraint
Conditional Policy != Schedule
Conditional Policy != Decision
Conditional Policy != Authority
Conditional Policy != Proposal/Request
Conditional Policy != Actual
Conditional Policy != Reminder/Notification
Conditional Policy != generic Workflow/Automation root
Trigger != standalone universal entity/root
```

---

# 19. Lifecycle / operational disposition / replanning

A single `status` field is insufficient and forbidden as the universal lifecycle model.

## 19.1 Planning/operational vocabulary may include

Depending on owning type and context:

- planned;
- available;
- in progress;
- rescheduled;
- postponed;
- suspended;
- cancelled;
- expired;
- closed.

These are not universal values applicable identically to every owner.

Rescheduled/postponed history must remain reconstructible even after current state advances.

## 19.2 Execution/result vocabulary is separate

Depending on context:

- completed;
- partially completed;
- skipped;
- missed;
- replaced;
- explicitly not completed;
- not applicable;
- unresolved/unconfirmed as epistemic workflow, not universal Outcome type.

## 19.3 Attendance is separate again

Event participation may record:

- invited;
- accepted;
- tentative;
- declined;
- attended;
- partially attended;
- did not attend;
- unknown.

Do not collapse this into Activity completion or Event state.

## 19.4 Movement policy

Required conceptual choices:

- locked;
- movable inside valid window;
- movable only after user confirmation/decision;
- freely replannable under applicable priorities/constraints/policy.

Movement policy may differ for one Occurrence versus the originating Routine/Program.

## 19.5 Divisibility/execution policy

Activity/planning item may be:

- indivisible;
- divisible into Sessions;
- partially completable;
- allowed to finish early when result is reached;
- mergeable with compatible execution where semantics allow;
- constrained by minimum Session duration;
- constrained by spacing/recovery/preparation.

These are not all Schedule fields and not all Activity table columns by default.

## 19.6 Fallback choices

When the original plan is no longer feasible, applicable policy/proposal may support:

- skip without replacement;
- postpone in valid range;
- move to another valid date;
- equivalent replacement;
- shorten;
- split;
- preserve highest-priority portion;
- replan dependencies;
- replan surrounding day/week/range;
- revise the remaining Routine/Program where separately authorized.

## 19.7 Replanning scope

Potential scopes:

- selected item;
- selected linked items/dependencies;
- current day;
- current week;
- remaining range;
- remaining Routine/Program.

Use the smallest scope that restores a valid useful plan, expanding only when necessary.

## 19.8 One occurrence / selected / future / whole source

Any edit capable of changing recurrence/source policy must expose scope semantics equivalent to:

- this occurrence only;
- this occurrence + selected linked items;
- this and future occurrences;
- whole Routine/Program/source policy.

## 19.9 Proposal versus accepted effect

Material replans must show affected items/constraints and remain proposals until authorized unless the user has explicitly enabled deterministic bounded automation.

## 19.10 Replanning non-collapse register

```text
reschedule != Actual deviation
postpone != skip
skip Occurrence != pause Routine
pause Routine != end Routine
replacement != rewrite original intention
constraint violation != known failure
proposal != applied effect
```

---

# 20. Product organization — Calendar / Life Area / Context / Tags

The user's `Palestra`, `Inglese`, `Lavoro`, `Famiglia`, etc. requirement has a product-level home: Calendar / Life Area organization.

## 20.1 Primary organizational context

Product requirement:

- planning items can be organized into calendars/life areas such as Personal, Work, Family, Study, Health/training, Travel, Creative projects or user-defined contexts;
- one planning item has one primary organizational calendar/life area in the product model;
- the same item may also have tags, Goal/Plan links, participants and other relations;
- organization must not duplicate the item across areas.

Example:

```text
Life Area: Inglese
├── Activity: Study chapter 3
├── Event: Lesson with teacher
├── Routine: Conversation practice 3x/week
└── related Occurrences/Sessions in derived views
```

## 20.2 Life Area versus Goal

A Goal may share the same visible label without being the same object.

```text
Goal: Imparare inglese
Life Area: Inglese
```

The Goal may complete/change while the organizational area remains useful.

```text
Life Area != Goal
Life Area != Plan
Life Area != Routine
Life Area != Tag
Life Area != Place
Life Area != external provider calendar source
```

## 20.3 Organization lifecycle

The product capability may require:

- create;
- rename;
- reorder;
- archive;
- hide/show;
- icon/color appearance;
- external-calendar mapping;
- actor-local organization of a shared item.

Grouping/filtering is projection choice, not scheduling-truth boundary. A hidden relevant commitment must not disappear from authorized conflict reasoning.

## 20.4 Sharing is separate

Personal/Work/etc. are organization. Shared/private is a separate participant/visibility property.

The same shared Event may be organized into different local Life Areas by different participants without duplicating shared canonical Event reality.

## 20.5 External calendar mapping

External calendars may map to a local Life Area or remain separate sources.

```text
external source identity != local organizational context
```

## 20.6 Tags

Tags are secondary many-valued organization/filter semantics and must not be used to fake primary ownership, Goal links, Participation, Place or provider source.

## 20.7 Context versus appearance

Current frontend contract already requires:

```text
Context/grouping membership != appearance
```

Color/icon/presentation override does not establish semantic organization/ownership. Color must not be the sole carrier of semantic state.

## 20.8 Existing Timeline prototype groups

Current Timeline group labels such as Focus/Riunioni/Salute/Creatività/Personale/Urgenze are historical frontend prototype vocabulary, not Domain taxonomy.

Future integration must map/reconcile product organization explicitly rather than promoting those hard-coded strings into canonical ontology.

## 20.9 Exact persistence caution

This semantic map requires the product organizational capability to be represented in the vertical integration, but does **not** invent a new PostgreSQL table/entity if the current Logical/Physical model uses another accepted mapping or has intentionally deferred this owner.

The implementation slice must verify exact current Logical/Physical coverage before any DDL/API write.

---

# 21. Temporal infrastructure — Clock, precision, timezone, DST, ranges

These are internal/shared capabilities but mandatory for correctness.

## 21.1 Clock

Time is an explicit dependency.

- production/system Clock;
- fixed deterministic Clock for tests/prototypes;
- ability to derive `today` in an explicit zone.

Do not hard-code prototype dates or rely on ambient system time inside domain/application tests.

## 21.2 Temporal forms

Keep distinct:

```text
date-only / date span
floating local wall-clock
named-zone/zoned local time
absolute instant
coarse accepted temporal precision where applicable
```

No form is silently converted to another.

## 21.3 Date-span semantics

All-day/date-only semantics must not be implemented as fake 00:00–24:00 timed occupation.

Current C1 uses a real per-day all-day lane.

## 21.4 DST

Named-zone/local ranges must handle:

- ordinary local times;
- ambiguous repeated local times;
- nonexistent local times;
- 23-hour local day;
- 25-hour local day.

Range queries must not assume every local day equals exactly 24 hours.

## 21.5 Travel/timezone policy

Wall-clock recurrence/scheduling may be:

- home/named-zone anchored;
- current-local/floating;
- absolute.

Do not infer travel behavior solely from current device zone.

## 21.6 Actual precision

Actual/Session timing may be:

- tracker-recorded exact instant;
- manually entered approximate time;
- rounded provider time;
- start known/end unknown;
- duration known while exact boundaries uncertain.

Do not manufacture timestamp precision not present in source data.

---

# 22. History / Version / current accepted state / Provenance / Reconciliation

## 22.1 Identity versus material state

```text
owner identity != material state/version
```

Ordinary correction/reschedule/revision preserves owner identity unless evidence demonstrates a genuinely different real-world object/expectation.

## 22.2 Explicit current accepted state

```text
current accepted state
!= newest UUID
!= highest integer revision
!= provider-most-recent record
!= last row inserted
```

Current state must be governed by the accepted material/current binding semantics.

## 22.3 Correction

Correction changes current accepted representation while retaining enough prior state/assertion lineage to explain history.

```text
correction != delete history
```

## 22.4 Version/material equivalence

A material change for the relevant facet/purpose may invalidate prior Confirmation/Acknowledgement/Decision applicability.

A technical ETag/hash/storage revision does not automatically imply semantic material change.

## 22.5 Provenance

Where consequential, preserve:

- source/importer/recorder;
- provider/device;
- assertion time/effective time;
- original value/state;
- correction source;
- policy/decision basis;
- represented actor/on-behalf-of basis where material.

Provenance explains lineage, not truth by itself.

## 22.6 Reconciliation

Reconciliation may:

- compare competing assertions;
- keep conflict unresolved;
- select/construct a current interpretation under policy/Authority;
- correct/split/merge records;
- preserve provider and user versions.

No universal winner rule such as newest/provider/user/AI/highest-priority is accepted.

## 22.7 Native/scoped/material/external references

Existing reference families remain internal infrastructure:

- NativeRef;
- ScopedRecordRef;
- MaterialStateRef;
- ExternalRef.

They must not leak as user-facing top-level concepts.

---

# 23. Provider / external reconciliation boundary

## 23.1 Event/provider identity

```text
DANTE Event identity != Google/Microsoft/provider event id
DANTE Occurrence identity != provider recurring-instance id
DANTE Schedule != provider start/end row automatically
```

Provider updates are assertions/integration inputs that require appropriate reconciliation under the owning policy.

## 23.2 Session/provider identity

Imported Session-like records preserve:

- provider;
- external record id;
- source app/device;
- source revision/version;
- import/update time;
- deletion/tombstone where exposed.

DANTE Session identity remains separate.

## 23.3 User correction after import

A later provider update must not silently erase a user-confirmed correction or masquerade as though corrected values were provider-original.

## 23.4 Recurrence interoperability

External RRULE/provider recurrence formats are adapters.

If a DANTE recurrence family cannot map losslessly, allowed integration choices include explicit unsupported state, controlled degradation, extra metadata or multiple provider objects. Do not weaken internal semantics merely for export convenience.

## 23.5 External side-effect truth

Authored provider intent does not equal successful provider execution.

```text
intent authored
!= request sent
!= provider accepted
!= remote canonical effect
```

The UI must never claim fake provider/backend success.

---

# 24. Input-surface convergence

Every product input surface must converge onto the same governed application/domain operations rather than reimplementing semantics independently.

Potential surfaces:

- Timeline `+`;
- C1 Create;
- double-click/Shift-range prefill;
- card drag;
- anchored time editor;
- Planning Tray placement;
- future structured Detail;
- Context Rail quick resolution;
- mobile controls;
- keyboard/command surface;
- future AI/NL;
- future voice;
- provider/import adapter.

Canonical architecture direction:

```text
input surface
→ typed/bounded application command
→ validation/precondition
→ application port/service
→ authoritative adapter/domain operation
→ truthful result
→ projection refresh
```

## 24.1 F0 inherited operation semantics

Current F0 already fixes:

- operationId idempotency;
- rejection of idempotency-key collision when payload/command differs;
- expected projection revision for mutations;
- stale write rejection;
- explicit result classes `applied / no-op / rejected / failed`;
- `pending != success`;
- guarded Undo;
- monotonic revisions after Undo;
- subscriber updates only on applied mutation;
- no fake network/storage/backend semantics.

Later real vertical operations must preserve equivalent correctness even if transport/API shape changes.

## 24.2 Direct component transport is not target architecture

```text
UI component
→ feature/application adapter
→ data-source/application port
→ transport client
→ DANTE backend
```

No direct arbitrary component `fetch()`/provider SDK coupling.

## 24.3 Manual/AI/voice non-collapse

```text
manual Create != AI interpretation != voice capture
```

but all three may ultimately call the same authorized domain operations after their distinct interpretation/proposal layer.

AI output remains proposal/inference unless the applicable operation policy/Authority allows direct bounded effect.

---

# 25. Timeline / Planning Tray / Detail / Resolution / range read models

## 25.1 Timeline

Timeline is a derived product/query projection over canonical temporal owners/facets.

```text
Timeline != canonical state
Timeline != universal Fact log
Timeline != event store
Timeline != history table
Timeline card != DB row
Timeline card != backend DTO
```

## 25.2 Frozen T1 behavior

Vertical implementation must preserve the frozen T1 contract unless the user explicitly authorizes a product behavior change.

Protected behavior includes:

- custom drag;
- first gesture works even when another card is focused;
- deselect-first focus grammar;
- no browser ghost/text selection;
- title/time/subitem explicit action regions;
- deterministic compact overlap;
- expanded group geometry alignment;
- move + Undo;
- anchored time editor;
- Firefox pointer/focus regression contract.

Backend integration is not permission to redesign Timeline behavior.

## 25.3 Planning Tray

Current product owner is unplaced Activity.

Required semantics:

- Activity may be created with no Schedule;
- Planning Tray shows that unplaced work;
- placing it changes Schedule of the same Activity identity;
- Escape cancellation/Undo remain operation semantics;
- no duplicate identity.

Do not silently equate these different reasons for no visible timed placement:

```text
unplaced Activity
!= Event postponed with date TBD
!= flexible Occurrence awaiting exact Schedule
```

A future unified UI may show multiple categories only if the read model keeps the reason/type explicit.

## 25.4 Resolution Queue

Derived projection of exact unresolved semantic questions. Not a generic notification feed.

## 25.5 Detail/History

Future C2 consumes existing semantics. It must not reinterpret card ViewModel fields as canonical DTO/DB fields.

## 25.6 Backend range-query bridge

Target path:

```text
canonical Activity/Event/Routine/Occurrence/provider-backed sources
→ application/backend temporal range query
→ normalized Timeline read model
→ Timeline engine
```

Range query must eventually define:

- temporal window semantics;
- user-local zone/day interpretation;
- paging/cursor/horizon;
- stable identity;
- provenance/source identity where relevant;
- recurrence materialization output;
- current/history selection;
- all-day/date-span handling;
- coarse placement handling;
- postponed/unplaced classification;
- cancellation/visibility filtering;
- partial/next-page determinism.

Browser-generated canonical recurring cards are forbidden.

---

# 26. Analytics / Statistics / Signals

Analytics is derived from accepted canonical history; it is not another mutable truth owner.

## 26.1 Safe base measures where source data exists

Potential base measures include:

- scheduled duration;
- Session elapsed duration;
- Session active duration;
- paused duration;
- start/end deviation against the correct accepted Schedule version;
- overrun/underrun;
- Schedule revision/reschedule count;
- postpone/cancel/skip patterns;
- Occurrence expected count;
- Actual establishment coverage;
- Outcome distributions by owning context;
- Confirmation coverage when applicable;
- time allocation by Life Area/tag/context;
- recurring conflict/overload counts;
- range-based week/month/year summaries.

## 26.2 Derived Routine analytics

Adherence/streak/consistency require explicit evaluation over:

- expected Occurrences;
- Actuals;
- Outcomes;
- confirmation policy/current accepted truth;
- period boundaries;
- possibly domain-specific criteria.

Do not derive adherence solely from Session existence.

## 26.3 Planned versus actual

Keep separate:

- estimated effort;
- scheduled time;
- actual elapsed time;
- actual active time;
- outcome/quantity results.

## 26.4 Overlap-aware time totals

Never universalize raw Session duration sum into `time spent today`.

Analytics should distinguish unique wall-clock coverage from domain/category contribution and deliberate overlapping behavior.

## 26.5 Corrected current value versus audit history

Statistics should normally use current corrected accepted truth for the requested analytical purpose while audit/history retains prior assertions/corrections.

## 26.6 No universal productivity ontology

Do not invent generic canonical measures such as:

- productivity score;
- success score;
- performance score;
- failure rate;

unless a later product/criterion design defines exact semantics.

Analytics may compare factual patterns without turning them into moral/evaluative labels.

## 26.7 Product analytics != observability

User-facing behavioral/time statistics are distinct from OTel/Grafana operational telemetry. An observability failure cannot change canonical temporal semantics.

---

# 27. Undo / correction / reopen / delete / archive are different

```text
Undo
= reverse a recent supported operation only if newer truth does not make reversal unsafe

Correction
= current accepted representation of a real historical fact/state changes

Reopen
= owning lifecycle becomes active again where semantics allow

Delete / invalidate
= false/invalid data or retention action according to policy

Archive / hide
= organization/visibility lifecycle, not correction of historical reality
```

F0 guardrail:

- Undo requires the exact expected revision/state produced by the original mutation;
- newer truth causes `undo-conflict` rather than blind overwrite;
- successful Undo creates a new monotonic revision rather than rewinding version counters.

Retention/privacy requirements may separately allow deletion/export/aggregation reduction; these data-governance operations must not be conflated with semantic correction.

---

# 28. Persistence/runtime integrity inherited from Logical/Physical/CP6

## 28.1 Historical CP6 baseline versus current protected-main truth

Historical CP6 concrete closure remains valid historical evidence:

```text
Alembic 20260826_08
68 tables
5 views
14 routines
75 triggers
95 indexes
68 FKs
120 CHECKs
```

It is **not** the current protected-main topology.

Current authoritative pre-vertical database truth at the freeze anchor is:

```text
PostgreSQL 18.6
Alembic 20260906_18
89 tables
5 views
18 routines
77 triggers
173 physical indexes
91 foreign keys
272 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

Every implementation slice must reverify current protected `main` and Alembic head immediately before work, because the roadmap freeze snapshot is not permission to assume the repository never changes.

## 28.2 Existing material-state facets relevant here

CP6 inventory already includes material-state semantics for at least:

- `schedule.placement`;
- `actual.realization`;
- `session.timing`;
- `routine.recurrence`;
- `event.recurrence`.

Exact current tables/columns/routines must be read from current Database Architecture & Dictionary and Alembic before vertical implementation.

## 28.3 Existing baseline does not equal product completeness

CP6 intentionally established semantic identity/material-history foundations without speculatively materializing every product payload/relation.

Examples requiring explicit per-slice physical proof include:

- Activity/Event/Routine descriptive product state;
- Temporal Constraint persistence;
- Outcome persistence;
- Confirmation/Acknowledgement persistence;
- Session execution-context relations;
- Life Area/product organization;
- advanced recurrence families;
- provider/offline mappings beyond current baseline;
- analytics materialization if ever justified.

## 28.4 Newly explicit semantic capability does not imply new DDL

Adding a requirement to this map does not authorize:

- generic `confirmations` table;
- generic `status` column;
- generic `timeline_entries` table;
- generic relationship table;
- generic JSON escape hatch;
- new Alembic revision by default.

The implementation slice must first map each requirement to existing Logical/Physical ownership and prove a real gap before DDL.

## 28.5 Idempotency/concurrency

Real mutations must classify:

- idempotency scope;
- immutable operation fingerprint;
- expected-state/concurrency behavior;
- retry safety;
- partial/async success semantics;
- reconciliation/failure recovery;
- Undo/reversal eligibility.

## 28.6 Canonical truth and local sync

Local/mobile/synced copies remain noncanonical.

Consequential offline mutations must reconcile/revalidate through the accepted backend path before being represented as authoritative canonical truth.

## 28.7 Recovery and anti-resurrection

Backup/PITR restores bytes, not semantic acceptance automatically. New temporal current-state/history/outbox data must be compatible with existing recovery/anti-resurrection doctrine before closure.

---

# 29. Master non-collapse / `!=` register

The following rules are blocking boundaries for roadmap and implementation review.

## 29.1 Owner boundaries

```text
Activity != Event != Routine
Activity != Goal != Plan
Routine != recurring Event
Occurrence != Activity/Event/Routine
one-off Activity/Event != automatic Occurrence wrapper
```

## 29.2 Temporal boundaries

```text
Schedule != Temporal Constraint
Schedule != Recurrence
Schedule != Occurrence
Schedule != Session
Schedule != Actual
Schedule != Availability / Capacity
Deadline != Schedule
Target date != Deadline by default
Review date != Temporal Constraint by default
wall-clock recurrence != elapsed recurrence
coarse Schedule != exact time block
all-day/date span != fake 24h timed occupancy
```

## 29.3 Reality/result boundaries

```text
Session != Actual
Actual != Outcome
Actual != Observation
Outcome != Observation
Outcome != Artifact
Outcome != lifecycle status
no Actual != known non-realization
no Outcome != negative Outcome
Session ended != Activity completed
passage of time != Actual/Outcome
```

## 29.4 Epistemic/common-ground boundaries

```text
Confirmation != Actual
Confirmation != Outcome
Confirmation != Provenance
Confirmation != Acknowledgement
Acknowledgement != read/delivered telemetry
Acknowledgement != Confirmation
Acknowledgement != Participation response
Acknowledgement != Authority/effect
no Confirmation != false
silence != acknowledgement/confirmation/non-realization
```

## 29.5 Organization boundaries

```text
Life Area != Goal
Life Area != Plan
Life Area != Tag
Life Area != Place
Life Area != external calendar source
Context != appearance
shared != Calendar/Life Area
frontend prototype group != Domain taxonomy
hidden in projection != nonexistent
```

## 29.6 Recurrence/generation boundaries

```text
Routine != Recurrence
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Conditional Policy
recurrence rule != browser-generated future cards
this occurrence change != future source-policy revision
observed repeated Sessions != Routine intent
recurrence_generated != explicit_extra
not-generated-by-rule != generated-and-skipped
pattern anchor != effective range
expected occurrence count != successful completion count
```

## 29.7 Session/runtime boundaries

```text
Timer/Stopwatch != Session
pause != Session boundary by default
Session identity != timestamps
Session identity != provider id
manual/timer/import != Session semantic type
one Activity/Occurrence may have 0..N Sessions
Schedule placement and Session do not require 1:1 cardinality
Session overlap != universal conflict
AuthSession != DANTE Session
```

## 29.8 Actor boundaries

```text
Person != Account != Principal != Actor
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Authority/Visibility/Ownership
Participation response != Actual Participation
accepted != attended
declined != established absence
Participation != Session
Participation != Responsibility
```

## 29.9 Provider/application boundaries

```text
provider identity != DANTE identity
provider assertion != canonical truth automatically
frontend ViewModel != backend DTO != persistence row
local sync copy != canonical truth
pending != success
retry != duplicate effect
idempotency key != Domain identity
Undo != blind overwrite
AI output != accepted fact
proposal != accepted effect
product analytics != observability telemetry
```

---

# 30. Explicit anti-pattern register

Do not introduce for convenience:

- generic Task kernel primitive;
- generic TimelineEntry;
- generic Entity / Thing;
- generic Fact;
- universal generic Version root where accepted owner-specific MaterialState semantics exist;
- generic Relationship used to erase specific relation meaning;
- generic Status;
- generic `confirmed` boolean;
- generic `done` boolean;
- ambiguous `assigned_to`;
- ambiguous `owner_id`;
- generic `due_at`;
- Activity `repeat` boolean;
- one-table-fits-all temporal object;
- universal SessionSegment primitive without specialist proof;
- universal EventSeries/MeetingSeries primitive without materially distinct identity proof;
- provider RRULE as DANTE recurrence ontology;
- browser recurrence engine producing canonical future Occurrences;
- `SUM(session.duration)` as universal total-time metric;
- silent last-write-wins for multi-device/provider conflict;
- fake retrospective Schedule created to match Actual;
- fake Session created for every Event attendance;
- fake Activity created for every Event attendance;
- fake Outcome created because time passed;
- fake human Confirmation from automation/AI;
- JSON payloads used to bypass required typed semantics;
- direct component provider/backend SDK calls as feature architecture;
- fake backend/provider/notification success in frontend;
- normal-runtime fake Timeline cards or mock repositories after real-data cutover.

---

# 31. Detailed coverage audit — previously missing/under-specified items

This table records whether each reviewed requirement has a semantic/process home. `COVERED` means represented in the architecture map; it does **not** mean implemented. Implementation completion is tracked only in §34.

| Requirement/gap | Classification | Explicit home in this map | Architecture result |
| --- | --- | --- | --- |
| Confirmation of Activity/Event/Actual/Outcome | contextual | §15 + §17 | COVERED |
| specific target MaterialState for Confirmation | internal/contextual | §15 + §22 | COVERED |
| Acknowledgement/common-ground after material change | contextual | §16 | COVERED |
| waiting-for-confirmation state | derived | §15.4 + §17 | COVERED |
| confirmation policy hierarchy | policy/product | §17.4 | COVERED |
| automatic outcomes | conditional bounded effect | §17.5 | COVERED |
| daily/weekly grouped review | derived workflow | §17 | COVERED |
| reminder intent | conditional response | §18 | COVERED |
| notification channels/quiet hours/repetition | external/product policy | §18 | COVERED |
| unplaced Activity/Planning Tray | derived projection | §5.4 + §25.3 | COVERED |
| `Palestra`/`Inglese` grouping | product organization | §20 | COVERED |
| primary Life Area versus tags | product organization | §20 | COVERED |
| Life Area versus Goal | non-collapse | §20.2 | COVERED |
| Context versus appearance | product/view | §20.7 | COVERED |
| current prototype groups not taxonomy | frontend boundary | §20.8 | COVERED |
| Activity sub-work decomposition | owner semantic | §5.2 | COVERED |
| Activity divisibility/partial/effort semantics | contextual policy | §5 + §19.5 | COVERED |
| Event Agenda/internal parts | Event internal | §6.6 | COVERED |
| Event preparation/follow-up Activities | relation boundary | §6.5 | COVERED |
| Event actual attendance separate from Session | contextual | §6.7 + §12.17 | COVERED |
| Event postponed/TBD with no current Schedule | lifecycle | §6.3 + §10 | COVERED |
| explicit Schedule extension during execution | Schedule history | §6.4 + §10.6 | COVERED |
| early/late actual execution without reschedule | Actual/Session | §10.6 | COVERED |
| Routine composite structure | Routine internal | §7.2 | COVERED |
| skip Occurrence vs pause/end Routine | lifecycle | §7.3 | COVERED |
| this occurrence vs future policy | lifecycle/version | §7.4 + §9.7 + §19.8 | COVERED |
| six semantic recurrence families | contextual | §8.1 | COVERED |
| four current CP6 materialized recurrence families | physical boundary | §8.1 | COVERED |
| recurrence pattern anchor vs effective range | contextual | §8.2 | COVERED |
| quota period frame and no fake ordinal | contextual | §8.7 | COVERED |
| no browser canonical recurrence | application boundary | §8.8 + §25.6 | COVERED |
| virtual versus materialized Occurrence horizon | contextual/runtime | §8.8 + §9.6 | COVERED |
| explicit-extra Occurrence exact CP6 semantics | contextual | §9.1 | COVERED |
| provider Occurrence identity mapping | integration | §9.8 + §23 | COVERED |
| coarse Schedule precision | contextual | §10.2 | COVERED |
| manual Session recording | top-level capture | §12 | COVERED |
| timer/stopwatch Session capture | runtime | §12.8 | COVERED |
| imported/automatic Session capture | runtime/provenance | §12.1 + §12.8 | COVERED |
| open/running Session | runtime | §12.1 | COVERED |
| pause/resume same Session | runtime | §12.5 | COVERED |
| end/restart new Session | runtime | §12.6 | COVERED |
| elapsed/active/paused time | derived execution | §12.1 | COVERED |
| Session timing correction | correction | §12.9 | COVERED |
| Session split/merge | reconciliation | §12.10 | COVERED |
| false Session deletion vs correction | data lifecycle | §12.11 + §27 | COVERED |
| stale running Session | recovery | §12.18 | COVERED |
| web/mobile Session control | runtime | §12.19 | COVERED |
| offline timer synchronization | runtime | §12.19 | COVERED |
| device clock drift | runtime | §12.19 | COVERED |
| concurrent Session operation conflict | runtime | §12.19 | COVERED |
| Session context attach/relation | relation boundary | §12.1 + §12.16 | COVERED |
| overlapping Sessions | contextual execution | §12.14 | COVERED |
| overlap-aware analytics | derived | §12.15 + §26.4 | COVERED |
| Actual absence vs known non-realization | contextual | §13.3 | COVERED |
| multiple Sessions one Actual | contextual | §13.4 | COVERED |
| provider/user competing Actual assertions | reconciliation | §13.9 + §22 | COVERED |
| Outcome contextual vocabulary | contextual | §14 | COVERED |
| no universal success/failure enum | invariant | §14 + §29 | COVERED |
| Undo vs correction vs reopen | lifecycle | §27 | COVERED |
| delete/invalidate vs archive/hide | lifecycle/data | §27 | COVERED |
| movement policy | contextual policy | §19.4 | COVERED |
| fallback/replanning scope | contextual policy | §19.6-19.8 | COVERED |
| conflict/infeasibility explanation | derived projection | §25.6 + §26 | COVERED |
| user statistics/metrics | derived analytics | §26 | COVERED |
| planned vs actual analytics | derived | §26.3 | COVERED |
| corrected truth used by statistics | derived/history | §26.5 | COVERED |
| Clock/test clock | internal | §21.1 | COVERED |
| date-only/floating/zoned/instant | temporal infrastructure | §21.2 | COVERED |
| DST 23h/25h local-day range | temporal infrastructure | §21.4 | COVERED |
| actual timestamp precision | temporal infrastructure | §21.6 | COVERED |
| provider reconciliation | integration | §23 | COVERED |
| input surfaces converge to same operations | application boundary | §24 | COVERED |
| F0 idempotency/revision/Undo semantics | internal/application | §24.1 | COVERED |
| Timeline T1 frozen behavior | frontend change-control | §25.2 | COVERED |
| range query horizon/pagination/zone/provenance | query boundary | §25.6 | COVERED |
| CP6/current-main baseline distinction | persistence guard | §28 | COVERED |
| recovery anti-resurrection boundary | recovery | §28.7 | COVERED |

---

# 32. Source coverage ledger used for this map

This map and its required audits were checked against current accepted material relevant to this vertical, including at minimum:

## Domain concepts

- `activity.md`;
- `event.md`;
- `routine.md`;
- `occurrence.md`;
- `schedule.md`;
- `temporal-constraint.md`;
- `recurrence.md`;
- `session.md`;
- `actual.md`;
- `outcome.md`;
- `confirmation.md`;
- `acknowledgement.md`;
- `conditional-policy.md`;
- Responsibility/Participation/Person/Actor/Place boundaries where they touch this lifecycle;
- downstream Version/Material-State, Provenance, Reconciliation, Decision/Authority/Visibility rules consumed by these concepts.

## Product requirements

- `v1-scheduling-flexibility.md`;
- `v1-execution-status.md`;
- `v1-confirmation-and-reminders.md`;
- `v1-calendar-contexts-and-grouped-views.md`;
- `v1-today-experience.md`;
- `v1-work-context-and-meeting-lifecycle.md`;
- `v1-data-history-and-privacy.md`;
- feature-discovery simulation pressure where already reflected by accepted Domain concepts.

## Frontend/application contracts

- `docs/frontend/README.md`;
- `home/temporal-f0-contract.md`;
- `home/timeline-t1-frozen-contract.md`;
- `home/temporal-create-c1-scope-amendment.md`;
- `home/temporal-create-c1-traceability.md`;
- `home/temporal-create-c1-manual-acceptance.md`;
- `home/temporal-create-c1-manual-findings-2026-09-04.md`;
- `home/temporal-create-c1-engineering-checkpoint.md`;
- `home/temporal-frontend-roadmap.md`;
- `frontend/ui-registry.md`;
- `frontend/production-readiness/component-architecture.md`;
- `frontend/production-readiness/backend-integration-contract.md`.

## Logical/Physical/PostgreSQL baseline

- closed Whole Logical classification/invariants and WL-H01..WL-H12;
- accepted Physical/PostgreSQL selection;
- CP1–CP5 backend foundation;
- CP6-01 coverage;
- CP6-02 PostgreSQL Persistence Constitution;
- CP6 M1–M6/M7+ accepted forward history;
- current `docs/database/README.md` and Alembic `20260906_18` baseline;
- current Dictionary/SQLAlchemy/live PostgreSQL as implementation authority.

## Final precision pressure

- second completeness audit;
- final relation/cardinality/operation/physical/frontend audit;
- external-product benchmark used only as pressure test;
- 38 adversarial scenarios from final pre-roadmap audit.

External products/standards are never DANTE ontology authority.

---

# 33. Pre-roadmap gate — CLOSED

The primary map survived the second completeness audit and final precision/benchmark/adversarial audit.

Current gate result:

```text
KNOWN REVIEWED SEMANTIC NODE WITHOUT HOME     0
KNOWN REVIEWED RELATION UNCLASSIFIED           0
KNOWN REVIEWED OPERATION WITHOUT EFFECT HOME   0
KNOWN REVIEWED != COLLAPSE UNRESOLVED          0
NEW DOMAIN OWNER REQUIRED                      0
EXTERNAL BENCHMARK-REQUIRED OWNER              0
OPEN-BY-DESIGN QUESTIONS                       EXPLICITLY REGISTERED
ROADMAP                                        FROZEN
IMPLEMENTATION                                 ACTIVE — B00/B01 CLOSED; B02 IN PROGRESS
```

The roadmap is authoritative for sequencing, while this map is authoritative for semantic coverage and live completion tracking.

---

# 34. Live implementation progress ledger

This is the **blocking green-check ledger** requested for the entire vertical.

## 34.0 Status semantics

```text
⬜ NOT STARTED
🟨 IN PROGRESS
✅ DONE
⛔ BLOCKED
```

Rules:

1. `✅` means all applicable Definition-of-Done gates in `timeline-temporal-operational-roadmap.md §0.3` have passed.
2. Code existing in an old prototype/mock does not earn `✅` unless it satisfies the real vertical contract and has been revalidated.
3. A roadmap block may be complete only when every checklist item assigned to it is `✅` or has an explicitly approved scope amendment.
4. Any newly discovered requirement must receive a new stable ID before implementation continues.
5. Every implementation PR/slice that changes one of these items must update its status/evidence in the same change.
6. No final branch/workstream closure with `⬜`, `🟨` or unreviewed `⛔` remaining.

## 34.1 Documentation / architecture gates

- ✅ **[DOC-001]** Primary semantic map established and deep-gap-audited.
- ✅ **[DOC-002]** Second completeness audit completed; current DB `_18 / 89|5|18|77|173|91|272|0|0|0` truth reconciled.
- ✅ **[DOC-003]** Final pre-roadmap precision audit completed; relations/operations/benchmark/adversarial sweep passed.
- ✅ **[DOC-004]** `explicit_extra` Occurrence governing-state correction bound into primary map.
- ✅ **[DOC-005]** Schedule coarse-precision and Recurrence anchor/effective-range hardenings bound into primary map.
- ✅ **[DOC-006]** Detailed end-to-end implementation roadmap frozen.
- ✅ **[DOC-007]** Live green-check rule made a fixed branch/workstream contract.
- ✅ **[DOC-008]** B01 candidate PostgreSQL/SQLAlchemy/Dictionary/current-catalog truth reconciled at Alembic `_19` with topology `91|5|19|77|177|95|275|0|0|0`; protected-main `_18` freeze truth remains historical/main authority and is not silently rewritten.

## 34.2 B00 — Real Data Spine / no runtime mocks

- ✅ **[SPINE-001]** Inventory every normal-runtime Timeline/Create mock/fake source. — Inventory covers prototype clock/groups/cards, distant-date generated fallback cards, Create in-memory fake-success, session-only local context creation and normal-runtime transport-failure fallback risks; evidence is frozen in the B00 execution amendment.
- ✅ **[SPINE-002]** Remove/isolate fake Timeline cards from normal runtime. — Normal runtime uses the real temporal read path; final exact-head frontend/full-stack reconciliation and manual empty-state proof passed.
- ✅ **[SPINE-003]** Move reusable fake datasets behind explicit test/dev-test-only boundaries. — T1 fixtures remain test-mode-only; production build/runtime cutover and frozen T1 regression passed on the closure candidate.
- ✅ **[SPINE-004]** Establish one real temporal frontend feature/application data-source path. — Strict remote temporal Timeline data-source/Home runtime boundary is active and exercised by real full-stack B00 proof.
- ✅ **[SPINE-005]** Establish real backend temporal operation/query boundary. — Authenticated bounded temporal Timeline endpoint/application path is active and passed backend/PostgreSQL/full-stack reconciliation.
- ✅ **[SPINE-006]** Reverify authenticated `DanteContext` Account→self Person path. — Real PostgreSQL/auth integration evidence passed in the final reconciliation suite.
- ✅ **[SPINE-007]** Reverify effective request timezone handling for temporal operations/queries. — `X-Dante-Time-Zone` and effective-zone behavior passed automated integration coverage on the closure candidate.
- ✅ **[SPINE-008]** Ensure normal runtime truthful empty state when no temporal product data exists. — Manual proof A and exact-head B00 full-stack proof both showed a real empty Timeline with no prototype cards.
- ✅ **[SPINE-009]** Ensure backend/network failure is never replaced by fake success. — Manual PostgreSQL-outage proof showed `Timeline non disponibile`, no fake cards and successful real Retry after restart; exact-head B00 E2E also passed.
- ✅ **[SPINE-010]** Define isolated `userTest`/test-data setup and cleanup flow. — Disposable stack, synthetic account, three manual proofs and scoped cleanup are documented and executed.
- ✅ **[SPINE-011]** Establish real-backend + real-test-PostgreSQL E2E harness for vertical slices. — Production web/FastAPI/disposable PostgreSQL 18.6 harness executed successfully for B00 and B01.
- ✅ **[SPINE-012]** Preserve F0/T1 behavior through real-data cutover. — Production/test fixture boundary remained explicit; frontend suite and frozen T1 Firefox interaction contract passed on exact closure candidate.
- ✅ **[B00-T01]** Automated frontend no-runtime-mock regression test. — Frontend contract/quality/unit/build gates passed in reconciliation run `34261607749`.
- ✅ **[B00-T02]** Backend real-query smoke/integration test. — Backend quality and full PostgreSQL acceptance passed on exact closure candidate.
- ✅ **[B00-T03]** Auth/DanteContext/timezone integration test. — Real auth/context/timezone coverage passed in the reconciled backend/PostgreSQL/full-stack suite.
- ✅ **[B00-T04]** Real PostgreSQL E2E harness smoke test. — B00 real full-stack Chromium proof passed on exact closure candidate; frozen Firefox interaction regression also passed.
- ✅ **[B00-T05]** Manual `userTest` empty/error/real-data-path acceptance. — `B00 userTest — APPROVED` recorded 2026-09-08 after proofs A/B/C passed on the disposable real stack; exact-head B00 E2E subsequently remained green.

## 34.3 B01 — Activity Core

- ✅ **[ACT-001]** Re-open Activity Domain/Logical/Physical authority before implementation. — Authority was re-read before B01 and the implementation stayed within Activity ownership boundaries.
- ✅ **[ACT-002]** Resolve minimum meaningful Activity descriptive/actionable persistence. — B01 persists stable Activity intention identity plus bounded title/actionable descriptive state; no generic Task/status payload was introduced.
- ✅ **[ACT-003]** Prove whether forward DDL is required; no speculative generic Task/status schema. — Real persistence gap was proven and forward Alembic `_19` added only `activity_intention`, `activity_create_operation` and governed create routine support.
- ✅ **[ACT-004]** Implement stable Activity creation identity. — Canonical UUIDv7 Activity identity persists across reload/refetch.
- ✅ **[ACT-005]** Implement idempotent `CreateActivity` application operation. — Operation identity/fingerprint/idempotent retry and collision behavior are covered by backend/PostgreSQL tests.
- ✅ **[ACT-006]** Implement unplaced Activity as valid canonical state. — Activity can exist with no accepted Schedule and is not converted into a fake all-day/timed item.
- ✅ **[ACT-007]** Implement real Planning Tray query for unplaced Activity. — Production Planning Tray consumes the real backend unplaced query and persisted Activity identity.
- ✅ **[ACT-008]** Make `Activity` default selected macro-class in `+` Create. — Canonical Timeline `+` path defaults to Activity and manual/automated proof exercised it.
- ✅ **[ACT-009]** Make Activity Create submit use real backend result. — Production create waits for the real governed backend effect; no local fake-success path remains.
- ✅ **[ACT-010]** Preserve `draft != canonical Activity` behavior. — Manual dirty-draft discard and automated regression prove discarded draft state does not create/delete canonical Activity.
- ✅ **[ACT-011]** Preserve Activity identity across reload/refetch. — Manual proof A and exact-head E2E retain the same canonical Activity once after reload.
- ✅ **[ACT-012]** Ensure duplicate projection/refetch cannot duplicate Activity identity. — Planning Tray projection/refetch remained one card for one canonical Activity; automated regression passed.
- ✅ **[ACT-013]** Preserve Activity `!= Event/Routine/Schedule/Session/Actual/Outcome/Goal/Plan` boundaries in implementation. — B01 activates only Activity intention; unsupported Event remains fail-closed and Schedule/Routine/Session/Actual/Outcome are not manufactured.
- ✅ **[ACT-014]** Preserve repeated Activity UX as future Routine-backed semantics, not Activity-owned recurrence. — B01 introduces no Activity-owned recurrence or `repeat` persistence; future repeated-intent activation remains Routine-backed by binding semantic authority.
- ✅ **[ACT-015]** Design/implement estimated effort when first required without equating it to scheduled/actual duration. — B01 applicability gate satisfied by explicit non-activation: the canonical unplaced path no longer exposes unsupported estimated effort, and normal runtime fails closed if non-baseline effort/duration intent is injected. Dedicated Activity effort semantics remain a future gate when first required.
- ✅ **[ACT-016]** Design/implement semantic sub-Activity structure when first required, separate from Session splitting. — B01 applicability gate satisfied by non-activation: no sub-Activity schema/UI shortcut was introduced; future activation must reopen this semantic gate.
- ✅ **[ACT-017]** Resolve completion profile semantics before any user-visible generic `done` behavior is accepted. — B01 accepts no generic `done`/completion behavior; completion-profile resolution remains a blocking future gate before such UI/persistence can be activated.
- ✅ **[B01-T01]** Activity domain/application validation tests. — Final backend quality suite passed.
- ✅ **[B01-T02]** Activity idempotency retry/collision tests. — Final backend/PostgreSQL suite passed.
- ✅ **[B01-T03]** Activity PostgreSQL persistence/integrity tests. — Full PostgreSQL 18.6 acceptance passed with `_19` topology/Dictionary alignment.
- ✅ **[B01-T04]** Activity API/integration tests. — Final API/application/backend suite passed.
- ✅ **[B01-T05]** Activity frontend Create/Planning Tray component tests. — Frontend unit/contract/architecture/type/build gates passed on exact closure candidate.
- ✅ **[B01-T06]** E2E `+ → Activity → Planning Tray → reload` test. — Real full-stack Chromium proof passed on exact closure candidate.
- ✅ **[B01-T07]** Dirty-draft discard `!= delete/cancel Activity` regression test. — Manual proof B and automated regression passed.
- ✅ **[B01-T08]** Manual `userTest` Activity creation/reload/error acceptance. — Real disposable-stack proofs A/B/C plus staged Event fail-closed check were reviewed; the user explicitly instructed B01 closure after the truthfulness repair. `B01 userTest — APPROVED` is recorded in the B01 userTest document.

B00/B01 closure evidence is anchored by exact-head reconciliation run `34261607749` on `303e75c56716008bfc352e92411884760727e043`, which completed successfully across backend quality, full PostgreSQL 18.6 acceptance, frontend quality/build/mobile checks, B00 real full-stack Chromium, B01 real full-stack Chromium, frozen T1 Firefox and the aggregate reconciliation gate.

## 34.4 B02 — Schedule Core

- ✅ **[SCH-001]** Re-open Schedule authority/current CP6 placement tables/views/validators before implementation. — Deep-read completed and frozen in `timeline-temporal-operational-b02-execution-plan.md`; B02 reuses the existing CP6 Schedule owner/placement/current/history machinery rather than creating a competing model.
- ⬜ **[SCH-002]** Preserve subject eligibility Activity/Event/Occurrence; first activate Activity path.
- ⬜ **[SCH-003]** Implement/consume date-span placement correctly.
- ✅ **[SCH-004]** Implement/consume floating-local placement correctly. — Floating-local same-day placement is implemented and proven by B02-A/B manual flow plus targeted backend/frontend tests.
- ⬜ **[SCH-005]** Implement/consume named-zone placement correctly.
- ⬜ **[SCH-006]** Implement/consume absolute placement correctly.
- ⬜ **[SCH-007]** Preserve coarse accepted placement precision without manufactured timestamps.
- ✅ **[SCH-008]** Preserve Schedule absence as valid state. — Unschedule leaves the Activity identity/history intact with no current placement; Planning Tray and reload proved this.
- ✅ **[SCH-009]** Preserve possible 0..N planned placements; do not hard-code universal 1:1. — B02-E1 real PostgreSQL proof established two independent current Schedule records for one Activity without a subject-level uniqueness constraint.
- ✅ **[SCH-010]** Implement accepted Schedule creation for Activity. — Activity Schedule creation is proven by the real create/place flow and PostgreSQL-backed targeted tests.
- ✅ **[SCH-011]** Implement Schedule MaterialState revision. — Governed floating-local revision creates a new current placement state; B02-B/C automated proof and manual revision passed.
- ✅ **[SCH-012]** Implement explicit current accepted Schedule binding. — Current binding is explicit and Timeline renders one canonical current item after authoritative reload.
- ✅ **[SCH-013]** Preserve Schedule history/original expectation. — Schedule history/original placement survives revision, unschedule and guarded Undo; direct PostgreSQL proof passed.
- ✅ **[SCH-014]** Implement expected-state concurrency check. — Expected-state conflicts are proven by stale revision/unschedule and stale two-tab manual conflict.
- ✅ **[SCH-015]** Implement Schedule mutation idempotency. — Operation replay/idempotency and reuse conflicts are covered by targeted PostgreSQL/application tests.
- ✅ **[SCH-016]** Implement real Planning Tray→Timeline placement. — Existing unplaced Activity placement preserves the same identity and removes it from Planning Tray after canonical refresh.
- ⬜ **[SCH-017]** Implement real Timeline drag earlier/later.
- ✅ **[SCH-018]** Implement supported duration/start/end adjustment without conflating Actual. — Supported same-day floating-local start/end and duration adjustment passed manual and frontend/backend tests; broader forms remain separate.
- ✅ **[SCH-019]** Implement anchored time editor against real Schedule mutation. — Anchored time editor revision passed manual B02-B and frontend contract tests.
- ✅ **[SCH-020]** Implement Activity unschedule back to Planning Tray where valid. — Unschedule to Planning Tray passed with reload, conflict protection and database-outage truthfulness.
- ✅ **[SCH-021]** Implement guarded Undo through a new monotonic state/revision. — Guarded Undo restored a new accepted current state and survived reload; targeted PostgreSQL and manual proof passed.
- ⬜ **[SCH-022]** Preserve explicit in-progress expectation change as Schedule revision.
- ⬜ **[SCH-023]** Preserve early/late/overrun reality as Session/Actual, not automatic Schedule rewrite.
- ✅ **[SCH-024]** Implement initial temporal range/local-day query for scheduled Activity. — The authenticated local-date Timeline window for the exposed floating-local Activity path is proven by backend/frontend integration tests and manual reload.
- ✅ **[B02-T01]** Schedule form/validator tests. — B02-E1 value tests cover date-span, cross-midnight floating-local, named-zone explicit DST policy, aware absolute and coarse local-period without fabricated boundaries.
- ✅ **[B02-T02]** Schedule current/history direct PostgreSQL tests. — B02-E1 real PostgreSQL matrix passed for all five forms, exact one-payload totality, three monotonic history episodes and one current state per Schedule.
- ✅ **[B02-T03]** Reschedule/unschedule/Undo application tests. — Cross-form revision, form-independent unschedule and generic guarded Undo passed on real PostgreSQL for the activated union.
- ✅ **[B02-T04]** Stale revision/idempotency conflict tests. — B02-E1 proves same-intent replay, changed-intent rejection, stale expected-state rejection and cross-self rejection for generic mutation.
- ⬜ **[B02-T05]** DST/local-day tests applicable to exposed Schedule forms.
- ✅ **[B02-T06]** Timeline drag/time-editor/Planning Tray frontend regressions. — Frontend Timeline/Planning Tray/time-editor/Undo regressions and the real browser flow passed.
- ⬜ **[B02-T07]** Firefox T1 critical interaction regressions.
- ⬜ **[B02-T08]** E2E create→place→move→unschedule/reload/history test.
- ✅ **[B02-T09]** Manual `userTest` Schedule/Undo/conflict acceptance. — Manual isolated full-stack B02 userTest A-F was approved on 2026-09-15.



### B02-A through B02-D evidence reconciliation — 2026-09-15

The exact supported B02 slice is now evidence-backed: same-day floating-local Activity Schedule creation, Planning Tray placement, governed revision, unschedule, guarded Undo, authoritative reload, stale two-tab conflict rejection and PostgreSQL-outage truthfulness. Automated targeted PostgreSQL proof passed (2 passed), and the isolated browser userTest A-F was approved.

The B02 block remains 🟨 IN PROGRESS. B02-E1 proves canonical persistence/mutation for date-span, floating-local interval, named-zone interval, absolute interval and coarse local-period, including 0..N Schedule cardinality. Timeline read/DST consumption, web authoring/rendering, drag-specific behavior, Event/Occurrence and B02-E closure remain open. CI remains deferred by instruction.

## 34.5 B03 — Event Core

- ⬜ **[EVT-001]** Re-open Event Domain/Logical/Physical authority before implementation.
- ⬜ **[EVT-002]** Resolve minimum meaningful Event descriptive persistence.
- ⬜ **[EVT-003]** Implement idempotent `CreateEvent`.
- ⬜ **[EVT-004]** Activate Event macro-class in `+` Create.
- ⬜ **[EVT-005]** Implement timed Event using shared Schedule.
- ⬜ **[EVT-006]** Implement all-day/date-span Event in real per-day all-day lane.
- ⬜ **[EVT-007]** Implement multi-day Event semantics/query/rendering.
- ⬜ **[EVT-008]** Implement postponed/TBD Event with identity/history and no fake placeholder Schedule.
- ⬜ **[EVT-009]** Preserve original expectation/current Schedule/Actual separation.
- ⬜ **[EVT-010]** Implement Event Agenda/internal parts at accepted product level.
- ⬜ **[EVT-011]** Preserve Agenda part `!= Activity/Event/Occurrence/Session/Actual` by default.
- ⬜ **[EVT-012]** Implement preparation/follow-up Activity relation when activated.
- ⬜ **[EVT-013]** Implement Place/conference intent only through justified relation/profile semantics.
- ⬜ **[EVT-014]** Preserve ordinary Event attendance `!= Session`.
- ⬜ **[EVT-015]** Preserve Event `!= Availability/Capacity Claim`.
- ⬜ **[B03-T01]** Event create/application tests.
- ⬜ **[B03-T02]** Timed/all-day/multi-day PostgreSQL/API tests.
- ⬜ **[B03-T03]** Postponed/TBD history/query tests.
- ⬜ **[B03-T04]** Event Agenda semantic/frontend tests.
- ⬜ **[B03-T05]** Shared Schedule regression suite rerun for Activity + Event.
- ⬜ **[B03-T06]** E2E Event create/reschedule/all-day/reload test.
- ⬜ **[B03-T07]** Manual `userTest` Event acceptance.

## 34.6 B04 — Temporal Constraints / movement policy

- ⬜ **[TC-001]** Re-open Temporal Constraint authority before persistence design.
- ⬜ **[TC-002]** Resolve first typed persistence/runtime representation; no generic `due_at`/JSON escape.
- ⬜ **[TC-003]** Implement earliest-start constraint where required.
- ⬜ **[TC-004]** Implement latest-start constraint where required.
- ⬜ **[TC-005]** Implement latest-completion/delivery Deadline semantics with explicit facet.
- ⬜ **[TC-006]** Implement hard validity window.
- ⬜ **[TC-007]** Implement preferred/soft window.
- ⬜ **[TC-008]** Implement minimum/maximum duration where required.
- ⬜ **[TC-009]** Implement minimum contiguous Session duration where required.
- ⬜ **[TC-010]** Implement spacing/recovery constraint where required.
- ⬜ **[TC-011]** Implement relative-before/after constraint where required.
- ⬜ **[TC-012]** Implement movement policy separately from Temporal Constraint.
- ⬜ **[TC-013]** Ensure hard planning violation does not block recording contradictory Actual reality.
- ⬜ **[TC-014]** Implement hard/soft conflict explanation.
- ⬜ **[B04-T01]** Constraint typed-validation tests.
- ⬜ **[B04-T02]** Constraint persistence/direct PostgreSQL tests if DDL added.
- ⬜ **[B04-T03]** Hard vs soft placement behavior tests.
- ⬜ **[B04-T04]** Deadline-passage `!= Outcome` test.
- ⬜ **[B04-T05]** Manual `userTest` constraint/explanation acceptance.

## 34.7 B05 — Life Area / Calendar / Tags

- ⬜ **[ORG-001]** Re-open product/Logical LR-12 organization authority before persistence design.
- ⬜ **[ORG-002]** Prove exact durable Life Area representation; no new LR-01 owner by convenience.
- ⬜ **[ORG-003]** Implement Life Area create.
- ⬜ **[ORG-004]** Implement rename.
- ⬜ **[ORG-005]** Implement reorder.
- ⬜ **[ORG-006]** Implement archive.
- ⬜ **[ORG-007]** Implement hide/show.
- ⬜ **[ORG-008]** Implement icon/color appearance metadata without making color semantic truth.
- ⬜ **[ORG-009]** Implement one primary Life Area relation for applicable planning item.
- ⬜ **[ORG-010]** Implement secondary Tags separately.
- ⬜ **[ORG-011]** Preserve Life Area `!= Goal/Plan/Tag/Place/provider calendar`.
- ⬜ **[ORG-012]** Replace/reconcile prototype Timeline groups with real product organization.
- ⬜ **[ORG-013]** Preserve hidden item relevance to authorized conflict/scheduling reasoning.
- ⬜ **[ORG-014]** Preserve future actor-local organization for shared canonical item.
- ⬜ **[ORG-015]** Ensure accessibility does not rely on color alone.
- ⬜ **[B05-T01]** Organization lifecycle tests.
- ⬜ **[B05-T02]** Item assignment/filter/grouping tests.
- ⬜ **[B05-T03]** Tags-vs-primary-area tests.
- ⬜ **[B05-T04]** Hidden-group conflict-awareness test.
- ⬜ **[B05-T05]** Accessibility/frontend grouping tests.
- ⬜ **[B05-T06]** Manual `userTest` Palestra/Inglese organization acceptance.

## 34.8 B06 — Routine / Recurrence / Occurrence baseline

### Routine

- ⬜ **[ROU-001]** Re-open Routine authority/current identity shell before implementation.
- ⬜ **[ROU-002]** Resolve minimum meaningful Routine product persistence.
- ⬜ **[ROU-003]** Implement Routine create and activate `Routine` macro-class.
- ⬜ **[ROU-004]** Implement Routine recurrence material-state authoring.
- ⬜ **[ROU-005]** Implement Routine pause.
- ⬜ **[ROU-006]** Implement Routine resume.
- ⬜ **[ROU-007]** Implement Routine end.
- ⬜ **[ROU-008]** Preserve skip Occurrence `!= pause != end`.
- ⬜ **[ROU-009]** Implement composite Routine structure when required without creating one Routine per internal step.
- ⬜ **[ROU-010]** Preserve observed pattern `!= canonical Routine intent`.

### Recurrence baseline

- ⬜ **[REC-001]** Implement calendar-wall-clock runtime authoring/evaluation.
- ⬜ **[REC-002]** Implement elapsed-interval runtime authoring/evaluation.
- ⬜ **[REC-003]** Implement quota-per-period runtime authoring/evaluation.
- ⬜ **[REC-004]** Implement cyclic-positional runtime authoring/evaluation.
- ⬜ **[REC-005]** Implement explicit pattern anchor/phase semantics.
- ⬜ **[REC-006]** Implement effective range: open/until/count.
- ⬜ **[REC-007]** Preserve expected-count `!= successful-completion-count`.
- ⬜ **[REC-008]** Implement named-zone/floating/absolute recurrence timezone modes as applicable.
- ⬜ **[REC-009]** Implement quota period frame where membership can differ.
- ⬜ **[REC-010]** Preserve stable quota identities without invented ordinal meaning.
- ⬜ **[REC-011]** Implement structural exclusion `!= generated then skipped`.
- ⬜ **[REC-012]** Define/implement virtual future/materialization horizon.
- ⬜ **[REC-013]** Ensure frontend authors specification only; backend owns canonical generation.
- ⬜ **[REC-014]** Reuse recurrence capability for Event recurrence; no duplicated engine.

### Occurrence

- ⬜ **[OCC-001]** Implement backend recurrence evaluator/checkpoint consumption.
- ⬜ **[OCC-002]** Materialize stable Occurrence identity when justified.
- ⬜ **[OCC-003]** For `recurrence_generated`, bind exact governing Recurrence MaterialState.
- ⬜ **[OCC-004]** For `recurrence_generated`, persist exactly one compatible generation coordinate.
- ⬜ **[OCC-005]** Implement `explicit_extra` with source relation and NULL governing recurrence state.
- ⬜ **[OCC-006]** Preserve Occurrence Schedule optionality.
- ⬜ **[OCC-007]** Implement one-off occurrence-specific Schedule exception.
- ⬜ **[OCC-008]** Implement this-occurrence-only change scope.
- ⬜ **[OCC-009]** Implement this-and-future source recurrence revision scope.
- ⬜ **[OCC-010]** Preserve historical Occurrence generating state after source revision.
- ⬜ **[OCC-011]** Preserve materialized future instance history when new recurrence no longer derives it.
- ⬜ **[OCC-012]** Preserve Occurrence identity through reschedule.

### Tests

- ⬜ **[B06-T01]** Four CP6 recurrence family unit/application tests.
- ⬜ **[B06-T02]** Recurrence direct PostgreSQL/current-state tests.
- ⬜ **[B06-T03]** DST wall-clock recurrence tests.
- ⬜ **[B06-T04]** Quota frame/no-exact-time tests.
- ⬜ **[B06-T05]** Pattern anchor/effective-range tests.
- ⬜ **[B06-T06]** Structural exclusion vs skip test.
- ⬜ **[B06-T07]** `explicit_extra` invariant tests.
- ⬜ **[B06-T08]** This-occurrence vs this-and-future tests.
- ⬜ **[B06-T09]** Historical generating-state preservation tests.
- ⬜ **[B06-T10]** Virtual vs materialized future reconciliation tests.
- ⬜ **[B06-T11]** Event + Routine shared recurrence regression suite.
- ⬜ **[B06-T12]** Frontend no-canonical-browser-expansion test.
- ⬜ **[B06-T13]** E2E Routine recurring items → Timeline test.
- ⬜ **[B06-T14]** Manual `userTest` Routine/Event recurrence acceptance.

## 34.9 B07 — Session Runtime

- ⬜ **[SES-001]** Re-open Session Domain/CP6 timing authority before implementation.
- ⬜ **[SES-002]** Resolve typed Session execution-context relation persistence; no arbitrary nullable FK shortcut.
- ⬜ **[SES-003]** Implement direct manual retrospective Session recording.
- ⬜ **[SES-004]** Implement spontaneous Session without fake Activity/Schedule.
- ⬜ **[SES-005]** Implement timer start.
- ⬜ **[SES-006]** Implement pause as same Session.
- ⬜ **[SES-007]** Implement resume.
- ⬜ **[SES-008]** Implement end/close.
- ⬜ **[SES-009]** Implement Activity contextual start.
- ⬜ **[SES-010]** Implement Occurrence contextual start.
- ⬜ **[SES-011]** Preserve ordinary Event attendance `!= Session`.
- ⬜ **[SES-012]** Implement absolute timing.
- ⬜ **[SES-013]** Implement elapsed-only/uncertain-boundary timing where product requires it.
- ⬜ **[SES-014]** Preserve timing precision/provenance.
- ⬜ **[SES-015]** Derive elapsed/paused/active durations.
- ⬜ **[SES-016]** Implement timing correction preserving Session identity.
- ⬜ **[SES-017]** Implement context correction preserving lineage.
- ⬜ **[SES-018]** Implement Session split with lineage.
- ⬜ **[SES-019]** Implement Session merge with lineage.
- ⬜ **[SES-020]** Implement false-data deletion/invalidation boundary.
- ⬜ **[SES-021]** Allow semantically compatible overlapping Sessions.
- ⬜ **[SES-022]** Support one Session related to multiple intentions without duplicate time capture.
- ⬜ **[SES-023]** Implement stale-running detection/review without fabricated end time.
- ⬜ **[SES-024]** Implement idempotent Session control operations.
- ⬜ **[SES-025]** Implement expected-state conflict on concurrent pause/resume/end.
- ⬜ **[SES-026]** Preserve `Session end != Activity/Occurrence completion`.
- ⬜ **[B07-T01]** Manual/spontaneous Session tests.
- ⬜ **[B07-T02]** Start/pause/resume/end state tests.
- ⬜ **[B07-T03]** Session timing/current-state direct PostgreSQL tests.
- ⬜ **[B07-T04]** Timing precision/correction tests.
- ⬜ **[B07-T05]** Split/merge/lineage tests.
- ⬜ **[B07-T06]** Overlap/multi-intention tests.
- ⬜ **[B07-T07]** Stale-running tests.
- ⬜ **[B07-T08]** Concurrent/idempotent control tests.
- ⬜ **[B07-T09]** E2E Activity/Occurrence→Session timer test.
- ⬜ **[B07-T10]** Manual Web `userTest` Session lifecycle acceptance.

## 34.10 B08 — Responsibility / Participation / actor relations

- ⬜ **[REL-001]** Re-open Responsibility/Participation/Actor authority before relation persistence.
- ⬜ **[REL-002]** Preserve Person/Account/Principal/Actor separation.
- ⬜ **[REL-003]** Implement bounded requester relation where required.
- ⬜ **[REL-004]** Implement bounded responsible/accountable Actor relation where required.
- ⬜ **[REL-005]** Preserve expected performer separately where required.
- ⬜ **[REL-006]** Preserve actual performer separately where required.
- ⬜ **[REL-007]** No ambiguous generic `assigned_to` persistence.
- ⬜ **[PAR-001]** Implement Event intended/invited Participation.
- ⬜ **[PAR-002]** Implement accepted response.
- ⬜ **[PAR-003]** Implement tentative response.
- ⬜ **[PAR-004]** Implement declined response.
- ⬜ **[PAR-005]** Preserve no-response as unknown, not declined.
- ⬜ **[PAR-006]** Implement Actual attendance separately.
- ⬜ **[PAR-007]** Support actual attendance without prior invitation where valid.
- ⬜ **[PAR-008]** Preserve accepted `!= attended` and declined `!= proven absence`.
- ⬜ **[ACK-001]** Preserve Acknowledgement as separate future/common-ground act for material shared changes.
- ⬜ **[B08-T01]** Responsibility role-separation tests.
- ⬜ **[B08-T02]** Participation response/history tests.
- ⬜ **[B08-T03]** Actual attendance independence tests.
- ⬜ **[B08-T04]** Unexpected participant test.
- ⬜ **[B08-T05]** No ambiguous generic-role persistence schema test/review.
- ⬜ **[B08-T06]** Manual `userTest` actor/participant acceptance when UI activated.

## 34.11 B09 — Actual / Outcome / Confirmation / Resolution

### Actual

- ⬜ **[ACTUAL-001]** Re-open Actual Domain/CP6 realization authority.
- ⬜ **[ACTUAL-002]** Implement Activity Actual subject path.
- ⬜ **[ACTUAL-003]** Implement Event Actual subject path.
- ⬜ **[ACTUAL-004]** Implement Occurrence Actual subject path.
- ⬜ **[ACTUAL-005]** Preserve no Actual as unknown.
- ⬜ **[ACTUAL-006]** Implement known non-realization distinctly.
- ⬜ **[ACTUAL-007]** Implement partial realization where product requires it.
- ⬜ **[ACTUAL-008]** Implement differently-realized/replacement context where required.
- ⬜ **[ACTUAL-009]** Support 0..N Session basis where applicable.
- ⬜ **[ACTUAL-010]** Support Event Actual without Session.
- ⬜ **[ACTUAL-011]** Preserve Observation/Measurement as external fact semantics.
- ⬜ **[ACTUAL-012]** Preserve current accepted realization/history/correction.
- ⬜ **[ACTUAL-013]** Preserve competing assertion/reconciliation boundary.

### Outcome

- ⬜ **[OUT-001]** Re-open Outcome authority and prove exact first persistence shape.
- ⬜ **[OUT-002]** Implement context-specific Activity result vocabulary required by product.
- ⬜ **[OUT-003]** Implement context-specific Event result vocabulary required by product.
- ⬜ **[OUT-004]** Implement context-specific Occurrence result vocabulary required by product.
- ⬜ **[OUT-005]** Preserve no Outcome `!= negative`.
- ⬜ **[OUT-006]** Preserve Outcome `!= lifecycle status/Observation/Artifact/Milestone`.
- ⬜ **[OUT-007]** Implement Outcome correction/history where consequential.

### Confirmation / Acknowledgement

- ⬜ **[CNF-001]** Re-open Confirmation authority and prove exact LR-03 persistence shape.
- ⬜ **[CNF-002]** Implement confirmer Actor.
- ⬜ **[CNF-003]** Implement exact target/material-state binding.
- ⬜ **[CNF-004]** Implement purpose/context where required.
- ⬜ **[CNF-005]** Preserve Confirmation S1 after target corrected to S2.
- ⬜ **[CNF-006]** Support conflicting actor Confirmations where required.
- ⬜ **[CNF-007]** Implement retraction/supersession where required by first workflows.
- ⬜ **[CNF-008]** Preserve no Confirmation `!= false/rejected/not-performed`.
- ⬜ **[ACK-002]** Implement Acknowledgement only when a real material common-ground workflow requires it.
- ⬜ **[ACK-003]** Preserve sent/delivered/read `!= acknowledged`.

### Resolution Queue

- ⬜ **[RES-001]** Implement derived resolution reason: Actual unknown.
- ⬜ **[RES-002]** Implement derived resolution reason: Outcome required/absent.
- ⬜ **[RES-003]** Implement derived resolution reason: Confirmation required/absent.
- ⬜ **[RES-004]** Implement derived resolution reason: Session anomaly.
- ⬜ **[RES-005]** Implement real `Fatto` operation mapping.
- ⬜ **[RES-006]** Implement real `Parziale` mapping.
- ⬜ **[RES-007]** Implement real `Saltato` mapping.
- ⬜ **[RES-008]** Implement real `Posticipato` mapping.
- ⬜ **[RES-009]** Implement real `Sostituito` mapping.
- ⬜ **[RES-010]** Implement `Conferma` mapping.
- ⬜ **[RES-011]** Implement `Correggi` entry path.
- ⬜ **[RES-012]** Implement batch/review workflow when activated.
- ⬜ **[RES-013]** Preserve Resolution Queue `!= Notification feed/status table`.
- ⬜ **[RES-014]** Implement atomic multi-effect operation where one UX action requires Actual+Outcome+Confirmation together.

### Tests

- ⬜ **[B09-T01]** Unknown vs known non-realization tests.
- ⬜ **[B09-T02]** Multiple Sessions→one Actual tests.
- ⬜ **[B09-T03]** Event Actual without Session test.
- ⬜ **[B09-T04]** Partial/different realization tests.
- ⬜ **[B09-T05]** Context-specific Outcome tests.
- ⬜ **[B09-T06]** Confirmation exact-state/correction tests.
- ⬜ **[B09-T07]** No-response/unresolved tests.
- ⬜ **[B09-T08]** Multi-effect transaction atomicity tests.
- ⬜ **[B09-T09]** Resolution Queue projection tests.
- ⬜ **[B09-T10]** E2E expected item→resolve→history test.
- ⬜ **[B09-T11]** Manual `userTest` Fatto/Parziale/Saltato/Conferma acceptance.

## 34.12 B10 — Advanced Recurrence / Conditional Policy / reminders

### Advanced recurrence

- ⬜ **[REC-ADV-001]** Prove dedicated persistence/runtime need for completion-relative recurrence.
- ⬜ **[REC-ADV-002]** Implement completion-relative qualifying Actual anchor.
- ⬜ **[REC-ADV-003]** Implement sequential chain/no-future-anchor behavior.
- ⬜ **[REC-ADV-004]** Prove dedicated persistence/runtime need for anchor-stream-relative recurrence.
- ⬜ **[REC-ADV-005]** Implement qualifying Session/anchor-stream mapping.
- ⬜ **[REC-ADV-006]** Preserve advanced recurrence `!= generic Trigger/workflow`.

### Conditional Policy

- ⬜ **[POL-001]** Re-open Conditional Policy authority before runtime representation.
- ⬜ **[POL-002]** Implement transition-based activation semantics.
- ⬜ **[POL-003]** Implement persistent-state activation semantics where required.
- ⬜ **[POL-004]** Implement per-new-qualifying-fact activation semantics where required.
- ⬜ **[POL-005]** Implement semantic dedup/idempotency for duplicate source/import facts.
- ⬜ **[POL-006]** Detect/handle competing policies without universal newest-wins rule.
- ⬜ **[POL-007]** Implement loop/cycle runtime safeguards where activated.
- ⬜ **[POL-008]** Preserve activation `!= response success`.

### Review/reminder/automatic effects

- ⬜ **[REM-001]** Implement immediate review/confirmation policy.
- ⬜ **[REM-002]** Implement later/end-of-day review policy.
- ⬜ **[REM-003]** Implement weekly review policy.
- ⬜ **[REM-004]** Implement silent-unresolved policy.
- ⬜ **[REM-005]** Implement explicitly authorized bounded automatic Outcome.
- ⬜ **[REM-006]** Preserve automatic effect provenance and no fake human Confirmation.
- ⬜ **[REM-007]** Implement Reminder intent separate from delivery.
- ⬜ **[REM-008]** Reuse Shared Email Platform for email delivery where configured.
- ⬜ **[REM-009]** Ensure durable intent/commit-before-provider-I/O semantics.
- ⬜ **[REM-010]** Handle ambiguous provider result without blind resend.
- ⬜ **[REM-011]** Implement user notification controls/quiet-hours/repetition when delivery channels support them.
- ⬜ **[B10-T01]** Completion-relative anchor tests.
- ⬜ **[B10-T02]** Anchor-stream duplicate/qualification tests.
- ⬜ **[B10-T03]** Conditional activation-mode tests.
- ⬜ **[B10-T04]** Policy conflict/loop safeguard tests.
- ⬜ **[B10-T05]** Automatic Outcome provenance tests.
- ⬜ **[B10-T06]** Reminder intent/email outbox/provider ambiguity tests.
- ⬜ **[B10-T07]** Daily/weekly review aggregation tests.
- ⬜ **[B10-T08]** Manual `userTest` review/reminder acceptance.

## 34.13 B11 — Replanning / conflict / solver

- ⬜ **[RPL-001]** Re-open movement/replanning/solver Physical authority before implementation.
- ⬜ **[RPL-002]** Build candidate input from current accepted Schedule/constraints, not stale ViewModel.
- ⬜ **[RPL-003]** Include hard constraints.
- ⬜ **[RPL-004]** Include soft constraints/preferences.
- ⬜ **[RPL-005]** Include movement policy.
- ⬜ **[RPL-006]** Include relevant hidden Life Area commitments under visibility rules.
- ⬜ **[RPL-007]** Preserve candidate `!= accepted Schedule`.
- ⬜ **[RPL-008]** Explain affected items/trade-offs without hidden-data leakage.
- ⬜ **[RPL-009]** Implement smallest useful replan scope.
- ⬜ **[RPL-010]** Implement move fallback.
- ⬜ **[RPL-011]** Implement postpone fallback.
- ⬜ **[RPL-012]** Implement skip fallback.
- ⬜ **[RPL-013]** Implement shorten fallback where semantics permit.
- ⬜ **[RPL-014]** Implement split fallback where semantics permit.
- ⬜ **[RPL-015]** Implement replacement fallback preserving original intention/history.
- ⬜ **[RPL-016]** Implement dependency/day/week scope expansion only when required.
- ⬜ **[RPL-017]** Preserve this-occurrence vs future-source scope.
- ⬜ **[RPL-018]** Revalidate expected state before applying candidate.
- ⬜ **[RPL-019]** Ensure solver unavailable/fails → canonical state unchanged.
- ⬜ **[B11-T01]** Hard/soft constraint solver tests.
- ⬜ **[B11-T02]** Candidate-vs-accepted test.
- ⬜ **[B11-T03]** Stale candidate conflict test.
- ⬜ **[B11-T04]** Minimal scope/fallback tests.
- ⬜ **[B11-T05]** Hidden-conflict privacy/non-interference tests.
- ⬜ **[B11-T06]** Manual `userTest` proposal/explanation/apply acceptance.

## 34.14 B12 — Provider / offline / multi-device

### Provider

- ⬜ **[EXT-001]** Re-open ExternalRef/provider integration authority.
- ⬜ **[EXT-002]** Implement provider Event identity mapping separate from DANTE Event.
- ⬜ **[EXT-003]** Implement provider recurring-series/instance mapping separate from DANTE Occurrence.
- ⬜ **[EXT-004]** Implement import/update assertion path.
- ⬜ **[EXT-005]** Implement provider deletion/tombstone handling.
- ⬜ **[EXT-006]** Preserve provider Schedule `!= accepted DANTE Schedule`.
- ⬜ **[EXT-007]** Implement detached recurring-instance mapping/reconciliation.
- ⬜ **[EXT-008]** Handle unsupported/lossy recurrence mappings explicitly.
- ⬜ **[EXT-009]** Preserve user correction against blind provider overwrite.
- ⬜ **[EXT-010]** Expose truthful external apply pending/success/failure/ambiguous state.
- ⬜ **[EXT-011]** Implement imported Session provider/source/device provenance.
- ⬜ **[EXT-012]** Implement duplicate imported Session detection/reconciliation.

### Offline / multi-device

- ⬜ **[SYNC-001]** Confirm/activate selected local-sync technology only through Physical gate.
- ⬜ **[SYNC-002]** Preserve local/synced copy as noncanonical.
- ⬜ **[SYNC-003]** Expose pending/offline mutation state truthfully.
- ⬜ **[SYNC-004]** Implement reconnect/replay idempotency.
- ⬜ **[SYNC-005]** Implement expected-state reconciliation after offline period.
- ⬜ **[SYNC-006]** Implement Web/Mobile concurrent Session control reconciliation.
- ⬜ **[SYNC-007]** Implement device clock drift handling.
- ⬜ **[SYNC-008]** No silent last-write-wins.
- ⬜ **[B12-T01]** Provider Event/Occurrence identity tests.
- ⬜ **[B12-T02]** Provider tombstone tests.
- ⬜ **[B12-T03]** Unsupported recurrence mapping tests.
- ⬜ **[B12-T04]** User-correction vs provider-update tests.
- ⬜ **[B12-T05]** Imported Session duplicate/reconciliation tests.
- ⬜ **[B12-T06]** Offline replay/idempotency tests.
- ⬜ **[B12-T07]** Concurrent Web/Mobile Session race tests.
- ⬜ **[B12-T08]** Device clock drift tests.
- ⬜ **[B12-T09]** Provider ambiguous-result tests.
- ⬜ **[B12-T10]** Manual `userTest` provider/offline acceptance on supported surfaces.

## 34.15 B13 — Analytics / Statistics / Signals

- ⬜ **[ANA-001]** Implement scheduled-duration metric.
- ⬜ **[ANA-002]** Implement Session elapsed-duration metric.
- ⬜ **[ANA-003]** Implement Session active-duration metric.
- ⬜ **[ANA-004]** Implement paused-duration metric.
- ⬜ **[ANA-005]** Implement early/late start metric against correct Schedule state.
- ⬜ **[ANA-006]** Implement early/late finish metric.
- ⬜ **[ANA-007]** Implement overrun/underrun metric.
- ⬜ **[ANA-008]** Implement Schedule revision/reschedule statistics.
- ⬜ **[ANA-009]** Implement postpone/cancel/skip patterns without generic status ontology.
- ⬜ **[ANA-010]** Implement expected Occurrence counts.
- ⬜ **[ANA-011]** Implement Actual coverage.
- ⬜ **[ANA-012]** Implement context-specific Outcome distributions.
- ⬜ **[ANA-013]** Implement Confirmation coverage where policy requires it.
- ⬜ **[ANA-014]** Implement time allocation by Life Area.
- ⬜ **[ANA-015]** Implement tag/context aggregation.
- ⬜ **[ANA-016]** Implement day/week/month/year range trends with correct timezone boundaries.
- ⬜ **[ANA-017]** Implement Routine adherence from Occurrence+Actual+Outcome+Confirmation basis.
- ⬜ **[ANA-018]** Implement streak only as derived evaluated metric where defined.
- ⬜ **[ANA-019]** Distinguish raw Session sum vs unique wall-clock coverage.
- ⬜ **[ANA-020]** Support intentional overlapping multi-domain contribution.
- ⬜ **[ANA-021]** Use corrected current accepted truth for ordinary analytics while preserving audit history.
- ⬜ **[ANA-022]** Ensure deleted/redacted source does not survive as hidden undeletable derived copy.
- ⬜ **[ANA-023]** Preserve product analytics `!= OTel/Grafana observability`.
- ⬜ **[ANA-024]** Do not introduce universal productivity/success/performance score without future Criterion semantics.
- ⬜ **[B13-T01]** Planned-vs-actual calculation tests.
- ⬜ **[B13-T02]** Overlap/unique-wall-clock tests.
- ⬜ **[B13-T03]** Routine adherence tests.
- ⬜ **[B13-T04]** Corrected-history analytics tests.
- ⬜ **[B13-T05]** Timezone/DST period-boundary tests.
- ⬜ **[B13-T06]** Life Area/tag aggregation tests.
- ⬜ **[B13-T07]** Privacy/deletion/non-interference analytics tests.
- ⬜ **[B13-T08]** Manual `userTest` statistics acceptance.

## 34.16 Cross-cutting history / provenance / security / privacy / recovery

These items span blocks and turn green only when their required implementing slices exist and have been proven.

- ⬜ **[HIST-001]** Owner identity remains separate from material state in every implemented mutable facet.
- ⬜ **[HIST-002]** Explicit current accepted state used; no latest-row/UUID inference.
- ⬜ **[HIST-003]** Correction preserves historical lineage.
- ⬜ **[HIST-004]** Material change invalidates old Confirmation/Acknowledgement applicability where required.
- ⬜ **[PROV-001]** Consequential source/actor/device/provider provenance preserved.
- ⬜ **[PROV-002]** Provenance never treated as truth by itself.
- ⬜ **[RECON-001]** Competing assertions can remain unresolved; no universal newest/provider/user winner.
- ⬜ **[AUTH-001]** DanteContext/Account/self-Person boundary respected by all temporal operations.
- ⬜ **[AUTH-002]** Person != Account != Principal != Actor preserved in APIs/persistence.
- ⬜ **[AUTH-003]** Consequential Authority/Visibility/Consent basis retained where applicable.
- ⬜ **[PRIV-001]** Sensitive temporal details can be projected as safe busy/free without leaking hidden title/context.
- ⬜ **[PRIV-002]** Counts/explanations/analytics respect non-interference/visibility.
- ⬜ **[PRIV-003]** Retention/deletion/redaction path distinct from semantic correction.
- ⬜ **[PRIV-004]** Derived user-linked data honors deletion/retention policy.
- ⬜ **[RECOV-001]** New canonical temporal state included in backup/restore considerations.
- ⬜ **[RECOV-002]** PITR/restore cannot silently resurrect retired accepted MaterialState.
- ⬜ **[RECOV-003]** New outbox/provider state has explicit recovery/reconciliation behavior.
- ⬜ **[OBS-001]** Temporal operations instrumented for operational observability without changing semantic outcomes.
- ⬜ **[OBS-002]** Observability outage cannot change canonical operation truth.

## 34.17 Read models / Timeline / Detail / range-query completeness

- ⬜ **[READ-001]** Timeline sourced only from real normalized backend/application read model in normal runtime.
- ⬜ **[READ-002]** Timeline projection preserves stable owner/Occurrence identity.
- ⬜ **[READ-003]** Timeline card `!= DB row/backend DTO` boundary maintained.
- ⬜ **[READ-004]** Planning Tray read model distinguishes unplaced Activity reason.
- ⬜ **[READ-005]** Future unified no-placement UI distinguishes postponed Event/flexible Occurrence from unplaced Activity.
- ⬜ **[READ-006]** Resolution Queue derived from exact unresolved reason.
- ⬜ **[READ-007]** Detail/History consumes canonical semantics without inventing new owner model.
- ⬜ **[READ-008]** Range query supports user-local day semantics.
- ⬜ **[READ-009]** Range query supports all-day/date spans.
- ⬜ **[READ-010]** Range query supports coarse placement semantics.
- ⬜ **[READ-011]** Range query defines paging/cursor/horizon deterministically.
- ⬜ **[READ-012]** Range query applies current/history/visibility/cancellation filters correctly.
- ⬜ **[READ-013]** Recurrence materialization output integrates without browser canonical synthesis.
- ⬜ **[READ-014]** 23h/25h local days handled correctly.
- ⬜ **[READ-015]** Frozen T1 interaction behavior preserved throughout all integrations.

## 34.18 B14 — Whole-vertical closure tests and proof

- ⬜ **[CLOSE-001]** Re-run full master `!=` closure sweep against implementation.
- ⬜ **[CLOSE-002]** Verify no generic Task/Status/done/repeat/due_at/assigned_to shortcuts entered implementation.
- ⬜ **[CLOSE-003]** Verify no runtime fake Timeline cards/mock repositories remain.
- ⬜ **[CLOSE-004]** Verify every ledger item is `✅` or covered by explicit approved scope amendment.
- ⬜ **[CLOSE-005]** Re-run all 38 final pre-roadmap adversarial scenarios.
- ⬜ **[CLOSE-006]** Full backend unit/application suite green.
- ⬜ **[CLOSE-007]** Full direct PostgreSQL acceptance suite green.
- ⬜ **[CLOSE-008]** Full API/integration suite green.
- ⬜ **[CLOSE-009]** Full frontend unit/component suite green.
- ⬜ **[CLOSE-010]** Full T1/F0/C1 regression suite green.
- ⬜ **[CLOSE-011]** Full real-backend E2E suite green.
- ⬜ **[CLOSE-012]** Full timezone/DST suite green.
- ⬜ **[CLOSE-013]** Full idempotency/concurrency suite green.
- ⬜ **[CLOSE-014]** Full recurrence/Occurrence history suite green.
- ⬜ **[CLOSE-015]** Full Session multi-device/offline suite green for activated surfaces.
- ⬜ **[CLOSE-016]** Full privacy/visibility/non-interference suite green.
- ⬜ **[CLOSE-017]** Full provider/reconciliation suite green for activated providers.
- ⬜ **[CLOSE-018]** Recovery/PITR anti-resurrection proof green.
- ⬜ **[CLOSE-019]** Timeline/range/review/analytics performance and query-plan review green.
- ⬜ **[CLOSE-020]** Alembic/SQLAlchemy/Dictionary/database docs/live PostgreSQL alignment green.
- ⬜ **[CLOSE-021]** Runtime ACL/owner/migrator/observer proof green for all new DB objects.
- ⬜ **[CLOSE-022]** Manual desktop `userTest` whole-vertical walkthrough green.
- ⬜ **[CLOSE-023]** Manual mobile/responsive `userTest` whole-vertical walkthrough green for supported surfaces.
- ⬜ **[CLOSE-024]** Accessibility acceptance green.
- ⬜ **[CLOSE-025]** Documentation drift audit green.
- ⬜ **[CLOSE-026]** Branch closure rules re-read and satisfied before protected-main integration.

---

# 35. Current execution state

Current workstream state:

```text
SEMANTIC MAP / AUDITS / ROADMAP              ✅ COMPLETE
B00 REAL DATA SPINE                          ✅ CLOSED
B01 ACTIVITY CORE                            ✅ CLOSED
B02 SCHEDULE CORE                            🟨 IN PROGRESS — B02-A/B/C/D + B02-E1 proven; E2 next
CANDIDATE DATABASE                           🟨 Alembic _25 E1 proven on real PostgreSQL; Dictionary/final reconciliation pending
B00 MANUAL userTest                          ✅ APPROVED — 2026-09-08
B01 MANUAL userTest                          ✅ APPROVED — 2026-09-08
EXACT-HEAD RECONCILIATION                     ✅ run 34261607749 on 303e75c56716008bfc352e92411884760727e043
EPHEMERAL B01 RECONCILIATION WORKFLOW         ✅ REMOVED IN B00/B01 CLOSURE
NEXT EXECUTION GATE                           B02-E2 Timeline read projection and DST
```

B00 established the truthful real-data spine: normal runtime no longer substitutes prototype Timeline data or fake persistence for backend truth. B01 established the first PostgreSQL-backed temporal product write/read path: one canonical unplaced Activity identity created through governed idempotent backend semantics and projected through the real Planning Tray.

B01 deliberately did **not** implement Schedule, estimated effort, Event, Routine, Session, Actual, Outcome or generic completion. Those capabilities remain governed by their later roadmap gates. In particular, Planning Tray `list_unplaced()` is valid for B01 because no Schedule history exists yet; B02 must redefine “unplaced” as absence of a **current accepted placement**, not absence of any historical Schedule row.

B02 Schedule authority/current CP6 placement truth is frozen in the B02 execution plan. The branch now contains candidate B02-A atomic scheduled creation and candidate B02-B placement of an existing unplaced Activity onto a new accepted Schedule/current placement. B02-B preserves the Activity identity, invalidates/refetches the authoritative Timeline, and defines Planning Tray membership as absence of a current accepted placement. These are implementation candidates only: the SCH/B02-T ledger remains open until the deferred automated and manual evidence gates pass.

Candidate B02-C now routes Timeline movement and anchored time editing through one bounded Schedule revision operation. The exact current placement MaterialStateRef is the concurrency basis; the same ScheduleRef survives, prior placement history remains, stale state conflicts, and the frontend waits for authoritative reload instead of presenting an optimistic canonical move. This remains candidate implementation, not executed evidence.

Candidate B02-D now routes Timeline unschedule and Undo through bounded self-scoped capabilities. Unschedule closes the exact current history episode and removes only explicit currentness; guarded Undo requires the exact receipt plus continued absence/no later history and creates a new monotonic placement state. Timeline and Planning Tray wait for authoritative refresh, so failures never manufacture canonical absence or restoration. Tests are authored but deliberately not executed in this slice.

This ledger is intentionally verbose. Its purpose is to make omission visible: if a capability or required proof is not green, it is not done.


### B02-E1 evidence reconciliation — 2026-09-15

The approved B02-E1 backend slice is proven at commits `db057a422361122f7eed506239b6489c35d7d520` and `dca566180ac96f4072820de60946a72d9ab99ba3`. Local unit/value proof passed (`29 passed, 2 deselected`), followed by real PostgreSQL proof supplied by the user (`4 passed, 2 deselected in 9.66s`). No CI was run.

This promotes only the canonical placement union, coarse local-period DDL/ACL, generic establish/revise/unschedule/Undo behavior, typed payload totality, history/current invariants and 0..N Schedule ownership. B02-T05 and all E2/E3/E4 obligations remain open.
