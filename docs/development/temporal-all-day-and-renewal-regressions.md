# All-day, runtime and renewal verification — 2026-11-23

## What was reused

Do not replace existing E2E suites. `temporal-stateful-personas.spec.ts`
already runs 40 independent, richly configured Activity/Event cases in Phase 1,
including all-day with Objectives, planned Sessions, Life Areas, Agenda and
recurrence variations. The existing Phase 1 canonical readback now also
asserts that an all-day case renders exactly one date-lane bar, preserves
the date-lane identity, and has no detached continuation glyphs.

Existing fast Vitest suites cover: date-lane geometry, in-flow expansion,
scroll limit, Week ruler/inverse mapping, Inspector click/keyboard positioning,
Session actual-vs-planned cutoff, Event save lifecycle, recurrence editor and
renewal notice 30→29. Existing Python/PostgreSQL tests cover explicit
730→1460 renewal, exhaustion, decline and no-decision expiry.

## New browser acceptance

`apps/web/e2e/auth/temporal-all-day-regressions.spec.ts` adds **7 tests**,
each using its own isolated real-stack account per browser
(411–417 Chromium; 418–424 Firefox; 425–431 WebKit):

1. AD-01 Activity all-day multi-day Create → Save title edit → Inspector closes
   → reload → canonical API profile and both date-lane days agree.
2. AD-01 Event same lifecycle with Event's independent editor.
3. AD-02 12 all-day items, two visible, in-flow expansion,
   6-row height cap / 10 overflow children / internal scrolling,
   collapse restores original frame height.
4. AD-03 Main Activity Session Play → Stop during a multi-day all-day plan,
   canonical finished Session retained, future all-day dates absent.
   Do not confuse this with subordinate named Sessions.
5. AD-04 Objective + planned named Session survive real PostgreSQL
   persistence and Timeline reload on an all-day Activity.
6. AD-05 Activity/Event daily `Dopo` = 3: UI caps pasted 9999 to 730,
   3 accepted instances and no fourth on reload.
7. AD-06 Renewal UI **deliberate HTTP stub only**: two notices (+2), 30→29
   → 0, 409 conflict displayed without claiming success.
   This test does **not** verify real server persistence; real expiry and
   renewal are separately checked in PostgreSQL integration tests.

The additional regression accounts are seeded only by the disposable
Access/Auth real-stack harness in `tooling/run-access-auth-stack.py`.
Do not point tests at a personal or production database.
No direct SQL fixtures for the E2E Activity/Event under test.

## New backend boundary coverage

`apps/backend/tests/test_occurrence_evaluator.py` adds three independent
date checks for `Dopo 730`: daily, weekly, monthly. The evaluator must
include exactly the 730th authorized occurrence and never generate the 731st.

## Chromium diagnostic and correction — 2026-11-23

On branch `4d4ebe562`, the owner ran the seven-case Chromium real-stack
selection: AD-02, AD-04 and AD-06 passed; both AD-01 variants, AD-03 and
AD-05 failed. TypeScript typecheck passed. The targeted three-case Python
selection failed before its assertions because its requested checkpoint
windows exceeded the evaluator's 62-day limit.

Trace and source review found test setup/locator faults: AD-01 matched the
original title as a prefix of the updated title; AD-03 looked for the main
Session checkbox before opening Advanced Create; AD-05 reused the same
Create date helper after navigating forward, but that helper could only
move the picker to later months. The backend test now evaluates a 32-day
window starting on the independently calculated 730th date; it checks that
the 730th is present and the following daily/weekly/monthly candidate is
absent. No product implementation was changed.

The new real-stack test and seven previously unregistered component test
files were added to the test-case registry, and the reviewed dual-zone
boundary test entry was qualified. Filename and registry integrity checks
pass on this corrected worktree. The corrected Python, Web typecheck and
Chromium tests are **NOT_RUN** here; the owner's WSL rerun must verify them
on one published candidate SHA before acceptance. A later real-stack failure
after these setup points must be diagnosed against API readback and traces.

## Owner-run order

1. Fast TypeScript, Vitest and Python tests.
2. Only **Chromium** for the new E2E spec on the existing dedicated
   Access/Auth stack; inspect failures and Playwright traces.
3. Existing stateful all-day persona cases and the broader E2E suite.
4. Firefox/WebKit then the complete parallel gate.
5. Manual visual review of the renewal icon/panel and final all-day layout.

Never mark tests passed based on static inspection. Fix any new or existing
assertions only when the real behavior has been verified against the
canonical backend contract. Do not weaken failures to satisfy the gate.
