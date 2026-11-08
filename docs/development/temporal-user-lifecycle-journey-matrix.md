## 2026-11-08 — Second Chromium RED and isolated parallel execution

Owner's second real-stack Chromium run on `cea61d37` again exposed seven
RED journeys; the stack and PostgreSQL started correctly. The newly deepened
checks uncovered several **driver expectations that did not match product
semantics**. The Home Timeline renders a multi-day window around the selected
date, so a card still visible when navigating to date+1 is not proof that
the card moved, persisted on that date, or propagated a local change. The
journey assertions now use the canonical card `data-planned-date` (alongside
Schedule identity) to target the actual day of each instance. This also
prevents the test from accidentally selecting an original instance when it
intended to edit a future one. Quick recurrence selector values are `custom`
when the user's interval differs from one (or monthly ordinal is selected);
the submitted canonical frequency and interval remain strictly asserted.

The conversion scenario had a five-minute opaque timeout; it now has a
bounded 120-second test deadline and 35-second response-wait limit so the
next failure identifies an unconfirmed conversion POST instead of consuming
the full suite. This is **diagnostic only**, not evidence of successful
conversion.

**Concurrency:** the seven journeys have distinct synthetic user identities
and no shared fixture mutations. The lifecycle `test.describe` now opts
into `mode: 'parallel'`; launch this suite with **`--workers=2`** to
retain a conservative bound against the shared real-stack Auth rate capacity.
Do **not** raise the global `playwright.auth.config.ts` worker count or
parallelize other auth specs until their accounts and mutating database
fixtures are audited. PostgreSQL targeted checks can remain in a single
`pytest` invocation with shared fixture startup.

**PostgreSQL RED / PASS:** the owner's Session-duration progression test
passed. The new hard-delete safety test failed *before* the deletion under
test: its helper passed a null expected policy state to an already-materialized
recurring Activity. The test now reads the canonical policy and, if needed,
performs the self-scoped CAS update. This change does not establish whether
the backend correctly rejects deleting an Activity with an open Session;
the expected rejection must still be executed and verified.

**Quality gate:** Ruff reported unsorted `asyncio` import, a `PT017`
exception assertion and a format issue in the new tests. These source-level
findings were corrected without relaxing the destructive guard assertion.
All subsequent commits are **NOT RUN** on owner WSL. Re-run the seven
Chromium user lifecycle journeys with two workers, then Ruff check/format
and targeted PostgreSQL tests; inspect any remaining RED at its exact step.

# Temporal user lifecycle — authenticated journey matrix

**Scope:** Activity, Event, recurring authoring, Session, Objectives, Life Area,
B14 Create/Edit, recurring structural edit, duplication and hard deletion.

**Runtime:** Playwright authenticated HTTPS stack and migrated PostgreSQL,
using the existing playwright.auth.config.ts. These are not fixture-only
layout tests. Every scenario has a separate synthetic test account.

## Automated scenarios

| ID | User workflow | Server/persistence checks |
| --- | --- | --- |
| UJ-01 | Create one-off Activity → Edit title → Duplica → cancel delete → confirm delete → reload | Distinct Activity/Schedule identities, changed profile, original 404, duplicate persists |
| UJ-02 | Same one-off lifecycle for Event | Event profile, accepted delete, independent Event/Schedule and retained duplicate |
| UJ-03 | Recurring Activity: daily, every 2 weeks, monthly day, monthly ordinal, yearly, custom every 3 weeks with count=4 | One source per configuration, HTTP recurrence family/range, Routine inventory after reload |
| UJ-04 | Recurring Event: daily, weekly, all-day every 2 months, monthly ordinal, yearly, custom every 2 weeks with count=3 | Source and recurrence HTTP identity, materialized Timeline after reload |
| UJ-05 | Existing one-off Activity and Event → Edit → Ripeti daily → Save → reload first and next day | Exactly one Start POST per item, first identity unchanged, next occurrence materializes |
| UJ-06 | Recurring Activity → local edit → edit selected+following → preview/confirm → delete one instance → delete series | No propagation of local title, correct series revision, deletion scopes and future survival |
| UJ-07 | Same local/following/deletion journey for recurring Event | Own Event identity, scoped revisions, next instance unchanged until series update |

The recurring matrices exercise **12 UI configurations** (six per subject).
The complex Activity includes a new Life Area, placement protection, an
untimed planned Session and an Objective with numeric target and unit.
The complex Event includes a new Life Area, placement protection, a
Scaletta item and a boolean Objective.

Seven tests are executed for Chromium, Firefox and WebKit: **21
isolated real-stack browser executions** in a complete run. E2E seed
accounts 81–101 are reserved for this matrix (Chromium 81–87,
Firefox 88–94, WebKit 95–101); the existing accounts 1–80 are unaffected.
Every title uses a new UUID suffix to avoid false comparisons.

## Evidence and limitations

Successful tests must pass a real sign-in, browser UI actions, authenticated
HTTP acceptance and fresh canonical reads or Timeline reloads. A screenshot
or DOM-only test does not prove persisted behavior. The suite does not mock
fetch, fabricate Occurrences or force successful responses.

The conversion of an already edited item into a recurring source currently
uses two separate backend transactions (Edit, then Start). A green browser
journey does not imply these form a single database transaction.

## Data-consistency checks added after first Chromium run

The first owner execution at `122c6a42` failed 7/7 journeys **before** lifecycle
acceptance, in two shared test-driver assumptions: the actual expanded Create
surface is `advanced` (not `full`) and hard-delete confirmation is a
portaled `alertdialog` with the action `Elimina definitivamente`.
These two test-driver contracts were repaired; no production feature was changed.

The seven existing paths now also check the following invariants across
successive authenticated Timeline loads and backend checkpoints:

| Transition | Consistency assertion |
| --- | --- |
| Cancel one-off hard delete | The original Activity/Event is still persisted in the canonical profile endpoint, not just temporarily shown in a stale card |
| Delete one-off, keep duplicate | Original returns HTTP 404 and is absent after day+1 checkpoint and return to day; duplicate keeps a distinct Schedule and persists unchanged |
| Daily recurring Create | Only one matching future card is materialized; future Schedule identity differs from first when available, is stable after revisiting earlier dates, and the advanced first/future Activity/Event cards retain the same named Life Area |
| Existing one-off → daily recurrence | Physical first Schedule identity survives; day+1/day+2 have distinct future Schedule identities; returning to earlier day does not duplicate or replace either |
| Local edit vs following-series edit | Changed local title does not propagate to day+1/day+2; a later series revision must not retroactively rewrite that local earlier occurrence |
| Delete one recurring instance | The deleted occurrence does not resurrect when materializing later dates and returning; following occurrences remain present until explicit whole-series deletion |

**Time semantics are tested in two distinct ways.** Browser navigation through
`dateAfter(day, 1/2/3)` triggers genuine authenticated backend Timeline reads
and recurrence checkpoints. This models **calendar progression**, but **does
not advance the server's actual wall clock**. The additional PostgreSQL test
`test_live_session_time_progression_is_persisted_and_stops_after_end` starts
a live Session at the real current time, verifies its canonical active
duration increases across elapsed time, then stops it and checks that
duration no longer grows. This test does not mock PostgreSQL time.

**New safety regression (PostgreSQL candidate):**
`test_open_live_activity_session_blocks_destructive_instance_deletion`
materializes a recurring Activity, starts a real live Session, attempts a
scoped hard delete, requires rejection, and checks that the Activity,
Occurrence, skip history and open Session survive a further checkpoint.
The test **has not been run** and may reveal an application defect.
Do not treat a hidden card as proof that an active Session was protected.

**Important not-yet-proven consistency contracts:** full first/future equivalence
for Life Area beyond the named daily Activity/Event pair, protection,
planned Sessions, quantitative Objectives, reminders and Event Scaletta;
an actual green active Session deletion rejection;
survival of other recorded facts after series edits; CAS conflicts and retry
after lost network response; DST transition with shared controllable
browser/backend clock; skip/cancel/delete on long-running routine histories.
These must be separately backed by source and test evidence; current browser
suite does not prove them merely by checking title or Schedule identity.

**Future expansion (explicitly deferred):** multiple realistic long-running
persona simulations (professions, objectives, routines and changing user
requirements) using a single isolated deterministic clock shared between
frontend, backend and database. Do not substitute browser-only `page.clock`
for server time in these scenarios.

**Verification:** all new checks above are candidate assertions pending WSL
execution on their exact branch commit. The first 7/7 failures at
`122c6a42` remain the recorded initial RED; do not label this checkpoint green.

## Important gaps to add in the next iteration

| Gap | Required proof |
| --- | --- |
| Lost reply / retry | Start accepted then transport fails, same operation replay/reopen gives one source and first occurrence |
| Simultaneous clock change + conversion | Fresh Schedule revision and matching recurrence wall time on both subjects, reload |
| Concurrent commands / stale CAS | Only one writer wins; no partial changes on rejected profile, placement or preview |
| DST | Nonexistent and ambiguous local time, earlier/later, original identity, future materialization |
| Recorded facts | Real Session/Actual/Objective facts survive selected/following edits; from-next applied correctly |
| Full combinations | Reminder, minimum Session duration, planned timed Session, overlapping and crossing-midnight intervals, Life Area reassignment |
| Calendar bounds | End date, 999 count, missing monthly dates, Feb 29, multiple selected weekdays and mixed month-day rules |
| Deletion audits | Exact deleted row counts, stale delete preview conflict, protected facts, replay and concurrent delete |
| Recurring duplication | Copy chosen occurrence template, not the source or recorded attempts; no unintended link |
| Draft / unplaced | Draft Vault, canonical unplaced Activity, duplicate into draft, re-placement and deletion with recorded Session |

These are open items, not presented as implemented in this matrix. The
existing unit and PostgreSQL suites remain authoritative for finer
invariants they already test.

## Commands

Focused real-stack Chromium, after pulling the branch:

    cd ~/projects/dante
    git pull --ff-only origin feature/timeline-temporal-operational
    pnpm --filter @dante/web exec playwright test \
      --config playwright.auth.config.ts \
      e2e/auth/temporal-user-lifecycle.spec.ts \
      --project=chromium

Run all three browsers by omitting --project=chromium, then run the full
DANTE gate:

    python3 tooling/testing/run_parallel_gate.py --group-workers 5 --postgres-workers 10 --postgres-jobs-per-worker 4

The full gate already executes WEB_BROWSER_REAL_STACK, which includes all
auth Playwright specs. No second runner, no CI dependency.

**Verification: NOT RUN** at this new SHA. Keep Playwright traces and the
exact HEAD for fixing red scenarios; older green UI-only tests are not
evidence for these user journeys.
