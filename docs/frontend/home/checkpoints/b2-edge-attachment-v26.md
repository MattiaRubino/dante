# B2 Home Edge Attachment v26

**Branch:** `prototype/frontend`  
**Date:** 2026-08-23  
**Status:** **USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN**  
**Base:** B2 Home Shell + Timeline Quick Add v25 over B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22

## Decision

The accepted Home working baseline advances to **v26** for a strictly bounded edge-attachment pass.

v26 records the user-reviewed geometry for the left-attached AI/timeline surfaces. It does not reopen the accepted v25 application bar or timeline quick-add composition, the v24 palette/background, the v23 DANTE identity, the v22 Home-stage boundary, Context Rail semantics, or backend/domain contracts.

## Accepted edge behavior

### Expanded AI

The visible AI card attaches to the left application edge while its parent layout geometry remains unchanged:

```text
left edge = 0
left corner radius = 0
right corner radius = preserved
```

The implementation targets the real node:

```text
#lifeosHero.home-vnext-test .hero-left-panel .ai-card.ai-chat-pro
```

The accepted delta expands only the visible card into the existing `--hv-outer` gutter. It does not move the central stage or alter Mondi geometry.

### Collapsed AI

The collapsed state targets the exact rail created by the Home structure layer:

```text
#lifeosHero.home-vnext-test.ai-collapsed .home-ai-rail
```

Accepted geometry:

```text
left = 0
border-radius = 0 18px 18px 0
```

The right-hand rounding is preserved. No `Now`, stage, orientation or world geometry is changed.

### Timeline

The timeline is the real `lifeos-today` custom element and its internal `.today` surface lives in Shadow DOM.

Accepted geometry:

```text
host margin-left = 0
host right margin = preserved
.today top-left radius = 0
.today bottom-left radius = 0
right-side rounding = preserved
```

The v25 temporal header itself remains:

```text
add / month / now / week / actions
```

No timeline date-navigation, event, drag, zoom, grouping or quick-add semantics are changed by v26.

## Durable transform

The accepted v26 edge state is stored as a deterministic transform over the accepted v25 Home string:

```text
prototypes/frontend/home/archive/b2-edge-attachment-v26/edge-v25-to-v26.js
size       2827 bytes
SHA-256    55b1ef7bdf3215a61e9d8aa4215ed6f93f81d98ee458d4ec7a852a37d99d6812
```

The transform is intentionally bounded to the shell width allowance and the three accepted visual edge targets listed above.

## User-reviewed preview evidence

The final local HTML accepted immediately before this checkpoint was:

```text
DANTE_Home_v38_VERIFIED_OPEN_COLLAPSED_TIMELINE.html
size       83055 bytes
SHA-256    07fab6068427a972f5201454e780d2b7a66db0e10ef9e0f5e80be7be7c5d9f22
```

The repository stores the compact deterministic v25 -> v26 transform rather than duplicating the local review wrapper.

## QA qualification

```text
user visual review of final v38 wrapper          PASS
v26 transform JavaScript syntax                  PASS (node --check)
v26 transform mock-structure execution           PASS
component geometry Chromium 1100 px              PASS
component geometry Chromium 1366 px              PASS
component geometry Chromium 1600 px              PASS
component geometry Chromium 1920 px              PASS
v25 shell/timeline semantics                     PRESERVED
v24 palette/background                           PRESERVED
v23 DANTE identity                               PRESERVED
v22 stage no-persistent-add semantics             PRESERVED
fresh full reconstructed-Home browser matrix     NOT CLAIMED
fresh accessibility rerun                        NOT CLAIMED
separate PARTIAL visual review                   NOT CLAIMED
```

## Explicit non-change

No change to:

- `home.stage.continuity` / Mondi semantics;
- `home.stage.signals` / Segnali semantics;
- v22 no-persistent-stage-add/configuration rule;
- v25 application-bar control order or timeline quick-add semantics;
- Capture/Resolution meaning in the Context Rail;
- date navigation, event drag, zoom, grouping or time-edit behavior;
- DANTE brand master geometry;
- v24 background asset/palette;
- backend/API/domain/logical/physical semantics;
- production frontend framework/runtime selection.

## Still open before B2 closure

- final production semantics for timeline quick-add, including context/date/time prefill and destination;
- legacy Review / historical launcher reconciliation in an explicit bounded scope;
- production semantic-token migration of the working visual skin;
- remaining small shell/detail refinements;
- final responsive, visual and accessibility QA.
