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
