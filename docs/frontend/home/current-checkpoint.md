# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 CUSTOMIZATION SAFETY CLOSED / PASS / M3-3 NEXT  
**Date:** 2026-09-04  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Do not reconstruct the current state from older phase labels, stale chat summaries or historical `NEXT` prose. Historical evidence remains valid as evidence; current sequencing authority lives here and in `world-focus-current-checkpoint.md`.

## 1. Branch workstreams

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

Permanent distinctions:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

## 2. Live World Focus sequence

```text
WF0 route/shell                              FROZEN / USER AUTHORIZED
WF-G3 geometry                              LOCKED / USER AUTHORIZED
WF-V4 visual treatment                      CANDIDATE
B0 foundation                               ENGINEERING CLOSED
WR0–WR2                                     CLOSED
B1 Orientation                              CLOSED FOR SEQUENCING
B2 Continuity / Resume                      IMPLEMENTED / AUTOMATED PASS
Workspace Platform                          ENGINEERING CLOSED
D0 contextual DANTE spatial contract        ACCEPTED
D1 quiet invoke + compact composer           CLOSED FOR SEQUENCING
WS0–WS8                                     CLOSED
POST-WS8 HYGIENE                            CLOSED / APPLIED
PRE-M0 FALSIFICATION                        CLOSED / PASS
M0 Materialization Mapping                  CLOSED
M1 Core Non-Visual Materialization          CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION                CLOSED / PASS
M2 Shared Visual Primitive Layer            CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION              CLOSED / PASS
M3 Adaptive World Composition               ACTIVE
M3-1 composition configuration foundation   CLOSED / VALIDATED
M3-2 adaptive candidate resolver             CLOSED / VALIDATED
PRE-M3-3 customization reachability safety  CLOSED / PASS
M3-3 Manual Customize UX                    NEXT / NOT STARTED
M3-4 integrated adaptive composition         BLOCKED BY M3-3
M3 final hostile closure                     BLOCKED BY M3-4
M4 Contextual DANTE / D2–D6                 BLOCKED BY M3
M5 complete contrasting Worlds              BLOCKED BY M4
M6 integrated visual/a11y/performance review BLOCKED BY M5
M7 pre-backend frontend freeze              BLOCKED BY M6
BACKEND                                     BLOCKED UNTIL M7
assistant manual visual review              NOT PERFORMED
```

## 3. Current evidence anchors

```text
M0 closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2 final code closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
70 / 70 web test files; 332 / 332 web unit tests
279 modules / 770 dependencies / 0 violations

M3-1 validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations

M3-2 validated code
HEAD b7892642dd66104ec04ea4b08ca11aa123789fa4
CI   33854543037 PASS
74 / 74 web test files; 356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS

PRE-M3-3 customization safety red-first
HEAD be63d49c43c88a491439b4014668a51c8ff8ad6b
CI   33861956558 EXPECTED FAILURE
new safety test 0 / 5 PASS; all 356 pre-existing web tests PASS

PRE-M3-3 customization safety closure
HEAD 7781c6751a455767595eaf159747da833117f8b2
CI   33862549244 PASS
safety test 5 / 5 PASS
75 / 75 web test files; 362 / 362 web unit tests
288 modules / 804 dependencies / 0 architecture violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

## 4. Closed substrate retained

M1 owns non-visual semantic/application seams. M2 owns bounded presentation and renderer vocabulary. Workspace Platform owns planning/placement. M3 consumes those layers; it does not reinterpret canonical Domain truth, AuthZ, provider state or persistence authority.

Permanent non-collapses remain:

```text
World != Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
AI output != fact
Proposal != Decision != effect
timeout != semantic negative
offline != source absent
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
```

## 5. M3-1 + PRE-M3-3 customization contract

The revisioned client composition config still contains composition metadata only:

```text
schemaVersion
revision
worldId
ordered entries[]

entry
  instanceId
  kind
  visibility: visible | hidden
  pinned: boolean
  prominenceOverride: lead | null
```

The finite customization command language is now:

```text
adopt
pin
unpin
hide
show
move
promote
restore
```

Sources remain finite:

```text
manual
dante-proposed
```

`adopt` closes the reachability gap for meaningful opportunities that are not yet represented in the current config. It accepts an already-normalized `WorldFocusCompositionOpportunity` and creates only composition metadata:

```text
visible
unpinned
prominenceOverride = null
```

It does **not** carry projection payload, references, AuthZ/disclosure state, scores, provider data or renderer code. The recorded operation keeps only `source / type / instanceId / kind`.

`restore` means restore to the draft-start base snapshot. Therefore an adopted entry that did not exist in the base snapshot is removed from the draft by `restore`.

Apply is hardened:

```text
revision mismatch
-> revision-conflict

same revision
+ base snapshot structurally identical to current snapshot
-> Apply may produce revision N+1

same revision
+ different base snapshot
-> FAIL CLOSED / invalid draft base snapshot
```

No implicit merge exists.

## 6. M3-2 candidate-resolution contract after hardening

Meaningful opportunity extraction remains sparse and bounded. Configuration precedence remains:

```text
hidden > adaptive signals
pinned > adaptive budget
configured relative order > adaptive ranking
```

The PRE-M3-3 hardening corrects one important prominence rule:

```text
configured + prominenceOverride = null
-> preserve opportunity.defaultProminence

configured + prominenceOverride = lead
-> lead
```

Therefore configuring/adopting a supporting Comparison or Trajectory does **not** silently turn it into primary content. Pin changes stability/ownership, not semantic or presentation importance. Adaptive value bands still apply only to unconfigured opportunities.

Pinned intent without a currently meaningful projection remains `unresolvedPinned`; no empty module is fabricated.

## 7. Current gate — M3-3 Manual Customize UX

M3-3 is next and **not started**.

It must build a professional manual/non-AI Customize experience over the real M3-1/PRE-M3-3 draft engine, not a visual mock or direct config mutation surface.

Required product behavior:

```text
View mode != Customize/Edit mode
explicit enter Customize
current config remains immutable while editing
meaningful unconfigured opportunity -> adopt before later commands
draft-only pin / unpin
draft-only hide / show
draft-only reorder
draft-only promote / restore
review dirty/changed state
Apply through applyWorldFocusCompositionDraft only
Cancel returns base snapshot
revision-conflict / invalid-state treatment
keyboard-first accessible reorder path
touch-usable controls
screen-reader semantics and focus management
responsive layout
```

M3-3 must **not** integrate resolved adaptive candidates into normal live World composition. M3-4 owns that integration.

## 8. M3-3 quality bar

A serious implementation must cover at least:

```text
unit/model integration
component interaction tests
real-browser E2E
keyboard
screen reader semantics
focus entry/return
pointer/touch when applicable
forced-colors
reduced-motion where motion exists
no horizontal overflow
pressure widths: 1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 / 721 / 720 / 719 / 390
```

Drag/drop is optional enhancement. It cannot be the only reorder path. Do not add React Aria or another dependency automatically; evaluate it only if the interaction complexity earns the dependency and accessibility parity can be proven.

## 9. Stop lines

```text
NO M3-4 live integration yet
NO localStorage fake persistence
NO durable server persistence/cross-device sync
NO DANTE D2–D6 before M4
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
NO manual generated route-tree edits
```

Backend remains after M7 only.

## 10. Operational rules

- stay on `feature/home-react` unless explicitly authorized otherwise;
- fresh live HEAD before every new write scope;
- define exact CREATE / UPDATE / DELETE scope and PRE-SCOPE before writes;
- red-first for new ownership or adversarial behavior where appropriate;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- fix CI root causes rather than weakening tests;
- do not claim human visual acceptance from automated green;
- old phase-time `NEXT` prose is historical evidence unless adopted by current authority.
