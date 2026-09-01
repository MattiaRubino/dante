# DANTE — World Focus Handoff

**Status:** CURRENT HANDOFF — PRE-BACKEND / WORLD WORKSPACE PLATFORM NEXT  
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
7. world-focus-workspace-scenario-oracle-evidence.md for already-completed workspace/module stress conclusions
8. delivery methodology
9. other research/review documents only as evidence
```

Frontend documents never override canonical semantic authorities.

## 4. Current implementation state

```text
WF0 route/shell structure            FROZEN
WF-G3 workspace/frame geometry       FROZEN
WF-V4 VFX                            candidate, not visually frozen
B0 foundation                        CLOSED
WR0 product reverse engineering      CLOSED
WR1 DANTE/user stress                complete; 7 material gaps found
WR2 gap closure                      CLOSED; 7/7 gaps closed
B1 Orientation                       CLOSED FOR SEQUENCING
B2 Continuity / Resume               IMPLEMENTED / AUTOMATED PASS
integrated B2 visual acceptance      DEFERRED
workspace/module uncertainty study   DONE / retained as evidence
next implementation gate             WORLD WORKSPACE PLATFORM MATERIALIZATION
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

## 8. Workspace/module scenario research already completed

Do **not** restart the broad architecture question of unknown future modules/surfaces.

The recovered evidence file `world-focus-workspace-scenario-oracle-evidence.md` preserves the durable result of the earlier scenario study.

Already pressure-tested:

```text
unknown future World
unknown future specialist module
sparse / dense / very large World
long/high-frequency history
multiple/stale/offline providers
AI unavailable
partial data
late async after World switch
same canonical reality in multiple Worlds
sensitive/multi-actor context
customization while adaptive content changes
narrow/reduced-motion/keyboard cases
layout/schema evolution
```

Already accepted direction:

```text
one workspace platform, not page-per-World
finite approved renderer/surface registry
unknown specialist surfaces through controlled extension
no arbitrary AI-generated executable UI
specialist renderer only when generic primitives materially lose meaning
stable / adaptive / ephemeral remain distinct
AI cannot silently mutate stable composition
DANTE can drive contextual Insight / Explore / deeper-surface intents
typed source drill-down on demand
bounded/aggregated large-data projections
same canonical reality reused across Worlds without duplication
future stable config needs version/evolution semantics
```

This is implementation input, not an open research gate.

## 9. B1 final disposition

The original visible global temporal Lens failed product review and was removed completely rather than hidden as future infrastructure.

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

## 10. B2 Continuity / Resume status

B2 is the first real question-driven content capability.

It means:

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

Automated gates passed. Integrated user acceptance is deferred until the real workspace orchestration/surface footprint exists; B2 remains valid and is not discarded.

## 11. Immediate next gate — World Workspace Platform materialization

The next scope is **inside the frozen rectangular workspace**. Do not spend time redesigning route/opening/sphere/VFX now.

Consume the already-completed scenario research and current Product/Platform contracts to materialize the smallest production-grade orchestration layer required by the accepted behavior.

It must cover, only as proven necessary:

```text
dynamic composition host
finite surface/renderer registry
interaction cursor ownership
selected projection/source context
open / close / replace / promote surface semantics
Insight / Explore / deeper contextual surfaces
World contextual DANTE presence/conversation footprint
stable / adaptive / ephemeral coexistence
focus / back / Escape ownership
responsive/mobile surface mapping
surface-local error/degraded behavior
race/generation safety
performance/resource behavior
```

### DANTE semantics already closed

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

Home AI is not the World DANTE surface.

### Concrete presentation still open

These were never frozen and may require focused product/interaction comparison before the relevant production write:

```text
exact quiet footprint
composer placement
conversation expansion geometry
inline vs sidecar vs overlay/full-workspace mapping
surface coexistence/exclusivity
focus/back/Escape precedence
responsive/mobile mapping
exact local state model required by those interactions
```

Do not turn these remaining choices into a repeat of the full unknown-module/World reverse engineering.

## 12. Dynamic composition

Persistent World content remains:

```text
available authorized reality
-> useful output questions now
-> ranking/composition
-> stable/adaptive/ephemeral presentation
```

Continuity, Next, Attention, Change, trend, metrics, timeline, people, artifacts and specialist surfaces are potential answers/renderers, not guaranteed page sections.

B2 will be re-reviewed inside the real workspace once this platform layer is usable.

## 13. Delivery method

Every implementation slice follows `world-focus-delivery-methodology.md`.

```text
authority/evidence re-read
-> focused failure/future pressure only where not already closed
-> product/tech research only for genuinely open decisions
-> architecture decision
-> production implementation
-> responsive/a11y/security/performance/state/tests
-> automated gates
-> real-browser review
-> user functional + visual validation
-> fixes
-> explicit user OK
-> freeze
```

Do not redo closed research merely because a new chat starts.

## 14. Backend stop line

Before the final authorized backend vertical, do not add:

- real World business API;
- database/Alembic World persistence;
- provider SDK/runtime;
- real LLM streaming/model routing;
- durable Run/Task backend;
- tool/effect execution;
- fake backend success.

Frontend may establish narrow ports/contracts and deterministic local behavior only when needed to prove the real product interaction.

## 15. Required read order for a new World Focus chat

1. `world-focus-current-checkpoint.md`
2. `world-focus-handoff.md`
3. `world-focus-product-contract.md`
4. `world-focus-platform-contract.md`
5. `world-focus-structural-contract.md`
6. `world-focus-geometry-contract.md`
7. `world-focus-workspace-scenario-oracle-evidence.md`
8. `world-focus-delivery-methodology.md`
9. `world-focus-frontend-roadmap.md`
10. `world-focus-evidence-index.md` for deeper research/review archaeology.

## 16. Operational safety

- stay on `feature/home-react` until explicitly authorized otherwise;
- fresh HEAD before production writes;
- do not modify frozen Timeline behavior as collateral damage;
- do not touch Access/Auth casually;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- never manually edit generated route output;
- update `world-focus-current-checkpoint.md` and this handoff whenever current gate/accepted disposition materially changes.
