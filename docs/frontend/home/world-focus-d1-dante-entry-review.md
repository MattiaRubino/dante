# World Focus — D1 Contextual DANTE Entry Review

Status: **CLOSED FOR SEQUENCING — ENGINEERING + AUTOMATED REAL-BROWSER ACCEPTANCE PASS; MANUAL INTEGRATED VISUAL POLISH DEFERRED**

Date: 2026-09-01
Branch: `feature/home-react`
Validated D1 code HEAD: `f17291de32e6bdced20536807b32928ec1be6aea`
Frontend CI: `33552437179` — PASS

## Purpose

D1 materializes the first concrete consumer of the engineering-closed World Workspace Platform:

```text
P0 QUIET
-> explicit DANTE invoke
-> P1 compact composer shell
```

It does not implement conversation, Insight, Proposal, tool execution or backend/model integration.

The accepted spatial direction comes from `world-focus-dante-spatial-presence-review.md`, which already compared current Google Workspace/Gemini, Microsoft 365/Copilot, VS Code/Copilot Chat, Notion Agent and Linear Agent patterns. That broad research is not repeated here.

## Product contract

The World remains useful without DANTE.

DANTE availability is persistent; DANTE footprint is not.

First-open behavior:

```text
World content
+
small quiet DANTE invoke affordance
```

No chat panel opens automatically.
No generated prose appears on first open.
No suggested prompts are invented to fill space.
No permanent column is reserved.

## D1 interaction

### Quiet invoke

The invoke control:

- lives at the lower trailing edge of the World workspace;
- has at least a 44 x 44 CSS px interactive target;
- remains a restrained invocation affordance rather than an AI output slot;
- has an accessible name tied to the current World;
- does not copy the Home AI component;
- stays predictable when DANTE is unavailable.

### Composer shell

Activation opens one finite registered `dante-composer` surface using existing workspace orchestration:

```text
interaction depth: peek
presentation:      popover
origin:            user
```

The popover is non-modal:

```text
main allocation:   unchanged
main interaction:  interactive
```

It does not consume a sidecar column in D1.

The composer contains:

- DANTE identity;
- bounded current World label;
- textarea with explicit accessible label;
- close action;
- send action only as a truthful pre-backend failure path;
- no suggested prompts;
- no conversation transcript.

The World label is a presentation/context hint only. It is not authorization and is not serialized source truth.

## Truthful pre-backend submit behavior

D1 intentionally has no model/runtime backend.

Submitting a non-empty draft therefore produces only a local truthful unavailable state:

```text
request remains in the composer
no fake answer is created
no user text is converted into canonical truth
no conversation/run identity is invented
```

The deterministic conversation adapter belongs to D3.

This degraded submit path proves that UI failure does not erase the user's draft or make the World unusable.

## Context-binding decision

The global quiet invoke opens the composer with:

```text
contextReference: null
```

This is intentional and permanent for D1.

An unrelated/currently selected workspace projection must not silently become DANTE context merely because the user presses the global DANTE invoke.

Explicit deictic context is deferred to D4, where invocation will carry a bounded deliberate reference rather than serialize DOM/source truth.

## Focus and keyboard contract

Implemented behavior:

```text
invoke
-> composer opens
-> textarea receives focus

close / Escape
-> composer closes
-> focus returns to the invoking DANTE control if still mounted
```

The composer is a non-modal dialog/surface:

- no focus trap;
- World remains interactive;
- `aria-modal="false"`;
- background updates may not steal focus.

If DANTE entry is unavailable before opening, invocation opens a truthful unavailable surface and focus moves to its close action rather than to a disabled/nonexistent textarea.

DOM focus ownership deliberately lives in `WorldFocusDanteEntryProvider`, not in `WorldInteractionCursor`. DOM nodes therefore cannot become DANTE context, authorization input or durable Run state.

## Responsive contract

D1 uses the current workspace surface layer and actual allocated container geometry.

The compact composer may become narrow on mobile because it is only a quick invocation surface. This does **not** authorize squeezing ongoing conversation into the mobile workspace.

D2 remains responsible for:

```text
wide workspace -> conversation sidecar
constrained/mobile -> route-owned focus overlay
explicit maximize / restore
```

No viewport-specific JavaScript breakpoint is introduced in D1.

Real Chromium acceptance now verifies the D1 composer remains bounded inside the contracted 390 px World workspace, with no horizontal page overflow and 44 px primary invoke/close targets.

## Surface interaction correction exposed by D1

The first concrete `popover` consumer exposed a real platform bug: a full-workspace overlay wrapper with `pointer-events:auto` makes the main plane physically unclickable even when the allocation model says the surface is non-modal and the main remains interactive.

The correction is presentation-generic:

```text
popover allocation wrapper -> pointer-transparent
actual popover panel        -> pointer-interactive
main plane                  -> remains interactive
```

This behavior is implemented by `WorldFocusSurfaceLayer` for `presentation === 'popover'`; it is not a DANTE-only CSS exception.

The browser acceptance suite verifies computed pointer behavior on both wrapper and composer.

## Security / semantic barriers

```text
World != AI memory
World label != authorization
selected context != authorization
surface visibility != disclosure permission
inert != authorization
composer draft != canonical truth
submit attempt != Run
submit attempt != tool call
submit attempt != effect
```

D1 does not introduce any backend/API/DB/provider/model contract.

## Failure / race behavior

- duplicate invoke while composer is already open does not create a second surface;
- blocking modal/full-focus surface remains authoritative over DANTE entry through the existing blocking-tail barrier;
- the quiet invoke itself becomes inert while a blocking allocation owns the workspace;
- route/World unmount does not attach composer state elsewhere;
- render failure remains surface-local through the existing surface render boundary;
- unavailable submit preserves the draft;
- no late AI result exists in D1 because D1 does not create a Run/model request.

## Implementation files

Concrete D1 implementation:

```text
apps/web/src/features/world-focus/ui/world-focus-dante-entry.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-entry.css
apps/web/src/features/world-focus/ui/world-focus-core-surfaces.tsx
apps/web/src/features/world-focus/ui/world-focus-page.tsx
apps/web/src/features/world-focus/ui/world-focus-surface-layer.tsx
packages/i18n/src/resources/it/world-focus.ts
packages/i18n/src/resources/en/world-focus.ts
```

Automated evidence:

```text
apps/web/src/features/world-focus/ui/world-focus-dante-entry.test.tsx
apps/web/e2e/world-focus-dante-entry.spec.ts
```

The former `world-focus-core-surfaces.ts` was removed after strict CI exposed that it contained JSX under a `.ts` extension; the finite registry now correctly lives in `.tsx`.

## Automated acceptance evidence

Validated D1 code HEAD:

`f17291de32e6bdced20536807b32928ec1be6aea`

Frontend CI:

`33552437179`

Evidence:

```text
Frontend contract drift check             PASS
Home / World Focus format checks          PASS
Lint                                      PASS
Typecheck                                 PASS
Architecture check                        PASS
Generated-source drift                    PASS
Unit tests                                PASS
Production build                          PASS
Diff / repository mutation checks         PASS
Mobile Bundle                             PASS
Chromium Web E2E                          PASS
Firefox frozen Timeline contract          PASS
Frontend CI Gate                          PASS
```

D1-specific unit/component coverage proves:

- first state is quiet; composer absent;
- one invocation creates one registered composer surface;
- global invoke binds `contextReference: null`;
- surface presentation is `popover` and interaction remains interactive;
- wrapper is pointer-transparent;
- textarea receives focus;
- degraded submit preserves draft;
- degraded submit creates no fake response;
- unavailable entry state is truthful and focuses close action;
- explicit close restores focus to exact invoker.

D1-specific Chromium E2E proves:

- no auto-open on `/worlds/music`;
- non-modal composer semantics;
- World main remains interactive;
- real computed pointer transparency outside the composer;
- real computed pointer interactivity on the composer;
- textarea focus;
- truthful unavailable submit + draft preservation;
- Escape closes only the composer and keeps the World route open;
- Escape restores focus to the invoke;
- 390 px containment;
- 44 px invoke/close targets;
- no horizontal page overflow;
- axe has zero detectable violations with composer open at wide and compact widths.

## Closure disposition

The user explicitly delegated closure judgment for this saturated-chat handoff and authorized continuation with “carta bianca / OK”.

Therefore D1 is **CLOSED FOR SEQUENCING** on the following truthful basis:

```text
product contract                    closed
architecture/state ownership        closed
implementation                      closed
strict static gates                 PASS
unit/integration                    PASS
real Chromium functional coverage   PASS
axe wide + compact                  PASS
390 px geometry                     PASS
Firefox frozen regression           PASS
Mobile regression                   PASS
manual assistant visual review      NOT PERFORMED / no browser-view tool
micro/integrated visual polish       DEFERRED to D7/integrated review
```

This closure does not pretend that a human visual inspection occurred. It authorizes D2 sequencing because D1's functional/interaction contract is now deterministic and browser-tested, while visual polish remains intentionally revisitable in the integrated DANTE/World composition review.

## Stop line

D1 does **not** implement:

- conversation history;
- assistant messages;
- streaming;
- real AI availability checks;
- model routing;
- DANTE Run lifetime;
- sidecar conversation;
- route-owned full-focus conversation;
- contextual projection selection;
- Insight;
- Proposal / confirmation / receipt;
- tools or effects.

Those remain later bounded slices from the accepted D0 sequence.

## Next gate

The next authorized bounded slice is:

> **D2 — adaptive conversation surface geometry and presentation ownership.**

D2 must consume the existing Workspace Platform rather than replace it and must prove:

```text
wide allocated workspace -> split sidecar allowed
constrained workspace     -> route-owned focus overlay
explicit maximize/restore
same conversation identity across presentation changes
sidecar does not become modal
focus overlay does not rewrite World macro geometry
Global Topbar remains outside World ownership
no fake messages / no backend / no D3 adapter pulled forward
```

D2 must resolve the route-owned overlay implementation seam carefully: the accepted D0 review explicitly requires the constrained/mobile conversation to use available route space below the Global Topbar rather than being trapped inside the ~238 px mobile World workspace.
