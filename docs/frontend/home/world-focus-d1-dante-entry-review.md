# World Focus — D1 Contextual DANTE Entry Review

Status: **IMPLEMENTATION AUTHORIZED — PRE-BACKEND**

Date: 2026-09-01

## Purpose

D1 materializes the first concrete consumer of the now automated-PASS World Workspace Platform:

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

It must not consume a sidecar column in D1.

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

This degraded submit path exists to prove that UI failure does not erase the user's draft or make the World unusable.

## Focus and keyboard contract

Required:

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
- no `aria-modal=true`;
- background updates may not steal focus.

If DANTE entry is unavailable before opening, invocation opens a truthful unavailable surface and focus moves to its close action rather than to a disabled/nonexistent textarea.

## Responsive contract

D1 uses the current workspace surface layer and actual allocated container geometry.

The compact composer may become narrow on mobile because it is only a quick invocation surface. This does **not** authorize squeezing ongoing conversation into the mobile workspace.

D2 remains responsible for:

```text
wide workspace -> conversation sidecar
constrained/mobile -> route-owned focus overlay
```

No viewport-specific JavaScript breakpoint is introduced in D1.

## Surface interaction correction exposed by D1

A non-modal popover wrapper must not intercept the entire workspace merely because its allocation slot is named `overlay`.

Therefore:

```text
popover overlay wrapper -> pointer-transparent outside actual panel
actual composer panel    -> pointer-interactive
main plane               -> remains interactive
```

This is a real platform behavior required by the first concrete popover consumer, not speculative framework work.

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
- route/World unmount does not attach composer state elsewhere;
- render failure remains surface-local through the existing surface render boundary;
- unavailable submit preserves the draft.

## Automated acceptance target

D1 must prove:

- quiet control absent from composition ranking and present only as workspace affordance;
- no auto-open;
- single composer surface;
- non-modal main remains interactive;
- textarea autofocus;
- close + Escape focus restoration;
- unavailable state has no fake response;
- draft preservation after unavailable submit;
- 44 px target;
- 390 px containment / no horizontal page overflow;
- existing World/Timeline/browser gates remain green.

## Stop line

D1 does **not** implement:

- conversation history;
- assistant messages;
- streaming;
- real AI availability checks;
- model routing;
- DANTE Run lifetime;
- sidecar conversation;
- full-focus conversation;
- contextual projection selection;
- Insight;
- Proposal / confirmation / receipt;
- tools or effects.

Those remain later bounded slices from the accepted D0 sequence.
