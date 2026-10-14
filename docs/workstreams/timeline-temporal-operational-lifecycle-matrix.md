# Activity / Session lifecycle acceptance matrix

**Status:** work in progress. No PostgreSQL or real-browser acceptance on the
current content SHA. The normative product rules are in
[`activity-session-operational-lifecycle-v2.md`](../domain/decisions/activity-session-operational-lifecycle-v2.md).

An Activity interval is a plan; a named Session is a configuration; each real
Session is an independent execution attempt. The database, API, editor,
Timeline, review rail and browser must agree before a row is accepted.

| Scenario | Required evidence | Current state |
| --- | --- | --- |
| Untimed named Session creation and recurrence | API and DB read, recurrence projection, Web form | Candidate; PostgreSQL pending |
| Early Start and late Stop | owner admission, unchanged Activity plan and factual timestamps | Unit/UI candidate; PostgreSQL pending |
| Main capture prerequisite and cascade | running, pause, stop, replay and concurrent transitions | PostgreSQL reconfirmation pending |
| Multiple Activity intervals | one attempt resumes across intervals; Stop then Play creates a new attempt | Panel unit candidate; PostgreSQL pending |
| Panel preview and Stop | availability follows Activity interval; ended attempt never gets Play again | Unit candidate; browser pending |
| Never-started generic and named Sessions | separate actionable review items, record/replan/delete, durable after an Activity move | **Missing** persistence, API and UI |
| Editor Keep/Delete/Cancel | choice before a mutation with attempts; stale fingerprint rejected | Candidate; PostgreSQL pending |
| Keep after a plan change | real timestamps and open/paused state retained | PostgreSQL regression written; not run |
| Delete attempts before edit | full linked graph, rollback, isolation and concurrency | `_147`/`_148` and regressions are candidates; PostgreSQL pending |
| Named X, Save and Cancel | Save removes configuration with its attempts atomically; Cancel leaves both | UI/API/DB candidate; PostgreSQL pending |
| Hard Activity deletion | one confirmation, complete owned graph, stale/owner checks | UI/API/DB candidate; PostgreSQL pending |
| Direct Timeline drag, time edit, unschedule and undo | same Keep/Delete/Cancel authority and coherent interval move | **Missing** coordinated UI; unconfirmed direct changes with attempts are rejected |
| Recurring instance versus future series | explicit scope, no rematerialization or unrelated loss | **Missing** scoped deletion; bare hard deletion of a materialized instance now fails closed |

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
  stale profile. Their test bodies have **not** executed against PostgreSQL.
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
  this corrective candidate is **NOT_RUN**.
- Intended `_148` Dictionary topology: `238|5|233|103|486|421|596`.
  This is a computed expectation, **not** a measured live catalog.
- This environment has no Docker, PostgreSQL 18/PostGIS or real-app browser
  stack. The previous full-gate result on an older SHA is not evidence for
  these changes.

Do not accept the destructive paths until a fresh database migration,
Dictionary/cross-representation checks, rollback/ACL/concurrency tests and
real-browser journey pass on the same final SHA. Then execute the complete
parallel gate from `docs/development/testing-standard.md` and inspect every
failed group; a test that describes a superseded rule must be corrected to
the normative contract rather than treated as product truth.
