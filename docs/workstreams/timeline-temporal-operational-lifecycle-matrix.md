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
