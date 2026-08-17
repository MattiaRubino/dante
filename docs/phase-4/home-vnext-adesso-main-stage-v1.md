# LifeOS — Home vNext Adesso + Main Stage v1

**Date:** 2026-08-17  
**Branch:** `prototype/phase-4-today-home`  
**Status:** APPROVED WORKING VISUAL CHECKPOINT — current preferred Home upper composition; iterative prototype, not production React/Node code and not a final IA vocabulary decision  
**Parent checkpoint:** `docs/phase-4/home-vnext-timeline-toolbar-v8.md`

---

## 1. Purpose

This checkpoint freezes the Home state approved after the v8 timeline-toolbar checkpoint while the upper Home composition was redesigned around three distinct situational roles:

- current moment / next (`Ora` + `Prossimo`);
- `In evidenza` as a consequential attention band;
- a contextual rotating discovery/suggestion area shown as `Per te` in the prototype.

The intent is to preserve the documented **stable semantics + adaptive presentation** direction without turning Home into a dashboard of permanent widget cards.

Exact artifact identity:

- filename: `lifeos_home_v8_world_stats_switch_contextual_v23_safe_mid_divider.html`
- size: `344559` bytes
- SHA-256: `a45d1f2b5fab677d738306154a93697e497ffb2c8b2e36ddbba4f4289b42cc77`
- exact v8 prefix: **yes** — the first `307487` bytes are byte-identical to the approved v8 artifact
- v8 SHA-256: `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`

The exact checkpoint is archived as a deterministic delta over the approved v8 artifact:

- payload: `prototypes/home/archive/home-vnext-adesso-main-stage-v1/v23_fragment.html.gz.b64`;
- restore script: `prototypes/home/archive/home-vnext-adesso-main-stage-v1/restore_v23.py`;
- decoded fragment SHA-256: `f79c603823ba34cc2ef5a52e8545fc97234cef1ff1879e6949f188e6aff12815`.

The restore script was executed before checkpointing and reproduced the `344559`-byte artifact byte-for-byte.

---

## 2. Current visual composition

### AI expanded

The upper Home area remains an open composition rather than a row of obvious cards:

```text
AI CHAT | ORA / PROSSIMO     IN EVIDENZA     PER TE
        |                    MAIN WORLDS / STATS STAGE
```

Working visual rules:

- `Ora` is visually dominant and does not need a visible `ADESSO` heading;
- `Prossimo` is subordinate to the current moment rather than a separate module;
- `In evidenza` is long/low and reads more like an editorial attention band than a third equal widget;
- `Per te` is dynamic/rotating contextual content, not an advertisement surface;
- obvious nested panel chrome is avoided;
- separators use the LifeOS purple/cyan palette and remain low-weight hierarchy cues rather than decorative neon objects.

### AI collapsed

The representation adapts when the AI chat collapses:

```text
AI RAIL | ORA / PROSSIMO  | IN EVIDENZA
        |                 | MAIN STAGE
        | PER TE          |
```

Current collapsed decisions:

- `Ora/Prossimo` and `Per te` remain stacked in the left contextual column;
- they are not restored as heavy cards/panels;
- one long right-side brand divider groups the stacked contextual area;
- one horizontal divider between the two stacked areas prevents them reading as one undifferentiated block;
- `In evidenza` remains a long band above the main stage;
- the main Worlds/Stats stage retains its own spatial region.

This is a representational adaptation of the same semantics, not a second information model.

---

## 3. Worlds / Stats surface selector

The selector remains associated with the surface it controls rather than becoming another Home toolbar.

Current rules:

- in `WORLDS`, the selector sits just above the active central World object;
- in `STATS`, it uses a different vertical placement above the statistics group so it does not overlap the central card;
- changing AI expanded/collapsed state must not introduce vertical travel/inversion of the stage;
- the underlying Worlds and Stats geometry must not be casually moved to accommodate the selector.

`Worlds` remains historical prototype vocabulary and is **not** canonized as a Domain Model primitive or final product noun.

---

## 4. Semantic distinction to preserve

```text
ORA / PROSSIMO
= current moment + immediate continuation

IN EVIDENZA
= a materially relevant change, risk, constraint, mismatch or upcoming item that deserves attention

PER TE / DYNAMIC
= contextual suggestions, opportunities or discoveries that may be useful, but are not equivalent to alerts

MAIN STAGE
= significant realities carried forward / contextual projection

TIMELINE
= temporal reality
```

Do not collapse `In evidenza` and dynamic suggestions into one semantic category.

---

## 5. QA / integrity gate

Static integrity performed before checkpointing:

- approved v8 is an exact byte-for-byte prefix;
- accepted v20 predecessor is also an exact byte-for-byte prefix of v23;
- duplicate DOM IDs: **0**;
- full inline CSS parse errors: **0**;
- inline JavaScript syntax failures: **0** across 14 scripts;
- all 13 scripts inherited from v8 remain hash-identical;
- exactly one post-v8 script exists and is scoped to the new Home upper composition;
- no CSS selector or new JavaScript added after v8 references `lifeos-today`, Today timeline selectors, event-card selectors, time-picker selectors or timeline modal/toast internals;
- v23 relative to v20 adds only three collapsed-state CSS rules and only `background-image`, `background-repeat`, `background-position`, and `background-size` properties.

Therefore the final v23 divider correction cannot change geometry, DOM structure, JavaScript behavior or Today internals.

### Browser-regression limitation

A full automated Chromium run was attempted in the current execution environment. Local navigation is blocked by runtime policy (`ERR_BLOCKED_BY_ADMINISTRATOR`) and `set_content` / CLI Chromium hangs on the full accumulated prototype lineage. Therefore **no false full-E2E PASS is claimed**.

Visual acceptance comes from the interactive browser review during the iteration. `tests/prototypes/today-v21-regression.py` remains the real browser regression authority when executed in an environment able to run the complete prototype.

---

## 6. Rejected intermediates

Do **not** continue from intermediate v11–v22 experiment files individually. Several were explicitly rejected because they caused overlapping layouts, restored unwanted panel chrome, misplaced the Worlds/Stats selector, or used intrusive divider effects.

This checkpoint supersedes those experiments as the continuation artifact.

---

## 7. Next continuation

1. preserve this upper Home geometry unless a concrete visual bug is found;
2. next review the two secondary/disappearing areas beside the timeline (`Appunti` / `Review` placeholders) and decide their actual product role;
3. only then define deeper popovers, inline expansions, dedicated pages/workspaces and navigation destinations;
4. keep Today/timeline behavior protected while those Home areas evolve.
