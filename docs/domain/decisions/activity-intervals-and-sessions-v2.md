# Activity intervals, planned Sessions, real Sessions — current product contract

- **Status:** CURRENT BRANCH CANDIDATE / accepted product semantics; implementation pending local proof
- **Date:** 2026-10-05
- **Scope:** timed Activity Create and Timeline; supersedes the Timeline card rule in `activity-planned-session-reschedule-product-v1.md`

**Current live execution/card overlay:** `activity-session-live-timeline-v1.md` defines the presentation-only reality geometry, main/internal execution controls, five-minute Session desk, and no-duplicate-card rules. This file continues to own the independent accepted Activity interval/technical envelope model.

## Three separate meanings

| Product name | Canonical persistence | Meaning |
| --- | --- | --- |
| Activity interval | Activity-owned Schedule, `interval` role | One accepted period during which the Activity is placed and shown as occupied on the Timeline. |
| Planned Session | Activity-owned Schedule, `planned` role | A future intended execution episode added with `+ Sessione`. It is nested planning detail; it is not a B08 Session. |
| Real Session | B08 Session | Execution that began through Play or was truthfully recorded afterward. |

The Activity keeps one identity across its intervals. `Schedule != Session != Actual`. Neither an Activity interval nor a planned Session asserts that work happened. The existing `planned_slices` API and `planned` database roles continue to mean future planned Sessions. New `activity_intervals` and the `interval` role mean only Activity placement. Existing data must not be relabelled during migration.

An Activity planned Session can be created without an orario. Its Activity-owned Schedule has the explicit `planned` role and no current or historical placement until the user assigns one. This is the only new-Schedule exception to the deferred owner-placement check; Event, envelope and interval Schedule owners still require a current placement at creation. The absence of a time must be stored as absence, never as an invented placement. This is planning intent, not evidence of a real B08 Session.

## Create and Timeline

The main Activity date/time fields define interval 1. `+ Aggiungi intervallo` below them adds another independently editable date/start/end row. The number of rows replaces the `Unica / Suddivisa` control. Rows have positive duration, use the Activity time frame and do not overlap; gaps are permitted. The additional intervals are available for timed Activities only, up to 100 total.

For example, one Activity can occupy 14:00–15:00 and 17:00–18:00. The Activity's parent `envelope` Schedule spans 14:00–18:00 solely for containment and existing structural relations; it does not make 15:00–17:00 occupied. The Timeline exposes the two `interval` Schedule placements as separate cards sharing the same Activity ref and title, with distinct Schedule refs. `planned` rows remain within Activity detail and do not create cards. An older Activity without `interval` roles retains its envelope card. Existing planned Session rows remain intact.

The parent envelope equals the first interval's start through the last interval's end. A server authoring command validates ownership, time frame, order, no overlap and exact envelope coverage; one transaction creates the Activity, envelope, intervals, future planned Sessions and any other accepted structure. Operation replay must retain the same identity and intent. A client cannot invent a second Activity or Session to represent an extra interval.

## Subsequent changes

Moving, resizing or removing an interval must maintain its parent envelope and preserve any planned Sessions and dependent placements. The previous `activity-planned-session-reschedule-product-v1.md` preview/admission rules for dependent planned Sessions remain applicable; they refer to the envelope as a containment boundary. A dedicated coordinated update command is still required before the Timeline may present a standalone interval drag/resize as a complete multi-interval replan. Direct Schedule mutation must not silently rewrite other intervals or planned Sessions.

The shared direct Schedule revision and unschedule application paths reject interval rows and the technical envelope of an Activity with intervals using `temporal.schedule.activity_interval_requires_replan` (409). The Timeline shows the reason when an old drag/remove action is attempted. Create permits editing/removing unsaved rows; a later post-create replan requires the coordinated command rather than mutating one Schedule in isolation. This gate is an application boundary; other scheduling capabilities still require audit before whole-vertical closure.

**Proof status:** The backend OpenAPI export and client regeneration completed; web/API-client TypeScript typechecks and Python Ruff checks passed. No tests, local PostgreSQL migration gate, or real-app visual acceptance were run. Do not mark the candidate closed until the user's local acceptance.

The B12 Plan conflict diagnostic intentionally retains its 40-Schedule limit and reports multiple accepted intervals as an unresolved basis; it cannot yet evaluate a multi-interval Activity as a single Plan step. The B14/B07 candidate therefore does not claim full solver support for this new shape. Its placement read excludes the technical envelope and future planned Sessions so it cannot treat gaps as placed work.
