# Timeline Session desk — current B14 contract

**Status:** live-execution extension TECHNICAL GATE GREEN at user-local branch head `8097918d` (2026-10-10); generated client publication and real-app user acceptance pending.
**Current authority:** `docs/domain/decisions/activity-session-live-timeline-v1.md`.
**Predecessor evidence:** `docs/workstreams/timeline-session-panel-scope.md` describes the already-published _135 panel, not the current product behavior.

## Placement and availability

The existing Session control lives in the Timeline toolbar, with one compact non-modal panel anchored to the **right within the Timeline bounds**, under the toolbar; never change Home reserved columns. It opens when the first eligible row enters its preview window. Close/Escape dismisses it without repeated unsolicited reopening during a mounted session; the icon/count always reopens it. Groups are Activity identities and rows are canonical main + optional planned internal Session identities. Keyboard focus, aria labels, overflows at 1440px/390px and reduced-motion preferences remain supported.

**New fixed v1 preview lead: exactly 5 minutes**, only for placements with a precise instant. Before the preview threshold no row; after it, a timed internal row is visible but Play is disabled until its own start. Main Play may start early if accepted live policy permits. Untimed internal rows are available only during real occupied Activity interval windows; the technical envelope never fills interval gaps. Date-only/coarse periods retain day precision and do not manufacture a minute-level threshold. Accepted rescheduling instantly invalidates the desk.

Main Session execution may coexist with internal Session executions. Main starts no child automatically; child Start/Resume requires main running when that control is configured. The main Pause atomically pauses all currently running children, main Resume resumes no child, and main Stop atomically ends every still-open child (running or paused). Already ended and never-started children remain untouched. Child Pause/Resume/Stop is independent. No clock event, Stop or historical read writes an Actual, Outcome or Confirmation.

## Data and synchronization

`GET /api/v1/temporal/session-panel` remains one authenticated self-scoped batched panel read through `list_self_session_panel_inputs`, with 30-second capped reconciliation, server-derived boundary wakeup, focus/visibility/online and canonical invalidations. In addition it reads bounded, actor-owned **real** timing/pauses via `list_self_activity_session_visuals` for the displayed window, keeping a completed Session visually reconstructible after Stop and refresh. No one-HTTP-request-per-row or clock-driven writes. `visible_start_at`/`visible_end_at` support bounded 31-day actor-local view windows. The browser can animate a running geometry between server refreshes without DB polling. Open sessions remain actionable until Stop even if the planning interval expires.

Accepted Schedule is the **original planned coordinate**, never overwritten by execution. The Timeline projects one card per canonical Activity interval, remodulated visually from the real Session clock when present; no duplicate card. Main controls the outer reality envelope when present; otherwise independent internal actual intervals can inform the projection. Life Area border identity is preserved, internal colored progress means active elapsed time, neutral segments mean pause or untracked gap. Planned times remain in the card/Inspector, with deviations. Multi-interval technical envelope gaps are never filled as occupied, and overlapping Activities are laid out without moving their accepted Schedules. No historical Session timestamp changes on Schedule moves.

## Database

`20261009_135` is the prior untimed-planned start + owner panel read. `20261010_136` introduces one owner-only atomic group transition capability and adds a main-running/precise-start admission check to the planned start. `20261010_137` adds one bounded owner-only Session-real-timing read. `20261010_138` repairs cascade UUIDv7 and Stop-while-paused, preserving a closed pause interval instead of a fake Resume. Both are forward-only with no new Session or hierarchy table. Runtime obtains EXECUTE only; SQLAlchemy and Dictionary exact catalog must reconcile at **237 tables, 5 views, 222 routines, 103 triggers, 484 indexes, 420 FKs, 593 checks**.

## Verification

User ran the focused local repair gate on `8097918d` after pulling `20261010_138`: **PY_SYNTAX, RUFF, POSTGRES, WEB_TYPECHECK, WEB_LINT, VITEST, BROWSER all exit 0**. Previous full-gate PY_UNIT, GENERATE, GENERATED_CHECK and API_TYPECHECK were already green. The prior red gate is superseded as current technical status but remains historical evidence. Exact details: `docs/workstreams/timeline-session-live-local-gate-2026-10-10.md`.

This is **technical verification, not real-app visual acceptance**. The seven generated Session API files are still only in the user's WSL and must be published unchanged; do not reset/clean or regenerate. The approved five-minute preview, overlapping groups, main/child hierarchy, independent resumes, actual vs planned card behavior and responsive panel require real-app user testing. Earlier _135 tests remain historical proof.
