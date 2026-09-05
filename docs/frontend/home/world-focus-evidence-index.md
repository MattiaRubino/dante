# DANTE — World Focus Research / Review Evidence Index

**Status:** CURRENT EVIDENCE MAP — M4 CLOSED / VALIDATED — MAIN RECONCILIATION NEXT  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`

This index separates live sequencing authority, closure authority, falsification and supporting evidence. Older phase-time status prose is historical unless adopted by current checkpoint authority.

## 1. Read first

```text
world-focus-current-checkpoint.md
world-focus-frontend-roadmap.md
world-focus-handoff.md
world-focus-evidence-index.md
current-checkpoint.md
world-focus-m4-final-hostile-closure-review.md
world-focus-d6-governed-operation-review.md
world-focus-d5-insight-presentation-review.md
world-focus-d4-contextual-invocation-review.md
world-focus-d3-deterministic-conversation-adapter-review.md
world-focus-d2-adaptive-conversation-surface-review.md
world-focus-m3-final-hostile-closure-review.md
world-focus-m3-adaptive-composition.md
world-focus-m3-4-integrated-adaptive-composition-review.md
world-focus-dante-spatial-presence-review.md
world-focus-d1-dante-entry-review.md
```

Protected-main Domain/Logical/Physical authority outranks frontend convenience whenever semantic boundaries are questioned.

## 2. Evidence families

```text
E0–E25   Workspace, product, substrate, M0–M2 historical evidence
E26      M3-1 composition configuration foundation
E27      M3-2 adaptive candidate resolver
E28      PRE-M3-3 customization reachability safety
E29      M3-3 Manual Customize UX + hostile closure
E30      M3-4 Integrated Adaptive Composition
E31      M3 final cross-layer hostile closure
E32      M4 / D2 adaptive conversation surface closure
E33      M4 / D3 deterministic conversation adapter closure
E34      M4 / D4 contextual/deictic invocation closure
E35      M4 / D5 Insight presentation closure
E36      M4 / D6 governed Proposal/Confirmation/Receipt closure
E37      M4 final cross-owner hostile sequencing closure
```

Key anchors:

```text
Workspace Platform   6c441335a75bb913af8da1eda569d8094d38a539 / CI 33549465793 PASS
M3 final hostile     d9c30a3c6148469b347754eab07dc2ade9be4c52 / CI 33951509083 PASS
D2 final             7b787766be83096e82eab1ac116b2704fae5f202 / CI 33958677991 PASS
D3 final             59c70af6005ee87918db7fe152c043699726e78c / CI 33963858340 PASS
D4 final             e8ab022b9b00b958235ac7d09e757b45227a4356 / CI 33967719861 PASS
D5 final             0873153d8b390b99c5b3aa024e0735c82a89660d / CI 33971615312 PASS
D6 first green       234eb159a5993db9b909880f58231a1e27cdefef / CI 33975428193 PASS
D6 owner-hardened    929c5ad7a056ff172a915e5070e7d72c936e692d / CI 33986493932 PASS
M4 final hostile     1b8ae1a3d953d85dcc14d513e512428d1f268c8d / CI 33990483780 PASS
```

## E31 — M3 Final Cross-Layer Hostile Closure

```text
PRE-SCOPE 2e69b1dd0bda25beaecbc5e5baa26f8720a76ff1
HOSTILE   d9c30a3c6148469b347754eab07dc2ade9be4c52
CI        33951509083 / run #944 PASS
80 / 80 web test files
391 / 391 web unit tests
300 modules / 899 dependencies / 0 architecture violations
```

Detailed review: `world-focus-m3-final-hostile-closure-review.md`.

## E32 — M4 / D2 Adaptive Conversation Surface — CLOSED / VALIDATED

```text
wide -> non-modal DANTE sidecar
compact/mobile -> route-owned DANTE focus
maximize/restore -> same conversation identity
```

Generic route presentation remains non-blocking; DANTE route-focus carries explicit `blocksWorkspaceInteraction=true`. Workspace host/allocator ownership was not duplicated.

```text
PRE-SCOPE 0a0a43ac06f93d986674f8521e521dcc05ea2c1e
CODE/TEST  7b787766be83096e82eab1ac116b2704fae5f202
CI         33958677991 / run #969 PASS
82 / 82 web test files
399 / 399 web unit tests
305 modules / 929 dependencies / 0 violations
```

Detailed review: `world-focus-d2-adaptive-conversation-surface-review.md`.

## E33 — M4 / D3 Deterministic Conversation Adapter — CLOSED / VALIDATED

D3 fills the D2 shell with deterministic typed mounted conversation behavior:

```text
D1 composer
-> same dante:conversation
-> typed World/generation/request correlation
-> deterministic local reader
-> finite validated answer | explanation or truthful technical state
```

Cancel, late completion, generation supersession, second-turn continuity and exact invoker focus return are executable. Mounted transcript remains frontend state, not durable DANTE Run state.

```text
PRE-SCOPE 57520cf0570bc2be875e7140d066e45ddd9080d5
CODE/TEST  59c70af6005ee87918db7fe152c043699726e78c
CI         33963858340 / run #1009 PASS
84 / 84 web test files
410 / 410 web unit tests
311 modules / 963 dependencies / 0 violations
```

Detailed review: `world-focus-d3-deterministic-conversation-adapter-review.md`.

## E34 — M4 / D4 Contextual / Deictic Invocation — CLOSED / VALIDATED

### E34.1 RED proof

```text
PRE-SCOPE c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
FIRST RED d017b17aec4b690a26781a88a17a372b0d670411
VALID RED 1cbcc27bf19c91e195dd1f0f4a5c57915facb432
RED CI    33966295853 / run #1030 EXPECTED FAILURE
```

The valid RED passed contracts/lint/typecheck/architecture/generated/Mobile and reached unit execution with exactly two intended failures: missing explicit request `contextReferences: null` and missing live Continuity contextual action. Existing D1 no-implicit-selection behavior remained green.

### E34.2 Bounded implementation

```text
Continuity -> continue
Attention  -> why
Comparison -> compare
Evidence   -> open-source
```

Only finite `WorldFocusContextReferenceSet` coordinates cross into the D3 request. Global DANTE invoke remains context-free. Arbitrary DOM/component/source payload is not serialized.

Contextual composer state is bound to World + Workspace generation. Stale-before-submit preserves the draft and fails closed. Valid follow-ups reuse the exact explicit reference set; a later generation change supersedes the contextual session and blocks stale follow-up context.

Only Evidence receives the source-opening action; Provenance, Integrity and History remain separate roles.

### E34.3 Hostile closure

```text
CODE/TEST e8ab022b9b00b958235ac7d09e757b45227a4356
CI        33967719861 / run #1038 PASS
87 / 87 web test files
422 / 422 web unit tests
317 modules / 1021 dependencies / 0 architecture violations
Frontend + World Focus contracts PASS
Lint / Typecheck / Generated / Build / Diff / Mutation PASS
Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

Real browser coverage uses `/worlds/music` Continuity at 1600 and 390. It proves seeded contextual composer, existing D3 conversation handoff, existing D2 sidecar/route focus, >=44px contextual target, no compact overflow, exact contextual invoker focus return and automated axe checks.

Detailed review: `world-focus-d4-contextual-invocation-review.md`.

## E35 — M4 / D5 Insight Presentation — CLOSED / VALIDATED

D5 materializes a standalone validated Insight rather than widening the D3 transcript.

```text
conversation answer | explanation
-> explicit Open as Insight
-> bounded request
-> deterministic Insight reader
-> observation | pattern | change artifact
-> registered dante-insight surface
```

```text
PRE-SCOPE 62b52137ab30778aae968f80fac59496c87171bf
VALID RED c803dac135c7a35d38d8eb8335f5b52c8b430114
RED CI    33969625586 / run #1045 EXPECTED FAILURE
CODE/TEST 0873153d8b390b99c5b3aa024e0735c82a89660d
CI        33971615312 / run #1050 PASS
89 / 89 web test files
431 / 431 web unit tests
324 modules / 1066 dependencies / 0 architecture violations
```

Global context-free DANTE cannot promote Insight. Basis references cannot widen. Pending/late Insight work fails closed on Workspace-generation change. Raw reference keys are not presented.

Detailed review: `world-focus-d5-insight-presentation-review.md`.

## E36 — M4 / D6 Governed Operation — CLOSED / VALIDATED

D6 materializes frontend-only governed-operation semantics:

```text
current validated D5 Insight
-> Proposal
-> required blocking Confirmation
-> local confirmed | declined Decision
-> truthful local Receipt
```

Permanent law:

```text
Insight != Proposal
Proposal != Decision
Decision != effect
confirmed != executed
Receipt != provider/runtime/canonical completion
```

RED/GREEN evidence:

```text
PRE-SCOPE        40dc630ba436317f89951e71c22172b2c3852558
VALID RED        fb1d002712bcd9b4c8c0c5a23156a13abb71303b
RED CI           33974791760 / run #1058 EXPECTED FAILURE
FIRST GREEN      234eb159a5993db9b909880f58231a1e27cdefef
GREEN CI         33975428193 / run #1061 PASS
OWNER-HARDENED   929c5ad7a056ff172a915e5070e7d72c936e692d
OWNER GREEN CI   33986493932 / run #1071 PASS
```

Confirmation blocks Workspace interaction and survives Escape. Receipt explicitly records no effect execution.

Detailed review: `world-focus-d6-governed-operation-review.md`.

## E37 — M4 Final Cross-Owner Hostile Sequencing Closure — CLOSED / PASS

The M4 closure did not rely on happy-path coverage. It found three real same-generation caller-injection seams.

### E37.1 D5 -> D6

```text
RED       775281b8bdca5dd5cccb63be5ecb6d9ebabd5b2d
RED CI    33985837951 / run #1066 EXPECTED FAILURE
GREEN     929c5ad7a056ff172a915e5070e7d72c936e692d
GREEN CI  33986493932 / run #1071 PASS
```

Fix: D6 derives exclusively the current D5-owned Insight; caller-supplied same-generation Insight substitution is not accepted.

### E37.2 D3 -> D5

```text
RED       bf6caef751505d35cbfd694ce6f1d532409517f3
RED CI    33987041073 / run #1076 EXPECTED FAILURE
GREEN     e8b836f49ddb85a95e0ba6b9472b56f3f45d83eb
GREEN CI  33987633070 / run #1080 PASS
```

Fix: D5 resolves the exact source assistant message from the D3 owner rather than trusting caller-supplied message content.

### E37.3 D4 -> D3

```text
RED       8dd3572652bde94778ee230cf80437fc8e22a1b8
RED CI    33988617249 / run #1085 EXPECTED FAILURE
GREEN     eccdc4d986a4880e9e45766900cb833b665d8cea
GREEN CI  33989942572 / run #1086 PASS
```

Fix: D3 derives the contextual reference seed from the D4 owner rather than accepting caller-supplied semantic context.

### E37.4 Final lifecycle matrix

```text
HEAD 1b8ae1a3d953d85dcc14d513e512428d1f268c8d
CI   33990483780 / run #1087 PASS
Quality PASS
Mobile Bundle PASS
Chromium Web E2E PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

Matrix coverage includes skip prevention, stale Proposal/Confirmation/Receipt invalidation, stale Decision rejection, owner binding, basis non-widening, global/context-free exclusion, Confirmation blocking/Escape behavior and truthful no-effect Receipt semantics.

Detailed review: `world-focus-m4-final-hostile-closure-review.md`.

## 3. Current layered result

```text
L0 Higher Authorities
L1 Work-Semantic Projections — M1
L2 Evidence/Basis
L3 Coordination/Disclosure
L4 Interaction/Reference
L5 Composition — M3 CLOSED / VALIDATED
L6 Operation/Effect presentation — D6 FRONTEND-ONLY GOVERNED PRESENTATION
L7 Renderer/Specialist Extension
L8 Platform/User Policy

M2 presentation boundary CLOSED
M3 Adaptive Composition CLOSED / VALIDATED
M4 Contextual DANTE CLOSED / VALIDATED
D2 Adaptive Conversation Surface CLOSED / VALIDATED
D3 Deterministic Conversation Adapter CLOSED / VALIDATED
D4 Contextual/Deictic Invocation CLOSED / VALIDATED
D5 Insight Presentation CLOSED / VALIDATED
D6 Governed Operation CLOSED / VALIDATED
M4 Final Hostile Closure CLOSED / PASS
M5 NOT STARTED
MAIN RECONCILIATION NEXT BEFORE M5
```

## 4. Current evidence gate

> **M1 — CLOSED / VALIDATED**

> **POST-M1 SAFETY — CLOSED / PASS**

> **M2 — CLOSED / VALIDATED**

> **M3 — CLOSED / VALIDATED**

> **M3 FINAL HOSTILE CLOSURE — CLOSED / PASS**

> **D2 — CLOSED / VALIDATED**

> **D3 — CLOSED / VALIDATED**

> **D4 — CLOSED / VALIDATED**

> **D5 — CLOSED / VALIDATED**

> **D6 — CLOSED / VALIDATED**

> **M4 FINAL HOSTILE CLOSURE — CLOSED / PASS**

> **M4 — CLOSED / VALIDATED**

> **M5 — NOT STARTED. Main reconciliation/integration is next.**

Human/manual visual acceptance remains **NOT PERFORMED**.
