# Activity / Session lifecycle acceptance matrix

**Status:** work in progress, not eligible for UI acceptance or branch closure.
**Branch baseline:** `feature/timeline-temporal-operational` at `6ca79a6e`.
**Product contract:** `../domain/decisions/activity-session-operational-lifecycle-v2.md`.

The named Session has a configuration identity and zero or more real attempts.
An Activity interval remains the plan. PostgreSQL constraints, API checks, UI
controls, and browser behavior must agree before marking a row accepted.

| Scenario | Required evidence | State |
| --- | --- | --- |
| Create named Session without its own time | authoring request, recurrence, DB read, Web form | Candidate; PostgreSQL pending |
| Edit/duplicate older timed configuration | no child time in UI/payload; no ghost Timeline placement | UI candidate; database transition pending |
| Early Start, late Stop | owner capability and actual timestamps unchanged by plan | Unit/UI candidate; PostgreSQL pending |
| Main running prerequisite; Pause/Stop cascade | concurrent named/main runtime transitions and replay | Existing tests require PostgreSQL reconfirmation |
| Multiple Activity intervals | one attempt can pause/resume across intervals, next interval can start a new attempt | Panel unit candidate; PostgreSQL pending |
| Stop during preview | never reoffer same attempt; do not suppress unrelated future interval | Panel unit candidate; browser pending |
| Named/generic never started | expire from panel, enter review independently with record/replan/delete actions | Missing |
| Edit or drag with active, paused or completed attempts | Keep/Delete/Cancel before mutation, concurrent stale ref, all entry points | Missing |
| Keep real attempts and change plan | real timestamps and current runtime state survive, no implicit Activity completion | Missing |
| Delete all real attempts before edit | linked pause/timing/operation/Actual/Outcome dependencies removed atomically | Missing; requires reviewed database lifecycle design |
| X on named configuration then Save/Cancel | Save removes configuration and all linked attempts; Cancel changes nothing | UI draft candidate; database cascade missing |
| Delete Activity | one confirmation and hard cascade through intervals, reminders, sessions, objectives and linked facts | Missing; current `retire_self_activity` deliberately rejects recorded truth |
| Move unstarted Activity out of current panel | old opportunities enter review without reappearing at new slot | Missing persistent review basis |
| Recurrence/occurrence boundary | selected instance versus future series, no cross-owner/cross-occurrence loss | Missing |

## Current local evidence

- Backend non-PostgreSQL: 628 passed, 372 PostgreSQL deselected, with proxy
  variables unset for the local test transport.
- Web Vitest: 1053 passed before adding two draft-cancellation tests; rerun
  the complete suite on the final content SHA.
- PostgreSQL 18/PostGIS and browser real stack: unavailable in this workspace.
  No migration acceptance or final gate is claimed here.

The current database retains immutable Session timing states and operation
ledgers. Its `retire_self_planned_schedule` rejects linked execution and its
`retire_self_activity` rejects both open and recorded facts. Hard deletion is a
cross-family migration and security-definer capability, not a client-side
filter or a silent rollback of recorded truth.


## Post-candidate focused test additions (pending PostgreSQL execution)

On 2026-10-14, new branch-local changes after the candidate SHA `ae8621ed`
added two PostgreSQL scenarios to the existing
`apps/backend/tests/integration/temporal/test_session_panel.py`:
- two simultaneous Activities with independent named rows: starting and stopping
  one must not remove the still-ready other Activity from the Session panel;
- named Session directly started two hours before its Activity interval,
  without generic capture: original accepted Activity plan remains unchanged,
  and the opened execution becomes independently actionable.

The backend error classifier in `session_runtime.py` now distinguishes a
configured generic Session that is not running from the obsolete pre-_146
internal-clock constraint. The existing Session authority unit test file has
a focused two-case regression for the actual PostgreSQL constraint names.

**Evidence:** the GitHub commits contain code/tests, not execution evidence.
PostgreSQL 18.6, Alembic `_146` and all changed files remain **NOT_RUN** in
this assistant environment (no checked-out WSL or PostgreSQL/Docker). The
user-side initial targeted gate is `temp/LIFECYCLE_POSTGRES_BASELINE.log`;
its results must be reviewed before new destructive migrations are written.

The remaining matrix rows (authoritative Keep/Delete/Cancel admission,
transactional history cascade and dependent facts, expiration to actionable
review queue, X + Save, Activity hard-delete, concurrency and recurrence
boundaries) remain **MISSING**, not accepted. Do not give the frontend the
appearance of working Delete until its database capability is correct.


## Editor attempt-state read follow-up (candidate)

Activity Edit now reads existing canonical Activity Session attempts through the
same authenticated `/api/v1/temporal/activities/{activity_ref}/sessions` data
source used elsewhere, refreshes on `dante:session-changed`, and displays the
current state of linked generic and named attempts as **in corso / in pausa /
conclusa**. This is a read-only UI improvement: it does not claim the new
Keep/Delete/Cancel mutation workflow has been implemented. The owning existing
Inspector/Edit Vitest file includes a focused fake-transport test of all three
labels and named provenance.

The renderer additionally distinguishes the two database rejection constraints
for missing main capture versus historical early-start admission; the current
`_146` migration removes the latter admission. This does not change the
database lifecycle or the authority rules.

**Source code published but NOT RUN:** local WSL Vitest, TypeScript, Ruff,
Mypy, focused PostgreSQL and browser acceptance are still required for all
post-`ae8621ed` commits. If the new data-source read cannot be verified, do
not enable destructive editing. The normative lifecycle matrix rows about
atomic deletion, review persistence, UI confirmation and recurrence are OPEN.
