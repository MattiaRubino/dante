# DANTE — Temporal Create C1 Manual Acceptance

**Status:** MANUAL ITERATION ACTIVE — FINAL C1 ACCEPTANCE NOT YET RUN  
**Reconciled:** 2026-09-04  
**Branch:** `feature/home-timeline`  
**Current automated-green code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**CI:** Frontend CI #937 / `33905239085` — FULL GREEN

## 1. Current manual process

The old pre-refactor acceptance protocol is retired. The user is now deliberately validating Create **one UX foundation at a time** before a final closure pass.

Do not convert this into a long checklist during incremental discussion. For each iteration, test only the behavior just agreed.

## 2. Current candidate to inspect

The current manual target is the Create/window coexistence foundation:

### Desktop simple Create

- click `+`;
- panel opens floating at a stable initial position;
- Timeline/Home is not dimmed/frozen;
- Timeline can still be scrolled/interacted with;
- simple panel can be moved;
- draft remains alive while inspecting Timeline;
- outside/backdrop does not silently discard;
- close/Cancel/Escape follow the explicit draft protection contract.

### Desktop Advanced

- `Opzioni avanzate` opens greater depth as a larger floating surface;
- it remains inside viewport;
- Timeline remains usable behind it;
- internal content can scroll without an intrusive visible scrollbar;
- back to simple, close and actions remain reachable.

### Mobile

- no horizontal overflow;
- Advanced remains viewport-bounded.

The possible simple-only left pin/dock mode is NOT part of this current test because it is not implemented.

## 3. Known recurrence limitation — do not fail the wrong layer

Choosing a repeating rule correctly authors recurrence intent, but the current local bridge does not generate the full future recurring series.

That future series belongs to backend recurrence evaluation/canonical Occurrences + temporal range query.

Therefore this incremental manual pass should judge recurrence authoring usability, ownership truth and stored intent, not demand browser-generated canonical future cards.

## 4. Final closure pass — later

When the user has finished the incremental visual/functional polish and asks for final C1 acceptance, write/run one coherent pass covering at least:

- normal Activity speed/clarity;
- normal Event speed/clarity;
- all-day behavior;
- unplaced Activity + Planning Tray;
- Repeat / custom recurrence authoring;
- Event Agenda;
- Advanced disclosure;
- Context vs appearance;
- mobile;
- frozen Timeline regression feel;
- draft close/discard behavior;
- no fake provider/backend success.

Final manual approval token:

`C1 MANUAL PASS — APPROVED`

Until that exact explicit approval, C1 remains OPEN and C2 remains BLOCKED.
