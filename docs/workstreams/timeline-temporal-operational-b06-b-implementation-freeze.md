# Timeline / Temporal-Operational — B06-B Recurrence Authoring Freeze

- **Status:** implementation authority — B06-B active
- **Date:** 2026-09-21
- **Predecessor:** B06-A ✅ CLOSED / PROVEN at Alembic `20260921_51`
- **CI / Actions:** none; direct local proof remains user-run

## 1. Exact semantic boundary

```text
Routine != Recurrence != Occurrence != Schedule
recurrence revision != one-occurrence exception
structural exclusion != generated-and-skipped Occurrence
current administrative MaterialState != effective state for every future coordinate
```

B06-B authors immutable, owner-bound Recurrence MaterialStates only. It creates
no Occurrence row, Activity, Event instance, Schedule, Session, Actual or
Timeline projection. Occurrence evaluation/checkpoint and reconciliation remain
strictly B06-C; shared Schedule/Timeline/UI flows remain B06-D.

Routine stays the source/lifecycle/product aggregate introduced by B06-A.
Event stays the B03 Event aggregate. Neither is converted into the other and
there is no generic series root.

## 2. Canonical command model

The public transport is a discriminated, strongly typed union. It is not an
RRULE string, a generic JSON recurrence blob, a polymorphic source edge or a
frontend-calculated expansion.

```text
PUT Routine current Recurrence   expected current MaterialStateRef required
PUT Event current Recurrence     expected current MaterialStateRef required on revise,
                                 absent only for the first Event Recurrence
GET Routine/Event current Recurrence  typed canonical state read
```

Each replacement command carries a stable actor-local operation id and an
intent fingerprint. Replaying the same command returns the accepted immutable
state; reusing the id for a different intent fails. A stale expected state
fails. A replacement closes the previous current-history interval, creates a
new MaterialState/address/payload/history interval and moves the bounded CP6
current-facet binding atomically.

The new state is administratively current immediately but has an explicit
effective boundary. A later evaluator must select the state effective for the
candidate coordinate from retained history/boundaries; it must not rewrite the
old state or erase materialized future history. That evaluator/reconciliation is
owned by B06-C.

## 3. Four accepted families

| Family | Canonical payload | Must not become |
|---|---|---|
| `calendar_wall_clock` | calendar pattern, selectors, optional wall-time set, clock basis, explicit effective range and optional pattern anchor | elapsed timer or accepted Schedule |
| `elapsed_interval` | positive elapsed seconds, fixed/previous-expected anchor mode, absolute anchor and absolute effective range | wall-clock calendar pattern |
| `quota_per_period` | positive quota, period unit/span, frame/zone/week start and date range | fabricated timed card or Goal progress |
| `cyclic_positional` | anchor date, day/week position unit, complete cycle positions and date range | recurrence of a completed execution |

`expected_count` counts generated expectations, including a later skipped one;
it never counts completed Actuals. Completion-relative and anchor-stream
families remain B11.

## 4. DST and timezone contract

`named_zone` calendar Recurrences persist both an IANA zone and an immutable
policy companion on the same MaterialState:

```text
nonexistent local civil time (spring gap)  -> skip_civil_candidate
ambiguous local civil time (fall overlap)  -> earlier | later
```

The API has no implicit library default. `floating_local` accepts no named-zone
or DST policy. `absolute_utc` accepts neither wall-clock zone nor DST policy.
The policy is historical state: revising it creates a new Recurrence state.

## 5. Effective-boundary and exception firewall

`pattern_anchor` and `effective_from` are independent. A change “this and
future” is a full new Recurrence state with an explicit effective boundary;
the preceding state remains immutable and historically addressable. B06-B does
not expose “this occurrence”, `skip`, `cancel`, `delete occurrence` or
`extra`; those are B06-C occurrence operations.

Pausing or ending a Routine remains source lifecycle. It neither deletes a
Recurrence nor synthesizes skipped/cancelled Occurrences.

## 6. Persistence and security shape

The existing CP6-M04 family tables, addresses, current views and deferred
aggregate checks are reused. B06-B adds exactly:

```text
routine_recurrence_calendar_dst_policy
event_recurrence_calendar_dst_policy
routine_recurrence_operation
event_recurrence_operation
```

The two policy rows persist the named-zone gap/overlap disposition. The two
receipt tables provide owner-specific idempotency; no `(kind,id)` generic owner
table is introduced. Runtime retains EXECUTE-only access through self-scoped
security-definer functions; raw CP6 writes stay denied.

## 7. Closure proof required

Direct proof must cover Routine and Event ownership; all four families; every
calendar selector form; open/until/count ranges; state CAS/replay/collision;
old-history closure/new-current equivalence; self isolation/ACL; floating vs
named-zone vs absolute separation; named-zone spring-gap and fall-overlap
policy persistence; and no Occurrence/Schedule/Activity materialization.

Generated OpenAPI/client, mapping/catalog/dictionary reconciliation and the
typed remote contract are part of B06-B closure. No CI/Actions are launched.
