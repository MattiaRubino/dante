## 2026-11-09 — Statefulness: first, middle, finite last and interval identity (NOT RUN)

**Context:** two user-provided WSL runs at `7c2886e0` and `46a8f3d4` returned four component Vitest failures each (the later run: 134 PASS, 4 FAIL), 5 TypeScript compiler errors, and 4 unregistered test files. These results are historical: none of the new code is marked green without a fresh run on its exact SHA.

**Test-only repairs:** updated the historical `Aggiungi obiettivo` button selectors after the owner-approved compact **`+ Obiettivo`** label in Activity/Event/Advanced Create; switched an obsolete accepted-Objective retirement/undo test to a genuinely **unrecorded** Objective (registered definitions remain locked); matched the current accessible Life Area *button* and checked its RGB swatch instead of querying a removed decorative img; corrected strict optional-prop, request-init, Activity settings and Event-only TS narrowing issues. Four omitted files were registered in the canonical test-case registry, not skipped/deleted.

**Added test path and failure boundaries:** P2's **bounded five-occurrence** personas (five per Event/Activity family) now explicitly read and locally edit the *actual last* occurrence, assert no sixth generated occurrence, then verify the modified last remains protected after edits of the first, an intermediate and the following slice. P3 already edits the original physical first after conversion, then a generated middle and future slice; expanded canonical duplicate scans across the first five displayed days. Assertions use a scoped Timeline API read, exact expected title and exact physical Schedule-ref cardinality; they inspect both flat Activity/Event placements and *nested* `placement` of recurring Event Occurrences. For Activity, **one activity_ref with N distinct interval schedule_ref/card values is correct**; duplicates are extra Schedule identities beyond those N or repeated identities. A smoke failure on first/middle/last must not be fixed by reducing the expected count.

**Evidence requirements:** run `python3 tooling/testing/verify_test_integrity.py`; targeted Vitest/TypeScript/format/lint; then discover browser inventory with `playwright test --list`, run 1 P1 + 1 P2 (finite) + 1 P3 + RT per browser, then all 102 v2 tests × Chromium, Firefox and WebKit on disposable real-stack accounts. Keep test.step traces and server response readbacks. Functional product bugs require owner review, not silently changed DANTE behavior.

---

## 2026-11-09 — Visual QA: unchanged Save and independent recorded-result deletion (UNVERIFIED)

The user reproduced two real UX faults in Activity Edit: **unchanged Save** transmitted a structurally empty atomic request and displayed an English backend 422 string; **Elimina registrazione** was blocked by a separately staged Objective addition and its canonical refresh would have erased that unsaved draft. Fix is narrow: no-op Activity Edit closes without network mutation; the atomic API client rejects empty edits locally and maps HTTP 422 to user-facing Italian text; recorded Objective deletion performs the confirmed backend action independently and merges only the affected Objective's canonical row. All other unsaved fields, new Objectives and staged removals survive; Event Edit follows the same independent-delete behavior.

**Regression coverage added (not yet executed):** jsdom Activity no-op with all four accepted Objective kinds, Event no-op with mixed accepted kinds; Activity/Event deletion-confirm flow while one newly added Objective has an empty name, preserving that draft; atomic client sends zero requests for empty edit and never exposes raw 422 text. Existing PostgreSQL and WSL tests from `035b28bc` remain historical **36 unit + 7 PostgreSQL PASS**, not a new green verdict for these changes. This candidate needs the focused web gate and real-app visual recheck before proceeding to parallel E2E.

**Error presentation rule:** technical backend validation details, raw stack traces, SQL diagnostics, and framework messages must not be shown as end-user text. Domain validation belongs next to the relevant field where that field can be identified; concurrency conflicts should offer a clear recovery action, and unexpected failures a short local-language message. Keep structured diagnostics in developer observability, without leaking sensitive input values. The Activity atomic 422 mapping is a local first repair, not proof that all DANTE error surfaces have been audited.

---

## 2026-11-09 — Recorded Objective Edit and converted-first identity candidate (NOT RUN)

**Normative decision:** [confirmed-objective-edit-and-recurring-protection-v1.md](../domain/decisions/confirmed-objective-edit-and-recurring-protection-v1.md). Owner-approved: recorded Objective rows are immutable/read-only in ordinary and local Edit until explicit, confirmed, permanent deletion of the result (not the Objective). Pending state and ordinary Create remain editable. Corrections remain a separate action. Running, paused and finished Sessions, recorded Objective facts and locally edited occurrences protect future-series scope.

**Implementation candidate (GitHub only, no new local gate):** forward-only migrations `20261109_182` and `20261109_183`; authenticated Objective deletion API and Objective-definition write guard; common recorded Objective row/dialog wired through Activity and Event Edit; explicit selected-instance protection in pure scope selection plus PostgreSQL admission; removal of old editable recorded row and duplicate result footer.

**Regressions added/updated:** PostgreSQL self-owner, other-owner, stale CAS, recorded definition lock, corrected result (two observations), irreversible removal and clean re-edit; UI component cancellation, confirmation and unlock in Activity and Event; v2 RT-01 Event real UI→API→reload; pure recurrence selected/future protected reasons and PostgreSQL direct inclusive refusal; P3 real UI local edit of the **physical first converted instance**, physical first Schedule identity preservation and canonical duplicate scans on initial/middle/future dates. Multiple interval Schedule/card rows for a single Activity remain expected, not duplicates. Existing unrelated scenarios are not skipped or weakened.

**Pre-acceptance requirements:** Run Ruff/format/pytest targeted PostgreSQL, Vitest/TypeScript/ESLint, OpenAPI/client generation and Dictionary/schema drift, followed by browser P1/P2/P3/RT and 27-group full gate on the same SHA. The candidate is **NOT GREEN**, and product defects found during real tests still require owner discussion; do not edit unrelated product behavior to satisfy the suite. Some legacy tests may still expect an editable recorded Objective and require a semantic review, never a silent weakening.

---

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


## 2026-11-09 — Stateful v2 executable candidate checkpoint (RED allowed, NOT RUN)

**Evidence caution:** The approved matrix above is the requirement, not a green test report. This checkpoint added executable Playwright cases to the existing suite but has **not run typecheck, Prettier, Vitest or real-stack Playwright at this SHA**. A run that has failures is a RED baseline to repair, never evidence of a green product. Do not disable, skip, mark \`test.fail\`, or narrow assertions just because an existing bug is expected.

### Files and current implementation

| Source | Concrete coverage |
| --- | --- |
| \`apps/web/e2e/auth/temporal-stateful-case-matrix.ts\` | Typed 20 Event + 20 Activity initial configurations with multi-feature variation and recurrence families |
| \`apps/web/e2e/auth/temporal-stateful-case-matrix.test.ts\` | Unit guard that population, goal kinds, recurrence families and synthetic user-account partitions cannot silently shrink |
| \`apps/web/e2e/auth/temporal-stateful-journey-support.ts\` | Real UI Create through advanced composer; independent expected-state builders; authenticated Life Area fixture creation; canonical Objectives, Event agenda and Activity plan readback |
| \`apps/web/e2e/auth/temporal-stateful-personas.spec.ts\` | 100 distinct tests per browser: P1 40 rich one-offs, P2 40 rich native series, P3 20 conversions. They chain CREATE, reload, nested edits/add/delete, Life Area, local/following/from-next scoped edits, exception boundaries, duplication and deletion. A subset also covers Draft Vault (Event copy versus Activity move) |
| \`apps/web/e2e/auth/temporal-stateful-runtime.spec.ts\` | Two further tests per browser for confirmed Objective evidence in Edit and a real live Session with Pause/Resume/End and Edit guard |
| \`tooling/run-access-auth-stack.py\` | Increases E2E seeded accounts 101→407: 1–101 untouched, 102–401 reserved for 100 personas × 3 browsers, 402–407 two runtime guards × 3. Never share a mutable account across parallel cases |

The E2E inventory adds **102 tests to each browser project** (306 browser slots). Previously existing test cases are retained. Total discovered slot counts and skip behavior must be verified using \`playwright test --list\` at the exact candidate SHA; the registry count is not a substitute for actual discovery.

### Known RED / diagnosis linking

- **\`V2-RT-01\`**: the user observed a confirmed Objective still presented as a mutable target in Event Edit; the test confirms an actual objective via the Work panel, then requires the original observation to remain and the ordinary Edit name input to be disabled. If the product is still broken, the latter assertion must be RED, with captured screenshot/trace. The same contract must later be generalized to Activity and recurrence outcomes.
- **\`V2-P2-E*\` and \`V2-P2-A*\`**: a native series's following editor must allow writing a new Life Area with color and changing the appearance of a preexisting shared area. UI → acceptance → catalog and future instances are checked. A known broken picker is a real test failure, not an exception.
- **\`V2-P1-*\`**: nested goals/agenda/planned Sessions are added, updated, removed and replaced across real Edit transactions; exact ordered readback, surviving identities, eliminated ghosts and faithful duplication are required. Some rows may be RED due domain gaps or inaccurate test drivers; classify with step-specific browser evidence.
- **\`V2-P2-*\`**: tests must prove selected-and-following includes the selection; locally protected instance must stay unchanged; \`from_next\` excludes its selected boundary. They recheck the canonical source snapshot, neighboring cards and original exception.
- **\`V2-RT-02\`**: timed near-current Activity with live capture must honor Session state/recorded facts, plan guard and Pause/Resume/End history. Do not simulate time progression with a mocked browser clock while the backend uses real time.

The Playwright \`test.step\` path combines **phase + persona ID + operation index**, e.g. \`V2-P1-A13 / 4 Edit, remove and add nested data\`. A RED fix requires the exact SHA, scenario ID, step name, browser, expectation mismatch, canonical HTTP result and trace, and a corresponding focused regression proof. \`testInfo.attach('scenario')\` provides the initial scenario JSON. Do not derive independent expected truth from observed API state: it is derived from the declared actions and updated on each accepted transition.

### Still OPEN and not to be misrepresented as complete

- Full cross-product of **twenty normal-source conversions per kind** (current P3 10 per kind) and different conversion frequencies (candidate P3 uses daily).
- Fully varied **multiple independently verified edits to every one of the 40 entities**. P1 currently has a dense initial create and one substantial mixed edit plus Life Area, cancel, duplication and deletion; the user-approved requirement explicitly calls for more repeated sequences, removals and reorderings per item.
- Recursive variation of **interval resizing and removal**, timed planned Sessions and their clock setting, verification mode mutation, multi-objective recorded history on both subject kinds, physical drag/move protection, full Draft Vault edit/re-authoring and result correction.
- **True concurrent browser writers with stale revision**, mid-write rollback injections (except previously authored specific PostgreSQL integration), lost network reply and replay, full DST/fold/gap/window matrix, protected recorded future instances, late materialization across months/years and all-day edge cases.
- Conversion+local+following target mapping and structural validation on both Event and Activity need real browser execution; the test code is not the proof.

### Local qualification order

First confirm checkout and a clean worktree; then format/lint/typecheck and the small inventory test. Next run one case from every phase plus the two runtime guards with one browser on isolated real-stack, keeping all failures and traces. Repair **test driver only if it mismatches the documented production UI contract**, and repair product code when real UI→API→DB fails; both require a new regression. Repeat focused tests, then the full v2 suite in Chromium/Firefox/WebKit with isolated stacks, then the complete gate on one SHA. No merging until the user has the all-green full gate and visual walkthrough, and no claiming GREEN for unexecuted test steps.

**Do not enable v2-only skips** to keep the older gate green. Every test in \`*.spec.ts\` is included in the normal real-stack Playwright inventory. The extra cost is intentional; schedule/batch with bounded parallelism while isolating backend and PostgreSQL stacks. Keep all reports, durations and original assertions.


## 2026-11-09 — v2 first real-stack smoke baseline (RED; 2289fdbc)

Source: user-supplied \`V2_SMOKE_20261109_180205.tar.gz\` (Playwright JUnit, logs and traces, Chromium/Firefox/WebKit). Exact tested SHA: \`2289fdbc1608193e1d8e7566bcee16746b111101\`. The 27 selected browser tests were discovered and recorded without skips; **6 passed, 18 assertion failures, 3 Playwright errors** (per browser: 2 pass, 6 fail, 1 error). Prettier/TypeScript/ESLint and the five persona inventory Vitest tests passed. The 6 passes are \`V2-P2-E01\` and the preexisting standalone conversion journey, each in all three browser projects.

Do **not** treat 21 red results as 21 different product bugs. Trace-backed classification:

- \`P1-A01\`/\`P3-A01\`: canonical planned Session name is \`display_name\`, not \`name\`. Actual persisted names match the independently declared fixtures. Test-driver issue.
- \`P2-A01\`: precisely two interval Schedules belonging to one Activity on the same date, at 09:10–09:50 and 10:20–11:20. The original test erroneously assumed one physical card per Activity; cardinality must derive from the declared interval count, and their unique Schedule IDs must be verified. Test-driver issue; *not* proof of duplicate creation.
- \`P3-E01\`: conversion preserves the first physical Event while future occurrences use the dedicated recurring Event source, as reported by \`GET /recurring/events/{original}/seed\`. The test incorrectly filtered future canonical occurrences by the original nonrecurring Event ref. Preserve the separate first-Schedule identity assertion.
- \`P1-E01\`: the driver navigated away approximately 75 ms after pressing Save, with no successful Event edit mutation visible in the trace. Await UI's successful save acknowledgement **before** reloading; until rerun, do not attribute this to a product bug.
- \`RT-02\`: malformed checkbox CSS selector prevented exercising any live Session behavior. Test-driver issue.
- Firefox \`RT-01\`: the same Life Area label appeared twice because typing before asynchronous catalog resolution could stage a second new Life Area; explicitly click the existing catalog option in the composer. This is a fixture-driver race; it is **not** evidence of product duplicate-card behavior.
- Chromium/WebKit \`RT-01\`: confirmed Boolean observation persisted, and Inspector showed the registered result and the \`Correggi risultato\` control, **but** the original goal's \`Nome obiettivo\` field remained enabled in Edit. **Open functional/UI decision:** must the entire goal definition be locked after confirmation, or only immutable recorded results shown with explicit correction? Do not change DANTE or weaken the assertion without user agreement.

Technical-only changes following baseline: \`7deb43ee\`, \`bbb444b7\`, \`01bca639\`, \`4ffa40f4\`, \`daa2ea89\`, \`911450df\`, \`616aced1\`. These modify only the two new Playwright helper/spec files; they have **not yet been run through CI or the local real-stack test gate**. Never mark them green based on code inspection alone.

**Distinct undisclosed-to-suite regression:** manual report says that editing the first instance after converting a one-off to a recurrence can create a duplicate card. The initial v2 P3 journey exercises modifications on later instances, not an independent edit of the original first instance. The current run cannot prove that the suite detects the manually described trigger. Preserve the original P3 test as a separate baseline and extend generic first/middle/last identity and materialization checks after the blind baseline is completed; never silently claim it already caught this.
