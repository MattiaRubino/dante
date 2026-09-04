# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / M3-3 NEXT  
**Date:** 2026-09-04  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Do not reconstruct current state from older phase labels or chat summaries.

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

## 2. Live World Focus state

```text
WF0 route/shell                           FROZEN / USER AUTHORIZED
WF-G3 geometry                           LOCKED / USER AUTHORIZED
WF-V4 visual treatment                   CANDIDATE
B0 foundation                            ENGINEERING CLOSED
WR0–WR2                                  CLOSED
B1 Orientation                           CLOSED FOR SEQUENCING
B2 Continuity / Resume                   IMPLEMENTED / AUTOMATED PASS
Workspace Platform                       ENGINEERING CLOSED
D0 contextual DANTE spatial contract     ACCEPTED
D1 quiet invoke + compact composer        CLOSED FOR SEQUENCING
WS0–WS8                                  CLOSED
POST-WS8 HYGIENE                         CLOSED / APPLIED
PRE-M0 FALSIFICATION                     CLOSED / PASS
M0 Materialization Mapping               CLOSED
M1 Core Non-Visual Materialization       CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION             CLOSED / PASS
M2 Shared Visual Primitive Layer         CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION           CLOSED / PASS
M3 Adaptive World Composition            ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver          CLOSED / VALIDATED
M3-3 manual Customize UX                  NEXT
M3-4 integrated adaptive composition      BLOCKED BY M3-3
M3 final hostile closure                  BLOCKED BY M3-4
M4–M7                                    BLOCKED BY SEQUENCE
D2–D6                                    DEFERRED TO M4
BACKEND                                  BLOCKED UNTIL M7
assistant manual visual review           NOT PERFORMED
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

M3-1 red-first
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE

M3-1 validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations

M3-2 red-first
HEAD c2688c46bcbdaf06f2c5da9470bae967550b456d
CI   33854105057 EXPECTED FAILURE
pre-production contracts PASS; M3-2 owner modules intentionally absent

M3-2 initial production candidate
HEAD 6486c99ce1f83d3fe463c2a1b065fa994b206c6a
CI   33854374288
one test-harness lint failure only; production owner lint issue not observed

M3-2 validated code
HEAD b7892642dd66104ec04ea4b08ca11aa123789fa4
CI   33854543037 PASS
74 / 74 web test files; 356 / 356 web unit tests
287 modules / 797 dependencies / 0 architecture violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

## 4. Closed substrate retained

M1 owns non-visual semantic/application seams. M2 owns bounded presentation and renderer vocabulary. M3 consumes both and does not reinterpret them.

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
```

## 5. M3-1 retained result

M3-1 owns revisioned client composition metadata and isolated customization drafts:

```text
WorldFocusCompositionConfig
  schemaVersion
  revision
  worldId
  ordered entries[]

commands
  pin / unpin / hide / show / move / promote / restore
```

Apply is the only transition creating revision `N+1`; stale revision returns `revision-conflict`; cross-World Apply fails closed; no implicit merge.

Manual UI and future DANTE proposals share the same finite command language and Apply/revision guards.

## 6. M3-2 validated result

M3-2 now owns the production candidate-resolution seam **before** the existing composition planner.

```text
validated M1 results
  -> meaningful opportunity extraction
  -> current M3-1 config + finite value signals
  -> adaptive candidate resolver
  -> WorldFocusCompositionCandidate[]
  -> existing planner
```

Meaningful opportunities only:

```text
Situation ready + content               -> situation
Continuity ready/partial/stale + content -> continuity
Attention ready                         -> one candidate per primitive
Next ready + content                    -> next
Comparison ready                        -> one candidate per primitive
Trajectory ready                        -> one candidate per primitive
Evidence/History with any role content  -> evidence-history
empty/unavailable                       -> no fabricated opportunity
```

Opportunity metadata does not retain projections, references, reason codes, Domain payload, disclosure/AuthZ state or renderer code.

Finite ranking signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No confidence, `aiRelevance` or weighted score exists.

Config precedence:

```text
hidden > signals
pinned > adaptive budget
configured relative order > adaptive ranking
promote -> lead presentation override only
```

Pinned but currently non-meaningful content becomes explicit `unresolvedPinned`; M3-2 never manufactures an empty candidate just to honor a pin.

Sparse and unknown-future Worlds remain supported.

## 7. Current gate — M3-3 next, not started

M3 is **ACTIVE**. M3-1 and M3-2 are **CLOSED / VALIDATED**.

M3-3 must materialize the manual Customize experience over the already-validated M3-1 command language:

```text
explicit Customize entry
draft state
pin / unpin
hide / show
reorder
promote / restore
Apply / Cancel
revision-conflict UX
keyboard + touch accessibility
responsive behavior
```

Drag/drop may exist but cannot be the only accessible reorder mechanism.

M3-3 does **not** integrate resolved candidates into the live World; M3-4 owns that.

## 8. Stop lines

```text
NO M3-4 live integration yet
NO localStorage fake persistence
NO server persistence/cross-device sync
NO DANTE D2–D6
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
```

Backend remains after M7 only.

## 9. Operational rules

- stay on `feature/home-react` unless explicitly authorized otherwise;
- fresh live HEAD before each new write scope;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- generated route tree is never manually edited;
- fix CI root causes rather than weaken tests;
- human visual review is recorded only when actually performed.
