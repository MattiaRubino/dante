# DANTE — World Focus M4 Final Hostile Closure Review

**Status:** M4 CLOSED / VALIDATED — FINAL HOSTILE CLOSURE PASS  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`  
**Final hostile test HEAD:** `1b8ae1a3d953d85dcc14d513e512428d1f268c8d`

## 1. Closure statement

M4 is closed only after completing D2–D6 **and** falsifying the owner boundaries that connect contextual invocation, conversation, Insight and governed Proposal/Decision/Receipt semantics.

The hostile pass found three real trust leaks. Each was first proven RED, then fixed by routing data through the existing semantic owner rather than by adding a new semantic layer.

Final owner chain:

```text
D4 owns bounded contextual reference set
  ↓
D3 owns the current contextual conversation and assistant messages
  ↓
D5 owns the validated current Insight
  ↓
D6 owns Proposal -> Confirmation -> local Decision -> local Receipt
```

Permanent M4 sequencing law:

```text
selected Workspace state != DANTE context
caller-supplied reference set != D4-owned context
conversation surface exists != arbitrary object is a D3 message
assistant prose != validated Insight
Insight surface exists != arbitrary object is the D5 Insight
Insight != Proposal
Proposal != Decision
Decision != effect
confirmed != executed
Receipt != canonical/provider/runtime completion
```

## 2. Hostile finding A — D5 -> D6 exact Insight ownership

### RED

```text
HEAD 775281b8bdca5dd5cccb63be5ecb6d9ebabd5b2d
CI   33985837951 / run #1066 EXPECTED FAILURE
```

Finding:

> While a valid D5 Insight surface existed, D6 accepted a caller-supplied different same-generation Insight object. World/generation/surface checks were not enough to prove exact D5 ownership.

The forged object used a different Insight id, semantic kind, text and basis while retaining the same World/generation.

### Fix

D6 no longer accepts an Insight object from the caller:

```text
requestProposal(insight) -> removed
requestProposal()        -> derives exact current D5-owned Insight
```

D6 derives source Insight identity, semantic fields and basis exclusively from the D5 owner.

### GREEN

```text
HEAD 929c5ad7a056ff172a915e5070e7d72c936e692d
CI   33986493932 / run #1071 PASS
```

The retained hostile test also calls the zero-argument function through a runtime cast and supplies a forged extra argument. The request still uses only the D5-owned Insight.

## 3. Hostile finding B — D3 -> D5 exact assistant-message ownership

### RED

```text
HEAD bf6caef751505d35cbfd694ce6f1d532409517f3
CI   33987041073 / run #1076 EXPECTED FAILURE
```

Finding:

> D5 could receive a caller-supplied assistant-message-shaped object while a valid contextual D3 conversation existed. The source was correlated by surrounding World/generation state but was not proven to be a message actually owned by D3.

The forged source used a different message id, result class and text inside the same current World/generation.

### Fix

The caller no longer supplies message semantic content to D5. It supplies only stable message identity, and D5 resolves the current assistant message from the D3 conversation owner before materializing an Insight request.

Required ownership now includes:

```text
message id exists in current D3 owner
message role == assistant
current World/generation/session remains valid
D5 derives resultClass/text from that owned message
```

### GREEN

```text
HEAD e8b836f49ddb85a95e0ba6b9472b56f3f45d83eb
CI   33987633070 / run #1080 PASS
```

## 4. Hostile finding C — D4 -> D3 exact contextual-reference ownership

### RED

```text
HEAD 8dd3572652bde94778ee230cf80437fc8e22a1b8
CI   33988617249 / run #1085 EXPECTED FAILURE
```

Finding:

> The D3 composer handoff could accept a caller-supplied different but structurally valid same-generation context-reference set instead of deriving the semantic seed from the active D4 owner.

This proved again that:

```text
valid shape + same World/generation != owned contextual truth
```

### Fix

D3 no longer accepts semantic context from the composer caller. The conversation handoff derives the bounded context seed exclusively from the D4 owner.

```text
beginFromComposer(callerContext) -> removed
beginFromComposer()              -> derives D4-owned context
```

Global invocation still resolves to explicit context-free behavior rather than inheriting Workspace selection.

### GREEN

```text
HEAD eccdc4d986a4880e9e45766900cb833b665d8cea
CI   33989942572 / run #1086 PASS
```

## 5. Final hostile lifecycle matrix

After the three owner-boundary findings were fixed, the final M4 hostile test was extended as a lifecycle matrix rather than duplicating the dedicated trust-boundary tests.

Final hostile test head:

```text
HEAD 1b8ae1a3d953d85dcc14d513e512428d1f268c8d
CI   33990483780 / run #1087 PASS
```

The matrix proves the following combined invariants:

```text
fake Insight surface != validated D5 ownership
no Proposal -> Decision skip
no Decision without Confirmation
stale materialized Proposal invalidated
stale Confirmation invalidated
stale Receipt invalidated
stale decision rejected
receipt has exact local-decision truth shape
receipt does not claim effect execution
receipt does not claim authorization
receipt does not claim provider/runtime/canonical completion
forged D5 Insight runtime argument ignored
D4 -> D3 exact context ownership
D3 -> D5 exact message ownership
D5 -> D6 exact Insight ownership
global/context-free DANTE cannot reach Insight/Proposal
D5 adapter cannot widen context basis
D6 adapter cannot widen Insight basis
Confirmation blocks Workspace interaction
Confirmation survives Escape
```

The same final SHA passed the complete frontend validation stack:

```text
Quality PASS
Mobile Bundle PASS
Chromium Web E2E PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

## 6. Why these findings matter

All three leaks had the same structural shape:

```text
correct surrounding owner exists
+
caller can still inject a same-generation object
=
sequencing is not actually owned
```

The fixes therefore follow one consistent architecture rule:

```text
adversarial RED
-> fix the existing owner seam
-> derive semantic source from owner
-> do not add a new semantic layer
```

This is the same falsification discipline used in earlier World Focus milestones for stale route handoff, cache/disclosure reuse and non-cooperative cancellation.

## 7. Closed M4 result

```text
D2 adaptive conversation surface        CLOSED / VALIDATED
D3 deterministic conversation adapter   CLOSED / VALIDATED
D4 contextual/deictic invocation        CLOSED / VALIDATED
D5 Insight presentation integration     CLOSED / VALIDATED
D6 Proposal/confirmation/receipt        CLOSED / VALIDATED
M4 final hostile closure                CLOSED / PASS
M4 Contextual DANTE                     CLOSED / VALIDATED
```

M4 now provides a bounded frontend-only progression:

```text
quiet/contextual invoke
-> deterministic mounted conversation
-> explicit bounded context
-> standalone validated Insight
-> Proposal
-> required Confirmation
-> local Decision
-> truthful local Receipt
```

without collapsing World, authorization, canonical Domain truth, backend persistence, provider execution or real effect execution into frontend state.

## 8. Visual truth

Automated structural/browser validation is green:

```text
wide/compact responsive pressure PASS
Chromium PASS
Firefox frozen Timeline PASS
automated accessibility checks PASS
```

This does not constitute human visual acceptance.

**human/manual visual acceptance: NOT PERFORMED**

The accepted sequence remains:

```text
M4 complete -> structural visual check only
M5 complete -> serious product/visual review
M6 -> integrated visual/responsive/motion/a11y/performance refinement
```

## 9. Explicit exclusions retained

```text
NO backend World implementation
NO API/DB/Alembic/AuthZ integration
NO provider/LLM execution
NO durable DANTE Run persistence
NO real effect execution
NO provider ACK == canonical completion
NO client World/context == authorization
NO page-per-World or new generic semantic root
NO fake human visual acceptance
```

## 10. Sequencing result

**M4 is CLOSED / VALIDATED. M5 is NOT STARTED.**

Because `feature/home-react` is now a long-lived, heavily divergent branch, M5 must not begin here before integration reconciliation.

Immediate next sequence:

```text
freeze exact M4 closure SHA
-> fetch current protected main
-> inspect divergence
-> reconcile main INTO feature/home-react under authority-based conflict ownership
-> full repository QA
-> documentation lifecycle cleanup
-> PR to protected main
-> merge commit only
-> protected-main readback
-> archive/delete feature/home-react only after verified merge
-> create a fresh bounded M5 branch from integrated main
```
