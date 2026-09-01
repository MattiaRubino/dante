# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — D1 CLOSED FOR SEQUENCING / D2 NEXT  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the **first document a new chat/agent must read** when continuing World Focus.

It is intentionally concise enough to act as a live control plane, but detailed enough to prevent a new chat from restarting an obsolete phase. For full historical/architectural continuity, immediately continue with `world-focus-handoff.md` and `world-focus-frontend-roadmap.md`.

---

## 1. Live state — authoritative sequencing

```text
WF0 structural route/shell             FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 visual treatment                 CANDIDATE / integrated visual freeze pending

B0 production foundation               ENGINEERING CLOSED
WR0 World product reverse engineering  CLOSED
WR1 DANTE <-> user reverse engineering COMPLETE / 7 material gaps found
WR2 gap closure                        CLOSED / 7 of 7 gaps closed

B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity / Resume                 IMPLEMENTED / AUTOMATED PASS
B2 integrated visual acceptance        DEFERRED TO D7 / integrated composition review

Workspace/module uncertainty research  DONE / retained as evidence
World Workspace Platform               ENGINEERING CLOSED
Platform code HEAD                     6c441335a75bb913af8da1eda569d8094d38a539
Platform Frontend CI                   33549465793 — PASS

D0 contextual DANTE spatial contract   ACCEPTED
D1 quiet invoke + compact composer      CLOSED FOR SEQUENCING
D1 validated code HEAD                 f17291de32e6bdced20536807b32928ec1be6aea
D1 Frontend CI                         33552437179 — PASS

assistant manual visual review          NOT PERFORMED / no live visual-browser tool
integrated visual/micro polish          DEFERRED TO D7

NEXT ACTIVE GATE                        D2 — ADAPTIVE CONVERSATION SURFACE
```

There is **no active backend/API/database/provider/real-LLM work** in this World Focus sequence.

There is also **no ZIP/failure artifact to carry forward**. Previous failed CI runs were inspected through logs only; no Playwright failure archive became branch/project state.

---

## 2. What must NOT be re-opened from zero

A new chat must not restart broad research already closed simply because it lacks conversational history.

Do **not** restart:

```text
What is a World?
Should every Goal/Project/Person/Asset become a World?
Do we need one page per World?
What if we do not know every future module?
Should DANTE be a permanent chatbot column?
Can AI generate arbitrary UI/components?
Do stable/adaptive/ephemeral content need separation?
Does every World need a universal time Lens?
Should recent = resumable?
Should current selected UI automatically become DANTE context?
```

Those questions were already investigated, falsified where necessary, and incorporated into current contracts/evidence.

Fresh research is justified only for a **genuinely unresolved concrete subproblem** in the active slice. The working standard is:

```text
1. identify the exact open problem;
2. ask how mature/high-level products solve that exact problem;
3. identify their failure modes/trade-offs;
4. decide whether DANTE can do better while preserving DANTE semantics;
5. implement the narrowest production-grade solution;
6. test it against contrasting Worlds, widths, failures and races.
```

Do not copy competitors blindly and do not perform broad competitor research as ritual.

---

## 3. Product North Star and World definition

DANTE product North Star:

> **DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.**

Product compass:

> **Understand life. Shape what comes next.**

World Focus compass:

> **Understand this part of my life and continue from here.**

A World is:

> **A user-recognizable continuity context for a significant part of reality.**

Core thesis:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

World is not:

```text
Domain owner
folder
life-area taxonomy
universal Entity/Thing container
Goal/Project/Person/Asset automatically
DB partition
ACL/security boundary
AI memory bucket
chat room
dashboard ontology
mandatory time-range/KPI surface
```

The same canonical reality may be projected into several Worlds without duplicating canonical identity.

---

## 4. Permanent semantic / architecture barriers

Do not weaken these during frontend work:

```text
World != canonical Domain owner
WorldProjection != canonical truth
ModuleConfig != canonical source data
ModuleProjection != canonical source data
LayoutConfig != Domain semantics

AI output != accepted fact
AI proposal != user Decision
Decision != effect
Tool call != authorization
Provider success != canonical completion
Provider state != DANTE canonical state

Planned/intended != Actual
Effort != execution != outcome != Goal progress
Observation != causation
Observed pattern != confirmed preference
Absence != false
UI hiding != authorization

World relevance != ownership
World relevance != authorization
World label != retrieval specification
selected context reference != authorization
surface visibility != disclosure permission
frontend interaction cursor != durable DANTE Run
DOM node != DANTE context payload
```

Domain/logical/physical authorities remain above frontend convenience. Product/UI nouns do not automatically become canonical ontology.

---

## 5. World Output Grammar — question-driven, not widget-driven

Possible answer families:

```text
1. Orientation
2. Situation
3. Continuity / Resume
4. Attention / Resolution
5. Next
6. Change
7. Trajectory / Comparison      [only when meaningful]
8. Evidence / History
9. Explore
10. Act / Decide
11. Intelligence
```

A World does **not** need all of them.

Rendering rule:

```text
available authorized reality
-> which World questions have meaningful answers now?
-> rank/current composition
-> render a restrained subset
-> deeper evidence/action on demand
```

Never fill empty space with fake cards, generic KPIs, fabricated progress percentages, AI prose or suggested prompts merely for visual density.

---

## 6. WR0–WR2 — closed DANTE/User context model

The four-layer model must remain separate:

```text
1. WORLD IDENTITY / PURPOSE
2. STABLE WORLD RELEVANCE DEFINITION
3. CURRENT WORLD INTERACTION CURSOR / SESSION WHEN NEEDED
4. AUTHORIZED PURPOSE-SCOPED DANTE CONTEXT
```

A conceptual interaction cursor carries only bounded frontend references such as:

```text
active World reference
interaction generation
selected projection/source/module reference
current surface reference
entry/surface context
```

It does not contain:

```text
raw DOM
React nodes
secrets
authorization decisions
copied canonical source truth
provider credentials
durable Run state
```

Future authorized DANTE context is reconstructed by a Context Builder from the actual user request/purpose plus Principal/Actor/recipient, disclosure/governance, sensitivity and freshness/material basis.

Current World is a relevance prior, not a prison: cross-World expansion is allowed only when the actual purpose materially requires authorized broader context.

DANTE presentation semantic depths are already accepted:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

These are semantic depths, not a one-to-one geometry enum.

---

## 7. Frozen structural baseline

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         └ shell controls
```

Permanent ownership rules:

- Global Topbar/AppShell remain outside World Focus ownership;
- the workspace is rectangular and persistent;
- ellipse/corona/VFX geometry is visual/reference geometry only;
- World-specific content may not resize the frozen macro shell/workspace;
- deeper route-owned overlays may cover the World experience but do not redefine AppShell ownership;
- VFX degrades before interaction/performance quality;
- geometry changes require explicit contract/version/test review, not opportunistic CSS edits.

---

## 8. B0 foundation — already available

Do not recreate its infrastructure in later verticals.

B0 established:

```text
model -> application -> ui -> route dependency direction
strict typed frontend platform vocabularies
runtime boundary-validation seam
latest-only async commit protection
AbortSignal/cancellation support
safe HTTPS external-link parsing
route error boundary
local render failure boundary
persistent rectangular workspace owner
container-query foundation
User Timing/open-to-usable instrumentation
accessibility/reduced-motion foundations
ornamental WebGL capability degradation
explicit dependency non-adoptions
backend/provider/LLM stop line
```

No generic repository/data-port abstraction was introduced without a real read intent.

---

## 9. B1 Orientation — final disposition

The initial B1 hypothesis included a universal temporal Lens. Product reverse engineering demonstrated that it was not a truthful universal first-screen control.

Final B1 retained:

```text
World identity/orientation
route-owned active World
entry/exit lifecycle
loading/error/unavailable states
responsive/a11y shell behavior
```

Removed completely, not merely hidden:

```text
universal visible time Lens
Lens fixture capability
?time= route contract
Lens model/tests
Lens-only Session snapshot/scaffolding
```

A future Lens/session must be justified by a real vertical.

B1 is closed for sequencing. Typography/spacing micro-polish is deliberately not frozen as final design and will be revisited in integrated D7 composition, not used to block functional progress now.

---

## 10. B2 Continuity / Resume — current meaning

Question:

> **What is actually in motion and where can I continue?**

Critical semantics:

```text
RECENT != RESUMABLE
LAST VIEWED != LAST MEANINGFUL CHECKPOINT
OPEN != IN MOTION
UNFINISHED != IMPORTANT
AI-GUESSED RELEVANCE != CONTINUITY FACT
```

First-open continuity requires:

```text
recognizable thread identity
+ meaningful current/unfinished state
+ meaningful checkpoint
```

No fake `Resume/Riprendi` action exists until a real continuation destination/capability exists.

Presentation vocabulary `active / paused / blocked` is projection/presentation vocabulary only; it is not a replacement Domain lifecycle.

Sparse/no-manufactured-content cases are intentional for Worlds such as Finance, Relationships, Routine, Body and Growth when no real continuity answer exists.

B2 is implemented and automated-PASS. Integrated visual acceptance/polish is deferred until D7, when DANTE and deeper surfaces establish the full composition hierarchy.

---

## 11. Workspace/module uncertainty research — already completed

Durable evidence:

`world-focus-workspace-scenario-oracle-evidence.md`

Already pressure-tested:

```text
unknown future World
unknown future specialist module/surface
sparse World
dense World
large/high-frequency history
stable content + changing adaptive content
AI unavailable
provider stale/offline/partial
late async result
sensitive/multi-actor content
layout/schema evolution
narrow/mobile/reduced-motion/keyboard behavior
same canonical reality across several Worlds
```

Already accepted direction:

```text
one shared World workspace platform
not page-per-World
finite approved module/surface registries
controlled specialist extension
no arbitrary model-generated executable UI
specialist renderer only when generic primitives materially lose meaning
stable/adaptive/ephemeral remain distinct
AI cannot silently rewrite stable composition
DANTE may drive contextual Insight/Explore/deeper-surface intents
typed source drill-down on demand
large data bounded/aggregated before React
```

Do not re-run this broad architecture study.

---

## 12. World Workspace Platform — engineering closed

Final platform HEAD:

`6c441335a75bb913af8da1eda569d8094d38a539`

Frontend CI:

`33549465793` — full PASS.

Platform capabilities:

```text
DYNAMIC COMPOSITION
- stable / adaptive / ephemeral
- lead / primary / supporting
- logical 12-unit plan
- adaptive physical rendering
- finite approved module registry

WORKSPACE INTERACTION
- local transient reducer
- bounded cursor references
- generation tracking
- select / clear context
- open / replace / promote / close surfaces
- Escape precedence
- stale expectedGeneration guard

SURFACE ALLOCATION
- mainAllocation: full | split
- topLayer: none | overlay | focus
- interaction: interactive | inert
- active/dormant surface placement
- blocking-tail barrier

RESPONSIVE / PHYSICAL
- actual workspace ResizeObserver measurement
- nested world-focus-main query container
- wide sidecar consumes real canvas width
- narrow sidecar degrades to non-modal overlay
- modal/full-focus main inert
- visible underlying sidecar inert under blocking layer
- route presentation external to workspace geometry
```

Stress evidence:

```text
500 deterministic composition scenarios
500 deterministic workspace-width / surface-stack scenarios
```

The platform is not a generic dashboard builder and not a remote plugin framework.

---

## 13. D0 contextual DANTE spatial contract — accepted

Evidence:

`world-focus-dante-spatial-presence-review.md`

Official high-level product patterns reviewed there include:

```text
Google Workspace / Gemini
Microsoft 365 / Copilot
VS Code / Copilot Chat
Notion Agent
Linear Agent
```

Cross-product synthesis:

> **AI availability is persistent; AI footprint is not.**

Accepted DANTE adaptive hybrid:

```text
P0 normal World
+ small quiet DANTE invoke

P1 quick invoke
-> compact transient non-modal composer

ongoing conversation + wide allocated workspace
-> CONTENT | DANTE SIDECAR

ongoing conversation + constrained/mobile route
-> route-owned DANTE focus overlay below Global Topbar

wide/deep work when user requests
-> explicit maximize sidecar -> focus overlay

contextual/deictic use
-> explicit bounded context reference
```

Rejected as universal models:

```text
always-open chatbot column
floating support-widget-only model
focus-overlay-only model
Home AI component copied into World
fixed 320-400px pane at every width
mobile conversation squeezed into ~238px World workspace
AI prose on first open
random suggested prompts
```

---

## 14. D1 quiet invoke + compact composer — closed for sequencing

Validated D1 code HEAD:

`f17291de32e6bdced20536807b32928ec1be6aea`

Frontend CI:

`33552437179` — full PASS.

D1 implemented:

```text
quiet lower-trailing DANTE invoke
>=44px target
localized World-specific accessible name
no automatic opening
finite registered dante-composer surface
interaction depth: peek
presentation: popover
origin: user
non-modal dialog semantics
World remains interactive
textarea initial focus
close/Escape focus restoration
truthful unavailable state
truthful pre-backend submit failure
draft preservation
no fake assistant reply
no fake Run/model/tool/effect
IT/EN localization
390px containment
axe wide + compact
```

### Critical D1 context rule

Global quiet invoke opens with:

```text
contextReference: null
```

This is intentional.

A currently selected projection/source does not silently become DANTE context merely because the user presses the global DANTE control.

Explicit deictic binding belongs to D4.

### Platform bug D1 exposed and fixed

The first real non-modal popover showed that a full-workspace overlay wrapper with `pointer-events:auto` could physically block the main World even though state said `mainInteraction=interactive`.

Fix:

```text
popover allocation wrapper -> pointer-transparent
actual popover panel        -> pointer-interactive
main World                  -> remains interactive
```

This was fixed generically in `WorldFocusSurfaceLayer`, not as a DANTE-specific CSS hack.

### D1 real-browser evidence

Chromium acceptance verifies:

```text
no auto-open
aria-modal=false
textarea autofocus
World main remains interactive
computed wrapper pointer-events=none
computed composer pointer-events=auto
submit preserves draft
no fake response
Escape closes composer only
World route remains open
focus returns to invoke
390px containment
>=44px invoke/close targets
no horizontal page overflow
axe zero detectable violations wide + compact
```

Firefox frozen Timeline and Mobile regressions also PASS.

### D1 closure honesty

The assistant did **not** perform a manual human visual inspection because the available toolset did not provide a live visual-browser review surface.

The user explicitly delegated closure judgment for this saturated-chat handoff (`carta bianca / un mio ok`). Therefore D1 is **closed for sequencing** based on engineering + strict automated + real-browser functional/a11y evidence.

Integrated visual hierarchy/micro-polish remains D7 work; it is not falsely marked reviewed.

---

## 15. CURRENT ACTIVE GATE — D2 Adaptive Conversation Surface

D2 is now the only active next World Focus slice.

### Product question

> **How does the same ongoing DANTE conversation occupy the World at different available widths/depths without turning presentation geometry into conversation identity and without trapping mobile conversation inside the narrow World workspace?**

### Accepted behavior to prove

```text
wide allocated workspace
-> internal split DANTE sidecar

constrained workspace/mobile
-> route-owned DANTE focus overlay below Global Topbar

wide deep work
-> explicit maximize from sidecar to focus overlay

restore
-> same conversation identity/presentation state returns appropriately
```

### Critical route-overlay warning

The existing Workspace Platform `full-screen`/focus slot is physically **inside the rectangular World workspace**.

That is not sufficient for D0's mobile requirement.

At 390px viewport, WF0 leaves approximately ~238px workspace inline width. An ongoing conversation at ~238px is not acceptable.

D2 therefore must introduce or consume a **route-owned World overlay seam** with ownership like:

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ WORLD FOCUS SHELL
      ├ visual frame
      ├ frozen rectangular workspace
      ├ shell controls
      └ route-owned focus overlay layer
         └ may cover World workspace
         └ uses route width below Global Topbar
         └ does NOT resize/re-own Global Topbar
         └ does NOT rewrite frozen workspace geometry
```

Do not solve mobile by merely doing `position:absolute; inset:0` inside the narrow workspace.

### D2 must preserve semantic identity across geometry

```text
conversation identity != sidecar
conversation identity != overlay
conversation identity != DOM instance
conversation identity != route width
```

Responsive presentation may change because available geometry changes; the conversation itself must remain the same logical interaction.

### D2 must NOT pull D3 forward

D2 proves spatial/presentation behavior only.

Do not invent:

```text
assistant transcript
streaming
real model call
conversation backend
canonical chat persistence
fake successful answer
provider runtime
tool/effect execution
```

If a tiny conversation identity seam is necessary to prove sidecar <-> focus continuity, keep it presentation-local, typed and explicitly pre-backend. D3 owns deterministic conversation data/result semantics.

### D2 required pressure cases

At minimum:

```text
large desktop split
just above split threshold
just below split threshold
ordinary laptop allocation
~720 constrained World
390 mobile
sidecar open -> workspace contracts below threshold
constrained -> becomes wide
explicit maximize
restore from maximize
Escape/back precedence
World route unmount/switch
blocking modal interactions where relevant
keyboard/focus restoration
reduced motion
no horizontal overflow
route overlay below Global Topbar
no macro geometry mutation
```

Use actual allocated/container geometry, not duplicated viewport JS breakpoints.

---

## 16. D3–D7 forward map

### D3 — deterministic pre-backend conversation adapter

Prove presentation-independent conversation semantics:

```text
typed user message
assistant/result distinctions
conversation identity
loading/error/unavailable
cancellation/generation protection
late-result behavior
no canonical-truth implication
no real LLM/provider/backend
```

A conversation message is not automatically an Insight, Observation, Proposal, Decision or canonical fact.

### D4 — explicit contextual/deictic invocation

Introduce deliberate bounded references:

```text
projection/source selection
-> explicit contextual Ask DANTE
-> bounded context reference
```

Rules:

```text
reference != source payload
reference != authorization
reference != permission to retrieve everything related to a label
DOM != context payload
World label != retrieval specification
```

Global quiet invoke remains context-null.

### D5 — Insight presentation integration

Prove:

```text
conversation != Insight
Insight != ordinary chat message
Explore != conversation
```

A validated Insight may have a standalone registered surface when evidence/readability benefits.

### D6 — Proposal / confirmation / receipt presentation

Prove frontend governed-operation grammar:

```text
assistant suggestion != Proposal automatically
Proposal != accepted Decision
Decision != effect
Tool invocation != authorization
provider success != canonical completion
```

Consequential confirmation uses a controlled blocking surface. Still no real effect backend.

### D7 — integrated World + DANTE review / pre-backend frontend freeze

This is where deferred integrated visual work must finally be judged together:

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

At D7 perform desktop/laptop/tablet/mobile human visual review, revisit B1/B2 micro-polish, verify DANTE does not dominate first-open, pressure sparse/dense/unknown Worlds, accessibility/reduced-motion, and obtain explicit user freeze before backend vertical.

---

## 17. Backend stop line

Until the final authorized backend vertical, do **not** add merely to make the frontend look complete:

- real World business endpoints;
- DB/Alembic World persistence;
- provider SDK/runtime;
- real model routing/streaming;
- durable DANTE Run/Task backend;
- real tool/effect execution;
- fake successful backend responses;
- generic DTO/schema that front-loads an unknown backend;
- provider response treated as canonical completion.

Frontend may establish narrow typed seams and deterministic local behavior only when a real product vertical proves the need.

The backend must later plug into explicit application/context/governance seams rather than force a frontend workspace rewrite.

---

## 18. Operational / quality rules for the next chat

Stay on:

```text
repo:     MattiaRubino/dante
branch:   feature/home-react
worktree: /home/mattia/projects/dante-frontend
```

Before production writes:

```text
fetch/pull current branch
verify exact HEAD
read live checkpoint/handoff/roadmap + active evidence
inspect current implementation, do not infer from old chat text alone
```

Do not casually touch:

```text
main
Access/Auth
frozen Timeline behavior
WF0 macro structure
WF-G3 geometry
canonical Domain/Logical/Physical semantics
```

Do not merge/rebase/force-push/rewrite history without explicit authorization.

Do not manually edit generated route output.

When a gate fails, fix the cause; do not weaken lint/typecheck/architecture/a11y/E2E tests to obtain green.

No failure ZIP/artifact should become a handoff dependency.

---

## 19. Read order for the new chat

Start here, in this order:

```text
1. docs/frontend/home/world-focus-current-checkpoint.md
2. docs/frontend/home/world-focus-handoff.md
3. docs/frontend/home/world-focus-frontend-roadmap.md
4. docs/frontend/home/world-focus-product-contract.md
5. docs/frontend/home/world-focus-platform-contract.md
6. docs/frontend/home/world-focus-structural-contract.md
7. docs/frontend/home/world-focus-geometry-contract.md
8. docs/frontend/home/world-focus-workspace-platform-checkpoint.md
9. docs/frontend/home/world-focus-dynamic-composition-allocation-review.md
10. docs/frontend/home/world-focus-dante-spatial-presence-review.md
11. docs/frontend/home/world-focus-d1-dante-entry-review.md
12. docs/frontend/home/world-focus-workspace-scenario-oracle-evidence.md
13. docs/frontend/home/world-focus-delivery-methodology.md
14. docs/frontend/home/world-focus-evidence-index.md
```

Only after those should deeper archaeology be needed.

---

## 20. Acceptance / closure rule going forward

Default mini-vertical closure remains rigorous:

```text
implementation
-> strict automated gates
-> real-browser automated acceptance
-> manual/human review where available and materially necessary
-> functional/visual fixes
-> explicit user acceptance or explicit delegated closure authority
-> freeze / close-for-sequencing
-> next vertical
```

Important honesty rule:

```text
automated browser PASS != human visual review
```

Never state that a manual visual review happened if it did not.

The user may explicitly delegate closure judgment, as happened for D1. That permits sequencing when evidence is strong, but does not retroactively manufacture a human visual inspection.

---

## 21. Immediate instruction to the next chat

Do **not** restart World Focus architecture.

Do **not** implement D3 conversation messages first.

Do **not** polish the D1 button for hours.

Resume naturally at:

> **D2 — adaptive conversation surface geometry/presentation, with route-owned mobile/constrained focus overlay and wide workspace sidecar, consuming the already-closed Workspace Platform and accepted D0 contract.**

First inspect current branch code around workspace/surface ownership, then design the narrow route-owned overlay seam and presentation continuity contract before writing visual conversation content.
