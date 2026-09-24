# B08-C — TC-009 Session Minimum Duration

- **Status:** implementation contract for the B08-C candidate
- **Reconciled:** 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Prior frontier:** B08-B / Alembic `20260924_64`
- **Candidate frontier:** B08-C / Alembic `20260924_65`
- **Authority:** `docs/domain/concepts/temporal-constraint.md`, `docs/domain/concepts/session.md`, B08 roadmap and current B08-B runtime

## 1. Activated subset

B08-C activates TC-009 as one typed duration rule:

```text
family             = duration
duration kind      = minimum
constrained facet  = session.active_duration
strength           = soft
subject             = directly constrained Activity
threshold           = positive integer microseconds
```

The existing immutable `temporal_constraint_state` and `temporal_constraint_duration_state` remain the canonical rule and payload. B08-C adds no table, routine, trigger, index or relationship family. Alembic `_65` widens the admitted facet, replaces the existing deferred totality function, and forward-renames the schedule-named duration mutation routine to `mutate_self_temporal_duration_constraint` before replacing its bounded implementation. The rename keeps routine counts flat while making the shared Schedule/Session duration contract explicit.

The existing Create Activity `splittable` minimum field authors this rule atomically with the Activity. Other execution settings such as session count, partial completion, early finish, and merge compatibility remain outside this B08-C activation.

## 2. Meaning of the constrained fact

```text
Session elapsed duration = end/start wall-clock span
Session paused duration  = captured pauses within that span
Session active duration  = elapsed duration - paused duration
```

The rule compares against the active duration of exactly one Session. Separate Session identities are never summed. Planned Schedule duration, Activity estimated effort, Session elapsed duration, and Session active duration remain distinct.

The constraint binds directly to an Activity. Occurrence Sessions do not inherit this rule from a Routine, Event, or source Activity. B08-C does not add Occurrence-owned Temporal Constraints; that requires a separately reviewed ownership/applicability slice.

## 3. Read-time evaluation and effects

Session reads return each directly owned current Session-duration rule with its rule and MaterialState references, threshold, soft strength, and derived evaluation:

| Session fact | Evaluation |
|---|---|
| Open, active time below minimum | `pending` |
| Active time at or above minimum | `satisfied` |
| Ended, active time below minimum | `violated` |

Evaluation is a read-time projection at the Session `evaluated_at`; it is not a new canonical state, completion, Actual, or Outcome. A violation never blocks Pause, Resume, or End and never implies Activity completion. No Schedule is created or changed.

Schedule-placement evaluation filters out `session.active_duration` rules. B08-C does not reinterpret the Session threshold as planned placement length or add hard Schedule movement semantics.

## 4. Database admission and disambiguation

The forward migration preserves B04-E Schedule-duration behavior and adds only this row-totality branch:

```text
schedule.placement: minimum or maximum, hard or soft
session.active_duration: minimum + soft + directly owned Activity only
```

The governed mutation capability rejects a Session facet on Event or other owner families, maximum Session duration, and hard Session minimum. Deferred typed-payload totality remains authoritative; runtime has no direct DML grant. Session evaluation reads the current rule under authenticated self scope.

The B08-C subset deliberately does not claim duration maximums, hard Session duration, Event/Occurrence Session constraints, inherited Routine/Event policy, spacing/recovery, or aggregation across Sessions.

## 5. Proof obligations

User-run proof must cover:

```text
Alembic reaches 20260924_65 with current topology reconciled
OpenAPI and generated API client match the Session evaluation contract
Create Activity persists one soft minimum active-duration MaterialState
rule survives authoritative read and immutable current/history contract
open below threshold is pending; ended below threshold is violated
paused time is excluded; one Session is not combined with another
violated policy does not prevent Session END
Schedule evaluation ignores session.active_duration
Occurrence receives no inherited Activity/Routine rule
Timeline/Create UI displays the configured minimum and current evaluation
no Activity completion, Actual, Outcome or Schedule mutation is fabricated
```

Automated and real-stack proof remains user-run. The checked-out candidate is not marked proven until that evidence is recorded.
