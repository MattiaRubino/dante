# DANTE — Frontend Production-Depth Handoff

**Status:** CURRENT HANDOFF — MULTI-WORKSTREAM FRONTEND BRANCH / WORLD FOCUS WS0–WS8 CLOSED / POST-CLOSURE HYGIENE APPLIED / M0 NEXT  
**Date:** 2026-09-02  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

Read `docs/frontend/home/current-checkpoint.md` first. For World Focus, continue with `world-focus-current-checkpoint.md` and `world-focus-post-ws8-hygiene-audit.md` before older evidence.

---

## 1. Branch topology

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

The workstreams share product/domain foundations but do not own one another's UI state or geometry.

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

## 3. Backend stop line

```text
frontend view model != backend DTO != Domain model != persistence row
```

Do not invent endpoint shapes, ORM rows, SQL contracts, provider truth, durable Runs or real effects to make frontend surfaces look complete.

---

## 4. AppShell / Home

Shared AppShell/Global Topbar is application infrastructure outside World Focus ownership.

Authorities:

```text
docs/frontend/home/contract.md
docs/frontend/home/home-structural-contract.md
docs/frontend/app-shell/p1-global-app-shell.md
docs/frontend/ui-registry.md
```

The legacy Global Topbar Review debt is closed. The disabled button, hard-coded fake badge, dedicated icon/CSS and shell copy were removed in a bounded AppShell/Home hygiene scope. `shell.review.legacy` is no longer an open decision.

No replacement global Review workflow was invented, and Home Context Rail Resolution was not promoted into the Topbar. Reintroducing a global unresolved-matter entry requires a new explicit product contract rather than resurrecting the deprecated placeholder.

---

## 5. Timeline

Timeline T1 remains frozen/user accepted for observable interaction and geometry behavior.

When explicitly resumed:

```text
1. timeline-current-checkpoint.md
2. timeline-handoff.md
3. timeline-t1-frozen-contract.md
4. temporal-experience-architecture.md
5. temporal-frontend-roadmap.md
```

World Focus work must not weaken Timeline regression guards.

---

## 6. World Focus current state

Read:

```text
1. world-focus-current-checkpoint.md
2. world-focus-post-ws8-hygiene-audit.md
3. world-focus-substrate-closure-plan.md
4. world-focus-ws8-final-falsification-review.md
5. world-focus-ws7-executable-harness-review.md
6. world-focus-ws6-universal-work-primitives.md
7. world-focus-ws6-primitive-pressure-matrix.md
8. world-focus-substrate-final-convergence-proof.md
9. world-focus-substrate-combinatorial-evidence.md
10. world-focus-handoff.md
11. world-focus-frontend-roadmap.md
12. product/platform/structural/geometry contracts
13. world-focus-evidence-index.md
```

Live state:

```text
WF0 structure/route                   FROZEN / USER AUTHORIZED
WF-G3 geometry                        LOCKED / USER AUTHORIZED
WF-V4 VFX                             CANDIDATE
B0 foundation                         ENGINEERING CLOSED
WR0–WR2                               CLOSED
B1 Orientation                        CLOSED FOR SEQUENCING
B2 Continuity                         IMPLEMENTED / AUTOMATED PASS
Workspace Platform                    ENGINEERING CLOSED
D0 contextual DANTE spatial contract  ACCEPTED
D1 quiet invoke + composer             CLOSED FOR SEQUENCING
WS0                                   CLOSED
WS1–WS5                               CLOSED
WS6                                   CLOSED
WS7                                   CLOSED
WS8                                   CLOSED
POST-WS8 WORLD FOCUS HYGIENE           APPLIED
APPSHELL LEGACY REVIEW CLEANUP         APPLIED
NEXT                                  M0 MATERIALIZATION MAPPING
```

D2–D6 are preserved under later M4 materialization. Old `D2 NEXT` handoff text is obsolete.

---

## 7. WS8 closure evidence retained

Validated proof/runtime HEAD:

```text
88db899391a3a41e23e76177d4896a657232b5eb
```

Frontend CI:

```text
33639741630 — PASS — attempt 1
```

WS8 closed the pre-materialization substrate program through hostile stateful pressure, mutation-kill and an independent confirmation pass. It did not claim real backend/AuthZ/provider/effect correctness or human visual approval.

---

## 8. Post-WS8 hygiene

The later coherence audit found no reason to reopen WS0–WS8.

It did find and repair local debt:

```text
unknown unregistered popover could physically block the World
unused localStorage motion-preference API/test was exported but not consumed
V2/V3 visual-frame CSS generations remained in the tree after V4 became the active candidate
base visual CSS retained dead SVG-renderer styling
branch-level live checkpoint/handoff still routed a new chat to D2
World switch could retain stale route-entry provenance / close policy
```

A separate AppShell/Home cleanup then removed the already-deprecated Global Topbar Review placeholder and synchronized its contracts. Neither cleanup starts M0.

---

## 9. Durable World Workspace/DANTE boundaries

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

No generic Entity/Thing/Fact/property-bag escape hatch.

---

## 10. Immediate next gate

> **M0 — Materialization Mapping / Scope Freeze**

M0 must map each closed invariant/primitive to exactly one production disposition before M1 starts.

Do not pull forward:

```text
M1–M7 implementation
D2–D6 conversation materialization
backend/API/DB/Alembic/AuthZ/LLM/provider/effect work
```

---

## 11. Operational safety

- fresh HEAD check before every write scope;
- stay on `feature/home-react` unless explicitly authorized otherwise;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not casually modify Access/Auth, frozen Timeline behavior or shared AppShell;
- generated route tree is never manually edited;
- fix root causes rather than weakening tests;
- record manual visual review only when it actually occurred.
