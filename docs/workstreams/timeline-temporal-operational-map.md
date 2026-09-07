# Timeline / Temporal-Operational Vertical — Semantic Work Map

- **Status:** DRAFT / SEMANTIC BOUNDARY MAP
- **Branch:** `feature/timeline-temporal-operational`
- **Purpose:** freeze the semantic work map before roadmap / implementation ordering.
- **Important:** this document is not a roadmap, not an implementation plan, not schema authority, and does not reopen Domain / Logical / Physical / CP1–CP6.

## 1. Vertical boundary

The vertical represents what the user intends to do or expects to happen, its temporal placement, repetition, specific expected instances, actual execution/reality, bounded result semantics, corrections/history, and Timeline projection.

### In scope

- Activity
- Event
- Routine
- Occurrence
- Schedule
- Temporal Constraint
- Recurrence
- Session
- Actual
- Outcome
- material/current/history semantics required by those capabilities
- corrections/replacement/reconciliation where required
- provenance where consequential
- time/range queries
- Timeline projection

### Out of scope for this vertical unless an explicit later scope reopens them

- Goal / Plan / Milestone as owners
- Observation / tracking vertical
- Availability / Capacity / Reservation
- Resource Requirement / Allocation
- broad collaboration/governance vertical
- AI orchestration
- generic Search vertical

`connectable owner != owner implemented by this vertical`.

## 2. Work-map classifications

### TOP-LEVEL
May originate directly from a user action through the creation/recording gateway.

- Activity
- Event
- Routine
- Session recording

### CONTEXTUAL
Semantically real, but usually created/changed within another owner's lifecycle.

- Schedule
- Temporal Constraint
- Recurrence
- Occurrence
- Actual
- Outcome
- Responsibility / Participation where a concrete operation requires them

### DERIVED / PROJECTION
Not independent canonical truth.

- Timeline
- range-query results
- current placement display
- history/detail projections
- derived early/late/overrun/underrun style labels

### INTERNAL
Persistence/runtime mechanisms, never user-facing creation concepts.

- NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef
- native/scoped/material addressing
- current accepted-state bindings
- current-history controls
- UUIDv7 issuance
- transaction / idempotency / locking mechanics
- SQLAlchemy rows
- Alembic revisions
- DB trigger/routine enforcement
- Occurrence generation coordinate tables

## 3. High-level tree

```text
TIMELINE / TEMPORAL-OPERATIONAL
│
├── ORIGINATING OWNERS
│   ├── Activity                   TOP-LEVEL
│   ├── Event                      TOP-LEVEL
│   ├── Routine                    TOP-LEVEL
│   └── Session                    TOP-LEVEL recording / CONTEXTUAL execution
│
├── EXPECTATION / TEMPORAL CONTEXT
│   ├── Schedule                   CONTEXTUAL
│   ├── Temporal Constraint        CONTEXTUAL
│   ├── Recurrence                 CONTEXTUAL
│   └── Occurrence                 CONTEXTUAL / generated identity
│
├── REALITY / REALIZATION
│   ├── Session                    TOP-LEVEL or CONTEXTUAL
│   ├── Actual                     CONTEXTUAL
│   └── Outcome                    CONTEXTUAL
│
├── CONNECTABLE CONTEXT
│   ├── Responsibility
│   ├── Participation
│   ├── Person / Actor
│   └── Place
│
├── SHARED SEMANTIC INFRASTRUCTURE
│   ├── Material State
│   ├── explicit current accepted state
│   ├── history
│   ├── correction / replacement / reconciliation
│   └── provenance where consequential
│
└── PRODUCT / QUERY PROJECTIONS
    ├── Timeline
    ├── range queries
    ├── detail
    └── history
```

This is a work tree, **not** an inheritance hierarchy and **not** a table hierarchy.

## 4. Creation / Recording Gateway

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

Observation is intentionally excluded from this vertical and belongs to a later tracking/observation vertical.

## 5. Activity

Activity is a persistent intention to act.

```text
Activity
├── identity / intention
├── Schedule                       contextual
├── Temporal Constraint            contextual
├── Session                        contextual execution
│   ├── start
│   ├── pause
│   ├── resume
│   └── end
├── Actual                         contextual realization
├── Outcome                        contextual result
├── Responsibility                 contextual
├── Place / other context          connectable
├── correction / history
└── Timeline projection            derived
```

Hard non-collapse rules:

```text
Activity != Event
Activity != Routine
Activity != Schedule
Activity != Temporal Constraint
Activity != Session
Activity != Actual
Activity != Outcome
Activity != Responsibility
Activity != performer
Activity != Participation
Activity != Goal
Activity != Plan
Activity != generic completed=true state

estimated effort != scheduled duration != actual Session duration
```

Activity has no generic recurrence owner in the accepted current baseline. Repeated behavioral intention must not be implemented as `Activity.repeat` merely for UI convenience.

Completion semantics are profile/context specific and must not be collapsed into a universal TODO/DOING/DONE kernel state.

## 6. Event

Event is occurrence-centred expectation whose temporal character is intrinsic to the represented thing.

```text
Event
├── expected-event identity
├── Schedule
├── Temporal Constraint            optional/contextual
├── Place                          connectable
├── Participation                  contextual
├── Recurrence                     contextual
│   └── Occurrences
├── Actual
├── Outcome
├── correction / provider reconciliation
└── Timeline projection
```

Hard non-collapse rules:

```text
Event != Activity
Event != Routine
Event != Schedule
Event != Occurrence
Event != participant
Event != Participation
Event != attendance
Event != Actual
Event != Outcome
Event != Place
```

Original expectation, current accepted Schedule, and actual reality must remain distinct.

Reschedule is clearly Schedule change. Postpone/cancel remain lifecycle operations whose exact semantics must not be prematurely flattened into one universal `event.status`.

## 7. Routine

Routine is persistent behavioral policy/intention.

```text
Routine
├── behavioral intention / policy
├── Recurrence
│   ├── calendar_wall_clock
│   ├── elapsed_interval
│   ├── quota_per_period
│   ├── cyclic_positional
│   └── semantically accepted but not-currently-materialized families
├── Occurrence generation
│   └── Occurrence
├── per-Occurrence Schedule
├── per-Occurrence Session / Actual / Outcome
├── recurrence correction / history
└── Timeline projection
```

Hard non-collapse rules:

```text
Routine != Activity
Routine != Event
Routine != Recurrence
Routine != Occurrence
Routine != Schedule
Routine != observed habit
```

A one-off Occurrence change/skip does not automatically change the Routine.

## 8. Recurrence

Recurrence is a rule/specification, not a native owner.

Current CP6 materialized families:

- calendar_wall_clock
- elapsed_interval
- quota_per_period
- cyclic_positional

Semantically accepted families outside the current CP6 baseline must not be faked through a generic JSON/RRULE fallback.

```text
Recurrence != Routine
Recurrence != Event
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Temporal Constraint
Recurrence != Trigger / Conditional Policy
Recurrence != provider RRULE ontology
```

Repeated applicability does not always imply Occurrence generation.

## 9. Occurrence

Occurrence is the stable identity of a specific distinguished expected instance.

```text
Occurrence
├── identity
├── source Routine/Event
├── origin
│   ├── recurrence_generated
│   └── explicit_extra
├── exact governing Recurrence MaterialState
├── generated coordinate
│   ├── calendar
│   ├── elapsed
│   ├── quota
│   └── cyclic
├── Schedule
├── Session
├── Actual
├── Outcome
└── history / provenance
```

```text
Occurrence != Event
Occurrence != Routine
Occurrence != Recurrence
Occurrence != Schedule
Occurrence != Session
Occurrence != Actual
Occurrence != Outcome
```

An Occurrence generated under recurrence state S1 remains historically governed by S1 even if the source later changes to S2.

## 10. Schedule

Schedule is current accepted temporal assignment.

Current subject eligibility:

- Activity
- Event
- Occurrence

```text
Schedule
├── subject
├── placement state
│   ├── date_span
│   ├── floating_local
│   ├── named_zone_local
│   └── absolute
├── schedule / reschedule / unschedule
├── current accepted placement
├── historical placements
├── correction
└── Timeline projection
```

```text
Schedule != Activity/Event/Occurrence
Schedule != Temporal Constraint
Schedule != Recurrence
Schedule != Availability
Schedule != Capacity Claim
Schedule != Session
Schedule != Actual
scheduled != happened
```

## 11. Temporal Constraint

Temporal Constraint owns temporal admissibility/preference/limits for a bounded target/facet.

```text
Temporal Constraint
├── target
├── constrained temporal facet
├── temporal rule
├── strictness/applicability semantics
├── material/history where consequential
└── feasibility/reasoning use
```

```text
Temporal Constraint != Schedule
Temporal Constraint != Availability
Temporal Constraint != preference automatically
Temporal Constraint != Dependency
Temporal Constraint != Recurrence
deadline != universal due_at
constraint violation in reality != invalid Actual
```

## 12. Session

Session is a bounded real execution episode and can be recorded directly or created in another owner's execution lifecycle.

```text
Session
├── identity
├── timing
│   ├── absolute
│   └── elapsed_only
├── timing precision
├── pause/resume
├── execution-context relation
├── correction
├── current timing state
├── history
└── Timeline projection
```

```text
Session != Activity
Session != Occurrence
Session != Schedule
Session != Actual
Session ended != Activity completed
Session exists != Outcome exists
```

A spontaneous Session must not require a synthetic Activity.

## 13. Actual

Actual reconciles a specific intention/expectation with established reality.

```text
Actual
├── subject Activity/Event/Occurrence
├── realization state
├── timing where applicable
├── exact Session basis where applicable
├── current accepted realization
├── historical realizations
├── correction
└── provenance
```

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != everything that happened
```

A non-realization Actual is not a generic Activity/Event failure status.

## 14. Outcome

Outcome is contextual result/disposition of realized context.

```text
Outcome
├── result semantics
├── context-specific vocabulary
├── material/history where needed
├── correction
└── detail/Timeline projection where useful
```

```text
Outcome != Actual
Outcome != Session
Outcome != Observation
Outcome != Activity status
Outcome != Milestone
no Outcome != negative Outcome
```

No universal SUCCESS/FAILURE ontology.

Outcome semantics are accepted; generic CP6 Outcome DDL is not currently materialized.

## 15. Responsibility / Participation / Person / Place

These are contextual integration points, not new top-level owners for this vertical.

```text
Responsibility != performer
Responsibility != Participation
Responsibility != Coordination Stewardship
Responsibility != Authority

Participation != Responsibility
Participation != Membership
Participation != Authority
Participation != actual attendance automatically

Person != Actor
Place != address/coordinates
expected Place != actual Place necessarily
```

Do not replace these semantics with ambiguous `assigned_to`, `owner_id`, `participant_status` or generic location fields.

## 16. History / Current / Correction / Provenance

Shared rules:

```text
identity != material state
current state != newest UUID / last row / highest revision
correction != delete history
new current state != old state never existed
```

Provenance is contextual and consequential, especially for correction, provider reconciliation and Occurrence generation. It is not a user-facing top-level create concept.

## 17. Timeline and range queries

Timeline is a derived product/query projection over canonical owners/facets; it is not a canonical owner or universal event log.

```text
Timeline != canonical state
Timeline != universal Fact log
Timeline != history table
Timeline != event store
```

Range queries are application/query capabilities and must support user-local temporal semantics without assuming every local day is 24 hours.

## 18. Explicit anti-pattern register

Do not introduce for convenience:

- generic Task
- generic TimelineEntry
- generic Entity / Thing
- generic Fact
- generic Version
- generic Relationship
- generic Status
- ambiguous `assigned_to`
- ambiguous `owner_id`
- generic `due_at`
- Activity `repeat` boolean
- generic `done` boolean
- one-table-fits-all temporal object
- JSON payloads used to bypass required semantics

## 19. Shared capability rule

A capability is implemented once and reused across eligible owners; later macro-owner work must not clone it.

```text
Activity ───────┐
Event ──────────┼── Schedule
Occurrence ─────┘

Routine ────────┐
Event ──────────┼── Recurrence ──> Occurrence

Activity ───────┐
Event ──────────┼── Actual
Occurrence ─────┘

Activity / Occurrence
        ↓
      Session

Actual / realized context
        ↓
      Outcome
```

## 20. Current state of this document

This file freezes the semantic map only. The following are intentionally **not yet fixed** here:

- implementation roadmap / stage ordering;
- exact vertical slices / milestones;
- exact API shapes;
- exact UI forms;
- new DDL decisions;
- unresolved product/profile semantics that require explicit discussion.

Those are decided only after the map is checked for missing pieces and semantic gaps.
