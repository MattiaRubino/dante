# B2 Home Infrastructure Color v27

**Branch:** `prototype/frontend`  
**Date:** 2026-08-23  
**Status:** **USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN**  
**Base:** B2 Home Edge Attachment v26 over B2 Home Shell + Timeline Quick Add v25 over B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22

## Decision

The accepted Home working baseline advances to **v27** for a strictly bounded infrastructure-color normalization pass.

v27 removes the remaining legacy purple from generic Home/Today chrome that the user explicitly reviewed and accepted, while preserving semantic colors for Mondi, timeline groups and event/category identity.

This checkpoint does **not** reopen v26 geometry, v25 shell/timeline composition, v24 palette/background, v23 DANTE identity, v22 Home-stage semantics, Context Rail meaning, or backend/domain contracts.

## Accepted color contract

Generic infrastructure follows the DANTE visual language:

```text
primary / active / selected interaction = DANTE orange
inactive generic controls               = neutral blue-grey / charcoal
semantic content identity               = preserve category/world color
```

The accepted pass specifically covers the remaining purple chrome reviewed in the Today surface:

```text
Ora
selected/current week day
current-time line / marker
Cattura add control
Cattura send control
Cattura "Registrato" status dots
Da risolvere icon/count chrome
Da risolvere "Conferma" action
```

The implementation targets the real `lifeos-today` Shadow DOM after the component has rendered, and reapplies the accepted colors across relevant state/rerender changes.

## Explicitly preserved semantic colors

v27 does **not** flatten or recolor semantic identities such as:

- Mondi/world colors (`Corpo`, `Viaggi`, `Musica`, `Studio`, etc.);
- timeline group colors (`Focus / lavoro profondo`, `Riunioni`, `Salute`, `Creatività`, etc.);
- event/category border colors;
- success/warning/error semantics where the color represents state rather than generic chrome.

## Durable transform

The accepted v27 color state is stored as a deterministic transform over the accepted v26 Home string:

```text
prototypes/frontend/home/archive/b2-infrastructure-color-v27/chrome-v26-to-v27.js
size       5332 bytes
SHA-256    73aa897923aae6523d52d770c4dc1453d61118387198f96b7a01445edcd3b0e1
```

The transform is intentionally bounded to generic infrastructure color. It does not change widths, margins, positioning, radii, stage geometry, timeline geometry, event layout or interaction semantics.

## User-reviewed preview evidence

The final local HTML accepted immediately before this checkpoint was:

```text
DANTE_Home_v43_VERIFIED_INJECTION_COLOR_FIX.html
size       87386 bytes
SHA-256    e82058e4e980208feb3f0c055dab3eec81812be1fa47e5f036e8d5d0e1fe859d
```

The repository stores the compact deterministic v26 -> v27 transform rather than duplicating the local review wrapper.

## QA qualification

```text
user visual review of final v43 wrapper          PASS
v27 transform JavaScript syntax                  PASS (node --check)
v27 transform mock-structure execution           PASS
v26 edge attachment geometry                     PRESERVED
v25 shell/timeline composition                   PRESERVED
v24 palette/background                           PRESERVED
v23 DANTE identity                               PRESERVED
v22 stage no-persistent-add semantics             PRESERVED
semantic World/group/event colors                PRESERVED BY CONTRACT
fresh full reconstructed-Home browser matrix     NOT CLAIMED
fresh accessibility rerun                        NOT CLAIMED
separate PARTIAL visual review                   NOT CLAIMED
```

## Explicit non-change

No change to:

- expanded/collapsed AI edge geometry from v26;
- timeline edge geometry from v26;
- `home.stage.continuity` / Mondi semantics;
- `home.stage.signals` / Segnali semantics;
- v22 no-persistent-stage-add/configuration rule;
- v25 application-bar control order or timeline quick-add semantics;
- Capture/Resolution meaning in the Context Rail;
- date navigation, event drag, zoom, grouping or time-edit behavior;
- DANTE brand master geometry;
- v24 background asset;
- backend/API/domain/logical/physical semantics;
- production frontend framework/runtime selection.

## Still open before B2 closure

- final production semantics for timeline quick-add, including context/date/time prefill and destination;
- legacy Review / historical launcher reconciliation in an explicit bounded scope;
- production semantic-token migration of the accepted working palette/chrome rules;
- remaining small shell/detail refinements;
- final responsive, visual and accessibility QA.
