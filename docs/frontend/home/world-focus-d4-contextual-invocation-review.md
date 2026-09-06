# DANTE — World Focus D4 Contextual / Deictic Invocation Review

**Status:** D4 CLOSED / VALIDATED  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`

This review is the durable closure authority for M4 / D4. It records the exact pre-scope, RED proof, bounded implementation, hostile coverage and scope compare. It does not claim backend/provider integration or human visual acceptance.

## 1. Closure anchors

```text
PRE-SCOPE  c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
FIRST RED  d017b17aec4b690a26781a88a17a372b0d670411
VALID RED  1cbcc27bf19c91e195dd1f0f4a5c57915facb432
RED CI     33966295853 / run #1030 EXPECTED FAILURE
APP        20a24c89090a8e7ca09f9aadc4ddbe4b15af9b0c
UI         95dcee59b666a8c5cda2b34587c438e46e038aee
LINT FIX   ccb6015ef428b5521a23ee286b0a7a08d606f771
HARDENING  e8ab022b9b00b958235ac7d09e757b45227a4356
FINAL CI   33967719861 / run #1038 PASS
```

Final code/test baseline:

```text
87 / 87 web test files
422 / 422 web unit tests
317 modules / 1021 dependencies / 0 architecture violations
Frontend + World Focus contracts PASS
Lint / Typecheck / Generated PASS
Production build PASS
Diff / repository mutation PASS
Mobile Bundle PASS
Chromium Web E2E PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

## 2. RED proof

The first RED was test-only. Mechanical lint/type narrowing corrections were made without changing the behavioral expectation until the RED reached unit execution cleanly.

The valid RED proved exactly two missing capabilities:

```text
1. the D3 request did not expose explicit `contextReferences: null`
2. live Continuity had no explicit `Chiedi a DANTE: Continua da qui` entry
```

All contracts, lint, typecheck, architecture and generated checks were green before the unit failure. The D1 guard that selected Workspace context must not become implicit DANTE context remained green.

Result:

```text
409 / 411 web unit tests PASS
2 / 411 FAIL exactly for the intended D4 gap
```

The RED contract was not weakened.

## 3. Product behavior materialized

D4 adds explicit contextual/deictic entry into the existing D1 composer and D3 conversation. It does not create another chatbot surface or state engine.

Finite live intents:

```text
Continuity -> continue    -> “Continua da qui”
Attention  -> why         -> “Perché?”
Comparison -> compare     -> “Confronta”
Evidence   -> open-source -> “Apri fonte”
```

Only an explicit contextual action carries references. The global DANTE invoke remains:

```text
contextReferences: null
```

even when the Workspace has a current selection.

## 4. Bounded context mapping

D4 owns a finite application mapping layer over existing semantic references.

Admitted context is only a normalized `WorldFocusContextReferenceSet`:

```text
primary
supporting[]
```

Mapping laws:

```text
Attention
-> matter primary
-> optional resolution supporting

Continuity
-> thread primary
-> checkpoint supporting
-> optional continuation supporting

Comparison
-> complete bounded subject set
-> optional basis
-> fail closed if the complete semantic comparison cannot fit the bounded context policy

Evidence
-> one actual Evidence reference
```

D4 does not serialize arbitrary DOM/component state, display payload, reason codes, authorization, disclosure state, provider metadata or model-specific bags into the conversation request.

Duplicate or invalid semantic coordinates fail closed.

## 5. Composer lifecycle

A contextual action invokes the existing D1 composer with:

```text
editable seeded prompt
finite context reference set
worldId
workspaceGeneration
exact invoker DOM element for focus restoration
```

Opening/closing a surface does not increment Workspace generation. Generation changes only when the Workspace context set changes, so a contextual composer does not stale itself merely by opening.

Before submit:

```text
if contextual world/generation still matches
-> hand off to existing D3 conversation

if world/generation changed
-> do not send
-> preserve edited draft
-> keep composer open
-> focus textarea
-> show truthful stale-context message
```

## 6. Conversation lifecycle

The existing `dante:conversation` remains the one mounted conversation identity.

For a valid contextual conversation:

```text
initial request carries exact bounded context set
follow-up carries the same context set
same D2 sidecar/route presentation behavior remains authoritative
```

If Workspace generation changes after a contextual conversation has settled:

```text
context session -> superseded
stale follow-up -> rejected
old context -> never silently reused
```

Pending D3 requests retain their existing abort/supersession correlation protection.

Composer -> conversation handoff does not restore focus prematurely. Actual composer close or conversation close returns focus to the exact contextual invoker when it remains mounted; the established global invoke is only a safe fallback.

## 7. Renderer integration and semantic separation

D4 integrates only into existing display-safe renderers:

```text
Continuity
Attention
Comparison
Evidence/History
```

Critical non-collapse proven by test:

```text
Evidence != Provenance != Integrity != History
```

Only the actual Evidence group receives `Apri fonte`. Provenance, integrity attestation and history receive no source-opening D4 action.

Comparison receives one complete comparison-context action rather than misleading partial per-subject contextualization.

## 8. Accessibility / responsive / browser pressure

Hostile unit coverage proves:

```text
explicit seed is editable
context reference is bound only by explicit contextual invocation
stale-before-submit preserves draft
exact contextual invoker focus return
context survives valid follow-up
context invalidates on generation change
Attention / Comparison finite actions exist
Evidence-only source action law holds
```

Real Chromium E2E uses the actual `/worlds/music` Continuity projection rather than a browser-only fake fixture.

Pressure:

```text
1600 x 900
390 x 844
```

Proved:

```text
real Continuity -> contextual composer -> same D3 conversation
seeded prompt editable
wide conversation -> existing sidecar
390 conversation -> existing route-owned focus
contextual action target >= 44 x 44
no document horizontal overflow at 390
exact contextual invoker focus after close
World route remains open
automated axe: no detected violations in new contextual entry/composer state
```

Existing D3 E2E remains green and continues to prove its own wide/compact conversation geometry and accessibility contract.

## 9. Scope compare

Exact code/test compare:

```text
base        c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
head        e8ab022b9b00b958235ac7d09e757b45227a4356
status      ahead
ahead_by    9
behind_by   0
merge-base  == base
net paths   19
```

The 19 net paths are exclusively D4 application/UI/tests/E2E/i18n under World Focus plus the existing D3 request/conversation owners required to carry the bounded context.

Explicitly unchanged:

```text
Workspace reducer / allocator policy
AppShell / GlobalTopbar ownership
Timeline
Access / Auth / AuthZ
WF0 / WF-G3 macro structure
Generated route tree
backend / API / DB / Alembic
provider / LLM integration
durable persistence
D5 Insight semantics
D6 Proposal / Decision / effect semantics
```

## 10. What D4 does not mean

D4 does **not** prove that a reference is available, fresh, disclosable or authorized. It only carries an explicit bounded semantic coordinate into the mounted pre-backend conversation boundary.

Permanent distinctions remain:

```text
context reference != canonical truth
selected UI/context != authorization
reference exists != payload available != current != disclosable != fresh
assistant output != accepted fact
conversation message != Insight
Insight != Proposal != Decision != effect
```

There is still no provider/LLM call in this slice.

## 11. Next sequence

```text
D4 contextual/deictic invocation       CLOSED / VALIDATED
D5 Insight presentation integration    NEXT / NOT STARTED
D6 Proposal/confirmation/receipt       BLOCKED BY D5
M5 contrasting complete Worlds         BLOCKED BY M4
M6 integrated visual/a11y/perf         BLOCKED BY M5
M7 pre-backend frontend freeze         BLOCKED BY M6
BACKEND                                BLOCKED UNTIL M7
```

D5 requires a fresh read-only preflight and a new exact write gate. It must preserve `conversation message != Insight` and must not pull D6 or backend/provider semantics forward.

## 12. Human visual status

Automated browser and axe coverage are green. Human/manual visual acceptance was **NOT PERFORMED** and must not be inferred from CI.
