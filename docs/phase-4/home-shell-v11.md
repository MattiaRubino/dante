# LifeOS — Phase 4 Home Shell v11

- Status: **Accepted visual/interaction checkpoint for the Home shell**
- Date: 2026-08-10
- Branch: `prototype/phase-4-today-home`
- Pull request: #2
- Prototype type: standalone HTML/CSS/JavaScript with simulated data
- Exact local source used for this checkpoint: `preview_11_compact_hero_vertical_spacing.html`
- SHA-256: `d21e54fce4f6417149b2b86e26bd2f3229581b716d6440459702add9c4f17c19`

## Purpose

Freeze the accepted Home visual shell before the next Phase 4 task: integrating the full Home/Today v21 timeline engine into this new shell without losing timeline behavior.

This checkpoint does **not** replace the v21 timeline engine. It freezes the new Home shell that the v21 timeline must be integrated into.

## Authority and integration boundary

For the next iteration, use both sources:

1. **Home shell authority:** this document + the restorable Home Shell v11 archive.
2. **Timeline behavior authority:** `docs/phase-4/frontend-master.md`, `docs/phase-4/today-v21.md`, `tests/prototypes/today-v21-regression.py`, and the v21 restorable prototype material.

Do not use the simplified Today block currently visible in Home Shell v11 as the functional timeline source. It is only a visual placeholder under the new Home shell.

## Accepted Home shell structure

### Global topbar

Accepted order:

```text
LifeOS brand | + Crea        Home | Mondi | Oggi        Cerca | Review | Grid | Profilo
```

Rules:

- `+ Crea` is the primary global create action and remains in the global shell, not next to `Ciao, Mattia`.
- The button is explicit (`+ Crea`), not an ambiguous standalone plus on desktop.
- Search belongs to the right utility cluster and opens the global LifeOS search/command surface.
- `Review` opens the Review Queue and keeps its badge/count behavior.
- `Grid` remains the launcher placeholder for secondary/global LifeOS surfaces; its final content is intentionally still open.
- Profile remains the right-most account/settings entry point.
- `Home / Mondi / Oggi` are primary destinations and must not be confused with the Home-internal Worlds/Stats surface switch.

### Home hero — three-zone composition

The Home hero uses three coordinated zones:

1. left: greeting + compact LifeOS conversational assistant;
2. center: Worlds/Stats spatial stage;
3. right: contextual detail for the selected World/statistic.

The layout is intentionally spatial/layered and must not regress into a flat card dashboard.

### Left assistant

Accepted behavior and visual direction:

- `Ciao, Mattia` remains outside the chat card as the Home greeting.
- Remove permanent labels such as `LifeOS AI` and `Proposta · da confermare` from the chat header.
- The assistant reads as a compact mobile-like conversation, not as a dashboard widget.
- The conversation area has a clearly perceptible semi-opaque internal surface so users immediately understand where LifeOS responses appear.
- Contextual proposal actions belong to the relevant message, not to a global chat status.
- composer remains at the bottom;
- expansion control remains at the upper-right of the assistant;
- `Continua su` remains a manual handoff control with ChatGPT / Claude options;
- external handoff is currently a prototype/interaction placeholder, not a finished provider integration.

### Center stage — Worlds

- Worlds are displayed in the Synaptic Nebula spatial/cosmic stage.
- World cards primarily communicate icon + name; no permanent percentage text.
- left/right carousel arrows loop continuously;
- drag loops continuously;
- clicking a non-central World selects it **and moves it to the center**;
- pointer click and drag must remain distinct: a click below the movement threshold centers the clicked item, while a real drag preserves drag behavior;
- selected World drives the contextual rail on the right.

### Center stage — Stats

- Stats use the same operational navigation contract as Worlds.
- left/right arrows loop continuously;
- drag loops continuously;
- clicking a non-central statistic selects it and moves it to the center;
- at rest exactly **three stat cards** are visible;
- no faded/ghost fourth or fifth card should bleed into the viewport;
- internal duplicate cards may exist only as an implementation mechanism for infinite looping, never as visible edge content;
- selected statistic drives the contextual rail on the right.

### Worlds / Stats surface switch

The old upper `Worlds | Stats` toggle is removed.

Accepted lower control:

```text
‹  WORLDS  ›
```

or

```text
‹  STATS  ›
```

Rules:

- small left/right arrows change the **surface type** (Worlds ↔ Stats and future peer surfaces);
- the center label is clickable and retains the previous center-button meaning: expand/open the full version of the current surface;
- when the surface changes, the center label and expansion target change with it;
- these arrows must remain visually and functionally distinct from the larger carousel arrows that move between Worlds/stat cards.

### Right contextual rail

- content changes with the currently selected World/statistic;
- the rail is contextual, not a fixed dashboard sidebar;
- compact Home detail stays concise;
- deeper information belongs to the expanded/full surface.

## Spacing checkpoint

The empty vertical gap between the topbar and the Home hero content was reduced in v11.

Accepted result:

- greeting and three-zone hero start higher;
- central Worlds/Stats stage starts higher;
- total hero height is reduced;
- the Today/timeline area below therefore rises and gains more viewport space;
- this is a layout/spacing change only and must not alter carousel/chat behavior.

## Functional validation preserved into v11

The carousel and topbar interaction work was functionally tested during the preceding accepted iterations, including:

- Worlds arrow navigation;
- Worlds click-off-center → center;
- Worlds drag;
- Stats arrow navigation;
- Stats click-off-center → center;
- Stats drag;
- Worlds ↔ Stats lower surface switch;
- exactly three visible Stats cards;
- `Continua su` menu;
- `+ Crea` menu;
- global Search menu.

The v10 and v11 changes are CSS-only refinements relative to the last tested interaction build. The complete JavaScript payload is byte-identical across preview 9, 10 and 11 after extraction:

```text
SHA-256 5359032364fc0f5d23ed81621786958866bde67ffffd16d8a7eca3601ee947fc
```

Final v11 JavaScript syntax validation:

```text
8 script blocks
node --check: PASS on all 8
```

Visual acceptance: the user approved the v11 shell in the Phase 4 design review conversation on 2026-08-10 and requested that it be frozen/documented before timeline integration.

## Explicitly open / not frozen as finished functionality

- final content and information architecture of the 3×3 Grid launcher;
- real ChatGPT/Claude handoff/provider integration;
- production component architecture (React/Next.js conversion);
- final logo/brand asset beyond the current prototype lockup;
- full Worlds and full Stats expanded surfaces;
- final mobile/responsive solution;
- real backend/API data.

## Next exact task — timeline integration

Do **not** redesign the timeline from scratch.

Integrate the existing v21 timeline engine beneath/inside the accepted Home Shell v11 while preserving the v21 behavior contract, including at minimum:

- complete 24-hour timeline;
- density mapper;
- overlap lanes;
- stable global groups;
- filtering without geometry changes;
- grouped expansion and conditional horizontal scroll;
- drag subsystem with threshold, fixed overlay, auto-scroll, cross-day move, Esc cancel and undo;
- cluster-based margins;
- current-time line;
- environmental path/options;
- focus behavior;
- detail popup;
- subtasks;
- semantic zoom;
- anchored time picker;
- manual minute precision and undo;
- progressive multi-day navigation.

Integration rule: **Home Shell v11 owns the outer visual shell; timeline v21 owns timeline behavior.** Any conflict must be resolved deliberately and documented, never by silently dropping timeline capability.

## Restorable artifact

Archive location:

```text
prototypes/home/archive/v11/
```

The archive contains a gzip-compressed base64 representation of the exact v11 HTML, split into parts for repository portability, plus a restore script.

Expected restored SHA-256:

```text
d21e54fce4f6417149b2b86e26bd2f3229581b716d6440459702add9c4f17c19
```
