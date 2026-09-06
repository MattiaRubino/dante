# DANTE — World Focus D3 Deterministic Conversation Adapter Review

**Status:** D3 CLOSED / VALIDATED — D4 READ-ONLY PREFLIGHT NEXT  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`

## 1. Scope and disposition

D3 materializes the deterministic **pre-backend** conversation adapter for World Focus on top of the already-closed D1 entry/composer and D2 adaptive conversation surface.

D3 does not create a chatbot framework, provider integration, durable Run store, backend contract or new Workspace/surface engine. It owns only the mounted frontend conversation bridge, typed local request/result boundary, deterministic fixture/runtime seam, cancellation/latest-only lifecycle and truthful transcript presentation needed to make the accepted D0–D2 interaction executable before backend integration.

The closed path is:

```text
D1 quiet invoke / compact composer
-> explicit user submit
-> atomic handoff to the existing `dante:conversation` surface
-> D3 mounted conversation state + typed local request
-> deterministic pre-backend reader
-> correlated typed local result | truthful unavailable/error/cancelled/superseded
-> same D2 surface identity through sidecar <-> route focus
```

Permanent separations proven by this slice:

```text
user input != assistant output
assistant output != canonical fact
conversation state != World canonical state
presentation geometry != conversation identity
mounted frontend transcript != future durable DANTE Run
cancel / abort != semantic success
late result from World/generation N != attachable to a newer generation
```

## 2. Scope anchor

```text
PRE-SCOPE  57520cf0570bc2be875e7140d066e45ddd9080d5
CODE/TEST  59c70af6005ee87918db7fe152c043699726e78c
CI         33963858340 / run #1009 PASS
```

Final code/test compare from PRE-SCOPE:

```text
status              ahead
ahead_by            23
behind_by           0
merge-base          == PRE-SCOPE
net code/test/i18n  14 paths
```

No Workspace allocator/model substrate, AppShell, Timeline, Access/Auth, generated route tree, backend/API/DB/Alembic, provider/LLM or persistence path changed.

## 3. Typed pre-backend boundary

D3 introduces a bounded application boundary instead of importing a provider DTO or free-form chat object.

The request is correlated to the mounted World interaction with explicit finite fields including:

```text
schema version
requestId
worldId
workspace generation
transient user input / bounded local history
locale
AbortSignal at the reader seam
```

The validated ready result is correlated back to the exact request and carries only the finite local result classes:

```text
answer
explanation
```

`unavailable` remains a truthful non-output outcome rather than a fabricated answer.

The validator fails closed on malformed or semantically widened results, including unexpected extra fields and correlation mismatches for request, World or generation. D3 does not serialize DOM payloads, selection payloads, provider metadata, confidence scores, authorization state, canonical facts, Insights, Proposals, Decisions or effects into the conversation result.

## 4. Deterministic fixture and runtime seam

The pre-backend runtime is deliberately replaceable and presentation-independent:

```text
world-focus-dante-conversation.ts
-> typed request/result contract + validation + coordinator semantics

world-focus-dante-conversation-fixture-adapter.ts
-> deterministic local fixture adapter

world-focus-dante-conversation-runtime.ts
-> current pre-backend runtime seam
```

The current fixture answer explicitly states that no model or external source was queried. This is test/dev product truth, not a fake provider response.

D3 therefore proves the frontend lifecycle while leaving the future backend/provider implementation free to replace the reader behind the same semantic boundary after M7.

## 5. Conversation ownership and atomic handoff

D3 reuses existing owners:

```text
WorldFocusWorkspaceHost
-> remains the one transient surface-stack owner

D1 WorldFocusDanteEntryProvider
-> still owns quiet invoke/composer entry state

D2 `dante:conversation` surface
-> remains the one ongoing conversation surface identity

D3 WorldFocusDanteConversationProvider
-> owns only mounted transcript/request lifecycle for that active World session
```

On submit, D1 does not close the composer and later open a disconnected conversation. The transition replaces the composer surface with `dante:conversation` through the existing guarded Workspace path, preserving one interaction rather than briefly creating two competing surfaces.

While the conversation exists, the DANTE invoke is occupied/disabled and cannot open a second composer beside it.

No second reducer, chat URL, Workspace host or surface stack was introduced.

## 6. Mounted transcript and follow-up behavior

D3 materializes a local transcript with explicit role/result distinctions:

```text
user turn
assistant local output
```

A successful first turn preserves the submitted user input and appends exactly one validated assistant output. A second follow-up runs through the same coordinator and remains on the same `dante:conversation` surface identity.

This transcript is mounted frontend state only:

```text
NO localStorage
NO cross-device persistence
NO server persistence
NO canonical World mutation
NO durable DANTE Run claim
```

Assistant output is displayable conversation output, not accepted/canonical fact.

## 7. Cancellation, latest-only and generation law

Every request has an internal cancellation lifecycle.

D3 proves:

```text
pending -> cancel
-> AbortSignal aborts
-> user turn remains visible
-> no assistant output is fabricated
-> a late completion is ignored

pending -> Workspace generation changes
-> request is superseded/aborted
-> truthful superseded state is shown
-> old result cannot attach to the new generation
```

Only the currently authoritative request/generation may commit a result. Cancellation and supersession are therefore control outcomes, not semantic answers.

The generation-change effect aborts immediately; UI publication of the superseded state is scheduled without weakening the cancellation guarantee or violating React lifecycle rules.

## 8. D1/D2 focus and presentation integration

D3 preserves D2's core law:

```text
presentation geometry != conversation identity
```

Wide viable workspace:

```text
`dante:conversation` -> non-modal sidecar
```

Constrained/mobile workspace:

```text
same `dante:conversation` -> route-owned focus surface
```

Explicit maximize/restore keeps the same logical surface and transcript.

D3 additionally closes the exact entry/exit focus law that D2 intentionally left open:

```text
composer -> conversation handoff
-> DO NOT restore focus to the D1 invoke

actual conversation close / Escape
-> restore focus to the exact original DANTE invoker
-> keep the World route open
```

A hostile unit test exposed a real React identity problem: the DANTE invoke was originally rendered inside D2's keyed `idle/active` presentation session, so the DOM button was remounted when the conversation session changed and exact-invoker focus could not be guaranteed.

The production fix moved stable invokes outside the keyed D2 presentation session while keeping the surface layers inside it. No Workspace or D2 allocator contract was reopened.

## 9. Responsive and accessibility closure

Browser pressure proves:

```text
1600px wide conversation -> sidecar
390px compact conversation -> route-owned focus
same surface identity across maximize / restore
390px route conversation wider than the narrow World workspace
World inert only through the existing D2 explicit route-focus law
no document horizontal overflow
compact close target >= 44px
axe A/AA automated scan passes at wide and compact conversation states
Escape closes conversation before the World
exact invoker focus returns after real conversation close
```

The compact path does not introduce a D3 viewport breakpoint or geometry fork. It consumes D2's existing measured Workspace allocation and route-focus presentation.

Automated browser coverage is not human visual acceptance.

## 10. RED / falsification history

D3 was developed RED-first and useful failures were kept as evidence.

Initial RED established that the existing product lacked two behaviors:

```text
composer submit did not hand off into an ongoing conversation
an existing conversation did not yet occupy/block a second DANTE composer invocation
```

Later CI failures exposed implementation/test weaknesses without weakening the contract:

### Static harness failures

Lint/typecheck caught:

```text
require-await test readers
unused presentation import
React effect-driven synchronous UI state publication
callback-assignment narrowing in tests
exactOptionalPropertyTypes misuse of optional reader props
```

Repairs were bounded to root causes; production semantics were not widened.

### Exact focus failure

One unit failure found the real DANTE-invoker DOM remount described above. Production structure was corrected instead of weakening the focus assertion.

### Browser locator false negative

A browser assertion used Playwright's default partial accessible-name matching:

```text
name: "DANTE"
```

which also matched:

```text
"Conversazione con DANTE"
```

The evidence already showed the handoff was correct. The E2E was fixed to use exact dialog-name matching rather than altering product behavior.

## 11. Final green

Final CI `33963858340` / run `#1009` on `59c70af6005ee87918db7fe152c043699726e78c`:

```text
Frontend pre-production contracts PASS
World Focus pre-production contracts PASS
Format active Home workstreams PASS
Lint PASS
Typecheck PASS
Architecture PASS
Generated-source drift PASS
Unit tests PASS
Production build PASS
Diff check PASS
Repository mutation check PASS
Mobile Bundle PASS
Chromium Web E2E PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

Measured suite:

```text
84 / 84 web test files
410 / 410 web unit tests
311 modules / 963 dependencies / 0 architecture violations
```

## 12. Net changed code/test/i18n paths

```text
apps/web/e2e/world-focus-dante-conversation.spec.ts
apps/web/e2e/world-focus-dante-entry.spec.ts
apps/web/src/features/world-focus/application/world-focus-dante-conversation-fixture-adapter.ts
apps/web/src/features/world-focus/application/world-focus-dante-conversation-runtime.ts
apps/web/src/features/world-focus/application/world-focus-dante-conversation.test.ts
apps/web/src/features/world-focus/application/world-focus-dante-conversation.ts
apps/web/src/features/world-focus/ui/world-focus-dante-conversation-context.test.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-conversation-context.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-conversation.css
apps/web/src/features/world-focus/ui/world-focus-dante-conversation.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-entry.tsx
apps/web/src/features/world-focus/ui/world-focus-page.tsx
packages/i18n/src/resources/en/world-focus.ts
packages/i18n/src/resources/it/world-focus.ts
```

## 13. Explicit non-effects

D3 does not materialize or change:

```text
D4 contextual/deictic reference widening
D5 Insight semantics/presentation
D6 Proposal / confirmation / receipt / Decision / effect semantics
backend/API/DB/Alembic
provider/LLM execution
AuthZ
canonical World/Domain truth
persistent/cross-device transcript
Workspace allocator or surface model ownership
AppShell / Global Topbar ownership
Timeline
Access/Auth
WF0 / WF-G3 macro geometry
```

## 14. Closure disposition

> **D3 DETERMINISTIC PRE-BACKEND CONVERSATION ADAPTER — CLOSED / VALIDATED.**

The next sequential owner is:

> **D4 CONTEXTUAL / DEICTIC INVOCATION — READ-ONLY PREFLIGHT NEXT.**

D4 must start from live code/authority inspection and an exact bounded RED-first gate. It must preserve selection/context as a reference input rather than authorization or canonical truth, and it must not pull D5 Insight or D6 Proposal/Decision/effect semantics forward.

Human/manual visual acceptance remains **NOT PERFORMED**. Automated CI/browser green is not a substitute for that review.
