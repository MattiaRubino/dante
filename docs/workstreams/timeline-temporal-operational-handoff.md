# Timeline / Temporal-Operational — Workstream Handoff

## 2026-10-17 — Owner screenshot correction: live now-line drag and Edit font parity

**Owner-reported reality after previous 3/3 focus tests:** dragging a card
across the **current-time** line still leaps discontinuously from
`00:00` to `21:15` with only a small physical move; Advanced Create
and especially Activity Edit texts still look too small. Owner explicitly
clarified that **midnight is NOT the bug trigger**; do not replace the
15-minute snapping or day-boundary semantics to address this.

**Root issue in earlier attempted drag freeze:** the child day stream only
froze its own rendered days. The parent `TimelineSurface` still reprojected
the live Session/clock mapper, scroll anchoring, ruler and recyclable day
window, allowing different pixel-to-minute coordinate systems while
dragging near now. The mapper itself remains nonlinear and the real
current-time line stays informational.

**Source candidate (not owner-tested):**
- Added an optional `onDragActiveChange` event from
  `TimelineDayStream` on begin/end to the parent, and moved the ruler
  to `displayedDays`, sharing the same frozen projection as cards.
- `TimelineSurface` now captures one frozen `renderedDays` and
  `timelineNowMinute` on actual drag activation, displays the frozen
  projection until release/cancel, suspends parent viewport re-anchoring,
  keeps `renderedDaysRef` pinned, and skips live day-window recycling
  during drag. Native auto-scroll still works; after drop the newest
  live projection resumes. Snapping (15m), canonical replan, timezone,
  actual Session timing and Undo are unchanged.
- Typography fixes now explicitly cover Edit: appended scoped rules in
  `activity-edit-panel.css` raise its legacy 10–12px body/buttons/
  schedule/reality/objective copy to 13–14px; footer/modal geometry
  remains unchanged. Advanced Create gains scoped 13–14px text rules
  with greater CSS specificity in `temporal-create-u1-polish.css`.
  Quick Create remains compact with existing buttons.
- Extended `timeline-drag-geometry.test.tsx` to assert the frozen
  **ruler** follows the same snapshot as card and now-line, and parent
  drag notification balances begin/end.
- Added browser CSS computed-style check in
  `e2e/temporal-create-unified-ui.spec.ts` for Activity Edit primary,
  secondary, verification, repeat and Objective-add typography.
  Existing tests also cover Advanced and compact Quick fonts.

**Verification:** code PUBLISHED / new source tests **NOT RUN** by
assistant. Request a single focused WSL Web typecheck, the drag-geometry
Vitest test, and Playwright selected drag+Create+Edit UI tests. Manual
authenticated actual drag across updating now-line and rendered text
sizing are still required; no basis yet to claim the reported jump
is completely fixed. No backend changes, full DB gate, or migrations.

## 2026-10-17 — Owner verification: drag geometry and Create readability tests green

Owner pulled branch `feature/timeline-temporal-operational` to
`f641e655cb0966a5147f835807ada4be59fed214` and ran focused checks:

- Web typecheck at `f641e655`: **FAIL** on a test-only TypeScript
  signature (`timeline-drag-geometry.test.tsx:98`, overly general
  `EventTarget` passed to `fireEvent`). Not a production/runtime failure.
- Focused `timeline-drag-geometry.test.tsx` Vitest:
  **1/1 PASS**, 104 ms.
- Focused `temporal-create-unified-ui.spec.ts` plus
  `timeline-hardening.spec.ts` Playwright: **2/2 PASS**,
  `PLAYWRIGHT=0`. Vite fixture built successfully.
  The isolated fixture's optional API proxies emitted nonfatal
  `ECONNREFUSED 127.0.0.1:8000` since the backend was not started.
- Corrected the test-only type declaration to
  `Document | HTMLElement` in code commit
  `fb33977735451d1561037873c2d579186dd767ff`.
- Owner fast-forwarded to exact `fb339777` and reran
  `pnpm --filter @dante/web typecheck`:
  **PASS**, `TYPECHECK=0`.

**Focused automated verification now green.** Only an isolated test
type signature was changed between the successful Vitest/Playwright
run and the successful typecheck; no production source or CSS was
changed in that correction. Authenticated manual visual check remains
pending for drag crossing a live, updating now-line and final Quick /
Advanced font fit. No need to rerun backend or full test gate. This
handoff update changes documentation only.

## 2026-10-17 — Create control microtype and current-time drag jitter candidate

Owner confirmed the previous changes in the real UI and requested two
precise follow-ups: (1) raise Quick/Advanced Create button and label text
a *little more*, particularly `Opzioni avanzate`, `Salva bozza`,
`Aggiungi`, `Attività`, `Evento` and the large Advanced option buttons,
without changing any panel/container geometry; (2) remove a jump/hesitation
when dragging a card near the moving current-time line.

**Source changes:**

- `timeline-day-stream.tsx`: when the pointer crosses drag activation,
  snapshot the already-rendered elastic `TimelineRenderedDay[]` and
  `nowMinute` for the duration of that one gesture. Render frozen
  day mappings/positions and use the same pinned mappings in
  `resolveDragPreview`, used by both preview and final drop. This
  prevents 15-second live Session reality projections / clock ticks
  from rebuilding the nonlinear minute↔pixel mapper under the pointer
  near the now-line. On release, Escape, pointer cancel or drag cleanup,
  restore live incoming days immediately. Existing 15-minute snap,
  auto-scroll, ruler pin, Undo and canonical replan paths unchanged.
  The now-line already has `pointer-events:none`; no new visible
  ghost overlay or interaction was introduced.
- `temporal-create-u1-polish.css`: modest fonts only:
  type labels 14px, Quick toggles 13.5px, Advanced reality buttons
  14px, Create footer actions 13px, secondary text about 12.5px.
  Crucially, `Salva bozza` previously inherited a high-specificity
  10px rule; the 13px footer rule now outranks it. Long labels stay
  inside the *unchanged* button boxes using ellipsis when necessary.
  No width/height/grid/padding/modal/footer/frame changes.
- `e2e/temporal-create-unified-ui.spec.ts`: browser computed font
  checks for Quick, Advanced and each footer action, plus unchanged
  Quick button-bounds containment. Existing compact vs full-size
  clock geometry assertions remain.
- `timeline-drag-geometry.test.tsx`: JSDOM regression simulates a
  real Session-time elastic geometry reproject after pointer-drag
  activation. Verifies day height and now marker remain from the
  original mapper during drag, and the updated mapper becomes visible
  immediately after pointerup. Pointer identity is supplied explicitly
  for deterministic native + React pointer listeners across JSDOM
  versions. Existing Playwright card preview/drop equality test
  continues to cover the full pointer pipeline.

**Verification status:** SOURCE CANDIDATE PUBLISHED, **focused tests
NOT YET EXECUTED** on the final commit by the assistant. Owner needs
only TypeScript, the new Vitest freeze regression and two selected
Playwright tests (Create readability and existing title drag preview).
No backend changes, migration or full 27-group gate. Authenticated
real-data visual confirmation around an actively updating Session
is still pending; do not call the jitter fully solved until that
scenario is checked on a real running Session.

## 2026-10-17 — Owner verification: post-Stop child review, cursor and typography

Owner provided WSL test output against **exact code HEAD**
`7810b80f873588a5d368df89ed00442c8fe88979`.

- Ruff on modified backend + tests: **PASS** (`RUFF=0`).
- Backend session-panel projection unit tests: **25/25 PASS**
  (`BACKEND_UNIT=0`).
- PostgreSQL real integration
  `test_past_unstarted_review_pauses_on_main_play_and_returns_for_children_on_stop`:
  **1/1 PASS** (`POSTGRES=0`).
- Web TypeScript `tsc --noEmit`: **PASS** (`TYPECHECK=0`).
- Web `activity-planned-sessions-card-detail.test.tsx`:
  **4/4 PASS**. Main active, paused and stopped Inspector behavior covered.
- Browser selected cases from `timeline-hardening.spec.ts` and
  `temporal-create-unified-ui.spec.ts`: **2/2 PASS**
  (`PLAYWRIGHT=0`), including normal title cursor and computed Quick /
  Advanced text size checks. The Vite fixture build succeeded.
- Browser fixture emitted `ECONNREFUSED 127.0.0.1:8000` on proxy
  requests to an unstarted local API. These were nonfatal to the
  selected UI tests.

**Total: 32 targeted tests passed; zero failures.** Previous 56-test
candidate is separate evidence and must not be combined with these
counts. The new behavior is source/test-verified but still requires
**authenticated, real-app visual acceptance** of unchanged modal geometry,
readable labels (including English), and actual past-Activity main Stop
followed by named Session review/Inspector states. No further test
rerun required solely for this documentation commit.

## 2026-10-17 — Owner screenshot feedback: cursor, Create typography, post-Stop child review

Owner inspected real UI after prior green 56-test candidate and reported three
misses. This patch intentionally **supersedes** the previous assumption that
main Play permanently dismisses every child "mai avviata" item:

1. Card title: production reference CSS removed the `cursor:pointer`
   match for `.timeline-event-card__title`. Without a drag, the
   mouse uses the normal arrow; once drag starts, the existing
   `.is-drag-source` grabbing cursor remains active. No click/drag
   dispatch logic was modified.
2. Create typography: real screenshots exposed 7.5–11px type on large
   Quick/Advanced controls despite the earlier limited CSS pass.
   U1 polish now gives main type choices 13px, toggle/choice labels
   12.5px, Advanced reality buttons 13px, descriptions 12px and
   footer actions 12px, plus appropriately sized timezone/form labels.
   **Widths, heights, padding, grid tracks, fixed footers, responsive
   layout and time logic are unchanged**. Text remains ellipsized where
   required. New browser assertions check actual computed font sizes.
3. Operational policy:
   - Past no-main-Play / no child history => main + unstarted named
     Session review entries.
   - Main started/open/paused => no unstarted review while in progress.
   - Main explicitly stopped => ONLY named Sessions without any
     historical attempt enter `Da verificare`, even if the plan has
     not yet ended. The real main never re-enters "mai avviata".
   - Named Sessions with a real attempt are historical, not unstarted.
   - Internal-only past planned Sessions remain read-only review
     without inventing autonomous child execution.
   - `resolution_queue_api.py` reads accepted main `ended_at`
     directly from owner-scoped Session history, not guessed UI state.
     It neither creates Actual nor alters Schedule/Session records.
4. Activity Inspector: previously rendered named Play buttons without
   looking at the main's state, leading to rejected child Start after
   the main was stopped. Detail-only Session listing now derives
   main `open`/`paused`/`stopped` from existing authoritative
   Activity Session GET; updates on `dante:session-changed`.
   Child Play controls only mount while main is actively running.
   Otherwise the inspector shows `Avvia prima la principale`,
   `Principale in pausa`, `Da verificare` (never started,
   main stopped), or `Registrata` (attempted child).
   The planned-session indicator band remains unchanged.
5. Tests updated:
   - unit `tests/test_session_panel.py` for expiry, main Play,
     Pause/open, Stop, future Stop and attempted child exclusion;
   - PostgreSQL `test_session_panel.py::test_past_unstarted_review_pauses_on_main_play_and_returns_for_children_on_stop`;
   - Web `activity-planned-sessions-card-detail.test.tsx` ensures
     no invalid child Play before/while main paused/after Stop,
     and only valid buttons while main running;
   - browser `timeline-hardening.spec.ts` asserts neutral title
     cursor; `temporal-create-unified-ui.spec.ts` asserts Create font.
   
**Verification:** SOURCE CANDIDATE PUBLISHED, new tests not run by
assistant. Prior 56 green tests belong to preceding source and do NOT
certify this new regression repair. Run only focused Ruff/backend
unit/one PostgreSQL integration, typecheck, Inspector Vitest and two
targeted browser cases. Manual authenticated acceptance of real
Session history and label fit remains pending. Avoid full 27-group
gate.

## 2026-10-17 — Owner verification: 56 focused tests green

Owner provided WSL terminal output after fast-forwarding and checking exact
source HEAD `b50742c05f5aacf05fa5411bfe4d730716ba2e5a`:

- Ruff changed Python files: **PASS**, `RUFF=0`.
- Backend targeted `tests/test_session_panel.py`: **25/25 PASS**,
  `BACKEND_UNIT=0`.
- Real PostgreSQL targeted Session Panel integrations (past unstarted queue
  disappears on main Play/Stop; main started before preview retains the
  permitted cascade): **2/2 PASS**, `POSTGRES=0`.
- Web `tsc --noEmit -p tsconfig.json`: **PASS**, `TYPECHECK=0`.
- Web focused `timeline-surface.test.tsx` and
  `context-rail.test.tsx`: **25/25 PASS** over two files.
  A non-fatal `react-i18next` NO_I18NEXT_INSTANCE diagnostic appeared
  within the test run; neither file failed.
- Browser selected `timeline-hardening.spec.ts` tests covering
  title drag, live snapped preview / ruler pin, informational time hover,
  and keyboard nudge/Undo: **4/4 PASS**, `PLAYWRIGHT=0`.
  Browser test build succeeded (1546 modules transformed).
  Local fixture proxy `ECONNREFUSED 127.0.0.1:8000` for optional
  endpoint reads is expected without the backend in the isolated
  browser run and did not fail tests.

**Total: 56 focused tests passed; no test failures.** No full suite
or 27-group gate requested or run. This is source/test acceptance;
manual authenticated visual acceptance is **still pending** for elastic
drag target position across densities/zoom, card title/control hit
zones, typography fit in unchanged panel bounds, and a real past
Activity disappearing from Da verificare on main Play.

This commit records owner test evidence only; it does not alter code
or require repeat of already green tests.

## 2026-10-17 — Timeline interactions, review-on-Play, conservative typography (candidate)

**Approved exact scope:**
- Move cards in **15-minute increments** (including Alt+arrow keyboard
  nudge). During the pointer drag, the same elastic inverse-mapper/boundary
  calculation controls BOTH live time inside the dragged card and the
  final drop. Show one small ruler time pin; **no full-width ghost line**.
  Preserve the established Undo/governed canonical replan flow.
- Keep the card time informative, without fake hover/click affordance.
  Title single-click still opens Inspector, while motion past the drag
  threshold initiates card movement. Ordinary body single/double clicks
  and real Play/Pause/Stop buttons retain their original priorities.
  Empty Session-action wrapper regions must not block card drag/click.
- Modest typography uplift, without changing any panel/card/modal width,
  height, grid tracks or general structure. Start with readable card
  title/time/meta, Create/Edit Objective rows and reality copy, Edit body
  labels, and Session Panel labels. Italian first; English overflow needs
  owner visual review.
- **New normative B08 review policy:** once the real main Activity Session
  has ANY historical attempt (running, paused or ended), remove the
  Activity's "mai avviata" review rows permanently from the projection.
  Expired, wholly unattempted main-enabled Activities expose main and
  missing named Sessions. Expired internal-only Activities without
  main capability retain only unattempted named items. No fake Actual,
  automatic child Play, mutation of historical Sessions or new DB state.
  The separate manual resolution flow for internal-only past Sessions
  remains **deferred**. This policy supersedes the previous
  "main Stop immediately queues unstarted children" rule.

**Changes published on this branch:**
1. `timeline-day-stream.tsx`: shared `resolveDragPreview` returns
   clamped 15-minute placement from the current elastic day mapper,
   called both for live cloned card time/ruler marker and commit. Marker
   removed on cancel/drop/unmount; title is an allowed drag source
   while real Session buttons remain protected; drag-created native
   clicks are suppressed without swallowing later real title clicks.
2. `model/timeline-policy.ts`: pointer/keyboard move snap at 15m;
   `timeline-surface.test.tsx` keyboard nudge expectations updated.
3. `timeline-reference-lock.css` and `timeline.css`: remove
   informational clock hover, keep a neutral cursor, restore click/drag
   in otherwise empty Session controls area, lightly enlarge labels,
   add tiny fixed ruler time marker (without timeline geometry edits).
4. Scoped typography increments only in
   `temporal-create-objectives.css`,
   `temporal-create-reality-objectives-section.css`,
   `activity-edit-panel.css` and
   `timeline-session-panel.css`, no structural changes.
5. Backend `resolution_queue_api.py`: expiry-only unstarted
   projection, suppression once the main has ever been started,
   internal-only fallback per planned child. Unit tests updated
   `tests/test_session_panel.py` and PostgreSQL
   `tests/integration/temporal/test_session_panel.py` for:
   historical main Play/Stop, no future synthetic review, internal-only
   expired review, owner isolation and main Session attempt persisted.
6. `context-rail.tsx`: listens to the existing
   `dante:session-changed` event to refetch the resolution queue
   **immediately** after accepted Play/Pause/Stop, rather than only
   on focus/60s polling. Existing rail test covers the event.
7. `e2e/timeline-hardening.spec.ts`: browser regression checks
   title pointer-drag, live snapped time pin, final drop equality,
   and read-only clock hover. The established browser Undo test stays.

**Verification status: code PUBLISHED, focused tests NOT EXECUTED by
assistant.** Owner should run Web typecheck and focused Vitest files,
one Playwright file plus Ruff, backend unit and one real PostgreSQL
test file/method (avoid the 27-group full gate). These are regression
**candidates**, not green evidence. Authenticated real-world visual
acceptance of drag and typography remains pending.

## 2026-10-17 — Owner verified Create clock chevrons via Playwright

Owner fast-forwarded `feature/timeline-temporal-operational` to exact
`418ef21d3fd6744ee4ae025f5e255e679144cd93` and ran:

`pnpm --filter @dante/web exec playwright test --config playwright.config.ts e2e/temporal-create-unified-ui.spec.ts`

**PASS: 1/1 browser test in 5.2s, PLAYWRIGHT=0**. Vite
transformed 1546 modules and the production preview build succeeded.
The test checks both Quick and Advanced Create eight-hour/minute arrow
computed styles (8px, borderless, transparent, matching Edit's
chevrons), while preserving the tested compact/full-size clock
field bounds and the Advanced shared Objective row.

Vite warned about large chunks; the unauthenticated isolated
`/home` fixture emitted non-fatal proxy `ECONNREFUSED
127.0.0.1:8000` for optional backend requests because the real
backend was not running. These did not fail Playwright.

**Automated acceptance of the isolated Create chevrons fix is
complete**. Owner's manual visual comparison in the authenticated
real-data UI is still pending. This entry is documentation only:
no additional source code or test reruns requested.

## 2026-10-17 — Exact Create vs Edit hour/minute chevron correction

Owner visually compared Quick Create, Advanced Create and Activity Edit
and clarified that **the only remaining desired visual change is
the up/down hour/minute chevrons**. Date/time field shells, sizes,
grid columns, timezone UI, duration, Activity plan logic and Objective
editor are already acceptable and must not be changed.

**Root cause:** `temporal-create-u1-polish.css` adds 22px-wide,
10px-tall bordered/background mini-buttons to
`.temporal-create-composer .temporal-create-time-segment > button`.
Edit uses the same TimeControl markup *outside* the Create composer,
so its base chevrons stay plain, borderless, transparent and 8px
tall. Previous parity changes had targeted input color/borders/widths,
not this actual cascade difference.

**Fix:** only
`temporal-create-time-visual-parity.css` now neutralizes the
Create-only button decoration for the two main start/end clock fields
in **Quick and Advanced Create** and for additional Advanced Activity
interval clock fields. The triangles match Edit's 8px, borderless,
transparent controls and 8/20/8 vertical segment rows.
Keep all clock/date field containers, modal geometry and clock behavior
intact. No new JS handlers or temporal/domain changes.

**Focused browser regression:** extended
`e2e/temporal-create-unified-ui.spec.ts` to require eight bare
arrows in both Quick and Advanced. Assertions check the actual
computed 8px height, zero border, transparent background and 5px
triangle glyph, alongside the already established compact Quick
field / full-size Advanced field assertions.

**Verification:** source candidate PUBLISHED / final Playwright
regression **NOT YET RUN** by assistant or owner. The prior
Objective 48/48 Vitest and TypeScript checks remain valid for
unchanged TS logic; do not claim visual acceptance until new browser
test passes and owner verifies the screenshot comparison. No full
gate warranted.

## 2026-10-17 — Owner verified i18n-independent Objective row

Owner pulled `c03819b22b051ba1c13cf73e025f560fa1b2b49d`
using `git pull --ff-only origin feature/timeline-temporal-operational`
and verified exact HEAD before running the two outstanding focused
checks:

- `pnpm --filter @dante/web typecheck`: **PASS, TYPECHECK=0**.
- `pnpm --filter @dante/web exec vitest run
  src/features/temporal-create/ui/temporal-objective-editor-row.test.tsx
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx`:
  **2/2 files PASS, 48/48 tests PASS, VITEST=0**. The shared-row tests
  passed 4/4; Activity Inspector tests passed 44/44, including the six
  previously failing Objective edit/recurrence/correction/add/remove/
  undo scenarios. No unhandled exception or missing translation
  context appeared in this run.

The earlier focused Advanced Create Vitest (2/2) and isolated
non-auth Quick/Advanced Playwright (1/1) had passed on the earlier
`fd85869d` code candidate; the `c03819b2` update only changed
the shared Objective row's locale dependency and related tests,
not the clock UI geometry.

**Automated changed-area verification is now green on these
source-equivalent boundaries.** A manual authenticated, real-data UI
comparison remains **NOT RUN**: Quick Create's hour/minute controls
must stay compact, Advanced Create's datetime controls should
visually match Edit, and Create/Edit Objectives should present the
same fields and spacing. No 27-group full gate requested or run.
This is an evidence-only handoff update.

## 2026-10-17 — Owner WSL focused UI evidence and i18n repair candidate

Owner supplied terminal evidence pinned to
`fd85869da30484496390cd792c75f86950fb02cc`:
- `@dante/web typecheck`: **PASS**, exit 0.
- Focused Vitest three files: **43 passed, 6 failed**, five caught
  unhandled exceptions. All six failures belong to
  `activity-inspector-actions.test.tsx`, covering persisted Objective
  editing, recurring scope, result correction, staged addition,
  X removal and undo.
- The shared Objective presentation row called
  `useTranslation('common')`, then unconditionally evaluated
  `i18n.language.toLowerCase()`. In the Activity Inspector test
  runtime there was **NO_I18NEXT_INSTANCE**, hence undefined language
  caused a render-time TypeError, unmount and missing selectors.
  The passing Advanced Create tests were not evidence that the Editor's
  test/runtime setup supported that extra implicit dependency.
- Focused non-auth `e2e/temporal-create-unified-ui.spec.ts`:
  **1 PASS, PLAYWRIGHT=0**. Vite built successfully. Proxy
  `ECONNREFUSED 127.0.0.1:8000` is fixture-only, not a passing
  backend contract.

**Repair now published, NOT YET OWNER-RETESTED:** the presentational
`TemporalObjectiveEditorRow` no longer invokes `useTranslation`.
It accepts a required explicit `italian: boolean` flag. The Create
owner passes the language it already resolves with its own existing
translation hook; the Activity Edit owner passes `italian`, preserving
the pre-existing Italian editor labels. The shared row test no longer
initializes global i18next and thus exercises the dependency-free row
directly. No Objective persistence, mutation/retry/CAS, recurring
lineage, recorded result correction or datetime logic changed.

**Only required next verification:** `pnpm --filter @dante/web
typecheck` and the two Objective-specific Vitest files
(`temporal-objective-editor-row.test.tsx` and
`activity-inspector-actions.test.tsx`) on one exact final SHA.
The 1/1 browser test and unrelated Advanced Create test already
passed on a source with unchanged layout. Do not launch full gate or
claim the previous six Editor failures are green before owner retest.

## 2026-10-17 — Unified Objective editor and scoped Create clock visuals (candidate)

Owner approved UI-only parity with an explicit exception: **Quick Create's
hour/minute controls alone may change their styling; the quick form must
remain compact and otherwise unchanged**. Advanced Create and Activity Edit
are the full-size surfaces.

**Implementation on this branch:**

1. Extracted `TemporalObjectiveEditorRow` as one shared presentational
   renderer for Advanced Create and Activity Edit: labels, result kind,
   comparator, numeric target/range, unit, move/remove controls and primary
   input use the same markup and CSS. `TemporalCreateObjectives` retains
   U2 authoring state/patches; `ActivityObjectiveRow` retains existing
   Objective identities, CAS revisions, persisted/recorded-result guards,
   recurring edit scope and the single-commit Activity Edit save. The
   existing result-correction flow is untouched. Edit can reorder staged
   Objective presentation order; changes stay staged for the same final Save.
   Retired the duplicated editor-specific row CSS.
2. `TimeControl` and `TemporalCreateDatePicker` were already shared by
   Create and Edit. Added a dedicated
   `temporal-create-time-visual-parity.css` imported only alongside
   `temporal-create-core-u2.tsx`, with full-sized Advanced Create
   date/time row matching Edit's five-track/820px layout and 46px controls.
   Quick Create rules affect only its two `TimeControl` faces: **no Quick
   date-picker, timezone, row width, modal geometry or 42px minimum size
   alteration**. No new date/clock logic, persistence semantics, or
   timezone/DST conversion. The pre-existing Activity polish file is
   unchanged, avoiding unrelated session/interval CSS side effects.
3. Tests added:
   - `temporal-objective-editor-row.test.tsx`: shared field structure,
     equivalent edit labels, callbacks for content/kind/order/remove and
     disabled-state protection.
   - `e2e/temporal-create-unified-ui.spec.ts`: Quick remains compact at
     42px; Advanced uses 820px full interval and 46px clock fields;
     Advanced Objective rows retain common markup.
   - Existing `activity-inspector-actions.test.tsx` and
     `temporal-create-advanced-activity-ia.test.tsx` cover staged
     persisted-edit Objective actions and Advanced Create identity.

**Verification:** candidate SOURCE PUBLISHED / local pnpm TypeScript,
Vitest, ESLint/Prettier and browser tests **NOT RUN** by assistant.
Must not call this fully accepted until the owner runs **only focused Web
checks** and visually confirms Quick vs Advanced vs Edit on the same final
source. User explicitly rejected the unrelated 27-group full gate.

## 2026-10-17 — Owner recheck on `fcb95fc3`: focused Web blockers green

Owner provided direct WSL terminal evidence after fast-forwarding from
`4b284ceb` to `fcb95fc3520b259bdce59a1659c90493ef03fe27`:

- `pnpm --filter @dante/web typecheck`: **PASS** — `tsc --noEmit`
  completed with no diagnostic and the following Playwright command ran.
  The optional Life Area `colorCode` TypeScript error is closed.
- `pnpm --filter @dante/web exec playwright test --config playwright.config.ts
  e2e/timeline-hardening.spec.ts -g "a long Activity title"`:
  **1 passed in 7.9s; PLAYWRIGHT=0**. The isolated non-auth browser
  test verifies Activity CSS ellipsis using the known fixture card.
- Vite build and the entry/size budget check completed successfully.
  Vite emitted a non-fatal large-chunk warning and the non-auth page's
  optional API proxy emitted `ECONNREFUSED 127.0.0.1:8000` because the
  real backend was not running; neither is a new failed test.

Together with the earlier owner results on `4b284ceb` (Ruff PASS,
24 Python unit PASS, 1 real PostgreSQL PASS, 84 Vitest PASS and the
Event indicator browser geometry test PASS), **all changed-area
automated checks have evidence of PASS**. The newer commit only
normalizes the dropdown optional color and the isolated browser fixture
selector and updates handoff. The user explicitly rejected running the
full 27-group gate for this task. **Actual authenticated real-app visual
acceptance of title, footer, short Stop and Life Area dropdown is still
pending**; do not claim it was browser-verified against owner data.

## 2026-10-17 — Owner focused tests / TypeScript and browser follow-up

Owner supplied WSL results after verifying exact source SHA
`4b284cebba41e494100f8b2e06af407a078d250c`:
- Ruff changed Python files: **PASS** (exit 0).
- Backend `tests/test_session_panel.py`: **24/24 PASS** (exit 0).
- Real PostgreSQL session-panel main Stop-to-review integration: **1/1 PASS** (exit 0).
- Four selected Vitest files: **84/84 PASS** (exit 0).
- `@dante/web` TypeScript typecheck: **FAIL**, TS2322 at
  `activity-edit-panel.tsx:1833`: optional catalog `colorCode` was
  emitted explicitly as `string | null | undefined`; the shared select
  accepts `colorCode?: string | null` with `exactOptionalPropertyTypes`.
- Two selected Playwright checks: **1 PASS / 1 FAIL**. Event footer
  lower-edge browser geometry passed. The Activity title test timed out
  looking for `.timeline-event-card--activity` on the unauthenticated
  static fixture page. That page has generic fixture cards but no real
  persisted Activity owner, so the failure is a **test setup/selector
  mismatch** rather than a demonstrated CSS wrapping defect.
  The fixture Vite proxy logged expected backend
  `ECONNREFUSED 127.0.0.1:8000` because real-stack API was not started.

**Follow-up commits:**
- Normalize dropdown `colorCode` to `area.colorCode ?? null` to satisfy
  exact optional property typing without losing any canonical non-null
  persisted Life Area color.
- Check computed browser Activity title cascade by adding only
  `timeline-event-card--activity` class to fixture card
  `[data-timeline-event="7"]`, as the isolated non-auth fixture does
  not instantiate a real scheduled Activity. This remains a CSS regression,
  **not** authenticated Activity persistence proof.

**Current verification status:** two specific fixes published, targeted
TypeScript and the one previously failing Playwright test **NOT RE-RUN**
on the updated HEAD. No repeat of 109 already passing tests or a
27-group full gate is requested. Inspect visual screenshots and actual
authenticated Activity independently in the real app.

## 2026-10-17 — Card layout, Life Area edit colors and Stop-to-review candidate

A separate conversation reported source changes prepared locally but not pushed.
GitHub branch was verified at `657c23cf582a7f835ae8c7f8a5919b230888904f`,
which had none of the new four screenshot fixes. The current candidate is
implemented directly on the existing branch; this is **not** an assertion
that the inaccessible local diff was cherry-picked.

**Source corrections:**

1. Activity card title is **one line with ellipsis** under both base and
   production reference CSS. Removed now-obsolete second-row height from
   `timelineEventReadableHeight` and its policy/test expectations. The
   real full title remains available via accessible name and tooltip.
2. Grouped **Sessioni / Obiettivi / Scaletta** indicator rows are rendered
   after the elastic drag spacer, in one lower-edge footer. Week view
   intentionally hides the entire footer. Event subitem expansion reserves
   space for its lower expander.
3. A completed main Session shorter than five minutes reserves **168px**
   of layout/clock-local readable height, including the planned/actual
   labels, Life Area and indicators. Longer completed Sessions keep their
   existing dynamic geometry; this neither adjusts Schedule nor factual
   Session times. Second-level Stop precision and mapper invariants remain.
4. Activity edit now passes canonical `colorCode` from the Life Area catalog
   into the already-shared `TemporalLifeAreaSelect` swatch control.
5. Read-only **Da verificare** projection now recognizes a genuine stopped
   main Activity Session as an immediate trigger for never-started named
   Sessions, without awaiting all planned intervals to end. Existing
   plan-expiry behavior remains. The owner-scoped read enriches existing
   historical attempts with their stored `ended_at`; no new facts,
   database objects or generated contracts. Previously started named
   Sessions are not incorrectly classified as unstarted.

**Added/updated focused regressions:**
- Vitest `model/timeline-density.test.ts` (long-title no-height change),
  `timeline-session-reality.test.ts` (short Stop readable floor),
  `timeline-surface.test.tsx` (indicator footer placement), and
  `activity-inspector-actions.test.tsx` (two distinct canonical Life Area
  colors in edit option swatches).
- Playwright `e2e/timeline-hardening.spec.ts` (production one-line
  computed style and lower-edge Event indicator geometry).
- Python `tests/test_session_panel.py` (explicit main Stop before a future
  Activity interval; both untouched children require review; previously
  attempted child excluded; no phantom children).
- Real PostgreSQL `tests/integration/temporal/test_session_panel.py`:
  the established early main/child Start-Stop sequence must show only
  the untouched child under `session_unstarted` after main Stop.

**Verification:** PUBLISHED SOURCE CANDIDATE / NOT RUN on final SHA.
No assistant-side pnpm, Ruff, pytest, PostgreSQL or real-browser
execution. Owner's previous 32 focused green tests were on
`f047d50b` and do not certify this candidate. User explicitly requested
**only changed-area focused tests, not the 27-group full gate.** Do not
claim visual/product acceptance until owner checks the screenshot cases in
the real application.

## 2026-10-16 — Owner WSL evidence for early-main child visibility

User ran focused checks after a verified fast-forward to
`f047d50b29203730205e7f2669e73297e90ef496`:

- `apps/backend/tests/test_session_panel.py`: **21 passed** (exit 0).
- Real PostgreSQL `tests/integration/temporal/test_session_panel.py::test_main_started_before_preview_exposes_all_children_and_preserves_cascade`: **1 passed** (exit 0).
- `apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx`: **10 passed** (exit 0).
- `pnpm --filter @dante/web typecheck`: **exit 0**.

**32 targeted tests PASS, all four focused commands exit 0.** This
closes focused unit/DB/Web/type verification for the early-start
Session panel projection, including owner-scoped reads, two configured
internal rows, Pause, Stop and no automatic child execution. Full gate,
authenticated real-stack browser and manual screenshot acceptance were
**not run**, by explicit user request to test only the changed behavior.
No new migration or API/client generation was required. This entry is a
documentation-only record of user-supplied terminal output; it does not
invalidate the source-equivalent focused code test evidence.

## 2026-10-16 — Early main Play must reveal configured internal Sessions

**Real-app regression:** an Activity with two named internal Sessions and
a planned 23:30–24:00 interval was started at approximately 20:46.
The Activity card and Session panel correctly showed the open main Session,
but the panel omitted both configured internal rows until the standard
five-minute preview. Screenshot evidence from user.

**Confirmed backend cause:** `build_panel` computed named-row eligibility
from `upcoming` only, whereas main execution visibility uses
`owner["executions"]` independently. When explicitly playing the main
Session hours early, its open execution existed but `upcoming=False`.

**Implemented candidate:**
- The read-only, owner-scoped panel projection admits configured unstarted
  internal rows when an actual main execution is open (running **or paused**),
  even before preview or after the accepted Activity interval. It never
  modifies the Schedule or starts children.
- In the existing UI the children show **Pronta** with individual Play when
  main is running; when main is paused they remain visible but Play is
  disabled. Main Resume does not resume any internal Session automatically.
  Main Stop removes early readiness again.
- A child ended within the current main attempt must not reappear as
  “Pronta”; restarting a **new** main attempt re-admits previously
  stopped configured children. The projection uses the actual open main
  start supplied by the same owner-scoped Session visuals read.
- No changes to PostgreSQL schema, SQL ACLs, migrations, Session command
  semantics, generated clients, or canonical temporal truth.

**Regressions added:** deterministic backend before-preview Play, two
internal names and refs, pause/Stop, outside the planned interval, child Stop
and new main attempt; Web card-originated `dante:session-changed`
refresh with two children, Play enabled/disabled and no auto-start;
PostgreSQL readback with two real persisted named Schedules, owner isolation,
early parent Play, explicit child Play/Stop, main Pause/Stop, and retained
configuration.

**Verification status:** GitHub source/test candidate only. Unit,
Vitest, TypeScript, PostgreSQL, authenticated browser and manual real-app
checks **NOT RUN** on this new SHA. Owner requested **focused tests only**;
do **not** launch the 27-group gate for this correction. The previous
40/40 Timeline Vitest and 1/1 nonauth browser PASS were on an **older**
SHA and do not certify this change.

## 2026-10-16 — Owner WSL focused acceptance on `62f9ebb3`

Owner supplied the full shell output after `git pull --ff-only` and an
exact-HEAD assertion to
`62f9ebb366617ed18e2af501c4e1116a71dca5b8`:
- `timeline-temporal.test.ts`: 4/4 PASS
- `timeline-density.test.ts`: 9/9 PASS
- `timeline-session-reality.test.ts`: 11/11 PASS
- `timeline-surface.test.tsx`: 16/16 PASS
- **Vitest 4 files / 40 tests PASS, zero failures**.
- `pnpm --filter @dante/web typecheck` completed with exit 0:
  subsequent Playwright ran in the same `set -euo pipefail` shell.
- Non-auth `playwright.config.ts`, single
  `e2e/temporal-create-contexts.spec.ts`: **1/1 PASS (5.2s)**.
  Vite client build and its entry-size check passed. Build reports a
  non-fatal oversized chunk warning.
- Vite proxy logged `ECONNREFUSED 127.0.0.1:8000` for Drafts,
  resolution queue, finished work and objective work: backend was not
  accepting connections. These are **not** real-stack API/DB evidence;
  they did not fail this non-auth browser test.

These results close the five originally reported *focused* Web regression
failures on exactly `62f9ebb3`, including short Stop placement and compact
overlap, **not** full 27-group acceptance or authenticated real-stack
browser proof. No source changes are inferred from the log. Next:
run the complete 27-group local gate on a clean, pinned branch HEAD and
preserve `LATEST_GATE_SUMMARY.md` + original log archive; then inspect
Timeline/Giorno with actual Play/Stop behavior in the real app. This
documentation-only checkpoint does not alter Web source or SQL.

## 2026-10-16 — Focused Web 5-red handoff after `5df23f72` (corrective candidate)

The user ran the exact `5df23f72c61f6867e1e0160e6109b3fc9c35d2c7`
focused Web Vitest command in WSL: **35 PASS / 5 FAIL** (4 files, 40
tests). Shell `&&` short-circuited at Vitest, therefore **typecheck and
Playwright were NOT RUN** in this user command.

Failures and corrective scope:

- `timeline-density.test.ts`: a one-minute Activity at 20:15–20:16
  expanded its enclosing 30-minute card to 306.8px, violating the <280px
  compactness assertion. The Timeline mapper now allocates minimum height
  shortest-first, accounting for pixels already reserved by overlapping
  cards instead of summing entire minimums twice. The original strict
  compactness test is retained, not loosened.
- `timeline-session-reality.test.ts`: a 19:31:20–19:31:25 completed
  Session's card end extended below the 19:31:30 now line. The original
  mapper used a one-minute floor for its required slope, giving only
  a few pixels between the real second anchors while the card reserved
  156px. A sub-minute knot now allocates its readable height between
  the factual fractional-minute start/end, without scaling the entire
  60-second minute. Interpolation uses the actual fractional interval,
  not the old `Math.max(1, duration)` denominator. The existing
  exact-now assertion remains; new midpoint/inverse/bounded-expansion
  assertions protect continuity and prevent whole-minute explosion.
- Three `timeline-surface.test.tsx` failures came from the intentionally
  retired inline `Modifica orario` control or 5-minute keyboard
  expectations. Tests now assert read-only card time, focus transfer by
  clicking that time, unchanged Inspector title flow, and one-minute
  `Alt+ArrowUp/Down` increments across repeated focus changes. No
  inline card time editor was reintroduced.

**Evidence:** GitHub commits published after `5df23f72`; all changes
are a **NOT_RUN candidate**. This assistant environment cannot run the
repo's pnpm/Vitest/PostgreSQL/Chromium stack. Must rerun the original
four focused Vitest files, `@dante/web` typecheck and the non-auth
`temporal-create-contexts.spec.ts` Playwright case **on the same
current HEAD**. If green, continue the full 27-group gate and real
Timeline/Giorno visual acceptance; do not infer green from source review.
No server, database, migration, API or recorded Session authority was
changed by this repair.

## 2026-10-16 — Minute-exact time authoring across Activity/Event/Timeline

**User-reported high-severity data-integrity issue:** authoring Activity or Event
`10:30–10:31` silently saved `10:30–10:35`. Every explicit minute must remain
canonical truth, including occupied Activity intervals and edited/moved cards.

**Confirmed root causes:** two `Math.max(5,...)` clamps in
`temporalCreateDurationFromEndDateTime` and `...FromEndTime`; Create timed
validation required `durationMinutes >= 5`. Create time spinner arrows
used 15-minute jumps in both U2 and legacy components. Timeline TimeEditor
minute arrows/wheel/ArrowUp used 5-minute steps, as did default drag snap.
There was no corresponding five-minute minimum on typed Schedule acceptance:
the backend requires positive intervals, not quarter-hour/five-minute grid.

**Published candidate:**
- Create calculations and validation accept **every whole minute >= 1**;
  invalid zero/negative still rejected.
- Both Create control variants use **1-minute** spinner arrows; arbitrary
  00–59 typed minutes remain accepted. Clock dropdown retains optional
  quarter-hour shortcuts but shows any exact off-grid authored value as the
  selected option. No rounded suggestion pretends to be the current time.
- Timeline TimeEditor arrows, wheel and minute ArrowUp/ArrowDown use 1 minute;
  PageUp/PageDown remain deliberate 15-minute acceleration shortcuts.
- Drag and keyboard replan snap at 1 minute at all zoom levels, not 5 minutes;
  the elastic ruler's 15-minute ticks remain merely visual.
- Existing recorded **Session minimum duration authority is unchanged**;
  planned Activity/Event Schedules and Activity occupied bands are not
  execution Session duration rules.
- Unit tests cover exact 1–4-minute durations, overnight and DST semantics,
  Quick/Advanced × Activity/Event manual input, picker selection and arrows,
  outgoing U2 canonical payload, extra Activity interval with non-grid ends,
  zero/negative invalid, Timeline TimeEditor and snap, plus a PostgreSQL
  integration test creating/revising/reading Activity and Event 1-minute
  Schedules without rounding or padding.

**Evidence boundary:** code and regressions pushed through GitHub.
Vitest, TypeScript, PostgreSQL and browser checks **NOT RUN by the assistant**;
user must verify on the new exact branch HEAD. Do not call this fixed until
`10:30–10:31` survives actual creation, reload and editing in browser.

## 2026-10-16 — Focused WSL acceptance: Quick Create vertical anchoring

User-provided `BROWSER_NONAUTH.log`, `BROWSER_REAL_STACK.log`,
`POSTGRES.log` and `TYPECHECK(3).log` show:
- TypeScript PASS; PostgreSQL 2/2 PASS.
- Authenticated Playwright 19 PASS and 2 WebKit skipped (no failures).
- Non-auth Playwright 22 PASS, **one failing test**:
  `temporal-create-manual-hardening.spec.ts` Quick Create bottom at
  1443.52px in a 900px-high browser window. Full Advanced was not reached
  because the Quick assertion failed first.
- No acceptance PostgreSQL volumes remained.

Root cause: Desktop Home Context Rail lives below the tall hero and carries
`transform: translateX(0)`, which creates a containing block for fixed
descendants even at an identity transform. Previous Quick Create CSS bounded
the panel's **height** but anchored its **top** to the below-fold rail.
The new base-only selector removes that transform while Quick Create is open
and positions its host `fixed` at viewport `top:104px; right:18px;
bottom:16px`, at 475px rail width. Quick's composer fills this bound.
Advanced uses separate `.is-advanced` selectors and is untouched.

The browser regression now requires the Quick host be fixed and Quick Y be
within 120px, in addition to the existing bounds and Advanced checks.

**Status: implementation published, user must run focused nonauth Playwright
again.** The assistant did not run tests or declare this fix PASS.

## 2026-10-16 — Full-gate archive triage (895794f9)

The actual `FULL_GATE_LOGS.tar(20261016-103821).gz` uploaded by the
user was inspected along with browser trace artifacts for SHA
`895794f9be8bbab592cd7e9d298a2f4104f0afe8`. All 27 groups ran.
Failures: 2 PostgreSQL expected-history/catalog checks; 7 nonauth
Playwright tests (120 passed); 10 real-stack Playwright tests (82 passed,
4 skipped). A transient PostgreSQL shard 06 failure recovered on isolation
retry. Docker acceptance volumes: none before or after.

Changes on this branch:
- Synchronize PostgreSQL catalog expected completed stages/counts and
  `20261015_159` forward-only downgrade message without altering SQL.
- Restore real Life Area label in Activity cards under planned/actual hours,
  above the internal-Session strip. Real-stack Golden test asserts placement.
- Replace obsolete browser selectors for retired unplaced-item management
  with direct canonical API persistence assertions and Draft Vault separation.
- Test actual defaults-off for optional Timeline milestones/margins and verify
  enabling, disabling and resetting them.
- Assert collision-free fixed-width cards within group columns and reachable
  in horizontally scrolled compact tracks instead of old proportional width.
- Reacquire a real visible card body point after scrolling for drag/focus
  tests; still require correct drag overlay and focus retarget.
- Double-click and Shift-drag Create test now finds a visible empty timed
  canvas spot below the all-day header, rather than hitting a card at x=600.
- Bound the basic Create host to viewport height without editing Advanced.

The long real-stack Schedule test was terminated under 27-group gate load
after using the removed unplaced management panel, so acceptance must check
it in isolation after the selector update.

**Evidence policy**: candidate code published. Tests intentionally NOT_RUN
by assistant, per user. Formatting-only checks are deliberately deferred.
Do not call this fully green until user WSL focused PostgreSQL and both
browser suites confirm it.

## 2026-10-16 — User-run Timeline geometry focused verification follow-up

User WSL evidence on `b92a6a659c8f7e868f0f24fbb631dbc2de19bc1b`:
60 focused Vitest tests: 57 passed, 3 failed; `@dante/web` typecheck:
3 TS2345 errors; `@dante/web` build: PASS (Vite chunk-size
advisory only). The failures were reported at exact source lines, not
guessed from a later commit.

Corrections published:
- Explicit `minimumGroupWidth: number` on the expanded track geometry;
  the previous inferred literal type `260` prevented actual group widths.
- Removed obsolete `compactLaneRegionPercent/2` cluster limit from the
  regression; lane order and right bound remain enforced, while the new
  fixed-pixel collision tests still cover actual non-overlap.
- Ended Activity projection regression now enforces min-height 116px,
  no expansion relative to its planned card, real visible interval end and
  preserved canonical Schedule instead of demanding a strict height shrink
  below the common minimum.
- Separate main/internal Session regression compares the same Activity
  with and without its named internal Session to directly assert its
  actual geometry and label are unchanged.

**Verification status:** edits are published, NOT_RUN by assistant. User
must rerun focused Vitest, typecheck and build together on this newer SHA.
Do not claim these corrections PASS until the logs confirm them.

## 2026-10-16 — Timeline card geometry / group packing regression repair

The user supplied four visual reproductions: moving several Activity/Event
cards toward the same starts caused intrinsic widths to shrink or grow,
occasional side-by-side cards to overlap, and expanded group columns to drift
in both rolling Timeline and Giorno views.

**Implementation candidate:** the production card now derives one immutable
width solely from title and Activity/Event kind (Activity floor 352px, Event
floor 292px, capped at 456px); Play/Pause/Stop and lane pressure cannot
re-measure or shrink it. Activity height reserves at least 116px for heading
and runtime actions, planned/real times and the internal-Session indicator;
Event height reserves 88px. The Activity heading reserves 74px for controls
even before Play and after Stop; long titles clamp to two lines.

The shared viewport runtime now positions collision lanes with a fixed pixel
pitch and expands the horizontal track whenever necessary. The same fixed
width is used in compact, partially-expanded and fully-grouped modes; the
grouped track/header share one computed width, including extra lanes needed
by multiple simultaneous cards in the same group. Hidden groups do not
inflate the visible group count. Crowded compact tracks enable horizontal
scroll instead of cropping events. The week view keeps its own compact
minimum and widens its seven-column track rather than compressing simultaneous
card slots. Live Session projection uses its unchanged **painted** height to
reserve a correct collision lane; the independent elastic ruler scale and
canonical Schedule are not changed by Play.

Colocated Vitest regressions now exercise four simultaneous cards,
variable starts, overlapping group members, every intermediate expansion
fraction, fixed DOM width, scroll reachability and relocated live-Session
painted-height collisions.

**Evidence boundary:** GitHub code and test changes are published. The
assistant has **NOT_RUN** Web Vitest, typecheck, lint, Prettier, real-browser
or full gate; these remain user-run WSL checks. Visual acceptance still
requires dragging real Activities/Events at identical starts in Timeline
and Giorno and opening group expansion to 100% while inspecting actual card
geometry on the final exact commit.

## 2026-10-16 — User visual review follow-up (candidate)

The first visual review found a too-small idle ruler/card scale, zoom clicks
at a bound appearing to reverse, view switches opening at the top of the day,
Play-dependent card width, raw fractional gap labels, unexplained milestone
flags and stale controls after Stop. The Web candidate now uses hourly labels
in a quiet day, adds quarter labels only where the nonlinear map has adequate
pixel separation, increases readable ruler/card type and reserves stable
Activity title/control/actual/count space. Zoom clamps before changing its
viewport anchor and disables the reached limit. Every view switch returns to
today with the current minute about one third below the viewport top. Margins
and milestones are opt-in; enabled gap labels round to whole minutes and say
what they measure. After Stop the card has no runtime controls, while the
Inspector retains a compact recorded duration and no Play/Stop.

Focused Web verification passed (9 files, 85 tests), as did Web typecheck,
changed-file ESLint, Prettier and the production build/bundle budget. The next
step is a user WSL visual pass on the published SHA. No PostgreSQL or
authenticated-browser evidence is inferred from the local component tests.

## 2026-10-16 — Activity Session card and three-view candidate

The Activity card now refreshes its configured internal Session count after
editing. The main Activity Session visually relocates on Play without changing
its height on Play/Pause; Stop immediately uses its actual interval, and a
short stopped interval remaps the elastic ruler to avoid a card extending past
its displayed end. The accepted Schedule remains unchanged. Internal Sessions
alone do not move the card. The paused fill retains a subdued orange instead
of turning the card gray; the card labels planned and actual times separately.

The toolbar has Timeline/Giorno/Settimana views. Giorno uses the same elastic
day layout, while Settimana aligns seven compact columns on one shared minute
scale and retains horizontal expansion. The ruler admits :15/:30/:45 labels
only when mapped pixel spacing allows them. In the scratch candidate the
complete Web Vitest run passed (222 files, 1065 tests); Web typecheck, global
ESLint, production build and bundle budget also passed. An unrelated but
adjacent `async` without `await` in the Inspector's Bozze regression was
removed to make the global lint gate truthful. Authenticated real-stack
Playwright and user visual acceptance remain pending in the user's WSL
environment; no PostgreSQL/backend gate is claimed for this Web-only change.

## 2026-10-16 — Direct Timeline withdrawal retired (candidate)

The user rejected “Rimuovi dalla Timeline”, its Undo, and the separate
“Da collocare” destination. The direct controls are removed from timed and
all-day cards and Inspectors. The Activity/Event withdrawal clients and their
five dedicated HTTP reads/writes are removed, the generated OpenAPI/Orval
client is updated, and forward migration `_159` drops the five dedicated SQL
functions introduced for those actions. The no-op postponed panel and unused
withdrawal copy/styles are gone. Generic Schedule revision and the older
Schedule primitives used by coordinated editing remain; historical operation
rows are not deleted or rewritten. The legacy existing-items tray is no longer mounted, and the Draft Vault
shows only inert drafts. Historical canonical rows remain in PostgreSQL;
no automatic data conversion or deletion is performed.

Focused Web component tests and Web/API-client typechecks pass in the scratch
worktree. PostgreSQL migration and deterministic FastAPI OpenAPI export could
not run here (no Docker/Python 3.14 toolchain); user WSL validation and visual
acceptance remain open. Do not claim an all-green gate.

## 2026-10-15 — Inspector and Activity card visual repair candidate

The current user screenshot review retired the direct Inspector controls that
unplace an already-created Activity/Event and the old "Sposta in Da collocare"
shortcut. Quick actions retain the distinct "Sposta in Bozze" Activity move and
"Copia in Bozze" Event copy. Canonical unplaced records and low-level recovery
capabilities remain in persistence for existing history; they are not relabeled
as inert drafts.

The Activity card keeps title and runtime controls in the heading, planned
time below it, then only its own main Session timing when recorded and the
planned Session indicator when present. After Stop its card controls vanish.
The density mapper reserves at least 94px for Activity card content at the
same minute scale as the ruler. The visible minor grid interval is 15 minutes
by explicit user preference in this correction; the adaptive density slots
also remain 15 minutes. Colocated regressions have been updated, but browser
and WSL focused checks on this candidate are **NOT_RUN**. Visual acceptance
remains open.

## 2026-10-15 — Disposable PostgreSQL test-volume retention correction

The PostgreSQL acceptance fixture previously used the Docker image-declared
anonymous data volume and removed only its container. Docker consequently
retained one anonymous volume for every completed disposable cluster. The
fixture now creates one uniquely named, labelled data volume per acceptance
cluster, mounts it explicitly and removes that exact volume in `finally`.
The parallel gate additionally removes only stale, dangling volumes bearing
the test label and generated-name pattern before it starts the PostgreSQL
queue. It never performs a global Docker prune and never targets the persistent
`dante-local` Compose volumes. The focused harness regression test and runner
self-test must pass before this operational correction is treated as verified.

## 2026-10-15 — Full gate at `43778ea4` and repair candidate

The user's WSL parallel gate at `43778ea49b0bc12285ebb1b08810da49463c6e67`
collected all 27 groups with a stable source tree: **18 PASS, 9 FAIL**.
Ruff/format, Mypy, Dictionary schema and Temporal OpenAPI inventory expose
deterministic source/test drift; Web lint found one unused function. The
authenticated real-stack browser could not start because the required
`dante-postgres-local:18.6` Docker image was absent. Five PostgreSQL cases
failed or errored, but the uploaded summary lacks their tracebacks, so their
causes are not yet established. OpenAPI snapshot and generated client are
behind the eight newly added Temporal routes.

This corrective source candidate formats affected Backend/Web files, fixes
the strict typing and outdated current-head downgrade assertion, admits all
70 current Dictionary stages, enumerates 193 Temporal operations and removes
the unused Web helper. Locally Ruff check/format, repository Prettier,
structural test registry, Web typecheck and 50 focused Inspector tests pass.
The full Web Vitest run had one jsdom computed-style failure in an unrelated
Planning Tray test (1064 passed, 1 failed); the five cases in that file pass
when rerun alone. This is **not** a same-SHA full green gate.

Remaining evidence: export and publish the governed OpenAPI/Orval artifacts
from the WSL Python 3.14/pnpm toolchain; inspect the original PostgreSQL
tracebacks in the existing `FULL_GATE_LOGS.tar.gz`; build the required local
PostgreSQL image; then rerun the full gate once on the final candidate SHA.
No real-data destructive acceptance or visual closure is claimed.

## 2026-10-15 — Destructive Inspector browser regression candidate

The one-off Activity and Event authenticated browser journeys now create their
own scheduled subject, open its Inspector, cancel a deletion, then confirm a
fresh deletion and prove the Schedule is absent after reload (Activity also
checks the canonical profile is gone).
Colocated Inspector tests cover recurring Activity scope choice and recurring
Event Occurrence selection versus full-series confirmation. The obsolete,
disabled Event delete icon was removed from the same toolbar as the now-live
Event action; it previously presented a contradictory inert control.

These source/tests are **NOT_RUN** in the WSL real-stack environment. A prior
single Playwright PASS on `624e3766` covered only Activity card move and cannot
certify this newer candidate. PostgreSQL migrations `_150`–`_158`, full gate,
Event recurring real-browser journeys and manual visual acceptance remain open.
Do not perform irreversible deletion on user data before isolated PostgreSQL
and browser proof at one SHA.

## 2026-10-15 — Review after Event Timeline candidate (`_158` pending PostgreSQL)

The branch reached `_157` with Event/Occurrence non-destructive Timeline
placement reads, removal and Undo, but no fresh same-SHA WSL gate. The latest
new PostgreSQL test file was missing from the registry; it is now registered.
An ownership audit found that `reality_review_policy` has a polymorphic
subject key without a NativeRef FK: the existing hard-deletion graph did not
select it. Forward-only `_158` adds the owned policy roots for Activity, Event
and Event Occurrence, including their FK descendants, and adds the policy's
current revision to recurring/Event deletion preview CAS. Focused PostgreSQL
regressions now check no retained policy, sibling preservation and stale
Event confirmation. Expected topology remains `238|5|244|104|486|421|596`.

Locally the test registry, Python compilation, Ruff and diff check pass.
PostgreSQL 18/PostGIS, generated API drift, the full 27-group gate and real-app
visual checks have **not** run on this candidate. Earlier `4ad30f90` 27/27
evidence does not cover `_150`–`_158`. Do not accept or apply destructive
operations to real user data until the new database graph and concurrency
scenarios pass in the user's isolated WSL fixtures.

## 2026-10-15 — Complete deletion candidate published (implementation; WSL verification required)

**Current forward migration head `20261015_156`**, exact expected catalog
`238 tables | 5 views | 242 functions | 104 triggers | 486 indexes | 421 FKs | 596 checks`.
This checkpoint supplies the previously open product paths in source code:

- `_152` creates owner-checked, fingerprinted, atomically scoped hard deletion
  of one recurring Activity / one Event Occurrence and full Routine/Event series
  (also one-off Event). Durable Occurrence skip prevents single-instance
  regeneration. The scheduler producer holds a matching transaction-level
  source advisory lock through checkpoint and policy materialization.
- `_153` recursively deletes one-off Activity children with a hard shared
  child/depth refusal. `_155` forces recurring Activity deletion to use the
  same safe child-graph code, replacing the original weaker duplicate.
- `_154` adds coordinated non-destructive Activity Timeline unplace and
  historical placement Undo. A private cloned generic Undo function is never
  runtime executable; a restricted SECURITY DEFINER wrapper verifies actor,
  current Session fingerprint, Schedule role and placement lock. Generic Undo
  retains the original Activity interval guard.
- `_156` provides actor-scoped Event Occurrence selection by date/identity.
  Inspector offers `Solo questa istanza`, `Tutta la serie`, and
  `Annulla` without guessing the Event source is the selected Occurrence.
- API routes: `GET/DELETE /api/v1/temporal/hard-deletion/{ref}` for preview
  and mutation; Activity `timeline-unplace`, `timeline-undo`,
  `timeline-undo-receipts`; Event `deletion-occurrences`.
  Web clients and both Inspector actions now invoke these routes.
- PostgreSQL regressions: `test_temporal_hard_deletion.py`,
  `test_activity_timeline_unplace_undo.py`, and updated Inspector,
  admission guard, migration and exact catalog tests. Existing bare recurring
  Activity DELETE remains fail-closed.

**Evidence policy:** The assistant did not run tests, per the user's explicit
instruction: user runs WSL/Docker/Postgres/Playwright gates. Code is an
**unverified integration candidate**, not a confirmed passing feature or
accepted production migration. The user must run all test groups on one SHA,
and failures must be fixed without weakening tests, DB constraints or security.

**Known experience boundary:** The Event Inspector supports manual explicit
selection from at most 1000 currently materialized Occurrences when the
caller has not supplied the selected `occurrenceRef`. The source Event has
stable identity separate from its Occurrences. The Activity Timeline unplace
form currently rejects an envelope with active child intervals and delegates
multi-interval mutation to the existing replan path. These are deliberate
fail-closed behaviors, not silent deletion.



## 2026-10-15 — Forward-only guarded generated Activity admission and Objective graph repair

Published candidate Alembic heads `20261015_150` and `20261015_151` add two
bounded persistence repairs. `_150` adds the owner-executed
`guard_generated_activity_creation()` BEFORE INSERT trigger on
`activity_create_operation`. Only the reserved
`b14:occurrence-activity:<occurrence_ref>` operation-id namespace gets
the owner/source/skip admission check and lock; ordinary Activity authoring
remains unchanged. It also redefines `bind_self_routine_occurrence_activity`
to refuse deleted/skipped or cross-owner Occurrences and retired/foreign
Activity rows while retaining existing binding replay behavior.

`_151` redefines `delete_self_activity_lifecycle_graph` with an explicit
owner-scoped `temporal_objective` root for Activity hard-deletion; this
polymorphic link has no ordinary FK and was not traversed by the old graph.
Dictionary and exact catalog constants now expect
`238|5|234|104|486|421|596` and Alembic head `20261015_151`.
New PostgreSQL regression `test_recurring_admission_guard.py` verifies
normal Activity admission and skipped-Occurrence rejection with zero orphan
create receipts; the existing `test_activity_inspector.py` now verifies
Objective deletion and other-owner preservation.

**Not verified by the assistant, per user test ownership.** No unit, PostgreSQL,
browser or 27-group test execution is claimed for these commits. More
importantly, these guards DO NOT IMPLEMENT hard deletion of a recurring
Activity instance/full Routine series or Event instance/full Event series,
nor coordinated Timeline unschedule/Undo. Producer materialization still
spans separate transactions; a deletion command must lock both source and
Occurrence and sweep in-flight generated creation receipts, and full graph
closure must cover child Activity identities, Event-specific and non-FK
ownership facets. Do not expose a destructive UI/API on the strength of
these guards alone. The full engineering obligations remain in
`timeline-recurring-deletion-atomicity-audit-2026-10-15.md`.



## 2026-10-15 — Deletion producer/consumer race audit (engineering gate)

The audited `_111` Activity binder does not check `occurrence_skip`, and
`RoutineOccurrenceMaterializationApplication._materialize_activity` commits
Activity creation and final binding in separate transactions. Therefore merely
wrapping `skip_self_occurrence` plus `delete_self_activity_lifecycle_graph`
in one deletion transaction is **not sufficient** for no-resurrection under a
concurrent materialization. The Event model has a different shape: one shared
Event source with individual Occurrences. The checked, concrete architecture,
negative scenarios, and 12 acceptance cases are documented in
`timeline-recurring-deletion-atomicity-audit-2026-10-15.md`.

**Do not activate a destructive API/UI until both producer atomicity and
owner-scoped graph deletion are proven in real PostgreSQL and the real browser.**
No new destructive runtime capability or passing test is claimed by this audit.

## 2026-10-15 — User extends deletion/recurrence parity to Event (normative scope)

The user expressly confirms that Event follows the same single-instance / full-series / cancel hard-deletion semantics as Activity, adapted to Event's own graph (agenda, expected participation/attendance, objectives, reminders, Actual/Outcome/Confirmation). A recurring Event instance is an Occurrence sharing the source Event; deleting one must not delete that source or siblings. A hard-deleted single Occurrence must never rematerialize; deleting the whole series must eliminate the source and every current/future Occurrence. Placement removal and Undo remain NON-DESTRUCTIVE for both kinds, and edit scopes are distinct from hard-deletion scopes. The accepted normative overlay is `docs/domain/decisions/activity-session-operational-lifecycle-v2.md`. These are requirements, **not delivered runtime or passing tests**. Event hard-delete capability, Event UI, and both recurring deletion scopes remain open. Don't reuse Activity-only graph deletion blindly for the Event graph; audit FK descendants/ownership and ensure one protected transaction and fail-closed cross-owner behavior before wiring a destructive action.


## 2026-10-15 — `_149` focused run and current-plan review correction

The user's WSL run on exact `cd3b589` completed **5 PASS / 1 FAIL**. Fresh
Alembic head, Alembic schema drift, the Schedule Undo file and the new direct
Activity interval Undo regression passed. The only failure was the exact
cross-representation test expecting `_148` while the fresh DB correctly had
`_149`. Six catalog tests held that same stale literal; all are corrected in
this candidate, with no test expectation weakened beyond the migration head.

The accepted Session review rule was corrected: a never-started generic/named
Session enters Da verificare only when **every current Activity interval** has
ended. Moving the Activity into the future removes its pending Session rows;
moving it back into the past restores them if no attempt exists. Visibility is
derived from the current owner-scoped plan and factual attempts, not stored
as an immutable missed event. The API/rail candidate shows distinct read-only
rows and refreshes after Activity Save/Delete. Resolution actions are a later
product workflow. Backend unit/integration and Web regression tests were
added; they still need the user-local PostgreSQL/Web/generated-client gate.

## 2026-10-15 — Generic Activity interval Undo guard candidate

Forward-only `_149` prevents the generic Schedule Undo capability from
restoring an interval removed by a coordinated Activity replan. The Python
application and HTTP route reject it, while the directly executable database
function takes the Activity lock and rejects it independently. A PostgreSQL
regression exercises a running Session, attempted application and raw SQL
Undo, and readback of both placement and Session impact. This candidate has
not been tested on PostgreSQL; the earlier 10/10 on `0e848943` is evidence
only for `_148`. The current catalog topology stays `238|5|233|103|486|421|596`.
The review queue, direct Timeline disposition UX, and recurring scope remain
open in the lifecycle matrix.

## 2026-10-14 — Owner TEMP corrective candidate: focused PostgreSQL PASS

The user's WSL run of ten selected PostgreSQL tests on exact source
`0e84894396ecb6692666ce7ecf2475fb16131f04` passed **10/10 in 31.18s**.
This covers the owner-only TEMP grant and denied login-role permissions,
non-broadening provisioning rerun, fresh migration head, bounded deletion
ACL, Dictionary cross-representation, three formerly failing destructive
paths, guarded direct revision and untimed recurring named Session. It does
not cover the full PostgreSQL inventory, full 27-group gate, or browser.
The current lifecycle matrix names the still-missing review queue, direct
Timeline disposition UX and recurring instance/series operation. The older
T08 entry in the Temporal regression matrix has been aligned with the newer
normative Activity/Session lifecycle decision; historical test evidence stays
at its original SHA.

## 2026-10-14 — Lifecycle deletion privilege repair candidate

The user's focused PostgreSQL run on `a4a5a15` executed all eight selected
tests: **5 passed, 3 failed**. Hard Activity deletion, editor Delete Sessions,
and named X all failed at the same owner-executed graph function because
`dante_owner` had no database `TEMPORARY` permission. This candidate grants
TEMP only to the NOLOGIN owner in explicit administrative provisioning, keeps
all login roles denied, verifies the grant and an actual owner temp table in
`test_privileges.py`, and records the required provisioning rerun for existing
databases. The migration head remains `_148`; no applied migration was edited.
Local Ruff/format, targeted mypy, 37 settings tests, test registry and diff
checks passed. PostgreSQL and real browser are unavailable in this workspace;
the destructive scenarios and complete gate remain unverified on this SHA.
The never-started review queue, direct Timeline mutation UX and recurring
instance/series behavior remain open in the lifecycle matrix.

## 2026-10-14 — Second static repair checkpoint (PostgreSQL rerun pending)

After the first published checkpoint (`bb6a9725`, tree `af2f90be`), a second focused backend pass reduced mypy diagnostics from **118 to 26** over `src tests`. It replaces test-only pseudo-contexts with real request/context contracts, checks nullable SQL rows and optional application reads, narrows response variants, and validates the Plan diagnosis and Recurrence response payloads through their declared Pydantic models. The latter two API paths still require the full PostgreSQL/real-stack proof. Ruff and Python formatting pass; focused non-PostgreSQL recurrence, Plan diagnosis, constraint boundary and execution-assessment tests passed (**7 tests**), and Quick Create API tests passed (**6 tests**). ESLint is still **RED: 140 errors** on the first checkpoint; no second-pass Web changes were made.

This is saved progress, **not a passing full gate**. On the final published SHA rerun the focused PostgreSQL tests under `apps/backend/tests/integration/temporal/` for the changed files, then the failing `BACKEND_MYPY` and `REPO_ESLINT` groups. Mypy still has 26 concrete diagnostics, so a complete 27-group run will remain red until those and ESLint are repaired. Preserve the 84 passed / 3 skipped browser evidence on `23545137` as historical evidence, not as a claim about this SHA.

## 2026-10-14 — Focused repair following `23545137` WSL browser evidence

The user's WSL rerun on `23545137` reports **WEB_BROWSER_NONAUTH: 1 passed** for the formerly failing scenario and **WEB_BROWSER_REAL_STACK: 84 passed, 3 skipped**. This closes those two browser failures on that SHA, not the full 27-group gate. Keep the 3 skipped cases visible in the suite report.

This follow-up repairs existing typing and lint diagnostics without disabling either gate. Backend tests now use real Activity edit, request/context and Plan application contracts, assert nullable API outcomes explicitly, and type Plan search arguments. Web fetch tests now require an actual URL or serialized JSON body instead of coercing unknown input with `String`; DOM tests assert actual element classes before reading their properties. Two production API readers validate string fields rather than coercing arbitrary JSON. Async Create runtime stubs retain their Promise contract with explicit `Promise.resolve` / `Promise.reject`. Locally measured diagnostic counts: **mypy 219 → 118** (`src tests`), **ESLint 295 → 140**; both gates remain **RED**. No old test was deleted or marked passing by changing its expected behavior.

Local verification of the follow-up: Python Ruff and format pass; Web typecheck, Prettier, architecture and Vitest (**225 files, 1055 tests**) pass; test integrity reports `REGISTERED=491 DISCOVERED=491` (all 491 still UNREVIEWED). Backend non-PostgreSQL has 626 passed and two local failures caused by an injected SOCKS proxy with no `socksio`; those exact two pass after removing proxy environment variables. This is an environment-specific local result, not a full gate PASS. The changed PostgreSQL tests require focused execution on WSL with Docker, and the complete 27-group gate must run on the final published SHA. Do not infer its outcome from focused or historical runs. Remaining ESLint errors are concentrated in synchronous async mocks (59), unsafe typing (45), and React hook rules (24); remaining mypy errors include PostgreSQL integration fixtures and API type boundaries. See the gate logs for individual diagnostics.

## 2026-10-14 — Repair candidate after full gate at `6c9d421`

The uploaded full WSL gate ran all 27 groups on `6c9d421`: 22 passed and five failed (`BACKEND_MYPY`, `REPO_FORMAT`, `REPO_ESLINT`, `WEB_BROWSER_NONAUTH`, `WEB_BROWSER_REAL_STACK`). Both browser failures share a Create start/end interaction: editing the start can temporarily roll the old end clock to the following day; later editing the end clock did not restore the same-day date. A focused component regression was red before the fix and now passes. Authenticated Event scenarios now enter an explicit 30-minute end through the current segmented control, while preserving canonical POST/readback assertions. The two Prettier failures have been formatted. Type and input-shape corrections reduced the observed mypy error count from 240 to 219, but this group remains red; ESLint also remains red (295 errors and three warnings in the current local rerun). Do not claim either browser group green until rerun in WSL against the candidate SHA. Locally checked: Web typecheck, 29 Create Vitest cases, five Activity replan unit cases, Python Ruff on changed backend, structural test registry and full Prettier. The local environment has no Docker or installed Playwright browsers, so PostgreSQL and browser proofs remain WSL-only.

Run only the five previously failing groups against the published SHA before another complete 27-group gate; treat any newly exposed functional failure as a real defect, not a test to retire without contract review.

## 2026-10-13 — Resource-aware full-gate scheduling (not WSL benchmarked)

The latest *measured* complete WSL run at `6476a5c1` took **1713.3s** (28m33s): PostgreSQL **392.5s**, browser non-auth **395.5s**, browser real-stack **918.6s**, browser session fixture **6.5s**. Non-auth and real-stack Playwright were serialized after PostgreSQL, leaving long idle CPU capacity. The real-stack suite intentionally stops/restarts PostgreSQL in auth and timeline recovery proofs, so blindly raising its single Playwright worker count is unsafe.

Opt-in `tooling/testing/run_parallel_gate.py` now runs PostgreSQL as **3 bounded Docker containers and 3 duration-balanced queued work items per worker by default**, with work stealing once any pytest subprocess finishes. Observed module timings are collected from `pytest --durations=0`, stored only in ignored `temp/POSTGRES_MODULE_TIMINGS.json`, and used to distribute the next run without splitting module fixture boundaries. Group timing history likewise starts heavy independent checks earlier; per-shard wall-times and longest-group summary are retained in the test archive. The fixture and non-auth browser runs stay serialized relative to each other but start before PostgreSQL finishes; non-auth Chromium has **3 independent workers** only in the opt-in parallel runner (ordinary Playwright config stays 1). Real-stack continues serial **after** PostgreSQL finishes, preserving destructive isolation. No original tests, acceptance gates or retries on functional failures were removed.

Commands from a clean checked-out branch: `python3 tooling/testing/run_parallel_gate.py --self-test`, `--dry-run`, then `python3 tooling/testing/run_parallel_gate.py --group-workers 5 --postgres-workers 3 --postgres-jobs-per-worker 3 --nonauth-workers 3`. The authoritative sequential reference is unchanged. **This candidate is not performance-verified in user WSL and not a passing 27-group result.** Measure one full same-SHA run and compare exact group durations before increasing a resource budget.


## 2026-10-13 — B01/B03 live browser contract repairs

The real-stack B01 browser scenario now creates a canonical *unplaced* Activity using the authenticated U2 `/authoring/activities` API with `placement: null`, rather than asking retired Quick Create to produce an unplaced item. It verifies accepted response, PostgreSQL readback, legacy existing-items management, isolation from the inert Draft Vault, reload and user-discarded draft isolation. This is an explicit API-plus-browser journey, **not** a claim that Quick supports unplaced authoring.

The B03 Event browser journey now waits for `/authoring/events`, verifies and unwraps the *real nested* accepted Schedule (without inventing identities), drives the current visible calendar widget and segmented time control, selects the original floating-local placement mode explicitly, and tests future dates to avoid already-past authoring. The future date is also routed into the viewed Timeline. The original acceptance assertions for schedule edit, all-day/multiday spans and reload remain in place. A fresh execution is required to learn whether other B03 behavior or test assumptions still fail.

Latest patchwork remains **UNVERIFIED**, not a new full gate; quality groups and additional real-stack journeys have known red evidence. The source changes are intended to let the owner resume B14 with targeted acceptance; do not claim all tests pass or B14 is complete.


## 2026-10-13 — Real-stack Create endpoint correction

The auth/browser B00 Event Create test has been updated to await the **current U2** `POST /api/v1/temporal/authoring/events` endpoint rather than the retired `/events/scheduled` endpoint, and to assert the actual nested `schedule.schedule_ref` from the accepted mutation. It sets time through the visible segmented editor and verifies the routed date through the controlled date picker instead of `.fill()` on hidden transport inputs. This was a concrete stale-test timeout cause, **not** evidence the full-stack journey now passes. The B01 canonical unplaced-Activity suite still uses the removed Quick unplaced path and must be rewritten around the explicit preexisting-items management API without confusing canonical records and inert Draft Vault records. Real-stack and browser acceptance remain pending WSL/Docker execution. A separate authoring type-guard change preserves rejection of non-timed Activity intervals while narrowing both the runtime and mypy contracts.


## 2026-10-13 — B14 gate repair continuation (GitHub candidate, unverified)

Current repair series after the previous `ff7cc98b` handoff includes narrow backend typing corrections for the elapsed/weekly recurrence and Activity authoring, and browser fixture scenario migrations for the new Life Area color/selector, rail-bound pinnable Create, root planned Session/capture, calendar recurrence, and the inert Draft Vault (replacing the retired "Da collocare" workflow in the non-auth UI harness). Draft Vault fixture tests explicitly stub only the HTTP contract; durable PostgreSQL behavior remains owned by auth/real-stack tests and is not proved here. The Home Timeline gesture bridge now avoids mutating the new aria-hidden date/time transport inputs after the controlled reseed, with an additional colocated regression.

This is **source repair only**. Neither the edited browser files nor the amended backend types were executed locally in the user's WSL; their result is UNKNOWN until typecheck/Vitest/Playwright/PostgreSQL probes run on this exact SHA. The user's previous 27-group gate on `6476a5c1` remains RED and should not be relabeled. In particular, `temporal-create-planning-tray.spec.ts` has a new mock HTTP contract that must pass real Chromium fixture execution; the old drag cases belonged to retired canonical unplaced authoring and cannot be claimed as Draft Vault coverage. The `_143` data-bearing migration path, current full-stack Create responses, historical Activity truth policy, and substantial Ruff/mypy/ESLint/format debt remain open. **B14 is not closed.**


## 2026-10-13 — Controlled Create reseed repair after the full gate

Live GitHub branch verification at `0450f539` showed six commits beyond the user's 27-group gate SHA `6476a5c1`; those candidates correct the focused objective/Dictionary assertions and parts of Web Create/browser/runner but have no new full gate proof. A subsequent repair series `370ec14c` → `21ee0493` → `00fb2e3f` → `d0d6fbf5` addresses the actual Home Timeline reseed mismatch: the interaction bridge previously writes DOM values into native date/time inputs, while Create now owns a controlled button-based date picker. The bridge now emits a bounded date/time reseed event to the mounted composer; the Create entry applies it to React state and resets draft validation through the canonical field update; the earlier native-input route remains available to embedded/legacy consumers. An existing UI test file now asserts the reseed contract. **Not verified on the user's WSL/Web browser or accepted as a full gate PASS.** The original non-auth browser failures, real-stack timeouts, format/lint/mypy debt, and the historical `_143` forward upgrade risk remain open. Do not run another costly full gate expecting green until these are addressed and the focused current-source tests pass.


## 2026-10-13 — Full parallel gate on cdad6bb2; repair candidate

**Focused follow-up on `6c3975ba`: 6 PostgreSQL tests passed in 18.00s**
on the user's WSL, covering `_145` migration drift/current catalog, relative
Recurrence anchors and advanced/conditional Recurrence journeys. The new
catalog test needed `SET ROLE dante_owner`, consistent with the schema ACL.
This is not a full PostgreSQL or full 27-group gate. Existing formatting,
lint, typing and browser failures remain open; avoid another complete run
until those known red groups have been repaired. Exact evidence is in the
full-gate baseline report.

The user's 27-group WSL gate completed with 19 PASS / 8 FAIL. Of 40 PostgreSQL jobs, 34 passed, three reported functional/catalog failures and three failed during Docker startup or cleanup. `_144` made relative elapsed Recurrence anchors non-null despite the earlier B11-A conditional CHECK; the new forward-only `_145` restores nullable columns and aligns two occurrence-policy indexes with the ORM/Dictionary. Browser API tests now send the required time-zone header, recovery URL tests honor the dynamic harness port, and quick Create portals outside the hidden Context Rail on narrow screens, including live viewport changes. Focused component and Web typecheck pass locally; PostgreSQL and browser full-stack acceptance **have not run on this candidate**. The historical `_143`-with-NULL upgrade path across `_144` remains unresolved, as do substantial formatting/lint/type debt and outdated Create browser journeys. See `docs/development/full-gate-baseline-2026-10-12.md` for exact failure evidence. Do not declare the gate green or merge.

## 2026-10-12 — User real-app regression report; focused repair candidate

Six screenshots show an Activity edit with a new quantity Objective whose numeric target is blank, a recurring Create with two Activity intervals and an untimed named planned Session rejected by an explicit frontend guard, missing Play after changing the Activity's capture toggle, a real Session card drawn below its displayed minute, and Timeline scroll that cannot return upward. Source repair candidate: validate/focus numeric Objective **before any partial edit writes**; invalidate and refresh the mounted card on accepted capture-policy save; preserve root untimed planned Session in recurring template and materialize it as an unplaced canonical Schedule (no invented time); snap real card geometry to the same displayed minute; only treat a changed route prop as external date navigation, breaking the scroll feedback loop. One frontend scroll regression test and recurring template/card tests pass with local Web typecheck and 30 focused Vitest tests; Python syntax only so far, PostgreSQL still requires the user's local targeted gate `tooling/verify-b14-oct12-regressions-local.sh`. Existing real-app visual behavior needs renewed acceptance.

**Separate open capability:** the `Ripeti · Mai` row in Edit is currently read-only for a one-off Activity. Converting an existing Activity into a recurring Routine needs an owner/CAS operation that links the first instance and safely captures the current planning/Objective template. Do not create a duplicate Activity or pretend the Create recurrence form can mutate this identity. This is still unimplemented and must be designed and verified as an end-to-end backend/UI block. Quantity Objectives continue to require a numeric target; the screenshot with `mele` and no value is invalid by design, but the editor now places the user at that field and shows the reason.

## 2026-10-11 — Generated API client published

User pushed the two WSL-generated API files (`packages/api-client/openapi/dante-v1.openapi.json` and `packages/api-client/src/generated/dante.ts`) in `72735407` after pulling the `_142` technical gate documentation. The GitHub branch readback confirms this head. Technical gate and generated client publication are complete. Next is real-app acceptance for Activity/main and planned Session Play, card width/actual time after Start/Stop, non-overlap, and past Activity/Objective review. Historical execution lock, correction/retraction and past authoring rules remain open product work; do not declare B14/B15 closed based on technical tests alone.

## 2026-10-11 — `_142` local technical gate verified; real-app acceptance open

User pulled `f497cb0b` and ran `test_current_database_cross_representation_is_exact` on PostgreSQL: **1 passed in 24.59s**. This closes the one red check from the preceding complete gate (`19 passed, 1 failed` before the stale stage-literal correction); that gate's PY_SYNTAX, RUFF, PY_UNIT, OpenAPI generation/determinism, API/Web typecheck, Web lint, Vitest and browser checks were green. The evidence is cumulative across two consecutive commits, not a single full rerun or visual acceptance. `_142` and the exact catalog are now user-locally verified; the two generated API files remain uncommitted in the user's WSL worktree, while card Play/width/actual-time and past review still need real-app acceptance. Do not repeat the technical gate or use the older October 4 snapshot in place of current generated files. Historical edit locks/correction policy remain open.

## 2026-10-11 — User-local `_142` gate and catalog assertion repair

User WSL gate after `1df81099` reports `19 passed, 1 failed` in PostgreSQL: only `test_current_database_cross_representation_is_exact` is red; PY_SYNTAX, RUFF, PY_UNIT, OpenAPI generation/determinism, API/Web typecheck, Web lint, Vitest and browser are green. The provided output contains the summary and migration log, not the assertion traceback. Static reconciliation found that `scope.json` includes `B14-PAST-ACTIVITY-REVIEW` but this exact-catalog test's completed-stage literal omitted it. The other current catalog test and functional PostgreSQL tests passed. Add the missing stage to that literal only; verify this specific test on the user's PostgreSQL before declaring the `_142` catalog gate green. Preserve the two user-local generated API files and do not rerun generation or the prior green gates. Real-app behavior remains unaccepted.

## Active handoff 2026-10-11 — regression repair candidate

User real-app screenshots after the prior patch show Play missing on some Activity cards, card widths jumping on Play, and stale planned time/undersized cards after Stop. The preceding “follow-up candidate” paragraph below is superseded as UX evidence. Current local edits rebuild the day time mapper from projected real Session bounds, recompute all card lanes/offsets, use card-associated Session refs for inline Play, and render actual time with planned time as context. `_142` extends the owner-only queue to unanswered past Activity plans and Objectives, with explicit Reality policy for never-started review; neither a missed Session nor a missed Objective is auto-marked complete. Web typecheck/focused Vitest and Ruff passed in assistant workspace. The new migration/integration test and visual behavior await user-local PostgreSQL/browser proof; no B14/B15 closure. Historical locking/correction scope remains a proposal.

## 2026-10-11 — Collision/Stop follow-up candidate

Current branch candidate after `_141`: Web layout lanes use final visible pixel rectangles and actual Session bounds; Session desk uses concluded planned Schedule identity rather than a five-minute time overlap; inline Session controls remove implicit Play after Stop. Focused workspace: 16 Python Session panel unit tests, 25 Vitest tests across four files, Web typecheck and Ruff pass. This does not prove the browser view or PostgreSQL repeat-start authority. Main attempts across multiple intervals currently have no explicit Session→interval link and use nearest-start association for the desk. Direct API can still create a distinct subsequent attempt; no authoritative historical lock, correction/retraction ledger or past Event/Activity authoring change has been made. User product alignment on scope and metadata remains open in `timeline-session-history-protection-and-past-authoring-proposal-2026-10-11.md`. One affected user-local gate and real-app check are needed after publication; no CI.

## USER REAL-APP FINDINGS 2026-10-11 — Session history protection / past editing

Following local `_141` technical gate and generated client publication, user screenshot exposed: visually overlapping/shifted Activity cards (actual geometry applied after collision layout), a concluded early Session e.g. 09:49–09:51 attached to a 10:00–10:30 planned card, and Play returning after Stop. Source review confirms both a window-overlap-only stopped-attempt check in `session_panel_api.py` and independent inline controls that re-enable Play whenever there is no open Session. Current `activity_replan_api.py` broadly rejects only **open Sessions or accepted Actual**, leaving an ended Session without an Actual insufficiently guarded.

User requests cross-entrypoint lock after Start/recording, explicit historical correction/retraction rather than accidental Activity deletion, and explicit past Event/Activity authoring. **All these additional semantics are PRODUCT PROPOSAL / NOT IMPLEMENTED** until scope is agreed; see `docs/workstreams/timeline-session-history-protection-and-past-authoring-proposal-2026-10-11.md`. Recommended lock scope is the **executed Activity interval/Occurrence**, not unrelated future intervals; separate planned intent, real Session and verified Actual. Do not claim B14 UX accepted from earlier green technical gates. Continue with user decision, then implement one coherent source/DB/test block; no CI and no migration rewriting.

## ARCHITECTURE/BLUEPRINT ALIGNMENT — 2026-10-11

After the user's question about DB/Blueprint synchronization, the branch's existing `_135`–`_141` chain was read back and confirmed linear from `_134`. The user-local catalog is already verified at `238|5|228|103|486|421|596`; the 14 generated API files were pushed at `a9a8353a`. No DB/Alembic changes are part of this audit. Active status pointers in `docs/PROJECT-STATUS.md`, `docs/ROADMAP.md`, `docs/physical-model/README.md`, `docs/logical-model/README.md`, `docs/database/README.md` and `docs/database/dictionary/README.md` now identify the real candidate and explicitly qualify old B06/B08/_57/_86 headings as historical. New additive Logical and Physical overlays `docs/logical-model/slices/b14-session-objective-home-workspace-2026-10-11.md` and `docs/physical-model/b14-session-objective-home-workspace-2026-10-11.md` bridge the Domain-approved independent Session and persistent Objective draft semantics to forward migrations and owner-only routines. The separate `dante-ai-05b` blueprint is an **AI workstream** design and does not claim to be the Timeline database blueprint; leave it unchanged. Target Physical PM-12 and Whole Logical snapshots also remain immutable. The **only remaining B14 gate** is real-app Home UI acceptance; do not substitute documentation alignment for UX PASS.

## CURRENT VERIFIED FRONTIER — B14 live Session + Home workspace (2026-10-10)

**Technical gate GREEN for source through `b71bf532` / Alembic `20261010_141`, based on successive user-executed WSL checks; real-app visual/product acceptance remains OPEN.** The initial full gate passed PY_SYNTAX, PY_UNIT, GENERATE, GENERATED_CHECK, API_TYPECHECK, VITEST and BROWSER. The first repair completed **14 functional PostgreSQL tests**. The subsequent targeted repair passed RUFF, WEB_TYPECHECK, WEB_LINT and VITEST_CHANGED, plus **7 of 8 PostgreSQL catalog checks**. The sole remaining `test_current_database_cross_representation_is_exact` was corrected to the live exact topology and the user then ran it: **1 passed in 6.75s**. Current catalog topology is **238 tables | 5 views | 228 routines | 103 triggers | 486 indexes | 421 foreign keys | 596 CHECK**. These are cumulative local evidence, **not a fresh full-suite rerun on one commit**, and GitHub CI was not used.

**API ARTIFACTS PUBLISHED:** user committed and pushed all **14 generated OpenAPI/Orval files** (3 modified, 11 new; 1,419 insertions) to this branch in commit **`a9a8353a`**, with `[skip ci]`; the reported worktree is clean. No regeneration, CI or further automatic gates are needed for unchanged source. **IMMEDIATE NEXT:** start the usual authorized local app stack with `export DANTE_E2E_CONTROL_ID=temporal-b08-d-usertest` and `uv run --project apps/backend python tooling/run-access-auth-stack.py`, then manually accept: independent planned child Play with main disabled, main Pause/Stop cascade and independent child Resume, five-minute Session desk/right-edge placement, Stop retiring operational rows, three Home rail tabs, bounded truthful Conclusi/Da verificare, persistent Objective draft and explicit ✓ Conferma both in Home and Inspector, mobile behavior. **Do not close B14/B15 until the actual app is accepted.** All older red-gate paragraphs below are dated historical diagnostic evidence, not current action items.

## B14 WORKSPACE — ultimo gate locale e fix catalogo (2026-10-10)

**Stato: una sola verifica PostgreSQL ancora aperta.** Ultimo gate WSL sul commit `6612db6b`: `RUFF=0`, `WEB_TYPECHECK=0`, `WEB_LINT=0`, `VITEST_CHANGED=0`; `POSTGRES_CATALOG=1` con **7 passed, 1 failed**. Il test `test_current_database_cross_representation_is_exact` conteneva ancora tre literal obsoleti per `scope.json`: `physical_indexes=484`, `foreign_keys=420`, `check_constraints=593`. Il catalogo migrato e lo scope corrente concordano invece su **486/421/596**, con topology `238|5|228|103|486|421|596|0|0|0`. Il test ora verifica tutti e tre i numeri effettivi e non modifica schema né migrazioni. **Fix pubblicato, verifica ancora NON eseguita dall'utente.** Ripetere soltanto `cd apps/backend && uv run --locked pytest -q --no-cov -m postgres tests/integration/database/test_database_current_catalog.py::test_current_database_cross_representation_is_exact` dopo `git pull --ff-only origin feature/timeline-temporal-operational`. Tutti gli altri gate precedentemente verdi vanno conservati, non ripetuti. Conservare i **14 artefatti OpenAPI/Orval locali** fino al gate verde; successivamente pubblicarli, poi accettazione UI reale di Sessioni interne, tre viste e conferma Obiettivi. Niente CI/reset/clean.

## LATEST B14 WORKSPACE REPAIR EVIDENCE — user-local 2026-10-10 21:45 +02

The user's second targeted WSL repair gate at prior head `2552cb64` reported **RUFF=1, POSTGRES=1 (14 passed/2 failed), WEB_TYPECHECK=2, WEB_LINT=1, VITEST_CHANGED=1**. Both PostgreSQL failures were *only* exact database catalog assertions expecting **485** indexes where live PostgreSQL has **486**: the new `temporal_objective_input_draft` has **one primary-key index plus one owner lookup index**. The functional PostgreSQL suite (including staged/confirmed Objectives, owner isolation, independent planned Sessions and ended history) had **14 passes**. Web typecheck/Vitest were blocked by a stray closing parenthesis in `objective-controls.test.tsx`; ESLint found unsafe `String(assessment)`; Ruff found one `B023` closure capture and a blank line.

**Corrections have been saved to the same branch**: pass Activity identity explicitly into the stopped-session helper; normalize Ruff spacing; remove the extra test parenthesis; narrow the Objective draft parser's assessment type checks; reconcile Dictionary scope, catalog assertion, and current DB/roadmap/map/handoff text to **238|5|228|103|486|421|596**. The remaining user-local gate script `tooling/verify-b14-session-home-workspace-repair-local.sh` now runs the *catalog-only* PostgreSQL tests plus Ruff, Web typecheck, Web lint and changed Vitest, preserving the already green 14 functional PostgreSQL cases, API generation/check/client typecheck and browser. **These newest commits have not been user-locally verified yet.** Preserve all generated OpenAPI/Orval artifacts, no CI, reset, clean, or further API generation before green.

## IMMEDIATE NEXT — first B14 workspace gate red, targeted fixes published (2026-10-10)

User output `Markdown incollato(20261010-182246).md`: `PY_SYNTAX=0 RUFF=1 PY_UNIT=0 POSTGRES=1 GENERATE=0 GENERATED_CHECK=0 API_TYPECHECK=0 WEB_TYPECHECK=2 WEB_LINT=1 VITEST=0 BROWSER=0`. PostgreSQL was blocked while applying `_139` because psycopg3 parsed `%ROWTYPE` in raw exec_driver_sql as a placeholder (`got '%R'`). Error propagated into 16 fixtures. Fixed `_139` raw driver escaping (unapplied failed candidate), Ruff import order and unused import, TS union index, ESLint mocks and unsafe String(input), React effect/memoization, decimal payload validation. **Not yet rerun or proven green.** A new **repair-only** gate was published: `tooling/verify-b14-session-home-workspace-repair-local.sh`; user should `git pull --ff-only origin feature/timeline-temporal-operational` and run it once, send summary and red logs only. Generated API artifacts from the user's WSL (modified OpenAPI/client/index and new Objective/Home models) must be preserved uncommitted; do not generate again, clean, reset or push before confirmation. B14/B15 acceptance remains open. If PostgreSQL progresses past `_139` and reveals `_140`/`_141` issues, fix those specifically, then repeat only needed red checks.

## CURRENT HANDOFF — B14 three-view workspace and independent planned Session (2026-10-10)

**Branch:** feature/timeline-temporal-operational; current source Alembic **20261010_141**; expected exact catalog **238|5|228|103|486|421|596**. User approved all features 2026-10-10: explicit internal planned Sessions execute without requiring a generic main Activity Session; main Pause/Stop still cascades when enabled; Home right rail has Conclusi, Da verificare, Obiettivi; durable provisional Objective inputs survive reload and produce canonical Observations only on ✓ Conferma, equally in Inspector and rail. Implemented: _139 staged Objective PostgreSQL table/functions, _140 bounded finished history and pending Objective work reads, _141 trusted owner-only planned start; current API, shared UI, Dictionary/SQLAlchemy and tests. B10 review queue remains policy-scoped. No automatic failed/completed inference from elapsed Schedule. **Status: UNVERIFIED candidate**. Prior 7/7 green gate at _138 is not this candidate proof. **IMMEDIATE NEXT:** user does one git pull --ff-only origin feature/timeline-temporal-operational and runs bash tooling/verify-b14-session-home-workspace-local.sh. Preserve Orval generated artifacts and publish them only after green. No CI, reset or clean. Real-app walkthrough through existing run-access-auth-stack.py remains open, as do other historical Bozze/M5 acceptances.

## CURRENT REAL-APP HANDOFF — 2026-10-10 (user screenshot follow-up)

The user exercised DANTE after the previously confirmed 7/7 technical gate. Source-visible defects: popup positioned relative to toolbar icon; after Stop the UI/BFF reproposed the ended planned row; parent-only capture policy hides child planned Sessions if Activity capture is disabled. The `Da verificare` rail currently intentionally shows only three B10 work reasons; Stop alone is not guaranteed to generate review. **New GitHub commits save** the inner-right panel host and Stop lifecycle correction, with unit/PG/React/Playwright regressions; these follow-up commits **have not yet passed the user-local gate**. Next: user pulls feature branch then runs `bash tooling/verify-b14-session-desk-realapp-fixes-local.sh` (no CI, no OpenAPI regeneration), report only red checks. Keep 7/7 prior green proof separate.

**Product decisions open, not implemented:** make child Session work independently from optional main capture in a *correct explicit canonical policy*, decide whether inactivity becomes governed review or remains unknown, define bounded `Conclusi` history, separate `Obiettivi` view and persisted provisional vs local staging before `Conferma` in Inspector + Context Rail. See `docs/workstreams/timeline-context-rail-three-views-proposal-2026-10-10.md`. Maintain Schedule≠real Session, no automatic completed Activity or Objective from Stop. Do not hide remaining work or imply B14/B15 closure.

## CURRENT HANDOFF — 2026-10-10 / live Activity Session execution

**Source branch/head proven by user:** `feature/timeline-temporal-operational` at `8097918d`, Alembic `20261010_138`. **Targeted repair gate GREEN, 7/7 checks:** PY_SYNTAX=0, RUFF=0, POSTGRES=0, WEB_TYPECHECK=0, WEB_LINT=0, VITEST=0, BROWSER=0; first full-gate nonfailed checks (PY_UNIT, GENERATE, GENERATED_CHECK, API_TYPECHECK) were already PASS. Evidence: `docs/workstreams/timeline-session-live-local-gate-2026-10-10.md`; user WSL log directory `/tmp/dante-session-live-repair.aEjb42`. The new panel previews precise starts by 5 minutes, controls main and internal Session executions, cascades main Pause/Stop atomically, resumes children only on their own Play, and preserves Schedule while one Timeline card projects actual elapsed/paused ranges.

**IMMEDIATE NEXT:** the user has seven uncommitted locally generated `packages/api-client` files, not yet visible to GitHub; publish **only** these seven with `[skip ci]` after pulling documentation-only remote commits. Never reset/clean or re-run generation to do this. Following publication, start their usual `run-access-auth-stack.py` and conduct real-app user acceptance (including mobile/overlaps/time moves); technical gate green does not close B14/B15. Do not repeat the passing PostgreSQL, Vitest, typecheck and browser checks for unchanged code. Existing Event canonical Move-to-Bozze parity and earlier unaccepted M5/Bozze real-app checks remain separate and open.

- **Status:** HISTORICAL HANDOFF checkpoint (2026-10-03) — B12 CLOSED / QUALIFIED USER ACCEPTANCE — B14+B07 active as one user-guided product/UI cycle; U1 Create-entry candidate awaits user visual proof; affected B12-D rerun unreported
- **U6 continuation:** `_102` structure and the B08 Session minimum combination have focused user-run PostgreSQL proof; the combined gate and real-app walkthrough remain open. Read `timeline-temporal-operational-b14-u6-candidate-2026-10-02.md` and the approved U6 gate before work.
- **Activity interval candidate:** `_106` introduces a separate Activity `interval` role, preserves future planned Session `planned` rows, and projects each accepted interval as a distinct card. Read `docs/domain/decisions/activity-intervals-and-sessions-v2.md`; local migration/build/visual acceptance and coordinated interval editing remain open. No proof claimed.
- **Reconciled:** 2026-10-03 (U6 continuation; historical sections retain their dated checkpoints)
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B13-A gate authority:** `docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md`
- **B13-A implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-a-implementation-2026-09-28.md`
- **B13-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-a-closure-2026-09-28.md`
- **B11 closure evidence:** `docs/workstreams/timeline-temporal-operational-b11-closure-2026-09-28.md`
- **B13-B approved scope:** `docs/workstreams/timeline-temporal-operational-b13-b-scope-2026-09-28.md`
- **B13-B candidate checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-b-implementation-2026-09-28.md`
- **B13-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-b-closure-2026-09-29.md`
- **B13-C scope:** `docs/workstreams/timeline-temporal-operational-b13-c-scope-2026-09-29.md`
- **B13-C implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b13-c-implementation-2026-09-29.md`
- **B13-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-c-closure-2026-09-29.md`
- **B12 block scope:** `docs/workstreams/timeline-temporal-operational-b12-scope-2026-09-29.md`
- **B12-A scope proposal:** `docs/workstreams/timeline-temporal-operational-b12-a-scope-2026-09-29.md`
- **B12-A closure:** `docs/workstreams/timeline-temporal-operational-b12-a-closure-2026-09-29.md`
- **B12-B scope proposal:** `docs/workstreams/timeline-temporal-operational-b12-b-scope-2026-09-29.md`
- **B12-B closure:** `docs/workstreams/timeline-temporal-operational-b12-b-closure-2026-09-29.md`
- **B12-C approved scope:** `docs/workstreams/timeline-temporal-operational-b12-c-scope-2026-09-29.md`
- **B12-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b12-c-closure-2026-09-29.md`
- **B12-D approved scope:** `docs/workstreams/timeline-temporal-operational-b12-d-scope-2026-09-29.md`
- **B12-D implementation checkpoint:** `docs/workstreams/timeline-temporal-operational-b12-d-implementation-2026-09-29.md`
- **B12-D local gate:** `docs/workstreams/timeline-temporal-operational-b12-d-gate-2026-09-29.md`
- **B12 closure:** `docs/workstreams/timeline-temporal-operational-b12-closure-2026-09-30.md`
- **B14/B07 working ledger:** `docs/workstreams/timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`
- **B13-D scope:** `docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md`
- **B13-D candidate gate:** `docs/workstreams/timeline-temporal-operational-b13-d-gate-2026-09-29.md`
- **B13-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current migration source head:** Alembic `20261005_106` (Activity intervals branch candidate, not locally proved)
- **Historical focused catalog topology:** `_93` / `196|5|155|100|397|344|497|0|0|0`; current Dictionary materialization is in `docs/database/dictionary/scope.json` and `_106` proof is pending.
- **B11 real-app acceptance:** USER-REPORTED PASS 2026-09-28
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset. Repository HEAD remains the source of truth; re-fetch it before any write.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
B10     ✅ CLOSED 2026-09-26
  B10-A ✅ CLOSED / PROVEN 2026-09-25
  B10-B ✅ CLOSED / PROVEN 2026-09-25
  B10-C ✅ CLOSED / PROVEN 2026-09-26
  B10-D ✅ CLOSED / PROVEN 2026-09-26
  B10-E ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-26
B11     ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-28
  B11-A ✅ CLOSED / PROVEN
  B11-B ✅ CLOSED / PROVEN
  B11-C ✅ CLOSED / PROVEN
  B11-D ✅ CLOSED / PROVEN
B13     ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-29
  B13-A ✅ CLOSED / PROVEN 2026-09-28
  B13-B ✅ CLOSED / PROVEN 2026-09-29
  B13-C ✅ CLOSED / PROVEN 2026-09-29
  B13-D ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-29
B12     ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
  B12-A ✅ CLOSED / PROVEN 2026-09-29
  B12-B ✅ CLOSED / PROVEN 2026-09-29
  B12-C ✅ CLOSED / PROVEN 2026-09-29
  B12-D ✅ CLOSED / QUALIFIED USER ACCEPTANCE 2026-09-30
B14+B07 ◐ ACTIVE — USER-GUIDED PRODUCT / UI CONSOLIDATION
B15     ⬜ NOT STARTED
```

Execution order:

```text
B09 → B10 → B11 → B13-A → B13-B → B13-C → B13-D → B12 → B14+B07 → B15
```

---

# 2. Permanent semantic boundaries

```text
Person != Account != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Outcome != Observation
Outcome != lifecycle / operational state
Confirmation != Authority != Verification
Confirmation != Decision / Approval
Reconciliation != universal truth
Reconciliation != Confirmation != Outcome
Resolution != deletion / rewrite of prior evidence
Responsibility != Participation
planned/intended != happened
Plan != Activity
Step != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
projection != canonical truth
current accepted state != latest row
MaterialState != mutable runtime object
idempotency key != Domain identity
Undo != history rewind
```

PostgreSQL is canonical authority. API, generated client, frontend, provider, solver and AI are projections/capabilities and may not create a second truth model.

---

# 3. Closed B10 chain

## B10-A — Actual

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence
current accepted realization != latest row
```

## B10-B — Outcome

```text
Alembic  20260925_78
Topology 163|5|119|93|317|268|440
facet: outcome.disposition
one stable Outcome per Actual
Outcome disposition pinned to exact Actual realization MaterialState
```

Never reintroduce the superseded `_75` vocabulary/result identity model.

## B10-C — Confirmation

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
facet: confirmation.attestation
identity = (Outcome disposition MaterialState, confirmer Person, purpose)
```

```text
Confirmation != Outcome
Confirmation != Authority / Verification / Decision
absence of Confirmation != false
Outcome correction does not transfer Confirmation
```

## B10-D — Reconciliation

Canonical identity:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

Authority boundary:

```text
Outcome owner is the only resolver in B10-D
can confirm != can resolve
resolver identity is state data, not reconciliation identity
```

Persistence frontier:

```text
20260926_80

dante.outcome_reconciliation
dante.outcome_reconciliation_state
dante.outcome_reconciliation_evidence
dante.outcome_reconciliation_current_history
dante.outcome_reconciliation_operation
facet: outcome.reconciliation
```

Evidence pins exact Confirmation attestation MaterialStates. Confirmation correction does not reinterpret older reconciliation. Outcome correction does not transfer reconciliation.

## B10-E — Final integration + acceptance

Repository integration coverage:

```text
apps/backend/tests/integration/temporal/test_b10_e_whole_block.py
apps/web/src/features/temporal/timeline-truth-inspector.test.tsx
```

The user performed the integrated real-app walkthrough on 2026-09-26 and reported the chain working end-to-end.

Classification remains:

```text
B10-A..D = CLOSED / PROVEN
B10-E    = CLOSED / USER-REPORTED ACCEPTANCE
B10      = CLOSED
```

---

# 4. B11 closure record

B11 is historical closed scope. Do not describe any B11 walkthrough as pending.

B11-A completion-relative and anchor-stream-relative recurrence uses `_81`. B11-B bounded `actual_realization` Condition uses `_82`–`_85`. B11-C Schedule-relative self Reminder uses `_86`. The shared `_86` catalog probe measured `184|5|144|100|370|323|480|0|0|0` and the exact catalog tests passed after the CHECK-name and mapping-registration repairs.

B11-D integrated A/B/C. The full user-run local gate reported OpenAPI 7, PostgreSQL 14, deterministic generation 364, both typechecks, web 24 and final Ruff pass. The first real-app attempt exposed recurring Create `Senza Life Area` validation and Advanced Recurrence read transaction defects; both were repaired. The final isolated B11-D PostgreSQL rerun passed (`1 passed in 6.81s`) and the user reported the restarted integrated real-app walkthrough working.

Closure authority:

```text
docs/workstreams/timeline-temporal-operational-b11-closure-2026-09-28.md
```

B11 is `CLOSED / USER-REPORTED ACCEPTANCE`.

---

# 5. Closed gate — B13-A Work Structure Core

Scope authority:

```text
docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md
```

Immediate semantic target:

```text
canonical Plan
→ Plan-owned internal work decomposition
→ structural Step semantics
→ optional reference to a real Activity without identity collapse
→ explicit ordering separate from decomposition
→ deterministic accepted/current-state + history behavior
→ bounded author/read proof
```

Frozen boundaries:

```text
Plan != Activity
Step != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
```

Treat Step as internal work-structure semantics unless stronger current repository authority requires promotion to a universal root semantic identity. Do not create generic `work_item`, `node` or `edge` abstractions merely to defer the decision.

The B13-A discovery checkpoint resolved the implementation choices before `_87` DDL:

1. whether existing Plan identity/address primitives are sufficient or a dedicated Plan state family is required;
2. whether this gate is `Plan -> Step` only or needs recursive structural nesting;
3. the smallest semantic decomposition representation;
4. the ordering representation and correction/reordering history semantics;
5. how an optional Activity reference remains referential without identity collapse;
6. which existing identity/material/current-history primitives can be reused correctly;
7. database versus guarded-operation boundaries for cross-Plan, duplicate-link and cycle invariants;
8. the minimum public API/client/UI slice required for author/read proof.

The decision is flat `Plan -> Step`, reusing Plan NativeRef and giving Step an internal Plan-owned reference. Normalized revision snapshots hold membership, title, presentation order and optional same-self Activity link. Guarded functions enforce ownership, duplicate links and expected-current revision; current/history bindings remain explicit. `_88` repaired replay and catalog names; `_89` qualified the accepted-current update. OpenAPI, web/API typechecks, deterministic client generation and the UI test passed. The final user-run PostgreSQL/catalog suite passed **9 tests in 24.09s** at `_89`; B13-A is **closed**. Evidence: `timeline-temporal-operational-b13-a-closure-2026-09-28.md`.

B13-A non-goals:

```text
B13-B Dependency semantics
B13-C maximum Session / merge / spacing / preparation / recovery constraints
B12 solver/replanning
auto-Schedule
proposal acceptance semantics
AI scheduling authority
generic graph ontology
B07 UI consolidation
```

B13-A focused automated closure does not claim whole B13 real-app acceptance; that remains B13-D.

---

# 6. B13 continuation

B13-B is closed / proven at `_90`; its closure evidence is `timeline-temporal-operational-b13-b-closure-2026-09-29.md`. B13-C is closed / focused proof at `_92`: the user-run B13-A/B/C and exact Dictionary/catalog suite passed **13 tests in 29.16s** after the forward CHECK-name repair. The earlier web suite passed **11 tests**, deterministic client generation and both typechecks passed. See `timeline-temporal-operational-b13-c-closure-2026-09-29.md`. B13-D whole-block automated gate initially passed on the user's local worktree: generated check (383 files), both typechecks, web **12**, backend contract/unit **3**, PostgreSQL **14 in 44.24s**, and Ruff. Acceptance preparation exposed the UUID copy/paste Activity-link path; the direct card-to-linked-Step repair was published and used in the real app. Screenshots confirmed linked Record/Mix Steps and the `Actual avvenuto` Record → Mix Dependency in `sconosciuta`; after receiving the complete walkthrough the user reported “ok va chiudiamo”. B13-D/B13 are closed on user-reported acceptance, while the final seven-file web rerun and itemized remaining manual observations are not recorded. See `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`. See its scope, implementation checkpoint and gate documents. Do not merge Dependency truth into execution-structure constraints.

```text
B13-B — Qualified Dependencies
B13-C — Execution Structure Constraints
B13-D — Whole-block Integration / Proof / Acceptance
```

B13-B owns real dependency semantics. B13-C owns execution-structure constraints only where current Domain/Logical authority supports them. B13-D proves the complete B13 chain and real product behavior.

B12 block scope and B12-A diagnosis scope are published in `timeline-temporal-operational-b12-scope-2026-09-29.md` and `timeline-temporal-operational-b12-a-scope-2026-09-29.md`. B12-A is closed / proven on the user-run focused local gate at `db6a568`: generated 389, both typechecks, web 4, API contract 1, Ruff and PostgreSQL/catalog 11 passed in 26.14s. See `timeline-temporal-operational-b12-a-closure-2026-09-29.md`. Its read-only Home diagnosis distinguishes known hard violations, blocked prerequisites and unknown/unsupported bases without generating placements. B12-B is closed / proven on the user-run focused local gate: generated 393, both typechecks, web 3, backend 8, Ruff and PostgreSQL/catalog 11 passed in 24.63s; see `timeline-temporal-operational-b12-b-closure-2026-09-29.md`. B12-C is closed on the reported focused local gate: generated 397, both typechecks, web 4, Ruff, backend 9 and PostgreSQL 19 passed. See `timeline-temporal-operational-b12-c-closure-2026-09-29.md`. The original B12-D candidate passed the user-run gate on `75891447` (generated 397, web 11, backend 9, PostgreSQL/catalog 20, both typechecks and Ruff). The hard-rule and Movement Policy click path was repaired, and placement-zone authoring was moved to Colloca. The user accepted qualified B12 closure; the affected automated rerun and itemized real-app observations are unreported. See `timeline-temporal-operational-b12-closure-2026-09-30.md` and `timeline-temporal-operational-b12-d-gate-2026-09-29.md`. Replanning/solver behavior consumes canonical structure/dependency truth.

---

# 7. Collaboration discipline

- user runs tests locally; assistant does not use CI/GitHub Actions
- push coherent checkpoints frequently with `[skip ci]`
- published migrations are immutable; persistence fixes are forward-only
- generated API client comes only from repository generator
- PostgreSQL remains canonical truth
- distinguish proven persistence/domain semantics from user-reported product acceptance
- repository HEAD is source of truth before any write

## B14-U6 continuation, 2026-10-03

Branch `feature/timeline-temporal-operational` implementation checkpoint `64916cf2882323b7e4dd29ac5e9e42b551565273` follows the `_101` manual Session and execution-policy CHECK-name repair at `c7fa7209faa6e36b8b1a3c21ae52c68e73c6e7c6`. The user-run `_100` gate reported 12 passed and two exact-catalog failures caused by `_97` CHECK naming expansion. The `_101` forward rename is published but not yet PostgreSQL-proven. Follow the U6 candidate checkpoint for scope, verification and open acceptance.

The subsequent `_101` user gate reported 8 passed and two catalog test-code/Dictionary reference failures, repaired at `f453c2e82abeee9fa03331db265513343cda01ac`. `_102` at `16fe795e68a3c7662b3baf764596db4176043018` persists exact Schedule envelope/planned role and order and exposes it on readback.

The user then ran the focused `_102` atomic Activity structure and both catalog tests from `39c846d0`: **9 passed in 20.80s**. This also confirms the earlier catalog repairs on this branch. The subsequent B08 soft Session minimum in atomic U6 authoring was published at `8b9e9158`; the user ran its focused PostgreSQL test: **1 passed in 7.04s**. The agent reran 36 focused web tests and both web/API-client typechecks successfully. The combined U6/Event/catalog gate and real-stack walkthrough remain unreported; no U6 acceptance is recorded.

## B14 placement lock continuation, 2026-10-06

The current branch includes `_110` explicit user Schedule placement lock and backend/Timeline/Create candidate wiring (`9d2b6130`, reconciliation repair `84161fa5`). Distinguish it from B04 automatic movement policy. No user-run PostgreSQL migration, generated OpenAPI/client, web typecheck or real-app proof is reported; do not mark the lock closed. Existing B04 blocked policies cannot be safely reinterpreted/backfilled as user locks. The separate complete recurring-Activity inheritance vertical is still open and the Create incompatibility guard remains. See the 2026-10-06 addenda in the B14 recurring authoring contract and live map before continuing.


## B14 recurring Activity parity continuation — 2026-10-06

The recurring Activity Create candidate now carries the complete occurrence
template implemented on the current branch (intervals, planned Sessions,
Sub-Activities, Session settings, outcome review, Reminder lead and explicit
placement protection). The earlier statement that complete recurring
inheritance was not implemented is superseded by this candidate state; it is
still **unproven** until the user-run local and real-app gates pass.

The same Create Life Area contract now applies to one-off and recurring
Activities: none, existing, or create-new. The virtual Timeline unassigned
bucket is presentation-only and is not an authorable Life Area. Timeline
organization/color projection is refreshed after checkpoint/materialization so
materialized recurring Activities can resolve their accepted assignment and
appearance. Root start-time editing preserves Activity duration instead of
silently turning a same-day Activity into an overnight window.

Do not clone Activity-only interval/Session/Sub-Activity semantics into Event.
The next Event pass should share recurrence/Life-Area/color/Reminder/Timeline
infrastructure while keeping Event-specific semantics separate.


### Product correction — Sub-Activities

Sub-Activities are implementation/backward-compatibility residue, not an active
Create product surface. Do not reintroduce them while aligning Activity and
Event. Shared Event work should cover recurrence, Life Area/color, location,
description, Reminder and other genuinely shared capabilities only.

## 2026-10-06 — Create closure decision freeze

The active Activity/Event Create cleanup is now governed by `timeline-temporal-operational-create-closure-mini-roadmap-2026-10-06.md`. It freezes the compact three-batch plan: existing Event/B09/common capability consolidation; shared Reality + Objectives; then cleanup and user-run closure gate. Product copy uses **Scaletta** for B03-D Agenda; Sub-Activities are not a current Create product capability; sharing one item does not imply shared calendar/free-busy access.

## 2026-10-06 — Create closure candidate

Current migration source head is now `20261006_114`.

The accepted Create product model is frozen for the closure gate:

```text
Activity/Event
├─ shared authoring: placement / Life Area / color / description / location / recurrence / Reminder
├─ Activity-only: Activity intervals / planned Sessions / placement protection
├─ Event-only: Scaletta / expected participants
├─ Reality: optional global realization-review policy
└─ Objectives 0..N: boolean / quantity / qualitative / range
```

Reality and Objectives are independent. Objective measurements are Observation-backed and evaluated; they are not B10 Outcome payloads. Raw B10 Outcome remains available as a lower-level contextual disposition capability but is not the default Create product field.

Recurring Activity materializes Reality/Objectives onto each Activity instance. Recurring Event materializes them onto each Occurrence. Sub-Activities remain non-product/internal compatibility only.

Status is **IMPLEMENTATION CANDIDATE / USER LOCAL GATE PENDING**. No CI or GitHub Actions were used for this candidate; user runs the final local gate.


## 2026-10-06 — Create closure catalog reconciliation

Create-closure persistence is now reconciled through Alembic `20261006_115`. The final candidate catalog topology is 229 tables / 5 views / 191 routines, with 103 triggers, 467 physical indexes, 401 foreign keys and 569 CHECK constraints. The 14 new persistence tables are mapped and documented; 17 new routine names are documented; the explicit Schedule placement-lock trigger is included in Dictionary truth.

The first user-run gate exposed generated drift, five stale web assertions/type-contracts, two stale catalog snapshots and one Ruff import-order failure. The source/test/catalog repairs are now published. Generated OpenAPI/Orval output still must be produced by the repository generator in the user's local worktree before the final deterministic generated check and real-stack acceptance.

## 2026-10-06 — Create closure automatic gate green

User-run final catalog verification at `6371768b01c54dcf7ae6e8800ae73e8488d7d67e` passed: current catalog + cross-representation catalog suite => **8 passed**. Together with the already-green generated/typecheck/focused web gate, the automatic Create-closure gate is complete. Next cursor: real-stack visual/product acceptance only; fix regressions found there without reopening the product model.

## 2026-10-06 — Life Area Create contract frozen

User-run Life Area regression is green at `a48eb93e41d7040aa540139efce7371b5b18ef83`: focused Create UI test **13/13**; dedicated `apps/web/e2e/auth/temporal-create-life-area-golden.spec.ts` **4 passed, 2 skipped** (Chromium + Firefox real-stack; WebKit intentionally skipped by project policy). This proves one-off and recurring Activity/Event Life Area behavior across none/existing/create-new, assignment/readback, color projection, materialized Timeline items and reload. The picker exposes only canonical Life Areas; the presentation-only unassigned bucket is not authorable and the removed create-on-Add helper must not return. Mark this slice **FROZEN**; regressions should be fixed without reopening the product model.

## 2026-10-06 — Verification rail candidate

The B14/B07 Today rail candidate at Alembic `20261006_117` extends the shared lower edge of Timeline, Context Rail and Quick Create by 48 px and derives pending Reality/Objective/B10 Reconciliation cards from canonical state. Activity review requires a completed bounded Session; Event and Event Occurrence review uses the accepted placement end in the person's effective IANA zone, including date spans. The Reality response carries the exact Session/timing basis; Objective responses write Observation/Evaluation through the existing owner API. The branch candidate is unproven pending user-run local migration, generated-client/typecheck, focused PostgreSQL/web and real-app acceptance. The active details and gate are in `timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`.

## B14 recurrence edit scope correction — 2026-10-08

**Newly user-confirmed product authority**, detailed in the final section of
`timeline-temporal-operational-b14-ui-consolidation-2026-09-30.md`:
For a selected recurring Activity/Event instance, the only save scopes are
`Solo questa` and `Questa e le prossime`. **Both always include the clicked
instance**. Following scope additionally includes future instances later than
the selected recurrence position, NEVER other past instances. Example:
past 1,2,3; NOW; future 4,5,6 — selecting 1 yields 1 or 1+4+5+6
(not 2,3); selecting 4 yields 4 or 4+5+6; selecting 5 yields 5 or 5+6.
No future-only choice without the selected instance.

This governs **all edits**, not just Objectives. Past recorded facts and
evaluated Objectives remain correctable with the user's corrected value
becoming current canonical truth; they are not deletable. Correcting an
Objective retains its logical product identity with internal immutable
history, not a required new visible Objective. Current/future planned
content can be edited/removed subject to domain rules and chosen scope.
Dependent assessments must be reconciled without inventing manual
judgments. Previous Objective versioning design gate was superseded.
**Only the rule/documentation is approved; no code or schema implements
the full scoped modification/correction lifecycle yet.**

## B14 inspector scope and implementation checkpoint — 2026-10-08

Reconciled against live branch `39e8ab96`, road map/map,
B14 consolidation ledger, current API/Activity editor/duplicate seed, and
_121 migration/DB Dictionary. **Use the complete M1–M5 status and evidence
matrix in the B14 ledger** rather than older U6 candidate descriptions.

Recent user-run green gates: Activity interval replan Ruff 0,
backend unit **4/4**, PostgreSQL/catalog **15/15**, previous web **15/15**,
API client source-generation deterministic **483**; six generator-produced
artifacts published by the user in `c22f04ae`. Post-create Activity
Objective ADD web typecheck 0 and **17/17 Vitest**, also user run.
Focused PASS is not final real-app Inspector acceptance.

Global modification policy is approved but **not yet implemented**:
`Solo questa` or `Questa e le prossime`, always including the clicked
instance; the second targets additional *future* instances only, never other
past occurrences. Past Objective/Observation corrections become current
truth, with immutable audit; past realized facts cannot be deleted.
No inference about the user's reason for editing. Applies to ALL relevant
Activity/Event modifications, not Objectives alone.

**Next**: M1 canonical recurrence-instance scope + safe preview/CAS,
then M2 Objective definition/recorded-fact correction, M3 Activity edit
gaps and past retirement policy, M4 faithful duplication/Event parity,
M5 user local end-to-end real-stack and B15 closure. Do not implement
future-only scope, direct Objective target mutation or copy of Actual/
Observation/Evaluation into duplicates. No CI/Actions; user alone runs
local WSL tests.

## B14 M1-A selector candidate — 2026-10-08

Live GitHub contains `apps/backend/src/dante/modules/temporal/occurrence_edit_scope.py`
and `apps/backend/tests/test_b14_occurrence_edit_scope.py`, plus a detailed
scope note at the end of the B14 ledger. This is an independent,
**not-yet-user-tested** pure selection candidate. It reuses existing B06/B11
Occurrence/Recurrence identity and enforces selected-anchor plus later
future only (not other past instances), detects skipped/overridden/
recorded-fact conflicts, distinguishes future template inheritance,
and rejects unverified/incomplete following inventories. It does NOT
yet add an API, SQL function, web wiring or persist multi-instance edits;
the full M1 block is OPEN. User runs Ruff and focused pytest in WSL.
Next deliverable: guarded authoritative current occurrence inventory +
source CAS/preview/apply integration, reusing B06/B11 functions rather
than rebuilding their already-proven functionality. The user explicitly
noted that several original backlog capabilities already exist, so
avoid counting implemented individual features as missing.

## 2026-10-08 — M1-A passed; M1-B guarded inventory checkpoint

**User-local PASS** at `a62ab230`: M1-A Ruff 0; 18/18 focused
unit tests. M1-A pure selector closed. **M1 remains OPEN**.
M1-B adds forward-only `20261008_122` a bounded owner-only
materialized Occurrence read via existing B06 `get_self_occurrence`,
a Python read application and read-only HTTP
`GET /temporal/occurrences/{ref}/edit-inventory`. It includes
skipped/Scheduled/extra materialized instances for both Routine and
Event source, with 10k hard failure and no newly generated future
assumptions; no apply authorization. The database Dictionary and
exact topology probes were advanced to 231/5/**197**/103/471/405/572.
New focused integration test is
`test_b14_m1_edit_inventory.py`.

**UNPROVEN candidate** until user local PostgreSQL, catalog, Ruff,
OpenAPI/generated client and typechecks. No multi-instance mutation
or scope UI is yet implemented. Next M1-C must add authoritative
write-time CAS, override/recorded-fact conflict resolution,
Activity/Event identity linking, future template revision and one
atomic idempotent apply. User runs tests locally, no CI.

## 2026-10-08 — M1 whole-vertical candidate _123, user gate pending

User-reported _122 inventory **Ruff PASS, PostgreSQL 10/10 PASS,
OpenAPI generated/check 484 PASS, API/Web typecheck PASS**.
Generated files currently uncommitted in local user worktree.

Live branch now includes forward migration `20261008_123`,
append-only `occurrence_profile_edit`, five self-scoped read/write
functions, ORM/Database Dictionary exact target
`232|5|202|103|473|408|576`, atomic recurrence-source
metadata edit with CAS/replay/owner controls, selected-anchor/future
inheritance, Activity readback/Timeline projection/materialization,
and scoped Activity general-metadata save UI. Event Occurrence
metadata patch has backend/Timeline support; M4 Event Inspector
UI parity remains open. New PostgreSQL and Vitest tests are
in the branch but not user-run. Latest work is one combined
candidate, **not** a claim of final whole B14 acceptance.

The user explicitly requests **no further small isolated steps**:
request ONE combined local gate. Preserve generated client output
once it passes. Do not claim that scoped editing already handles
Objective facts, Session/Scaletta, Schedule or all other fields;
M2/M3/M4 will integrate those owners with the global
`Solo questa / Questa e le prossime` contract.

## 2026-10-08 — _124 fixes M1 gate regression (user proof pending)

M1 _123 local user gate results: Ruff 1 (2 I001), 18/18 unit
PASS, PostgreSQL 16 PASS / 4 FAIL; OpenAPI generation PASS,
generated 489 deterministic PASS, API/Web typecheck PASS,
Vitest 21 PASS. Four PostgreSQL failures share a single
one-off Activity Inspector profile NULL Occurrence access,
not a security failure in the strict Occurrence function.

On branch: `20261008_124_b14_scoped_activity_profile_guard.py`
forward-only existing function replacement (explicit null guard);
Timeline one-off Activity CASE guard; two import sort fixes;
Dictionary (one routine now PL/pgSQL) and _124 exact catalog
expected revision; focused one-off Activity regression test.
No new objects; topology unchanged 232|5|202|103|473|408|576.
_124 user-run local proof **PENDING**. User should run one
combined focused local gate, preserving locally generated
API client artifacts. No CI. M1 metadata candidate is NOT yet
closed until that proof.

## 2026-10-08 — _124 user local gate: PostgreSQL/Web all green; lint-only fix

User confirmed after pulling `14b38334`:
`POSTGRES=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`,
`WEB_TYPECHECK=0`, `VITEST=0`. The previous four B14 Activity
Inspector failures are gone and the new one-off profile regression
test passed. Ruff found exactly one new test-only rule `DTZ011`
(`date.today()` in
`tests/integration/temporal/test_b14_m1_activity_profile_guard.py`).
Commit `62c18771` replaces it with
`datetime.now(ZoneInfo("Europe/Rome")).date()`.
**Only focused Ruff rerun remains** for _124 technical gate.
Generated client OpenAPI/TypeScript artifacts pass deterministic
check but are still modified/untracked in the user's local worktree;
they are NOT yet published to the remote branch. Preserve them and
reconcile their commit before marking M1 metadata delivery closed.
No CI. B14 domain M2–M5 remain open.

## 2026-10-08 — M1 recurring general-metadata vertical closed, all artifacts on GitHub

User completed final local `set -e` gate at _124 and published `55a017b9` to `feature/timeline-temporal-operational`. Ruff **All checks passed!**, earlier _124 PostgreSQL/Generated Check/API Typecheck/Web Typecheck/Vitest all exit **0**. User-produced commit adds nine generated OpenAPI/Orval files (1,013 insertions), push succeeds, and `git status --short` is clean. M1-A 18 unit and M1-B 10 PostgreSQL were separately proven. **Mark M1 CLOSED only for recurring Activity/Event general metadata,** with the user-run focused gate. No hidden claim of visual acceptance or other domain edits. Revision _124 exact catalog unchanged 232/5/202/103/473/408/576. Resume M2 complete Objective definition/reality correction with stable logical Objective identity (retain old accepted snapshots/Observations/Evaluation for audit; newest corrected values canonical), no deleting recorded historical facts, correct deterministic re-evaluation, actor-scope, CAS and operation replay. The product rule for ALL edits remains selected included in either of exactly two scopes; future-only excludes the other already-past Occurrences. M3/M4/M5/B15 open. The dependency advisory shown by GitHub upon push (34 on default branch) is not a result of this gate and was not investigated; treat independently, not as B14 blocker. No CI/Actions.

## 2026-10-08 — M2 complete Objective correction candidate (_125/_126), local proof open

Latest M1 general metadata: published generated `55a017b9`, user Ruff+PostgreSQL+Web+client all green, exact _124 catalog. M2 newly committed on branch: `20261008_125_b14_objective_corrections.py` adds append-only `temporal_objective_definition_revision` and 3 self-scoped capability functions, replacing effective list/result readers; `20261008_126_b14_scoped_objective_definition.py` adds append-only `temporal_objective_series_edit` and 2 new self-scoped functions, replacing effective definition read to apply selected+later future source-template policies. SQLAlchemy mappings and exact Dictionary now 234/5/207/103/477/414/586. Changes never delete Observations, Evaluation states or previous definitions. User-corrected past definitions become current truth under same `objective_ref`, with deterministic quantitative/boolean reassessment; manual qualitative assessment cannot be fabricated.

Objective series scope uses trusted `b14:objective:{kind}:{subject_ref}:{slot}` materializer provenance and current source/Recurrence CAS, *not* name or `presentation_order`. Both scope choices include clicked instance; other past excluded. Skip, Actual, locally corrected future Objective and prior Observation block all-or-nothing series update. Future newly materialized Objective inherits read-side source policy; its own recorded result is never copied. Manual one-off Objective edits work with selected scope only and the UI makes limitations explicit. New Objective definition/result correction API, typed Web data source and Activity editor (existing Objective edit and result correction) plus focused PostgreSQL and Vitest tests are committed.

**Status: CANDIDATE, USER LOCAL GATE NOT RUN.** One whole test pass required (Ruff, _125/_126 migration/DB exact catalog, Objective correction and recurring-scope PostgreSQL + prior M1/Objective regression, generated/check, TypeScript, Vitest). Publish canonical generated files after the gate. Do not mark M2 or B14 closed before user gate. Do not reopen previous B06/B11, no CI or Actions. M3/M4/M5/B15 still open.

## 2026-10-08 — First local M2 gate: syntax blocker repaired, focused rerun required

User local first M2 gate at branch `4f7c90d3`: `RUFF=1` (malformed ORM mapping and Objective audit test), `POSTGRES=2` (seven collection errors from ORM SyntaxError), `GENERATE=1` (FastAPI cannot import), `GENERATED_CHECK=1` (TSX malformed), `API_TYPECHECK=0`, `WEB_TYPECHECK=2`, `VITEST=1` (11 other tests green; Activity editor TSX failed to parse). **No passing DB functional assessment was reached**.

Fixes since gate: rebuilt `b14_create_closure.py` from pre-M2 stable mapping and added exactly one immutable Objective definition row and one series row with exact named constraints and complete fingerprint regex; repaired test's `asyncio` audit count closure; repaired `activity-edit-panel.tsx` JSX handler. Additionally tightened historical recorded-result replay to precede current definition type/shape validation, and made result correction require an actual previous Evaluation state under CAS in SQL, FastAPI and the Web UI/data source. No Alembic revision/count changes; catalog target remains `20261008_126`, `234/5/207/103/477/414/586`.

**Status remains M2 CANDIDATE, NOT GATE-GREEN**. User must run ONE complete new local gate for Ruff, Postgres, generation/check, typecheck and Vitest. Generated OpenAPI/Orval files are not published yet. M3/M4/M5/B15 remain open; no Actions/CI.

## 2026-10-08 — Second user local M2 gate, remaining blockers fixed in branch

Second user gate at `7b3f1df1`: `RUFF=1`, `POSTGRES=2` (collection aborted), `GENERATE=1` and `GENERATED_CHECK=1`, all cascading from **two remaining orphan trailing ORM CheckConstraint snippets** in `b14_create_closure.py` (lines 223, 302). `WEB_TYPECHECK=2` reported nullable `objective.evaluationStateRef` at Activity editor line 313. `API_TYPECHECK=0`, **`VITEST=0`** with the prior TSX syntax already fixed.

Branch repairs: surgically removed both malformed orphan fragments after legitimate class `__table_args__` (commit `302a74ac`, readback confirms 16 unique classes and no orphan line), added explicit non-null Evaluation guard at correction call site before submitting required correction state (commit `96b3ecf6`). These changes are syntax/call-site corrections, not a migration revision bump. Current expected catalog remains `20261008_126`, `234/5/207/103/477/414/586`. Source readbacks verified correct base classes, legacy Objective methods and template-generated Event/Activity origin contract.

**M2 NOT GREEN: functional PostgreSQL tests still have not executed, and generated OpenAPI/Orval files have not been committed.** Rerun one complete local gate before claiming any M2 closure; avoid CI.

Additional pre-gate static review: corrected all three M2 recurring test queries that had incorrectly read `generated_date` from `dante.occurrence_generation`; generated calendar dates live in `dante.occurrence_generation_calendar` and are now joined explicitly. No effect on runtime schema, extra migration or dictionary topology.

## 2026-10-08 — M2 third user local gate: actual PostgreSQL frontier (supersedes earlier "pending" notes)

User local gate on `2e5028df` reached `SYNTAX=0`, `POSTGRES=1` (**16 passed, 4 failed**), `GENERATE=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`, `WEB_TYPECHECK=0`, `VITEST=0`. The sole Ruff failure `RUFF=1` was an import-format `I001` in `mappings/b14_create_closure.py`; the source was corrected on GitHub in `1ff3e500` but still needs local verification. Unlike the two earlier M2 gates, migrations through `20261008_126` ran and PostgreSQL executed the functional suite, so this is **not** a collection/syntax failure.

The **four remaining failures** are exactly:
1. `test_b14_m2_objective_corrections.py::test_objective_definition_and_result_corrections_are_canonical_without_deletion`
2. `test_b14_m2_objective_scope.py::test_generated_routine_objective_scope_selected_past_and_later_future`
3. `test_b14_m2_objective_scope.py::test_generated_event_objectives_share_future_scope_without_copying_results`
4. `test_database_current_catalog.py::test_current_database_cross_representation_is_exact`

The pasted gate output included the final summary and only the last 100 lines of the PostgreSQL log; the **individual failure tracebacks are not available** in the shared excerpt. Do not invent diagnoses or mark M2/test catalog green. The user's full traceback source is `/tmp/dante-m2-final.2m48YP/POSTGRES.log` in their local worktree. Read it **without re-running the suite**. `pnpm api:generate` created modified/untracked canonical OpenAPI/Orval files in the local working tree; deterministic generated check passed locally, **but these files are not yet committed/pushed**.

**Current frontier:** M1 general-metadata recurring scope is user-proven and published in `55a017b9`. M2 Objective corrections, immutable history and template-derived selected/future policy are implemented as **candidate only** on `_125/_126`; clear four PostgreSQL failures and exact Dictionary/catalog comparison, rerun one consolidated user-local gate, then publish generated client and record closure. M3 remaining Activity/Session/Life Area/Schedule edits, M4 Event Inspector and faithful Activity/Event Duplica, M5 real app/visual acceptance, and B15 whole-vertical closure remain open. Preserve approved semantics: only `Solo questa` / `Questa e le prossime`, clicked always included, other past unaffected, no deleting factual history or fabricating future Observations. User runs tests in `~/projects/dante`; no Actions/CI; no extra micro-gates.

## 2026-10-08 — M2 third PostgreSQL failure forensics and four-source fixes

The user supplied the **full `FAILURES` section** from `/tmp/dante-m2-final.2m48YP/POSTGRES.log`. Concrete root causes were confirmed, rather than guessed:
1. `test_objective_definition_and_result_corrections_are_canonical_without_deletion`: all actual HTTP recording/definition/replay/CAS checks reached their expected status; the last assertion incorrectly expected JSON numeric `6` instead of the contract's Decimal serialization string `"6"`. Test now uses `Decimal(str(...))`. The same test's subsequent internal-audit query was also preemptively repaired to use the **isolated test administrator**; `dante_runtime` must not gain raw Observation/Evaluation table SELECT.
2. `test_generated_routine_objective_scope_selected_past_and_later_future`: test setup generated a `floating_local` recurrence, but the real recurring-Activity template materializer requires an actual `named_zone` wall time and zone. Test now uses a named-zone daily recurrence (`Europe/Rome`, explicit DST policies); production materializer unchanged.
3. `test_generated_event_objectives_share_future_scope_without_copying_results`: the test attempted direct SELECT on `dante.temporal_objective` under `dante_runtime` and correctly received `InsufficientPrivilege`. Both Event and Routine tests now read **replayable B06 checkpoint identities**, linked Activity refs via `dante.list_self_routine_occurrence_activities`, and Objective refs through `dante.list_self_temporal_objectives`. Removed all raw protected-table SELECTs from the routine/event Objective-scope test; production owner ACL unchanged.
4. `test_current_database_cross_representation_is_exact`: the final ORM registry count assertion still expected 232 tables even though mapping, dictionary and live catalog all enumerate **234**. Changed only stale test literal to 234.

All fixes committed/pushed on `feature/timeline-temporal-operational` (not CI): `fae4dcbf`, `b72d7f2b`, `470fde9d`, `61dd6913`, `b5c55489`. Post-edit branch readback verified single Objective mapping classes, correct fingerprints, no test table-policy bypass, and all four corrections. **These edits have not yet been subjected to the next user-run local gate; M2 is NOT closed.** DB expected revision `20261008_126` and topology `234/5/207/103/477/414/586` remain unchanged; no speculative migrations and no role grants. Rerun the whole focused Ruff + PostgreSQL/catalog + generated API/check + API/Web TS typechecks + Vitest gate once. If green, stage and publish only deterministic generated client files, then record M2 closure. M3/M4/M5/B15 remain open.

## 2026-10-08 — AUTHORITATIVE LATEST HANDOFF: M2 GATE GREEN, generated client published

This entry **supersedes earlier M2 pending/failing status lines**; preserve them solely as historical investigation. On the user's final WSL `~/projects/dante` gate after pulling `b1599c19`:
```text
SYNTAX=0
RUFF=0
POSTGRES=0
GENERATE=0
GENERATED_CHECK=0
API_TYPECHECK=0
WEB_TYPECHECK=0
VITEST=0
LOG_DIR=/tmp/dante-m2-gate.ZTDo2Z
TUTTI I GATE VERDI
CLIENT_API_PUBLISH_EXIT=0
```
The user then committed/pushed canonical generated OpenAPI/Orval client in `09dc26f9` (ten changed files); verified remote `feature/timeline-temporal-operational` HEAD `09dc26f9e7140698856461d8e1b7652eadc93404` and generated Objective model file availability. `20261008_126` Dictionary/catalog expected topology 234/5/207/103/477/414/586 is included in the successful focused tests. **M2 CLOSED for automated technical scope only**, not an assertion of visual or full-stack usage acceptance. M1 already closed for scoped general metadata. No fresh independent assistant-side PostgreSQL run was performed.

**Next action, M3:** inspect already working Activity Inspector/Edit/Replan and domain-owned B08 Session, B05 Life Area, B02/B04 Schedule/Reminder, and B14 retirement to avoid redundant implementations. Finish remaining existing planned Session display-name mutation; null/unassign primary Life Area; outstanding temporal forms/settings and Schedule/Reminder/policy edits; history-aware Activity retirement. Design authoritative scoped edits for recurrence-derived instances without changing unrelated past facts. One complete bounded M3 backend/DB/Dictionary/API/Web integration and one user-local combined gate; no micro-gates, no CI. Thereafter M4 faithful Activity/Event Duplicate + Event Inspector, M5 product dogfood, B15 whole vertical. User runs tests from local worktree `~/projects/dante`; do not use GitHub Actions.

## 2026-10-08 — M3 post-create Activity residual edit candidate on _127

**CURRENT STATUS: IMPLEMENTED CANDIDATE; THE USER HAS NOT RUN THE _127 LOCAL GATE.** Do not call M3 proven or B14/B15 closed. Following M2 user-green gate and generated publication `09dc26f9`, forward-only `20261008_127` adds three post-create behaviors:
- Actor-local Activity **and Event primary Life Area explicit unassignment**: four existing `life_area_ref` columns (current row + immutable operation receipts) accept NULL. The existing guarded assign functions retain self ownership, expected-revision CAS, durable operation receipt, replay/reuse rejection and monotonic revision after unassignment/reassignment; `list_self_unassigned_life_area_items` now recognizes explicitly null assignments. API/request/response/ORM, Activity editor and remote source accept NULL. No fake Life Area is created and no row deletion resets revision.
- Existing **planned Activity Session display name** can be revised through the same `activity_schedule_role` Schedule identity, using a new self-scoped `revise_self_planned_session_name` function (expected-name compare, idempotent same-target replay, validation, actor-ownership and retired guard). This is **presentation metadata**, not actual Session timing or schedule-history mutation. API, remote client, Activity editor and tests added; no history of prior *label values* is modeled in this candidate, so do not misrepresent it as a full append-only label ledger or a recurring template-wide edit.
- **Activity retirement historical-truth veto**: the existing guarded `retire_self_activity` function now rejects deletion/retirement whenever a Session (even ended), accepted Actual or recorded Objective observation/evaluation exists. The existing open-Session veto and retirement operation replay remain. Inspector explains the restriction and shows a conflict for recorded truth. Corrections to historical data continue through their own domain-owned edit endpoints.

Candidate DB topology `234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK` at `20261008_127`; ORM, Dictionary entries, scope and exact catalog test expectations updated. The additional routine is the planned label capability; nullable columns create no new tables/constraints. Backend PostgreSQL test `test_b14_m3_residual_editor.py` checks Life Area null CAS/replay/actor isolation, Event parity, planned Schedule identity and recorded Session retirement veto; focused Web remote-contract regression added.

**Outstanding verification and scope:** no automated _127 proof yet; migrations/DB exact catalog, legacy B05/B14 and M2 regression, API generation/determinism, Web/API-client typecheck and Vitest must pass on the user local worktree before publishing canonical generated files. Remaining broad M3 questions include recurrence-template propagation for domain-owned Session name/Life Area, non-supported temporal-form UX and acceptance of historical label edits; do not claim these solved by selected-only mutations. Preserve `Solo questa`/`Questa e le prossime` for supported recurring edits with clicked included. After honest M3 gating/reconciliation, M4 faithful Activity/Event Duplica and Event Inspector and M5/B15 full product acceptance remain. No GitHub Actions or CI.


## 2026-10-08 14:28 — M3 first user-local gate: blocked by _127 migration, repair published

User pulled M3 candidate `4ed4497e` and ran consolidated `/tmp/dante-m3-gate.scSaU4`. Reported `SYNTAX=0 RUFF=1 POSTGRES=1 GENERATE=0 GENERATED_CHECK=0 API_TYPECHECK=0 WEB_TYPECHECK=0 VITEST=0`. The reported `26 PostgreSQL errors` were **all migration setup failures**, not 26 individually executed/failing assertions. Primary blocker: Psycopg treats SQL `dante.activity_intention%ROWTYPE` inside unescaped raw `exec_driver_sql` as an invalid `%R` placeholder. The M3 _127 migration was never applied successfully in that gate. Ruff listed three findings: SQL interpolated function string, import order in `test_b14_m3_residual_editor.py`, and PT018 compound assertion. All eight gate results have not been reverified after the repairs. Client API generated files exist **only as local user worktree changes**, not on remote; do not delete or hand-edit them.

**Repair pushed on the same branch after failed migration gate:** replace PL/pgSQL `%ROWTYPE` local variable with `record` (equivalent `SELECT * INTO` behavior without driver placeholder); scope `# noqa: S608` to the *closing Python triple-string line* so the literal SQL contains no Python comment; sort tests imports and split compound assertion. Last repair commit `4dfd046f`, branch advanced since original `4ed4497e`. No local user retest has been reported. Next gate should run Ruff, PostgreSQL and exact catalog with existing suite, then TypeScript/Orval determinism as needed; one consolidated command. Fix actual subsequent failures together, never count setup failures as passing domain tests, no CI. **M3 remains OPEN, not proven.**

## 2026-10-08 14:42 — M3 second local gate: 21 PASS / 5 FAIL (repairs pending user verification)

The user pulled `c7206a10` and executed the M3 combined recheck; `RUFF=1` (test import ordering), `POSTGRES=1` with **21 passed, 5 failed**, while `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK` and `VITEST` were previously green. The failed tests were M3 Activity null Life Area, M3 Event null Life Area, legacy B05 primary reassignment, M2 Event Objective definition (which uses a scheduled Event with an assigned Life Area), and exact database cross-representation catalog. The displayed log was only `tail -n 100`, so full individual test tracebacks were not included; log path on user's WSL: `/tmp/dante-m3-recheck.LM4nCX/POSTGRES.log`.

Code review established that `20261008_127`'s `assign_self_{activity,event}_life_area` functions used unqualified `WHERE life_area_ref=requested_life_area_ref` although `life_area_ref` is also a PL/pgSQL output variable under `#variable_conflict error`. The new SQL now explicitly uses `target.life_area_ref`, `target.self_person_ref`, `target.archived` (commit `39e11193`). The B05 legacy and M2 scheduled Event tests both call these replacement Life Area functions, explaining their shared likely failure path. Ruff import placement corrected in `test_b14_m3_residual_editor.py` (commit `7ad57b87`). Exact-catalog test stale values were updated to **208 routines**, **447 standalone entries**, and to expect `B14-M3-RESIDUAL-EDITOR` in completed stages (commit `56a6e4de`). The physical topology expected remains **234 tables / 5 views / 208 routines / 103 triggers / 477 indexes / 414 FKs / 586 CHECK**.

**Latest state: _127 M3 implementation candidate, NOT verified green.** Recheck focused Ruff and PostgreSQL, then the full local gate before generated-client publication. User's uncommitted OpenAPI/Orval outputs must be preserved (do not reset/overwrite manually); no Actions or CI. If additional failure remains, collect complete pytest failure traceback rather than another `tail -n 100` summary. M1/M2 remain closed and published; M4/M5/B15 still open.

## 2026-10-08 — AUTHORITATIVE M3 LOCAL GATE RESULT: GREEN, client in 6fdda05f

The previous first and second failing M3 logs below/above are **superseded**. User's WSL local worktree `~/projects/dante` pulled `d09af8a0` and ran the complete 8-part gate:
```text
SYNTAX=0
RUFF=0
POSTGRES=0
GENERATE=0
GENERATED_CHECK=0
API_TYPECHECK=0
WEB_TYPECHECK=0
VITEST=0
PUBLISH_EXIT=0
LOG_DIR=/tmp/dante-m3-final.rAAiah
```
GitHub received `6fdda05f`: 10 generated OpenAPI/Orval artifacts (343 insertions, 10 deletions), including planned Session name models and Life Area nullable response/request changes. GitHub branch `feature/timeline-temporal-operational` was independently read back at `6fdda05feb0035a66274dfbbf1723aad495b6637`. The focused PG suite includes M3 tests, B05 existing Life Area tests, Activity inspector/replan/snapshot, M2 Objective regression, current schema/catalog assertions; green. Exact _127 Dictionary target 234 tables/5 views/208 routines/103 triggers/477 indexes/414 FK/586 CHECK, standalone 447; green within the user's tested suite.

**Status:** M1, M2 and **M3-A owner-domain residual edit implementation** technically proven and generated code published. M3 as entire roadmap block **remains open**, because generated Routine/Event recurrence source template propagation for newly edited Life Area/planned Session label and all Create/Edit temporal policy settings parity have not been demonstrated. Current UI safely restricts these new domain edits to selected-only, and explicitly refuses `Questa e le prossime`; no hidden propagation. Do not turn off the guard as a workaround or call M3/M4/B14/B15 completely closed.

**Next action:** inspect actual source/template Life Area and planned Session naming ownership, established M1/M2 guarded scope machinery, Schedule/Reminder policy editor read/write surfaces, existing tests and Domain/Logical/Physical/Dictionary before choosing a bounded implementation. Preserve invariant `Solo questa` includes clicked, `Questa e le prossime` includes clicked plus later future only and never other past; no implicit copying of recorded truth. Implement a full coherent chunk, then request one user-local gate, no GitHub Actions/CI. Then M4 Activity/Event faithful Duplica + Event Inspector, M5 real-stack visual acceptance, B15 closure.

## 2026-10-08 — M3-B owner-domain scope integrity candidate (no migration)

After M3-A user-green `_127` gate and published generated client `6fdda05f`, M3-B review of the actual Domain/Logical/Physical contracts, `routine_occurrence_materialization.py`, M1 `_123` and M2 `_126` established **no canonical following-series policy for Life Area or planned Session labels**. Routine materializer reads the owner's Life Area from `list_self_routines`; planned Session labels are copied from `routine_occurrence_policy.activity_template.planned_slices[].name`. Following edits cannot be safely implemented as a loop over already materialized Activity/Schedule rows: that misses future checkpoint instances and breaks owner/source CAS and historical exceptions. Routine/Event source semantics differ; do not imply parity without proof. The detailed negative-scope acceptance plan is in `docs/workstreams/timeline-temporal-operational-m3-b-owner-scope-2026-10-08.md`.

**Implemented on GitHub, newly UNTESTED:** the Activity editor now treats pending planned Session names as dirty and blocks general save and replan preview/apply until individually saved; after successful replanning it rebuilds the planned-name baseline. The recurring scope controls are visible even for Life Area/name-only drafts but disable `Questa e le prossime` when there is no supported metadata change, with explicit owner-domain-only guidance. Unsupported temporal Schedule forms are left untouched, with a non-conversion explanation. The remote Activity Inspector displays the recorded-truth retirement veto specifically instead of a generic stale conflict. Focused Vitest cases were added for draft loss, replan coexistence, recurring Life Area and Session name scopes, unsupported absolute temporal form, and retirement error/invalidation.

**State:** M3-A remains technically green; **M3-B candidate UI/guard implementation needs a fresh user-local Web typecheck and focused Vitest gate**. M3-B following-source implementation remains open: a new source policy must protect original selected Occurrence, future not-yet-generated occurrences, stable planned-template slot identity, independent per-instance edits, skip/Actual/recorded Session/Observation, owner and recurrence CAS; no such source policy is claimed or silently emulated. No new migrations or Dictionary topology changes: still `20261008_127` and `234/5/208/103/477/414/586`. M4/M5/B15 remain open. No GitHub Actions/CI; user runs local gate.

### M3-B extra integration proof added after UI audit (pending local run)

The new test `apps/backend/tests/integration/temporal/test_b14_m3_b_instance_scope_boundary.py` creates a canonical daily Routine with a named root planned Session, materializes two Occurrences, edits only the first generated Activity's Life Area and first planned Session display name, then checkpoints a third future Occurrence. It asserts the selected Activity/label change preserves Schedule identity, and the other materialized and newly generated Activities retain the **source** Life Area (unassigned) and template planned name, with no covert following-series propagation. It reads exact checkpoint IDs and links through existing owner-scoped capabilities rather than raw runtime table grants. This test and newly added UI tests **have not yet run in the user's local PostgreSQL/Web harness**; do not treat the negative assertion as proven until the gate. The consolidated M3-B gate must include this new test plus the B14 M3-A/M2 owner regression, Web typecheck and two focused Vitest files. Schema/catalog unchanged _127; no generated client publication needed for this UI/negative-test-only change.

## 2026-10-08 — M3-B user local gate and Web test repair (pending rerun)

User pulled `71117ae5` and ran consolidated `/tmp/dante-m3b-gate.qlpPBc` on `~/projects/dante`. **Verified green locally:** `SYNTAX=0`, `RUFF=0`, `POSTGRES=0` (including the new negative-future-checkpoint test plus M2/M3-A regressions and exact DB catalog), `GENERATED_CHECK=0`, `API_TYPECHECK=0`. **Two Web-only failures:** `WEB_TYPECHECK=2` (`activity-inspector-actions.test.tsx:662`: array index `getAllByLabelText('Inizio')[0]` typed `HTMLElement | undefined` under strict no-unsafe-index) and `VITEST=1` (35 passed, one test failed at :717 because selected-only Life Area was *already* correctly preventing `this_and_following` and showing the general "Life Area e nomi delle Session pianificate si salvano soltanto per questa istanza" explanatory paragraph, whereas the test incorrectly expected the conditional warning shown only after an unsupported scope selection). This is **not** a PostgreSQL/schema regression.

**Code correction published:** `23daae86`, only `apps/web/src/features/home/ui/timeline/activity-inspector-actions.test.tsx`. Add explicit nonnull array index for first `Inizio` input (the Testing Library `getAllBy...` contract throws if there are zero elements) and assert the exact, reachable selected-only scope guidance. The guarded UI behavior, persistence, recurring source policy and DB code are unchanged. Remote HEAD verified at `23daae86029462c33213070ca855cb72e2e44aa8` before this documentation update. **Next action:** user runs just `pnpm --filter @dante/web typecheck` and the four M3-B focused Vitest files after `git pull --ff-only`. No reason to re-run passing PG and generated-client checks for this test-only change; no regenerated client needed. **M3-B guard subvertical NOT closed until local Web recheck passes.** This does not close the separate, unimplemented source/template `Questa e le prossime` policy for Life Area/planned Session names; full M3, M4/M5 and B15 still OPEN. No CI/Actions.

## 2026-10-08 — M3-B UI/negative-scope guard subvertical locally GREEN

**Latest acceptance supersedes earlier M3-B "pending Web recheck" entries.** The user pulled `b03d8aa4` into WSL `~/projects/dante` and ran the focused Web recheck: `WEB_TYPECHECK=0`, `VITEST=0`, 4 test files / **36 tests passed** (Activity Inspector UI 23, Remote Inspector 3, Remote Activity Settings 7, Remote Recurring Profile 3). Log directory `/tmp/dante-m3b-web-final.L8HfvO`. The preceding combined M3-B gate had already passed `SYNTAX=0`, `RUFF=0`, `POSTGRES=0` (including the new negative future-checkpoint Routine test and prior M3-A/M2 regression), `GENERATED_CHECK=0`, `API_TYPECHECK=0`; after these, **all bounded M3-B guard checks are proven green locally**. No schema/client change after the original backend green run; final Web fix was test-only `23daae86`. No new API generation or client publication required.

**CLOSED as bounded technical work:** M3-B editor safeguards, explicit individual-only mode, unsaved planned-name replan/save protection, truthful incompatible temporal-form UI, recorded-fact retirement reporting, and negative no-implicit-following provenance proof. **NOT CLOSED:** M3 following-source policy for optional Life Area or planned Session names of recurrence-derived Activity/Event Occurrences. `Questa e le prossime` remains explicitly disabled for these owner-domain fields. Future and already materialized later instances require an owner-authoritative policy, source CAS, immutable operation replay and template slot provenance. M1, M2 and M3-A remain green; broader M3 open. M4 (Event Inspector / faithful Activity/Event duplication), M5 product UI acceptance and B15 closure open. Next work: read actual Routine/Event Domain/Logical/Physical and M1/M2 source policy implementations and implement bounded canonical source policy, then one user-local gate. No CI/Actions.

## 2026-10-08 — M3 delivered scope consolidated; no more micro-stages; M4 begun

Per user priority, **stop splitting the already user-proven M3 editor implementation** and advance to one combined **M4 Inspector/Edit/Duplicate** workstream (requirements and current candidate in `docs/workstreams/timeline-temporal-operational-m4-delivery.md`). M3 delivered/proven scope: Activity/Event nullable primary Life Area owner CAS, Activity planned Session renaming without Schedule/execution identity replacement, historic-fact retirement guard, supported core policy/Reminder and replan paths, clear selected-only recurring edit guards, and safe nonconverting temporal forms. _127 exact DB catalog + generated client `6fdda05f` and M3-B 36/36 Web regression are user-verified. **M3 implementation is accepted as delivered for this bounded scope; this does NOT waive or falsely close the global source-following feature.** The missing future source policy for Life Area and planned Session names remains **explicit B14 global-scope parity debt before B15**, with `Questa e le prossime` still disabled; never silently claim it works. No user-requested additional micro-gates.

**M4 underway (NOT green):** new Event duplicate seed from persisted canonical Timeline Schedule + Agenda/Life Area/expected participants; Event Inspector duplicate action that validates participants; explicit refusal of unrepresentable absolute Schedule and Activity duplicates with visible child content, plus focused tests. This is **not full Event Inspector/Edit/Duplicate parity**: still requires Event metadata modification, full Activity hierarchy/recurrent-template fidelity, other stored Event fields and full acceptance. Defer all validation requests until a coherent M4 block is complete, then one consolidated user-local gate. M5/B15 remain open. No GitHub Actions/CI.

## 2026-10-08 — M4 whole-block candidate assembled; ONE user-local gate outstanding

The M4 Event post-create edit/duplicate vertical is assembled on the GitHub branch. This entry **supersedes the earlier incomplete-M4 candidate cursor**; no local tests are claimed for the newly added code. New canonical `20261008_128_b14_m4_event_profile.py` (only one Alembic `_128` revision) owns immutable Event metadata revision history, actor/CAS/replay, with an explicit no-unscoped-recurring-source edit veto. The Event read exposes a canonical profile revision. `event_api.py` accepts guarded Event metadata edits. Event Inspector now supports metadata Title/Description/Location/Color, existing B03 Agenda, B05 Life Area and B09 Participation owners without forging replacements for them. One new integration test `test_b14_m4_event_profile.py` covers owner, CAS, replay, history and current read.

Event Duplica uses canonical persisted Schedule placement and per-Event details, Life Area and expected participants. The Event DST disambiguation now retains the resolved earlier/later fold; cross-fold, invalid clock precision and absolute forms without faithful Create representation are rejected, never silently normalized. A new owner-scoped `remote-event-recurrence-guard.ts` checks the authoritative Event Recurrence before Duplicate, and explicitly blocks unfaithful template-to-one-off conversion; unresolved participants likewise block. Activity Duplica checks authoritative persisted child count and occurrence provenance, not just displayed subitems, and refuses structures/series that cannot be fully reconstructed, preserving all existing Actual/Observation/Evaluation/Session history. These refusals are **known capability limits**, not claims of full copying of complex trees or series.

**Canonical DB target _128:** 235 tables, 5 views, 210 routines, 103 triggers, 479 indexes, 416 FKs, 587 CHECK. Dictionary scope/routine/table and exact current catalog expectations are updated. Backend+Web tests added/extended; OpenAPI/Orval generation for the new Event profile endpoint still needs publication from user-local checkout, not a manually authored generated client.

**Single consolidated verification:** user runs `bash tooling/verify-b14-m4-local.sh` in `~/projects/dante`, with PostgreSQL, Ruff, unit, API export/client determinism, TS and relevant Vitest. Logs and concise result codes remain visible; the script conditionally publishes **only** verified generated client files after all gates pass, with no CI/Actions. If red, fix all real failures before another whole-block gate; no micro-gates. M4 is **candidate / awaiting this one local gate**, not green. Then perform M5/B15 real-UI click-through; the separate M3 global `Questa e le prossime` owner-source policy for Life Area and planned Session labels remains an explicit B14 parity debt before B15. No misleading "fully complete" claim.

## 2026-10-08 — M4 first user gate, focused repair pending complete rerun

User-local gate at `244ecaef` returned green `PULL/SYNTAX/UNIT/POSTGRES/GENERATE/GENERATED_CHECK/API_TYPECHECK`, red `RUFF=1`, `WEB_TYPECHECK=2`, `VITEST=1` (66/67). The reported failures were two import blocks, three TypeScript test errors and one stale Italian Event Agenda accessible-name assertion. The consolidated repair formats those imports, uses valid Testing Library exact-name regexes, guards optional fetch-init access, and checks Agenda actions across the two existing Italian label variants. Local Ruff, Web typecheck and all 67 selected Web tests now pass. Only source/test/docs changed; the first gate's generated client was intentionally not published. Await a **single whole-block user-local rerun** via `bash tooling/verify-b14-m4-local.sh` after pulling the repair. M4 remains unverified until that rerun and M5/B15 visual acceptance remains separate.

## 2026-10-08 — M4 integrated technical gate GREEN; client published

**This supersedes the preceding M4 pending-gate checkpoint.** The user's WSL `bash tooling/verify-b14-m4-local.sh` returned zero for all ten stages: `PULL`, `SYNTAX`, `RUFF`, `UNIT`, `POSTGRES`, `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK`, `VITEST`. Log directory `/tmp/dante-m4-whole.5cpYvA`. The verified seven-file Event profile OpenAPI/Orval output was committed and pushed by the gate as `77968de6` (`M4_CLIENT_PUBLISH=OK`); remote branch readback matches. M4's implemented Inspector/edit and supported duplicate paths are technically user-verified, with the explicit refusals for unsupported complex duplication intact. **Next:** one real-app M5 visual/keyboard walkthrough and defects, then B15 parity/closure review. No additional M4 micro-gates. `Questa e le prossime` for owner-domain Life Area/planned Session labels remains guarded, unimplemented global B14 debt, and the automated gate is not visual acceptance. Read `docs/workstreams/timeline-temporal-operational-m4-delivery.md` for the M5 journey. No CI/Actions.

## 2026-10-09 — M5 Session editor, validation and Objective Inspector repair candidate

User real-app screenshots exposed three defects after the green M4 technical gate: Edit's planned-Session clock controls inherited broad Timeline input/button styling, Create showed an English range paragraph with a misplaced section-wide red outline, and entering a numeric Objective observation in Inspector opened the error boundary. The Web candidate excludes the shared Session clock controls from those broad editor selectors, removes the Edit-only offset, localizes the bounded structure message, and targets the invalid Session's date/time row. Numeric Objective input now snapshots the DOM value before React's deferred state updater. A dedicated Inspector regression records `8 km`; targeted Create validation checks outside-range and reversed Session times, and a form test confirms the inline Italian error and precise invalid row.

Coding-workspace proof: Web typecheck, changed runtime/new-test ESLint and four focused Vitest files (54 tests) pass. The older Create entry test file has pre-existing ESLint violations and was excluded from this lint command; its tests are included. No user WSL run, real-app visual proof, or PostgreSQL proof is claimed for this candidate. Alembic `_129/_130` untimed planned-Session persistence and Docker-assigned acceptance port are already on branch HEAD `ec648022`, but their user-local PostgreSQL/catalog gate remains pending. M4 stays technically green, M5 remains open, and B15 parity debt for `Questa e le prossime` Life Area/planned Session labels remains unchanged. Run one consolidated affected gate after publication; no CI or extra M4 gate.

## 2026-10-09 — User-local M5/untimed acceptance gate, Ruff repair pending

After pulling `b1b74c6d`, the user's WSL gate reported 13/13 PostgreSQL integration and exact-catalog tests passing on `_130`, Web typecheck passing, and 54/54 focused Vitest tests passing. Ruff alone reported four style violations in `test_b14_u2_authoring.py`: literal dict, compound assertion, and two intentionally naive datetimes for floating-local placement. The focused repair preserves test semantics and marks those two datetimes with `DTZ001` exemptions. This repair is not yet user-local Ruff verified; no second PostgreSQL/Web run is needed solely for this test-style change. The Create entry test also emitted an existing React cross-component setState warning while all tests passed; track separately from this blocking Ruff gate. M5 visual acceptance remains open; B14 source-following Life Area/planned Session naming remains guarded.

## 2026-10-09 — M5/untimed focused technical gate GREEN

The user pulled `0754ba1e` in WSL and reran the exact focused Ruff selection; **All checks passed**. The preceding run on `b1b74c6d` had already passed 13/13 PostgreSQL integration and exact-catalog tests, Web typecheck, and 54/54 focused Vitest tests. The intervening commit changed only test lint/syntax and documentation, so this completes the bounded technical gate without repeating green PostgreSQL/Web checks. The React cross-component update warning seen in an existing Create-entry test remains a non-failing follow-up observation. Next: the user inspects planned Session clock layout in Activity Edit, the localized precise range validation in Create, and numeric Objective input/recording in Inspector in the real app. M5 visual acceptance and B14 source-following `Questa e le prossime` parity debt remain open; no CI/Actions.

## 2026-10-09 — M5 Edit follow-up candidate, local gate pending

Real-app feedback after `5fcbe7e` reports inability to remove an existing planned Session, a stuck placement lock save, stale runtime Session controls, creation-only type choices in Edit, duplicate/misaligned Description, missing new Life Area creation, and renewed Objective crash. This candidate adds `_132` owner-scoped planned-role retirement (history retained, recorded execution veto, active-role filtering), fixes the first-lock CAS basis `0 → null` and finite request wait, invalidates card capability after capture-policy save, positions Inspector runtime controls by the title, removes the type selector from Activity Edit, simplifies Description, and creates then assigns a new Life Area from Edit. New backend and Web regressions cover the main changed paths. Static Web typecheck and Python compilation passed in the coding workspace; **the user-local Ruff/PostgreSQL/Vitest gate, migration, generated API contract publication, and real-app visual checks remain pending**. The renewed Objective white page has no `Show Error` trace, so its cause is unconfirmed and it remains open. M5/B15 stay open. No CI.

## 2026-10-09 — M5 whole-block technical candidate assembled

The source-generated OpenAPI/Orval client now includes the `_129`–`_132` Activity planning request and snapshot shapes, including distinct `delete_planned_sessions`; two consecutive source generations produced identical file hashes. `_131`'s unproven candidate PL/pgSQL record declaration matches the user's earlier local correction. `_132` rejects placement of a retired planned row; a PostgreSQL regression now asserts this guard. The Web request expectation includes the delete field, and deferred React input updaters in Activity planned names and Event metadata snapshot values before scheduling state. Workspace evidence: Ruff on changed backend files, Python compilation, 23 backend unit tests, 75 focused Web tests, API/Web typechecks, and generated determinism passed. PostgreSQL/catalog and real-app acceptance remain user-local and unproven. Run **one** gate: `bash tooling/verify-b14-m5-local.sh`; it performs no commit, push or CI. The renewed Objective report has only a generic boundary screenshot; numeric Inspector entry is guarded and regression-tested, but a further crash requires its `Show Error` detail. M5/B15 and source-following Life Area/planned-name parity remain open.

### 2026-10-09 — Activity Edit planned time and Timeline runtime candidate

The Activity Edit `Orario` switch now adds or withdraws a planned Session time through coordinated preview/apply. A new guarded `_131` placement capability preserves the Schedule identity when timing an unplaced planned row, including after a previous unschedule; the edit snapshot keeps untimed planned rows visible. New planned rows may be saved without a time. Core Edit requests have bounded database and web timeouts with an Italian retry error instead of an endless spinner. Timeline Activity cards show a combined Play/Pausa button and Stop. Workspace web typecheck and 40/40 focused Vitest tests pass; Python syntax and diff checks pass. PostgreSQL/Ruff and real-app acceptance await the user's local gate. No CI/Actions.

## 2026-10-09 — M5 PostgreSQL gate failures repaired, user-local rerun pending

After the candidate commit `2a30359`, the user-local `bash tooling/verify-b14-m5-local.sh` run reported green `PULL`, `SYNTAX`, `RUFF`, `UNIT`, `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK`, and `VITEST` (75 focused Web tests). `POSTGRES` remained red for two verified source defects: `activity_replan_api.py` zipped all free planned-Schedule order slots against fewer new Sessions with `strict=True`; `test_database_current_catalog.py` still expected pre-_131/_132 Dictionary totals and omitted their two completed-stage markers. Both are fixed on the same feature branch by commits `604459a9` and `677ea8d1`, respectively. The first change takes exactly as many free slots as newly requested planned Sessions; the second aligns exact assertions to Alembic `20261009_132` and Dictionary `236 tables / 5 views / 214 routines / 103 triggers / 482 indexes / 420 FKs / 589 CHECK`, including `B14-PLANNED-SESSION-TIME-EDIT` and `B14-M5-PLANNED-RETIREMENT`. No database migration or generated client artifacts were modified during this repair. The `_131` `DECLARE prior record;` correction was already present on the remote branch.

**Status: REPAIR PUBLISHED / POSTGRES RERUN PENDING; NOT GREEN, NOT M5 CLOSED.** Next: the user pulls the latest feature branch and reruns the single affected PostgreSQL selection from `tooling/verify-b14-m5-local.sh` (Activity replan, U2 authoring, Activity edit snapshot, M2 objectives, current catalogs), plus the selected Ruff file check if desired. Preserve any local worktree edits before pulling; never reset or overwrite user changes. If PostgreSQL is green, accept the consolidated M5 technical candidate without rerunning unrelated previously green Web/API gates, then complete real-app visual/keyboard acceptance (including the unresolved Objective white-page report if reproducible). B14 source-following `Questa e le prossime` for Life Area and planned-Session names remains guarded and not implemented; B15 remains open. No CI/Actions.


## 2026-10-09 — M5 Objective editor one-save candidate; local verification required

The user requested direct editing of existing Objectives by expanding their row, a single **Salva modifiche** after adding/changing/removing Objectives (no intermediate confirmation), and an **×** removal affordance per row. The branch candidate implements these in `apps/web/src/features/home/ui/timeline/activity-objective-row.tsx`, `activity-edit-panel.tsx` and their style/tests. The previously separate Objective definition actions were folded into Activity Edit submit. Draft additions have no server side effects until the final Save; removal is staged and undoable. Recorded-result correction remains a separate factual-history operation and was not silently rewritten as a definition edit.

The new **Objective-only** `PUT /api/v1/temporal/activities/{subject_ref}/objective-edits` API uses a *single SERIALIZABLE database transaction* to apply all newly authored, revised and retired Objective definitions. It uses existing owner-scoped Objective create/revision/source-policy functions; the new forward-only `20261009_133_b14_objective_retirement.py` adds a retirement tombstone and an owner-scoped function with definition CAS, replay and veto of any recorded Observation/Evaluation or template-generated recurring Objective. Retired Objectives remain in historical storage, but active read/definition capabilities no longer return them. The database Dictionary, SQLAlchemy mapping and exact-catalog expectations have been reconciled to `20261009_133`: **236 tables / 5 views / 215 routines / 103 triggers / 482 indexes / 420 FKs / 589 CHECK**, standalone **456**. New Objective batch command and precise veto response are in `reality_objective_api.py`.

The remote Web Objective batch call has a bounded 20s timeout, stable per-row operation IDs and retained CAS basis for retries. The general Activity Save visually drives the Objective batch without extra buttons. **Important domain boundary:** the batch is atomic *among Objective changes*; other domain-owned edits on the same Activity continue using their established guarded commands and are **not a single cross-domain database transaction**. Do not claim a global atomic Activity save. Unsupported source-wide deletion is refused, and a recorded Objective cannot be erased. Existing selected/following Objective definition scopes remain available only with verified template provenance; the unrelated Life Area/planned Session following-source parity debt remains open.

**Current status: CODE/TEST/DOCUMENTATION CANDIDATE ONLY; ZERO NEW USER-LOCAL PROOF.** The preceding `_132` M5 PostgreSQL selection passed **26/26** in the user's WSL, but this new `_133` candidate is not covered by those 26 tests. Run **one complete local gate** via `bash tooling/verify-b14-m5-objectives-local.sh` on `~/projects/dante` (Ruff, syntax, PostgreSQL new Objective batch/history and existing regression/catalog, deterministic generated API, API/Web typechecks and focused Vitest). The script does not commit/push and does not trigger CI/Actions. A new OpenAPI/Orval client artifact is expected from `pnpm api:generate` and must be published only after a green gate; never hand-edit generated files. Follow with real-app visual/keyboard acceptance including the earlier Objective white-page report. Neither M5 nor B15 is closed.


### 2026-10-09 — M5 Objective editor first user-local gate: PostgreSQL GREEN / Web parse + Ruff repairs published

The user's first `bash tooling/verify-b14-m5-objectives-local.sh` run returned **PULL=0, SYNTAX=0, POSTGRES=0, GENERATE=0, API_TYPECHECK=0** at Alembic `20261009_133` (covering new Objective batch/retirement tests, prior M2, Activity edit snapshot and exact Dictionary/catalog). **RUFF=1** for exactly two reported issues: `RUF001` right-curly apostrophe in the new backend error text and `PT018` combined tombstone assertion in the new test. **GENERATED_CHECK=1, WEB_TYPECHECK=2 and VITEST=1** because the Activity editor had one unmatched JSX `</div>` after the Objective correction block (at the formerly reported line 1245); Vite/OXC could not parse that source. The separate unaffected Web test files passed 12 tests. User log `/tmp/dante-m5-objectives.CAzpn9`.

The three verified source failures have been corrected directly on the feature branch: remove exactly the orphan closing `</div>`, replace the ambiguous apostrophe with a straight apostrophe and split the tombstone test assertion. **These repairs have no new PostgreSQL business/schema changes** and do not justify repeating the already passing  `_133` PostgreSQL gate. No Web PASS is claimed: perform one focused **Ruff + generated/check + Web typecheck + focused Vitest** local rerun after pull, then close the technical gate only if green and publish the generated API client separately. The first generation modified two preexisting files and created four new Orval model files locally; preserve these user files and never reset/clean the worktree. Real-app acceptance/old Objective error boundary, M5 and B15 remain open; no CI.

### 2026-10-09 — M5 Objective editor second user-local gate: Web/TS tests repair published

The user pulled `b213aa7d` and ran the **focused** follow-up. **Ruff PASS**; **generated:check PASS** (OpenAPI/Orval generated files deterministic, 508 files); Vite production build PASS (chunk-size warning only). Web typecheck reported precisely **three TS2552 references** to `objective` in two new tests under the `Activity Inspector` suite: the fixture had been declared inside the preceding `Objective correction in Activity Editor` suite. Focused Vitest reported **45 passed / 3 failed**: two fixture-scope ReferenceErrors, plus an accessible-button-name mismatch (UI is `＋ Aggiungi obiettivo` while the test required exactly `Aggiungi obiettivo`). The untouched Web settings/control tests passed.

Commit `330fc5a0` moves the shared Objective fixture to module scope and adjusts the add-button query to match the visible accessible name. These are **test-only** changes; no backend/migration/business code altered. **Awaiting one focused user-local rerun of Web typecheck and focused Vitest; do not repeat already-green PostgreSQL (previous gate), Ruff or generated:check.** The generated client files remain only in the user's local worktree, pending publication; never remove them with reset/clean. Full B14 M5 and B15 closure remains dependent on real-app acceptance and previously documented scope parity.

### 2026-10-09 — Objective editor M5 focused technical gate GREEN (user WSL)

The user pulled `0d2c71c2` and reran the exact focused Web gate. **Web typecheck: PASS (exit 0); focused Vitest: 3/3 files, 48/48 tests PASS.** The preceding user-local gates on the same `_133` Objective editor candidate already proved PostgreSQL integration/catalog PASS, Ruff PASS, API typecheck PASS, and deterministic OpenAPI/Orval `generated:check` PASS (508 files). The test-only repairs `330fc5a0` do not alter backend/domain behavior. This **closes the bounded Objective-editor technical gate**; do not rerun completed PostgreSQL/Ruff/TypeScript/Vitest checks just to repeat the same evidence.

**Publication still outstanding:** Generated API artifacts exist in the user's WSL worktree, not on GitHub: tracked modifications to `packages/api-client/openapi/dante-v1.openapi.json`, `packages/api-client/src/generated/dante.ts`, `packages/api-client/src/generated/model/index.ts`; new `packages/api-client/src/generated/model/{activityObjectiveBatchCommand,objectiveBatchRetirement,objectiveBatchRevision,temporalApplyActivityObjectiveEditsBody}.zod.ts`. The client is deterministically source-generated and already checked. Publish **exactly these seven files** without resetting/cleaning any local worktree data. The GitHub connector cannot access the user's uncommitted WSL bytes. No CI. Then real-app acceptance of Objective editing (inline expansion, new, edit, X/remove/undo, Save, error/retry) remains; larger M5/B15 closure and recurring source-following parity debts remain open.


### 2026-10-09 — M5 Objective API generated artifacts PUBLISHED

The user completed the exact seven-file Orval/OpenAPI publication on the feature branch in commit `f950d22f7d51d432a02b7527dc6ee322fe06d3de` (`chore(api-client): publish B14 M5 Objective API [skip ci]`). GitHub comparison against `c44e9a0b` confirms **one commit ahead, exactly seven generated API client files**, with no other changes in that publication. The user-local command ended with no `git status --short` entries, consistent with a clean worktree at that point. **The Objective editor bounded technical gate is green, and source-generated API publication is complete.** No more migrations, Ruff, PostgreSQL, code generation, typechecks or repeated Vitest are required solely for this accepted technical gate. Next: inspect the running app and manually validate new Objective rows, direct editing, removal/reinstatement, Save, recorded-history veto and error feedback; report concrete defects before marking M5 visually accepted. The remaining B14 source-following parity and B15 close-out remain explicitly open; no CI/Actions.


### 2026-10-09 — M5 real-app visual feedback: sessions, Title, Objectives, Life Area color (candidate)

Real-app screenshots after the green `_133` Objective editor gate and published Orval client `f950d22f` exposed four remaining issues: adding timed or untimed planned Sessions reports a generic planning conflict when the Activity has placement protection enabled; Activity Edit's Title has a second nested rectangular border; existing Objectives are collapsed and show their name twice (row header plus input); newly created Life Areas from Activity Edit display a color briefly, then Timeline falls back to gray.

The bounded follow-up candidate (no schema migration or generated API changes) changes `activity_replan_api.py` so **new planned Sessions within an unchanged, already accepted Activity envelope** are authorable while the envelope is locked. Movement of *existing* Schedule coordinates, removals and interval edits continue to require unlocking; open execution/recorded Actual veto remains. New PostgreSQL regression covers a locked Activity with one new untimed and one new timed Session, verifies the envelope state is unchanged and a subsequent move still conflicts. The existing user screenshot had an enabled “Sblocca spostamenti” control; this is the identified root guard rather than a UI-only error.

The Activity Edit Title CSS now removes its nested label/input borders while preserving one controlled outer border and responsive layout. Every Objective (new and existing) shows a **single editable name field** and all its other definition controls immediately; no duplicate static heading or extra expand step. Series-origin lookup is deferred until focus, and the same Object definition CAS/one-button Save/history veto semantics remain unchanged. Activity Edit Life Area choices carry canonical revision/appearance metadata; creating a new Life Area now sets its canonical area appearance color with owner-scoped revision before assignment, and an explicitly selected color for an existing Life Area is persisted through the same capability rather than changing only the item's color. A colorless existing Life Area shows a neutral gray swatch instead of misleading orange. Failed appearance writes retain pending draft and error for retry. **Create authoring already routes new-Life-Area color through `resolve_authoring_life_area` in the existing backend; its reported real-app color behavior still needs confirmation after this fix, not a made-up backend change.**

New/refocused tests: `test_b14_activity_replan.py` locked new Session acceptance/protection veto; `activity-inspector-actions.test.tsx` always-visible Objective inputs, timed/untimed Session edits, newly created Life Area appearance and existing Life Area color change; `remote-activity-edit-settings.test.ts` appearance revision persistence/CSRF and catalog metadata. **CANDIDATE, NOT VERIFIED**: the previously green Objective gate does not prove this new behavior. One user-local affected gate should include Ruff, the new PostgreSQL test, Web typecheck and both focused Vitest files; no need to rerun earlier broad suites or regenerate the API client. Then real-app visual and persistence acceptance; M5/B15 remain open and recurring owner-field `Questa e le prossime` parity is unchanged. No CI/Actions.

### 2026-10-09 — M5 four real-app fixes: USER-LOCAL GATE GREEN, visual acceptance pending

User pulled branch to `497e8b1a` and ran `bash tooling/verify-b14-m5-ui-acceptance-local.sh` in WSL. The reported consolidated result is **PULL=0, SYNTAX=0, RUFF=0, POSTGRES=0, WEB_TYPECHECK=0, VITEST=0**; full logs at `/tmp/dante-m5-ui.xsV9uI`. The new locked-Activity timed/untimed Session regression, always-open Objective editor and Life Area appearance path are covered by this affected gate. **The M5 follow-up technical gate is VERIFIED GREEN**; do not rerun it unnecessarily.

**What is still open:** real-app manual acceptance of (1) adding both timed and untimed planned Sessions while keeping locked placement unchanged, (2) the single, correctly aligned Activity Title field, (3) always-open Objectives with only one editable name and one general Save, and (4) persistent Life Area colors after saving, Timeline refresh and reopening, including new area creation. Existing protection of historical truths and source-scoped editing rules must remain intact. Product/UI acceptance, M5 and B15 overall are **NOT YET CLOSED**, despite automated green results. User will report visual outcomes. No database revision, Orval regeneration or CI was needed for the four-defect fix.

GitHub workflow: assistant publishes docs/code to `feature/timeline-temporal-operational`; user does **explicit `git pull --ff-only origin feature/timeline-temporal-operational`** in WSL. Always provide the pull command separately before any local action.


### 2026-10-09 — B14 Draft Vault («Bozze») whole-block implementation CANDIDATE

User-approved product shift: retire “Da collocare” as an *authoring choice*; introduce an actor-owned inert Draft Vault for possible future Activity and Event, with full Quick/Advanced Create field snapshots (including uncommitted Session/Objectives/recurrence settings). `Salva bozza` beside `Aggiungi` in both Create surfaces; discard dialog now offers Save draft. Explicit Add authors accepted subject through the existing path; the original draft is removed only after success. Resume and Duplicate reopen the same Create editor; Delete removes inert snapshot. Drafts do **not** establish Activity/Event/Schedule/Session/Actual/reminders or recurrence: see `docs/domain/concepts/draft-vault.md`.

New *forward-only* PostgreSQL `20261009_134` adds `dante.temporal_draft_vault` owner-only table and 3 SECURITY DEFINER CAS/replay/list/delete functions with dante_runtime EXECUTE but no direct table privileges. New `/api/v1/temporal/drafts` authenticated API, TypeScript remote source, Home vault panel, Create integration and tests. Updated Dictionary/SQLAlchemy/catalog to **candidate 237 tables, 5 views, 218 routines, 103 triggers, 484 indexes, 420 FKs, 593 CHECK constraints** (new table + 3 funcs + 1 PK index + 4 CHECK). **Counts are expectations, not user-proven until PostgreSQL gate.** OpenAPI/Orval generated API client files must be published separately after deterministic generation. Local full affected gate scripted in `tooling/verify-b14-draft-vault-local.sh`, no CI or automatic push.

**Historical protection and gaps, explicitly OPEN:** the old planning tray holds *real* canonical unplaced/postponed Activity/Event identities. These remain distinct legacy canonical records, not silently moved or deleted as drafts; the vault exposes an explicit **Gestisci elementi già creati** handoff to the unchanged B01 placement/replan controls under a separately titled **Elementi già creati** panel (its old trigger is hidden). Inspector “Sposta in Bozze” for Activity uses existing canonical retirement guard, preserving history; moving real Event is **not yet supported** because Event has no matching safe retirement capability, so the Event Inspector visibly says “Copia in Bozze” and keeps the original. Do not treat this as Move or mark the full legacy transition accepted. Full Event move needs explicit follow-up owner-retirement capability without corrupting accepted facts. User visual and end-to-end acceptance remains **NOT VERIFIED**, including real app, keyboard interactions, and previous M5 regression checks. No new Timer/Alarm operational functionality. Avoid claiming B14/B15 or Bozze closed.

**User workflow:** Assistant writes and updates `feature/timeline-temporal-operational`; user performs explicitly displayed `git pull --ff-only origin feature/timeline-temporal-operational` in WSL. User runs a SINGLE COMPLETE local gate; do not request CI. User is not asked to push source changes except genuinely local generated OpenAPI artifacts that cannot be read by the connector.


### 2026-10-09 — Draft Vault first user-local gate FAILED; focused repair pending recheck

After pulling `16fdb7ed`, the user ran the single `tooling/verify-b14-draft-vault-local.sh` gate (log directory `/tmp/dante-draft-vault.dBVhHO`). Results: **SYNTAX=1, RUFF=1, POSTGRES=1, GENERATE=0, GENERATED_CHECK=1, API_TYPECHECK=0, WEB_TYPECHECK=2, WEB_VITEST=1**. Precisely observed root blockers: unterminated `_RETIRE` Python SQL literal in migration `20261009_134` (all 10 PostgreSQL cases could not load Alembic); misordered `draft_vault` / `confirmation` imports; incorrect `../../platform/api/web-fetch` reference from `features/temporal-create/application` (Vite build and 5 Vitest suites failed during module import). Four Web suites **ran and passed 11 tests**; the 5 unresolved suites **have not yet been verified**. Fixes were pushed in GitHub commits `dbfa1a89`, `01cf064b`, `20e5c351` respectively. This was NOT a green Draft Vault gate, and these focused fixes still need a new user-local gate. 

Seven generated API files were produced in the user's WSL (`packages/api-client/openapi/dante-v1.openapi.json`, `src/generated/dante.ts`, `model/index.ts`, plus four new `draftVaultResponse.zod.ts`, `draftVaultSaveRequest.zod.ts`, `temporalRetireDraftParams.zod.ts`, `temporalSaveDraftBody.zod.ts`). **Preserve the local modifications, do not reset them.** They are not yet published to the branch; assistant cannot read uncommitted WSL bytes through GitHub. Next: user performs explicit `git pull --ff-only origin feature/timeline-temporal-operational` (new commits do not touch generated files), then reruns the one local `bash tooling/verify-b14-draft-vault-local.sh` gate. Evaluate any newly exposed failures as one coherent repair round, not micro-gates. Overall Bozze candidate remains open, with Event Move parity and real-app visual acceptance pending.


### 2026-10-09 — B14 Draft Vault second local gate: all Web and generation GREEN, 3 PostgreSQL fixes pending

User-local run at `/tmp/dante-draft-vault.4KmEkB` after pulling `e65be88c`: `SYNTAX=0`, `RUFF=0`, `POSTGRES=1` (**7 passed, 3 failed**), `GENERATE=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`, `WEB_TYPECHECK=0`, `WEB_VITEST=0`. All tested front-end suites, OpenAPI generation, deterministic source checks and lint pass; do not rerun them merely to prove these backend-only corrections. Two PostgreSQL failures were caused by missing explicit `session.begin()` in `draft_vault_api.list_drafts` and two read sessions of `test_b14_draft_vault.py`; this runtime has autobegin disabled. Third failure was stale hard-coded `(236,5,215)` assertions in `test_database_current_catalog.py`; other counts and the `B14-DRAFT-VAULT` stage assertion in that file would also have been stale. GitHub commits `2e12ddb8`, `6c9854f4`, `7f61a076` respectively fix all three files and all stale hard-coded catalog assertions (expect 237 tables, 5 views, 218 routines, 484 indexes, 593 checks, 237 SQLAlchemy mappings). Code review confirms the read sessions now begin explicit transactions and no old count literals remain in the focused catalog test. **Not yet re-run locally; do not mark PostgreSQL gate green.** Next: user performs *separate explicit* `git pull --ff-only origin feature/timeline-temporal-operational`, preserving the existing seven locally generated API artifacts, then runs just `cd apps/backend && uv run --locked pytest -q --no-cov --tb=short -m postgres tests/integration/temporal/test_b14_draft_vault.py tests/integration/database/test_current_catalog.py tests/integration/database/test_database_current_catalog.py`. If green, publish seven generated API client artifacts from the user's WSL and manually verify Bozze. Event Move parity and existing-items legacy handling remain open; no CI.


### 2026-10-09 — B14 Draft Vault TECHNICAL GATE GREEN (user-local WSL)

After pulling GitHub branch head `59547421`, user ran `uv run --locked ruff check` on the three amended backend files (**All checks passed!**) and `uv run --locked pytest -q --no-cov --tb=short -m postgres` across `test_b14_draft_vault.py`, `test_current_catalog.py`, `test_database_current_catalog.py`: **10 passed in 23.76 seconds**. This completes the PostgreSQL repair gate. The immediately preceding full Draft Vault gate had **SYNTAX=0, RUFF=0, GENERATE=0, GENERATED_CHECK=0, API_TYPECHECK=0, WEB_TYPECHECK=0 and WEB_VITEST=0**; the only failing component was PostgreSQL, now green. **Technical candidate gate is GREEN based on those combined user-local results.** Do not request redundant full reruns for unchanged Web/source.

**Release handoff NOT YET COMPLETE:** Orval/OpenAPI generator created **seven local uncommitted artifacts in user's WSL**, not yet in GitHub feature branch: `packages/api-client/openapi/dante-v1.openapi.json`, `packages/api-client/src/generated/dante.ts`, `packages/api-client/src/generated/model/index.ts`, `packages/api-client/src/generated/model/draftVaultResponse.zod.ts`, `packages/api-client/src/generated/model/draftVaultSaveRequest.zod.ts`, `packages/api-client/src/generated/model/temporalRetireDraftParams.zod.ts`, `packages/api-client/src/generated/model/temporalSaveDraftBody.zod.ts`. Preserve and publish **only** these generated files with `[skip ci]`; they are the deterministic result of the passing generator and are not GitHub-accessible until user uploads or pushes them. Avoid reset/clean of user worktree. Assistant documents green gate on remote, then user explicitly pulls docs (pull does not overlap the seven generated paths); user can push precisely those seven files or supply the generated artifacts for assistant to publish. Once generated artifacts are published, manually accept Create Quick+Advanced Save, durable vault reload, Resume, Duplicate, explicit Add/consume, Delete, legacy existing-item placement, guarded Activity move. Real-app user acceptance **PENDING**; Event canonical Move is not supported (Copy into Bozze preserves original). This does not close overall B14/B15 or previous M5 visual acceptance.


### 2026-10-09 — B14 Draft Vault generated client PUBLISHED; TECHNICAL GATE COMPLETE, visual acceptance OPEN

The user successfully rebased their local `chore(b14-drafts): publish generated API client [skip ci]` commit onto GitHub `3f25c130` and pushed it as **`a3271cf9`** to `feature/timeline-temporal-operational`. GitHub comparison confirms this was precisely **one commit containing seven generated client files**: OpenAPI `dante-v1.openapi.json`, generated `dante.ts`, `model/index.ts`, and four newly generated draft Zod models. The user's `git status` reported **clean and aligned with origin**. Together with prior user-local proof (**10 PostgreSQL tests passed, Ruff green, full Draft Vault Web/Typecheck/Generate gates green**), **Draft Vault candidate technical verification and generated artifact publication are COMPLETE**. Do not repeatedly ask for old gates, commits or CI.

**NEXT: real-app acceptance, NOT YET CLAIMED**. Ensure the actual local DANTE database is migrated to `20261009_134` before running the app (the previous PostgreSQL pytest gate created temporary migrated databases, not necessarily the persistent local instance). Check Quick and Advanced Create → Save draft without operational persistence; refresh/reopen saved drafts; Resume full configuration; Duplicate retains original; Add explicit confirm consumes only source draft after accepted creation; Delete requires confirmation; locked inert Session/notification/recurrence behavior; and legacy canonical ‘Elementi già creati’ remain distinct, safely placeable. Retire an existing Activity only where history guard permits. Existing Events currently support **Copia in Bozze**, not canonical Move; Event retirement parity and prior M5 real-app verification remain open. No Timeline/Home H0 cosmetic refactor, no CI. Assistant source/docs pushes require user-visible, standalone `cd ~/projects/dante && git pull --ff-only origin feature/timeline-temporal-operational` before local app check.

## 2026-10-13 — B14 focused repair from uploaded WSL logs

Observed local run at `594c85c3` from user-provided `TYPECHECK.log`, `VITEST.log`, `BROWSER.log`, `REAL_STACK.log`: Web typecheck 2 (four errors in Draft Vault fixture), focused Vitest PASS 9/9, fixture browser 12 failed / 3 passed, real stack 11 failed / 3 passed across Chromium/Firefox/WebKit. This is **not** a green full gate.

Repair batch published on `feature/timeline-temporal-operational`:

- Playwright Draft Vault fixture invokes `route.request()` (the previous destructuring read the method itself, causing TS2339 and cascading fixture runtime errors).
- Browser selectors use exact accessible names for Create `Aggiungi` and recurrence `Ripeti`. Unplaced Activity real-stack reads consistently include `X-Dante-Time-Zone`.
- The existing product CSS deliberately hides speculative Timeline previews until committed; B14 browser acceptance now explicitly checks that policy and verifies the resulting committed card.
- Create start-time edits that cross the old same-day end retain their prior duration rather than silently creating a next-day interval. Context E2E now asserts 15:00–15:45 for the 45-minute flow. Created card metadata preserves the Life Area label as well as its colour. Quick Create rail is bounded to viewport height.
- The legacy advanced Event fields (free-form provider options, Scopo, etc.) are intentionally unavailable in the accepted U2 UI. The affected browser scenario now tests **actual U2 Scaletta**, participant-referent staging, description round-trip, and committed Event card; it does not assert removed fields.
- Authoritative Event browser tests explicitly reload and assert Schedule presence in the canonical GET response before comparing rendered cards; this diagnoses persistence vs. hydration rather than accepting an optimistic result. Email worker failure loops now back off on a temporarily unavailable PostgreSQL during destructive outage tests.

**Verification still required:** no WSL browser/PostgreSQL/TypeScript runner is available in this GitHub-editing environment. No all-green claim; rerun the full 27-group same-SHA gate, inspect new failure logs if any and preserve original assertions. Separate root cause analysis may still be needed for the all-day Create failure and the destructive outage recovery timeout; neither is marked resolved without a fresh run.

## 2026-10-13 — Second focused B14 WSL gate (0937dadf; partial)

User-provided complete logs `B14_REPAIR_LOGS.tar.gz` from `0937dadf042243fe3caca9f9b70bf243b851cdbb` show `TYPECHECK=0`, `VITEST=0` (focused suites), `BROWSER=1` (6 PASS, 9 FAIL), `REAL_STACK=1` (9 PASS, 11 FAIL, 1 historical B03-E WebKit SKIP). The run was **8.2m** in real-stack. This is a genuine red gate, not acceptable to declare green.

Root causes/repairs committed after that SHA:

- Four Draft Vault browser failures all targeted missing `Apri Bozze`: MODE=test omitted the product Draft Vault altogether. The actual component is now rendered in fixture builds while the preexisting fixture-only planning tray remains separately available. Tests still use an explicit isolated HTTP fixture and prove inertness, resume, duplicate and deletion.
- Desktop quick Create overflow reached y=1481 at 900px viewport: the absolute host inherited the full Context Rail height. Define a real viewport-bounded host height (not `max-height` alone).
- The non-auth browser fixture does not persist canonical new Life Areas or advanced U6 Activity structures and B03 legacy Event runtime rejects rich Notes. The fixture tests now assert staged input, preserved date/time values and **fail-closed** non-creation instead of expecting fabricated successful persistence. The full-stack U2 suites remain responsible for actual accepted authoring. **U6 advanced acceptance is not proven by these fixture tests; this is an outstanding verification obligation** and must not be presented as a closed B14 feature.
- Real B02 scheduling test waited for retired `/temporal/activities` and `/temporal/activities/scheduled` POSTs plus removed `Fascia`/native date input. It now authors truly canonical U2 Activities via authenticated HTTP, reloads before reading the existing-item inventory, and checks the same establish→move→cross-form→unschedule→Undo, all-day/coarse/named-zone PostgreSQL contracts. Coarse is API-only, not falsely described as a product Create option.
- B03-E Event full-stack timed/all-day creation and reschedule passed until **third multi-day Event**, where **no U2 POST fired**. Error reporting in the helper now prints actual form validation alerts and selected end/start dates instead of only a generic 10s timeout; the **multi-day authoring failure is still unresolved** pending that diagnostic.
- The deliberate real PostgreSQL outage ran into the global 60s UI timeout. That one test now has a bounded 120s Docker lifecycle budget, with its 500/error/explicit retry/200 assertions unchanged. This is not evidence recovery works; the next WSL run must establish it.

**Still no WSL test has been run after this batch.** Do not claim B14 or the 27-group full gate is green. Record exact post-fix SHA, collect the smallest affected browser/auth rerun before issuing another expensive full gate.

## 2026-10-13 — Third focused B14 check (68e52633)

The uploaded `B14_CHECK_LOGS.tar.gz` covers `68e526333b727c696bc8084e91676d98f2f5e2d7`, reporting `TYPECHECK=0`, `BROWSER=1` (11/15 pass), `REAL_STACK=1` (5/7 Chromium pass). **This is not a full green gate.** Browser failures: Context Rail quick composer box extends to y=1443 at 900px viewport; Draft duplication test asserts record count before async save completes; Draft Vault popup right boundary at x=401.97 on 390px viewport; generic 'Call cliente' card locator finds one already-present card in a non-auth negative-creation test. Real-stack failures: third multi-day Event never POSTs; PostgreSQL outage remained stopped for 120 seconds, causing a global test timeout.

Committed source-backed fixes after this baseline:
- Enforce viewport-derived height on the **composer itself**, not only its absolute host; bound mobile Draft Vault by fixed viewport edges.
- Await draft duplicate form closure before reading fixture state; assign the isolated Event UI scenario a unique nonseeded title.
- **Identified root cause for multi-day Event**: as Start date changes, the inactive `scheduling` default date fields remain anchored to the initial Create date. `temporalCreateU2QuickIntentSupported` incorrectly compared these semantically inactive dates against defaults for the new date, returned false and diverted the Event into B03 legacy runtime without a canonical U2 POST. `equivalentSchedulingForU2` now disregards **only** those four inactive default date values; all effective constraint kinds, movement and fallback policy, time policies and advanced options remain checked. Added a regression covering three-day 2026-10-15..17 Event and exact half-open date-span request.
- For the destructive real-stack DB outage, backend E2E database engine already uses a 1-second connect timeout and 5-second pool timeout. It remains **unresolved** why the frontend never observed a 5xx within the previous 120-second budget. The test now probes the authenticated Timeline endpoint with an explicit 12-second bound before UI navigation, independently bounds Home response and subsequent recovery response, and always restores the disposable database in `finally`. No skip or false success.
- A full 27-group gate is still required after B14 cross-browser passes; the older gate's broad Ruff/mypy/format/ESLint red inventory has **not** been cleared or remeasured against this new HEAD.

Verification remains pending on WSL. Never claim B14 closure until TYPECHECK, focused Vitest, Chromium browser fixtures and all required real-stack browsers pass. Then execute all 27 reference gate groups on the same SHA.

## 2026-10-13 — Fourth B14 check (bd50a5ae)

Uploaded `B14_FINALCHECK_LOGS.tar.gz` at exact SHA `bd50a5ae304076dc1f11b8c301c5f84899491bae` confirms TYPECHECK=0, focused VITEST=0 (11/11), BROWSER=1 (14 PASS / 1 FAIL), Chromium REAL_STACK=1 (6 PASS / 1 FAIL). Full-stack three-day Event creation, DaySpan readback, Draft Vault, and all previously failing canonical B02 Activity scenarios now pass **in Chromium**. No Firefox/WebKit or whole 27-group run has been certified on this SHA.

**Remaining browser failure:** `temporal-create-manual-hardening.spec.ts` desktop Context Rail quick composer, bounding box bottom y=1443.77 on 900px viewport. The Home Today layout starts after the 650px Hero, at approximately document y=724. Bounding the composer/host height to 720px did not help because the host remained anchored *below* the Hero. Committed desktop-only CSS in `home-u1-layout.css` making the rail-owned host viewport-fixed when Create is open (top 96px/right 18px/bottom 16px/width 475px) and disabling the Context Rail zero-offset CSS transform while open, because transforms otherwise create the wrong fixed-position containing block. Keeps DOM ownership and inside-rail horizontal alignment.

**Remaining Chromium real-stack failure:** `temporal-runtime-foundation.spec.ts` deliberate PostgreSQL stop + recovery. The authenticated direct Timeline GET probe correctly returned HTTP 5xx under outage. The UI test then waited 12s for a GET `/api/v1/temporal/timeline/window` that never fired. Root cause from `timeline-runtime-boundary.tsx`: each Timeline read **must first POST `/api/v1/temporal/occurrences/checkpoint`**. Under DB outage, that POST fails, so the frontend never calls GET and instead sets state `error`. Updated E2E to assert checkpoint failure and actual UI error instead. Also changed from full `page.goto` during outage to in-app Week Next UI navigation on the existing authenticated SPA, avoiding auth bootstrap being retested during DB-down. Test still requires: direct probe HTTP 5xx, checkpoint HTTP 5xx, UI shows 'Timeline non disponibile', zero stale cards, real DB restart, explicit 'Riprova', real GET HTTP 200, state ready. No mocking and no skipping.

These two latest fixes are **NOT yet WSL-validated**. A focused 2-test rerun with browser fixture and Chromium auth stack plus TYPECHECK is appropriate. Then verify Firefox/WebKit and run the 27-group full parallel reference gate. Older full-gate reference `6476a5c1` had nine failing groups (format, Ruff, mypy, repo format, ESLint, PostgreSQL, Vitest, browser nonauth and real-stack), so passing B14 **does not imply** full 27-group closure.

## 2026-10-13 — Fifth B14 focused closure check (4ad42f0f)

User-provided `B14_CLOSURE_LOGS.tar.gz`, `BROWSER.log`, `REAL_STACK.log`, and `SUMMARY.txt` confirm exactly SHA `4ad42f0f1506141bc044ddf698ffa4970678868d`: `TYPECHECK=0`, `BROWSER=1` (1/1 failed), `REAL_STACK=1` (1/1 failed), full gate **not started**.

- Browser geometry no longer fails for its previous y=1443 bottom; it fails first at `temporal-create-manual-hardening.spec.ts:37`: visible Create x=929.344px against Context Rail x>=946px. Fixed host has redundant `right:18px`; the 17px mismatch is consistent with the right inset being applied to a scrollable/rail-aligned fixed containing block. The editor is still owned by Context Rail. The next change eliminates the rail transform transition *while Create is open* and removes that extra fixed host inset, leaving `right:0`; retain strict x and right edge assertions.
- Real-stack outage: browser waits 12 seconds for POST `/api/v1/temporal/occurrences/checkpoint` and times out. `remote-timeline-read.ts` explicitly first calls GET `/api/v1/auth/session` for CSRF *before* any checkpoint POST; with PostgreSQL stopped, the authenticated session fetch itself can fail. The direct authenticated GET `/api/v1/temporal/timeline/window` probe returned a 5xx (else the code would throw a distinct error). Updated test to assert a real HTTP 5xx from the direct probe, require the *actual* UI `Timeline non disponibile` after in-app date navigation, require absence of stale events, restart PostgreSQL, click `Riprova`, demand a real 200 GET and ready status. Captures browser API responses in error diagnostics; **no mock, no skip, no removed outage or recovery assertions.**

Changes are not yet tested on user's WSL. Do not state these two tests or the 27-group full gate are green.

## 2026-10-13 — Sixth B14 focused verify (590bdd93)

The user supplied `B14_VERIFY_LOGS.tar.gz` for exact SHA `590bdd937cc841549f375dcc10d881dec8f04183`: TYPECHECK=0, Chromium real-stack outage/recovery PASS (1/1 in 22.6s), browser manual-hardening FAIL (1/1), full gate not started. The previously failing PostgreSQL disruption and explicit UI retry are now **verified passing** under a real disposable PostgreSQL stack.

The browser log now has exact element coordinates at viewport 1440×900: `railBox x=947..1422, y=724..1482`; `hostBox x=965..1440, y=96..884`; `quickBox x=965.344..1439.656`. Quick height is bounded; only horizontal alignment failed: the host is precisely 18px right of the measured Context Rail. With the ancestor transform disabled immediately (`transition:none;transform:none`), the fixed host now resolves against viewport. The fixed host must use `right:18px` for x=947, not `right:0` (x=965). Published that geometry fix.

Proactively traced subsequent Advanced expansion: desktop rail host is only 475px wide and overflow:hidden. Without a separate advanced CSS mode, the 1040px full-screen Advanced composer is clipped after Quick geometry starts passing. When host contains `.temporal-create-backdrop.is-advanced`, now override the host to full fixed viewport and restore the modal backdrop and its pointer interactions while retaining the Quick rail host when base mode is active. This remains unverified by local WSL. Only the one browser hardening spec needs focused rerun before full 27-group gate; the auth outage test was already proven passing on 590bdd93 and no auth/backend code was changed since.


## 2026-10-14 — Continuation after Work's 38e1813c handoff

User provided the complete console log `Markdown incollato(20261014-085508).md` for SHA `38e1813c61b9c63cf46ca7a4d5da7b2869fc50f7` (Work published its changes). This is the source of truth **before subsequent chat-side fixes**:

- `uv run --locked pytest -q --no-cov -m postgres tests/integration/temporal/`: **184 PASS, 5 deselected** in **459.51 seconds**; not the entire PostgreSQL or 27-group gate.
- `uv run --locked mypy src tests`: **26 errors in 17 files**; specifically three unreachable defensive temporal-constraint fallback branches, typed test fakes, eight or more unchecked SQL `fetchone()` results and optionals, two unannotated API-test response helpers, one mismatched Session row mapping. This is NOT evidence of any runtime failures.
- `pnpm lint`: **140 errors + 3 warnings** (143 issues); many `require-await` and unsafe-value test mocks, plus real hook/state/refs concerns in Create, Inspector, Timeline, placement lock and related components. This is NOT the full browser gate.

Chat-side GitHub changes after `38e1813c`, not yet verified: preserving defensive rule fallbacks through widened string discrimination; typed explicitly the recurrence occurrence fixture; added actual row assertions before SQL fetch tuple unpacking and optional-result access; typed HTTP test response helpers and bounded ASGI fakes; accepted `Sequence[Mapping[str, object]]` at the pure Session duration evaluator; guarded parent native references. Additional low-risk ESLint cleanup preserves compatibility imports for intentionally retired U3/B14 panels and validates the Event agenda's string array rather than unsafe spread.

React product-safety fixes carefully isolate asynchronous results by canonical subject identity rather than calling setState synchronously in effects. Applied to Inspector Reality, Activity Structure readback, Placement Lock, Event Agenda Editor, Advanced Recurrence Controls and Schedule Reminder Controls. The renamed source-specific editor inner components are keyed by Event/owner/Schedule so switching selection discards stale unsubmitted edits. Kept existing real UI components and test assertions; did not remove tests or apply global ESLint auto-fix. Tests were also made type-aware for Plan mock invocations, actual fetch Promise behavior and Activity/Timeline readbacks. The React Create core time-picker/ref/validation and other hook findings need careful source review; do not auto-remove behavior to silence rules.

Added `tooling/testing/verify_work_handoff_20261014.sh`: clean branch + pull, Ruff/Prettier format, full Python bytecode compilation, generated drift and whole-repo TS gate **before push** of any formatting, then concurrent Ruff, mypy, ESLint and **all Web Vitest**, producing `temp/WORK_HANDOFF_CHECK_LOGS.tar.gz` and `temp/WORK_HANDOFF_CHECK_SUMMARY.txt`. These diagnostics are pending; no new green status should be claimed for mypy/ESLint/Vitest. Only rerun the 27-group PostgreSQL/browser full acceptance gate after static and frontend unit correction. Never weaken browser/auth outage, historical guard or UI behavior assertions to achieve green.



## 2026-10-14 — Latest full static + Web Vitest evidence (fa272269)

User uploaded `WORK_HANDOFF_CHECK_LOGS.tar.gz` generated from `START_HEAD=3c580b755732d55aaed9ea30c65e22c9c6fa0da7` and formatted/pushed `HEAD=fa272269496e6caea563adcc54cff82f3913ee8e`. **Verified on that exact SHA:** `PYTHON_COMPILE=0`, `REPO_TYPECHECK=0`, `GENERATED_DRIFT=0`, `PYTHON_FORMAT=0`, `REPO_FORMAT=0`, **WEB_VITEST=0: 225 test files / 1,055 tests PASS in 18.19s**, `RUFF=1` (one import-order I001), `MYPY=1` (**3 errors**), `ESLINT=1` (**107 errors + 3 warnings**). Neither PostgreSQL nor browser Playwright was included in this check. Do not conflate its green Web Vitest with full acceptance.

The 3 mypy defects on `fa272269`: (a) `session_runtime._duration_evaluations` expected mapping but was passed `list[RowMapping]`; repaired via read-only `Sequence[RowMapping | Mapping[str, object]]`, admitting both real SQL rows and test dictionaries; (b) two integration test helpers imported `httpx.Response`, not visible to mypy in this isolated backend environment; replaced with local minimal status/json `Protocol` return contract, preserving live TestClient responses. Also sorted the sole Ruff import block. All subsequent changes are still **unverified**.

ESLint issues on `fa272269` were dominated by `@typescript-eslint/require-await` and `no-unsafe-*` in test HTTP mocks, plus actual React hooks/ref rules in Create, Timeline, and planning UI. Since the user requires current functional UI, patches preserve expected HTTP payloads, CSRF, 404/409 behavior, and tests rather than removing test assertions. Replaced unnecessary `async` fetch mocks with explicit `Promise<Response>` paths in Responsibility, Actual, Outcome, Confirmation, Reconciliation, Reminder, Plan and Draft Vault tests; strongly scoped changed callbacks; set aside any mock/React test where a safe transformation is not yet validated. Event Agenda and Planning Tray initial fetch effects now enter an async continuation rather than causing state writes synchronously in `useEffect`; require Vitest/browser proof before declaring correctness. Sensitive Quick Create time/ref localization is intentionally **not** changed automatically.

The single next local diagnostic remains:
```bash
cd ~/projects/dante || exit 1
git pull --ff-only origin feature/timeline-temporal-operational || exit 1
bash tooling/testing/verify_work_handoff_20261014.sh
```
It formats on the clean checkout, verifies Python compilation, generated drift, and full TypeScript **before** commit/push, then runs Ruff, mypy, ESLint, all 1,055+ Web Vitest. Attach `temp/WORK_HANDOFF_CHECK_LOGS.tar.gz` to measure actual residual issues. Do not rerun 27-group PostgreSQL/Playwright until the static/frontend suite is stable. Nothing is skipped/disabled.


## 2026-10-14 — Work handoff second gate e3758f9b and targeted recovery

Uploaded `WORK_HANDOFF_CHECK_LOGS.tar(1).gz` is the exact all-static-and-Web-unit run for `HEAD=e3758f9bac344d7b61fa7fe74d1fa4d6605c15b0`, after formatter commit from `c78e185e`. Observed Python compile 0, repository TS typecheck 0, generated drift 0, Ruff format 0, Prettier 0, **Ruff 0**; **mypy 1** (test_objective_definition_result_correction.py:281 accesses `event.text` missing from a local `_TestHttpResponse` typing protocol), **ESLint 67 errors + 3 warnings**, **Web Vitest 1 failure** (1054 PASS/1055 in 225 files, 18.53s). This is not a full PostgreSQL or Playwright gate.

The only Vitest failure `remote-session-capability-data-source.test.ts > keeps live controls hidden for the explicit record-only policy` was due to test mock `mockResolvedValue(response(...))`: the same consumable Fetch Response body was reused by sequential `activityEnabled` and `activityMode` reads, yielding protocol/JSON error. Replaced with `mockImplementation(() => Promise.resolve(response(...)))` to allocate fresh Response per call, with every assertion retained. No production Session behavior changed. Corrected mypy protocol with required diagnostic `text: str`, retaining the actual `TestClient` behavior. Both corrections are pending a fresh local check.

Follow-up ESLint repairs only remove unsafe type propagation from test-only Vitest asymmetric matchers and unknown JSON values by checking runtime body contracts, reading operation ID types explicitly, preserving the original request payload checks, and typing mocks for Planning Tray, Quick Create, Activity Inspector, Plan and Temporal operations. Also repaired the React effect dependency for Timeline organization, keyed the hidden Activity planned-session detail to avoid stale state, derived Life Area typed-entry and canonical context options without synchronous effect resets, and memoized the Create reseed patch callback. These UI changes require full Web Vitest and focused browser proof before the acceptance gate is called green. Sensitive Create segmented time input / composer inline-validation refs and U2 provider draft lifecycles are deliberately **not** blanket-autofixed; they remain React lint hotspots with real focus and draft semantics.

Run `bash tooling/testing/verify_work_handoff_20261014.sh` from a clean, up-to-date feature branch. Its artifact `temp/WORK_HANDOFF_CHECK_LOGS.tar.gz` provides the exact residual lint/test causes on the new commit. After static and all Vitest green, run the complete unskipped hardware-adaptive 27-group PostgreSQL + authenticated-browser gate and confirm UI functionality. Never modify test expectations simply to obtain a pass, and do not infer green results for unexecuted newer commits.



## 2026-10-14 — Verify after ddbb53c8: 8cf52057 static gate and final Create React corrections

Uploaded `WORK_HANDOFF_CHECK_LOGS.tar(2).gz`, exact `START_HEAD=ddbb53c8fa91508a410fb49efa0b8948b6943ff0`, formatter published `HEAD=8cf52057694de0fac0523c14c14c67766e3d54fb`: **PYTHON_COMPILE=0, REPO_TYPECHECK=0, GENERATED_DRIFT=0, PYTHON_FORMAT=0, REPO_FORMAT=0, RUFF=0, MYPY=0, WEB_VITEST=0**, 225 Vitest files / **1,055 tests passed** (18.85s), **ESLINT=1 with only 13 errors + 1 warning**. No PostgreSQL or browser E2E test was run in this gate, and these results apply only to `8cf52057`, not subsequent source changes.

Remaining ESLint on this SHA was exclusively React behavior in four Create files:
- `temporal-create-composer.tsx`: 5 `react-hooks/refs` diagnostics from reading `dialogRef.current` during render to locate validation error portals/fallbacks.
- `temporal-create-core-fields.tsx` and `temporal-create-core-u2.tsx`: three each from effect synchronous segmented hour/minute state resets and reading `lastValidRef.current` inside the render-only raw input/quarter-hour selection; **do not remove** segments, wheel, initial committed clock, focus behavior, or hidden validation input.
- `temporal-create-u2-draft-context.tsx`: two synchronous effect state writes for baseline reset and date-specific endDate normalization, potentially wiping staged Life Area/U6 intentions.
- `temporal-create-entry.tsx`: single React Hook exhaustive-deps warning on a callback that captures `session.draft.current`.

After that green source checkpoint, direct GitHub source corrections were published, but are **pending actual WSL typecheck, lint, Vitest, and browser verification**:
1. Both segmented time components now track the committed string for render and use a guarded `previousValue !== value` state adjustment on genuine controlled-prop changes; lastValidRef remains available only in event/effect callbacks. Kept hidden input, hour/minute fields, arrow buttons, quarter picker, Enter/Escape and existing callbacks.
2. Composer field-error portals and unlocated-issue fallback now locate DOM targets after commit in an animation-frame effect, storing a stable target/known-path snapshot; no `dialogRef` reads during render. Kept red-field marking, scroll-to-error, field-level portal and global fallback.
3. U2 authoring provider remounts only on `resetKey` baseline changes and uses guarded date state normalization; all staged Life Area, color and structure remains in the active draft on ordinary field edits. On mount and after state changes the committed draft is reported to parent via an effect. Avoid weakening this functionality to silence React lint; browser and authoring tests are required.
4. Entry captures `currentDraft` for its patch callback dependency without changing reminder eligibility semantics.

No test, validation or eslint rule has been removed/disabled. **Do not assert that the 13 ESLint findings are now green** until `bash tooling/testing/verify_work_handoff_20261014.sh` reports the actual new output. This script formats and verifies generated drift, Python compilation and all TS before pushing its formatter commit; then concurrently executes all Ruff/mypy/ESLint and 1,055+ Vitest tests. If all static/unit gates pass, run `bash tooling/testing/run_full_gate_adaptive.sh` for the complete 27 groups (374+ PostgreSQL tests and Playwright fixture/non-auth/real-stack), and explicitly verify Quick Create date/time focus, validation localization, Draft Vault persistence, Quick/Advanced mode, Session Panel and Inspector.


## 2026-10-14 — Static suite all-green except planned Session field validation (7f724e7d)

The user supplied `WORK_HANDOFF_CHECK_LOGS.tar(3).gz`, generated from `START_HEAD=1fe98f6575e6fca223dfc7a452e314946f45628f` with formatter commit `HEAD=7f724e7dd221c9d0a93ff033f4c299b4903c52a4`. This is **verified** for that SHA: Python compile 0, repo TypeScript 0, generated drift 0, Python/Prettier format 0, Ruff 0, mypy 0 (489 files), ESLint 0. **Web Vitest 1 FAIL, 1054 PASS (225 files).** The single failure is `temporal-create-entry-authoring.test.tsx` case `shows an out-of-range Session error in Italian on its time controls`: it requires `data-create-invalid="true"` on the `.temporal-create-tree-time-editor` and the original Italian message on that editor. This is active B14 behavior, NOT a deprecated test; never weaken it or remove the field-level error.

Root-cause analysis: U2 provider was refactored to `useEffect(() => onDraftChange(state), [state, onDraftChange])` while the parent `temporal-create-entry.tsx` still supplied an inline `onU2DraftChange` lambda. Any parent rerender, including `setFailureTarget`/validation output, changed the lambda identity and reran the provider's effect, triggering the parent's queued `setFailureTarget(null)` and clearing the legitimate field error after validation. Published targeted fix in `temporal-create-entry.tsx`: `useCallback(..., [])` stable `handleU2DraftChange` with identity guard `if (u2DraftRef.current === draft) return`; actual user edits still invalidate staged vault save, update the ref and state, clear old error. Parent validation-only renders no longer clear errors. No test assertions altered; this code is **unverified** until the next WSL run.

Next: on clean branch pull; run `bash tooling/testing/verify_work_handoff_20261014.sh`, attach `temp/WORK_HANDOFF_CHECK_LOGS.tar.gz`. If all static checks and all 1,055 Web Vitest pass, run `bash tooling/testing/run_full_gate_adaptive.sh` for all 27 acceptance groups, PostgreSQL and browser fixture/non-auth/real-stack, respecting actual current SHA and including the Quick Create error visualization. No claim of all-green gate until witnessed.


## 2026-10-14 — Additional verification after a1222ca4 (13:02 logs)

User uploaded `WORK_HANDOFF_CHECK_LOGS.tar(4).gz`, with `START_HEAD=HEAD=a1222ca42766870c873fb1c9d945cb5bdde366b5`. Verified at that SHA: `PYTHON_COMPILE=0`, `REPO_TYPECHECK=0`, `GENERATED_DRIFT=0`, `PYTHON_FORMAT=0`, `REPO_FORMAT=0`, `RUFF=0`, `MYPY=0`, `ESLINT=0`; Web Vitest **1 FAIL / 1054 PASS** in 225 test files. The **only** failed case remains `temporal-create-entry-authoring.test.tsx`: “shows an out-of-range Session error in Italian on its time controls”, which insists on `.temporal-create-tree-time-editor[data-create-invalid="true"]` and exact Italian error text. It is current product behavior, not a deprecated test; no assertions changed.

The prior fix `a1222ca4` stabilized the parent's `onU2DraftChange` reference but did not resolve this failure. A deeper lifecycle review found `TemporalCreateU2DraftProviderInstance` still invoked `onDraftChange` from **inside a React setState functional updater**, potentially committing the parent's `queueMicrotask(() => setFailureMessage(''); setFailureTarget(null))` only after the user had clicked “Aggiungi” and the validation had set the error. The provider also invoked the same callback during `useEffect` mount/date synchronization. Thus the parent could not distinguish a genuine user edit from an automatic draft synchronization.

Three precise source changes published *after the logged SHA*:
- `temporal-create-u2-draft-context.tsx`: callback now carries source `'user' | 'sync'`; user edits compute and publish the next authoring draft directly inside the input event, rather than inside React's deferred state updater; mount/date synchronizations explicitly notify with `'sync'`.
- `temporal-create-composer.tsx`: forwards the source through its typed callback; no UI controls/validation behavior deleted.
- `temporal-create-entry.tsx`: stable `handleU2DraftChange` still updates ref, state and staged-vault invalidation, but clears prior failure message/target **only** on a true `'user'` edit, synchronously without a queued microtask. Initial provider synchronization never clears a just-produced validation error.

**New changes not yet tested** by WSL; do not claim full green. Efficient next check: first run the exact failing file via `pnpm --filter @dante/web exec vitest run src/features/temporal-create/ui/temporal-create-entry-authoring.test.tsx`. On PASS, execute `bash tooling/testing/verify_work_handoff_20261014.sh` (Ruff, mypy, ESLint, TypeScript, all 1055 Vitest, generated/formatted contracts) and on complete PASS execute `bash tooling/testing/run_full_gate_adaptive.sh` (27 groups incl. PostgreSQL and browser real-stack). Do not change or mute the Session visual-error test. Preserve complete per-run log archives.


## 2026-10-14 — Focused Quick Create regression: three failures after 6e929e2d

The user supplied `CREATE_SESSION_FOCUSED_VITEST.log` from a WSL run after `6e929e2d`: 16 tests in `temporal-create-entry-authoring.test.tsx`, **13 PASS / 3 FAIL**. Exact failing cases: (1) out-of-range planned Session still not marked with `data-create-invalid="true"` at the session time editor; (2) staging `Formazione` new Life Area then Add sent a request with `lifeArea=undefined` instead of the default orange `#EA5C12`; (3) staging `Formazione blu` after choosing item color blue sent `lifeArea=undefined` instead of `#4285F4`. All three test contracts are valid product behavior: do not remove, skip or weaken them. The chained all-gate command did NOT progress beyond focused Vitest, so no new broad static/PostgreSQL/Playwright results exist.

Root cause identified for the two new Life Area failures: `TemporalCreateLifeAreaField.stageTypedName` calls `onLifeAreaChange(newArea)` and `onItemColorChange(null)` synchronously in one event. The last provider refactor replaced a functional `setState(current=>...)` with `patchTemporalCreateU2AuthoringDraft(state, patch)`, capturing the **previous render's** `state` in both callbacks. The second patch could overwrite the new Life Area with `kind:'none'`. Potential related source for the Session validation: a stale provider `useEffect` syncing a preceding render could overwrite newer Activity Structure data in the entry ref before Submit, even when clearing failureTarget on auto-sync was prevented.

Published a targeted U2 provider fix after this log: `latestDraftRef = useRef(state)`, synced to committed `state` in `useLayoutEffect`. User-initiated `patch` composes against `latestDraftRef.current`, updates it synchronously, then sets React state and calls `onDraftChange(next,'user')`. The post-commit sync effect only publishes `onDraftChange(state,'sync')` when the committed `state` matches the current ref; old commits cannot replace newer data. This protects same-event Life Area/color changes, queued time-field edits and future Create validation without changing any tests or removing UI behavior. The previous user/sync distinctions in the entry/composer remain. **New fix is UNVERIFIED**; do not claim the three tests now pass until the focused Vitest reports success.

Next verification on a clean checkout:
```bash
cd ~/projects/dante || exit 1
git pull --ff-only origin feature/timeline-temporal-operational || exit 1
pnpm --filter @dante/web exec vitest run src/features/temporal-create/ui/temporal-create-entry-authoring.test.tsx
```
Only when all 16 pass, run `bash tooling/testing/verify_work_handoff_20261014.sh`, then `bash tooling/testing/run_full_gate_adaptive.sh` with log archives and provenance. If targeted tests still fail, inspect actual U2 create validation and stage/edit source before modifying more logic.


## 2026-10-14 — 15/16 Quick Create focused PASS; final Session error rendering

New uploaded log `CREATE_SESSION_FOCUSED_VITEST(1).log` confirms **15 PASS / 1 FAIL** in the full 16-case Quick Create U2 authoring test file (Vitest v4.1.11; started at 13:16:52, duration 3.95s). Both newly broken Life Area tests from the prior attempt now PASS: new area with orange `#EA5C12` and preserving selected blue `#4285F4`. The sole remaining failure is the valid product contract `shows an out-of-range Session error in Italian on its time controls`: the Session's `.temporal-create-tree-time-editor` lacked `data-create-invalid="true"`; expected the exact Italian alert `La Sessione deve rientrare nell’orario dell’attività.`. User's local run stopped before the full static and 27-group gate; no subsequent green claims are justified.

Review confirms domain mapping is correct: `validateTemporalCreateU6StructureIssue` resolves the invalid planned Session to `plannedSession:<slice.id>`, and the corresponding child editor renders `data-create-path="plannedSession:<slice.id>"`. The weakness was **imperative visual error marking** in `TemporalCreateComposer.useLayoutEffect` (querySelector/dataset mutating DOM, cleanup unsetting it) coupled with a separate requestAnimationFrame-based host lookup to portal the Italian text. These can be lost across U2 provider child rerenders/DOM replacement and are harder to test than a declarative React error.

New direct UI implementation published, **not yet verified**: `TemporalCreateAdvancedActivityStructure` receives optional `validationTarget`/`validationMessage`; for the targeted enabled planned Session it directly renders `data-create-invalid="true"` and `aria-invalid="true"` on the exact time editor and the translated error as a child `role="alert"`. `TemporalCreateComposer` routes targets beginning `plannedSession:` to the component, preserving the prior generic error portal and DOM annotation for other fields, but skipping imperative annotation and duplicate global/portal error for the handled session. No tests were removed/changed; Session editing and other controls are untouched.

Verification next:
```bash
cd ~/projects/dante || exit 1
git pull --ff-only origin feature/timeline-temporal-operational || exit 1
mkdir -p temp
pnpm --filter @dante/web exec vitest run src/features/temporal-create/ui/temporal-create-entry-authoring.test.tsx 2>&1 | tee temp/CREATE_SESSION_FOCUSED_VITEST.log
```
On **16/16 PASS** proceed to `bash tooling/testing/verify_work_handoff_20261014.sh` (all static + full Web Vitest) and only then `bash tooling/testing/run_full_gate_adaptive.sh` (all 27 PostgreSQL/browser groups). If it remains red, capture whether the parent `failureTarget` and `failureMessage` were produced before changing any domain validation.


## 2026-10-14 — 27/27 acceptance PASS on 4ad30f90 (final full-gate evidence)

**Verified directly from user's uploaded `FULL_GATE_LOGS.tar(20261014-113549).gz` and `FULL_GATE_SUMMARY(10).md`**. The adaptive full parallel gate completed on **source SHA `4ad30f905db0c37520fe180aeebcff74779e8d93`**, captured 2026-10-14 at 11:35:22 UTC, **27 of 27 groups PASS; source stability PASS; exit code 0; elapsed 660.4 seconds (11m 0.4s)**. This is an acceptance-test success for the exact SHA; it is *not* proof that every manual UI behavior or every historical contract is fully covered.

Test evidence from separate archived logs:
- Backend non-PostgreSQL `628 passed, 374 deselected` (intentional separate Postgres selection), 42.92s.
- Backend PostgreSQL **374 selected tests covered in 21 module-atomic, duration-balanced queued jobs**, maximum **7 disposable isolated clusters**; PostgreSQL group passed, 465.6s total wall-clock.
- `BACKEND_POSTGRES_SHARD_19` initially exited 2 due to transient **PostgreSQL readiness/cleanup**: startup reported `FATAL: the database system is starting up`, NOT an assertion failure; the full shard was retried once in isolation as `BACKEND_POSTGRES_SHARD_19_RETRY_01` and **17/17 passed**. Preserve this as an infrastructure observation and do not misreport 21 shards having clean first-attempt passes.
- Web Vitest **225 test files, 1,055/1,055 cases PASS**, including the previously failing planned Session validation and Life Area colors; 26.36s inside log.
- Playwright fixture / Session Panel **2/2 PASS** at 1440px and 390px.
- Playwright nonauth **127/127 PASS** using 4 workers; web-server proxy emitted `ECONNREFUSED 127.0.0.1:8000` diagnostic noise because the nonauth browser route does not require a live backend; does not negate the passing assertions.
- Playwright authenticated real-stack **84 PASS, 3 SKIPPED** out of 87 declared checks, using 1 isolated worker across Chromium, Firefox, WebKit; **3 skips are explicitly declared WebKit exclusions**: one B03-E Event closure check from `e2e/auth/event-create-read.spec.ts`, and two Life Area golden checks from `e2e/auth/temporal-create-life-area-golden.spec.ts`; these contracts are exercised in Chromium and Firefox by design. The real-stack email workers logged transient `OperationalError` during orchestrated database-outage scenarios. No Playwright failures.
- `TEST_INTEGRITY` shows `REGISTERED=491 DISCOVERED=491 UNREVIEWED=491` with structural-consistency PASS; this *is not* an audit of all 491 historical test expectations or deprecation status. Do not characterize structural completeness as semantic review.
- Python Ruff/format/mypy, repo ESLint/format/typecheck, architecture, generated drift, build, mobile bundle, all listed platform/eval/tooling/i18n/time/api contracts **PASS**.

**Decision:** close the immediate static/type/unit/integration/E2E green-up phase for `4ad30f90`. Do not perform another 27-group run without a changed source SHA or a specific need. Future work may evaluate the single startup flake and nonauth backend-proxy/error noise as separate infrastructure/observability improvements, and independently audit whether all historical tests reflect the current UI; these are not reasons to reopen all passed tests. Preserve current product UI contracts (Bozze, Quick Create, red local validation, Session hierarchy, Timeline/Inspector, recurring edit scopes) without resurrecting deprecated features. If updating docs or any other file after this gate, explicitly tie the acceptance verdict to the tested SHA, not to a newer documentation-only HEAD.

## 2026-10-15 — Session review candidate and coordinated Timeline revision

The user's attached WSL run on `5e87cc26` passed test integrity, Ruff, six non-PostgreSQL tests, 21 PostgreSQL tests (including six catalog modules, owner-scoped Session review and Activity policy), Web TypeScript, the six rail tests and generated-source determinism. The OpenAPI/Orval resolution queue model was published later on `f7eb26c`; do not attribute the earlier run to the newer SHA.

A subsequent Timeline candidate routes Activity keyboard/drag and time-editor changes through Activity replan rather than the generic Schedule mutation. It loads the current Activity plan, accounts for every interval, rejects stale or overlapping inputs, and requests Keep/Delete/Cancel before a real Session is affected. Successful Keep changes can be undone from the returned plan state with a fresh Session choice. Event Schedule mutation remains on its own path. Local focused Web tests passed 14/14 and complete Web Vitest passed 1,061/1,061 in 225 files; Web TypeScript and targeted ESLint passed. These checks use the locally installed dependency tree and are not the WSL full gate.

Still open: Activity unschedule is a separate coordinated operation; the generic Schedule path is rejected for governed intervals. Recurring instance/series deletion needs an explicit scope and materialization-safe database command. Real-stack PostgreSQL/browser acceptance and visual verification remain to be run after these paths are complete.

## 2026-10-15 — Recurring Timeline scope and browser journey candidate

After `c298769`, a recurring Activity card move and its plan Undo explicitly ask
the user to confirm that the operation applies to **only this occurrence**;
the same dialog offers Keep/Delete/Cancel if real Session attempts exist. A
new focused UI case asserts no mutation before the scope choice. An existing
authenticated browser suite now includes an Activity card keyboard move,
checks the coordinated `PUT /activities/{ref}/replan` request, then reloads
and reads the persisted five-minute change. The focused UI test passed 6/6
locally; Web TypeScript, targeted ESLint and Prettier passed. The new browser
case has **not** run against the real stack, and the complete 27-group gate
has **not** run on this candidate. The complete local Web Vitest suite passed
**1,062/1,062 in 225 files** on this candidate. The earlier 1,061/1,061 Web
result belongs to `c298769`, before these changes. This scratch dependency
tree lacks Playwright, so browser discovery/execution must run in WSL.

Coordinated unplacement and its Undo are still open: generic Schedule mutation
rejects governed Activity intervals. Materialized recurring instance deletion
still requires a scoped, materialization-safe operation. Do not route either
through the Activity hard-delete function or mark them accepted before real
PostgreSQL and browser tests. User's WSL generated `dante.ts` change was not
included in the three generated files published on `f7eb26c`; inspect its
diff before changing the user's local generated worktree.

## 2026-10-15 — Accepted recurring Activity deletion semantics

Deletion is now explicitly defined in
`docs/domain/decisions/activity-session-operational-lifecycle-v2.md`:

- a non-recurring Activity hard-deletes its full owned graph;
- a materialized recurring Activity asks **Solo questa istanza**, **Tutta la
  serie**, or **Annulla**;
- Solo questa atomically deletes the selected Activity graph and persists a
  skip for its Occurrence, preventing rematerialization while preserving the
  other instances and Routine;
- Tutta la serie atomically deletes the Routine source, all materialized and
  future instances, and every owned graph; and
- neither scope may leave a partial cascade or recreate a deleted instance.

This is a product rule, not implementation evidence. The present backend
continues to fail closed for recurring Activity hard deletion until the scoped
database command, API, UI confirmation and PostgreSQL/browser regressions
are delivered.


## 2026-10-15 — Disposable-volume regression and generated API publication

User-local WSL evidence on exact source `4ad9df9cec17a7db50647e8b3ce89017b960eee4`: **7 passed in 21.82s** for `tests/test_postgres_harness_cleanup.py` (2 cases), runtime outage/readiness recovery, schema/search_path hardening, WebAuthn account/session/user-handle binding and both forward-only downgrade guards. These seven tests pass; this is not a full-gate result.

The user then ran `pnpm api:generate` followed by `pnpm generated:check`. The supplied console ends with **PASS: generated sources are deterministic and current (550 files)**. The supplied `DANTE_GENERATED_API.tar.gz` contains 547 API artifacts. Comparing their Git blob hashes with the exact candidate tree identifies **17 changed/new API files and no deletions**. Publish those exact generator-produced bytes: OpenAPI, generated client, model index and fourteen Zod models for hard deletion, Timeline unplacement/Undo and Event occurrence/Schedule selection. No generated file is hand-edited.

**Still open:** one complete 27-group gate on the candidate containing these generated artifacts, plus real-app visual acceptance. Prior PostgreSQL and generated checks are scoped evidence from the user, not proof that every group passes on the publication commit. Preserve local generated work before pulling; after publication the remote files should match the uploaded artifacts exactly. Do not reapply an obsolete generated-only stash over the published client. No CI/Actions requested.


## 2026-10-15 — Focused browser failures: exact title and isolated sign-in fixtures

The next supplied WSL log reports Mypy **PASS, 495 source files**, all **15 selected tests PASS** across Dictionary scope, governed OpenAPI export and Temporal operation inventory, and authenticated Chromium **2 PASS / 4 FAIL in 24.6s**. The console does not print HEAD, so do not invent a pinned-SHA verdict from this log.

Both new deletion journeys failed before opening the Inspector: substring matching of the title button also selected the time-edit button, whose accessible name includes the same title. Both selectors now use `exact: true`. Two later Schedule journeys stopped at signin with HTTP 429: four scenarios shared one project account while the real-stack harness intentionally permits only two sign-ins. Each Schedule scenario now has a dedicated seeded account per browser (65–76); Event scenarios likewise use distinct accounts per Chromium/Firefox (77–80), avoiding their previous shared account across projects. The disposable harness seeds 80 accounts. The rate limit remains two; no retries, skips, production changes or relaxed assertions are introduced.

Local verification of this repair: targeted ESLint PASS; Prettier PASS; Python syntax PASS; all sixteen scenario/project accounts are distinct and within the seeded range; Playwright discovery lists exactly the existing six Chromium cases. Real-stack execution is **NOT RUN here**, because Docker is unavailable. Rerun only these two Playwright files, preserving the actual candidate SHA in the output. Do not repeat the already passing Backend/PostgreSQL/API checks for this test-fixture-only repair. This is scoped repair evidence, not a 27-group/global acceptance claim; manual Activity/Session lifecycle acceptance remains separate.
