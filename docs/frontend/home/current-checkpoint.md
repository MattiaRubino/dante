# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M3 CLOSED / VALIDATED — M4 ACTIVE / D2–D4 CLOSED / D5 NEXT  
**Date:** 2026-09-05  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Current sequencing authority lives here and in `world-focus-current-checkpoint.md`; older `NEXT` prose is historical unless explicitly adopted again.

## 1. Branch workstreams

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

Permanent distinctions:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

## 2. Live World Focus sequence

```text
WF0 / WF-G3                                FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                    CLOSED AS RECORDED
Workspace Platform                         ENGINEERING CLOSED
D0                                         ACCEPTED
D1                                         CLOSED FOR SEQUENCING
WS0–WS8                                    CLOSED
POST-WS8 HYGIENE                           CLOSED / APPLIED
PRE-M0 FALSIFICATION                       CLOSED / PASS
M0                                         CLOSED
M1                                         CLOSED / VALIDATED
POST-M1 SAFETY                             CLOSED / PASS
M2                                         CLOSED / VALIDATED
M2 FINAL CLOSURE                           CLOSED / PASS
M3                                         CLOSED / VALIDATED
M3-1 / M3-2 / M3-3 / M3-4                CLOSED / VALIDATED
M3 final hostile closure                   CLOSED / PASS
M4 Contextual DANTE / D2–D6               ACTIVE
D2 adaptive conversation surface           CLOSED / VALIDATED
D3 deterministic conversation adapter      CLOSED / VALIDATED
D4 contextual/deictic invocation           CLOSED / VALIDATED
D5 Insight presentation integration        NEXT / NOT STARTED
D6 Proposal/confirmation/receipt           BLOCKED BY D5
M5 complete contrasting Worlds             BLOCKED BY M4
M6 integrated visual/a11y/performance      BLOCKED BY M5
M7 pre-backend frontend freeze              BLOCKED BY M6
BACKEND                                    BLOCKED UNTIL M7
human/manual visual review                  NOT PERFORMED
```

## 3. Current evidence anchors

```text
M3 final hostile
HEAD d9c30a3c6148469b347754eab07dc2ade9be4c52
CI   33951509083 / run #944 PASS
80 / 80 web test files; 391 / 391 web unit tests
300 modules / 899 dependencies / 0 violations

D2 adaptive conversation surface
PRE-SCOPE 0a0a43ac06f93d986674f8521e521dcc05ea2c1e
CODE/TEST  7b787766be83096e82eab1ac116b2704fae5f202
CI         33958677991 / run #969 PASS
82 / 82 web test files; 399 / 399 web unit tests
305 modules / 929 dependencies / 0 violations

D3 deterministic conversation adapter
PRE-SCOPE 57520cf0570bc2be875e7140d066e45ddd9080d5
CODE/TEST  59c70af6005ee87918db7fe152c043699726e78c
CI         33963858340 / run #1009 PASS
84 / 84 web test files; 410 / 410 web unit tests
311 modules / 963 dependencies / 0 violations

D4 contextual/deictic invocation
PRE-SCOPE c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
VALID RED 1cbcc27bf19c91e195dd1f0f4a5c57915facb432
RED CI    33966295853 / run #1030 EXPECTED FAILURE
CODE/TEST e8ab022b9b00b958235ac7d09e757b45227a4356
CI        33967719861 / run #1038 PASS
87 / 87 web test files; 422 / 422 web unit tests
317 modules / 1021 dependencies / 0 violations
Contracts / lint / typecheck / generated / build / diff / mutation / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

Detailed D4 authority: `world-focus-d4-contextual-invocation-review.md`.

## 4. Closed D4 result

D4 adds explicit bounded semantic context to the existing D1/D3 path:

```text
Continuity -> continue
Attention  -> why
Comparison -> compare
Evidence   -> open-source
-> finite WorldFocusContextReferenceSet
-> same D1 composer + editable seed
-> same D3 conversation
```

The global invoke remains explicitly `contextReferences: null`; generic Workspace selection is not inherited as DANTE context.

Context is bound to World + Workspace generation. A generation change before submit preserves the draft and fails closed; a generation change after a contextual session is established supersedes that session and rejects stale follow-up context.

Only actual Evidence receives `open-source`; Provenance, Integrity and History remain distinct.

No new Workspace/surface engine, provider/LLM call, persistence or backend semantics entered D4.

## 5. Permanent non-collapses

```text
World != Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
AI output != fact
Proposal != Decision != effect
Comparison != Decision
client composition config != canonical Domain state
presentation geometry != conversation identity
route presentation != automatically blocking interaction
context/selection != authorization
context reference != canonical truth
mounted frontend transcript != durable DANTE Run
cancelled/aborted request != semantic success
conversation message != Insight
Insight != Proposal != Decision != effect
```

## 6. D5 next gate

D5 is next and is **NOT STARTED**.

Before writes inspect live:

```text
D4 bounded contextual request/session ownership
D3 typed conversation/result ownership
registered World surfaces and finite renderer grammar
existing semantic owners that could support an Insight without inventing truth
reference/disclosure/basis qualifiers
responsive/a11y/browser harness
```

D5 must preserve:

```text
conversation message != Insight
assistant prose != validated Insight
Insight != canonical truth
Insight != Proposal != Decision != effect
context reference != authorization
```

Start D5 with a fresh PRE-SCOPE and explicit RED-first write gate. Do not pull D6 or backend/provider integration forward.

## 7. Visual sequence

```text
finish M4 -> structural visual check only
finish M5 -> serious product/visual review
M6 -> visual/responsive/motion/a11y/performance refinement
M7 -> pre-backend frontend freeze
```

Human/manual visual acceptance remains **NOT PERFORMED**.

## 8. Operational stop lines

```text
NO second DANTE surface/conversation state engine
NO D6 hidden inside D5
NO AppShell/GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO localStorage fake persistence
NO backend/API/DB/Alembic/AuthZ/provider/LLM before sequence permits it
NO arbitrary DOM/component payload serialization as DANTE context
NO Timeline/Access/Auth collateral work
NO claim of human visual acceptance from automated green
```
