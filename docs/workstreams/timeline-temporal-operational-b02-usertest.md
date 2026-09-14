# Timeline / Temporal-Operational — B02 isolated userTest

- **Status:** READY FOR USER EXECUTION
- **Workstream branch:** feature/timeline-temporal-operational
- **Purpose:** manual B02 Schedule Core acceptance only
- **Data class:** disposable synthetic test data; never personal/production data
- **Targeted direct PostgreSQL proof:** 2 passed on candidate f712b77bb78751fea4eb53656d77b523c1627625
- **CI:** deliberately deferred; this protocol does not claim CI evidence
- **Scope:** B02-A/B/C/D only; B02-E is not authorized

## 1. Acceptance boundary

This protocol proves real product behavior. It does not treat browser state, mocks or a prototype card as canonical success.

~~~
production web build
→ HTTPS Vite preview
→ real FastAPI
→ real dante_runtime role
→ fresh migrated PostgreSQL 18.6
→ synthetic account only
~~~

The disposable database/container exists only for this run. Do not point any step at a normal LOCAL DANTE database, staging, production or personal account.

The B02 boundaries under test remain:

~~~
Activity != Schedule
scheduled != happened
no current placement != no Schedule history
Undo != history rewind
~~~

## 2. Preconditions

From the repository root:

~~~bash
git status -sb
git branch --show-current
~~~

The branch must be feature/timeline-temporal-operational. The worktree must be clean before starting.

Build the canonical image if it is not already available:

~~~bash
docker compose -f infra/compose/local.yaml build postgres
~~~

## 3. Start the isolated stack

Use one control id for the entire manual run:

~~~bash
export DANTE_E2E_CONTROL_ID=temporal-b02-usertest
uv run --project apps/backend python tooling/run-access-auth-stack.py
~~~

Wait for the full-stack-ready message, then open:

~~~
https://127.0.0.1:4173
~~~

The local certificate is intentionally self-signed.

Synthetic credentials:

~~~
email:    synthetic.user@example.com
password: correct horse battery staple
~~~

Sign in and open /home. For each asynchronous mutation, wait until the Timeline/Planning Tray finishes its authoritative reload before judging the result.

## 4. Proof A — create one Activity and place the same identity

Use a unique title, for example B02 manual place <current-time>.

1. Open the Timeline + surface.
2. Keep Attività selected and create the Activity on the unplaced path.
3. Open Attività da collocare / Planning Tray and verify that title appears exactly once.
4. Select Colloca for that Activity.
5. Use one same-day interval, for example start 10:00 and duration 45 minutes.
6. Press Colloca in Timeline once.
7. Wait for the canonical refresh.

Expected result:

- the Planning Tray no longer contains that Activity;
- Timeline contains exactly one card with that title at the chosen interval;
- no second Activity/card with the same title is manufactured.
- reload the browser: the same title remains exactly once in Timeline and remains absent from Planning Tray.

## 5. Proof B — governed time revision

Use the Activity from proof A.

1. Open its time control, labelled Modifica orario di <titolo>.
2. Move the start forward by a visible amount, for example from 10:00 to 10:15.
3. Press Conferma once.
4. Wait for the message that Timeline is rereading current state.
5. Verify the rendered interval has changed while retaining the intended duration.
6. Reload the browser and verify the revised interval remains.

Expected semantic result:

~~~
same Schedule identity
+ new accepted current placement state
+ historical previous placement retained
!= browser-only move
~~~

## 6. Proof C — unschedule survives reload and returns the same Activity

Create and place a second uniquely titled Activity, for example B02 manual unschedule <current-time>, using the same path as proof A.

1. Open its Timeline card.
2. In the details surface select Riporta nel Planning Tray.
3. Wait for Attività riportata nel Planning Tray. La Timeline si sta aggiornando.
4. Verify the card is absent from Timeline.
5. Open Planning Tray and verify exactly one card with the same title is present.
6. Reload the browser.
7. Verify the same title is still absent from Timeline and still present exactly once in Planning Tray.

Expected semantic result:

~~~
current placement removed
+ Schedule/history retained
+ same Activity identity becomes unplaced
!= Activity deletion
~~~

## 7. Proof D — guarded Undo restores a new current state

Create and place a third uniquely titled Activity, for example B02 manual undo <current-time>.

1. Unschedule it using Riporta nel Planning Tray.
2. Wait until it disappears from Timeline and appears in Planning Tray.
3. Without reloading or performing another placement change, press Annulla in the Undo toast.
4. Wait for the authoritative refresh.
5. Verify the card returns exactly once to Timeline and disappears from Planning Tray.
6. Reload and verify it remains exactly once in Timeline.

Expected semantic result:

~~~
Undo creates a new accepted current placement
from the exact unschedule receipt
!= reopening/deleting historical truth
~~~

## 8. Proof E — stale mutation cannot overwrite newer truth

Use the currently scheduled Activity from proof D.

1. Open /home in a second browser tab and wait until the same Timeline card is loaded there.
2. In the first tab, unschedule that Activity and wait until it appears in Planning Tray.
3. In the second tab, use its already-loaded stale card and choose Riporta nel Planning Tray.
4. Expect the truthful conflict message:

   ~~~
   La pianificazione è cambiata altrove. Non è stata rimossa.
   ~~~

5. Verify no fake second removal, duplicate card or local success is shown; after the authoritative refresh, the Activity is still exactly one unplaced Planning Tray item.
6. In the first tab, use Annulla for the original unschedule and verify the Activity returns once to Timeline.

This is the user-visible stale-current-state proof. Do not try to invent database writes or edit identifiers in DevTools.

## 9. Proof F — real database failure never becomes fake unschedule success

Keep the isolated stack running. In a second terminal, using the same control id:

~~~bash
export DANTE_E2E_CONTROL_ID=temporal-b02-usertest
uv run --project apps/backend python tooling/access-auth-e2e-control.py database-stop
~~~

Back in the first browser tab, use a currently scheduled B02 Activity:

1. choose Riporta nel Planning Tray;
2. wait for the product error state.

Expected while PostgreSQL is stopped:

- the Activity is **not** reported as returned to Planning Tray;
- the Timeline card is not fabricated away;
- no unplaced Planning Tray card is manufactured locally;
- the UI exposes a truthful failure, for example Impossibile riportare questa pianificazione in sicurezza.

Restart the same disposable database:

~~~bash
uv run --project apps/backend python tooling/access-auth-e2e-control.py database-start
~~~

Reload /home and verify the Activity remains scheduled exactly once. The failed operation must not have become durable success.

## 10. Cleanup

1. Ensure the disposable database is running if proof F stopped it.
2. Return to the terminal running run-access-auth-stack.py.
3. Press Ctrl+C once and wait for cleanup.

If the harness was killed before cleanup, remove only the container with this exact control label:

~~~bash
docker ps -aq \
  --filter "label=dante.e2e.control_id=${DANTE_E2E_CONTROL_ID}" \
  | xargs -r docker rm -f
~~~

Never use an unscoped Docker prune/remove command.

## 11. Approval record

Fill this only after the manual run:

~~~
Proof A — create/place same Activity identity + reload          PASS / FAIL
Proof B — governed revision + reload                           PASS / FAIL
Proof C — unschedule → Planning Tray + reload                  PASS / FAIL
Proof D — guarded Undo creates restored current state           PASS / FAIL
Proof E — stale mutation is rejected without overwrite         PASS / FAIL
Proof F — real database failure never fakes success             PASS / FAIL

B02 userTest — APPROVED / NOT APPROVED
Observed findings:
- ...
~~~

B02 ledger reconciliation remains forbidden until this record has been reviewed and explicitly approved. B02-E remains a separate exact PRE-SCOPE after that reconciliation.
