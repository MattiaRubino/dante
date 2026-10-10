# Activity execution / Session desk / dynamic Timeline — accepted product contract

- **Status:** APPROVED PRODUCT BEHAVIOR; implementation candidate pending user-local gate and real-app acceptance
- **Date:** 2026-10-10
- **Branch:** `feature/timeline-temporal-operational`
- **Current presentation authority for this scope:** this decision plus `docs/frontend/home/timeline-session-panel.md`
- **Structural authority:** `docs/domain/concepts/session.md`, `docs/domain/concepts/schedule.md`, `activity-intervals-and-sessions-v2.md`
- **Historical, superseded presentation:** `activity-planned-session-reschedule-product-v1.md` §4.1 and any single-envelope/old session-desk presentation rule; preserve that document as historical evidence, not competing current UX.

## 1. Canonical separation and identities

Activity is intended work; Activity-owned `interval` Schedule is planned occupancy; `planned` Schedule is an intended future Session slice; Session (B08) is actual execution; Actual/Outcome/Confirmation are independent. A planned Session is NOT a real Session. No clock passage creates Session, Actual, skipped, failed, completed, Outcome or Confirmation. The UI may recompute geometry from real timing but must not mutate accepted Schedule timestamps.

A single Activity may have several nonoverlapping planned intervals and several planned Session slices, with or without exact placement. The user may execute the Activity generically using a **main** real Session and also execute linked **internal** real Sessions. These are peer canonical B08 Session identities associated by Activity owner and optionally an explicit planned Schedule link: **no Session→Session owner relationship**.

## 2. Session desk (Timeline right-side floating panel)

A non-modal overlay anchored to the right edge *within the Timeline's visible bounds*, immediately below the top Timeline toolbar, not a new permanent column. It may overlap timeline content but never overflow viewport/TL boundaries, move the Home rail, or change reserved widths. It groups simultaneous Activities, and contains independent rows with Play/Pause/Resume and Stop for the main Session and each planned internal Session. Stop is disabled before execution. Accessible close/Escape/focus return; close preference persists for the mounted desk and does not auto-reopen each polling tick. Toolbar icon with count allows reopening. The desk is not tied to which past/future day the user is currently viewing.

**Availability:** publish an exact-clock row at `scheduled_start - 5 minutes` (fixed for this version; future user configurability deferred); before the threshold it is absent. Preview is not permission to play early. Timed internal Session Play is admitted at its own planned start, until that interval expires (unless an execution is already open). Untimed planned rows become eligible with a real accepted Activity interval, with no fabricated start instant. The main Session may be started *early* manually when the Activity's capture policy permits; preview should not force a premature start or bypass capture policy. A generic main control can coexist with named internal rows; do not invent an extra planned slice to represent the main. With no real open/eligible rows, hide the panel trigger instead of leaving an empty obstruction. Live rows remain visible while running or paused, including after planned deadlines and timeline movements.

Multiple Activities are separated by titled groups, and rows are keyed by canonical `activity_ref` + optional `planned_schedule_ref` + actual `session_ref`, never by array index alone.

## 3. One dynamic card, no duplicate Activity card

The Timeline retains one card per canonical scheduled Activity interval, consistent with `activity-intervals-and-sessions-v2.md`; do not introduce parallel planned + actual Activity cards. Before execution the card uses accepted planned coordinates. When execution exists, **visual projection only** follows the real Session start/end or live server-relative now, including early starts, late starts, pauses and overruns. It must not mutate/unschedule/resize the accepted plan, nor move adjacent Activity Schedules.

An Activity with main Session uses that main Session's real envelope as the principal visual timing, while internal Sessions contribute status/detail, not an independent competing outer border. An Activity without main Session may use the bounds of associated real internal Sessions while preserving planned intervals/gaps. When several distinct planned intervals exist, project each separately; **never fill technical envelope gaps**, merge unrelated intervals, or add elapsed time twice for simultaneous sessions. Day-boundary spillover uses truthful clipping at displayed-day bounds; no horizontal overflow or rendering outside Timeline surface.

Maintain Life Area identity/color on the card border, not as the sole signal of running/paused. A subtle internal active fill/neutral pause segment and explicit text/status (accessible without color), with separate overflow indication, represent actual elapsed execution. Paused elapsed time counts in real bounds, but not in active duration. After Stop, actual final bounds and pause segments remain available through canonical history on refresh, with planned start/end and deviations in Inspector. Stop does NOT assert Activity completion or Objective results. When reality is absent the card remains planned, not an inferred failure.

## 4. Main Session and internal Sessions — directional control

- Starting the **main** creates only the main real Session. No internal Session auto-starts.
- A configured main must be **running** before starting or resuming an internal Session; when main is paused, internal start/resume is rejected. A legacy Activity without a configured main is not silently assigned a fictional main runtime.
- A planned internal Session with an explicit start cannot be started before its own start from the automatic desk. Early-start of the main remains legal when capture policy allows it.
- **Pause main:** atomically pauses the main plus every currently running internal real Session owned by that Activity. Already paused remain paused; never-started and ended sessions stay untouched.
- **Resume main:** resumes **only the main**. Every internal paused by a cascade or earlier user choice remains paused until individually resumed.
- **Stop main:** atomically ends the main plus **every still-open** internal real Session (both paused and running); never creates fake executions for never-started rows. Stopping a paused real Session closes its pause at exactly Stop (no synthetic Resume or tiny fake active interval), and leaves earlier immutable MaterialStates untouched.
- **Internal Pause/Resume/Stop:** changes only the targeted internal Session, never its main or siblings. A failed/stale operation fails visibly, without falsely showing partial success.
- These transitions require actor ownership, accepted Activity relation, idempotent operation replay, current MaterialState/CAS and one database transaction under concurrency, not multiple unrelated browser mutations. If the backend cannot guarantee atomicity, do NOT expose a fake cascade.
- Do not infer an Activity Completed/Actual/Outcome from main or internal Stop. The recorded-history veto and lock on moving an Activity with an open Session still apply.

## 5. Movement / expired planned work / review

Moving an unexecuted Activity in/out of the current window recomputes the desk's eligible rows from **accepted** new placements. Moving it into a completely elapsed past interval with no Play leaves execution unknown, without any auto-created Session/Actual. When configured B10 reality-review policy requires follow-up, group review by Activity in **Da verificare**; do not spawn one task for every unused planned Session. Moving current Schedule never relocates historical Session timestamps. A confirmed completed/occurred Activity remains historically protected. Open execution blocks ordinary Activity drag/resize. Explicit Episode reality correction is separate from plan reflow.

## 6. Time and clock correctness

Timezone/DST: use canonically resolved instants with effective actor timezone, not client local wall clock guesses. Server `evaluated_at` and `next_change_at` drive wakeup scheduling; debounce/coalesce subsequent invalidations. Never poll the DB every animation frame, never make one HTTP request per visible card or Session. Reconcile focus/online/visibility and committed transitions; fail closed on stale/denied actions and keep evidence immutable. Pauses/resumes never create separate child Sessions.

## 7. Acceptance / exit gate

Backend owner/CAS/replay/transaction rollback and policy tests; early/late start, timed + untimed slices, simultaneous Activities, pause-main cascading, resume-main noncascade, stop-main cascading, internal isolation, stale races, early internal rejection, open Session after planned end; frontend card geometry single identity, schedule unchanged, live/paused/ended fill, multi-interval gaps, clipping, overlapping cards, no UI overflow at 1440px + 390px, toolbar reopen semantics, keyboard, refresh and network failure, real backend + real browser manual walkthrough. Preserve previous M5 and Draft Vault regressions. User runs one consolidated local gate; no CI. Record exact failures and repair before marking code passed. The five-minute offset is a non-configurable product constant in v1.

## 8. Approved addendum — independent internal Session + result workspace (2026-10-10)

The user explicitly approved the combined implementation. **Main Session is optional.** The Activity's main `Sessione` toggle controls the generic Activity live clock, not the existence or executability of explicit Activity-owned `planned` Session slices. An explicit planned Session is an individually executable scoped work unit even when the generic main clock is disabled. When main is enabled, child Start/Resume requires a running main and main Pause/Stop cascades atomically downwards; the inverse never happens. When main is disabled, internal Sessions are independently controllable within their own admitted time windows. No fabricated main is created.

**Home Context Rail:** one compact right-side surface, with three tabs: **Conclusi** = bounded owner-only history of factually ended real Sessions, actually completed Events and explicitly completed Activities (never infer Activity completion from Session Stop); **Da verificare** = canonical B10 policy-derived review/reconciliation queue and *optional governed* unanswered questions; **Obiettivi** = current Objectives requiring a confirmed recorded result, including unfinished staged input. Same Objective identity and write contract in Inspector and Home, no duplicate Result.

**Objective input:** typing/selecting persists an **unconfirmed draft** associated with actor and Objective; the draft survives reload and does not create Observation, Evaluation, Actual, Outcome or Confirmation. A distinct explicit **Conferma** action persists the canonical ObjectiveResult atomically and consumes the draft with owner/CAS/idempotent protection. A completed Result remains historical; any correction uses the existing dedicated Objective correction contract, not overwriting history. The UI must distinguish `bozza`, `registrato/confermato`, `valutazione obiettivo`, and `Attività completata`. This controls both Inspector and Home rail identically.

A Session timed slice that expires without Play is never automatically failed/completed. It may yield one grouped Activity review only if explicit reality/review policy qualifies it. Side navigation is non-modal, accessible and does not widen existing Home rail. Bounded paging for finished history and objective work is mandatory; never query an unlimited actor history per refresh. Desktop, mobile and timezone/DST remain subject to the established execution contract.

**Implementation/proof status:** approved user product requirement; workstream acceptance remains OPEN until revised PostgreSQL/Dictionary, generated OpenAPI, UI test and real-app manual checks pass. Do not declare complete just because this paragraph has been saved.
