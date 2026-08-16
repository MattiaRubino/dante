# LifeOS — Frontend Architecture Handoff — 2026-08-16

**Status:** operational handoff / current frontend continuation checkpoint  
**Branch:** `prototype/phase-4-today-home`  
**Supersedes for continuation:** `docs/phase-4/frontend-architecture-handoff-2026-08-15.md`  
**Current approved working artifact:** `docs/phase-4/home-vnext-timeline-toolbar-v8.md`

---

## 1. Current state

The Web Home macro-composition is close to convergence. The current saved visual state is the v8 timeline-toolbar checkpoint built on top of the previously approved Home vNext soft-surfaces checkpoint.

Restore/use:

`prototypes/home/archive/home-vnext-timeline-toolbar-v8/`

Exact HTML identity:

- size: `307487` bytes
- SHA-256: `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`

Do not continue from the rejected timeline-header / premium-skin / overlay / toolbar experiments that appeared between the soft-surfaces checkpoint and v8. Those were iterative failures and are not repository baselines.

---

## 2. Current Home composition

### AI expanded

```text
TOP BAR

ORIENTATION
Ciao, Mattia | displayed day/date | route/current-person indicator

AI CHAT      | ADESSO
             | EX-WORLDS / MAIN AREA

TODAY / TIMELINE
```

### AI collapsed

```text
AI RAIL | ADESSO | EX-WORLDS / MAIN AREA

TODAY / TIMELINE
```

The AI chat remains a modern standard chat surface with attachment, text, audio and send controls plus only the LifeOS-specific actions: continue to ChatGPT/Claude, full-screen/expand and collapse.

---

## 3. Current timeline chrome — approved working arrangement

```text
[ month/year ▾ ] [ Ora ] [ previous | 7-day week | next ] [ legend icon ] [ expand icon ]

[ reset ○ ] [ group chips ... ]

[ timeline ]
```

Rules to preserve:

- `Ora` stays left, immediately after month/year;
- week navigation stays between `Ora` and the far-right utility icons;
- `Legenda` and expand/compact are icon-only at the far right in both compact and expanded states;
- group controls remain on their own row;
- the reset circle precedes group chips;
- group chips and timeline columns are a single dynamic geometric system, not independent decorative rows;
- never add arbitrary controls before the group chips if doing so breaks group/column alignment.

---

## 4. Validation discipline — mandatory

The Phase 4 workstream explicitly requires:

- functional changes → real browser regression checks;
- visual changes → visual browser verification before delivery.

The real regression authority is `tests/prototypes/today-v21-regression.py`, which covers rendering/collisions, adaptive cards, margins, time picker, zoom and drag among other Today guarantees.

Do not claim a timeline candidate safe merely because JavaScript parses.

---

## 5. Adesso remains unresolved

The current `Adesso` cards/cells are placeholders. The exact content contract is still open.

Useful conceptual distinction remains:

```text
ADESSO
= current situation / what matters for understanding now

MAIN AREA / ex-WORLDS
= significant realities carried forward / goals / priorities / ongoing items

DYNAMIC / IN EVIDENZA
= what deserves attention now

TIMELINE
= temporal reality
```

Do not canonize placeholder values or the `World` noun.

---

## 6. Immediate continuation

The agreed order after the timeline checkpoint is:

1. minor visual corrections only if necessary;
2. decide what belongs in the two secondary/disappearing Home areas;
3. define `Adesso` precisely;
4. then define popovers, inline expansion, deeper pages/workspaces and navigation destinations.

The user explicitly wants structure/content placement decided before detailed popup/page behavior.

---

## 7. Technical caution

The HTML is still an iterative prototype with accumulated override layers. Do not copy this patch-stack into production React/Node code. Use it as the accepted visual/behavioral reference and refactor ownership during production implementation.

The mature Today engine is not a generic calendar mockup and must not be casually restyled by overriding geometry-sensitive selectors.
