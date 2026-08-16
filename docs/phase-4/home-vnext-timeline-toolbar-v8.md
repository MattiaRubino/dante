# LifeOS — Home vNext Timeline Toolbar v8

**Date:** 2026-08-16  
**Branch:** `prototype/phase-4-today-home`  
**Status:** APPROVED WORKING VISUAL CHECKPOINT — current preferred Home/Today presentation state; not production React code and not a final IA decision  
**Parent checkpoint:** `docs/phase-4/home-vnext-soft-surfaces-v1.md`

---

## 1. Purpose

This checkpoint freezes the Home vNext state after the user approved the latest timeline-toolbar arrangement. It preserves the previously accepted soft-surfaces Home, professional AI chat, orientation strip and mature Today behavior, while recording the current timeline chrome arrangement.

Exact archived artifact:

- filename: `lifeos_home_timeline_toolbar_verified_v8.html`
- size: `307487` bytes
- SHA-256: `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`
- reconstruction base: `docs/phase-4/home-vnext-soft-surfaces-v1.md` / exact restored `lifeos_home_vnext_soft_surfaces.html`
- delta payload: `prototypes/home/archive/home-vnext-timeline-toolbar-v8/v8_fragment.html.gz.b64`
- decoded fragment SHA-256: `dd1b81859548eaa3c299ef8db903e0f26c9f69b30b8c68635b100bed29e834bd`

---

## 2. Approved working timeline toolbar arrangement

The timeline chrome is currently arranged as:

```text
[ agosto 2026 ▾ ] [ Ora ] [ ‹  LUN MAR MER GIO VEN SAB DOM  › ] [ icon Legenda ] [ icon Espandi ]

[ ○ reset selection ] [ Focus ] [ Riunioni ] [ Salute ] [ Creatività ] [ Personale ] ...

[ time axis ] [ timeline / events ]
```

Current visual decisions:

- month/year stays on the left and opens the existing calendar;
- `Ora` is immediately to its right;
- week navigation follows, with previous/next arrows;
- only icons for `Legenda` and timeline expansion remain at the far right;
- this far-right placement must remain true in compact and expanded timeline states;
- the group row is separate from the control toolbar;
- the group row keeps the reset-selection circle followed by the clean group chips;
- group presentation must stay synchronized with the timeline column geometry rather than being positioned independently by eye.

The user approved saving this v8 state after the final change moving `Ora` left and removing the visible `Legenda` / `Espandi` text labels.

---

## 3. Home state inherited from the previous checkpoint

This checkpoint continues to preserve the vNext Home direction documented in `home-vnext-soft-surfaces-v1.md`:

- lightweight global orientation strip;
- modern professional AI chat surface;
- collapsible AI rail;
- `Adesso` structurally present but semantically still unresolved;
- ex-Worlds/main-stage semantics still unresolved;
- soft-surfaces visual language rather than decorative nested panel chrome;
- mature Today/timeline behavior retained as the behavioral reference.

The top-bar vocabulary remains intentionally pending later review.

---

## 4. Timeline functionality that remains protected

Do not treat the toolbar redesign as permission to simplify the Today engine. Preserve the existing behavioral contract, including at minimum:

- 24-hour timeline;
- nonlinear density mapping;
- adaptive event cards;
- overlap handling;
- group filters and grouped expansion;
- margins/gap semantics;
- card focus;
- subtasks and mapper reflow;
- drag/move/cross-day/Undo;
- zoom;
- time editing;
- past/future day navigation;
- synchronized week strip;
- month/year calendar navigation;
- contextual `Ora` action;
- timeline panel expansion.

`docs/phase-4/today-v21.md` and `tests/prototypes/today-v21-regression.py` remain regression authorities for the underlying Today behavior.

---

## 5. QA / validation status

The exact v8 file is the user-approved visual checkpoint from the interactive review.

Static integrity inherited/performed during the iteration includes:

- no duplicate DOM IDs in the delivered candidate;
- inline JavaScript syntax checks passed in the candidate lineage;
- the saved artifact is archived byte-for-byte with SHA-256 `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`.

Important process rule for future timeline edits:

> functional changes require real browser regression checks; visual changes require visual browser verification before delivery.

Do not use `node --check` alone as evidence that Today is visually or behaviorally safe.

Several intermediate timeline experiments in the conversation were rejected because they changed or misaligned timeline/group geometry. They are **not approved checkpoints** and must not be reconstructed or used as a base. Continue from this v8 artifact or from the archived predecessor if explicitly rolling back.

---

## 6. Known prototype debt

This standalone HTML remains an iterative coded UX prototype. It contains accumulated CSS/JS override layers from previous Home/Today iterations. It is a visual/behavioral reference, not the target React component architecture.

When production implementation begins, preserve the accepted behavior and visual grammar while replacing the patch-stack with explicit component ownership and tested layout primitives.

---

## 7. Next exact sequence

After this saved checkpoint, the intended sequence is:

1. only small visual corrections if clearly necessary;
2. decide what the two disappearing/secondary Home areas should contain;
3. define the exact information contract of `Adesso` (current placeholder cells are not product truth);
4. then decide which elements open inline expansions, popovers/overlays, dedicated pages or full workspaces;
5. only after those decisions continue toward production React/Node architecture.

Do not reopen broad architecture or semantic naming without a concrete reason.
