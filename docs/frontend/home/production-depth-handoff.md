# DANTE — Frontend Production-Depth Handoff

**Status:** CURRENT HANDOFF — WORLD FOCUS WS0–WS8 CLOSED / POST-CLOSURE HYGIENE + PRE-M0 FALSIFICATION CLOSED / M0 CLOSED / M1 ACTIVE / M1-1 CLOSED + VALIDATED / M1-2 NEXT  
**Date:** 2026-09-02  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

Read `docs/frontend/home/current-checkpoint.md` first. For World Focus, continue with `world-focus-current-checkpoint.md`, `world-focus-m1-core-nonvisual-materialization-review.md` and `world-focus-m1-next-subblock.md` before older evidence.

---

## 1. Branch topology

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

Shared foundations do not imply shared UI ownership.

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

---

## 2. Production-depth standard

Every bounded capability must address the applicable layers before closure:

```text
product semantics / scenarios
React + TypeScript ownership
state / async / race behavior
loading / empty / partial / stale / error / unavailable
responsive / container behavior
keyboard / focus / accessibility / reduced motion
security / privacy / disclosure boundaries
performance / resource cleanup
deterministic pre-backend seams only where earned
unit / integration / E2E / real-browser evidence
human visual review only when actually performed
truthful final disposition
```

Green CI never means human visual acceptance happened.

---

## 3. World Focus current state

```text
WF0 structure/route                    FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 VFX                              CANDIDATE
B0 foundation                          ENGINEERING CLOSED
WR0–WR2                                CLOSED
B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity                          IMPLEMENTED / AUTOMATED PASS
Workspace Platform                     ENGINEERING CLOSED
D0 contextual DANTE spatial contract   ACCEPTED
D1 quiet invoke + composer              CLOSED FOR SEQUENCING
WS0                                    CLOSED
WS1–WS5                                CLOSED
WS6                                    CLOSED
WS7                                    CLOSED
WS8                                    CLOSED
POST-WS8 HYGIENE                       APPLIED
PRE-M0 FALSIFICATION                   CLOSED / PASS
M0 Materialization Mapping             CLOSED
M1 Core Non-Visual Materialization     ACTIVE
M1-1 identity/reference ownership      CLOSED / VALIDATED
M1-2 non-visual facets + seams         NEXT
M2–M7                                  BLOCKED
BACKEND                                BLOCKED UNTIL M7
D2–D6                                  DEFERRED TO M4
```

Final pre-M0 gate evidence:

```text
discovery commit  798170e0c1ad12e0263364ab5c542a6ffe3d5e06
fix HEAD          7c9feab50c6e2a04a9a3b1e36c92958362dba704
Frontend CI       33664655614 PASS
```

The gate discovered stale transient route-handoff resurrection on World/source mismatch and fixed it in the existing transition owner without reopening WS0–WS8.

M0 closure evidence:

```text
HEAD        6ea74f630cb35af65d58e7ae873882d6d975411e
Frontend CI 33668744509 PASS
```

Validated M1-1 production-code evidence:

```text
CODE HEAD   e0f4003496bfbf828ed9ab7718af8e7e30342ad3
Frontend CI 33679425668 PASS
```

Later documentation-only commits do not replace the M1-1 CODE HEAD evidence point.

---

## 4. Durable World Workspace / DANTE boundaries

Preserve:

```text
finite module/surface registries
stable/adaptive/ephemeral composition
bounded workspace cursor
worldId + generation stale guard
blocking-tail interaction ownership
actual workspace allocation / responsive fallback
local renderer failure isolation
D1 global invoke contextReference:null
AI output != canonical truth
Proposal != Decision != effect
World relevance != authorization
```

M1-1 production materialization now also preserves:

```text
open-ended production World identity != open-ended routability
fixture World IDs != permanent production taxonomy
context reference != canonical payload
context reference != disclosure authorization
workspace contextReferences owns primary + ordered bounded supporting refs
surface fallback inherits primary only
semantic same-set context update is an exact no-op
clear-context removes primary + supporting atomically
```

The current non-enumerable `contextReferences` interaction-cursor compatibility property is transitional and must be reviewed/removed before M1 closure.

No generic Entity/Thing/Fact/property-bag escape hatch.

---

## 5. AppShell / Home and Timeline

The deprecated Global Topbar Review placeholder is removed; no global replacement workflow was invented.

Timeline T1 observable interaction/geometry remains frozen/user accepted. M1 materialization must not alter Timeline behavior as collateral work.

---

## 6. Backend stop line

```text
frontend view model != backend DTO != Domain model != persistence row
```

Do not invent endpoint shapes, ORM rows, SQL contracts, provider truth, durable Runs or real effects to make frontend surfaces look complete.

Before the explicit later backend vertical:

```text
NO World DB/Alembic
NO real World API merely for demos
NO real AuthZ/provider runtime
NO model routing/streaming
NO canonical chat persistence
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

---

## 7. Current materialization contract

M0 is CLOSED. Its complete production-disposition map remains authoritative in `world-focus-m0-materialization-mapping.md`.

M1 is ACTIVE. M1-1 is CLOSED / VALIDATED and M1-2 is the next bounded engineering subblock.

M1-2 must materialize only the remaining frozen non-visual deltas: safe reference-resolution presentation semantics, stronger WP-01 production alignment, WP-02/03/04 application/model seams, narrow basis/freshness/validity/disclosure/effect/sync facets, and direct typed O2 Situation / O5 Next / O8 Evidence application seams.

Do not pull forward M2 shared visuals, M3 adaptive composition, D2–D6/M4, M5 complete Worlds, M6 integrated visual/a11y/performance acceptance or backend/API/DB/Alembic/AuthZ/LLM/provider/effect work.

Proof/oracle code remains proof/audit; it does not become production runtime authority automatically.

---

## 8. Read order

```text
1. current-checkpoint.md
2. world-focus-current-checkpoint.md
3. world-focus-m1-core-nonvisual-materialization-review.md
4. world-focus-m1-next-subblock.md
5. world-focus-m0-materialization-mapping.md
6. world-focus-contract-sequencing-supersession.md
7. world-focus-pre-m0-falsification-review.md
8. world-focus-post-ws8-hygiene-audit.md
9. world-focus-substrate-closure-plan.md
10. world-focus-ws8-final-falsification-review.md
11. world-focus-ws7-executable-harness-review.md
12. world-focus-ws6-universal-work-primitives.md
13. world-focus-substrate-final-convergence-proof.md
14. world-focus-substrate-combinatorial-evidence.md
15. world-focus-frontend-roadmap.md
16. world-focus-handoff.md
17. world-focus-evidence-index.md
```

Older `D2 NEXT`, `M0 NEXT/ACTIVE` or `M1 NEXT/BLOCKED` wording is phase-time history only unless a newer live authority explicitly adopts it.

---

## 9. Operational safety

- fresh HEAD check before every write scope;
- stay on `feature/home-react` unless explicitly authorized otherwise;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not casually modify Access/Auth, frozen Timeline behavior or shared AppShell;
- generated route tree is never manually edited;
- fix root causes rather than weakening tests;
- record manual visual review only when it actually occurred.
