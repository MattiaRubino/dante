# DANTE — World Focus Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — PRE-BACKEND — D2 NEXT  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope stop:** complete production-grade frontend/product behavior before real backend/API/database/provider/LLM integration.

This roadmap supersedes the old `WF0 -> WF8` sequencing and the later temporary `Workspace Platform next` phase. The reusable Workspace Platform is now engineering-closed; D0 spatial direction is accepted; D1 is closed for sequencing. The next bounded slice is D2.

## 1. Delivery rule

World Focus is built one complete product/platform slice at a time:

```text
authority + already-closed evidence
-> pressure only genuinely open decisions
-> external product/technology research when it can improve the decision
-> architecture/state contract
-> complete frontend implementation
-> responsive/a11y/security/performance/errors/races
-> automated gates
-> real-browser automated acceptance
-> human functional/visual review when available/required
-> fixes
-> explicit/delegated acceptance disposition
-> freeze or close-for-sequencing
-> next slice
```

Do not build all models/services first and UI later. Do not open several broad feature tracks in parallel. Do not redo closed research merely because a new chat starts.

Visual micro-polish must not block higher-value functional/product verticals when the integrated composition is not yet mature; however this is not permission to lower structural, interaction, accessibility or code quality.

## 2. Authority / historical sequence

The branch reached its current state through these major phases:

```text
Home React foundation
-> World Focus structural route/shell
-> WF-G3 frozen geometry
-> B0 production foundation
-> initial B1 Orientation + universal Lens hypothesis
-> WR0 product reverse engineering falsifies universal Lens
-> WR1 DANTE <-> user reverse engineering finds G1..G7
-> WR2 closes G1..G7
-> revised B1 closes for sequencing with Lens fully removed
-> B2 Continuity / Resume first real question-driven projection
-> workspace/module uncertainty evidence recovered and retained
-> reusable Workspace Platform materialized and hardened
-> D0 contextual DANTE spatial/presence reverse engineering
-> D1 quiet invoke + compact composer
-> D2 NEXT
```

Historical evidence remains in the evidence index; historical status lines do not override this roadmap.

## 3. Frozen / closed foundations

### WF0 structural route/shell — FROZEN / USER AUTHORIZED

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ World Focus shell
         ├ visual frame
         ├ rectangular workspace
         └ shell controls
```

World Focus is route-backed, not a Home overlay. AppShell/Global Topbar remain outside World Focus ownership.

### WF-G3 geometry — LOCKED / USER AUTHORIZED

The workspace is a persistent rectangle. Ellipses/corona are VFX/reference geometry only and may never clip or own content layout.

Macro geometry may not be changed casually by DANTE, modules or a World-specific renderer.

### WF-V4 visual treatment — CANDIDATE

VFX is intentionally not frozen by engineering PASS. Interaction quality wins over ornament; software/unsupported rendering degrades.

### B0 production foundation — ENGINEERING CLOSED

Established:

- `model -> application -> ui -> route` direction;
- strict typed platform vocabulary;
- runtime-validation seam;
- latest-read stale-commit protection;
- AbortSignal/cancellation foundation;
- safe external HTTPS parsing;
- route/local render failure isolation;
- persistent workspace/container-query foundation;
- User Timing seam;
- accessibility/reduced-motion foundations;
- capability-driven VFX degradation;
- no speculative global state/query/plugin/DI library adoption;
- no fake backend/provider/LLM behavior.

### WR0-WR2 product/context reverse engineering — CLOSED

Established:

- World as user-recognizable continuity context;
- World-worthiness criteria;
- Home vs World vs deeper Explore boundaries;
- question-driven Output Grammar;
- four-layer World context model;
- purpose-scoped authorized DANTE context;
- coherent visible/DANTE basis;
- cross-World expansion rules;
- interaction cursor semantics;
- DANTE P0-P5 semantic depths;
- LLM-independent first-open requirement;
- no new Domain/Logical/Physical/DB/Intelligence structural gap.

### B1 Orientation — CLOSED FOR SEQUENCING

Kept:

```text
World identity/orientation
route-owned active World
entry/exit lifecycle
loading/error/unavailable behavior
responsive/a11y shell behavior
```

Removed after product falsification:

```text
universal visible time Lens
Lens fixture capability
?time= route contract
Lens-only model/tests/session snapshot
```

A future Lens/session must be re-earned by a real vertical; no hidden stale Lens scaffolding is retained.

### B2 Continuity / Resume — IMPLEMENTED / AUTOMATED PASS

First real World output family:

> **What is actually in motion and where can I continue?**

Important semantics:

```text
recent != resumable
last viewed != meaningful checkpoint
open != in motion
unfinished != important
AI-guessed relevance != continuity fact
```

B2 remains valid. Integrated visual acceptance is intentionally deferred until more of D0/D1-D7 establishes the real workspace composition footprint.

## 4. Workspace/module uncertainty research — ALREADY DONE

Do not restart the broad question of unknown future Worlds/modules.

Authority/evidence:

`world-focus-workspace-scenario-oracle-evidence.md`

Already pressure-tested:

```text
unknown future World
unknown future specialist surface
sparse and dense Worlds
large/high-frequency history
multiple/stale/offline providers
AI unavailable
partial data
late async results
same canonical reality in multiple Worlds
sensitive/multi-actor context
customization vs adaptive content
narrow/reduced-motion/keyboard cases
schema/layout evolution
```

Already accepted:

```text
one shared workspace platform
not page-per-World
finite approved renderer/surface registries
controlled specialist extension
no arbitrary model-generated executable UI
stable/adaptive/ephemeral remain distinct
AI cannot silently rewrite stable composition
DANTE may request contextual Insight/Explore/deeper surfaces
source drill-down remains typed/bounded
large data aggregated/bounded before React
same canonical reality can project into several Worlds without duplication
```

## 5. Workspace Platform — ENGINEERING CLOSED

Final platform HEAD:

`6c441335a75bb913af8da1eda569d8094d38a539`

CI:

`33549465793` — full PASS.

Implemented/hardened capabilities:

```text
dynamic composition planner
finite module registry
finite surface registry
transient workspace reducer
bounded interaction cursor
interaction generations
selected bounded references
surface open/replace/promote/close
Escape ownership
blocking-stack barrier
main/full-vs-split allocation
none/overlay/focus layer axis
interactive/inert axis
actual workspace ResizeObserver measurement
nested world-focus-main container queries
wide sidecar real-width allocation
narrow sidecar overlay degradation
modal/full-focus background inert
dormant surface filtering
underlying sidecar inert under blocking layer
local renderer/surface failure isolation
```

Stress:

```text
500 deterministic composition scenarios
500 deterministic allocation/surface-stack scenarios
```

The platform is infrastructure, not a speculative plugin framework and not a semantic World ontology.

## 6. D0 adaptive contextual DANTE spatial contract — ACCEPTED

Research/evidence:

`world-focus-dante-spatial-presence-review.md`

External patterns reviewed included current Google Workspace/Gemini, Microsoft 365/Copilot, VS Code/Copilot Chat, Notion Agent and Linear Agent.

Cross-product synthesis:

> **AI availability is persistent; AI footprint is not.**

Accepted DANTE geometry ladder:

```text
P0 quiet World
+ small DANTE invoke

P1 quick invoke
-> compact transient non-modal composer

ongoing conversation + wide allocated workspace
-> CONTENT | DANTE SIDECAR

ongoing conversation + constrained/mobile route
-> route-owned DANTE focus overlay below Global Topbar

wide/deep work when user asks
-> explicit maximize from sidecar to focus overlay
```

Permanent rejects:

```text
always-open chatbot column
Home AI copied into World
fixed-width side panel at every width
238px mobile conversation squeezed inside World workspace
AI prose on first open
random prompt suggestions for visual fullness
LLM-selected executable UI
chat history as canonical World truth
selected DOM serialized as DANTE context
surface visibility as authorization or Run lifetime
```

## 7. D1 quiet invoke + composer — CLOSED FOR SEQUENCING

Final D1 code HEAD:

`f17291de32e6bdced20536807b32928ec1be6aea`

CI:

`33552437179` — full PASS.

D1 implemented:

```text
quiet lower-trailing DANTE invoke
>=44px target
accessible World-specific invoke name
no auto-open
finite registered dante-composer
peek + popover + user origin
non-modal composer
World remains interactive
textarea initial focus
close/Escape focus restoration
truthful unavailable state
truthful submit failure with draft preservation
no fake assistant response
no fake Run/model/tool/effect
IT/EN localization
390px containment
axe wide + compact
presentation-generic popover pointer transparency
```

Critical context decision:

```text
global quiet DANTE invoke
-> contextReference: null
```

The currently selected projection is not silently inherited as DANTE context. D4 owns explicit deictic binding.

Closure basis is documented in `world-focus-d1-dante-entry-review.md`.

Human/manual visual inspection is **not fabricated**. The user explicitly delegated closure judgment in the saturated-chat handoff, so D1 is closed for sequencing on engineering + automated real-browser evidence; integrated visual polish remains D7 work.

## 8. CURRENT NEXT GATE — D2 Adaptive Conversation Surface

D2 is the next and only active product/platform slice after this handoff.

### D2 product question

> How does the same ongoing DANTE conversation occupy the World experience at different available widths/depths without turning geometry into conversation identity or trapping mobile in the narrow World rectangle?

### D2 required behavior

Accepted direction from D0:

```text
wide allocated workspace
-> internal split sidecar

constrained workspace / mobile
-> route-owned focus overlay using route width below Global Topbar

wide deep work
-> explicit maximize to focus overlay

restore
-> same conversation identity returns to appropriate presentation
```

### Critical D2 architecture rule

The current Workspace Platform owns allocation **inside the rectangular World workspace**.

But D0 explicitly established that constrained/mobile ongoing conversation cannot be trapped inside that rectangle: at 390px viewport WF0 leaves roughly 238px of workspace width.

Therefore D2 must carefully introduce/consume a **route-owned World overlay seam** without violating frozen macro ownership:

```text
APP SHELL / GLOBAL TOPBAR      remains outside World ownership
route outlet / World shell     owns focus overlay region below Topbar
rectangular workspace          remains frozen in place underneath
focus overlay                  may cover World workspace; does not resize it
```

Do not solve mobile by simply mapping `full-screen` to `position:absolute; inset:0` inside the narrow workspace if that leaves conversation at ~238px.

### D2 must not pull D3 forward

D2 proves surface geometry/presentation continuity. It must not invent:

```text
real assistant messages
streaming
model calls
conversation backend
canonical chat persistence
tool execution
fake successful reply
```

If a conversation identity seam is needed to prove presentation switching, keep it minimal, typed and presentation-local. D3 owns deterministic pre-backend conversation data semantics.

### D2 pressure cases

At minimum:

```text
>= split threshold desktop
just above/below threshold
ordinary laptop allocation
720-ish constrained World
390 mobile
sidecar open -> resize below threshold
constrained -> resize wide
explicit maximize
restore from maximize
Escape/back precedence
World switch/unmount
blocking modal over sidecar/focus where relevant
reduced motion
keyboard/focus
no horizontal overflow
```

### D2 external/research rule

The broad DANTE spatial research is already done; do not repeat it.

Fresh focused research is allowed only if D2 reaches a concrete unresolved implementation question where current official platform patterns materially improve the decision, e.g. route-level focus layer ownership, responsive presentation continuity or accessibility semantics.

Ask:

```text
How do mature products solve this exact subproblem?
What failure modes do they avoid?
Can DANTE do better while preserving its own product semantics?
```

Do not copy competitors blindly.

## 9. D3 — Deterministic Pre-Backend Conversation Adapter

After D2 passes its gate:

```text
typed user message
assistant/result distinctions
conversation identity
loading/error/unavailable states
cancellation/generation behavior
late result protection
presentation-independent conversation state
no canonical truth implication
```

D3 is deterministic/local. No real LLM/provider/backend.

A conversation message is not automatically an Insight, Proposal, Decision, Observation or canonical fact.

## 10. D4 — Explicit Contextual / Deictic Invocation

D4 introduces intentional bounded context references.

Examples:

```text
select/reference a Continuity item
-> contextual "Ask DANTE"
-> explicit projection/source reference
-> user can ask "why?", "compare with before", "open the source"
```

Rules:

```text
reference != copied source truth
reference != authorization
reference != permission to retrieve everything with matching label
DOM != context payload
World label != retrieval specification
```

Future Context Builder reconstructs authorized purpose-scoped context from reference + user purpose + Principal/Actor/recipient + disclosure/governance + freshness/material basis.

## 11. D5 — Insight Presentation Integration

Prove:

```text
conversation != Insight
Insight != chat message
Explore != conversation
```

A validated/derived Insight may have a standalone registered presentation when evidence/readability benefits.

No AI statement becomes accepted fact merely because it is rendered as Insight.

## 12. D6 — Proposal / Confirmation / Receipt Presentation

Prove presentation grammar up to the frontend governed-operation seam:

```text
assistant suggestion
!= Proposal automatically

Proposal
!= accepted Decision

Decision
!= effect

tool invocation
!= authorization

provider success
!= canonical completion
```

Consequential confirmation uses a controlled blocking surface and existing Escape/blocking-stack semantics. Still no real effect backend in D6.

## 13. D7 — Integrated World + DANTE Review / Pre-Backend Freeze

This is the major integrated human/product review milestone.

Review together:

```text
Orientation
Continuity
quiet DANTE
composer
adaptive conversation
contextual invocation
Insight
Proposal/confirmation/receipt
responsive behavior
VFX/content hierarchy
```

At D7:

- perform desktop/laptop/tablet/mobile visual review;
- revisit B1/B2 deferred micro-polish in real composition context;
- verify DANTE does not visually dominate first-open;
- verify sparse and dense Worlds;
- verify accessibility/focus/reduced-motion;
- run unknown future World/specialist pressure;
- obtain explicit user freeze before backend vertical.

## 14. Content verticals outside D1-D7

World Output Grammar remains:

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

Do not pre-freeze a dashboard/module list. After D0/D1-D7 stabilizes contextual DANTE and workspace behavior, choose additional product verticals by cross-World user value, semantic risk and architecture proof value.

## 15. Personalization milestone

Only after several real output families prove the model:

```text
View
-> Customize Draft
-> Apply / Cancel
```

Removing a module never deletes canonical source reality.

Future persisted stable configuration requires explicit version/concurrency semantics rather than silent last-write-wins.

DANTE may propose configuration changes; it does not silently apply them.

## 16. Contrasting complete Worlds milestone

Before backend freeze validate materially different Worlds using the same platform:

```text
Music
Travel
Finance
Study or Body
Relationships / qualitative pressure
unknown future World
```

Pressure:

```text
empty
1-2 useful answers
4-8
12
20 potential answers
fresh/partial/stale/provider unavailable
AI unavailable
multi-actor/privacy
large history
same canonical reality in several Worlds
unknown specialist surface
```

If success requires a page architecture branch by World identity, the platform has failed.

## 17. Backend stop line

D1-D7 and current frontend product work must not add:

- real World business API merely to satisfy UI;
- database/Alembic World persistence;
- provider SDK/runtime;
- real LLM/model routing/streaming;
- durable Run/Task backend;
- tool/effect execution;
- fake backend success;
- provider response treated as canonical completion.

Frontend may establish narrow typed seams and deterministic local adapters only where required to prove the real interaction.

## 18. Final backend vertical

Only after frontend/product freeze, replace deterministic/local adapters with real application/API/runtime capabilities as justified:

- authoritative projection/read APIs;
- AuthZ/disclosure enforcement;
- persisted configuration sync;
- DANTE Context Builder/runtime;
- streaming and durable Run/Task semantics;
- provider/tool/effect integration;
- governance/confirmation/audit/reconciliation;
- backend contract tests.

The frontend must not need a product/workspace rewrite simply to connect backend authority.

## 19. Permanent semantic barriers

```text
World != canonical Domain owner
WorldProjection != canonical truth
ModuleConfig != canonical source data
layout != Domain semantics
AI output != accepted fact
AI proposal != Decision
Decision != effect
tool call != authorization
provider state != canonical DANTE state
planned != Actual
Observation != causation
absence != false
UI hiding != authorization
```

## 20. Roadmap maintenance rule

Whenever a gate closes or a recovered decision changes sequencing materially, immediately align:

```text
world-focus-current-checkpoint.md
world-focus-handoff.md
world-focus-frontend-roadmap.md
world-focus-evidence-index.md when evidence map changes
relevant disposition/review checkpoint
```

A new chat must never restart from an obsolete phase because live documentation was left behind.
