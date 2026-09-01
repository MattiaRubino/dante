# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — PRE-BACKEND — D1 CLOSED FOR SEQUENCING / D2 NEXT  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the **durable high-detail handoff** for continuing the Home / World Focus workstream in a new chat without losing architecture, product reasoning, engineering standards, rejected paths, test evidence or sequencing.

For exact live status, read `world-focus-current-checkpoint.md` first. This handoff explains **why the current state exists, what has already been proven, how the branch evolved, and how the next chat must work**.

---

# 1. Mission / working standard

DANTE is not being built as a prototype that will later be “cleaned up”. Each frontend mini-vertical must be implemented as a production-grade slice whose backend seam can later be connected without a product/architecture rewrite.

Required working sequence:

```text
product semantics / user job
-> authority + already-closed research
-> focused external research only for genuinely open questions
-> architecture/state ownership
-> UI structure
-> interactions
-> responsive/container behavior
-> accessibility/focus/reduced motion
-> degraded/error/unavailable/race behavior
-> performance/resource ownership
-> tests
-> exact future backend/application seam
-> strict automated gates
-> real-browser automated acceptance
-> human/user review where available
-> truthful closure disposition
```

The expected quality bar is mature/enterprise application engineering, not demo engineering.

When an interaction/layout question is genuinely open, the decision process is:

```text
How do mature/high-level products solve this exact problem?
What trade-offs/failure modes do they expose?
What is reusable as a pattern rather than cargo cult?
Can DANTE do better while preserving its own semantics?
```

Do not blindly copy Google/Notion/Linear/Copilot/etc. They are comparison evidence, not product authority.

Do not spend multiple iterations moving a label a few pixels while high-value functional verticals are missing. Micro typography/spacing polish can be deferred until real integrated content establishes the composition — but code quality, accessibility, interaction correctness and structural design are never deferred under the label “polish”.

No fake green status is acceptable:

```text
CI green != manual visual review
implemented != accepted
provider success != canonical completion
frontend mock != backend reality
```

If the available toolset cannot perform a human visual review, say so explicitly. Never pretend one occurred.

The user explicitly delegated closure judgment for the saturated-chat D1 handoff (`carta bianca / un mio ok`), which allowed D1 to close for sequencing on strong engineering + real-browser evidence while honestly deferring integrated human visual polish.

---

# 2. Global product North Star

DANTE product North Star:

> **DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.**

Compass:

> **Understand life. Shape what comes next.**

Important product rules:

```text
life is not naturally divided by tools
life, not task/calendar/metric, is the center
time is foundational but not the container of all life
song != next Session
vehicle != next maintenance Event
effort != execution != outcome != Goal progress
no universal life score
```

DANTE's operating capability chain is broader than task management or chat:

```text
UNDERSTAND
-> DISCOVER
-> ORCHESTRATE
-> DECIDE
-> PLAN & COORDINATE
-> ACT
-> OBSERVE
-> LEARN & ADAPT
```

AI/model output remains under user and governance authority.

---

# 3. Domain / Logical / Physical invariants that frontend must respect

Frontend architecture does not get to invent a simpler ontology because it is convenient for rendering.

Domain authority: `docs/domain/README.md`.

Core semantic rules:

```text
accepted = current best justified decision, not immutable truth
specific truthful semantics > generic catch-all abstraction
native identity != contextual role
planned/intended state != Actual reality
Observation != Actual
Evidence != Provenance
Authority != Visibility
Responsibility != Participation
Ownership != Possession
provider identity != canonical DANTE identity
product/UI terminology != automatic ontology
```

Rejected canonical shortcuts:

```text
universal Entity / Thing root
universal Relationship / generic edge
universal Subject / Actor / Resource / User / ManagedObject roots
generic EAV/property-bag as canonical truth
```

Logical model remains authoritative for ownership/freshness/disclosure/concurrency semantics. Particularly important frontend consequences:

```text
absence != false
canonical != provider
freshness matters
expected-state / optimistic concurrency matters for future effects
projection/disclosure != canonical source ownership
AuthZ provenance matters
visibility/non-interference matters
```

Physical persistence remains PostgreSQL-family canonical authority; World must never become a canonical DB ownership partition simply because the UI has a World route.

Before any future DB work, re-read current DB/Alembic authority rather than relying on frontend docs or old branch snapshots.

---

# 4. Home vs Worlds vs World Focus

Home contract:

Home is the recurring cross-life orientation/operation surface for:

```text
current situation
conversational access
temporal reality
contextual information
direct action
secondary context
```

Home is not:

```text
universal dashboard
ontology browser
AI-only cockpit
```

Mondi definition:

> **Significant realities the user wants readily recoverable, resumable or explorable over time.**

World Focus is the focused route-backed surface for one World continuity context.

Product boundary:

```text
HOME
cross-life compression/orientation/operation

MONDI OVERVIEW
view/management of Worlds as a system

WORLD FOCUS
scoped expansion/understanding/continuation of one World

EXPLORE / DETAIL
specialist/evidence/history/deeper depth
```

World Focus route:

`/worlds/:worldId`

It is not a Home overlay and not a chat route disguised as a World.

---

# 5. What a World is — final product contract

World Focus compass:

> **Understand this part of my life and continue from here.**

A World is:

> **A user-recognizable continuity context for a significant part of reality.**

Core thesis:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

World-worthiness is about recurring re-entry and continuity, not ontology class:

```text
recurring re-entry
continuity / history / intent
resumability
situational understanding
meaningful change
scoped decisions/actions
deeper exploration
stable human-recognizable identity
```

Never auto-map:

```text
Goal -> World
Project -> World
Person -> World
Asset -> World
Calendar -> World
Domain category -> World
```

World is not:

```text
canonical Domain owner
folder
life-area taxonomy
dashboard ontology
universal relation container
universal Entity/Thing container
DB partition
ACL/security boundary
AI memory bucket
chat room
mandatory Goal/time-range/KPI surface
```

Worlds may overlap. The same canonical reality may appear in several Worlds without duplication of canonical identity/source truth.

World relevance is a contextual prior, not ownership or authorization.

---

# 6. World Output Grammar

World Focus is **question-driven, not widget-driven**.

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

A World need not answer all 11.

Sparse rule:

```text
available meaningful authorized answers
-> rank by current value
-> render restrained subset
-> deeper evidence/action on demand
```

Do not fill missing questions with:

```text
fake cards
fake KPIs
fake % progress
recent-activity filler
AI prose on first open
suggested prompts for visual fullness
dummy charts
```

A composition module is a renderer/presentation capability, not a canonical semantic owner and not automatically equivalent to one Output Grammar question.

---

# 7. WR0 / WR1 / WR2 history and closed context model

## WR0 — World product reverse engineering

WR0 pressure-tested World definition and first-open behavior against external patterns and contrasting World archetypes.

It also falsified the early assumption that every World should expose a universal visible time Lens on first open.

Durable result:

```text
World is continuity context, not a dashboard template
first-open is sparse/question-driven
time Lens only exists where multiple prominent projections genuinely share the same meaningful temporal scope
```

## WR1 — DANTE <-> user reverse engineering

WR1 found seven material gaps around World relevance, visible/DANTE basis coherence, cross-World escalation, DANTE presence, deictic cursor, Home/World attention identity and first-open LLM independence.

## WR2 — targeted gap closure

All seven gaps were closed. No new structural Domain/Logical/Physical/DB/Intelligence gap remained.

Four-layer World context model:

```text
1. WORLD IDENTITY / PURPOSE
2. STABLE WORLD RELEVANCE DEFINITION
3. CURRENT WORLD INTERACTION CURSOR / SESSION WHEN ACTUALLY NEEDED
4. AUTHORIZED PURPOSE-SCOPED DANTE CONTEXT
```

The frontend interaction cursor may contain bounded refs such as:

```text
world reference
interaction generation
selected projection/source/module ref
active Insight/Explore/surface ref
entry/surface context
```

Never:

```text
DOM node
React tree
secrets
authorization decision
copied canonical source truth
provider credentials
durable DANTE Run state
```

Future Context Builder:

```text
World identity/purpose
+ stable relevance
+ interaction cursor
+ actual user request/purpose
+ Principal / Actor / recipient
+ sensitivity/disclosure/governance
+ freshness/material basis
-> authorized minimized DANTE context
```

Current World is a relevance bias, not a reasoning prison. DANTE may use broader cross-World context only when the user purpose materially requires it and authorization/disclosure permit it.

Visible projection and DANTE output must remain coherent in basis/freshness; DANTE cannot silently answer from materially newer/different source state while the screen pretends old state is current.

DANTE semantic presentation depths:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

These are semantic depths, not fixed geometries.

---

# 8. Structural baseline — WF0 / WF-G3 / WF-V4

## WF0 route/shell — frozen

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         └ shell controls
```

The Global Topbar/AppShell are outside World Focus ownership.

## WF-G3 geometry — locked

Frozen macro geometry concepts:

```text
workspace = rectangular content/interaction authority
ellipse/corona = visual/reference geometry only
```

The workspace must never be clipped into the ellipse and World content may not reposition macro shell geometry by identity.

Historical geometry values include:

```text
center 50/50
outer ellipse rx 52.25%, ry 90%
origin rx 50%, ry 87%
inner rx 47.75%, ry 84%
standard workspace inline inset clamp(136px, 14vw, 224px)
compact inline inset clamp(76px, 18vw, 112px)
standard block inset clamp(32px, 5vh, 64px)
compact block inset 20px
compact <=720
```

If a future change really requires macro geometry modification, update the structural/geometry contracts and tests explicitly; do not silently drift CSS.

## WF-V4 VFX — candidate

Visual treatment remains candidate, not human-frozen final design.

VFX must degrade before it harms:

```text
input latency
scroll/focus
battery/resource use
software-rendered environments
reduced-motion preference
```

VFX has no authority to move product content.

---

# 9. B0 production foundation — engineering closed

B0 created reusable infrastructure later slices must consume rather than recreate:

```text
model -> application -> ui -> route dependency direction
strict typed frontend platform vocabulary
runtime validation seam for untrusted boundaries
WorldFocusLatestReadCoordinator / latest-only commit behavior
AbortSignal propagation
safe HTTPS external URL parser
route error boundary
local renderer error boundary
persistent rectangular workspace
container-query foundation
open-to-usable User Timing
accessibility/focus/reduced-motion baseline
ornamental WebGL capability degradation
```

Explicit non-adoptions were intentional: no Redux/Zustand/XState/TanStack Query/Zod/etc. merely because the feature might grow. Add dependencies only when a real vertical proves material value that existing code cannot meet cleanly.

No generic repository/data port was invented; each real projection vertical introduces intent-specific seams.

---

# 10. B1 Orientation — history and final disposition

Initial B1 included a universal visible temporal Lens. User/product challenge triggered deeper reverse engineering rather than cosmetic defense of the design.

WR0–WR2 showed that a global Lens would be misleading for many Worlds.

Final B1 retained:

```text
World orientation
World title/description
route-owned active World
entry/exit lifecycle
loading/error/unavailable states
responsive/a11y behavior
```

Removed completely:

```text
visible universal time Lens
Lens fixture capability
?time= route contract
Lens model/tests
Lens-only Session state/scaffolding
```

Important engineering lesson:

> When product semantics reject a capability, remove its hidden infrastructure too unless another real vertical independently justifies it.

B1 is closed for sequencing. Micro title/spacing polish is intentionally deferred to the integrated D7 composition review; it must not distract from serious functional verticals.

---

# 11. B2 Continuity / Resume — first real question-driven capability

Question:

> **What is actually in motion and where can I continue?**

Durable semantic rules:

```text
RECENT != RESUMABLE
LAST VIEWED != LAST MEANINGFUL CHECKPOINT
OPEN != IN MOTION
UNFINISHED != IMPORTANT
AI-GUESSED RELEVANCE != CONTINUITY FACT
```

A first-open continuity item requires:

```text
recognizable thread identity
+ meaningful current/unfinished state
+ meaningful checkpoint
```

A checkpoint is not `lastViewedAt`. Future truthful bases may include meaningful Session, artifact/version, accepted Decision, confirmed plan step, explicit progress marker or provider-backed state.

Presentation states:

```text
active
paused
blocked
```

These are UI/projection vocabulary only, not replacement Domain lifecycle.

No fake `Riprendi/Resume` button exists until a real route/capability can truthfully continue the work.

Cross-World sparse behavior is intentional. Example pressure:

```text
Music/Travel/Study/Projects may have real continuity
Finance/Relationships/Routine/Body/Growth may legitimately have none
```

No content is manufactured to fill the workspace.

B2 application design:

```text
intent-specific read adapter / reader
runtime validation
bounded first-open projection
ready / empty / partial / stale / unavailable distinctions
latest-only/race-safe read
surface-local/read-local degradation
deterministic pre-backend fixture adapter
```

B2 remains automated PASS. Human integrated visual polish is deferred to D7, where DANTE and deeper surfaces establish the full hierarchy.

---

# 12. Unknown future World/module research — already completed

The broad “we do not know all future modules” question was already studied and recovered as durable evidence:

`world-focus-workspace-scenario-oracle-evidence.md`

Pressure included:

```text
unknown future World
unknown specialist module
sparse and dense Worlds
large/high-frequency history
multiple providers
stale/offline/partial data
AI unavailable
late async after navigation/generation change
sensitive/multi-actor material
customization + changing adaptive content
responsive/reduced-motion/keyboard
schema/layout evolution
same canonical reality projected into several Worlds
```

Accepted results:

```text
one shared workspace platform
not page-per-World
no generic WorldItem/Thing semantic root
finite approved renderers/surfaces
controlled specialist extension
no arbitrary AI/model executable UI
specialist renderer only when reusable primitives materially lose meaning
stable/adaptive/ephemeral remain distinct
AI cannot silently mutate stable composition
DANTE can request contextual Insight/Explore/deeper surface intents
typed source drill-down on demand
large data bounded/aggregated before React
same canonical reality reused across Worlds without duplication
future persisted stable configuration needs version/evolution semantics
```

A new chat must not repeat this research as if it were missing.

---

# 13. World Workspace Platform — final engineering closure

Final platform code HEAD:

`6c441335a75bb913af8da1eda569d8094d38a539`

Frontend CI:

`33549465793` — full green.

Durable checkpoint:

`docs/frontend/home/world-focus-workspace-platform-checkpoint.md`

Detailed allocation research:

`docs/frontend/home/world-focus-dynamic-composition-allocation-review.md`

## 13.1 Dynamic composition

Planner distinctions:

```text
stability: stable | adaptive | ephemeral
prominence: lead | primary | supporting
footprint: wide | standard | compact
```

Logical plan uses a 12-unit contract. Physical CSS rendering is adaptive and may collapse to one column at narrow allocated width rather than maintaining pathological 12 physical tracks/gaps.

Automated deterministic stress:

```text
500 synthetic World/user compositions
0-20 candidate answers
unknown kinds
sparse/dense mixes
```

No World identity branch is required for layout planning.

## 13.2 Workspace state / interaction cursor

Local transient reducer owns:

```text
world id
generation
selection reference
surface descriptors
```

Surface operations:

```text
open
replace
promote
close
close top
```

`expectedGeneration` makes stale async presentation intents deterministic no-ops.

This is frontend presentation protection, not durable Run cancellation.

## 13.3 Escape / blocking stack

Escape ownership:

```text
blocking non-dismissible top surface
-> consumes Escape
-> World cannot close underneath

dismissible top surface
-> close surface only

no surface
-> route may close World
```

A blocking-tail barrier also prevents a newer non-blocking surface from jumping semantically above an authoritative modal/full-focus state.

## 13.4 Allocation axes

Instead of a combinatorial “workspace mode” enum, the platform separates:

```text
mainAllocation   full | split
topLayer         none | overlay | focus
mainInteraction  interactive | inert
```

This supports states such as a split DANTE sidecar visible under a confirmation modal without losing deterministic restoration.

Current pre-backend UI policy:

```text
minimum split workspace   900 px
minimum useful main       520 px
minimum sidecar           300 px
maximum sidecar           420 px
preferred sidecar         36%
split gap                 16 px
```

These are presentation policy, not Domain semantics or persisted World configuration.

## 13.5 Sidecar / overlay / focus rules

```text
wide sidecar
-> takes real canvas width
-> main remains interactive

sidecar when split minima cannot be satisfied
-> non-modal overlay fallback
-> main remains interactive

modal/full-focus
-> main inert
-> visible underlying sidecar inert

older competing surfaces
-> dormant / not competing in DOM

route presentation
-> external to workspace geometry
```

## 13.6 Actual allocated container

Reusable modules adapt against the **main canvas they truly received**, not `window.innerWidth` and not the full workspace.

Example:

```text
workspace 1280
├ main 844  <- container: world-focus-main / inline-size
├ gap 16
└ sidecar 420
```

A module sees 844 px.

`ResizeObserver` measures workspace allocation. Missing `ResizeObserver` support degrades safely after initial measurement rather than crashing.

## 13.7 External benchmark used

Official mature patterns reviewed for this problem:

```text
Microsoft Fluent 2 Drawer
WAI-ARIA modal dialog pattern
MDN CSS Container Queries
```

Important synthesis:

```text
visual overlay geometry != modal interaction
```

A popover/non-modal overlay can cover part of content while the main remains interactive; a real modal/full-focus surface must make underlying interaction inert.

---

# 14. D0 contextual DANTE spatial/presence reverse engineering

Document:

`docs/frontend/home/world-focus-dante-spatial-presence-review.md`

The broad product question was:

> How should DANTE occupy a World without turning the World into a chatbot, permanently wasting content width or becoming a disconnected support widget?

Official product patterns reviewed:

```text
Google Workspace / Gemini
Microsoft 365 / Copilot
VS Code / Copilot Chat
Notion Agent
Linear Agent
```

Cross-product conclusion:

> **AI availability is persistent; AI footprint is not.**

The mature pattern is multi-depth presence:

```text
small invoke
contextual/local invocation
side-by-side conversation when width supports it
focus/deep surface when task depth or geometry requires it
explicit confirmation for consequential work
```

Accepted D0 adaptive hybrid:

```text
P0
World content + quiet DANTE invoke

P1
compact transient non-modal composer

ongoing conversation, wide allocation
CONTENT | DANTE SIDECAR

ongoing conversation, constrained/mobile
DANTE FOCUS OVERLAY using route space below Global Topbar

wide deep work
explicit MAXIMIZE -> focus overlay

P2 contextual invocation
explicit bounded selected projection/source reference
```

Rejected as universal models:

```text
always-open right chat column
floating support widget only
focus overlay only
Home AI surface copied into World
fixed 320-400px pane at every width
mobile chat squeezed into the ~238px World workspace
AI prose on World first-open
random suggested prompts
model-selected executable components
chat history as canonical World truth
```

Important D0 mobile geometry finding:

At 390px viewport, WF0 leaves roughly ~238px of World workspace width. This is acceptable for the compact D1 invoke/composer but **not for an ongoing D2 conversation**.

Therefore D2 must use route-owned space below the Global Topbar for constrained/mobile focus conversation.

---

# 15. D1 contextual DANTE entry — final state

D1 was the first concrete consumer of the closed Workspace Platform.

Validated D1 **code** HEAD:

`f17291de32e6bdced20536807b32928ec1be6aea`

CI:

`33552437179` — complete PASS.

Final review/disposition:

`docs/frontend/home/world-focus-d1-dante-entry-review.md`

## 15.1 D1 product behavior

First-open remains:

```text
World
+
small quiet DANTE invoke
```

DANTE does not auto-open.

The compact composer is:

```text
instanceId: dante:composer
kind:       dante-composer
depth:      peek
presentation: popover
origin:     user
```

It is non-modal:

```text
aria-modal=false
no focus trap
World main remains interactive
no sidecar width reservation
```

## 15.2 Critical context decision

Global quiet invoke explicitly passes:

```text
contextReference: null
```

This is deliberate.

The currently selected workspace item must not silently become DANTE context just because the user clicked the global DANTE affordance.

Explicit contextual/deictic invocation belongs to D4 and will pass a deliberate bounded reference.

## 15.3 DOM focus ownership

`WorldFocusDanteEntryProvider` owns:

```text
worldId
worldLabel
feature availability
invokerRef
restoreInvokerFocus
```

DOM focus references deliberately stay outside the generic World interaction cursor so DOM nodes cannot become:

```text
DANTE context
authorization input
canonical source state
durable Run state
```

## 15.4 Focus behavior

```text
invoke
-> composer opens
-> textarea focus

feature unavailable before open
-> composer unavailable state
-> close action focus

explicit close or Escape
-> composer closes
-> focus returns exact invoking DANTE control when still mounted
```

Background updates do not steal focus.

## 15.5 Truthful pre-backend submit

D1 has no model/runtime backend.

Submitting a non-empty draft therefore:

```text
preserves draft
shows localized truthful unavailable status
returns focus to textarea
creates NO fake answer
creates NO conversation Run
creates NO tool call
creates NO effect
creates NO canonical fact
```

This proves degraded UI safety without faking D3/backend behavior.

## 15.6 Pointer-events platform bug found and fixed

The first real `popover` consumer exposed a mismatch:

```text
allocation said: main interactive
DOM wrapper said: pointer-events auto over entire workspace
```

That physically blocked World interaction.

Fix is generic in `WorldFocusSurfaceLayer`:

```text
presentation=popover wrapper -> pointer-events:none
actual popover panel          -> pointer-events:auto
```

This is not a one-off DANTE CSS exception.

## 15.7 Invalid TS/TSX registry issue found and cleaned

Initial D1 HEAD `e49aaeca...` failed CI because `world-focus-core-surfaces.ts` contained JSX.

Correct fix:

```text
create world-focus-core-surfaces.tsx
remove invalid .ts duplicate
```

We did **not** replace JSX with `createElement` simply to preserve a wrong file extension.

## 15.8 D1 automated evidence

D1-specific unit/component suite covers:

```text
quiet initial state
single composer surface
contextReference=null
popover + interactive allocation
pointer-transparent wrapper
textarea initial focus
truthful degraded submit
draft preservation
no fake response
unavailable state
close focus
focus restoration
```

D1 Chromium E2E covers:

```text
no auto-open
aria-modal=false
World remains interactive
computed wrapper pointer-events=none
composer pointer-events=auto
textarea focus
truthful submit degradation
Escape closes composer only
World route remains /worlds/music
focus restored to invoke
390px containment
>=44px invoke/close targets
no horizontal page overflow
axe zero detectable violations at wide + 390
```

Full CI additionally preserves:

```text
lint
typecheck
architecture
generated-source drift
production build
Mobile bundle
Firefox frozen Timeline behavior
Frontend CI Gate
```

No failure ZIP/artifact was made part of the handoff.

## 15.9 D1 closure disposition

D1 is:

**CLOSED FOR SEQUENCING — ENGINEERING + AUTOMATED REAL-BROWSER ACCEPTANCE PASS; MANUAL INTEGRATED VISUAL POLISH DEFERRED**

The assistant did not have a live manual visual-browser tool, so no human visual review is claimed.

The user explicitly delegated closure judgment for the saturated-chat handoff. That supports sequencing to D2; it does not manufacture a manual visual review.

---

# 16. Documentation alignment performed during saturated-chat closure

The branch had several live docs still describing an obsolete `Workspace Platform next` phase after that platform had already closed and D1 had started.

The cleanup aligned:

```text
world-focus-d1-dante-entry-review.md
world-focus-workspace-platform-checkpoint.md
world-focus-frontend-roadmap.md
world-focus-evidence-index.md
world-focus-current-checkpoint.md
world-focus-handoff.md
```

Key stale statements removed/reframed:

```text
Workspace Platform is next              -> false; platform is closed
production surface registry is empty    -> false; D1 composer registered
DANTE spatial gate still open           -> false; D0 accepted
no later World vertical active          -> false; D1 closed / D2 next
```

Research files may retain historical status language where useful as evidence, but the evidence index explicitly states that historical status lines never override live checkpoint/roadmap authority.

`world-focus-dante-spatial-presence-review.md` should also be read as D0 decision evidence; its original “decision requested” wording is historical because D1 subsequently implemented the accepted direction. If its top status remains historical, current checkpoint/handoff/roadmap override it.

---

# 17. CURRENT NEXT GATE — D2 Adaptive Conversation Surface

D2 is now the only active World Focus implementation slice.

## 17.1 D2 product question

> **How does the same ongoing DANTE conversation occupy the World at different available widths/depths without turning geometry into conversation identity and without trapping mobile conversation inside the narrow World workspace?**

## 17.2 Accepted D2 geometry from D0

```text
wide allocated workspace
-> internal split sidecar

constrained workspace / mobile
-> route-owned DANTE focus overlay below Global Topbar

wide deep work
-> explicit maximize sidecar -> focus overlay

restore
-> same logical conversation returns to appropriate presentation
```

## 17.3 Critical route-owned overlay seam

The currently implemented Workspace Platform `focus/full-screen` slot is physically inside `world-focus-workspace`.

That cannot by itself satisfy D0 mobile requirements because the mobile workspace may be only ~238px wide.

D2 must design a narrow route-owned overlay seam:

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ WORLD FOCUS SHELL
      ├ visual frame
      ├ rectangular workspace      [stays frozen in place]
      ├ shell controls
      └ route-owned focus overlay
         ├ covers World experience when active
         ├ uses route width below Global Topbar
         ├ does not resize/re-own Topbar
         └ does not mutate WF-G3 workspace geometry
```

Do not “solve” D2 mobile by applying `position:absolute; inset:0` inside the narrow workspace.

## 17.4 Conversation identity must be presentation-independent

D2 must enforce conceptually:

```text
conversation identity != sidecar
conversation identity != overlay
conversation identity != route width
conversation identity != DOM instance
conversation identity != React component mount
```

Responsive geometry may change because allocation changes; the logical conversation interaction must remain the same.

## 17.5 D2 must not implement D3 by accident

D2 is geometry/presentation/state ownership.

Do not add:

```text
assistant transcript
fake assistant message
streaming
real model request
provider adapter
conversation API
canonical conversation persistence
real Run/Task backend
tool/effect execution
```

A tiny typed conversation/session identity seam may exist only if required to prove sidecar <-> route-overlay continuity. Keep it presentation-local/pre-backend and do not invent backend schema.

## 17.6 D2 pressure matrix

At minimum verify:

```text
wide desktop split
just above split threshold
just below split threshold
ordinary laptop workspace
~900 / ~720 edge widths
390 mobile
sidecar open -> container contracts below split threshold
constrained -> container becomes wide
explicit maximize
restore from maximize
Escape/back precedence
World route unmount/switch
blocking modal/focus interactions where applicable
keyboard
focus placement/restoration
reduced motion
no horizontal overflow
Global Topbar ownership unchanged
WF0/WF-G3 macro geometry unchanged
```

Use actual allocated/container geometry. Avoid duplicate JS viewport breakpoint state.

## 17.7 Focus/accessibility expectations

Ordinary sidecar conversation:

```text
not modal
no focus trap
main World remains usable
clear accessible region/name
```

Route-owned focus conversation:

- define whether it behaves as a modal/focus-owned application surface based on actual interaction semantics, not visual size alone;
- if background is non-interactive, implementation must truly enforce inert/focus semantics;
- Escape/back must be deterministic and never close the World underneath a blocking child incorrectly;
- focus restoration must follow the actual invoker/logical continuation.

Do not misuse `aria-modal` on a surface that does not actually make outside content inert.

## 17.8 D2 research rule

Broad DANTE spatial competitor research is already done.

Fresh research is allowed only for an unresolved subproblem such as:

```text
route-level overlay ownership
responsive presentation continuity
focus surface accessibility semantics
maximize/restore interaction pattern
```

Use current official sources where fresh research matters.

---

# 18. D3–D7 roadmap after D2

## D3 — deterministic pre-backend conversation adapter

Goal: prove conversation semantics independent of presentation.

Expected bounded concepts:

```text
conversation identity
user message
assistant/result distinction
loading
error
unavailable
cancellation/generation behavior
late-result protection
```

Still no real LLM/provider/backend.

Important barriers:

```text
conversation message != Insight automatically
conversation message != Observation automatically
assistant text != accepted fact
assistant suggestion != Proposal automatically
```

## D4 — explicit contextual/deictic invocation

Introduce deliberate references from selected/source-backed UI.

Example:

```text
Continuity item
-> explicit Ask DANTE
-> bounded projection/source reference
-> user can ask "why?", "compare with before", "show source"
```

Rules:

```text
bounded reference != source truth
bounded reference != authorization
bounded reference != broad retrieval permission
DOM != context payload
World label != retrieval spec
```

Global quiet invoke remains `contextReference:null`.

## D5 — Insight presentation integration

Prove separation:

```text
conversation != Insight
Insight != ordinary message
Explore != conversation
```

A validated Insight may use its own registered surface when evidence/readability benefits.

## D6 — Proposal / confirmation / receipt

Prove frontend grammar up to governed operation boundary:

```text
assistant suggestion != Proposal automatically
Proposal != Decision
Decision != effect
Tool call != authorization
provider 2xx != canonical completion
runtime completion != Actual automatically
```

Consequential confirmation uses a controlled blocking surface. Existing blocking-tail/Escape behavior must be consumed rather than recreated.

Still no real backend effect.

## D7 — integrated visual/product/a11y review and pre-backend freeze

Review the entire World interaction composition together:

```text
Orientation
Continuity
quiet DANTE
composer
adaptive conversation
contextual invocation
Insight
Proposal / confirmation / receipt
responsive behavior
VFX/content hierarchy
```

D7 is where deferred B1/B2 micro-polish must be revisited with real integrated context.

Pressure:

```text
desktop
laptop
tablet
mobile
sparse World
dense World
AI unavailable
unknown future World
unknown specialist surface
keyboard/reduced motion
```

Obtain explicit user frontend/product freeze before real backend vertical.

---

# 19. Additional World content verticals

The Output Grammar remains broader than DANTE D1-D7:

```text
Orientation
Situation
Continuity / Resume
Attention / Resolution
Next
Change
Trajectory / Comparison
Evidence / History
Explore
Act / Decide
Intelligence
```

Do not pre-freeze a giant module roadmap now.

After D0/D1-D7 stabilizes contextual interaction and workspace ownership, choose additional World question verticals by:

```text
cross-World user value
semantic truthfulness
architecture proof value
risk
pre-backend implementability
interaction with frozen workspace/DANTE behavior
```

Do not create generic plumbing before a real output family requires it.

---

# 20. Personalization / future stable configuration

Do not jump to a freeform dashboard builder.

Only after several real modules/compositions prove the model, consider deliberate customization:

```text
View
-> Customize Draft
-> Apply / Cancel
```

Rules:

```text
removing a module != deleting canonical reality
layout/config != Domain semantics
DANTE suggestion != applied config
future persisted config needs version/concurrency semantics
no silent last-write-wins for meaningful stable configuration
```

---

# 21. Contrasting World validation requirement

Before final frontend freeze, the same platform must work across materially different Worlds:

```text
Music
Travel
Finance
Study or Body
Relationships / qualitative pressure
unknown future World
```

Pressure should include:

```text
empty
1-2 useful answers
4-8 answers
12
20 potential answers
fresh/partial/stale/provider unavailable
AI unavailable
multi-actor/privacy
large history
same canonical reality across Worlds
unknown specialist surface
```

If success requires a separate page architecture branch by World identity, the platform has failed.

---

# 22. Backend stop line — do not cross in D1-D7

Before explicit backend vertical authorization, do not add merely to make UI look complete:

```text
real World business API
DB/Alembic World persistence
provider SDK/runtime
real LLM/model routing
real streaming
durable Run/Task backend
real tool/effect execution
fake successful backend result
generic fake DTO/schema pretending future backend is known
provider state treated as canonical DANTE truth
```

Frontend may create narrow typed seams/deterministic adapters only when a real product slice proves need.

Later backend integration must plug into explicit application/context/governance seams rather than requiring frontend redesign.

Architecture/effect reminder:

```text
caller intent/request
-> operation interpretation / target resolution
-> Governed Operation Request
-> material/freshness preconditions
-> governance/disclosure/autonomy/confirmation
-> execution
-> canonical/provider/runtime/user result axes
```

Tool invocation is not authorization and runtime completion is not automatically Actual.

---

# 23. Code areas the next chat should understand before D2 writes

Primary current World Focus frontend:

```text
apps/web/src/features/world-focus/model/
apps/web/src/features/world-focus/application/
apps/web/src/features/world-focus/ui/
apps/web/e2e/
packages/i18n/src/resources/{it,en}/world-focus.ts
```

Key current files:

```text
model/world-focus-platform.ts
model/world-focus-workspace.ts
model/world-focus-workspace-allocation.ts
model/world-focus-composition-plan.ts

ui/world-focus-page.tsx
ui/world-focus-workspace.tsx
ui/world-focus-workspace-host.tsx
ui/world-focus-workspace-allocation-context.tsx
ui/world-focus-surface-layer.tsx
ui/world-focus-surface-registry.ts
ui/world-focus-core-surfaces.tsx
ui/world-focus-composition-host.tsx
ui/world-focus-core-composition.tsx or corresponding current core composition file
ui/world-focus-dante-entry.tsx
ui/world-focus-dante-entry.css
ui/world-focus.css
```

Before modifying D2, fetch/inspect actual current files. Do not trust filenames from an old chat blindly if the branch changed.

Relevant tests:

```text
world-focus-workspace*.test.*
world-focus-composition*.test.*
world-focus-surface-layer.test.tsx
world-focus-dante-entry.test.tsx
apps/web/e2e/world-focus-dante-entry.spec.ts
apps/web/e2e/world-focus-workspace-platform.spec.ts
apps/web/e2e/world-focus.spec.ts
```

Preserve frozen Timeline regression coverage.

---

# 24. CI / gate discipline learned during current work

Several issues were caught by strict CI and fixed at root cause rather than suppressed:

```text
invalid JSX in .ts registry
strict TypeScript/ESLint unsafe mock typing
legacy SurfaceLayer tests outside new provider contract
non-modal popover DOM wrapper blocking main pointer interaction
```

The correct pattern is:

```text
failure
-> inspect exact job logs
-> understand whether production code, test harness or architecture is wrong
-> fix root cause
-> rerun exact HEAD
```

Do not:

```text
disable lint rule
weaken assertion
skip failing test without evidence
claim flaky when root cause is unknown
carry failure ZIP as project state
claim PASS from an older SHA
```

The final validated D1 code SHA is explicitly recorded so later doc commits cannot be confused with code validation evidence.

---

# 25. Documentation authority / read order

A new chat should read in this order:

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

Then consult deeper WR/B0/B1/B2/VFX evidence only as needed.

Rules:

- live checkpoint + handoff + roadmap define current sequencing;
- Product/Platform/Structural/Geometry contracts define accepted product/architecture boundaries;
- evidence docs preserve reasoning and may contain historical status language;
- frontend docs never override Domain/Logical/Physical/DB/Intelligence authority.

---

# 26. Operational safety

Stay on:

```text
repo:     MattiaRubino/dante
branch:   feature/home-react
worktree: /home/mattia/projects/dante-frontend
```

Before writes:

```text
git/fetch/pull current branch or inspect remote branch HEAD
verify exact HEAD
inspect current status/diff
read active contract/evidence
```

Do not casually modify:

```text
main
Access/Auth
frozen Timeline behavior
WF0 macro structure
WF-G3 geometry
canonical DB/domain model
```

No merge, rebase, force-push, main mutation or history rewrite without explicit authorization.

Do not manually edit generated route output.

Keep commits focused and reviewable. Update live docs when sequencing materially changes.

---

# 27. Acceptance / closure policy

Default gate:

```text
implementation
-> strict automated PASS
-> real-browser automated acceptance
-> human/manual review when available and materially required
-> user functional/visual review
-> fixes/rerun
-> explicit user OK
-> freeze
```

However, the user can explicitly delegate closure authority. D1 is the precedent:

```text
engineering complete
strict CI complete
real browser functional/a11y complete
manual assistant visual review unavailable
user delegates closure judgment
-> CLOSED FOR SEQUENCING
-> integrated visual polish honestly deferred
```

Never transform delegated closure into a false claim that a manual review happened.

---

# 28. Immediate next-chat operating instruction

The next chat should **not** spend time re-learning what a World is or proposing another generic workspace architecture.

It should:

```text
1. fetch/read current feature/home-react branch;
2. verify current HEAD and docs;
3. inspect current World shell/workspace/surface ownership;
4. re-read D0 + D1 + final Workspace Platform evidence;
5. start D2 product/architecture pass narrowly around adaptive conversation geometry;
6. define the route-owned focus-overlay seam below Global Topbar;
7. define sidecar <-> focus presentation continuity without inventing D3 message semantics;
8. implement complete D2 behavior;
9. pressure wide/laptop/threshold/720/390, maximize/restore, Escape/focus, reduced motion;
10. run exact-head lint/typecheck/architecture/unit/build/Chromium/Firefox/Mobile/axe;
11. document factual disposition before moving to D3.
```

The most important D2 warning to carry forward is:

> **Do not treat the current workspace-local `full-screen` surface as the final mobile conversation solution. D0 explicitly requires constrained/mobile ongoing DANTE conversation to use route-owned width below the Global Topbar, because the frozen World workspace can be only ~238px wide at 390px viewport.**

And the most important semantic warning is:

> **Presentation geometry is not conversation identity, World relevance is not authorization, and DANTE output is not canonical truth.**
