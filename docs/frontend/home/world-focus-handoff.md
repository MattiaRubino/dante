# DANTE — World Focus Handoff

**Status:** CURRENT HANDOFF — PRE-BACKEND / DANTE PRESENCE GATE NEXT  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This file is the durable handoff for continuing World Focus in a new chat. For exact live state, read `world-focus-current-checkpoint.md` first.

## 1. Product purpose

World Focus is the focused application surface for one meaningful continuity context.

Compass:

> **Understand this part of my life and continue from here.**

It is distinct from:

```text
HOME
cross-life compression/orientation/operation

MONDI OVERVIEW
broad view/management of Worlds as a system

WORLD FOCUS
scoped expansion/understanding/continuation of one World

EXPLORE / DETAIL
deeper evidence/history/specialist depth
```

World Focus is route-backed at `/worlds/:worldId`; it is not a Home overlay.

## 2. What a World is

A World is a **user-recognizable continuity context for a significant part of reality**.

Core thesis:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

Permanent rejects:

```text
World != Domain owner
World != universal Entity/Thing
World != folder/life-area taxonomy
World != Goal/Project/Person/Asset automatically
World != database partition
World != ACL/security boundary
World != AI memory bucket
World != mandatory dashboard/time-range/KPI surface
```

The same canonical reality may be projected into several Worlds without duplication of canonical identity.

## 3. Authority hierarchy

For current World Focus work, use this order:

```text
1. current Domain / Logical / Physical / Database / Intelligence authorities
2. world-focus-product-contract.md
3. world-focus-platform-contract.md
4. world-focus-structural-contract.md
5. world-focus-geometry-contract.md
6. world-focus-current-checkpoint.md for implementation status / next gate
7. delivery methodology
8. review/stress documents as evidence
```

Frontend documents never override canonical semantic authorities.

## 4. Current implementation state

```text
WF0 route/shell structure         FROZEN
WF-G3 workspace/frame geometry    FROZEN
WF-V4 VFX                         candidate, not visually frozen
B0 foundation                     CLOSED
WR0 product reverse engineering   CLOSED
WR1 DANTE/user stress             complete; 7 material gaps found
WR2 gap closure                   CLOSED; 7/7 gaps closed
B1 Orientation                    CLOSED FOR SEQUENCING
B2 Continuity / Resume            IMPLEMENTED / AUTOMATED PASS
integrated B2 visual acceptance   DEFERRED
next implementation gate          NOT CODE — DANTE presence/spatial reverse engineering first
```

## 5. Structural baseline

Frozen ownership:

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         └ shell controls

future transient overlay layer
```

Permanent structural rules:

- AppShell/Topbar remains outside World Focus ownership;
- the workspace is rectangular;
- visual ellipses are reference/VFX geometry, never content-layout authority;
- World-specific content/skin may not resize the shell/workspace;
- transient overlays do not become a second persistent layout system;
- geometry changes require explicit user approval + contract/version/test update.

## 6. B0 foundation already available

B0 established production infrastructure that later verticals should consume rather than recreate:

- `model -> application -> ui -> route` dependency direction;
- strict typed platform vocabularies;
- runtime-validation seam for untrusted boundaries;
- `WorldFocusLatestReadCoordinator` / latest-only stale-commit protection;
- upstream AbortSignal support;
- distinction between obsolete frontend reads and durable future DANTE runs;
- safe HTTPS external-link parser;
- route error surface + local render boundary;
- persistent workspace owner + container-query foundation;
- User Timing seam;
- capability-driven VFX degradation when WebGL/software rendering would harm responsiveness;
- WCAG 2.2 AA target and current keyboard/focus/reduced-motion foundations;
- no speculative state/query/plugin/DI libraries.

No real API/DB/provider/LLM behavior was faked.

## 7. Product model closed by WR0-WR2

World Focus is question-driven, not widget-driven.

Output families:

```text
Orientation
Situation
Continuity / Resume
Attention / Resolution
Next
Change
Trajectory / Comparison [optional]
Evidence / History
Explore
Act / Decide
Intelligence
```

A World shows only useful answers supported by available authorized reality.

Sparse, dormant and completed Worlds remain truthful rather than manufacturing urgency/content.

### Four-layer World context model

Never collapse:

```text
1. World identity / purpose
2. Stable World relevance definition
3. Current World interaction cursor/session when actually needed
4. Authorized purpose-scoped DANTE context
```

World relevance is presentation/application context, not ownership or authorization.

The Context Builder remains purpose/recipient/sensitivity/freshness aware.

### DANTE cross-World rule

Current World supplies the default relevance bias, not a reasoning prison.

Broader context is used only when the actual user purpose materially requires it and it is authorized.

### Coherent basis

Visible projections and DANTE answers must preserve compatible basis/freshness semantics. A provider refresh that changes the relevant fact cannot be hidden behind an answer pretending the old screen is still current.

## 8. B1 final disposition

The original visible global temporal Lens failed product review and was removed completely rather than hidden as dead foundation.

Final B1:

```text
World Orientation                KEEP
route-owned active World         KEEP
entry/exit lifecycle             KEEP
loading/error/unavailable        KEEP
responsive/a11y foundation       KEEP
visible time Lens                REMOVED
Lens fixture capability          REMOVED
URL `time` contract              REMOVED
Lens model/tests                 REMOVED
Lens-only Session snapshot       REMOVED
micro visual polish              deferred to integrated composition review
```

A future Lens/session is reintroduced only when a real vertical proves the need.

## 9. B2 Continuity / Resume status

B2 is the first real question-driven content capability.

It deliberately means:

> **What is actually in motion and where can I continue?**

It is not a Recents list and does not infer `recent = resumable`.

Implemented pre-backend properties include:

- intent-specific continuity read boundary;
- runtime validation;
- deterministic scenario adapter;
- bounded first-open result set;
- ready/empty/partial/stale/error/unavailable states;
- latest-only/race protection;
- local read/render failure isolation;
- responsive/container behavior;
- accessible semantics;
- no fake Resume CTA without a real route/capability.

Automated gates passed. Integrated user acceptance is intentionally deferred until the DANTE spatial/presence contract is resolved; B2 remains available evidence/capability and is not discarded.

## 10. Immediate next gate — contextual DANTE presence / spatial UX

DANTE is foundational to World Focus, but **Home AI is not the World AI surface**.

WR2 already closed the semantic presentation depths:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

What remains open — and must be solved before more World content is composed — is the spatial/interaction contract.

Required reverse engineering and stress test:

```text
always visible vs on demand
quiet footprint
composer placement
long-conversation expansion
sidecar / dock / overlay / full-surface alternatives
when DANTE consumes layout space vs overlays
minimum content area left to dynamic composition
content reflow during expansion
selected-module/source contextual interaction
deictic follow-up (“questa”, “perché?”, “continua”)
conversation vs Insight relationship
conversation vs Explore relationship
Proposal / confirmation / receipt placement
World switch and conversation binding
large desktop / laptop / tablet / mobile
focus / keyboard / SR / touch / reduced motion
AI unavailable/degraded state
pre-backend shell now vs real streaming/runtime later
```

Stress at least:

```text
Music
Body
Travel
Finance
Study
Relationships
sparse World
dense World
AI quiet
long conversation
Insight
Proposal/action state
```

External products may be studied for interaction patterns, but no product — including Home — is copied as the semantic/layout answer.

Do not write production World DANTE UI until this gate has been reviewed with the user.

## 11. Dynamic composition after the DANTE gate

Persistent World content remains dynamic/question-driven:

```text
available authorized reality
-> useful output questions now
-> ranking/composition
-> stable/adaptive/ephemeral presentation
```

Continuity, Next, Attention, Change, trend, metrics, timeline, people, artifacts etc. are potential answers/renderers, not guaranteed page sections.

Once DANTE's real footprint is frozen, re-run B2 integrated visual review inside the real remaining workspace, then continue one complete mini-vertical at a time.

## 12. Delivery method

Every World Focus vertical follows `world-focus-delivery-methodology.md`.

Required simplified sequence:

```text
authority re-read
-> scenario/failure/future pressure
-> current product/tech research
-> architecture alternatives
-> explicit decision/rejections
-> UX/responsive/a11y/security/performance/state/test design
-> smallest complete production implementation
-> automated gates
-> real-browser review
-> user functional + visual validation
-> fixes
-> explicit user OK
-> freeze
-> next vertical
```

No hidden infrastructure-only phase replaces visible product progress after B0, unless a demonstrated dependency must be resolved first — as with the current DANTE spatial gate.

## 13. Backend stop line

Before the final authorized backend vertical, do not add:

- real World business API;
- database/Alembic World persistence;
- provider SDK/runtime;
- real LLM streaming/model routing;
- durable Run/Task backend;
- tool/effect execution;
- fake backend success.

Frontend may establish narrow ports/contracts and deterministic local behavior only when needed to prove the real product interaction.

## 14. Required read order for a new World Focus chat

1. `world-focus-current-checkpoint.md`
2. `world-focus-handoff.md`
3. `world-focus-product-contract.md`
4. `world-focus-platform-contract.md`
5. `world-focus-structural-contract.md`
6. `world-focus-geometry-contract.md`
7. `world-focus-delivery-methodology.md`
8. `world-focus-frontend-roadmap.md`
9. evidence documents only as required by the scope.

Deep evidence set:

- `world-focus-wf0-scenario-oracle.md`
- `world-focus-product-reverse-engineering-stress-test.md`
- `world-focus-product-reverse-engineering-stress-matrix.md`
- `world-focus-dante-user-reverse-engineering-stress-test.md`
- `world-focus-dante-user-gap-closure-stress-test.md`
- `world-focus-b0-foundation-review.md`
- `world-focus-b1-product-disposition.md`
- `world-focus-b2-continuity-resume-review.md`
- `world-focus-b2-continuity-resume-disposition.md`
- `world-focus-vfx-research.md`

## 15. Operational safety

- stay on `feature/home-react` until explicitly authorized otherwise;
- fresh HEAD before production writes;
- do not modify frozen Timeline behavior as collateral damage;
- do not touch Access/Auth casually;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- never manually edit generated route output;
- update `world-focus-current-checkpoint.md` and this handoff whenever current gate/accepted disposition materially changes.
