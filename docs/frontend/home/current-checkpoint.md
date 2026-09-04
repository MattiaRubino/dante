# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3-3 CLOSED / VALIDATED / M3-4 NEXT  
**Date:** 2026-09-04  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Do not reconstruct current state from older phase labels, stale chat summaries or historical `NEXT` prose. Historical evidence remains evidence; current sequencing authority lives here and in `world-focus-current-checkpoint.md`.

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
M3-2 adaptive candidate resolver            CLOSED / VALIDATED
PRE-M3-3 customization reachability safety  CLOSED / PASS
M3-3 Manual Customize UX                    CLOSED / VALIDATED
M3-4 integrated adaptive composition         NEXT / NOT STARTED
M3 final hostile closure                     BLOCKED BY M3-4
M4 Contextual DANTE / D2–D6                 BLOCKED BY M3
M5 complete contrasting Worlds              BLOCKED BY M4
M6 integrated visual/a11y/performance review BLOCKED BY M5
M7 pre-backend frontend freeze              BLOCKED BY M6
BACKEND                                     BLOCKED UNTIL M7
human/manual visual review                  NOT PERFORMED
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

M3-2 validation
HEAD b7892642dd66104ec04ea4b08ca11aa123789fa4
CI   33854543037 PASS
74 / 74 web test files; 356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations

PRE-M3-3 safety closure
HEAD 7781c6751a455767595eaf159747da833117f8b2
CI   33862549244 PASS
75 / 75 web test files; 362 / 362 web unit tests
288 modules / 804 dependencies / 0 architecture violations

M3-3 valid RED
PRE-SCOPE 7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
HEAD      fd1d503268608df89724e216f3a5fc59f697dbef
CI        33875210161 EXPECTED FAILURE
362 / 362 pre-existing web unit tests PASS
5 / 5 new M3-3 tests FAIL because Customize was absent

M3-3 baseline green
HEAD 168d3c9565914c8fcc47a578c0750b030d42223f
CI   33876915226 PASS

M3-3 hostile closure
HEAD 1978fe5c77c0e2661239372bf0f9bee238021faa
CI   33879774332 / run #907 PASS
77 / 77 web test files; 376 / 376 web unit tests
294 modules / 851 dependencies / 0 architecture violations
Quality / build / diff / mutation / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
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
adopt != semantic truth != authorization != persistence
```

## 5. M3-3 closed result

M3-3 now provides the actual manual/non-AI customization experience over the canonical M3 transaction:

```text
View mode
-> explicit Customize
-> isolated draft from accepted in-memory config
-> meaningful unconfigured opportunity must enter through adopt
-> pin / unpin / hide / show / move / promote / restore
-> review
-> Apply | Cancel
```

The route-scoped customization owner keeps accepted config, draft, read state and conflict/invalid-state handling in memory. This is not durable persistence.

The aggregate customization reader consumes the seven existing M1 runtime seams and returns only bounded M3 opportunity metadata. It does not leak projection payload, references, reason codes or authorization/disclosure state.

Reorder is deterministic and keyboard-operable without drag. Focus remains on the moved entry and assistive technology receives the resulting position.

Apply uses `applyWorldFocusCompositionDraft` only, advances revision exactly once on success and never merges/rebases conflicts implicitly. Cancel preserves accepted config and revision. Cancel/Escape/successful Apply restore focus to the exact invoker.

The surface uses the existing finite World surface registry. Wide allocation presents the requested sidecar; compact allocation degrades through the existing Workspace allocator to overlay. No AppShell modal hack or new surface planner exists.

Normal live World composition intentionally remains pre-M3-4.

## 6. M3-3 hostile quality bar achieved

Automated coverage proves:

```text
bounded seven-reader aggregation and cancellation
no payload/reference/reasonCode/AuthZ leakage
adopt + all canonical manual commands
keyboard reorder + focus + SR announcement
Apply once / revision N -> N+1
revision conflict without merge/rebase
invalid base fail closed
sparse World remains sparse
wide sidecar / compact overlay
pressure widths 1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 /
  721 / 720 / 719 / 390
no horizontal overflow
axe checks
forced-colors operability
```

Human visual acceptance remains **NOT PERFORMED** and must not be inferred from CI.

## 7. Current gate — M3-4 Integrated Adaptive Composition

M3-4 is next and **not started**.

Its target is to integrate the already-validated composition pipeline into normal World rendering:

```text
validated M1 results
-> meaningful opportunities
+ accepted M3 config
+ finite value signals
-> M3-2 candidate resolver
-> existing Workspace planner
-> finite registry
-> CompositionHost
```

Required invariants:

```text
sparse remains sparse
hidden remains hidden
pinned user intent survives adaptive budget
configured order remains user-owned
configured supporting stays supporting unless promoted
unresolved pin does not create fake content
unknown future kinds remain safe/representable
renderer failure remains local
no fake persistence
no frontend Domain/AuthZ authority
```

Before M3-4 writes: fresh live HEAD, read-only preflight, exact CREATE/UPDATE/DELETE/PRE-SCOPE/red-first/out-of-scope gate, then explicit authorization.

## 8. Stop lines

```text
NO M3-4 write without a fresh bounded gate
NO M3 final hostile closure before M3-4
NO M4 / D2–D6 before M3 closes
NO localStorage fake persistence
NO durable server/cross-device persistence yet
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
NO generated route-tree edits
NO claim of human visual acceptance from automated green
```

Backend remains after M7 only.

## 9. Operational rules

- stay on `feature/home-react` unless explicitly authorized otherwise;
- fresh live HEAD before every new write scope;
- define exact CREATE / UPDATE / DELETE scope and PRE-SCOPE before writes;
- red-first for new ownership or adversarial behavior where appropriate;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- fix CI root causes rather than weakening tests;
- old phase-time `NEXT` prose is historical evidence unless adopted by current authority.
