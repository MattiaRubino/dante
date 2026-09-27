# B11-C — Schedule-relative personal Reminder — Scope Gate

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Parent:** B11 Advanced Recurrence / Conditional / Reminder
- **Status:** APPROVED SEMANTIC SCOPE; implementation and local gates closed 2026-09-27
- **Persistence predecessor:** `20260927_85`
- **Closure evidence:** `timeline-temporal-operational-b11-c-closure-2026-09-27.md`

## Purpose and owner

B11-C makes the Create reminder-lead intent and an in-app temporal reminder usable for a self-owned, accepted Schedule. A Reminder is a bounded personal configuration anchored to one stable Schedule identity, not a generic notification, automation, Conditional Policy, Activity, Event, Routine, Occurrence, or delivery job.

```text
Schedule placement = accepted planned time
Reminder configuration = self-personal attention intent
due status = derived presentation from accepted Schedule and Reminder state
delivery = not part of B11-C
```

The self Person and Schedule form the stable identity key. A server-generated UUIDv7 identifies the Reminder independently of its configuration operation id. Multiple Schedules for one Activity can have distinct Reminder configurations; an Occurrence without Schedule has none.

## Admissibility and temporal meaning

Only an accepted Schedule with an unambiguous start instant is admissible: absolute interval or named-zone interval whose accepted placement resolves to an instant. Floating local time, coarse periods, all-day/date spans, unscheduled subjects, Recurrence definitions, and Routine sources are not silently coerced to instants.

`lead_minutes` is an integer from 0 through 10080. The due instant is derived from the accepted current Schedule start minus that duration. It is not copied as a second canonical timestamp. Schedule revision changes the projection; Schedule withdrawal makes it unavailable. Past MaterialStates and accepted Schedule placement history remain unchanged.

The in-app read may report `pending`, `due`, or `unavailable` relative to the server's query instant. It does not report `sent`, `seen`, `acknowledged`, or `completed`. A due read is repeatable, not an exactly-once emission. A past-due configuration does not assert that a notification was delivered.

## State, authority, and concurrency

The Reminder's configuration is immutable append-only MaterialState: `enabled`/`disabled` plus `lead_minutes`, with an explicit accepted-current binding and history. Disabling is a new state, not deletion or history rewind. Each change uses expected-current-state compare-and-swap and a bounded operation id/fingerprint; replay of identical intent returns the same accepted result, while key reuse for different intent rejects. PostgreSQL is the sole evaluator of self ownership, current Schedule placement, and current Reminder state.

```text
idempotency key != Reminder identity
current accepted state != latest row
projection != canonical truth
Reminder != Schedule != Actual
Reminder due != happened / notification sent
```

No caller-supplied due status or delivery result becomes truth.

## Public vertical and Create behavior

The complete capability comprises forward-only Alembic after `_85`, SQLAlchemy mappings, Dictionary/current DB reference, backend guarded functions and runtime, self-scoped API/OpenAPI, generated client from the repository generator, web data source and visible controls, local automated tests, and reconciled workstream documents. Domain, Logical, and Physical current references receive only the narrowly accepted semantics; historical evidence is not rewritten.

The Create reminder selector is offered only when the selected Create path can produce an admissible Schedule. After the Schedule commit, a separate guarded command configures its Reminder. A failure in that second command is shown as a partial success with a retry path keyed to the committed Schedule; the UI never calls the whole Create a failure and never repeats the subject creation to hide the partial effect. Unsupported paths do not collect a value they silently drop.

Existing-Schedule controls read and configure the same canonical Reminder, including after reload. Generated client files are never edited manually.

## Local proof and exclusions

Focused PostgreSQL tests cover admissibility, self ownership, stable identity, current-state history, exact Schedule/current placement, CAS, idempotency/conflict, Schedule revision/withdrawal, temporal `pending/due/unavailable`, no delivery, and no Actual/Outcome mutation. API/OpenAPI, deterministic generated-client check, web typecheck/tests and relevant B11-A/B regressions are required. The user runs local tests; no CI/GitHub Actions. The integrated real-app walkthrough is reserved for whole-B11 closure.

Out of scope: push/email/OS notification, provider delivery, outbox worker, retry/dedup of delivery, recurring Reminder without an accepted Schedule, all-day/floating reminder precision, configurable global inheritance, automatic outcome/confirmation, solver/replanning, and generic trigger/policy/workflow engines. These require separately reviewed semantics rather than a shortcut in B11-C.
