# B2 Home Shell + Timeline Quick Add v25

**Branch:** `prototype/frontend`  
**Date:** 2026-08-23  
**Status:** **USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN**  
**Base:** B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22

## Decision

The accepted Home working baseline advances to **v25** for a bounded shell/timeline pass.

v25 records the user-reviewed application-bar arrangement and the contextual timeline quick-add affordance. It does not reopen the accepted v24 palette/background, v23 DANTE identity, v22 central-stage add/configuration boundary, Context Rail semantics, or backend/domain contracts.

## Accepted global app bar

The Home topbar is treated as a real application bar rather than a floating rounded card:

```text
LEFT                         CENTER                    RIGHT
DANTE + Cerca                Home / Mondi / Oggi       Crea / Review / launcher / account
```

Accepted presentation/placement:

- the bar is `sticky` at the top of the viewport;
- the bar is edge-to-edge at shell level, with a normal **24 px internal horizontal inset**;
- DANTE identity and Search are on the left;
- primary Home/Mondi/Oggi navigation remains centered;
- `Crea` is the **first control in the right utility group**, before the legacy Review control;
- Review, launcher and account remain present with their existing prototype status;
- existing Search/Create controls are moved/reused rather than duplicated;
- the outer Home-stage vertical side frame is suppressed in the working shell treatment to reduce the nested-panel reading.

This checkpoint accepts placement and shell behavior only. It does not promote mock search/create/review/account interactions into production routing/backend contracts.

## Accepted timeline quick add

The timeline temporal-header grid is extended from:

```text
month / now / week / actions
```

to:

```text
add / month / now / week / actions
```

The new `+`:

- is a real button inside the timeline component markup, not a ghost slot or decorative overlay;
- sits at the left edge of the temporal header;
- uses a dedicated first grid column;
- shifts `agosto 2026` and `Ora` to the right as part of the same grid, preserving alignment rather than applying independent pixel nudges;
- uses the accepted charcoal/orange visual language;
- currently reuses the existing global `Crea` popover in the prototype.

The current click reuse is **prototype-only**. v25 does not yet define the final production quick-add form, date/time prefill contract, route, command, persistence behavior or backend endpoint.

The central-stage v22 rule remains unchanged: the new timeline `+` is contextual to the temporal surface and is **not** a persistent Mondi/Segnali add control.

## Durable transform

The accepted v25 shell/timeline state is stored as a deterministic transform over the accepted v24 Home string:

```text
prototypes/frontend/home/archive/b2-shell-timeline-v25/shell-v24-to-v25.js
size       8391 bytes
SHA-256    6e9d3e25270f8d73482aa6a2f48f709e1ffc2324007dde2fa6d40cdea90d1d69
```

The transform is intentionally bounded to:

- topbar control placement and app-bar presentation;
- outer shell side-frame cleanup already present in the accepted reviewed state;
- timeline temporal-header grid extension;
- the timeline quick-add button and its local prototype click bridge to `Crea`.

It does not modify Mondi/Segnali rendering/data, AI contents, Context Rail behavior, background asset, palette source values, backend/API/domain semantics or persistence contracts.

## User-reviewed preview evidence

The final local HTML accepted immediately before this checkpoint was:

```text
DANTE_Home_v24_v13_PLUS_REFINED_MONTH_RIGHT.html
size       80922 bytes
SHA-256    0b9491525a99643837dc42e4150113db50d00bf7ff73549ea4fd3f9994adcdf9
```

The repository stores the compact deterministic v24 -> v25 transform rather than duplicating the local review wrapper.

## QA qualification

```text
user visual review of final v13 wrapper      PASS
v25 transform JavaScript syntax              PASS (node --check)
transform mock-structure execution           PASS
final reviewed wrapper inline-JS syntax      PASS
v24 palette/background                       PRESERVED
v23 DANTE identity                           PRESERVED
v22 stage no-persistent-add semantics         PRESERVED
fresh 24-case browser matrix                 NOT CLAIMED
fresh accessibility rerun                    NOT CLAIMED
separate PARTIAL visual review               NOT CLAIMED
```

## Explicit non-change

No change to:

- `home.stage.continuity` / Mondi semantics;
- `home.stage.signals` / Segnali semantics;
- the v22 prohibition on persistent stage add/configuration controls;
- Capture/Resolution meaning in the Context Rail;
- event/timeline drag, zoom, grouping, calendar navigation or time-edit semantics;
- DANTE brand master geometry;
- v24 background asset;
- backend/API/Domain/logical/physical semantics;
- production frontend framework/runtime selection.

## Still open before B2 closure

- final production semantics for timeline quick-add, including context/date/time prefill and destination;
- legacy Review / historical launcher reconciliation in an explicit bounded scope;
- production semantic-token migration of the working visual skin;
- remaining small shell/detail refinements;
- final responsive, visual and accessibility QA.
