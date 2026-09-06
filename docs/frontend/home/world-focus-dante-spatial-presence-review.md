# DANTE — World Focus Contextual DANTE Spatial / Presence Review

**Status:** D0 PRODUCT DIRECTION ACCEPTED — RESEARCH CLOSED / D1 IMPLEMENTED / D2 CONSUMES THIS CONTRACT  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

> Current disposition note: this review originally ended with a request for user acceptance before production DANTE UI. That gate was subsequently accepted and D1 was implemented against the adaptive-hybrid direction. The research/alternatives below remain authoritative evidence; the old acceptance request is historical, not a current blocker. Live sequencing is controlled by `world-focus-current-checkpoint.md`, `world-focus-handoff.md` and `world-focus-frontend-roadmap.md`.

## 1. Scope

This review closes the product/interaction question intentionally left open by WR2, B1, B2 and the Workspace Platform:

> **How should contextual DANTE occupy and interact with the World Focus experience without turning the World into a chatbot, destroying content density, or creating a second disconnected AI product?**

This is a spatial/presence decision only. It does not reopen Domain, Logical, Physical/DB, World semantics, DANTE Intelligence architecture or the frozen WF0 route/workspace geometry.

## 2. Existing non-negotiable constraints

```text
World != chatbot page
DANTE is native but World must work without AI
P0 QUIET through P5 ACTION/RECEIPT are semantic depths, not geometry
Home AI surface != World contextual DANTE surface
World workspace is the persistent rectangular application authority for ordinary composition
route/topbar/visual-frame/workspace macro geometry remains WF0/WF-G3 frozen
route-owned focus overlay may cover World experience but may not reauthor AppShell/Topbar ownership
World composition != DANTE context universe
selection/cursor references != authorization
AI output != fact
AI proposal != Decision
Decision != effect
```

## 3. External product reverse engineering

The useful pattern is not that one mature product has "the answer". The useful finding is that mature AI-enabled workspaces increasingly use **multiple spatial modes tied to task depth**, rather than one permanent chat geometry.

### 3.1 Google Workspace / Gemini

Google Workspace guidance exposes Gemini through a side panel across apps. In Docs, Google also supports a lower-footprint bottom bar and lets the user move between bottom bar and side panel. The bottom bar can minimize to clear the document, while the side panel supports larger responses and persistent conversation beside the work.

Official references reviewed:

- https://support.google.com/a/users/answer/15146419
- https://support.google.com/docs/answer/13447609

Useful lesson:

```text
quiet/minimized entry
!=
expanded persistent conversation
```

A single AI geometry is unnecessary even inside one application surface.

### 3.2 Microsoft 365 / Copilot

Microsoft's Dynamic Action Button consolidates Copilot invocation into a small corner entry point in Word/Excel/PowerPoint. Activating it opens agent/chat UI with more room. Word also combines in-canvas work with chat/pane behavior.

Official references reviewed:

- https://support.microsoft.com/en-us/office/foundations-experiences/copilot-dab/the-copilot-dynamic-action-button-in-word-excel-and-powerpoint
- https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word

Useful lesson:

```text
persistent AI availability can be represented by a small invoke control
without permanently reserving a large pane
```

### 3.3 VS Code / Copilot Chat

VS Code supports several interaction depths: Secondary Side Bar for ongoing Chat, chat editor when more room is useful, inline chat for local context and Quick Chat for lower-interruption questions.

Official references reviewed:

- https://code.visualstudio.com/docs/agents/run/chat-view
- https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet

Useful lesson:

```text
ongoing conversation -> side-by-side surface
quick contextual question -> local/ephemeral surface
deep conversation -> larger dedicated surface
```

The semantic assistant can remain one capability while presentation depth changes with the task.

### 3.4 Notion Agent

Notion exposes its Agent from a small corner presence. Chat opened from a page can receive page context; selected blocks can narrow that context. Notion also exposes larger AI surfaces when broader thinking/drafting benefits from space.

Official references reviewed:

- https://www.notion.com/help/notion-agent
- https://www.notion.com/help/guides/everything-you-can-do-with-notion-ai

Useful lesson:

```text
quiet corner presence
+ deictic page/selection context
+ larger surface when task depth increases
```

This maps well to DANTE's bounded World interaction cursor model, while DANTE retains stricter authorization/context-reconstruction boundaries.

### 3.5 Linear Agent

Linear exposes Agent through a small bottom-right entry, keyboard invocation, dedicated chat and contextual use. Deeper Agent work can move into a maximized overlay so it remains connected to the same interaction rather than becoming a disconnected product route.

Official references reviewed:

- https://linear.app/docs/linear-agent
- https://linear.app/changelog/2026-04-23-linear-agent-mcp-support

Useful lesson:

```text
contextual invocation and deep conversation do not need the same footprint
```

## 4. Cross-product synthesis

The strongest common pattern is:

> **AI availability is persistent; AI footprint is not.**

Mature products combine several of:

```text
small invoke affordance
contextual inline invocation
side-by-side conversation
focus/full-surface expansion
explicit confirmation for consequential edits/actions
```

This directly matches DANTE's accepted semantic ladder better than a single permanent chat panel.

DANTE-specific improvement over naive copying:

```text
presentation geometry != conversation identity
World label != authorization
selected UI != automatically authorized AI context
AI output != accepted fact
Proposal != Decision != effect
```

## 5. DANTE workspace pressure test

WF0 freezes viewport-relative workspace insets. Approximate resulting workspace inline widths from the original pressure study were:

| viewport | workspace inline width |
|---:|---:|
| 1856 | 1408 px |
| 1600 | 1152 px |
| 1366 | 984 px |
| 1200 | 864 px |
| 1024 | 737 px |
| 901 | 629 px |
| 900 | 628 px |
| 760 | 488 px |
| 721 | 449 px |
| 720 | 496 px |
| 719 | 495 px |
| 390 | 238 px |

Consequences:

1. A permanently open 320–400 px right pane can work at large desktop widths but is destructive on many ordinary laptop/tablet/narrow workspace allocations.
2. Ongoing conversation constrained to the ~238 px mobile World workspace would be unusably narrow.
3. Narrow/deep DANTE interaction therefore needs route-owned space below the Global Topbar, not merely a smaller desktop sidecar.
4. Split eligibility should derive from actual allocated workspace/container geometry, not duplicated global viewport JS state.

## 6. Alternatives and disposition

### Alternative A — always-open right sidecar

```text
CONTENT | DANTE
```

Strengths:

- conversation continuously visible;
- simple mental model;
- good large-desktop side-by-side inspection.

Material failures:

- violates P0 QUIET;
- makes AI visually co-primary when not useful;
- compresses content below acceptable width;
- encourages `World = dashboard + chatbot` perception;
- poor mobile path.

**Disposition: REJECT as universal model.**

### Alternative B — floating chat window only

```text
CONTENT
        [floating DANTE window]
```

Strengths:

- low initial footprint;
- preserves content layout;
- easy contextual invocation.

Material failures:

- covers content at medium/narrow widths;
- weak for long evidence-rich conversations;
- creates z-index/focus complexity;
- can feel like a foreign support widget rather than a native operating capability.

**Disposition: REJECT as sole model.**

### Alternative C — maximized overlay only

```text
DANTE FOCUS SURFACE
covers World experience while open
```

Strengths:

- excellent conversation width;
- clean constrained/mobile solution;
- good for long/agentic work.

Material failures:

- destroys side-by-side deictic inspection on large screens;
- too disruptive for quick contextual questions;
- hides the World exactly when comparison may be useful.

**Disposition: REJECT as sole model.**

### Alternative D — adaptive hybrid presence

```text
P0
World content + quiet DANTE invoke

P1 / quick P2
compact transient composer / contextual invoke

ongoing conversation, wide workspace
CONTENT | DANTE SIDECAR

ongoing conversation, constrained workspace/mobile
DANTE ROUTE-OWNED FOCUS OVERLAY

user-requested deep work on wide workspace
SIDECAR -> explicit MAXIMIZE -> FOCUS OVERLAY
```

Strengths:

- preserves P0 QUIET;
- keeps DANTE native and one interaction away;
- preserves World visibility for contextual questions when width allows;
- uses route width on mobile/narrow screens;
- supports long conversation without inventing a second disconnected route product;
- consumes the Workspace Platform rather than bypassing it;
- lets presentation adapt without changing conversation identity.

Costs:

- more states than one fixed pane;
- requires disciplined focus restoration and state continuity;
- requires a route-owned overlay seam in addition to workspace-local allocation;
- responsive geometry must not become semantic conversation state.

**Disposition: ACCEPTED.**

## 7. Accepted D0 spatial contract

### D0.1 P0 Quiet presence

DANTE has one small persistent invoke affordance inside the World experience.

```text
location: lower trailing edge of workspace
minimum target: 44x44 CSS px
state: quiet / available / unavailable / truthful busy only
no generated prose
no permanent chat box
no auto-open on World entry
```

The control is an invocation affordance, not an AI output slot and not a copy of the Home AI component.

D1 has now implemented and browser-tested this behavior.

### D0.2 P1 Invoke

Activation opens a compact transient composer without reserving a large layout column.

It may expose bounded current World presentation context, but that context is not authorization.

Empty prompt state must not invent suggestions merely to fill space.

D1 implementation uses a registered non-modal `popover` and explicitly opens the global invoke with:

```text
contextReference: null
```

so a current selection is not silently inherited.

### D0.3 P2 Contextual entry

A selected projection/source may later expose a restrained explicit Ask DANTE action.

Invocation passes only a bounded deliberate context reference.

The user may then ask deictically:

```text
perché?
confronta con prima
aprimi la fonte
continua da qui
```

without the frontend serializing source truth or DOM into chat state.

This remains D4 scope.

### D0.4 Ongoing conversation — wide workspace

Use an internal workspace sidecar only when the actual allocated workspace can preserve a useful main content area.

The final Workspace Platform uses a presentation policy around a 900 px split threshold with bounded main/sidecar minima and actual container measurement.

Important rule:

```text
actual allocated workspace geometry
-> determines whether split sidecar is physically viable
```

No global `window.innerWidth` semantic state should duplicate this.

### D0.5 Constrained workspace / mobile

Below split viability, ongoing conversation uses a **route-owned focus overlay**.

Important ownership:

```text
route-owned focus overlay may cover World workspace
but does not resize/re-own Global Topbar
and does not rewrite frozen WF-G3 workspace geometry
```

This distinction is critical because the Workspace Platform's current `full-screen` slot is workspace-local and is not sufficient at ~238 px mobile workspace width.

D2 owns this route-level seam.

### D0.6 Explicit maximize / restore

On wide screens, long/deep work may be promoted from sidecar to focus overlay through explicit user intent.

Do not automatically take over the full World solely because a response became long.

Promotion/restore must preserve the same logical conversation identity and context binding.

Presentation geometry is not conversation identity.

### D0.7 Insight is not synonymous with chat

```text
conversation != Insight
Insight != ordinary conversation message
Explore != conversation
Proposal != generic assistant text
```

A conversation may produce an Insight, but a validated Insight may use its own registered surface when that improves evidence/readability.

### D0.8 Proposal / confirmation / receipt

P4/P5 remain distinct from generic assistant prose.

Consequential confirmation uses a controlled blocking surface, not an ordinary chat bubble.

Existing Workspace Platform blocking/Escape semantics must be consumed:

```text
required confirmation owns interaction/Escape
-> World may not close underneath it
```

Receipt/result remains distinguishable from Proposal and from canonical/provider/runtime completion axes.

### D0.9 World switch / race behavior

```text
DANTE interaction starts in World A / generation N
user changes World/context generation
late result arrives
-> must not attach to active World B/new generation
```

Workspace generation guards protect frontend presentation commits. Durable future DANTE Run lifetime remains outside mounted React state.

### D0.10 AI unavailable

AI failure must be local:

```text
World content remains usable
DANTE invoke remains predictable
invoking reports truthful unavailable state
no fake answer
no disappearance that looks like lost user data
```

D1 proves this at the entry/composer level.

### D0.11 Focus / accessibility

Required across D1-D7:

- deterministic focus into active composer/conversation surface;
- closing restores focus to exact invoker/logical continuation when mounted;
- sidecar/focus surfaces have clear accessible names/regions;
- ordinary sidecar conversation is not modal and has no focus trap;
- modal/confirmation uses modal semantics only when outside interaction is truly inert;
- Escape obeys workspace/surface precedence;
- >=44 px primary invoke/close targets;
- non-color-only busy/unavailable state;
- reduced motion changes choreography, not state semantics;
- background DANTE updates do not steal focus.

## 8. Archetype stress result

### Music

A user may inspect Continuity and explicitly ask why an item is paused. Wide side-by-side behavior is materially useful; overlay-only is unnecessarily disruptive.

### Travel

A user may begin contextually beside the World, then move into a long itinerary discussion and explicitly maximize. Cross-World retrieval remains Context Builder/governance work, not presentation permission.

### Finance

Sparse first-open remains valid. No fake AI slot before invocation.

### Relationships

Sensitive qualitative context makes automatic AI prose/suggestions especially inappropriate. Quiet explicit invocation and purpose-scoped reconstruction are required.

### Specialist asset context

Future diagnostics may benefit from evidence visible beside DANTE. Sidecar at wide width and focus overlay at constrained width both remain useful.

### Unknown future World

Quiet invoke remains available; DANTE does not infer ontology/membership or invent modules from the label.

## 9. Rejected shortcuts

Do not implement:

```text
always-on chatbot column
Home AI surface copied into World
fixed 360px panel at every width
mobile conversation squeezed inside ~238px workspace
AI prose on first open
random suggested prompts
LLM-selected executable UI
chat history as canonical World truth
selected DOM serialized as DANTE context
surface visibility used as Run lifetime
World navigation cancelling governed backend effects by assumption
```

## 10. Accepted implementation sequence

```text
D1 — quiet invoke + composer shell
     CLOSED FOR SEQUENCING
     code HEAD f17291de32e6bdced20536807b32928ec1be6aea
     CI 33552437179 PASS

D2 — adaptive conversation surface
     NEXT ACTIVE GATE
     wide -> sidecar
     constrained/mobile -> route-owned focus overlay
     explicit maximize/restore

D3 — deterministic pre-backend conversation adapter
     typed message/result distinctions
     cancellation/generation tests
     no fake canonical truth

D4 — contextual selection/deictic invocation
     bounded explicit context references only

D5 — Insight presentation integration
     conversation vs standalone Insight separation

D6 — Proposal / confirmation / receipt presentation
     governed-operation boundary only; no real effect backend

D7 — integrated desktop/laptop/tablet/mobile review
     deferred B1/B2/DANTE visual polish
     user frontend freeze before backend
```

No backend/API/DB/provider/real LLM/tool execution is introduced in D1–D7.

## 11. Final D0 disposition

Accepted direction:

> **D0 ADAPTIVE HYBRID — quiet DANTE invoke, compact non-modal invocation, wide-workspace sidecar, constrained/mobile route-owned focus overlay, explicit maximize/restore, and explicit bounded contextual selection entry.**

This decision is closed unless implementation evidence or new product constraints materially falsify it.

The active next question is not whether D0 is accepted; it is how to implement **D2 route/sidecar presentation continuity** at enterprise quality while preserving frozen World ownership and without pulling D3 conversation semantics forward.
