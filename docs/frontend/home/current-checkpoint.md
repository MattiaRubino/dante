# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS D2 NEXT  
**Date:** 2026-09-01  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This file is the **branch-level live entry point** for a new chat/agent. Do not reconstruct current state from older phase labels, historical roadmaps or old conversational summaries.

For the currently active World Focus workstream, `world-focus-current-checkpoint.md` is the detailed live authority immediately after this file.

---

## 1. Workstreams currently present on this branch

Three distinct frontend concerns coexist:

```text
APP SHELL / HOME
shared application shell and Home composition

TEMPORAL / TIMELINE
Home Timeline + shared temporal capability

WORLD FOCUS
one focused World as its own route/application surface
```

They share product/domain authorities but do not own one another's layout or interaction semantics.

Permanent distinctions:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

Do not transfer component geometry/state semantics from one surface to another merely because the underlying capability is related.

---

## 2. Active workstream

**World Focus is the active product workstream.**

Current top-level state:

```text
WF0 structural shell / route            FROZEN / USER AUTHORIZED
WF-G3 geometry                          LOCKED / USER AUTHORIZED
WF-V4 visual treatment                  CANDIDATE
B0 production foundation                ENGINEERING CLOSED
WR0-WR2 World/DANTE product model       CLOSED
B1 Orientation                          CLOSED FOR SEQUENCING
B2 Continuity / Resume                  IMPLEMENTED / AUTOMATED PASS
Workspace Platform                      ENGINEERING CLOSED
D0 contextual DANTE spatial direction   ACCEPTED
D1 quiet invoke + compact composer       CLOSED FOR SEQUENCING
NEXT                                     D2 ADAPTIVE CONVERSATION SURFACE
```

Final reusable Workspace Platform code evidence:

```text
HEAD 6c441335a75bb913af8da1eda569d8094d38a539
CI   33549465793 — PASS
```

Final D1 code evidence:

```text
HEAD f17291de32e6bdced20536807b32928ec1be6aea
CI   33552437179 — PASS
```

D1 closure is based on strict engineering + real Chromium functional/a11y acceptance. Human/manual visual review is **not falsely claimed**; the user delegated sequencing closure and integrated visual polish remains D7 work.

---

## 3. Global AppShell / Home baseline

The shared AppShell/Global Topbar is already productionized and remains outside World Focus ownership.

Durable rules:

- persistent shared AppShell / Global Topbar;
- real application routing;
- Home / Mondi / Oggi navigation;
- inline Topbar Search rather than Home-owned modal behavior;
- centralized design-token/theme ownership;
- no fake backend writes;
- Access/Auth remains a separate workstream and must not be casually modified here.

Durable Home authorities:

```text
docs/frontend/home/contract.md
docs/frontend/home/home-structural-contract.md
docs/frontend/app-shell/p1-global-app-shell.md
```

---

## 4. Timeline current state

Timeline Phase T1 is **user-accepted and frozen** for observable interaction/geometry behavior.

No Timeline work is authorized merely because later temporal roadmap phases exist.

When Timeline is explicitly resumed, read:

```text
1. docs/frontend/home/timeline-current-checkpoint.md
2. docs/frontend/home/timeline-handoff.md
3. docs/frontend/home/timeline-t1-frozen-contract.md
4. docs/frontend/home/temporal-experience-architecture.md
5. docs/frontend/home/temporal-frontend-roadmap.md
```

Never weaken Timeline regression tests to accommodate unrelated World Focus work. Current World Focus CI intentionally continues to run the frozen Firefox Timeline interaction contract.

---

## 5. World Focus current state and read order

World Focus detailed live state is in:

```text
1. docs/frontend/home/world-focus-current-checkpoint.md
2. docs/frontend/home/world-focus-handoff.md
3. docs/frontend/home/world-focus-frontend-roadmap.md
```

Then read current product/architecture contracts and active evidence:

```text
4. world-focus-product-contract.md
5. world-focus-platform-contract.md
6. world-focus-structural-contract.md
7. world-focus-geometry-contract.md
8. world-focus-workspace-platform-checkpoint.md
9. world-focus-dynamic-composition-allocation-review.md
10. world-focus-dante-spatial-presence-review.md
11. world-focus-d1-dante-entry-review.md
12. world-focus-workspace-scenario-oracle-evidence.md
13. world-focus-delivery-methodology.md
14. world-focus-evidence-index.md
```

Do not restart WR0/WR1/WR2, broad unknown-module research or broad DANTE spatial research from zero.

---

## 6. D0/D1 state in one paragraph

D0 reverse engineering compared current mature AI workspace patterns and accepted an adaptive hybrid:

```text
quiet invoke
-> compact non-modal composer
-> wide ongoing conversation sidecar
-> constrained/mobile route-owned focus overlay
-> explicit maximize/restore
-> explicit bounded contextual invocation
```

D1 implemented only the first two steps truthfully:

```text
quiet invoke
compact composer
no automatic chat
no fake prompt suggestions
no fake assistant response
no real backend/model/Run/tool/effect
```

The global invoke deliberately uses `contextReference:null`; explicit deictic context is D4.

---

## 7. Immediate next gate — D2 Adaptive Conversation Surface

Do **not** start D3 message/model semantics yet.

D2 must prove the spatial/presentation behavior of one ongoing DANTE conversation:

```text
wide allocated workspace
-> internal split sidecar

constrained/mobile
-> route-owned focus overlay below Global Topbar

explicit deep work
-> maximize sidecar -> focus overlay

restore
-> same logical conversation / appropriate presentation
```

Critical warning:

The current Workspace Platform's `full-screen` slot is workspace-local. At 390px viewport the frozen World workspace can be roughly ~238px wide, so that slot alone is **not** the mobile ongoing-conversation solution.

D2 must define a route-owned World focus-overlay seam that can cover the World while using route width below Global Topbar, without resizing/re-owning the Topbar or changing WF-G3 workspace geometry.

Presentation geometry must not become conversation identity.

D2 must not fabricate assistant transcript, streaming, provider/model calls or backend persistence.

---

## 8. Production-depth delivery method

Every bounded frontend capability follows:

```text
authority/current evidence
-> requirements
-> targeted simulations/adversarial pressure
-> focused product/technology comparison where genuinely open
-> architecture alternatives
-> explicit decision / rejected paths
-> complete frontend implementation
-> responsive / a11y / security / performance / async / errors
-> automated gates
-> real-browser automated acceptance
-> human/user functional + visual review when available
-> truthful disposition
-> next vertical
```

A green CI run is necessary but does not itself prove human visual acceptance.

If the user explicitly delegates closure authority, sequencing may proceed on sufficient evidence, but no manual review may be claimed unless it actually occurred.

---

## 9. Backend stop line

Current frontend phase remains pre-backend.

Do not invent:

- real business APIs;
- DB/Alembic changes;
- persistence rows as frontend contracts;
- provider integrations;
- real LLM/model routing/streaming;
- durable Run/Task backend;
- real tool/effect execution;
- fake durable success.

Use narrow typed frontend/application seams and deterministic local adapters only when a real product vertical proves need.

Permanent rule:

```text
frontend view model != backend DTO != Domain model != persistence row
```

---

## 10. Global semantic alignment

Frontend consumes rather than redefines:

- Product Identity / North Star;
- product simulations;
- Domain Atlas / Language Map;
- Logical Model;
- Physical Model;
- current DB/Alembic source of record;
- Intelligence Context/Runtime boundaries;
- Governed Operation/Effect contracts;
- frontend production-readiness contracts.

Permanent examples:

```text
AI output != canonical fact
AI proposal != Decision
Decision != effect
World != canonical Domain owner
World relevance != authorization
selected context != authorization
planned != actual
absence != false
UI hiding != authorization
```

A frontend label/layout convenience never creates a new Domain concept.

---

## 11. Operational rules

- continue on `feature/home-react` until explicitly authorized otherwise;
- inspect fresh branch HEAD before production writes;
- do not casually touch parallel Access/Auth work;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- never manually edit generated route-tree output;
- preserve frozen Timeline and World geometry contracts unless explicitly reopened;
- fix CI/test root causes rather than weaken gates;
- do not carry failure ZIPs/artifacts as project state;
- update this file + relevant workstream checkpoint/handoff whenever the active gate materially changes.
