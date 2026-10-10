# Timeline Session panel

Status: branch implementation candidate; focused technical gate passed, real-app acceptance pending.

## Product contract

The Timeline toolbar exposes a Session icon and count when at least one Session control is available. The non-modal panel opens on the right inside the Timeline, groups rows by Activity and places Play/Pause and Stop beside each name. Closing the panel preserves that preference while the Timeline is mounted; the icon reopens it. Escape closes it and restores focus. No clock event steals focus, starts execution, or asserts an Actual/Outcome.

- Untimed planned rows become available during an accepted Activity interval; the technical envelope does not fill gaps between intervals.
- Timed planned rows become available at their own start, up to their exclusive planned end. Named-zone placements use resolved instants; floating times use the authenticated effective zone. Date-only/coarse placements retain their day precision; no exact hourly time is invented for a coarse period.
- When there are no planned rows, a live-enabled Activity offers its generic Session control during its interval. Planned rows do not create an extra generic control; an already-open generic Session remains accessible.
- Open Sessions remain visible regardless of expired planning windows, viewed Timeline date or a subsequently disabled capture policy. All simultaneous open attempts are retained.
- New execution respects the Activity's existing live-capture policy. Pausing, resuming and ending use the existing Session CAS/idempotency commands. Stop never completes the Activity.
- Retired planned rows are excluded. A missing placement is not a retired row and does not prohibit explicit execution.

## Read and update boundary

`GET /api/v1/temporal/session-panel` is authenticated, self-scoped and read-only, with `Cache-Control: no-store`. One database statement invokes `list_self_session_panel_inputs`, a DEFINER capability composing owned current placements, profile/policy capabilities and `list_self_open_activity_sessions`. The latter is an owner-checked, set-based open-execution reader: the panel does not fetch each Activity's full execution history, nor issue one HTTP request per row. The new capabilities grant EXECUTE to the runtime and introduce no new direct table grant; pre-existing table ACLs are reconciled by the catalog test. No timeline checkpoint/materialization is triggered by this read.

The response carries server evaluation time and the next known placement boundary. The Web schedules one refresh at that boundary, capped by a 30-second reconciliation interval, and refreshes after canonical Session/Timeline changes, focus, reconnect and visibility restoration. Background-tab polling stops. Reads are coalesced; unmount aborts them; stale pre-command responses cannot overwrite accepted command results. Database reads have an 8-second statement timeout; requests have a 12-second timeout. Failed refresh retains visible rows with commands disabled and explicit Retry. Failed commands retain errors and a retry operation ID; no optimistic timing state is invented.

`20261009_135` updates only the planned-start capability's admission boundary (allow untimed active rows, reject retired Activity/role, lock against retirement) and adds two read capabilities with owner/ACL isolation. It does not rewrite earlier migrations or add a Session table. Candidate topology is `237|5|220|103|484|420|593|0|0|0`.

## Verification

Run `bash tooling/verify-b14-session-panel-local.sh` after the approved branch update. The gate covers rules, owner isolation, timed/untimed runtime, pause/resume/stop, retirement, current catalog, deterministic API generation, types, new-code lint, existing neighboring Create/Edit/Inspector regressions and two browser scenarios (1440px and 390px).

Browser scenarios mount the real Timeline with controlled API responses. They are not a live-backend end-to-end proof. After the technical gate, migrate the persistent local app database to the approved head and verify with real Activities: untimed/timed rows, overlapping Activities, interval gaps, closing/reopening, refresh while paused, expiry while running, a second tab changing state, and a network failure followed by retry.

Workspace evidence: 10 Python rule tests and 93 tests across 9 Web suites passed; API/Web TypeScript checks, new-code ESLint, selected Ruff and Vite test-mode build passed. OpenAPI and Orval were generated from backend source. In the user-local gate, generated-source verification passed (516 files), browser scenarios passed (2/2), and PostgreSQL initially reported 17 passed with one failure in an incorrect ACL assertion. After removing that assertion, the user pulled `93011bb1` and reran `test_b14_session_panel.py`: both PostgreSQL integration tests passed (2/2). Thus every scenario in the original focused PostgreSQL selection has passing evidence across the two runs; the full selection was not repeated after the test-only correction. The existing `timeline-surface.tsx` has an unrelated `_previousColor` ESLint error and `organization` dependency warning; these pre-existing lines were preserved. The browser fixture uses controlled API responses, so real-app visual acceptance and performance remain unproved.
