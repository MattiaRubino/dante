# Workstream — Phase 4 Home / Today

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2 (`prototype/phase-4-today-home` → `main`), draft
- Work type: coded UX prototype / design validation
- Current approved working checkpoint: **Home vNext Orientation + Day Ribbon v1**
- Current approved artifact documentation: `docs/phase-4/home-vnext-orientation-day-ribbon-v1.md`
- Exact artifact: `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/lifeos_home_vnext_orientation_day_ribbon_v1.html`
- Exact HTML SHA-256: `986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df`
- Exact Git blob SHA: `fd9788212fbbd1ee40e53271cc39cedd9275b341`
- Current handoff: `docs/phase-4/frontend-architecture-handoff-2026-08-18.md`
- Historical/regression anchors: Home Shell v11, Today v21, Integrated v1, Timeline Toolbar v8, Adesso + Main Stage v1

## Purpose

Validate the Home/Today experience before production implementation, including spatial hierarchy, situational orientation, timeline density, progressive disclosure, overlap handling, grouped expansion, temporal navigation, direct manipulation, contextual/adaptive presentation and the integration between Home and Today.

Phase 4 is a coded UX/design-validation workstream. It must not silently create backend schema, change accepted Domain/Logical semantics or canonize temporary prototype labels.

## Mandatory reading before editing Phase 4

1. root `README.md` on current `main`;
2. `docs/PROJECT-STATUS.md` on current `main`;
3. `docs/development/agent-operating-manual.md`;
4. `docs/development/operating-rules.md`;
5. this workstream handoff;
6. `docs/phase-4/frontend-architecture-handoff-2026-08-18.md`;
7. `docs/phase-4/home-vnext-orientation-day-ribbon-v1.md`;
8. `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/README.md` and the exact archived HTML;
9. `docs/phase-4/interaction-architecture-decisions-v0.md`;
10. `docs/phase-4/frontend-architecture-requirements-v0.md`;
11. `docs/phase-4/cross-platform-interaction-rule-v0.md`;
12. `docs/phase-4/interaction-architecture-guide-v0.md` where research/rationale is material;
13. `docs/phase-4/frontend-master.md` and `docs/phase-4/today-v21.md` for mature timeline behavior;
14. relevant tests under `tests/prototypes/`;
15. current Git refs and branch relation to current `main` before any write.

The accepted Product/Domain/Logical/architecture baseline comes from current `main`. Phase 4 branch-local files are authoritative only for newer bounded unmerged Phase 4 UX/prototype work.

## Current source of truth

For the next Home/Today prototype iteration, the authoritative working artifact is:

- `docs/phase-4/home-vnext-orientation-day-ribbon-v1.md`;
- `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/lifeos_home_vnext_orientation_day_ribbon_v1.html`;
- exact HTML size `748625` bytes;
- exact HTML SHA-256 `986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df`;
- exact Git blob SHA `fd9788212fbbd1ee40e53271cc39cedd9275b341`.

The initially checkpointed HTML was replaced by the user on commit `cb58b1528292398ccedeaedb60b44a4ff6e6235f` after identifying that the wrong local variant had been uploaded. The corrective delta changes exactly one source line: `drRoadGrad` now uses `gradientUnits:'userSpaceOnUse'` with percentage x coordinates. This corrected blob is the only current working source.

Use the archived HTML exactly. Do not reconstruct the current state approximately from screenshots or conversation history.

Older checkpoints remain truthful historical/regression evidence, but they no longer override this continuation checkpoint.

## Product / interaction architecture constraints

The current Phase 4 direction remains:

- one LifeOS reality with multiple projections;
- time is primary but not sovereign;
- current situation is broader than the timeline;
- natural language is a global interaction layer over the same structured reality;
- GUI remains first-class for comprehension and direct control;
- adaptive/contextual UI uses a controlled grammar;
- persistent UI serves recurring user needs rather than internal entity types;
- hidden/non-current knowledge remains recoverable and governable;
- attention priority and action authority remain distinct;
- progressive disclosure prevents breadth from becoming an infinite dashboard;
- Mobile and Web may differ representationally without changing semantic outcomes.

Prototype labels such as `Worlds`, `Stats`, `Per te` or other current copy do not become Domain/Logical primitives or final Information Architecture solely because they are visible in the artifact.

## Explicit current constraints

### Preserve the exact accepted base

- Preserve approved areas unless the user explicitly puts them in scope.
- Do not silently transplant UI from discarded conversation previews.
- Do not independently execute an old handoff's “next task” after a newer user-approved checkpoint exists.
- Create a new checkpoint after an accepted iteration rather than overwriting this one.

### No new Home wing expansion

Do not add/restore new Home wing expansion behavior unless the user explicitly requests it in a later scope. Dormant/accumulated prototype code is not permission to surface rejected behavior.

This does not remove the existing Today/timeline panel expansion controlled by the timeline behavior.

### Timeline margin placement

Timeline gap/margin indicators remain on the **left**, close to the time axis, unless the user explicitly reopens that decision.

### Visual/commercial discipline

- Do not add controls merely because functionality exists.
- Avoid a permanent grid of equal-weight widgets.
- Avoid enterprise cockpit heaviness and toy/gamified treatment as defaults.
- Prefer hierarchy, progressive disclosure and contextual depth.
- Keep AI useful but visibly bounded by user authority.
- Functional changes require real browser regression appropriate to the change; visual changes require visual browser verification before delivery.

## Current integrated behavior to preserve

The exact archived HTML artifact is authoritative. At a high level it includes:

- Home topbar/shell and professional conversational AI surface;
- current-situation / attention / contextual-dynamic upper composition;
- current central `Worlds`/`Stats` prototype surfaces and navigation behavior;
- Home orientation strip and synchronized day context;
- week/day ribbon and calendar navigation;
- contextual `Ora` return-to-current-time action;
- navigation into past and future temporal context;
- 24-hour timeline and nonlinear density mapping;
- overlap lanes;
- group filters, group reorder and grouped timeline expansion;
- timeline panel expansion;
- card focus and subtask reflow lineage;
- event drag/move and Undo lineage;
- zoom and anchored manual time editing;
- environmental/path context;
- secondary side surfaces present in the approved artifact.

This summary is a handoff index, not permission to reimplement features approximately.

## QA of current checkpoint

Corrected artifact verification:

```text
artifact size                 748625 bytes
artifact SHA-256              986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob SHA                  fd9788212fbbd1ee40e53271cc39cedd9275b341
exact reconstruction          PASS
duplicate DOM IDs             0
CSS parse errors              0
inline JS syntax failures     0
```

The integrated Chromium smoke previously recorded for this checkpoint lineage was executed on the immediately preceding mistaken blob. It was **NOT RERUN after the corrective replacement** and must not be attributed to the current corrected blob. The complete `today-v21-regression.py` suite was also **NOT RUN** as part of this correction.

## Historical/regression checkpoints

Preserve and use when needed:

### Home Shell v11

- `docs/phase-4/home-shell-v11.md`;
- `prototypes/home/archive/v11/`.

### Today v21

- `docs/phase-4/frontend-master.md`;
- `docs/phase-4/today-v21.md`;
- `prototypes/today/archive/v21/`;
- `tests/prototypes/today-v21-regression.py`.

### Integrated v1

- `docs/phase-4/home-today-integrated-v1.md`;
- `prototypes/home/archive/integrated-v1/`.

### Timeline Toolbar v8

- `docs/phase-4/home-vnext-timeline-toolbar-v8.md`;
- `prototypes/home/archive/home-vnext-timeline-toolbar-v8/`.

### Adesso + Main Stage v1

- `docs/phase-4/home-vnext-adesso-main-stage-v1.md`;
- `prototypes/home/archive/home-vnext-adesso-main-stage-v1/`.

These are regression/history anchors. **Home vNext Orientation + Day Ribbon v1 is the current working starting point.**

## Parallel-work boundary

Backend/architecture work may proceed independently. The prototype may continue using simulated data until stable application contracts exist.

Do not force backend schema/provider decisions from temporary visual implementation details. Conversely, do not change accepted Product/Domain/Logical meaning merely to simplify the prototype.

Phase 4 normally owns:

- `docs/phase-4/`;
- relevant Phase 4 files under `docs/ux/`;
- `prototypes/home/` and `prototypes/today/`;
- `tests/prototypes/`;
- this handoff.

Avoid editing `PROJECT-STATUS.md`, root README or broad architecture files for ordinary prototype iterations. Update global files only when Phase 4 changes global project truth or reaches an accepted integration milestone needing promotion.

## Next exact task

**Await the user's next explicit direction.**

Do not independently continue any older design backlog. The next modification begins from the exact current checkpoint and only the new user-defined scope.

Before eventual merge, compare the branch against current `main` and run the semantic/documentation coherence gate from `docs/development/operating-rules.md`.

## Handoff rule

A new chat/AI must be able to resume without conversation history by reading this file plus `docs/phase-4/frontend-architecture-handoff-2026-08-18.md`, `docs/phase-4/home-vnext-orientation-day-ribbon-v1.md`, and opening `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/lifeos_home_vnext_orientation_day_ribbon_v1.html`.
