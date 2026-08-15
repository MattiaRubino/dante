# LifeOS — Frontend Architecture Handoff — 2026-08-15

**Status:** operational handoff / current frontend continuation checkpoint  
**Branch:** `prototype/phase-4-today-home`  
**Supersedes for continuation:** `docs/phase-4/frontend-architecture-handoff-2026-08-14.md`  
**Authority:** this handoff records the latest working frontend state. It does not override the canonical domain/product/interaction decisions referenced below.

---

## 1. Where the work is now

The frontend exploration has narrowed temporarily to the **Web Home composition only**.

Do not restart broad information-architecture research and do not jump into detailed popup/page behavior yet. The current sequence is:

```text
Home visual structure
        ↓
small visual cleanup
        ↓
exact ADESSO content
        ↓
which elements expand / open popup / open deeper surfaces
```

The exact current visual artifact is frozen by:

`docs/phase-4/home-vnext-soft-surfaces-v1.md`

and archived under:

`prototypes/home/archive/home-vnext-soft-surfaces-v1/`

---

## 2. Current working Home direction

### Expanded AI

```text
TOP BAR

ORIENTATION
Ciao, Mattia  |  displayed day/date  |  route/current-person indicator

AI CHAT       |  ADESSO
              |  EX-WORLDS / MAIN AREA

TODAY / TIMELINE
```

### Collapsed AI

```text
AI RAIL  |  ADESSO  |  EX-WORLDS / MAIN AREA

TODAY / TIMELINE
```

This row-style collapsed variant is the current preferred test direction.

Important: this is a **working visual checkpoint**, not a final product IA decision.

---

## 3. Current visual language

The user preferred the latest **soft-surfaces** iteration over the more panel-heavy version.

Do not interpret this as “no panels”. Current rule:

> visible panels/surfaces are appropriate when they have a real functional boundary; otherwise prefer spacing, alignment and typography over decorative boxes.

Current application:

- AI = real surface;
- Timeline/Today = real surface;
- Orientation = lightweight/open;
- Adesso = lightweight/open;
- ex-Worlds outer area = open;
- real selectable objects inside those areas may still use cards/panels.

---

## 4. AI chat direction is now materially clearer

The previous assistant-card treatment was rejected visually.

The desired chat should look and behave like a modern professional chat interface, not like a dashboard component pretending to be chat.

Normal persistent controls:

```text
+ attachment/add
text input
microphone/audio
send
```

LifeOS-specific additions:

```text
Continua su → ChatGPT / Claude
full-screen / expand
collapse → narrow AI rail
```

No permanent row of arbitrary message buttons. Structured AI output may later render structured UI when warranted, but ordinary conversation should remain ordinary conversation.

React/Node will improve implementation quality and motion, but **must not be expected to repair a bad design automatically**. Preserve this visual grammar during migration.

---

## 5. `Adesso` — current status

`Adesso` has a structural place in the current Home candidate, but its exact content is **NOT YET DECIDED**.

The current cells in the prototype are layout placeholders and must not be treated as product semantics.

The prior conceptual distinction remains useful:

```text
ADESSO
= current situation / what the user needs to know to understand where they are now

MAIN AREA / ex-WORLDS
= significant things being carried forward / goals / priorities / ongoing realities

DYNAMIC / IN EVIDENZA
= what LifeOS judges deserves attention now

TIMELINE
= temporal reality
```

The next substantive design pass should determine what `Adesso` actually contains, with real examples and constraints, before deciding navigation or popup mechanics around it.

---

## 6. Search / AI / Create / Command distinction remains important

Do not collapse these into one concept:

```text
SEARCH
→ find something that already exists

AI / CHAT
→ discuss, reason, ask, modify, negotiate

CREATE
→ add something

COMMAND
→ execute a quick action
```

The current Home chat is the AI/conversation channel, not Search.

---

## 7. Existing baseline that must remain protected

The vNext artifact was derived from the existing integrated Home/Today baseline. It is not a greenfield mockup.

Continue to protect the mature Today/timeline behavior documented by:

- `docs/phase-4/today-v21.md`
- `docs/phase-4/frontend-master.md`
- `docs/phase-4/home-today-integrated-v1.md`

The current Home restructuring must not silently remove timeline density, overlap handling, groups, subtasks, drag/move/undo, zoom/time editing, day navigation, week strip, calendar navigation, `Ora`, expansion, or other previously integrated behavior.

The top bar is intentionally left essentially as inherited for now. The central `Home | Mondi | Oggi` language/navigation is explicitly pending later review.

---

## 8. `World` / ex-Worlds caution

The inherited stage is still referred to operationally as `ex-Worlds`, `main area`, or `main stage` during exploration.

Do not promote `World` into a universal LifeOS semantic container.

The useful visual/stage mechanics may survive while the semantic model and naming change.

Goals/objectives must not disappear merely because the old `World` noun is under review. Where Goals ultimately live or how they surface remains a later product/UI decision.

---

## 9. Technical status of current HTML

The exact snapshot passed static integrity checks:

- no duplicate IDs;
- no external network assets;
- no static broken `aria-controls` targets;
- 12/12 inline JS blocks pass `node --check`;
- exact baseline + archived delta reconstructs the final HTML byte-for-byte with verified SHA-256.

Known limitation:

- collapse/expand motion is slightly stuttery;
- the prototype contains accumulated CSS/JS override layers from iterative design work;
- this is acceptable for the standalone checkpoint but should **not** be copied as the production React component structure.

Treat the HTML as a behavior/visual reference. Refactor component ownership during migration once the Home grammar is stable enough.

---

## 10. Objectivity protocol still mandatory

Keep conclusions separated as:

- **DECIDED / DOCUMENTED**
- **EVIDENCE**
- **DEDUCTION**
- **OPEN HYPOTHESIS**

Do not call a checkpoint “final architecture”. Do not flip direction merely because the latest suggestion sounds plausible. Evaluate alternatives against the LifeOS product contract and the concrete interface already built.

---

## 11. Immediate continuation

The user considers the Home macro-composition close to convergence.

Next:

1. make only small visual fixes that are clearly needed;
2. define the exact `Adesso` information contract;
3. then decide which items deserve inline expansion, popovers/overlays, dedicated views/pages, or other surfaces;
4. only after those decisions continue toward the production React/Node implementation architecture.

Do not reopen broad market/competitor/psychology research unless a specific unresolved question genuinely requires it.
