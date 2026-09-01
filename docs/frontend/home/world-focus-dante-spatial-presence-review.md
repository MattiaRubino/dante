# DANTE — World Focus Contextual DANTE Spatial / Presence Review

**Status:** REVERSE ENGINEERING COMPLETE — RECOMMENDATION READY — USER ACCEPTANCE REQUIRED BEFORE PRODUCTION DANTE UI  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

## 1. Scope

This review closes the product/interaction question intentionally left open by WR2, B1 and B2:

> **How should contextual DANTE occupy and interact with the World Focus workspace without turning the World into a chatbot, destroying content density, or creating a second disconnected AI product?**

This is a spatial/presence decision only. It does not reopen Domain, Logical, Physical/DB, World semantics, DANTE Intelligence architecture or the frozen WF0 route/workspace geometry.

The production DANTE World UI remains unauthorized until the user accepts one spatial direction.

## 2. Existing non-negotiable constraints

```text
World != chatbot page
DANTE is native but World must work without AI
P0 QUIET through P5 ACTION/RECEIPT are semantic depths, not geometry
Home AI surface != World contextual DANTE surface
World workspace is the one persistent rectangular application authority
route/topbar/visual-frame/workspace macro geometry remains WF0-frozen
transient overlay may cover workspace but may not reauthor macro geometry
World composition != DANTE context universe
selection/cursor references != authorization
AI output != fact
AI proposal != Decision
Decision != effect
```

## 3. External product reverse engineering

The useful pattern is not that one mature product has "the answer". The useful finding is that mature AI-enabled workspaces increasingly use **multiple spatial modes tied to task depth**, rather than one permanent chat geometry.

### 3.1 Google Workspace / Gemini

Current Google Workspace guidance exposes Gemini through a side panel across apps. In Docs, Google also supports a lower-footprint bottom bar and explicitly lets the user move between bottom bar and side panel. The bottom bar can auto-minimize to clear the document, while the side panel is used when the user wants a larger response display and persistent conversation beside the work.

Relevant official references:

- https://support.google.com/a/users/answer/15146419
- https://support.google.com/docs/answer/13447609

Useful lesson for DANTE:

```text
quiet/minimized entry
!=
expanded persistent conversation
```

A single AI geometry is unnecessary even inside one application surface.

### 3.2 Microsoft 365 / Copilot

Microsoft's 2026 Dynamic Action Button consolidates Copilot invocation into a small corner entry point in Word/Excel/PowerPoint. Activating it opens the agent/chat pane on the right. Word also combines in-canvas Copilot work with the chat pane.

Relevant official references:

- https://support.microsoft.com/en-us/office/foundations-experiences/copilot-dab/the-copilot-dynamic-action-button-in-word-excel-and-powerpoint
- https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word

Useful lesson:

```text
persistent AI availability can be represented by a small invoke control
without permanently reserving a large pane
```

### 3.3 VS Code / Copilot Chat

Current VS Code keeps Chat in the Secondary Side Bar by default for ongoing work, but also supports a chat editor tab when more room is needed, inline chat in the editor/terminal, and Quick Chat for lower-interruption questions.

Relevant official references:

- https://code.visualstudio.com/docs/agents/run/chat-view
- https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet

Useful lesson:

```text
ongoing conversation -> side-by-side surface
quick contextual question -> local/ephemeral surface
deep conversation -> larger dedicated surface
```

The semantic assistant is one capability while presentation depth changes with the task.

### 3.4 Notion Agent

Notion exposes its Agent from a small bottom-corner presence. A chat opened from a page automatically receives current-page context; selected blocks narrow that context. Notion also exposes AI from Search in a full-page view when broader thinking/drafting benefits from more space.

Relevant official references:

- https://www.notion.com/help/notion-agent
- https://www.notion.com/help/guides/everything-you-can-do-with-notion-ai

Useful lesson:

```text
quiet corner presence
+ deictic page/selection context
+ larger surface when task depth increases
```

This is particularly relevant to the WorldInteractionCursor model.

### 3.5 Linear Agent

Linear's 2026 Agent is reachable through a bottom-right entry, `Cmd/Ctrl+J`, dedicated chat, and contextual `@Linear` use inside comments. Linear supports multiple chat threads. An April 2026 interaction update moved Agent chat into a maximized overlay so deeper AI work feels like an extension of the toolbar chat rather than a disconnected route.

Relevant official references:

- https://linear.app/docs/linear-agent
- https://linear.app/changelog/2026-04-23-linear-agent-mcp-support

Useful lesson:

```text
contextual invocation and deep conversation do not need the same footprint
```

A maximized overlay can be preferable when a side pane would compress the primary work too far.

## 4. Cross-product synthesis

The strongest common pattern is:

```text
AI availability is persistent
AI footprint is not
```

Mature products combine several of:

```text
small invoke affordance
contextual inline invocation
side-by-side conversation
focus/full-surface expansion
explicit accept/reject for consequential edits/actions
```

This directly matches DANTE's accepted semantic ladder better than a single permanent chat panel.

## 5. DANTE workspace pressure test

WF0 freezes viewport-relative workspace insets. Approximate resulting workspace inline widths at the current pressure widths are:

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

1. A permanently open 320–400 px right pane is acceptable at large desktop widths but becomes destructive on ordinary laptop/tablet/narrow workspace widths.
2. A chat UI constrained to the 238 px mobile workspace would be unusably narrow.
3. The reserved route-owned overlay layer is therefore necessary for narrow/deep DANTE interaction; mobile cannot be solved by merely shrinking a desktop sidecar.
4. The decision must use **workspace/container width**, not duplicated viewport JS breakpoints.

## 6. Alternatives

### Alternative A — always-open right sidecar

```text
CONTENT | DANTE
```

Strengths:

- conversation continuously visible;
- simple mental model;
- works well for large desktop.

Material failures:

- violates the P0 QUIET product intent;
- permanently makes AI visually co-primary even when not useful;
- compresses B2/future content below acceptable width on many pressure cases;
- encourages "World = dashboard + chatbot" perception;
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
- persistent floating rectangle can feel like a foreign support widget rather than native operating capability.

**Disposition: REJECT as sole model.**

### Alternative C — maximized overlay only

```text
DANTE FOCUS SURFACE
covers World workspace while open
```

Strengths:

- excellent conversation width;
- clean mobile solution;
- good for long/agentic work.

Material failures:

- destroys side-by-side deictic inspection on large screens;
- too disruptive for "perché questo?" / quick context questions;
- hides the World exactly when contextual comparison may be useful.

**Disposition: REJECT as sole model.**

### Alternative D — adaptive hybrid presence

```text
P0
World content + quiet DANTE invoke affordance

P1 / quick P2
compact transient composer / contextual invoke

ongoing conversation, wide workspace
CONTENT | DANTE SIDECAR

ongoing conversation, constrained workspace
DANTE FOCUS OVERLAY

user-requested deep work on wide workspace
SIDECAR -> explicit MAXIMIZE -> FOCUS OVERLAY
```

Strengths:

- preserves P0 QUIET;
- keeps DANTE native and one interaction away;
- preserves World visibility for contextual questions when width allows;
- uses full usable route width on mobile/narrow screens;
- supports long conversation without inventing a second route product;
- maps cleanly to existing `sidecar` and `full-screen` presentation primitives;
- consumes the Workspace Platform already implemented rather than bypassing it.

Costs:

- more states than a single pane;
- requires disciplined focus restoration and state continuity when presentation changes;
- must not let responsive geometry accidentally become semantic conversation state.

**Disposition: RECOMMENDED.**

## 7. Recommended DANTE spatial contract — candidate D0

The recommended direction is Alternative D.

### D0.1 P0 Quiet presence

DANTE has one small, persistent invoke control anchored inside the World experience.

Candidate behavior:

```text
location: lower trailing edge of the workspace
minimum target: 44x44 CSS px
state: quiet / available / unavailable / busy indicator only when truthful
no generated prose
no permanent chat box
no auto-open on World entry
```

The control is an invocation affordance, not an AI output slot.

It must not copy the Home AI component merely because both invoke DANTE.

### D0.2 P1 Invoke

Activation opens a compact transient composer without immediately reserving a large layout column.

The composer may show bounded visible context references such as:

```text
World: Musica
Context: Neon Static
```

but those are frontend hints/references, not claims of authorization.

Empty prompt state must not invent suggested questions merely to fill space. Suggestions are allowed only when deterministic product/application logic has a meaningful reason to surface them.

### D0.3 P2 Contextual entry

A selected projection/source may expose a restrained contextual action such as "Chiedi a DANTE" or an equivalent icon/command.

Invocation passes only a bounded context reference into the current workspace cursor.

The user should be able to continue with deictic language such as:

```text
perché?
confronta con prima
aprimi la fonte
continua da qui
```

without the frontend serializing source reality into chat state.

### D0.4 Ongoing conversation — wide workspace

Use an **internal workspace sidecar** only when its container has enough width to preserve a useful primary-content area.

Candidate rule derived from minimum useful geometry:

```text
primary content minimum     560 px
DANTE sidecar minimum       320 px
gap                         20 px
--------------------------------
minimum split workspace     900 px
```

Candidate sidecar width:

```text
clamp(320px, 34cqi, 400px)
```

Therefore:

```text
workspace container >= 900 px
-> split presentation is allowed

workspace container < 900 px
-> do not squeeze content into a sidecar split
```

Use CSS container-query ownership rather than viewport-width JavaScript.

### D0.5 Constrained workspace / mobile

Below the split threshold, ongoing conversation uses the reserved **route-owned overlay layer**.

Important:

```text
overlay may cover World workspace
but does not resize shell/workspace/visual-frame macro geometry
Global Topbar remains outside World Focus ownership
```

The overlay should use the available route surface below the Topbar rather than being trapped inside the narrow mobile workspace rectangle.

This is the only viable current web path at 390 px, where WF0 leaves about 238 px of workspace inline width.

### D0.6 Explicit maximize

On wide screens, long/deep work may be promoted from sidecar to focus overlay through an explicit user action.

Do not automatically take over the full workspace solely because a response became long.

Presentation promotion must preserve the same conversation/run identity and initiating cursor binding.

### D0.7 Insight is not synonymous with chat

```text
conversation != Insight
Insight != conversation message
Explore != conversation
Proposal != generic assistant text
```

A conversation may produce an Insight, but the validated Insight can be presented through its own registered surface when that improves evidence/readability.

Do not force every DANTE-derived result into chat bubbles.

### D0.8 Proposal / confirmation / receipt

P4/P5 remain inside the active DANTE interaction flow until a governed action needs confirmation.

Consequential confirmation uses a dedicated controlled surface; it is not an ordinary assistant message.

Escape precedence already implemented by the Workspace Platform applies:

```text
confirmation owns Escape while required
-> World may not close underneath it
```

Receipt/result remains distinguishable from proposal and from canonical/provider/runtime completion axes.

### D0.9 World switch / race behavior

```text
DANTE request starts in World A, generation N
user switches World or cursor generation changes
late result arrives
-> never attaches to active World B/new generation
```

The current workspace generation guard handles frontend presentation commits. Future durable DANTE Run lifetime remains outside mounted React state.

### D0.10 AI unavailable

AI failure must be local.

```text
World content remains usable
DANTE invoke location remains predictable
opening/invoking reports truthful unavailable state
no fake answer
no disappearance that looks like lost user data
```

### D0.11 Focus / accessibility

Required:

- deterministic focus into composer when invoked;
- closing restores focus to the exact invoking control/context when still mounted;
- sidecar and overlay have clear accessible names/landmarks;
- focus is not trapped by ordinary sidecar conversation;
- modal/confirmation follows modal focus semantics only when it is actually modal;
- `Escape` obeys workspace surface precedence;
- 44 px minimum touch target for primary invoke/close actions;
- visible non-color busy/unavailable status;
- reduced motion removes spatial transition choreography without changing state semantics;
- no auto-focus stealing on background DANTE updates.

## 8. Archetype stress test

### Music

User sees Continuity and asks "perché questo è in pausa?".

Best behavior:

```text
select/reference item
-> contextual invoke
-> sidecar on wide desktop
-> World content remains visible for comparison
```

Hybrid passes. Overlay-only is unnecessarily disruptive.

### Travel

User asks DANTE to compare Japan planning with affordability and then continues into a long itinerary discussion.

Best behavior:

```text
start contextual beside World when wide
-> explicit maximize for deep multi-step work if useful
-> cross-World retrieval remains backend/governance concern
```

Hybrid passes.

### Finance

Sparse World, user explicitly invokes DANTE to understand a trade-off.

No fake AI slot should be present before invocation. Hybrid P0 quiet passes.

### Relationships

Potentially sensitive sparse context. Persistent AI prose or automatic suggestions would be especially intrusive. Quiet explicit invocation and purpose-scoped reconstruction are required.

Hybrid passes.

### Vehicle / specialist asset context

A future diagnostic projection may need evidence visible while DANTE explains it. Wide side-by-side mode is materially useful; narrow overlay remains necessary.

Hybrid passes.

### Unknown future World

No specific World renderer can be assumed. Quiet invoke remains available; DANTE does not infer membership or invent modules merely from the label.

Hybrid passes.

## 9. Rejected shortcuts

Do not implement:

```text
always-on chatbot column
Home AI surface copied into World
fixed 360px panel at every width
mobile 238px chat squeezed inside workspace
AI prose on first open
random suggested prompts for visual fullness
LLM-selected UI components
chat history stored as canonical World truth
selected DOM serialized as DANTE context
sidecar visibility used as Run lifetime
World switch cancelling governed backend effects
```

## 10. Implementation sequence after user acceptance

If candidate D0 is accepted, implementation should proceed in bounded slices:

```text
D1 — quiet invoke + composer shell
     focus/keyboard/a11y + AI-unavailable local state

D2 — adaptive conversation surface
     >=900cqi split sidecar
     <900cqi route overlay
     explicit maximize/restore

D3 — deterministic pre-backend conversation adapter
     typed message/result distinctions
     no fake canonical truth
     cancellation/generation tests

D4 — contextual selection/deictic invocation
     bounded context references only

D5 — Insight presentation integration
     conversation vs standalone Insight separation

D6 — Proposal / confirmation / receipt presentation
     governed-operation boundary only; no real effect backend yet

D7 — integrated desktop/laptop/tablet/mobile visual review
     then user acceptance/freeze
```

No backend/API/DB/provider/real LLM/tool execution is introduced in D1–D7.

## 11. Decision requested

Recommended direction:

> **D0 ADAPTIVE HYBRID — quiet DANTE invoke, compact invocation, wide-workspace sidecar, constrained/mobile route overlay, explicit maximize, contextual selection entry.**

This recommendation is ready for user approval. No production DANTE World UI should be written until that approval is explicit.
