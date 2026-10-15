# Activity / Session lifecycle acceptance matrix

**Status:** work in progress. A focused PostgreSQL run passed on `0e848943`;
the complete PostgreSQL inventory and real-browser acceptance have not run on
that SHA. The normative product rules are in
[`activity-session-operational-lifecycle-v2.md`](../domain/decisions/activity-session-operational-lifecycle-v2.md).

An Activity interval is a plan; a named Session is a configuration; each real
Session is an independent execution attempt. The database, API, editor,
Timeline, review rail and browser must agree before a row is accepted.

| Scenario | Required evidence | Current state |
| --- | --- | --- |
| Untimed named Session creation and recurrence | API and DB read, recurrence projection, Web form | Focused PostgreSQL case passed on `0e848943`; browser pending |
| Early Start and late Stop | owner admission, unchanged Activity plan and factual timestamps | Unit/UI candidate; PostgreSQL pending |
| Main capture prerequisite and cascade | running, pause, stop, replay and concurrent transitions | PostgreSQL reconfirmation pending |
| Multiple Activity intervals | one attempt resumes across intervals; Stop then Play creates a new attempt | Panel unit candidate; PostgreSQL pending |
| Panel preview and Stop | availability follows Activity interval; ended attempt never gets Play again | Unit candidate; browser pending |
| Never-started generic and named Sessions | separate read-only rows after the current plan ends; moving into the future clears them; real attempts suppress only their own row | Focused WSL PostgreSQL 21/21 and Web rail 6/6 passed on `5e87cc26`; browser real-stack pending. Resolution actions intentionally deferred |
| Editor Keep/Delete/Cancel | choice before a mutation with attempts; stale fingerprint rejected | Candidate; PostgreSQL pending |
| Keep after a plan change | real timestamps and open/paused state retained | Focused PostgreSQL case passed on `0e848943`; browser pending |
| Delete attempts before edit | full linked graph, rollback, isolation and concurrency | Focused rollback case passed on `0e848943`; complete inventory pending |
| Named X, Save and Cancel | Save removes configuration with its attempts atomically; Cancel leaves both | Focused PostgreSQL case passed on `0e848943`; browser pending |
| Hard Activity deletion | one confirmation, complete owned graph, stale/owner checks | Focused PostgreSQL case passed on `0e848943`; browser pending |
| Direct Timeline drag, time edit, unschedule and undo | same Keep/Delete/Cancel authority and coherent interval move | Candidate coordinates exact floating/named-zone Activity revisions, including Keep/Delete/Cancel and plan Undo with fresh Session choice. Targeted Web 14/14 and full Web 1,061/1,061 passed locally on `c298769`; a later browser real-stack case checks the card mutation and persistence but has not run in WSL. Unschedule still uses generic Schedule boundary and cannot remove a governed Activity interval |
| Recurring instance versus future series | explicit scope, no rematerialization or unrelated loss | Timeline move/Undo now prompts for the scope of a recurring instance; its focused UI test passed 6/6 and full Web suite 1,062/1,062 in this later local candidate. **Missing** scoped deletion; bare hard deletion of a materialized instance fails closed. Browser and full gate pending |

## Evidence on this checkout

- The published baseline audited was `1eae6ff8`. Local changes correct the
  Psycopg percent escaping in `_146`/`_147`, refresh `_148` Dictionary/catalog
  expectations, regenerate the API client, and repair one Web type narrowing.
- Local backend non-PostgreSQL: **630 passed, 381 deselected** with proxy
  variables removed from the test process. Web Vitest: **1,057 passed in
  225 files**. Web/API TypeScript, targeted ESLint, Ruff, Mypy, test registry
  and `git diff --check` passed before the recurrence guard was added.
- New PostgreSQL scenarios cover graph deletion, owner isolation, stale
  confirmation, Keep with a running attempt, named X, and rollback after a
  stale profile. Their latest selected test bodies passed on `0e848943`.
- The first WSL run on `3c0ddeb` stopped while creating `_148`: both the
  database hash and Inspector read passed two arguments to the three-argument
  runtime metrics capability. All eight selected cases were blocked at
  migration setup (one failure and seven errors), so none supplies acceptance
  evidence. The corrected candidate passes the existing timing state ref as
  the third argument and needs a fresh PostgreSQL run.
- The rerun on `332ccbf` reached the test bodies: **5 passed, 3 failed**.
  Two newly written tests incorrectly assumed an untimed named Schedule
  appears in the create return value; they now read its persisted Activity
  role. The third surfaced a 503 for a stale profile during Delete; core edit
  now checks that revision before attempting the Session graph mutation.
  Destructive graph acceptance remains pending the next PostgreSQL run.
- The next rerun on `a4a5a15` reached all eight bodies: **5 passed, 3 failed**.
  All three destructive paths encountered `InsufficientPrivilege` when the
  owner-executed graph created its temporary working table. The corrective
  candidate grants database `TEMPORARY` only to the `NOLOGIN` owner during
  administrative provisioning, asserts the exact login-role denials and
  exercises owner temporary table creation in the PostgreSQL privilege test.
  Existing databases need explicit provisioning rerun. PostgreSQL proof of
  this corrective candidate was obtained in the next focused run.
- The user's WSL run on `0e84894396ecb6692666ce7ecf2475fb16131f04`
  passed **10/10 in 31.18 seconds**, including the owner TEMP/denied login
  privilege check, non-broadening provisioning rerun, fresh Alembic head,
  bounded lifecycle function ACL, Dictionary cross-representation, hard
  deletion, stale-profile rollback, Keep and named X, guarded direct envelope
  revision, and untimed recurring named Session. This is focused PostgreSQL
  evidence for those ten cases, not a full-gate or visual acceptance.
- The `_148` Dictionary topology expectation is
  `238|5|233|103|486|421|596`; cross-representation equality passed in the
  selected database test, while the complete catalog test inventory remains
  outside this focused run.
- A forward-only `_149` candidate guards generic Undo of an Activity interval
  after a coordinated removal, in both the API and the directly executable
  PostgreSQL routine. Its focused regression checks refusal with a running
  Session and preserved removal; PostgreSQL has not run on `_149`. The expected
  catalog topology is unchanged. Direct Timeline mutation UX is still open.
- The user's focused `_149` run on `cd3b589` passed five cases and failed the
  exact cross-representation test only because its hard-coded head still read
  `_148`; the migration itself, Alembic drift and Undo suite passed. All six
  catalog head literals now advance to `_149` together. Current-plan Session
  review visibility is a candidate and has no PostgreSQL or browser proof yet.
- The user's WSL run on `5e87cc26` passed test integrity, Ruff, six
  non-PostgreSQL tests, **21/21 PostgreSQL tests** (including all six current
  catalog modules and Activity review), Web typecheck, **6/6 rail tests** and
  deterministic generated-source check. The API client schema was then
  published on `f7eb26c`; that newer SHA has not run the complete gate.
- A subsequent local Timeline candidate routes drag, keyboard and time edits
  for exact Activity intervals through the coordinated replan. It previews
  no local optimistic movement, asks Keep/Delete/Cancel for real attempts,
  uses the session fingerprint at the backend CAS boundary and makes a plan
  Undo from the returned current revision. The targeted Timeline set and
  all **1,061 Web Vitest** passed locally; no PostgreSQL or real-browser proof
  exists for this newer candidate. Generic Event mutations remain separate.
- A later unverified browser real-stack case in the existing Schedule forms
  suite exercises Activity card keyboard move through `PUT /activities/{ref}/replan`
  and reads the persisted five-minute shift after reload. The recurring
  instance scope prompt has a focused Web test (6/6 locally) and the full Web
  Vitest suite passed 1,062/1,062 in 225 files; TypeScript,
  targeted ESLint and Prettier pass. These additions have **not** run against
  PostgreSQL or the real browser. The real-stack test cannot be discovered
  locally because this scratch dependency tree lacks Playwright; WSL must run it.
- This environment has no Docker, PostgreSQL 18/PostGIS or real-app browser
  stack. The previous full-gate result on an older SHA is not evidence for
  these changes.

Do not accept the full destructive vertical until the complete database and
concurrency inventory plus real-browser journey pass on the same final SHA.
Then execute the complete
parallel gate from `docs/development/testing-standard.md` and inspect every
failed group; a test that describes a superseded rule must be corrected to
the normative contract rather than treated as product truth.
