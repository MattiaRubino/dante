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
performs the self-scoped CAS update. The owner's later clarification allows deleting an Activity with an
open Session after explicit confirmation. The obsolete rejection test has
been replaced with an accepted-deletion/atomic-cascade regression.

**Quality gate:** Ruff reported unsorted `asyncio` import, a `PT017`
exception assertion and a format issue in the new tests. These source-level
findings were corrected; the subsequent user clarification superseded the
incorrect destructive-guard assertion with an accepted-deletion contract.
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

**Active-Session deletion contract (clarified by user):**
`test_confirmed_recurring_instance_deletion_removes_open_session_atomically`
materializes two recurring Activity instances and starts a real live Session
on one. A read-only preview leaves the Activity and running Session intact.
After the user-confirmed destructive operation, the Activity and its open
Session graph **must both be deleted**, the technical skip must prevent
regeneration, and the other instance must remain untouched. Active execution
is **not a deletion veto**. The new positive-acceptance regression is not yet
run on PostgreSQL.

**Important not-yet-proven consistency contracts:** full first/future equivalence
for Life Area beyond the named daily Activity/Event pair, protection,
planned Sessions, quantitative Objectives, reminders and Event Scaletta;
a green active-Session **confirmed deletion** cascade and untouched siblings;
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


---

## 2026-11-09 — Approved stateful user-journey v2 contract (OPEN IMPLEMENTATION)

**Status:** user-approved design, **NOT YET IMPLEMENTED/EXECUTED** as an 80-source E2E suite. The seven prior browser journeys and their later incremental extensions do **not** satisfy this expanded contract. A green current gate cannot be interpreted as v2 coverage. Keep this section as the admission/coverage source of truth; additional fields and edge scenarios may be appended without removing earlier assertions.

### A. Test population and controlled scope

- **Phase 1:** create **20 independent one-off Events and 20 independent one-off Activities**, then perform many sequential mutations on **each**, finishing with faithful duplication, deletion and Draft Vault flows where applicable.
- **Phase 2:** independently create **20 native recurring Events and 20 native recurring Activities**, reusing the diversified phase-1 combinations and adding frequency, range and occurrence-specific changes. Do not replace the creation matrix with a single-feature-per-object series.
- **Phase 3:** take one-off Events/Activities (or equivalent rich new one-offs), activate a recurrence through **Edit**, then reuse phase-2 local/following/exception/duplication/deletion logic. Minimum ten converted sources per kind; expand to the full twenty when the reusable journey engine is proven.
- For each kind, scenarios **01–10 are varied multi-feature** and **11–20 are high-density**, with *several* settings per item. The numbers below indicate starting configuration, not the number of operations or final counts.
- Presently **exclude** incomplete **location**, **reminders** and **participants** from mandatory v2 acceptance. When those verticals are complete, append explicit validated scenarios; never introduce hidden skips to make a feature appear covered.
- Subject terminology: **Event** has agenda parts, not Activity intervals/Activity Sessions; **Activity** has intervals, planned Sessions (timed/untimed), live/recorded sessions and goals. Avoid impossible cross-subject fixture fields.
- Life Area color belongs to the shared Life Area and changing an existing area's color is **global**, including previously linked items. Changing an assignment for selected-and-following occurrences is a different operation from globally recoloring an area.

### B. Deterministic creation inventory

Legend: \`L\` = Life Area (none / existing / new); \`G\` = number of Objectives; \`A\` = number of Event agenda parts; \`I\` = number of Activity intervals; \`S\` = number of planned Sessions (timed + untimed); \`D\` = description; \`P\` = placement protection; \`T\` = timed / all-day. Goals mix boolean/quantity/range and verification settings where supported. Every nonempty set receives stable, unique labels, distinct values and a recorded creation order. The actual composer must author all represented fields via UI; test fixtures **must not bypass the UI with database inserts**.

| Event ID | T | A | G | L | D | P | Additional contrast |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| E01 | timed | 2 | 1 | existing | yes | no | distinct color |
| E02 | timed | 3 | 2 | new | no | yes | quantitative goal |
| E03 | all-day | 4 | 2 | existing | yes | no | range goal |
| E04 | timed | 1 | 3 | none | yes | yes | three goal kinds |
| E05 | timed | 5 | 1 | new | yes | no | alternate area color |
| E06 | all-day | 2 | 3 | new | yes | yes | varied goal verification |
| E07 | timed | 3 | 2 | existing | no | yes | different time zone |
| E08 | timed | 4 | 3 | none | yes | no | cross-day schedule |
| E09 | all-day | 5 | 2 | existing | yes | yes | multi-day range |
| E10 | timed | 2 | 4 | new | yes | yes | mixed target values |
| E11 | timed | 6 | 4 | existing | yes | yes | high-density baseline |
| E12 | all-day | 7 | 5 | new | yes | yes | high-density date span |
| E13 | timed | 8 | 4 | new | yes | yes | reorder agenda |
| E14 | timed | 5 | 5 | existing | yes | yes | change several goals |
| E15 | timed | 9 | 3 | new | yes | yes | delete middle agenda |
| E16 | all-day | 6 | 4 | existing | yes | yes | remove/reassign area |
| E17 | timed | 7 | 5 | existing | yes | yes | conflicting edit |
| E18 | timed | 8 | 5 | new | yes | yes | repeated save/reopen |
| E19 | all-day | 9 | 5 | new | yes | yes | rejection and retry |
| E20 | timed | 10 | 5 | existing | yes | yes | maximal editable mix |

| Activity ID | T | I | S timed + untimed | G | L | D | P |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| A01 | timed | 2 | 1 + 1 | 2 | existing | yes | no |
| A02 | timed | 3 | 2 + 0 | 2 | new | no | yes |
| A03 | timed | 2 | 1 + 2 | 3 | existing | yes | yes |
| A04 | timed | 0 | 2 + 1 | 2 | none | yes | no |
| A05 | timed | 4 | 1 + 0 | 3 | new | yes | yes |
| A06 | all-day | 0 | 0 + 2 | 3 | existing | yes | yes |
| A07 | timed | 3 | 3 + 1 | 2 | none | yes | yes |
| A08 | timed | 2 | 0 + 3 | 4 | new | yes | no |
| A09 | timed | 4 | 2 + 2 | 3 | existing | no | yes |
| A10 | timed | 3 | 3 + 2 | 4 | new | yes | yes |
| A11 | timed | 5 | 4 + 2 | 4 | existing | yes | yes |
| A12 | timed | 5 | 3 + 3 | 5 | new | yes | yes |
| A13 | timed | 6 | 4 + 3 | 5 | existing | yes | yes |
| A14 | timed | 4 | 5 + 2 | 5 | new | yes | yes |
| A15 | timed | 6 | 5 + 3 | 4 | existing | yes | yes |
| A16 | all-day | 0 | 0 + 4 | 5 | new | yes | yes |
| A17 | timed | 5 | 4 + 4 | 5 | existing | yes | yes |
| A18 | timed | 6 | 6 + 2 | 5 | new | yes | yes |
| A19 | timed | 7 | 5 + 4 | 5 | existing | yes | yes |
| A20 | timed | 7 | 6 + 4 | 5 | new | yes | yes |

**Fixture validity gate:** Before encoding the numbers as executable tests, verify the actual Create authoring constraints for interval length, session placement/overlap, all-day untimed sessions, goal types and maximum counts. A table entry is a **required scenario to implement or explicitly resolve**, not proof that its proposed configuration is accepted by today's domain. If an entry conflicts with documented invariants, replace it with an equally complex *valid* configuration and record the reason here; never skip it silently.

### C. Mandatory multi-step mutation journey for EACH source

1. Persist creation via real user UI. Read canonical complete snapshot (one-off) or source + selected/neighboring occurrence snapshots (recurring). Compare **exact ordered arrays, values, identities and types** against the independently declared scenario state, not against the POST echo.
2. **ADD:** several new objectives / Event agenda parts / Activity intervals / Activity planned Sessions where applicable, with changing quantities, time values and Life Area assignment. Save; read again.
3. **UPDATE:** change multiple existing values (title, description, amount, objective type/verification, agenda wording, interval bounds, session name/timing, Life Area selection/color, event/activity times, timezone when valid). Save; verify *changed and unchanged* properties.
4. **REMOVE:** delete first/middle/last entries, then add replacements, then change another surviving entry. Verify exact count, order, persistent IDs of surviving entities and the **absence** of every removed element after complete reload.
5. **REORDER:** where supported, move goals/agenda/intervals/Sessions, and check exact saved and rerendered order; no phantom rows or stale duplicate references.
6. **CANCEL:** modify multiple controls then X/Annulla; exercise the discard decision, cancel and confirm paths. No changed authoritative values or hidden unintended writes.
7. **EXECUTE/RECORD:** start/pause/resume/stop Activity Sessions, include registered sessions, inspect blocked replan/drag while active and post-stop edit policy. Confirm Objective outcomes and validate persisted evidence; **a confirmed objective must not reappear as an unrestricted editable target**.
8. **DUPLICATE:** reopen the *final edited* source. Composer is prefilled with exact duplicate-eligible values, not initial values. Persist new source with distinct native/Schedule/objective/session identities. Never duplicate live execution, observations or historical confirmations.
9. **DRAFT / DELETE:** move to Draft Vault where supported; verify non-executable state. Cancel and confirm deletion, prove canonical 404/deletion and that surviving duplicates remain unchanged.
10. Repeat complete assertions after reloading Home, reopening the Inspector/Edit, and returning to the same date after navigating away. **Every mutation updates an independent expected-state model and is checked immediately**, not only at journey end.

The operations above are a **coverage contract**, not a directive to force unavailable edit commands. If policy forbids a mutation (recorded session, protected exception), the required test proves the explicit refusal and zero persisted changes; after permitted resolution, it retries the originally requested mutation and checks success. Some journeys reorder operations (REMOVE→ADD→UPDATE, UPDATE→CANCEL→UPDATE, etc.) so the engine cannot pass by always exercising the same happy path.

### D. Native series (40) and conversion series (at least 20)

- Reuse **all 20 per-subject creation configurations** with a recurrence matrix spanning daily, weekly (multiple weekdays and steps), monthly by day and ordinal weekday, yearly, bounded count, end date and custom intervals. Assert the canonical requested cadence/range and materialization over a bounded but representative series window, including first, middle and later dates.
- For **each** series, exercise local instance changes and a selected-and-following revision. The exact selected occurrence **is included**, earlier clean occurrences remain unchanged, and protected local exceptions stay intact. When the selected instance is already an exception, prove the correct **from-next** boundary rather than silently rewriting it.
- Distribute independent local changes across **first / middle / last** materialized occurrences; combine local exceptions before and after whole/following revisions. Confirm the preview enumerates protected exceptions and stable references. Preserve recorded facts, confirmations and Session policy across lawful changes.
- Test repeated scoped revisions, addition/modification/removal of structural fields, duplicate from clean and locally modified instances, delete one instance, delete multiple at different times, delete whole source. Check that a later checkpoint **does not resurrect hard-deleted or explicitly skipped instances**.
- Convert at least **ten one-off Events + ten one-off Activities** through Edit into distinct recurrence modes; rerun the same scoped/local/deletion/duplication proofs. Original physical identity must survive; no duplicate source/first placement.
- For an existing Life Area, a color change propagates **globally** (including past linked items). For a new area scoped to the future, previous unmodified/exception instances must not inherit that *new assignment*. Distinguish these operations in expected state.

### E. Cross-cutting consistency / fault contracts

| ID | Required independent evidence |
| --- | --- |
| INV-01 | Every command is fully atomic; failure after intermediate DB write rolls back all changed fields, linked rows and newly created Life Areas |
| INV-02 | Exact list equality for named nested elements, counts, order and stable identities of untouched items; no duplicates or deleted ghosts |
| INV-03 | Compare UI + canonical API + relevant PostgreSQL persisted facts, using a separate expected-state model driven by explicit actions |
| INV-04 | No unintended retroactive series propagation; selected boundary inclusive; from-next exclusive; protected exceptions not overwritten |
| INV-05 | Execution and outcome history cannot be copied by Duplicate or silently deleted/changed by an unrelated Edit |
| INV-06 | Different browser sessions editing stale revisions produce a conflict, not last-writer-wins loss; replay of same operation ID is idempotent |
| INV-07 | Clock boundaries include midnight, month/year rollovers, February and DST ambiguous/nonexistent local hours with supported zone semantics |
| INV-08 | An error response or network interruption cannot hide partial writes or permit duplicate resources on retry |
| INV-09 | Move/drag and changes during live/paused/recorded sessions follow the actual documented Edit guard and confirmation contract |
| INV-10 | No disabled, skipped, weakened or conditional-only assertions to turn known product bugs green; preserve original suites in addition to v2 |

### F. Execution strategy and evidence

The matrix must be **materialized into actual executable, named test cases**; checking that a fixture list contains 40 rows does not establish behavior. Split into isolated per-scenario journeys, not one monolithic fail-fast test. Each step logs scenario ID, operation number, seed, prior accepted state and exact expected/actual field diff. Separate browser test data/users and PostgreSQL lifecycle; no shared mutable database across parallel browser workers. Prefer deterministic pairwise coverage plus bounded reproducible adversarial sequences (recorded seed), never an unrepeatable random walk.

Run local small tests and targeted PostgreSQL first, then targeted real-stack flows, then the entire 27-group gate on the **same commit**; record exact PASS/FAIL/SKIP, total inventory and elapsed time. Four previously known WebKit skips are **open inherited coverage gaps**: do not mistake them for the four formerly failing tests or claim 0 SKIP until genuinely exercised.

**Acceptance rule:** each entry in the matrix must have a linked executable scenario, concrete UI/API/DB assertions and a green run on the exact candidate commit. Missing or unrun cells stay OPEN. Future feature additions may extend the matrix without weakening or deleting existing assertions.
