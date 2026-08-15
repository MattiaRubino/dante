# LifeOS — Home vNext Soft Surfaces v1

**Date:** 2026-08-15  
**Branch:** `prototype/phase-4-today-home`  
**Status:** WORKING VISUAL CHECKPOINT — current preferred Home direction, not final IA and not production frontend code  
**Parent repository HEAD before this checkpoint:** `3354c9e39ebf7c513eef00fdf89c2ae25cb93348`

---

## 1. Purpose

This checkpoint preserves the current Home visual/composition direction after the frontend-architecture exploration moved back from abstract IA discussion to concrete Home validation.

It is intentionally narrower than a final frontend architecture decision. It freezes the current visual working state so subsequent iterations can continue from a known artifact without reconstructing or silently changing the layout.

The exact standalone HTML is restorable from the existing `integrated-v1` baseline plus the deterministic delta archived under:

`prototypes/home/archive/home-vnext-soft-surfaces-v1/`

Restored artifact identity:

- filename: `lifeos_home_vnext_soft_surfaces.html`
- size: `297872` bytes
- SHA-256: `5c38d9a9ed17f0ea950f23f21cf84928b00c4bdfa9fac694bdb282a52373fd56`

---

## 2. Current preferred Home composition

### AI expanded

Conceptual geometry:

```text
TOP BAR

ORIENTATION STRIP
Ciao, Mattia  |  displayed day / date  |  day route / current-person indicator

AI CHAT       |  ADESSO
              |  EX-WORLDS / MAIN STAGE

TIMELINE / TODAY
```

The top bar is still the inherited Home shell for now. Its central labels (`Home | Mondi | Oggi`) remain subject to later review; this checkpoint does not canonize those nouns.

### AI collapsed

Current preferred collapsed geometry:

```text
AI RAIL  |  ADESSO  |  EX-WORLDS / MAIN STAGE

TIMELINE / TODAY
```

The collapsed AI becomes a narrow reopening rail. `Adesso` receives a bounded column and the main stage receives the remaining width.

This is the selected working direction over the alternative where the right side merely expands without changing into a row.

---

## 3. Orientation strip

The following items are grouped as one orientation layer at the top of Home:

- stable greeting (`Ciao, Mattia.` in the prototype);
- displayed day/date;
- the existing day-route/current-person visualization that was previously attached to the Today header.

Reasoning: these elements all answer “where/when am I in the current LifeOS view?” and should not consume vertical space twice across Home and Today.

The strip is visually lightweight rather than a strongly framed dashboard panel.

---

## 4. AI chat surface

The previous compact assistant card was visually rejected as an unprofessional pseudo-chat with arbitrary controls and card-like message treatment.

The current checkpoint changes the chat grammar to a conventional professional conversational UI:

### Standard chat controls

- `+` attachment/add control;
- text composer;
- microphone/audio control;
- send control.

### LifeOS-specific controls only

- `Continua su` handoff, preserving the existing ChatGPT / Claude choices;
- full-screen / expanded conversation;
- collapse to the narrow AI rail.

Normal assistant and user messages are presented as conversation, not as dashboard cards. Extra message-level action rows are not persistently surfaced.

This is a visual/interaction direction. Detailed attachment semantics, audio implementation, external-handoff protocol and AI orchestration are not decided by this checkpoint.

---

## 5. Soft-surfaces direction

The current preferred visual direction reduces visible nested panel chrome without introducing a rule that “panels are bad”.

Current working rule:

> Use a visible container when it represents a real functional surface or interaction boundary. Use spacing, alignment and typography when a hard visual box adds no functional meaning.

In this checkpoint:

- AI chat remains a real functional surface;
- Today/timeline remains a real functional surface;
- orientation is visually open/lightweight;
- `Adesso` is visually lighter and no longer reads as a large card containing smaller cards;
- the ex-Worlds/main stage is not wrapped in an additional visible outer panel;
- actual selectable objects/cards inside a surface may still use cards where useful.

This is a preferred visual direction, not a universal design-system prohibition against panels.

---

## 6. Preserved baseline behavior

The vNext HTML is derived from the existing integrated Home/Today artifact rather than a fresh mockup.

The intent of the iteration was to preserve the existing Home/Today functionality while changing upper-Home composition and chat presentation. In particular, the mature Today/timeline implementation remains the behavioral reference and is not replaced with a generic calendar.

The old contextual right wing remains in the prototype DOM/JS model but is intentionally visually suppressed in the vNext Home composition. This is prototype compatibility, not a statement that the old wing remains part of the future architecture.

---

## 7. What remains OPEN

The following are deliberately unresolved and must not be inferred from placeholder content in the prototype:

1. Exact semantic contents of `Adesso`. The currently rendered status cells are placeholders for layout evaluation.
2. Exact semantics/name of the ex-Worlds/main stage. `World` must not be treated as the final universal LifeOS noun merely because the inherited prototype contains it.
3. Which items warrant dedicated pages, contextual views, popovers, overlays or full-screen workspaces.
4. Final top-bar/navigation nouns and destinations.
5. Detailed Search vs AI vs Create vs Command interactions.
6. Full-screen AI behavior and cross-provider handoff implementation.
7. Final responsive behavior across desktop/tablet/mobile.

The next product-design step after small visual cleanup is to define the actual information contract for `Adesso`, then decide which Home elements expand inline, open overlays/popovers, or lead to deeper surfaces.

---

## 8. Technical QA performed before checkpoint

Static QA was run on the exact archived HTML:

- HTML successfully parsed;
- `<html>`, `<head>`, `<body>` and title present;
- duplicate DOM IDs: `0`;
- external HTTP(S) assets: `0`;
- static `aria-controls` references with missing source targets: `0`;
- inline `onclick` handlers: `0`;
- inline JavaScript blocks syntax-checked with Node.js: `12/12 PASS`;
- archive restore round-trip: PASS;
- restored SHA-256 exactly matches `5c38d9a9ed17f0ea950f23f21cf84928b00c4bdfa9fac694bdb282a52373fd56`.

A headless-browser runtime pass could not be completed in the execution environment because local/file navigation was blocked by the environment administrator. Therefore this checkpoint does **not** claim automated end-to-end runtime verification beyond the static/code checks above and the interactive browser validation already performed during the design iteration.

---

## 9. Known technical debt — do not misread as production architecture

The standalone HTML has accumulated iterative override layers while preserving the older integrated prototype:

- `27` style blocks;
- `12` script blocks;
- late CSS overlays for vNext structure, collapse layout, orientation, professional chat and soft surfaces.

This is acceptable for a restorable visual prototype checkpoint, but it is **not** the target implementation style for React/component migration.

The user-observed slight stutter when collapsing/expanding the AI is consistent with the prototype currently transitioning several layout-affecting properties (`left`, `right`, `top`, `width`, `height`, etc.) across multiple surfaces at once.

Do not spend a major refactor on this standalone HTML unless the prototype itself becomes blocked. When the visual grammar is sufficiently stable and migration begins, implement the layout with clear component ownership and transform/layout strategies that avoid carrying forward the patch stack.

---

## 10. Continuation rule

Resume from this exact checkpoint. Do not:

- revert to the old three-wing Home by assumption;
- convert the professional chat back into a dashboard assistant card;
- restore heavy nested panel framing merely because the old baseline used it;
- treat placeholder `Adesso` cells as approved product semantics;
- treat ex-Worlds as a final domain/category decision;
- remove mature Today/timeline behavior while simplifying Home.

Next intended sequence:

```text
minor visual cleanup
        ↓
define exact ADESSO information contract
        ↓
decide surface / popup / page behavior for Home elements
        ↓
continue frontend architecture validation
```
